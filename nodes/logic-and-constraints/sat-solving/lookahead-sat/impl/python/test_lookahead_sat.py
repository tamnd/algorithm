# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lookahead-sat/. The authors are listed in prov/AM6WAY.jsonl.

import itertools
import random

from lookahead_sat import Stats, lookahead, propagate, reduction, score, solve

PAGE = [[1, -3, -4], [1, 2, 5], [2, -5], [-1, 2, 5], [1, -4, -5], [2, -3], [2, 3, 5],
        [-1, 3, 4], [2, -4, -5], [1, 4, 5], [-1, 3, -5]]


def satisfiable(clauses: list[list[int]], n: int) -> bool:
    return any(all(any(b[abs(a) - 1] == (a > 0) for a in c) for c in clauses)
               for b in itertools.product([False, True], repeat=n))


def random_3sat(rng: random.Random, n: int, m: int) -> list[list[int]]:
    return [[v if rng.random() < 0.5 else -v for v in rng.sample(range(1, n + 1), 3)]
            for _ in range(m)]


def pigeonhole(p: int, h: int) -> list[list[int]]:
    var = lambda i, j: i * h + j + 1
    cs = [[var(i, j) for j in range(h)] for i in range(p)]
    cs += [[-var(a, j), -var(b, j)] for j in range(h)
           for a in range(p) for b in range(a + 1, p)]
    return cs


def test_page_example() -> None:
    st = Stats()
    kind, info = lookahead(PAGE, {}, st)
    # -x2 is a failed literal: it forces -x5 and -x3, and (x2 v x3 v x5) is false.
    assert propagate(PAGE, {2: False}) is None
    assert st.failed_literals == 1 and st.autarkies == 0
    assert kind == "branch"
    x, d, assign = info
    assert assign == {2: True}
    assert x == 1 and d == {1: 2, -1: 3} and score(2, 3) == 6149
    table = {}
    for v in (3, 4, 5):
        side = {lit: propagate(PAGE, {2: True, v: lit > 0}) for lit in (v, -v)}
        table[v] = tuple(reduction(PAGE, assign, side[lit]) for lit in (v, -v))
    assert table == {3: (1, 2), 4: (2, 2), 5: (2, 1)}
    st = Stats()
    model = solve(PAGE, 5, st)
    assert model == {1: True, 2: True, 3: True, 4: False, 5: False}
    assert (st.nodes, st.failed_literals, st.autarkies, st.lookaheads) == (2, 1, 1, 7)


def test_score_prefers_balanced_reductions() -> None:
    assert score(3, 3) > score(1, 8)
    assert score(2, 2) > score(0, 100)


def test_reduction_counts_shortened_open_clauses() -> None:
    f = [[1, 2], [-1, 2, 3], [-1, 4], [2, 5]]
    after = propagate(f, {1: True})
    assert after == {1: True, 4: True}
    assert reduction(f, {}, after) == 1  # only (-x1 v x2 v x3) is shortened and open


def test_against_brute_force() -> None:
    rng = random.Random(1997)
    for _ in range(300):
        n = rng.randint(1, 12)
        f = random_3sat(rng, n, rng.randint(1, 6 * n)) if n >= 3 else \
            [[rng.choice([1, -1]) * rng.randint(1, n)] for _ in range(rng.randint(1, 3))]
        model = solve(f, n)
        assert (model is not None) == satisfiable(f, n)
        if model is not None:
            assert all(any(model[abs(a)] == (a > 0) for a in c) for c in f)


def test_failed_literals_and_autarkies_are_sound() -> None:
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(3, 10)
        f = random_3sat(rng, n, rng.randint(n, 5 * n))
        a0 = propagate(f, {})
        if a0 is None:
            continue
        st = Stats()
        kind, info = lookahead(f, a0, st)
        if kind == "branch":
            _, _, assign = info
            # Every fixed literal keeps satisfiability.
            restricted = f + [[v if b else -v] for v, b in assign.items()]
            assert satisfiable(restricted, n) == satisfiable(f, n)
        if kind == "unsat":
            assert not satisfiable(f, n)


def test_pigeonhole_is_unsatisfiable() -> None:
    st = Stats()
    assert solve(pigeonhole(5, 4), 20, st) is None
    assert solve(pigeonhole(4, 4), 16) is not None
