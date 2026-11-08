# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randu/. The authors are listed in prov/352H47.jsonl.

M = 2**31  # the modulus
MASK = M - 1
A = 65539  # the multiplier 2^16 + 3


def randu_seed(seed: int) -> int:
    """Return the start state. RANDU needs an odd state in [1, 2^31 - 1]."""
    x = seed & MASK
    if x % 2 == 0:
        raise ValueError("the seed must be odd modulo 2^31")
    return x


def randu_next(x: int) -> int:
    """Return 65539 * x mod 2^31 with a shift and two additions.

    Precondition: x is odd and 0 < x < 2^31. Cost: O(1) word operations.
    """
    return ((x << 16) + (x << 1) + x) & MASK  # @line L1


def randu_uniform(x: int) -> float:
    """Map a state to the float x / 2^31 in (0, 1)."""
    return x / M  # @line L2


def randu_stream(seed: int, n: int) -> list[int]:
    """Return the next n states after the seed."""
    x = randu_seed(seed)
    out: list[int] = []
    for _ in range(n):
        x = randu_next(x)
        out.append(x)
    return out


def randu_plane(x0: int, x1: int, x2: int) -> int:
    """Return the integer j with 9 u0 - 6 u1 + u2 = j for three consecutive states.

    The page proves that 9 x0 - 6 x1 + x2 is a multiple of 2^31, so every
    triple of outputs lies on one of the planes 9x - 6y + z = j, j = -5, ..., 9.
    """
    v = 9 * x0 - 6 * x1 + x2
    if v % M != 0:
        raise ValueError("the three states are not consecutive RANDU states")
    return v // M
