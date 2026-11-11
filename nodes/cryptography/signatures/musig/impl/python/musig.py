# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/musig/. The authors are listed in prov/AZY9JE.jsonl.
"""MuSig2 on secp256k1 in the form of BIP 327, with BIP 340 verification.

key_agg follows BIP 327 KeyAgg (plain 33-byte keys, no tweaks), so it
reproduces the official key aggregation vectors. sign, partial_sig_verify
and partial_sig_agg follow BIP 327 Sign, PartialSigVerify and PartialSigAgg
with no tweaks. The final signature verifies under plain BIP 340.

Simplification: nonce_gen draws two random nonces from a caller's
random.Random (or from secrets) instead of the hashed NonceGen of BIP 327,
so the signing test vectors of BIP 327 are not reproduced. Tweaking
(BIP 32, Taproot) is not implemented.

NOT SECURE. Affine arithmetic in Python, not constant time, no secure
erasure of nonces. For study only.
"""

import hashlib
import random
import secrets

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
)

Point = tuple[int, int] | None  # None is the point at infinity


def point_add(a: Point, b: Point) -> Point:
    if a is None:
        return b
    if b is None:
        return a
    if a[0] == b[0] and (a[1] + b[1]) % P == 0:
        return None
    if a == b:
        lam = 3 * a[0] * a[0] * pow(2 * a[1], -1, P) % P
    else:
        lam = (b[1] - a[1]) * pow(b[0] - a[0], -1, P) % P
    x3 = (lam * lam - a[0] - b[0]) % P
    return x3, (lam * (a[0] - x3) - a[1]) % P


def point_neg(a: Point) -> Point:
    return None if a is None else (a[0], (-a[1]) % P)


def point_mul(a: Point, k: int) -> Point:
    result = None
    for bit in bin(k % N)[2:] if k % N else "":
        result = point_add(result, result)
        if bit == "1":
            result = point_add(result, a)
    return result


def has_even_y(a: Point) -> bool:
    assert a is not None
    return a[1] % 2 == 0


def xbytes(a: Point) -> bytes:
    assert a is not None
    return a[0].to_bytes(32, "big")


def cbytes(a: Point) -> bytes:
    """The 33-byte compressed encoding."""
    assert a is not None
    return (b"\x02" if has_even_y(a) else b"\x03") + xbytes(a)


def cbytes_ext(a: Point) -> bytes:
    return b"\x00" * 33 if a is None else cbytes(a)


