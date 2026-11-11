# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-cryptosystem/. The authors are listed in prov/D5K7RQ.jsonl.
"""Textbook RSA: key generation, the encryption primitive and CRT decryption.

The key format follows RFC 8017 (PKCS #1 v2.2) Section 3, and the CRT
decryption follows Section 5.1.2. The attack helpers at the end work only on
toy parameters and show why textbook RSA needs a padding scheme.

For study only. This code is not constant time, it has no blinding, and it
must not be used to protect real data. Use a FIPS 140 validated module, or
the RSA code of libsodium or of your platform's standard library.
"""

import math
import secrets
from dataclasses import dataclass

_SMALL_PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)


@dataclass(frozen=True)
class PublicKey:
    """An RSA public key (n, e)."""

    n: int
    e: int


@dataclass(frozen=True)
class PrivateKey:
    """An RSA private key with both representations of RFC 8017 Section 3.2."""

    n: int
    e: int
    d: int
    p: int
    q: int
    dp: int
    dq: int
    qinv: int

    def public(self) -> PublicKey:
        return PublicKey(self.n, self.e)


def is_probable_prime(n: int, rounds: int = 40, randbelow=secrets.randbelow) -> bool:
    """Miller-Rabin test with `rounds` random bases. One-sided: a composite passes
    one round with probability at most 1/4. Cost: O(rounds * log n) modular
    multiplications on numbers of log n bits."""
    if n < 2:
        return False
    for p in (2,) + _SMALL_PRIMES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        a = 2 + randbelow(n - 3)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def random_prime(bits: int, randbits=secrets.randbits, randbelow=secrets.randbelow) -> int:
    """A random probable prime with exactly `bits` bits. Expected cost: O(bits)
    candidates by the prime number theorem, each with a Miller-Rabin test."""
    if bits < 8:
        raise ValueError("use at least 8 bits")
    while True:
        cand = randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(cand, randbelow=randbelow):
            return cand


def generate_key(
    bits: int = 2048, e: int = 65537, randbits=secrets.randbits, randbelow=secrets.randbelow
) -> PrivateKey:
    """Generate an RSA key with a modulus of exactly `bits` bits.

    Precondition: bits >= 16 and e is odd and at least 3. The two primes have
    ceil(bits/2) and floor(bits/2) bits, so n has bits or bits - 1 bits; the
    loop keeps only the keys with exactly `bits` bits. Cost: the prime search
    dominates. The default e = 65537 makes encryption 17 squarings and
    multiplications.
    """
    if bits < 16 or e < 3 or e % 2 == 0:
        raise ValueError("bits >= 16 and an odd e >= 3 are needed")
    while True:  # @line L1
        p = random_prime(bits - bits // 2, randbits, randbelow)  # @line L2
        q = random_prime(bits // 2, randbits, randbelow)  # @line L2
        if p == q or math.gcd(e, (p - 1) * (q - 1)) != 1:  # @line L3
            continue
        n = p * q  # @line L4
        if n.bit_length() != bits:  # @line L3
            continue
        lam = (p - 1) * (q - 1) // math.gcd(p - 1, q - 1)  # @line L4
        d = pow(e, -1, lam)  # @line L5
        dp, dq = d % (p - 1), d % (q - 1)  # @line L6
        qinv = pow(q, -1, p)  # @line L6
        return PrivateKey(n, e, d, p, q, dp, dq, qinv)  # @line L7


def encrypt(pk: PublicKey, m: int) -> int:
    """RSAEP of RFC 8017 Section 5.1.1: c = m^e mod n for 0 <= m < n.
    Cost: O(log e) modular multiplications. This is textbook RSA: it is
    deterministic, so it is not IND-CPA. Use OAEP for real messages."""
    if not 0 <= m < pk.n:
        raise ValueError("message representative out of range")
    return pow(m, pk.e, pk.n)  # @line L8


def decrypt(sk: PrivateKey, c: int) -> int:
    """RSADP of RFC 8017 Section 5.1.2 with the CRT quintuple (p, q, dP, dQ, qInv).
    Cost: two exponentiations modulo a half-size prime, about 4 times faster
    than one exponentiation modulo n."""
    if not 0 <= c < sk.n:
        raise ValueError("ciphertext representative out of range")
    m1 = pow(c, sk.dp, sk.p)  # @line L9
    m2 = pow(c, sk.dq, sk.q)  # @line L10
    h = (m1 - m2) * sk.qinv % sk.p  # @line L11
    return m2 + sk.q * h  # @line L12


def decrypt_single_exponent(sk: PrivateKey, c: int) -> int:
    """The first form of RFC 8017 Section 5.1.2: m = c^d mod n."""
    if not 0 <= c < sk.n:
        raise ValueError("ciphertext representative out of range")
    return pow(c, sk.d, sk.n)


def i2osp(x: int, length: int) -> bytes:
    """Integer to octet string, RFC 8017 Section 4.1."""
    if x < 0 or x >= 1 << (8 * length):
        raise ValueError("integer too large")
    return x.to_bytes(length, "big")


def os2ip(data: bytes) -> int:
    """Octet string to integer, RFC 8017 Section 4.2."""
    return int.from_bytes(data, "big")


def integer_root(a: int, k: int) -> int:
    """The largest integer r with r^k <= a, for a >= 0 and k >= 1, by binary search."""
    if a < 0 or k < 1:
        raise ValueError("a >= 0 and k >= 1 are needed")
    if a < 2:
        return a
    lo, hi = 1, 1 << (a.bit_length() // k + 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid**k <= a:
            lo = mid
        else:
            hi = mid - 1
    return lo


def cube_root_attack(pk: PublicKey, c: int) -> int | None:
    """Recover m from c = m^3 mod n when m^3 < n (no padding, small message).
    Returns None when the cube root is not exact. Toy attack, local data only."""
    if pk.e != 3:
        raise ValueError("this attack needs e = 3")
    r = integer_root(c, 3)
    return r if r**3 == c else None


def crt_combine(residues: list[int], moduli: list[int]) -> int:
    """The unique x in [0, prod) with x = residues[i] mod moduli[i], for pairwise
    coprime moduli. Garner style, one step for each modulus."""
    x, m = residues[0] % moduli[0], moduli[0]
    for r, n in zip(residues[1:], moduli[1:]):
        if math.gcd(m, n) != 1:
            raise ValueError("the moduli must be pairwise coprime")
        x += m * ((r - x) * pow(m, -1, n) % n)
        m *= n
    return x


def hastad_broadcast_attack(keys: list[PublicKey], ciphertexts: list[int]) -> int | None:
    """Hastad's broadcast attack for e = 3: the same m, below each modulus, sent to
    three or more keys with the same small e. The CRT gives m^e modulo the product,
    and m^e is below the product, so an exact integer root gives m.
    Toy attack, local data only."""
    e = keys[0].e
    if len(keys) < e or any(k.e != e for k in keys):
        raise ValueError("this attack needs at least e keys with the same exponent e")
    x = crt_combine(ciphertexts[:e], [k.n for k in keys[:e]])
    r = integer_root(x, e)
    return r if r**e == x else None
