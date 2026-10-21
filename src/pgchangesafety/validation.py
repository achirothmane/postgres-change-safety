"""Narrow evidence invariants; validation does not authenticate measurements."""
from __future__ import annotations

import json
from math import isfinite
from pathlib import Path
from typing import Any


def _unique_members(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("JSON contains a duplicate object member")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError("JSON contains a non-finite constant")


def read_json(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_unique_members, parse_constant=_reject_constant,
    )


def number(value: Any, path: str, *, minimum: float = 0.0, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError(f"{path} must be a finite number")
    try:
        result = float(value)
    except (ValueError, OverflowError):
        raise ValueError(f"{path} must be a finite number") from None
    if not isfinite(result) or result < minimum or (positive and result <= 0):
        bound = "positive" if positive else f">= {minimum:g}"
        raise ValueError(f"{path} must be finite and {bound}")
    return result


def query_map(snapshot: Any, name: str, *, measured: bool = False) -> dict[str, dict[str, Any]]:
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get("queries"), list):
        raise ValueError(f"{name}.queries must be a list")
    indexed = {}
    for index, row in enumerate(snapshot["queries"]):
        path = f"{name}.queries[{index}]"
        if not isinstance(row, dict):
            raise ValueError(f"{path} must be an object")
        fp = row.get("fingerprint")
        if not isinstance(fp, str) or not fp.strip():
            raise ValueError(f"{path}.fingerprint must be nonempty text")
        if fp in indexed:
            raise ValueError(f"{path}: duplicate fingerprint; supply distinct measurement identities")
        number(row.get("calls"), f"{path}.calls", positive=measured)
        for field in ("mean_ms", "p95_ms", "total_exec_ms"):
            if field in row:
                number(row[field], f"{path}.{field}")
        if measured:
            latency = row.get("p95_ms", row.get("mean_ms"))
            number(latency, f"{path}.latency (p95_ms or mean_ms)", positive=True)
        indexed[fp] = row
    number(sum(float(row["calls"]) for row in indexed.values()), f"{name}.total_calls")
    return indexed


def validate_assessment(payload: Any) -> None:
    if not isinstance(payload, dict):
        raise ValueError("assessment must be an object")
    for name in ("baseline", "candidate"):
        query_map(payload.get(name), name, measured=True)

    coverage = payload.get("coverage", {})
    if coverage is None:
        coverage = {}
    if not isinstance(coverage, dict):
        raise ValueError("coverage must be an object")
    for field in ("workload_volume_pct", "bind_value_diversity_pct",
                  "environment_match_pct", "replay_failure_pct"):
        value = coverage.get(field)
        if value in (None, ""):
            continue
        if number(value, f"coverage.{field}") > 100:
            raise ValueError(f"coverage.{field} must be in [0,100]")
    for field in ("write_workload_covered", "peak_concurrency_covered",
                  "background_jobs_covered", "measurement_window_valid"):
        value = coverage.get(field)
        if value is None or isinstance(value, bool):
            continue
        if isinstance(value, str) and value.strip().lower() in {"true", "false", "yes", "no", "1", "0"}:
            continue
        raise ValueError(f"coverage.{field} must be boolean or null")
    unknowns = coverage.get("additional_unknowns")
    if unknowns is not None and (
        not isinstance(unknowns, list) or any(not isinstance(item, str) for item in unknowns)
    ):
        raise ValueError("coverage.additional_unknowns must be a list of text")

    thresholds = payload.get("thresholds", {})
    if not isinstance(thresholds, dict):
        raise ValueError("thresholds must be an object")
    if number(thresholds.get("regression_ratio", 1.25), "thresholds.regression_ratio") <= 1:
        raise ValueError("thresholds.regression_ratio must be greater than 1")
    number(thresholds.get("min_delta_ms", 5.0), "thresholds.min_delta_ms")

    for field in ("experiments", "environment_diffs", "plan_variant_diffs"):
        rows = payload.get(field, [])
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise ValueError(f"{field} must be a list of objects")
    for index, trial in enumerate(payload.get("experiments", [])):
        path = f"experiments[{index}]"
        if not isinstance(trial.get("controlled", False), bool):
            raise ValueError(f"{path}.controlled must be boolean")
        for field in ("changed_ms", "restored_ms"):
            if field in trial:
                number(trial[field], f"{path}.{field}")
        if "replicates" in trial:
            count = number(trial["replicates"], f"{path}.replicates", positive=True)
            if not count.is_integer():
                raise ValueError(f"{path}.replicates must be an integer")
    for index, diff in enumerate(payload.get("plan_variant_diffs", [])):
        if diff.get("distribution_shift_pct") is not None:
            path = f"plan_variant_diffs[{index}].distribution_shift_pct"
            if number(diff["distribution_shift_pct"], path) > 100:
                raise ValueError(f"{path} must be in [0,100]")
