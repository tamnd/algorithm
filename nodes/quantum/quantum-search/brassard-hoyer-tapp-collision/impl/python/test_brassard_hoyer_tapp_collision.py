# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brassard-hoyer-tapp-collision/. The authors are listed in prov/QEG4BF.jsonl.
import math
import random

from brassard_hoyer_tapp_collision import (
    collision,
    default_k,
    grover_iterations,
    grover_state,
    random_r_to_one,
    success_probability,
)
from qsim import TOL, probabilities


def test_worked_example():
    # N = 64, F(x) = x mod 32, K = {5, 17, 40}
    f = [x % 32 for x in range(64)]
    keys = [5, 17, 40]
    marked = [x not in keys and f[x] in {f[y] for y in keys} for x in range(64)]
    assert [x for x in range(64) if marked[x]] == [8, 37, 49]
    assert grover_iterations(64, 3) == 3
    p = probabilities(grover_state(6, marked, 3))
    assert abs(sum(p[x] for x in (8, 37, 49)) - 0.998139) < 1e-6
    x0, x1, evals = collision(f, 2, 3, random.Random(1), keys=keys)
    assert (x0, x1, evals) == (40, 8, 7)


def test_grover_part_matches_closed_form():
    rng = random.Random(11)
    for n, r in ((6, 2), (7, 2), (7, 4), (8, 2)):
        size = 1 << n
        f = random_r_to_one(n, r, rng)
        k = default_k(size, r)
        while True:
            keys = rng.sample(range(size), k)
            if len({f[x] for x in keys}) == k:  # no collision inside K
                break
        vals = {f[x] for x in keys}
        marked = [x not in keys and f[x] in vals for x in range(size)]
        t = sum(marked)
        assert t == (r - 1) * k
        for j in range(grover_iterations(size, t) + 2):
            p = probabilities(grover_state(n, marked, j))
            got = sum(p[x] for x in range(size) if marked[x])
            assert abs(got - success_probability(size, t, j)) < TOL


def test_collisions_are_correct():
    rng = random.Random(2026)
    for trial in range(30):
        n = 5 + trial % 4
        r = (2, 3, 4)[trial % 3] if trial % 3 != 1 else 2
        if (1 << n) % r:
            r = 2
        f = random_r_to_one(n, r, rng)
        k = default_k(1 << n, r)
        x0, x1, evals = collision(f, r, k, rng)
        assert x0 != x1 and f[x0] == f[x1]
        assert evals >= k


def test_expected_cost_against_brute_force():
    # average evaluations over runs stay near k + (iterations + 1) / p, with p from the closed form
    rng = random.Random(5)
    n, r = 8, 2
    size = 1 << n
    k = default_k(size, r)
    total = 0
    runs = 40
    for _ in range(runs):
        f = random_r_to_one(n, r, rng)
        x0, x1, evals = collision(f, r, k, rng)
        pairs = {(a, b) for a in range(size) for b in range(a + 1, size) if f[a] == f[b]}
        assert (min(x0, x1), max(x0, x1)) in pairs
        total += evals
    it = grover_iterations(size, (r - 1) * k)
    bound = k + (it + 1) / success_probability(size, (r - 1) * k, it)
    assert total / runs <= bound + 1e-9
    assert total / runs < math.sqrt(size)
