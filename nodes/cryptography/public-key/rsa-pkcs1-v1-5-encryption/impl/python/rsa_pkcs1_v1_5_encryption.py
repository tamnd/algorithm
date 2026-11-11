# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-pkcs1-v1-5-encryption/. The authors are listed in prov/GMTEEK.jsonl.
"""RSAES-PKCS1-v1_5 encryption and Bleichenbacher's chosen ciphertext attack.

The encoding and the two operations follow RFC 8017 (PKCS #1 v2.2)
Section 7.2. The attack follows Bleichenbacher (CRYPTO 1998) and runs only
against the local simulated oracle in this file, on a toy key that the test
file makes.

For study only. This code is not constant time, and it must not be used to
protect real data. RFC 8017 Section 7 says that new applications must use
RSAES-OAEP. The attack code is here to show why.
"""

import math
import secrets
from dataclasses import dataclass, field


class DecryptionError(Exception):
    """Raised for every malformed ciphertext, as RFC 8017 Section 7.2.2 asks."""


def i2osp(value: int, length: int) -> bytes:
    """Integer to octet string, RFC 8017 Section 4.1."""
    if value < 0 or value >= 1 << (8 * length):
        raise ValueError("integer too large")
    return value.to_bytes(length, "big")


def os2ip(data: bytes) -> int:
    """Octet string to integer, RFC 8017 Section 4.2."""
    return int.from_bytes(data, "big")


def modulus_length(n: int) -> int:
    """The length k of the modulus in octets."""
    return (n.bit_length() + 7) // 8


def eme_pkcs1_v1_5_encode(message: bytes, k: int, rand_nonzero=None) -> bytes:
    """EM = 0x00 || 0x02 || PS || 0x00 || M, with PS of nonzero octets.

    RFC 8017 Section 7.2.1 steps 1 and 2. PS has k - mLen - 3 octets, so it
    has at least eight octets, and every octet of PS is nonzero.
    """
    if rand_nonzero is None:
        rand_nonzero = _secure_nonzero
    if k < 11:
        raise ValueError("modulus too short")
    if len(message) > k - 11:  # @line L1
        raise ValueError("message too long")
    ps = rand_nonzero(k - len(message) - 3)  # @line L2
    if len(ps) != k - len(message) - 3 or 0 in ps:
        raise ValueError("the padding string must have no zero octet")
    return b"\x00\x02" + ps + b"\x00" + message  # @line L3


def eme_pkcs1_v1_5_decode(em: bytes) -> bytes:
    """Undo the encoding, or raise DecryptionError.

    RFC 8017 Section 7.2.2 step 3. The three failures (a wrong first pair, no
    zero separator, and a padding string below eight octets) must not be told
    apart by the caller.
    """
    if len(em) < 11 or em[0] != 0x00 or em[1] != 0x02:  # @line L9
        raise DecryptionError("decryption error")
    separator = em.find(b"\x00", 2)  # @line L10
    if separator < 10:  # @line L11
        raise DecryptionError("decryption error")
    return em[separator + 1:]  # @line L12


def encrypt(n: int, e: int, message: bytes, rand_nonzero=None) -> bytes:
    """RSAES-PKCS1-V1_5-ENCRYPT, RFC 8017 Section 7.2.1."""
    k = modulus_length(n)
    em = eme_pkcs1_v1_5_encode(message, k, rand_nonzero)  # @line L4
    m = os2ip(em)  # @line L5
    return i2osp(pow(m, e, n), k)  # @line L6


def decrypt(n: int, d: int, ciphertext: bytes) -> bytes:
    """RSAES-PKCS1-V1_5-DECRYPT, RFC 8017 Section 7.2.2."""
    k = modulus_length(n)
    if len(ciphertext) != k or k < 11:  # @line L7
        raise DecryptionError("decryption error")
    em = i2osp(pow(os2ip(ciphertext), d, n), k)  # @line L8
    return eme_pkcs1_v1_5_decode(em)


def _secure_nonzero(count: int) -> bytes:
    """count nonzero octets from the system random source."""
    out = bytearray()
    while len(out) < count:
        out.extend(b for b in secrets.token_bytes(count) if b != 0)
    return bytes(out[:count])


def nonzero_from_random(rnd, count: int) -> bytes:
    """count nonzero octets from a random.Random, for repeatable tests."""
    return bytes(rnd.randrange(1, 256) for _ in range(count))


# ---------------------------------------------------------------------------
# A local simulated padding oracle and Bleichenbacher's attack on it.
# Both run only on the toy keys that the test file makes.
# ---------------------------------------------------------------------------


