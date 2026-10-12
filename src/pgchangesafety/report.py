"""Static, offline evidence report for PostgreSQL change assessments.

Only formats an existing assessment; does not authorize a deployment or access a DB.
"""
from __future__ import annotations

from hashlib import sha256
from html import escape
import json
from typing import Any


def _esc(value: Any) -> str:
    if value is None:
        return "UNKNOWN"
    if isinstance(value, bool):
        return "yes" if value else "no"
    return escape(str(value), quote=True)


def _table(title: str, rows: list[dict[str, Any]], fields: tuple[tuple[str, str], ...]) -> str:
    headers = "".join(f"<th scope='col'>{_esc(title)}</th>" for _, title in fields)
    if rows:
        body = "\n".join(
            "<tr>" + "".join(f"<td>{_esc(row.get(key))}</td>" for key, _ in fields) + "</tr>"
            for row in rows
        )
    else:
        body = f"<tr><td colspan='{len(fields)}'>No observations supplied</td></tr>"
    return (
        f"<section><h2>{_esc(title)}</h2><div class='scroll'>"
        f"<table><thead><tr>{headers}</tr></thead><tbody>{body}</tbody></table>"
        "</div></section>"
    )


def _list(title: str, items: list[Any]) -> str:
    content = (
        "<ul>" + "".join(f"<li>{_esc(item)}</li>" for item in items) + "</ul>"
        if items else "<p>None declared by the supplied evidence. This does not prove complete coverage.</p>"
    )
    return f"<section><h2>{_esc(title)}</h2>{content}</section>"


def render_html(result: dict[str, Any], *, synthetic: bool = False) -> str:
    """Return a print-ready offline HTML report with SHA-256 of canonical JSON.

    Assessment content may contain confidential infrastructure details: do not
    distribute it without reviewing the inputs. All interpolated text is escaped.
    """
    canonical = json.dumps(
        result, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    )
    digest = sha256(canonical.encode("utf-8")).hexdigest()
    regressions = result.get("regressions") or []
    overlap = result.get("observed_workload_overlap_pct")
    ratio = result.get("causal_resolution_rate")
    rate = (
        f"{ratio * 100:.1f}%" if isinstance(ratio, (float, int)) and not isinstance(ratio, bool)
        else "UNKNOWN"
    )
    banner = (
        "SYNTHETIC DEMONSTRATION — NOT PRODUCTION EVIDENCE" if synthetic
        else "EVIDENCE REPORT — NOT DEPLOYMENT AUTHORIZATION"
    )
    metrics = (
        ("Evidence strength", result.get("evidence_strength")),
        ("Evidence score", result.get("evidence_score")),
        ("Decision coverage", result.get("decision_coverage_score")),
        ("Observed workload overlap", f"{overlap}%" if overlap is not None else None),
        ("Detected regressions", len(regressions)),
        ("Causal resolution rate", rate),
    )
    cards = "".join(
        f"<div class='metric'><strong>{_esc(value)}</strong><span>{_esc(name)}</span></div>"
        for name, value in metrics
    )
    return (
        "<!doctype html>\n<html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<meta http-equiv='Content-Security-Policy' "
        "content=\"default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'\">"
        "<title>PostgreSQL Change Safety — Evidence</title>"
        "<style>"
        ":root{font-family:system-ui,sans-serif;color:#17212e;background:#f5f7f9}"
        "body{max-width:1080px;margin:0 auto;padding:22px;line-height:1.5}"
        "header,section,footer{background:#fff;border:1px solid #dee4e9;"
        "border-radius:10px;padding:20px;margin-bottom:14px}"
        "h1{margin:0}h2{font-size:1.1rem;margin:0 0 12px}"
        ".notice{background:#fff2d4;color:#6c4500;padding:10px;font-weight:700}"
        ".metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));"
        "gap:9px;margin-top:16px}.metric{background:#edf3f8;padding:12px;border-radius:6px}"
        ".metric strong{font-size:1.2rem;display:block;overflow-wrap:anywhere}"
        ".metric span{font-size:.85rem}.scroll{overflow:auto}table{border-collapse:collapse;"
        "width:100%;font-size:.85rem}td,th{padding:8px;text-align:left;"
        "border:1px solid #dee4e9;overflow-wrap:anywhere}th{background:#edf3f8}"
        "li,code{overflow-wrap:anywhere}footer{font-size:.8rem}"
        "@media print{body{background:#fff;padding:0}header,section,footer{break-inside:avoid}}"
        "</style></head><body><header><h1>PostgreSQL Change Safety</h1>"
        "<p>Independent before/after workload evidence</p>"
        f"<p class='notice'>{_esc(banner)}</p>"
        "<p>Scores cover the supplied evidence only. No guarantee of production safety, "
        "workload completeness, or absence of regressions.</p>"
        f"<div class='metrics'>{cards}</div></header>"
        + _table("Detected regressions", regressions, (
            ("fingerprint", "Query fingerprint"), ("baseline_ms", "Before (ms)"),
            ("candidate_ms", "After (ms)"), ("ratio", "Ratio"),
            ("workload_share_pct", "Workload share (%)"), ("severity", "Severity"),
            ("cause_status", "Cause status"), ("cause", "Candidate cause"),
            ("cause_confidence", "Cause confidence"), ("supporting_trials", "Trials"),
        ))
        + _table("Execution-plan changes", result.get("plan_variant_diffs") or [], (
            ("fingerprint", "Query fingerprint"), ("status", "Status"),
            ("baseline_variant_count", "Before variants"),
            ("candidate_variant_count", "After variants"),
            ("dominant_plan_changed", "Dominant changed"),
            ("distribution_shift_pct", "Distribution shift (%)"),
            ("parameter_sensitivity_status", "Parameter coverage"),
        ))
        + _table("Environment changes", result.get("environment_diffs") or [], (
            ("factor", "Factor"), ("baseline", "Before"), ("candidate", "After"),
        ))
        + _list("Known unknowns", result.get("known_unknowns") or [])
        + _list("Unresolved confounders", result.get("unresolved_confounders") or [])
        + "<footer><strong>Canonical assessment JSON SHA-256:</strong> "
        f"<code>{digest}</code><p>Hash applies to the canonical JSON assessment (UTF-8, "
        "sorted keys, compact separators, non-ASCII preserved), not this HTML.</p>"
        "<p>This document is static and loads no external assets. Review for sensitive "
        "information before sharing. Retain the JSON assessment to verify the hash.</p>"
        "</footer></body></html>\n"
    )
