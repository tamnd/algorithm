# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/undeniable-signature/. The authors are listed in prov/PHAD4A.jsonl.
"""The Chaum-van Antwerpen undeniable signature in a prime-order subgroup.

The signer has secret a and public y = g^a. A message is hashed to h in the
subgroup of order q, and the signature is s = h^a. Nobody can check s alone:

    confirm:  V sends c = s^e1 * y^e2, S answers d = c^(a^-1 mod q),
              V accepts if d = h^e1 * g^e2.
    disavow:  two rounds of the same with fresh (e1, e2) and (f1, f2), both
              failing; V concludes "forgery" if
              (d * g^-e2)^f1 = (D * g^-f2)^e1, and "the signer cheated" if not.

This is the basic protocol as given in textbooks (for example Stinson). It is
not zero knowledge against a dishonest verifier; Chaum's 1990 version adds
commitments for that.

The group is a toy: p = 2039 = 2q + 1, q = 1019, and g = 4 generates the
subgroup of order q (the squares mod p). For study only: the code is not
constant time, the parameters give no security, and the signer is simulated
by a local function.
"""

import hashlib
import random
import secrets
from collections.abc import Callable

P, Q, G = 2039, 1019, 4

Responder = Callable[[int], int]


def hash_to_group(msg: bytes) -> int:
    """Map msg to a square mod p other than 1, so it has order q."""
    u = int.from_bytes(hashlib.sha256(b"UNDENIABLE|" + msg).digest(), "big") % (P - 3) + 2
    return u * u % P


def keygen(rng: random.Random | None = None) -> tuple[int, int]:
    rng = rng or secrets.SystemRandom()
    a = rng.randrange(1, Q)
    return a, pow(G, a, P)


def sign(a: int, msg: bytes) -> int:
    h = hash_to_group(msg)  # @line L1
    return pow(h, a, P)  # @line L2


def honest_signer(a: int) -> Responder:
    a_inv = pow(a, -1, Q)
    return lambda c: pow(c, a_inv, P)  # @line L4


def _round(y: int, s: int, respond: Responder, rng: random.Random) -> tuple[int, int, int]:
    e1, e2 = rng.randrange(1, Q), rng.randrange(1, Q)
    c = pow(s, e1, P) * pow(y, e2, P) % P
    return e1, e2, respond(c)


def confirm(y: int, msg: bytes, s: int, respond: Responder, rng: random.Random | None = None) -> bool:
    """V's side of the confirmation protocol: True if S proved s valid."""
    rng = rng or secrets.SystemRandom()
    h = hash_to_group(msg)
    e1, e2, d = _round(y, s, respond, rng)  # @line L3
    return d == pow(h, e1, P) * pow(G, e2, P) % P  # @line L5


def disavow(y: int, msg: bytes, s: int, respond: Responder, rng: random.Random | None = None) -> str:
    """V's side of the disavowal protocol.

    Returns "valid" if S's answers match a valid signature, "forgery" if S
    proved that s is not its signature, and "signer cheated" if S tried to
    deny a valid signature.
    """
    rng = rng or secrets.SystemRandom()
    h = hash_to_group(msg)
    e1, e2, d = _round(y, s, respond, rng)  # @line L6
    if d == pow(h, e1, P) * pow(G, e2, P) % P:  # @line L7
        return "valid"
    f1, f2, D = _round(y, s, respond, rng)  # @line L8
    if D == pow(h, f1, P) * pow(G, f2, P) % P:  # @line L9
        return "valid"
    left = pow(d * pow(G, -e2, P) % P, f1, P)  # @line L10
    right = pow(D * pow(G, -f2, P) % P, e1, P)
    return "forgery" if left == right else "signer cheated"