@dataclass
class SimulatedOracle:
    """A server that leaks whether the first two octets of EM are 0x00 0x02.

    This is the oracle of Bleichenbacher's paper, Section 3. A real server
    leaks it through an error message, an alert code or a timing difference.
    """

    n: int
    d: int
    limit: int = 1 << 22
    queries: int = 0
    strict: bool = False
    log: list = field(default_factory=list)

    def __call__(self, ciphertext: int) -> bool:
        if self.queries >= self.limit:
            raise RuntimeError("the query budget is used up")
        self.queries += 1
        k = modulus_length(self.n)
        em = i2osp(pow(ciphertext, self.d, self.n), k)
        if em[0] != 0x00 or em[1] != 0x02:
            return False
        if not self.strict:
            return True
        separator = em.find(b"\x00", 2)
        return separator >= 10


def is_conforming(oracle, n: int, e: int, c0: int, s: int) -> bool:
    """Ask the oracle about c0 * s^e mod n."""
    return oracle(c0 * pow(s, e, n) % n)


def narrow(intervals, s: int, n: int, big_b: int):
    """Step 3 of the attack: keep the m values that agree with a conforming s.

    A conforming s means 2B <= m*s - r*n < 3B for some integer r, so for each
    old interval [a, b] and each possible r the new bounds are
    max(a, ceil((2B + r*n)/s)) and min(b, floor((3B - 1 + r*n)/s)).
    """
    out = []
    for a, b in intervals:
        r_low = -((-(a * s - 3 * big_b + 1)) // n)
        r_high = (b * s - 2 * big_b) // n
        for r in range(r_low, r_high + 1):
            low = max(a, -((-(2 * big_b + r * n)) // s))
            high = min(b, (3 * big_b - 1 + r * n) // s)
            if low <= high:
                out.append((low, high))
    out.sort()
    merged = []
    for interval in out:
        if merged and interval[0] <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
        else:
            merged.append(interval)
    return merged


def bleichenbacher_attack(n: int, e: int, ciphertext: bytes, oracle, trace=None) -> bytes:
    """Recover the padded message of a conforming ciphertext from oracle answers.

    The four steps are those of Bleichenbacher (CRYPTO 1998), Section 3.1:

    1. Blind the ciphertext. Here c0 comes from the sender, so it is already
       conforming and the blinding step is the identity with s0 = 1.
    2a. Search s from ceil(n / (3B)) upward for one conforming value.
    2b. With more than one interval left, keep increasing s.
    2c. With one interval [a, b] left, pick r >= 2*(b*s - 2B)/n and search s
        in [ceil((2B + r*n)/b), floor((3B + r*n)/a)].
    3.  Narrow the interval set with every conforming s.
    4.  Stop when one value is left, and return it as EM.

    This is an adaptive chosen ciphertext attack. It needs about one million
    queries for a 1024 bit key, and much fewer for the toy key of the test.
    """
    k = modulus_length(n)
    big_b = 1 << (8 * (k - 2))
    c0 = os2ip(ciphertext)
    if not oracle(c0):
        raise ValueError("the given ciphertext is not conforming")
    s = -(-n // (3 * big_b))
    while not is_conforming(oracle, n, e, c0, s):
        s += 1
    intervals = narrow([(2 * big_b, 3 * big_b - 1)], s, n, big_b)
    step = 0
    while True:
        step += 1
        if trace is not None:
            width = sum(b - a + 1 for a, b in intervals)
            trace.append((step, s, len(intervals), width))
        if len(intervals) == 1 and intervals[0][0] == intervals[0][1]:
            return i2osp(intervals[0][0], k)
        if len(intervals) > 1:
            s += 1
            while not is_conforming(oracle, n, e, c0, s):
                s += 1
        else:
            a, b = intervals[0]
            r = -((-2 * (b * s - 2 * big_b)) // n)
            found = False
            while not found:
                low = -((-(2 * big_b + r * n)) // b)
                high = (3 * big_b + r * n) // a
                for candidate in range(low, high + 1):
                    if is_conforming(oracle, n, e, c0, candidate):
                        s, found = candidate, True
                        break
                r += 1
        intervals = narrow(intervals, s, n, big_b)


@dataclass(frozen=True)
class ToyKey:
    """A toy RSA key. Far too small for any real use."""

    n: int
    e: int
    d: int

    @property
    def k(self) -> int:
        return modulus_length(self.n)


def toy_key(p: int, q: int, e: int = 65537) -> ToyKey:
    """Build a toy key from two given primes."""
    n = p * q
    lam = (p - 1) * (q - 1) // math.gcd(p - 1, q - 1)
    if math.gcd(e, lam) != 1:
        raise ValueError("e is not invertible")
    return ToyKey(n=n, e=e, d=pow(e, -1, lam))
