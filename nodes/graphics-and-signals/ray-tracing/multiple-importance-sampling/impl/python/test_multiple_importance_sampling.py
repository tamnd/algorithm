# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-importance-sampling/. The authors are listed in prov/T595A6.jsonl.

import math
import random
from fractions import Fraction as Fr

from multiple_importance_sampling import (Scene, Sphere, balance, exact_moments, mis_estimate, power, render,
                                          solid_angle_pdfs)

Z = 4.0

# A finite domain 0..5 with two techniques. Technique 0 cannot sample x = 0,
# technique 1 cannot sample x = 5.
F = [Fr(2), Fr(3), Fr(1), Fr(4), Fr(0), Fr(6)]
P = [[Fr(0), Fr(1, 10), Fr(1, 10), Fr(1, 5), Fr(1, 5), Fr(2, 5)],
     [Fr(1, 2), Fr(1, 5), Fr(1, 10), Fr(1, 10), Fr(1, 10), Fr(0)]]


def weights_from(heuristic, counts):
    return lambda i, x: heuristic(i, counts, [P[k][x] for k in range(len(P))])


def max_heuristic(i, counts, pdfs):
    best = max(range(len(pdfs)), key=lambda k: counts[k] * pdfs[k])
    return Fr(1) if i == best and pdfs[i] > 0 else Fr(0)


def split_evenly(i, counts, pdfs):
    alive = [k for k in range(len(pdfs)) if pdfs[k] > 0]
    return Fr(1, len(alive)) if i in alive else Fr(0)


def test_weights_sum_to_one() -> None:
    rng = random.Random(0)
    for _ in range(200):
        k = rng.randint(1, 4)
        counts = [rng.randint(1, 5) for _ in range(k)]
        pdfs = [Fr(rng.randint(0, 9), rng.randint(1, 9)) for _ in range(k)]
        if all(p == 0 for p in pdfs):
            continue
        for h in (balance, power, lambda i, c, p: power(i, c, p, 3), max_heuristic, split_evenly):
            assert sum(h(i, counts, pdfs) for i in range(k)) == 1
            assert all(h(i, counts, pdfs) == 0 for i in range(k) if pdfs[i] == 0)


def test_exact_unbiased_on_a_finite_domain() -> None:
    for counts in ((1, 1), (2, 3), (4, 1)):
        for h in (balance, power, max_heuristic, split_evenly):
            mean, _ = exact_moments(F, P, counts, weights_from(h, counts))
            assert mean == sum(F)
    # Weights that do not sum to 1 give a wrong mean.
    mean, _ = exact_moments(F, P, (1, 1), lambda i, x: Fr(1, 2))
    assert mean != sum(F)


def test_balance_heuristic_bound() -> None:
    # Veach: V[balance] <= V[any other weights] + (1 / min n_i - 1 / sum n_i) mu^2.
    for counts in ((1, 1), (2, 3), (4, 1), (3, 3)):
        _, v_bal = exact_moments(F, P, counts, weights_from(balance, counts))
        slack = (Fr(1, min(counts)) - Fr(1, sum(counts))) * sum(F) ** 2
        for h in (power, max_heuristic, split_evenly, lambda i, c, p: power(i, c, p, 4)):
            _, v = exact_moments(F, P, counts, weights_from(h, counts))
            assert v_bal <= v + slack


def test_one_sample_balance_is_the_mixture() -> None:
    # Pick technique i with probability c_i; the balance weight turns
    # w_i f / (c_i p_i) into f / sum_k c_k p_k, the mixture estimator.
    c = [Fr(1, 3), Fr(2, 3)]
    mean = var2 = Fr(0)
    for i in range(2):
        for x, fx in enumerate(F):
            if P[i][x] > 0:
                mix = c[0] * P[0][x] + c[1] * P[1][x]
                w = c[i] * P[i][x] / mix
                y = w * fx / (c[i] * P[i][x])
                assert y == fx / mix
                mean += c[i] * P[i][x] * y
    assert mean == sum(F)


def test_continuous_estimate_within_bound() -> None:
    # The integral of 3x^2 + 1 on [0, 1] is 2. Technique 0 is uniform,
    # technique 1 has the density 2x.
    f = lambda x: 3 * x * x + 1
    samplers = [lambda r: r.random(), lambda r: math.sqrt(r.random())]
    pdfs = [lambda x: 1.0, lambda x: 2 * x]
    for h, seed in ((balance, 1), (power, 2)):
        rng = random.Random(seed)
        vals = [mis_estimate(f, samplers, pdfs, (1, 2), rng, h) for _ in range(4000)]
        m = sum(vals) / len(vals)
        sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))
        assert abs(m - 2.0) <= Z * sd / math.sqrt(len(vals))


