# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cube-and-conquer/. The authors are listed in prov/7ZW1HX.jsonl.

import itertools
import random

from cube_and_conquer import conquer, create_cubes, cube_and_conquer


def models(clauses: list[list[int]], n: int):
    for bits in itertools.product([False, True], repeat=n):
        if all(any(bits[abs(a) - 1] == (a > 0) for a in c) for c in clauses):
            yield bits


def satisfiable(clauses, n) -> bool:
    return next(models(clauses, n), None) is not None


def random_3sat(rng: random.Random, n: int, m: int) -> list[list[int]]:
    return [[v if rng.random() < 0.5 else -v for v in rng.sample(range(1, n + 1), 3)]
            for _ in range(m)]


def pigeonhole(p: int, h: int) -> list[list[int]]:
    var = lambda i, j: i * h + j + 1
    cs = [[var(i, j) for j in range(h)] for i in range(p)]
    cs += [[-var(a, j), -var(b, j)] for j in range(h)
           for a in range(p) for b in range(a + 1, p)]
    return cs


def test_threshold_rules() -> None:
    f = random_3sat(random.Random(1), 10, 30)
    part = create_cubes(f, theta=1000.0)
    assert abs(part.theta_trace[0] - 1050.0) < 1e-9  # +5% at the root, no conflict
    part = create_cubes(pigeonhole(4, 3), theta=1.0)
    # Every refuted node multiplies theta by 1.05 and then by 0.7.
    assert any(abs(b - a * 1.05 * 0.7) < 1e-9
               for a, b in zip(part.theta_trace, part.theta_trace[1:]))


def test_partition_covers_the_models() -> None:
    rng = random.Random(2011)
    for _ in range(60):
        n = rng.randint(4, 10)
        f = random_3sat(rng, n, rng.randint(n, 5 * n))
        part = create_cubes(f, theta=rng.choice([0.05, 0.3, 2.0]))
        for c in part.clauses:  # each learned clause is implied by F
            assert not satisfiable(f + [[-a] for a in c], n)
        for a, b in itertools.combinations(part.cubes, 2):  # cubes are disjoint
            assert any(-x in b for x in a)
        for bits in models(f, n):  # each model satisfies exactly one cube
            hits = [c for c in part.cubes if all(bits[abs(a) - 1] == (a > 0) for a in c)]
            assert len(hits) == 1


def test_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(150):
        n = rng.randint(3, 12)
        f = random_3sat(rng, n, rng.randint(n, 6 * n))
        theta = rng.choice([0.02, 0.2, 1.0, 1000.0])
        part = create_cubes(f, theta=theta)
        want = satisfiable(f, n)
        for use_cores in (True, False):
            model, _ = conquer(f, part, n, use_cores)
            assert (model is not None) == want
            if model is not None:
                assert all(any(model[abs(a)] == (a > 0) for a in c) for c in f)


def test_pigeonhole_page_example() -> None:
    f = pigeonhole(5, 4)
    part = create_cubes(f, theta=0.5)
    assert part.cubes == [[-1, -2, 3], [-1, -2, -3]]
    assert part.clauses == [[1, -2, 5], [1, -2, -5], [-1, 6], [-1, -6]]
    trace = [round(t, 3) for t in part.theta_trace]
    assert trace == [0.525, 0.551, 0.579, 0.608, 0.638, 0.67, 0.492, 0.362, 0.38, 0.279, 0.205]
    model, solved = conquer(f, part, 20)
    assert model is None and solved == len(part.cubes)
    assert cube_and_conquer(pigeonhole(4, 4), 16, theta=0.5) is not None
