# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/x3dh/. The authors are listed in prov/F1F34V.jsonl.
"""X3DH (Marlinspike and Perrin, Signal specification, revision 1,
2016-11-04), with curve X25519 and hash SHA-256.

Local copies written for this page: X25519 (RFC 7748), HKDF (RFC 5869),
edwards25519 arithmetic, and XEdDSA signing and verification (Perrin, "The
XEdDSA and VXEdDSA Signature Schemes", revision 1, 2016-10-20). SHA-256,
SHA-512 and HMAC come from hashlib and hmac. The first message carries a
study AEAD (encrypt-then-MAC with an HMAC-SHA256 key stream), not a standard
AEAD.

For study only. The code is not constant time, and it must not protect real
data. Use libsignal or another maintained implementation.

Lines marked L1 to L16 match the pseudocode on the page.
"""

import hashlib
import hmac
import secrets

# ---------------------------------------------------------------- X25519 (RFC 7748, Section 5), local copy

P = 2**255 - 19
A24 = 121665


def clamp(k: bytes) -> int:
    b = bytearray(k)
    b[0] &= 248
    b[31] &= 127
    b[31] |= 64
    return int.from_bytes(b, "little")


def x25519(k: bytes, u: bytes) -> bytes:
    kk = clamp(k)
    b = bytearray(u)
    b[31] &= 127
    x1 = int.from_bytes(b, "little") % P
    x2, z2, x3, z3, swap = 1, 0, x1, 1, 0
    for t in range(254, -1, -1):
        kt = (kk >> t) & 1
        swap ^= kt
        if swap:
            x2, x3, z2, z3 = x3, x2, z3, z2
        swap = kt
        a, b_ = (x2 + z2) % P, (x2 - z2) % P
        aa, bb = a * a % P, b_ * b_ % P
        e = (aa - bb) % P
        c, d = (x3 + z3) % P, (x3 - z3) % P
        da, cb = d * a % P, c * b_ % P
        x3 = (da + cb) ** 2 % P
        z3 = x1 * (da - cb) ** 2 % P
        x2 = aa * bb % P
        z2 = e * (aa + A24 * e) % P
    if swap:
        x2, z2 = x3, z3
    return (x2 * pow(z2, P - 2, P) % P).to_bytes(32, "little")


BASE_U = (9).to_bytes(32, "little")

# ---------------------------------------------------------------- edwards25519 (RFC 8032, Section 5.1)

