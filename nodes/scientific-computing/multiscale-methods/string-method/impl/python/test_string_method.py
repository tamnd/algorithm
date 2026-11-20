# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/string-method/. The authors are listed in prov/SDPAV5.jsonl.
import math

import pytest

from string_method import arc_lengths, muller_brown, reparametrize, string_method

A = [-0.55822, 1.44173]
C = [-0.05001, 0.46669]
S1 = (-0.82200, 0.62431, -40.6648)


def ring(p):
    # V = 4 (r - 1)^2 + sin(theta)^2: minima (1, 0) and (-1, 0), saddles (0, 1) and (0, -1)
    # with V = 1, and the minimum energy path is the unit circle.
    x, y = p
    r = math.hypot(x, y)
    th = math.atan2(y, x)
    dvdr = 8.0 * (r - 1.0)
    dvdth = 2.0 * math.sin(th) * math.cos(th)
    v = 4.0 * (r - 1.0) ** 2 + math.sin(th) ** 2
    return v, [dvdr * x / r - dvdth * y / (r * r), dvdr * y / r + dvdth * x / (r * r)]


def test_reparametrize_by_hand():
    poly = [[0.0, 0.0], [1.0, 0.0], [1.0, 2.0], [3.0, 2.0]]
    assert arc_lengths(poly) == pytest.approx([0.0, 0.2, 0.6, 1.0])
    out = reparametrize(poly)
    assert out[0] == [0.0, 0.0] and out[3] == [3.0, 2.0]
    assert out[1] == pytest.approx([1.0, 2.0 / 3.0])
    assert out[2] == pytest.approx([4.0 / 3.0, 2.0])
    gaps = [math.dist(a, b) for a, b in zip(poly, poly[1:])]
    assert sum(gaps) == pytest.approx(5.0)


def ring_string(n):
    init = [[1.0 - 2.0 * i / n, 0.8 * math.sin(math.pi * i / n)] for i in range(n + 1)]
    return string_method(ring, None, None, n, h=0.02, tol=1e-6, images=init)


def test_ring_string_goes_to_the_circle():
    errors = []
    for n in (8, 32):
        phi, en, it, ok = ring_string(n)
        assert ok and it < 200
        j = max(range(n + 1), key=lambda i: en[i])
        assert j == n // 2
        assert phi[j] == pytest.approx([0.0, 1.0], abs=1e-6)
        assert en[j] == pytest.approx(1.0, abs=1e-9)
        # The arc lengths are equal along the polygon before the last
        # reparametrization; along the new polygon they are nearly equal.
        gaps = [math.dist(a, b) for a, b in zip(phi, phi[1:])]
        assert max(gaps) - min(gaps) < 0.01 * min(gaps)
        errors.append(max(abs(math.hypot(*p) - 1.0) for p in phi))
    assert errors[0] < 0.025 and errors[1] < 0.004
    assert errors[1] < errors[0] / 4.0


def test_muller_brown_string():
    tops = []
    for n in (8, 32):
        phi, en, it, ok = string_method(muller_brown, A, C, n, h=2e-4, tol=1e-2)
        assert ok and it < 1000
        # The ends do steepest descent on their own and stay in the minima.
        assert phi[0] == pytest.approx(A, abs=1e-4)
        assert phi[-1] == pytest.approx(C, abs=1e-4)
        j = max(range(n + 1), key=lambda i: en[i])
        tops.append((en[j], phi[j]))
    assert tops[0][0] < S1[2] - 3.0
    assert tops[1][0] == pytest.approx(S1[2], abs=2e-3)
    assert tops[1][1] == pytest.approx(list(S1[:2]), abs=2e-3)
