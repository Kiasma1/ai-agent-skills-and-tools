import json
import sys
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from update_marketplace import build_marketplace, write_atomic  # noqa: E402


def test_build_marketplace_preserves_other_plugins():
    current = {
        "name": "personal",
        "interface": {"displayName": "Mine"},
        "plugins": [{"name": "other", "source": "./other"}],
    }
    result = build_marketplace(current)
    assert result["interface"]["displayName"] == "Mine"
    assert [item["name"] for item in result["plugins"]] == [
        "other",
        "sansheng-distill",
    ]
    entry = result["plugins"][-1]
    assert entry["source"]["path"] == "./plugins/sansheng-distill"
    assert entry["policy"]["installation"] == "AVAILABLE"


def test_write_atomic_round_trip(tmp_path):
    path = tmp_path / "nested" / "marketplace.json"
    doc = build_marketplace()
    write_atomic(path, doc)
    assert json.loads(path.read_text(encoding="utf-8")) == doc
