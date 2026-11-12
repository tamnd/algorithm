# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/porter-duff-compositing/. The authors are listed in prov/BSR165.jsonl.

"""The twelve Porter-Duff compositing operators on premultiplied RGBA pixels.

A pixel is a tuple (r, g, b, a) whose color channels are already multiplied
by the coverage a, so 0 <= r, g, b <= a <= 1. The values can be floats or
fractions.Fraction; with Fraction every result is exact.
"""

from fractions import Fraction
from typing import Callable, Sequence, Union

Num = Union[int, float, Fraction]
Pixel = tuple
Image = list
Factor = Callable[[Num, Num], Num]

# For each operator: (F_A, F_B) as functions of (alpha_A, alpha_B).
# Porter and Duff 1984, Section 4.2, the table of operators.
OPERATORS: dict[str, tuple[Factor, Factor]] = {
    "clear": (lambda aa, ab: 0, lambda aa, ab: 0),
    "A": (lambda aa, ab: 1, lambda aa, ab: 0),
    "B": (lambda aa, ab: 0, lambda aa, ab: 1),
    "A over B": (lambda aa, ab: 1, lambda aa, ab: 1 - aa),
    "B over A": (lambda aa, ab: 1 - ab, lambda aa, ab: 1),
    "A in B": (lambda aa, ab: ab, lambda aa, ab: 0),
    "B in A": (lambda aa, ab: 0, lambda aa, ab: aa),
    "A out B": (lambda aa, ab: 1 - ab, lambda aa, ab: 0),
    "B out A": (lambda aa, ab: 0, lambda aa, ab: 1 - aa),
    "A atop B": (lambda aa, ab: ab, lambda aa, ab: 1 - aa),
    "B atop A": (lambda aa, ab: 1 - ab, lambda aa, ab: aa),
    "A xor B": (lambda aa, ab: 1 - ab, lambda aa, ab: 1 - aa),
}


def porter_duff_compositing(op: str, image_a: Image, image_b: Image) -> Image:
    """Composite two premultiplied RGBA images of the same size, pixel by pixel.

    Precondition: both images are H rows of W pixels with the same channel
    count, the last channel being the coverage alpha, and every color channel
    at most alpha. Cost: O(WH) time and O(WH) space for the output.
    """
    fa_of, fb_of = OPERATORS[op]  # @line L1
    if len(image_a) != len(image_b) or any(len(r) != len(s) for r, s in zip(image_a, image_b)):
        raise ValueError("the images differ in size")
    out: Image = []
    for row_a, row_b in zip(image_a, image_b):  # @line L2
        row = []
        for a, b in zip(row_a, row_b):
            alpha_a, alpha_b = a[-1], b[-1]  # @line L3
            fa, fb = fa_of(alpha_a, alpha_b), fb_of(alpha_a, alpha_b)  # @line L4
            row.append(tuple(fa * x + fb * y for x, y in zip(a, b)))  # @line L5
        out.append(row)
    return out  # @line L6


def composite_pixel(op: str, a: Sequence[Num], b: Sequence[Num]) -> Pixel:
    """Composite one premultiplied pixel a with one pixel b. O(1)."""
    return porter_duff_compositing(op, [[tuple(a)]], [[tuple(b)]])[0][0]


def over(a: Sequence[Num], b: Sequence[Num]) -> Pixel:
    """A over B on premultiplied pixels."""
    return composite_pixel("A over B", a, b)


def plus(a: Sequence[Num], b: Sequence[Num]) -> Pixel:
    """A plus B: F_A = F_B = 1. The caller keeps the sum in range."""
    return tuple(x + y for x, y in zip(a, b))


def darken(a: Sequence[Num], phi: Num) -> Pixel:
    """Scale the color channels by phi and keep the coverage."""
    return tuple(phi * x for x in a[:-1]) + (a[-1],)


def dissolve(a: Sequence[Num], delta: Num) -> Pixel:
    """Scale all channels, coverage included, by delta."""
    return tuple(delta * x for x in a)


def opaque(a: Sequence[Num], omega: Num) -> Pixel:
    """Scale only the coverage by omega."""
    return tuple(a[:-1]) + (omega * a[-1],)


def premultiply(color: Sequence[Num], alpha: Num) -> Pixel:
    """Turn a straight color and a coverage into a premultiplied pixel."""
    return tuple(alpha * c for c in color) + (alpha,)


def unpremultiply(p: Sequence[Num]) -> tuple:
    """Return (straight color, alpha). A pixel with alpha 0 gets color 0."""
    alpha = p[-1]
    if alpha == 0:
        return tuple(0 for _ in p[:-1]), alpha
    return tuple(c / alpha for c in p[:-1]), alpha
