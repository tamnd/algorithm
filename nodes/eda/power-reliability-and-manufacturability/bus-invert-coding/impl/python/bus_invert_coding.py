# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bus-invert-coding/. The authors are listed in prov/7HE5BF.jsonl.
"""Bus-invert coding (Stan and Burleson 1995).

An n-bit bus gets one extra line, INV. Before each transfer the encoder counts
H, the number of the n + 1 lines that would toggle if the word D went out as it
is with INV = 0. If H > n / 2 it sends the complement of D with INV = 1, which
toggles n + 1 - H lines. The receiver XORs the bus with INV.

Words are Python ints in [0, 2^n).
"""

from __future__ import annotations

from typing import Iterable, List, Tuple


def popcount(v: int) -> int:
    return bin(v).count("1")


def encode(words: Iterable[int], n: int, bus: int = 0, inv: int = 0) -> List[Tuple[int, int]]:
    """The sequence of (bus value, INV) for the words, from the state (bus, inv)."""
    mask = (1 << n) - 1
    out = []  # @line L1: the state (bus, inv) is (0, 0) unless the caller gives one
    for d in words:  # @line L2
        h = popcount(bus ^ d) + inv  # @line L3: toggles of (d, 0) against (bus, inv)
        if 2 * h > n:  # @line L4
            bus, inv = d ^ mask, 1
        else:  # @line L5
            bus, inv = d, 0
        out.append((bus, inv))  # @line L6
    return out


def decode(bus: int, inv: int, n: int) -> int:
    """The data word: the bus, inverted when INV = 1."""
    return bus ^ (((1 << n) - 1) if inv else 0)  # @line L7


def toggles(states: List[Tuple[int, int]], start: Tuple[int, int] = (0, 0)) -> List[int]:
    """Toggles on all n + 1 lines for each transfer."""
    out, prev = [], start
    for s in states:
        out.append(popcount(prev[0] ^ s[0]) + (prev[1] ^ s[1]))
        prev = s
    return out


def encode_data_only(words: Iterable[int], n: int, bus: int = 0, inv: int = 0) -> List[Tuple[int, int]]:
    """A flawed variant that counts only the n data lines when it decides."""
    mask = (1 << n) - 1
    out = []
    for d in words:
        if 2 * popcount(bus ^ d) > n:
            bus, inv = d ^ mask, 1
        else:
            bus, inv = d, 0
        out.append((bus, inv))
    return out