def lift_x(x: int) -> Point:
    if x >= P:
        return None
    c = (pow(x, 3, P) + 7) % P
    y = pow(c, (P + 1) // 4, P)
    if y * y % P != c:
        return None
    return x, y if y % 2 == 0 else P - y


def cpoint(b: bytes) -> Point:
    if len(b) != 33 or b[0] not in (2, 3):
        raise ValueError("bad compressed point")
    pt = lift_x(int.from_bytes(b[1:], "big"))
    if pt is None:
        raise ValueError("x is not on the curve")
    return pt if b[0] == 2 else point_neg(pt)


def cpoint_ext(b: bytes) -> Point:
    return None if b == b"\x00" * 33 else cpoint(b)


def tagged_hash(tag: str, msg: bytes) -> bytes:
    t = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(t + t + msg).digest()


def hint(tag: str, msg: bytes) -> int:
    return int.from_bytes(tagged_hash(tag, msg), "big") % N


# ------------------------------------------------------------ BIP 340 verify
def schnorr_verify(msg: bytes, pubkey: bytes, sig: bytes) -> bool:
    if len(pubkey) != 32 or len(sig) != 64:
        return False
    pub = lift_x(int.from_bytes(pubkey, "big"))
    r = int.from_bytes(sig[:32], "big")
    s = int.from_bytes(sig[32:], "big")
    if pub is None or r >= P or s >= N:
        return False
    e = hint("BIP0340/challenge", sig[:32] + pubkey + msg)
    r_pt = point_add(point_mul(G, s), point_neg(point_mul(pub, e)))
    return r_pt is not None and has_even_y(r_pt) and r_pt[0] == r


# ------------------------------------------------------------ key aggregation
def key_agg_coeff(pubkeys: list[bytes], pk: bytes) -> int:
    ell = tagged_hash("KeyAgg list", b"".join(pubkeys))  # @line L1
    second = next((k for k in pubkeys[1:] if k != pubkeys[0]), b"\x00" * 33)
    if pk == second:  # @line L2
        return 1
    return hint("KeyAgg coefficient", ell + pk)


def key_agg(pubkeys: list[bytes]) -> Point:
    """BIP 327 KeyAgg without tweaks: Q = sum a_i P_i."""
    q = None
    for pk in pubkeys:
        q = point_add(q, point_mul(cpoint(pk), key_agg_coeff(pubkeys, pk)))  # @line L3
    if q is None:
        raise ValueError("the aggregate key is the point at infinity")
    return q


# ------------------------------------------------------------ signing
def nonce_gen(rng: random.Random | None = None) -> tuple[tuple[int, int], bytes]:
    """Round 1: two secret nonces and the 66-byte public nonce (simplified)."""
    draw = (lambda: rng.randrange(1, N)) if rng else (lambda: secrets.randbelow(N - 1) + 1)
    k1, k2 = draw(), draw()  # @line L4
    return (k1, k2), cbytes(point_mul(G, k1)) + cbytes(point_mul(G, k2))


def nonce_agg(pubnonces: list[bytes]) -> bytes:
    out = b""
    for j in (0, 1):
        r_j = None
        for pn in pubnonces:
            r_j = point_add(r_j, cpoint(pn[33 * j : 33 * j + 33]))  # @line L5
        out += cbytes_ext(r_j)
    return out


def session_values(aggnonce: bytes, pubkeys: list[bytes], msg: bytes) -> tuple[Point, int, Point, int]:
    q = key_agg(pubkeys)
    b = hint("MuSig/noncecoef", aggnonce + xbytes(q) + msg)  # @line L6
    r = point_add(cpoint_ext(aggnonce[:33]), point_mul(cpoint_ext(aggnonce[33:]), b))
    if r is None:
        r = G
    e = hint("BIP0340/challenge", xbytes(r) + xbytes(q) + msg)  # @line L7
    return q, b, r, e


def sign(secnonce: tuple[int, int], sk: int, aggnonce: bytes, pubkeys: list[bytes], msg: bytes) -> int:
    """Round 2: the partial signature s_i of the signer with secret key sk."""
    q, b, r, e = session_values(aggnonce, pubkeys, msg)
    k1, k2 = secnonce
    if not has_even_y(r):  # @line L8
        k1, k2 = N - k1, N - k2
    g = 1 if has_even_y(q) else N - 1
    a = key_agg_coeff(pubkeys, cbytes(point_mul(G, sk)))
    return (k1 + b * k2 + e * a * g * sk) % N  # @line L9


def partial_sig_verify(psig: int, pubnonce: bytes, pk: bytes, aggnonce: bytes, pubkeys: list[bytes], msg: bytes) -> bool:
    q, b, r, e = session_values(aggnonce, pubkeys, msg)
    re = point_add(cpoint(pubnonce[:33]), point_mul(cpoint(pubnonce[33:]), b))
    if not has_even_y(r):
        re = point_neg(re)
    g = 1 if has_even_y(q) else N - 1
    a = key_agg_coeff(pubkeys, pk)
    rhs = point_add(re, point_mul(cpoint(pk), e * a * g))
    return point_mul(G, psig) == rhs  # @line L10


def partial_sig_agg(psigs: list[int], aggnonce: bytes, pubkeys: list[bytes], msg: bytes) -> bytes:
    _, _, r, _ = session_values(aggnonce, pubkeys, msg)
    s = sum(psigs) % N  # @line L11
    return xbytes(r) + s.to_bytes(32, "big")


# ------------------------------------------------------------ the naive scheme
def naive_key_sum(pubkeys: list[bytes]) -> Point:
    """Q = P_1 + ... + P_u with no coefficients: open to rogue keys."""
    q = None
    for pk in pubkeys:
        q = point_add(q, cpoint(pk))
    return q


def bip340_sign_with_scalar(d0: int, msg: bytes, k0: int) -> bytes:
    """Single-signer BIP 340 signing with a given nonce, for the rogue key demo."""
    pub = point_mul(G, d0)
    d = d0 if has_even_y(pub) else N - d0
    r_pt = point_mul(G, k0)
    k = k0 if has_even_y(r_pt) else N - k0
    e = hint("BIP0340/challenge", xbytes(r_pt) + xbytes(pub) + msg)
    return xbytes(r_pt) + ((k + e * d) % N).to_bytes(32, "big")
