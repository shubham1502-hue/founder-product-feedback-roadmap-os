# How To Fork And Use

This guide is written for non-technical founders and operators.

## Step 1: Fork the repo

Open the GitHub repo and click Fork. Rename it if you want the repo name to match your company.

## Step 2: Replace the sample CSV

Open:

```text
data/sample_product_feedback.csv
```

Replace the synthetic rows with your own product feedback tracker. Keep the same column names for the first run.

You can export feedback from a spreadsheet, CRM, CS tracker, support tool, product tracker, or your own notes.

## Step 3: Edit the company config

Open:

```text
config/company_profile.yml
```

Edit:

- Company stage
- Product motion
- Target segments
- Strategic product themes
- Roadmap capacity
- High-value threshold
- Revenue blocked threshold
- Review cadence

## Step 4: Optional scoring edits

Open:

```text
config/scoring_rules.yml
```

Only change this if you want to adjust how much the system weighs revenue impact, retention risk, expansion potential, frequency, urgency, effort, or confidence.

## Step 5: Run the system

From the repo folder, run:

```bash
make install
make run
```

## Step 6: Read outputs in order

Read these first:

1. `outputs/founder_roadmap_memo.md`
2. `outputs/roadmap_decision_queue.csv`
3. `outputs/product_gap_summary.csv`
4. `outputs/non_product_fix_queue.csv`
5. `outputs/score_explanations.csv`

## Step 7: Make decisions

Use the outputs to decide:

- Build now
- Validate with customers
- Add to roadmap candidate list
- Solve with onboarding
- Solve with sales narrative
- Solve with support process
- Defer
- Reject
