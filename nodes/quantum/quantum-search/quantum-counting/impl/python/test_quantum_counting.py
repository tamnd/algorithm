# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-counting/. The authors are listed in prov/STRRDC.jsonl.

import cmath
import math
import random

from qsim import basis_state, norm
from quantum_counting import (
    counting_state,
    error_bound,
    estimate,
    inverse_qft,
    outcome_probabilities,
    quantum_counting,
)

TOL = 1e-9
GOOD = 8 / math.pi ** 2


def marked_f(n_items: int, n_marked: int, seed: int):
    marked = set(random.Random(seed).sample(range(n_items), n_marked))
    return marked, (lambda x, s=marked: 1 if x in s else 0)


def test_inverse_qft_is_the_inverse_dft() -> None:
    # On 1 to 5 qubits, and on a register that does not start at qubit 0.
    for width in range(1, 6):
        p = 1 << width
        for low in (0, 2):
            for y in range(p):
                state = basis_state(low + width, y << low)
                inverse_qft(state, low, width)
                for k in range(p):
                    want = cmath.exp(-2j * math.pi * y * k / p) / math.sqrt(p)
                    assert abs(state[k << low] - want) < TOL


def test_error_bound_with_probability_8_over_pi2() -> None:
    # Theorem 13 with k = 1: |M~ - M| <= 2 pi sqrt(M (N - M)) / P + pi^2 N / P^2
    # with probability >= 8 / pi^2, checked exactly for every M.
    cases = [(2, (3, 4, 5)), (4, (3, 4, 5, 6)), (5, (3, 4, 5)), (8, (3, 4, 5, 6)),
             (12, (4, 5)), (16, (3, 4, 5, 6)), (32, (4, 5, 6))]
    for n_items, ts in cases:
        for n_marked in range(0, n_items + 1):
            if n_items == 32 and n_marked % 3 != 0 and n_marked not in (1, 31):
                continue
            _, f = marked_f(n_items, n_marked, 13 * n_items + n_marked)
            for t in ts:
                probs = outcome_probabilities(n_items, f, t)
                assert abs(sum(probs) - 1.0) < TOL
                bound = error_bound(n_items, n_marked, t)
                good = sum(p for y, p in enumerate(probs)
                           if abs(estimate(n_items, y, t) - n_marked) <= bound + TOL)
                assert good >= GOOD - TOL


def test_error_bound_k2() -> None:
    # Theorem 12 / 13 with k = 2: probability > 1 - 1/(2(k - 1)) = 1/2.
    for n_items in (8, 16):
        for n_marked in range(0, n_items + 1):
            _, f = marked_f(n_items, n_marked, n_items + 7 * n_marked)
            for t in (3, 4, 5):
                probs = outcome_probabilities(n_items, f, t)
                bound = error_bound(n_items, n_marked, t, k=2)
                good = sum(p for y, p in enumerate(probs)
                           if abs(estimate(n_items, y, t) - n_marked) <= bound + TOL)
                assert good > 0.5


def test_extreme_counts_are_exact() -> None:
    for n_items in (2, 4, 5, 8, 16):
        for t in (2, 3, 4):
            p0 = outcome_probabilities(n_items, lambda x: 0, t)
            assert abs(p0[0] - 1.0) < TOL
            p_all = outcome_probabilities(n_items, lambda x: 1, t)
            assert abs(p_all[(1 << t) // 2] - 1.0) < TOL
            assert abs(estimate(n_items, (1 << t) // 2, t) - n_items) < TOL


def test_exact_when_theta_fits_the_grid() -> None:
    # N = 16, M = 4: theta = pi/6 is not on the grid; M = 8: theta = pi/4
    # gives y in {P/4, 3P/4} with certainty and M~ = 8.
    _, f = marked_f(16, 8, 1)
    probs = outcome_probabilities(16, f, 4)
    assert abs(probs[4] + probs[12] - 1.0) < TOL
    assert abs(estimate(16, 4, 4) - 8) < TOL


def test_state_is_unit_and_queries() -> None:
    _, f = marked_f(16, 3, 5)
    for t in (1, 2, 3, 4, 5):
        state, n, queries = counting_state(16, f, t)
        assert n == 4
        assert queries == (1 << t) - 1
        assert abs(norm(state) - 1.0) < TOL


def test_example_table() -> None:
    # N = 16, M = 3, t = 4: the two most likely outcomes are y = 2 and 14,
    # each giving M~ = 16 sin^2(pi/8) = 2.343.
    _, f = marked_f(16, 3, 99)
    probs = outcome_probabilities(16, f, 4)
    top = sorted(range(16), key=lambda y: -probs[y])[:2]
    assert sorted(top) == [2, 14]
    assert abs(estimate(16, 2, 4) - 2.343) < 1e-3
    assert abs(probs[2] - 0.3855) < 1e-4
    assert abs(probs[13] - 0.0603) < 1e-4
    # The table of the page: t, bound, P(within bound), most likely y, its probability.
    rows = [(4, 3.069, 0.9482, 0.3855), (5, 1.380, 0.8208, 0.2547),
            (6, 0.652, 0.9700, 0.4756), (7, 0.316, 0.9029, 0.4079)]
    for t, bound_want, good_want, top_want in rows:
        probs = outcome_probabilities(16, f, t)
        bound = error_bound(16, 3, t)
        assert abs(bound - bound_want) < 1e-3
        good = sum(p for y, p in enumerate(probs) if abs(estimate(16, y, t) - 3) <= bound)
        assert abs(good - good_want) < 1e-4
        assert abs(max(probs) - top_want) < 1e-4


def test_seeded_runs_match_the_distribution() -> None:
    # N = 16, M = 5, t = 4: 1500 seeded runs. The empirical rate of
    # estimates within the bound is within the Hoeffding tolerance
    # sqrt(ln(2 / 1e-3) / 3000) < 0.051 of the exact rate.
    rng = random.Random(31)
    _, f = marked_f(16, 5, 4)
    t = 4
    probs = outcome_probabilities(16, f, t)
    bound = error_bound(16, 5, t)
    exact_rate = sum(p for y, p in enumerate(probs) if abs(estimate(16, y, t) - 5) <= bound + TOL)
    runs = 1500
    hits = 0
    for _ in range(runs):
        m_est, y, queries = quantum_counting(16, f, t, rng)
        assert queries == 15
        assert abs(m_est - estimate(16, y, t)) < TOL
        if abs(m_est - 5) <= bound + TOL:
            hits += 1
    assert abs(hits / runs - exact_rate) < math.sqrt(math.log(2 / 1e-3) / (2 * runs))
