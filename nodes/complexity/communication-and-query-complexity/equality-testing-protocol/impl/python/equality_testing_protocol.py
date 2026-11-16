# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/equality-testing-protocol/. The authors are listed in prov/SVFWAE.jsonl.

import random
from collections.abc import Sequence
from fractions import Fraction


def is_prime(m: int) -> bool:
    """Return True if m is a prime. Trial division, enough for q of about n^2."""
    if m < 2:
        return False
    d = 2
    while d * d <= m:
        if m % d == 0:
            return False
        d += 1
    return True


def field_size(n: int) -> int:
    """Return the least prime q with q >= max(2, n^2)."""
    q = max(2, n * n)
    while not is_prime(q):
        q += 1
    return q


def word_length(q: int) -> int:
    """Return the number of bits that write each of 0, ..., q - 1 in binary."""
    return max(1, (q - 1).bit_length())


def fingerprint(x: Sequence[int], r: int, q: int) -> int:
    """Return A_x(r) mod q, where A_x(z) = x[0] + x[1] z + ... + x[n-1] z^(n-1).

    The sum is computed by Horner's rule, from the highest coefficient down.
    """
    v = 0
    for bit in reversed(x):
        v = (v * r + bit) % q
    return v


def exchange(x: Sequence[int], y: Sequence[int], r: int, q: int) -> tuple[bool, str]:
    """Run lines L3 to L7 with the field size q and the random point r.

    Return the common output and the transcript, as a string of '0' and '1'.
    """
    w = word_length(q)
    a = fingerprint(x, r, q)  # @line L3
    transcript = format(r, f"0{w}b") + format(a, f"0{w}b")  # @line L4
    r_bob = int(transcript[:w], 2)
    a_bob = int(transcript[w:], 2)
    b = fingerprint(y, r_bob, q)  # @line L5
    bit = "1" if a_bob == b else "0"  # @line L6
    transcript += bit
    return bit == "1", transcript  # @line L7


def equality_test(x: Sequence[int], y: Sequence[int], rng: random.Random) -> tuple[bool, str]:
    """Run the randomized equality testing protocol on Alice's x and Bob's y.

    x and y are bit sequences of the same length n. Alice draws the random
    point with rng (private coins). The result is (output, transcript).
    The output is True when x == y. When x != y it is False, except with
    probability at most (n - 1) / q over the random point.
    """
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    q = field_size(len(x))  # @line L1
    r = rng.randrange(q)  # @line L2
    return exchange(x, y, r, q)


def error_probability(x: Sequence[int], y: Sequence[int]) -> Fraction:
    """Return the exact probability that the protocol gives a wrong answer on (x, y).

    The probability is over the q equally likely values of the random point.
    """
    q = field_size(len(x))
    want = list(x) == list(y)
    wrong = sum(1 for r in range(q) if exchange(x, y, r, q)[0] != want)
    return Fraction(wrong, q)


def protocol_cost(n: int) -> int:
    """Return the length in bits of every transcript for inputs of length n."""
    return 2 * word_length(field_size(n)) + 1
