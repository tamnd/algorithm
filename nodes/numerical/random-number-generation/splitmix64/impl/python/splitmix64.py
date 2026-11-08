# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/splitmix64/. The authors are listed in prov/V3VE7E.jsonl.

MASK64 = (1 << 64) - 1
GOLDEN_GAMMA = 0x9E3779B97F4A7C15  # odd, close to 2^64 divided by the golden ratio
M1 = 0xBF58476D1CE4E5B9  # the multipliers of Stafford's mix variant 13
M2 = 0x94D049BB133111EB


def mix64(z: int) -> int:
    """The output function g: a bijection of 64-bit words."""
    z = ((z ^ (z >> 30)) * M1) & MASK64  # @line L3
    z = ((z ^ (z >> 27)) * M2) & MASK64  # @line L4
    return z ^ (z >> 31)


def splitmix64_next(x: int, gamma: int = GOLDEN_GAMMA) -> tuple[int, int]:
    """Advance the Weyl state by gamma and return (new state, output).

    gamma must be odd; then the state has period exactly 2^64.
    Cost: one addition, two multiplications, three shifts and three XORs.
    """
    x = (x + gamma) & MASK64  # @line L1
    z = x  # @line L2
    z = mix64(z)
    return x, z  # @line L5


def _unxorshift_right(z: int, s: int) -> int:
    """Invert z -> z ^ (z >> s) on 64-bit words."""
    x = z
    for _ in range(64 // s + 1):
        x = z ^ (x >> s)
    return x


def unmix64(y: int) -> int:
    """The inverse of mix64, which shows that mix64 is a bijection."""
    z = _unxorshift_right(y, 31)
    z = _unxorshift_right((z * pow(M2, -1, 1 << 64)) & MASK64, 27)
    z = _unxorshift_right((z * pow(M1, -1, 1 << 64)) & MASK64, 30)
    return z


def splitmix64_stream(seed: int, n: int, gamma: int = GOLDEN_GAMMA) -> list[int]:
    """Return the first n outputs from a 64-bit seed (any value, including 0)."""
    if gamma % 2 == 0:
        raise ValueError("gamma must be odd")
    x = seed & MASK64
    out: list[int] = []
    for _ in range(n):
        x, z = splitmix64_next(x, gamma)
        out.append(z)
    return out


def seed_state(seed: int, words: int) -> list[int]:
    """Fill the state of another generator, such as xoshiro256 (4 words), from one seed."""
    return splitmix64_stream(seed, words)
