# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nudged-elastic-band/. The authors are listed in prov/NNCV7X.jsonl.
import math

import pytest

from nudged_elastic_band import improved_tangent, muller_brown, neb_forces, nudged_elastic_band

A = [-0.55822, 1.44173]
B = [0.62350, 0.02804]
C = [-0.05001, 0.46669]
S1 = (-0.82200, 0.62431, -40.6648)
S2 = (0.21249, 0.29299, -72.2489)


def double_well(p):
    x, y = p
    return (x * x - 1.0) ** 2 + 2.0 * y * y, [4.0 * x * (x * x - 1.0), 4.0 * y]


def test_tangent_rules():
    r0, r1, r2 = [0.0, 0.0], [1.0, 0.0], [1.0, 2.0]
    # Energy rises along the path: the tangent points to the next image.
    assert improved_tangent(r0, r1, r2, 0.0, 1.0, 2.0) == pytest.approx([0.0, 1.0])
    # Energy falls: the tangent points from the previous image.
    assert improved_tangent(r0, r1, r2, 2.0, 1.0, 0.0) == pytest.approx([1.0, 0.0])
    # A maximum with e_next > e_prev: weights d_max = 1 on t_plus, d_min = 0.5 on t_minus.
    t = improved_tangent(r0, r1, r2, 0.5, 1.0, 0.0)
    w = [0.5 * 0.0 + 1.0 * 1.0, 0.5 * 2.0 + 1.0 * 0.0]
    assert t == pytest.approx([c / math.hypot(*w) for c in w])


def test_force_by_hand():
    # The page example: images (-1, 0), (0, 0.5), (1, 0) on the double well.
    ims = [[-1.0, 0.0], [0.0, 0.5], [1.0, 0.0]]
    en = [double_well(p)[0] for p in ims]
    gr = [double_well(p)[1] for p in ims]
    assert en == pytest.approx([0.0, 1.5, 0.0])
    f, i_c = neb_forces(ims, en, gr, 5.0, False)
    assert i_c == -1
    assert f[1] == pytest.approx([0.0, -2.0])
    f, i_c = neb_forces(ims, en, gr, 5.0, True)
    assert i_c == 1
    assert f[1] == pytest.approx([0.0, -2.0])


def test_double_well_band_goes_to_the_axis():
    n = 8
    init = [[-1.0 + 2.0 * i / n, 0.5 * math.sin(math.pi * i / n)] for i in range(n + 1)]
    ims, en, i_c, it, ok = nudged_elastic_band(double_well, init[0], init[-1], n, k=5.0, h=0.05,
                                               tol=1e-8, climb=True, images=init)
    assert ok and it < 1000
    assert i_c == 4
    assert ims[i_c] == pytest.approx([0.0, 0.0], abs=1e-8)
    for i, p in enumerate(ims):
        assert p == pytest.approx([-1.0 + 2.0 * i / n, 0.0], abs=1e-6)


def mb_band(start, end, climb):
    return nudged_elastic_band(muller_brown, start, end, 8, k=50.0, h=2e-4, tol=1e-3,
                               climb=climb, climb_tol=5.0, max_iter=10000)


@pytest.mark.parametrize("start,end,saddle", [(A, C, S1), (C, B, S2)])
def test_climbing_image_finds_the_muller_brown_saddle(start, end, saddle):
    ims, en, i_c, it, ok = mb_band(start, end, True)
    assert ok
    assert ims[i_c] == pytest.approx(list(saddle[:2]), abs=1e-4)
    assert en[i_c] == pytest.approx(saddle[2], abs=1e-3)
    # The force on the climbing image has the norm of the gradient, so the image is a stationary point.
    assert math.hypot(*muller_brown(ims[i_c])[1]) < 1e-3


def test_plain_band_is_below_the_saddle_and_evenly_spaced():
    ims, en, i_c, it, ok = mb_band(A, C, False)
    assert ok and i_c == -1
    top = max(en)
    assert -44.5 < top < S1[2] - 1.0
    gaps = [math.dist(ims[i], ims[i + 1]) for i in range(8)]
    assert max(gaps) - min(gaps) < 1e-3


def test_straight_line_is_far_above_the_path():
    top = max(muller_brown([A[0] + s / 200 * (C[0] - A[0]), A[1] + s / 200 * (C[1] - A[1])])[0]
              for s in range(201))
    assert top > 0.0 > S1[2]
