# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/noise-protocol-framework/. The authors are listed in prov/E0N5YS.jsonl.
"""The Noise Protocol Framework (revision 34, 2018-07-11), for the patterns NN and XX,
with the cipher suite 25519_ChaChaPoly_SHA256.

Everything except SHA-256 and HMAC is written here: X25519 (RFC 7748, Section 5),
ChaCha20 and Poly1305 (RFC 8439), and the CipherState, SymmetricState and
HandshakeState objects of the Noise specification (Section 5). The tests check
the results against the Noise_NN and Noise_XX test vectors of cacophony.

For study only. Python big integers are not constant time, the code branches
on secret data, and it must not protect real data. Use a maintained Noise
library instead, such as snow (Rust), noise-c, or the Noise code of
WireGuard or libp2p.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets

# ---------------------------------------------------------------- X25519, RFC 7748 Section 5

P25519 = 2**255 - 19


def x25519(k: bytes, u: bytes) -> bytes:
    """The Montgomery ladder on Curve25519, with the scalar clamped as in RFC 7748."""
    kb = bytearray(k)
    kb[0] &= 248
    kb[31] &= 127
    kb[31] |= 64
    kn = int.from_bytes(kb, "little")
    x1 = int.from_bytes(u, "little") & ((1 << 255) - 1)
    x2, z2, x3, z3, swap = 1, 0, x1, 1, 0
    for t in reversed(range(255)):
        bit = (kn >> t) & 1
        swap ^= bit
        if swap:
            x2, x3, z2, z3 = x3, x2, z3, z2
        swap = bit
        a, b = x2 + z2, x2 - z2
        aa, bb = a * a % P25519, b * b % P25519
        e = aa - bb
        c, d = x3 + z3, x3 - z3
        da, cb = d * a % P25519, c * b % P25519
        x3, z3 = (da + cb) ** 2 % P25519, x1 * (da - cb) ** 2 % P25519
        x2, z2 = aa * bb % P25519, e * (aa + 121665 * e) % P25519
    if swap:
        x2, z2 = x3, z3
    return (x2 * pow(z2, P25519 - 2, P25519) % P25519).to_bytes(32, "little")


def public_key(priv: bytes) -> bytes:
    return x25519(priv, (9).to_bytes(32, "little"))


# ---------------------------------------------------------------- ChaCha20-Poly1305, RFC 8439


def _rotl(x: int, n: int) -> int:
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def _qr(s: list[int], a: int, b: int, c: int, d: int) -> None:
    s[a] = (s[a] + s[b]) & 0xFFFFFFFF
    s[d] = _rotl(s[d] ^ s[a], 16)
    s[c] = (s[c] + s[d]) & 0xFFFFFFFF
    s[b] = _rotl(s[b] ^ s[c], 12)
    s[a] = (s[a] + s[b]) & 0xFFFFFFFF
    s[d] = _rotl(s[d] ^ s[a], 8)
    s[c] = (s[c] + s[d]) & 0xFFFFFFFF
    s[b] = _rotl(s[b] ^ s[c], 7)


def _block(key: bytes, counter: int, nonce: bytes) -> bytes:
    w = lambda b: [int.from_bytes(b[i : i + 4], "little") for i in range(0, len(b), 4)]  # noqa: E731
    state = [0x61707865, 0x3320646E, 0x79622D32, 0x6B206574] + w(key) + [counter] + w(nonce)
    x = list(state)
    for _ in range(10):
        for a, b, c, d in ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15), (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14)):
            _qr(x, a, b, c, d)
    return b"".join(((p + q) & 0xFFFFFFFF).to_bytes(4, "little") for p, q in zip(x, state))


def _chacha20(key: bytes, nonce: bytes, data: bytes) -> bytes:
    out = bytearray()
    for j in range(0, len(data), 64):
        out += bytes(p ^ q for p, q in zip(data[j : j + 64], _block(key, 1 + j // 64, nonce)))
    return bytes(out)


def _poly1305(key: bytes, msg: bytes) -> bytes:
    r = int.from_bytes(key[:16], "little") & 0x0FFFFFFC0FFFFFFC0FFFFFFC0FFFFFFF
    acc, p = 0, (1 << 130) - 5
    for i in range(0, len(msg), 16):
        acc = (acc + int.from_bytes(msg[i : i + 16] + b"\x01", "little")) * r % p
    return ((acc + int.from_bytes(key[16:32], "little")) % (1 << 128)).to_bytes(16, "little")


def _mac_data(ad: bytes, c: bytes) -> bytes:
    pad = lambda x: bytes(-len(x) % 16)  # noqa: E731
    return ad + pad(ad) + c + pad(c) + len(ad).to_bytes(8, "little") + len(c).to_bytes(8, "little")


def aead_encrypt(key: bytes, nonce: bytes, ad: bytes, plain: bytes) -> bytes:
    c = _chacha20(key, nonce, plain)
    return c + _poly1305(_block(key, 0, nonce)[:32], _mac_data(ad, c))


def aead_decrypt(key: bytes, nonce: bytes, ad: bytes, data: bytes) -> bytes | None:
    c, tag = data[:-16], data[-16:]
    if not hmac.compare_digest(_poly1305(_block(key, 0, nonce)[:32], _mac_data(ad, c)), tag):
        return None
    return _chacha20(key, nonce, c)


# ---------------------------------------------------------------- Noise objects, Section 5

HASHLEN = 32


def HASH(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def HKDF(ck: bytes, ikm: bytes, n: int) -> tuple[bytes, ...]:
    """Section 4.3: HKDF with HMAC-SHA256, chaining key as salt, empty info."""
    temp = hmac.new(ck, ikm, hashlib.sha256).digest()
    out, prev = [], b""
    for i in range(1, n + 1):
        prev = hmac.new(temp, prev + bytes([i]), hashlib.sha256).digest()
        out.append(prev)
    return tuple(out)


class CipherState:
    def __init__(self, k: bytes | None = None):
        self.k, self.n = k, 0

    def _nonce(self) -> bytes:
        if self.n >= 2**64 - 1:
            raise ValueError("nonce exhausted")
        return bytes(4) + self.n.to_bytes(8, "little")

    def encrypt_with_ad(self, ad: bytes, plain: bytes) -> bytes:
        if self.k is None:
            return plain
        out = aead_encrypt(self.k, self._nonce(), ad, plain)
        self.n += 1
        return out

    def decrypt_with_ad(self, ad: bytes, data: bytes) -> bytes:
        if self.k is None:
            return data
        out = aead_decrypt(self.k, self._nonce(), ad, data)
        if out is None:
            raise ValueError("authentication failed")
        self.n += 1
        return out


class SymmetricState:
    def __init__(self, protocol_name: bytes):
        self.h = protocol_name.ljust(HASHLEN, b"\x00") if len(protocol_name) <= HASHLEN else HASH(protocol_name)  # @line L1
        self.ck = self.h
        self.cs = CipherState()

    def mix_key(self, ikm: bytes) -> None:
        self.ck, temp_k = HKDF(self.ck, ikm, 2)
        self.cs = CipherState(temp_k)

    def mix_hash(self, data: bytes) -> None:
        self.h = HASH(self.h + data)

    def encrypt_and_hash(self, plain: bytes) -> bytes:
        c = self.cs.encrypt_with_ad(self.h, plain)
        self.mix_hash(c)
        return c

    def decrypt_and_hash(self, c: bytes) -> bytes:
        plain = self.cs.decrypt_with_ad(self.h, c)
        self.mix_hash(c)
        return plain

    def split(self) -> tuple[CipherState, CipherState]:
        k1, k2 = HKDF(self.ck, b"", 2)
        return CipherState(k1), CipherState(k2)


PATTERNS = {
    "NN": [["e"], ["e", "ee"]],
    "XX": [["e"], ["e", "ee", "s", "es"], ["s", "se"]],
}


class HandshakeState:
    """One party's handshake. s is the static private key; e may be fixed for tests."""

    def __init__(self, pattern: str, initiator: bool, prologue: bytes = b"", s: bytes | None = None, e: bytes | None = None):
        self.ss = SymmetricState(f"Noise_{pattern}_25519_ChaChaPoly_SHA256".encode())
        # NN and XX have no pre-message keys, so only the prologue is hashed here.
        self.ss.mix_hash(prologue)  # @line L2
        self.messages = PATTERNS[pattern]
        self.initiator = initiator
        self.s, self.e_fixed = s, e
        self.e = self.re = self.rs = None
        self.index = 0
        self.send = self.recv = None
        self.handshake_hash = None

    def _dh_pair(self, token: str) -> tuple[bytes, bytes]:
        mine, theirs = token[0], token[1]
        if not self.initiator:
            mine, theirs = theirs, mine
        priv = self.e if mine == "e" else self.s
        pub = self.re if theirs == "e" else self.rs
        return priv, pub

    def _finish_if_done(self) -> None:
        if self.index == len(self.messages):
            c1, c2 = self.ss.split()  # @line L8
            self.send, self.recv = (c1, c2) if self.initiator else (c2, c1)
            self.handshake_hash = self.ss.h

    def write_message(self, payload: bytes) -> bytes:
        buf = b""
        for token in self.messages[self.index]:  # @line L3
            if token == "e":
                self.e = self.e_fixed if self.e_fixed is not None else secrets.token_bytes(32)
                pub = public_key(self.e)
                buf += pub  # @line L4
                self.ss.mix_hash(pub)
            elif token == "s":
                buf += self.ss.encrypt_and_hash(public_key(self.s))  # @line L5
            else:
                self.ss.mix_key(x25519(*self._dh_pair(token)))  # @line L6
        buf += self.ss.encrypt_and_hash(payload)  # @line L7
        self.index += 1
        self._finish_if_done()
        return buf

    def read_message(self, msg: bytes) -> bytes:
        for token in self.messages[self.index]:  # @line L3
            if token == "e":
                self.re, msg = msg[:32], msg[32:]  # @line L4
                self.ss.mix_hash(self.re)
            elif token == "s":
                n = 32 + (16 if self.ss.cs.k is not None else 0)
                self.rs, msg = self.ss.decrypt_and_hash(msg[:n]), msg[n:]  # @line L5
            else:
                self.ss.mix_key(x25519(*self._dh_pair(token)))  # @line L6
        payload = self.ss.decrypt_and_hash(msg)  # @line L7
        self.index += 1
        self._finish_if_done()
        return payload
