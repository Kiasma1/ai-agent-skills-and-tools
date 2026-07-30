import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";
import { StringEnum } from "@earendil-works/pi-ai";
import { Type } from "typebox";
import {
	enabledSkills,
	formatList,
	formatMutationReport,
	formatStatus,
	groupInstallUnits,
	inspectStatus,
	isInteractiveMutationAllowed,
	loadCatalog,
	mutationChanged,
	mutationHasFailures,
	resolveCatalogPath,
	runInstallAll,
	runSync,
} from "./kiasma-skills-core.js";

const ACTIONS = ["list", "install-all", "sync", "status"] as const;
type Action = (typeof ACTIONS)[number];

interface ProgressUpdate {
	(content: { content: Array<{ type: "text"; text: string }>; details: Record<string, never> }): void;
}

export default function kiasmaSkills(pi: ExtensionAPI) {
	const catalogPath = resolveCatalogPath(import.meta.url);

	async function readCatalog() {
		return loadCatalog(catalogPath);
	}

	function actionFromText(text: string): Action | undefined {
		const value = (text.trim() || "status") as Action;
		return ACTIONS.includes(value) ? value : undefined;
	}

	async function runAction(
		action: Action,
		ctx: ExtensionContext,
		onUpdate?: ProgressUpdate,
	) {
		const catalog = await readCatalog();
		if (action === "list") {
			return {
				text: formatList(catalog, await inspectStatus(catalog)),
				changed: false,
				failed: false,
			};
		}
		if (action === "status") {
			return {
				text: formatStatus(await inspectStatus(catalog)),
				changed: false,
				failed: false,
			};
		}

		if (!isInteractiveMutationAllowed(ctx.mode)) {
			throw new Error("install-all 和 sync 只允许在交互式 Pi TUI 中执行");
		}

		const units = groupInstallUnits(catalog);
		const sourceLines = units.map((unit) => `• ${unit.source}: ${unit.skills.length} Skills`);
		const confirmed = await ctx.ui.confirm(
			action === "sync" ? "同步 Kiasma Skills？" : "安装全部 Kiasma Skills？",
			[
				`将处理 ${enabledSkills(catalog).length} 个 Skills，来源 ${units.length} 组：`,
				...sourceLines,
				"",
				"目标：~/.agents/skills",
				"策略：跟随各上游最新版；不会删除清单之外的 Skill。",
				"第三方 Skill 可能包含可执行脚本，请仅在信任这些来源时继续。",
			].join("\n"),
		);
		if (!confirmed) {
			return { text: "已取消。", changed: false, failed: false, cancelled: true };
		}

		ctx.ui.setStatus("kiasma-skills", action === "sync" ? "同步 Kiasma Skills…" : "安装 Kiasma Skills…");
		onUpdate?.({
			content: [{ type: "text", text: action === "sync" ? "正在同步 Kiasma Skills…" : "正在安装 Kiasma Skills…" }],
			details: {},
		});

		const exec = (command: string, args: string[], options: { timeout: number }) =>
			pi.exec(command, args, { signal: ctx.signal, timeout: options.timeout });

		try {
			const report = action === "sync" ? await runSync(catalog, exec) : await runInstallAll(catalog, exec);
			return {
				text: formatMutationReport(report),
				changed: mutationChanged(report),
				failed: mutationHasFailures(report),
			};
		} finally {
			ctx.ui.setStatus("kiasma-skills", undefined);
		}
	}

	pi.registerCommand("kiasma-skills-reload", {
		description: "Reload Pi after Kiasma Skill changes",
		handler: async (_args, ctx) => {
			await ctx.reload();
			return;
		},
	});

	pi.registerCommand("kiasma-skills", {
		description: "List, install, sync, or inspect Kiasma's curated Skills",
		getArgumentCompletions: (prefix) => {
			const items = ACTIONS.filter((action) => action.startsWith(prefix)).map((action) => ({
				value: action,
				label: action,
			}));
			return items.length > 0 ? items : null;
		},
		handler: async (args, ctx) => {
			const action = actionFromText(args);
			if (!action) {
				ctx.ui.notify(`未知操作：${args.trim()}。可用：${ACTIONS.join(", ")}`, "error");
				return;
			}
			try {
				const result = await runAction(action, ctx);
				ctx.ui.notify(result.text, result.failed ? "error" : "info");
				if (result.changed) {
					await ctx.reload();
					return;
				}
			} catch (error) {
				ctx.ui.notify(error instanceof Error ? error.message : String(error), "error");
			}
		},
	});

	pi.registerTool({
		name: "kiasma_skills",
		label: "Kiasma Skills",
		description: "List, install, sync, or inspect the curated active Skills in the Kiasma catalog",
		promptSnippet: "Manage the curated Kiasma Agent Skills catalog",
		promptGuidelines: [
			"Use kiasma_skills only for the fixed Kiasma catalog; require the tool's user confirmation before installing or syncing third-party Skills.",
		],
		parameters: Type.Object({
			action: StringEnum(ACTIONS),
		}),
		async execute(_toolCallId, params, _signal, onUpdate, ctx) {
			const result = await runAction(params.action, ctx, onUpdate);
			if (result.changed) {
				pi.sendUserMessage("/kiasma-skills-reload", { deliverAs: "followUp" });
			}
			if (result.failed) throw new Error(result.text);
			return {
				content: [{ type: "text", text: result.text }],
				details: { action: params.action, changed: result.changed },
			};
		},
	});
}
