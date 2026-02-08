"""TDD tests for P3 — wordCount.py

Written *before* the implementation exists.  Each test runs the program,
parses the output file, and compares word frequencies to expected results.
"""

import os

import pytest

from tests.conftest import run_program, run_pylint, parse_p3_expected, ROOT_DIR

PROGRAM = os.path.join(ROOT_DIR, "P3", "source", "wordCount.py")
TESTS_DIR = os.path.join(ROOT_DIR, "P3", "tests")


def _parse_word_count_output(filepath):
    """Parse ``WordCountResults.txt``.

    Returns ``(word_counts, grand_total)`` where *word_counts* is
    ``{word: count}`` and *grand_total* is ``int | None``.
    """
    word_counts: dict[str, int] = {}
    grand_total = None
    with open(filepath, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line.strip() or line.lower().startswith("elapsed time"):
                continue
            for sep in ("\t", ":"):
                if sep in line:
                    parts = line.split(sep, 1)
                    label = parts[0].strip()
                    value = parts[1].strip()
                    if not value:
                        break
                    if label.lower() in ("row labels", "word", ""):
                        break  # header row
                    if label.lower() == "grand total":
                        grand_total = int(value)
                    else:
                        word_counts[label] = int(value)
                    break
    return word_counts, grand_total


# ------------------------------------------------------------------
# Functional correctness — one test per TC
# ------------------------------------------------------------------

@pytest.mark.parametrize("tc", range(1, 6))
def test_functional_correctness(tc, tmp_path):
    """wordCount TC{tc}: word frequencies match expected results."""
    input_file = os.path.join(TESTS_DIR, f"TC{tc}.txt")
    assert os.path.isfile(input_file), f"{input_file} not found"

    result = run_program(PROGRAM, input_file, working_dir=str(tmp_path))
    assert result.returncode == 0, (
        f"Program exited with code {result.returncode}\n"
        f"stderr: {result.stderr}"
    )

    output_file = tmp_path / "WordCountResults.txt"
    assert output_file.exists(), "WordCountResults.txt was not created"

    actual_counts, actual_total = _parse_word_count_output(str(output_file))
    expected_counts, expected_total = parse_p3_expected(tc)

    # Every expected word must be present with the right count
    for word, exp_count in expected_counts.items():
        assert word in actual_counts, (
            f"TC{tc}: word '{word}' missing from output"
        )
        assert actual_counts[word] == exp_count, (
            f"TC{tc}: word '{word}' — "
            f"expected {exp_count}, got {actual_counts[word]}"
        )

    # No unexpected extra words
    for word in actual_counts:
        assert word in expected_counts, (
            f"TC{tc}: unexpected word '{word}' in output"
        )

    # Grand total
    if expected_total and actual_total is not None:
        assert actual_total == expected_total, (
            f"TC{tc}: Grand Total — "
            f"expected {expected_total}, got {actual_total}"
        )


# ------------------------------------------------------------------
# Static analysis
# ------------------------------------------------------------------

def test_pylint_score():
    """wordCount.py must score 10.00/10 on pylint."""
    score = run_pylint(PROGRAM)
    assert score == pytest.approx(10.0), f"pylint score is {score}"
