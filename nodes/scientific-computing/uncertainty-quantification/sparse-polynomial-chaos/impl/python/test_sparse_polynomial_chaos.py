# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-polynomial-chaos/. The authors are listed in prov/NEQJ8H.jsonl.
import itertools
import math
import random

from sparse_polynomial_chaos import (
    apply,
    apply_t,
    debias,
    design_row,
    ista,
    lipschitz,
    objective,
    sample,
    soft,
    sparse_pce,
    total_degree_set,
)


def random_problem(seed, n=8, d=2, p=3):
    rng = random.Random(seed)
    fams = ["uniform"] * d
    index = total_degree_set(d, p)
    rows = [[v / math.sqrt(n) for v in design_row(index, fams, sample(fams, rng))] for _ in range(n)]
    y = [rng.gauss(0, 1) for _ in range(n)]
    return rows, y


def test_soft_thresholding():
    assert soft(3.0, 1.0) == 2.0
    assert soft(-3.0, 1.0) == -2.0
    assert soft(0.5, 1.0) == 0.0
    assert soft(-1.0, 1.0) == 0.0


def test_lipschitz_bounds_the_gradient():
    rows, _ = random_problem(1)
    lip = lipschitz(rows)
    rng = random.Random(2)
    for _ in range(20):
        v = [rng.gauss(0, 1) for _ in rows[0]]
        w = apply_t(rows, apply(rows, v))
        assert math.sqrt(sum(t * t for t in w)) <= lip * math.sqrt(sum(t * t for t in v)) + 1e-12


def test_ista_objective_never_increases():
    rows, y = random_problem(3)
    lam = 0.05 * max(abs(t) for t in apply_t(rows, y))
    lip = lipschitz(rows)
    prev = objective(rows, y, [0.0] * len(rows[0]), lam)
    for k in range(1, 60):
        f = objective(rows, y, ista(rows, y, lam, k, lip), lam)
        assert f <= prev + 1e-12
        prev = f


def test_beck_teboulle_sublinear_bound():
    rows, y = random_problem(4)
    lam = 0.05 * max(abs(t) for t in apply_t(rows, y))
    lip = lipschitz(rows)
    c_star = ista(rows, y, lam, 20000, lip)
    f_star = objective(rows, y, c_star, lam)
    r2 = sum(t * t for t in c_star)
    for k in range(1, 80):
        gap = objective(rows, y, ista(rows, y, lam, k, lip), lam) - f_star
        assert gap <= lip * r2 / (2 * k) + 1e-9


def test_limit_satisfies_the_optimality_conditions():
    rows, y = random_problem(5)
    lam = 0.05 * max(abs(t) for t in apply_t(rows, y))
    c = ista(rows, y, lam, 20000)
    g = apply_t(rows, [b - a for a, b in zip(apply(rows, c), y)])
    for cj, gj in zip(c, g):
        if cj != 0.0:
            assert abs(gj - math.copysign(lam, cj)) < 1e-6
        else:
            assert abs(gj) <= lam + 1e-6


def test_large_penalty_gives_zero():
    rows, y = random_problem(6)
    lam = 1.0001 * max(abs(t) for t in apply_t(rows, y))
    assert all(v == 0.0 for v in ista(rows, y, lam, 50))


def test_matches_brute_force_l0_oracle_with_fewer_runs_than_terms():
    fams = ["uniform", "uniform"]
    index = total_degree_set(2, 3)
    true = [0.0] * len(index)
    true[index.index((1, 0))] = 1.5
    true[index.index((0, 2))] = -0.8

    def q(x):
        return sum(a * b for a, b in zip(design_row(index, fams, x), true))

    n = 7
    rng = random.Random(8)
    xs = [sample(fams, rng) for _ in range(n)]
    rows = [design_row(index, fams, x) for x in xs]
    y = [q(x) for x in xs]
    best = None
    for supp in itertools.combinations(range(len(index)), 2):
        c = debias(rows, y, list(supp))
        res = sum((a - b) ** 2 for a, b in zip(apply(rows, c), y))
        if best is None or res < best[0]:
            best = (res, supp)
    assert best[1] == (index.index((1, 0)), index.index((0, 2)))
    _, c, _ = sparse_pce(q, fams, 3, n, 0.01, 3000, random.Random(8))
    assert max(abs(a - b) for a, b in zip(c, true)) < 1e-8


def test_sparse_polynomial_in_five_inputs_from_25_runs():
    fams = ["uniform"] * 5
    index = total_degree_set(5, 3)
    rng = random.Random(0)
    true = [0.0] * len(index)
    for j in rng.sample(range(1, len(index)), 4):
        true[j] = rng.choice([-1, 1]) * rng.uniform(0.5, 1.5)
    true[0] = 1.0

    def q(x):
        return sum(a * b for a, b in zip(design_row(index, fams, x), true))

    _, c, support = sparse_pce(q, fams, 3, 25, 0.01, 2000, random.Random(100))
    assert len(index) == 56
    assert max(abs(a - b) for a, b in zip(c, true)) < 1e-8
    assert len(support) < 25
