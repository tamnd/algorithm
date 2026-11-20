# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-flux-sampling/. The authors are listed in prov/0GTKCK.jsonl.
import math
import random

import pytest

from forward_flux_sampling import forward_flux_sampling

# Metropolis random walk on 0..6 with a barrier in the middle, beta = 1.
ENERGY = [0.0, 2.0, 4.0, 5.0, 4.0, 2.0, 0.0]
S = len(ENERGY)
L = S - 1
INTERFACES = [1, 2, 3, 4, 5, 6]


def step(i, rng):
    j = i + (1 if rng.random() < 0.5 else -1)
    if j < 0 or j >= S:
        return i
    if rng.random() < math.exp(-(ENERGY[j] - ENERGY[i])):
        return j
    return i


def lam(x):
    return x


def in_a(x):
    return x == 0


def exact():
    """k_AB, the flux and the crossing probabilities of the walk, per step.

    With the committor q (q(0) = 0, q(L) = 1), the equilibrium pi and
    p(x, x+1), the rate of A to B transitions per step of time in the region
    of A is k = pi(0) p(0, 1) q(1) / sum_x pi(x) (1 - q(x)). The flux is
    the same without q(1), and P(i+1 | i) = q(i) / q(i+1).
    """
    w = [math.exp(-e) for e in ENERGY]
    pi = [v / sum(w) for v in w]
    up = [0.5 * min(1.0, math.exp(-(ENERGY[x + 1] - ENERGY[x]))) for x in range(L)]
    r = [1.0 / (pi[x] * up[x]) for x in range(L)]
    q = [sum(r[:x]) / sum(r) for x in range(S)]
    den = sum(pi[x] * (1.0 - q[x]) for x in range(S))
    flux = pi[0] * up[0] / den
    probabilities = [q[i] / q[i + 1] for i in range(1, L)]
    return flux * q[1], flux, probabilities


def test_exact_values_of_the_page():
    k, flux, probabilities = exact()
    assert k == pytest.approx(1.02696e-3, rel=1e-4)
    assert flux == pytest.approx(0.058484, rel=1e-4)
    assert probabilities[0] == pytest.approx(1.0 / (1.0 + math.e ** 2))
    assert flux * math.prod(probabilities) == pytest.approx(k)


def test_estimates_agree_with_the_exact_values():
    k, flux, exact_p = exact()
    rate, f, probabilities, work = forward_flux_sampling(0, step, lam, in_a, INTERFACES, random.Random(1), 2000, 300)
    assert work <= 10000
    # For this walk every point on an interface is the same state, so each
    # estimate is a binomial proportion of 300 trials.
    for p_hat, p in zip(probabilities, exact_p):
        assert abs(p_hat - p) < 3.0 * math.sqrt(p * (1.0 - p) / 300)
    assert f == pytest.approx(flux, rel=0.2)
    assert rate == pytest.approx(k, rel=0.5)
    assert rate == pytest.approx(f * math.prod(probabilities))


def test_jumps_over_interfaces_by_hand():
    def jump(x, rng):
        return min(x + 2, L)
    rate, f, probabilities, work = forward_flux_sampling(0, jump, lam, in_a, INTERFACES, FirstChoice(), 5, 3)
    # Flux run: 0 -> 2 (a crossing of lam_0 = 1), 4, then 6 in B. Time in the
    # region of A is 2 steps, so the flux is 1/2. Points at 2 and 4 already lie
    # on the next interface and need no step.
    assert f == 0.5
    assert probabilities == [1.0] * 5
    assert rate == 0.5
    assert work == 5 + 3 * 2


class FirstChoice:
    def choice(self, seq):
        return seq[0]


def test_no_success_gives_rate_zero():
    def back_to_a(x, rng):
        return 1 if x == 0 else 0
    rate, f, probabilities, _ = forward_flux_sampling(0, back_to_a, lam, in_a, INTERFACES, FirstChoice(), 10, 4)
    assert f == pytest.approx(0.5)
    assert probabilities == [0.0] and rate == 0.0
