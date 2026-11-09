# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ite-operator/. The authors are listed in prov/X6QCE3.jsonl.

import random

from ite_operator import BDD, FALSE, TRUE


def rtable(rng: random.Random, n: int) -> list[int]:
    return [rng.randrange(2) for _ in range(1 << n)]


def check_reduced(b: BDD) -> None:
    seen = set()
    for u in range(2, len(b.nodes)):
        v, lo, hi = b.nodes[u]
        assert lo != hi and (v, lo, hi) not in seen
        assert v < b.var(lo) and v < b.var(hi)
        seen.add((v, lo, hi))


def test_example() -> None:
    # f = x0, g = x1, h = x2: ite is the multiplexer (x0 AND x1) OR (NOT x0 AND x2).
    b = BDD(3)
    r = b.ite(b.ithvar(0), b.ithvar(1), b.ithvar(2))
    assert b.size(r) == 5
    assert b.truth_table(r) == [(a >> 1 & 1) if a & 1 else (a >> 2 & 1) for a in range(8)]


def test_terminal_cases() -> None:
    b = BDD(2)
    x, y = b.ithvar(0), b.ithvar(1)
    assert b.ite(TRUE, x, y) == x and b.ite(FALSE, x, y) == y
    assert b.ite(x, y, y) == y and b.ite(x, TRUE, FALSE) == x
    assert b.ite(x, FALSE, TRUE) == b.build([1, 0, 1, 0])


def test_ite_against_truth_tables() -> None:
    rng = random.Random(1990)
    for n in range(1, 11):
        for normalize in (True, False):
            b = BDD(n, normalize)
            for _ in range(4):
                tf, tg, th = rtable(rng, n), rtable(rng, n), rtable(rng, n)
                f, g, h = b.build(tf), b.build(tg), b.build(th)
                r = b.ite(f, g, h)
                want = [tg[a] if tf[a] else th[a] for a in range(1 << n)]
                assert b.truth_table(r) == want
                assert r == b.build(want)  # canonical: the same node id
            check_reduced(b)


def test_all_sixteen_operators() -> None:
    rng = random.Random(16)
    n = 6
    b = BDD(n)
    tf, tg = rtable(rng, n), rtable(rng, n)
    f, g = b.build(tf), b.build(tg)
    for op in range(16):
        r = b.binop(op, f, g)
        assert b.truth_table(r) == [(op >> (2 * x + y)) & 1 for x, y in zip(tf, tg)]


def test_normalization_shares_work() -> None:
    rng = random.Random(3)
    n = 8
    for _ in range(10):
        tf, tg, th = rtable(rng, n), rtable(rng, n), rtable(rng, n)
        b = BDD(n)
        f, g, h = b.build(tf), b.build(tg), b.build(th)
        # The cache holds at most |f| |g| |h| triples (times a constant for the swaps).
        b.ite(f, g, h)
        assert b.calls <= b.size(f) * b.size(g) * b.size(h)
        # f AND g and g AND f are one cache entry after normalization.
        b.cache.clear()
        b.calls = 0
        r1 = b.ite(f, g, FALSE)
        c1 = b.calls
        r2 = b.ite(g, f, FALSE)
        assert r1 == r2 and b.calls == c1
        # ite(f, f, h) = f OR h.
        assert b.ite(f, f, h) == b.ite(f, TRUE, h)
        assert b.ite(f, g, f) == b.ite(f, g, FALSE)
