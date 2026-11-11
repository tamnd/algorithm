# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/secure-messaging/. The authors are listed in prov/8PE1DX.jsonl.
"""A harness that scores toy two-party messaging protocols for forward
secrecy (FS) and post-compromise security (PCS) under a simulated
compromise.

The four toy protocols:
* StaticKey: one long-term shared key encrypts every message.
* SessionDH: a fresh Diffie-Hellman exchange starts each session, as in
  OTR-like designs at the granularity of a session; the session key is
  erased when the next session starts.
* HashRatchet: a symmetric chain per direction; each message key is a hash
  of the chain key, which then moves forward (as in SCIMP or sender keys).
* DHRatchet: the hash chains plus a Diffie-Hellman ratchet step at each
  change of direction (a minimal Double Ratchet).

The attack: at one point the attacker copies the full state of one party.
It then reads every record that crosses the network, but sends nothing.
* Past messages: the attacker tries to decrypt each earlier record with the
  copied state. A message that it can read breaks forward secrecy.
* Later messages: the attacker runs the copied state forward on the
  records. It does not know the fresh random values that the real party
  draws after the copy, so where the protocol uses one, the copy draws its
  own and its keys stop matching. A later message that it can still read
  shows how long the compromise lasts.

The encryption is a study AEAD (encrypt-then-MAC with an HMAC-SHA256 key
stream) and X25519 is a local copy of RFC 7748. For study only: the code
is not constant time and none of these toy protocols should be used. Use
libsignal or an MLS library for real messaging.
"""

import copy
import hashlib
import hmac
import secrets
from typing import Dict, List, NamedTuple, Optional, Tuple

# ---------------------------------------------------------------- X25519 (RFC 7748 Section 5)

P = 2**255 - 19


def x25519(k: bytes, u: bytes) -> bytes:
    b = bytearray(k)
    b[0] &= 248
    b[31] &= 127
    b[31] |= 64
    kk = int.from_bytes(b, "little")
    x1 = int.from_bytes(u, "little") % (2**255) % P
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
        z2 = e * (aa + 121665 * e) % P
    if swap:
        x2, z2 = x3, z3
    return (x2 * pow(z2, P - 2, P) % P).to_bytes(32, "little")


BASE_U = (9).to_bytes(32, "little")


class KeyPair:
    def __init__(self) -> None:
        self.private = secrets.token_bytes(32)
        self.public = x25519(self.private, BASE_U)


# ---------------------------------------------------------------- KDF and the study AEAD


def kdf(key: bytes, label: bytes) -> bytes:
    return hmac.new(key, label, hashlib.sha256).digest()


class AuthError(ValueError):
    pass


