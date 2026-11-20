# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/range-doppler-algorithm/. The authors are listed in prov/76HEMZ.jsonl.

import math

from range_doppler_algorithm import Stripmap, rda, simulate_raw, target_pixel

G = Stripmap()
TARGETS = [(0.0, 400.0, 1.0), (10.0, 410.0, 0.7)]
RAW = simulate_raw(G, TARGETS)
IMG = rda(G, RAW)
IMG_NO_RCMC = rda(G, RAW, rcmc=False)


def matched_filter(x, r0):
    """Brute force: correlate the raw data with the exact echo of a unit target at (x, r0)."""
    ref = simulate_raw(G, [(x, r0, 1.0)])
    return sum(a.conjugate() * b for ra, rb in zip(ref, RAW) for a, b in zip(ra, rb))


def ideal_gain(x, r0):
    """The matched filter output of a unit target on itself: chirp samples times pulses."""
    ref = simulate_raw(G, [(x, r0, 1.0)])
    return sum(abs(a) ** 2 for row in ref for a in row)


def local_peak(img, p0, j0, w=3):
    return max((abs(img[p][j]), p, j) for p in range(p0 - w, p0 + w + 1) for j in range(j0 - w, j0 + w + 1))


def test_targets_focus_at_their_pixels() -> None:
    for x, r0, _ in TARGETS:
        p0, j0 = (round(v) for v in target_pixel(G, x, r0))
        _, p, j = local_peak(IMG, p0, j0)
        assert (p, j) == (p0, j0)


def test_peak_is_close_to_the_brute_force_matched_filter() -> None:
    for x, r0, amp in TARGETS:
        p0, j0 = (round(v) for v in target_pixel(G, x, r0))
        brute = abs(matched_filter(x, r0))
        assert abs(brute - amp * ideal_gain(x, r0)) < 0.02 * brute
        got = abs(IMG[p0][j0])
        assert 0.85 * brute < got < 1.05 * brute


def test_rcmc_is_needed() -> None:
    p0, j0 = (round(v) for v in target_pixel(G, 0.0, 400.0))
    with_rcmc = abs(IMG[p0][j0])
    without = abs(IMG_NO_RCMC[p0][j0])
    assert without < 0.7 * with_rcmc

    def concentration(img):
        total = sum(abs(v) ** 2 for row in img for v in row)
        return abs(img[p0][j0]) ** 2 / total

    assert concentration(IMG_NO_RCMC) < 0.5 * concentration(IMG)


def test_linear_in_the_data() -> None:
    a = simulate_raw(G, [(0.0, 400.0, 1.0)])
    b = simulate_raw(G, [(10.0, 410.0, 0.7)])
    ia, ib = rda(G, a), rda(G, b)
    for p in (60, 64, 72):
        for j in (14, 16, 20):
            assert abs(ia[p][j] + ib[p][j] - IMG[p][j]) < 1e-6 * abs(IMG[64][16])


def test_amplitude_ratio_is_kept() -> None:
    a = abs(IMG[64][16]) / ideal_gain(0.0, 400.0)
    p1, j1 = (round(v) for v in target_pixel(G, 10.0, 410.0))
    b = abs(IMG[p1][j1]) / ideal_gain(10.0, 410.0)
    assert abs(b / a - 0.7) < 0.05


def test_resolution_matches_c_over_2b() -> None:
    """The range impulse response falls to its first null near c / (2 B) = 1.5 m, 1.2 bins."""
    row = [abs(v) for v in IMG[64]]
    peak = row[16]
    assert row[15] < 0.75 * peak and row[17] < 0.75 * peak
    assert max(row[:13] + row[20:]) < 0.35 * peak
    assert abs(G.dr * 1.2 - 3.0e8 / (2 * G.bandwidth)) < 1e-9
    assert math.isclose(G.dr, 1.25)
