# Founder Product Feedback Roadmap OS

Turn customer feedback, sales objections, onboarding blockers, churn drivers, and expansion requests into roadmap priorities and founder-ready product decisions.

This helps founders see which product gaps block revenue, which themes keep repeating, which asks are noisy, and what product, CS, sales, support, or founder action should happen next. The core decisions are build now, validate with customers, solve outside product, defer, or reject.

## Founder quick read

| If you need to know... | Open this |
| --- | --- |
| What should we build or validate next | outputs/founder_roadmap_memo.md |
| Which product gaps are blocking revenue | outputs/product_gap_summary.csv |
| Which roadmap decisions need owner action | outputs/roadmap_decision_queue.csv |
| Which issues should be solved outside product | outputs/non_product_fix_queue.csv |
| Which asks are noisy, low-fit, or should be rejected | outputs/founder_roadmap_memo.md |
| Which accounts are creating product pressure | outputs/account_feedback_view.csv |
| Why a feedback item received a score or decision | outputs/score_explanations.csv |

Fastest path:
1. Replace data/sample_product_feedback.csv.
2. Edit config/company_profile.yml.
3. Run make run.
4. Open outputs/founder_roadmap_memo.md.

## Output preview

The included sample run produces:

- `outputs/founder_roadmap_memo.md`: founder-ready roadmap decision memo
- `outputs/roadmap_decision_queue.csv`: build, validate, defer, reject, or solve elsewhere decisions
- `outputs/product_gap_summary.csv`: repeated product gaps with impact
- `outputs/non_product_fix_queue.csv`: onboarding, sales, support, docs, or CS fixes
- `outputs/customer_signal_matrix.csv`: signal strength by theme, source, lifecycle stage, and segment
- `outputs/account_feedback_view.csv`: account-level feedback pressure
- `outputs/score_explanations.csv`: score and decision rationale

## 7-day Founder's Office sprint

- Day 1: Pull feedback from sales, onboarding, support, retention, and founder notes
- Day 2: Clean the feedback tracker and align themes
- Day 3: Run the roadmap prioritization workflow
- Day 4: Review build-now, validate-next, and non-product fix queues
- Day 5: Assign product, CS, sales, support, or founder owners
- Day 6: Turn top unknowns into customer discovery questions
- Day 7: Roll roadmap decisions into the weekly operating review

## Founder's Office signal

This repo demonstrates:

- separating signal from loud requests
- linking customer feedback to revenue, retention, and expansion
- deciding product versus non-product fixes
- roadmap tradeoff communication
- cross-functional owner assignment
- founder-ready decision memo writing

## The founder problem

Founders hear product feedback from sales calls, onboarding, support, retention reviews, expansion conversations, demos, and founder intuition. The hard part is deciding what deserves roadmap attention, what needs discovery, what should be solved outside product, and what should be ignored.

This repo turns scattered feedback into a founder-ready roadmap prioritization system.

## What this repo does

- Scores product feedback
- Clusters repeated themes
- Identifies revenue-blocking product gaps
- Flags retention-risk product gaps
- Finds expansion unlocks
- Separates product work from onboarding, sales, support, documentation, or CS fixes
- Creates roadmap decision queue
- Explains scores and recommendations
- Generates founder roadmap memo
- Creates product operating review

## What a founder gets in 10 minutes

- Roadmap priority scorecard
- Product gap summary
- Roadmap decision queue
- Non-product fix queue
- Customer signal matrix
- Account feedback view
- Score explanations
- Founder roadmap memo

## Before and after

Before:
- Product feedback scattered across calls, tickets, notes, and Slack
- Loud customers dominate roadmap
- Sales objections and churn drivers do not connect to product priorities
- Team builds without clear revenue, retention, or expansion logic
- Founder relies on memory

After:
- Structured feedback scorecard
- Product gap summary
- Roadmap decision queue
- Non-product fix queue
- Founder-ready roadmap memo
- Clear owners and next actions

## Who this is for

- Early-stage founders
- Founder's Office teams
- Product operators
- BizOps operators
- RevOps operators
- Customer Success operators
- B2B SaaS teams
- AI startup founders
- Founder-led services teams moving toward productization

## Quick start

1. Fork this repo.
2. Clone it locally.
3. Run `make install`.
4. Replace the sample feedback CSV.
5. Edit the company config.
6. Run `make run`.
7. Open `outputs/founder_roadmap_memo.md`.

| Step | File or command | What to do |
| --- | --- | --- |
| 1 | data/sample_product_feedback.csv | Replace with your feedback tracker |
| 2 | config/company_profile.yml | Edit product themes, segments, roadmap capacity, priorities |
| 3 | make run | Generate scorecards, queues, memo, and review |
| 4 | outputs/founder_roadmap_memo.md | Read this first |
| 5 | outputs/score_explanations.csv | Check why scores and recommendations were assigned |

