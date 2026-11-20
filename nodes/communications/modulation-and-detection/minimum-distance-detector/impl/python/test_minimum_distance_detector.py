# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-distance-detector/. The authors are listed in prov/NW9AYJ.jsonl.

import math
import random

import cbb
import constel
from minimum_distance_detector import detect, detect_general, detect_pam, detect_psk, detect_qam

# ---------------------------------------------------------------- the shared helper cbb.py


def test_cbb_q_function() -> None:
    assert abs(cbb.qfunc(1.0) - 0.158655) < 5e-7
    assert abs(cbb.qfunc(2.0) - 0.022750) < 5e-7
    assert abs(cbb.qfunc(3.0) - 0.0013499) < 5e-8
    assert abs(cbb.qinv(1e-5) - 4.26489) < 5e-6
    assert abs(cbb.qfunc(cbb.qinv(0.3)) - 0.3) < 1e-12
    # No cancellation in the far tail: Q(10) is about 7.6199e-24.
    assert abs(cbb.qfunc(10.0) / 7.619853024160527e-24 - 1) < 1e-9
    assert abs(cbb.db(2.0) - 3.0103) < 5e-5
    assert abs(cbb.undb(cbb.db(7.5)) - 7.5) < 1e-12


def test_cbb_dft_round_trip_and_parseval() -> None:
    rng = random.Random(1)
    x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(8)]
    xf = cbb.dft(x)
    assert max(abs(a - b) for a, b in zip(cbb.idft(xf), x)) < 1e-12
    assert abs(cbb.norm2(xf) - 8 * cbb.norm2(x)) < 1e-12
    u = cbb.udft(x)
    assert max(abs(a - b) for a, b in zip(cbb.uidft(u), x)) < 1e-12
    assert abs(cbb.norm2(u) - cbb.norm2(x)) < 1e-12
    # The DFT turns circular convolution into a product.
    h = [0.5 + 0.1j, -0.2j, 0.3]
    lhs = cbb.dft(cbb.cconv(x, h, 8))
    hf = cbb.dft(h + [0j] * 5)
    assert max(abs(a - b * c) for a, b, c in zip(lhs, xf, hf)) < 1e-12
    assert cbb.conv([1, 2], [1, -1, 3]) == [1, 1, 1, 6]


def test_cbb_linear_algebra() -> None:
    a = [[2 + 1j, 1, -1j], [0.5, 3 - 1j, 1 + 1j], [1j, -1, 4]]
    x = [1 - 2j, 0.5j, -1 + 1j]
    b = cbb.matvec(a, x)
    got = cbb.solve(a, b)
    assert max(abs(p - q) for p, q in zip(got, x)) < 1e-12
    ai = cbb.inv(a)
    i3 = cbb.matmul(a, ai)
    assert cbb.norm2(cbb.sub(i3, cbb.eye(3))) < 1e-24
    # det by cofactor expansion
    d = (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
         - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
         + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    assert abs(cbb.det(a) - d) < 1e-12
    assert cbb.det([[1, 2], [2, 4]]) == 0
    # Cholesky of A^H A + I
    g = cbb.add(cbb.matmul(cbb.herm(a), a), cbb.eye(3))
    low = cbb.cholesky(g)
    assert cbb.norm2(cbb.sub(cbb.matmul(low, cbb.herm(low)), g)) < 1e-22
    assert all(low[i][k] == 0 for i in range(3) for k in range(i + 1, 3))
    assert abs(cbb.dot([1j, 2], [1j, 1]) - 3) < 1e-15
    assert cbb.scale(2, [[1, 1j]]) == [[2, 2j]]
    assert cbb.zeros(2) == [0j, 0j] and cbb.zeros(1, 2) == [[0j, 0j]]


def test_cbb_noise_and_wilson() -> None:
    rng = random.Random(2)
    n = 20000
    mean = sum(abs(cbb.cn(rng, 0.5)) ** 2 for _ in range(n)) / n
    assert abs(mean - 0.5) < 0.03 * 0.5
    y = cbb.awgn(rng, [1 + 0j] * 4, 0.0)
    assert y == [1 + 0j] * 4
    lo, hi = cbb.wilson(50, 1000)
    assert lo < 0.05 < hi
    # The two ends are the roots of (p - 0.05)^2 = z^2 p (1 - p) / n.
    for p in (lo, hi):
        assert abs((p - 0.05) ** 2 - 3.29 ** 2 * p * (1 - p) / 1000) < 1e-15


# ---------------------------------------------------------------- the shared helper constel.py


def test_constel_energy_and_labels() -> None:
    raw16 = [p * math.sqrt(10) for p in constel.qam(16)]
    assert abs(constel.energy(raw16) - 10) < 1e-12
    for m in (2, 4, 8, 16):
        assert abs(constel.energy(constel.pam(m)) - 1) < 1e-12
        assert abs(constel.energy(constel.psk(m)) - 1) < 1e-12
    for m in (4, 16, 64):
        assert abs(constel.energy(constel.qam(m)) - 1) < 1e-12
    assert constel.pam(2) == [1 + 0j, -1 + 0j]
    q4 = constel.qam(4)
    s = 1 / math.sqrt(2)
    assert all(abs(a - b) < 1e-15 for a, b in zip(q4, [s + s * 1j, s - s * 1j, -s + s * 1j, -s - s * 1j]))
    assert [constel.gray(i) for i in range(8)] == [0, 1, 3, 2, 6, 7, 5, 4]
    assert constel.bits(6, 4) == [0, 1, 1, 0]
    assert constel.bit_errors(0b1011, 0b0010) == 2
    assert constel.bit_errors([1, 2, 3], [1, 1, 0]) == 4


def _dmin(points):
    return min(abs(a - b) for i, a in enumerate(points) for b in points[i + 1:])


def test_constel_gray_neighbors_differ_in_one_bit() -> None:
    cases = [constel.pam(m) for m in (2, 4, 8, 16)]
    cases += [constel.qam(m) for m in (4, 16, 64)]
    cases += [constel.psk(m) for m in (4, 8, 16)] + [constel.psk(8, math.pi / 8)]
    for pts in cases:
        d = _dmin(pts)
        pairs = 0
        for i, a in enumerate(pts):
            for k in range(i + 1, len(pts)):
                if abs(abs(a - pts[k]) - d) < 1e-9:
                    pairs += 1
                    assert constel.bit_errors(i, k) == 1
        assert pairs >= len(pts) - 1


def test_constel_check_values() -> None:
    assert abs(_dmin(constel.qam(16)) ** 2 - 0.4) < 1e-12
    assert abs(_dmin(constel.psk(8)) - 0.76537) < 5e-6


def test_constel_ml_vector_matches_ml_detect() -> None:
    rng = random.Random(3)
    pts = constel.qam(16)
    for _ in range(200):
        y = complex(rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5))
        h = complex(rng.uniform(-1, 1), rng.uniform(-1, 1))
        assert constel.ml_vector([y], [[h]], pts) == [constel.ml_detect(y, pts, h)]


