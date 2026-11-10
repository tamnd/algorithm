# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coupling-from-the-past/. The authors are listed in prov/3S0NKB.jsonl.

import random
from typing import Callable, Hashable, Sequence, TypeVar

S = TypeVar("S", bound=Hashable)
U = TypeVar("U")


class NoCoalescence(RuntimeError):
    """Raised when the chains have not met after the largest allowed start time."""


def monotone_cftp(
    update: Callable[[S, U], S],
    bottom: S,
    top: S,
    draw: Callable[[random.Random], U],
    rng: random.Random,
    max_t: int = 1 << 20,
) -> tuple[S, int]:
    """Return (sample, T): one exact draw from the stationary distribution.

    update(x, u) is a monotone update rule: x <= y implies
    update(x, u) <= update(y, u) for every u, and bottom <= x <= top for
    every state x. draw(rng) returns one random value u. The value u_t,
    which drives the step from time -t to time -t + 1, is drawn once and
    reused for each larger start time T. T doubles: 1, 2, 4, ...

    The values are drawn in the order u_1, u_2, u_3, ..., so a scripted
    generator sees the same order on each run. Raises NoCoalescence if
    the chains from bottom and top do not meet for T = max_t.
    """
    t_start = 1  # @line L1
    us: list[U] = []  # @line L2
    while True:  # @line L3
        while len(us) < t_start:  # @line L4
            us.append(draw(rng))
        lo, hi = bottom, top  # @line L5
        for t in range(t_start, 0, -1):  # @line L6
            u = us[t - 1]
            lo, hi = update(lo, u), update(hi, u)  # @line L7
        if lo == hi:  # @line L8
            return lo, t_start
        if t_start >= max_t:
            raise NoCoalescence(f"no coalescence from T = {t_start}")
        t_start *= 2  # @line L9


def coupling_from_the_past(
    update: Callable[[S, U], S],
    states: Sequence[S],
    draw: Callable[[random.Random], U],
    rng: random.Random,
    max_t: int = 1 << 20,
) -> tuple[S, int]:
    """Return (sample, T) by CFTP that follows every state of a finite chain.

    No order is needed. It costs |states| updates for each step, so it is
    for small chains and for tests. The output is exact when, with
    probability 1, some composition of the random maps is constant.
    """
    t_start = 1
    us: list[U] = []
    while True:
        while len(us) < t_start:
            us.append(draw(rng))
        image = set(states)
        for t in range(t_start, 0, -1):
            u = us[t - 1]
            image = {update(x, u) for x in image}
        if len(image) == 1:
            return next(iter(image)), t_start
        if t_start >= max_t:
            raise NoCoalescence(f"no coalescence from T = {t_start}")
        t_start *= 2


def forward_coupling(
    update: Callable[[S, U], S],
    bottom: S,
    top: S,
    draw: Callable[[random.Random], U],
    rng: random.Random,
    max_steps: int = 1 << 20,
) -> tuple[S, int]:
    """The wrong method, kept for comparison: run forward until the chains meet.

    It returns the state where the chains from bottom and top first meet.
    The meeting time depends on the path, so the output is biased.
    """
    lo, hi = bottom, top
    for step in range(1, max_steps + 1):
        u = draw(rng)
        lo, hi = update(lo, u), update(hi, u)
        if lo == hi:
            return lo, step
    raise NoCoalescence(f"no meeting after {max_steps} steps")


def walk_update(k: int, m: int, down: int, up: int) -> Callable[[int, int], int]:
    """A monotone update rule for a walk on 0..k, driven by a draw u in 0..m-1.

    A draw u < down moves down (or stays at 0). A draw u >= m - up moves up
    (or stays at k). Other draws stay. With a uniform draw, the chain moves
    down with probability down/m and up with probability up/m. It is the
    example of the page, with k = 2, m = 4, down = 2 and up = 1.
    """
    if down + up > m:
        raise ValueError("down + up must be at most m")

    def update(x: int, u: int) -> int:
        if u < down:
            return max(x - 1, 0)
        if u >= m - up:
            return min(x + 1, k)
        return x

    return update
