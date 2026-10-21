# Product engineering trial — 21 October 2026

## Decision and scope

**INVESTIGATE** a fixed-scope PostgreSQL change evidence review, using the existing
offline tool. This is a commercial validation candidate, not an approved business
or a production certification service. No buyer commitment, payment, settlement,
collection or profit has been established in this trial.

The full product promise is to help a PostgreSQL change owner examine comparable
workloads, material regressions, causal experiments, plan changes and missing
evidence before a consequential change. Required capabilities include defensible
input identity, comparable measurement windows, privacy, explicit abstention,
repeatable analysis, understandable reports and a supportable delivery process.
The owner retains deployment authority. An attractive HTML report cannot substitute
for representative workloads or an independent database specialist when needed.

The first commercial experiment would be a **service**, not a new hosted platform:
review one authorized, sanitized baseline/candidate comparison and deliver a
portable report, limitations and a prioritized next-test list. No production
credentials, production execution, unattended monitoring or upgrade guarantee are
included. The MIT tool remains available without buying the service.

## Opportunity comparison before implementation

The comparison used current repository state and primary vendor sources on
2026-10-21. Advertised offerings and vendor customer stories indicate categories
of spending; they do not establish contestable budget or demand for our offer.
No arbitrary weighted score was used.

| Candidate | Buyer/problem hypothesis and existing alternative | Decisive limitation | Decision |
| --- | --- | --- | --- |
| n8n release evidence | Automation owner wants safer workflow changes; n8n sells source control/environments and evaluations | Existing ReleaseGuard service needs a database, credentials and deployment; published offer link did not yield a verifiable checkout in this research; our buyer and collection remain unproven | Defer runtime expansion; validate adoption and purchase path first |
| Local document generation | Operations/development teams produce recurring documents; Docmosis markets paid document generation and customer deployments | Mature alternatives; differentiated buyer need is unproven; document fidelity and trusted-template boundaries require additional environment and review | Investigate a specific customer workflow before further general SDK expansion |
| PostgreSQL change evidence | DBA/platform/change owner needs evidence before an upgrade or other change; manual pg_stat_statements/EXPLAIN and pganalyze Workbooks are alternatives | No qualified buyer, proven willingness to pay or verified seller/payment route; input validity could falsely strengthen reports | Selected bounded trial: falsify the report contract, repair a demonstrated defect, prepare a buyer experiment |

Selection favors a meaningful, bounded uncertainty that can be tested without
customer access. It does not establish that this is the institution's best market.
Do not expand into a SaaS or marketplace application on this evidence.

## Solution decision and killer unknown

At main commit `624b8bb66e1b7b88980855f060f666e2984b4fa2`, can malformed input
silently suppress a regression and still produce strong-looking evidence?

Alternatives considered:

- Keep the current behavior and warn only in documentation: rejected; the report
  would still conceal invalid observations.
- Aggregate duplicate identities automatically: rejected for this repair; rows may
  belong to different users/databases and percentiles cannot be combined by
  averaging. Aggregation needs an explicit measurement/identity contract.
- Adopt a full schema-validation dependency: feasible, but unnecessary for this
  narrow invariant; it would not itself select a safe aggregation policy.
- Validate before indexing/assessment and reject ambiguous observations: selected.
  Keep the stdlib core and existing CLI/report architecture.
- Buy/integrate a monitoring system or stop: valid customer alternatives; neither
  repairs our existing report's integrity. Reconsider product investment after the
  commercial experiment.

PostgreSQL documents pg_stat_statements rows by database, user, query and top-level
status. Repeated normalized fingerprints are therefore a plausible input, not
necessarily malicious. This trial must reject them explicitly rather than choose
the last row. It does not claim complete SQL canonicalization or fingerprint
collision resistance.

## Execution contract and acceptance — specified before repair

Authorized: local source/tests, sanitized examples, GitHub branch, CI and unmerged
PR. No spending, customer contact, account changes, production deployment, merge,
database access or legal commitments. Use one execution agent; multi-agent overhead
has no demonstrated benefit for this bounded repair. Stop after two unexplained
repair attempts; diagnose before retrying. Escalate a material product-promise
change or a need for sensitive customer data.

