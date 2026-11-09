# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kronecker-functional-decision-diagram/. The authors are listed in prov/EDCXTM.jsonl.

import random

from kronecker_functional_decision_diagram import KFDD

TYPES = ["S", "pD", "nD"]


def robdd_size(n: int, table: list[int]) -> int:
    """The ROBDD size for the order x_0, ..., x_{n-1}, by counting subfunctions."""
    total = len(set(table))
    for k in range(n):
        subs = set()
        for top in range(1 << k):
            lo = tuple(table[top | low << (k + 1)] for low in range(1 << (n - k - 1)))
            hi = tuple(table[top | 1 << k | low << (k + 1)] for low in range(1 << (n - k - 1)))
            if lo != hi:
                subs.add((lo, hi))
        total += len(subs)
    return total


def test_against_truth_tables() -> None:
    rng = random.Random(1994)
    checked = 0
    for _ in range(600):
        n = rng.randrange(0, 8)
        dtl = [rng.choice(TYPES) for _ in range(n)]
        d = KFDD(dtl)
        s = [rng.randrange(2) for _ in range(1 << n)]
        t = [rng.randrange(2) for _ in range(1 << n)]
        f, g = d.from_table(s), d.from_table(t)
        assert [d.evaluate(f, a) for a in range(1 << n)] == s
        assert d.from_table(list(s)) == f
        h = d.xor(f, g)
        assert h == d.from_table([x ^ y for x, y in zip(s, t)])
        assert (f == g) == (s == t)
        d.check_invariant()
        checked += 1
    assert checked >= 500


def test_shannon_only_is_the_robdd() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randrange(0, 8)
        s = [rng.randrange(2) for _ in range(1 << n)]
        d = KFDD(["S"] * n)
        assert d.size(d.from_table(s)) == robdd_size(n, s)


def test_parity_of_products() -> None:
    # f = x_0 x_1 XOR x_2 x_3 XOR ...: the positive Davio form has one product per pair
    for k in range(1, 5):
        n = 2 * k
        s = [0] * (1 << n)
        for a in range(1 << n):
            s[a] = sum(a >> (2 * i) & a >> (2 * i + 1) & 1 for i in range(k)) % 2
        sizes = {}
        for dtl in (["S"] * n, ["pD"] * n):
            d = KFDD(dtl)
            sizes[dtl[0]] = d.size(d.from_table(s))
        assert sizes["S"] == robdd_size(n, s)
        assert sizes["pD"] <= sizes["S"]
