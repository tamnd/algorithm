# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cpace/. The authors are listed in prov/RGPFSD.jsonl.
"""CPace with the group G_X25519 and the hash SHA-512, as in
draft-irtf-cfrg-cpace-21 (April 2026), Sections 6 to 8.2 and Appendix A.

X25519 (RFC 7748) and the Elligator 2 map (RFC 9380, as repeated in the
draft, Appendix A.5) are small local copies written for this page. SHA-512
comes from hashlib.

For study only. The code is not constant time (Python ints are not, and the
square test branches), and it must not protect real data. Use a maintained
library instead.

Lines marked L1 to L12 match the pseudocode on the page.
"""

import hashlib
import secrets

# ---------------------------------------------------------------- X25519 (RFC 7748, Section 5), local copy

Q25519 = 2**255 - 19
A24 = 121665
A_MONT = 486662


def decode_scalar(k: bytes) -> int:
    b = bytearray(k)
    b[0] &= 248
    b[31] &= 127
    b[31] |= 64
    return int.from_bytes(b, "little")


def decode_u(u: bytes) -> int:
    """decodeUCoordinate: mask bit 255, then read little-endian (not reduced mod q)."""
    b = bytearray(u)
    b[31] &= 127
    return int.from_bytes(b, "little")


def encode_u(u: int) -> bytes:
    return (u % Q25519).to_bytes(32, "little")


def x25519(k: bytes, u: bytes) -> bytes:
    """The Montgomery ladder of RFC 7748, Section 5."""
    kk = decode_scalar(k)
    x1 = decode_u(u) % Q25519
    x2, z2, x3, z3, swap = 1, 0, x1, 1, 0
    for t in range(254, -1, -1):
        kt = (kk >> t) & 1
        swap ^= kt
        if swap:
            x2, x3, z2, z3 = x3, x2, z3, z2
        swap = kt
        a = (x2 + z2) % Q25519
        aa = a * a % Q25519
        b = (x2 - z2) % Q25519
        bb = b * b % Q25519
        e = (aa - bb) % Q25519
        c = (x3 + z3) % Q25519
        d = (x3 - z3) % Q25519
        da = d * a % Q25519
        cb = c * b % Q25519
        x3 = (da + cb) ** 2 % Q25519
        z3 = x1 * (da - cb) ** 2 % Q25519
        x2 = aa * bb % Q25519
        z2 = e * (aa + A24 * e) % Q25519
    if swap:
        x2, x3, z2, z3 = x3, x2, z3, z2
    return encode_u(x2 * pow(z2, Q25519 - 2, Q25519))


# ---------------------------------------------------------------- Elligator 2 for Curve25519 (RFC 9380, Section 6.7.1)

Z_ELL2 = 2  # the non-square of the draft, Appendix A.5


def elligator2(r: int) -> int:
    """Map a field element r to the u-coordinate of a point of Curve25519."""
    q = Q25519
    v = (-A_MONT * pow(1 + Z_ELL2 * r * r, q - 2, q)) % q              # v = -A / (1 + z r^2)
    eps = pow((v * v * v + A_MONT * v * v + v) % q, (q - 1) // 2, q)   # the Legendre symbol, 1 or q-1 (or 0)
    if eps == q - 1:
        eps = -1
    x = (eps * v - (1 - eps) * A_MONT * pow(2, q - 2, q)) % q          # x = eps v - (1 - eps) A / 2
    return x


# ---------------------------------------------------------------- string utilities (draft, Appendix A.1 to A.3)


def prepend_len(data: bytes) -> bytes:
    """Prepend the LEB128 encoding of the length."""
    length = len(data)
    enc = b""
    while True:
        if length < 128:
            enc += bytes([length])
        else:
            enc += bytes([(length & 0x7F) + 0x80])
        length >>= 7
        if length == 0:
            break
    return enc + data


def lv_cat(*args: bytes) -> bytes:
    return b"".join(prepend_len(a) for a in args)


def lexiographically_larger(b1: bytes, b2: bytes) -> bool:
    for x, y in zip(b1, b2):
        if x != y:
            return x > y
    return len(b1) > len(b2)


def o_cat(b1: bytes, b2: bytes) -> bytes:
    return b"oc" + (b1 + b2 if lexiographically_larger(b1, b2) else b2 + b1)


def transcript_ir(Ya: bytes, ADa: bytes, Yb: bytes, ADb: bytes) -> bytes:
    return lv_cat(Ya, ADa) + lv_cat(Yb, ADb)


def transcript_oc(Ya: bytes, ADa: bytes, Yb: bytes, ADb: bytes) -> bytes:
    return o_cat(lv_cat(Ya, ADa), lv_cat(Yb, ADb))


# ---------------------------------------------------------------- CPace with G_X25519 and SHA-512

DSI = b"CPace255"
S_IN_BYTES = 128  # the input block size of SHA-512
IDENTITY = bytes(32)


def h_hash(m: bytes, length: int = 64) -> bytes:
    return hashlib.sha512(m).digest()[:length]


def generator_string(dsi: bytes, prs: bytes, ci: bytes, sid: bytes, s_in_bytes: int = S_IN_BYTES) -> bytes:
    len_zpad = max(0, s_in_bytes - 1 - len(prepend_len(prs)) - len(prepend_len(dsi)))
    return lv_cat(dsi, prs, bytes(len_zpad), ci, sid)


def calculate_generator(prs: bytes, ci: bytes, sid: bytes) -> bytes:
    gen_str = generator_string(DSI, prs, ci, sid)                     # @line L1
    gen_hash = h_hash(gen_str, 32)                                    # @line L2
    u = decode_u(gen_hash)                                            # @line L3
    return encode_u(elligator2(u))                                    # @line L4


def sample_scalar() -> bytes:
    return secrets.token_bytes(32)


def scalar_mult_vfy(y: bytes, X: bytes) -> bytes:
    return x25519(y, X)


class CPaceError(ValueError):
    pass


def message(prs: bytes, ci: bytes, sid: bytes, y: bytes) -> bytes:
    """The public share Y = X25519(y, g) of one party."""
    g = calculate_generator(prs, ci, sid)
    return x25519(y, g)                                               # @line L5


def derive_isk(y: bytes, Y_peer: bytes, sid: bytes, transcript: bytes) -> bytes:
    K = scalar_mult_vfy(y, Y_peer)                                    # @line L6
    if K == IDENTITY:                                                 # @line L7
        raise CPaceError("K is the neutral element")
    return h_hash(lv_cat(DSI + b"_ISK", sid, K) + transcript)         # @line L8


def run(prs_a: bytes, prs_b: bytes, ci: bytes = b"", sid: bytes = b"", ada: bytes = b"ADa", adb: bytes = b"ADb",
        ya: bytes | None = None, yb: bytes | None = None, initiator_responder: bool = True):
    """One CPace run. Returns (ISK_A, ISK_B)."""
    ya = ya or sample_scalar()
    yb = yb or sample_scalar()
    Ya = message(prs_a, ci, sid, ya)                                  # @line L9: A sends Ya, ADa
    Yb = message(prs_b, ci, sid, yb)                                  # @line L10: B sends Yb, ADb
    tr = transcript_ir if initiator_responder else transcript_oc
    isk_a = derive_isk(ya, Yb, sid, tr(Ya, ada, Yb, adb))             # @line L11
    isk_b = derive_isk(yb, Ya, sid, tr(Ya, ada, Yb, adb))             # @line L12
    return isk_a, isk_b
