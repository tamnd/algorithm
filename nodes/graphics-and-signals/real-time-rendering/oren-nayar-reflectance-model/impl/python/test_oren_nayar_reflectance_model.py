# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/oren-nayar-reflectance-model/. The authors are listed in prov/TGP977.jsonl.

"""Tests of the qualitative Oren-Nayar model against Lambert and against a 1D reference."""

import math
import random

from oren_nayar_reflectance_model import (
    albedo,
    coefficients,
    oren_nayar,
    oren_nayar_vectors,
    sphere_lit_from_viewer,
)

N = (0.0, 0.0, 1.0)


def sph(t: float, p: float) -> tuple[float, float, float]:
    return (math.sin(t) * math.cos(p), math.sin(t) * math.sin(p), math.cos(t))


def albedo_1d(theta_i: float, sigma: float, steps: int = 20000) -> float:
    """A + (2 B / pi) times the integral of sin(alpha) tan(beta) cos(t) sin(t) dt.

    The integral of max(0, cos dphi) over a full turn is 2, which removes the azimuth.
    """
    a, b = coefficients(sigma)
    dt = (math.pi / 2.0) / steps
    total = 0.0
    for i in range(steps):
        t = (i + 0.5) * dt
        al, be = max(theta_i, t), min(theta_i, t)
        total += math.sin(al) * math.tan(be) * math.cos(t) * math.sin(t)
    return a + 2.0 * b / math.pi * total * dt


def test_coefficients() -> None:
    table = {0.25: (0.9204, 0.1844), 0.5: (0.7845, 0.3309), 1.0: (0.6241, 0.4128), 2.0: (0.5381, 0.4401)}
    for s, (a, b) in table.items():
        ca, cb = coefficients(s)
        assert abs(ca - a) < 5e-5 and abs(cb - b) < 5e-5
    assert coefficients(0.0) == (1.0, 0.0)


def test_smooth_is_lambert() -> None:
    rng = random.Random(1)
    for _ in range(500):
        l = sph(rng.uniform(0, 1.55), rng.uniform(0, 2 * math.pi))
        v = sph(rng.uniform(0, 1.55), rng.uniform(0, 2 * math.pi))
        rho = rng.uniform(0, 1)
        assert abs(oren_nayar_vectors(N, l, v, 0.0, rho) - rho / math.pi) < 1e-15


def test_forms_agree_and_reciprocity() -> None:
    rng = random.Random(2)
    for _ in range(2000):
        ti, pi_ = rng.uniform(0, 1.55), rng.uniform(0, 2 * math.pi)
        tr, pr = rng.uniform(0, 1.55), rng.uniform(0, 2 * math.pi)
        s = rng.uniform(0.0, 1.5)
        f_ang = oren_nayar(ti, tr, math.cos(pr - pi_), s)
        f_vec = oren_nayar_vectors(N, sph(ti, pi_), sph(tr, pr), s)
        assert abs(f_ang - f_vec) < 1e-9 * max(1.0, f_ang)
        assert abs(oren_nayar(tr, ti, math.cos(pi_ - pr), s) - f_ang) < 1e-15
        assert f_ang >= 0.0


def test_backscatter() -> None:
    t = math.radians(60.0)
    assert abs(math.pi * oren_nayar(t, t, 1.0, 0.5) - 1.2808) < 5e-5
    assert abs(math.pi * oren_nayar(t, t, -1.0, 0.5) - 0.7845) < 5e-5
    assert abs(math.pi * oren_nayar(t, t, 1.0, 1.0) - 1.2433) < 5e-5
    assert abs(math.pi * oren_nayar(t, t, -1.0, 1.0) - 0.6241) < 5e-5


def test_albedo() -> None:
    table = {
        0.25: (0.9204, 0.9428, 0.9754, 1.0012, 1.0116),
        0.5: (0.7845, 0.8247, 0.8831, 0.9295, 0.9481),
        1.0: (0.6241, 0.6743, 0.7472, 0.8049, 0.8282),
    }
    for s, vals in table.items():
        for deg, val in zip((0.0, 30.0, 60.0, 80.0, 89.0), vals):
            ref = albedo_1d(math.radians(deg), s)
            assert abs(ref - val) < 5e-4
            assert abs(albedo(math.radians(deg), s, nt=300, npf=32) - ref) < 2e-3
        # At normal incidence tan(beta) = 0, so only A is left (the midpoint rule adds about 4e-5).
        assert abs(albedo(0.0, s, nt=100, npf=8) - coefficients(s)[0]) < 1e-4
        assert abs(albedo_1d(0.0, s, steps=10) - coefficients(s)[0]) < 1e-15


def test_sphere_lit_from_viewer() -> None:
    table = {0.0: (1.0, 0.866, 0.5, 0.1736), 0.5: (0.7845, 0.7621, 0.6404, 0.4571), 1.0: (0.6241, 0.6437, 0.6217, 0.5088)}
    for s, vals in table.items():
        for deg, val in zip((0.0, 30.0, 60.0, 80.0), vals):
            assert abs(sphere_lit_from_viewer(math.radians(deg), s) - val) < 5e-5
