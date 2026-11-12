# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mean-field-approximation/. The authors are listed in prov/0P6CAT.jsonl.

import math
import random

from mean_field_approximation import bound, exact, kl_q_p, mean_field, neighbors


def random_ising(rng, n, p_edge=0.5, scale=1.0):
    h = [rng.uniform(-1, 1) for _ in range(n)]
    edges = [(i, j, rng.uniform(-scale, scale)) for i in range(n) for j in range(i + 1, n) if rng.random() < p_edge]
    return h, edges


def test_lower_bound_on_log_z():
    rng = random.Random(11)
    for _ in range(40):
        n = rng.randint(2, 9)
        h, edges = random_ising(rng, n, scale=rng.choice([0.3, 1.0, 2.0]))
        m, val, _ = mean_field(h, edges, m0=[rng.uniform(-1, 1) for _ in range(n)])
        log_z, _ = exact(h, edges)
        assert val <= log_z + 1e-12


def test_each_update_does_not_decrease_the_bound():
    rng = random.Random(12)
    for _ in range(30):
        n = rng.randint(2, 8)
        h, edges = random_ising(rng, n, scale=1.5)
        _, _, _, trace = mean_field(h, edges, m0=[rng.uniform(-1, 1) for _ in range(n)], trace=True)
        for u, v in zip(trace, trace[1:]):
            assert v >= u - 1e-12


def test_increase_is_at_least_half_the_squared_step():
    # L is 1-strongly concave in m_i, and the update maximizes it in m_i.
    rng = random.Random(13)
    h, edges = random_ising(rng, 6, scale=1.0)
    nb = neighbors(6, edges)
    m = [rng.uniform(-0.9, 0.9) for _ in range(6)]
    for i in range(6):
        before = bound(h, edges, m)
        new = math.tanh(h[i] + sum(w * m[j] for j, w in nb[i]))
        step = new - m[i]
        m[i] = new
        assert bound(h, edges, m) - before >= 0.5 * step * step - 1e-12


def test_fixed_point_equations_hold():
    rng = random.Random(14)
    h, edges = random_ising(rng, 7, scale=0.5)
    m, _, _ = mean_field(h, edges, tol=1e-13)
    nb = neighbors(7, edges)
    for i in range(7):
        assert abs(m[i] - math.tanh(h[i] + sum(w * m[j] for j, w in nb[i]))) < 1e-12


def test_exact_without_couplings():
    h = [0.4, -1.3, 0.0, 2.0]
    m, val, _ = mean_field(h, [])
    log_z, means = exact(h, [])
    assert abs(val - log_z) < 1e-12
    assert max(abs(a - b) for a, b in zip(m, means)) < 1e-12


def test_two_spin_example_from_the_page():
    h, edges = [0.0, 0.0], [(0, 1, 2.0)]
    m, val, _ = mean_field(h, edges, m0=[0.0, 0.1])
    assert abs(m[0] - 0.9575040240771567) < 1e-9 and abs(m[1] - m[0]) < 1e-9
    assert abs(val - 2.0393421359737385) < 1e-9
    log_z, means = exact(h, edges)
    assert abs(log_z - math.log(2 * math.exp(2) + 2 * math.exp(-2))) < 1e-12
    assert means == [0.0, 0.0]
    assert abs(kl_q_p(h, edges, m) - (log_z - val)) < 1e-12


def test_mode_seeking_on_symmetric_ferromagnet():
    # Zero fields and strong couplings: p is symmetric, every exact mean is 0,
    # but mean field from a random start picks one of the two modes.
    edges = [(0, 1, 1.0), (1, 2, 1.0), (2, 3, 1.0), (3, 0, 1.0)]
    h = [0.0] * 4
    _, means = exact(h, edges)
    assert max(abs(v) for v in means) < 1e-12
    rng = random.Random(15)
    signs = set()
    for _ in range(20):
        m, _, _ = mean_field(h, edges, m0=[rng.uniform(-1, 1) for _ in range(4)])
        assert min(abs(v) for v in m) > 0.9
        assert len({v > 0 for v in m}) == 1
        signs.add(m[0] > 0)
    assert signs == {True, False}


def test_zero_is_a_worse_fixed_point_above_the_critical_coupling():
    h, edges = [0.0, 0.0], [(0, 1, 2.0)]
    zero = bound(h, edges, [0.0, 0.0])
    assert abs(zero - 2 * math.log(2)) < 1e-12
    _, val, _ = mean_field(h, edges, m0=[0.5, 0.5])
    assert val > zero
