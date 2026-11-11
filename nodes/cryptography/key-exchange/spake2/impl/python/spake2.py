# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spake2/. The authors are listed in prov/KH3HNV.jsonl.
"""SPAKE2 over P-256 with SHA-256, HKDF and HMAC (RFC 9382, ciphersuite
SPAKE2-P256-SHA256-HKDF-HMAC).

The P-256 arithmetic and HKDF are small local copies written for this page.
SHA-256 and HMAC-SHA256 come from hashlib and hmac.

For study only. The code is not constant time (the scalar multiplication
branches on the bits of the scalar), and it must not protect real data. Use a
maintained library instead.

Lines marked L1 to L12 match the pseudocode on the page.
"""

import hashlib
import hmac
import secrets

# ---------------------------------------------------------------- P-256 (FIPS 186-5, SP 800-186)

P = 2**256 - 2**224 + 2**192 + 2**96 - 1
A_CURVE = P - 3
B_CURVE = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
ORDER = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
GX = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
GY = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5
COFACTOR = 1
INF = None  # the point at infinity, the unit element I


def on_curve(Q) -> bool:
    if Q is INF:
        return True
    x, y = Q
    return 0 <= x < P and 0 <= y < P and (y * y - (x * x * x + A_CURVE * x + B_CURVE)) % P == 0


def point_neg(Q):
    return INF if Q is INF else (Q[0], (-Q[1]) % P)


def point_add(Q, R):
    """The group law in affine coordinates."""
    if Q is INF:
        return R
    if R is INF:
        return Q
    x1, y1 = Q
    x2, y2 = R
    if x1 == x2:
        if (y1 + y2) % P == 0:
            return INF
        lam = (3 * x1 * x1 + A_CURVE) * pow(2 * y1, -1, P) % P
    else:
        lam = (y2 - y1) * pow(x2 - x1, -1, P) % P
    x3 = (lam * lam - x1 - x2) % P
    return (x3, (lam * (x1 - x3) - y1) % P)


def scalar_mult(k: int, Q):
    """k Q by double and add, from the top bit. Not constant time."""
    R = INF
    for bit in bin(k % ORDER)[2:] if Q is not INF else "":
        R = point_add(R, R)
        if bit == "1":
            R = point_add(R, Q)
    return R


G = (GX, GY)


def encode_uncompressed(Q) -> bytes:
    """SEC1 uncompressed encoding 04 || x || y."""
    if Q is INF:
        raise ValueError("cannot encode the point at infinity")
    return b"\x04" + Q[0].to_bytes(32, "big") + Q[1].to_bytes(32, "big")


