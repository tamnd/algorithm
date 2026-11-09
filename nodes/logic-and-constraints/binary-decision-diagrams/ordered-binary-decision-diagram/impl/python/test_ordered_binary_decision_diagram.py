# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ordered-binary-decision-diagram/. The authors are listed in prov/8Z0NZS.jsonl.

import random

from ordered_binary_decision_diagram import FALSE, OBDD, TRUE


def pairs_table(n: int, pairs: list[tuple[int, int]]) -> list[int]:
    """The truth table of the OR over the pairs (a, b) of x_a AND x_b."""
    return [int(any((a >> i) & 1 and (a >> j) & 1 for i, j in pairs)) for a in range(1 << n)]


def random_obdd(b: OBDD, rng: random.Random, count: int) -> int:
    """A random ordered (not reduced) diagram: each edge goes to a lower level."""
    pool = [FALSE, TRUE]
    for _ in range(count):
        i = rng.randrange(b.n)
        ok = [u for u in pool if b.lev(u) > b.level[i]]
        pool.append(b.node(i, rng.choice(ok), rng.choice(ok)))
    return pool[-1]


def count_beads(n: int, order: list[int], table: list[int]) -> int:
    """Distinct subfunctions that fix the top k variables and depend on the next one, plus the sinks used."""
    total = len(set(table))  # the terminals that occur
    for k in range(n):
        top, v = order[:k], order[k]
        subs = set()
        for fix in range(1 << k):
            base = sum(((fix >> t) & 1) << top[t] for t in range(k))
            sub = tuple(table[a] for a in range(1 << n) if all(((a >> top[t]) & 1) == ((base >> top[t]) & 1) for t in range(k)))
            subs.add(sub)
        for sub in subs:
            # sub is indexed by the free variables in increasing order; split it on v
            free = [w for w in range(n) if w not in top]
            pos = free.index(v)
            lo = tuple(s for idx, s in enumerate(sub) if not (idx >> pos) & 1)
            hi = tuple(s for idx, s in enumerate(sub) if (idx >> pos) & 1)
            total += lo != hi
    return total


def test_example() -> None:
    b = OBDD(3)
    t = b.tree([0, 0, 0, 1, 1, 1, 1, 1])  # (x0 AND x1) OR x2
    assert b.size(t) == 7 + 2 and b.is_ordered(t)  # the tree shares its two sinks
    r = b.reduce(t)
    assert b.size(r) == 5 and b.is_ordered(r)
    assert b.truth_table(r) == [0, 0, 0, 1, 1, 1, 1, 1]


def test_tree_and_reduce_against_truth_tables() -> None:
    rng = random.Random(1986)
    for n in range(1, 11):
        for _ in range(3):
            order = list(range(n))
            rng.shuffle(order)
            b = OBDD(n, order)
            table = [rng.randint(0, 1) for _ in range(1 << n)]
            t = b.tree(table)
            assert b.size(t) == (1 << n) - 1 + len(set(table)) and b.is_ordered(t)
            r = b.reduce(t)
            assert b.is_ordered(r)
            assert b.truth_table(r) == table
            seen = set()
            for u in b.reachable(r):
                if u > TRUE:
                    i, lo, hi = b.nodes[u]
                    assert lo != hi and (i, lo, hi) not in seen
                    seen.add((i, lo, hi))
            if n <= 6:
                assert b.size(r) == count_beads(n, order, table)


def test_reduce_is_canonical() -> None:
    rng = random.Random(42)
    for n in range(1, 9):
        order = list(range(n))
        rng.shuffle(order)
        b = OBDD(n, order)
        for _ in range(20):
            g = random_obdd(b, rng, rng.randint(1, 15))
            assert b.is_ordered(g)
            table = b.truth_table(g)
            assert b.reduce(g) == b.reduce(b.tree(table))
            assert b.reduce(b.reduce(g)) == b.reduce(g)


def test_order_matters() -> None:
    for k in range(1, 5):
        n = 2 * k
        pairs = [(2 * t, 2 * t + 1) for t in range(k)]
        table = pairs_table(n, pairs)
        good = OBDD(n)
        bad = OBDD(n, [2 * t for t in range(k)] + [2 * t + 1 for t in range(k)])
        assert good.size(good.reduce(good.tree(table))) == 2 * k + 2
        assert bad.size(bad.reduce(bad.tree(table))) == 1 << (k + 1)


def test_is_ordered_rejects() -> None:
    b = OBDD(3)
    u = b.node(0, FALSE, TRUE)
    assert not b.is_ordered(b.node(1, u, TRUE))  # x_1 above x_0
    assert not b.is_ordered(b.node(0, u, TRUE))  # x_0 twice
    assert b.is_ordered(b.node(2, TRUE, TRUE)) and b.reduce(b.node(2, TRUE, TRUE)) == TRUE
