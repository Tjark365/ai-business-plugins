# B2B Lead Finder

Find high-value B2B prospects using current public information.

## Repository implementation

- `lead_finder.py` — core ranking, scoring and Free/Pro output logic.
- `plugin-spec.md` — product contract and required behavior.
- `test_lead_finder.py` — unit tests.

## Free
- Preview mode
- Maximum 3 leads
- Lightweight fields only

## Pro
- Full ranked research output
- Buying signals
- Ability-to-pay assessment
- Evidence and source tracking
- Next actions
- Score from 0–100

Target price: €49/month.

### Score

| Factor | Weight |
|---|---:|
| ICP fit | 30 |
| Buying signal | 25 |
| Ability to pay | 15 |
| Problem/offer fit | 15 |
| Timing | 10 |
| Evidence | 5 |

### Important

This module does not perform web search by itself. The host must inject a search provider that returns current, sourced evidence.

Never invent contacts, buying intent, revenue, or private personal data.
