# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-ec-drbg/. The authors are listed in prov/E3TY1F.jsonl.

"""Dual_EC_DRBG on the NIST curve P-256, as specified in NIST SP 800-90A (2012), Section 10.3.1,
and the Shumow-Ferguson state recovery for a point Q whose discrete logarithm relation to P is known.

This generator was withdrawn by NIST in 2014 and removed from SP 800-90A in 2015. The code exists to
show how it works and how its trapdoor works; do not use it to generate secrets."""

import hashlib
from typing import Iterable, List, Optional, Tuple

# ---------------------------------------------------------------- the curve P-256 (FIPS 186)

PRIME = 2 ** 256 - 2 ** 224 + 2 ** 192 + 2 ** 96 - 1
A = PRIME - 3
B = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
ORDER = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
GX = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
GY = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5

# The points of SP 800-90A, Appendix A.1.1, for P-256: P is the base point, Q is the published constant.
P_POINT = (GX, GY)
Q_POINT = (0xC97445F45CDEF9F0D3E05E1E585FC297235B82B5BE8FF3EFCA67C59852018192,
           0xB28EF557BA31DFCBDD21AC46E2A91E3C304F44CB87058ADA2CB815151E610046)

SEEDLEN = 256  # bits
OUTLEN = 240   # bits: the rightmost 240 of the 256-bit x coordinate are output
Point = Optional[Tuple[int, int]]  # None is the point at infinity


def on_curve(pt: Point) -> bool:
    if pt is None:
        return True
    x, y = pt
    return 0 <= x < PRIME and 0 <= y < PRIME and (y * y - (x * x * x + A * x + B)) % PRIME == 0


def _jdouble(X, Y, Z):
    if Y == 0 or Z == 0:
        return (0, 1, 0)
    p = PRIME
    YY = Y * Y % p
    S = 4 * X * YY % p
    ZZ = Z * Z % p
    M = 3 * (X - ZZ) * (X + ZZ) % p  # a = -3
    X3 = (M * M - 2 * S) % p
    Y3 = (M * (S - X3) - 8 * YY * YY) % p
    Z3 = 2 * Y * Z % p
    return (X3, Y3, Z3)


def _jadd_affine(X1, Y1, Z1, x2, y2):
    """Jacobian point plus affine point."""
    p = PRIME
    if Z1 == 0:
        return (x2, y2, 1)
    Z1Z1 = Z1 * Z1 % p
    U2 = x2 * Z1Z1 % p
    S2 = y2 * Z1 * Z1Z1 % p
    H = (U2 - X1) % p
    R = (S2 - Y1) % p
    if H == 0:
        if R == 0:
            return _jdouble(X1, Y1, Z1)
        return (0, 1, 0)
    HH = H * H % p
    HHH = H * HH % p
    V = X1 * HH % p
    X3 = (R * R - HHH - 2 * V) % p
    Y3 = (R * (V - X3) - Y1 * HHH) % p
    Z3 = Z1 * H % p
    return (X3, Y3, Z3)


def scalar_mult(k: int, pt: Point) -> Point:
    """k * pt by left-to-right double and add (not constant time)."""
    if pt is None or k % ORDER == 0:
        return None
    k %= ORDER
    x, y = pt
    R = (0, 1, 0)
    for bit in bin(k)[2:]:
        R = _jdouble(*R)
        if bit == "1":
            R = _jadd_affine(*R, x, y)
    X, Y, Z = R
    if Z == 0:
        return None
    zi = pow(Z, -1, PRIME)
    zi2 = zi * zi % PRIME
    return (X * zi2 % PRIME, Y * zi2 * zi % PRIME)


