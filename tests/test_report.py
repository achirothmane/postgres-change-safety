"""Offline evidence report contract and CLI smoke tests."""
from __future__ import annotations

from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys

from pgchangesafety.demo import build_demo_assessment
from pgchangesafety.report import render_html


class _DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = set()
        self.attributes = []

    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        self.attributes.extend(attrs)


def test_report_has_evidence_and_corresponding_canonical_json_hash():
    result = build_demo_assessment()
    html = render_html(result, synthetic=True)
    digest = sha256(
        json.dumps(
            result, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode("utf-8")
    ).hexdigest()
    parsed = _DocumentParser()
    parsed.feed(html)

    assert html.startswith("<!doctype html>")
    assert "SYNTHETIC DEMONSTRATION" in html
    assert "NOT DEPLOYMENT AUTHORIZATION" not in html
    assert "Known unknowns" in html
    assert result["regressions"][0]["fingerprint"] in html
    assert digest in html
    assert "table" in parsed.tags and "style" in parsed.tags
    assert "script" not in parsed.tags
    assert "iframe" not in parsed.tags
    assert "img" not in parsed.tags
    assert "link" not in parsed.tags
    assert not any(key.startswith("on") for key, _ in parsed.attributes)


def test_escaped_values_and_unknown_are_preserved_without_executable_markup():
    result = {
        "evidence_strength": "UNKNOWN",
        "observed_workload_overlap_pct": None,
        "regressions": [{
            "fingerprint": '<img src=x onerror="alert(1)">',
            "cause": "<script>evil()</script>",
            "severity": '" autofocus onfocus="evil()"',
        }],
        "known_unknowns": ["Missing <strong>write workload</strong> evidence"],
        "unresolved_confounders": ["control & test"],
    }
    html = render_html(result)
    parsed = _DocumentParser()
    parsed.feed(html)

    assert "NOT DEPLOYMENT AUTHORIZATION" in html
    assert "UNKNOWN%" not in html
    assert "&lt;img" in html
    assert "&lt;script&gt;" in html
    assert "&lt;strong&gt;" in html
    assert "&amp;" in html
    assert "img" not in parsed.tags
    assert "script" not in parsed.tags
    assert not any(key.startswith("on") for key, _ in parsed.attributes)


def test_cli_demo_and_assess_emit_self_contained_report(tmp_path: Path):
    demo_html = tmp_path / "demo.html"
    subprocess.run(
        [sys.executable, "-m", "pgchangesafety.cli", "demo", "--format", "html",
         "--output", str(demo_html)],
        check=True, capture_output=True, text=True,
    )
    text = demo_html.read_text(encoding="utf-8")
    assert "SYNTHETIC DEMONSTRATION" in text
    assert re.search(r"[0-9a-f]{64}", text)

    result = subprocess.run(
        [sys.executable, "-m", "pgchangesafety.cli", "assess",
         "examples/major-upgrade.json", "--format", "html"],
        check=True, capture_output=True, text=True,
    )
    assert "EVIDENCE REPORT" in result.stdout
    assert "SYNTHETIC DEMONSTRATION" not in result.stdout
    assert "https://" not in result.stdout


def test_cli_compare_supports_offline_html(tmp_path: Path):
    before = tmp_path / "before.json"
    after = tmp_path / "after.json"
    before.write_text(json.dumps({
        "label": "before", "postgres_version": "17", "queries": [
            {"fingerprint": "q1", "calls": 100, "mean_ms": 3.0},
        ]
    }), encoding="utf-8")
    after.write_text(json.dumps({
        "label": "after", "postgres_version": "17", "queries": [
            {"fingerprint": "q1", "calls": 100, "mean_ms": 10.0},
        ]
    }), encoding="utf-8")
    output = tmp_path / "comparison.html"
    subprocess.run(
        [sys.executable, "-m", "pgchangesafety.cli", "compare",
         str(before), str(after), "--format", "html", "--output", str(output)],
        check=True, capture_output=True, text=True,
    )
    html = output.read_text(encoding="utf-8")
    assert "<!doctype html>" in html
    assert "Detected regressions" in html
    assert "q1" in html
