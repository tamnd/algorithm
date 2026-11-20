# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-factorized-backprojection/. The authors are listed in prov/NKKE4Y.jsonl.

from fast_factorized_backprojection import (_box, direct_backprojection, ffbp, ffbp_cost, image_grid,
                                            simulate_compressed)

F0, B, FS, T0, N = 300e6, 100e6, 120e6, 2 * 370 / 3.0e8, 64
XA = [-40.0 + 1.25 * p for p in range(64)]
TARGETS = [(0.0, 400.0, 1.0), (3.75, 403.75, 0.5), (-4.375, 396.25, 0.7)]
PIX = image_grid([-5.0 + 0.625 * i for i in range(17)], [395.0 + 0.625 * i for i in range(17)])
DATA = simulate_compressed(XA, TARGETS, F0, B, FS, T0, N)
REF = direct_backprojection(DATA, XA, PIX, F0, FS, T0)
COUNT = []
FAST = ffbp(DATA, XA, PIX, F0, FS, T0, count=COUNT)
PEAK = max(abs(v) for v in REF)


def test_matches_direct_backprojection() -> None:
    assert max(abs(a - b) for a, b in zip(FAST, REF)) < 0.04 * PEAK


def test_targets_focus_at_their_positions() -> None:
    for x, y, amp in TARGETS:
        i = PIX.index((x, y))
        assert abs(abs(FAST[i]) - 64 * amp) < 0.05 * 64


def test_finer_beta_sampling_lowers_the_error() -> None:
    coarse = ffbp(DATA, XA, PIX, F0, FS, T0, oversample=4.0)
    e_coarse = max(abs(a - b) for a, b in zip(coarse, REF))
    e_fine = max(abs(a - b) for a, b in zip(FAST, REF))
    assert e_fine < 0.3 * e_coarse


def test_cost_formula_matches_the_count() -> None:
    assert COUNT[0] == ffbp_cost(XA, _box(PIX), len(PIX), F0, FS)


def test_speedup_grows_with_the_aperture() -> None:
    """P pulses and an n x n image with n = P / 4: direct costs P n^2, FFBP about n^2 log n."""
    ratios = []
    for p in (64, 256, 1024, 4096):
        n = p // 4
        xa = [1.25 * k for k in range(p)]
        r0, mid = 400.0 * p / 64, 1.25 * p / 2
        box = (mid - 0.3125 * n, mid + 0.3125 * n, r0, r0 + 0.625 * n)
        ratios.append(p * n * n / ffbp_cost(xa, box, n * n, F0, FS))
    assert all(b > 2.5 * a for a, b in zip(ratios, ratios[1:]))
    assert ratios[0] < 1 < ratios[2]


def test_linear_in_the_data() -> None:
    xa = XA[24:40]  # 16 pulses: two merging stages, enough to test linearity quickly
    d1 = simulate_compressed(xa, TARGETS[:1], F0, B, FS, T0, N)
    d2 = simulate_compressed(xa, TARGETS[1:], F0, B, FS, T0, N)
    small = PIX[::7]
    a = ffbp(d1, xa, small, F0, FS, T0)
    b = ffbp(d2, xa, small, F0, FS, T0)
    both = ffbp([[u + v for u, v in zip(r1, r2)] for r1, r2 in zip(d1, d2)], xa, small, F0, FS, T0)
    assert max(abs(u + v - w) for u, v, w in zip(a, b, both)) < 1e-9
