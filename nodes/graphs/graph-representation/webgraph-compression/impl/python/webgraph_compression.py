# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/webgraph-compression/. The authors are listed in prov/763NVN.jsonl.

"""A simplified Boldi-Vigna (WebGraph) compressor for adjacency lists.

Each list is coded with a reference to one of the previous `window` lists,
copy blocks, intervals of consecutive successors, and gap-coded residuals.
Every integer is written with the Elias gamma code (WebGraph itself uses
zeta codes for residuals). The output is a string of '0' and '1'.
"""

from typing import Sequence


def gamma(k: int) -> str:
    """Elias gamma code of k + 1, for k >= 0."""
    b = bin(k + 1)[2:]
    return "0" * (len(b) - 1) + b


def nu(x: int) -> int:
    """Map an integer to a natural number: 0, -1, 1, -2, ... to 0, 1, 2, 3, ..."""
    return 2 * x if x >= 0 else -2 * x - 1


def nu_inv(k: int) -> int:
    return k // 2 if k % 2 == 0 else -(k + 1) // 2


class Reader:
    def __init__(self, bits: str) -> None:
        self.bits, self.pos = bits, 0

    def gamma(self) -> int:
        z = 0
        while self.bits[self.pos] == "0":
            z += 1
            self.pos += 1
        v = int(self.bits[self.pos:self.pos + z + 1], 2)
        self.pos += z + 1
        return v - 1


def copy_blocks(ref: Sequence[int], succ: set[int]) -> list[int]:
    """Run lengths of the copy mask of ref, starting with a copy run (which
    may be empty), without the last run, which the decoder infers."""
    runs, cur, length = [], 1, 0
    for y in ref:
        bit = 1 if y in succ else 0
        if bit == cur:
            length += 1
        else:
            runs.append(length)
            cur, length = bit, 1
    return runs


def split_intervals(extra: Sequence[int], lmin: int) -> tuple[list[tuple[int, int]], list[int]]:
    """Maximal runs of consecutive integers of length >= lmin, and the rest."""
    intervals, residuals, i = [], [], 0
    while i < len(extra):
        j = i
        while j + 1 < len(extra) and extra[j + 1] == extra[j] + 1:
            j += 1
        if j - i + 1 >= lmin:
            intervals.append((extra[i], j - i + 1))
        else:
            residuals.extend(extra[i:j + 1])
        i = j + 1
    return intervals, residuals


def encode(adj: Sequence[Sequence[int]], window: int = 7, lmin: int = 3) -> str:
    """Compress the sorted, duplicate-free successor lists adj[0..n-1].

    Time O(n * window * d) for maximum degree d, with set lookups.
    """
    out = [gamma(len(adj))]
    for x, lst in enumerate(adj):
        succ = set(lst)
        out.append(gamma(len(lst)))  # @line L1
        if not lst:
            continue
        best, gain = 0, 0
        for r in range(1, min(window, x) + 1):  # @line L2
            g = sum(1 for y in adj[x - r] if y in succ)
            if g > gain:
                best, gain = r, g  # @line L3
        out.append(gamma(best))  # @line L4
        copied: set[int] = set()
        if best:
            ref = adj[x - best]
            runs = copy_blocks(ref, succ)  # @line L5
            out.append(gamma(len(runs)))
            out.extend(gamma(b if i == 0 else b - 1) for i, b in enumerate(runs))
            copied = succ & set(ref)
        extra = [y for y in lst if y not in copied]  # @line L6
        intervals, residuals = split_intervals(extra, lmin)  # @line L7
        out.append(gamma(len(intervals)))  # @line L8
        prev_end = None
        for left, length in intervals:
            out.append(gamma(nu(left - x)) if prev_end is None else gamma(left - prev_end - 1))
            out.append(gamma(length - lmin))
            prev_end = left + length
        prev = None
        for y in residuals:  # @line L9
            out.append(gamma(nu(y - x)) if prev is None else gamma(y - prev - 1))  # @line L10
            prev = y
    return "".join(out)  # @line L11


def decode(bits: str, lmin: int = 3) -> list[list[int]]:
    """Invert encode (the window is not needed to decode)."""
    rd = Reader(bits)
    n = rd.gamma()
    adj: list[list[int]] = []
    for x in range(n):
        d = rd.gamma()
        if d == 0:
            adj.append([])
            continue
        r = rd.gamma()
        copied: list[int] = []
        if r:
            ref = adj[x - r]
            b = rd.gamma()
            runs = [rd.gamma() + (1 if i else 0) for i in range(b)]
            i, cur = 0, 1
            for length in runs:
                if cur:
                    copied.extend(ref[i:i + length])
                i += length
                cur ^= 1
            if cur:
                copied.extend(ref[i:])
        extra: list[int] = []
        prev_end = None
        for _ in range(rd.gamma()):
            left = x + nu_inv(rd.gamma()) if prev_end is None else prev_end + 1 + rd.gamma()
            length = rd.gamma() + lmin
            extra.extend(range(left, left + length))
            prev_end = left + length
        prev = None
        for _ in range(d - len(copied) - len(extra)):
            y = x + nu_inv(rd.gamma()) if prev is None else prev + 1 + rd.gamma()
            extra.append(y)
            prev = y
        adj.append(sorted(copied + extra))
    return adj
