# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-input-output/. The authors are listed in prov/5WGXT1.jsonl.

import math
import random

from hybrid_input_output import hio, hio_step, magnitude_projection, object_projection
from imgkit import dft2

OBJ = [[1, 2, 0, 1], [0, 3, 1, 0], [2, 1, 4, 1], [0, 1, 0, 2]]


def dist(a, b):
    return math.sqrt(sum(abs(x - y) ** 2 for ra, rb in zip(a, b) for x, y in zip(ra, rb)))


def page_problem():
    f = [[float(OBJ[i][j]) if i < 4 and j < 4 else 0.0 for j in range(8)] for i in range(8)]
    twin = [[float(OBJ[3 - i][3 - j]) if i < 4 and j < 4 else 0.0 for j in range(8)] for i in range(8)]
    support = [[i < 4 and j < 4 for j in range(8)] for i in range(8)]
    amp = [[abs(v) for v in row] for row in dft2(f)]
    return f, twin, support, amp


def fourier_error(g, amp):
    gf = dft2(g)
    n = len(gf) * len(gf[0])
    return math.sqrt(sum((abs(v) - a) ** 2 for rv, ra in zip(gf, amp) for v, a in zip(rv, ra)) / n)


def test_twin_has_the_same_magnitudes() -> None:
    _, twin, _, amp = page_problem()
    assert fourier_error(twin, amp) < 1e-12


def test_beta_one_with_support_only_is_douglas_rachford() -> None:
    # Bauschke, Combettes and Luke 2002: x + P_S(2 P_M x - x) - P_M x.
    rng = random.Random(1)
    _, _, support, amp = page_problem()
    x = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(8)] for _ in range(8)]
    pm = magnitude_projection(x, amp)
    refl = [[2 * p - v for p, v in zip(rp, rv)] for rp, rv in zip(pm, x)]
    ps = object_projection(refl, support)
    dr = [[v + s - p for v, s, p in zip(rv, rs, rp)] for rv, rs, rp in zip(x, ps, pm)]
    step, _ = hio_step(x, amp, support, beta=1.0)
    assert dist(step, dr) < 1e-12


def test_off_support_feedback_rule() -> None:
    rng = random.Random(2)
    _, _, support, amp = page_problem()
    x = [[rng.uniform(-1, 1) for _ in range(8)] for _ in range(8)]
    for beta in (0.5, 0.9):
        step, gp = hio_step(x, amp, support, beta=beta, positive=True)
        for i in range(8):
            for j in range(8):
                p = gp[i][j]
                if support[i][j] and p >= 0:
                    assert abs(step[i][j] - p) < 1e-15
                else:
                    assert abs(step[i][j] - (x[i][j] - beta * p)) < 1e-15


def test_true_object_is_a_fixed_point() -> None:
    f, _, support, amp = page_problem()
    for positive in (False, True):
        est, g, errors = hio(amp, support, f, 5, 0.9, positive)
        assert dist(g, f) < 1e-9
        assert dist(est, f) < 1e-9
        assert max(errors) < 1e-9


def test_reconstruction_where_error_reduction_stagnates() -> None:
    # Measurement, not a theorem: on the example of the page, error reduction from
    # these starts stops at an error near 0.6, while 300 HIO steps (beta = 0.9) and
    # 20 error reduction steps find the object up to its twin.
    f, twin, support, amp = page_problem()
    for seed in (1, 2):
        rng = random.Random(seed)
        g0 = [[rng.uniform(0, 1) for _ in range(8)] for _ in range(8)]
        est, _, _ = hio(amp, support, g0, 300, 0.9, True)
        g = est
        for _ in range(20):
            g = object_projection(magnitude_projection(g, amp), support, True)
        assert fourier_error(g, amp) < 1e-3
        assert min(dist(g, f), dist(g, twin)) < 1e-2
