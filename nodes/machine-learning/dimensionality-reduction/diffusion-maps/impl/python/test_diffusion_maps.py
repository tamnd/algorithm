# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diffusion-maps/. The authors are listed in prov/T8KPAP.jsonl.

import math
import random
from fractions import Fraction

import pytest

from diffusion_maps import diffusion_map, diffusion_map_from_kernel, gaussian_kernel

# A 5-vertex graph with self-loops and rational weights.
KERNEL = [
    [2, 1, 0, 1, 0],
    [1, 3, 1, 0, 1],
    [0, 1, 2, 1, 0],
    [1, 0, 1, 2, 2],
    [0, 1, 0, 2, 1],
]


def exact_diffusion_distances(k, alpha, t):
    """D_t(x, y)^2 = sum_z (p_t(x, z) - p_t(y, z))^2 / pi(z), computed with fractions."""
    n = len(k)
    k = [[Fraction(v) for v in row] for row in k]
    q = [sum(row) for row in k]
    if alpha == 1:
        k = [[k[i][j] / (q[i] * q[j]) for j in range(n)] for i in range(n)]
    d = [sum(row) for row in k]
    pi = [x / sum(d) for x in d]
    p = [[k[i][j] / d[i] for j in range(n)] for i in range(n)]
    pt = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for _ in range(t):
        pt = [[sum(pt[i][l] * p[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
    return [[sum((pt[x][z] - pt[y][z]) ** 2 / pi[z] for z in range(n)) for y in range(n)] for x in range(n)]


@pytest.mark.parametrize("alpha", [0, 1])
@pytest.mark.parametrize("t", [1, 2, 3])
def test_diffusion_distance_equals_euclidean_distance_in_the_map(alpha, t):
    n = len(KERNEL)
    exact = exact_diffusion_distances(KERNEL, alpha, t)
    emb, _, _ = diffusion_map_from_kernel(KERNEL, n - 1, t, alpha)
    for x in range(n):
        for y in range(n):
            sq = sum((a - b) ** 2 for a, b in zip(emb[x], emb[y]))
            assert abs(sq - float(exact[x][y])) < 1e-10


def test_eigenvectors_of_the_random_walk():
    n = len(KERNEL)
    emb, lam, pi = diffusion_map_from_kernel(KERNEL, n - 1, 0, alpha=0)
    d = [sum(row) for row in KERNEL]
    p = [[KERNEL[i][j] / d[i] for j in range(n)] for i in range(n)]
    assert abs(sum(pi) - 1) < 1e-12
    for l in range(n - 1):
        psi = [row[l] for row in emb]  # t = 0 gives the eigenvectors themselves
        p_psi = [sum(p[i][j] * psi[j] for j in range(n)) for i in range(n)]
        assert max(abs(p_psi[i] - lam[l] * psi[i]) for i in range(n)) < 1e-12
        assert abs(sum(pi[i] * psi[i] ** 2 for i in range(n)) - 1) < 1e-12
        assert abs(sum(pi[i] * psi[i] for i in range(n))) < 1e-12
        assert abs(lam[l]) < 1
    assert all(abs(a) >= abs(b) for a, b in zip(lam, lam[1:]))


def test_alpha_one_removes_the_effect_of_the_density_on_a_circle():
    # Angles drawn with density proportional to 1 + 0.6 cos(theta). With alpha = 1 the
    # first two coordinates approximate cos and sin of the angle, so they lie close to a
    # circle. With alpha = 0 the dense side dominates and the circle is badly distorted.
    rng = random.Random(1)
    th = []
    while len(th) < 60:
        a = rng.uniform(0, 2 * math.pi)
        if rng.uniform(0, 1.6) < 1 + 0.6 * math.cos(a):
            th.append(a)
    pts = [(math.cos(a), math.sin(a)) for a in th]
    k = gaussian_kernel(pts, 0.1)
    ratios = {}
    for alpha in (0.0, 1.0):
        y, _, _ = diffusion_map_from_kernel(k, 2, 1, alpha)
        r = [math.hypot(a, b) for a, b in y]
        ratios[alpha] = min(r) / max(r)
    assert ratios[1.0] > 0.5
    assert ratios[0.0] < 0.2


def test_larger_t_shrinks_distances():
    rng = random.Random(2)
    pts = [(rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(12)]
    y1, lam, _ = diffusion_map(pts, 3, 0.2, t=1)
    y4, _, _ = diffusion_map(pts, 3, 0.2, t=4)
    assert all(0 <= v < 1 for v in lam)
    for i in range(12):
        for c in range(3):
            assert abs(y4[i][c] - lam[c] ** 3 * y1[i][c]) < 1e-12


def test_disconnected_kernel_is_rejected():
    k = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
    with pytest.raises(ValueError):
        diffusion_map_from_kernel(k, 1)
