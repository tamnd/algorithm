# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hamiltonian-monte-carlo/. The authors are listed in prov/8S8XNZ.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from hamiltonian_monte_carlo import hamiltonian, hamiltonian_monte_carlo, leapfrog


def ess(xs):
    """Effective sample size by Geyer's initial positive sequence."""
    n = len(xs)
    m = sum(xs) / n
    c = [x - m for x in xs]
    var = sum(v * v for v in c) / n
    if var == 0:
        return 1.0

    def rho(k):
        return sum(c[i] * c[i + k] for i in range(n - k)) / (n * var)

    tau, k = -1.0, 0
    while k + 1 < n:
        g = rho(k) + rho(k + 1)
        if g <= 0:
            break
        tau += 2 * g
        k += 2
    return n / max(tau, 1e-9)


def check_mean(xs, mu, sd):
    # the sample mean has standard error about sd / sqrt(ESS)
    assert abs(sum(xs) / len(xs) - mu) < 5 * sd / math.sqrt(ess(xs))


def std_normal(q):
    return -0.5 * sum(v * v for v in q)


def std_normal_grad(q):
    return [-v for v in q]


A = [[F(2), F(1)], [F(1), F(3)]]  # precision matrix of a 2-D Gaussian


def linear_grad(q):
    return [-(A[i][0] * q[0] + A[i][1] * q[1]) for i in range(2)]


def quartic(q):
    return -sum(v**4 for v in q) / 4


def quartic_grad(q):
    return [-(v**3) for v in q]


def det(m):
    m = [row[:] for row in m]
    n = len(m)
    d = F(1)
    for c in range(n):
        piv = next(r for r in range(c, n) if m[r][c] != 0)
        if piv != c:
            m[c], m[piv] = m[piv], m[c]
            d = -d
        d *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [a - f * b for a, b in zip(m[r], m[c])]
    return d


def test_trace_from_page() -> None:
    q, p = leapfrog(std_normal_grad, [F(1)], [F(0)], F(1, 2), 4)
    assert q == [F(-223, 512)]
    q2, p2 = leapfrog(std_normal_grad, q, [F(3, 2)], F(1, 2), 4)
    dh = (q2[0] ** 2 + p2[0] ** 2 - q[0] ** 2 - F(9, 4)) / 2
    assert abs(math.exp(-float(dh)) - 0.9301) < 1e-4


def test_leapfrog_reversible_exactly() -> None:
    q0, p0 = [F(1), F(-2)], [F(1, 3), F(5, 7)]
    q1, p1 = leapfrog(linear_grad, q0, p0, F(1, 3), 5)
    q2, p2 = leapfrog(linear_grad, q1, [-v for v in p1], F(1, 3), 5)
    assert q2 == q0 and [-v for v in p2] == p0


def test_leapfrog_reversible_nonlinear() -> None:
    q0, p0 = [1.0, -0.4], [0.3, 1.1]
    q1, p1 = leapfrog(quartic_grad, q0, p0, 0.3, 10)
    q2, p2 = leapfrog(quartic_grad, q1, [-v for v in p1], 0.3, 10)
    assert max(abs(a - b) for a, b in zip(q2 + [-v for v in p2], q0 + p0)) < 1e-12


def test_jacobian_determinant_is_one_exactly() -> None:
    # for a linear gradient the leapfrog map is linear; build its 4 x 4 matrix
    cols = []
    for j in range(4):
        e = [F(int(i == j)) for i in range(4)]
        q, p = leapfrog(linear_grad, e[:2], e[2:], F(2, 5), 3)
        cols.append(q + p)
    m = [[cols[j][i] for j in range(4)] for i in range(4)]
    assert det(m) == 1


def test_shadow_hamiltonian_kept_exactly() -> None:
    eps = F(1, 2)
    q, p = [F(1)], [F(0)]
    shadow = p[0] ** 2 / 2 + (1 - eps**2 / 4) * q[0] ** 2 / 2
    for _ in range(6):
        q, p = leapfrog(std_normal_grad, q, p, eps, 1)
        assert p[0] ** 2 / 2 + (1 - eps**2 / 4) * q[0] ** 2 / 2 == shadow
    assert leapfrog(std_normal_grad, [F(1)], [F(0)], eps, 1) == ([F(7, 8)], [F(-15, 32)])


def test_energy_error_is_order_eps_squared() -> None:
    errs = []
    for eps in (0.2, 0.1, 0.05):
        q, p = [1.0], [0.0]
        h0 = hamiltonian(quartic, q, p)
        worst = 0.0
        for _ in range(int(round(5 / eps))):
            q, p = leapfrog(quartic_grad, q, p, eps, 1)
            worst = max(worst, abs(hamiltonian(quartic, q, p) - h0))
        errs.append(worst)
    assert 3.5 < errs[0] / errs[1] < 4.5 and 3.5 < errs[1] / errs[2] < 4.5


def test_standard_normal_moments() -> None:
    rng = random.Random(1)
    chain, acc = hamiltonian_monte_carlo(std_normal, std_normal_grad, [3.0], 0.3, 8, 4000, rng)
    xs = [x[0] for x in chain[200:]]
    check_mean(xs, 0.0, 1.0)
    check_mean([x * x for x in xs], 1.0, math.sqrt(2))
    assert acc / 4000 > 0.9


def test_correlated_gaussian() -> None:
    rho = 0.95
    det_s = 1 - rho * rho

    def log_t(q):
        return -(q[0] ** 2 - 2 * rho * q[0] * q[1] + q[1] ** 2) / (2 * det_s)

    def grad(q):
        return [-(q[0] - rho * q[1]) / det_s, -(q[1] - rho * q[0]) / det_s]

    rng = random.Random(2)
    chain, acc = hamiltonian_monte_carlo(log_t, grad, [0.0, 0.0], 0.15, 15, 4000, rng)
    for i in range(2):
        xs = [x[i] for x in chain]
        check_mean(xs, 0.0, 1.0)
        check_mean([v * v for v in xs], 1.0, math.sqrt(2))
    check_mean([x[0] * x[1] for x in chain], rho, math.sqrt(1 + rho * rho))
    assert acc / 4000 > 0.6


def test_periodic_trajectory_is_not_ergodic() -> None:
    # eps = sqrt(2), L = 2 maps (q, p) to about (-q, -p) on N(0, 1): the chain only flips sign
    rng = random.Random(3)
    chain, acc = hamiltonian_monte_carlo(std_normal, std_normal_grad, [0.7], math.sqrt(2), 2, 50, rng)
    assert acc == 50
    assert all(abs(abs(x[0]) - 0.7) < 1e-9 for x in chain)


def test_bad_inputs() -> None:
    rng = random.Random(4)
    with pytest.raises(ValueError):
        hamiltonian_monte_carlo(std_normal, std_normal_grad, [0.0], 0.0, 5, 10, rng)
    with pytest.raises(ValueError):
        hamiltonian_monte_carlo(std_normal, std_normal_grad, [0.0], 0.1, 0, 10, rng)
