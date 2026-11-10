# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thread-block-and-grid/.
"""Index arithmetic of CUDA thread blocks and grids, the grid-stride loop, and launch limits.

All sizes are (x, y, z) triples. x varies fastest, as in CUDA.
"""

from itertools import product

WARP_SIZE = 32

# CUDA Programming Guide v13.5, Section 5.1.3, Table 33. Equal for compute capability 7.5 to 12.x.
LIMITS = {"threads_per_block": 1024, "block": (1024, 1024, 64), "grid": (2**31 - 1, 65535, 65535)}


def ceil_div(a, b):
    return -(-a // b)


def linear_thread(thread_idx, block_dim):
    """The rank of a thread in its block; it sets the warp (rank // 32) and the lane (rank % 32)."""
    x, y, z = thread_idx
    bx, by, _ = block_dim
    return x + y * bx + z * bx * by


def linear_block(block_idx, grid_dim):
    x, y, z = block_idx
    gx, gy, _ = grid_dim
    return x + y * gx + z * gx * gy


def global_xyz(block_idx, thread_idx, block_dim):
    """The global (column, row, layer) of a thread: blockIdx * blockDim + threadIdx per axis."""
    return tuple(b * d + t for b, d, t in zip(block_idx, block_dim, thread_idx))


def threads_of(grid_dim, block_dim):
    """Every (blockIdx, threadIdx) of a launch."""
    for bz, by, bx in product(*(range(g) for g in reversed(grid_dim))):
        for z, y, x in product(*(range(d) for d in reversed(block_dim))):
            yield (bx, by, bz), (x, y, z)


def grid_for(shape, block_dim):
    """The smallest grid that covers an array of the given (x, y, z) shape."""
    return tuple(ceil_div(s, d) for s, d in zip(shape, block_dim))


def grid_stride_indices(n, grid_x, block_x):
    """The indices that each thread of a 1D grid-stride loop visits, keyed by global thread id.

    for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < n; i += blockDim.x * gridDim.x)
    """
    stride = grid_x * block_x
    return {g: list(range(g, n, stride)) for g in range(stride)}


def valid_launch(grid_dim, block_dim, limits=LIMITS):
    """True when the launch obeys the size limits of Table 33."""
    if any(d < 1 for d in grid_dim + block_dim):
        return False
    if block_dim[0] * block_dim[1] * block_dim[2] > limits["threads_per_block"]:
        return False
    if any(d > m for d, m in zip(block_dim, limits["block"])):
        return False
    return all(g <= m for g, m in zip(grid_dim, limits["grid"]))


def warps_per_block(block_dim):
    t = block_dim[0] * block_dim[1] * block_dim[2]
    return ceil_div(t, WARP_SIZE)


def idle_lanes(block_dim):
    """Lanes of the last warp that hold no thread when the block size is not a multiple of 32."""
    t = block_dim[0] * block_dim[1] * block_dim[2]
    return warps_per_block(block_dim) * WARP_SIZE - t
