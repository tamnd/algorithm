# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chaum-blind-signature/. The authors are listed in prov/BFYHY3.jsonl.
"""Chaum's RSA blind signature in the form of RFC 9474 (RSABSSA).

The client encodes its message with EMSA-PSS (RFC 8017, Section 9.1.1),
multiplies the encoding by r^e and sends the product. The signer applies its
private exponent without seeing the message. The client multiplies the answer
by r^-1 and gets an ordinary RSASSA-PSS signature, which any RSA-PSS verifier
accepts. The four named variants of RFC 9474, Section 5, use SHA-384 and MGF1
with SHA-384; they differ in the salt length (48 or 0) and in the message
preparation (a random 32-byte prefix or none).

For study only. The code is not constant time (Python big integers), it does
not protect the signer against timing or fault attacks, and it must not
protect real data.
"""

import hashlib
import math
import secrets
from dataclasses import dataclass

HASH = hashlib.sha384
H_LEN = 48


@dataclass(frozen=True)
class Variant:
    name: str
    salt_len: int
    randomized: bool


PSS_RANDOMIZED = Variant("RSABSSA-SHA384-PSS-Randomized", 48, True)
PSSZERO_RANDOMIZED = Variant("RSABSSA-SHA384-PSSZERO-Randomized", 0, True)
PSS_DETERMINISTIC = Variant("RSABSSA-SHA384-PSS-Deterministic", 48, False)
PSSZERO_DETERMINISTIC = Variant("RSABSSA-SHA384-PSSZERO-Deterministic", 0, False)


@dataclass(frozen=True)
class PublicKey:
    n: int
    e: int

    @property
    def k(self) -> int:
        """modulus_len, the length of n in bytes."""
        return (self.n.bit_length() + 7) // 8


@dataclass(frozen=True)
class SecretKey:
    pk: PublicKey
    d: int


def key_from_primes(p: int, q: int, e: int = 65537) -> SecretKey:
    n = p * q
    d = pow(e, -1, math.lcm(p - 1, q - 1))
    return SecretKey(PublicKey(n, e), d)


def i2osp(x: int, length: int) -> bytes:
    return x.to_bytes(length, "big")


def os2ip(b: bytes) -> int:
    return int.from_bytes(b, "big")


# ------------------------------------------------------- EMSA-PSS (RFC 8017)


def mgf1(seed: bytes, length: int) -> bytes:
    out = b""
    c = 0
    while len(out) < length:
        out += HASH(seed + i2osp(c, 4)).digest()
        c += 1
    return out[:length]


def emsa_pss_encode(m: bytes, em_bits: int, salt: bytes) -> bytes:
    em_len = (em_bits + 7) // 8
    m_hash = HASH(m).digest()
    if em_len < H_LEN + len(salt) + 2:
        raise ValueError("encoding error")
    h = HASH(bytes(8) + m_hash + salt).digest()
    db = bytes(em_len - len(salt) - H_LEN - 2) + b"\x01" + salt
    masked = bytes(a ^ b for a, b in zip(db, mgf1(h, em_len - H_LEN - 1)))
    top = 8 * em_len - em_bits  # clear the leftmost bits above em_bits
    masked = bytes([masked[0] & (0xFF >> top)]) + masked[1:]
    return masked + h + b"\xbc"


def emsa_pss_verify(m: bytes, em: bytes, em_bits: int, salt_len: int) -> bool:
    em_len = (em_bits + 7) // 8
    if len(em) != em_len or em_len < H_LEN + salt_len + 2 or em[-1] != 0xBC:
        return False
    masked, h = em[: em_len - H_LEN - 1], em[em_len - H_LEN - 1 : -1]
    top = 8 * em_len - em_bits
    if masked[0] & ~(0xFF >> top) & 0xFF:
        return False
    db = bytes(a ^ b for a, b in zip(masked, mgf1(h, em_len - H_LEN - 1)))
    db = bytes([db[0] & (0xFF >> top)]) + db[1:]
    pad = em_len - H_LEN - salt_len - 2
    if db[:pad] != bytes(pad) or db[pad] != 1:
        return False
    salt = db[pad + 1 :]
    return HASH(bytes(8) + HASH(m).digest() + salt).digest() == h


def rsassa_pss_verify(pk: PublicKey, m: bytes, sig: bytes, salt_len: int) -> bool:
    """RFC 8017, Section 8.1.2."""
    if len(sig) != pk.k:
        return False
    s = os2ip(sig)
    if s >= pk.n:
        return False
    em_bits = pk.n.bit_length() - 1
    em = i2osp(pow(s, pk.e, pk.n), (em_bits + 7) // 8)
    return emsa_pss_verify(m, em, em_bits, salt_len)


# ------------------------------------------------------------ the protocol


def prepare(msg: bytes, v: Variant, prefix: bytes | None = None) -> bytes:
    """RFC 9474, Section 4.1. Returns input_msg."""
    if not v.randomized:
        return msg
    prefix = secrets.token_bytes(32) if prefix is None else prefix
    return prefix + msg  # @line L1


def blind(
    pk: PublicKey, input_msg: bytes, v: Variant, salt: bytes | None = None, r: int | None = None
) -> tuple[bytes, int]:
    """Client. RFC 9474, Section 4.2. Returns (blinded_msg, inv)."""
    salt = secrets.token_bytes(v.salt_len) if salt is None else salt
    encoded = emsa_pss_encode(input_msg, pk.n.bit_length() - 1, salt)
    m = os2ip(encoded)  # @line L2
    if math.gcd(m, pk.n) != 1:  # @line L3
        raise ValueError("invalid input")
    while r is None or math.gcd(r, pk.n) != 1:
        r = 1 + secrets.randbelow(pk.n - 1)
    inv = pow(r, -1, pk.n)  # @line L4
    z = m * pow(r, pk.e, pk.n) % pk.n  # @line L5
    return i2osp(z, pk.k), inv


def blind_sign(sk: SecretKey, blinded_msg: bytes) -> bytes:
    """Signer. RFC 9474, Section 4.3. It never sees input_msg."""
    m = os2ip(blinded_msg)
    if len(blinded_msg) != sk.pk.k or m >= sk.pk.n:
        raise ValueError("message representative out of range")
    s = pow(m, sk.d, sk.pk.n)  # @line L6
    if pow(s, sk.pk.e, sk.pk.n) != m:  # @line L7
        raise ValueError("signing failure")
    return i2osp(s, sk.pk.k)


def finalize(pk: PublicKey, input_msg: bytes, blind_sig: bytes, inv: int, v: Variant) -> bytes:
    """Client. RFC 9474, Section 4.4."""
    if len(blind_sig) != pk.k:
        raise ValueError("unexpected input size")
    sig = i2osp(os2ip(blind_sig) * inv % pk.n, pk.k)  # @line L8
    if not rsassa_pss_verify(pk, input_msg, sig, v.salt_len):  # @line L9
        raise ValueError("invalid signature")
    return sig


def verify(pk: PublicKey, input_msg: bytes, sig: bytes, v: Variant) -> bool:
    """RFC 9474, Section 4.5: plain RSASSA-PSS verification of input_msg."""
    return rsassa_pss_verify(pk, input_msg, sig, v.salt_len)  # @line L10


def blinding_factor_for(pk: PublicKey, blinded_msg: bytes, blind_sig: bytes, sig: bytes) -> int:
    """For one signer view (z, s') and one final signature s, return the r
    with z = m * r^e and s = s' / r. Such an r exists for every pair, which is
    why the signer cannot link a signature to its session."""
    return os2ip(blind_sig) * pow(os2ip(sig), -1, pk.n) % pk.n