def seal(key: bytes, nonce: bytes, pt: bytes, ad: bytes) -> bytes:
    ke, km = kdf(key, b"enc"), kdf(key, b"mac")
    stream = b"".join(kdf(ke, nonce + i.to_bytes(4, "big")) for i in range(len(pt) // 32 + 1))
    ct = bytes(a ^ b for a, b in zip(pt, stream))
    return ct + kdf(km, ad + nonce + ct)[:16]


def open_sealed(key: Optional[bytes], nonce: bytes, ct: bytes, ad: bytes) -> bytes:
    if key is None:
        raise AuthError("no key")
    ke, km = kdf(key, b"enc"), kdf(key, b"mac")
    body, tag = ct[:-16], ct[-16:]
    if not hmac.compare_digest(tag, kdf(km, ad + nonce + body)[:16]):
        raise AuthError("bad tag")
    stream = b"".join(kdf(ke, nonce + i.to_bytes(4, "big")) for i in range(len(body) // 32 + 1))
    return bytes(a ^ b for a, b in zip(body, stream))


class Record(NamedTuple):
    sender: str  # "A" or "B"
    kind: str  # "data" or "dh"
    label: int  # the message number in the run (-1 for handshake records)
    pub: bytes  # a public value: a nonce, a DH share or a ratchet key
    n: int  # a counter, where the protocol has one
    ct: bytes


# ---------------------------------------------------------------- the four toy protocols


class StaticKey:
    name = "static key"

    def __init__(self, me: str, key: bytes) -> None:
        self.me, self.key = me, key

    @staticmethod
    def pair() -> Tuple["StaticKey", "StaticKey"]:
        k = secrets.token_bytes(32)
        return StaticKey("A", k), StaticKey("B", k)

    @staticmethod
    def new_session(a, b) -> List[Record]:
        return []

    def send(self, label: int, pt: bytes) -> Record:
        nonce = secrets.token_bytes(12)
        return Record(self.me, "data", label, nonce, 0, seal(self.key, nonce, pt, self.me.encode()))

    def recv(self, r: Record) -> bytes:
        return open_sealed(self.key, r.pub, r.ct, r.sender.encode())

    peek = recv  # the sender can read its own records too


class SessionDH:
    """A fresh X25519 exchange per session; data uses the session key."""

    name = "DH per session (OTR-like)"

    def __init__(self, me: str) -> None:
        self.me = me
        self.k: Optional[bytes] = None
        self.x: Optional[KeyPair] = None

    @staticmethod
    def pair() -> Tuple["SessionDH", "SessionDH"]:
        a, b = SessionDH("A"), SessionDH("B")
        SessionDH.new_session(a, b)
        return a, b

    @staticmethod
    def new_session(a: "SessionDH", b: "SessionDH") -> List[Record]:
        r1 = a.start()
        r2 = b.answer(r1)
        a.recv(r2)
        return [r1, r2]

    def start(self) -> Record:
        self.x = KeyPair()
        return Record(self.me, "dh", -1, self.x.public, 0, b"")

    def answer(self, r: Record) -> Record:
        y = KeyPair()
        self.k = kdf(x25519(y.private, r.pub), b"session")  # y is erased on return
        return Record(self.me, "dh", -1, y.public, 0, b"")

    def send(self, label: int, pt: bytes) -> Record:
        assert self.k is not None
        nonce = secrets.token_bytes(12)
        return Record(self.me, "data", label, nonce, 0, seal(self.k, nonce, pt, self.me.encode()))

    def recv(self, r: Record) -> bytes:
        if r.kind == "dh":
            if self.x is not None:  # the initiator finishes the exchange
                self.k = kdf(x25519(self.x.private, r.pub), b"session")
                self.x = None
            else:  # the responder: a copy of the state draws its own y
                self.answer(r)
            return b""
        return open_sealed(self.k, r.pub, r.ct, r.sender.encode())

    def peek(self, r: Record) -> bytes:
        if r.kind == "dh":  # a share that this party sent; its private part is fresh
            self.x = KeyPair()
            return b""
        return open_sealed(self.k, r.pub, r.ct, r.sender.encode())


class HashRatchet:
    """One symmetric chain per direction: mk = KDF(ck, 1), ck <- KDF(ck, 2)."""

    name = "hash ratchet only"

    def __init__(self, me: str, ck_s: bytes, ck_r: bytes) -> None:
        self.me, self.ck_s, self.ck_r, self.ns, self.nr = me, ck_s, ck_r, 0, 0

    @staticmethod
    def pair() -> Tuple["HashRatchet", "HashRatchet"]:
        ab, ba = secrets.token_bytes(32), secrets.token_bytes(32)
        return HashRatchet("A", ab, ba), HashRatchet("B", ba, ab)

    @staticmethod
    def new_session(a, b) -> List[Record]:
        return []

    def send(self, label: int, pt: bytes) -> Record:
        mk, self.ck_s = kdf(self.ck_s, b"\x01"), kdf(self.ck_s, b"\x02")
        r = Record(self.me, "data", label, b"", self.ns, seal(mk, bytes(12), pt, self.me.encode()))
        self.ns += 1
        return r

    def recv(self, r: Record) -> bytes:
        if r.n < self.nr:
            raise AuthError("the key of this message was deleted")
        ck = self.ck_r
        for _ in range(r.n - self.nr):
            ck = kdf(ck, b"\x02")
        pt = open_sealed(kdf(ck, b"\x01"), bytes(12), r.ct, r.sender.encode())
        self.ck_r, self.nr = kdf(ck, b"\x02"), r.n + 1
        return pt

    def peek(self, r: Record) -> bytes:
        if r.n < self.ns:
            raise AuthError("the key of this message was deleted")
        ck = self.ck_s
        for _ in range(r.n - self.ns):
            ck = kdf(ck, b"\x02")
        pt = open_sealed(kdf(ck, b"\x01"), bytes(12), r.ct, r.sender.encode())
        self.ck_s, self.ns = kdf(ck, b"\x02"), r.n + 1
        return pt


class DHRatchet:
    """Hash chains plus a DH ratchet step whenever a new ratchet key arrives."""

    name = "DH ratchet (Double Ratchet)"

    def __init__(self, me: str, rk: bytes, dhs: KeyPair, dhr: Optional[bytes]) -> None:
        self.me, self.rk, self.dhs, self.dhr = me, rk, dhs, dhr
        self.ck_s: Optional[bytes] = None
        self.ck_r: Optional[bytes] = None
        if dhr is not None:
            self.rk, self.ck_s = self._kdf_rk(x25519(dhs.private, dhr))

    def _kdf_rk(self, dh_out: bytes) -> Tuple[bytes, bytes]:
        return kdf(self.rk, b"root" + dh_out), kdf(self.rk, b"chain" + dh_out)

    @staticmethod
    def pair() -> Tuple["DHRatchet", "DHRatchet"]:
        sk, bob = secrets.token_bytes(32), KeyPair()
        return DHRatchet("A", sk, KeyPair(), bob.public), DHRatchet("B", sk, bob, None)

    @staticmethod
    def new_session(a, b) -> List[Record]:
        return []

    def send(self, label: int, pt: bytes) -> Record:
        assert self.ck_s is not None
        mk, self.ck_s = kdf(self.ck_s, b"\x01"), kdf(self.ck_s, b"\x02")
        return Record(self.me, "data", label, self.dhs.public, 0, seal(mk, bytes(12), pt, self.me.encode() + self.dhs.public))

    def recv(self, r: Record) -> bytes:
        saved = copy.deepcopy(self.__dict__)
        try:
            if r.pub != self.dhr:  # a DH ratchet step
                self.dhr = r.pub
                self.rk, self.ck_r = self._kdf_rk(x25519(self.dhs.private, self.dhr))
                self.dhs = KeyPair()
                self.rk, self.ck_s = self._kdf_rk(x25519(self.dhs.private, self.dhr))
            if self.ck_r is None:
                raise AuthError("no receiving chain")
            mk, self.ck_r = kdf(self.ck_r, b"\x01"), kdf(self.ck_r, b"\x02")
            return open_sealed(mk, bytes(12), r.ct, r.sender.encode() + r.pub)
        except AuthError:
            self.__dict__.update(saved)
            raise

    def peek(self, r: Record) -> bytes:
        if r.pub != self.dhs.public or self.ck_s is None:
            raise AuthError("sent under a ratchet key that this state does not hold")
        mk, self.ck_s = kdf(self.ck_s, b"\x01"), kdf(self.ck_s, b"\x02")
        return open_sealed(mk, bytes(12), r.ct, r.sender.encode() + r.pub)


PROTOCOLS = (StaticKey, SessionDH, HashRatchet, DHRatchet)

# ---------------------------------------------------------------- the harness


class Score(NamedTuple):
    past: List[int]  # earlier messages that the attacker reads with the copied state
    future: List[int]  # later messages that the attacker reads by running the copy forward
    fs: bool  # no earlier message is exposed
    pcs: bool  # the exposure of later messages stops before the run ends


def run(proto, n: int = 16, compromise_at: int = 6, session_len: int = 4, victim: str = "A") -> Score:
    """Alternate messages A, B, A, ...; start a new session every session_len
    messages; copy the victim's state just before message compromise_at."""
    a, b = proto.pair()
    log: List[Record] = []
    stolen = None
    cut = 0
    for i in range(n):
        if i and i % session_len == 0:
            log += proto.new_session(a, b)
        if i == compromise_at:
            stolen, cut = copy.deepcopy(a if victim == "A" else b), len(log)
        sender, receiver = (a, b) if i % 2 == 0 else (b, a)
        r = sender.send(i, b"message %d" % i)
        assert receiver.recv(r) == b"message %d" % i  # honest delivery always works
        log.append(r)
    assert stolen is not None

    past = []
    for r in log[:cut]:
        if r.kind != "data":
            continue
        trial = copy.deepcopy(stolen)
        try:
            (trial.peek if r.sender == victim else trial.recv)(r)
            past.append(r.label)
        except AuthError:
            pass

    future = []
    shadow = copy.deepcopy(stolen)
    for r in log[cut:]:
        try:
            pt = (shadow.peek if r.sender == victim else shadow.recv)(r)
            if r.kind == "data" and pt == b"message %d" % r.label:
                future.append(r.label)
        except AuthError:
            pass
    return Score(past, future, not past, not future or future[-1] < n - 1)


def score_all(**kw) -> Dict[str, Score]:
    return {p.name: run(p, **kw) for p in PROTOCOLS}
