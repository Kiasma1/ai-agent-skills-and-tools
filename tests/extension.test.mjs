import assert from "node:assert/strict";
import test from "node:test";
import extension from "../extensions/kiasma-skills.ts";

function loadExtension() {
	const commands = new Map();
	const tools = new Map();
	let execCalls = 0;
	const pi = {
		registerCommand(name, command) {
			commands.set(name, command);
		},
		registerTool(tool) {
			tools.set(tool.name, tool);
		},
		async exec() {
			execCalls++;
			return { code: 0, stdout: "", stderr: "" };
		},
		sendUserMessage() {},
	};
	extension(pi);
	return { commands, tools, getExecCalls: () => execCalls };
}

test("extension registers the public command, reload command, and LLM tool", () => {
	const { commands, tools } = loadExtension();
	assert.deepEqual([...commands.keys()], ["kiasma-skills-reload", "kiasma-skills"]);
	assert.deepEqual([...tools.keys()], ["kiasma_skills"]);
	assert.deepEqual(
		commands.get("kiasma-skills").getArgumentCompletions("s").map((item) => item.value),
		["sync", "status"],
	);
});

test("non-interactive mutation is rejected before npx or confirmation", async () => {
	const { tools, getExecCalls } = loadExtension();
	let confirmCalls = 0;
	const ctx = {
		mode: "print",
		hasUI: false,
		signal: undefined,
		ui: {
			async confirm() {
				confirmCalls++;
				return true;
			},
			setStatus() {},
		},
	};
	await assert.rejects(
		() => tools.get("kiasma_skills").execute("test", { action: "install-all" }, undefined, undefined, ctx),
		/只允许在交互式 Pi TUI 中执行/,
	);
	assert.equal(confirmCalls, 0);
	assert.equal(getExecCalls(), 0);
});
