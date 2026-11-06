# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lucas-lehmer-test/. The authors are listed in prov/X19VXC.jsonl.

"""Lucas-Lehmer test for Mersenne numbers M_p = 2^p - 1.

lucas_lehmer_test(p) returns True exactly when 2^p - 1 is prime, for every
integer p >= 2. The answer is always right: the test is deterministic.

Cost: p - 2 squarings modulo M_p, each followed by a reduction that needs only
shifts and additions. That is O(p M(p)) bit operations, O(p^3) with schoolbook
multiplication, where p is the number of binary digits of M_p. Integers are of
arbitrary precision (Python int).
"""


def reduce_mersenne(x: int, p: int) -> int:
    """Return x mod (2^p - 1) for x >= 0, with shifts, masks and additions only."""
    m = (1 << p) - 1
    while x > m:
        x = (x & m) + (x >> p)
    return 0 if x == m else x


def lucas_lehmer_test(p: int) -> bool:
    """Return True if 2^p - 1 is prime, for an integer p >= 2."""
    if p < 2:
        raise ValueError("p must be at least 2")
    if p == 2:  # @line L1
        return True
    m = (1 << p) - 1  # @line L2
    s = 4  # @line L3
    for _ in range(p - 2):  # @line L4
        s = reduce_mersenne(s * s + m - 2, p)  # @line L5
    return s == 0  # @line L6


def lucas_lehmer_residues(p: int) -> list[int]:
    """The values s_0, s_1, ..., s_(p-2) modulo 2^p - 1, for p >= 3."""
    if p < 3:
        raise ValueError("p must be at least 3")
    m = (1 << p) - 1
    out = [4 % m]
    for _ in range(p - 2):
        out.append((out[-1] * out[-1] - 2) % m)
    return out


def is_mersenne_number_prime(n: int) -> bool:
    """Primality of a Mersenne number n = 2^p - 1 with p >= 0, by the Lucas-Lehmer test."""
    if n < 0 or (n + 1) & n:
        raise ValueError("n must be of the form 2^p - 1")
    p = (n + 1).bit_length() - 1
    if p < 2:
        return False  # n is 0 or 1
    return lucas_lehmer_test(p)
