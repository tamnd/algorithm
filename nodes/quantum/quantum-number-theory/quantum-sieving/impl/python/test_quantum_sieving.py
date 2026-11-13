# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-sieving/. The authors are listed in prov/Y3ARK8.jsonl.
"""Tests of the Gauss sieve with quantum (BBHT) partner search, with fixed seeds."""

import math
import random

import pytest

import qsim
from quantum_sieving import (
    Counter,
    classical_search,
    dot,
    gauss_sieve,
    goldstein_mayer_basis,
    grover_measure,
    in_goldstein_mayer,
    norm2,
    quantum_search,
    shortest_length2,
)


def grover_state(marked, q, j):
    """The state after j Grover iterations, built gate by gate with qsim."""
    state = qsim.basis_state(q, 0)
    for k in range(q):
        qsim.apply_1q(state, k, qsim.H)
    for _ in range(j):
        qsim.apply_diagonal(state, lambda i: math.pi if marked[i] else 0.0)  # the oracle
        for k in range(q):
            qsim.apply_1q(state, k, qsim.H)
        qsim.apply_diagonal(state, lambda i: 0.0 if i == 0 else math.pi)  # 2|0><0| - I
        for k in range(q):
            qsim.apply_1q(state, k, qsim.H)
    return state


@pytest.mark.parametrize("q,marked_set", [(3, {5}), (4, {3, 7, 12}), (5, {0, 9, 17, 30}), (2, {0, 1, 3})])
def test_grover_state_matches_closed_form(q, marked_set):
    size = 1 << q
    marked = [i in marked_set for i in range(size)]
    theta = math.asin(math.sqrt(len(marked_set) / size))
    for j in range(8):
        probs = qsim.probabilities(grover_state(marked, q, j))
        p_good = math.sin((2 * j + 1) * theta) ** 2
        for i in range(size):
            want = p_good / len(marked_set) if marked[i] else (1 - p_good) / (size - len(marked_set))
            assert abs(probs[i] - want) < 1e-9


def test_sampler_matches_state_vector():
    q, marked_set = 4, {3, 7, 12}
    marked = [i in marked_set for i in range(16)]
    rng = random.Random(4)
    for j in (0, 1, 2, 5):
        probs = qsim.probabilities(grover_state(marked, q, j))
        trials = 20000
        freq = [0] * 16
        for _ in range(trials):
            freq[grover_measure(marked, q, j, rng)] += 1
        for i in range(16):
            assert abs(freq[i] / trials - probs[i]) < 0.015


def test_overshoot_example():
    """Three marked of four: one iteration gives sin^2(pi) = 0, the reason BBHT draws j at random."""
    probs = qsim.probabilities(grover_state([True, True, False, True], 2, 1))
    assert abs(probs[2] - 1) < 1e-9


def test_quantum_search_returns_only_marked_items():
    rng = random.Random(7)
    items = list(range(600))  # padded to 2^10 indices
    for trial in range(100):
        t = trial % 5
        marked = set(rng.sample(items, t))
        c = Counter()
        i = quantum_search(items, lambda x: x in marked, rng, c)
        if t == 0:
            assert i is None and c.missed == 0
        else:
            assert i is not None and items[i] in marked
    assert quantum_search([], lambda x: True, rng, Counter()) is None


def test_query_counts_against_classical_scan():
    """On 1024 items the mean query count is near sqrt(1024 / t), against about 1024 / (t + 1) for a scan."""
    items = list(range(1024))
    for t, q_bound, c_low in ((1, 2.5 * 32, 400), (4, 2.5 * 16, 150), (16, 2.5 * 8, 40)):
        quantum, classical = [], []
        for seed in range(200):
            rng = random.Random(seed)
            marked = set(rng.sample(items, t))
            cq = Counter()
            assert quantum_search(items, lambda x: x in marked, rng, cq) is not None
            quantum.append(cq.queries)
            cc = Counter()
            classical_search(items, lambda x: x in marked, cc)
            classical.append(cc.queries)
        assert sum(quantum) / 200 < q_bound
        assert sum(classical) / 200 > c_low
    c = Counter()
    assert quantum_search(items, lambda x: False, random.Random(1), c) is None
    assert c.queries <= math.ceil(9 * 32) + 32  # the budget, plus the last round


def test_classical_search_counts_every_check():
    c = Counter()
    assert classical_search([5, 6, 7, 8], lambda x: x == 7, c) == 2 and c.queries == 3
    assert classical_search([5, 6], lambda x: False, c) is None and c.queries == 5


def pairwise_reduced(L):
    return all(2 * abs(dot(u, w)) <= min(norm2(u), norm2(w)) for k, u in enumerate(L) for w in L[k + 1:])


@pytest.mark.parametrize("n,seed", [(4, 0), (5, 1), (6, 2)])
def test_quantum_sieve_finds_a_shortest_vector(n, seed):
    basis = goldstein_mayer_basis(n, 1009, random.Random(seed))
    best, L, counter = gauss_sieve(basis, random.Random(100 + seed), quantum=True)
    assert best is not None and norm2(best) > 0
    assert all(in_goldstein_mayer(v, basis) for v in L)
    l2 = norm2(best)
    assert shortest_length2(basis, math.isqrt(l2) + 1) == l2  # exact check by brute force
    if counter.missed == 0:
        assert pairwise_reduced(L)


def test_classical_sieve_list_is_pairwise_reduced():
    basis = goldstein_mayer_basis(4, 1009, random.Random(0))
    best, L, counter = gauss_sieve(basis, random.Random(100), quantum=False)
    assert counter.missed == 0 and pairwise_reduced(L)
    assert norm2(best) == shortest_length2(basis, math.isqrt(norm2(best)) + 1) == 17


def test_brute_force_on_a_known_lattice():
    # rows (7, 0) and (3, 1): y_0 = 3 y_1 mod 7; (1, -2) has squared length 5 and nothing shorter exists
    basis = [(7, 0), (3, 1)]
    assert shortest_length2(basis, 3) == 5
    assert in_goldstein_mayer((1, -2), basis) and not in_goldstein_mayer((1, 1), basis)
