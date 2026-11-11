# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signal-protocol/. The authors are listed in prov/EQ8HBA.jsonl.
"""A compact Signal session: an X3DH handshake (Marlinspike and Perrin,
revision 1, 2016) that starts a Double Ratchet (Perrin and Marlinspike,
revision 1, 2016), between two parties and a key server.

What is simplified:
* One device per user, so there is no Sesame session management.
* The signed prekey is signed with a separate Ed25519 key (RFC 8032). Signal
  signs with the X25519 identity key through XEdDSA instead.
* Keys are encoded as raw 32-byte strings, without the type byte of the
  Signal encoding.
* Messages are protected with a study AEAD (encrypt-then-MAC with an
  HMAC-SHA256 key stream), not AES-256-CBC with HMAC-SHA256.
* No header encryption, no sealed sender and no PQXDH.

X25519, Ed25519 and HKDF are local copies. For study only. The code is not
constant time and must not protect real data. Use libsignal.
"""

import copy
import hashlib
import hmac
import secrets
from typing import Dict, Optional, Tuple

# ---------------------------------------------------------------- X25519 (RFC 7748 Section 5)

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


class KeyPair:
    def __init__(self, private: Optional[bytes] = None) -> None:
        self.private = private if private is not None else secrets.token_bytes(32)
        self.public = x25519(self.private, BASE_U)


def dh(pair: KeyPair, public: bytes) -> bytes:
    return x25519(pair.private, public)


# ---------------------------------------------------------------- Ed25519 (RFC 8032 Section 5.1)

