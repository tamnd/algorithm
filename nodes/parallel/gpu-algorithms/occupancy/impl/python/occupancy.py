# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/occupancy/.
"""Theoretical occupancy of an SM from the resource use of one block.

occupancy = resident warps / maximum resident warps. A block is resident only when all its
threads, warps, registers and shared memory fit. The register model allocates registers per warp
in units of 256 and splits the register file into 4 equal partitions, one per warp scheduler; a
warp lives in one partition. These two rules reproduce the examples of the CUDA C++ Best
Practices Guide, Section 11.1.1, but they are a model, not a vendor specification.
"""

from fractions import Fraction

WARP = 32
REG_UNIT = 256
PARTITIONS = 4

# Per-SM limits. CUDA Programming Guide v13.5, Section 5.1.3, Tables 33 and 34.
CC = {
    "8.0": dict(max_threads=2048, max_warps=64, max_blocks=32, regs=65536, smem=164 * 1024),
    "8.6": dict(max_threads=1536, max_warps=48, max_blocks=16, regs=65536, smem=100 * 1024),
    "9.0": dict(max_threads=2048, max_warps=64, max_blocks=32, regs=65536, smem=228 * 1024),
    # The values of the Guide's occupancy example in Section 2.3.7 (a device of compute capability 10.0).
    "10.0": dict(max_threads=2048, max_warps=64, max_blocks=32, regs=65536, smem=233472),
    # Best Practices Guide 11.1.1 gives 65,536 registers and 2048 threads for compute capability 7.0.
    # The block and shared memory limits here are set so that they do not bind in its examples.
    "7.0": dict(max_threads=2048, max_warps=64, max_blocks=32, regs=65536, smem=96 * 1024),
}


def ceil_div(a, b):
    return -(-a // b)


def regs_per_warp(regs_per_thread):
    return ceil_div(WARP * regs_per_thread, REG_UNIT) * REG_UNIT


def limits(dev, threads, regs_per_thread, smem_per_block):
    """The number of resident blocks allowed by each resource."""
    wb = ceil_div(threads, WARP)
    out = {"blocks": dev["max_blocks"], "threads": dev["max_threads"] // threads,
           "warps": dev["max_warps"] // wb}
    if regs_per_thread > 0:
        per_part = (dev["regs"] // PARTITIONS) // regs_per_warp(regs_per_thread)
        out["registers"] = (PARTITIONS * per_part) // wb
    out["shared"] = dev["smem"] // smem_per_block if smem_per_block > 0 else dev["max_blocks"]
    return out


def resident_blocks(dev, threads, regs_per_thread, smem_per_block):
    return min(limits(dev, threads, regs_per_thread, smem_per_block).values())


def occupancy(dev, threads, regs_per_thread, smem_per_block):
    b = resident_blocks(dev, threads, regs_per_thread, smem_per_block)
    return Fraction(b * ceil_div(threads, WARP), dev["max_warps"])


def fits(dev, b, threads, regs_per_thread, smem_per_block):
    """Brute force: try to place b blocks, warp by warp, on the 4 register partitions."""
    wb = ceil_div(threads, WARP)
    if b > dev["max_blocks"] or b * threads > dev["max_threads"] or b * wb > dev["max_warps"]:
        return False
    if b * smem_per_block > dev["smem"]:
        return False
    free = [dev["regs"] // PARTITIONS] * PARTITIONS
    need = regs_per_warp(regs_per_thread) if regs_per_thread > 0 else 0
    for _ in range(b * wb):  # put each warp in the partition with the most free registers
        j = max(range(PARTITIONS), key=lambda q: free[q])
        if free[j] < need:
            return False
        free[j] -= need
    return True


def brute_force_blocks(dev, threads, regs_per_thread, smem_per_block):
    b = 0
    while fits(dev, b + 1, threads, regs_per_thread, smem_per_block):
        b += 1
    return b
