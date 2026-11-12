# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/irradiance-caching/. The authors are listed in prov/P0YEZ8.jsonl.

import math
import random

from irradiance_caching import (
    BoxRoom,
    IrradianceCache,
    Record,
    render_floor,
    sample_hemisphere,
    weight,
)

ROOM = BoxRoom(2.0, 2.0, 1.0, 0.75, 1.25, 0.75, 1.25, 1.0)


def _unit(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def test_weight_formula():
    rec = Record((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), 1.0, 2.0)
    assert weight(rec, (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)) == math.inf
    assert math.isclose(weight(rec, (0.5, 0.0, 0.0), (0.0, 0.0, 1.0)), 4.0)
    n = (math.sin(0.3), 0.0, math.cos(0.3))
    assert math.isclose(weight(rec, (0.0, 0.0, 0.0), n), 1.0 / math.sqrt(1.0 - math.cos(0.3)))


def test_exact_irradiance_under_the_center_matches_the_rectangle_formula():
    # Four rectangles of 0.25 x 0.25 at the height 1, each with a corner above the point.
    a = 0.25 / math.sqrt(1.0 + 0.25**2)
    f_corner = (1 / (2 * math.pi)) * 2 * a * math.atan(a)
    assert math.isclose(ROOM.exact_floor_irradiance(1.0, 1.0), math.pi * 4 * f_corner, rel_tol=1e-12)


def test_hemisphere_sampling_is_unbiased():
    for px, py in [(1.0, 1.0), (0.3, 1.6)]:
        vals = [sample_hemisphere(ROOM, (px, py, 0.0), 8, random.Random(s))[0] for s in range(200)]
        m = sum(vals) / len(vals)
        sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))
        assert abs(m - ROOM.exact_floor_irradiance(px, py)) < 4 * sd / math.sqrt(len(vals))


def test_harmonic_mean_distance_is_small_near_walls():
    _, r_center = sample_hemisphere(ROOM, (1.0, 1.0, 0.0), 16, random.Random(2))
    _, r_corner = sample_hemisphere(ROOM, (0.05, 0.05, 0.0), 16, random.Random(2))
    assert r_corner < 0.3 * r_center
    # From the center of the floor every wall is at least 1 away and at most sqrt(3) away.
    assert 1.0 <= r_center <= math.sqrt(3.0)


def test_grid_lookup_matches_brute_force():
    rng = random.Random(4)
    for a in (0.3, 0.1):
        cache = IrradianceCache(a, cell=0.25)
        for _ in range(300):
            x = (rng.uniform(0, 2), rng.uniform(0, 2), rng.uniform(0, 1))
            n = _unit((rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), 1.0))
            cache.insert(Record(x, n, rng.random(), rng.uniform(0.05, 1.5)))
        for _ in range(300):
            x = (rng.uniform(0, 2), rng.uniform(0, 2), rng.uniform(0, 1))
            n = _unit((rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), 1.0))
            fast = sorted(id(r) for _, r in cache.valid(x, n))
            slow = sorted(id(r) for _, r in cache.valid_brute_force(x, n))
            assert fast == slow


def test_a_record_reproduces_itself():
    cache = IrradianceCache(0.2, cell=0.5)
    rng = random.Random(0)
    x, n = (0.7, 1.1, 0.0), (0.0, 0.0, 1.0)
    e = cache.irradiance(ROOM, x, n, 8, rng)
    assert len(cache.records) == 1
    assert cache.irradiance(ROOM, x, n, 8, rng) == e
    assert len(cache.records) == 1


def test_error_and_record_count_against_the_exact_irradiance():
    results = []
    for a in (0.4, 0.2, 0.1):
        got, exact, n_records = render_floor(ROOM, 30, 30, a, 8, random.Random(1), exact_records=True)
        rel = [abs(g - e) / e for g, e in zip(got, exact)]
        results.append((a, math.sqrt(sum(r * r for r in rel) / len(rel)), max(rel), n_records))
    rms = [r[1] for r in results]
    counts = [r[3] for r in results]
    assert rms[0] > rms[1] > rms[2]
    assert rms[2] < 0.5 * rms[0]
    assert counts[0] < counts[1] < counts[2] <= 900
    # Each value interpolates records whose weights pass 1/a: they lie within a R_i of the point.
    assert results[-1][2] < 0.4


def test_sampled_records_carry_their_noise():
    # With noisy records the error cannot fall below the noise of one record.
    got, exact, _ = render_floor(ROOM, 20, 20, 0.05, 8, random.Random(3))
    rel = [abs(g - e) / e for g, e in zip(got, exact)]
    rms = math.sqrt(sum(r * r for r in rel) / len(rel))
    assert rms > 0.05
