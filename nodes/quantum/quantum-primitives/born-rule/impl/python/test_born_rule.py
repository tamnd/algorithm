# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/born-rule/. The authors are listed in prov/K1PK1V.jsonl.

import cmath
import math
import random
from fractions import Fraction

import pytest

from born_rule import (
    exact_probabilities, expectation, marginal, prob_basis, prob_projector, projector_onto, sample_counts,
)
from qsim import basis_state, close, probabilities

R = math.sqrt(0.5)
Z_BASIS = [[1 + 0j, 0j], [0j, 1 + 0j]]
X_BASIS = [[complex(R), complex(R)], [complex(R), complex(-R)]]
Y_BASIS = [[complex(R), 1j * R], [complex(R), -1j * R]]
Z = [[1 + 0j, 0j], [0j, -1 + 0j]]


def rand_state(rng: random.Random, d: int) -> list[complex]:
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)]
    s = math.sqrt(sum(abs(a) ** 2 for a in v))
    return [a / s for a in v]


def test_worked_example_exact() -> None:
    # psi = 3/5 |0> + 4i/5 |1>
    f = Fraction
    assert exact_probabilities([(f(3, 5), f(0)), (f(0), f(4, 5))]) == [f(9, 25), f(16, 25)]
    # the same state in the X basis has amplitudes (3 + 4i)/(5 sqrt 2) and (3 - 4i)/(5 sqrt 2): each squared magnitude is 1/2
    # in the Y basis the amplitudes are (3/5 + 4/5)/sqrt 2 and (3/5 - 4/5)/sqrt 2, with squares 49/50 and 1/50
    assert f(7, 5) ** 2 / 2 == f(49, 50) and f(-1, 5) ** 2 / 2 == f(1, 50)
    psi = [0.6 + 0j, 0.8j]
    assert close(prob_basis(psi, Z_BASIS), [0.36, 0.64])
    assert close(prob_basis(psi, X_BASIS), [0.5, 0.5])
    assert close(prob_basis(psi, Y_BASIS), [0.98, 0.02])
    with pytest.raises(ValueError):
        exact_probabilities([(f(1, 2), f(0)), (f(1, 2), f(0))])


def test_probabilities_sum_to_one_and_ignore_global_phase() -> None:
    rng = random.Random(51)
    for d in (2, 4, 8, 16):
        for _ in range(20):
            s = rand_state(rng, d)
            p = probabilities(s)
            assert abs(sum(p) - 1) < 1e-12 and min(p) >= 0
            g = cmath.exp(1j * rng.uniform(0, 2 * math.pi))
            assert close(probabilities([g * a for a in s]), p)


def test_projector_form_agrees_with_the_basis_form() -> None:
    rng = random.Random(52)
    for _ in range(20):
        s = rand_state(rng, 8)
        p = probabilities(s)
        # P = projector onto span(|1>, |4>, |6>)
        proj = projector_onto([basis_state(3, 1), basis_state(3, 4), basis_state(3, 6)])
        assert abs(prob_projector(s, proj) - (p[1] + p[4] + p[6])) < 1e-12
        # P_+ = |+><+| on one qubit
        t = rand_state(rng, 2)
        assert abs(prob_projector(t, projector_onto([X_BASIS[0]])) - prob_basis(t, X_BASIS)[0]) < 1e-12
        assert abs(expectation(t, Z) - (abs(t[0]) ** 2 - abs(t[1]) ** 2)) < 1e-12


def test_marginals_of_a_bell_state_and_a_product_state() -> None:
    bell = [complex(R), 0j, 0j, complex(R)]
    assert close(marginal(bell, [0]), [0.5, 0.5]) and close(marginal(bell, [1]), [0.5, 0.5])
    assert close(marginal(bell, [0, 1]), [0.5, 0, 0, 0.5])
    # |1> on qubit 1 and |+> on qubit 0: outcome 1 on qubit 1 is certain
    s = [0j, 0j, complex(R), complex(R)]
    assert close(marginal(s, [1]), [0, 1]) and close(marginal(s, [0]), [0.5, 0.5])


def test_amplitudes_add_probabilities_do_not() -> None:
    # (|+> + |->)/sqrt 2 = |0>: the contributions to |1> cancel.
    plus, minus = X_BASIS
    s = [(a + b) * R for a, b in zip(plus, minus)]
    assert close(probabilities(s), [1, 0])
    # The probability of 1 is 0, but each of |+> and |-> alone gives 1/2.
    assert prob_basis(plus, Z_BASIS)[1] > 0.49 and prob_basis(minus, Z_BASIS)[1] > 0.49


def test_rejects_unnormalized_states() -> None:
    with pytest.raises(ValueError):
        prob_basis([1 + 0j, 1 + 0j], Z_BASIS)


def test_sampled_frequencies() -> None:
    rng = random.Random(2026)
    s = [0.6 + 0j, 0.8j]
    shots = 20000
    c = sample_counts(s, shots, rng)
    # Hoeffding: |freq - p| >= 0.02 has probability at most 2 exp(-2 * 20000 * 0.02^2) < 2e-6.
    assert abs(c[0] / shots - 0.36) < 0.02 and sum(c) == shots
    t = rand_state(random.Random(53), 8)
    c = sample_counts(t, shots, rng)
    assert all(abs(k / shots - p) < 0.02 for k, p in zip(c, probabilities(t)))
