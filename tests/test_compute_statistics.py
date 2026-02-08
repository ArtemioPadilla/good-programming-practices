"""TDD tests for P1 — computeStatistics.py

Written *before* the implementation exists.  Every test runs the program
as a subprocess, parses the output file, and compares to expected results.
"""

import os

import pytest

from tests.conftest import run_program, run_pylint, parse_p1_expected, ROOT_DIR

PROGRAM = os.path.join(ROOT_DIR, "P1", "source", "computeStatistics.py")
TESTS_DIR = os.path.join(ROOT_DIR, "P1", "tests")
EXPECTED = parse_p1_expected()

# Tolerance for floating-point comparisons
REL_TOL = 1e-4


def _parse_statistics_file(filepath):
    """Parse ``StatisticsResults.txt`` into ``{metric: raw_string}``.

    Accepts both ``KEY: value`` and ``KEY\\tvalue`` separators.
    """
    results = {}
    with open(filepath, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            for sep in (":", "\t"):
                if sep in line:
                    key, _, val = line.partition(sep)
                    key = key.strip().upper()
                    val = val.strip()
                    if key in (
                        "COUNT", "MEAN", "MEDIAN", "MODE",
                        "SD", "VARIANCE",
                        "STANDARD DEVIATION", "STD DEV",
                    ):
                        # Normalise alternative names
                        if key in ("STANDARD DEVIATION", "STD DEV"):
                            key = "SD"
                        results[key] = val
                    break
    return results


# ------------------------------------------------------------------
# Functional correctness — one test per TC
# ------------------------------------------------------------------

@pytest.mark.parametrize("tc", range(1, 8))
def test_functional_correctness(tc, tmp_path):
    """computeStatistics TC{tc}: output matches expected statistics."""
    input_file = os.path.join(TESTS_DIR, f"TC{tc}.txt")
    assert os.path.isfile(input_file), f"{input_file} not found"

    result = run_program(PROGRAM, input_file, working_dir=str(tmp_path))
    assert result.returncode == 0, (
        f"Program exited with code {result.returncode}\n"
        f"stderr: {result.stderr}"
    )

    output_file = tmp_path / "StatisticsResults.txt"
    assert output_file.exists(), "StatisticsResults.txt was not created"

    actual = _parse_statistics_file(str(output_file))
    expected = EXPECTED[tc]

    # COUNT
    assert float(actual["COUNT"]) == float(expected["COUNT"]), (
        f"TC{tc} COUNT mismatch"
    )

    # MEAN
    assert float(actual["MEAN"]) == pytest.approx(
        float(expected["MEAN"]), rel=REL_TOL
    ), f"TC{tc} MEAN mismatch"

    # MEDIAN
    assert float(actual["MEDIAN"]) == pytest.approx(
        float(expected["MEDIAN"]), rel=REL_TOL
    ), f"TC{tc} MEDIAN mismatch"

    # MODE — may be #N/A
    exp_mode = expected["MODE"]
    if exp_mode == "#N/A":
        assert actual.get("MODE", "").upper() in (
            "N/A", "#N/A", "NA", "NO MODE",
        ), f"TC{tc} MODE: expected N/A, got {actual.get('MODE')}"
    else:
        assert float(actual["MODE"]) == pytest.approx(
            float(exp_mode), rel=REL_TOL
        ), f"TC{tc} MODE mismatch"

    # SD (Population Standard Deviation)
    assert float(actual["SD"]) == pytest.approx(
        float(expected["SD"]), rel=REL_TOL
    ), f"TC{tc} SD mismatch"

    # VARIANCE (Population Variance)
    assert float(actual["VARIANCE"]) == pytest.approx(
        float(expected["VARIANCE"]), rel=REL_TOL
    ), f"TC{tc} VARIANCE mismatch"


# ------------------------------------------------------------------
# Static analysis
# ------------------------------------------------------------------

def test_pylint_score():
    """computeStatistics.py must score 10.00/10 on pylint."""
    score = run_pylint(PROGRAM)
    assert score == pytest.approx(10.0), f"pylint score is {score}"