| ID | Acceptance criterion | Evidence method and limit |
| --- | --- | --- |
| A1 | Duplicate fingerprints cannot disappear through dictionary indexing in assessment, comparison or window derivation | Predetermined malformed fixtures, direct API and CLI rejection; not proof that every identity collision is detectable |
| A2 | Assessed rows require finite positive calls and effective latency; missing, negative, zero, boolean and non-finite observations cannot appear valid | Parameterized negative cases and a valid fourfold-regression control; no claim that supplied measurements are truthful |
| A3 | Coverage percentages are finite in [0,100]; unknown values stay unknown and unrecognized boolean declarations cannot become true | Boundary/unknown/invalid metadata cases; no independent verification of declared coverage |
| A4 | JSON duplicate members and non-finite constants fail; CLI validation failure is nonzero, diagnostic and emits no success report or overwritten artifact | Subprocess tests across assess/compare/window and output formats; no hostile-file sandbox certification |
| A5 | Existing valid examples and regression/unknown semantics remain usable; empty workload cannot obtain HIGH evidence | Full existing tests, explicit controls and blind benchmark; fixtures are repository-authored, not external customer validation |
| A6 | Package and real PostgreSQL integration checks pass on the reviewed commit, or failures remain explicit | Existing GitHub Actions matrix and wheel smoke; CI executes independently of the local shell but uses repository-authored tests/oracles |

Task accounting: capability/source audit, opportunity decision, acceptance contract,
repair, verification/PR, pilot preparation and evidence closure are separate work
items. Count accepted **A1–A6** only when their specified evidence exists; report the
numerator/denominator and failures. These are repair acceptance criteria, not a
general agent task-success benchmark. Founder interventions count only requests
needed to perform this session's authorized work; do not infer a lifecycle-wide
autonomy percentage. Time starts at the recorded input-defect reproduction and
ends at the first verified repair; session preparation is additional time.
Provider/token cost and existing subscriptions are unknown unless supplied by
billing records. No new paid service is authorized.

## Commercial experiment prepared for approval

Target an identifiable PostgreSQL change owner with an upcoming change, an existing
review process and authority over the relevant budget. Ask what they currently do,
what it costs, why manual analysis or an incumbent is insufficient, and whether
they can purchase from this seller. A user's enthusiasm is not purchasing authority.

Draft hypothesis: one fixed-scope review at **EUR 150**, including input validation,
one report, a next-test list and one clarification round. This is an unvalidated
price hypothesis for approval, not a published offer or a quote sent to a buyer.
Agree the input limits, turnaround, confidentiality, acceptance and refund terms
before any paid pilot. Do not promise production clearance or full security review.

Cheapest decisive test: after seller eligibility and a lawful invoicing/collection
route are confirmed, obtain one authorized buyer's explicit paid-pilot commitment
against this scope and price, then deliver and reconcile actual payment and fees.
No checkout/account is being created in this trial. The founder must approve buyer
contact and commercial terms; no engineering audit by the founder is required.

Continue only if a qualified buyer identifies a material gap, can legally buy, and
accepts a price that covers delivery/support/acquisition and fees. Investigate if
the problem is real but procurement, data sharing or willingness to pay remains
unresolved. Revise if buyers value a different bounded outcome. Stop if incumbents
or manual work are sufficient, data cannot be shared safely, collection is blocked,
or delivery economics fail. One pilot is not repeatable demand.

Record independently: interest → problem confirmation → trial willingness → paid
commitment → invoice → settled payment → collected funds → use/renewal. None is
inferred from the previous step. All remain **NOT TESTED for our offer** here.

Unit economics must include analysis/rework/support time, acquisition, payment and
platform fees, taxes/obligations where applicable, infrastructure and refunds.
Contribution = collected receipts minus attributable delivery/acquisition/refund
costs; net profit also deducts all relevant overhead. At a proposed EUR 150, the
maximum affordable delivery effort is `(150 - fees - acquisition - other costs) /
loaded hourly cost`; the inputs are unresolved, so profitability is unproven.

## Sources, currency and evidence limits

Primary sources accessed 2026-10-21:

