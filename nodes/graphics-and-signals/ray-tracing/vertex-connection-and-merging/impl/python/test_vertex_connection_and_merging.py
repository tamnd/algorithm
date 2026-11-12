# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertex-connection-and-merging/. The authors are listed in prov/PT5JRY.jsonl.

import math
import random
from fractions import Fraction

from vertex_connection_and_merging import (
    INV_2PI,
    INV_4PI,
    Furnace,
    HashGrid,
    LightVertex,
    MisState,
    balance_weights,
    recursive_weights,
    uniform_sphere,
    vcm_iteration,
)


def _pdfs(p_a, cm, cp, d2, pwf, pwr):
    k = len(cm)
    p_fwd = [p_a] + [pwf[i - 1] * cm[i] / d2[i - 1] for i in range(1, k)]
    p_rev = [pwr[i + 1] * cp[i] / d2[i] for i in range(k - 1)]
    return p_fwd, p_rev


def test_recursive_weights_equal_brute_force_balance_weights_exactly():
    rng = random.Random(0)

    def rf():
        return Fraction(rng.randint(1, 9), rng.randint(1, 9))

    for k in range(1, 8):
        for trial in range(30):
            cm, cp, d2, pwf, pwr = ([rf() for _ in range(k)] for _ in range(5))
            p_a = rf()
            eta = rf() if trial % 2 else Fraction(0)
            brute = balance_weights(*_pdfs(p_a, cm, cp, d2, pwf, pwr), eta)
            brute = {t: w for t, w in brute.items() if w != 0}
            rec = recursive_weights(p_a, cm, cp, d2, pwf, pwr, eta)
            assert rec == brute
            assert sum(rec.values()) == 1


def test_weights_of_sphere_paths_sum_to_one():
    # The pdfs of the renderer: a cosine emission and uniform hemisphere scattering.
    rng = random.Random(1)
    for k in range(1, 7):
        for _ in range(50):
            xs = [uniform_sphere(rng) for _ in range(k)]
            d2 = [math.dist(xs[i], xs[i + 1]) ** 2 for i in range(k - 1)] + [1.0]
            # Inside the unit sphere the cosine at both ends of a chord of length d is d / 2.
            # The camera is at the center, so the last edge has length 1 and meets the sphere at a right angle.
            cp = [math.sqrt(d2[i]) / 2 for i in range(k - 1)] + [1.0]
            cm = [1.0] + [math.sqrt(d2[i - 1]) / 2 for i in range(1, k)]
            pwf = [cp[0] / math.pi] + [INV_2PI] * (k - 1)
            pwr = [INV_2PI] * k
            eta = 64 * math.pi * 0.2**2
            rec = recursive_weights(INV_4PI, cm, cp, d2, pwf, pwr, eta)
            brute = balance_weights(*_pdfs(INV_4PI, cm, cp, d2, pwf, pwr), eta)
            assert math.isclose(sum(rec.values()), 1.0, rel_tol=1e-12)
            for t, w in brute.items():
                assert math.isclose(rec[t], w, rel_tol=1e-9, abs_tol=1e-15)


def test_hand_example():
    # The path of the example: in units of 1/(4 pi), p->0 = p->1 = 1, p->2 = 2, p<-0 = 1, p<-1 = 2.
    w = balance_weights([1, 1, 2], [1, 2], Fraction(5, 2))
    assert w == {
        ("vc", 0): Fraction(2, 15),
        ("vc", 1): Fraction(2, 15),
        ("vc", 2): Fraction(1, 15),
        ("vm", 1): Fraction(1, 3),
        ("vm", 2): Fraction(1, 3),
    }


def test_hash_grid_query_matches_brute_force():
    rng = random.Random(2)
    zero = MisState(0.0, 0.0, 0.0)
    verts = [LightVertex(uniform_sphere(rng), (0.0, 0.0, 1.0), 1.0, 1, zero) for _ in range(2000)]
    for r in (0.05, 0.2, 0.7):
        grid = HashGrid(r, verts)
        for _ in range(100):
            p = uniform_sphere(rng)
            fast = sorted(id(v) for v in grid.query(p))
            slow = sorted(id(v) for v in verts if math.dist(v.x, p) < r)
            assert fast == slow


def test_merge_disc_on_the_unit_sphere_has_area_pi_r_squared():
    # The points of the unit sphere within the distance r of a point form a cap of area pi r^2
    # (Archimedes), so a fraction r^2 / 4 of uniform points falls in it.
    rng = random.Random(3)
    n = 40000
    for r in (0.3, 1.0):
        p = uniform_sphere(rng)
        hits = sum(math.dist(uniform_sphere(rng), p) < r for _ in range(n))
        q = r * r / 4
        assert abs(hits / n - q) < 4 * math.sqrt(q * (1 - q) / n)


def test_black_furnace_sees_only_the_emission():
    est = vcm_iteration(Furnace(0.0), 16, 0.3, 4, random.Random(4))
    assert est == [1.0] * 16


def _mean_and_se(scene, n, r, k_max, merge, iterations, seed):
    vals = []
    for it in range(iterations):
        e = vcm_iteration(scene, n, r, k_max, random.Random(seed + it), merge)
        vals.append(sum(e) / len(e))
    m = sum(vals) / len(vals)
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))
    return m, sd / math.sqrt(len(vals))


def test_bidirectional_weights_match_the_exact_radiance():
    scene = Furnace(0.5)
    m, se = _mean_and_se(scene, 48, 0.1, 4, False, 80, 100)
    assert abs(m - scene.exact(4)) < 4 * se


def test_vcm_matches_the_exact_radiance():
    scene = Furnace(0.6)
    for r, seed in ((0.15, 300), (0.5, 400)):
        m, se = _mean_and_se(scene, 48, r, 4, True, 80, seed)
        assert abs(m - scene.exact(4)) < 4 * se
        assert se < 0.01 * scene.exact(4)
