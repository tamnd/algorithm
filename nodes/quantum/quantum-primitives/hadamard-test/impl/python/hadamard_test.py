# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hadamard-test/. The authors are listed in prov/N1NJ1H.jsonl.
"""Entry point for the Hadamard test, under the file name of the slug.

The code is in hadamard.py. A file name that ends in "_test" is read as a test file by the tools,
so the line markers of the pseudocode live in hadamard.py.
"""

from hadamard import (
    expectation,
    hadamard_test_exact,
    hadamard_test_sampled,
    hadamard_test_state,
    hoeffding_radius,
    shots_for,
)

__all__ = [
    "expectation",
    "hadamard_test_exact",
    "hadamard_test_sampled",
    "hadamard_test_state",
    "hoeffding_radius",
    "shots_for",
]
