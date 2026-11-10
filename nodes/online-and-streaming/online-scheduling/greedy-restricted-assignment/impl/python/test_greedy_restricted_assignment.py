# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-restricted-assignment/. The authors are listed in prov/FJFX7X.jsonl.

import math
import random
from fractions import Fraction

import pytest

from greedy_restricted_assignment import GreedyRestrictedAssignment, greedy_restricted_assignment


def opt(m, jobs):
    """Optimal makespan by trying all assignments, with pruning."""
    order = sorted(range(len(jobs)), key=lambda t: -jobs[t][0])
    best = [sum(p for p, _ in jobs) + 1]

    def rec(k, loads):
        if max(loads) >= best[0]:
            return
        if k == len(order):
            best[0] = max(loads)
            return
        p, eligible = jobs[order[k]]
        for i in sorted(set(eligible)):
            loads[i] += p
            rec(k + 1, loads)
            loads[i] -= p

    rec(0, [0] * m)
    return best[0]


def random_instance(rng, m, n, sizes):
    jobs = []
    for _ in range(n):
        eligible = [i for i in range(m) if rng.random() < 0.5] or [rng.randrange(m)]
        jobs.append((rng.choice(sizes), eligible))
    return jobs


def bound(m):
    return math.ceil(math.log2(m)) + 1


def test_example() -> None:
    jobs = [(2, [0, 1, 2]), (2, [0, 1]), (1, [1, 2]), (3, [0]), (2, [2])]
    assignment, loads = greedy_restricted_assignment(3, jobs)
    assert assignment == [0, 1, 2, 0, 2]
    assert loads == [5, 2, 3]
    assert opt(3, jobs) == 4


def test_edges() -> None:
    assert greedy_restricted_assignment(2, []) == ([], [0, 0])
    assert greedy_restricted_assignment(1, [(3, [0]), (4, [0])]) == ([0, 0], [7])
    with pytest.raises(ValueError):
        greedy_restricted_assignment(2, [(1, [])])
    with pytest.raises(ValueError):
        greedy_restricted_assignment(2, [(1, [2])])
    with pytest.raises(ValueError):
        GreedyRestrictedAssignment(0)


def test_eligibility_is_respected() -> None:
    rng = random.Random(11)
    for _ in range(300):
        m = rng.randint(1, 6)
        jobs = random_instance(rng, m, rng.randint(0, 10), [1, 2, 3, 5])
        assignment, loads = greedy_restricted_assignment(m, jobs)
        assert all(a in eligible for a, (_, eligible) in zip(assignment, jobs))
        assert sum(loads) == sum(p for p, _ in jobs)


def test_competitive_bound() -> None:
    rng = random.Random(7)
    for _ in range(400):
        m = rng.randint(1, 5)
        jobs = random_instance(rng, m, rng.randint(1, 7), [1, 2, 3, 4, 6])
        _, loads = greedy_restricted_assignment(m, jobs)
        assert max(loads) <= bound(m) * opt(m, jobs)


def test_bound_on_every_prefix() -> None:
    rng = random.Random(8)
    for _ in range(100):
        m = rng.randint(2, 4)
        jobs = random_instance(rng, m, 6, [1, 2, 5])
        g = GreedyRestrictedAssignment(m)
        for t, (p, eligible) in enumerate(jobs):
            g.assign(p, eligible)
            assert g.makespan() <= bound(m) * opt(m, jobs[: t + 1])


def test_halving_lemma() -> None:
    rng = random.Random(9)
    for _ in range(200):
        m = rng.randint(1, 5)
        jobs = random_instance(rng, m, rng.randint(1, 7), [1, 2, 3, 7])
        _, loads = greedy_restricted_assignment(m, jobs)
        star = opt(m, jobs)

        def v(x):
            return sum(max(Fraction(0), ell - x) for ell in loads)

        for q in range(0, 4 * (bound(m) + 1)):
            x = Fraction(q * star, 4)
            assert 2 * v(x + star) <= v(x)


def test_unit_jobs_with_opt_one() -> None:
    rng = random.Random(10)
    for _ in range(400):
        m = rng.randint(1, 9)
        n = rng.randint(1, m)
        hidden = rng.sample(range(m), n)
        jobs = []
        for h in hidden:
            eligible = {h} | {i for i in range(m) if rng.random() < 0.4}
            jobs.append((1, sorted(eligible)))
        _, loads = greedy_restricted_assignment(m, jobs)
        assert max(loads) <= m.bit_length()  # floor(log2 m) + 1


def pair_adversary(m, choose):
    """The adversary of the lower bound. Returns the jobs and the witness assignment with load 1."""
    k = m.bit_length() - 1
    active = list(range(2**k))
    jobs, witness = [], []
    while len(active) > 1:
        chosen = []
        for a, b in zip(active[0::2], active[1::2]):
            i = choose(1, [a, b])
            jobs.append((1, [a, b]))
            witness.append(b if i == a else a)
            chosen.append(i)
        active = chosen
    choose(1, [active[0]])
    jobs.append((1, [active[0]]))
    witness.append(active[0])
    return jobs, witness


def test_pair_adversary_forces_greedy() -> None:
    for m in range(1, 33):
        g = GreedyRestrictedAssignment(m)
        jobs, witness = pair_adversary(m, g.assign)
        assert all(w in eligible for w, (_, eligible) in zip(witness, jobs))
        assert len(set(witness)) == len(witness)
        lower = math.ceil(math.log2(m + 1))
        assert g.makespan() == lower == m.bit_length()
        assert g.makespan() <= bound(m)
        if m <= 8:
            assert opt(m, jobs) == 1


def test_identical_machines_is_list_scheduling() -> None:
    rng = random.Random(12)
    for _ in range(300):
        m = rng.randint(1, 4)
        sizes = [rng.randint(1, 9) for _ in range(rng.randint(1, 7))]
        jobs = [(p, list(range(m))) for p in sizes]
        _, loads = greedy_restricted_assignment(m, jobs)
        assert max(loads) * m <= (2 * m - 1) * opt(m, jobs)
