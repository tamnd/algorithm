# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/final-gathering/. The authors are listed in prov/9YA41P.jsonl.

import math
import random

from final_gathering import (
    NORMALS,
    Room,
    exact_indirect_irradiance,
    exact_radiance,
    final_gather,
    gauss_legendre,
    photon_radiance,
    trace_photons,
)

ROOM = Room(2.0, 2.0, 1.0, 0.75, 1.25, 0.75, 1.25, 1.0, 0.5)
CENTER = (1.0, 1.0, 0.0)
UP = (0.0, 0.0, 1.0)


def test_lambert_formula_matches_quadrature_over_the_emitter():
    gl = gauss_legendre(30)
    for y, n in [((0.0, 0.7, 0.4), NORMALS[0]), ((1.3, 2.0, 0.9), NORMALS[3]), ((0.2, 0.3, 0.0), UP)]:
        total = 0.0
        for gu, wu in gl:
            for gv, wv in gl:
                e = (1.0 + 0.25 * gu, 1.0 + 0.25 * gv, 1.0)
                dv = (e[0] - y[0], e[1] - y[1], e[2] - y[2])
                d2 = dv[0] ** 2 + dv[1] ** 2 + dv[2] ** 2
                cos_y = (n[0] * dv[0] + n[1] * dv[1] + n[2] * dv[2]) / math.sqrt(d2)
                cos_e = dv[2] / math.sqrt(d2)
                total += wu * wv * 0.0625 * cos_y * cos_e / d2
        assert math.isclose(ROOM.direct_irradiance(y, n), total, rel_tol=1e-10)


def test_exact_reference_has_converged():
    for x in (CENTER, (0.3, 1.5, 0.0)):
        assert math.isclose(exact_indirect_irradiance(ROOM, x, 20), exact_indirect_irradiance(ROOM, x, 40), rel_tol=1e-5)


def test_photon_lookup_matches_brute_force_and_keeps_the_power():
    direct, _ = trace_photons(ROOM, 3000, 0.15, random.Random(1))
    assert math.isclose(sum(p for _, _, p in direct.photons), math.pi * 0.25, rel_tol=1e-12)
    rng = random.Random(2)
    for _ in range(200):
        wall = rng.randrange(5)
        y = ROOM.wall_point(wall, 2 * rng.random(), rng.random()) if wall < 4 else (2 * rng.random(), 2 * rng.random(), 0.0)
        assert math.isclose(direct.flux_within(wall, y), direct.flux_within_brute_force(wall, y), abs_tol=1e-15)


def test_gather_with_exact_radiance_is_unbiased():
    exact = exact_indirect_irradiance(ROOM, CENTER)
    vals = [final_gather(ROOM, CENTER, UP, 8, exact_radiance(ROOM), random.Random(s)) for s in range(200)]
    m = sum(vals) / len(vals)
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))
    assert abs(m - exact) < 4 * sd / math.sqrt(len(vals))


def test_final_gathering_beats_the_direct_lookup():
    # The same photons give the one-bounce indirect irradiance at the floor center in two ways:
    # the density of the bounced photons on the floor, or a gather over the direct map of the walls.
    exact = exact_indirect_irradiance(ROOM, CENTER)
    fg, dl = [], []
    for s in range(6):
        rng = random.Random(100 + s)
        direct, indirect = trace_photons(ROOM, 10000, 0.1, rng)
        fg.append((final_gather(ROOM, CENTER, UP, 16, photon_radiance(ROOM, direct), rng) - exact) / exact)
        dl.append((indirect.irradiance(4, CENTER) - exact) / exact)
    rms_fg = math.sqrt(sum(e * e for e in fg) / len(fg))
    rms_dl = math.sqrt(sum(e * e for e in dl) / len(dl))
    assert rms_fg < 0.08
    assert rms_dl > 3 * rms_fg