## How to fork and use this for your company

- Click Fork.
- Rename the repo if needed.
- Replace `data/sample_product_feedback.csv` with your own feedback tracker.
- Edit `config/company_profile.yml`.
- Edit `config/scoring_rules.yml` if your roadmap logic uses different weights.
- Run `make run`.
- Review `outputs/founder_roadmap_memo.md` first.
- Review `outputs/roadmap_decision_queue.csv` second.
- Review `outputs/non_product_fix_queue.csv` third.
- Connect outputs to Google Sheets, Notion, Airtable, Linear, Jira, Productboard, HubSpot, Salesforce, Attio, Intercom, Zendesk, or your product tracker if relevant.

Non-technical path:
- Replace one CSV
- Edit one YAML file
- Run one command
- Read one memo

## Standalone or integrated

Standalone:
Use this repo by itself if you only need to turn scattered product feedback into roadmap decisions.

Integrated:
Use this repo with the Founder OS ecosystem if you want to connect product priorities to sales calls, onboarding, retention, weekly review, board narrative, and AI workflow prioritization.

## Lifecycle handoff

Before:
- [founder-led-sales-call-os](https://github.com/shubham1502-hue/founder-led-sales-call-os) for sales objections and deal risks
- [founder-customer-onboarding-os](https://github.com/shubham1502-hue/founder-customer-onboarding-os) for onboarding blockers
- [founder-retention-expansion-os](https://github.com/shubham1502-hue/founder-retention-expansion-os) for retention risks, churn drivers, and expansion asks
- [startup-metrics-playbook](https://github.com/shubham1502-hue/startup-metrics-playbook) for product and customer metric definitions

This repo produces:
- Roadmap priority scorecard
- Product gap summary
- Roadmap decision queue
- Non-product fix queue
- Customer signal matrix
- Founder roadmap memo

After:
- [founder-weekly-operating-review-agent](https://github.com/shubham1502-hue/founder-weekly-operating-review-agent) for weekly review
- [board-pack-investor-update-agent](https://github.com/shubham1502-hue/board-pack-investor-update-agent) for product or retention narrative
- [founder-ai-workflow-roi-os](https://github.com/shubham1502-hue/founder-ai-workflow-roi-os) if product operations workflows should be automated

## Where this fits in the Founder OS

- Use [ai-gtm-command-center](https://github.com/shubham1502-hue/ai-gtm-command-center) before calls.
- Use [founder-led-sales-call-os](https://github.com/shubham1502-hue/founder-led-sales-call-os) after sales calls.
- Use [founder-customer-onboarding-os](https://github.com/shubham1502-hue/founder-customer-onboarding-os) after close-won.
- Use [founder-retention-expansion-os](https://github.com/shubham1502-hue/founder-retention-expansion-os) after activation.
- Use founder-product-feedback-roadmap-os to convert customer and market signals into roadmap priorities.
- Use [founder-weekly-operating-review-agent](https://github.com/shubham1502-hue/founder-weekly-operating-review-agent) to roll product decisions into weekly review.
- Use [board-pack-investor-update-agent](https://github.com/shubham1502-hue/board-pack-investor-update-agent) for investor narrative.
- Use [founder-ai-workflow-roi-os](https://github.com/shubham1502-hue/founder-ai-workflow-roi-os) if feedback tagging, routing, summaries, or roadmap reporting should be automated.
- Use [startup-metrics-playbook](https://github.com/shubham1502-hue/startup-metrics-playbook) to define product and customer metrics before using them in roadmap decisions.
- Use [founder-os](https://github.com/shubham1502-hue/founder-os) as the umbrella operating system.

## Input format

Replace `data/sample_product_feedback.csv` with a CSV containing these required columns:

| Column | What it means |
| --- | --- |
| feedback_id | Unique feedback item ID |
| feedback_date | Date the signal was captured |
| source | Source such as sales call, onboarding, support, retention review, expansion review, demo, or founder observation |
| source_detail | Short context for the source |
| customer_name | Customer or prospect name |
| segment | Customer segment |
| industry | Customer industry |
| account_value | Annual contract value or estimated opportunity value |
| lifecycle_stage | Sales, demo, onboarding, activation, support, retention, renewal, or expansion |
| feedback_type | Product gap, feature request, bug, objection, support issue, churn driver, expansion ask, proof signal, or workflow pain |
| feedback_theme | Normalized theme used for clustering |
| feedback_text | Plain-language feedback |
| product_area | Product area affected |
| requested_feature | Feature or capability requested |
| severity | Critical, High, Medium, or Low |
| frequency_signal | Widespread, Repeated, Some, or Single |
| revenue_blocked | Estimated revenue blocked by the issue |
| retention_risk | Critical, High, Medium, Low, or None |
| expansion_potential | High, Medium, Low, or None |
| strategic_alignment | High, Medium, Low, or Outside |
| customer_urgency | High, Medium, or Low |
| workaround_available | Yes, Partial, or No |
| implementation_effort | Low, Medium, High, or Very high |
| confidence_level | High, Medium, or Low |
| owner | Current owner if known |
| current_status | New, Candidate, Discovery, Planned, Needs validation, Non-product fix, or Defer |
| next_step | Current next step |
| notes | Extra context |

The included sample dataset is synthetic and fictionalized.

## Output files

Open `outputs/founder_roadmap_memo.md` first.

- `outputs/roadmap_priority_scorecard.csv`: ranked feedback item scorecard with decisions, owners, and next actions.
- `outputs/product_gap_summary.csv`: grouped product gaps with account impact, revenue blocked, retention risk, expansion potential, suggested resolution, and owner role.
- `outputs/roadmap_decision_queue.csv`: prioritized queue of build, validate, and roadmap candidate decisions.
- `outputs/non_product_fix_queue.csv`: issues that should be solved through onboarding, sales narrative, support, documentation, training, CS, pricing, or rejection.
- `outputs/customer_signal_matrix.csv`: theme-level source mix, lifecycle stage mix, segment mix, signal strength, and decision implication.
- `outputs/account_feedback_view.csv`: customer-level view of top themes, revenue blocked, risk, expansion potential, and account action.
- `outputs/founder_roadmap_memo.md`: founder-ready summary of roadmap priorities, repeated themes, revenue blockers, retention gaps, expansion unlocks, noisy asks, non-product fixes, and next actions.
- `outputs/product_operating_review.md`: weekly product feedback review agenda with metrics, themes, decisions, discovery, owners, and tracker updates.
- `outputs/score_explanations.csv`: transparent explanation of why each item received its score and recommendation.

## How to trust the scores

The base workflow is deterministic. It does not call an LLM, use paid APIs, or hide a model behind the scoring.

- `config/scoring_rules.yml` contains the editable weights.
- `config/company_profile.yml` contains thresholds, target segments, roadmap capacity, product areas, and decision rules.
- `outputs/score_explanations.csv` explains the drivers behind every recommendation.
- Every score is generated from CSV fields and YAML rules.

| Recommendation | Founder interpretation |
| --- | --- |
| Build now | Strong score, strong strategic fit, and enough revenue, retention, expansion, urgency, or repeated signal to use roadmap capacity |
| Validate with customers | Promising signal, but scope, confidence, or pattern still needs customer discovery |
| Add to roadmap candidate list | Worth tracking, but not urgent or repeated enough for this cycle |
| Solve with onboarding | The issue is better handled through setup, handoff, training, or activation process before product scope |
| Solve with sales narrative | The issue is mainly positioning, expectation setting, proof, or sales explanation |
| Solve with support process | The issue is better handled through support, documentation, training, or CS playbook |
| Defer | The item is not strong enough for current roadmap capacity |
| Reject | The ask is too niche, low-fit, or outside the company strategy |

Owner recommendations are also deterministic:

- Product owns build-now roadmap work.
- Founder or Product owns customer validation.
- Customer Success owns onboarding and customer process fixes.
- Sales or Founder owns sales narrative fixes.
- Support or Customer Success owns support, documentation, and training fixes.
- Founder owns explicit reject calls when a customer ask could distract the roadmap.

## Example founder workflow

- Monday: Review founder roadmap memo
- Tuesday: Inspect roadmap decision queue
- Wednesday: Validate top customer problems
- Thursday: Assign product, CS, sales, or support owners
- Friday: Update weekly operating review and roadmap tracker

## Customization guide

Customize:
- Strategic themes
- Roadmap capacity
- Target segments
- Scoring weights
- Feedback sources
- Owner roles
- Non-product fix rules
- Output format

Start with `config/company_profile.yml`. Only edit `config/scoring_rules.yml` when the defaults do not match how your company makes roadmap tradeoffs.

## Why this matters

This is not a Productboard clone and it is not a generic product backlog. It is a founder operating system for deciding which customer signals deserve roadmap attention, which need validation, which should be solved outside product, which should be deferred, and which should be rejected.

## Roadmap

- Google Sheets export
- Notion export
- Linear/Jira sync
- Productboard sync
- Intercom/Zendesk import
- CRM feedback import
- Slack feedback intake
- LLM-assisted feedback clustering
- Customer interview question generator
- Roadmap change log
- Product strategy memo export

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License. See [LICENSE](LICENSE).

## Built by

Built by Shubham Singh, a founder-facing operator focused on RevOps, GTM systems, startup metrics, AI workflows, and operating systems for early-stage teams.
