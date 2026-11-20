# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delay-multiply-and-sum/. The authors are listed in prov/SF6EBZ.jsonl.

import random

from delay_multiply_and_sum import (beamform, das, dmas, dmas_pairs, element_positions, signed_sqrt,
                                    simulate_rf)

F0, SIGMA, FS, T0, NS = 5.0, 0.1, 40.0, 7.0, 120
ELEMENTS = element_positions(16, 0.3)
XS = [round(-1.5 + 0.1 * k, 10) for k in range(31)]
ZS = [round(6.0 + 0.01 * k, 10) for k in range(-10, 11)]


def test_page_example() -> None:
    s = [4.0, 1.0, -1.0, 9.0]
    assert dmas_pairs(s) == 5.0
    assert dmas(s) == 5.0
    assert das(s) == 13.0


def test_fast_form_equals_the_pair_sum() -> None:
    rng = random.Random(3105)
    for _ in range(300):
        m = rng.randint(1, 24)
        s = [rng.uniform(-5, 5) for _ in range(m)]
        if rng.random() < 0.2:
            s[rng.randrange(m)] = 0.0
        assert abs(dmas(s) - dmas_pairs(s)) <= 1e-9 * (1 + sum(abs(v) for v in s) * m)


def test_identical_channels_give_the_rectified_value() -> None:
    for v in (2.25, -2.25, 0.0):
        for m in (1, 2, 5, 16):
            assert abs(dmas([v] * m) - m * (m - 1) / 2 * abs(v)) < 1e-12


def test_homogeneous_of_degree_one_in_the_magnitude() -> None:
    rng = random.Random(3106)
    s = [rng.uniform(-3, 3) for _ in range(10)]
    for a in (4.0, 0.25, -1.0, -9.0):
        assert abs(dmas([a * v for v in s]) - abs(a) * dmas(s)) < 1e-9


def test_signed_sqrt() -> None:
    assert signed_sqrt(9.0) == 3.0 and signed_sqrt(-9.0) == -3.0 and signed_sqrt(0.0) == 0.0


def _profile(combiner):
    data = simulate_rf(ELEMENTS, [(0.0, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
    img = beamform(data, ELEMENTS, XS, ZS, T0, FS, combiner)
    prof = [max(abs(img[i][j]) for i in range(len(ZS))) for j in range(len(XS))]
    peak = max(prof)
    return [v / peak for v in prof], peak


def test_point_target_peak_and_lower_sidelobes_than_das() -> None:
    p_das, peak_das = _profile(das)
    p_dmas, peak_dmas = _profile(dmas)
    assert p_das.index(1.0) == XS.index(0.0) and p_dmas.index(1.0) == XS.index(0.0)
    # at the peak all 16 aligned samples are close to equal, so DMAS is close to 120 times one of them
    assert abs(peak_dmas - 120 * peak_das / 16) < 0.02 * peak_dmas
    side_das = max(v for x, v in zip(XS, p_das) if abs(x) >= 0.6)
    side_dmas = max(v for x, v in zip(XS, p_dmas) if abs(x) >= 0.6)
    assert side_dmas < 0.5 * side_das
    i3 = XS.index(0.3)
    assert p_dmas[i3] < p_das[i3]
