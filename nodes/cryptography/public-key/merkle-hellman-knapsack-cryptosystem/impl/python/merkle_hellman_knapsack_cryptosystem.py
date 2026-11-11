# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-hellman-knapsack-cryptosystem/. The authors are listed in prov/FC4WWX.jsonl.
"""The Merkle-Hellman knapsack cryptosystem (1978), and the lattice attack that broke it.

The scheme hides a superincreasing sequence behind a modular multiplication.
The public key is the disguised sequence, encryption adds up the entries the
message selects, and the private modulus and multiplier undo the disguise so
that a greedy pass over the superincreasing sequence reads the message back.

The scheme is broken. This file also holds the low density lattice attack of
Lagarias and Odlyzko (1985), which recovers the message from the public key
and the ciphertext alone, with no knowledge of the trapdoor, because the
Merkle-Hellman knapsack has density close to 1/2.

For study only. The code is not constant time, the parameters are toy
parameters, and the attack runs against a local key made in the same process.
Never use this scheme.
"""

import math
from dataclasses import dataclass
from fractions import Fraction

from lll import lll_reduce


class DecryptionError(Exception):
    """The disguised sum was not a sum of a subset of the private sequence."""


def superincreasing_sequence(n: int, rnd) -> list:
    """A random superincreasing sequence of n terms.

    Each term is larger than the sum of all the terms before it, by a random
    gap of up to 2^n. So the last term is near 2^(2n) and the density of the
    knapsack is close to 1/2, which is the shape Merkle and Hellman proposed.
    """
    sequence: list = []
    total = 0
    for _ in range(n):
        term = total + 1 + rnd.randrange(1 << n)
        sequence.append(term)
        total += term
    return sequence


def is_superincreasing(sequence) -> bool:
    """True when every term is larger than the sum of the terms before it."""
    total = 0
    for term in sequence:
        if term <= total:
            return False
        total += term
    return True


def solve_superincreasing(sequence, target: int):
    """The greedy pass: the only subset of a superincreasing sequence that sums to target.

    Walk from the largest term down. A term that is at most what is left must
    be taken, because all the smaller terms together are less than it. Return
    None when no subset sums to the target.
    """
    bits = [0] * len(sequence)
    rest = target
    for index in range(len(sequence) - 1, -1, -1):
        if sequence[index] <= rest:
            bits[index] = 1
            rest -= sequence[index]
    if rest != 0:
        return None
    return bits


@dataclass
class MerkleHellmanKey:
    """A Merkle-Hellman key. The public key is the disguised sequence."""

    sequence: list  # the private superincreasing sequence a
    modulus: int  # m, larger than the sum of the sequence
    multiplier: int  # w, a unit modulo m
    permutation: list  # the public position j holds the private index permutation[j]

    def __post_init__(self) -> None:
        if not is_superincreasing(self.sequence):
            raise ValueError("the private sequence must be superincreasing")
        if self.modulus <= sum(self.sequence):
            raise ValueError("the modulus must exceed the sum of the sequence")
        if math.gcd(self.multiplier, self.modulus) != 1:
            raise ValueError("the multiplier must be a unit modulo the modulus")
        if sorted(self.permutation) != list(range(len(self.sequence))):
            raise ValueError("the permutation must be a permutation of the indices")
        self.inverse = pow(self.multiplier, -1, self.modulus)
        # @line L4
        disguised = [self.multiplier * term % self.modulus for term in self.sequence]
        # @line L5
        self.public_key = [disguised[index] for index in self.permutation]

    @classmethod
    def generate(cls, n: int, rnd) -> "MerkleHellmanKey":
        """A random key with n terms."""
        # @line L1
        sequence = superincreasing_sequence(n, rnd)
        total = sum(sequence)
        # @line L2
        modulus = total + 1 + rnd.randrange(total)
        # @line L3
        multiplier = rnd.randrange(2, modulus)
        while math.gcd(multiplier, modulus) != 1:
            multiplier = rnd.randrange(2, modulus)
        permutation = list(range(n))
        rnd.shuffle(permutation)
        # @line L6
        return cls(
            sequence=sequence,
            modulus=modulus,
            multiplier=multiplier,
            permutation=permutation,
        )


def encrypt(public_key, bits) -> int:
    """Add up the public terms that the message selects."""
    if len(bits) != len(public_key):
        raise ValueError("the message must have one binary digit per public term")
    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("the message must be binary digits")
    # @line L7
    return sum(bit * term for bit, term in zip(bits, public_key))


def decrypt(key: MerkleHellmanKey, ciphertext: int) -> list:
    """Undo the disguise, then read the message with the greedy pass."""
    # @line L8
    target = key.inverse * ciphertext % key.modulus
    # @line L9
    private_bits = solve_superincreasing(key.sequence, target)
    if private_bits is None:
        raise DecryptionError("the disguised sum is not a subset sum of the sequence")
    # @line L10
    return [private_bits[index] for index in key.permutation]


def density(public_key) -> float:
    """The density n / log2(max term). Lattice attacks work below about 0.64."""
    return len(public_key) / math.log2(max(public_key))


def _is_binary_solution(vector, public_key, ciphertext):
    """Check a candidate: all entries in {0, 1} and the subset sum is right."""
    for sign in (1, -1):
        bits = [sign * int(entry) for entry in vector]
        if all(bit in (0, 1) for bit in bits) and encrypt(public_key, bits) == ciphertext:
            return bits
    return None


def low_density_attack(public_key, ciphertext: int, delta=Fraction(99, 100)):
    """The Lagarias-Odlyzko lattice attack, with no knowledge of the trapdoor.

    The message is a short vector of the lattice generated by the rows

        (1, 0, ..., 0, K*b_1)
        (0, 1, ..., 0, K*b_2)
            ...
        (0, 0, ..., 1, K*b_n)
        (0, 0, ..., 0, K*c)

    because the combination that takes b_i with the message digit x_i and the
    last row with coefficient -1 gives (x_1, ..., x_n, 0). Its length is at
    most sqrt(n), while a lattice of this determinant has no other vector that
    short when the density of the knapsack is below about 0.6463. The large
    multiplier K forces every short vector to have a last coordinate of 0, so
    LLL reduction returns the message among its first rows.

    Return the message digits, or None when no row of the reduced basis is a
    binary solution.
    """
    n = len(public_key)
    multiplier = math.isqrt(n) + 1  # K > sqrt(n)/2 is enough for the proof
    basis = []
    for index in range(n):
        row = [0] * (n + 1)
        row[index] = 1
        row[n] = multiplier * public_key[index]
        basis.append(row)
    basis.append([0] * n + [multiplier * ciphertext])
    reduced = lll_reduce(basis, delta)
    for row in reduced:
        if row[n] != 0:
            continue
        found = _is_binary_solution(row[:n], public_key, ciphertext)
        if found is not None:
            return found
    return None