# ---- rendering ----

def solve(a, b):
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                g = m[r][c] / m[c][c]
                m[r] = [x - g * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def exact(albedo, form, emit, bounces=None):
    n = len(emit)
    t = [[albedo[i] * form[i][j] for j in range(n)] for i in range(n)]
    if bounces is None:
        return solve([[(1 if i == j else 0) - t[i][j] for j in range(n)] for i in range(n)], emit)
    term, total = emit[:], emit[:]
    for _ in range(bounces):
        term = [sum(t[i][j] * term[j] for j in range(n)) for i in range(n)]
        total = [x + y for x, y in zip(total, term)]
    return total


def zoned(cuts, emit, albedo):
    s = Sphere(1.0, True, tuple(map(float, cuts)), tuple(map(float, emit)), tuple(map(float, albedo)))
    area = [(cuts[j + 1] - cuts[j]) / 2 for j in range(len(emit))]
    return Scene([s], 0.0, list(map(float, cuts))), [area[:] for _ in emit]


def concentric(e_out, a_out, e_in, a_in):
    q = Fr(9, 100)
    outer = Sphere(2.0, True, (-1.0, 1.0), (float(e_out),), (float(a_out),))
    inner = Sphere(0.6, False, (-1.0, 1.0), (float(e_in),), (float(a_in),))
    return Scene([outer, inner], -1.0, [-1.0, 0.8, 1.0]), [[1 - q, q], [Fr(1), Fr(0)]]


def check(est, ref):
    for (mean, se), r in zip(est, ref):
        assert abs(mean - float(r)) <= Z * se + 1e-12, (mean, se, float(r))


def test_render_zoned_sphere() -> None:
    cuts, emit, albedo = [Fr(-1), Fr(0), Fr(9, 10), Fr(1)], [Fr(0), Fr(0), Fr(20)], [Fr(3, 4), Fr(1, 2), Fr(0)]
    scene, form = zoned(cuts, emit, albedo)
    ref = exact(albedo, form, emit)
    assert ref == [Fr(15, 8), Fr(5, 4), Fr(20)]
    for h, seed in ((balance, 3), (power, 4)):
        check(render(scene, 1500, random.Random(seed), h), ref)


def test_render_emitting_walls() -> None:
    # Large emitters: both techniques matter.
    cuts, emit, albedo = [Fr(-1), Fr(0), Fr(1)], [Fr(1), Fr(3)], [Fr(1, 2), Fr(1, 4)]
    scene, form = zoned(cuts, emit, albedo)
    check(render(scene, 1500, random.Random(5)), exact(albedo, form, emit))


def test_render_concentric_spheres() -> None:
    for e_out, a_out, e_in, a_in, seed in ((Fr(0), Fr(4, 5), Fr(1), Fr(1, 2), 6), (Fr(1), Fr(1, 2), Fr(0), Fr(3, 4), 7)):
        scene, form = concentric(e_out, a_out, e_in, a_in)
        check(render(scene, 1500, random.Random(seed)), exact([a_out, a_in], form, [e_out, e_in]))


def test_render_depth_limit() -> None:
    scene, form = concentric(Fr(0), Fr(4, 5), Fr(1), Fr(1, 2))
    for b in (1, 2):
        ref = exact([Fr(4, 5), Fr(1, 2)], form, [Fr(0), Fr(1)], b)
        check(render(scene, 1500, random.Random(30 + b), balance, max_depth=b), ref)


def test_path_weights_sum_to_one() -> None:
    scene, _ = concentric(Fr(1), Fr(1, 2), Fr(1), Fr(3, 4))
    rng = random.Random(8)
    x = scene.intersect(scene.camera, (0.0, 0.0, -1.0))
    for _ in range(200):
        y, ny, e, _ = scene.sample_light(rng)
        pl, pb = solid_angle_pdfs(scene, x.point, x.normal, y, ny, e)
        if pl > 0 or pb > 0:
            for h in (balance, power):
                assert abs(h(0, (1, 1), (pl, pb)) + h(1, (1, 1), (pl, pb)) - 1) < 1e-12
