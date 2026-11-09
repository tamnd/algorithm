# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/great-deluge-algorithm/. The authors are listed in prov/HPWTJM.jsonl.

import random
from typing import Callable, TypeVar

S = TypeVar("S")


def great_deluge(
    x0: S,
    f: Callable[[S], float],
    neighbor: Callable[[S, random.Random], S],
    level: float,
    rain: float,
    steps: int,
    rng: random.Random,
    trace: list | None = None,
) -> tuple[S, float]:
    """Minimize f by the great deluge algorithm of Dueck (1993). Return (best, f(best)).

    A neighbor y is accepted if and only if f(y) < level, whatever f(x) is.
    After each accepted move the level falls by rain > 0. If trace is a list,
    append (level, x, y, f(x), f(y), accepted) for each step, with the level
    used in the test.
    """
    x, fx = x0, f(x0)  # @line L1
    best, fb = x, fx
    for _ in range(steps):  # @line L2
        y = neighbor(x, rng)  # @line L3
        fy = f(y)
        accepted = fy < level  # @line L4
        if trace is not None:
            trace.append((level, x, y, fx, fy, accepted))
        if accepted:
            x, fx = y, fy  # @line L5
            level -= rain  # @line L6
            if fx < fb:  # @line L7
                best, fb = x, fx
    return best, fb  # @line L8
