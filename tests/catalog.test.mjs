import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { loadCatalog } from "../extensions/kiasma-skills-core.js";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const catalogPath = join(root, "catalog.json");

test("catalog is valid, unique, and contains only the 32 active installable skills", async () => {
	const catalog = await loadCatalog(catalogPath);
	assert.equal(catalog.skills.length, 32);
	assert.equal(new Set(catalog.skills.map((skill) => skill.name)).size, 32);
	assert.ok(catalog.skills.every((skill) => skill.enabled));

	const names = new Set(catalog.skills.map((skill) => skill.name));
	for (const excluded of ["dataviz", "brainstorming", "writing-plans", "codegraph", "caveman", "ponytail"]) {
		assert.equal(names.has(excluded), false, `${excluded} must not be in the default install set`);
	}
});

test("catalog contains the path-specific leader and Chinese liquid glass sources", async () => {
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
});

test("package manifest exposes only the intended Pi extension", async () => {
	const packageJson = JSON.parse(await readFile(join(root, "package.json"), "utf8"));
	assert.ok(packageJson.keywords.includes("pi-package"));
	assert.deepEqual(packageJson.pi, { extensions: ["extensions/kiasma-skills.ts"] });
	assert.equal(packageJson.peerDependencies["@earendil-works/pi-coding-agent"], "*");
	assert.equal(packageJson.peerDependencies.typebox, "*");
});
