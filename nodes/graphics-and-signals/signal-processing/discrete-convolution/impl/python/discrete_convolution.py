# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-convolution/. The authors are listed in prov/BWFWVW.jsonl.

"""Direct discrete convolution of two finite sequences.

A finite sequence is a list of values together with the index of its first
entry, so that x[n] = values[n - start] for start <= n < start + len(values)
and x[n] = 0 elsewhere. The values may be int, Fraction, float or complex.
"""

from typing import Sequence, TypeVar

T = TypeVar("T")


def convolve(x: Sequence[T], h: Sequence[T]) -> list[T]:
    """Full linear convolution of x and h, both starting at index 0.

    The result has len(x) + len(h) - 1 entries and starts at index 0.
    It costs len(x) * len(h) multiplications.
    """
    if not x or not h:
        return []
    y = [x[0] * h[0] - x[0] * h[0]] * (len(x) + len(h) - 1)  # zeros of the right type
    for i, xi in enumerate(x):
        for k, hk in enumerate(h):
            y[i + k] += xi * hk
    return y


def convolve_indexed(x: Sequence[T], x_start: int, h: Sequence[T], h_start: int) -> tuple[list[T], int]:
    """Convolution of two finite sequences with arbitrary start indices.

    Returns (values, start). The support of the result starts at
    x_start + h_start, because x[i] h[k] lands at time i + k.
    """
    return convolve(x, h), x_start + h_start


def convolve_mode(x: Sequence[T], h: Sequence[T], mode: str = "full") -> list[T]:
    """Linear convolution trimmed to one of three common output windows.

    full:  all len(x) + len(h) - 1 outputs.
    same:  len(x) outputs, centred as y[n + (len(h) - 1) // 2].
    valid: the len(x) - len(h) + 1 outputs whose window lies inside x
           (empty when h is longer than x).
    """
    y = convolve(x, h)
    n, m = len(x), len(h)
    if mode == "full":
        return y
    if mode == "same":
        off = (m - 1) // 2
        return y[off:off + n]
    if mode == "valid":
        if m > n:
            return []
        return y[m - 1:n]
    raise ValueError("mode must be full, same or valid")
