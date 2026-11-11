# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elgamal-encryption/. The authors are listed in prov/V93QWB.jsonl.
"""ElGamal encryption in a cyclic group of order q inside Z_p^*.

The intended setting is a safe prime p = 2q + 1 and a generator g of the
subgroup of quadratic residues, which has prime order q. Then a message must
be an element of that subgroup; encode() maps the integers 1 to q into it.
The same code also runs the textbook scheme of Handbook of Applied
Cryptography Algorithm 8.18, where g generates all of Z_p^* and q = p - 1.

For study only. This code is not constant time, it does not hide the length
or the timing of its arithmetic, and it must not be used to protect real
data. Use a FIPS 140 validated module, or libsodium, for real encryption.
"""

import random
import secrets
from dataclasses import dataclass

# The toy group of this page. P_TOY is the smallest safe prime above 2^63:
# a search over q = 2^62, 2^62 + 1, ... for q and 2q + 1 both prime gives
# q = 2^62 + 1339. The tests check both numbers with a deterministic
# Miller-Rabin test. G_TOY = 4 = 2^2 is a square, so it lies in the subgroup
# of order Q_TOY, and it is not 1, so it generates that subgroup.
P_TOY = 9223372036854778487
Q_TOY = 4611686018427389243
G_TOY = 4


@dataclass(frozen=True)
class Group:
    """A cyclic subgroup of Z_p^*: g generates it and q is its order."""

    p: int
    q: int
    g: int


TOY_GROUP = Group(P_TOY, Q_TOY, G_TOY)


@dataclass(frozen=True)
class PublicKey:
    group: Group
    h: int


@dataclass(frozen=True)
class PrivateKey:
    group: Group
    x: int


def _below(n: int, rng: random.Random | None) -> int:
    """A uniform integer in {0, ..., n - 1}, from rng if one is given."""
    return rng.randrange(n) if rng is not None else secrets.randbelow(n)


def is_member(group: Group, a: int) -> bool:
    """True when 1 <= a < p and a lies in the subgroup of order q."""
    return 0 < a < group.p and pow(a, group.q, group.p) == 1


def keygen(group: Group, rng: random.Random | None = None) -> tuple[PublicKey, PrivateKey]:
    """Make a key pair. Cost: one exponentiation modulo p."""
    x = _below(group.q, rng)  # @line L1
    h = pow(group.g, x, group.p)  # @line L2
    return PublicKey(group, h), PrivateKey(group, x)  # @line L3


def encrypt(pk: PublicKey, m: int, r: int | None = None, rng: random.Random | None = None) -> tuple[int, int]:
    """Encrypt a group element m. Cost: two exponentiations modulo p.

    The precondition is that m is in the subgroup. A message outside it is
    refused, because it would leak its quadratic character (CVE-2018-6829).
    """
    grp = pk.group
    if not is_member(grp, m):
        raise ValueError("the message is not an element of the group")
    if r is None:
        r = _below(grp.q, rng)  # @line L4
    c1 = pow(grp.g, r, grp.p)  # @line L5
    c2 = m * pow(pk.h, r, grp.p) % grp.p  # @line L6
    return c1, c2  # @line L7


def decrypt(sk: PrivateKey, c: tuple[int, int]) -> int:
    """Decrypt (c1, c2). Cost: one exponentiation and one multiplication."""
    grp = sk.group
    c1, c2 = c
    if not (is_member(grp, c1) and is_member(grp, c2)):  # @line L8
        raise ValueError("the ciphertext is not a pair of group elements")
    return c2 * pow(c1, grp.q - sk.x, grp.p) % grp.p  # @line L9


def encode(group: Group, m: int) -> int:
    """Map an integer 1 <= m <= q to a quadratic residue modulo a safe prime.

    For p = 2q + 1 with p = 3 (mod 4), -1 is a non-residue, so exactly one of
    m and p - m is a residue. The map is a bijection onto the subgroup.
    """
    if group.p != 2 * group.q + 1 or not 1 <= m <= group.q:
        raise ValueError("encode needs a safe prime group and 1 <= m <= q")
    return m if pow(m, group.q, group.p) == 1 else group.p - m


def decode(group: Group, a: int) -> int:
    """The inverse of encode."""
    return a if a <= group.q else group.p - a


def multiply(group: Group, c: tuple[int, int], d: tuple[int, int]) -> tuple[int, int]:
    """Componentwise product: it encrypts the product of the two messages."""
    return c[0] * d[0] % group.p, c[1] * d[1] % group.p


def rerandomize(pk: PublicKey, c: tuple[int, int], s: int) -> tuple[int, int]:
    """Multiply by an encryption of 1 with randomness s: same message, new look."""
    return multiply(pk.group, c, encrypt(pk, 1, r=s))


def encrypt_exponent(pk: PublicKey, v: int, rng: random.Random | None = None) -> tuple[int, int]:
    """Exponential ElGamal: encrypt g^v, so that products add the plaintexts."""
    return encrypt(pk, pow(pk.group.g, v, pk.group.p), rng=rng)


def decrypt_exponent(sk: PrivateKey, c: tuple[int, int], bound: int) -> int:
    """Decrypt exponential ElGamal when 0 <= v <= bound.

    The last step is a small discrete logarithm. This version uses
    baby-step giant-step: O(sqrt(bound)) multiplications and memory.
    """
    grp = sk.group
    target = decrypt(sk, c)
    m = 1
    while m * m <= bound:
        m += 1
    table = {}
    e = 1
    for j in range(m):
        table.setdefault(e, j)
        e = e * grp.g % grp.p
    step = pow(grp.g, grp.q - m, grp.p)  # g^(-m)
    y = target
    for i in range(m + 1):
        if y in table and i * m + table[y] <= bound:
            return i * m + table[y]
        y = y * step % grp.p
    raise ValueError("the plaintext is not in the range 0 to bound")
