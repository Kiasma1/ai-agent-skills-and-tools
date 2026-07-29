# build_author.py 测试 -- distill.json fixture 全部程序化构造,不重蒸、不联网
import json, subprocess, sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "build_author.py"

def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True, encoding="utf-8")

def distill(slug, year=None, author="测试作者"):
    """最小合法 distill.json(派生所需字段:slug/author/title/book_type/core_question/concepts/pub_year)。"""
    d = {"slug": slug, "author": author, "title": f"《{slug}》",
         "book_type": "思想史", "core_question": f"{slug} 的核心问题?",
         "concepts": [{"concept": f"概念{slug}", "concept_en": "",
                       "one_liner": "一句话", "stance": "支持"}]}
    if year is not None:
        d["pub_year"] = year
    return d

def write_distills(tmp_path, *ds):
    """落若干 distill 文件,返回匹配它们的 glob 串。"""
    in_dir = tmp_path / "in"; in_dir.mkdir()
    for d in ds:
        (in_dir / f"{d['slug']}.json").write_text(
            json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return str(in_dir / "*.json")

def out_arg(tmp_path):
    return str(tmp_path / "out" / "author.json")

# --- 回归:>=2 部已蒸但全部缺 pub_year -> exit 3 干净拒跑(原来 IndexError 裸栈 exit 1) ---
def test_all_missing_pub_year_exit3(tmp_path):
    pat = write_distills(tmp_path, distill("b1"), distill("b2"))
    r = run("--inputs", pat, "--out", out_arg(tmp_path))
    assert r.returncode == 3
    assert "Traceback" not in r.stderr
    assert "pub_year" in r.stderr

# --- --inputs glob 一个文件都没匹配到 = 输入有误 -> exit 2(原来混进 <2 部 exit 3) ---
def test_inputs_glob_no_match_exit2(tmp_path):
    r = run("--inputs", str(tmp_path / "nothing*.json"), "--out", out_arg(tmp_path))
    assert r.returncode == 2
    assert "未匹配" in r.stderr

# --- 触发门槛:单本 -> exit 3 ---
def test_single_book_threshold_exit3(tmp_path):
    pat = write_distills(tmp_path, distill("b1", 2001))
    r = run("--inputs", pat, "--out", out_arg(tmp_path))
    assert r.returncode == 3 and "门槛" in r.stderr

# --- 正常路径:两本带 pub_year -> exit 0,时间线按年排序 ---
def test_two_books_success(tmp_path):
    pat = write_distills(tmp_path, distill("b1", 2001), distill("b2", 2011))
    out = tmp_path / "out" / "author.json"
    r = run("--inputs", pat, "--out", str(out))
    assert r.returncode == 0, r.stderr
    doc = json.loads(out.read_text(encoding="utf-8"))
    assert [b["slug"] for b in doc["books"]] == ["b1", "b2"]
    assert doc["concept_graph"]["nodes"]

# --- 防覆盖栏:out 已存在且 manual 缺失 -> exit 2;--force 放行 ---
def test_overwrite_guard_exit2_without_force(tmp_path):
    pat = write_distills(tmp_path, distill("b1", 2001), distill("b2", 2011))
    target = tmp_path / "out" / "author.json"
    target.parent.mkdir()
    target.write_text("{}", encoding="utf-8")
    r = run("--inputs", pat, "--out", str(target))
    assert r.returncode == 2 and "防覆盖" in r.stderr
    r2 = run("--inputs", pat, "--out", str(target), "--force")
    assert r2.returncode == 0, r2.stderr

# --- 损坏的 --manual JSON -> exit 2(输入问题),不裸栈 ---
def test_corrupt_manual_exit2(tmp_path):
    pat = write_distills(tmp_path, distill("b1", 2001), distill("b2", 2011))
    manual = tmp_path / "manual.json"
    manual.write_text("{ 这不是合法 JSON", encoding="utf-8")
    r = run("--inputs", pat, "--manual", str(manual), "--out", out_arg(tmp_path))
    assert r.returncode == 2
    assert "Traceback" not in r.stderr
    assert "manual" in r.stderr
