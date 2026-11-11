# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/designated-verifier-signature/. The authors are listed in prov/FAQZXV.jsonl.
"""A designated verifier signature from a Schnorr OR proof.

The signer S has y_s = g^x_s and the designated verifier V has y_v = g^x_v.
A signature on m is a Fiat-Shamir proof of the statement

    "I know x_s  OR  I know x_v"

made with the Cramer-Damgard-Schoenmakers OR technique: the signer answers
the S branch with its key and simulates the V branch. V knows that V did not
make it, so V is convinced that S signed. Anyone else sees a proof that S or
V made it, and V can make one as easily as S (see simulate). So V cannot use
the signature to convince a third party.

This is the two-key OR-proof form; Jakobsson, Sako and Impagliazzo proved
"this undeniable signature is valid OR I know x_v" instead.

The group is a toy: p = 2039 = 2q + 1, q = 1019, and g = 4 generates the
subgroup of order q. For study only: the code is not constant time and the
parameters give no security.
"""

import hashlib
import random
import secrets
from dataclasses import dataclass

P, Q, G = 2039, 1019, 4


def h(y_s: int, y_v: int, msg: bytes, t_s: int, t_v: int) -> int:
    data = b"DVS|%d|%d|" % (y_s, y_v) + msg + b"|%d|%d" % (t_s, t_v)
    return int.from_bytes(hashlib.sha256(data).digest(), "big") % Q


def keygen(rng: random.Random | None = None) -> tuple[int, int]:
    rng = rng or secrets.SystemRandom()
    x = rng.randrange(1, Q)
    return x, pow(G, x, P)


def in_group(y: int) -> bool:
    return 1 < y < P and pow(y, Q, P) == 1


@dataclass(frozen=True)
class Signature:
    c_s: int
    c_v: int
    z_s: int
    z_v: int


def sign(x_s: int, y_v: int, msg: bytes, coins: tuple[int, int, int] | None = None) -> Signature:
    """S signs msg for the designated verifier y_v. coins = (k, c_v, z_v)."""
    y_s = pow(G, x_s, P)
    k, c_v, z_v = coins if coins is not None else (secrets.randbelow(Q) for _ in range(3))  # @line L1
    t_s = pow(G, k, P)  # @line L2
    t_v = pow(G, z_v, P) * pow(y_v, c_v, P) % P
    c = h(y_s, y_v, msg, t_s, t_v)  # @line L3
    c_s = (c - c_v) % Q  # @line L4
    z_s = (k - c_s * x_s) % Q
    return Signature(c_s, c_v, z_s, z_v)  # @line L5


def verify(y_s: int, y_v: int, msg: bytes, sig: Signature) -> bool:
    if not (in_group(y_s) and in_group(y_v) and y_s != y_v):
        return False
    if not all(0 <= v < Q for v in (sig.c_s, sig.c_v, sig.z_s, sig.z_v)):
        return False
    t_s = pow(G, sig.z_s, P) * pow(y_s, sig.c_s, P) % P  # @line L6
    t_v = pow(G, sig.z_v, P) * pow(y_v, sig.c_v, P) % P
    return (sig.c_s + sig.c_v) % Q == h(y_s, y_v, msg, t_s, t_v)  # @line L7


def simulate(y_s: int, x_v: int, msg: bytes, coins: tuple[int, int, int] | None = None) -> Signature:
    """V makes a valid "signature of S" alone, with its own key. coins = (k, c_s, z_s)."""
    y_v = pow(G, x_v, P)
    k, c_s, z_s = coins if coins is not None else (secrets.randbelow(Q) for _ in range(3))
    t_s = pow(G, z_s, P) * pow(y_s, c_s, P) % P  # @line L8
    t_v = pow(G, k, P)
    c_v = (h(y_s, y_v, msg, t_s, t_v) - c_s) % Q  # @line L9
    return Signature(c_s, c_v, z_s, (k - c_v * x_v) % Q)


def signer_coins(sig: Signature, x_s: int) -> tuple[int, int, int]:
    """The coins with which S would have output sig."""
    return (sig.z_s + sig.c_s * x_s) % Q, sig.c_v, sig.z_v


def simulator_coins(sig: Signature, x_v: int) -> tuple[int, int, int]:
    """The coins with which V's simulator would have output sig."""
    return (sig.z_v + sig.c_v * x_v) % Q, sig.c_s, sig.z_s
