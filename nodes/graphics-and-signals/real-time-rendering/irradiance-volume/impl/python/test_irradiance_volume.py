# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/irradiance-volume/. The authors are listed in prov/CE3Y53.jsonl.

"""Tests of the irradiance volume against a brute force blend and a dict model.

The sample at a probe is the probe, affine fields of coefficients are
reproduced exactly, the weights form a partition of unity, the blend is
linear in the probe data and equals a sum of tensor-product hat functions
over all probes, random stores and samples agree with a dict model, and a
thin wall between two probes shows the light leak that the page describes.
"""

import math
import random

import pytest

from irradiance_volume import IrradianceVolume, eval_sh, irradiance_coeffs, sh9


def rand_dir(rng: random.Random) -> tuple[float, float, float]:
    while True:
        v = (rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1))
        r = math.sqrt(sum(c * c for c in v))
        if r > 1e-6:
            return (v[0] / r, v[1] / r, v[2] / r)


def rand_coeffs(rng: random.Random) -> list[float]:
    return [rng.uniform(-1, 1) for _ in range(9)]


def hat(u: float) -> float:
    return max(0.0, 1.0 - abs(u))


def brute_force(vol: IrradianceVolume, p) -> list[float]:
    """Sum over every probe of its coefficients times the product of three hat functions."""
    g = []
    for a in range(3):
        x = (p[a] - vol.origin[a]) / vol.spacing
        g.append(min(max(x, 0.0), vol.dims[a] - 1.0))
    nx, ny, nz = vol.dims
    out = [0.0] * 9
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                w = hat(g[0] - i) * hat(g[1] - j) * hat(g[2] - k)
                if w:
                    pr = vol.probe(i, j, k)
                    for m in range(9):
                        out[m] += w * pr[m]
    return out


def test_point_light_probe() -> None:
    # One probe lit by a unit point light from +z: E(+z) = 17/16, E(-z) = 1/16, E(+x) = 3/32.
    vol = IrradianceVolume(dims=(2, 2, 2))
    vol.bake(lambda p: irradiance_coeffs(sh9((0.0, 0.0, 1.0))))
    for p in ((0, 0, 0), (0.3, 0.7, 0.2), (5, -3, 2)):
        assert abs(vol.sample(p, (0, 0, 1)) - 17 / 16) < 1e-12
        assert abs(vol.sample(p, (0, 0, -1)) - 1 / 16) < 1e-12
        assert abs(vol.sample(p, (1, 0, 0)) - 3 / 32) < 1e-12


def test_sample_at_probe_is_the_probe() -> None:
    rng = random.Random(1)
    vol = IrradianceVolume(origin=(-1.0, 2.0, 0.5), spacing=0.75, dims=(3, 4, 2))
    vol.bake(lambda p: rand_coeffs(rng))
    for i in range(3):
        for j in range(4):
            for k in range(2):
                got = vol.sample_coeffs(vol.probe_position(i, j, k))
                assert all(abs(a - b) < 1e-12 for a, b in zip(got, vol.probe(i, j, k)))


def test_affine_fields_are_exact() -> None:
    rng = random.Random(2)
    base = rand_coeffs(rng)
    grad = [rand_coeffs(rng) for _ in range(3)]

    def field(p):
        return [base[m] + sum(grad[a][m] * p[a] for a in range(3)) for m in range(9)]

    vol = IrradianceVolume(origin=(0.0, 0.0, 0.0), spacing=0.5, dims=(4, 3, 5))
    vol.bake(field)
    for _ in range(500):
        p = (rng.uniform(0, 1.5), rng.uniform(0, 1.0), rng.uniform(0, 2.0))
        got = vol.sample_coeffs(p)
        assert all(abs(a - b) < 1e-12 for a, b in zip(got, field(p)))


def test_weights_are_a_partition_of_unity() -> None:
    rng = random.Random(3)
    vol = IrradianceVolume(spacing=1.0, dims=(3, 3, 3))
    c = rand_coeffs(rng)
    vol.bake(lambda p: c)
    for _ in range(500):
        p = (rng.uniform(-2, 4), rng.uniform(-2, 4), rng.uniform(-2, 4))
        assert all(abs(a - b) < 1e-12 for a, b in zip(vol.sample_coeffs(p), c))
        (i, j, k), f = vol.cell_and_weights(p)
        assert all(0.0 <= x <= 1.0 for x in f)
        assert 0 <= i <= 1 and 0 <= j <= 1 and 0 <= k <= 1


