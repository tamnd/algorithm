# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-signal-processing/. The authors are listed in prov/9B38VZ.jsonl.

import cmath
import math
import random

from quantum_signal_processing import (
    find_phases,
    qsp_polynomial,
    qsp_unitary,
    reflection_form,
    reflection_sequence,
    to_reflection_phases,
)
from qsim import chebyshev_t

GRID = [-1 + 2 * k / 200 for k in range(201)]


def chebyshev_u(k, x):
    """U_k(x), the Chebyshev polynomial of the second kind (U_(-1) = 0)."""
    if k < 0:
        return 0.0
    a, b = 1.0, 2 * x
    if k == 0:
        return a
    for _ in range(k - 1):
        a, b = b, 2 * x * b - a
    return b


def chebyshev_coefficients(g, n):
    """The first n Chebyshev coefficients of g, from n Chebyshev nodes (exact for degree < n)."""
    xs = [math.cos((j + 0.5) * math.pi / n) for j in range(n)]
    vals = [g(x) for x in xs]
    out = []
    for k in range(n):
        c = sum(v * math.cos(k * (j + 0.5) * math.pi / n) for j, v in enumerate(vals)) * 2 / n
        out.append(c / 2 if k == 0 else c)
    return out


def test_hand_example_degree_one():
    # Phi = (pi/6, pi/6): P(x) = e^(i pi/3) x, so Re P = x/2.
    ph = find_phases(lambda x: x / 2, 1)
    assert all(abs(p - math.pi / 6) < 1e-12 for p in ph)
    for x in GRID:
        assert abs(qsp_polynomial(ph, x) - cmath.exp(1j * math.pi / 3) * x) < 1e-12


def test_zero_phases_give_chebyshev_polynomials():
    # W(x)^d = e^(i d theta X) with x = cos(theta): P = T_d and the corner is i sqrt(1 - x^2) U_(d-1).
    for d in range(9):
        for x in GRID:
            u = qsp_unitary([0.0] * (d + 1), x)
            s = math.sqrt(1 - x * x)
            assert abs(u[0][0] - chebyshev_t(d, x)) < 1e-11
            assert abs(u[0][1] - 1j * s * chebyshev_u(d - 1, x)) < 1e-11


def test_lemma_9_chebyshev_phases_in_the_reflection_convention():
    # Gilyen, Su, Low and Wiebe, Lemma 9: phi_1 = (1 - d) pi/2 and phi_j = pi/2 for j >= 2 give P = T_d.
    for d in range(1, 9):
        phases = [(1 - d) * math.pi / 2] + [math.pi / 2] * (d - 1)
        for x in GRID:
            assert abs(reflection_sequence(phases, x)[0][0] - chebyshev_t(d, x)) < 1e-11


def test_reflection_conversion():
    rng = random.Random(31)
    for d in [1, 2, 5]:
        phases = [rng.uniform(-math.pi, math.pi) for _ in range(d + 1)]
        psi = to_reflection_phases(phases)
        for x in GRID[::10]:
            a, b = reflection_form(psi, x), qsp_unitary(phases, x)
            for i in range(2):
                for j in range(2):
                    assert abs(a[i][j] - (-1j) ** d * b[i][j]) < 1e-12


def test_theorem_3_properties_for_random_phases():
    # Degree at most d, parity d mod 2 for P and (d - 1) mod 2 for Q, and |P|^2 + (1 - x^2)|Q|^2 = 1.
    rng = random.Random(32)
    for d in [3, 4, 7]:
        phases = [rng.uniform(-math.pi, math.pi) for _ in range(d + 1)]
        for x in GRID:
            u = qsp_unitary(phases, x)
            s2 = 1 - x * x
            p = u[0][0]
            q = u[0][1] / (1j * math.sqrt(s2)) if s2 > 1e-6 else None
            assert abs(qsp_polynomial(phases, -x) - (-1) ** d * p) < 1e-12
            if q is not None:
                assert abs(abs(p) ** 2 + s2 * abs(q) ** 2 - 1) < 1e-12
        for part in (lambda x: qsp_polynomial(phases, x).real, lambda x: qsp_polynomial(phases, x).imag):
            coeffs = chebyshev_coefficients(part, d + 6)
            assert max(abs(c) for c in coeffs[d + 1:]) < 1e-12
            assert max(abs(c) for c in coeffs[(d + 1) % 2::2]) < 1e-12  # the other parity is absent


def random_parity_polynomial(rng, d, bound):
    """A random real Chebyshev sum of parity d mod 2 and degree d, scaled so max |f| on the grid is bound."""
    coeffs = [rng.uniform(-1, 1) if k % 2 == d % 2 else 0.0 for k in range(d + 1)]
    fine = [math.cos(math.pi * j / 2000) for j in range(2001)]
    peak = max(abs(sum(c * chebyshev_t(k, x) for k, c in enumerate(coeffs))) for x in fine)
    coeffs = [c * bound / peak for c in coeffs]
    return lambda x: sum(c * chebyshev_t(k, x) for k, c in enumerate(coeffs))


def test_found_phases_reproduce_random_targets_on_a_grid():
    rng = random.Random(33)
    for d in [2, 3, 5, 8, 11]:
        f = random_parity_polynomial(rng, d, 0.9)
        ph = find_phases(f, d)
        assert len(ph) == d + 1
        assert all(abs(ph[j] - ph[d - j]) < 1e-15 for j in range(d + 1))  # symmetric
        assert max(abs(qsp_polynomial(ph, x).real - f(x)) for x in GRID) < 1e-10


def test_the_example_of_degree_three():
    f = lambda x: (x ** 3 + x) / 4
    ph = find_phases(f, 3)
    assert abs(ph[0] - 0.752429) < 1e-6 and abs(ph[1] + 0.228830) < 1e-6
    assert max(abs(qsp_polynomial(ph, x).real - f(x)) for x in GRID) < 1e-12


def test_minus_phases_give_the_conjugate_so_two_branches_give_the_real_part():
    # <0|U_(-Phi)|0> = P^*, so the average of the two sequences has Re P in the corner.
    rng = random.Random(34)
    for d in [2, 5]:
        ph = [rng.uniform(-math.pi, math.pi) for _ in range(d + 1)]
        neg = [-p for p in ph]
        for x in GRID[::5]:
            p, pm = qsp_polynomial(ph, x), qsp_polynomial(neg, x)
            assert abs(pm - p.conjugate()) < 1e-12
            assert abs((p + pm) / 2 - p.real) < 1e-12
