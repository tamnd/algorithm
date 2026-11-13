# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anisotropic-diffusion/. The authors are listed in prov/MYHS4D.jsonl.

"""Perona-Malik diffusion (1990) by the explicit 4-neighbor scheme.

An image is a list of H rows of W numbers, image[y][x]. One step is

    J(p) = I(p) + lam * sum over 4-neighbors q of p of g(|I(q) - I(p)|) (I(q) - I(p)).

Border rule: reflecting (Neumann) border. A neighbor outside the image adds
no flux, which is the same as giving it the value of the pixel itself.

If 0 <= g <= 1 and 0 < lam <= 1/4, every J(p) is a convex combination of
I(p) and its neighbors, so the values never leave [min I, max I]. The flux
between p and q is the negative of the flux between q and p, so the sum of
all pixels never changes.
"""

import math
from fractions import Fraction
from typing import Callable, List, Sequence, Union

Num = Union[int, float, Fraction]
Image = List[List[Num]]
NEIGHBORS = ((0, -1), (0, 1), (-1, 0), (1, 0))


def g_exponential(k: float) -> Callable[[Num], Num]:
    """Perona and Malik's first conductance, exp(-(s / K)^2)."""
    return lambda s: math.exp(-((s / k) ** 2))


def g_rational(k: Num) -> Callable[[Num], Num]:
    """Perona and Malik's second conductance, 1 / (1 + (s / K)^2); exact for Fraction K."""
    k2 = k * k
    return lambda s: k2 / (k2 + s * s)


def diffusion_step(image: Sequence[Sequence[Num]], lam: Num, g: Callable[[Num], Num]) -> Image:
    """One explicit step. O(WH)."""
    h = len(image)
    w = len(image[0]) if h else 0
    out: Image = []
    for y in range(h):  # @line L2
        row = []
        for x in range(w):
            p = image[y][x]
            flux: Num = 0  # @line L3
            for dy, dx in NEIGHBORS:  # @line L4
                qy, qx = y + dy, x + dx
                if 0 <= qy < h and 0 <= qx < w:
                    d = image[qy][qx] - p  # @line L5
                    flux = flux + g(abs(d)) * d  # @line L6
            row.append(p + lam * flux)  # @line L7
        out.append(row)
    return out


def anisotropic_diffusion(image: Sequence[Sequence[Num]], steps: int, lam: Num,
                          g: Callable[[Num], Num]) -> Image:
    """Run `steps` explicit Perona-Malik steps.

    Precondition for the maximum principle: 0 < lam <= 1/4 and 0 <= g <= 1.
    Cost: O(steps WH).
    """
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    cur = [list(row) for row in image]
    for _ in range(steps):  # @line L1
        cur = diffusion_step(cur, lam, g)  # @line L8
    return cur  # @line L9
