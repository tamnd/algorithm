# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swendsen-wang/. The authors are listed in prov/PXDRJN.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

import pytest

from swendsen_wang import clusters, swendsen_wang, transition_matrix


def autocorrelation_time(xs):
    """Integrated autocorrelation time by Geyer's initial positive sequence."""
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
    return max(tau, 1e-9)


def check_mean(xs, mu, sd):
    # the sample mean has standard error about sd * sqrt(tau / n)
    assert abs(sum(xs) / len(xs) - mu) < 5 * sd * math.sqrt(autocorrelation_time(xs) / len(xs))


def grid(rows, cols):
    e = []
    for i in range(rows):
        for j in range(cols):
            v = i * cols + j
            if j + 1 < cols:
                e.append((v, v + 1))
            if i + 1 < rows:
                e.append((v, v + cols))
    return e


def torus(size):
    e = []
    for i in range(size):
        for j in range(size):
            v = i * size + j
            e.append((v, i * size + (j + 1) % size))
            e.append((v, ((i + 1) % size) * size + j))
    return e


def agreements(edges, s):
    return sum(s[u] == s[v] for u, v in edges)


def potts_law(edges, states, p):
    # pi(sigma) is proportional to exp(J * agreements) = (1 / (1 - p)) ** agreements
    w = [(1 / (1 - p)) ** agreements(edges, s) for s in states]
    z = sum(w)
    return [x / z for x in w]


@pytest.mark.parametrize(
    "n, edges, q, p",
    [(6, grid(2, 3), 2, F(1, 2)), (4, [(0, 1), (1, 2), (0, 2), (2, 3)], 3, F(1, 3))],
)
def test_exact_kernel_is_reversible_and_positive(n, edges, q, p) -> None:
    states, mat = transition_matrix(n, edges, q, p)
    pi = potts_law(edges, states, p)
    m = len(states)
    assert all(sum(row) == 1 for row in mat)
    assert all(pi[i] * mat[i][j] == pi[j] * mat[j][i] for i in range(m) for j in range(m))
    assert [sum(pi[i] * mat[i][j] for i in range(m)) for j in range(m)] == pi
    # all bonds closed has positive probability, so every state is reached in one step
    assert all(v > 0 for row in mat for v in row)


def test_edwards_sokal_marginals() -> None:
    n, edges, q, p = 4, [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)], 3, F(2, 5)
    states = list(itertools.product(range(q), repeat=n))
    subsets = list(itertools.product((0, 1), repeat=len(edges)))

    def joint(s, a):
        w = F(1)
        for (u, v), bit in zip(edges, a):
            w *= (p if s[u] == s[v] else 0) if bit else 1 - p
        return w

    pi = potts_law(edges, states, p)
    z = sum(joint(s, a) for s in states for a in subsets)
    for s, target in zip(states, pi):
        assert sum(joint(s, a) for a in subsets) / z == target
    fk = [p ** sum(a) * (1 - p) ** (len(edges) - sum(a)) * q ** (max(clusters(n, [e for e, b in zip(edges, a) if b])) + 1) for a in subsets]
    for a, w in zip(subsets, fk):
        assert sum(joint(s, a) for s in states) / z == w / sum(fk)


def test_page_example_path() -> None:
    p = F(3, 10)
    states, mat = transition_matrix(3, [(0, 1), (1, 2)], 2, p)
    i, j = states.index((0, 0, 1)), states.index((0, 0, 0))
    assert mat[i][j] == p / 4 + (1 - p) / 8


BETA_C = math.log(1 + math.sqrt(2)) / 2


def exact_ising(size, beta):
    edges = torus(size)
    n = size * size
    z = m2 = 0.0
    for code in range(1 << n):
        s = [1 if code >> v & 1 else -1 for v in range(n)]
        w = math.exp(beta * sum(s[u] * s[v] for u, v in edges))
        z += w
        m2 += w * (sum(s) / n) ** 2
    return m2 / z


def metropolis(size, beta, n_sweeps, rng):
    n = size * size
    nb = [[] for _ in range(n)]
    for u, v in torus(size):
        nb[u].append(v)
        nb[v].append(u)
    s = [1] * n
    total = n
    out = []
    for _ in range(n_sweeps):
        for v in range(n):
            d = 2 * s[v] * sum(s[w] for w in nb[v])
            if d <= 0 or rng.random() < math.exp(-beta * d):
                s[v] = -s[v]
                total += 2 * s[v]
        out.append((total / n) ** 2)
    return out


def sw_m2(size, beta, n_steps, rng):
    n = size * size
    chain = swendsen_wang(n, torus(size), 2, 1 - math.exp(-2 * beta), [0] * n, n_steps, rng)
    return [(sum(1 if x == 0 else -1 for x in s) / n) ** 2 for s in chain]


def test_ising_magnetization_matches_brute_force() -> None:
    exact = exact_ising(4, BETA_C)
    assert abs(exact - 0.7613589) < 1e-6
    sd = math.sqrt(exact * (1 - exact))  # m^2 lies in [0, 1], so its variance is at most E m^2 (1 - E m^2)
    check_mean(sw_m2(4, BETA_C, 20000, random.Random(1)), exact, sd)
    check_mean(metropolis(4, BETA_C, 20000, random.Random(1)), exact, sd)


def test_potts_three_states_matches_brute_force() -> None:
    size, q, p = 3, 3, 0.5
    edges = torus(size)
    n = size * size
    w = z = 0.0
    for s in itertools.product(range(q), repeat=n):
        a = agreements(edges, s)
        weight = 2.0**a
        z += weight
        w += weight * a
    exact = w / z
    chain = swendsen_wang(n, edges, q, p, [0] * n, 20000, random.Random(4))
    check_mean([agreements(edges, s) for s in chain], exact, len(edges) / 2)


def test_less_critical_slowing_down_than_metropolis() -> None:
    tau_sw = autocorrelation_time(sw_m2(16, BETA_C, 10000, random.Random(1)))
    tau_metropolis = autocorrelation_time(metropolis(16, BETA_C, 10000, random.Random(1)))
    assert tau_sw < 10 < tau_metropolis


def test_bad_inputs() -> None:
    rng = random.Random(5)
    with pytest.raises(ValueError):
        swendsen_wang(2, [(0, 1)], 1, 0.5, [0, 0], 5, rng)
    with pytest.raises(ValueError):
        swendsen_wang(2, [(0, 1)], 2, 1.0, [0, 0], 5, rng)
    with pytest.raises(ValueError):
        swendsen_wang(2, [(0, 1)], 2, 0.5, [0, 2], 5, rng)
    with pytest.raises(ValueError):
        swendsen_wang(2, [(0, 0)], 2, 0.5, [0, 1], 5, rng)
