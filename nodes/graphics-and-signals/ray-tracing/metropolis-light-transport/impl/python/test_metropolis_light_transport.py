# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/metropolis-light-transport/. The authors are listed in prov/6R7C43.jsonl.

"""Metropolis light transport against exact answers.

The chain mixes an independence proposal and a symmetric perturbation, so
the acceptance rule is checked exactly: on a finite state space with
Fraction values, the target is a fixed point of the kernel. The images are
the means of 16 independent chains, each unbiased because its first state
and its normalization come from the same bootstrap samples. A test passes
when each pixel is within 4 standard errors (over the chains) of the Neumann
series cut after K - 1 reflections, computed with Fraction.
"""

import math
import random
from fractions import Fraction as Fr

from metropolis_light_transport import (
    Scene,
    Sphere,
    acceptance,
    contribution,
    density_independent,
    perturb,
    render,
    sample_independent,
)

Z = 4.0


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
    """Outer sphere R = 2, inner sphere r = 3/5, camera at distance 1 from the center."""
    q = Fr(9, 100)
    outer = Sphere(2.0, True, (-1.0, 1.0), (float(e_out),), (float(a_out),))
    inner = Sphere(0.6, False, (-1.0, 1.0), (float(e_in),), (float(a_in),))
    return Scene([outer, inner], -1.0, [-1.0, 0.8, 1.0]), [[1 - q, q], [Fr(1), Fr(0)]]


def check(est, ref):
    for (mean, se), r in zip(est, ref):
        assert abs(mean - float(r)) <= Z * se + 1e-12, (mean, se, float(r))


def test_target_is_stationary_exactly() -> None:
    # A finite state space with the same two proposals: an independence
    # proposal T and a symmetric walk S on a cycle, mixed with p = 3/10.
    f = [Fr(1), Fr(3), Fr(2), Fr(5), Fr(0), Fr(1, 2)]
    t = [Fr(1, 10), Fr(2, 10), Fr(3, 10), Fr(1, 10), Fr(1, 10), Fr(2, 10)]
    n, p = len(f), Fr(3, 10)

    def s(x, y):
        return Fr(1, 2) if (x - y) % n in (1, n - 1) else Fr(0)

    total = sum(f)
    pi = [v / total for v in f]
    kernel = [[Fr(0)] * n for _ in range(n)]
    for x in range(n):
        if f[x] == 0:
            continue
        for y in range(n):
            if y != x:
                kernel[x][y] = p * t[y] * acceptance(f[x], f[y], t[y], t[x]) + (1 - p) * s(x, y) * acceptance(f[x], f[y], 1, 1)
        kernel[x][x] = 1 - sum(kernel[x])
    for y in range(n):
        assert sum(pi[x] * kernel[x][y] for x in range(n)) == pi[y]


def test_acceptance_never_moves_to_a_zero_path() -> None:
    assert acceptance(2.0, 0.0, 1.0, 1.0) == 0
    assert acceptance(2.0, 4.0, 1.0, 1.0) == 1
    assert acceptance(Fr(2), Fr(1), Fr(1, 3), Fr(1, 2)) == Fr(3, 4)


def test_perturbation_is_symmetric_and_stays_on_the_sphere() -> None:
    rng = random.Random(1)
    x = [(0, 0.95, 6.2), (1, -0.9, 0.1)]
    for _ in range(500):
        y = perturb(x, rng, 0.2)
        assert len(y) == 2 and sum(a != b for a, b in zip(x, y)) <= 1
        for i, z, phi in y:
            assert -1 <= z <= 1 and 0 <= phi < 2 * math.pi
    # Near the pole the step is reflected. The density of z' = 0.98 from z = 0.9
    # and of z' = 0.9 from z = 0.98 are both 2 / (2 step), so the moves into a
    # bin of width 0.02 around the other point have the probability 1/10 both ways.
    a = b = 0
    for _ in range(4000):
        if 0.97 < perturb([(0, 0.9, 0.0)], rng, 0.2)[0][1] <= 0.99:
            a += 1
        if 0.89 < perturb([(0, 0.98, 0.0)], rng, 0.2)[0][1] <= 0.91:
            b += 1
    for c in (a, b):
        assert abs(c - 400) < 4 * math.sqrt(4000 * 0.1 * 0.9)


def test_independent_density_matches_sampling() -> None:
    scene, _ = concentric(Fr(0), Fr(4, 5), Fr(1), Fr(1, 2))
    rng = random.Random(2)
    inner = 0
    for _ in range(4000):
        x, t = sample_independent(scene, rng, 3)
        assert t == density_independent(scene, x, 3)
        inner += sum(i == 1 for i, _, _ in x)
    assert inner > 0


def test_furnace() -> None:
    # Emission 1 and albedo 1/2: paths of at most 3 edges give 1 + 1/2 + 1/4.
    scene, _ = zoned([Fr(-1), Fr(1)], [Fr(1)], [Fr(1, 2)])
    check(render(scene, 16, 800, random.Random(3), 3, n_boot=800), [Fr(7, 4)])


def test_zoned_sphere_against_truncated_linear_system() -> None:
    cuts = [Fr(-1), Fr(-1, 2), Fr(0), Fr(1, 2), Fr(1)]
    emit, albedo = [Fr(0), Fr(0), Fr(0), Fr(4)], [Fr(1, 2), Fr(1, 4), Fr(3, 4), Fr(1, 2)]
    scene, form = zoned(cuts, emit, albedo)
    check(render(scene, 16, 1500, random.Random(4), 3, n_boot=1500), exact(albedo, form, emit, 2))


def test_concentric_spheres_with_occlusion() -> None:
    scene, form = concentric(Fr(0), Fr(4, 5), Fr(1), Fr(1, 2))
    check(render(scene, 16, 1500, random.Random(5), 2, n_boot=1500), exact([Fr(4, 5), Fr(1, 2)], form, [Fr(0), Fr(1)], 1))


def test_contribution_of_a_known_path() -> None:
    # In the zoned sphere with the camera at the center, every G toward the
    # center is 1 and the one-edge path from the light is E W_j G = E / Omega_j.
    scene, _ = zoned([Fr(-1), Fr(0), Fr(1)], [Fr(0), Fr(2)], [Fr(3, 4), Fr(1, 4)])
    j, f = contribution(scene, [(0, 0.5, 1.0)])
    assert j == 1 and abs(f - 2 / (2 * math.pi)) < 1e-12
    assert contribution(scene, [(0, -0.5, 1.0)])[1] == 0
