# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frequency-response/. The authors are listed in prov/7WHC1B.jsonl.

"""Frequency response of a filter with a rational transfer function.

The filter is a0 y[n] + a1 y[n-1] + ... + ap y[n-p] = b0 x[n] + ... + bq x[n-q],
with a0 != 0, causal and at rest before the input starts. Its transfer
function is H(z) = B(z) / A(z) with B(z) = sum b_k z^(-k) and A(z) = sum a_k z^(-k).
The frequency w is in radians per sample.
"""

import cmath
from typing import Sequence


def poly_at(c: Sequence, zinv: complex) -> complex:
    """sum_k c[k] zinv^k by Horner's rule: len(c) - 1 multiplications."""
    acc = 0j
    for v in reversed(c):
        acc = acc * zinv + v
    return acc


def freq_response(b: Sequence, a: Sequence, w: float) -> complex:
    """H(e^(iw)) = B(e^(-iw)) / A(e^(-iw)). Valid as a frequency response only for a stable filter."""
    zinv = cmath.exp(-1j * w)
    return poly_at(b, zinv) / poly_at(a, zinv)


def group_delay(b: Sequence, a: Sequence, w: float) -> float:
    """-d arg H / dw in samples. For P(w) = sum p_k e^(-iwk), -d arg P / dw = Re(sum k p_k e^(-iwk) / P)."""
    zinv = cmath.exp(-1j * w)

    def tau(c: Sequence) -> float:
        num = poly_at([k * v for k, v in enumerate(c)], zinv)
        return (num / poly_at(c, zinv)).real

    return tau(b) - tau(a)


def lfilter(b: Sequence, a: Sequence, x: Sequence) -> list:
    """Run the difference equation on x with initial rest. Exact on Fractions."""
    a0 = a[0]
    y: list = []
    for n in range(len(x)):
        acc = sum(b[k] * x[n - k] for k in range(len(b)) if n - k >= 0)
        acc -= sum(a[k] * y[n - k] for k in range(1, len(a)) if n - k >= 0)
        y.append(acc / a0)
    return y


def impulse_response(b: Sequence, a: Sequence, count: int) -> list:
    """The first count samples of h, the response to the unit impulse."""
    one = b[0] * 0 + 1 if b else 1
    return lfilter(b, a, [one] + [one * 0] * (count - 1))


def dtft(h: Sequence, w: float) -> complex:
    """Direct DTFT of a finite sequence starting at n = 0: sum h[n] e^(-iwn)."""
    return sum(h[n] * cmath.exp(-1j * w * n) for n in range(len(h)))
