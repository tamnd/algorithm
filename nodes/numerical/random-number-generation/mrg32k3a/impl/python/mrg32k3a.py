# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mrg32k3a/. The authors are listed in prov/3EWTJP.jsonl.

M1 = 4294967087  # 2^32 - 209, prime
M2 = 4294944443  # 2^32 - 22853, prime
A12, A13N = 1403580, 810728  # x1_n = (A12 x1_{n-2} - A13N x1_{n-3}) mod M1
A21, A23N = 527612, 1370589  # x2_n = (A21 x2_{n-1} - A23N x2_{n-3}) mod M2
NORM = 2.328306549295728e-10  # the constant of the reference code, about 1 / (M1 + 1)

# One-step matrices on the state (x_{n-3}, x_{n-2}, x_{n-1}), oldest first.
A1 = [[0, 1, 0], [0, 0, 1], [(-A13N) % M1, A12, 0]]
A2 = [[0, 1, 0], [0, 0, 1], [(-A23N) % M2, 0, A21]]


def check_seed(x1: list[int], x2: list[int]) -> None:
    """A valid seed has x1 in [0, M1)^3 and x2 in [0, M2)^3, neither all zero."""
    if len(x1) != 3 or len(x2) != 3:
        raise ValueError("each component needs three values")
    if not all(0 <= v < M1 for v in x1) or not all(0 <= v < M2 for v in x2):
        raise ValueError("seed values out of range")
    if not any(x1) or not any(x2):
        raise ValueError("a component seed must not be all zero")


def mrg32k3a_next(x1: list[int], x2: list[int]) -> float:
    """Advance both components in place (oldest value first) and return u in (0, 1).

    Integer version of L'Ecuyer's 1999 code; the float result is bit-for-bit the
    same as the double-precision reference. Cost: 4 multiplications, 2 reductions.
    """
    p1 = (A12 * x1[1] - A13N * x1[0]) % M1  # @line L1
    x1[0], x1[1], x1[2] = x1[1], x1[2], p1  # @line L2
    p2 = (A21 * x2[2] - A23N * x2[0]) % M2  # @line L3
    x2[0], x2[1], x2[2] = x2[1], x2[2], p2  # @line L4
    if p1 > p2:  # @line L5
        return (p1 - p2) * NORM
    return (p1 - p2 + M1) * NORM  # @line L6


def mrg32k3a_stream(n: int, x1: list[int] | None = None, x2: list[int] | None = None) -> list[float]:
    """The first n outputs; the default seed is the reference seed 12345 in all six places."""
    x1 = list(x1) if x1 is not None else [12345] * 3
    x2 = list(x2) if x2 is not None else [12345] * 3
    check_seed(x1, x2)
    return [mrg32k3a_next(x1, x2) for _ in range(n)]


def mat_mul(A: list[list[int]], B: list[list[int]], m: int) -> list[list[int]]:
    return [[sum(A[i][t] * B[t][j] for t in range(3)) % m for j in range(3)] for i in range(3)]


def mat_pow2(A: list[list[int]], e: int, m: int) -> list[list[int]]:
    """A^(2^e) mod m by e squarings."""
    for _ in range(e):
        A = mat_mul(A, A, m)
    return A


def mat_vec(A: list[list[int]], v: list[int], m: int) -> list[int]:
    return [sum(A[i][t] * v[t] for t in range(3)) % m for i in range(3)]


def mrg32k3a_jump(x1: list[int], x2: list[int], e: int) -> tuple[list[int], list[int]]:
    """The state 2^e steps ahead: e = 127 for the next stream, e = 76 for the next substream."""
    return mat_vec(mat_pow2(A1, e, M1), x1, M1), mat_vec(mat_pow2(A2, e, M2), x2, M2)
