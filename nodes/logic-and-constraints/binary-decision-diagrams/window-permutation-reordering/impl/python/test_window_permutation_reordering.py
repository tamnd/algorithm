# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/window-permutation-reordering/. The authors are listed in prov/83R3H0.jsonl.

import random
from itertools import permutations
from math import factorial

from window_permutation_reordering import Manager, sjt_swaps, window_permutation


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
        else:
            pairs = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randrange(1, n + 1))]
            out.append([int(any(a >> i & 1 and a >> j & 1 for i, j in pairs)) for a in range(1 << n)])
    return out


def test_sjt_visits_all_orders() -> None:
    for w in range(1, 6):
        perm = list(range(w))
        seen = {tuple(perm)}
        for j in sjt_swaps(w):
            perm[j], perm[j + 1] = perm[j + 1], perm[j]
            seen.add(tuple(perm))
        assert len(sjt_swaps(w)) == factorial(w) - 1
        assert len(seen) == factorial(w)
    assert sjt_swaps(3) == [1, 0, 1, 0, 1]


def test_window_never_grows_and_is_a_local_optimum() -> None:
    rng = random.Random(1991)
    checked = 0
    for _ in range(500):
        n = rng.randrange(2, 8)
        w = rng.choice([2, 3]) if n >= 3 else 2
        order = list(range(n))
        rng.shuffle(order)
        tables = random_tables(rng, n, rng.randrange(1, 3))
        m = Manager(n, order)
        for t in tables:
            m.build(t)
        start = m.size()
        end = window_permutation(m, w)
        m.check_invariant()
        assert end <= start
        assert tables_of(m) == tables
        assert end == fresh_size(n, m.order, tables)
        if checked < 120:  # no window of w levels can be improved
            for k in range(n - w + 1):
                for p in permutations(m.order[k:k + w]):
                    other = m.order[:k] + list(p) + m.order[k + w:]
                    assert fresh_size(n, other, tables) >= end
        checked += 1
    assert checked >= 500


def test_separated_order() -> None:
    k = 3
    n = 2 * k
    table = [int(any(a >> (2 * i) & 1 and a >> (2 * i + 1) & 1 for i in range(k))) for a in range(1 << n)]
    m = Manager(n, list(range(0, n, 2)) + list(range(1, n, 2)))
    m.build(table)
    assert m.size() == 16
    assert window_permutation(m, 2) <= 16
    m = Manager(n, list(range(0, n, 2)) + list(range(1, n, 2)))
    m.build(table)
    assert window_permutation(m, 3) <= 16
