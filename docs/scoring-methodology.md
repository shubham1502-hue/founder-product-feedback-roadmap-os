# Scoring Methodology

The scoring is deterministic and editable.

The workflow reads:

- `data/sample_product_feedback.csv`
- `config/company_profile.yml`
- `config/scoring_rules.yml`

It calculates:

- Revenue impact score
- Retention impact score
- Expansion impact score
- Strategic fit score
- Urgency score
- Effort score
- Confidence score
- Roadmap priority score

## Inputs that increase priority

- Repeated or widespread feedback
- Revenue blocked
- High retention risk
- High expansion potential
- High strategic alignment
- High urgency
- High-value account impact
- High severity
- No workaround
- High confidence
- Strong target segment fit

## Inputs that reduce priority

- Low frequency
- No revenue blocked
- No retention risk
- No expansion potential
- Low strategic alignment
- Available workaround
- High implementation effort
- Low confidence
- Poor segment fit

## Decision categories

- Build now: 80 to 100
- Validate next: 60 to 79
- Watch: 40 to 59
- Defer: 20 to 39
- Reject or solve elsewhere: below 20

## Decision routing

The score is not the only rule. A high-pain issue can still be routed outside product if the better fix is operational.

| Decision | Typical reason |
| --- | --- |
| Build now | Strong score, high strategic fit, and enough revenue, retention, expansion, urgency, or repeated signal |
| Validate with customers | Strong signal, but more discovery is needed before using roadmap capacity |
| Add to roadmap candidate list | Useful signal that should be watched next cycle |
| Solve with onboarding | Setup, handoff, training, or activation workflow should improve before product scope |
| Solve with sales narrative | Buyer confusion, positioning, expectation setting, or proof problem |
| Solve with support process | Support, documentation, training, or CS process should fix the issue |
| Defer | Low current leverage or high effort relative to the signal |
| Reject | Outside strategy, niche customization, or poor target segment fit |

## Owner routing

- Product owns build-now roadmap work.
- Founder or Product owns validation work.
- Customer Success owns onboarding and customer process fixes.
- Sales or Founder owns sales narrative fixes.
- Support or Customer Success owns support, documentation, and training fixes.
- Founder owns explicit reject calls when a request could distract the roadmap.

## Why recommendations can differ from scores

Some issues should not become product work even if the customer pain is real. The system routes likely non-product issues into onboarding, sales narrative, support process, documentation, training, CS playbook, pricing, or rejection.

For every feedback item, read:

```text
outputs/score_explanations.csv
```
