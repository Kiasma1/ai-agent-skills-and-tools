import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { loadCatalog } from "../extensions/kiasma-skills-core.js";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const catalogPath = join(root, "catalog.json");

test("catalog is valid, unique, and contains only the 34 active installable skills", async () => {
	const catalog = await loadCatalog(catalogPath);
	assert.equal(catalog.skills.length, 34);
	assert.equal(new Set(catalog.skills.map((skill) => skill.name)).size, 34);
	assert.ok(catalog.skills.every((skill) => skill.enabled));

	const names = new Set(catalog.skills.map((skill) => skill.name));
	for (const excluded of ["dataviz", "brainstorming", "writing-plans", "codegraph", "caveman", "ponytail"]) {
		assert.equal(names.has(excluded), false, `${excluded} must not be in the default install set`);
	}
});

test("catalog contains the path-specific leader, minimal-diff, and Chinese liquid glass sources", async () => {
	const catalog = await loadCatalog(catalogPath);
	const byName = new Map(catalog.skills.map((skill) => [skill.name, skill]));
	assert.deepEqual(
		{
			source: byName.get("leader")?.source,
			path: byName.get("leader")?.path,
		},
		{
			source: "KKKKhazix/khazix-skills",
			path: "leader/SKILL.md",
		},
	);
	assert.equal(
		byName.get("liquid-glass-design")?.installSource,
		"https://github.com/affaan-m/ECC/tree/main/docs/zh-CN/skills/liquid-glass-design",
	);
	assert.deepEqual(
		{
			source: byName.get("minimal-diff")?.source,
			path: byName.get("minimal-diff")?.path,
			installSource: byName.get("minimal-diff")?.installSource,
		},
		{
			source: "dhruvinrsoni/agentskills-garden",
			path: "skills/100-engineering/25-pragmatism/minimal-diff/SKILL.md",
			installSource:
				"https://github.com/dhruvinrsoni/agentskills-garden/tree/main/skills/100-engineering/25-pragmatism/minimal-diff",
		},
	);
	assert.deepEqual(
		{
			source: byName.get("research")?.source,
			path: byName.get("research")?.path,
		},
		{
			source: "mattpocock/skills",
			path: "skills/engineering/research/SKILL.md",
		},
	);
});

test("package manifest exposes only the intended Pi extension", async () => {
	const packageJson = JSON.parse(await readFile(join(root, "package.json"), "utf8"));
	assert.ok(packageJson.keywords.includes("pi-package"));
	assert.deepEqual(packageJson.pi, { extensions: ["extensions/kiasma-skills.ts"] });
	assert.equal(packageJson.peerDependencies["@earendil-works/pi-coding-agent"], "*");
	assert.equal(packageJson.peerDependencies.typebox, "*");
});
