# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sankoff-rna-algorithm/. The authors are listed in prov/XKWWEX.jsonl.

import random

from sankoff_rna_algorithm import GAP, can_pair, sankoff, score_solution


def all_alignments(x: str, y: str):
    """Yield every alignment of x and y as a list of columns."""
    stack = [(0, 0, [])]
    while stack:
        i, j, cols = stack.pop()
        if i == len(x) and j == len(y):
            yield cols
            continue
        if i < len(x):
            stack.append((i + 1, j, cols + [(x[i], GAP, i, None)]))
        if j < len(y):
            stack.append((i, j + 1, cols + [(GAP, y[j], None, j)]))
        if i < len(x) and j < len(y):
            stack.append((i + 1, j + 1, cols + [(x[i], y[j], i, j)]))


def all_structures(cols, hmin):
    """Return every nested set of consensus pairs on the columns, as lists of (c1, c2)."""
    memo = {}

    def rec(a, b):
        if (a, b) in memo:
            return memo[(a, b)]
        if a >= b:
            return [[]]
        out = [s for s in rec(a + 1, b)]
        xa, ya, ia, ka = cols[a]
        if xa != GAP and ya != GAP:
            for c in range(a + 1, b):
                xc, yc, ic, kc = cols[c]
                if xc == GAP or yc == GAP:
                    continue
                if not (can_pair(xa, xc) and can_pair(ya, yc)):
                    continue
                if ic - ia - 1 < hmin or kc - ka - 1 < hmin:
                    continue
                for s1 in rec(a + 1, c):
                    for s2 in rec(c + 1, b):
                        out.append([(a, c)] + s1 + s2)
        memo[(a, b)] = out
        return out

    return rec(0, len(cols))


def brute(x, y, match, mismatch, d, bonus, hmin):
    best = None
    for cols in all_alignments(x, y):
        base = 0
        for a, b, _, _ in cols:
            base += -d if (a == GAP or b == GAP) else (match if a == b else mismatch)
        for s in all_structures(cols, hmin):
            v = base + bonus * len(s)
            if best is None or v > best:
                best = v
    return best


def check(x, y, **kw):
    score, top, bot, st = sankoff(x, y, **kw)
    assert top.replace(GAP, "") == x and bot.replace(GAP, "") == y
    assert score_solution(top, bot, st, **kw) == score
    return score, top, bot, st


def test_example() -> None:
    score, top, bot, st = check("GCAAGC", "CGAACG")
    assert score == 4
    assert (top, bot, st) == ("GCAAGC", "CGAACG", "((..))")
    # Without the pair bonus, the best alignment has gaps and score 0.
    assert sankoff("GCAAGC", "CGAACG", bonus=0)[0] == 0
    assert brute("GCAAGC", "CGAACG", 1, -1, 1, 0, 1) == 0


def test_edges() -> None:
    assert sankoff("", "") == (0, "", "", "")
    assert sankoff("A", "") == (-1, "A", "-", ".")
    assert sankoff("", "GU") == (-2, "--", "GU", "..")
    assert sankoff("A", "A")[0] == 1


def test_against_brute_force() -> None:
    rng = random.Random(1985)
    schemes = [
        dict(match=1, mismatch=-1, d=1, bonus=3, hmin=1),
        dict(match=2, mismatch=-1, d=2, bonus=1, hmin=0),
        dict(match=1, mismatch=0, d=1, bonus=4, hmin=0),
    ]
    for trial in range(60):
        kw = schemes[trial % 3]
        x = "".join(rng.choice("ACGU") for _ in range(rng.randint(0, 4)))
        y = "".join(rng.choice("ACGU") for _ in range(rng.randint(0, 4)))
        score, _, _, _ = check(x, y, **kw)
        assert score == brute(x, y, **kw), (x, y, kw)


def test_longer_runs_and_is_valid() -> None:
    rng = random.Random(7)
    for _ in range(3):
        x = "".join(rng.choice("ACGU") for _ in range(9))
        y = "".join(rng.choice("ACGU") for _ in range(9))
        check(x, y)
