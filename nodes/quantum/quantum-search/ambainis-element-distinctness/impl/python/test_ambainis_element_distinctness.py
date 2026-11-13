# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ambainis-element-distinctness/. The authors are listed in prov/VT4428.jsonl.
import math
import random

from ambainis_element_distinctness import (
    best_t1,
    collision_sets,
    default_r,
    k_distinctness,
    measure_full,
    queries,
    reduced_step,
    run_full,
    run_reduced,
    start_vector,
    success_full,
    success_reduced,
    t2_steps,
    type_counts,
)
from qsim import TOL, norm


def test_worked_example():
    x = [3, 1, 4, 1, 5, 9, 2, 6]
    r = default_r(8, 2)
    t2 = t2_steps(r, 2)
    t1 = best_t1(8, 2, r)
    assert (r, t2, t1, queries(r, t1, t2)) == (4, 2, 1, 8)
    assert type_counts(8, 2, 4) == {(0, 0): 30, (0, 1): 30, (1, 0): 120, (1, 1): 40, (2, 0): 60}
    assert abs(success_full(x, 2, r, 0, t2) - 3 / 14) < TOL
    assert abs(success_full(x, 2, r, t1, t2) - 0.7573714285714286) < TOL
    assert measure_full(x, 2, r, t1, t2, random.Random(1)) == ([1, 3], 8)


def test_full_matches_reduced():
    cases = [
        ([0, 1, 2, 3, 1, 4], 2, 2),
        ([0, 1, 2, 3, 1, 4], 2, 3),
        ([5, 0, 1, 2, 3, 4, 0], 2, 3),
        ([0, 1, 2, 3, 4, 5, 6, 2], 2, 4),
        ([0, 1, 1, 2, 1, 3, 4, 5], 3, 4),
    ]
    for x, k, r in cases:
        t2 = t2_steps(r, k)
        for t1 in range(4):
            assert abs(success_full(x, k, r, t1, t2) - success_reduced(len(x), k, r, t1, t2)) < TOL


def test_full_state_stays_normalized_and_counts_queries():
    x = [0, 1, 2, 3, 4, 5, 6, 2]
    for t1, t2 in ((0, 0), (1, 2), (2, 3)):
        state, _, q = run_full(x, 2, 4, t1, t2)
        assert abs(norm(state) - 1) < TOL
        assert q == queries(4, t1, t2) == 4 + 2 * t1 * t2


def test_type_counts_sum():
    for n, k, r in ((8, 2, 4), (20, 3, 7), (100, 2, 21)):
        assert sum(type_counts(n, k, r).values()) == math.comb(n, r) * (n - r)
        assert abs(sum(a * a for a in start_vector(n, k, r).values()) - 1) < TOL


def _walk_matrix(n, k, r):
    types = list(start_vector(n, k, r))
    cols = [reduced_step({u: float(u == t) for u in types}, n, k, r) for t in types]
    return [[cols[j][types[i]] for j in range(len(types))] for i in range(len(types))]


def test_lemma2_eigenphases():
    # k = 2: U has eigenvalues 1, exp(+-i theta_1), exp(+-i theta_2) with theta_j ~ 2 sqrt(j / r)
    n, k, r = 10**6, 2, 1000
    u = _walk_matrix(n, k, r)
    d = len(u)
    tr = sum(u[i][i] for i in range(d))
    tr2 = sum(u[i][m] * u[m][i] for i in range(d) for m in range(d))
    a = (tr - 1) / 2  # cos t1 + cos t2
    b = (tr2 + 3) / 4  # cos^2 t1 + cos^2 t2
    p = (a * a - b) / 2
    disc = math.sqrt(a * a - 4 * p)
    thetas = sorted(math.acos(c) for c in ((a + disc) / 2, (a - disc) / 2))
    for j, th in enumerate(thetas, start=1):
        assert abs(th * math.sqrt(r) / (2 * math.sqrt(j)) - 1) < 1e-3
    s = start_vector(n, k, r)
    w = reduced_step(dict(s), n, k, r)
    assert max(abs(w[t] - s[t]) for t in s) < TOL


def test_success_and_query_growth():
    for k in (2, 3):
        for n in (64, 256, 1024, 4096, 16384, 65536):
            r = default_r(n, k)
            t1, t2 = best_t1(n, k, r), t2_steps(r, k)
            assert success_reduced(n, k, r, t1, t2) > 0.7
            assert queries(r, t1, t2) < 3 * n ** (k / (k + 1))
    v = run_reduced(1000, 2, 99, 8, 8)
    assert abs(sum(a * a for a in v.values()) - 1) < TOL


def test_against_brute_force():
    rng = random.Random(2026)
    for trial in range(40):
        n = 6 + trial % 3
        k = 2
        x = rng.sample(range(100), n)
        if trial % 2:
            i, j = rng.sample(range(n), 2)
            x[j] = x[i]
        r = default_r(n, k)
        t2 = t2_steps(r, k)
        t1 = best_t1(n, k, r) if collision_sets(x, k) else 1
        got, q = measure_full(x, k, r, t1, t2, rng)
        truth = collision_sets(x, k)
        if not truth:
            assert got is None
        else:
            assert got is None or got == truth[0]
        assert q == queries(r, t1, t2)
    found = 0
    for trial in range(60):
        n = 1000
        x = rng.sample(range(10**6), n)
        if trial % 3:
            i, j = rng.sample(range(n), 2)
            x[j] = x[i]
        got, _ = k_distinctness(x, 2, rng)
        truth = collision_sets(x, 2)
        if not truth:
            assert got is None
        elif got is not None:
            assert got == sorted(truth[0])
            found += 1
    assert found >= 25  # 40 inputs with a collision, success probability 0.81 each
