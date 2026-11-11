# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sigma-key-exchange/. The authors are listed in prov/7AWQRY.jsonl.
"""SIGMA-I, the SIGn-and-MAc key exchange of Krawczyk (CRYPTO 2003), with identity protection.

    m1  A -> B : s, X = g^x
    m2  B -> A : s, Y = g^y, E_Ke( B, SIG_B("1", s, X, Y), MAC_Km("1", s, B) )
    m3  A -> B : s, E_Ke( A, SIG_A("0", s, Y, X), MAC_Km("0", s, A) )
    (Ke, Km, Ks) from g^(xy) and s; Ks is the session key.

The signed and MACed data follow the form that Canetti and Krawczyk (CRYPTO
2002) analysed. The flags encrypt and use_mac switch off parts of the
protocol so that the tests can show what each part does:

- encrypt=False gives basic SIGMA (no identity protection);
- use_mac=False as well gives the insecure "sign only" protocol, which falls
  to an identity misbinding (unknown key-share) attack by a registered user.

SIG is a Schnorr signature and MAC is HMAC-SHA-256. E is a toy stream cipher
(SHA-256 in counter mode); in IKEv2 it is an authenticated cipher.
The group is the subgroup of prime order q of Z_p^* for a 256-bit safe prime.
For study only. This code is not constant time, it branches on secret data,
and the parameters are toys. Use IKEv2 (strongSwan, libreswan) or TLS 1.3
(OpenSSL, BoringSSL, rustls), or a FIPS 140 validated module.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets

P = 0xC00000000000000000000000000000000000000000000000000000000000A0EB
Q = (P - 1) // 2
G = 4


def b32(x: int) -> bytes:
    return x.to_bytes(32, "big")


def lp(*parts: bytes) -> bytes:
    """Unambiguous encoding: each part with a 2-byte length."""
    return b"".join(len(p).to_bytes(2, "big") + p for p in parts)


def unlp(data: bytes) -> list[bytes]:
    out, i = [], 0
    while i < len(data):
        n = int.from_bytes(data[i : i + 2], "big")
        out.append(data[i + 2 : i + 2 + n])
        i += 2 + n
    return out


def in_group(v: int) -> bool:
    return 1 < v < P and pow(v, Q, P) == 1


def h_int(*parts: bytes) -> int:
    return int.from_bytes(hashlib.sha256(lp(*parts)).digest(), "big") % Q


def keygen(rng=None) -> tuple[int, int]:
    sk = (rng or secrets.SystemRandom()).randrange(1, Q)
    return sk, pow(G, sk, P)


def sign(sk: int, msg: bytes) -> bytes:
    """Schnorr signature e || s with a deterministic nonce."""
    k = h_int(b"nonce", b32(sk), msg) or 1
    e = h_int(b"chal", b32(pow(G, k, P)), msg)
    return b32(e) + b32((k + e * sk) % Q)


def verify(pk: int, msg: bytes, sig: bytes) -> bool:
    if len(sig) != 64 or not in_group(pk):
        return False
    e, s = int.from_bytes(sig[:32], "big"), int.from_bytes(sig[32:], "big")
    return e < Q and s < Q and h_int(b"chal", b32(pow(G, s, P) * pow(pk, Q - e, P) % P), msg) == e


def derive(z: int, s: bytes) -> tuple[bytes, bytes, bytes]:
    """(Ke, Km, Ks) = PRF_{g^xy}(s, label) for three labels. The session key Ks is never used inside the protocol."""
    prk = hmac.new(s, b32(z), hashlib.sha256).digest()
    return tuple(hmac.new(prk, label, hashlib.sha256).digest() for label in (b"enc", b"mac", b"session"))


def mac(km: bytes, *parts: bytes) -> bytes:
    return hmac.new(km, lp(*parts), hashlib.sha256).digest()


def enc(ke: bytes, nonce: bytes, data: bytes) -> bytes:
    stream = b"".join(hashlib.sha256(ke + nonce + i.to_bytes(4, "big")).digest() for i in range((len(data) + 31) // 32))
    return bytes(a ^ b for a, b in zip(data, stream))


class Party:
    """One SIGMA-I session. Cost: about six exponentiations per party (DH, check, sign, verify)."""

    def __init__(self, name: str, sk: int, directory: dict[str, int], rng=None, encrypt: bool = True, use_mac: bool = True):
        self.name, self.sk, self.directory = name.encode(), sk, directory
        self.rng = rng or secrets.SystemRandom()
        self.encrypt, self.use_mac = encrypt, use_mac
        self.e = 0
        self.s = b""
        self.x_pub = self.y_pub = 0
        self.keys: tuple[bytes, bytes, bytes] = (b"", b"", b"")

    def _wrap(self, nonce: bytes, ident: bytes, sig: bytes, tag: bytes) -> bytes:
        body = lp(ident, sig, tag)
        return enc(self.keys[0], nonce, body) if self.encrypt else body

    def _unwrap(self, nonce: bytes, data: bytes) -> list[bytes]:
        parts = unlp(enc(self.keys[0], nonce, data) if self.encrypt else data)
        return parts if len(parts) == 3 else [b"", b"", b""]

    def _check(self, ident: bytes, sig: bytes, tag: bytes, label: bytes, first: int, second: int) -> bool:
        pk = self.directory.get(ident.decode(errors="replace"))
        if pk is None or not verify(pk, lp(label, self.s, b32(first), b32(second)), sig):
            return False
        return not self.use_mac or hmac.compare_digest(tag, mac(self.keys[1], label, self.s, ident))

    # ---- initiator
    def start(self) -> tuple[bytes, int]:
        self.s = self.rng.randbytes(16)
        self.e = self.rng.randrange(1, Q)  # @line L1
        self.x_pub = pow(G, self.e, P)
        return self.s, self.x_pub

    def finish(self, m2: tuple[bytes, int, bytes]) -> tuple[tuple[bytes, bytes], tuple[bytes, str]] | None:
        s, y_pub, body = m2
        if s != self.s or not in_group(y_pub):  # @line L5
            return None
        self.y_pub, self.keys, self.e = y_pub, derive(pow(y_pub, self.e, P), s), 0
        peer, sig_b, tag_b = self._unwrap(b"m2", body)
        if not self._check(peer, sig_b, tag_b, b"1", self.x_pub, y_pub):  # @line L6
            return None
        tag_a = mac(self.keys[1], b"0", s, self.name) if self.use_mac else b""
        m3 = (s, self._wrap(b"m3", self.name, sign(self.sk, lp(b"0", s, b32(y_pub), b32(self.x_pub))), tag_a))  # @line L7
        return m3, (self.keys[2], peer.decode())

    # ---- responder
    def reply(self, m1: tuple[bytes, int]) -> tuple[bytes, int, bytes] | None:
        s, x_pub = m1
        if not in_group(x_pub):  # @line L2
            return None
        y = self.rng.randrange(1, Q)
        self.s, self.x_pub, self.y_pub = s, x_pub, pow(G, y, P)
        self.keys = derive(pow(x_pub, y, P), s)  # @line L3
        tag_b = mac(self.keys[1], b"1", s, self.name) if self.use_mac else b""
        return s, self.y_pub, self._wrap(b"m2", self.name, sign(self.sk, lp(b"1", s, b32(x_pub), b32(self.y_pub))), tag_b)  # @line L4

    def complete(self, m3: tuple[bytes, bytes]) -> tuple[bytes, str] | None:
        s, body = m3
        peer, sig_a, tag_a = self._unwrap(b"m3", body)
        if s != self.s or not self._check(peer, sig_a, tag_a, b"0", self.y_pub, self.x_pub):  # @line L8
            return None
        return self.keys[2], peer.decode()  # @line L9


def run(a: Party, b: Party):
    m2 = b.reply(a.start())
    if m2 is None:
        return None, None
    out = a.finish(m2)
    if out is None:
        return None, None
    m3, res_a = out
    return res_a, b.complete(m3)


def misbind_m3(m3: tuple[bytes, bytes], eve_name: str, eve_sk: int, x_pub: int, y_pub: int, reuse_tag: bytes = b"") -> tuple[bytes, bytes]:
    """Eve, a registered user, replaces A's identity and signature in a plaintext m3 by her own.

    She can sign ("0", s, Y, X) with her own key, since the signature names no peer.
    She cannot compute MAC_Km("0", s, "E") without Km, so she can only reuse A's tag.
    """
    s, _ = m3
    sig_e = sign(eve_sk, lp(b"0", s, b32(y_pub), b32(x_pub)))
    return s, lp(eve_name.encode(), sig_e, reuse_tag)
