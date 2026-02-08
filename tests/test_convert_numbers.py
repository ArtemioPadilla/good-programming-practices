"""TDD tests for P2 — convertNumbers.py

TC3/TC4 have expected results that align with their input files and are
compared exactly.  TC1/TC2 expected results come from different input data
(Excel export artifact), so we verify *internal consistency* — that each
row's binary and hex are mathematically correct for the value shown.
"""

import os

import pytest

from tests.conftest import run_program, run_pylint, ROOT_DIR

PROGRAM = os.path.join(ROOT_DIR, "P2", "source", "convertNumbers.py")
TESTS_DIR = os.path.join(ROOT_DIR, "P2", "tests")
AUX_P2 = os.path.join(ROOT_DIR, "aux", "P2")


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _parse_p2_expected_section(tc_number):
    """Extract expected rows for *tc_number* from the results file.

    Returns a list of ``(item, value_str, binary_str, hex_str)``.
    """
    filepath = os.path.join(AUX_P2, "A4.2.P2.Results.txt")
    results = []
    in_section = False

    with open(filepath, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("ITEM") and f"TC{tc_number}" in line:
                in_section = True
                continue
            if in_section:
                if not line.strip():
                    if results:
                        break
                    continue
                parts = line.split("\t")
                # TC1/TC2 have 5 columns (extra seed column)
                if len(parts) >= 5 and tc_number in (1, 2):
                    results.append((
                        int(parts[0]), parts[2], parts[3], parts[4],
                    ))
                elif len(parts) >= 4:
                    results.append((
                        int(parts[0]), parts[1], parts[2], parts[3],
                    ))
    return results


def _parse_conversion_output(filepath):
    """Parse ``ConvertionResults.txt``.

    Returns a list of dicts with keys *value*, *binary*, *hex*.
    """
    rows = []
    with open(filepath, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.upper().startswith("ITEM") or "time" in line.lower():
                continue
            parts = line.split("\t")
            if len(parts) >= 4:
                rows.append({
                    "value": parts[1].strip(),
                    "binary": parts[2].strip(),
                    "hex": parts[3].strip(),
                })
    return rows


def _verify_internal_consistency(value_str, binary_str, hex_str):
    """Assert binary/hex are correct representations of *value_str*."""
    if "#VALUE!" in binary_str or "#VALUE!" in hex_str:
        return  # invalid-data row — skip

    value = int(value_str)

    # Binary check
    if value >= 0:
        expected_bin = format(value, "b") if value != 0 else "0"
    else:
        expected_bin = format(value & 0x3FF, "b")  # 10-bit two's complement

    assert binary_str.lstrip("0") == expected_bin.lstrip("0") or \
        binary_str == expected_bin, (
        f"Binary mismatch for {value}: expected {expected_bin}, "
        f"got {binary_str}"
    )

    # Hex check
    if value >= 0:
        expected_hex = format(value, "X") if value != 0 else "0"
    else:
        expected_hex = format(value & 0xFFFFFFFF, "X")

    assert hex_str.upper() == expected_hex, (
        f"Hex mismatch for {value}: expected {expected_hex}, "
        f"got {hex_str}"
    )


# ------------------------------------------------------------------
# TC3 & TC4 — exact match against expected results
# ------------------------------------------------------------------

@pytest.mark.parametrize("tc", [3, 4])
def test_functional_exact_match(tc, tmp_path):
    """convertNumbers TC{tc}: output rows match expected binary/hex."""
    input_file = os.path.join(TESTS_DIR, f"TC{tc}.txt")
    assert os.path.isfile(input_file)

    result = run_program(PROGRAM, input_file, working_dir=str(tmp_path))
    assert result.returncode == 0, f"stderr: {result.stderr}"

    output_file = tmp_path / "ConvertionResults.txt"
    assert output_file.exists(), "ConvertionResults.txt was not created"

    expected = _parse_p2_expected_section(tc)
    actual = _parse_conversion_output(str(output_file))

    # Only compare valid (non-#VALUE!) rows
    valid_expected = [
        (item, val, b, h)
        for item, val, b, h in expected
        if "#VALUE!" not in b
    ]
    valid_actual = [
        r for r in actual
        if "error" not in r.get("binary", "").lower()
        and "#VALUE!" not in r.get("binary", "")
    ]

    assert len(valid_actual) == len(valid_expected), (
        f"TC{tc}: expected {len(valid_expected)} valid rows, "
        f"got {len(valid_actual)}"
    )

    for (exp_item, _, exp_bin, exp_hex), act in zip(valid_expected, valid_actual):
        assert act["binary"] == exp_bin, (
            f"TC{tc} item {exp_item}: binary mismatch "
            f"(expected {exp_bin}, got {act['binary']})"
        )
        assert act["hex"].upper() == exp_hex.upper(), (
            f"TC{tc} item {exp_item}: hex mismatch "
            f"(expected {exp_hex}, got {act['hex']})"
        )


# ------------------------------------------------------------------
# TC1 & TC2 — internal consistency (results file ≠ input file)
# ------------------------------------------------------------------

@pytest.mark.parametrize("tc", [1, 2])
def test_functional_internal_consistency(tc, tmp_path):
    """convertNumbers TC{tc}: each output row is internally correct."""
    input_file = os.path.join(TESTS_DIR, f"TC{tc}.txt")
    assert os.path.isfile(input_file)

    result = run_program(PROGRAM, input_file, working_dir=str(tmp_path))
    assert result.returncode == 0, f"stderr: {result.stderr}"

    output_file = tmp_path / "ConvertionResults.txt"
    assert output_file.exists(), "ConvertionResults.txt was not created"

    actual = _parse_conversion_output(str(output_file))
    assert len(actual) > 0, "No output rows found"

    for row in actual:
        _verify_internal_consistency(row["value"], row["binary"], row["hex"])


# ------------------------------------------------------------------
# TC4 — invalid data handling
# ------------------------------------------------------------------

def test_invalid_data_handling(tmp_path):
    """convertNumbers TC4: program handles ABC/ERR/VAL without crashing."""
    input_file = os.path.join(TESTS_DIR, "TC4.txt")
    result = run_program(PROGRAM, input_file, working_dir=str(tmp_path))
    assert result.returncode == 0, (
        f"Program crashed on invalid data.\nstderr: {result.stderr}"
    )


# ------------------------------------------------------------------
# Static analysis
# ------------------------------------------------------------------

def test_pylint_score():
    """convertNumbers.py must score 10.00/10 on pylint."""
    score = run_pylint(PROGRAM)
    assert score == pytest.approx(10.0), f"pylint score is {score}"
