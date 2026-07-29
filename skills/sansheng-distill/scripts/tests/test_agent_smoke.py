# agent_smoke.py 测试 -- 假 repo 布局程序化构造;manifest 读取健壮性 + cli_command shim 分支
import importlib.util
import json
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "agent_smoke.py"


def _load():
    spec = importlib.util.spec_from_file_location("agent_smoke", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


sm = _load()
PLUGIN = sm.PLUGIN_NAME


def make_repo(tmp_path, with_codex=True):
    """造一个最小假 repo 布局;with_codex=False 时缺 .codex-plugin/plugin.json。"""
    skill = tmp_path / "skills" / PLUGIN
    (skill / "references").mkdir(parents=True)
    (skill / "scripts").mkdir()
    (skill / "templates").mkdir()
    (skill / "agents").mkdir()
    (skill / "SKILL.md").write_text("# x", encoding="utf-8")
    (skill / "agents" / "openai.yaml").write_text("x", encoding="utf-8")
    claude_dir = tmp_path / ".claude-plugin"; claude_dir.mkdir()
    (claude_dir / "plugin.json").write_text(
        json.dumps({"name": PLUGIN, "version": "1.0.0"}), encoding="utf-8")
    (claude_dir / "marketplace.json").write_text(
        json.dumps({"plugins": [{"name": PLUGIN, "version": "1.0.0"}]}), encoding="utf-8")
    if with_codex:
        codex_dir = tmp_path / ".codex-plugin"; codex_dir.mkdir()
        (codex_dir / "plugin.json").write_text(
            json.dumps({"name": PLUGIN, "version": "1.0.0", "skills": "./skills/"}),
            encoding="utf-8")
    return tmp_path


# --- validate_layout:布局齐 -> 全过 ---
def test_validate_layout_all_present_passes(tmp_path):
    checks = sm.validate_layout(make_repo(tmp_path))
    assert all(checks.values())

# --- validate_layout:缺 manifest -> 记失败检查项返回,不抛异常(原来 read_text 裸栈) ---
def test_validate_layout_missing_manifest_records_failed_check(tmp_path):
    checks = sm.validate_layout(make_repo(tmp_path, with_codex=False))
    assert checks["codex_manifest"] is False
    assert checks["codex_name"] is False
    assert not all(checks.values())

# --- validate_layout:manifest 损坏 -> 同样记失败检查项,不抛异常 ---
def test_validate_layout_corrupt_manifest_records_failed_check(tmp_path):
    root = make_repo(tmp_path)
    (root / ".claude-plugin" / "marketplace.json").write_text("{ 损坏", encoding="utf-8")
    checks = sm.validate_layout(root)
    assert checks["marketplace_manifest"] is False
    assert not all(checks.values())

# --- cli_command shim 分支(纯函数,monkeypatch which) ---
def test_cli_command_not_found_returns_none(monkeypatch):
    monkeypatch.setattr(sm.shutil, "which", lambda name: None)
    assert sm.cli_command("claude", "plugin") is None


def test_cli_command_ps1_shim(monkeypatch):
    exe = "C:\\tools\\claude.ps1"
    monkeypatch.setattr(sm.shutil, "which", lambda name: exe)
    cmd = sm.cli_command("claude", "plugin", "validate")
    assert cmd[0] == "powershell.exe" and "-File" in cmd
    assert cmd[-3:] == [exe, "plugin", "validate"]


def test_cli_command_cmd_shim(monkeypatch):
    exe = "C:\\tools\\claude.cmd"
    monkeypatch.setattr(sm.shutil, "which", lambda name: exe)
    cmd = sm.cli_command("claude", "plugin", "validate")
    assert cmd[:4] == ["cmd.exe", "/d", "/s", "/c"]
    assert cmd[4] == sm.subprocess.list2cmdline([exe, "plugin", "validate"])


def test_cli_command_plain_executable(monkeypatch):
    monkeypatch.setattr(sm.shutil, "which", lambda name: "/usr/local/bin/claude")
    assert sm.cli_command("claude", "--version") == ["/usr/local/bin/claude", "--version"]