Q = 2**252 + 27742317777372353535851937790883648493  # the order of the base point
D = -121665 * pow(121666, P - 2, P) % P
SQRT_M1 = pow(2, (P - 1) // 4, P)


def _recover_x(y: int, sign: int):
    if y >= P:
        return None
    x2 = (y * y - 1) * pow(D * y * y + 1, P - 2, P) % P
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (P + 3) // 8, P)
    if (x * x - x2) % P != 0:
        x = x * SQRT_M1 % P
    if (x * x - x2) % P != 0:
        return None
    if x & 1 != sign:
        x = P - x
    return x


BY = 4 * pow(5, P - 2, P) % P
BASE = (_recover_x(BY, 0), BY, 1, _recover_x(BY, 0) * BY % P)  # extended coordinates (X, Y, Z, T)
IDENT = (0, 1, 1, 0)


def ed_add(p1, p2):
    x1, y1, z1, t1 = p1
    x2, y2, z2, t2 = p2
    a = (y1 - x1) * (y2 - x2) % P
    b = (y1 + x1) * (y2 + x2) % P
    c = 2 * t1 * t2 * D % P
    d = 2 * z1 * z2 % P
    e, f, g, h = b - a, d - c, d + c, b + a
    return (e * f % P, g * h % P, f * g % P, e * h % P)


def ed_mul(k: int, pt):
    r = IDENT
    while k > 0:
        if k & 1:
            r = ed_add(r, pt)
        pt = ed_add(pt, pt)
        k >>= 1
    return r


def ed_encode(pt) -> bytes:
    x, y, z, _ = pt
    zi = pow(z, P - 2, P)
    x, y = x * zi % P, y * zi % P
    return (y | ((x & 1) << 255)).to_bytes(32, "little")


def ed_decode(s: bytes):
    v = int.from_bytes(s, "little")
    y, sign = v & ((1 << 255) - 1), v >> 255
    x = _recover_x(y, sign)
    if x is None:
        return None
    return (x, y, 1, x * y % P)


def ed_equal(p1, p2) -> bool:
    return (p1[0] * p2[2] - p2[0] * p1[2]) % P == 0 and (p1[1] * p2[2] - p2[1] * p1[2]) % P == 0


def sha512_int(*parts: bytes) -> int:
    return int.from_bytes(hashlib.sha512(b"".join(parts)).digest(), "little")


# Ed25519 (RFC 8032, Section 5.1.5 to 5.1.7): only used to check the curve code.

def ed25519_public(seed: bytes) -> bytes:
    h = hashlib.sha512(seed).digest()
    return ed_encode(ed_mul(clamp(h[:32]), BASE))


def ed25519_sign(seed: bytes, msg: bytes) -> bytes:
    h = hashlib.sha512(seed).digest()
    a = clamp(h[:32])
    A = ed_encode(ed_mul(a, BASE))
    r = sha512_int(h[32:], msg) % Q
    R = ed_encode(ed_mul(r, BASE))
    s = (r + sha512_int(R, A, msg) * a) % Q
    return R + s.to_bytes(32, "little")


def ed25519_verify(public: bytes, msg: bytes, sig: bytes) -> bool:
    A = ed_decode(public)
    R = ed_decode(sig[:32])
    s = int.from_bytes(sig[32:], "little")
    if A is None or R is None or s >= Q:
        return False
    k = sha512_int(sig[:32], public, msg) % Q
    return ed_equal(ed_mul(s, BASE), ed_add(R, ed_mul(k, A)))


# ---------------------------------------------------------------- XEdDSA (Perrin 2016, Sections 2.3 and 3)


def calculate_key_pair(k: int):
    """From a Montgomery private scalar k: the Edwards public key A with sign bit 0, and a."""
    E = ed_mul(k, BASE)
    enc = ed_encode(E)
    sign = enc[31] >> 7
    A = enc[:31] + bytes([enc[31] & 0x7F])
    a = (-k) % Q if sign else k % Q
    return A, a


def hash_i(i: int, *parts: bytes) -> int:
    """hash_i(X) = SHA-512(2^256 - 1 - i as 32 little-endian bytes || X)."""
    prefix = (2**256 - 1 - i).to_bytes(32, "little")
    return sha512_int(prefix, *parts)


def xeddsa_sign(k_bytes: bytes, msg: bytes, Z: bytes) -> bytes:
    k = clamp(k_bytes)
    A, a = calculate_key_pair(k)
    r = hash_i(1, a.to_bytes(32, "little"), msg, Z) % Q
    R = ed_encode(ed_mul(r, BASE))
    h = sha512_int(R, A, msg) % Q
    s = (r + h * a) % Q
    return R + s.to_bytes(32, "little")


def u_to_y(u: int) -> int:
    return (u - 1) * pow(u + 1, P - 2, P) % P


def xeddsa_verify(u_bytes: bytes, msg: bytes, sig: bytes) -> bool:
    u = int.from_bytes(u_bytes, "little") & ((1 << 255) - 1)
    R_bytes, s = sig[:32], int.from_bytes(sig[32:], "little")
    if u >= P or (int.from_bytes(R_bytes, "little") & ((1 << 255) - 1)) >= P or s >= Q:
        return False
    A_bytes = u_to_y(u).to_bytes(32, "little")      # convert_mont: sign bit 0
    A = ed_decode(A_bytes)
    if A is None:
        return False
    h = sha512_int(R_bytes, A_bytes, msg) % Q
    Rcheck = ed_add(ed_mul(s, BASE), ed_mul((Q - h) % Q, A))
    return hmac.compare_digest(ed_encode(Rcheck), R_bytes)


# ---------------------------------------------------------------- HKDF (RFC 5869), local copy


def hkdf(ikm: bytes, salt: bytes, info: bytes, length: int) -> bytes:
    prk = hmac.new(salt, ikm, hashlib.sha256).digest()
    out, t, i = b"", b"", 1
    while len(out) < length:
        t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
        out += t
        i += 1
    return out[:length]


# ---------------------------------------------------------------- X3DH (Section 2 and 3 of the spec)

INFO = b"X3DHStudy"


class KeyPair:
    def __init__(self, private: bytes):
        self.private = private
        self.public = x25519(private, BASE_U)


def encode(pk: bytes) -> bytes:
    """Encode(PK): a one-byte curve type 0x05, then the little-endian u-coordinate."""
    return b"\x05" + pk


def dh(pair: KeyPair, pk: bytes) -> bytes:
    return x25519(pair.private, pk)


def kdf(km: bytes) -> bytes:
    """KDF(KM) = HKDF(salt = 32 zero bytes, ikm = 32 0xFF bytes || KM, info), 32 bytes."""
    return hkdf(b"\xff" * 32 + km, bytes(32), INFO, 32)


class X3DHError(ValueError):
    pass


class Bob:
    """The responder. He publishes a prekey bundle to a server, then goes offline."""

    def __init__(self, rng=secrets.token_bytes, n_opk: int = 3):
        self.rng = rng
        self.IK = KeyPair(rng(32))
        self.SPK = KeyPair(rng(32))
        self.spk_sig = xeddsa_sign(self.IK.private, encode(self.SPK.public), rng(64))   # @line L1
        self.OPK = {i: KeyPair(rng(32)) for i in range(n_opk)}

    def bundle(self, with_opk: bool = True):
        opk_id = next(iter(self.OPK), None) if with_opk else None
        opk = self.OPK[opk_id].public if opk_id is not None else None
        return dict(IK=self.IK.public, SPK=self.SPK.public, sig=self.spk_sig, opk_id=opk_id, OPK=opk)   # @line L2

    def receive(self, msg: dict) -> bytes:
        dh1 = dh(self.SPK, msg["IK"])                                  # @line L11
        dh2 = dh(self.IK, msg["EK"])
        dh3 = dh(self.SPK, msg["EK"])
        km = dh1 + dh2 + dh3
        if msg["opk_id"] is not None:
            if msg["opk_id"] not in self.OPK:
                raise X3DHError("unknown or used one-time prekey")
            km += dh(self.OPK.pop(msg["opk_id"]), msg["EK"])           # @line L12 (delete after use)
        sk = kdf(km)                                                   # @line L13
        ad = encode(msg["IK"]) + encode(self.IK.public)                # @line L14
        if aead_decrypt(sk, msg["ct"], ad) is None:                    # @line L15
            raise X3DHError("first message does not decrypt")
        return sk                                                      # @line L16


def alice_send(IK_A: KeyPair, bundle: dict, plaintext: bytes, rng=secrets.token_bytes):
    if not xeddsa_verify(bundle["IK"], encode(bundle["SPK"]), bundle["sig"]):   # @line L3
        raise X3DHError("bad signature on the signed prekey")
    EK = KeyPair(rng(32))                                              # @line L4
    dh1 = dh(IK_A, bundle["SPK"])                                      # @line L5
    dh2 = dh(EK, bundle["IK"])                                         # @line L6
    dh3 = dh(EK, bundle["SPK"])                                        # @line L7
    km = dh1 + dh2 + dh3
    if bundle["OPK"] is not None:
        km += dh(EK, bundle["OPK"])                                    # @line L8
    sk = kdf(km)                                                       # @line L9
    ad = encode(IK_A.public) + encode(bundle["IK"])
    msg = dict(IK=IK_A.public, EK=EK.public, opk_id=bundle["opk_id"], ct=aead_encrypt(sk, plaintext, ad))   # @line L10
    return sk, ad, msg


# ---------------------------------------------------------------- the study AEAD for the first message


def aead_encrypt(key: bytes, pt: bytes, ad: bytes) -> bytes:
    ks = b"".join(hmac.new(key, b"enc" + i.to_bytes(4, "big"), hashlib.sha256).digest()
                  for i in range((len(pt) + 31) // 32))
    ct = bytes(a ^ b for a, b in zip(pt, ks))
    return ct + hmac.new(key, b"mac" + ad + ct, hashlib.sha256).digest()


def aead_decrypt(key: bytes, data: bytes, ad: bytes):
    ct, tag = data[:-32], data[-32:]
    if not hmac.compare_digest(tag, hmac.new(key, b"mac" + ad + ct, hashlib.sha256).digest()):
        return None
    ks = b"".join(hmac.new(key, b"enc" + i.to_bytes(4, "big"), hashlib.sha256).digest()
                  for i in range((len(ct) + 31) // 32))
    return bytes(a ^ b for a, b in zip(ct, ks))
