# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-radix-sort/. The authors are listed in prov/GHWWJ6.jsonl.

"""Parallel LSD radix sort with p blocks, simulated one block at a time.

Each pass counts digits per block, takes one prefix sum over the count
table in digit-major, block-minor order, and lets every block scatter
its keys to their final places. The blocks touch disjoint cells, so
running them one after the other gives the same result as running them
at the same time.
"""


def block_bounds(n: int, p: int, j: int) -> tuple[int, int]:
    """The index range of block j when n keys are cut into p blocks."""
    return j * n // p, (j + 1) * n // p


def digit(x: int, t: int, radix: int) -> int:
    """Digit t of x in base radix, with digit 0 the least significant."""
    return (x // radix**t) % radix


def radix_pass(a: list[int], t: int, radix: int, p: int) -> list[int]:
    """One stable counting-sort pass on digit t, with p blocks."""
    n = len(a)
    counts = [[0] * p for _ in range(radix)]
    for j in range(p):  # @line L2
        lo, hi = block_bounds(n, p, j)
        for i in range(lo, hi):  # @line L3
            counts[digit(a[i], t, radix)][j] += 1
    offset = [[0] * p for _ in range(radix)]
    total = 0
    for d in range(radix):  # @line L4
        for j in range(p):
            offset[d][j] = total
            total += counts[d][j]
    out = [0] * n
    for j in range(p):  # @line L5
        lo, hi = block_bounds(n, p, j)
        for i in range(lo, hi):  # @line L6
            d = digit(a[i], t, radix)  # @line L7
            out[offset[d][j]] = a[i]
            offset[d][j] += 1
    return out  # @line L8


def parallel_radix_sort(a: list[int], radix: int = 256, p: int = 4) -> list[int]:
    """Return the non-negative integers of a in sorted order."""
    if any(x < 0 for x in a):
        raise ValueError("keys must be non-negative")
    if radix < 2 or p < 1:
        raise ValueError("need radix >= 2 and p >= 1")
    passes = 1
    while a and radix**passes <= max(a):
        passes += 1
    out = list(a)
    for t in range(passes):  # @line L1
        out = radix_pass(out, t, radix, p)
    return out


def split_radix_sort(a: list[int], bits: int) -> list[int]:
    """Blelloch's split radix sort: one stable split by each bit, low bit first."""
    out = list(a)
    for t in range(bits):
        flags = [(x >> t) & 1 for x in out]
        zeros = len(out) - sum(flags)
        ones_before, pos = 0, [0] * len(out)
        for i, f in enumerate(flags):  # a prefix sum of the flags
            pos[i] = zeros + ones_before if f else i - ones_before
            ones_before += f
        nxt = [0] * len(out)
        for i, x in enumerate(out):
            nxt[pos[i]] = x
        out = nxt
    return out
