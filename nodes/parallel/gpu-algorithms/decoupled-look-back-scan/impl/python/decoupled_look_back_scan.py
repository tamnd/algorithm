# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decoupled-look-back-scan/. The authors are listed in prov/T9HRJ5.jsonl.
"""Decoupled look-back scan (Merrill and Garland 2016) on a small simulator.

The simulator models what the protocol depends on: global memory, a fixed
number of resident thread blocks (slots), a hardware dispatcher that starts
blocks in any order, and an interleaving of the resident blocks that a seeded
random generator picks.  Each block is a Python generator.  It yields after
each step that touches global memory, so the scheduler can switch blocks
there.  The work inside one tile (the load, the reduce, the local scan) runs
in parallel on a GPU; here it is one step, and the code counts its global
reads and writes.

The CUDA kernel on the page is not run by these tests.
"""

from functools import reduce

X, A, P = "X", "A", "P"
WAIT, STEP = "wait", "step"


class Deadlock(Exception):
    """Every resident block polls a descriptor that no running block can change."""


class Machine:
    """Global memory, the cost counters, and the descriptor array."""

    def __init__(self, data, tile, op):
        self.inp = list(data)
        self.n = len(self.inp)
        self.tile = tile
        self.op = op
        self.tiles = (self.n + tile - 1) // tile
        self.out = [None] * self.n
        self.desc = [(X, None)] * self.tiles
        self.counter = 0
        self.item_reads = 0
        self.item_writes = 0
        self.desc_writes = 0
        self.desc_reads = 0
        self.polls = 0
        self.atomics = 0
        self.lookback = {}


def _block(m, block_idx, mode, dynamic, window):
    """The program of one thread block. It yields WAIT on a failed poll and STEP otherwise."""
    op = m.op
    if dynamic:
        g = m.counter  # @line L1: atomicAdd(&tile_counter, 1)
        m.counter += 1
        m.atomics += 1
        yield STEP
    else:
        g = block_idx  # the tile is blockIdx.x: unsafe
    lo, hi = g * m.tile, min(m.n, (g + 1) * m.tile)
    vals = m.inp[lo:hi]  # @line L2: the only read of the input
    m.item_reads += hi - lo
    yield STEP
    agg = reduce(op, vals)  # @line L3
    excl = None
    looked = 0
    if g == 0:  # @line L4
        m.desc[0] = (P, agg)  # @line L5
        m.desc_writes += 1
        yield STEP
    else:  # @line L6
        if mode == "decoupled":
            m.desc[g] = (A, agg)  # @line L7: flag and value in one word
            m.desc_writes += 1
            yield STEP
        j = g - 1  # @line L8
        while True:  # @line L9
            if mode == "chained":
                flag, val = m.desc[j]
                if flag != P:
                    m.polls += 1
                    yield WAIT
                    continue
                m.desc_reads += 1
                looked += 1
                excl = val
                break
            # Decoupled look-back over a window of up to `window` predecessors.
            span = [m.desc[k] for k in range(j, max(j - window, -1), -1)]  # @line L10
            stop = next((t for t, (f, _) in enumerate(span) if f != A), None)
            if stop is not None and span[stop][0] == X:  # @line L11
                m.polls += 1
                yield WAIT
                continue
            used = span if stop is None else span[: stop + 1]
            for _, val in used:
                excl = val if excl is None else op(val, excl)  # @line L12: val comes first
            m.desc_reads += len(used)
            looked += len(used)
            if stop is not None:  # @line L13: reached a P
                break
            j -= len(used)  # @line L14
            yield STEP
        m.desc[g] = (P, op(excl, agg))  # @line L15
        m.desc_writes += 1
        yield STEP
    run = excl
    for i, v in zip(range(lo, hi), vals):
        run = v if run is None else op(run, v)
        m.out[i] = run  # @line L16
    m.item_writes += hi - lo
    m.lookback[g] = looked


def simulate(data, tile, slots, rng, op=lambda a, b: a + b, mode="decoupled", dynamic=True, window=1):
    """Run the single-pass scan and return the machine with the inclusive scan in m.out.

    tile is the number of items of a tile, slots the number of blocks that can be
    resident at once, rng a random.Random that picks the dispatch order and the
    interleaving. mode is "decoupled" or "chained". With dynamic=False the tile
    index is the block index, which can deadlock; the run then raises Deadlock.
    """
    m = Machine(data, tile, op)
    pending = list(range(m.tiles))
    rng.shuffle(pending)  # the hardware may dispatch blocks in any order
    running = []
    stuck = set()
    while pending or running:
        while pending and len(running) < slots:
            b = pending.pop()
            running.append((b, _block(m, b, mode, dynamic, window)))
            stuck.clear()
        k = rng.randrange(len(running))
        b, prog = running[k]
        try:
            r = next(prog)
        except StopIteration:
            running.pop(k)
            stuck.clear()
            continue
        if r == WAIT:
            stuck.add(b)
            if len(stuck) == len(running):
                raise Deadlock(sorted(stuck))
        else:
            stuck.clear()
    return m


def reduce_then_scan(data, tile, op=lambda a, b: a + b):
    """Three passes: reduce each tile, scan the tile sums, scan each tile again.

    Returns (output, reads, writes) with the global reads and writes of items
    and tile sums.
    """
    n = len(data)
    tiles = (n + tile - 1) // tile
    reads = writes = 0
    sums = []
    for g in range(tiles):  # pass 1, one block per tile
        part = data[g * tile:(g + 1) * tile]
        reads += len(part)
        sums.append(reduce(op, part))
        writes += 1
    reads += tiles  # pass 2, one block
    pref = []
    for s in sums:
        pref.append(s if not pref else op(pref[-1], s))
    writes += tiles
    out = []
    for g in range(tiles):  # pass 3, one block per tile
        part = data[g * tile:(g + 1) * tile]
        reads += len(part) + (1 if g else 0)
        run = pref[g - 1] if g else None
        for v in part:
            run = v if run is None else op(run, v)
            out.append(run)
        writes += len(part)
    return out, reads, writes
