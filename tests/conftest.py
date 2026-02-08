"""Shared fixtures and helpers for all test modules."""

import os
import subprocess

import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUX_DIR = os.path.join(ROOT_DIR, "aux")


def run_program(program_path, input_file, working_dir=None):
    """Run a Python program via subprocess.

    Returns the CompletedProcess with stdout, stderr, and returncode.
    The program runs with *working_dir* as cwd so output files land there.
    """
    if working_dir is None:
        working_dir = os.path.dirname(program_path)
    result = subprocess.run(
        ["python3", program_path, input_file],
        capture_output=True,
        text=True,
        cwd=working_dir,
        timeout=120,
    )
    return result


def run_pylint(program_path):
    """Run pylint on *program_path* and return the numeric score."""
    result = subprocess.run(
        ["pylint", program_path],
        capture_output=True,
        text=True,
        timeout=60,
    )
    for line in result.stdout.splitlines():
        if "Your code has been rated at" in line:
            score_str = line.split("rated at ")[1].split("/")[0]
            return float(score_str)
    return 0.0


# ---------------------------------------------------------------------------
# P1 expected-results parser
# ---------------------------------------------------------------------------

def parse_p1_expected():
    """Parse ``aux/P1/A4.2.P1.Results-errata.txt``.

    Returns ``{tc_number: {metric: raw_string}}``.
    *tc_number* is 1-7; *metric* is one of
    COUNT, MEAN, MEDIAN, MODE, SD, VARIANCE.
    """
    filepath = os.path.join(AUX_DIR, "P1", "A4.2.P1.Results-errata.txt")
    with open(filepath, encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh if ln.strip()]

    headers = lines[0].split("\t")
    tc_indices = {}
    for idx, header in enumerate(headers):
        if header.startswith("TC") and header != "TC":
            tc_indices[int(header[2:])] = idx

    result: dict[int, dict[str, str]] = {}
    for line in lines[1:]:
        parts = line.split("\t")
        metric = parts[0].strip()
        for tc_num, col_idx in tc_indices.items():
            if tc_num not in result:
                result[tc_num] = {}
            if col_idx < len(parts):
                result[tc_num][metric] = parts[col_idx].strip()
    return result


# ---------------------------------------------------------------------------
# P3 expected-results parser
# ---------------------------------------------------------------------------

def parse_p3_expected(tc_number):
    """Parse ``aux/P3/TC{tc_number}.Results.txt``.

    Returns ``(word_counts, grand_total)`` where *word_counts* is
    ``{word: count}`` and *grand_total* is an int.
    """
    filepath = os.path.join(AUX_DIR, "P3", f"TC{tc_number}.Results.txt")
    word_counts: dict[str, int] = {}
    grand_total = 0
    with open(filepath, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            label = parts[0].strip()
            value = parts[1].strip()
            if label in ("Row Labels", "(blank)", "") or not value:
                continue
            if label == "Grand Total":
                grand_total = int(value)
            else:
                word_counts[label] = int(value)
    return word_counts, grand_total
