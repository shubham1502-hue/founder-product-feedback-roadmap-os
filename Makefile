PYTHON ?= python3

.PHONY: install run demo test clean

install:
	$(PYTHON) -m pip install -e ".[dev]"

run:
	$(PYTHON) -m founder_product_roadmap.cli run --input data/sample_product_feedback.csv --company-config config/company_profile.yml --scoring-config config/scoring_rules.yml --output-dir outputs

demo:
	$(PYTHON) -m founder_product_roadmap.cli demo

test:
	$(PYTHON) -m pytest

clean:
	rm -f outputs/*.csv outputs/*.md
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
