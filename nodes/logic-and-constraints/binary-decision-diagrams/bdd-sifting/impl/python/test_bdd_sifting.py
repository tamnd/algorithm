# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bdd-sifting/. The authors are listed in prov/KV4EXG.jsonl.

import random

from bdd_sifting import Manager, sift


def tables_of(m: Manager) -> list[list[int]]:
    return [[m.evaluate(r, a) for a in range(1 << m.n)] for r in m.roots]


def fresh_size(n: int, order: list[int], tables: list[list[int]]) -> int:
    m = Manager(n, order)
    for t in tables:
        m.build(t)
    return m.size()


def random_tables(rng: random.Random, n: int, count: int) -> list[list[int]]:
    out = []
    for _ in range(count):
        if rng.random() < 0.5:
            density = rng.random()
            out.append([int(rng.random() < density) for _ in range(1 << n)])
        else:  # a sum of products over random pairs: these depend on the order
            pairs = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randrange(1, n + 1))]
            out.append([int(any(a >> i & 1 and a >> j & 1 for i, j in pairs)) for a in range(1 << n)])
    return out


def test_swap_keeps_functions_and_other_levels() -> None:
    rng = random.Random(1993)
    checked = 0
    for _ in range(300):
        n = rng.randrange(2, 8)
        order = list(range(n))
        rng.shuffle(order)
        tables = random_tables(rng, n, rng.randrange(1, 4))
        m = Manager(n, order)
        roots = [m.build(t) for t in tables]
        k = rng.randrange(n - 1)
        x, y = m.order[k], m.order[k + 1]
        before = {u: list(w) for u, w in m.nodes.items() if w[0] not in (x, y)}
        m.swap(k)
        m.check_invariant()
        assert m.roots == roots
        assert tables_of(m) == tables
        assert m.size() == fresh_size(n, m.order, tables)
        after = {u: list(w) for u, w in m.nodes.items() if w[0] not in (x, y)}
        assert after == before
        checked += 1
    assert checked >= 300


def test_sift_never_grows_and_keeps_functions() -> None:
    rng = random.Random(42)
    for _ in range(250):
        n = rng.randrange(1, 9)
        order = list(range(n))
        rng.shuffle(order)
        tables = random_tables(rng, n, rng.randrange(1, 3))
        m = Manager(n, order)
        for t in tables:
            m.build(t)
        start = m.size()
        end = sift(m, max_growth=rng.choice([1.2, 2.0, 100.0]))
        m.check_invariant()
        assert end <= start
        assert tables_of(m) == tables
        assert end == fresh_size(n, m.order, tables)


def test_sift_fixes_the_separated_order() -> None:
    k = 4
    n = 2 * k
    table = [int(any(a >> (2 * i) & 1 and a >> (2 * i + 1) & 1 for i in range(k))) for a in range(1 << n)]
    m = Manager(n, list(range(0, n, 2)) + list(range(1, n, 2)))
    m.build(table)
    assert m.size() == 2 ** (k + 1)
    assert sift(m, max_growth=100.0) == 2 * k + 2
