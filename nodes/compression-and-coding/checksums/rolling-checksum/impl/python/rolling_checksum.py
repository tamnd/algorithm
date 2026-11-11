# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rolling-checksum/. The authors are listed in prov/6HMBPD.jsonl.

"""Rolling checksums: the rsync weak checksum and a Rabin fingerprint for chunking.

1. The rsync weak checksum (Tridgell and Mackerras 1996, Section 3). For the
   window X_k..X_l of length L = l - k + 1 and M = 2^16:

       a = sum X_i mod M,    b = sum (l - i + 1) X_i mod M,    s = a + 2^16 b.

   Moving the window one byte to the right takes O(1) work:

       a' = a - X_k + X_{l+1},    b' = b - L X_k + a'    (both mod M).

2. A minimal rsync delta. The receiver sends one (weak, strong) pair per
   block of S bytes of its old file. The sender slides a window of S bytes
   over the new file, rolls the weak checksum, and checks the strong hash only
   when the weak one is found. It emits COPY j for a matched block and
   literal bytes for the rest. The 1996 paper uses MD4 as the strong hash;
   this code uses MD5 from hashlib (as rsync 3 does), a stand-in that the
   method does not depend on.

3. Content-defined chunking with a Rabin fingerprint (Rabin 1981; LBFS,
   Muthitacharoen, Chen and Mazieres 2001). The fingerprint of a window of w
   bytes is the window, read as a polynomial over GF(2), modulo a fixed
   irreducible polynomial P. A chunk ends where the low bits of the
   fingerprint equal a fixed value, subject to a minimum and maximum length.

Cost: roll is O(1); the delta takes Theta(n) rolls plus one strong hash per
weak hit; chunking takes Theta(n) table steps.
"""

import hashlib

M = 1 << 16


# ---------------------------------------------------------------- rsync weak checksum


def weak(block: bytes) -> tuple[int, int]:
    """(a, b) for a block, from the definition."""
    n = len(block)
    a = sum(block) % M
    b = sum((n - i) * x for i, x in enumerate(block)) % M
    return a, b


def pack(a: int, b: int) -> int:
    """s = a + 2^16 b, the 32-bit weak checksum."""
    return a | (b << 16)


def roll(a: int, b: int, out_byte: int, in_byte: int, length: int) -> tuple[int, int]:
    """Slide the window one byte: drop out_byte at the left, add in_byte at the right."""
    a = (a - out_byte + in_byte) % M  # @line L9
    b = (b - length * out_byte + a) % M  # @line L10
    return a, b


def strong(block: bytes) -> bytes:
    """The strong block hash (MD5 here; MD4 in the 1996 paper)."""
    return hashlib.md5(block).digest()


def signature(old: bytes, size: int) -> list[tuple[int, bytes]]:
    """One (weak, strong) pair per full block of old. A short last block is not indexed."""
    return [(pack(*weak(old[i : i + size])), strong(old[i : i + size])) for i in range(0, len(old) - size + 1, size)]


def delta(new: bytes, sig: list[tuple[int, bytes]], size: int) -> list[tuple[str, object]]:
    """Instructions that rebuild new from the old file: ("copy", j) or ("data", bytes)."""
    index: dict[int, list[tuple[int, bytes]]] = {}  # @line L1
    for j, (s, h) in enumerate(sig):
        index.setdefault(s, []).append((j, h))
    out: list[tuple[str, object]] = []
    lit = bytearray()
    n = len(new)
    k = 0  # @line L2
    if n >= size:
        a, b = weak(new[0:size])
    while k + size <= n:  # @line L3
        j = None
        cands = index.get(pack(a, b))
        if cands:  # @line L4
            h = strong(new[k : k + size])
            j = next((jj for jj, hh in cands if hh == h), None)
        if j is not None:
            if lit:  # @line L5
                out.append(("data", bytes(lit)))
                lit = bytearray()
            out.append(("copy", j))
            k += size
            if k + size <= n:
                a, b = weak(new[k : k + size])  # @line L6
        else:  # @line L7
            lit.append(new[k])  # @line L8
            if k + size < n:
                a, b = roll(a, b, new[k], new[k + size], size)
            k += 1  # @line L11
    lit.extend(new[k:])  # @line L12
    if lit:
        out.append(("data", bytes(lit)))
    return out


def patch(old: bytes, instructions: list[tuple[str, object]], size: int) -> bytes:
    """Apply a delta to the old file."""
    res = bytearray()
    for op, arg in instructions:
        if op == "copy":
            j = int(arg)  # type: ignore[arg-type]
            res += old[j * size : (j + 1) * size]
        else:
            res += arg  # type: ignore[operator]
    return bytes(res)


# ---------------------------------------------------------------- Rabin fingerprint and CDC

# An irreducible polynomial of degree 63 over GF(2); the tests check that it is irreducible.
RABIN_POLY = 0xBFE6B8A5BF378D83


def poly_mod(a: int, p: int) -> int:
    """a mod p, with integers read as polynomials over GF(2)."""
    dp = p.bit_length() - 1
    while a and a.bit_length() - 1 >= dp:
        a ^= p << (a.bit_length() - 1 - dp)
    return a


class RabinWindow:
    """Rolling Rabin fingerprint of the last `window` bytes."""

    def __init__(self, window: int = 48, poly: int = RABIN_POLY) -> None:
        self.window = window
        self.poly = poly
        self.deg = poly.bit_length() - 1
        # shift[t] = t * x^deg mod P, used to multiply by x^8.
        self.shift = [poly_mod(t << self.deg, poly) for t in range(256)]
        # drop[b] = b * x^(8 window) mod P, the term of the byte that leaves.
        self.drop = [poly_mod(b << (8 * window), poly) for b in range(256)]
        self.reset()

    def reset(self) -> None:
        self.fp = 0
        self.buf = bytearray(self.window)
        self.pos = 0

    def slide(self, byte: int) -> int:
        old = self.buf[self.pos]
        self.buf[self.pos] = byte
        self.pos = (self.pos + 1) % self.window
        low = self.fp & ((1 << (self.deg - 8)) - 1)
        top = self.fp >> (self.deg - 8)
        self.fp = (low << 8) ^ self.shift[top] ^ byte ^ self.drop[old]
        return self.fp


def cdc_chunks(data: bytes, window: int = 48, mask_bits: int = 8, magic: int = 0x5A, min_size: int = 64, max_size: int = 2048) -> list[bytes]:
    """Split data where the low mask_bits bits of the window fingerprint equal magic."""
    rw = RabinWindow(window)
    mask = (1 << mask_bits) - 1
    chunks = []
    start = 0
    for i, byte in enumerate(data):
        fp = rw.slide(byte)
        length = i + 1 - start
        if (length >= min_size and (fp & mask) == magic) or length >= max_size:
            chunks.append(data[start : i + 1])
            start = i + 1
    if start < len(data):
        chunks.append(data[start:])
    return chunks
