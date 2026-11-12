# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fresnel-equations/. The authors are listed in prov/S05FMF.jsonl.

import math
import random

from fresnel_equations import cos_transmitted, fresnel, reflectance, schlick


def angle_form(n1, n2, th1):
    """Reference: the angle form of the Fresnel equations (Born and Wolf, Section 1.5.2).

    rs = -sin(t1 - t2) / sin(t1 + t2), rp = tan(t1 - t2) / tan(t1 + t2),
    ts = 2 sin t2 cos t1 / sin(t1 + t2), tp = 2 sin t2 cos t1 / (sin(t1 + t2) cos(t1 - t2)).
    It needs 0 < th1 < pi / 2 and no total internal reflection.
    """
    th2 = math.asin(n1 * math.sin(th1) / n2)
    rs = -math.sin(th1 - th2) / math.sin(th1 + th2)
    rp = math.tan(th1 - th2) / math.tan(th1 + th2)
    ts = 2 * math.sin(th2) * math.cos(th1) / math.sin(th1 + th2)
    tp = 2 * math.sin(th2) * math.cos(th1) / (math.sin(th1 + th2) * math.cos(th1 - th2))
    return rs, rp, ts, tp


def random_case(rng):
    n1 = rng.uniform(1.0, 3.0)
    n2 = rng.uniform(1.0, 3.0)
    return n1, n2, rng.uniform(0.0, 1.0)


def test_against_angle_form():
    rng = random.Random(1)
    done = 0
    while done < 1000:
        n1, n2, _ = random_case(rng)
        th1 = rng.uniform(0.01, math.pi / 2 - 0.01)
        if abs(n1 - n2) < 1e-3 or n1 * math.sin(th1) / n2 >= 0.999:
            continue
        f = fresnel(n1, n2, math.cos(th1))
        want = angle_form(n1, n2, th1)
        assert all(abs(x - y) < 1e-9 for x, y in zip((f.rs, f.rp, f.ts, f.tp), want))
        done += 1


def test_energy_conservation():
    # R + T = 1 for each polarization, and so for unpolarized light, below the critical angle.
    rng = random.Random(2)
    for _ in range(2000):
        n1, n2, c = random_case(rng)
        f = fresnel(n1, n2, c)
        assert abs(f.Rs + f.Ts - 1.0) < 1e-12
        assert abs(f.Rp + f.Tp - 1.0) < 1e-12
        assert 0.0 <= f.Rs <= 1.0 and 0.0 <= f.Rp <= 1.0


def test_total_internal_reflection():
    n1, n2 = 1.5, 1.0
    crit = math.asin(n2 / n1)
    rng = random.Random(3)
    for _ in range(1000):
        th = rng.uniform(0.0, math.pi / 2)
        if abs(th - crit) < 1e-9:
            continue
        r = reflectance(n1, n2, math.cos(th))
        if th > crit:
            assert r == 1.0 and fresnel(n1, n2, math.cos(th)).Ts == 0.0
        else:
            assert r < 1.0
    # Reflectance rises to 1 as the angle reaches the critical angle from below.
    assert reflectance(n1, n2, math.cos(crit - 1e-6)) > 0.99


def test_normal_incidence_and_grazing():
    for n1, n2 in ((1.0, 1.5), (1.5, 1.0), (1.0, 1.333), (1.0, 2.42)):
        r0 = ((n1 - n2) / (n1 + n2)) ** 2
        assert abs(reflectance(n1, n2, 1.0) - r0) < 1e-15
        assert abs(schlick(n1, n2, 1.0) - r0) < 1e-15
    assert abs(reflectance(1.0, 1.5, 1.0) - 0.04) < 1e-15
    assert abs(reflectance(1.0, 1.5, 0.0) - 1.0) < 1e-15
    assert abs(schlick(1.0, 1.5, 0.0) - 1.0) < 1e-15


def test_brewster_angle():
    for n1, n2 in ((1.0, 1.5), (1.5, 1.0), (1.0, 1.333)):
        tb = math.atan(n2 / n1)
        f = fresnel(n1, n2, math.cos(tb))
        assert f.Rp < 1e-28
        assert f.Rs > 0.0
    assert abs(math.degrees(math.atan(1.5)) - 56.3099324740) < 1e-9


def test_stokes_relations_and_symmetry():
    # Light from the other side at theta2 has r' = -r and t t' = 1 - r^2, and the same reflectance.
    rng = random.Random(4)
    for _ in range(1000):
        n1, n2, c1 = random_case(rng)
        c2 = cos_transmitted(n1, n2, c1)
        if c2 is None:
            continue
        f = fresnel(n1, n2, c1)
        g = fresnel(n2, n1, c2)
        assert abs(g.rs + f.rs) < 1e-12 and abs(g.rp + f.rp) < 1e-12
        assert abs(f.ts * g.ts - (1 - f.rs ** 2)) < 1e-12
        assert abs(f.tp * g.tp - (1 - f.rp ** 2)) < 1e-12
        assert abs(reflectance(n1, n2, c1) - reflectance(n2, n1, c2)) < 1e-12


def max_schlick_error(n1, n2, steps=90000):
    worst = 0.0
    for k in range(steps + 1):
        c = math.cos(math.radians(90.0 * k / steps))
        worst = max(worst, abs(schlick(n1, n2, c) - reflectance(n1, n2, c)))
    return worst


def test_schlick_error_against_exact():
    # The largest absolute error on a grid of 90001 angles, a step of 0.001 degree.
    e_glass = max_schlick_error(1.0, 1.5)
    assert 0.0356 < e_glass < 0.0358
    # From inside the glass, with the cosine taken in air, the error is the same.
    assert abs(max_schlick_error(1.5, 1.0) - e_glass) < 1e-4
    assert 0.0591 < max_schlick_error(1.0, 1.333) < 0.0593
    assert 0.0739 < max_schlick_error(1.0, 2.4) < 0.0742
    # With the incident cosine in place of cos(theta2) inside glass, the error is far larger.
    worst = 0.0
    r0 = 0.04
    for k in range(9001):
        c = math.cos(math.radians(90.0 * k / 9000))
        worst = max(worst, abs(r0 + (1 - r0) * (1 - c) ** 5 - reflectance(1.5, 1.0, c)))
    assert worst > 0.9
