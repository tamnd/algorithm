# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/needleman-wunsch/. The authors are listed in prov/2FKWQD.jsonl.

import random
from typing import Iterator

from needleman_wunsch import GAP, alignment_score, match_mismatch, needleman_wunsch

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


def check_valid(x: str, y: str, top: str, bottom: str) -> None:
    assert len(top) == len(bottom)
    assert top.replace(GAP, "") == x
    assert bottom.replace(GAP, "") == y
    assert all(not (a == GAP and b == GAP) for a, b in zip(top, bottom))


def test_worked_example() -> None:
    assert needleman_wunsch("ACGTC", "AGTAC", TOY, 2) == (4, "ACGT-C", "A-GTAC")


def test_edges() -> None:
    assert needleman_wunsch("", "", TOY, 2) == (0, "", "")
    assert needleman_wunsch("ACG", "", TOY, 2) == (-6, "ACG", "---")
    assert needleman_wunsch("", "TT", TOY, 2) == (-4, "--", "TT")
    assert needleman_wunsch("A", "A", TOY, 2) == (2, "A", "A")
    assert needleman_wunsch("AAAA", "AAAA", TOY, 2) == (8, "AAAA", "AAAA")
    # A mismatch (-1) is better than two gaps (-4).
    assert needleman_wunsch("A", "C", TOY, 2) == (-1, "A", "C")
    # With a mismatch of -5, two gaps (-4) win.
    assert needleman_wunsch("A", "C", match_mismatch(2, -5), 2)[0] == -4


def test_number_of_alignments_is_delannoy() -> None:
    want = {(1, 1): 3, (2, 2): 13, (3, 3): 63, (4, 4): 321, (3, 5): 231}
    for (m, n), count in want.items():
        assert sum(1 for _ in all_alignments("A" * m, "C" * n)) == count


def test_against_brute_force() -> None:
    rng = random.Random(1970)
    for _ in range(500):
        x = "".join(rng.choice("ACGT") for _ in range(rng.randrange(6)))
        y = "".join(rng.choice("ACGT") for _ in range(rng.randrange(6)))
        match = rng.randrange(0, 4)
        mismatch = rng.randrange(-4, 1)
        d = rng.randrange(0, 5)
        s = match_mismatch(match, mismatch)
        best, top, bottom = needleman_wunsch(x, y, s, d)
        want = max(alignment_score(t, b, s, d) for t, b in all_alignments(x, y))
        assert best == want
        check_valid(x, y, top, bottom)
        assert alignment_score(top, bottom, s, d) == best


def test_general_matrix_against_brute_force() -> None:
    rng = random.Random(48)
    alphabet = "ACDE"
    for _ in range(200):
        table = {(a, b): rng.randrange(-5, 6) for a in alphabet for b in alphabet}
        s = lambda a, b, t=table: t[a, b]
        x = "".join(rng.choice(alphabet) for _ in range(rng.randrange(5)))
        y = "".join(rng.choice(alphabet) for _ in range(rng.randrange(5)))
        d = rng.randrange(-1, 6)
        best, top, bottom = needleman_wunsch(x, y, s, d)
        assert best == max(alignment_score(t, b, s, d) for t, b in all_alignments(x, y))
        check_valid(x, y, top, bottom)
        assert alignment_score(top, bottom, s, d) == best


def lcs_length(x: str, y: str) -> int:
    best = 0
    for mask in range(1 << len(x)):
        sub = "".join(x[i] for i in range(len(x)) if mask >> i & 1)
        it = iter(y)
        if all(c in it for c in sub):
            best = max(best, len(sub))
    return best


def test_special_cases_lcs_and_edit_distance() -> None:
    rng = random.Random(7)
    for _ in range(200):
        x = "".join(rng.choice("AB") for _ in range(rng.randrange(8)))
        y = "".join(rng.choice("AB") for _ in range(rng.randrange(8)))
        assert needleman_wunsch(x, y, match_mismatch(1, 0), 0)[0] == lcs_length(x, y)
        # Unit edit costs: the best score is minus the Levenshtein distance.
        prev = list(range(len(y) + 1))
        for i in range(1, len(x) + 1):
            cur = [i] + [0] * len(y)
            for j in range(1, len(y) + 1):
                cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x[i - 1] != y[j - 1]))
            prev = cur
        assert needleman_wunsch(x, y, match_mismatch(0, -1), 1)[0] == -prev[len(y)]
