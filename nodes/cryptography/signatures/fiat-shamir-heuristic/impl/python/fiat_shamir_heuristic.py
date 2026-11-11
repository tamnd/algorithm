# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fiat-shamir-heuristic/. The authors are listed in prov/PWQQZB.jsonl.
"""The Fiat-Shamir transform on a toy group, in its strong and weak forms.

Two sigma protocols are made non-interactive here:
- the Schnorr proof of knowledge of x = log_g y, and
- the Chaum-Pedersen proof that log_g u = log_h v (a proof of equal logarithms).
The strong form hashes the statement and the commitment. The weak form hashes
only the commitment. The module also holds the two attacks of the page on the
weak form: a valid proof for a false Chaum-Pedersen statement, and the move of
a Schnorr signature from one key to a related key when the key is not hashed.

For study only. The group has order 1019, which offers no security at all, and
the code is not constant time. Do not use it to protect real data. Real proof
systems should use a vetted library and a transcript object that hashes every
public input, for example the Merlin or the Strobe based transcripts.
"""

import hashlib

# p = 2q + 1, and g, h are squares, so both have order q.
P = 2039
Q = 1019
G = 4
H = 9


def challenge(*items: object) -> int:
    """Hash a list of integers and byte strings to Z_q, with a length prefix for each item."""
    data = b""
    for item in items:
        raw = item if isinstance(item, bytes) else str(item).encode()
        data += len(raw).to_bytes(4, "big") + raw
    return int.from_bytes(hashlib.sha256(data).digest(), "big") % Q


def in_group(a: int) -> bool:
    return 1 <= a < P and pow(a, Q, P) == 1


# ---------------------------------------------------------- Schnorr proof
def prove_dlog(x: int, k: int, strong: bool = True) -> tuple[int, int]:
    """Non-interactive proof of knowledge of x for y = g^x. k is the fresh nonce."""
    y = pow(G, x, P)
    r = pow(G, k, P)  # @line L1
    c = challenge(G, y, r) if strong else challenge(r)  # @line L2
    return r, (k + c * x) % Q  # @line L3


def verify_dlog(y: int, proof: tuple[int, int], strong: bool = True) -> bool:
    r, s = proof
    if not (in_group(y) and in_group(r) and 0 <= s < Q):
        return False
    c = challenge(G, y, r) if strong else challenge(r)  # @line L4
    return pow(G, s, P) == r * pow(y, c, P) % P  # @line L5


# ---------------------------------------------------- Chaum-Pedersen proof
def prove_dleq(w: int, k: int, strong: bool = True) -> tuple[tuple[int, int], tuple[int, int, int]]:
    """Prove log_g u = log_h v = w. Returns the statement (u, v) and the proof (a1, a2, s)."""
    u, v = pow(G, w, P), pow(H, w, P)
    a1, a2 = pow(G, k, P), pow(H, k, P)
    c = challenge(G, H, u, v, a1, a2) if strong else challenge(a1, a2)
    return (u, v), (a1, a2, (k + c * w) % Q)


def verify_dleq(u: int, v: int, proof: tuple[int, int, int], strong: bool = True) -> bool:
    a1, a2, s = proof
    if not all(in_group(z) for z in (u, v, a1, a2)) or not 0 <= s < Q:
        return False
    c = challenge(G, H, u, v, a1, a2) if strong else challenge(a1, a2)
    return pow(G, s, P) == a1 * pow(u, c, P) % P and pow(H, s, P) == a2 * pow(v, c, P) % P


def forge_weak_dleq(alpha: int, beta: int, s: int) -> tuple[tuple[int, int], tuple[int, int, int]]:
    """Forge a weak Fiat-Shamir proof for a statement (u, v) with log_g u != log_h v.

    Fix the commitments first, hash them, and only then choose the statement
    that makes the two verification equations hold. Needs alpha != beta mod q
    and a nonzero challenge.
    """
    a1, a2 = pow(G, alpha, P), pow(H, beta, P)
    c = challenge(a1, a2)
    if c == 0:
        raise ValueError("challenge is zero; pick other alpha and beta")
    c_inv = pow(c, -1, Q)
    u = pow(G, (s - alpha) * c_inv % Q, P)
    v = pow(H, (s - beta) * c_inv % Q, P)
    return (u, v), (a1, a2, s)


# --------------------------------------- Schnorr signature without the key
def sign_no_key_prefix(x: int, msg: bytes, k: int) -> tuple[int, int]:
    """Schnorr signature with e = H(R || m): the public key is not hashed."""
    r = pow(G, k, P)
    e = challenge(r, msg)
    return r, (k + e * x) % Q


def verify_no_key_prefix(y: int, msg: bytes, sig: tuple[int, int]) -> bool:
    r, s = sig
    if not (in_group(y) and in_group(r) and 0 <= s < Q):
        return False
    return pow(G, s, P) == r * pow(y, challenge(r, msg), P) % P


def move_to_related_key(sig: tuple[int, int], msg: bytes, delta: int) -> tuple[int, int]:
    """Turn a signature under y into one under y * g^delta, without any secret."""
    r, s = sig
    return r, (s + challenge(r, msg) * delta) % Q
