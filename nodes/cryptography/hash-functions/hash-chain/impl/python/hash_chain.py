# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-chain/. The authors are listed in prov/WAQZTJ.jsonl.
"""Hash chains: Lamport's one-time passwords and the OTP system of RFC 2289.

A hash chain is x_0 = s, x_i = f(x_{i-1}). The prover keeps s (or some
checkpoints) secret and gives the anchor x_n to the verifier. It then reveals
x_{n-1}, x_{n-2}, ... in turn, and the verifier checks each value by hashing
it once and comparing with the last value it accepted.

RFC 2289 fixes f(x) = FOLD(H(x)), where H is MD4, MD5 or SHA-1 and FOLD
reduces the digest to 64 bits. MD4 is not in hashlib (OpenSSL 3 removed it
from the default provider), so this module has a small MD4 of its own, as in
RFC 1320. MD5 and SHA-1 come from hashlib.

For study only. The code is not constant time and must not protect real data.
MD4, MD5 and SHA-1 are broken for collisions, and RFC 2289 passwords have only
64 bits. For real one-time passwords use TOTP or HOTP from a maintained library
such as pyotp, or better a FIDO2 or WebAuthn authenticator.
"""

import hashlib
import struct
from collections.abc import Callable

# ---------------------------------------------------------------- MD4 (RFC 1320)

_M32 = 0xFFFFFFFF


def _rotl(x: int, s: int) -> int:
    return ((x << s) | (x >> (32 - s))) & _M32


def md4(data: bytes) -> bytes:
    """MD4 as in RFC 1320, Section 3. Only for the RFC 2289 MD4 vectors."""
    n = len(data)
    msg = data + b"\x80" + b"\x00" * ((55 - n) % 64) + struct.pack("<Q", (8 * n) & 0xFFFFFFFFFFFFFFFF)
    a, b, c, d = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476
    for off in range(0, len(msg), 64):
        x = struct.unpack("<16I", msg[off : off + 64])
        aa, bb, cc, dd = a, b, c, d
        for i in range(16):  # round 1: F(x, y, z) = xy or (not x)z
            k, s = i, (3, 7, 11, 19)[i % 4]
            a = _rotl((a + ((b & c) | (~b & d)) + x[k]) & _M32, s)
            a, b, c, d = d, a, b, c
        for i in range(16):  # round 2: G = majority, constant 5a827999
            k, s = (0, 4, 8, 12)[i % 4] + i // 4, (3, 5, 9, 13)[i % 4]
            a = _rotl((a + ((b & c) | (b & d) | (c & d)) + x[k] + 0x5A827999) & _M32, s)
            a, b, c, d = d, a, b, c
        for i in range(16):  # round 3: H = xor, constant 6ed9eba1
            k, s = (0, 8, 4, 12)[i % 4] + (0, 2, 1, 3)[i // 4], (3, 9, 11, 15)[i % 4]
            a = _rotl((a + (b ^ c ^ d) + x[k] + 0x6ED9EBA1) & _M32, s)
            a, b, c, d = d, a, b, c
        a, b, c, d = (a + aa) & _M32, (b + bb) & _M32, (c + cc) & _M32, (d + dd) & _M32
    return struct.pack("<4I", a, b, c, d)


# ---------------------------------------------------------------- RFC 2289 OTP


def fold(digest: bytes, alg: str) -> bytes:
    """Reduce a digest to 64 bits as in RFC 2289, Appendix A."""
    if alg in ("md4", "md5"):
        return bytes(digest[i] ^ digest[i + 8] for i in range(8))
    if alg == "sha1":
        w = struct.unpack(">5I", digest)  # the SHA-1 words d0..d4
        d0, d1 = w[0] ^ w[2] ^ w[4], w[1] ^ w[3]
        return struct.pack("<2I", d0, d1)  # copied out in little endian order
    raise ValueError("unknown OTP hash")


def otp_hash(alg: str) -> Callable[[bytes], bytes]:
    """The step function f(x) = FOLD(H(x)) of RFC 2289."""
    if alg == "md4":
        h = md4
    elif alg in ("md5", "sha1"):
        def h(x: bytes) -> bytes:
            return hashlib.new(alg, x).digest()
    else:
        raise ValueError("unknown OTP hash")
    return lambda x: fold(h(x), alg)


def otp(passphrase: str, seed: str, count: int, alg: str = "md5") -> bytes:
    """The 64-bit one-time password for a challenge (alg, count, seed)."""
    if not (1 <= len(seed) <= 16 and seed.isalnum()):
        raise ValueError("seed must be 1 to 16 alphanumeric characters")
    if len(passphrase) < 10:
        raise ValueError("pass phrase too short")
    f = otp_hash(alg)
    x = f(seed.lower().encode() + passphrase.encode())  # @line L7
    for _ in range(count):
        x = f(x)  # @line L7
    return x


# ---------------------------------------------------------------- the chain


def sha256(x: bytes) -> bytes:
    return hashlib.sha256(x).digest()


class HashChain:
    """The prover side: a chain of n + 1 values with checkpoints every t steps."""

    def __init__(self, s: bytes, n: int, t: int = 1, f: Callable[[bytes], bytes] = sha256):
        if n < 1 or t < 1:
            raise ValueError("need n >= 1 and t >= 1")
        self.f, self.n, self.t = f, n, t
        x = s  # @line L1
        self.checkpoints = {0: x}  # @line L1
        for i in range(1, n + 1):
            x = f(x)  # @line L2
            if i % t == 0:
                self.checkpoints[i] = x  # @line L2
        self.anchor = x  # @line L3
        self.used = 0
        self.hash_calls = 0

    def value(self, i: int) -> bytes:
        """x_i, recomputed from the nearest checkpoint at or below i."""
        c = (i // self.t) * self.t
        x = self.checkpoints[c]  # @line L4
        for _ in range(i - c):
            x = self.f(x)  # @line L4
            self.hash_calls += 1
        return x

    def next(self) -> bytes:
        """Reveal the next value x_{n-1}, x_{n-2}, ..., x_0 in turn."""
        if self.used >= self.n:
            raise ValueError("chain used up")
        self.used += 1
        return self.value(self.n - self.used)  # @line L4


class Verifier:
    """The verifier side: it stores only the last accepted value."""

    def __init__(self, anchor: bytes, f: Callable[[bytes], bytes] = sha256):
        self.v, self.f = anchor, f

    def verify(self, y: bytes) -> bool:
        if self.f(y) == self.v:  # @line L5
            self.v = y  # @line L5
            return True
        return False  # @line L6

    def verify_skip(self, y: bytes, max_skip: int) -> bool:
        """Accept y if f^j(y) = v for some 1 <= j <= max_skip (lost values, as in TESLA)."""
        x = y
        for _ in range(max_skip):
            x = self.f(x)
            if x == self.v:
                self.v = y
                return True
        return False
