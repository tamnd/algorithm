# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-normalization/. The authors are listed in prov/FFNMF4.jsonl.

import math
import random

from spectral_normalization import (SpectralNorm, matvec, norm, power_step, relu_net, sn_weight_grad,
                                    top_singular)


def rand_mat(rng: random.Random, r: int, c: int):
    return [[rng.gauss(0.0, 1.0) for _ in range(c)] for _ in range(r)]


def test_exact_value_on_a_known_matrix() -> None:
    sigma, u, v = top_singular([[3.0, 0.0], [4.0, 5.0]])
    assert math.isclose(sigma, 3 * math.sqrt(5), rel_tol=1e-12)
    assert math.isclose(abs(v[0]), 1 / math.sqrt(2), rel_tol=1e-9)


def test_exact_value_matches_frobenius_and_determinant_checks() -> None:
    rng = random.Random(0)
    w = rand_mat(rng, 2, 2)
    s1, _, _ = top_singular(w)
    det = abs(w[0][0] * w[1][1] - w[0][1] * w[1][0])
    fro2 = sum(a * a for row in w for a in row)
    s2 = det / s1
    assert math.isclose(s1 * s1 + s2 * s2, fro2, rel_tol=1e-10)


def test_power_estimate_never_exceeds_and_converges_to_sigma() -> None:
    rng = random.Random(1)
    for r, c in [(3, 4), (5, 2), (4, 4), (2, 6)]:
        w = rand_mat(rng, r, c)
        exact, _, _ = top_singular(w)
        u = [rng.gauss(0.0, 1.0) for _ in range(r)]
        u = [a / norm(u) for a in u]
        prev = 0.0
        for _ in range(1000):
            u, _, est = power_step(w, u)
            assert est <= exact * (1 + 1e-12)
            assert est >= prev * (1 - 1e-12)
            prev = est
        assert math.isclose(est, exact, rel_tol=1e-9)


def test_one_step_per_update_tracks_a_fixed_matrix() -> None:
    rng = random.Random(2)
    w = rand_mat(rng, 4, 3)
    exact, _, _ = top_singular(w)
    layer = SpectralNorm(4, random.Random(3))
    errors = []
    for _ in range(60):
        w_sn, sigma = layer.normalize(w)
        errors.append(exact - sigma)
    assert errors[-1] < 1e-9 and errors[0] >= errors[-1]
    assert math.isclose(top_singular(w_sn)[0], exact / sigma, rel_tol=1e-12)
    assert top_singular(w_sn)[0] >= 1 - 1e-12


def test_one_step_per_update_tracks_a_slowly_moving_matrix() -> None:
    rng = random.Random(4)
    w = rand_mat(rng, 5, 4)
    layer = SpectralNorm(5, random.Random(5))
    for _ in range(30):
        layer.normalize(w)
    for _ in range(50):
        w = [[a + 0.001 * rng.gauss(0.0, 1.0) for a in row] for row in w]
        _, sigma = layer.normalize(w)
        exact, _, _ = top_singular(w)
        assert 0 <= exact - sigma < 1e-3 * exact


def test_normalized_relu_network_is_one_lipschitz() -> None:
    rng = random.Random(6)
    ws = []
    for r, c in [(6, 4), (5, 6), (3, 5)]:
        w = rand_mat(rng, r, c)
        s, _, _ = top_singular(w)
        ws.append([[a / s for a in row] for row in w])
    for _ in range(200):
        x = [rng.gauss(0.0, 2.0) for _ in range(4)]
        y = [rng.gauss(0.0, 2.0) for _ in range(4)]
        fx, fy = relu_net(ws, x), relu_net(ws, y)
        assert norm([a - b for a, b in zip(fx, fy)]) <= norm([a - b for a, b in zip(x, y)]) * (1 + 1e-12)
    s, _, v = top_singular(ws[0])
    assert math.isclose(norm(matvec(ws[0], v)), 1.0, rel_tol=1e-9)


def test_gradient_through_sigma_matches_central_differences() -> None:
    rng = random.Random(7)
    w = rand_mat(rng, 3, 4)
    c = rand_mat(rng, 3, 4)

    def loss(m):
        s, _, _ = top_singular(m)
        return sum(ci * a / s for crow, row in zip(c, m) for ci, a in zip(crow, row))

    grad = sn_weight_grad(w, c)
    h = 1e-6
    for i in range(3):
        for j in range(4):
            wp = [row[:] for row in w]
            wm = [row[:] for row in w]
            wp[i][j] += h
            wm[i][j] -= h
            assert abs((loss(wp) - loss(wm)) / (2 * h) - grad[i][j]) < 1e-6
