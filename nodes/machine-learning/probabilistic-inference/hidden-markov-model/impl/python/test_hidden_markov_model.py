# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hidden-markov-model/. The authors are listed in prov/A7E9ZX.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction as F
from itertools import product

import pytest

from hidden_markov_model import joint, likelihood_by_enumeration, sample, state_marginals, validate

PI = [F(1, 2), F(1, 2)]
A = [[F(7, 10), F(3, 10)], [F(2, 10), F(8, 10)]]
B = [[F(9, 10), F(1, 10)], [F(2, 10), F(8, 10)]]


def rand_row(rng: random.Random, m: int) -> list:
    while True:
        w = [rng.randint(0, 4) for _ in range(m)]
        if sum(w):
            return [F(x, sum(w)) for x in w]


def rand_hmm(rng: random.Random, n: int, m: int):
    return rand_row(rng, n), [rand_row(rng, n) for _ in range(n)], [rand_row(rng, m) for _ in range(n)]


def test_worked_example() -> None:
    validate(PI, A, B)
    assert joint(PI, A, B, [0, 0, 0, 0], [0, 0, 1, 0]) == F(250047, 20000000)
    assert likelihood_by_enumeration(PI, A, B, [0, 0, 1, 0]) == F(982301, 20000000)


def test_joint_is_a_distribution() -> None:
    rng = random.Random(1966)
    for _ in range(30):
        n, m, T = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 4)
        pi, a, b = rand_hmm(rng, n, m)
        total = sum(joint(pi, a, b, q, o) for q in product(range(n), repeat=T) for o in product(range(m), repeat=T))
        assert total == 1


def cond(pi, a, b, T, event, given):
    """P(event | given) by enumeration of all (Q, O); event and given are predicates on (q, o)."""
    n, m = len(pi), len(b[0])
    num = den = F(0)
    for q in product(range(n), repeat=T):
        for o in product(range(m), repeat=T):
            if given(q, o):
                p = joint(pi, a, b, q, o)
                den += p
                if event(q, o):
                    num += p
    return num / den if den else None


def test_conditional_independences() -> None:
    rng = random.Random(7)
    T = 3
    for _ in range(4):
        n, m = 2, 2
        pi, a, b = rand_hmm(rng, n, m)
        for q in product(range(n), repeat=T):
            for o in product(range(m), repeat=T):
                for t in range(T):
                    # output independence: o_t depends only on q_t
                    r = cond(pi, a, b, T, lambda qq, oo: oo[t] == o[t],
                             lambda qq, oo: qq == q and all(oo[s] == o[s] for s in range(T) if s != t))
                    if r is not None:
                        assert r == b[q[t]][o[t]]
                for t in range(T - 1):
                    # Markov property of the hidden chain, also given the past outputs
                    r = cond(pi, a, b, T, lambda qq, oo: qq[t + 1] == q[t + 1],
                             lambda qq, oo: qq[: t + 1] == q[: t + 1] and oo[: t + 1] == o[: t + 1])
                    if r is not None:
                        assert r == a[q[t]][q[t + 1]]


def test_outputs_alone_are_not_markov() -> None:
    # P(o_3 = u | o_2 = u, o_1) depends on o_1, so the outputs are not a first-order Markov chain
    p_uu = cond(PI, A, B, 3, lambda q, o: o[2] == 0, lambda q, o: o[:2] == (0, 0))
    p_nu = cond(PI, A, B, 3, lambda q, o: o[2] == 0, lambda q, o: o[:2] == (1, 0))
    assert p_uu != p_nu


def test_state_marginals_match_enumeration() -> None:
    rng = random.Random(3)
    pi, a, b = rand_hmm(rng, 3, 2)
    T = 4
    marg = state_marginals(pi, a, T)
    for t in range(T):
        for i in range(3):
            assert marg[t][i] == cond(pi, a, b, T, lambda q, o: q[t] == i, lambda q, o: True)


def test_sampling_frequencies_match_the_joint() -> None:
    pi = [0.3, 0.7]
    a = [[0.6, 0.4], [0.1, 0.9]]
    b = [[0.5, 0.2, 0.3], [0.1, 0.1, 0.8]]
    T, runs = 3, 60000
    rng = random.Random(42)
    counts = Counter(tuple(map(tuple, sample(pi, a, b, T, rng))) for _ in range(runs))
    for q in product(range(2), repeat=T):
        for o in product(range(3), repeat=T):
            p = joint(pi, a, b, q, o)
            sd = math.sqrt(p * (1 - p) / runs)
            assert abs(counts[(q, o)] / runs - p) <= 5 * sd + 1e-12
    # zero-probability pairs never appear
    assert all(joint(pi, a, b, q, o) > 0 for q, o in counts)


def test_sampling_respects_zeros_and_is_reproducible() -> None:
    pi = [1.0, 0.0, 0.0]
    a = [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]]
    b = [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]]
    q, o = sample(pi, a, b, 7, random.Random(1))
    assert q == [0, 1, 2, 0, 1, 2, 0]
    assert o[0] == 0 and o[1] == 1 and o[3] == 0
    assert sample(pi, a, b, 7, random.Random(9)) == sample(pi, a, b, 7, random.Random(9))
    assert sample(pi, a, b, 0, random.Random(9)) == ([], [])


def test_validate_rejects_bad_parameters() -> None:
    with pytest.raises(ValueError):
        validate([0.5, 0.6], [[1, 0], [0, 1]], [[1], [1]])
    with pytest.raises(ValueError):
        validate([1.0], [[1.0]], [[0.5, 0.6]])
    with pytest.raises(ValueError):
        validate([1.0, 0.0], [[1.0, 0.0]], [[1.0], [1.0]])
    with pytest.raises(ValueError):
        joint(PI, A, B, [0], [0, 1])
