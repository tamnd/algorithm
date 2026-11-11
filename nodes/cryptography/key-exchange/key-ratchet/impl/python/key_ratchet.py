# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-ratchet/. The authors are listed in prov/EE0J5J.jsonl.
"""Two key ratchets: a KDF chain (the symmetric or hash ratchet) and a
Diffie-Hellman ratchet. The KDF chain uses HMAC-SHA256 with the constants
0x01 and 0x02, as the Double Ratchet specification recommends. The DH
ratchet uses X25519 (RFC 7748) and HKDF (RFC 5869), both small local copies.

For study only. The code is not constant time, and it must not protect real
data.

Lines marked L1 to L9 match the pseudocode on the page.
"""

import hashlib
import hmac
import secrets

# ---------------------------------------------------------------- X25519 (RFC 7748, Section 5), local copy

_P = 2**255 - 19
_A24 = 121665


def _clamp(k: bytes) -> int:
    b = bytearray(k)
    b[0] &= 248
    b[31] &= 127
    b[31] |= 64
    return int.from_bytes(b, "little")


def x25519(k: bytes, u: bytes) -> bytes:
    kk = _clamp(k)
    b = bytearray(u)
    b[31] &= 127
    x1 = int.from_bytes(b, "little") % _P
    x2, z2, x3, z3, swap = 1, 0, x1, 1, 0
    for t in range(254, -1, -1):
        kt = (kk >> t) & 1
        swap ^= kt
        if swap:
            x2, x3, z2, z3 = x3, x2, z3, z2
        swap = kt
        a, b_ = (x2 + z2) % _P, (x2 - z2) % _P
        aa, bb = a * a % _P, b_ * b_ % _P
        e = (aa - bb) % _P
        c, d = (x3 + z3) % _P, (x3 - z3) % _P
        da, cb = d * a % _P, c * b_ % _P
        x3 = (da + cb) ** 2 % _P
        z3 = x1 * (da - cb) ** 2 % _P
        x2 = aa * bb % _P
        z2 = e * (aa + _A24 * e) % _P
    if swap:
        x2, z2 = x3, z3
    return (x2 * pow(z2, _P - 2, _P) % _P).to_bytes(32, "little")


BASE_U = (9).to_bytes(32, "little")

# ---------------------------------------------------------------- HKDF (RFC 5869), local copy


def hkdf(ikm: bytes, salt: bytes, info: bytes, length: int) -> bytes:
    prk = hmac.new(salt or bytes(32), ikm, hashlib.sha256).digest()
    out, t, i = b"", b"", 1
    while len(out) < length:
        t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
        out += t
        i += 1
    return out[:length]


# ---------------------------------------------------------------- the KDF chain (symmetric ratchet)


def chain_step(ck: bytes):
    """One step of the KDF chain. Returns (next chain key, message key)."""
    mk = hmac.new(ck, b"\x01", hashlib.sha256).digest()          # @line L1
    ck_next = hmac.new(ck, b"\x02", hashlib.sha256).digest()     # @line L2
    return ck_next, mk                                           # @line L3 (the caller deletes ck)


class SymmetricRatchet:
    """Holds only the current chain key. Each call moves forward and forgets the past."""

    def __init__(self, ck: bytes):
        self.ck = ck
        self.n = 0

    def next_key(self) -> bytes:
        self.ck, mk = chain_step(self.ck)
        self.n += 1
        return mk


# ---------------------------------------------------------------- the Diffie-Hellman ratchet

INFO = b"KeyRatchetStudy"


def kdf_rk(rk: bytes, dh_out: bytes):
    out = hkdf(dh_out, rk, INFO, 64)
    return out[:32], out[32:]


class DHRatchet:
    """One party of a ping-pong DH ratchet. Each turn the sender picks a new key pair."""

    def __init__(self, root: bytes, private: bytes, peer_public: bytes):
        self.rk = root
        self.priv = private
        self.pub = x25519(private, BASE_U)
        self.peer = peer_public

    def send_step(self, rng=secrets.token_bytes):
        """Pick a fresh key pair and derive a new sending chain key. Returns (public key, chain key)."""
        self.priv = rng(32)                                       # @line L4
        self.pub = x25519(self.priv, BASE_U)                      # @line L5
        self.rk, ck = kdf_rk(self.rk, x25519(self.priv, self.peer))   # @line L6
        return self.pub, ck

    def receive_step(self, peer_public: bytes) -> bytes:
        """Take the peer's new public key and derive the matching receiving chain key."""
        self.peer = peer_public                                   # @line L7
        self.rk, ck = kdf_rk(self.rk, x25519(self.priv, self.peer))   # @line L8
        return ck                                                 # @line L9