def decode_point(data: bytes):
    """Decode a SEC1 compressed or uncompressed point, and check that it is on the curve."""
    if len(data) == 65 and data[0] == 4:
        Q = (int.from_bytes(data[1:33], "big"), int.from_bytes(data[33:], "big"))
    elif len(data) == 33 and data[0] in (2, 3):
        x = int.from_bytes(data[1:], "big")
        if x >= P:
            raise ValueError("x out of range")
        rhs = (x * x * x + A_CURVE * x + B_CURVE) % P
        y = pow(rhs, (P + 1) // 4, P)       # P = 3 mod 4
        if y * y % P != rhs:
            raise ValueError("x is not on the curve")
        if y % 2 != data[0] % 2:
            y = P - y
        Q = (x, y)
    else:
        raise ValueError("bad point encoding")
    if not on_curve(Q):
        raise ValueError("point not on the curve")
    return Q


# RFC 9382, Section 6, the P-256 seeds of M and N (compressed SEC1).
M = decode_point(bytes.fromhex("02886e2f97ace46e55ba9dd7242579f2993b64e16ef3dcab95afd497333d8fa12f"))
N = decode_point(bytes.fromhex("03d8bbd6c639c62937b04d997f38c3770719c629d7014d49a24b4f98baa1292b49"))

# ---------------------------------------------------------------- HKDF (RFC 5869), local copy


def hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
    if not salt:
        salt = bytes(32)
    return hmac.new(salt, ikm, hashlib.sha256).digest()


def hkdf_expand(prk: bytes, info: bytes, length: int) -> bytes:
    out, t, i = b"", b"", 1
    while len(out) < length:
        t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
        out += t
        i += 1
    return out[:length]


def hkdf(ikm: bytes, salt: bytes, info: bytes, length: int) -> bytes:
    return hkdf_expand(hkdf_extract(salt, ikm), info, length)


# ---------------------------------------------------------------- SPAKE2 (RFC 9382, Sections 3 and 4)


def len8(s: bytes) -> bytes:
    """len(S) as an eight-byte little-endian number, then S."""
    return len(s).to_bytes(8, "little") + s


class Spake2Error(ValueError):
    pass


def start_a(w: int, x: int) -> bytes:
    """A: X = x P, pA = w M + X."""
    X = scalar_mult(x, G)                                              # @line L1
    return encode_uncompressed(point_add(scalar_mult(w, M), X))        # @line L2


def start_b(w: int, y: int) -> bytes:
    """B: Y = y P, pB = w N + Y."""
    Y = scalar_mult(y, G)                                              # @line L3
    return encode_uncompressed(point_add(scalar_mult(w, N), Y))        # @line L4


def finish(role: str, w: int, secret: int, pA: bytes, pB: bytes, idA: bytes, idB: bytes, aad: bytes = b""):
    """Return (K, TT, Ke, KcA, KcB). role is "A" or "B"."""
    peer = decode_point(pB if role == "A" else pA)                     # @line L5 (membership check)
    blind = N if role == "A" else M
    K = scalar_mult(COFACTOR * secret, point_add(peer, point_neg(scalar_mult(w, blind))))  # @line L6
    if K is INF:
        raise Spake2Error("K is the identity")
    Kb = encode_uncompressed(K)
    TT = (len8(idA) + len8(idB) + len8(pA) + len8(pB)                  # @line L7
          + len8(Kb) + len8(w.to_bytes(32, "big")))
    h = hashlib.sha256(TT).digest()
    Ke, Ka = h[:16], h[16:]                                            # @line L8
    kc = hkdf(Ka, b"", b"ConfirmationKeys" + aad, 32)                 # @line L9
    return Kb, TT, Ke, kc[:16], kc[16:]


def confirm(Kc: bytes, TT: bytes) -> bytes:
    """cA = MAC(KcA, TT) or cB = MAC(KcB, TT), with HMAC-SHA256."""
    return hmac.new(Kc, TT, hashlib.sha256).digest()                   # @line L10


def run(pw_a: int, pw_b: int, idA: bytes = b"client", idB: bytes = b"server", rng=secrets.randbelow):
    """A full run with key confirmation. Returns (Ke_A, Ke_B) or raises Spake2Error."""
    x = rng(ORDER - 1) + 1
    y = rng(ORDER - 1) + 1
    pA = start_a(pw_a, x)
    pB = start_b(pw_b, y)
    _, TTa, KeA, KcA_a, KcB_a = finish("A", pw_a, x, pA, pB, idA, idB)
    _, TTb, KeB, KcA_b, KcB_b = finish("B", pw_b, y, pA, pB, idA, idB)
    cA = confirm(KcA_a, TTa)
    if not hmac.compare_digest(cA, confirm(KcA_b, TTb)):               # @line L11
        raise Spake2Error("B rejects cA")
    cB = confirm(KcB_b, TTb)
    if not hmac.compare_digest(cB, confirm(KcB_a, TTa)):               # @line L12
        raise Spake2Error("A rejects cB")
    return KeA, KeB


def password_to_scalar(password: bytes, salt: bytes = b"spake2 demo") -> int:
    """w = MHF(pw) mod p. The page uses scrypt with small parameters for a demo.

    RFC 9382 leaves the MHF to the application and suggests a hash 64 bits
    longer than p before the reduction; scrypt gives 40 bytes here.
    """
    h = hashlib.scrypt(password, salt=salt, n=2**10, r=8, p=1, dklen=40)
    return int.from_bytes(h, "big") % ORDER
