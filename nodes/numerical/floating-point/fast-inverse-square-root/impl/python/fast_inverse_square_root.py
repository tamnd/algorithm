# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-inverse-square-root/. The authors are listed in prov/10WFYW.jsonl.

"""Fast inverse square root (the Quake III routine), in emulated binary32."""

import math
import struct

MAGIC = 0x5F3759DF
_F32 = struct.Struct("<f")
_U32 = struct.Struct("<I")
SMALLEST = 2.0**-125  # x and x/2 are normal binary32 numbers
LARGEST = (2.0 - 2.0**-23) * 2.0**127  # the largest finite binary32 number


def f32(v: float) -> float:
    """Round a binary64 value to the nearest binary32 value (ties to even)."""
    return _F32.unpack(_F32.pack(v))[0]


def bits32(x: float) -> int:
    """The 32-bit pattern of the binary32 value x, as an unsigned integer."""
    return _U32.unpack(_F32.pack(x))[0]


def float32(i: int) -> float:
    """The binary32 value whose pattern is the unsigned 32-bit integer i."""
    return _F32.unpack(_U32.pack(i & 0xFFFFFFFF))[0]


def fast_inverse_square_root(x: float, magic: int = MAGIC, newton_steps: int = 1) -> float:
    """Approximate 1/sqrt(x) with the bit trick and Newton steps in binary32.

    x is first rounded to binary32. Precondition: the rounded x lies in
    [2^(-125), largest binary32]; otherwise ValueError is raised. Each
    operation is a correctly rounded binary32 operation (a binary64 operation
    on binary32 inputs, rounded to binary32, gives the same result). With the
    default magic constant and one step, the relative error y*sqrt(x) - 1 lies
    in [-0.0017525, 2e-7]. Cost: O(newton_steps) operations, O(1) space.
    """
    x = f32(x)
    if not (SMALLEST <= x <= LARGEST):
        raise ValueError("x must be a binary32 value in [2^(-125), max]")
    x2 = f32(0.5 * x)  # @line L1
    i = bits32(x)  # @line L2
    i = magic - (i >> 1)  # @line L3
    y = float32(i)  # @line L4
    for _ in range(newton_steps):
        y = f32(y * f32(1.5 - f32(f32(x2 * y) * y)))  # @line L5
    return y  # @line L6


def initial_guess(x: float, magic: int = MAGIC) -> float:
    """The guess of line L4 alone (no Newton step), for a binary32 x in the domain."""
    return fast_inverse_square_root(x, magic, newton_steps=0)


def relative_error(x: float, y: float) -> float:
    """y*sqrt(x) - 1, computed in binary64 (its own error is about 1e-16)."""
    return y * math.sqrt(x) - 1.0
