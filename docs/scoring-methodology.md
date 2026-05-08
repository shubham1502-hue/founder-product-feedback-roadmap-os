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

## Why recommendations can differ from scores

Some issues should not become product work even if the customer pain is real. The system routes likely non-product issues into onboarding, sales narrative, support process, documentation, training, CS playbook, pricing, or rejection.

For every feedback item, read:

```text
outputs/score_explanations.csv
```
