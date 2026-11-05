# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/golden-section-search/. The authors are listed in prov/ZDRDPS.jsonl.

import math
from typing import Callable

RHO = (math.sqrt(5) - 1) / 2  # 1/phi, about 0.618


def golden_section_min(f: Callable[[float], float], a: float, b: float, steps: int = 100) -> float:
    """Return a point near the minimum of a strictly unimodal f on [a, b].

    It evaluates f exactly steps + 2 times. After the loop the minimum lies in
    an interval of length (b - a) * RHO ** (steps + 1), whose midpoint is returned.
    """
    rho = RHO  # @line L1
    c = b - rho * (b - a)  # @line L2
    d = a + rho * (b - a)
    fc = f(c)  # @line L3
    fd = f(d)
    for _ in range(steps):  # @line L4
        if fc < fd:  # @line L5
            b, d, fd = d, c, fc  # @line L6
            c = b - rho * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd  # @line L7
            d = a + rho * (b - a)
            fd = f(d)
    if fc < fd:  # @line L8
        b = d
    else:
        a = c
    return a + (b - a) / 2  # @line L9
