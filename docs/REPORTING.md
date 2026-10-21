# Portable PostgreSQL upgrade evidence report

This report is a **static offline HTML file**, not a safety certificate or deployment approval.
It helps database teams review evidence from a before/after PostgreSQL change.

## Try without a database

Install the project with pip install -e . and run:

~~~bash
pgchangesafe demo --format html --output demo.html
pgchangesafe demo --format json --output demo.json
~~~

The demo is synthetic and marked as such. Do not present it as customer evidence.

## Produce a real before/after report

After collecting comparable start/end measurement windows for baseline and candidate:

~~~bash
pgchangesafe compare baseline-window.json candidate-window.json --format json --output assessment.json
pgchangesafe compare baseline-window.json candidate-window.json --format html --output assessment.html
~~~

Open assessment.html offline, or print to PDF. Both outputs derive from the same
comparison. Keep the source windows and JSON in the evidence archive.

## Independently check the assessment identity

The HTML includes SHA-256 of the canonical JSON **assessment content**.
It is not the hash of the HTML file or a digital signature.

~~~bash
python - <<'PY'
import hashlib, json
from pathlib import Path
result = json.loads(Path("assessment.json").read_text(encoding="utf-8"))
canonical = json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
print(hashlib.sha256(canonical.encode("utf-8")).hexdigest())
PY
~~~

Compare the output with the hash shown in assessment.html.

## Evidence and limits

- Shows regression fingerprints, timings, severity, suspected cause, evidence confidence,
  execution-plan changes, environment changes, unknowns and confounders.
- Escapes untrusted text in HTML. Inline CSS only; no JavaScript, remote fonts or trackers.
- The data can expose sensitive infrastructure details. Review it before sharing.
- Query text remains opt-in in the underlying capture; the report does not add it.
- Missing evidence remains UNKNOWN. A clear report does not establish full workload coverage.
- It does not authorize deployment, guarantee query equivalence or certify migration safety.

## Validation status

Automated offline reporting can be tested in CI. Customer acceptance, commercial
demand and willingness to pay are **not yet proven**. This is a product component,
not a paid product by itself.
## Input validity

`assess` and `compare` require one row per nonempty fingerprint in each snapshot,
finite positive calls, and a finite positive effective latency (`p95_ms` when
present, otherwise `mean_ms`). A row without usable observations must be omitted
and its missing coverage retained as unknown, rather than supplied as zero latency.
An empty baseline cannot support strong evidence. Cumulative capture/window inputs
may contain zero counters, but duplicate fingerprints are rejected before indexing.

Coverage percentages must be in [0,100] or unknown (`null`/omitted). Coverage flags
accept booleans, null, or the existing explicit true/false, yes/no, 1/0 string
forms. Other strings cannot imply true. Assessment thresholds must be finite,
with regression ratio > 1 and minimum delta >= 0. These are structural checks;
they do not authenticate measurements or prove declared coverage.

CLI JSON rejects repeated object members and NaN/Infinity constants. Validation
errors exit 2, produce a diagnostic on stderr and leave any existing output
untouched. The HTML report hash applies to assessment JSON, not the truth of its
input. [Product trial and acceptance evidence](PRODUCT_CASE.md).
