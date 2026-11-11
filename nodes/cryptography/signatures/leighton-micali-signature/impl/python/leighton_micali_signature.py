# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leighton-micali-signature/. The authors are listed in prov/MNZ6ET.jsonl.
"""Leighton-Micali signatures (LMS), LM-OTS and HSS, as in RFC 8554.

Only the SHA-256 parameter sets with n = m = 32 of RFC 8554 are here:
LMOTS_SHA256_N32_W1, W2, W4, W8 and LMS_SHA256_M32_H5 .. H25. The private
key of one LMS tree is (SEED, I), and the one-time secret values come from
SEED as in Appendix A of the RFC. The signer stores the whole tree.

The page is about the signature, not the hash, so SHA-256 comes from hashlib.
For study only. The code is not constant time and it must not protect real
data. LMS is stateful: the counter q must never repeat. For real use take
LMS/HSS from a FIPS 140 validated module (NIST SP 800-208).
"""

import hashlib
import secrets
import struct

D_PBLC, D_MESG, D_LEAF, D_INTR = 0x8080, 0x8181, 0x8282, 0x8383

# typecode: (n, w, p, ls)
LMOTS = {1: (32, 1, 265, 7), 2: (32, 2, 133, 6), 3: (32, 4, 67, 4), 4: (32, 8, 34, 0)}
# typecode: (m, h)
LMS = {5: (32, 5), 6: (32, 10), 7: (32, 15), 8: (32, 20), 9: (32, 25)}


def H(*parts: bytes) -> bytes:
    return hashlib.sha256(b"".join(parts)).digest()


def u32(x: int) -> bytes:
    return struct.pack(">I", x)


def u16(x: int) -> bytes:
    return struct.pack(">H", x)


