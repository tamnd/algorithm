# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eax-mode/. The authors are listed in prov/V9AB4V.jsonl.
"""EAX mode of Bellare, Rogaway and Wagner (FSE 2004), Figures 1 and 2 of the paper.

For study only. This code is not constant time (the AES in aes.py uses table
lookups, and the doubling branches on a secret bit) and must not protect real
data. EAX is not a NIST approved mode. If you need EAX, use the one in Botan or
Crypto++; otherwise use AES-GCM from a FIPS 140 validated module.

OMAC here is OMAC1 with the constants 2L and 4L, which is the same function as
CMAC (NIST SP 800-38B). OMAC^t(M) is OMAC([t]_n || M).
"""

from typing import Protocol

INVALID = "INVALID"
N_BYTES = 16


class BlockCipher(Protocol):
    block_size: int

    def encrypt_block(self, block: bytes) -> bytes: ...


def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def _dbl(x: bytes) -> bytes:
    """Multiply by x in GF(2^128) modulo x^128 + x^7 + x^2 + x + 1 (big-endian)."""
    v = int.from_bytes(x, "big") << 1
    if v >> 128:
        v ^= (1 << 128) | 0x87
    return v.to_bytes(16, "big")


class Omac:
    """OMAC (= CMAC) as an online object: update with any chunks, then final.

    It keeps at most one block of input, because the last block is masked with
    B = 2L if it is full and with P = 4L after padding if it is not.
    """

    def __init__(self, cipher: BlockCipher, t: int | None = None) -> None:
        self.cipher = cipher
        ell = cipher.encrypt_block(bytes(N_BYTES))
        self.b = _dbl(ell)
        self.p = _dbl(self.b)
        self.state = bytes(N_BYTES)
        self.buf = b""
        if t is not None:
            self.update(t.to_bytes(N_BYTES, "big"))  # the tweak [t]_n

    def update(self, data: bytes) -> None:
        self.buf += data
        while len(self.buf) > N_BYTES:  # keep the last block back: it may be the final one
            self.state = self.cipher.encrypt_block(_xor(self.state, self.buf[:N_BYTES]))
            self.buf = self.buf[N_BYTES:]

    def final(self) -> bytes:
        if len(self.buf) == N_BYTES:
            last = _xor(self.buf, self.b)
        else:
            last = _xor(self.buf + b"\x80" + bytes(N_BYTES - 1 - len(self.buf)), self.p)
        return self.cipher.encrypt_block(_xor(self.state, last))


def omac(cipher: BlockCipher, m: bytes) -> bytes:
    o = Omac(cipher)
    o.update(m)
    return o.final()


def omac_t(cipher: BlockCipher, t: int, m: bytes) -> bytes:
    o = Omac(cipher, t)  # @line L1
    o.update(m)
    return o.final()


def ctr(cipher: BlockCipher, n: bytes, m: bytes) -> bytes:
    """CTR of Figure 1: the key stream is E(N), E(N+1), ... with N+i taken modulo 2^128."""
    start = int.from_bytes(n, "big")
    out = bytearray()
    for i in range(0, len(m), N_BYTES):
        s = cipher.encrypt_block(((start + i // N_BYTES) % (1 << 128)).to_bytes(N_BYTES, "big"))
        out += _xor(m[i : i + N_BYTES], s)
    return bytes(out)


def tags_equal(a: bytes, b: bytes) -> bool:
    """Read every byte and fold the differences with OR: no early exit."""
    d = len(a) ^ len(b)
    for x, y in zip(a, b):
        d |= x ^ y
    return d == 0


def eax_encrypt(cipher: BlockCipher, n: bytes, h: bytes, m: bytes, tau: int = 16) -> bytes:
    """Figure 2, EAX.Encrypt. tau is the tag length in bytes, 0 to 16."""
    n1 = omac_t(cipher, 0, n)  # @line L2
    h1 = omac_t(cipher, 1, h)  # @line L3
    c = ctr(cipher, n1, m)  # @line L4
    c1 = omac_t(cipher, 2, c)  # @line L5
    tag = _xor(_xor(n1, c1), h1)  # @line L6
    return c + tag[:tau]  # @line L7


def eax_decrypt(cipher: BlockCipher, n: bytes, h: bytes, ct: bytes, tau: int = 16) -> bytes | str:
    """Figure 2, EAX.Decrypt. The tag is checked before any decryption."""
    if len(ct) < tau:  # @line L8
        return INVALID
    c, t = ct[: len(ct) - tau], ct[len(ct) - tau :]  # @line L9
    n1, h1, c1 = omac_t(cipher, 0, n), omac_t(cipher, 1, h), omac_t(cipher, 2, c)  # @line L10
    if not tags_equal(t, _xor(_xor(n1, c1), h1)[:tau]):  # @line L11
        return INVALID
    return ctr(cipher, n1, c)  # @line L12


class EaxHeader:
    """A static header processed once: H' = OMAC^1(H) is kept and used for every message."""

    def __init__(self, cipher: BlockCipher, h: bytes) -> None:
        self.cipher = cipher
        self.h1 = omac_t(cipher, 1, h)

    def encrypt(self, n: bytes, m: bytes, tau: int = 16) -> bytes:
        n1 = omac_t(self.cipher, 0, n)
        c = ctr(self.cipher, n1, m)
        return c + _xor(_xor(n1, omac_t(self.cipher, 2, c)), self.h1)[:tau]


class EaxOnlineEncryptor:
    """On-line encryption: the length of M is not known until finish is called.

    Memory is constant apart from one partial block of key stream and one
    block kept back by OMAC.
    """

    def __init__(self, cipher: BlockCipher, n: bytes, h: bytes) -> None:
        self.cipher = cipher
        self.n1 = omac_t(cipher, 0, n)
        self.h1 = omac_t(cipher, 1, h)
        self.mac = Omac(cipher, 2)
        self.counter = int.from_bytes(self.n1, "big")
        self.stream = b""

    def update(self, m: bytes) -> bytes:
        while len(self.stream) < len(m):
            self.stream += self.cipher.encrypt_block(self.counter.to_bytes(N_BYTES, "big"))
            self.counter = (self.counter + 1) % (1 << 128)
        c, self.stream = _xor(m, self.stream), self.stream[len(m) :]
        self.mac.update(c)
        return c

    def finish(self, tau: int = 16) -> bytes:
        return _xor(_xor(self.n1, self.mac.final()), self.h1)[:tau]
