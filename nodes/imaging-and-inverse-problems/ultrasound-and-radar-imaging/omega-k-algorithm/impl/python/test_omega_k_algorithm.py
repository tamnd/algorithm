# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/omega-k-algorithm/. The authors are listed in prov/R4DMS8.jsonl.

from omega_k_algorithm import Stripmap, omega_k, simulate_raw, target_pixel

G = Stripmap()
TARGETS = [(0.0, 400.0, 1.0), (10.0, 410.0, 0.6j), (-12.5, 425.0, -0.5)]
RAW = simulate_raw(G, TARGETS)
IMG = omega_k(G, RAW)
WIDE = Stripmap(beam=0.35, prf=200.0, n_az=256, r_start=80.0)


def matched_filter(g, raw, x, r0):
    """Brute force: correlate the raw data with the exact echo of a unit target at (x, r0)."""
    ref = simulate_raw(g, [(x, r0, 1.0)])
    return sum(a.conjugate() * b for ra, rb in zip(ref, raw) for a, b in zip(ra, rb))


def ideal_gain(g, x, r0):
    ref = simulate_raw(g, [(x, r0, 1.0)])
    return sum(abs(a) ** 2 for row in ref for a in row)


def local_peak(img, p0, j0, w=3):
    return max((abs(img[p][j]), p, j) for p in range(p0 - w, p0 + w + 1) for j in range(j0 - w, j0 + w + 1))


def pixel(g, x, r0):
    return tuple(round(v) for v in target_pixel(g, x, r0))


def test_targets_focus_at_their_pixels() -> None:
    for x, r0, _ in TARGETS:
        p0, j0 = pixel(G, x, r0)
        assert local_peak(IMG, p0, j0)[1:] == (p0, j0)


def test_peak_is_close_to_the_brute_force_matched_filter() -> None:
    for x, r0, amp in TARGETS:
        p0, j0 = pixel(G, x, r0)
        brute = abs(matched_filter(G, RAW, x, r0))
        assert abs(brute - abs(amp) * ideal_gain(G, x, r0)) < 0.03 * brute
        assert 0.85 * brute < abs(IMG[p0][j0]) < 1.05 * brute


def test_complex_amplitudes_are_kept() -> None:
    """The image keeps the ratio of the complex reflectivities, phase included."""
    ref_val = IMG[64][16] / ideal_gain(G, 0.0, 400.0)
    for x, r0, amp in TARGETS[1:]:
        p0, j0 = pixel(G, x, r0)
        ratio = (IMG[p0][j0] / ideal_gain(G, x, r0)) / ref_val
        assert abs(ratio - amp) < 0.06


def test_stolt_mapping_focuses_far_from_the_reference_range() -> None:
    """Wide beam: bulk compression alone defocuses a target 24 m from r_ref; Stolt fixes it."""
    raw = simulate_raw(WIDE, [(0.0, 96.0, 1.0)])
    ideal = ideal_gain(WIDE, 0.0, 96.0)
    p0, j0 = pixel(WIDE, 0.0, 96.0)
    full = omega_k(WIDE, raw, r_ref=120.0)
    bulk = omega_k(WIDE, raw, r_ref=120.0, stolt=False)
    assert local_peak(full, p0, j0)[1:] == (p0, j0)
    assert abs(full[p0][j0]) > 0.9 * ideal
    assert local_peak(bulk, p0, j0)[0] < 0.4 * ideal


def test_bulk_compression_alone_is_exact_at_the_reference_range() -> None:
    raw = simulate_raw(WIDE, [(0.0, 120.0, 1.0)])
    p0, j0 = pixel(WIDE, 0.0, 120.0)
    full = omega_k(WIDE, raw, r_ref=120.0)
    bulk = omega_k(WIDE, raw, r_ref=120.0, stolt=False)
    assert abs(full[p0][j0] - bulk[p0][j0]) < 0.05 * abs(full[p0][j0])


def test_linear_in_the_data() -> None:
    a = omega_k(G, simulate_raw(G, TARGETS[:1]))
    b = omega_k(G, simulate_raw(G, TARGETS[1:]))
    for p in (58, 64, 72):
        for j in (12, 16, 24):
            assert abs(a[p][j] + b[p][j] - IMG[p][j]) < 1e-6 * abs(IMG[64][16])