Q = 2**252 + 27742317777372353535851937790883648493
D = -121665 * pow(121666, P - 2, P) % P
SQRT_M1 = pow(2, (P - 1) // 4, P)


def _recover_x(y: int, sign: int) -> Optional[int]:
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
    return P - x if x & 1 != sign else x


_BY = 4 * pow(5, P - 2, P) % P
_BX = _recover_x(_BY, 0)
assert _BX is not None
BASE = (_BX, _BY, 1, _BX * _BY % P)
IDENT = (0, 1, 1, 0)


def ed_add(p1: tuple, p2: tuple) -> tuple:
    x1, y1, z1, t1 = p1
    x2, y2, z2, t2 = p2
    a = (y1 - x1) * (y2 - x2) % P
    b = (y1 + x1) * (y2 + x2) % P
    c = 2 * t1 * t2 * D % P
    d = 2 * z1 * z2 % P
    e, f, g, h = b - a, d - c, d + c, b + a
    return (e * f % P, g * h % P, f * g % P, e * h % P)


def ed_mul(k: int, pt: tuple) -> tuple:
    r = IDENT
    while k > 0:
        if k & 1:
            r = ed_add(r, pt)
        pt = ed_add(pt, pt)
        k >>= 1
    return r


def ed_encode(pt: tuple) -> bytes:
    x, y, z, _ = pt
    zi = pow(z, P - 2, P)
    x, y = x * zi % P, y * zi % P
    return (y | ((x & 1) << 255)).to_bytes(32, "little")


def ed_decode(s: bytes) -> Optional[tuple]:
    v = int.from_bytes(s, "little")
    y, sign = v & ((1 << 255) - 1), v >> 255
    x = _recover_x(y, sign)
    return None if x is None else (x, y, 1, x * y % P)


def _h512(*parts: bytes) -> int:
    return int.from_bytes(hashlib.sha512(b"".join(parts)).digest(), "little")


def ed25519_public(seed: bytes) -> bytes:
    return ed_encode(ed_mul(clamp(hashlib.sha512(seed).digest()[:32]), BASE))


def ed25519_sign(seed: bytes, msg: bytes) -> bytes:
    h = hashlib.sha512(seed).digest()
    a = clamp(h[:32])
    pub = ed_encode(ed_mul(a, BASE))
    r = _h512(h[32:], msg) % Q
    big_r = ed_encode(ed_mul(r, BASE))
    return big_r + ((r + _h512(big_r, pub, msg) * a) % Q).to_bytes(32, "little")


def ed25519_verify(public: bytes, msg: bytes, sig: bytes) -> bool:
    if len(sig) != 64 or len(public) != 32:
        return False
    pa, pr = ed_decode(public), ed_decode(sig[:32])
    s = int.from_bytes(sig[32:], "little")
    if pa is None or pr is None or s >= Q:
        return False
    k = _h512(sig[:32], public, msg) % Q
    lhs, rhs = ed_mul(s, BASE), ed_add(pr, ed_mul(k, pa))
    return (lhs[0] * rhs[2] - rhs[0] * lhs[2]) % P == 0 and (lhs[1] * rhs[2] - rhs[1] * lhs[2]) % P == 0


# ---------------------------------------------------------------- HKDF (RFC 5869), KDFs and the study AEAD


def hkdf(ikm: bytes, salt: bytes, info: bytes, length: int) -> bytes:
    prk = hmac.new(salt or bytes(32), ikm, hashlib.sha256).digest()
    out, t, i = b"", b"", 1
    while len(out) < length:
        t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
        out += t
        i += 1
    return out[:length]


def x3dh_kdf(km: bytes) -> bytes:
    """X3DH Section 2.2: HKDF over F || KM with F = 32 bytes of 0xFF and a zero salt."""
    return hkdf(b"\xff" * 32 + km, bytes(32), b"SignalStudy X3DH", 32)


def kdf_rk(rk: bytes, dh_out: bytes) -> Tuple[bytes, bytes]:
    out = hkdf(dh_out, rk, b"SignalStudy Ratchet", 64)
    return out[:32], out[32:]


def kdf_ck(ck: bytes) -> Tuple[bytes, bytes]:
    """(next chain key, message key)."""
    return hmac.new(ck, b"\x02", hashlib.sha256).digest(), hmac.new(ck, b"\x01", hashlib.sha256).digest()


class AuthError(ValueError):
    pass


def seal(mk: bytes, plaintext: bytes, ad: bytes) -> bytes:
    keys = hkdf(mk, bytes(32), b"SignalStudy Message", 64)
    ek, ak = keys[:32], keys[32:]
    stream = b"".join(hmac.new(ek, i.to_bytes(8, "big"), hashlib.sha256).digest() for i in range(len(plaintext) // 32 + 1))
    ct = bytes(a ^ b for a, b in zip(plaintext, stream))
    return ct + hmac.new(ak, ad + ct, hashlib.sha256).digest()


def open_sealed(mk: bytes, ciphertext: bytes, ad: bytes) -> bytes:
    keys = hkdf(mk, bytes(32), b"SignalStudy Message", 64)
    ek, ak = keys[:32], keys[32:]
    ct, tag = ciphertext[:-32], ciphertext[-32:]
    if len(ciphertext) < 32 or not hmac.compare_digest(tag, hmac.new(ak, ad + ct, hashlib.sha256).digest()):
        raise AuthError("bad tag")
    stream = b"".join(hmac.new(ek, i.to_bytes(8, "big"), hashlib.sha256).digest() for i in range(len(ct) // 32 + 1))
    return bytes(a ^ b for a, b in zip(ct, stream))


# ---------------------------------------------------------------- the Double Ratchet session

MAX_SKIP = 100
Header = Tuple[bytes, int, int]  # (ratchet public key, PN, N)


def encode_header(h: Header) -> bytes:
    return h[0] + h[1].to_bytes(4, "big") + h[2].to_bytes(4, "big")


class Session:
    def __init__(self, ad: bytes, rk: bytes, dhs: KeyPair, dhr: Optional[bytes]) -> None:
        self.ad, self.RK, self.DHs, self.DHr = ad, rk, dhs, dhr
        self.CKs: Optional[bytes] = None
        self.CKr: Optional[bytes] = None
        self.Ns = self.Nr = self.PN = 0
        self.skipped: Dict[Tuple[bytes, int], bytes] = {}
        if dhr is not None:  # the initiator makes its first sending chain at once
            self.RK, self.CKs = kdf_rk(rk, dh(dhs, dhr))

    def send(self, plaintext: bytes) -> Tuple[Header, bytes]:
        assert self.CKs is not None, "the responder sends after it has received"
        self.CKs, mk = kdf_ck(self.CKs)  # @line L7
        header = (self.DHs.public, self.PN, self.Ns)
        self.Ns += 1
        return header, seal(mk, plaintext, self.ad + encode_header(header))

    def receive(self, header: Header, ciphertext: bytes) -> bytes:
        ad = self.ad + encode_header(header)
        key = (header[0], header[2])
        if key in self.skipped:  # @line L8
            pt = open_sealed(self.skipped[key], ciphertext, ad)
            del self.skipped[key]
            return pt
        saved = self._snapshot()
        try:
            if header[0] != self.DHr:  # @line L9
                self._skip(header[1])
                self._dh_ratchet(header[0])
            self._skip(header[2])  # @line L11
            assert self.CKr is not None
            self.CKr, mk = kdf_ck(self.CKr)
            self.Nr += 1
            return open_sealed(mk, ciphertext, ad)
        except Exception:
            self.__dict__.update(saved)  # roll back: a forged message must not change the state
            raise

    def _skip(self, until: int) -> None:
        if self.Nr + MAX_SKIP < until:
            raise AuthError("too many skipped messages")
        while self.CKr is not None and self.Nr < until:
            self.CKr, mk = kdf_ck(self.CKr)
            assert self.DHr is not None
            self.skipped[(self.DHr, self.Nr)] = mk
            self.Nr += 1

    def _dh_ratchet(self, their_public: bytes) -> None:
        self.PN, self.Ns, self.Nr = self.Ns, 0, 0  # @line L10
        self.DHr = their_public
        self.RK, self.CKr = kdf_rk(self.RK, dh(self.DHs, self.DHr))
        self.DHs = KeyPair()
        self.RK, self.CKs = kdf_rk(self.RK, dh(self.DHs, self.DHr))

    def _snapshot(self) -> dict:
        d = dict(self.__dict__)
        d["skipped"] = dict(self.skipped)
        return d


# ---------------------------------------------------------------- users, the key server and X3DH


class User:
    def __init__(self, name: str, n_prekeys: int = 5) -> None:
        self.name = name
        self.ik = KeyPair()  # identity key for X3DH
        self.sign_seed = secrets.token_bytes(32)  # stands in for XEdDSA on the identity key
        self.sign_public = ed25519_public(self.sign_seed)
        self.spk = KeyPair()
        self.spk_sig = ed25519_sign(self.sign_seed, self.spk.public)
        self.opks: Dict[int, KeyPair] = {i: KeyPair() for i in range(n_prekeys)}


class KeyServer:
    """Holds prekey bundles. It is trusted to deliver, not to keep secrets."""

    def __init__(self) -> None:
        self.bundles: Dict[str, dict] = {}

    def publish(self, u: User) -> None:  # @line L1
        self.bundles[u.name] = dict(ik=u.ik.public, sign=u.sign_public, spk=u.spk.public, sig=u.spk_sig, opks={i: k.public for i, k in u.opks.items()})

    def fetch(self, name: str) -> dict:
        b = self.bundles[name]
        out = dict(ik=b["ik"], sign=b["sign"], spk=b["spk"], sig=b["sig"], opk_id=None, opk=None)
        if b["opks"]:
            i = min(b["opks"])
            out["opk_id"], out["opk"] = i, b["opks"].pop(i)  # each one-time prekey is handed out once
        return out


def start_session(alice: User, bundle: dict, first: bytes, trusted_sign_key: Optional[bytes] = None) -> Tuple[Session, dict]:
    """Alice's side of X3DH, then her first Double Ratchet message.

    trusted_sign_key is Bob's signing key as Alice verified it out of band
    (the safety number); without it Alice trusts the server's copy."""
    sign_key = trusted_sign_key or bundle["sign"]
    if not ed25519_verify(sign_key, bundle["spk"], bundle["sig"]):  # @line L2
        raise AuthError("bad signature on the signed prekey")
    ek = KeyPair()
    km = dh(alice.ik, bundle["spk"]) + dh(ek, bundle["ik"]) + dh(ek, bundle["spk"])
    if bundle["opk"] is not None:
        km += dh(ek, bundle["opk"])
    sk = x3dh_kdf(km)  # @line L3
    ad = alice.ik.public + bundle["ik"]
    s = Session(ad, sk, KeyPair(), bundle["spk"])  # @line L4
    header, ct = s.send(first)
    init = dict(ik=alice.ik.public, ek=ek.public, opk_id=bundle["opk_id"], header=header, ct=ct)
    return s, init


def accept_session(bob: User, init: dict) -> Tuple[Session, bytes]:
    """Bob's side: recompute SK, start his ratchet with the signed prekey, decrypt."""
    opk = None
    if init["opk_id"] is not None:
        opk = bob.opks.pop(init["opk_id"], None)  # @line L5
        if opk is None:
            raise AuthError("unknown or used one-time prekey")
    km = dh(bob.spk, init["ik"]) + dh(bob.ik, init["ek"]) + dh(bob.spk, init["ek"])
    if opk is not None:
        km += dh(opk, init["ek"])
    sk = x3dh_kdf(km)
    s = Session(init["ik"] + bob.ik.public, sk, bob.spk, None)  # @line L6
    return s, s.receive(init["header"], init["ct"])


def forge_initial_message(bob: User, alice_ik_public: bytes, text: bytes) -> dict:
    """Deniability: Bob alone makes a first message 'from Alice' that his own
    accept_session accepts. He needs Alice's public identity key only."""
    ek = KeyPair()
    km = dh(bob.spk, alice_ik_public) + dh(bob.ik, ek.public) + dh(bob.spk, ek.public)
    i = min(bob.opks)
    km += dh(bob.opks[i], ek.public)
    sk = x3dh_kdf(km)
    s = Session(alice_ik_public + bob.ik.public, sk, KeyPair(), bob.spk.public)
    header, ct = s.send(text)
    return dict(ik=alice_ik_public, ek=ek.public, opk_id=i, header=header, ct=ct)


def steal(s: Session) -> Session:
    """An attacker's copy of a session state (a device compromise)."""
    return copy.deepcopy(s)
