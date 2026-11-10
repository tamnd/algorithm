# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyperloglog-plus-plus/. The authors are listed in prov/417CHM.jsonl.
"""HyperLogLog++ (Heule, Nunkesser and Hall 2013), after Figures 6 and 7 of the paper.

Simplifications against the paper: the sparse list is a dict from the
25-bit index to the largest rho seen, its size is counted as 32 bits per
entry (no variable length or difference encoding), and there is no
temporary insertion buffer. The bias table and the threshold are inputs.
"""

import math
from typing import Callable, Hashable, Iterable, Optional, Sequence

HASH_BITS = 64
P_SPARSE = 25  # p' of the paper
SPARSE_ENTRY_BITS = 32
REGISTER_BITS = 6


def alpha(m: int) -> float:
    if m == 16:
        return 0.673
    if m == 32:
        return 0.697
    if m == 64:
        return 0.709
    return 0.7213 / (1.0 + 1.079 / m)


def rho_left(w: int, width: int) -> int:
    """Position of the leftmost 1 in the width-bit string w, counted from 1 (width + 1 if w == 0)."""
    return width - w.bit_length() + 1


def linear_counting(m: int, v: int) -> float:
    return m * math.log(m / v)


def dense_update_of(y: int, p: int) -> tuple[int, int]:
    """Register index and rho value of a 64-bit hash y at precision p."""
    width = HASH_BITS - p
    return y >> width, rho_left(y & ((1 << width) - 1), width)


def sparse_update_of(y: int) -> tuple[int, int]:
    """The sparse pair (idx', rho(w')) of a 64-bit hash y at precision p' = 25."""
    width = HASH_BITS - P_SPARSE
    return y >> width, rho_left(y & ((1 << width) - 1), width)


def sparse_to_dense(idx_s: int, rho_s: int, p: int) -> tuple[int, int]:
    """Decode a sparse pair into the (idx, rho) that the dense update of the same hash would give."""
    shift = P_SPARSE - p
    low = idx_s & ((1 << shift) - 1)
    if low != 0:
        return idx_s >> shift, shift - low.bit_length() + 1
    return idx_s >> shift, shift + rho_s


class BiasTable:
    """Pairs (raw estimate, bias) for one precision; the bias at E is the mean over the k nearest raw estimates."""

    def __init__(self, raw: Sequence[float], bias: Sequence[float], k: int = 6) -> None:
        if len(raw) != len(bias) or len(raw) < k:
            raise ValueError("need at least k points")
        self.points = sorted(zip(raw, bias))
        self.k = k

    def __call__(self, e: float) -> float:
        nearest = sorted(self.points, key=lambda pb: abs(pb[0] - e))[: self.k]
        return sum(b for _, b in nearest) / self.k


class HyperLogLogPlusPlus:
    """HLL with a 64-bit hash, empirical bias correction and a sparse mode.

    h maps an item to a 64-bit integer. In dense mode the state is m = 2^p
    registers of 6 bits; in sparse mode it is the sparse map, kept while it
    costs at most 6m bits. An update costs one hash and O(1) expected
    time; a query costs O(m) in dense mode and O(1) in sparse mode.
    """

    def __init__(self, p: int, h: Callable[[Hashable], int], bias: Optional[BiasTable] = None, threshold: Optional[float] = None) -> None:
        if not 4 <= p <= 18:
            raise ValueError("p must be in 4 .. 18")
        self.p = p
        self.m = 1 << p
        self.h = h
        self.bias = bias
        # The paper's threshold for p = 14 is 11500; other values come from its online appendix.
        self.threshold = threshold if threshold is not None else (11500.0 if p == 14 else 11500.0 * self.m / (1 << 14))
        self.sparse: Optional[dict[int, int]] = {}  # @line L1
        self.registers: Optional[list[int]] = None

    def is_sparse(self) -> bool:
        return self.sparse is not None

    def add(self, x: Hashable) -> None:
        y = self.h(x)  # @line L3
        if self.sparse is not None:
            i, r = sparse_update_of(y)  # @line L4
            if r > self.sparse.get(i, 0):
                self.sparse[i] = r
            if SPARSE_ENTRY_BITS * len(self.sparse) > REGISTER_BITS * self.m:  # @line L5
                self.to_dense()
        else:
            j, r = dense_update_of(y, self.p)  # @line L6
            if r > self.registers[j]:
                self.registers[j] = r

    def add_all(self, stream: Iterable[Hashable]) -> None:
        for x in stream:  # @line L2
            self.add(x)

    def to_dense(self) -> None:
        if self.sparse is None:
            return
        regs = [0] * self.m
        for i, r in self.sparse.items():
            j, rr = sparse_to_dense(i, r, self.p)
            if rr > regs[j]:
                regs[j] = rr
        self.registers = regs
        self.sparse = None

    def dense_registers(self) -> list[int]:
        """The registers that a dense sketch of the same stream would hold."""
        if self.sparse is None:
            return list(self.registers)
        copy = HyperLogLogPlusPlus(self.p, self.h, self.bias, self.threshold)
        copy.sparse = dict(self.sparse)
        copy.to_dense()
        return copy.registers

    def raw_estimate(self) -> float:
        regs = self.dense_registers()
        return alpha(self.m) * self.m * self.m / sum(2.0 ** (-r) for r in regs)

    def estimate(self) -> float:
        if self.sparse is not None:
            m_s = 1 << P_SPARSE
            return linear_counting(m_s, m_s - len(self.sparse))  # @line L7
        e = self.raw_estimate()
        e_corr = e - self.bias(e) if (self.bias is not None and e <= 5 * self.m) else e  # @line L8
        v = self.registers.count(0)
        hh = linear_counting(self.m, v) if v != 0 else e_corr  # @line L9
        return hh if hh <= self.threshold else e_corr  # @line L10

    def merge(self, other: "HyperLogLogPlusPlus") -> "HyperLogLogPlusPlus":
        """The sketch of the union (same p and the same hash)."""
        if other.p != self.p or other.h is not self.h:
            raise ValueError("sketches are not compatible")
        out = HyperLogLogPlusPlus(self.p, self.h, self.bias, self.threshold)
        if self.sparse is not None and other.sparse is not None:
            merged = dict(self.sparse)
            for i, r in other.sparse.items():
                if r > merged.get(i, 0):
                    merged[i] = r
            out.sparse = merged
            if SPARSE_ENTRY_BITS * len(merged) > REGISTER_BITS * self.m:
                out.to_dense()
            return out
        out.sparse = None
        out.registers = [max(a, b) for a, b in zip(self.dense_registers(), other.dense_registers())]
        return out
