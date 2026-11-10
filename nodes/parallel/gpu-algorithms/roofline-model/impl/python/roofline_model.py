# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roofline-model/.
"""The roofline model of Williams, Waterman and Patterson (2009), with exact fractions.

attainable(I) = min(peak, I * bandwidth), for an arithmetic intensity I in FLOP per byte.
Units: FLOP/s, bytes/s, FLOP/byte. Hardware numbers are inputs, not facts of the model.
"""

from fractions import Fraction as F

# NVIDIA A100 40 GB (Ampere whitepaper): peak FLOP/s and HBM2 bandwidth. They differ for other parts.
# "shared" is derived, not quoted: 32 banks x 4 bytes per clock x 108 SMs x 1.41 GHz, no bank conflicts.
A100 = {
    "fp32": F(195, 10) * 10**12,
    "fp64": F(97, 10) * 10**12,
    "fp64_tensor": F(195, 10) * 10**12,
    "fp16_tensor": F(312) * 10**12,
    "hbm": F(1555) * 10**9,
    "shared": F(128 * 108 * 1410) * 10**6,
}


def attainable(intensity, peak, bandwidth):
    return min(F(peak), F(intensity) * F(bandwidth))


def ridge(peak, bandwidth):
    """The intensity at which the two roofs meet."""
    return F(peak) / F(bandwidth)


def bound(intensity, peak, bandwidth):
    return "memory" if F(intensity) < ridge(peak, bandwidth) else "compute"


def with_ceilings(intensity, compute_ceilings, bandwidth_ceilings):
    """The roof under the lowest ceilings that apply: min over all compute and bandwidth ceilings."""
    return min([F(c) for c in compute_ceilings] + [F(intensity) * F(b) for b in bandwidth_ceilings])


def hierarchical(peak, levels):
    """levels: (intensity against that level, bandwidth of that level). The lowest roof wins."""
    return min([F(peak)] + [F(i) * F(b) for i, b in levels])


def time_lower_bound(flops, bytes_moved, peak, bandwidth):
    """A kernel needs at least max(W / peak, Q / bandwidth) seconds; this equals W / attainable(W/Q)."""
    return max(F(flops) / F(peak), F(bytes_moved) / F(bandwidth))