# ---------------------------------------------------------------- the detector


def _grid(k, r):
    """A k by k grid on [-r, r]^2, shifted by an irrational step so few points sit on a boundary."""
    step = 2 * r / k
    return [complex(-r + (i + 0.5 * math.sqrt(2) - 0.5) * step, -r + (q + 0.5 * math.sqrt(3) - 0.5) * step)
            for i in range(k) for q in range(k)]


def _check(fast, pts, ys, h):
    ties = 0
    for y in ys:
        got = fast(y)
        ref = constel.ml_detect(y, pts, h)
        if got != ref:
            # Allowed only on a tie: the slicer's point is as close as the brute-force choice.
            assert abs(abs(y - h * pts[got]) - abs(y - h * pts[ref])) < 1e-12
            ties += 1
    assert ties <= len(ys) // 100


def test_slicer_matches_brute_force_on_a_grid() -> None:
    ys = _grid(36, 1.8)
    for h in (1, 0.6 + 0.8j, -0.3 + 0.2j):
        hy = [h * y for y in ys]
        for m in (2, 4, 8):
            _check(lambda y: detect_pam(y, m, h), constel.pam(m), hy, h)
        for m in (4, 16, 64):
            _check(lambda y: detect_qam(y, m, h), constel.qam(m), hy, h)
        for m in (2, 4, 8, 16):
            for ph in (0.0, math.pi / 4):
                _check(lambda y: detect_psk(y, m, h, ph), constel.psk(m, ph), hy, h)


def test_slicer_exact_on_points_and_far_away() -> None:
    for m in (4, 16, 64):
        pts = constel.qam(m)
        for i, p in enumerate(pts):
            assert detect(p, "qam", m) == i
            assert detect(10 * p, "qam", m) == constel.ml_detect(10 * p, pts)
    for m in (2, 8, 16):
        pts = constel.pam(m)
        for i, p in enumerate(pts):
            assert detect(p + 0.3j, "pam", m) == i
        pts = constel.psk(m, 0.1)
        for i, p in enumerate(pts):
            assert detect(0.01 * p, "psk", m, phase0=0.1) == i
            assert detect_general(p, pts) == i


def test_16qam_symbol_error_rate() -> None:
    # 16-QAM at Es/N0 = 15 dB: SER = 0.017782 (check value). n = 20000 symbols gives about
    # 356 expected errors. Seed 5, Wilson interval with z = 3.29.
    rng = random.Random(5)
    m, n = 16, 20000
    pts = constel.qam(m)
    n0 = 1 / cbb.undb(15.0)
    errors = 0
    for _ in range(n):
        i = rng.randrange(m)
        y = pts[i] + cbb.cn(rng, n0)
        errors += detect_qam(y, m) != i
    p = 2 * (1 - 1 / math.sqrt(m)) * cbb.qfunc(math.sqrt(3 * cbb.undb(15.0) / (m - 1)))
    ser = 1 - (1 - p) ** 2
    assert abs(ser - 0.017782) < 5e-7
    lo, hi = cbb.wilson(errors, n)
    assert lo <= ser <= hi


def test_8psk_symbol_error_rate_with_a_channel_gain() -> None:
    # 8-PSK at Es/N0 = 12 dB through h = 0.6 + 0.8j (|h| = 1). The approximation
    # 2Q(sqrt(2 Es/N0) sin(pi/8)) is about 0.0236 here. n = 10000, seed 6.
    rng = random.Random(6)
    m, n, h = 8, 10000, 0.6 + 0.8j
    pts = constel.psk(m)
    n0 = 1 / cbb.undb(12.0)
    errors = 0
    for _ in range(n):
        i = rng.randrange(m)
        y = h * pts[i] + cbb.cn(rng, n0)
        errors += detect_psk(y, m, h) != i
    approx = 2 * cbb.qfunc(math.sqrt(2 * cbb.undb(12.0)) * math.sin(math.pi / m))
    lo, hi = cbb.wilson(errors, n)
    assert lo <= approx <= hi
