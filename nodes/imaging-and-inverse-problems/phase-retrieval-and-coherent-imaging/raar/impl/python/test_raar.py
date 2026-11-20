# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/raar/. The authors are listed in prov/MJJXEG.jsonl.

import random

from imgkit import dft2, idft2
from raar import distance, magnitude_projection, raar, raar_generic, raar_step, support_projection

OBJ = [[1, 2, 0, 1], [0, 3, 1, 0], [2, 1, 4, 1], [0, 1, 0, 2]]
SUPPORT = [[i < 4 and j < 4 for j in range(8)] for i in range(8)]


def page_problem():
    f = [[float(OBJ[i][j]) if i < 4 and j < 4 else 0.0 for j in range(8)] for i in range(8)]
    twin = [[float(OBJ[3 - i][3 - j]) if i < 4 and j < 4 else 0.0 for j in range(8)] for i in range(8)]
    amp = [[abs(v) for v in row] for row in dft2(f)]
    return f, twin, amp


def random_complex(rng):
    return [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(8)] for _ in range(8)]


def convex_problem(seed):
    """A = images on the support, B = images with known DFT values on a random half of the
    frequencies. Both are convex, and the true image f is in both."""
    rng = random.Random(seed)
    f = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) if SUPPORT[i][j] else 0j for j in range(8)]
         for i in range(8)]
    known = [[rng.random() < 0.5 for _ in range(8)] for _ in range(8)]
    ff = dft2(f)

    def proj_b(x):
        xf = dft2(x)
        for i in range(8):
            for j in range(8):
                if known[i][j]:
                    xf[i][j] = ff[i][j]
        return idft2(xf)

    return f, support_projection(SUPPORT), proj_b, rng


def real_inner(a, b):
    return sum((u.conjugate() * v).real for ra, rb in zip(a, b) for u, v in zip(ra, rb))


def test_beta_one_is_douglas_rachford() -> None:
    rng = random.Random(1)
    _, _, amp = page_problem()
    x = random_complex(rng)
    ps = support_projection(SUPPORT)
    pm = magnitude_projection(x, amp)
    dr = [[v + s - p for v, s, p in zip(rv, rs, rp)]
          for rv, rs, rp in zip(x, ps([[2 * p - v for p, v in zip(rp, rv)] for rp, rv in zip(pm, x)]), pm)]
    step = raar_step(x, ps, lambda g: magnitude_projection(g, amp), 1.0)
    assert distance(step, dr) < 1e-12


def test_pointwise_form_for_a_support() -> None:
    # Support only: V x = P_M x on the support and beta x + (1 - 2 beta) P_M x off it.
    rng = random.Random(2)
    _, _, amp = page_problem()
    x = random_complex(rng)
    pm = magnitude_projection(x, amp)
    for beta in (0.3, 0.75, 0.9):
        step = raar_step(x, support_projection(SUPPORT), lambda g: magnitude_projection(g, amp), beta)
        for i in range(8):
            for j in range(8):
                want = pm[i][j] if SUPPORT[i][j] else beta * x[i][j] + (1 - 2 * beta) * pm[i][j]
                assert abs(step[i][j] - want) < 1e-12


def test_firmly_nonexpansive_for_convex_sets() -> None:
    _, proj_a, proj_b, rng = convex_problem(3)
    for beta in (0.5, 0.9, 1.0):
        for _ in range(5):
            x, y = random_complex(rng), random_complex(rng)
            vx, vy = raar_step(x, proj_a, proj_b, beta), raar_step(y, proj_a, proj_b, beta)
            d = [[u - v for u, v in zip(ru, rv)] for ru, rv in zip(vx, vy)]
            e = [[u - v for u, v in zip(ru, rv)] for ru, rv in zip(x, y)]
            assert real_inner(d, d) <= real_inner(d, e) + 1e-9


def test_convex_case_is_fejer_monotone_and_converges() -> None:
    # The distance to the point f of the intersection never grows (Fejer monotone). Here the
    # intersection is the single point f (16 unknowns, about 32 equations), so the limit is f.
    f, proj_a, proj_b, rng = convex_problem(4)
    x0 = random_complex(rng)
    path = raar_generic(proj_a, proj_b, x0, 200, 0.8)
    dists = [distance(x, f) for x in path]
    for d0, d1 in zip(dists, dists[1:]):
        assert d1 <= d0 + 1e-10
    assert distance(proj_b(path[-1]), f) < 1e-9


def test_true_object_is_a_fixed_point() -> None:
    f, _, amp = page_problem()
    for beta in (0.5, 0.95):
        est, x = raar(amp, SUPPORT, f, 3, beta, positive=True)
        assert distance(x, f) < 1e-9
        assert distance(est, f) < 1e-9


def test_reconstruction_on_the_page_example() -> None:
    # Measurement, not a theorem: beta = 0.95, 250 steps, nonnegativity, three seeds.
    f, twin, amp = page_problem()
    for seed in (1, 2, 3):
        rng = random.Random(seed)
        x0 = [[rng.uniform(0, 1) for _ in range(8)] for _ in range(8)]
        est, _ = raar(amp, SUPPORT, x0, 250, 0.95, positive=True)
        assert min(distance(est, f), distance(est, twin)) < 1e-6