def coef(s: bytes, i: int, w: int) -> int:
    """The i-th w-bit value of s, most significant first (RFC 8554, 3.1.3)."""
    return (2**w - 1) & (s[i * w // 8] >> (8 - (w * (i % (8 // w)) + w)))


def cksm(s: bytes, n: int, w: int, ls: int) -> bytes:
    total = sum(2**w - 1 - coef(s, i, w) for i in range(n * 8 // w))
    return u16(total << ls)


def ots_digits(I: bytes, q: int, C: bytes, message: bytes, otstype: int) -> list[int]:
    n, w, p, ls = LMOTS[otstype]
    Q = H(I, u32(q), u16(D_MESG), C, message)  # @line L2
    v = Q + cksm(Q, n, w, ls)
    return [coef(v, i, w) for i in range(p)]  # @line L3


def chain(I: bytes, q: int, i: int, tmp: bytes, start: int, end: int) -> bytes:
    """Steps start .. end - 1 of chain i of leaf q."""
    for j in range(start, end):
        tmp = H(I, u32(q), u16(i), bytes([j]), tmp)  # @line L5
    return tmp


def ots_secret(seed: bytes, I: bytes, q: int, i: int) -> bytes:
    """x_q[i] of Appendix A."""
    return H(I, u32(q), u16(i), b"\xff", seed)


def ots_public_hash(seed: bytes, I: bytes, q: int, otstype: int) -> bytes:
    n, w, p, ls = LMOTS[otstype]
    y = [chain(I, q, i, ots_secret(seed, I, q, i), 0, 2**w - 1) for i in range(p)]
    return H(I, u32(q), u16(D_PBLC), *y)


def ots_sign(seed: bytes, I: bytes, q: int, otstype: int, message: bytes, C: bytes | None = None) -> bytes:
    n, w, p, ls = LMOTS[otstype]
    if C is None:
        C = secrets.token_bytes(n)  # @line L1
    a = ots_digits(I, q, C, message, otstype)
    y = [chain(I, q, i, ots_secret(seed, I, q, i), 0, a[i]) for i in range(p)]  # @line L4
    return u32(otstype) + C + b"".join(y)  # @line L6


class LmsSigner:
    """One LMS tree. The counter q is the state."""

    def __init__(self, lmstype: int, otstype: int, seed: bytes | None = None, I: bytes | None = None) -> None:
        self.lmstype, self.otstype = lmstype, otstype
        m, h = LMS[lmstype]
        self.h = h
        self.seed = seed if seed is not None else secrets.token_bytes(32)
        self.I = I if I is not None else secrets.token_bytes(16)
        T = [b""] * (2 ** (h + 1))
        for q in range(2**h):
            r = 2**h + q
            T[r] = H(self.I, u32(r), u16(D_LEAF), ots_public_hash(self.seed, self.I, q, otstype))
        for r in range(2**h - 1, 0, -1):
            T[r] = H(self.I, u32(r), u16(D_INTR), T[2 * r], T[2 * r + 1])
        self.T = T
        self.q = 0

    def public_key(self) -> bytes:
        return u32(self.lmstype) + u32(self.otstype) + self.I + self.T[1]

    def sign(self, message: bytes, C: bytes | None = None) -> bytes:
        q = self.q
        if q >= 2**self.h:  # @line L7
            raise RuntimeError("all one-time keys are used")
        self.q = q + 1
        ots = ots_sign(self.seed, self.I, q, self.otstype, message, C)  # @line L8
        r = 2**self.h + q
        path = [self.T[(r >> i) ^ 1] for i in range(self.h)]  # @line L9
        return u32(q) + ots + u32(self.lmstype) + b"".join(path)  # @line L10


def lms_signature_length(sig: bytes) -> int:
    """Length of the LMS signature at the start of sig, or -1."""
    if len(sig) < 8:
        return -1
    otstype = struct.unpack(">I", sig[4:8])[0]
    if otstype not in LMOTS:
        return -1
    n, w, p, ls = LMOTS[otstype]
    k = 8 + n * (p + 1)
    if len(sig) < k + 4:
        return -1
    lmstype = struct.unpack(">I", sig[k : k + 4])[0]
    if lmstype not in LMS:
        return -1
    m, h = LMS[lmstype]
    return k + 4 + h * m


def lms_verify(pub: bytes, message: bytes, sig: bytes) -> bool:
    if len(pub) != 56:
        return False
    lmstype, otstype = struct.unpack(">II", pub[:8])
    I, T1 = pub[8:24], pub[24:]
    if lmstype not in LMS or otstype not in LMOTS:
        return False
    m, h = LMS[lmstype]
    n, w, p, ls = LMOTS[otstype]
    if lms_signature_length(sig) != len(sig):  # @line L11
        return False
    q, sig_ots = struct.unpack(">II", sig[:8])
    k = 8 + n * (p + 1)
    if sig_ots != otstype or struct.unpack(">I", sig[k : k + 4])[0] != lmstype or q >= 2**h:
        return False
    C = sig[8 : 8 + n]
    y = [sig[8 + n * (i + 1) : 8 + n * (i + 2)] for i in range(p)]
    path = [sig[k + 4 + m * i : k + 4 + m * (i + 1)] for i in range(h)]
    a = ots_digits(I, q, C, message, otstype)  # @line L12
    z = [chain(I, q, i, y[i], a[i], 2**w - 1) for i in range(p)]  # @line L13
    Kc = H(I, u32(q), u16(D_PBLC), *z)  # @line L14
    r = 2**h + q
    tmp = H(I, u32(r), u16(D_LEAF), Kc)  # @line L15
    for i in range(h):  # @line L16
        if r & 1:
            tmp = H(I, u32(r // 2), u16(D_INTR), path[i], tmp)
        else:
            tmp = H(I, u32(r // 2), u16(D_INTR), tmp, path[i])
        r //= 2
    return tmp == T1  # @line L17


def hss_verify(pub: bytes, message: bytes, sig: bytes) -> bool:
    """Verify an HSS signature (RFC 8554, Section 6.3)."""
    if len(pub) < 4 or len(sig) < 4:
        return False
    L = struct.unpack(">I", pub[:4])[0]
    nspk = struct.unpack(">I", sig[:4])[0]
    if nspk + 1 != L:  # @line L18
        return False
    key, rest = pub[4:], sig[4:]
    for _ in range(nspk):  # @line L19
        k = lms_signature_length(rest)
        if k < 0 or len(rest) < k + 56:
            return False
        lsig, child, rest = rest[:k], rest[k : k + 56], rest[k + 56 :]
        if not lms_verify(key, child, lsig):
            return False
        key = child
    return lms_verify(key, message, rest)  # @line L20


class HssSigner:
    """A two-level HSS signer (L = 2, RFC 8554, Sections 6.1 and 6.2).

    The top tree signs the public key of the current bottom tree once, and
    the signer keeps that signature. When the bottom tree is used up, a new
    bottom tree is made and signed with the next top leaf.
    """

    def __init__(self, top: tuple[int, int], bottom: tuple[int, int]) -> None:
        self.bottom_types = bottom
        self.top = LmsSigner(*top)
        self._new_bottom()

    def _new_bottom(self) -> None:
        self.bottom = LmsSigner(*self.bottom_types)
        self.bottom_sig = self.top.sign(self.bottom.public_key())

    def public_key(self) -> bytes:
        return u32(2) + self.top.public_key()

    def sign(self, message: bytes) -> bytes:
        if self.bottom.q >= 2**self.bottom.h:
            self._new_bottom()
        sig = self.bottom.sign(message)
        return u32(1) + self.bottom_sig + self.bottom.public_key() + sig
