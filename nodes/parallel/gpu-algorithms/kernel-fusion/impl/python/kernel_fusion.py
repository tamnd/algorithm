# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-fusion/. The authors are listed in prov/R2RS59.jsonl.
"""Kernel fusion on a counting model of a GPU.

Global memory is a Mem object that counts the words each kernel reads and
writes.  A kernel is a function of (mem, block) run for every block of a grid;
values that a block keeps in registers or shared memory are Python locals and
cost nothing.  Each launch is counted.  The CUDA code on the page is not run by
these tests.
"""
from functools import reduce


class Mem:
    def __init__(self):
        self.arrays = {}
        self.reads = 0
        self.writes = 0
        self.launches = 0

    def alloc(self, name, n, fill=None):
        self.arrays[name] = [fill] * n

    def put(self, name, values):          # host data, not counted
        self.arrays[name] = list(values)

    def load(self, name, i):
        self.reads += 1
        return self.arrays[name][i]

    def store(self, name, i, v):
        self.writes += 1
        self.arrays[name][i] = v

    def launch(self, kernel, blocks):
        self.launches += 1
        for blk in range(blocks):
            kernel(self, blk)


def _blocks(n, b):
    return (n + b - 1) // b


def map_reduce_unfused(x, f, op, b):
    """y = map f x in one kernel, block partial sums in a second, the total in a third."""
    n = len(x)
    m = Mem()
    m.put("x", x)
    m.alloc("y", n)
    t = _blocks(n, b)
    m.alloc("part", t)
    m.alloc("out", 1)

    def k_map(mem, blk):
        for i in range(blk * b, min(n, blk * b + b)):
            mem.store("y", i, f(mem.load("x", i)))

    def k_reduce(mem, blk):
        vals = [mem.load("y", i) for i in range(blk * b, min(n, blk * b + b))]
        mem.store("part", blk, reduce(op, vals))

    def k_final(mem, blk):
        mem.store("out", 0, reduce(op, [mem.load("part", g) for g in range(t)]))

    m.launch(k_map, t)
    m.launch(k_reduce, t)
    m.launch(k_final, 1)
    return m.arrays["out"][0], m


def map_reduce_fused(x, f, op, b):
    """One kernel applies f in registers and reduces the block; a second adds the partials."""
    n = len(x)
    m = Mem()
    m.put("x", x)
    t = _blocks(n, b)
    m.alloc("part", t)
    m.alloc("out", 1)

    def k_fused(mem, blk):
        vals = [f(mem.load("x", i)) for i in range(blk * b, min(n, blk * b + b))]  # f stays in registers
        mem.store("part", blk, reduce(op, vals))

    def k_final(mem, blk):
        mem.store("out", 0, reduce(op, [mem.load("part", g) for g in range(t)]))

    m.launch(k_fused, t)
    m.launch(k_final, 1)
    return m.arrays["out"][0], m


def chain_unfused(x, fs, b):
    """k elementwise kernels, each reading the previous output from global memory."""
    n = len(x)
    m = Mem()
    m.put("a0", x)
    for k, f in enumerate(fs):
        m.alloc("a%d" % (k + 1), n)

        def kern(mem, blk, f=f, k=k):
            for i in range(blk * b, min(n, blk * b + b)):
                mem.store("a%d" % (k + 1), i, f(mem.load("a%d" % k, i)))

        m.launch(kern, _blocks(n, b))
    return m.arrays["a%d" % len(fs)], m


def chain_fused(x, fs, b):
    n = len(x)
    m = Mem()
    m.put("a0", x)
    m.alloc("out", n)

    def kern(mem, blk):
        for i in range(blk * b, min(n, blk * b + b)):
            v = mem.load("a0", i)
            for f in fs:                      # every intermediate stays in a register
                v = f(v)
            mem.store("out", i, v)

    m.launch(kern, _blocks(n, b))
    return m.arrays["out"], m


def occupancy_warps(regs_per_thread, threads_per_block, regfile=65536, max_warps=64, max_blocks=32):
    """Resident warps per SM limited by registers, under stated assumptions (no allocation granularity)."""
    warps_per_block = -(-threads_per_block // 32)
    blocks_by_regs = regfile // (regs_per_thread * threads_per_block)
    blocks = min(blocks_by_regs, max_blocks, max_warps // warps_per_block)
    return blocks * warps_per_block
