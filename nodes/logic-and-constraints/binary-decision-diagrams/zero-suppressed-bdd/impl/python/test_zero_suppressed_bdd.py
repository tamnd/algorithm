# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-suppressed-bdd/. The authors are listed in prov/73ZZQJ.jsonl.

import random

from zero_suppressed_bdd import BASE, EMPTY, ZDD


def random_family(rng: random.Random, n: int) -> set[frozenset[int]]:
    size = rng.randrange(0, min(1 << n, 12) + 1)
    p = rng.random()
    return {frozenset(i for i in range(n) if rng.random() < p) for _ in range(size)}


def bdd_size(n: int, family: set[frozenset[int]]) -> int:
    """The size of the reduced OBDD (order 0, 1, ..., n-1) of the characteristic function."""
    table = [0] * (1 << n)
    for s in family:
        table[sum(1 << i for i in s)] = 1
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


def test_operations_against_sets_of_sets() -> None:
    rng = random.Random(1993)
    checked = 0
    for _ in range(600):
        n = rng.randrange(0, 8)
        z = ZDD(n)
        a, b = random_family(rng, n), random_family(rng, n)
        p, q = z.from_family(a), z.from_family(b)
        assert z.to_family(p) == a and z.count(p) == len(a)
        assert z.to_family(z.union(p, q)) == a | b
        assert z.to_family(z.intersect(p, q)) == a & b
        assert z.to_family(z.diff(p, q)) == a - b
        assert z.to_family(z.join(p, q)) == {s | t for s in a for t in b}
        if n:
            v = rng.randrange(n)
            assert z.to_family(z.subset0(p, v)) == {s for s in a if v not in s}
            assert z.to_family(z.subset1(p, v)) == {s - {v} for s in a if v in s}
            assert z.to_family(z.change(p, v)) == {s ^ {v} for s in a}
        assert z.from_family(set(a)) == p  # canonical: the same family gives the same node
        assert (p == q) == (a == b)
        z.check_invariant()
        checked += 1
    assert checked >= 500


def test_size_relation_with_bdds() -> None:
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randrange(1, 8)
        a = random_family(rng, n)
        z = ZDD(n)
        zs = z.size(z.from_family(a))
        bs = bdd_size(n, a)
        assert zs <= n * bs + 2 and bs <= n * zs + 2


def test_extreme_families() -> None:
    for n in range(1, 8):
        z = ZDD(n)
        power = BASE
        for v in reversed(range(n)):
            power = z.getnode(v, power, power)
        all_sets = {frozenset(i for i in range(n) if a >> i & 1) for a in range(1 << n)}
        assert z.to_family(power) == all_sets
        assert z.size(power) == n + 1 and bdd_size(n, all_sets) == 1
        assert z.size(BASE) == 1 and bdd_size(n, {frozenset()}) == n + 2
        assert z.size(EMPTY) == 1
