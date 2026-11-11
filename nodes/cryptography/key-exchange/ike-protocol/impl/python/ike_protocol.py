# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ike-protocol/. The authors are listed in prov/FRQGKN.jsonl.
"""A simplified model of the IKEv2 initial exchanges (RFC 7296) with signature authentication.

    IKE_SA_INIT  I -> R : SPIi, SAi1, KEi, Ni           (R may first answer with a COOKIE)
                 R -> I : SPIi, SPIr, SAr1, KEr, Nr
    keys         SKEYSEED = prf(Ni | Nr, g^ir)                                   (Section 2.14)
                 SK_d | SK_ai | SK_ar | SK_ei | SK_er | SK_pi | SK_pr
                     = prf+(SKEYSEED, Ni | Nr | SPIi | SPIr)                     (Section 2.13)
    IKE_AUTH     I -> R : SK{ IDi, AUTH = SIG_I(msg1 | Nr | prf(SK_pi, IDi)) }
                 R -> I : SK{ IDr, AUTH = SIG_R(msg2 | Ni | prf(SK_pr, IDr)) }
    child SA     KEYMAT = prf+(SK_d, Ni | Nr)

prf is HMAC-SHA-256, and prf, prf+ and SKEYSEED follow RFC 7296 exactly; the
test checks them against the NIST CAVP SP 800-135 IKEv2 vector. The rest is a
model, not the wire protocol: messages are length-prefixed byte strings, there
is one fixed proposal, no traffic selectors and no NAT detection, the signature
is a toy Schnorr signature, SK{...} is a toy encrypt-then-MAC (SHA-256 counter
mode with an HMAC tag), and the group is a 256-bit safe-prime group.

For study only. This code is not constant time, it branches on secret data,
and the parameters are toys. Use strongSwan or libreswan for real IPsec.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets

P = 0xC00000000000000000000000000000000000000000000000000000000000A0EB
Q = (P - 1) // 2
G = 4
KEYLEN = 32  # each SK_* key, as for PRF_HMAC_SHA2_256 and 256-bit cipher keys
SA = b"ENCR_TOY|PRF_HMAC_SHA2_256|AUTH_TOY|GROUP_TOY256"


def prf(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha256).digest()


def prf_plus(key: bytes, seed: bytes, length: int) -> bytes:
    """RFC 7296 Section 2.13: T1 = prf(K, S | 0x01), Tn = prf(K, Tn-1 | S | n)."""
    out, t, n = b"", b"", 1
    while len(out) < length:
        t = prf(key, t + seed + bytes([n]))
        out += t
        n += 1
    return out[:length]


def skeyseed(ni: bytes, nr: bytes, g_ir: bytes) -> bytes:
    """RFC 7296 Section 2.14: SKEYSEED = prf(Ni | Nr, g^ir)."""
    return prf(ni + nr, g_ir)


def lp(*parts: bytes) -> bytes:
    return b"".join(len(t).to_bytes(2, "big") + t for t in parts)


def unlp(data: bytes) -> list[bytes]:
    out, i = [], 0
    while i < len(data):
        n = int.from_bytes(data[i : i + 2], "big")
        out.append(data[i + 2 : i + 2 + n])
        i += 2 + n
    return out


def b32(v: int) -> bytes:
    return v.to_bytes(32, "big")


def in_group(v: int) -> bool:
    return 1 < v < P and pow(v, Q, P) == 1


# Toy Schnorr signature in the same group.
def sig_keypair(rng=None) -> tuple[int, int]:
    k = (rng or secrets.SystemRandom()).randrange(1, Q)
    return k, pow(G, k, P)


def _chal(r: int, pub: int, m: bytes) -> int:
    return int.from_bytes(hashlib.sha256(lp(b32(r), b32(pub), m)).digest(), "big") % Q


def sign(sk: int, m: bytes, rng=None) -> bytes:
    k = (rng or secrets.SystemRandom()).randrange(1, Q)
    r = pow(G, k, P)
    c = _chal(r, pow(G, sk, P), m)
    return b32(c) + b32((k + c * sk) % Q)


def verify(pk: int, m: bytes, s: bytes) -> bool:
    c, z = int.from_bytes(s[:32], "big"), int.from_bytes(s[32:], "big")
    r = pow(G, z, P) * pow(pk, Q - c, P) % P
    return _chal(r, pk, m) == c


# Toy SK{...}: encrypt-then-MAC with SK_e and SK_a.
def sk_seal(ke: bytes, ka: bytes, plain: bytes, rng=None) -> bytes:
    iv = (rng or secrets.SystemRandom()).randbytes(16)
    stream = b"".join(hashlib.sha256(ke + iv + i.to_bytes(4, "big")).digest() for i in range(len(plain) // 32 + 1))
    ct = bytes(a ^ b for a, b in zip(plain, stream))
    return iv + ct + prf(ka, iv + ct)[:16]


def sk_open(ke: bytes, ka: bytes, box: bytes) -> bytes | None:
    iv, ct, tag = box[:16], box[16:-16], box[-16:]
    if not hmac.compare_digest(prf(ka, iv + ct)[:16], tag):
        return None
    stream = b"".join(hashlib.sha256(ke + iv + i.to_bytes(4, "big")).digest() for i in range(len(ct) // 32 + 1))
    return bytes(a ^ b for a, b in zip(ct, stream))


def derive(ni: bytes, nr: bytes, spi_i: bytes, spi_r: bytes, g_ir: int) -> dict[str, bytes]:
    seed = skeyseed(ni, nr, b32(g_ir))  # @line L4
    dkm = prf_plus(seed, ni + nr + spi_i + spi_r, 7 * KEYLEN)  # @line L5
    names = ["d", "ai", "ar", "ei", "er", "pi", "pr"]
    return {n: dkm[i * KEYLEN : (i + 1) * KEYLEN] for i, n in enumerate(names)}


class Initiator:
    def __init__(self, ident: bytes, sk: int, directory: dict[bytes, int], rng=None):
        self.id, self.sk, self.dir, self.rng = ident, sk, directory, rng or secrets.SystemRandom()
        self.keymat = self.peer = None

    def message1(self, cookie: bytes = b"") -> bytes:
        self.spi_i = self.rng.randbytes(8)
        self.x = self.rng.randrange(1, Q)
        self.ni = self.rng.randbytes(32)
        self.msg1 = lp(b"INIT", self.spi_i, SA, b32(pow(G, self.x, P)), self.ni, cookie)  # @line L1
        return self.msg1

    def auth(self, msg2: bytes) -> bytes | None:
        _, spi_i, self.spi_r, sa, ker, self.nr = unlp(msg2)
        if spi_i != self.spi_i or sa != SA or not in_group(int.from_bytes(ker, "big")):
            return None
        self.msg2 = msg2
        self.k = derive(self.ni, self.nr, self.spi_i, self.spi_r, pow(int.from_bytes(ker, "big"), self.x, P))
        signed = self.msg1 + self.nr + prf(self.k["pi"], self.id)
        return lp(b"AUTH", sk_seal(self.k["ei"], self.k["ai"], lp(self.id, sign(self.sk, signed, self.rng)), self.rng))  # @line L6

    def finish(self, msg4: bytes) -> bool:
        plain = sk_open(self.k["er"], self.k["ar"], unlp(msg4)[1])
        if plain is None:
            return False
        id_r, auth_r = unlp(plain)
        signed = self.msg2 + self.ni + prf(self.k["pr"], id_r)
        if id_r not in self.dir or not verify(self.dir[id_r], signed, auth_r):  # @line L8
            return False
        self.peer = id_r
        self.keymat = prf_plus(self.k["d"], self.ni + self.nr, 64)  # @line L9
        return True


class Responder:
    def __init__(self, ident: bytes, sk: int, directory: dict[bytes, int], rng=None):
        self.id, self.sk, self.dir, self.rng = ident, sk, directory, rng or secrets.SystemRandom()
        self.secret = self.rng.randbytes(32)  # cookie secret
        self.under_load = False
        self.sessions: dict[bytes, dict] = {}
        self.keymat = self.peer = None

    def cookie_for(self, ni: bytes, ip: bytes, spi_i: bytes) -> bytes:
        return prf(self.secret, ni + ip + spi_i)

    def respond(self, msg1: bytes, ip: bytes = b"192.0.2.1") -> bytes | None:
        try:
            tag, spi_i, sa, kei, ni, cookie = unlp(msg1)
        except ValueError:
            return None
        if tag != b"INIT" or sa != SA:
            return None
        if self.under_load and not hmac.compare_digest(cookie, self.cookie_for(ni, ip, spi_i)):  # @line L2
            return lp(b"COOKIE", self.cookie_for(ni, ip, spi_i))  # no state is kept, no exponentiation
        if not in_group(int.from_bytes(kei, "big")):
            return None
        y, nr, spi_r = self.rng.randrange(1, Q), self.rng.randbytes(32), self.rng.randbytes(8)
        msg2 = lp(b"RESP", spi_i, spi_r, SA, b32(pow(G, y, P)), nr)  # @line L3
        k = derive(ni, nr, spi_i, spi_r, pow(int.from_bytes(kei, "big"), y, P))
        self.sessions[spi_i] = {"msg1": msg1, "msg2": msg2, "ni": ni, "nr": nr, "k": k}
        return msg2

    def auth(self, spi_i: bytes, msg3: bytes) -> bytes | None:
        s = self.sessions.get(spi_i)
        if s is None:
            return None
        k = s["k"]
        plain = sk_open(k["ei"], k["ai"], unlp(msg3)[1])
        if plain is None:
            return None
        id_i, auth_i = unlp(plain)
        signed = s["msg1"] + s["nr"] + prf(k["pi"], id_i)
        if id_i not in self.dir or not verify(self.dir[id_i], signed, auth_i):  # @line L7
            return None
        self.peer = id_i
        self.keymat = prf_plus(k["d"], s["ni"] + s["nr"], 64)
        signed_r = s["msg2"] + s["ni"] + prf(k["pr"], self.id)
        return lp(b"AUTH", sk_seal(k["er"], k["ar"], lp(self.id, sign(self.sk, signed_r, self.rng)), self.rng))
