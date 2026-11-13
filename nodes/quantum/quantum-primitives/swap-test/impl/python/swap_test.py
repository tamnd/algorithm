# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swap-test/. The authors are listed in prov/P7XCAZ.jsonl.
"""The public module of the swap-test page.

The code, with its @line markers, is in swap_circuit.py. The tools read a file
whose name ends in _test.py as a test file, so the markers cannot be here.
"""

from swap_circuit import (
    bell_rotated,
    circuit,
    cnot,
    controlled_swap,
    destructive_probability_zero,
    destructive_swap_test,
    estimate_overlap,
    exact_overlap,
    final_state,
    num_qubits,
    overlap_by_destructive_test,
    probability_zero,
    probability_zero_mixed,
    runs_needed,
    sample_basis,
    singlet_parity,
    swap_test,
)

__all__ = [
    "bell_rotated",
    "circuit",
    "cnot",
    "controlled_swap",
    "destructive_probability_zero",
    "destructive_swap_test",
    "estimate_overlap",
    "exact_overlap",
    "final_state",
    "num_qubits",
    "overlap_by_destructive_test",
    "probability_zero",
    "probability_zero_mixed",
    "runs_needed",
    "sample_basis",
    "singlet_parity",
    "swap_test",
]
