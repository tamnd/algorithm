# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/percentage-closer-soft-shadows/. The authors are listed in prov/EXXNC3.jsonl.

import random

from percentage_closer_soft_shadows import (
    blocker_search,
    exact_visibility,
    flatland_map,
    pcss,
    penumbra_width,
    search_half_width,
)


def test_example_on_the_page():
    n, d_b, d_r, wl = 1.0, 2.0, 4.0, 1.0
    assert penumbra_width(d_r, d_b, wl) == 1.0
    assert search_half_width(d_r, wl, n, 0.05) == 7.5
    s = flatland_map(64, 0.05, n, d_b, d_r)
    d, count = blocker_search(s, 32.0, 1.5, d_r, wl, n, 0.05, 0.0)
    assert (d, count) == (2.0, 24)
    got = [pcss(s, xw * n / d_r / 0.05 + 32, 1.5, d_r, wl, n, 0.05) for xw in (-0.5, -0.25, 0.0, 0.25, 0.5)]
    assert [round(g, 12) for g in got] == [0.0, 0.2, 0.5, 0.8, 1.0]
    want = [exact_visibility(xw, d_b, d_r, wl) for xw in (-0.5, -0.25, 0.0, 0.25, 0.5)]
    assert want == [0.0, 0.25, 0.5, 0.75, 1.0]


def test_flatland_parallel_planes_match_the_area_light():
    # Precondition: the filter square stays inside the map, so no tap is clamped.
    rng = random.Random(1)
    tested = 0
    while tested < 30:
        n = rng.uniform(0.5, 1.5)
        d_b = n + rng.uniform(0.5, 2.0)
        d_r = d_b + rng.uniform(0.5, 3.0)
        wl = rng.uniform(0.3, 1.5)
        h = 0.0125
        s = flatland_map(64, h, n, d_b, d_r)
        rf = penumbra_width(d_r, d_b, wl) * n / (2 * d_r * h)
        if not 3 <= rf <= 18:
            continue
        tested += 1
        for _ in range(10):
            x = 32 + rng.uniform(-12.0, 12.0)
            xw = (x - 32) * h * d_r / n
            got = pcss(s, x, 1.5, d_r, wl, n, h)
            want = exact_visibility(xw, d_b, d_r, wl)
            assert abs(got - want) <= 1.0 / (2 * rf) + 1e-9


def test_blocker_search_equals_brute_force():
    rng = random.Random(2)
    for _ in range(100):
        w, hh = rng.randrange(4, 20), rng.randrange(4, 20)
        s = [[rng.uniform(1.0, 5.0) for _ in range(w)] for _ in range(hh)]
        x, y = rng.uniform(0, w), rng.uniform(0, hh)
        d_r, wl, n, h = rng.uniform(2.0, 6.0), rng.uniform(0.1, 2.0), 1.0, rng.uniform(0.05, 0.3)
        rs = wl * (d_r - n) / (2 * d_r * h)
        taps = [s[j][i] for j in range(hh) for i in range(w)
                if abs(i + 0.5 - x) <= rs and abs(j + 0.5 - y) <= rs]
        if not taps:
            taps = [s[min(int(y), hh - 1)][min(int(x), w - 1)]]
        near = [t for t in taps if t < d_r]
        d, count = blocker_search(s, x, y, d_r, wl, n, h, 0.0)
        assert count == len(near)
        if near:
            assert abs(d - sum(near) / len(near)) < 1e-12


def test_search_region_holds_every_blocker_of_the_light():
    # A point on the segment from the receiver to a point of the light, at a
    # depth in [n, d_r), projects within the search half-width of the receiver.
    rng = random.Random(3)
    for _ in range(2000):
        n, d_r = rng.uniform(0.2, 1.0), rng.uniform(1.5, 8.0)
        wl, h = rng.uniform(0.1, 2.0), rng.uniform(0.01, 0.2)
        xr = rng.uniform(-3.0, 3.0)
        xl = rng.uniform(-wl / 2, wl / 2)
        z = rng.uniform(n, d_r)
        xp = xr + (xl - xr) * (d_r - z) / d_r
        u_p, u_r = xp * n / z, xr * n / d_r
        assert abs(u_p - u_r) / h <= search_half_width(d_r, wl, n, h) + 1e-9


def test_no_blocker_is_lit_and_no_light_size_is_the_hard_test():
    s = [[5.0] * 8 for _ in range(8)]
    assert pcss(s, 4.0, 4.0, 3.0, 1.0, 1.0, 0.1) == 1.0
    rng = random.Random(4)
    for _ in range(200):
        s = [[rng.uniform(1.0, 5.0) for _ in range(6)] for _ in range(6)]
        x, y, d_r = rng.uniform(0, 6), rng.uniform(0, 6), rng.uniform(1.0, 5.0)
        hard = 1.0 if d_r <= s[int(y)][int(x)] else 0.0
        assert pcss(s, x, y, d_r, 0.0, 1.0, 0.1) == hard


def test_result_in_range_and_wider_light_widens_the_penumbra():
    n, d_b, d_r, h = 1.0, 2.0, 4.0, 0.0125
    s = flatland_map(64, h, n, d_b, d_r)
    prev = None
    for wl in (0.2, 0.4, 0.8):
        lit = [pcss(s, 32 + k / 4, 1.5, d_r, wl, n, h) for k in range(-40, 41)]
        assert all(0.0 <= v <= 1.0 for v in lit)
        soft = sum(1 for v in lit if 0.0 < v < 1.0)
        if prev is not None:
            assert soft > prev
        prev = soft
