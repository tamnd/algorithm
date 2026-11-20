# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variational-network-mri/. The authors are listed in prov/THXH29.jsonl.

import math
import random

from variational_network_mri import (
    filter_adjoint,
    filter_apply,
    foe_energy,
    foe_regularizer,
    forward_differences,
    make_operator,
    variational_network,
)

N1, N2 = 6, 5


def rand_c(rng):
    return complex(rng.gauss(0, 1), rng.gauss(0, 1))


def rand_image(rng):
    return [rand_c(rng) for _ in range(N1 * N2)]


def rand_mask(rng):
    return [1 if rng.random() < 0.5 else 0 for _ in range(N1 * N2)]


def two_coils(rng):
    c1, c2 = [], []
    for _ in range(N1 * N2):
        a, b = rand_c(rng), rand_c(rng)
        s = math.sqrt(abs(a) ** 2 + abs(b) ** 2)
        c1.append(a / s)
        c2.append(b / s)
    return [c1, c2]


def re_inner(u, v):
    return sum((a.conjugate() * b).real for a, b in zip(u, v))


def charbonnier(eps):
    return (lambda z: math.sqrt(z * z + eps * eps)), (lambda z: z / math.sqrt(z * z + eps * eps))


def energy(u, f, apply_a, lam, eps):
    phi, _ = charbonnier(eps)
    kern = forward_differences()
    fit = sum(abs(a - b) ** 2 for ac, fc in zip(apply_a(u), f) for a, b in zip(ac, fc))
    return foe_energy(u, kern, [phi] * 4, N1, N2) + 0.5 * lam * fit


def gradient_stage(alpha, lam, eps):
    """One stage that is alpha times the gradient of energy(., lam, eps)."""
    _, dphi = charbonnier(eps)
    reg = foe_regularizer(forward_differences(), [lambda z: alpha * dphi(z)] * 4, N1, N2)
    return reg, alpha * lam


def test_operator_adjoint():
    rng = random.Random(1)
    mask = rand_mask(rng)
    for coils in (None, two_coils(rng)):
        apply_a, apply_ah = make_operator(mask, N1, N2, coils)
        u = rand_image(rng)
        y = [rand_image(rng) for _ in range(1 if coils is None else 2)]
        lhs = sum(sum(a.conjugate() * b for a, b in zip(ac, yc)) for ac, yc in zip(apply_a(u), y))
        rhs = sum(a.conjugate() * b for a, b in zip(u, apply_ah(y)))
        assert abs(lhs - rhs) < 1e-10 * abs(lhs)


def test_filter_adjoint():
    rng = random.Random(2)
    kernel = (
        {(di, dj): rng.gauss(0, 1) for di in (-1, 0, 1) for dj in (-1, 0, 1)},
        {(di, dj): rng.gauss(0, 1) for di in (-1, 0, 1) for dj in (0, 2)},
    )
    u = rand_image(rng)
    z = [rng.gauss(0, 1) for _ in range(N1 * N2)]
    lhs = sum(a * b for a, b in zip(filter_apply(kernel, u, N1, N2), z))
    rhs = re_inner(u, filter_adjoint(kernel, z, N1, N2))
    assert abs(lhs - rhs) < 1e-10 * abs(lhs)


def test_forward_difference_filter_norm():
    # sum_i K_i^T K_i is minus the periodic Laplacian on Re u and on Im u; its norm is at most 8.
    rng = random.Random(3)
    kern = forward_differences()
    u = rand_image(rng)
    for _ in range(30):
        v = [0j] * (N1 * N2)
        for k in kern:
            w = filter_adjoint(k, filter_apply(k, u, N1, N2), N1, N2)
            v = [a + b for a, b in zip(v, w)]
        nv = math.sqrt(re_inner(v, v))
        u = [a / nv for a in v]
    assert 0 < nv <= 8 + 1e-9


def test_stage_is_a_gradient_step_on_a_known_energy():
    rng = random.Random(4)
    mask = rand_mask(rng)
    coils = two_coils(rng)
    apply_a, apply_ah = make_operator(mask, N1, N2, coils)
    f = apply_a(rand_image(rng))
    u0 = rand_image(rng)
    alpha, lam, eps = 0.01, 3.0, 0.5
    reg, lam_t = gradient_stage(alpha, lam, eps)
    hist = []

    def ah_start(data):
        return u0 if data is f else apply_ah(data)

    variational_network(f, [(reg, lam_t)], apply_a, ah_start, hist)
    grad = [(a - b) / alpha for a, b in zip(hist[0], hist[1])]
    for _ in range(3):
        h = rand_image(rng)
        s = 1e-5
        plus = energy([a + s * b for a, b in zip(u0, h)], f, apply_a, lam, eps)
        minus = energy([a - s * b for a, b in zip(u0, h)], f, apply_a, lam, eps)
        assert abs((plus - minus) / (2 * s) - re_inner(grad, h)) < 1e-5 * (1 + abs(re_inner(grad, h)))


def test_energy_decreases_for_safe_steps():
    rng = random.Random(5)
    mask = rand_mask(rng)
    apply_a, apply_ah = make_operator(mask, N1, N2)
    f = apply_a(rand_image(rng))
    lam, eps = 4.0, 0.2
    alpha = 1.0 / (8.0 / eps + lam)
    hist = []
    variational_network(f, [gradient_stage(alpha, lam, eps)] * 8, apply_a, apply_ah, hist)
    for u, v in zip(hist, hist[1:]):
        step = sum(abs(a - b) ** 2 for a, b in zip(u, v))
        assert energy(v, f, apply_a, lam, eps) <= energy(u, f, apply_a, lam, eps) - step / (2 * alpha) + 1e-9


def test_call_counts():
    rng = random.Random(6)
    apply_a, apply_ah = make_operator(rand_mask(rng), N1, N2)
    calls = {"a": 0, "ah": 0, "net": 0}

    def a(u):
        calls["a"] += 1
        return apply_a(u)

    def ah(d):
        calls["ah"] += 1
        return apply_ah(d)

    def net(u):
        calls["net"] += 1
        return [0.1 * v for v in u]

    f = apply_a(rand_image(rng))
    u = variational_network(f, [(net, 0.5)] * 7, a, ah)
    assert calls == {"a": 7, "ah": 8, "net": 7}
    assert len(u) == N1 * N2


def test_no_regularizer_is_landweber():
    rng = random.Random(7)
    apply_a, apply_ah = make_operator(rand_mask(rng), N1, N2)
    f = apply_a(rand_image(rng))
    zero = lambda u: [0j] * len(u)
    u = variational_network(f, [(zero, 0.7)] * 3, apply_a, apply_ah)
    # u_0 = A^* f is consistent with the data, so Landweber steps keep it.
    u0 = apply_ah(f)
    assert max(abs(a - b) for a, b in zip(u, u0)) < 1e-12
