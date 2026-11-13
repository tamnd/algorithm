# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-wavelet-transform/. The authors are listed in prov/CM5P8S.jsonl.

import math
import random
from fractions import Fraction

import pytest

from discrete_wavelet_transform import (
    HAAR_AVG,
    LEGALL_53,
    analysis_step,
    dwt,
    idwt,
    orthonormal_bank,
)


class QR2:
    """Exact numbers a + b*sqrt(2) with rational a and b."""

    def __init__(self, a, b=0):
        self.a, self.b = Fraction(a), Fraction(b)

    def _c(self, o):
        return o if isinstance(o, QR2) else QR2(o)

    def __add__(self, o):
        o = self._c(o)
        return QR2(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self):
        return QR2(-self.a, -self.b)

    def __sub__(self, o):
        return self + (-self._c(o))

    def __mul__(self, o):
        o = self._c(o)
        return QR2(self.a * o.a + 2 * self.b * o.b, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def __eq__(self, o):
        o = self._c(o)
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))


R = QR2(0, Fraction(1, 2))  # 1/sqrt(2)


def dense_reference(x, ht, gt, levels):
    """Brute force: build each level as an explicit matrix and multiply."""
    a, out = list(x), []
    for _ in range(levels):
        m = len(a)
        rows_s = [[0] * m for _ in range(m // 2)]
        rows_d = [[0] * m for _ in range(m // 2)]
        for i in range(m // 2):
            for k in range(m):
                for l, c in ht.items():
                    if (2 * i + l - k) % m == 0:
                        rows_s[i][k] = rows_s[i][k] + c
                for l, c in gt.items():
                    if (2 * i + l - k) % m == 0:
                        rows_d[i][k] = rows_d[i][k] + c
        s = [sum((r[k] * a[k] for k in range(m)), 0) for r in rows_s]
        d = [sum((r[k] * a[k] for k in range(m)), 0) for r in rows_d]
        out.append(d)
        a = s
    return a, out


def test_example_ramp() -> None:
    x = [1, 2, 3, 4, 5, 6, 7, 8]
    a, ds = dwt(x, LEGALL_53[0], LEGALL_53[1], 1)
    assert a == [2, 3, 5, 8] and ds == [[0, 0, 0, 4]]
    a, ds = dwt(x, LEGALL_53[0], LEGALL_53[1], 3)
    assert a == [Fraction(9, 2)]
    assert ds == [[0, 0, 0, 4], [Fraction(-1, 2), Fraction(9, 2)], [3]]
    a, ds = dwt(x, HAAR_AVG[0], HAAR_AVG[1], 3)
    assert a == [Fraction(9, 2)]
    assert ds == [[Fraction(-1, 2)] * 4, [-1, -1], [-2]]


@pytest.mark.parametrize("bank", [HAAR_AVG, LEGALL_53])
def test_perfect_reconstruction_exact(bank) -> None:
    ht, gt, h, g = bank
    rng = random.Random(7)
    for n, levels in [(2, 1), (4, 2), (8, 3), (16, 4), (24, 3), (32, 2)]:
        for _ in range(10):
            x = [Fraction(rng.randint(-50, 50), rng.randint(1, 9)) for _ in range(n)]
            a, ds = dwt(x, ht, gt, levels)
            assert idwt(a, ds, h, g) == x
            assert (a, ds) == dense_reference(x, ht, gt, levels)


def test_biorthogonality_of_53() -> None:
    ht, gt, h, g = LEGALL_53

    def corr(p, q, shift):
        return sum(c * q.get(l - shift, 0) for l, c in p.items())

    for k in range(-4, 5):
        assert corr(ht, h, 2 * k) == (1 if k == 0 else 0)
        assert corr(gt, g, 2 * k) == (1 if k == 0 else 0)
        assert corr(ht, g, 2 * k) == 0
        assert corr(gt, h, 2 * k) == 0


def test_mean_is_kept() -> None:
    rng = random.Random(3)
    for bank in (HAAR_AVG, LEGALL_53):
        x = [rng.randint(0, 255) for _ in range(16)]
        a, _ = dwt(x, bank[0], bank[1], 4)
        assert a == [Fraction(sum(x), 16)]


def test_vanishing_moments() -> None:
    # 5/3 analysis high-pass has two vanishing moments: sum g = sum l g = 0.
    gt = LEGALL_53[1]
    assert sum(gt.values()) == 0
    assert sum(l * c for l, c in gt.items()) == 0
    assert sum(l * l * c for l, c in gt.items()) != 0


def test_orthonormal_haar_energy_exact() -> None:
    lo, hi, slo, shi = orthonormal_bank([R, R])
    rng = random.Random(11)
    for t in range(1, 6):
        n = 1 << t
        x = [QR2(rng.randint(-20, 20)) for _ in range(n)]
        a, ds = dwt(x, lo, hi, t)
        energy_in = sum((v * v for v in x), QR2(0))
        energy_out = sum((v * v for v in a + [c for d in ds for c in d]), QR2(0))
        assert energy_out == energy_in
        assert idwt(a, ds, slo, shi) == x
        # closed form: block sums over the Haar supports
        for j, d in enumerate(ds):
            blk = 1 << (j + 1)
            for k, c in enumerate(d):
                left = sum(x[k * blk + r].a for r in range(blk // 2))
                right = sum(x[k * blk + blk // 2 + r].a for r in range(blk // 2))
                assert c * c == QR2((left - right) ** 2 / blk)


def test_daubechies4_float() -> None:
    s3 = math.sqrt(3)
    h = [(1 + s3) / (4 * math.sqrt(2)), (3 + s3) / (4 * math.sqrt(2)), (3 - s3) / (4 * math.sqrt(2)), (1 - s3) / (4 * math.sqrt(2))]
    lo, hi, slo, shi = orthonormal_bank(h)
    rng = random.Random(5)
    for n, levels in [(8, 2), (16, 3), (64, 5)]:
        x = [rng.uniform(-1, 1) for _ in range(n)]
        a, ds = dwt(x, lo, hi, levels)
        e_in = sum(v * v for v in x)
        e_out = sum(v * v for v in a) + sum(c * c for d in ds for c in d)
        assert abs(e_in - e_out) <= 1e-12 * n
        back = idwt(a, ds, slo, shi)
        assert max(abs(p - q) for p, q in zip(back, x)) <= 1e-12
        ra, rds = dense_reference(x, lo, hi, levels)
        assert max(abs(p - q) for p, q in zip(a + sum(ds, []), ra + sum(rds, []))) <= 1e-12
    # two vanishing moments: zero details on a ramp away from the wrap
    _, d = analysis_step([float(i) for i in range(8)], lo, hi)
    assert all(abs(v) < 1e-12 for v in d[:3]) and abs(d[3]) > 1


def test_edges() -> None:
    a, ds = dwt([5, 7], *HAAR_AVG[:2], 0)
    assert a == [5, 7] and ds == []
    with pytest.raises(ValueError):
        dwt([1, 2, 3], *HAAR_AVG[:2], 1)
    with pytest.raises(ValueError):
        dwt([1, 2, 3, 4, 5, 6], *HAAR_AVG[:2], 2)
