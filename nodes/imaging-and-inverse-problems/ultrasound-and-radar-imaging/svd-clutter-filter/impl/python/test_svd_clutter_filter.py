# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/svd-clutter-filter/. The authors are listed in prov/BBV2DJ.jsonl.

import cmath
import math
import random

from imgla import svd
from svd_clutter_filter import (casorati, frames_of, simulate, singular_values, svd_clutter_filter,
                                svd_filter_matrix)


def _cgauss(rng, sig=1.0):
    return complex(rng.gauss(0.0, sig), rng.gauss(0.0, sig))


def _rand(rng, m, n):
    return [[_cgauss(rng) for _ in range(n)] for _ in range(m)]


def _fro2(a):
    return sum(abs(v) ** 2 for row in a for v in row)


def _diff2(a, b):
    return sum(abs(x - y) ** 2 for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def test_matches_the_reference_svd_of_the_real_embedding() -> None:
    # Reference: imgla.svd of [[Re S, -Im S], [Im S, Re S]], whose singular values
    # are those of S, each twice; removing its top 2k terms removes the top k of S.
    rng = random.Random(6201)
    m, n, k = 20, 7, 2
    s = _rand(rng, m, n)
    emb = [[v.real for v in r] + [-v.imag for v in r] for r in s] + [[v.imag for v in r] + [v.real for v in r] for r in s]
    u, sv, v = svd(emb)
    sigma = singular_values(s)
    for j in range(n):
        assert abs(sigma[j] - sv[2 * j]) < 1e-9 * sv[0]
        assert abs(sigma[j] - sv[2 * j + 1]) < 1e-9 * sv[0]
    ref = [[emb[i][j] - sum(sv[q] * u[i][q] * v[j][q] for q in range(2 * k)) for j in range(2 * n)] for i in range(2 * m)]
    sf, _ = svd_filter_matrix(s, k)
    for i in range(m):
        for j in range(n):
            assert abs(sf[i][j] - complex(ref[i][j], ref[m + i][j])) < 1e-9 * sv[0]


def test_exact_separation_when_tissue_and_blood_are_orthogonal() -> None:
    # Tissue in rows 0, 1, 4, 5 with slow time tones on DFT bins 0 and 1; blood in
    # rows 2, 3 with tones on bins 3 to 7. The two parts are orthogonal in space and
    # in slow time, and the tissue singular values are the largest ones.
    nz, nx, nt = 6, 4, 8
    rng = random.Random(6202)
    tissue_rows, vessel = (0, 1, 4, 5), (2, 3)
    a = [[_cgauss(rng, 5.0) if i in tissue_rows else 0j for j in range(nx)] for i in range(nz)]
    b = [[_cgauss(rng, 4.0) if i in tissue_rows else 0j for j in range(nx)] for i in range(nz)]
    blood_bin = [[3 + (i * nx + j) % 5 for j in range(nx)] for i in range(nz)]
    blood_amp = [[_cgauss(rng, 0.3) if i in vessel else 0j for j in range(nx)] for i in range(nz)]
    frames, blood = [], []
    for t in range(nt):
        e0, e1 = 1.0, cmath.exp(2j * math.pi * t / nt)
        bl = [[blood_amp[i][j] * cmath.exp(2j * math.pi * blood_bin[i][j] * t / nt) for j in range(nx)]
              for i in range(nz)]
        blood.append(bl)
        frames.append([[a[i][j] * e0 + b[i][j] * e1 + bl[i][j] for j in range(nx)] for i in range(nz)])
    out, _, sigma = svd_clutter_filter(frames, 2)
    assert sigma[1] > 5 * sigma[2]
    for t in range(nt):
        for i in range(nz):
            for j in range(nx):
                assert abs(out[t][i][j] - blood[t][i][j]) < 1e-9


def test_removed_energy_is_the_tail_and_no_rank_k_matrix_does_better() -> None:
    rng = random.Random(6203)
    m, n = 18, 6
    s = _rand(rng, m, n)
    sigma = singular_values(s)
    for k in range(n + 1):
        sf, _ = svd_filter_matrix(s, k)
        assert abs(_fro2(sf) - sum(x * x for x in sigma[k:])) < 1e-9 * _fro2(s)
        assert abs(_diff2(s, sf) - sum(x * x for x in sigma[:k])) < 1e-9 * _fro2(s)
    # S - S_f is the best rank-k approximation: random rank-one competitors fit worse.
    sf, _ = svd_filter_matrix(s, 1)
    best = _fro2(sf)
    for _ in range(30):
        x = [_cgauss(rng) for _ in range(m)]
        y = [_cgauss(rng) for _ in range(n)]
        # the best scalar for the direction x y^H, so each competitor is fitted
        num = sum(x[i].conjugate() * s[i][j] * y[j] for i in range(m) for j in range(n))
        den = sum(abs(v) ** 2 for v in x) * sum(abs(v) ** 2 for v in y)
        g = num / den
        resid = sum(abs(s[i][j] - g * x[i] * y[j].conjugate()) ** 2 for i in range(m) for j in range(n))
        assert resid >= best - 1e-9


def test_noise_cut_keeps_the_middle_band() -> None:
    rng = random.Random(6204)
    s = _rand(rng, 15, 6)
    sigma = singular_values(s)
    sf, _ = svd_filter_matrix(s, 1, 4)
    assert abs(_fro2(sf) - sum(x * x for x in sigma[1:4])) < 1e-9 * _fro2(s)
    full, _ = svd_filter_matrix(s, 0)
    assert _diff2(full, s) < 1e-18 * _fro2(s)


def test_pixel_order_and_global_phase_do_not_matter() -> None:
    rng = random.Random(6205)
    s = _rand(rng, 12, 5)
    sf, _ = svd_filter_matrix(s, 2)
    perm = list(range(12))
    rng.shuffle(perm)
    g = 0.7 * cmath.exp(0.9j)
    sp, _ = svd_filter_matrix([[g * v for v in s[p]] for p in perm], 2)
    for r, p in enumerate(perm):
        for t in range(5):
            assert abs(sp[r][t] - g * sf[p][t]) < 1e-9


def test_a_frequency_shift_of_all_echoes_gives_the_shifted_output() -> None:
    # Multiplying slow time sample t by exp(i w t) is a unitary change of the
    # columns, so the filter output is shifted in the same way. The SVD filter
    # separates by energy and spatial coherence, not by Doppler frequency.
    rng = random.Random(6206)
    s = _rand(rng, 14, 6)
    w = 1.3
    shifted = [[v * cmath.exp(1j * w * t) for t, v in enumerate(row)] for row in s]
    sf, _ = svd_filter_matrix(s, 2)
    ss, _ = svd_filter_matrix(shifted, 2)
    for row_f, row_s in zip(sf, ss):
        for t in range(6):
            assert abs(row_s[t] - row_f[t] * cmath.exp(1j * w * t)) < 1e-9


def test_casorati_round_trip() -> None:
    rng = random.Random(6207)
    frames = [[[_cgauss(rng) for _ in range(3)] for _ in range(4)] for _ in range(5)]
    s = casorati(frames)
    assert len(s) == 12 and len(s[0]) == 5
    assert s[1 * 3 + 2][4] == frames[4][1][2]
    assert frames_of(s, 4, 3) == frames


def test_power_doppler_contrast_on_a_simulated_vessel() -> None:
    nz, nx, nt = 8, 6, 16
    frames, mask = simulate(nz, nx, nt, (3, 5), seed=6208)

    def contrast(pd):
        inside = [pd[i][j] for i in range(nz) for j in range(nx) if mask[i][j]]
        outside = [pd[i][j] for i in range(nz) for j in range(nx) if not mask[i][j]]
        return (sum(inside) / len(inside)) / (sum(outside) / len(outside))

    _, raw, sigma = svd_clutter_filter(frames, 0)
    _, pd1, _ = svd_clutter_filter(frames, 1)
    _, pd3, _ = svd_clutter_filter(frames, 3)
    # The tissue is strong and close to rank one: sigma_1 holds almost all the energy.
    assert sigma[0] ** 2 > 0.95 * sum(x * x for x in sigma)
    assert contrast(raw) < 0.5
    assert contrast(pd1) > 50.0
    # A cut-off rank that is too high also removes blood.
    assert contrast(pd3) < contrast(pd1)
