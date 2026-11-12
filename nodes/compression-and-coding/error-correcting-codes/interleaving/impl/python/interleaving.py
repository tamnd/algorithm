# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interleaving/. The authors are listed in prov/E58STP.jsonl.
"""Interleaving: block interleavers (write rows, read columns) and convolutional interleavers
(I branches with delays 0, J, 2J, ... symbols times I), with their deinterleavers, and the
template that wraps a code with an interleaver.
"""

from collections import deque
from typing import Callable, Hashable, List, Sequence


# ---- block interleaver -------------------------------------------------------

def block_position(r: int, c: int, depth: int) -> int:
    """Channel position of symbol c of codeword r when the I x n array is read by columns."""
    return c * depth + r


def block_interleave(codewords: Sequence[Sequence[Hashable]]) -> List[Hashable]:
    """Write the I codewords as the rows of an array and read it out column by column."""
    depth, n = len(codewords), len(codewords[0])
    out = [None] * (depth * n)
    for r, word in enumerate(codewords):
        if len(word) != n:
            raise ValueError("all codewords must have the same length")
        for c, s in enumerate(word):
            out[block_position(r, c, depth)] = s
    return out


def block_deinterleave(stream: Sequence[Hashable], depth: int) -> List[List[Hashable]]:
    """Inverse of block_interleave: write by columns, read the rows."""
    if len(stream) % depth:
        raise ValueError("the stream length must be a multiple of the depth")
    n = len(stream) // depth
    return [[stream[block_position(r, c, depth)] for c in range(n)] for r in range(depth)]


# ---- the template ------------------------------------------------------------

def interleaved_link(messages: Sequence, encode: Callable, decode: Callable,
                     channel: Callable[[List], List]) -> List:
    """Encode I messages, interleave the I codewords, send them, deinterleave and decode.

    The holes are ENCODE and DECODE (a code that corrects t errors, or bursts of length b)
    and the interleaver, here a block interleaver of depth I = len(messages).
    """
    depth = len(messages)
    words = []
    for j in range(depth):                     # @line L1
        words.append(list(encode(messages[j])))  # @line L2
    x = block_interleave(words)               # @line L3
    y = channel(x)                            # @line L4
    rows = block_deinterleave(y, depth)       # @line L5
    out = []
    for j in range(depth):                     # @line L6
        out.append(decode(rows[j]))           # @line L7
    return out                                # @line L8


# ---- convolutional interleaver ------------------------------------------------

class ConvolutionalInterleaver:
    """I branches; branch i is a FIFO of i * J cells (branch 0 has no delay).

    A commutator sends input symbol u to branch u mod I and takes the channel symbol from the
    same branch. So symbol u leaves at channel time u + I J (u mod I).
    """

    def __init__(self, branches: int, unit: int, fill: Hashable = None) -> None:
        self.branches = branches
        self.lines = [deque([fill] * (i * unit)) for i in range(branches)]
        self.turn = 0

    def push(self, symbol: Hashable) -> Hashable:
        line = self.lines[self.turn]
        self.turn = (self.turn + 1) % self.branches
        if not line:
            return symbol
        line.append(symbol)
        return line.popleft()

    def run(self, symbols: Sequence[Hashable]) -> List[Hashable]:
        return [self.push(s) for s in symbols]


class ConvolutionalDeinterleaver(ConvolutionalInterleaver):
    """Branch i has (I - 1 - i) J cells, so every symbol is delayed by (I - 1) J commutator
    turns in total: the output is the input stream delayed by I (I - 1) J symbols."""

    def __init__(self, branches: int, unit: int, fill: Hashable = None) -> None:
        super().__init__(branches, unit, fill)
        self.lines = [deque([fill] * ((branches - 1 - i) * unit)) for i in range(branches)]


def convolutional_position(u: int, branches: int, unit: int) -> int:
    """Channel time of input symbol u in the convolutional interleaver."""
    return u + branches * unit * (u % branches)


def convolutional_memory(branches: int, unit: int) -> int:
    """Cells on one side: J (0 + 1 + ... + (I - 1)) = J I (I - 1) / 2."""
    return unit * branches * (branches - 1) // 2


def convolutional_delay(branches: int, unit: int) -> int:
    """End-to-end delay of interleaver plus deinterleaver, in symbols: I (I - 1) J."""
    return branches * (branches - 1) * unit


# ---- measuring the spread ---------------------------------------------------------

def max_hits_per_codeword(positions: Sequence[int], n: int, length: int, offset: int = 0) -> int:
    """Largest number of symbols of one codeword in any window of `length` channel positions.

    positions[u] is the channel position of input symbol u; codeword k holds the input symbols
    u with (u - offset) // n == k.
    """
    where = {q: u for u, q in enumerate(positions)}
    lo, hi = min(where), max(where)
    worst = 0
    for start in range(lo, hi - length + 2):
        count = {}
        for q in range(start, start + length):
            u = where.get(q)
            if u is not None:
                k = (u - offset) // n
                count[k] = count.get(k, 0) + 1
        if count:
            worst = max(worst, max(count.values()))
    return worst


# ---- a small code for the end-to-end tests ----------------------------------------

_H_COLS = [0b011, 0b101, 0b110, 0b111, 0b001, 0b010, 0b100]  # parity-check columns of Hamming [7, 4]


def hamming74_encode(m: Sequence[int]) -> List[int]:
    d1, d2, d3, d4 = m
    return [d1, d2, d3, d4, d1 ^ d2 ^ d4, d1 ^ d3 ^ d4, d2 ^ d3 ^ d4]


def hamming74_decode(r: Sequence[int]) -> List[int]:
    s = 0
    for bit, col in zip(r, _H_COLS):
        if bit:
            s ^= col
    r = list(r)
    if s:
        r[_H_COLS.index(s)] ^= 1
    return r[:4]