- [PostgreSQL pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html): row identity and statistics semantics; refresh for the target server version.
- [pganalyze Workbooks](https://pganalyze.com/docs/workbooks): existing baseline/variant, plan and parameter comparisons; a material competitor, not proof that our offer is superior.
- [pganalyze pricing](https://pganalyze.com/pricing/): retrieved page advertised paid plans but had an old crawl age; no numeric price is relied on in this decision.
- [n8n pricing](https://n8n.io/pricing/) and [source control](https://docs.n8n.io/administer/use-source-control-and-environments/): native paid alternatives; refresh before a purchase/feature decision.
- [Docmosis pricing](https://www.docmosis.com/pricing/) and [customer example](https://www.docmosis.com/reviews-and-case-studies/gappless-generates-construction-reports-with-docmosis/): vendor-reported category activity, not independent evidence of transactions with us.

Research compared three existing assets and their principal alternatives. It was
not an exhaustive market survey, buyer interview study or paid-demand experiment.
Refresh buyer, competition, seller eligibility, prices and fees before commercial
commitment. Preserve this decision if conditions remain unchanged.

## Execution results

**VERIFIED within the specified repair scope:**

- Baseline main `624b8bb66e1b7b88980855f060f666e2984b4fa2`: all 40 existing tests
  passed. A valid 10→40 ms comparison produced one regression; appending a duplicate
  with 10 ms suppressed it and yielded HIGH evidence with no unknowns. Missing or
  negative candidate timing did likewise. The first 55 new acceptance cases failed
  before repair; seven boundary/unknown controls were subsequently added.
- [Acceptance contract commit](https://github.com/achirothmane/postgres-change-safety/commit/642fc78c6fb2d9144493d1543bb6f7cb8d12bdc4)
  contains the contract/tests with the pre-repair source. The repair is a separate
  commit, so the negative control can be rerun without accepting this narrative.
- Repair commit `074bdb454722c41d93f3b68d5bf92f4b7f497f01`: all 102 tests pass
  locally (Python 3.12) and in CI (Python 3.10/3.12/3.13). The synthetic blind
  benchmark passes 12/12 cases with no observed false causal attribution or
  clearance event. This is a small repository-authored suite, not measured
  generalization to customer workloads.
- [GitHub Actions run 39659462212](https://github.com/achirothmane/postgres-change-safety/actions/runs/39659462212)
  succeeded in all 13 jobs: unit matrix, clean wheel install/offline report,
  PostgreSQL 14/17 benchmarks, multi-query workloads (three trials), pgss windows,
  cross-version fingerprints and plan variants. The run started at 19:11:39Z and
  completed by 19:12:36Z on 2026-10-21 (57 seconds wall time; not engineering labor
  or billable compute time). `git diff --check` also passed locally.
- Controlled-workload input, benchmark result and sample report were uploaded for
  each of three trials. [Trial 1 artifact](https://github.com/achirothmane/postgres-change-safety/actions/runs/39659462212/artifacts/12373216813)
  archive digest: `2b323b38d4f368818da457a35724119eae08459eb0450b3dd008378e5bf4b8f0`.
  Metadata/upload logs were inspected; the binary archive was not independently
  downloaded in this session. GitHub currently records expiry on 2027-01-19;
  preserve needed evidence before expiry. These are controlled database runs,
  not customer workloads or production acceptance.

Acceptance: **6/6 of A1–A6 supported**, with the independence limits in the table.
The same AI execution session authored tests and repair; the prior-source failures,
product-derived criteria, PostgreSQL documentation and separately executed CI add
evidence but do not constitute an external expert audit or held-out evaluation.
[PR #15](https://github.com/achirothmane/postgres-change-safety/pull/15) remains
unmerged; no new production version was published.

One code repair passed the initial local suite; subsequent boundary tests passed
too. A general rework rate and total time to verified deliverable were not
instrumented and are **UNRESOLVED**. There were zero founder intervention requests
during the authorized trial; no lifecycle-wide autonomy percentage is inferred.
New paid-service purchases: none. Token/provider billing, CI charges, loaded labor
and opportunity cost are unavailable, so total cost per verified deliverable is
**UNRESOLVED**, not zero.

**SUPPORTED BUT LIMITED:** bounded in-session agentic research → acceptance →
repair → CI → reviewable PR. **NOT TESTED:** customer task success, an independent
specialist review, live installation, production release, acquisition, paid pilot,
settlement, collection, renewal, sustainable economics, multi-agent benefit and
continuous autonomous operation.

The improvement retained in code is validation **before lossy indexing**, plus
negative acceptance controls and preserved benchmark inputs. Future work should
reuse these checks, reassess identities/measurement comparability for the target
customer, and run the commercial test before substantial product expansion.

Resume from PR #15's actual head/checks and unresolved commercial gates. Review the
acceptance contract and changed inputs; do not restart settled market/category
research unless its assumptions change. The next executable step is an authorized,
qualified-buyer pilot and verified seller/collection route, not another platform.
