# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bdd-compose/. The authors are listed in prov/SRJKH7.jsonl.

import random

from bdd_compose import BDD, FALSE, TRUE


def rtable(rng: random.Random, n: int) -> list[int]:
    return [rng.randrange(2) for _ in range(1 << n)]


def check_reduced(b: BDD) -> None:
    seen = set()
    for u in range(2, len(b.nodes)):
        v, lo, hi = b.nodes[u]
        assert lo != hi and (v, lo, hi) not in seen
        assert v < b.var(lo) and v < b.var(hi)
        seen.add((v, lo, hi))


def AND(b: BDD, f: int, g: int) -> int:
    return b.ite(f, g, FALSE)


def OR(b: BDD, f: int, g: int) -> int:
    return b.ite(f, TRUE, g)


def NOT(b: BDD, f: int) -> int:
    return b.ite(f, FALSE, TRUE)


def test_small_example() -> None:
    # f = x0 AND x2; put x1 OR x3 in place of x2: (x0 AND x1) OR (x0 AND x3).
    b = BDD(4)
    x = [b.ithvar(i) for i in range(4)]
    f = AND(b, x[0], x[2])
    r = b.compose(f, 2, OR(b, x[1], x[3]))
    assert r == OR(b, AND(b, x[0], x[1]), AND(b, x[0], x[3]))
    assert b.size(r) == 5


def test_restrict_against_truth_tables() -> None:
    rng = random.Random(44)
    for n in range(1, 9):
        b = BDD(n)
        t = rtable(rng, n)
        f = b.build(t)
        for i in range(n):
            for c in (0, 1):
                want = [t[(a & ~(1 << i)) | (c << i)] for a in range(1 << n)]
                r = b.restrict(f, i, c)
                assert r == b.build(want) and b.size(r) <= b.size(f)


def test_compose_against_truth_tables() -> None:
    rng = random.Random(1986)
    for n in range(1, 11):
        b = BDD(n)
        for _ in range(4):
            tf, tg = rtable(rng, n), rtable(rng, n)
            f, g = b.build(tf), b.build(tg)
            i = rng.randrange(n)
            r = b.compose(f, i, g)
            want = [tf[(a & ~(1 << i)) | (tg[a] << i)] for a in range(1 << n)]
            assert b.truth_table(r) == want
            assert r == b.build(want)
        check_reduced(b)


def test_cost_bound() -> None:
    rng = random.Random(9)
    for n in range(2, 9):
        b = BDD(n)
        f, g = b.build(rtable(rng, n)), b.build(rtable(rng, n))
        i = rng.randrange(n)
        b.cache.clear()
        b.ite_misses = 0
        r = b.compose(f, i, g)
        assert b.ite_misses <= b.size(f) ** 2 * b.size(g)
        assert b.size(r) <= b.size(f) ** 2 * b.size(g)


def test_special_cases() -> None:
    b = BDD(3)
    f = b.build([0, 1, 1, 1, 0, 0, 1, 0])
    x1 = b.ithvar(1)
    assert b.compose(f, 1, x1) == f  # x_i := x_i
    for c in (FALSE, TRUE):
        assert b.compose(f, 1, c) == b.restrict(f, 1, c)
    assert b.compose(x1, 1, f) == f  # x_i[x_i := g] = g


def eq_const(b: BDD, base: int, k: int, j: int) -> int:
    m = TRUE
    for t in reversed(range(k)):
        v = b.ithvar(base + t)
        m = AND(b, v if (j >> t) & 1 else NOT(b, v), m)
    return m


def mux(b: BDD, base: int, k: int, data: int) -> int:
    r = FALSE
    for j in range(1 << k):
        r = OR(b, r, AND(b, eq_const(b, base, k, j), b.ithvar(data + j)))
    return r


def test_quadratic_growth() -> None:
    # Order: x, addresses a and b, data d_0..d_{L-1}, z. f = x ? c_a : c_b, and x := z.
    for k, want in [(1, 15), (2, 47), (3, 159), (4, 575), (5, 2175)]:
        size_l = 1 << k
        n = 1 + 2 * k + size_l + 1
        b = BDD(n)
        ca, cb = mux(b, 1, k, 1 + 2 * k), mux(b, 1 + k, k, 1 + 2 * k)
        f = b.ite(b.ithvar(0), ca, cb)
        r = b.compose(f, 0, b.ithvar(n - 1))
        assert b.size(f) == 3 * size_l + 1
        assert b.size(r) == want == 2 * size_l * size_l + 4 * size_l - 1
