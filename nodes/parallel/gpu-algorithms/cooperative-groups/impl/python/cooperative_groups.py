# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cooperative-groups/.
"""Cooperative groups: tiles of a block, and the co-residency condition of grid.sync().

tile_ranks gives the ranks that tiled_partition<S>(this_thread_block()) assigns. run_grid models
the blocks of one launch on a GPU with a fixed number of resident block slots: a block takes a
slot when it starts and frees it when it ends. A grid barrier releases only when every block of
the grid has reached it, so a grid with more blocks than slots deadlocks.
"""


def tile_ranks(block_threads, size):
    """(thread_rank, meta_group_rank) in the tile, for each thread rank of the block."""
    assert size >= 1 and size & (size - 1) == 0 and size <= 1024
    return [(r % size, r // size) for r in range(block_threads)]


def meta_group_size(block_threads, size):
    return -(-block_threads // size)


def run_grid(blocks, slots, kernel, glob):
    """Run kernel(b, glob) for b in range(blocks); each `yield` in it is grid.sync().

    Returns True when the grid finishes, False on deadlock.
    """
    waiting_to_start = list(range(blocks))
    resident = {}  # block -> generator; a block in here is at a barrier or not yet started
    at_barrier = set()
    while waiting_to_start or resident:
        while waiting_to_start and len(resident) < slots:  # fill the free slots
            b = waiting_to_start.pop(0)
            resident[b] = kernel(b, glob)
        progressed = False
        for b in list(resident):
            if b in at_barrier:
                continue
            try:
                next(resident[b])
                at_barrier.add(b)  # reached grid.sync()
            except StopIteration:
                del resident[b]  # finished; its slot is free
            progressed = True
        if len(at_barrier) == blocks:  # every block of the grid is at the barrier
            at_barrier.clear()
            continue
        if not progressed and not (waiting_to_start and len(resident) < slots):
            return False  # all resident blocks wait at the barrier for blocks that cannot start
    return True


def grid_sum_kernel(threads):
    def kernel(b, glob):
        x = glob["x"]
        lo, hi = b * threads, min(len(x), (b + 1) * threads)
        glob["partial"][b] = sum(x[lo:hi])  # phase 1: each block writes its partial sum
        yield  # grid.sync()
        if b == 0:
            glob["out"] = sum(glob["partial"])  # phase 2: all partial sums are visible
    return kernel


def cooperative_sum(x, threads, blocks, slots):
    glob = {"x": list(x), "partial": [0] * blocks, "out": None}
    assert blocks * threads >= len(x)
    ok = run_grid(blocks, slots, grid_sum_kernel(threads), glob)
    return glob["out"] if ok else None


def max_cooperative_blocks(num_sms, blocks_per_sm):
    """The largest grid that a cooperative launch accepts: every block must be resident at once."""
    return num_sms * blocks_per_sm
