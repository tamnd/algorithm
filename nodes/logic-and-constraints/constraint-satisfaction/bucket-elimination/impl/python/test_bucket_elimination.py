# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bucket-elimination/. The authors are listed in prov/GJ1MVJ.jsonl.

import itertools
import random

from bucket_elimination import bucket_count, bucket_elimination, induced_width


def solutions(domains, cons):
    return [t for t in itertools.product(*[sorted(d) for d in domains])
            if all(tuple(t[v] for v in s) in r for s, r in cons)]


def test_example() -> None:
    # x0 + x1 = x2, x2 != x3, x1 < x3, all in {0, 1, 2}
    d = range(3)
    cons = [((0, 1, 2), {(a, b, a + b) for a in d for b in d if a + b <= 2}),
            ((2, 3), {(a, b) for a in d for b in d if a != b}),
            ((1, 3), {(a, b) for a in d for b in d if a < b})]
    doms = [set(d)] * 4
    stats: dict[str, int] = {}
    assert bucket_elimination(doms, cons, None, stats) == [0, 0, 0, 1]
    assert stats["max_scope"] == 2 == induced_width(4, [s for s, _ in cons], range(4))
    assert bucket_count(doms, cons) == len(solutions(doms, cons)) == 5


def test_edges() -> None:
    assert bucket_elimination([], []) == []
    assert bucket_count([], []) == 1
    assert bucket_elimination([{3}], []) == [3]
    assert bucket_elimination([set()], []) is None
    assert bucket_count([{0, 1}, set()], []) == 0
    assert bucket_elimination([{0, 1}], [((0,), {(1,)})]) == [1]
    assert bucket_elimination([{0}, {0}], [((0, 1), set())]) is None


def test_random_against_brute_force() -> None:
    rng = random.Random(9)
    for _ in range(300):
        n, d = rng.randint(1, 6), rng.randint(1, 3)
        domains = [{a for a in range(d) if rng.random() > 0.1} for _ in range(n)]
        cons = []
        for _ in range(rng.randint(0, 6)):
            r = rng.randint(1, min(3, n))
            scope = tuple(rng.sample(range(n), r))
            allowed = {t for t in itertools.product(range(d), repeat=r) if rng.random() > 0.35}
            cons.append((scope, allowed))
        order = list(range(n))
        rng.shuffle(order)
        sols = solutions(domains, cons)
        stats: dict[str, int] = {}
        got = bucket_elimination(domains, cons, order, stats)
        if sols:
            assert got is not None and tuple(got) in set(sols)
            # every new constraint has at most w* variables
            assert stats["max_scope"] <= induced_width(n, [s for s, _ in cons], order)
        else:
            assert got is None
        assert bucket_count(domains, cons, order) == len(sols)
