# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hp-finite-element-method/. The authors are listed in prov/9VWB60.jsonl.

import math
import random

import hp_finite_element_method as H


def rel_error(nodes, degrees, model):
    u, moment, energy = model
    _, _, bTU = H.solve_hp(nodes, degrees, u, moment)
    return H.energy_error(energy, bTU) / math.sqrt(energy)


def test_hand_example_one_quadratic_element():
    u = lambda x: x - x * x
    moment = H.quadrature_moment(lambda x: 1 - 2 * x)
    V, C, bTU = H.solve_hp([0.0, 1.0], [2], u, moment)
    assert V == []
    assert abs(C[0][0] + math.sqrt(1.5) / 3) < 1e-14
    assert abs(bTU - 1.0 / 3.0) < 1e-14  # |u|_1^2 = 1/3, so the error is 0
    for x in (0.1, 0.5, 0.8):
        assert abs(H.evaluate([0.0, 1.0], V, C, x) - u(x)) < 1e-14


def test_bubbles_are_orthonormal_in_energy():
    xs, ws = H.gauss_legendre(20)
    for k in range(2, 9):
        for m in range(2, 9):
            val = sum(w * math.sqrt((2 * k - 1) / 2) * H.legendre(k - 1, t)
                      * math.sqrt((2 * m - 1) / 2) * H.legendre(m - 1, t) for t, w in zip(xs, ws))
            assert abs(val - (1.0 if k == m else 0.0)) < 1e-13
        # orthogonal to the hats, whose derivative is constant
        assert abs(sum(w * H.legendre(k - 1, t) for t, w in zip(xs, ws))) < 1e-14


def test_gauss_legendre_rule():
    xs, ws = H.gauss_legendre(7)
    assert abs(sum(ws) - 2) < 1e-14
    for d in range(14):
        exact = 0.0 if d % 2 else 2.0 / (d + 1)
        assert abs(sum(w * x ** d for x, w in zip(xs, ws)) - exact) < 1e-14


def test_singular_moments_are_exact():
    _, moment, _ = H.corner_model(0.7)
    xs, ws = H.gauss_legendre(200)
    b = 0.3
    for j in range(0, 6):
        total = 0.0
        for s, w in zip(xs, ws):  # t = r^10 removes the singularity at 0
            r = (s + 1) / 2
            t = r ** 10
            x = b * t
            total += w * 5 * r ** 9 * 2 * (0.7 * x ** -0.3 - 1) * H.legendre(j, 2 * t - 1)
        assert abs(total - moment(0.0, b, j)) < 1e-10


def test_nodal_values_are_exact_on_random_meshes():
    model = H.corner_model(0.7)
    u, moment, _ = model
    rng = random.Random(3)
    for _ in range(5):
        n = rng.randint(2, 12)
        nodes = sorted([0.0, 1.0] + [rng.uniform(0.01, 0.99) for _ in range(n - 1)])
        degrees = [rng.randint(1, 5) for _ in range(n)]
        V, C, _ = H.solve_hp(nodes, degrees, u, moment)
        for i, v in enumerate(V):
            assert abs(v - u(nodes[i + 1])) < 1e-12


def test_h_and_p_versions_are_algebraic():
    model = H.corner_model(0.7)
    e1 = rel_error([i / 64 for i in range(65)], [1] * 64, model)
    e2 = rel_error([i / 256 for i in range(257)], [1] * 256, model)
    slope_h = math.log(e2 / e1) / math.log(255 / 63)
    assert -0.22 < slope_h < -0.18  # N^(-0.2)
    e3 = rel_error([0.0, 1.0], [9], model)
    e4 = rel_error([0.0, 1.0], [17], model)
    slope_p = math.log(e4 / e3) / math.log(16 / 8)
    assert -0.44 < slope_p < -0.36  # N^(-0.4)


def test_geometric_hp_is_exponential_in_sqrt_n():
    u, moment, energy = H.corner_model(0.7)
    rows = []
    for n in (12, 20):
        N, _, _, bTU = H.hp_geometric(n, 0.15, 0.5, u, moment)
        rows.append((N, H.energy_error(energy, bTU) / math.sqrt(energy)))
    (n1, e1), (n2, e2) = rows
    assert (n1, n2) == (41, 109)
    assert e2 < 1e-3
    b = -math.log(e2 / e1) / (math.sqrt(n2) - math.sqrt(n1))
    assert 0.7 < b < 0.8
    e_uniform = rel_error([i / 1024 for i in range(1025)], [1] * 1024, (u, moment, energy))
    assert e_uniform > 100 * e2


def test_geometric_mesh_alone_stalls():
    model = H.corner_model(0.7)
    e1 = rel_error(H.geometric_mesh(16, 0.15), [1] * 16, model)
    e2 = rel_error(H.geometric_mesh(32, 0.15), [1] * 32, model)
    assert abs(e1 - e2) < 1e-3 * e1 + 1e-6  # the error of the last element with p = 1 stays


def test_smooth_solution_converges_exponentially_in_p():
    u = lambda x: math.sin(math.pi * x)
    moment = H.quadrature_moment(lambda x: math.pi * math.cos(math.pi * x))
    nodes = [0.0, 0.5, 1.0]
    errs = []
    for p in (2, 4, 6, 8):
        V, C, _ = H.solve_hp(nodes, [p, p], u, moment)
        errs.append(max(abs(H.evaluate(nodes, V, C, x) - u(x)) for x in (0.13, 0.3, 0.71)))
    assert errs[3] < 1e-8
    assert all(b < a / 50 for a, b in zip(errs, errs[1:]))
