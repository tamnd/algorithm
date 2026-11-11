# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diffie-hellman/. The authors are listed in prov/65FYHX.jsonl.
"""Finite field Diffie-Hellman key exchange in a safe-prime group.

The group is the 2048-bit MODP group of RFC 3526 Section 3 (group 14):
p is a safe prime, p = 2q + 1 with q prime, and g = 2 generates the
subgroup of order q (the quadratic residues mod p, since p = 7 mod 8).
Each party picks a secret exponent, sends g^x mod p, checks the value it
gets back, and raises it to its own secret.

For study only. The code is not constant time (Python's pow and integers
leak timing), and plain Diffie-Hellman has no authentication. Do not use it
to protect real data. Use the X25519 or ECDH of a maintained library
(libsodium, OpenSSL, the Python package cryptography) or a FIPS 140
validated module instead.

Cost: one exponentiation mod p for the key pair and one for the shared
value, each about m squarings and m/2 multiplications of m-bit numbers for
an m-bit exponent; the subgroup check costs one more exponentiation.
"""

import random
import secrets
from typing import Optional

# RFC 3526 Section 3, the 2048-bit MODP group, copied by hand.
# p = 2^2048 - 2^1984 - 1 + 2^64 * ( [2^1918 pi] + 124476 )
P_HEX = (
    "FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1"
    "29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD"
    "EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245"
    "E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED"
    "EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D"
    "C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F"
    "83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D"
    "670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B"
    "E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9"
    "DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510"
    "15728E5A 8AACAA68 FFFFFFFF FFFFFFFF"
)
P = int(P_HEX.replace(" ", ""), 16)
G = 2
Q = (P - 1) // 2
SIZE = 256  # bytes in an element of the group


class ValidationError(ValueError):
    """A public value failed the check, or the shared value is 1."""


def generate_key_pair(rng: Optional[random.Random] = None) -> tuple[int, int]:
    """A secret exponent x uniform in [1, q - 1] and the public value g^x mod p."""
    r = rng or secrets.SystemRandom()
    x = r.randrange(1, Q)  # @line L1
    big_x = pow(G, x, P)  # @line L2
    return x, big_x  # @line L3


def validate_public_value(y: int) -> None:
    """Full public key validation for a safe-prime group (SP 800-56A Rev. 3, 5.6.2.3.1).

    The value must lie in [2, p - 2] and in the subgroup of order q.
    """
    if not 2 <= y <= P - 2:
        raise ValidationError("the public value is out of range")
    if pow(y, Q, P) != 1:
        raise ValidationError("the public value is not in the subgroup of order q")


def shared_secret(x: int, y: int) -> bytes:
    """The shared value Z = y^x mod p as 256 big-endian bytes (SP 800-56A Rev. 3, 5.7.1.1).

    The caller gives its own secret x and the peer's public value y.
    """
    if not 2 <= y <= P - 2:  # @line L4
        raise ValidationError("the public value is out of range")
    if pow(y, Q, P) != 1:  # @line L5
        raise ValidationError("the public value is not in the subgroup of order q")
    z = pow(y, x, P)  # @line L6
    if z == 1:  # @line L7
        raise ValidationError("the shared value is 1")
    return z.to_bytes(SIZE, "big")  # @line L8
