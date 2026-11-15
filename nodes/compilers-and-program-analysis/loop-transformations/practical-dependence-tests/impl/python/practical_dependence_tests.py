# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/practical-dependence-tests/. The authors are listed in prov/B1R5XX.jsonl.
"""Entry point named after the slug. The code is in subscript_dependence.py,
because the tools treat a file whose name ends in _tests as a test file."""

from subscript_dependence import (
    EMPTY,
    FREE,
    coupled_groups,
    delta_test,
    dependence,
    level_view,
    meet,
    siv_kind,
    siv_solve,
)

__all__ = [
    "EMPTY",
    "FREE",
    "coupled_groups",
    "delta_test",
    "dependence",
    "level_view",
    "meet",
    "siv_kind",
    "siv_solve",
]
