# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/numerical-privacy-accounting/. The authors are listed in prov/XTW2ZE.jsonl.

import cmath
import itertools
import math
import random
from fractions import Fraction
from math import comb
from statistics import NormalDist

import pytest

from numerical_privacy_accounting import (
    Pld,
    compose,
    delta_for_epsilon,
    epsilon_for_delta,
    fft,
    gaussian_pld,
    numerical_accountant,
    randomized_response_pld,
)


def gaussian_delta(epsilon, mu):
    """The exact delta of mu-GDP (the Gaussian mechanism), in closed form."""
    phi = NormalDist().cdf
    return phi(-epsilon / mu + mu / 2) - math.exp(epsilon) * phi(-epsilon / mu - mu / 2)


def brute_delta(pld, k, epsilon):
    """An independent oracle: sum over all k-tuples of grid points, no FFT."""
    finite = 1.0 - pld.inf_mass
    total = 1.0 - finite**k
    for idx in itertools.product(range(len(pld.masses)), repeat=k):
        weight = math.prod(pld.masses[j] for j in idx)
        loss = sum(pld.loss(j) for j in idx)
        if weight > 0 and loss > epsilon:
            total += weight * (1 - math.exp(epsilon - loss))
    return min(1.0, total)


def rr_delta_exact(b, k, i):
    """Exact delta of k-fold randomized response with e^eps0 = b, at epsilon = i * eps0.

    The loss is (2j - k) eps0 when j of the k answers have loss +eps0, so
    e^(epsilon - loss) = b^(i - 2j + k), a rational number.
    """
    b = Fraction(b)
    total = Fraction(0)
    for j in range(k + 1):
        ratio = b ** (i - 2 * j + k)
        if ratio < 1:
            total += comb(k, j) * b**j / (1 + b) ** k * (1 - ratio)
    return total


def test_worked_example():
    # Randomized response with eps0 = 1, k = 2 steps, epsilon = 0.
    pld = randomized_response_pld(1, 1.0)
    p = math.e / (1 + math.e)
    composed = compose(pld, 2)
    assert composed.lo == -2
    assert composed.masses[0] == pytest.approx((1 - p) ** 2)
    assert composed.masses[2] == pytest.approx(2 * p * (1 - p))
    assert composed.masses[4] == pytest.approx(p * p)
    want = p * p * (1 - math.exp(-2))
    assert numerical_accountant(pld, 2, 0.0) == pytest.approx(want, abs=1e-12)
    assert want == pytest.approx(0.462117, abs=1e-6)


def test_gaussian_brackets_the_exact_value():
    # 10 Gaussian steps with mu_i = 1 / sqrt(10) compose to exactly 1-GDP.
    k, mu = 10, 1 / math.sqrt(10)
    upper = numerical_accountant(gaussian_pld(mu, 2e-3, pessimistic=True), k, 1.0)
    lower = numerical_accountant(gaussian_pld(mu, 2e-3, pessimistic=False), k, 1.0)
    exact = gaussian_delta(1.0, 1.0)
    assert exact == pytest.approx(0.126937, abs=1e-6)
    assert lower <= exact <= upper
    assert upper - lower < 5e-3


def test_randomized_response_exact_fraction():
    for b_num, k in [(3, 5), (2, 8), (5, 3)]:
        eps0 = math.log(b_num)
        pld = randomized_response_pld(1, eps0)
        for i in range(0, k + 1):
            got = numerical_accountant(pld, k, i * eps0)
            assert got == pytest.approx(float(rr_delta_exact(b_num, k, i)), abs=1e-12)


def test_edges_and_bad_input():
    pld = randomized_response_pld(2, 0.25)
    same = compose(pld, 1)
    assert same.lo == pld.lo
    assert all(abs(a - b) < 1e-15 for a, b in zip(same.masses, pld.masses))
    # Far above the largest loss, only the mass at infinity is left.
    inf_pld = Pld(0, (0.5, 0.25), 1.0, 0.25)
    assert delta_for_epsilon(inf_pld, 100.0) == pytest.approx(0.25)
    assert compose(inf_pld, 3).inf_mass == pytest.approx(1 - 0.75**3)
    # epsilon = 0 for a point mass at loss 0: the two outputs are the same.
    assert numerical_accountant(Pld(0, (1.0,), 0.5), 4, 0.0) == 0.0
    with pytest.raises(ValueError):
        compose(pld, 0)
    with pytest.raises(ValueError):
        fft([1, 2, 3])
    with pytest.raises(ValueError):
        gaussian_pld(0.0, 0.01)
    with pytest.raises(ValueError):
        randomized_response_pld(0, 0.1)
    with pytest.raises(ValueError):
        epsilon_for_delta(inf_pld, 0.2)


def test_fft_against_naive_dft():
    rng = random.Random(11)
    for size in [1, 2, 4, 8, 32]:
        a = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(size)]
        naive = [sum(a[t] * cmath.exp(-2j * math.pi * s * t / size) for t in range(size)) for s in range(size)]
        got = fft(a)
        assert all(abs(x - y) < 1e-9 for x, y in zip(got, naive))
        back = fft(got, invert=True)
        assert all(abs(x - y) < 1e-12 for x, y in zip(back, a))


def test_monotone_in_epsilon_and_steps():
    pld = gaussian_pld(0.5, 0.02)
    composed = compose(pld, 4)
    deltas = [delta_for_epsilon(composed, e / 4) for e in range(13)]
    assert all(x >= y for x, y in zip(deltas, deltas[1:]))
    by_k = [numerical_accountant(pld, k, 1.0) for k in range(1, 6)]
    assert all(x <= y for x, y in zip(by_k, by_k[1:]))


def test_epsilon_for_delta_inverts():
    pld = compose(gaussian_pld(0.5, 0.01), 4)  # close to 1-GDP
    eps = epsilon_for_delta(pld, 1e-5)
    assert delta_for_epsilon(pld, eps) <= 1e-5
    assert delta_for_epsilon(pld, eps - 1e-6) > 1e-5
    # The exact 1-GDP value is 4.3772; the pessimistic grid stays above it.
    assert 4.3772 < eps < 4.42
    assert epsilon_for_delta(pld, 0.9) == 0.0


def test_pessimistic_dominates_single_step():
    for mu in [0.3, 1.0, 2.0]:
        up = gaussian_pld(mu, 0.01)
        down = gaussian_pld(mu, 0.01, pessimistic=False)
        for e in [0.0, 0.5, 1.0, 2.0]:
            exact = gaussian_delta(e, mu)
            assert delta_for_epsilon(down, e) <= exact + 1e-12
            assert exact <= delta_for_epsilon(up, e) + 1e-12


def test_random_against_brute_force():
    rng = random.Random(2106)
    for _ in range(500):
        n = rng.randint(1, 5)
        k = rng.randint(1, 4)
        raw = [rng.random() for _ in range(n)]
        inf_mass = rng.choice([0.0, 0.0, rng.uniform(0.0, 0.1)])
        scale = (1 - inf_mass) / sum(raw)
        pld = Pld(rng.randint(-4, 2), tuple(r * scale for r in raw), rng.choice([0.1, 0.25, 0.5]), inf_mass)
        epsilon = rng.uniform(0.0, 2.0)
        got = numerical_accountant(pld, k, epsilon)
        assert got == pytest.approx(brute_delta(pld, k, epsilon), rel=1e-9, abs=1e-12)
