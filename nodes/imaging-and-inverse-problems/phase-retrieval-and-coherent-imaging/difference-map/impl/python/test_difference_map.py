# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/difference-map/. The authors are listed in prov/CRHCPN.jsonl.

import math
import random

from difference_map import difference_map, dm_step, magnitude_projection, object_projection
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


def random_complex(rng):
    return [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(8)] for _ in range(8)]


def hio_reference(x, amp, support, beta):
    """Fienup's HIO step for a support constraint only, written out directly."""
    p = magnitude_projection(x, amp)
    return [[p[i][j] if support[i][j] else x[i][j] - beta * p[i][j] for j in range(8)] for i in range(8)]


def test_hio_is_the_case_gamma_s_minus_one_gamma_m_one_over_beta() -> None:
    rng = random.Random(1)
    _, _, support, amp = page_problem()
    for beta in (0.5, 0.9, 1.0):
        x = random_complex(rng)
        step, _ = dm_step(x, amp, support, beta, -1.0, 1.0 / beta)
        assert dist(step, hio_reference(x, amp, support, beta)) < 1e-12


def test_beta_one_with_elser_choice_is_douglas_rachford() -> None:
    rng = random.Random(2)
    _, _, support, amp = page_problem()
    x = random_complex(rng)
    pm = magnitude_projection(x, amp)
    ps = object_projection([[2 * p - v for p, v in zip(rp, rv)] for rp, rv in zip(pm, x)], support)
    dr = [[v + s - p for v, s, p in zip(rv, rs, rp)] for rv, rs, rp in zip(x, ps, pm)]
    step, _ = dm_step(x, amp, support, 1.0, -1.0, 1.0)
    assert dist(step, dr) < 1e-12


def test_solution_is_a_fixed_point_and_is_read_out() -> None:
    f, _, support, amp = page_problem()
    for beta, positive in ((0.9, True), (0.7, False), (-0.8, True)):
        step, est = dm_step(f, amp, support, beta, -1.0 / beta, 1.0 / beta, positive)
        assert dist(step, f) < 1e-9
        assert dist(est, f) < 1e-9


def test_reconstruction_on_the_page_example() -> None:
    # Measurement, not a theorem: beta = 0.9 with Elser's gamma values, 250 steps,
    # three seeds. The two read-outs agree and give the object or its twin.
    f, twin, support, amp = page_problem()
    for seed in (1, 2, 3):
        rng = random.Random(seed)
        x0 = [[rng.uniform(0, 1) for _ in range(8)] for _ in range(8)]
        est, x, gaps = difference_map(amp, support, x0, 250, beta=0.9, positive=True)
        assert gaps[-1] < 1e-6
        f_m = [[(1 + 1 / 0.9) * p - v / 0.9 for p, v in zip(rp, rv)]
               for rp, rv in zip(magnitude_projection(x, amp), x)]
        other = object_projection(f_m, support, True)
        assert dist(est, other) < 1e-5
        assert min(dist(est, f), dist(est, twin)) < 1e-5
