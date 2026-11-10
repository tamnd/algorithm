# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/warp-specialization/. The authors are listed in prov/G81808.jsonl.
"""A model of warp specialization: producer warps load tiles, consumer warps compute.

The producer and the consumers share a ring of k buffers in shared memory.
Tile t goes to buffer t mod k.  The producer may load tile t only when the
consumers have released tile t - k; the consumers may compute tile t only when
it is loaded.  load[t] and comp[t] are the times of each step.  Times are exact
Fractions.  No CUDA code is run.
"""
from fractions import Fraction as F


def specialized(load, comp, k):
    """Start and end times of loads and computes with a ring of k >= 1 buffers."""
    T = len(load)
    ls, le, cs, ce = [], [], [], []
    for t in range(T):                                       # @line L1: the producer's loop over tiles
        s = le[t - 1] if t else F(0)
        if t >= k:
            s = max(s, ce[t - k])                            # @line L2: wait until buffer t mod k is EMPTY
        ls.append(s)
        le.append(s + F(load[t]))                            # @line L3: load tile t, then arrive on FULL
        # the consumers' iteration for the same tile t         @line L4
        c = le[t] if not t else max(le[t], ce[t - 1])        # @line L5: wait until the buffer is FULL
        cs.append(c)
        ce.append(c + F(comp[t]))                            # @line L6: compute, then arrive on EMPTY
    return ls, le, cs, ce


def specialized_time(load, comp, k):
    return specialized(load, comp, k)[3][-1] if load else F(0)


def unspecialized_time(load, comp):
    """The same warps load and then compute each tile, with no overlap inside the block."""
    return sum((F(a) + F(b) for a, b in zip(load, comp)), F(0))


def uniform_time(T, L, C, k):
    """Closed form for T equal tiles: with k >= 2 buffers, fill, T - 1 bottleneck steps, drain."""
    L, C = F(L), F(C)
    if T == 0:
        return F(0)
    if k == 1:
        return T * (L + C)
    return L + C + (T - 1) * max(L, C)


def register_split(regfile, producer_threads, consumer_threads, producer_regs):
    """Registers per consumer thread when producers keep only producer_regs each."""
    return (regfile - producer_threads * producer_regs) // consumer_threads
