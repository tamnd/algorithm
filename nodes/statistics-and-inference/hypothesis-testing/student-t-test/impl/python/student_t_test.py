# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/student-t-test/. The authors are listed in prov/M2JJ9R.jsonl.
"""Entry point named after the slug. The code lives in student_t_core.py, because tools treat
a file whose name ends in _test.py as a test file and skip its @line markers."""

from student_t_core import (
    ALTERNATIVES, mean_and_ss, one_sample_t_test, paired_t_test, pooled_t_test, t_p_value,
)

__all__ = ["ALTERNATIVES", "mean_and_ss", "one_sample_t_test", "paired_t_test", "pooled_t_test",
           "t_p_value"]
