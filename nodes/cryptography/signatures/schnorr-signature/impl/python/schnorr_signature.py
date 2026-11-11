# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schnorr-signature/. The authors are listed in prov/PS9P4P.jsonl.
"""Schnorr signatures: the textbook scheme on a toy group, and BIP 340 on secp256k1.

The first part is the scheme of the page on a small subgroup of Z_p^*, in the
two forms (R, s) and (e, s). The second part is BIP 340 (Schnorr signatures
for secp256k1, 2020), with x-only public keys and tagged hashes. The curve
arithmetic is written here from the curve equation y^2 = x^3 + 7. SHA-256 comes
from hashlib: the page is about the signature, not about the hash.

For study only. This code is not constant time, it branches on secret data,
and it must not be used to protect real data. Use libsecp256k1 for BIP 340, or
a FIPS 140 validated module or libsodium for other signatures.
"""

import hashlib
import secrets

# ---------------------------------------------------------------- toy group
# p = 2q + 1 with q prime. g = 4 is a square, so it has order q.
TOY_P = 2039
TOY_Q = 1019
TOY_G = 4


def toy_hash(r_elem: int, msg: bytes) -> int:
    """The challenge e = H(R || m) mod q of the toy scheme."""
    data = r_elem.to_bytes(2, "big") + msg
    return int.from_bytes(hashlib.sha256(data).digest(), "big") % TOY_Q


def toy_keygen(x: int) -> int:
    """Public key y = g^x mod p for a secret x in [1, q - 1]."""
    if not 1 <= x < TOY_Q:
        raise ValueError("secret key out of range")
    return pow(TOY_G, x, TOY_P)  # @line L0


def toy_sign(x: int, msg: bytes, k: int) -> tuple[int, int]:
    """Sign in the (R, s) form: R = g^k, e = H(R || m), s = k + e x mod q.

    The caller draws k uniformly in [1, q - 1], fresh for each signature.
    """
    if not 1 <= k < TOY_Q:  # @line L1
        raise ValueError("nonce out of range")
    r_elem = pow(TOY_G, k, TOY_P)  # @line L2
    e = toy_hash(r_elem, msg)  # @line L3
    s = (k + e * x) % TOY_Q  # @line L4
    return r_elem, s  # @line L5


def toy_verify(y: int, msg: bytes, sig: tuple[int, int]) -> bool:
    """Check g^s == R * y^e mod p with e = H(R || m)."""
    r_elem, s = sig
    if not 1 <= r_elem < TOY_P or pow(r_elem, TOY_Q, TOY_P) != 1:  # @line L6
        return False
    if not 0 <= s < TOY_Q:
        return False
    e = toy_hash(r_elem, msg)  # @line L7
    return pow(TOY_G, s, TOY_P) == r_elem * pow(y, e, TOY_P) % TOY_P  # @line L8


def toy_to_es(y: int, msg: bytes, sig: tuple[int, int]) -> tuple[int, int]:
    """Turn an (R, s) signature into the (e, s) form."""
    r_elem, s = sig
    return toy_hash(r_elem, msg), s


def toy_verify_es(y: int, msg: bytes, sig: tuple[int, int]) -> bool:
    """Check the (e, s) form: recompute R = g^s * y^(-e) and test e == H(R || m)."""
    e, s = sig
    if not (0 <= e < TOY_Q and 0 <= s < TOY_Q):
        return False
    r_elem = pow(TOY_G, s, TOY_P) * pow(y, TOY_Q - e, TOY_P) % TOY_P
    return e == toy_hash(r_elem, msg)


# ---------------------------------------------------------------- secp256k1
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
)

Point = tuple[int, int] | None  # None is the point at infinity


def point_add(a: Point, b: Point) -> Point:
    """The group law of y^2 = x^3 + 7 over F_p, in affine coordinates."""
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
    """k * a by double and add, from the most significant binary digit."""
    result = None
    for bit in bin(k)[2:] if k > 0 else "":
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


def lift_x(x: int) -> Point:
    """The point with x coordinate x and an even y, or None if there is none."""
    if x >= P:
        return None
    c = (pow(x, 3, P) + 7) % P
    y = pow(c, (P + 1) // 4, P)
    if y * y % P != c:
        return None
    return x, y if y % 2 == 0 else P - y


def tagged_hash(tag: str, msg: bytes) -> bytes:
    """hash_tag(x) = SHA256(SHA256(tag) || SHA256(tag) || x), BIP 340."""
    t = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(t + t + msg).digest()


def int_from(b: bytes) -> int:
    return int.from_bytes(b, "big")


def pubkey_gen(seckey: bytes) -> bytes:
    """The x-only public key bytes(d' G) of a 32-byte secret key."""
    d0 = int_from(seckey)
    if not 1 <= d0 <= N - 1:
        raise ValueError("secret key out of range")
    return xbytes(point_mul(G, d0))


def schnorr_sign(msg: bytes, seckey: bytes, aux_rand: bytes | None = None) -> bytes:
    """BIP 340 signing. aux_rand is 32 bytes of fresh randomness (None: draw it)."""
    if aux_rand is None:
        aux_rand = secrets.token_bytes(32)
    if len(aux_rand) != 32:
        raise ValueError("aux_rand must have 32 bytes")
    d0 = int_from(seckey)
    if not 1 <= d0 <= N - 1:
        raise ValueError("secret key out of range")
    pub = point_mul(G, d0)
    d = d0 if has_even_y(pub) else N - d0  # negate so that d G has an even y
    t = (d ^ int_from(tagged_hash("BIP0340/aux", aux_rand))).to_bytes(32, "big")
    k0 = int_from(tagged_hash("BIP0340/nonce", t + xbytes(pub) + msg)) % N
    if k0 == 0:
        raise ValueError("nonce is zero; this happens with negligible probability")
    r_pt = point_mul(G, k0)
    k = k0 if has_even_y(r_pt) else N - k0  # negate so that k G has an even y
    e = int_from(tagged_hash("BIP0340/challenge", xbytes(r_pt) + xbytes(pub) + msg)) % N
    sig = xbytes(r_pt) + ((k + e * d) % N).to_bytes(32, "big")
    if not schnorr_verify(msg, xbytes(pub), sig):
        raise RuntimeError("the new signature does not verify")
    return sig


def schnorr_verify(msg: bytes, pubkey: bytes, sig: bytes) -> bool:
    """BIP 340 verification of a 64-byte signature under a 32-byte x-only key."""
    if len(pubkey) != 32 or len(sig) != 64:
        return False
    pub = lift_x(int_from(pubkey))
    if pub is None:
        return False
    r = int_from(sig[:32])
    s = int_from(sig[32:])
    if r >= P or s >= N:
        return False
    e = int_from(tagged_hash("BIP0340/challenge", sig[:32] + pubkey + msg)) % N
    r_pt = point_add(point_mul(G, s), point_neg(point_mul(pub, e)))  # R = sG - eP
    if r_pt is None or not has_even_y(r_pt) or r_pt[0] != r:
        return False
    return True
