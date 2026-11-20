# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brownian-dynamics/. The authors are listed in prov/1T83PZ.jsonl.
import math
import random

import pytest

from brownian_dynamics import brownian_dynamics, constant_force, free, harmonic, rpy_tensor
from scimat import cholesky, matmul, transpose


def test_harmonic_well_has_the_exact_discrete_stationary_variance():
    # x' = (1 - c) x + sqrt(2 D h) R with c = D k h / kT has stationary
    # variance (kT / k) / (1 - c / 2). Here c = 0.5, so the variance is 4/3
    # where the continuous process gives 1.
    n, h, d, kT, k = 400, 0.5, 1.0, 1.0, 1.0
    rng = random.Random(1)
    x = [[0.0] for _ in range(n)]
    x, samples = brownian_dynamics(x, harmonic(k), h, 300, kT, d, rng, every=2)
    vals = [p[0] ** 2 for s in samples[10:] for p in s]
    var = sum(vals) / len(vals)
    c = d * k * h / kT
    assert var == pytest.approx((kT / k) / (1 - c / 2), rel=0.03)


def test_small_step_gives_the_boltzmann_variance():
    n, h = 400, 0.02
    rng = random.Random(2)
    x = [[rng.gauss(0.0, 1.0)] for _ in range(n)]
    _, samples = brownian_dynamics(x, harmonic(1.0), h, 400, 1.0, 1.0, rng, every=20)
    vals = [p[0] ** 2 for s in samples for p in s]
    assert sum(vals) / len(vals) == pytest.approx(1.0 / (1 - 0.01), rel=0.04)


def test_free_mean_square_displacement_is_2_d_D_t():
    n, h, steps, d = 400, 0.1, 50, 0.7
    rng = random.Random(3)
    x0 = [[0.0, 0.0] for _ in range(n)]
    x, _ = brownian_dynamics(x0, free(), h, steps, 1.0, [d] * n, rng)
    msd = sum(p[0] ** 2 + p[1] ** 2 for p in x) / n
    t = h * steps
    # |dx|^2 / (2 D t) is chi-squared with 2 degrees of freedom: variance 4
    assert msd == pytest.approx(4 * d * t, abs=4 * 2 * d * t * 2 / math.sqrt(n))


def test_constant_force_gives_drift_D_F_over_kT():
    n, h, steps, d, kT = 400, 0.1, 20, 0.5, 2.0
    rng = random.Random(4)
    x, _ = brownian_dynamics([[0.0]] * n, constant_force([3.0]), h, steps, kT, d, rng)
    mean = sum(p[0] for p in x) / n
    t = h * steps
    assert mean == pytest.approx(d * 3.0 * t / kT, abs=4 * math.sqrt(2 * d * t / n))


def test_tensor_noise_has_covariance_2_D_h():
    # A fixed 2 by 2 diffusion tensor for one particle in 2D, no force.
    dm = [[1.0, 0.6], [0.6, 0.5]]
    rng = random.Random(5)
    _, samples = brownian_dynamics([[0.0, 0.0]], free(), 0.1, 4000, 1.0, lambda pos: dm, rng)
    prev = [0.0, 0.0]
    acc = [[0.0, 0.0], [0.0, 0.0]]
    for s in samples:
        dx = [s[0][0] - prev[0], s[0][1] - prev[1]]
        prev = s[0]
        for i in range(2):
            for j in range(2):
                acc[i][j] += dx[i] * dx[j] / len(samples)
    for i in range(2):
        for j in range(2):
            assert acc[i][j] == pytest.approx(2 * 0.1 * dm[i][j], abs=0.01)


def test_tensor_drift_is_D_F_over_kT():
    # Same fixed tensor with a constant force: the mean step is h D f / kT.
    dm = [[1.0, 0.6], [0.6, 0.5]]
    rng = random.Random(6)
    x, _ = brownian_dynamics([[0.0, 0.0]], constant_force([1.0, -2.0]), 0.1, 4000, 2.0, lambda pos: dm, rng)
    t = 0.1 * 4000
    expect = [t * (1.0 * 1.0 + 0.6 * -2.0) / 2.0, t * (0.6 * 1.0 + 0.5 * -2.0) / 2.0]
    for a in range(2):
        assert x[0][a] == pytest.approx(expect[a], abs=4 * math.sqrt(2 * dm[a][a] * t))


def test_rpy_tensor_is_symmetric_positive_definite_and_has_stokes_einstein_diagonal():
    rng = random.Random(7)
    a, kT, eta = 1.0, 1.0, 1.0
    tensor = rpy_tensor(a, kT, eta)
    for spread in (0.5, 2.0, 10.0):  # overlapping, near and far spheres
        pos = [[rng.uniform(0, spread) for _ in range(3)] for _ in range(4)]
        dm = tensor(pos)
        assert all(dm[i][j] == dm[j][i] for i in range(12) for j in range(12))
        low = cholesky(dm)
        back = matmul(low, transpose(low))
        assert max(abs(back[i][j] - dm[i][j]) for i in range(12) for j in range(12)) < 1e-12
        assert dm[0][0] == pytest.approx(kT / (6 * math.pi * eta * a), rel=1e-12)


def test_rpy_tensor_is_continuous_at_contact_and_decays_like_oseen():
    tensor = rpy_tensor(1.0, 1.0, 1.0)
    d0 = 1.0 / (6 * math.pi)
    inside = tensor([[0.0, 0.0, 0.0], [2.0 - 1e-9, 0.0, 0.0]])
    outside = tensor([[0.0, 0.0, 0.0], [2.0 + 1e-9, 0.0, 0.0]])
    assert inside[0][3] == pytest.approx(outside[0][3], abs=1e-8)
    assert outside[0][3] == pytest.approx(d0 * (7 / 16 + 3 / 16), abs=1e-8)
    far = tensor([[0.0, 0.0, 0.0], [1000.0, 0.0, 0.0]])
    # Oseen limit along the line of centers: kT / (4 pi eta r)
    assert far[0][3] == pytest.approx(1.0 / (4 * math.pi * 1000.0), rel=1e-5)


def test_bad_arguments_raise():
    with pytest.raises(ValueError):
        brownian_dynamics([[0.0]], free(), 0.1, 1, 1.0, -1.0, random.Random(0))
