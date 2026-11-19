# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/volume-of-fluid-method/. The authors are listed in prov/TBCGQZ.jsonl.
import math
import random

from volume_of_fluid_method import (
    disk_fractions,
    donor_acceptor_flux,
    l1_error,
    smeared_cells,
    total_volume,
    vof_advect,
)


def band(n, x0, x1):
    dx = 1.0 / n
    return [[max(0.0, min((i + 1) * dx, x1) - max(i * dx, x0)) / dx for _ in range(n)] for i in range(n)]


def test_flux_hand_values():
    assert donor_acceptor_flux(1.0, 1.0, 1.0, 0.3) == 0.3  # full cells
    assert abs(donor_acceptor_flux(0.5, 0.0, 0.0, 0.3)) < 1e-15  # front: the void leaves first
    assert abs(donor_acceptor_flux(0.8, 0.0, 0.0, 0.3) - 0.1) < 1e-15
    assert abs(donor_acceptor_flux(0.2, 1.0, 1.0, 0.3) - 0.2) < 1e-15  # back: only what is there
    assert abs(donor_acceptor_flux(0.5, 0.5, 0.5, 0.3) - 0.15) < 1e-15


def test_flux_bounds():
    rng = random.Random(1)
    for _ in range(2000):
        fd, fa, c = rng.random(), rng.random(), rng.random()
        fad = rng.choice((fd, fa))
        q = donor_acceptor_flux(fd, fa, fad, c)
        assert -1e-15 <= q <= min(c, fd) + 1e-15
        assert c - q <= 1.0 - fd + 1e-15  # void given <= void held


def test_band_translation_is_exact():
    n = 20
    dt = 0.3 / n
    one = vof_advect(band(n, 0.2, 0.5), dt, 1, lambda y: 1.0, lambda x: 0.0)
    assert [round(one[i][0], 12) for i in range(3, 12)] == [0.0, 0.7, 1.0, 1.0, 1.0, 1.0, 1.0, 0.3, 0.0]
    F = vof_advect(band(n, 0.2, 0.5), dt, 7, lambda y: 1.0, lambda x: 0.0)
    E = band(n, 0.2 + 7 * dt, 0.5 + 7 * dt)
    assert max(abs(a - b) for ra, rb in zip(F, E) for a, b in zip(ra, rb)) < 1e-13
    G = vof_advect(band(n, 0.2, 0.5), dt, 7, lambda y: -1.0, lambda x: 0.0)
    E = band(n, 0.2 - 7 * dt, 0.5 - 7 * dt)
    assert max(abs(a - b) for ra, rb in zip(G, E) for a, b in zip(ra, rb)) < 1e-13


def test_rotation_conserves_and_stays_bounded():
    n = 32
    w = 2 * math.pi
    F0 = disk_fractions(n, 0.5, 0.75, 0.15)
    assert abs(total_volume(F0) - math.pi * 0.15 ** 2) < 1e-3
    steps = 201
    F = vof_advect(F0, 1.0 / steps, steps, lambda y: -w * (y - 0.5), lambda x: w * (x - 0.5))
    assert abs(total_volume(F) - total_volume(F0)) < 1e-14
    assert min(min(r) for r in F) >= -1e-14 and max(max(r) for r in F) <= 1 + 1e-14
    rel = l1_error(F, F0) / total_volume(F0)
    assert abs(rel - 0.2378) < 5e-4
    U = vof_advect(F0, 1.0 / steps, steps, lambda y: -w * (y - 0.5), lambda x: w * (x - 0.5), "upwind")
    assert abs(total_volume(U) - total_volume(F0)) < 1e-14
    assert smeared_cells(F) < 60 < 800 < smeared_cells(U)


def test_courant_limit_and_bad_input():
    F0 = band(8, 0.2, 0.5)
    for args in ((0.2, 1), (0.0, 1), (0.1, -1)):
        try:
            vof_advect(F0, args[0], args[1], lambda y: 1.0, lambda x: 0.0)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    try:
        vof_advect(F0, 0.1, 1, lambda y: 1.0, lambda x: 0.0, "magic")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
