# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probsat/. The authors are listed in prov/RPJ893.jsonl.

import itertools
import math
import random

from probsat import State, normalize, probabilities, probsat, weight


def satisfies(clauses: list[list[int]], x: list[bool]) -> bool:
    return all(any(x[abs(l) - 1] == (l > 0) for l in cl) for cl in clauses)


def brute_sat(n: int, clauses: list[list[int]]) -> bool:
    return any(satisfies(clauses, list(b)) for b in itertools.product([False, True], repeat=n))


def random_cnf(rng: random.Random, n: int, m: int, k: int) -> list[list[int]]:
    return [[rng.choice([1, -1]) * v for v in rng.sample(range(1, n + 1), k)] for _ in range(m)]


EXAMPLE = [[2, 3, -4], [1, 3, 4], [1, -3], [-1, 3], [-1, 2], [-3, 4]]


def test_example() -> None:
    # the page example, with cb = 2.38 and eps = 1
    s = State(4, EXAMPLE, [False, False, False, False])
    assert [EXAMPLE[j] for j in s.false_list] == [[1, 3, 4]]
    p = dict(probabilities(s, [1, 3, 4], 2.38, 1.0, "poly"))
    assert [s.break_count(v) for v in (1, 3, 4)] == [2, 2, 1]
    assert abs(p[1] - 0.2162) < 1e-4 and abs(p[3] - 0.2162) < 1e-4 and abs(p[4] - 0.5675) < 1e-4
    s.flip(4)
    p = dict(probabilities(s, [2, 3, -4], 2.38, 1.0, "poly"))
    assert abs(p[2] - 0.7224) < 1e-4 and abs(p[3] - 0.1388) < 1e-4 and abs(p[4] - 0.1388) < 1e-4
    s.flip(2)
    assert s.false_list == []
    models = [list(b) for b in itertools.product([False, True], repeat=4) if satisfies(EXAMPLE, list(b))]
    assert models == [[False, True, False, True], [True, True, True, True]]
    for seed in range(20):
        assert probsat(4, EXAMPLE, rng=random.Random(seed)) in models


def test_weights() -> None:
    assert weight(0, 2.38, 1.0, "poly") == 1.0
    assert math.isclose(weight(2, 2.0, 1.0, "poly"), 1 / 9)
    assert math.isclose(weight(3, 2.5, 0.0, "exp"), 2.5 ** -3)
    # cb = 0 gives the uniform choice of Schöning's walk
    s = State(3, [[1, 2, 3], [-1, 2], [-2, 3]], [False, False, False])
    assert all(math.isclose(q, 1 / 3) for _, q in probabilities(s, [1, 2, 3], 0.0, 1.0, "poly"))
    try:
        weight(1, 2.0, 1.0, "other")
    except ValueError:
        pass
    else:
        raise AssertionError


def test_edges() -> None:
    assert probsat(0, []) == []
    assert probsat(2, [[]]) is None
    assert probsat(1, [[1, -1]], rng=random.Random(0)) is not None
    assert probsat(1, [[1], [-1]], max_flips=50, rng=random.Random(0)) is None
    assert probsat(1, [[1, 1]], rng=random.Random(0)) == [True]
    assert normalize([[2, 1, 2], [3, -3]]) == [[1, 2]]


def test_probabilities_are_a_distribution_falling_with_break() -> None:
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(3, 8)
        cls = normalize(random_cnf(rng, n, rng.randint(2, 4 * n), 3))
        assert cls is not None
        s = State(n, cls, [rng.random() < 0.5 for _ in range(n)])
        x = s.x[1:]
        assert sorted(s.false_list) == sorted(j for j, cl in enumerate(cls) if not satisfies([cl], x))
        if not s.false_list:
            continue
        c = cls[s.false_list[0]]
        for kind, cb in (("poly", 2.38), ("exp", 2.5)):
            probs = probabilities(s, c, cb, 1.0, kind)
            assert math.isclose(sum(q for _, q in probs), 1.0)
            for (v, q), (u, r) in itertools.product(probs, probs):
                if s.break_count(v) < s.break_count(u):
                    assert q > r
                if s.break_count(v) == s.break_count(u):
                    assert math.isclose(q, r)


def test_sampling_frequency() -> None:
    # the measured flip frequency at the start of the example matches the formula
    s = State(4, EXAMPLE, [False, False, False, False])
    probs = probabilities(s, [1, 3, 4], 2.38, 1.0, "poly")
    rng = random.Random(7)
    counts = {1: 0, 3: 0, 4: 0}
    for _ in range(20000):
        counts[rng.choices([v for v, _ in probs], weights=[q for _, q in probs])[0]] += 1
    assert abs(counts[4] / 20000 - 0.5675) < 0.02


def test_random_against_brute_force() -> None:
    rng = random.Random(2024)
    sat = unsat = 0
    for _ in range(600):
        n = rng.randint(3, 10)
        m = rng.randint(1, int(4.5 * n))
        clauses = random_cnf(rng, n, m, rng.choice([2, 3, 3, 4]) if n >= 4 else 2)
        x = probsat(n, clauses, max_tries=5, max_flips=200, rng=random.Random(rng.randrange(10**9)))
        if x is not None:
            assert satisfies(clauses, x)
        if brute_sat(n, clauses):
            assert x is not None
            sat += 1
        else:
            assert x is None
            unsat += 1
    assert sat > 200 and unsat > 50


def test_planted() -> None:
    rng = random.Random(5)
    n = 200
    planted = [rng.random() < 0.5 for _ in range(n)]
    clauses = [cl for cl in random_cnf(rng, n, 1200, 3) if satisfies([cl], planted)]
    x = probsat(n, clauses, max_tries=3, max_flips=20000, rng=random.Random(6))
    assert x is not None and satisfies(clauses, x)
