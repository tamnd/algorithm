# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lfsr-reseeding/. The authors are listed in prov/NQ6987.jsonl.
"""LFSR reseeding: find a seed whose LFSR output matches a test cube.

The LFSR has n stages and a tap set T, a subset of {1, ..., n}. Its output
stream a_0, a_1, ... starts with the n seed bits, a_t = s_t for t < n, and then
follows the recurrence

    a_t = XOR of a_(t-i) over i in T        (t >= n).

A test cube is a string over '0', '1' and 'X', written in the order in which
its bits leave the LFSR (bit t of the cube is a_t). A seed encodes the cube
when a_t equals the cube at every position that is not 'X'.

Every a_t is a fixed XOR of seed bits, so each care bit gives one linear
equation over GF(2) in the n seed bits. The cube is encodable exactly when
this system is consistent. reseed solves it by Gaussian elimination in
O(L |T| + c n) operations on n-bit words, for a cube of length L with c care
bits.
"""

from __future__ import annotations

from typing import Iterable, Optional


def _check(n: int, taps: Iterable[int]) -> list[int]:
    taps = sorted(set(taps))
    if n < 1 or not taps or taps[0] < 1 or taps[-1] > n:
        raise ValueError("taps must be a nonempty subset of 1..n")
    return taps


def output_forms(n: int, taps: Iterable[int], length: int) -> list[int]:
    """Bit mask over the seed bits of every output a_0 .. a_(length-1). O(length |T|)."""
    taps = _check(n, taps)
    forms: list[int] = []
    for t in range(length):
        if t < n:
            forms.append(1 << t)
        else:
            f = 0
            for i in taps:
                f ^= forms[t - i]
            forms.append(f)
    return forms


def expand(n: int, taps: Iterable[int], seed: int, length: int) -> str:
    """Run the LFSR from a seed and return the first `length` output bits, as a '0'/'1' string."""
    taps = _check(n, taps)
    if not 0 <= seed < 1 << n:
        raise ValueError("the seed must have n bits")
    a: list[int] = []
    for t in range(length):
        if t < n:
            a.append((seed >> t) & 1)
        else:
            v = 0
            for i in taps:
                v ^= a[t - i]
            a.append(v)
    return "".join(map(str, a))


def reseed(n: int, taps: Iterable[int], cube: str) -> Optional[int]:
    """A seed (bit t is s_t) whose output matches the cube, or None when no seed does.

    Precondition: the cube is a string over '0', '1', 'X'. Free seed bits are set to 0.
    Cost: O(L |T|) to build the forms and O(c n) word operations to eliminate.
    """
    if set(cube) - set("01X"):
        raise ValueError("the cube must be over 0, 1, X")
    forms = output_forms(n, taps, len(cube))  # @line L1
    pivots: dict[int, tuple[int, int]] = {}  # leading bit -> (mask, value)
    for t, ch in enumerate(cube):  # @line L2
        if ch == "X":
            continue
        mask, val = forms[t], int(ch)
        while mask:  # @line L3
            lead = mask.bit_length() - 1
            if lead not in pivots:
                break
            pm, pv = pivots[lead]
            mask, val = mask ^ pm, val ^ pv
        if mask == 0 and val == 1:  # @line L4
            return None
        if mask:  # @line L5
            pivots[mask.bit_length() - 1] = (mask, val)
    seed = 0  # @line L6
    for lead in sorted(pivots):  # @line L7
        mask, val = pivots[lead]
        rest = mask ^ (1 << lead)
        bit = val ^ (bin(rest & seed).count("1") & 1)
        seed |= bit << lead
    return seed  # @line L8


def rank_of_cube(n: int, taps: Iterable[int], cube: str) -> int:
    """Rank over GF(2) of the care-bit rows of a cube (values ignored)."""
    forms = output_forms(n, taps, len(cube))
    basis: dict[int, int] = {}
    for t, ch in enumerate(cube):
        if ch == "X":
            continue
        m = forms[t]
        while m and (m.bit_length() - 1) in basis:
            m ^= basis[m.bit_length() - 1]
        if m:
            basis[m.bit_length() - 1] = m
    return len(basis)
