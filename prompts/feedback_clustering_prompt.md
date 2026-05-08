# Feedback Clustering Prompt

Use this prompt manually with your own exported CSV or the generated outputs. The base repo does not require AI.

Prompt:

You are helping a founder review product feedback. I will paste feedback items with customer segment, lifecycle stage, feedback theme, product area, requested feature, revenue blocked, retention risk, expansion potential, and notes.

Cluster the feedback into practical product themes. For each cluster, return:

- Cluster name
- Feedback items included
- Customer segments affected
- Lifecycle stages affected
- Revenue blocked
- Retention risk
- Expansion potential
- Whether this is a product issue or should be solved outside product
- Recommended next action

Use concise founder-facing language. Do not invent facts beyond the data.
