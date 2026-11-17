# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/timing-attack/. The authors are listed in prov/M5SV5X.jsonl.
"""Cost models for modular exponentiation, the leak they carry, and two fixes.

Nothing here reads a clock. A timing attack needs one number for each run,
and that number is the amount of work. So the work is counted exactly:

* ``modexp_square_and_multiply`` reports the multiplications it does for
  each exponent bit. A bit of 1 costs one more multiplication than a bit
  of 0, so the list of counts is the secret exponent written in another
  alphabet. ``recover_exponent`` reads it back.
* ``modexp_montgomery_ladder`` does one squaring and one multiplication for
  every bit, whatever the bit is, so the same list is constant.
* ``Montgomery`` counts the extra reduction of each Montgomery
  multiplication. That count depends on the input, which is the leak that
  Brumley and Boneh used over a network in 2003. ``blinded_cost`` shows
  that RSA blinding removes the dependence.

For study only. This code is not constant time, and it is not a secure
implementation of anything; it is a measuring instrument for a toy device.
"""

from dataclasses import dataclass, field


@dataclass
class Trace:
    """What an attacker gets from one run: the work, not the result.

    ``per_bit[i]`` is the number of modular multiplications the device did
    while it processed exponent bit ``i``, counted from the most significant
    bit of the exponent. ``total`` is their sum, which is what a single
    stopwatch reading gives.
    """

    per_bit: list = field(default_factory=list)
    squarings: int = 0
    multiplications: int = 0
    extra_reductions: int = 0

    @property
    def total(self) -> int:
        return self.squarings + self.multiplications


def bits_of(exponent: int) -> list:
    """The exponent, most significant bit first. The length is public."""
    if exponent <= 0:
        raise ValueError("the exponent must be positive")
    return [(exponent >> i) & 1 for i in range(exponent.bit_length() - 1, -1, -1)]


def modexp_square_and_multiply(base: int, exponent: int, modulus: int) -> tuple:
    """Left to right square and multiply. Returns the value and the trace.

    The loop body is a squaring, and a multiplication only when the bit is
    1. This is the shape that leaks: the work of one iteration names the
    bit of that iteration.
    """
    trace = Trace()
    value = 1
    for bit in bits_of(exponent):
        cost = 0
        value = value * value % modulus
        trace.squarings += 1
        cost += 1
        if bit:
            value = value * base % modulus
            trace.multiplications += 1
            cost += 1
        trace.per_bit.append(cost)
    return value, trace


def modexp_montgomery_ladder(base: int, exponent: int, modulus: int) -> tuple:
    """The Montgomery ladder. One squaring and one multiplication for each bit.

    The two registers hold x^k and x^(k+1) for the prefix k of the exponent
    read so far. Both branches do the same two operations, so the trace is
    the constant list [2, 2, ..., 2] and it says only how long the exponent
    is, which is public.
    """
    trace = Trace()
    r0, r1 = 1, base % modulus
    for bit in bits_of(exponent):
        if bit:
            r0 = r0 * r1 % modulus
            r1 = r1 * r1 % modulus
        else:
            r1 = r0 * r1 % modulus
            r0 = r0 * r0 % modulus
        trace.squarings += 1
        trace.multiplications += 1
        trace.per_bit.append(2)
    return r0, trace


def recover_exponent(trace: Trace) -> int:
    """The attack: read the secret exponent out of the per-bit work counts.

    A count of 2 is a bit of 1 and a count of 1 is a bit of 0. The attacker
    needs no key, no plaintext and no result, only the work of each
    iteration. A constant trace raises ValueError, because it holds nothing.
    """
    counts = set(trace.per_bit)
    if len(counts) < 2:
        raise ValueError("the trace is constant, so it carries no exponent bits")
    low, high = min(trace.per_bit), max(trace.per_bit)
    if (low, high) != (1, 2):
        raise ValueError("unexpected costs; this reader is for square and multiply")
    value = 0
    for cost in trace.per_bit:
        value = (value << 1) | (1 if cost == high else 0)
    return value


def hamming_weight_from_total(trace: Trace, exponent_bits: int) -> int:
    """One stopwatch reading gives the number of 1 bits, not their places.

    The total work is exponent_bits squarings plus one multiplication for
    each 1 bit, so the weight comes straight out of the total.
    """
    return trace.total - exponent_bits


@dataclass
class Montgomery:
    """Montgomery multiplication modulo an odd n, with the extra reduction counted.

    The product is (a * b * R^-1) mod n for R = 2^r. The last step of the
    algorithm has a value below 2n and subtracts n when it must. That
    subtraction is the "extra reduction": it happens or it does not,
    depending on the operands, so it makes the cost of a multiplication a
    function of the data.
    """

    n: int
    word: int = 64
    extra_reductions: int = 0
    multiplications: int = 0

    def __post_init__(self) -> None:
        if self.n % 2 == 0 or self.n < 3:
            raise ValueError("the modulus must be odd and at least 3")
        self.r_bits = ((self.n.bit_length() + self.word - 1) // self.word) * self.word
        self.r = 1 << self.r_bits
        self.mask = self.r - 1
        self.n_prime = (-pow(self.n, -1, self.r)) % self.r

    def mul(self, a: int, b: int) -> int:
        """One Montgomery multiplication. Updates the two counters."""
        t = a * b
        m = ((t & self.mask) * self.n_prime) & self.mask
        u = (t + m * self.n) >> self.r_bits
        self.multiplications += 1
        if u >= self.n:
            u -= self.n
            self.extra_reductions += 1
        return u

    def enter(self, a: int) -> int:
        """Map a into the Montgomery domain: a * R mod n."""
        return a % self.n * self.r % self.n

    def leave(self, u: int) -> int:
        """Map u back out of the Montgomery domain."""
        return self.mul(u, 1)

    def exponentiate(self, base: int, exponent: int) -> int:
        """Square and multiply inside the Montgomery domain."""
        one = self.enter(1)
        value, factor = one, self.enter(base)
        for bit in bits_of(exponent):
            value = self.mul(value, value)
            if bit:
                value = self.mul(value, factor)
        return self.leave(value)


def extra_reduction_cost(modulus: int, exponent: int, ciphertext: int) -> tuple:
    """The work of one private operation, in the Montgomery cost model.

    Returns the plaintext and the number of extra reductions. The second
    number is the part of the cost that depends on the ciphertext, so it is
    the part an attacker can steer. The same ciphertext always gives the
    same number, which lets an attacker average away the noise of a real
    measurement.
    """
    engine = Montgomery(modulus)
    value = engine.exponentiate(ciphertext, exponent)
    return value, engine.extra_reductions


def blinded_cost(modulus: int, public_exponent: int, exponent: int,
                 ciphertext: int, blind: int) -> tuple:
    """The same operation with RSA blinding, and its cost.

    The device computes (c * r^e)^d and multiplies by r^-1. The result is
    the same plaintext, but the exponentiation runs on c * r^e mod n, which
    the attacker cannot choose or predict, so the extra reduction count
    belongs to a random number.
    """
    engine = Montgomery(modulus)
    blinded = ciphertext * pow(blind, public_exponent, modulus) % modulus
    value = engine.exponentiate(blinded, exponent)
    plain = value * pow(blind, -1, modulus) % modulus
    return plain, engine.extra_reductions
