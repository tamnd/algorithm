# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-ratchet/. The authors are listed in prov/EJKDEP.jsonl.
"""The Double Ratchet of Perrin and Marlinspike (Signal specification,
revision 1, 2016-11-20), Section 3 (without header encryption).

The building blocks follow Section 5.2 of the specification (recommended
cryptographic algorithms), with one change in ENCRYPT:

* GENERATE_DH and DH: X25519 (RFC 7748), a small local copy.
* KDF_RK: HKDF with SHA-256, salt = rk, ikm = dh_out, a fixed info string.
* KDF_CK: HMAC-SHA256 with the constant 0x01 for the message key and 0x02
  for the next chain key.
* ENCRYPT: the spec recommends AES-256-CBC with HMAC-SHA256. This file uses
  an encrypt-then-MAC scheme whose key stream is HMAC-SHA256 in counter mode,
  keyed by the same HKDF output. It is a study AEAD, not a standard one.

For study only. The code is not constant time, and it must not protect real
data. Use libsignal or another maintained implementation.

Lines marked L1 to L27 match the pseudocode on the page.
"""

import hashlib
import hmac
import secrets

# ---------------------------------------------------------------- X25519 (RFC 7748, Section 5), local copy

_P = 2**255 - 19
_A24 = 121665


def _clamp(k: bytes) -> int:
    b = bytearray(k)
    b[0] &= 248
    b[31] &= 127
    b[31] |= 64
    return int.from_bytes(b, "little")


def x25519(k: bytes, u: bytes) -> bytes:
    kk = _clamp(k)
    b = bytearray(u)
    b[31] &= 127
    x1 = int.from_bytes(b, "little") % _P
    x2, z2, x3, z3, swap = 1, 0, x1, 1, 0
    for t in range(254, -1, -1):
        kt = (kk >> t) & 1
        swap ^= kt
        if swap:
            x2, x3, z2, z3 = x3, x2, z3, z2
        swap = kt
        a, b_ = (x2 + z2) % _P, (x2 - z2) % _P
        aa, bb = a * a % _P, b_ * b_ % _P
        e = (aa - bb) % _P
        c, d = (x3 + z3) % _P, (x3 - z3) % _P
        da, cb = d * a % _P, c * b_ % _P
        x3 = (da + cb) ** 2 % _P
        z3 = x1 * (da - cb) ** 2 % _P
        x2 = aa * bb % _P
        z2 = e * (aa + _A24 * e) % _P
    if swap:
        x2, z2 = x3, z3
    return (x2 * pow(z2, _P - 2, _P) % _P).to_bytes(32, "little")


BASE_U = (9).to_bytes(32, "little")


class KeyPair:
    def __init__(self, private: bytes):
        self.private = private
        self.public = x25519(private, BASE_U)


def generate_dh(rng=secrets.token_bytes) -> KeyPair:
    return KeyPair(rng(32))


def dh(pair: KeyPair, public: bytes) -> bytes:
    return x25519(pair.private, public)


# ---------------------------------------------------------------- HKDF (RFC 5869), local copy


def hkdf(ikm: bytes, salt: bytes, info: bytes, length: int) -> bytes:
    prk = hmac.new(salt or bytes(32), ikm, hashlib.sha256).digest()
    out, t, i = b"", b"", 1
    while len(out) < length:
        t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
        out += t
        i += 1
    return out[:length]


# ---------------------------------------------------------------- KDFs and the study AEAD

KDF_RK_INFO = b"DoubleRatchetStudy RootKey"
ENC_INFO = b"DoubleRatchetStudy MessageKeys"


def kdf_rk(rk: bytes, dh_out: bytes):
    """(root key, chain key) = HKDF(salt = rk, ikm = dh_out), 64 bytes."""
    out = hkdf(dh_out, rk, KDF_RK_INFO, 64)
    return out[:32], out[32:]


def kdf_ck(ck: bytes):
    """(chain key, message key): HMAC(ck, 0x02) and HMAC(ck, 0x01)."""
    return (hmac.new(ck, b"\x02", hashlib.sha256).digest(),
            hmac.new(ck, b"\x01", hashlib.sha256).digest())


class AuthError(ValueError):
    pass


def _keystream(key: bytes, iv: bytes, n: int) -> bytes:
    out, ctr = b"", 0
    while len(out) < n:
        out += hmac.new(key, iv + ctr.to_bytes(8, "big"), hashlib.sha256).digest()
        ctr += 1
    return out[:n]


def encrypt(mk: bytes, plaintext: bytes, ad: bytes) -> bytes:
    """Encrypt-then-MAC: 80 bytes of HKDF give an encryption key, a MAC key and an IV."""
    keys = hkdf(mk, bytes(32), ENC_INFO, 80)
    ek, ak, iv = keys[:32], keys[32:64], keys[64:]
    ct = bytes(p ^ s for p, s in zip(plaintext, _keystream(ek, iv, len(plaintext))))
    return ct + hmac.new(ak, ad + ct, hashlib.sha256).digest()


