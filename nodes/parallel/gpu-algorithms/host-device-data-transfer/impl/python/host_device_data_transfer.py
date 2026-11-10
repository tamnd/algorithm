# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/host-device-data-transfer/. The authors are listed in prov/J2CVHF.jsonl.
"""The latency-bandwidth model of a host-device copy, in exact arithmetic.

A copy of s bytes takes t(s) = L + s / beta, with a fixed latency L in seconds
and a bandwidth beta in bytes per second.  All functions take and return
Fractions (or ints), so the worked examples on the page can be checked exactly.
The numbers used in the tests are assumptions, not the figures of a given GPU.
No CUDA code is run.
"""
from fractions import Fraction as F


def transfer_time(latency, beta, size):
    return F(latency) + F(size) / F(beta)


def effective_bandwidth(latency, beta, size):
    """Bytes per second seen by one copy of `size` bytes: beta * s / (s + L * beta)."""
    return F(size) / transfer_time(latency, beta, size)


def half_bandwidth_size(latency, beta):
    """The size at which a copy reaches half the peak bandwidth: s = L * beta."""
    return F(latency) * F(beta)


def separate_vs_batched(latency, beta, chunk, count):
    """Time of `count` copies of `chunk` bytes, and of one copy of all of them."""
    return count * transfer_time(latency, beta, chunk), transfer_time(latency, beta, count * chunk)


def pcie_rate(gigatransfers, lanes, payload=128, block=130):
    """Raw rate per direction in GB/s for PCIe 3.0 and later (128b/130b encoding)."""
    return F(gigatransfers) * lanes * F(payload, block) / 8


def offload_time(flops, nbytes, gpu_rate, beta, latency=0):
    """Copy the data, then compute: no overlap."""
    return transfer_time(latency, beta, nbytes) + F(flops) / F(gpu_rate)


def min_intensity(gpu_rate, beta):
    """FLOP per transferred byte at which the copy time equals the compute time."""
    return F(gpu_rate) / F(beta)


def matmul_transfer_intensity(n, word=4):
    """2 n^3 FLOP over the 3 n^2 words of A, B and C moved across the bus."""
    return F(2 * n ** 3, 3 * n * n * word)
