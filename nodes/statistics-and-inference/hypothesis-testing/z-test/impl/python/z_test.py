# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/z-test/. The authors are listed in prov/PZWGTN.jsonl.
"""Entry point named after the slug. The code lives in z_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from z_core import ALTERNATIVES, normal_p_value, proportion_z_test, two_sample_z_test, z_test

__all__ = ["ALTERNATIVES", "normal_p_value", "proportion_z_test", "two_sample_z_test", "z_test"]