def lift_x(x: int) -> Point:
    """A point with x coordinate x, or None if x is not the x coordinate of a curve point.
    P-256 has p = 3 mod 4, so a square root of c is c^((p+1)/4) when it exists."""
    if not 0 <= x < PRIME:
        return None
    c = (x * x * x + A * x + B) % PRIME
    y = pow(c, (PRIME + 1) // 4, PRIME)
    return (x, y) if y * y % PRIME == c else None


# ---------------------------------------------------------------- the generator


def hash_df(data: bytes, nbits: int = SEEDLEN, name: str = "sha256") -> bytes:
    """Hash_df (SP 800-90A, Section 10.4.1), the same function as in Hash_DRBG."""
    out = b""
    counter = 1
    while 8 * len(out) < nbits:
        out += hashlib.new(name, bytes([counter]) + nbits.to_bytes(4, "big") + data).digest()
        counter += 1
    return out[: nbits // 8]


class ReseedRequired(Exception):
    pass


class DualEC:
    """Dual_EC_DRBG on P-256 with security strength 128. P and Q may be replaced to study the trapdoor."""

    def __init__(self, entropy: bytes, nonce: bytes = b"", personalization: bytes = b"", hash_name: str = "sha256",
                 P: Point = P_POINT, Q: Point = Q_POINT, reseed_interval: int = 2 ** 32) -> None:
        if 8 * len(entropy) < 128:
            raise ValueError("entropy input shorter than the security strength")
        if not (on_curve(P) and on_curve(Q)) or P is None or Q is None:
            raise ValueError("P and Q must be finite points on the curve")
        self.hash_name = hash_name
        self.P, self.Q = P, Q
        self.reseed_interval = reseed_interval
        self.s = int.from_bytes(hash_df(entropy + nonce + personalization, SEEDLEN, hash_name), "big")
        self.reseed_counter = 0

    def reseed(self, entropy: bytes, additional: bytes = b"") -> None:
        seed = self.s.to_bytes(SEEDLEN // 8, "big") + entropy + additional
        self.s = int.from_bytes(hash_df(seed, SEEDLEN, self.hash_name), "big")
        self.reseed_counter = 0

    def _phi_x(self, k: int, pt: Point) -> int:
        R = scalar_mult(k, pt)
        if R is None:  # x(O) is taken as 0; it happens only with probability about 2^-256
            return 0
        return R[0]

    def generate(self, nbytes: int, additional: bytes = b"", entropy: Optional[bytes] = None) -> bytes:
        """Return nbytes pseudorandom bytes. Passing entropy requests prediction resistance:
        the generator reseeds with it and the additional input first (SP 800-90A, Section 9.3.1)."""
        if entropy is not None:
            self.reseed(entropy, additional)
            additional = b""
        nblocks = -(-8 * nbytes // OUTLEN)
        if self.reseed_counter + nblocks > self.reseed_interval:  # @line L1
            raise ReseedRequired()
        if additional:  # @line L2
            t = self.s ^ int.from_bytes(hash_df(additional, SEEDLEN, self.hash_name), "big")  # @line L2
        else:
            t = self.s  # @line L2
        W = b""  # @line L3
        while True:  # @line L4
            self.s = self._phi_x(t, self.P)  # @line L5
            r = self._phi_x(self.s, self.Q)  # @line L6
            W += (r % 2 ** OUTLEN).to_bytes(OUTLEN // 8, "big")  # @line L6
            self.reseed_counter += 1  # @line L6
            t = self.s  # @line L6
            if len(W) >= nbytes:  # @line L7
                break
        self.s = self._phi_x(self.s, self.P)  # @line L8
        return W[:nbytes]  # @line L9


# ---------------------------------------------------------------- the trapdoor (Shumow and Ferguson 2007)


def candidate_states(e: int, block: bytes, Q: Point, candidates: Iterable[int]) -> List[int]:
    """Given e with P = e * Q and one output block r' (the rightmost OUTLEN bits of x(s*Q)),
    return the possible next inner states x(e * R) over the candidate high parts of x(s*Q)."""
    low = int.from_bytes(block, "big")
    states = []
    for hi in candidates:
        x = (hi << OUTLEN) | low
        R = lift_x(x)
        if R is None:
            continue
        # R = +-(s*Q), so e*R = +-(s*P) and its x coordinate is the next state, whatever the sign
        S = scalar_mult(e, R)
        states.append(0 if S is None else S[0])
    return states


def recover_state(e: int, block1: bytes, block2_prefix: bytes, P: Point, Q: Point,
                  candidates: Iterable[int] = range(2 ** (SEEDLEN - OUTLEN))) -> List[int]:
    """Shumow-Ferguson: from one full output block and a prefix of the next block of the same request,
    return the inner states s2 consistent with both. Each candidate s2 predicts every later block."""
    found = []
    for s2 in candidate_states(e, block1, Q, candidates):
        R = scalar_mult(s2, Q)
        r2 = 0 if R is None else R[0]
        if (r2 % 2 ** OUTLEN).to_bytes(OUTLEN // 8, "big").startswith(block2_prefix):
            found.append(s2)
    return found


def predict_blocks(s: int, nblocks: int, P: Point, Q: Point) -> bytes:
    """Output blocks that a generator with inner state s produces next within the same request."""
    out = b""
    for _ in range(nblocks):
        R = scalar_mult(s, Q)
        out += ((0 if R is None else R[0]) % 2 ** OUTLEN).to_bytes(OUTLEN // 8, "big")
        S = scalar_mult(s, P)
        s = 0 if S is None else S[0]
    return out
