# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/davis-putnam-elimination/. The authors are listed in prov/1EV788.jsonl.

import random

from davis_putnam_elimination import davis_putnam, eliminate, resolvents


def table(n: int, clauses) -> int:
    """Bitset over the 2^n assignments: bit a is 1 when assignment a (bit v-1
    of a is x_v) satisfies every clause."""
    size = 1 << n
    full = (1 << size) - 1
    xs = []
    for v in range(n):
        period = 1 << (v + 1)
        block = ((1 << (1 << v)) - 1) << (1 << v)
        xs.append(block * sum(1 << (i * period) for i in range(size // period)))
    f = full
    for c in clauses:
        b = 0
        for q in c:
            b |= xs[q - 1] if q > 0 else full ^ xs[-q - 1]
        f &= b
    return f


def satisfies(model: list[int], clauses) -> bool:
    s = set(model)
    return all(any(q in s for q in c) for c in clauses)


def random_formula(rng: random.Random, n: int, t: int) -> list[list[int]]:
    if t % 2 == 0:
        m, k = round(4.26 * n), min(3, n)
        return [[v if rng.random() < 0.5 else -v for v in rng.sample(range(1, n + 1), k)] for _ in range(m)]
    f = []
    for _ in range(rng.randint(0, 4 * n)):
        vs = rng.sample(range(1, n + 1), rng.randint(1, min(4, n)))
        f.append([v if rng.random() < 0.5 else -v for v in vs])
    return f


def test_page_examples() -> None:
    log: list[tuple[str, int, int]] = []
    a = [[1, 2], [-1, 3], [-2, 3], [-3, 4], [-3, -4]]
    assert davis_putnam(4, a, log) is None
    assert [(r, x) for r, x, _ in log] == [("eliminate", 1), ("eliminate", 2), ("unit", 3), ("unit", -4)]
    assert [s for _, _, s in log] == [4, 3, 2, 1]
    log = []
    b = [[1, 2], [-1, 2], [1, -2], [-1, -2, 3], [3, 4]]
    assert davis_putnam(4, b, log) == [1, 2, 3, -4]
    assert log == [("pure", 3, 3), ("eliminate", 1, 1), ("unit", 2, 0)]


def test_resolvents_drop_tautologies() -> None:
    pos = [frozenset({1, 2}), frozenset({1, -2})]
    neg = [frozenset({-1, 2})]
    assert resolvents(pos, neg, 1) == {frozenset({2})}


def test_hand_cases() -> None:
    assert davis_putnam(0, []) == []
    assert davis_putnam(0, [[]]) is None
    assert davis_putnam(3, []) == [-1, -2, -3]
    assert davis_putnam(1, [[1], [-1]]) is None
    assert davis_putnam(2, [[1, -1]]) == [-1, -2]
    assert davis_putnam(2, [[1, 2], [-1, 2], [1, -2], [-1, -2]]) is None


def test_pigeonhole() -> None:
    for h in range(1, 4):
        p = h + 1
        x = lambda i, j: i * h + j + 1  # noqa: E731
        f = [[x(i, j) for j in range(h)] for i in range(p)]
        f += [[-x(a, j), -x(b, j)] for j in range(h) for a in range(p) for b in range(a + 1, p)]
        assert davis_putnam(p * h, f) is None


def test_one_elimination_keeps_satisfiability_and_is_implied() -> None:
    rng = random.Random(1960)
    for t in range(500):
        n = rng.randint(1, 8)
        f = random_formula(rng, n, t)
        fs = {frozenset(c) for c in f if not any(-q in c for q in c)}
        x = rng.randint(1, n)
        g, removed = eliminate(fs, x)
        assert all(x not in c and -x not in c for c in g)
        tf, tg = table(n, fs), table(n, g)
        assert tf & ~tg == 0  # every resolvent follows from F
        assert (tf != 0) == (tg != 0)  # F and the new formula are equisatisfiable
        assert len(removed) == sum(1 for c in fs if x in c or -x in c)


def test_random_against_brute_force() -> None:
    rng = random.Random(1962)
    for t in range(600):
        n = rng.randint(1, 10)
        f = random_formula(rng, n, t)
        got = davis_putnam(n, f)
        if got is None:
            assert table(n, f) == 0
        else:
            assert len(got) == n and satisfies(got, f)
