.PHONY: all format lint test clean


all: 
	uv run mcf_bordeaux.py

format:
	uv run black ./tikz_presentations_aliaume
	uv run black mcf_bordeaux.py

lint:
	uv run ruff check --config pyproject.toml .

test:
	echo "No tests defined yet"


clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf .coverage*
	rm -rf coverage_html_report
	rm -rf coverage_xml_report
	rm -rf coverage_json_report
	rm -rf coverage.txt
	rm -rf coverage.xml
	rm -rf coverage.json
	rm -rf coverage.html
	rm -rf .hypothesis/
	rm -rf .hypothesis/
	rm -f *.egg-info
	rm -f *.egg
	rm -f *.whl
	rm -f *.dist-info
	rm -f *.pyc
