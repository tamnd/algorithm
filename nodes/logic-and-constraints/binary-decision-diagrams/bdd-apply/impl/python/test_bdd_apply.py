# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bdd-apply/. The authors are listed in prov/5A7H4K.jsonl.

import random

from bdd_apply import AND, BDD, FALSE, IMPLIES, OR, TRUE, XOR


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
    # (x0 AND x2) OR (x1 AND x2) = if x0 then x2 else (x1 AND x2).
    b = BDD(3)
    x0, x1, x2 = b.ithvar(0), b.ithvar(1), b.ithvar(2)
    f = b.apply(AND, x0, x2)
    g = b.apply(AND, x1, x2)
    r = b.apply(OR, f, g)
    assert b.nodes[r] == (0, g, x2)
    assert b.size(r) == 5


def test_operator_constants() -> None:
    for a in (0, 1):
        for c in (0, 1):
            k = 2 * a + c
            assert (AND >> k) & 1 == (a & c)
            assert (OR >> k) & 1 == (a | c)
            assert (XOR >> k) & 1 == (a ^ c)
            assert (IMPLIES >> k) & 1 == ((1 - a) | c)


def test_apply_against_truth_tables() -> None:
    rng = random.Random(1986)
    for n in range(1, 11):
        for use_cache in (True, False) if n <= 6 else (True,):
            for use_short in (True, False):
                b = BDD(n, use_cache, use_short)
                for _ in range(3):
                    tf, tg = rtable(rng, n), rtable(rng, n)
                    f, g = b.build(tf), b.build(tg)
                    for op in range(16):
                        r = b.apply(op, f, g)
                        want = [(op >> (2 * x + y)) & 1 for x, y in zip(tf, tg)]
                        assert b.truth_table(r) == want
                        assert r == b.build(want)  # canonical: the same node id
                check_reduced(b)


def test_terminal_arguments() -> None:
    b = BDD(3)
    f = b.build([0, 1, 1, 0, 1, 0, 0, 1])
    for op in range(16):
        for c in (FALSE, TRUE):
            r = b.apply(op, f, c)
            assert b.truth_table(r) == [(op >> (2 * x + c)) & 1 for x in b.truth_table(f)]
            r = b.apply(op, c, f)
            assert b.truth_table(r) == [(op >> (2 * c + x)) & 1 for x in b.truth_table(f)]


def test_call_bound() -> None:
    rng = random.Random(7)
    for n in range(2, 10):
        for _ in range(5):
            b = BDD(n, use_short=False)
            f, g = b.build(rtable(rng, n)), b.build(rtable(rng, n))
            for op in (AND, OR, XOR, IMPLIES):
                b.cache.clear()
                b.calls = b.misses = 0
                b.apply(op, f, g)
                assert b.misses <= b.size(f) * b.size(g)
                assert b.calls <= 2 * b.size(f) * b.size(g)


def parities(b: BDD) -> tuple[int, int]:
    p = q = FALSE
    for i in range(b.n):
        p = b.apply(XOR, p, b.ithvar(i))
        if i % 2 == 0:
            q = b.apply(XOR, q, b.ithvar(i))
    return p, q


def test_cache_saves_calls() -> None:
    # AND of the parity of all n variables and the parity of the even-indexed ones.
    want = {4: (23, 31), 10: (71, 2047), 16: (119, 131071)}
    for n, (with_cache, without) in want.items():
        counts = []
        for use_cache in (True, False):
            b = BDD(n, use_cache, use_short=False)
            p, q = parities(b)
            b.cache.clear()
            b.calls = 0
            r = b.apply(AND, p, q)
            counts.append(b.calls)
            assert (b.size(p), b.size(q)) == (2 * n + 1, n + 1)
        assert tuple(counts) == (with_cache, without)


def disjoint_products(b: BDD, xs: list[int], ys: list[int]) -> int:
    r = FALSE
    for x, y in zip(xs, ys):
        r = b.apply(OR, r, b.apply(AND, b.ithvar(x), b.ithvar(y)))
    return r


def test_product_bound_is_tight() -> None:
    # Bryant's example: the result has |f| |g| / 2 nodes.
    for n in range(1, 4):
        for m in range(1, 4):
            b = BDD(2 * n + 2 * m)
            f = disjoint_products(b, list(range(n)), list(range(n + m, 2 * n + m)))
            g = disjoint_products(b, list(range(n, n + m)), list(range(2 * n + m, 2 * n + 2 * m)))
            r = b.apply(OR, f, g)
            assert (b.size(f), b.size(g)) == (2 ** (n + 1), 2 ** (m + 1))
            assert b.size(r) == 2 ** (n + m + 1) == b.size(f) * b.size(g) // 2
