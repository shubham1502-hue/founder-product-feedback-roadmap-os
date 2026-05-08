from __future__ import annotations

import argparse
from pathlib import Path

from founder_product_roadmap.config import load_company_config, load_scoring_config
from founder_product_roadmap.ingest import load_feedback_csv
from founder_product_roadmap.reporting import write_outputs
from founder_product_roadmap.scoring import score_feedback
from founder_product_roadmap.utils import project_root


def run_workflow(input_path: str | Path, company_config_path: str | Path, scoring_config_path: str | Path, output_dir: str | Path) -> dict[str, Path]:
    company_config = load_company_config(company_config_path)
    scoring_config = load_scoring_config(scoring_config_path)
    feedback = load_feedback_csv(input_path)
    scored = score_feedback(feedback, company_config, scoring_config)
    return write_outputs(scored, company_config, output_dir)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Founder Product Feedback Roadmap OS")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the roadmap workflow on a CSV input.")
    run_parser.add_argument("--input", required=True, help="Path to product feedback CSV.")
    run_parser.add_argument("--company-config", required=True, help="Path to company profile YAML.")
    run_parser.add_argument("--scoring-config", required=True, help="Path to scoring rules YAML.")
    run_parser.add_argument("--output-dir", required=True, help="Directory for generated outputs.")

    subparsers.add_parser("demo", help="Run the workflow on the included synthetic sample data.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    root = project_root()
    if args.command == "demo":
        outputs = run_workflow(
            root / "data" / "sample_product_feedback.csv",
            root / "config" / "company_profile.yml",
            root / "config" / "scoring_rules.yml",
            root / "outputs",
        )
    else:
        outputs = run_workflow(args.input, args.company_config, args.scoring_config, args.output_dir)
    print("Generated outputs:")
    for output in outputs.values():
        print(f"- {output}")


if __name__ == "__main__":
    main()