def decrypt(mk: bytes, ciphertext: bytes, ad: bytes) -> bytes:
    keys = hkdf(mk, bytes(32), ENC_INFO, 80)
    ek, ak, iv = keys[:32], keys[32:64], keys[64:]
    ct, tag = ciphertext[:-32], ciphertext[-32:]
    if len(ciphertext) < 32 or not hmac.compare_digest(tag, hmac.new(ak, ad + ct, hashlib.sha256).digest()):
        raise AuthError("bad tag")
    return bytes(c ^ s for c, s in zip(ct, _keystream(ek, iv, len(ct))))


# ---------------------------------------------------------------- headers

class Header:
    def __init__(self, dh_pub: bytes, pn: int, n: int):
        self.dh, self.pn, self.n = dh_pub, pn, n

    def encode(self) -> bytes:
        return self.dh + self.pn.to_bytes(4, "big") + self.n.to_bytes(4, "big")


def concat(ad: bytes, header: Header) -> bytes:
    """CONCAT(AD, header): AD has a fixed length here, so the split is unique."""
    return len(ad).to_bytes(4, "big") + ad + header.encode()


# ---------------------------------------------------------------- the state and the algorithm (Section 3)

MAX_SKIP = 100


class State:
    def __init__(self):
        self.DHs = None       # our ratchet key pair
        self.DHr = None       # their ratchet public key
        self.RK = None        # root key
        self.CKs = None       # sending chain key
        self.CKr = None       # receiving chain key
        self.Ns = 0           # number of the next message to send
        self.Nr = 0           # number of the next message to receive
        self.PN = 0           # number of messages in the previous sending chain
        self.MKSKIPPED = {}   # (ratchet public key, n) -> message key
        self.max_skip = MAX_SKIP


def ratchet_init_alice(SK: bytes, bob_dh_public_key: bytes, rng=secrets.token_bytes) -> State:
    s = State()
    s.DHs = generate_dh(rng)                                          # @line L1
    s.DHr = bob_dh_public_key
    s.RK, s.CKs = kdf_rk(SK, dh(s.DHs, s.DHr))                        # @line L2
    return s


def ratchet_init_bob(SK: bytes, bob_dh_key_pair: KeyPair) -> State:
    s = State()
    s.DHs = bob_dh_key_pair                                           # @line L3
    s.RK = SK
    return s


def ratchet_encrypt(s: State, plaintext: bytes, AD: bytes):
    s.CKs, mk = kdf_ck(s.CKs)                                         # @line L4
    header = Header(s.DHs.public, s.PN, s.Ns)                         # @line L5
    s.Ns += 1                                                         # @line L6
    return header, encrypt(mk, plaintext, concat(AD, header))         # @line L7


def ratchet_decrypt(s: State, header: Header, ciphertext: bytes, AD: bytes, rng=secrets.token_bytes) -> bytes:
    plaintext = try_skipped_message_keys(s, header, ciphertext, AD)   # @line L8
    if plaintext is not None:
        return plaintext
    snapshot = _copy(s)                                               # roll back on failure
    try:
        if header.dh != s.DHr:                                        # @line L9
            skip_message_keys(s, header.pn)                           # @line L10
            dh_ratchet(s, header, rng)                                # @line L11
        skip_message_keys(s, header.n)                                # @line L12
        s.CKr, mk = kdf_ck(s.CKr)                                     # @line L13
        s.Nr += 1                                                     # @line L14
        return decrypt(mk, ciphertext, concat(AD, header))            # @line L15
    except Exception:
        _restore(s, snapshot)                                         # @line L16
        raise


def try_skipped_message_keys(s: State, header: Header, ciphertext: bytes, AD: bytes):
    key = (header.dh, header.n)
    if key in s.MKSKIPPED:                                            # @line L17
        mk = s.MKSKIPPED[key]
        pt = decrypt(mk, ciphertext, concat(AD, header))
        del s.MKSKIPPED[key]                                          # @line L18
        return pt
    return None


class TooManySkipped(ValueError):
    pass


def skip_message_keys(s: State, until: int):
    if s.Nr + s.max_skip < until:                                     # @line L19
        raise TooManySkipped("too many skipped messages")
    if s.CKr is not None:
        while s.Nr < until:                                           # @line L20
            s.CKr, mk = kdf_ck(s.CKr)                                 # @line L21
            s.MKSKIPPED[(s.DHr, s.Nr)] = mk                           # @line L22
            s.Nr += 1


def dh_ratchet(s: State, header: Header, rng=secrets.token_bytes):
    s.PN = s.Ns                                                       # @line L23
    s.Ns = 0
    s.Nr = 0
    s.DHr = header.dh                                                 # @line L24
    s.RK, s.CKr = kdf_rk(s.RK, dh(s.DHs, s.DHr))                      # @line L25
    s.DHs = generate_dh(rng)                                          # @line L26
    s.RK, s.CKs = kdf_rk(s.RK, dh(s.DHs, s.DHr))                      # @line L27


def _copy(s: State) -> dict:
    d = dict(s.__dict__)
    d["MKSKIPPED"] = dict(s.MKSKIPPED)
    return d


def _restore(s: State, d: dict):
    s.__dict__.update(d)
