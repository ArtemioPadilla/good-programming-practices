PYTHON  ?= python3.11
PYLINT  ?= $(PYTHON) -m pylint
PYTEST  ?= $(PYTHON) -m pytest

P1_SRC  = P1/source/computeStatistics.py
P2_SRC  = P2/source/convertNumbers.py
P3_SRC  = P3/source/wordCount.py
SOURCES = $(P1_SRC) $(P2_SRC) $(P3_SRC)

.PHONY: all test test-p1 test-p2 test-p3 lint lint-p1 lint-p2 lint-p3 clean help

all: lint test

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "  all        Lint + test everything (default)"
	@echo "  lint       Run pylint on all programs"
	@echo "  lint-p1    Run pylint on computeStatistics.py"
	@echo "  lint-p2    Run pylint on convertNumbers.py"
	@echo "  lint-p3    Run pylint on wordCount.py"
	@echo "  test       Run all 20 pytest tests"
	@echo "  test-p1    Run P1 tests (7 TCs + pylint)"
	@echo "  test-p2    Run P2 tests (5 TCs + pylint)"
	@echo "  test-p3    Run P3 tests (5 TCs + pylint)"
	@echo "  clean      Remove output files and caches"

# ── Tests ──────────────────────────────────────────────────────────
test:
	$(PYTEST) tests/ -v

test-p1:
	$(PYTEST) tests/test_compute_statistics.py -v

test-p2:
	$(PYTEST) tests/test_convert_numbers.py -v

test-p3:
	$(PYTEST) tests/test_word_count.py -v

# ── Lint ───────────────────────────────────────────────────────────
lint:
	$(PYLINT) $(SOURCES)

lint-p1:
	$(PYLINT) $(P1_SRC)

lint-p2:
	$(PYLINT) $(P2_SRC)

lint-p3:
	$(PYLINT) $(P3_SRC)

# ── Cleanup ────────────────────────────────────────────────────────
clean:
	rm -f StatisticsResults.txt ConvertionResults.txt WordCountResults.txt
	rm -rf __pycache__ tests/__pycache__ .pytest_cache
