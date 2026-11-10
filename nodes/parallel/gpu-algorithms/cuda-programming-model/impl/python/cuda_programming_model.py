# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cuda-programming-model/.
"""A minimal model of a CUDA launch: a grid of blocks, a block of threads, shared memory per block,
__syncthreads() as `yield`, and the end of a kernel as the only barrier across blocks.

The blocks of one launch run one after another, in an order given by the caller, because the
programming model makes no promise about the order of blocks. A kernel that is correct must give
the same result for every block order.
"""

from itertools import product


class Ctx:
    """The built-in variables of one thread and the memories it can reach."""

    def __init__(self, block_idx, thread_idx, block_dim, grid_dim, shared, glob):
        self.blockIdx, self.threadIdx = block_idx, thread_idx
        self.blockDim, self.gridDim = block_dim, grid_dim
        self.shared, self.glob = shared, glob


def launch(kernel, grid, block, glob, shared_words=0, args=(), order=None):
    """kernel<<<grid, block>>>(args) on the global memory dict glob.

    grid and block are (x, y, z) triples. order is a list of block indices that sets the order in
    which blocks run; the default is the linear order. Returns the number of threads that ran.
    """
    blocks = [(bx, by, bz) for bz, by, bx in product(range(grid[2]), range(grid[1]), range(grid[0]))]
    if order is not None:
        assert sorted(order) == sorted(blocks)
        blocks = list(order)
    count = 0
    for b in blocks:
        shared = [0] * shared_words  # shared memory lives as long as the block
        gens = []
        for z, y, x in product(range(block[2]), range(block[1]), range(block[0])):
            g = kernel(Ctx(b, (x, y, z), block, grid, shared, glob), *args)
            count += 1
            if hasattr(g, "__next__"):
                gens.append(g)
        while gens:  # every live thread runs to its next __syncthreads()
            live = []
            for g in gens:
                try:
                    next(g)
                    live.append(g)
                except StopIteration:
                    pass
            gens = live
    return count


def vec_add_kernel(t, n):
    i = t.blockIdx[0] * t.blockDim[0] + t.threadIdx[0]
    if i < n:
        t.glob["C"][i] = t.glob["A"][i] + t.glob["B"][i]


def vec_add(a, b, threads=256):
    """The host side: allocate, copy in, launch ceil(n / threads) blocks, copy out."""
    n = len(a)
    glob = {"A": list(a), "B": list(b), "C": [0] * n}  # cudaMalloc and cudaMemcpy
    blocks = (n + threads - 1) // threads
    ran = launch(vec_add_kernel, (blocks, 1, 1), (threads, 1, 1), glob, args=(n,))
    return list(glob["C"]), ran


def block_sum_kernel(t, n):
    """Kernel 1: each block sums its slice in shared memory and writes one partial sum."""
    T = t.blockDim[0]
    tid = t.threadIdx[0]
    i = t.blockIdx[0] * T + tid
    t.shared[tid] = t.glob["x"][i] if i < n else 0
    yield  # __syncthreads(): every slot of shared memory is written
    s = T // 2
    while s > 0:
        if tid < s:
            t.shared[tid] += t.shared[tid + s]
        yield  # __syncthreads() after each halving
        s //= 2
    if tid == 0:
        t.glob["partial"][t.blockIdx[0]] = t.shared[0]


def final_sum_kernel(t, m):
    """Kernel 2: one thread adds the partial sums. It runs after kernel 1 has finished."""
    if t.blockIdx[0] == 0 and t.threadIdx[0] == 0:
        t.glob["out"][0] = sum(t.glob["partial"][:m])


def two_kernel_sum(x, threads=64, order=None):
    """The sum of x with two launches; the kernel boundary is the global barrier."""
    assert threads & (threads - 1) == 0
    n = len(x)
    blocks = max(1, (n + threads - 1) // threads)
    glob = {"x": list(x), "partial": [0] * blocks, "out": [0]}
    launch(block_sum_kernel, (blocks, 1, 1), (threads, 1, 1), glob, threads, (n,), order)
    launch(final_sum_kernel, (1, 1, 1), (1, 1, 1), glob, args=(blocks,))
    return glob["out"][0]


def fused_kernel(t, n, m):
    """Wrong: kernel 1 and kernel 2 fused, with block 0 reading the partial sums of other blocks.

    No barrier inside one launch orders block 0 after the other blocks.
    """
    yield from block_sum_kernel(t, n)
    if t.blockIdx[0] == 0 and t.threadIdx[0] == 0:
        t.glob["out"][0] = sum(t.glob["partial"][:m])


def one_kernel_sum(x, threads=64, order=None):
    n = len(x)
    blocks = max(1, (n + threads - 1) // threads)
    glob = {"x": list(x), "partial": [0] * blocks, "out": [0]}
    launch(fused_kernel, (blocks, 1, 1), (threads, 1, 1), glob, threads, (n, blocks), order)
    return glob["out"][0]
