# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simt-model/.
"""A small SIMT simulator that counts warp instructions.

A kernel is a Python function kernel(t, *args) of one thread t. Each `yield` in the kernel is a
__syncthreads() barrier. The threads of one block run one after another up to the next barrier, so
the code between two barriers is one phase. Each thread records events: named instructions
(t.op) and memory accesses (t.ld, t.st, t.lds, t.sts). Events of the lanes of one warp that carry
the same label are one warp instruction, issued once with a mask of the lanes that ran it.
The simulator shows the algorithm and counts its costs. It does not model timing.
"""

from itertools import product

WARP_SIZE = 32


class Thread:
    """One thread of a launch: its indices, the memories it can reach, and its events."""

    def __init__(self, block_idx, thread_idx, block_dim, grid_dim, shared, glob):
        self.blockIdx, self.threadIdx = block_idx, thread_idx
        self.blockDim, self.gridDim = block_dim, grid_dim
        x, y, z = thread_idx
        self.tid = x + y * block_dim[0] + z * block_dim[0] * block_dim[1]
        self.lane, self.warp = self.tid % WARP_SIZE, self.tid // WARP_SIZE
        self.shared, self.glob = shared, glob
        self.events, self.nmem = [], 0

    def _mem(self, kind, space, index, label):
        if label is None:
            label = ("mem", self.nmem)
        self.nmem += 1
        self.events.append((label, kind, space, index))

    def op(self, label):
        """One instruction that is not a memory access. Equal labels in one warp are one instruction."""
        self.events.append((label, "op", None, None))

    def ld(self, name, i, label=None):
        self._mem("ld", name, i, label)
        return self.glob[name][i]

    def st(self, name, i, value, label=None):
        self._mem("st", name, i, label)
        self.glob[name][i] = value

    def lds(self, i, label=None):
        self._mem("ld", "shared", i, label)
        return self.shared[i]

    def sts(self, i, value, label=None):
        self._mem("st", "shared", i, label)
        self.shared[i] = value


def _group(threads, block_idx, phase):
    by_warp = {}
    for t in threads:
        for label, kind, space, index in t.events:
            groups = by_warp.setdefault(t.warp, {})
            groups.setdefault(label, []).append((t.lane, kind, space, index))
        t.events, t.nmem = [], 0
    return [{"block": block_idx, "phase": phase, "warp": w, "groups": g} for w, g in sorted(by_warp.items())]


def launch(kernel, grid, block, glob, shared_words=0, args=()):
    """Run kernel(t, *args) on every thread. grid and block are (x, y, z) triples.

    Returns a list of records, one for each (block, phase, warp) that did something. A record maps
    each instruction label to the list of (lane, kind, space, index) of the lanes that ran it.
    """
    records = []
    for bz, by, bx in product(range(grid[2]), range(grid[1]), range(grid[0])):
        shared = [0] * shared_words
        threads = [Thread((bx, by, bz), (x, y, z), block, grid, shared, glob)
                   for z in range(block[2]) for y in range(block[1]) for x in range(block[0])]
        pending = []
        for t in threads:
            g = kernel(t, *args)
            if hasattr(g, "__next__"):
                pending.append((t, g))
        phase = 0
        while True:
            waiting = []
            for t, g in pending:  # every thread that has not exited runs to its next barrier
                try:
                    next(g)
                    waiting.append((t, g))
                except StopIteration:
                    pass
            records.extend(_group(threads, (bx, by, bz), phase))
            if not waiting:
                break
            pending, phase = waiting, phase + 1
    return records


# ---------------------------------------------------------------- costs of the SIMT model


def warp_cost(records):
    """(warp instructions issued, lane instructions executed). One issue serves up to 32 lanes."""
    issued = sum(len(r["groups"]) for r in records)
    lanes = sum(len(v) for r in records for v in r["groups"].values())
    return issued, lanes


# ---------------------------------------------------------------- example kernels


def vec_add_kernel(t, n):
    """c[i] = a[i] + b[i] with the usual bounds guard."""
    i = t.blockIdx[0] * t.blockDim[0] + t.threadIdx[0]
    t.op("index")
    t.op("compare")
    if i < n:
        a = t.ld("a", i)
        b = t.ld("b", i)
        t.op("add")
        t.st("c", i, a + b)


def vec_add(a, b, block=128):
    n = len(a)
    glob = {"a": list(a), "b": list(b), "c": [0] * n}
    grid = ((n + block - 1) // block, 1, 1)
    records = launch(vec_add_kernel, grid, (block, 1, 1), glob, args=(n,))
    return glob["c"], records


def reverse_kernel(t, n, sync):
    """One block reverses x[0 .. n-1] into y through shared memory."""
    i = t.tid
    t.sts(i, t.ld("x", i))
    if sync:
        yield  # __syncthreads()
    t.st("y", i, t.lds(n - 1 - i))


def reverse_in_block(x, sync=True):
    n = len(x)
    glob = {"x": list(x), "y": [0] * n}
    launch(reverse_kernel, (1, 1, 1), (n, 1, 1), glob, shared_words=n, args=(n, sync))
    return glob["y"]


def branch_kernel(t, split):
    """if (lane < split) { two instructions } else { one instruction }"""
    t.op("cond")
    if t.lane < split:
        t.op("then-1")
        t.op("then-2")
    else:
        t.op("else-1")
    t.op("after")
