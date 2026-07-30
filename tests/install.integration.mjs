import assert from "node:assert/strict";
import { mkdtemp, readdir, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { spawn } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";
import {
	inspectStatus,
	loadCatalog,
	mutationHasFailures,
	runInstallAll,
	runSync,
} from "../extensions/kiasma-skills-core.js";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const catalog = await loadCatalog(join(root, "catalog.json"));

function createExec(homeDirectory) {
	return async (command, args, options) =>
		new Promise((resolve, reject) => {
			const child = spawn(command, args, {
				shell: process.platform === "win32",
				env: {
					...process.env,
					HOME: homeDirectory,
					USERPROFILE: homeDirectory,
				},
			});
			let stdout = "";
			let stderr = "";
			child.stdout?.on("data", (chunk) => {
				stdout = (stdout + chunk).slice(-100_000);
			});
			child.stderr?.on("data", (chunk) => {
				stderr = (stderr + chunk).slice(-100_000);
			});
			const timeout = setTimeout(() => {
				child.kill();
				reject(new Error(`Timed out: ${command} ${args.join(" ")}`));
			}, options.timeout);
			child.on("error", (error) => {
				clearTimeout(timeout);
				reject(error);
			});
			child.on("close", (code) => {
				clearTimeout(timeout);
				resolve({ code: code ?? 1, stdout, stderr });
			});
		});
}

async function installedDirectoryNames(homeDirectory) {
	return (await readdir(join(homeDirectory, ".agents", "skills"))).sort();
}

test("all catalog skills install, reinstall idempotently, and sync in an isolated home", { timeout: 30 * 60 * 1000 }, async () => {
	const home = await mkdtemp(join(tmpdir(), "kiasma-skills-integration-"));
	const exec = createExec(home);
	try {
		const first = await runInstallAll(catalog, exec, { timeout: 10 * 60 * 1000 });
		assert.equal(mutationHasFailures(first), false, JSON.stringify(first, null, 2));
		const firstStatus = await inspectStatus(catalog, { homeDirectory: home });
		assert.equal(firstStatus.entries.every((entry) => entry.state === "installed"), true, JSON.stringify(firstStatus, null, 2));
		assert.equal(firstStatus.duplicates.length, 0);

		const directoriesBefore = await installedDirectoryNames(home);
		const second = await runInstallAll(catalog, exec, { timeout: 10 * 60 * 1000 });
		assert.equal(mutationHasFailures(second), false, JSON.stringify(second, null, 2));
		assert.deepEqual(await installedDirectoryNames(home), directoriesBefore);

		const sync = await runSync(catalog, exec, { timeout: 10 * 60 * 1000 });
		assert.equal(mutationHasFailures(sync), false, JSON.stringify(sync, null, 2));
		const finalStatus = await inspectStatus(catalog, { homeDirectory: home });
		assert.equal(finalStatus.entries.every((entry) => entry.state === "installed"), true, JSON.stringify(finalStatus, null, 2));
	} finally {
		await rm(home, { recursive: true, force: true });
	}
});
