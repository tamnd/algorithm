# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chirp-scaling-algorithm/. The authors are listed in prov/C270V5.jsonl.

from chirp_scaling_algorithm import Stripmap, csa, migration_factor, modified_fm_rate, simulate_raw, target_pixel

G = Stripmap()
TARGETS = [(0.0, 400.0, 1.0), (10.0, 410.0, 0.7), (-12.5, 395.0, 0.5)]  # on the 1.25 m pixel grid
RAW = simulate_raw(G, TARGETS)
IMG = csa(G, RAW)


def matched_filter(g, raw, x, r0):
    """Brute force: correlate the raw data with the exact echo of a unit target at (x, r0)."""
    ref = simulate_raw(g, [(x, r0, 1.0)])
    return sum(a.conjugate() * b for ra, rb in zip(ref, raw) for a, b in zip(ra, rb))


def ideal_gain(g, x, r0):
    ref = simulate_raw(g, [(x, r0, 1.0)])
    return sum(abs(a) ** 2 for row in ref for a in row)


def local_peak(img, p0, j0, w=3):
    return max((abs(img[p][j]), p, j) for p in range(p0 - w, p0 + w + 1) for j in range(j0 - w, j0 + w + 1))


def test_targets_focus_at_their_pixels() -> None:
    for x, r0, _ in TARGETS:
        p0, j0 = (round(v) for v in target_pixel(G, x, r0))
        _, p, j = local_peak(IMG, p0, j0)
        assert (p, j) == (p0, j0)


def test_peak_matches_the_brute_force_matched_filter() -> None:
    for x, r0, amp in TARGETS:
        p0, j0 = (round(v) for v in target_pixel(G, x, r0))
        brute = abs(matched_filter(G, RAW, x, r0))
        assert abs(brute - amp * ideal_gain(G, x, r0)) < 0.03 * brute
        assert abs(abs(IMG[p0][j0]) - brute) < 0.06 * brute


def test_scaling_corrects_range_varying_migration() -> None:
    """Wide beam and short range: the target is 24 m from r_ref, so its migration differs."""
    g = Stripmap(beam=0.35, prf=200.0, n_az=256, r_start=80.0)
    raw = simulate_raw(g, [(0.0, 96.0, 1.0)])
    ideal = ideal_gain(g, 0.0, 96.0)
    p0, j0 = (round(v) for v in target_pixel(g, 0.0, 96.0))
    with_scaling = local_peak(csa(g, raw, r_ref=120.0), p0, j0)
    without = local_peak(csa(g, raw, r_ref=120.0, scaling=False), p0, j0)
    assert with_scaling[1:] == (p0, j0)
    assert with_scaling[0] > 0.95 * ideal
    assert without[0] < 0.8 * ideal
    assert without[1:] != (p0, j0)


def test_linear_in_the_data() -> None:
    parts = [csa(G, simulate_raw(G, [t])) for t in TARGETS]
    for p in (58, 64, 72):
        for j in (12, 16, 20):
            total = sum(im[p][j] for im in parts)
            assert abs(total - IMG[p][j]) < 1e-6 * abs(IMG[64][16])


def test_modified_fm_rate_tends_to_kr_at_zero_doppler() -> None:
    assert migration_factor(G, 0.0) == 1.0
    assert modified_fm_rate(G, 0.0, 400.0) == G.kr
    f = 20.0
    d = migration_factor(G, f)
    assert abs(d - (1 - (3.0e8 * f / (2 * G.v * G.f0)) ** 2) ** 0.5) < 1e-15
    assert modified_fm_rate(G, f, 400.0) > G.kr
