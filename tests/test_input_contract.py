"""Product acceptance cases specified before the input-validity repair.

The oracle comes from observable report promises: ambiguous/missing evidence must
not turn into a successful, stronger-looking assessment. These tests are not an
external database or security audit.
"""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest

from pgchangesafety.engine import assess
from pgchangesafety.snapshot import build_assessment_payload, derive_window_snapshot


def comparison():
    return {
        "baseline": {"queries": [{"fingerprint": "q1", "calls": 1000, "mean_ms": 10}]},
        "candidate": {"queries": [{"fingerprint": "q1", "calls": 1000, "mean_ms": 40}]},
        "coverage": {
            "workload_volume_pct": 100, "bind_value_diversity_pct": 100,
            "environment_match_pct": 100, "replay_failure_pct": 0,
            "write_workload_covered": True, "peak_concurrency_covered": True,
            "background_jobs_covered": True,
        },
    }


@pytest.mark.parametrize("side", ["baseline", "candidate"])
@pytest.mark.parametrize("entry", ["assess", "compare", "window"])
def test_duplicate_cannot_replace_evidence(side, entry):
    p = comparison()
    duplicate = deepcopy(p[side]["queries"][0])
    duplicate["mean_ms"] = 10
    p[side]["queries"].append(duplicate)
    with pytest.raises(ValueError, match="duplicate fingerprint"):
        if entry == "assess":
            assess(p)
        elif entry == "compare":
            build_assessment_payload(p["baseline"], p["candidate"])
        else:
            derive_window_snapshot(p["baseline"], p["candidate"])


@pytest.mark.parametrize("field,value", [
    ("mean_ms", None), ("mean_ms", -1), ("mean_ms", 0), ("mean_ms", True),
    ("mean_ms", float("nan")), ("mean_ms", float("inf")),
    ("calls", -1), ("calls", 0), ("calls", True), ("calls", float("inf")),
])
def test_invalid_observation_cannot_produce_report(field, value):
    p = comparison()
    p["candidate"]["queries"][0][field] = value
    with pytest.raises(ValueError, match="candidate.queries"):
        assess(p)


def test_missing_latency_cannot_mean_zero_latency():
    p = comparison()
    del p["candidate"]["queries"][0]["mean_ms"]
    with pytest.raises(ValueError, match="latency"):
        assess(p)


@pytest.mark.parametrize("field", [
    "workload_volume_pct", "bind_value_diversity_pct", "environment_match_pct", "replay_failure_pct",
])
@pytest.mark.parametrize("value", [-1, 101, True, float("nan"), float("inf")])
def test_invalid_coverage_does_not_strengthen_evidence(field, value):
    p = comparison()
    p["coverage"][field] = value
    with pytest.raises(ValueError, match="coverage"):
        assess(p)


@pytest.mark.parametrize("field", [
    "write_workload_covered", "peak_concurrency_covered", "background_jobs_covered",
    "measurement_window_valid",
])
def test_unknown_boolean_string_is_not_true(field):
    p = comparison()
    p["coverage"][field] = "unknown"
    with pytest.raises(ValueError, match="coverage"):
        assess(p)


def test_valid_regression_unknowns_and_empty_observations():
    p = comparison()
    r = assess(p)
    assert len(r.regressions) == 1
    assert r.regressions[0].ratio == 4
    assert r.regressions[0].cause == "UNKNOWN"
    del p["coverage"]
    assert assess(p).known_unknowns
    assert assess(p).evidence_strength != "HIGH"
    p = comparison()
    p["baseline"]["queries"] = []
    p["candidate"]["queries"] = []
    r = assess(p)
    assert r.evidence_strength == "LOW"
    assert any("workload" in item.lower() for item in r.known_unknowns)


@pytest.mark.parametrize("value", [0, 100, None])
def test_percentage_boundaries_and_unknown_are_accepted(value):
    p = comparison()
    p["coverage"]["bind_value_diversity_pct"] = value
    r = assess(p)
    assert len(r.regressions) == 1
    if value is None:
        assert any("Bind-value diversity coverage is unknown" == item for item in r.known_unknowns)


@pytest.mark.parametrize("value", ["false", "no", "0", None])
def test_explicit_false_or_unknown_declaration_does_not_become_true(value):
    p = comparison()
    p["coverage"]["write_workload_covered"] = value
    r = assess(p)
    assert r.evidence_strength != "HIGH"
    assert any("Write" in item for item in r.known_unknowns)


@pytest.mark.parametrize("command", ["assess", "compare", "window"])
@pytest.mark.parametrize("fmt", ["text", "json", "html"])
def test_cli_invalid_input_leaves_no_success_artifact(tmp_path: Path, command, fmt):
    p = comparison()
    p["candidate"]["queries"].append(deepcopy(p["candidate"]["queries"][0]))
    source = tmp_path / "input.json"
    before = tmp_path / "before.json"
    after = tmp_path / "after.json"
    output = tmp_path / "report"
    source.write_text(json.dumps(p))
    before.write_text(json.dumps(p["baseline"]))
    after.write_text(json.dumps(p["candidate"]))
    output.write_text("previous valid artifact")
    args = [str(source)] if command == "assess" else [str(before), str(after)]
    if command != "window":
        args += ["--format", fmt]
    run = subprocess.run(
        [sys.executable, "-m", "pgchangesafety.cli", command, *args, "--output", str(output)],
        capture_output=True, text=True,
    )
    assert run.returncode == 2
    assert "duplicate fingerprint" in run.stderr
    assert "Traceback" not in run.stderr
    assert run.stdout == ""
    assert output.read_text() == "previous valid artifact"


@pytest.mark.parametrize("command", ["assess", "benchmark"])
@pytest.mark.parametrize("text", [
    '{"baseline": {}, "baseline": {}}',
    '{"coverage": {"workload_volume_pct": NaN}}',
    '{"coverage": {"workload_volume_pct": Infinity}}',
    '{"coverage": {"workload_volume_pct": -Infinity}}',
])
def test_cli_rejects_ambiguous_json(tmp_path: Path, text, command):
    source = tmp_path / "input.json"
    source.write_text(text)
    output = tmp_path / "report.html"
    args = ["--format", "html", "--output", str(output)] if command == "assess" else ["--json"]
    run = subprocess.run(
        [sys.executable, "-m", "pgchangesafety.cli", command, str(source), *args],
        capture_output=True, text=True,
    )
    assert run.returncode == 2
    assert "invalid input" in run.stderr.lower()
    assert "Traceback" not in run.stderr
    assert run.stdout == ""
    assert not output.exists()