def test_blend_is_linear_and_matches_brute_force() -> None:
    rng = random.Random(4)
    dims = (4, 3, 3)
    a = IrradianceVolume(origin=(1.0, -1.0, 0.0), spacing=0.4, dims=dims)
    b = IrradianceVolume(origin=(1.0, -1.0, 0.0), spacing=0.4, dims=dims)
    s = IrradianceVolume(origin=(1.0, -1.0, 0.0), spacing=0.4, dims=dims)
    for i in range(dims[0]):
        for j in range(dims[1]):
            for k in range(dims[2]):
                ca, cb = rand_coeffs(rng), rand_coeffs(rng)
                a.set_probe(i, j, k, ca)
                b.set_probe(i, j, k, cb)
                s.set_probe(i, j, k, [2 * x - 3 * y for x, y in zip(ca, cb)])
    for _ in range(300):
        p = (rng.uniform(0.5, 2.6), rng.uniform(-1.5, 0.2), rng.uniform(-0.3, 1.2))
        n = rand_dir(rng)
        assert abs(s.sample(p, n) - (2 * a.sample(p, n) - 3 * b.sample(p, n))) < 1e-12
        got, want = a.sample_coeffs(p), brute_force(a, p)
        assert all(abs(x - y) < 1e-12 for x, y in zip(got, want))
        assert abs(a.sample(p, n) - eval_sh(want, n)) < 1e-12


def test_random_operations_against_a_dict() -> None:
    rng = random.Random(5)
    dims = (3, 2, 4)
    vol = IrradianceVolume(origin=(0.0, 0.0, 0.0), spacing=2.0, dims=dims)
    model = {}
    for _ in range(1500):
        if rng.random() < 0.5:
            key = (rng.randrange(dims[0]), rng.randrange(dims[1]), rng.randrange(dims[2]))
            c = rand_coeffs(rng)
            vol.set_probe(*key, c)
            model[key] = c
        else:
            key = (rng.randrange(dims[0]), rng.randrange(dims[1]), rng.randrange(dims[2]))
            n = rand_dir(rng)
            want = eval_sh(model.get(key, [0.0] * 9), n)
            assert abs(vol.sample(vol.probe_position(*key), n) - want) < 1e-12
            p = (rng.uniform(0, 4), rng.uniform(0, 2), rng.uniform(0, 6))
            ref = IrradianceVolume(origin=(0.0, 0.0, 0.0), spacing=2.0, dims=dims)
            for kk, cc in model.items():
                ref.set_probe(*kk, cc)
            assert abs(vol.sample(p, n) - eval_sh(brute_force(ref, p), n)) < 1e-12
        vol.check_invariant()


def test_light_leak_through_a_thin_wall() -> None:
    # A measurement of the failure, not a property to rely on: probes at x = 0 are in a
    # dark room, probes at x = 1 in a bright one, and a wall stands at x = 0.5. A point
    # at x = 0.4, still on the dark side, gets 40 percent of the bright irradiance.
    vol = IrradianceVolume(spacing=1.0, dims=(2, 2, 2))
    bright = irradiance_coeffs(sh9((0.0, 0.0, 1.0)))
    for j in range(2):
        for k in range(2):
            vol.set_probe(0, j, k, [0.0] * 9)
            vol.set_probe(1, j, k, bright)
    e = vol.sample((0.4, 0.5, 0.5), (0, 0, 1))
    assert abs(e - 0.4 * 17 / 16) < 1e-12


def test_bad_arguments() -> None:
    with pytest.raises(ValueError):
        IrradianceVolume(dims=(1, 2, 2))
    with pytest.raises(ValueError):
        IrradianceVolume(spacing=0.0)
    with pytest.raises(ValueError):
        IrradianceVolume().set_probe(0, 0, 0, [1.0, 2.0])
