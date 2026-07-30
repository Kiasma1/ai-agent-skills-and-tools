import { readFile, readdir, realpath, stat } from "node:fs/promises";
import { homedir } from "node:os";
import { join, normalize, resolve } from "node:path";

const SKILL_NAME_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const GITHUB_SOURCE_PATTERN = /^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/;
const DEFAULT_TIMEOUT_MS = 5 * 60 * 1000;

function assert(condition, message) {
	if (!condition) throw new Error(`Invalid catalog: ${message}`);
}

function normalizeSkillPath(path) {
	return path.replaceAll("\\", "/").replace(/^\.\//, "");
}

export function normalizeSource(source) {
	if (typeof source !== "string") return undefined;
	const normalized = source
		.trim()
		.replace(/^git:/, "")
		.replace(/^https?:\/\/github\.com\//i, "")
		.replace(/^git@github\.com:/i, "")
		.replace(/\.git$/i, "")
		.replace(/\/$/, "");
	return normalized.split("/").slice(0, 2).join("/").toLowerCase();
}

export function validateCatalog(value) {
	assert(value && typeof value === "object" && !Array.isArray(value), "root must be an object");
	assert(value.version === 1, "version must be 1");
	assert(Array.isArray(value.skills), "skills must be an array");

	const names = new Set();
	for (const [index, skill] of value.skills.entries()) {
		const at = `skills[${index}]`;
		assert(skill && typeof skill === "object" && !Array.isArray(skill), `${at} must be an object`);
		assert(typeof skill.name === "string" && SKILL_NAME_PATTERN.test(skill.name), `${at}.name is invalid`);
		assert(!names.has(skill.name), `duplicate skill name ${skill.name}`);
		names.add(skill.name);
		assert(typeof skill.source === "string" && GITHUB_SOURCE_PATTERN.test(skill.source), `${at}.source is invalid`);
		assert(typeof skill.path === "string" && skill.path.length > 0, `${at}.path is required`);
		const normalizedPath = normalizeSkillPath(skill.path);
		assert(!normalizedPath.startsWith("/") && !normalizedPath.split("/").includes(".."), `${at}.path must stay inside its repository`);
		assert(normalizedPath === "SKILL.md" || normalizedPath.endsWith("/SKILL.md"), `${at}.path must point to SKILL.md`);
		assert(typeof skill.group === "string" && skill.group.length > 0, `${at}.group is required`);
		assert(typeof skill.enabled === "boolean", `${at}.enabled must be boolean`);
		if (skill.installSource !== undefined) {
			assert(
				typeof skill.installSource === "string" && /^https:\/\/github\.com\//i.test(skill.installSource),
				`${at}.installSource must be a GitHub URL`,
			);
			assert(normalizeSource(skill.installSource) === normalizeSource(skill.source), `${at}.installSource must match source`);
		}
	}

	return value;
}

export async function loadCatalog(catalogPath) {
	const text = await readFile(catalogPath, "utf8");
	return validateCatalog(JSON.parse(text));
}

export function enabledSkills(catalog) {
	return catalog.skills.filter((skill) => skill.enabled);
}

export function groupInstallUnits(catalog) {
	const units = new Map();
	for (const skill of enabledSkills(catalog)) {
		const installTarget = skill.installSource ?? skill.source;
		const key = `${skill.source}\0${installTarget}`;
		let unit = units.get(key);
		if (!unit) {
			unit = { source: skill.source, installTarget, skills: [] };
			units.set(key, unit);
		}
		unit.skills.push(skill);
	}
	return [...units.values()];
}

export function buildInstallArgs(unit) {
	return [
		"--yes",
		"skills",
		"add",
		unit.installTarget,
		"--global",
		"--agent",
		"codex",
		"--yes",
		"--full-depth",
		"--skill",
		...unit.skills.map((skill) => skill.name),
	];
}

export function buildUpdateArgs() {
	return ["--yes", "skills", "update", "--global", "--yes"];
}

async function executeStep(exec, label, command, args, timeout) {
	try {
		const result = await exec(command, args, { timeout });
		return {
			label,
			command,
			args,
			ok: result.code === 0,
			code: result.code,
			stdout: result.stdout ?? "",
			stderr: result.stderr ?? "",
		};
	} catch (error) {
		return {
			label,
			command,
			args,
			ok: false,
			code: undefined,
			stdout: "",
			stderr: error instanceof Error ? error.message : String(error),
		};
	}
}

export async function runInstallAll(catalog, exec, options = {}) {
	const outcomes = [];
	for (const unit of groupInstallUnits(catalog)) {
		const outcome = await executeStep(
			exec,
			unit.source,
			"npx",
			buildInstallArgs(unit),
			options.timeout ?? DEFAULT_TIMEOUT_MS,
		);
		outcomes.push({ ...outcome, skills: unit.skills.map((skill) => skill.name) });
	}
	return {
		action: "install-all",
		outcomes,
		skipped: catalog.skills.filter((skill) => !skill.enabled).map((skill) => skill.name),
	};
}

export async function runSync(catalog, exec, options = {}) {
	const timeout = options.timeout ?? DEFAULT_TIMEOUT_MS;
	const update = await executeStep(exec, "global skill update", "npx", buildUpdateArgs(), timeout);
	const install = await runInstallAll(catalog, exec, { timeout });
	return {
		action: "sync",
		update,
		outcomes: install.outcomes,
		skipped: install.skipped,
	};
}

function parseFrontmatterName(text) {
	const frontmatter = /^---\s*\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(text)?.[1];
	if (!frontmatter) return undefined;
	return /^name:\s*["']?([^\r\n"']+)["']?\s*$/m.exec(frontmatter)?.[1]?.trim();
}

async function collectSkillFiles(directory, files, visited) {
	let canonical;
	try {
		canonical = await realpath(directory);
	} catch {
		return;
	}
	const visitKey = process.platform === "win32" ? canonical.toLowerCase() : canonical;
	if (visited.has(visitKey)) return;
	visited.add(visitKey);

	let entries;
	try {
		entries = await readdir(directory, { withFileTypes: true });
	} catch {
		return;
	}

	const skillFile = entries.find((entry) => entry.isFile() && entry.name === "SKILL.md");
	if (skillFile) {
		files.push(join(directory, skillFile.name));
		return;
	}

	for (const entry of entries) {
		if (entry.name === ".git" || entry.name === "node_modules") continue;
		const path = join(directory, entry.name);
		if (entry.isDirectory()) {
			await collectSkillFiles(path, files, visited);
			continue;
		}
		if (entry.isSymbolicLink()) {
			try {
				if ((await stat(path)).isDirectory()) await collectSkillFiles(path, files, visited);
			} catch {
				// Broken links are reported as missing through the catalog comparison.
			}
		}
	}
}

async function scanInstalledSkills(skillsDirectory) {
	const files = [];
	await collectSkillFiles(skillsDirectory, files, new Set());
	const byName = new Map();
	for (const path of files) {
		let name;
		try {
			name = parseFrontmatterName(await readFile(path, "utf8"));
		} catch {
			continue;
		}
		if (!name) continue;
		const paths = byName.get(name) ?? [];
		paths.push(path);
		byName.set(name, paths);
	}
	return byName;
}

async function readLock(lockPath) {
	try {
		const value = JSON.parse(await readFile(lockPath, "utf8"));
		return value && typeof value === "object" && value.skills && typeof value.skills === "object"
			? value.skills
			: {};
	} catch {
		return {};
	}
}

export async function inspectStatus(catalog, options = {}) {
	const homeDirectory = resolve(options.homeDirectory ?? homedir());
	const agentsDirectory = join(homeDirectory, ".agents");
	const skillsDirectory = join(agentsDirectory, "skills");
	const lockPath = join(agentsDirectory, ".skill-lock.json");
	const [installedByName, lock] = await Promise.all([
		scanInstalledSkills(skillsDirectory),
		readLock(lockPath),
	]);

	const entries = enabledSkills(catalog).map((skill) => {
		const installedPaths = installedByName.get(skill.name) ?? [];
		const lockEntry = lock[skill.name];
		const sourceMismatch = Boolean(
			lockEntry && normalizeSource(lockEntry.source ?? lockEntry.sourceUrl) !== normalizeSource(skill.source),
		);
		const pathMismatch = Boolean(
			lockEntry?.skillPath && normalizeSkillPath(lockEntry.skillPath) !== normalizeSkillPath(skill.path),
		);
		let state = "installed";
		if (installedPaths.length === 0) state = "missing";
		else if (installedPaths.length > 1) state = "duplicate";
		else if (sourceMismatch) state = "source-mismatch";
		else if (pathMismatch) state = "path-mismatch";
		else if (!lockEntry) state = "installed-untracked";
		return {
			...skill,
			state,
			installedPaths,
			lockEntry,
		};
	});

	const duplicates = [...installedByName.entries()]
		.filter(([, paths]) => paths.length > 1)
		.map(([name, paths]) => ({ name, paths }));

	return {
		homeDirectory,
		skillsDirectory,
		lockPath,
		entries,
		duplicates,
		counts: Object.fromEntries(
			["installed", "installed-untracked", "missing", "duplicate", "source-mismatch", "path-mismatch"].map(
				(state) => [state, entries.filter((entry) => entry.state === state).length],
			),
		),
	};
}

const STATE_SYMBOLS = {
	installed: "✓",
	"installed-untracked": "?",
	missing: "○",
	duplicate: "!",
	"source-mismatch": "!",
	"path-mismatch": "!",
};

export function formatList(catalog, status) {
	const statusByName = new Map(status.entries.map((entry) => [entry.name, entry.state]));
	const lines = [`Kiasma 默认安装集合：${enabledSkills(catalog).length} Skills`];
	let currentGroup;
	for (const skill of enabledSkills(catalog)) {
		if (skill.group !== currentGroup) {
			currentGroup = skill.group;
			lines.push(`\n[${currentGroup}]`);
		}
		const state = statusByName.get(skill.name) ?? "missing";
		lines.push(`${STATE_SYMBOLS[state]} ${skill.name} — ${skill.source}:${skill.path}`);
	}
	return lines.join("\n");
}

export function formatStatus(status) {
	const { counts } = status;
	const lines = [
		`Kiasma Skill 状态：${status.entries.length} 项`,
		`已安装 ${counts.installed}｜未追踪 ${counts["installed-untracked"]}｜缺失 ${counts.missing}｜异常 ${counts.duplicate + counts["source-mismatch"] + counts["path-mismatch"]}`,
	];
	for (const entry of status.entries) {
		lines.push(`${STATE_SYMBOLS[entry.state]} ${entry.name}: ${entry.state}`);
		if (entry.state === "source-mismatch") {
			lines.push(`  expected ${entry.source}; locked ${entry.lockEntry?.source ?? entry.lockEntry?.sourceUrl ?? "unknown"}`);
		}
		if (entry.state === "path-mismatch") {
			lines.push(`  expected ${entry.path}; locked ${entry.lockEntry?.skillPath ?? "unknown"}`);
		}
		if (entry.state === "duplicate") {
			for (const path of entry.installedPaths) lines.push(`  ${path}`);
		}
	}
	return lines.join("\n");
}

function conciseFailure(outcome) {
	const output = (outcome.stderr || outcome.stdout || `exit code ${outcome.code ?? "unknown"}`).trim();
	return output.length > 600 ? `…${output.slice(-600)}` : output;
}

export function mutationHasFailures(report) {
	return Boolean((report.update && !report.update.ok) || report.outcomes.some((outcome) => !outcome.ok));
}

export function mutationChanged(report) {
	return Boolean((report.update && report.update.ok) || report.outcomes.some((outcome) => outcome.ok));
}

export function formatMutationReport(report) {
	const succeeded = report.outcomes.filter((outcome) => outcome.ok);
	const failed = report.outcomes.filter((outcome) => !outcome.ok);
	const succeededSkills = succeeded.flatMap((outcome) => outcome.skills);
	const failedSkills = failed.flatMap((outcome) => outcome.skills);
	const lines = [
		`${report.action === "sync" ? "同步" : "安装"}完成：${succeededSkills.length} 成功，${report.skipped.length} 跳过，${failedSkills.length} 失败。`,
	];
	if (report.update) {
		lines.push(`全局更新：${report.update.ok ? "成功" : `失败 — ${conciseFailure(report.update)}`}`);
	}
	if (succeededSkills.length > 0) lines.push(`成功：${succeededSkills.join(", ")}`);
	if (report.skipped.length > 0) lines.push(`跳过：${report.skipped.join(", ")}`);
	for (const outcome of failed) {
		lines.push(`失败 ${outcome.label} (${outcome.skills.join(", ")}): ${conciseFailure(outcome)}`);
	}
	return lines.join("\n");
}

export function isInteractiveMutationAllowed(mode) {
	return mode === "tui";
}

export function resolveCatalogPath(extensionUrl) {
	const extensionPath = new URL(extensionUrl).pathname;
	const decoded = decodeURIComponent(extensionPath);
	const windowsPath = /^\/[A-Za-z]:\//.test(decoded) ? decoded.slice(1) : decoded;
	return normalize(resolve(windowsPath, "..", "..", "catalog.json"));
}
