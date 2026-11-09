# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bdd-quantification/. The authors are listed in prov/8DCSXX.jsonl.

import random

from bdd_quantification import AND, BDD, FALSE, OR, TRUE


def rtable(rng: random.Random, n: int) -> list[int]:
    return [rng.randrange(2) for _ in range(1 << n)]


def brute(table: list[int], n: int, xs: set[int], use_all: bool) -> list[int]:
    out = []
    mask = sum(1 << i for i in xs)
    for a in range(1 << n):
        base = a & ~mask
        vals = []
        sub = mask
        while True:  # all subsets of mask
            vals.append(table[base | sub])
            if sub == 0:
                break
            sub = (sub - 1) & mask
        out.append(int(all(vals)) if use_all else int(any(vals)))
    return out


def check_reduced(b: BDD) -> None:
    seen = set()
    for u in range(2, len(b.nodes)):
        v, lo, hi = b.nodes[u]
        assert lo != hi and (v, lo, hi) not in seen
        assert v < b.var(lo) and v < b.var(hi)
        seen.add((v, lo, hi))


def test_small_example() -> None:
    # f = (x0 AND x1) OR (NOT x0 AND x2): exists x0 gives x1 OR x2, forall x0 gives x1 AND x2.
    b = BDD(3)
    x0, x1, x2 = b.ithvar(0), b.ithvar(1), b.ithvar(2)
    f = b.apply(OR, b.apply(AND, x0, x1), b.apply(AND, b.neg(x0), x2))
    assert b.exists(f, {0}) == b.apply(OR, x1, x2)
    assert b.forall(f, {0}) == b.apply(AND, x1, x2)
    assert b.exists(f, {0, 1, 2}) == TRUE
    assert b.forall(f, {0, 1, 2}) == FALSE


def test_against_truth_tables() -> None:
    rng = random.Random(2024)
    for n in range(1, 11):
        b = BDD(n)
        for _ in range(4):
            t = rtable(rng, n)
            f = b.build(t)
            for _ in range(3):
                xs = {i for i in range(n) if rng.random() < 0.4}
                e, a = b.exists(f, xs), b.forall(f, xs)
                want_e, want_a = brute(t, n, xs, False), brute(t, n, xs, True)
                assert b.truth_table(e) == want_e and e == b.build(want_e)
                assert b.truth_table(a) == want_a and a == b.build(want_a)
        check_reduced(b)


def test_relational_product() -> None:
    rng = random.Random(1990)
    for n in range(1, 10):
        b = BDD(n)
        for _ in range(5):
            f, g = b.build(rtable(rng, n)), b.build(rtable(rng, n))
            xs = frozenset(i for i in range(n) if rng.random() < 0.5)
            assert b.and_exists(f, g, xs) == b.exists(b.apply(AND, f, g), set(xs))


def test_edge_cases() -> None:
    b = BDD(4)
    f = b.build([0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0])
    assert b.exists(f, set()) == f and b.forall(f, set()) == f
    g = b.apply(AND, b.ithvar(1), b.ithvar(2))
    assert b.exists(g, {0, 3}) == g  # variables outside the support
    assert b.exists(FALSE, {0}) == FALSE and b.forall(TRUE, {0}) == TRUE


def eq_const(b: BDD, base: int, k: int, j: int) -> int:
    """The minterm that says the k address variables from base spell j."""
    m = TRUE
    for t in reversed(range(k)):
        v = b.ithvar(base + t)
        m = b.apply(AND, v if (j >> t) & 1 else b.neg(v), m)
    return m


def mux(b: BDD, base: int, k: int, data: int) -> int:
    """The data variable selected by k address variables from base."""
    r = FALSE
    for j in range(1 << k):
        r = b.apply(OR, r, b.apply(AND, eq_const(b, base, k, j), b.ithvar(data + j)))
    return r


def test_squaring_example() -> None:
    # Order: x, then the addresses a and b (k each), then the L = 2^k data variables.
    for k, want in [(1, 8), (2, 27), (3, 101), (4, 393), (5, 1553)]:
        size_l = 1 << k
        b = BDD(1 + 2 * k + size_l)
        ca = mux(b, 1, k, 1 + 2 * k)
        cb = mux(b, 1 + k, k, 1 + 2 * k)
        f = b.apply(OR, b.apply(AND, b.ithvar(0), ca), b.apply(AND, b.neg(b.ithvar(0)), cb))
        e = b.exists(f, {0})
        assert b.size(ca) == b.size(cb) == 2 * size_l + 1
        assert b.size(f) == 3 * size_l + 1
        assert b.size(e) == want == (3 * size_l * size_l + size_l + 2) // 2
        assert e == b.apply(OR, ca, cb)


def test_exponential_growth() -> None:
    # f = OR_i (s = i AND x_i AND y_i), order s, then x_1..x_m, then y_1..y_m, m = 2^s.
    # exists s f = x_1 y_1 OR ... OR x_m y_m, which needs 2^(m+1) nodes in this order.
    sizes = []
    for s in range(1, 4):
        m = 1 << s
        b = BDD(s + 2 * m)
        f = FALSE
        for i in range(m):
            term = b.apply(AND, b.ithvar(s + i), b.ithvar(s + m + i))
            f = b.apply(OR, f, b.apply(AND, eq_const(b, 0, s, i), term))
        e = b.exists(f, set(range(s)))
        assert b.size(e) == 2 ** (m + 1)
        sizes.append((b.size(f), b.size(e)))
    assert sizes == [(7, 8), (13, 32), (25, 512)]


def test_many_selectors() -> None:
    # s selector variables pick one of 2^s address blocks; all s are quantified.
    for s, k, want_f, want_e in [(1, 2, 13, 27), (2, 2, 21, 96), (2, 3, 41, 1091), (3, 3, 73, 6544)]:
        m, size_l = 1 << s, 1 << k
        b = BDD(s + m * k + size_l)
        data = s + m * k
        f = FALSE
        for t in range(m):
            block = mux(b, s + t * k, k, data)
            f = b.apply(OR, f, b.apply(AND, eq_const(b, 0, s, t), block))
        e = b.exists(f, set(range(s)))
        assert (b.size(f), b.size(e)) == (want_f, want_e)
