# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semi-global-dp/. The authors are listed in prov/GQAPYM.jsonl.

import random
from typing import Iterator

from semi_global_dp import GAP, match_mismatch, semi_global_dp, semi_global_score

TOY = match_mismatch(2, -1)


def all_alignments(x: str, y: str) -> Iterator[tuple[str, str]]:
    """Every global alignment of x and y, as (top, bottom) rows."""
    if not x and not y:
        yield "", ""
        return
    if x and y:
        for t, b in all_alignments(x[1:], y[1:]):
            yield x[0] + t, y[0] + b
    if x:
        for t, b in all_alignments(x[1:], y):
            yield x[0] + t, GAP + b
    if y:
        for t, b in all_alignments(x, y[1:]):
            yield GAP + t, y[0] + b


def check(x: str, y: str, s, d: int, flags: tuple[bool, ...], result: tuple[int, str, str]) -> None:
    score, top, bottom = result
    assert len(top) == len(bottom)
    assert top.replace(GAP, "") == x
    assert bottom.replace(GAP, "") == y
    assert semi_global_score(top, bottom, s, d, *flags) == score


def test_worked_examples() -> None:
    overlap = (True, False, False, True)
    assert semi_global_dp("TTCAGTAC", "AGTACGGA", TOY, 2, *overlap) == (10, "TTCAGTAC---", "---AGTACGGA")
    fitting = (True, True, False, False)
    assert semi_global_dp("CAGGTACT", "TAGTAC", TOY, 2, *fitting) == (7, "CAGGTACT", "TA-GTAC-")
    assert semi_global_dp("CAGGTACT", "TAGTAC", TOY, 2)[0] == 5


def test_edges() -> None:
    every = (True, True, True, True)
    assert semi_global_dp("", "", TOY, 2, *every) == (0, "", "")
    assert semi_global_dp("ACG", "", TOY, 2, True) == (0, "ACG", "---")
    assert semi_global_dp("ACG", "", TOY, 2, False, True) == (0, "ACG", "---")
    assert semi_global_dp("ACG", "", TOY, 2) == (-6, "ACG", "---")
    assert semi_global_dp("", "AC", TOY, 2, *every) == (0, "--", "AC")
    assert semi_global_dp("AAAA", "CCCC", TOY, 2, *every)[0] == 0


def test_against_brute_force() -> None:
    rng = random.Random(1974)
    for _ in range(600):
        x = "".join(rng.choice("ACG") for _ in range(rng.randrange(6)))
        y = "".join(rng.choice("ACG") for _ in range(rng.randrange(6)))
        flags = tuple(rng.random() < 0.5 for _ in range(4))
        s = match_mismatch(rng.randrange(0, 4), rng.randrange(-4, 1))
        d = rng.randrange(0, 5)
        result = semi_global_dp(x, y, s, d, *flags)
        want = max(semi_global_score(t, b, s, d, *flags) for t, b in all_alignments(x, y))
        assert result[0] == want
        check(x, y, s, d, flags, result)


def test_fitting_against_substrings() -> None:
    # Fitting y into x equals the best global alignment of y with a substring of x.
    rng = random.Random(3)
    for _ in range(150):
        x = "".join(rng.choice("ACGT") for _ in range(rng.randrange(7)))
        y = "".join(rng.choice("ACGT") for _ in range(rng.randrange(4)))
        best = None
        for a in range(len(x) + 1):
            for b in range(a, len(x) + 1):
                v = max(semi_global_score(t, u, TOY, 2) for t, u in all_alignments(x[a:b], y))
                best = v if best is None else max(best, v)
        assert semi_global_dp(x, y, TOY, 2, True, True)[0] == best
