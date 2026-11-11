# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pollard-rho-collision-search/. The authors are listed in prov/YJ25N1.jsonl.
"""Pollard rho collision search: iterate f, find the cycle, return the two points that meet.

For study only. The code is not constant time, and it is meant to run only on
toy targets, such as SHA-256 cut down to 24 to 32 bits. Do not use a truncated
hash to protect real data; use a full-length hash from the standard library, a
FIPS 140 validated module, or libsodium.

f maps the integers 0 .. N-1 to themselves. Cost: about 3 * sqrt(pi N / 2)
calls of f on average for Floyd, and O(1) memory.
"""

import random
from typing import Callable, Optional

Func = Callable[[int], int]


def rho_collision(f: Func, x0: int) -> Optional[tuple[int, int]]:
    """Return (a, b) with a != b and f(a) == f(b), found on the rho path from x0.

    Returns None when x0 lies on its own cycle (tail length 0), since then no
    collision is on the path; the caller restarts from another point.
    """
    tortoise = f(x0)  # @line L1
    hare = f(f(x0))  # @line L1
    while tortoise != hare:  # @line L2
        tortoise = f(tortoise)  # @line L3
        hare = f(f(hare))  # @line L3
    tortoise = x0  # @line L4
    if tortoise == hare:  # @line L5
        return None  # @line L5
    ft, fh = f(tortoise), f(hare)
    while ft != fh:  # @line L6
        tortoise, hare = ft, fh  # @line L7
        ft, fh = f(tortoise), f(hare)  # @line L7
    return tortoise, hare  # @line L8


def find_collision(f: Func, n_values: int, rng: random.Random, tries: int = 64) -> tuple[int, int]:
    """Run rho_collision from random start points until it finds a collision."""
    for _ in range(tries):
        res = rho_collision(f, rng.randrange(n_values))
        if res is not None:
            return res
    raise RuntimeError("every start point was on its own cycle")


def tail_and_cycle(f: Func, x0: int) -> tuple[int, int]:
    """Return (mu, lam): the tail length and the cycle length of the path from x0, by Brent's method."""
    power = lam = 1
    tortoise, hare = x0, f(x0)
    while tortoise != hare:
        if power == lam:
            tortoise = hare
            power *= 2
            lam = 0
        hare = f(hare)
        lam += 1
    tortoise = hare = x0
    for _ in range(lam):
        hare = f(hare)
    mu = 0
    while tortoise != hare:
        tortoise, hare = f(tortoise), f(hare)
        mu += 1
    return mu, lam


def distinguished_point_search(
    f: Func, n_values: int, dp_bits: int, rng: random.Random, max_walks: int = 1 << 20
) -> tuple[tuple[int, int], int]:
    """Parallel collision search with distinguished points (van Oorschot and Wiener).

    Walks start at random points and stop at a point whose low dp_bits bits are
    zero. The walks here run one after another, as one machine would simulate
    many. Returns ((a, b), stored) with a != b and f(a) == f(b), and the number
    of distinguished points stored.
    """
    mask = (1 << dp_bits) - 1
    limit = 20 << dp_bits  # drop walks that seem to loop with no distinguished point
    table: dict[int, tuple[int, int]] = {}
    for _ in range(max_walks):
        start = rng.randrange(n_values)
        x, steps = start, 0
        while x & mask and steps < limit:
            x = f(x)
            steps += 1
        if x & mask:
            continue
        if x in table and table[x][0] != start:
            res = _locate(f, table[x], (start, steps))
            if res is not None:
                return res, len(table)
        table[x] = (start, steps)
    raise RuntimeError("no collision found")


def _locate(f: Func, w1: tuple[int, int], w2: tuple[int, int]) -> Optional[tuple[int, int]]:
    """Two walks reach the same distinguished point: step them to the merge point."""
    (a, la), (b, lb) = w1, w2
    while la > lb:
        a, la = f(a), la - 1
    while lb > la:
        b, lb = f(b), lb - 1
    if a == b:
        return None  # one start point lies on the other trail
    fa, fb = f(a), f(b)
    while fa != fb:
        a, b = fa, fb
        fa, fb = f(a), f(b)
    return a, b
