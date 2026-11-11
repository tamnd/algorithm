# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-only-attack/. The authors are listed in prov/XJ1ZFG.jsonl.
"""Key-only attacks on two schemes that sign without a hash: textbook RSA and
ElGamal on raw integers. The adversary gets the public key and nothing else,
and still outputs a valid (message, signature) pair. It cannot choose the
message: these are existential forgeries.

For study only. The code is not constant time, the attacks run only on toy
parameters against the local verifiers in this file, and nothing here may
protect real data. Use a hashed and padded scheme such as RSA-PSS or Ed25519
from the pyca/cryptography library or from a FIPS 140 validated module.
"""

import hashlib
from math import gcd
from typing import Callable, Optional, Tuple


# Local verifiers -------------------------------------------------------------

def textbook_rsa_verify(n: int, e: int, m: int, s: int) -> bool:
    """Accept s for the integer message m if s^e = m (mod n), with 0 <= m, s < n."""
    return 0 <= m < n and 0 <= s < n and pow(s, e, n) == m


def hashed_rsa_verify(n: int, e: int, message: bytes, s: int) -> bool:
    """A full-domain-hash style check: s^e mod n must equal SHA-256(message) mod n."""
    h = int.from_bytes(hashlib.sha256(message).digest(), "big") % n
    return 0 <= s < n and pow(s, e, n) == h


def raw_elgamal_verify(p: int, g: int, y: int, m: int, sig: Tuple[int, int]) -> bool:
    """ElGamal verification on the integer m itself, with no hash:
    1 <= r <= p - 1, 1 <= s <= p - 2 and y^r * r^s = g^m (mod p)."""
    r, s = sig
    if not (1 <= r <= p - 1 and 1 <= s <= p - 2):
        return False
    return pow(y, r, p) * pow(r, s, p) % p == pow(g, m % (p - 1), p)


# Forgeries that use only the public key -------------------------------------

def forge_textbook_rsa(n: int, e: int, s: int) -> Tuple[int, int]:
    """Pick the signature first, then compute the message it signs: m = s^e mod n."""
    return pow(s, e, n), s


def forge_raw_elgamal(p: int, g: int, y: int, u: int, v: int) -> Tuple[int, Tuple[int, int]]:
    """The one-parameter forgery of ElGamal (1985), see HAC Note 11.66:
    r = g^u y^v mod p, s = -r v^(-1) mod (p - 1), m = s u mod (p - 1).
    Then y^r r^s = y^(r + v s) g^(u s) = g^(u s) = g^m, because r + v s = 0 mod (p - 1)."""
    if gcd(v, p - 1) != 1:
        raise ValueError("v must be invertible modulo p - 1")
    r = pow(g, u, p) * pow(y, v, p) % p
    s = (-r * pow(v, -1, p - 1)) % (p - 1)
    m = s * u % (p - 1)
    return m, (r, s)


# The game ------------------------------------------------------------------

def key_only_game(pk: tuple, verify: Callable[..., bool],
                  adversary: Callable[[tuple], Optional[tuple]]) -> bool:
    """The adversary sees only pk; it wins if its (message, signature) verifies.
    There is no signing oracle, so every valid output is a forgery."""
    out = adversary(pk)
    if out is None:
        return False
    message, signature = out
    return verify(*pk, message, signature)
