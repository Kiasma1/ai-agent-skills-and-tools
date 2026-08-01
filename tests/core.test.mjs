import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import {
	buildInstallArgs,
	formatMutationReport,
	groupInstallUnits,
	inspectStatus,
	isInteractiveMutationAllowed,
	loadCatalog,
	mutationHasFailures,
	runInstallAll,
	runSync,
} from "../extensions/kiasma-skills-core.js";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const catalog = await loadCatalog(join(root, "catalog.json"));

async function withTempHome(run) {
	const home = await mkdtemp(join(tmpdir(), "kiasma-skills-test-"));
	try {
		await run(home);
	} finally {
		await rm(home, { recursive: true, force: true });
	}
}

async function writeSkill(home, directoryName, frontmatterName) {
	const directory = join(home, ".agents", "skills", directoryName);
	await mkdir(directory, { recursive: true });
	await writeFile(
		join(directory, "SKILL.md"),
		`---\nname: ${frontmatterName}\ndescription: test\n---\n`,
		"utf8",
	);
}

test("install units group normal repositories but preserve path-scoped sources", () => {
	const units = groupInstallUnits(catalog);
	const matt = units.find((unit) => unit.source === "mattpocock/skills");
	assert.equal(matt.skills.length, 14);
	assert.ok(buildInstallArgs(matt).includes("--full-depth"));
	assert.deepEqual(buildInstallArgs(matt).slice(-14), matt.skills.map((skill) => skill.name));

	const liquidGlass = units.find((unit) => unit.source === "affaan-m/ECC");
	assert.equal(
		liquidGlass.installTarget,
		"https://github.com/affaan-m/ECC/tree/main/docs/zh-CN/skills/liquid-glass-design",
	);
});

test("install-all records partial failures without rolling back successful sources", async () => {
	let calls = 0;
	const report = await runInstallAll(catalog, async (_command, args) => {
		calls++;
		const source = args[3];
		return source.includes("emilkowalski")
			? { code: 1, stdout: "", stderr: "simulated failure" }
			: { code: 0, stdout: "ok", stderr: "" };
	});
	assert.equal(calls, groupInstallUnits(catalog).length);
	assert.equal(report.outcomes.filter((outcome) => !outcome.ok).length, 1);
	assert.equal(mutationHasFailures(report), true);
	assert.match(formatMutationReport(report), /simulated failure/);
});

test("missing npx and timeouts become explicit per-source failures", async () => {
	const report = await runInstallAll(catalog, async () => {
		throw new Error("spawn npx ENOENT");
	});
	assert.ok(report.outcomes.every((outcome) => !outcome.ok));
	assert.match(formatMutationReport(report), /spawn npx ENOENT/);
});

test("sync attempts catalog reconciliation even when the global update fails", async () => {
	let calls = 0;
	const report = await runSync(catalog, async (_command, args) => {
		calls++;
		if (args[1] === "skills" && args[2] === "update") return { code: 1, stdout: "", stderr: "update failed" };
		return { code: 0, stdout: "ok", stderr: "" };
	});
	assert.equal(report.update.ok, false);
	assert.equal(report.outcomes.every((outcome) => outcome.ok), true);
	assert.equal(calls, groupInstallUnits(catalog).length + 1);
});

test("status is read-only and reports missing, source mismatch, untracked, and duplicates", async () => {
	await withTempHome(async (home) => {
		await writeSkill(home, "lzc-explain-words", "lzc-explain-words");
		await writeSkill(home, "lxgw-screen-typography", "lxgw-screen-typography");
		await writeSkill(home, "lxgw-copy", "lxgw-screen-typography");
		await writeSkill(home, "understand-learn", "understand-learn");
		await writeSkill(home, "huashu-nuwa", "huashu-nuwa");
		await writeSkill(home, "huashu-nuwa/examples/steve-jobs-perspective", "steve-jobs-perspective");

		const lockPath = join(home, ".agents", ".skill-lock.json");
		await writeFile(
			lockPath,
			JSON.stringify({
				version: 3,
				skills: {
					"lzc-explain-words": {
						source: "someone-else/repo",
						skillPath: "SKILL.md",
					},
					"lxgw-screen-typography": {
						source: "Kiasma1/lxgw-screen-typography",
						skillPath: "SKILL.md",
					},
				},
			}),
			"utf8",
		);

		const before = await readFile(lockPath, "utf8");
		const report = await inspectStatus(catalog, { homeDirectory: home });
		const state = new Map(report.entries.map((entry) => [entry.name, entry.state]));
		assert.equal(state.get("lzc-explain-words"), "source-mismatch");
		assert.equal(state.get("lxgw-screen-typography"), "duplicate");
		assert.equal(state.get("understand-learn"), "installed-untracked");
		assert.equal(state.get("huashu-nuwa"), "installed-untracked");
		assert.equal(state.get("steve-jobs-perspective"), "missing");
		assert.equal(state.get("youtube-bilibili-bilingual"), "missing");
		assert.equal(await readFile(lockPath, "utf8"), before);
	});
});

test("mutations require TUI mode", () => {
	assert.equal(isInteractiveMutationAllowed("tui"), true);
	for (const mode of ["print", "json", "rpc"]) assert.equal(isInteractiveMutationAllowed(mode), false);
});
