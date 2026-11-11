# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rabin-cryptosystem/. The authors are listed in prov/3WNX9E.jsonl.
"""The Rabin cryptosystem (1979): encryption is squaring modulo a Blum integer.

Encryption is c = m^2 mod N for N = pq with p and q congruent to 3 modulo 4.
Decryption takes the four square roots of c and keeps the one that carries
the agreed redundancy. Breaking the scheme is provably as hard as factoring
N, and the proof is a program: a decryption oracle gives a factor of N with
probability 1/2 for each query it answers. That same program is a chosen
ciphertext attack, so Rabin encryption must never be used bare.

The file holds the key generation, the encoding with a redundancy tag,
encryption, decryption, the four roots, and the factoring reduction.

For study only. The code is not constant time, the keys are toy keys, and
the attack runs against a local oracle in the same process.
"""

import hashlib
import math
from dataclasses import dataclass

TAG_BYTES = 2  # the redundancy: 16 binary digits of a hash of the message


class DecryptionError(Exception):
    """No root of the ciphertext carried a valid redundancy tag."""


def is_probable_prime(n: int, rounds: int = 24) -> bool:
    """Miller-Rabin with fixed bases, enough for the toy primes of this page."""
    if n < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    for p in small:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in small[:rounds]:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def random_blum_prime(bits: int, rnd) -> int:
    """A prime congruent to 3 modulo 4, with the top bit set."""
    while True:
        candidate = rnd.randrange(1 << (bits - 1), 1 << bits) | 1
        candidate += (3 - candidate % 4) % 4  # move to 3 mod 4
        if candidate.bit_length() == bits and is_probable_prime(candidate):
            return candidate


@dataclass
class RabinKey:
    """A Rabin key. N is public; p and q are the trapdoor."""

    p: int
    q: int

    def __post_init__(self) -> None:
        if self.p % 4 != 3 or self.q % 4 != 3:
            raise ValueError("both primes must be 3 modulo 4")
        if self.p == self.q:
            raise ValueError("the two primes must differ")
        # @line L3
        self.n = self.p * self.q
        self.p_inverse = pow(self.p, -1, self.q)
        self.q_inverse = pow(self.q, -1, self.p)

    @classmethod
    def generate(cls, bits: int, rnd) -> "RabinKey":
        """Two Blum primes of bits/2 binary digits each."""
        half = bits // 2
        # @line L1
        p = random_blum_prime(half, rnd)
        # @line L2
        q = random_blum_prime(half, rnd)
        while q == p:
            q = random_blum_prime(half, rnd)
        return cls(p=p, q=q)

    @property
    def public(self) -> int:
        return self.n


def encode(message: bytes) -> int:
    """Add the redundancy that picks one root out of four.

    The integer is 0x01 || message || tag, where tag is the first TAG_BYTES
    octets of SHA-256 of the message. The leading octet fixes the length,
    and the tag makes a wrong root pass with probability about 2^-16.
    Rabin's paper repeats a block of the message instead; a hash tag is the
    modern form of the same idea.
    """
    tag = hashlib.sha256(message).digest()[:TAG_BYTES]
    return int.from_bytes(b"\x01" + message + tag, "big")


def decode(value: int):
    """Undo encode, or return None when the redundancy does not check."""
    if value <= 0:
        return None
    data = value.to_bytes((value.bit_length() + 7) // 8, "big")
    if len(data) < 1 + TAG_BYTES or data[0] != 1:
        return None
    message, tag = data[1:-TAG_BYTES], data[-TAG_BYTES:]
    if hashlib.sha256(message).digest()[:TAG_BYTES] != tag:
        return None
    return message


def max_message_length(n: int) -> int:
    """The longest message that fits: the encoded integer must be below N."""
    return (n.bit_length() - 1) // 8 - 1 - TAG_BYTES


def encrypt(n: int, message: bytes) -> int:
    """Rabin encryption: square the encoded message modulo N."""
    # @line L4
    m = encode(message)
    if m >= n:
        raise ValueError("the message is too long for this modulus")
    # @line L5
    return m * m % n


def square_roots(key: RabinKey, c: int) -> list:
    """The four square roots of c modulo N = pq, for a Blum integer N.

    Because p and q are 3 modulo 4, a root modulo p is c^((p+1)/4) mod p,
    and likewise modulo q. The Chinese remainder theorem glues the two
    choices of sign into four roots.
    """
    # @line L6
    root_p = pow(c % key.p, (key.p + 1) // 4, key.p)
    # @line L7
    root_q = pow(c % key.q, (key.q + 1) // 4, key.q)
    # @line L8
    weight_p = key.q * key.q_inverse % key.n
    weight_q = key.p * key.p_inverse % key.n
    # @line L9
    first = (weight_p * root_p + weight_q * root_q) % key.n
    second = (weight_p * root_p - weight_q * root_q) % key.n
    # @line L10
    roots = {first, key.n - first, second, key.n - second}
    return sorted(root for root in roots if root * root % key.n == c % key.n)


def decrypt(key: RabinKey, c: int) -> bytes:
    """Rabin decryption: take the four roots and keep the one with the tag."""
    # @line L11
    for root in square_roots(key, c):
        message = decode(root)
        if message is not None:
            return message
    # @line L12
    raise DecryptionError("no root carried a valid redundancy tag")


@dataclass
class RootOracle:
    """A decryption oracle for the bare squaring map, as the proof assumes.

    On a ciphertext c that is a quadratic residue it returns one square
    root. Which one is its own business; this one answers with a uniform
    choice among the four, which is the worst case for the attacker and the
    case the reduction is stated for.
    """

    key: RabinKey
    rnd: object
    queries: int = 0

    def __call__(self, c: int) -> int:
        self.queries += 1
        roots = square_roots(self.key, c)
        if not roots:
            raise DecryptionError("not a quadratic residue")
        return self.rnd.choice(roots)


def factor_with_root_oracle(n: int, oracle, rnd, tries: int = 64):
    """The reduction: an oracle that extracts square roots factors N.

    Draw x, ask for a root y of x^2 mod N. The four roots are x, -x and two
    others; the two others give gcd(x - y, N) in {p, q}. So each query
    succeeds with probability 1/2 when the oracle answers uniformly, and
    the expected number of queries is 2.
    """
    for _ in range(tries):
        x = rnd.randrange(2, n - 1)
        if math.gcd(x, n) != 1:
            return math.gcd(x, n), n // math.gcd(x, n)  # a free factor, never happens
        y = oracle(x * x % n)
        if y in (x, n - x):
            continue  # this query told us nothing
        factor = math.gcd(x - y, n)
        if 1 < factor < n:
            return factor, n // factor
    return None


def chosen_ciphertext_attack(n: int, oracle, rnd, target: int):
    """Decrypt a target ciphertext without ever sending it to the oracle.

    The attacker factors N with the reduction above, rebuilds the private
    key, and decrypts. This is why bare Rabin encryption is not secure
    against chosen ciphertext attacks: the proof of security against a
    passive attacker is itself the active attack.
    """
    found = factor_with_root_oracle(n, oracle, rnd)
    if found is None:
        return None
    p, q = found
    return decrypt(RabinKey(p=p, q=q), target), (p, q)
