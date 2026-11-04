# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knuth-plass-line-breaking/. The authors are listed in prov/RPQTNB.jsonl.

import itertools
import math
import random

from knuth_plass_line_breaking import INF, knuth_plass, paragraph_demerits

PARAMS = dict(line_penalty=10, flagged_demerits=3000, fitness_demerits=3000)


def legal(items, b):
    it = items[b]
    if it[0] == "penalty":
        return it[2] < INF
    return it[0] == "glue" and b > 0 and items[b - 1][0] == "box"


def line_measure(items, a, b):
    """Direct scan: natural width, stretch and shrink of the line a..b."""
    i = a + 1
    while i < b and not (items[i][0] == "box" or (items[i][0] == "penalty" and items[i][2] == -INF)):
        i += 1
    width = stretch = shrink = 0.0
    for it in items[i:b]:
        if it[0] == "box":
            width += it[1]
        elif it[0] == "glue":
            width += it[1]
            stretch += it[2]
            shrink += it[3]
    if items[b][0] == "penalty":
        width += items[b][1]
    return width, stretch, shrink


def fit_class(r):
    return 0 if r < -0.5 else 1 if r <= 0.5 else 2 if r <= 1 else 3


def brute_cost(items, line_width, breaks, tolerance, line_penalty, flagged_demerits, fitness_demerits):
    total, a, prev_fit = 0.0, -1, 1
    for b in breaks:
        width, stretch, shrink = line_measure(items, a, b)
        if width < line_width:
            r = (line_width - width) / stretch if stretch > 0 else INF
        elif width > line_width:
            r = (line_width - width) / shrink if shrink > 0 else -INF
        else:
            r = 0.0
        bad = min(100 * abs(r) ** 3, 10000.0)
        if r < -1 or bad > tolerance:
            return None
        p = items[b][2] if items[b][0] == "penalty" else 0
        if p >= 0:
            d = (line_penalty + bad) ** 2 + p * p
        elif p > -INF:
            d = (line_penalty + bad) ** 2 - p * p
        else:
            d = (line_penalty + bad) ** 2
        if a >= 0 and items[a][0] == "penalty" and items[a][3] and items[b][0] == "penalty" and items[b][3]:
            d += flagged_demerits
        if abs(fit_class(r) - prev_fit) > 1:
            d += fitness_demerits
        total += d
        a, prev_fit = b, fit_class(r)
    return total


def brute(items, line_width, tolerance=INF, **kw):
    kw = {**PARAMS, **kw}
    m = len(items)
    cand = [b for b in range(m - 1) if legal(items, b)]
    forced = [b for b in cand if items[b][0] == "penalty" and items[b][2] == -INF]
    free = [b for b in cand if b not in forced]
    best = None
    for k in range(len(free) + 1):
        for sub in itertools.combinations(free, k):
            breaks = sorted(set(sub) | set(forced)) + [m - 1]
            c = brute_cost(items, line_width, breaks, tolerance, **kw)
            if c is not None and (best is None or c < best):
                best = c
    return best


def close(x, y):
    return math.isclose(x, y, rel_tol=1e-9, abs_tol=1e-6)


def check(items, line_width, tolerance=INF, **kw):
    got = knuth_plass(items, line_width, tolerance, **{**PARAMS, **kw})
    want = brute(items, line_width, tolerance, **kw)
    if want is None:
        assert got is None
        return
    assert got is not None
    total, breaks = got
    assert close(total, want)
    assert breaks[-1] == len(items) - 1
    assert all(legal(items, b) for b in breaks)
    assert close(brute_cost(items, line_width, breaks, tolerance, **{**PARAMS, **kw}), total)
    assert close(paragraph_demerits(items, line_width, breaks, tolerance, **{**PARAMS, **kw}), total)


def words_to_items(words, space=(1, 1, 1)):
    items = []
    for k, word in enumerate(words):
        if k > 0:
            items.append(("glue",) + space)
        items.append(("box", len(word)))
    items.append(("penalty", 0, INF, False))
    items.append(("glue", 0, INF, 0))
    items.append(("penalty", 0, -INF, False))
    return items


def test_example() -> None:
    words = "Dynamic programming finds the best way to break a paragraph into lines".split()
    items = words_to_items(words)
    total, breaks = knuth_plass(items, 19)
    assert breaks == [3, 11, 19, len(items) - 1]  # after programming, way, paragraph
    assert close(total, 2 * 100 + 2 * (10 + 100 / 27) ** 2)
    assert close(total, brute(items, 19))


def test_single_line_and_infeasible() -> None:
    items = words_to_items(["ab", "cd"])
    assert knuth_plass(items, 10) is not None
    assert knuth_plass(items, 10)[1] == [len(items) - 1]
    rigid = words_to_items(["abcdef", "gh"], space=(1, 0, 0))
    assert knuth_plass(rigid, 5) is None  # a box wider than the line
    check(rigid, 5)


def test_forced_break_inside() -> None:
    items = [("box", 3), ("glue", 1, 1, 1), ("box", 2), ("penalty", 0, -INF, False),
             ("box", 4), ("glue", 1, 1, 1), ("box", 3)] + words_to_items([])[-3:]
    total, breaks = knuth_plass(items, 7)
    assert 3 in breaks
    check(items, 7)


def random_paragraph(rng):
    items = []
    nwords = rng.randint(1, 7)
    for k in range(nwords):
        if k > 0:
            w = rng.randint(1, 3)
            items.append(("glue", w, rng.choice([0, 1, 2, 3]), rng.randint(0, w)))
        for s in range(rng.randint(1, 2)):
            if s > 0:
                items.append(("penalty", rng.choice([0, 1]), rng.choice([50, 100, -20]), True))
            items.append(("box", rng.randint(1, 6)))
        if rng.random() < 0.15:
            items.append(("penalty", 0, rng.choice([-50, 0, 30, INF]), rng.random() < 0.5))
        if rng.random() < 0.08 and k < nwords - 1:
            items.append(("penalty", 0, -INF, False))
    items.append(("penalty", 0, INF, False))
    items.append(("glue", 0, rng.choice([INF, 3]), 0))
    items.append(("penalty", 0, -INF, False))
    return items


def test_against_brute_force() -> None:
    rng = random.Random(1981)
    for _ in range(700):
        items = random_paragraph(rng)
        line_width = rng.randint(6, 24)
        tolerance = rng.choice([INF, 10000, 200, 1000, 50])
        kw = dict(
            line_penalty=rng.choice([0, 10, 100]),
            flagged_demerits=rng.choice([0, 3000, 10000]),
            fitness_demerits=rng.choice([0, 3000, 10000]),
        )
        check(items, line_width, tolerance, **kw)
