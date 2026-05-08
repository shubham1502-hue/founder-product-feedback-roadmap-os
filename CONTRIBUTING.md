# Contributing

Thanks for considering a contribution.

This project is designed to stay practical for founders and operators. Contributions should preserve the offline-first workflow, deterministic scoring, and simple CSV/YAML setup.

## Good contributions

- Clearer documentation for founders
- Better sample data coverage with synthetic and fictionalized records
- Additional tests for scoring, clustering, and reporting
- Safer validation and error messages
- Optional export formats that do not require paid APIs

## Guidelines

- Do not add emojis.
- Do not use em dash characters.
- Do not add private company data.
- Do not add fake production claims.
- Do not require an LLM for the base workflow.
- Do not add paid API dependencies to core functionality.
- Keep code readable for beginners.

## Local checks

Run:

```bash
make install
make test
make run
git diff --check
```
