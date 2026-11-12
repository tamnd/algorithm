# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/banded-smith-waterman/. The authors are listed in prov/HNEF8P.jsonl.

import random

import pytest

from banded_smith_waterman import banded_smith_waterman


def dna(match: int, mismatch: int):
    return lambda a, b: match if a == b else mismatch


def affine_score(row1, row2, s, d, e):
    total, prev = 0, None
    for a, b in zip(row1, row2):
        kind = "X" if b == "-" else "Y" if a == "-" else "M"
        if kind == "M":
            total += s(a, b)
        else:
            total -= e if kind == prev else d
        prev = kind
    return total


def local_alignments(x, y):
    """Yield (row1, row2, path) for every alignment of every pair of substrings.

    The path is the list of cells (i, j) that the alignment visits, start cell included.
    """
    for i0 in range(len(x) + 1):
        for j0 in range(len(y) + 1):
            stack = [(i0, j0, "", "", [(i0, j0)])]
            while stack:
                i, j, r1, r2, path = stack.pop()
                yield r1, r2, path
                if i < len(x) and j < len(y):
                    stack.append((i + 1, j + 1, r1 + x[i], r2 + y[j], path + [(i + 1, j + 1)]))
                if i < len(x):
                    stack.append((i + 1, j, r1 + x[i], r2 + "-", path + [(i + 1, j)]))
                if j < len(y):
                    stack.append((i, j + 1, r1 + "-", r2 + y[j], path + [(i, j + 1)]))


def brute(x, y, s, d, e, lo, hi):
    best = 0
    for r1, r2, path in local_alignments(x, y):
        if all(lo <= j - i <= hi for i, j in path):
            best = max(best, affine_score(r1, r2, s, d, e))
    return best


def check_result(x, y, s, d, e, lo, hi, res):
    score, r1, r2, i, j = res
    assert affine_score(r1, r2, s, d, e) == score
    if score == 0:
        assert (r1, r2, i, j) == ("", "", 0, 0)
        return
    a, b = r1.replace("-", ""), r2.replace("-", "")
    assert x[i - len(a):i] == a and y[j - len(b):j] == b
    # The path of the returned alignment stays in the band.
    ci, cj = i - len(a), j - len(b)
    assert lo <= cj - ci <= hi
    for p, q in zip(r1, r2):
        ci += p != "-"
        cj += q != "-"
        assert lo <= cj - ci <= hi


def test_page_example():
    s = dna(2, -3)
    x, y = "TTGACCTGAAT", "CCGACCTTGAAG"
    full = banded_smith_waterman(x, y, s, 5, 2, -len(x), len(y))
    assert full == (11, "GACC-TGAA", "GACCTTGAA", 10, 11)
    narrow = banded_smith_waterman(x, y, s, 5, 2, 0, 0)
    assert narrow == (10, "GACCT", "GACCT", 7, 7)
    assert banded_smith_waterman(x, y, s, 5, 2, -1, 1) == full
    assert banded_smith_waterman(x, y, s, 5, 2, 1, 3)[0] == 8


def test_edges():
    s = dna(1, -1)
    assert banded_smith_waterman("", "", s, 2, 1, 0, 0) == (0, "", "", 0, 0)
    assert banded_smith_waterman("AAA", "CCC", s, 2, 1, -3, 3) == (0, "", "", 0, 0)
    assert banded_smith_waterman("ACGT", "ACGT", s, 2, 1, 2, 1) == (0, "", "", 0, 0)
    assert banded_smith_waterman("ACGT", "ACGT", s, 2, 1, 0, 0)[0] == 4
    assert banded_smith_waterman("ACGT", "ACGT", s, 2, 1, 1, 3)[0] == 0
    with pytest.raises(ValueError):
        banded_smith_waterman("A", "A", s, 1, 2, 0, 0)


def test_against_brute_force():
    rng = random.Random(3)
    for _ in range(120):
        x = "".join(rng.choice("ACG") for _ in range(rng.randint(0, 4)))
        y = "".join(rng.choice("ACG") for _ in range(rng.randint(0, 4)))
        lo = rng.randint(-3, 2)
        hi = lo + rng.randint(0, 3)
        e = rng.randint(0, 2)
        d = e + rng.randint(0, 3)
        s = dna(rng.randint(1, 3), -rng.randint(1, 3))
        res = banded_smith_waterman(x, y, s, d, e, lo, hi)
        assert res[0] == brute(x, y, s, d, e, lo, hi)
        check_result(x, y, s, d, e, lo, hi, res)


def test_full_band_and_monotone():
    rng = random.Random(5)
    for _ in range(100):
        x = "".join(rng.choice("ACGT") for _ in range(rng.randint(1, 12)))
        y = "".join(rng.choice("ACGT") for _ in range(rng.randint(1, 12)))
        s = dna(2, -3)
        full = banded_smith_waterman(x, y, s, 5, 2, -len(x), len(y))[0]
        wide = banded_smith_waterman(x, y, s, 5, 2, -len(x) - 3, len(y) + 3)[0]
        assert full == wide
        prev = 0
        for w in range(0, max(len(x), len(y)) + 1):
            cur = banded_smith_waterman(x, y, s, 5, 2, -w, w)[0]
            assert prev <= cur <= full
            prev = cur
        assert prev == full


def test_band_can_miss_the_optimum():
    # The best local alignment needs a gap of length 3, so it leaves the band |j - i| <= 1.
    s = dna(2, -3)
    x, y = "ACGTACGTAC", "ACGTAGGGCGTAC"
    full = banded_smith_waterman(x, y, s, 3, 1, -len(x), len(y))
    narrow = banded_smith_waterman(x, y, s, 3, 1, -1, 1)
    assert full[0] == 15 and narrow[0] == 10
