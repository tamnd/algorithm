# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tls-handshake/. The authors are listed in prov/VZ8M1C.jsonl.
"""The TLS 1.3 handshake of RFC 8446 (August 2018): the key schedule of
Section 7.1, the traffic keys of Section 7.3, Finished (Section 4.4.4),
CertificateVerify (Section 4.4.3), PSK binders (Section 4.2.11.2),
resumption (Section 4.6.1) and 0-RTT with single-use tickets (Section 8.1).

The key schedule is exact for the cipher suite TLS_AES_128_GCM_SHA256 and
X25519, and the tests check it against the trace of RFC 8448 Section 3.

What is simplified in the simulated handshake:
* The message bodies use a short private encoding, not the TLS wire format;
  only the 4-byte handshake header (type and length) is real.
* Records are protected with a study AEAD (encrypt-then-MAC with an
  HMAC-SHA256 key stream), keyed by the real traffic key and IV, in place
  of AES-128-GCM.
* Certificates are replaced by one Ed25519 key that the client trusts for
  the server name; there is no X.509 and no chain.
* There is no cipher suite, group or version negotiation, and no client
  authentication.

X25519 (RFC 7748), HKDF (RFC 5869) and Ed25519 (RFC 8032) are local copies.
For study only. The code is not constant time and must not protect real
data. Use a maintained TLS library such as OpenSSL, BoringSSL, rustls or the
ssl module of the Python standard library.
"""

import hashlib
import hmac
import secrets
from typing import Dict, List, Optional, Tuple

HASH_LEN = 32
KEY_LEN = 16  # AES-128-GCM key length
IV_LEN = 12

# Handshake types, RFC 8446 Section 4
CLIENT_HELLO, SERVER_HELLO, NEW_SESSION_TICKET = 1, 2, 4
ENCRYPTED_EXTENSIONS, CERTIFICATE, CERTIFICATE_VERIFY, FINISHED = 8, 11, 15, 20
MESSAGE_HASH = 254


class HandshakeError(Exception):
    pass


# ---------------------------------------------------------------- X25519, RFC 7748 Section 5

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

# ---------------------------------------------------------------- Ed25519, RFC 8032 Section 5.1

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
    s = (r + _h512(big_r, pub, msg) * a) % Q
    return big_r + s.to_bytes(32, "little")


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


# ---------------------------------------------------------------- HKDF and the TLS 1.3 key schedule


def hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
    return hmac.new(salt or bytes(HASH_LEN), ikm, hashlib.sha256).digest()


def hkdf_expand(prk: bytes, info: bytes, length: int) -> bytes:
    out, t, i = b"", b"", 1
    while len(out) < length:
        t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
        out += t
        i += 1
    return out[:length]


def hkdf_label(label: bytes, context: bytes, length: int) -> bytes:
    """The HkdfLabel structure of RFC 8446 Section 7.1."""
    full = b"tls13 " + label
    return length.to_bytes(2, "big") + bytes([len(full)]) + full + bytes([len(context)]) + context


def expand_label(secret: bytes, label: bytes, context: bytes, length: int) -> bytes:
    return hkdf_expand(secret, hkdf_label(label, context, length), length)


def transcript_hash(*messages: bytes) -> bytes:
    return hashlib.sha256(b"".join(messages)).digest()


def derive_secret(secret: bytes, label: bytes, th: bytes) -> bytes:
    """Derive-Secret with the transcript hash th already computed."""
    return expand_label(secret, label, th, HASH_LEN)


EMPTY_HASH = transcript_hash()
ZEROS = bytes(HASH_LEN)


def early_secret(psk: Optional[bytes]) -> bytes:
    return hkdf_extract(ZEROS, psk if psk is not None else ZEROS)


def handshake_secret(es: bytes, ecdhe: bytes) -> bytes:
    return hkdf_extract(derive_secret(es, b"derived", EMPTY_HASH), ecdhe)


def master_secret(hs: bytes) -> bytes:
    return hkdf_extract(derive_secret(hs, b"derived", EMPTY_HASH), ZEROS)


def traffic_keys(secret: bytes) -> Tuple[bytes, bytes]:
    """RFC 8446 Section 7.3: the write key and IV of a traffic secret."""
    return expand_label(secret, b"key", b"", KEY_LEN), expand_label(secret, b"iv", b"", IV_LEN)


def finished_key(base_key: bytes) -> bytes:
    return expand_label(base_key, b"finished", b"", HASH_LEN)


def verify_data(base_key: bytes, th: bytes) -> bytes:
    """Finished.verify_data, RFC 8446 Section 4.4.4."""
    return hmac.new(finished_key(base_key), th, hashlib.sha256).digest()


def resumption_psk(res_master: bytes, ticket_nonce: bytes) -> bytes:
    return expand_label(res_master, b"resumption", ticket_nonce, HASH_LEN)


def message_hash(client_hello1: bytes) -> bytes:
    """The synthetic message that replaces ClientHello1 after a HelloRetryRequest (Section 4.4.1)."""
    return bytes([MESSAGE_HASH, 0, 0, HASH_LEN]) + transcript_hash(client_hello1)


def cv_content(th: bytes) -> bytes:
    """The signed content of a server CertificateVerify, Section 4.4.3."""
    return b"\x20" * 64 + b"TLS 1.3, server CertificateVerify" + b"\x00" + th


# ---------------------------------------------------------------- records (study AEAD) and messages


def handshake(msg_type: int, body: bytes) -> bytes:
    return bytes([msg_type]) + len(body).to_bytes(3, "big") + body


def _record_keys(secret: bytes) -> Tuple[bytes, bytes, bytes]:
    key, iv = traffic_keys(secret)
    return hmac.new(key, b"enc", hashlib.sha256).digest(), hmac.new(key, b"mac", hashlib.sha256).digest(), iv


def protect(secret: bytes, seq: int, plaintext: bytes) -> bytes:
    ke, km, iv = _record_keys(secret)
    nonce = bytes(a ^ b for a, b in zip(iv, seq.to_bytes(IV_LEN, "big")))
    stream = b"".join(hmac.new(ke, nonce + i.to_bytes(4, "big"), hashlib.sha256).digest() for i in range(len(plaintext) // 32 + 1))
    ct = bytes(a ^ b for a, b in zip(plaintext, stream))
    return ct + hmac.new(km, nonce + ct, hashlib.sha256).digest()[:16]


def unprotect(secret: bytes, seq: int, record: bytes) -> bytes:
    ke, km, iv = _record_keys(secret)
    nonce = bytes(a ^ b for a, b in zip(iv, seq.to_bytes(IV_LEN, "big")))
    ct, tag = record[:-16], record[-16:]
    if not hmac.compare_digest(tag, hmac.new(km, nonce + ct, hashlib.sha256).digest()[:16]):
        raise HandshakeError("bad_record_mac")
    stream = b"".join(hmac.new(ke, nonce + i.to_bytes(4, "big"), hashlib.sha256).digest() for i in range(len(ct) // 32 + 1))
    return bytes(a ^ b for a, b in zip(ct, stream))


class Ticket:
    """What the client keeps from a NewSessionTicket."""

    def __init__(self, identity: bytes, psk: bytes, max_early_data: int) -> None:
        self.identity, self.psk, self.max_early_data = identity, psk, max_early_data


# ---------------------------------------------------------------- the server


class Server:
    def __init__(self, name: str, seed: bytes, single_use_tickets: bool = True) -> None:
        self.name, self.seed = name, seed
        self.public = ed25519_public(seed)
        self.single_use = single_use_tickets
        self.tickets: Dict[bytes, bytes] = {}  # ticket identity -> PSK
        self.early_data_log: List[bytes] = []  # 0-RTT data that the server acted on
        self.sessions: Dict[bytes, dict] = {}

    def respond(self, ch: bytes, early_record: Optional[bytes] = None) -> List[bytes]:
        body = ch[4:]
        cx, flags = body[32:64], body[64]
        psk: Optional[bytes] = None
        accept_early = False
        if flags & 1:  # a PSK is offered: identity, then the binder as the last 32 bytes
            ident_len = int.from_bytes(body[65:67], "big")
            identity, binder = body[67:67 + ident_len], ch[-HASH_LEN:]
            psk = self.tickets.get(identity)
            if psk is not None:
                es = early_secret(psk)  # @line L3
                binder_key = derive_secret(es, b"res binder", EMPTY_HASH)
                if not hmac.compare_digest(binder, verify_data(binder_key, transcript_hash(ch[:-HASH_LEN]))):
                    raise HandshakeError("decrypt_error: bad PSK binder")
                if self.single_use:
                    del self.tickets[identity]  # RFC 8446 Section 8.1
                accept_early = bool(flags & 2) and early_record is not None
        es = early_secret(psk)
        if accept_early:
            assert early_record is not None
            c_e = derive_secret(es, b"c e traffic", transcript_hash(ch))
            self.early_data_log.append(unprotect(c_e, 0, early_record))
        y = secrets.token_bytes(32)  # @line L4
        sh = handshake(SERVER_HELLO, secrets.token_bytes(32) + x25519(y, BASE_U) + bytes([1 if psk is not None else 0]))
        z = x25519(y, cx)
        hs = handshake_secret(es, z)  # @line L5
        th = transcript_hash(ch, sh)
        c_hs, s_hs = derive_secret(hs, b"c hs traffic", th), derive_secret(hs, b"s hs traffic", th)  # @line L6
        ee = handshake(ENCRYPTED_EXTENSIONS, bytes([1 if accept_early else 0]))
        flight = [ee]
        if psk is None:  # a full handshake authenticates the server with its signature key
            cert = handshake(CERTIFICATE, self.name.encode() + b"\x00" + self.public)
            cv = handshake(CERTIFICATE_VERIFY, ed25519_sign(self.seed, cv_content(transcript_hash(ch, sh, ee, cert))))  # @line L7
            flight += [cert, cv]
        fin = handshake(FINISHED, verify_data(s_hs, transcript_hash(ch, sh, *flight)))
        flight.append(fin)
        ms = master_secret(hs)  # @line L8
        th_sf = transcript_hash(ch, sh, *flight)
        c_ap, s_ap = derive_secret(ms, b"c ap traffic", th_sf), derive_secret(ms, b"s ap traffic", th_sf)  # @line L9
        sid = sh[4:36]
        self.sessions[sid] = dict(transcript=[ch, sh] + flight, c_hs=c_hs, ms=ms, c_ap=c_ap, s_ap=s_ap)
        return [sh] + [protect(s_hs, i, m) for i, m in enumerate(flight)]

    def finish(self, sid: bytes, record: bytes) -> bytes:
        """Check the client Finished, then send a NewSessionTicket under s_ap."""
        st = self.sessions[sid]
        fin = unprotect(st["c_hs"], 0, record)
        if fin != handshake(FINISHED, verify_data(st["c_hs"], transcript_hash(*st["transcript"]))):  # @line L14
            raise HandshakeError("decrypt_error: bad client Finished")
        st["transcript"].append(fin)
        rms = derive_secret(st["ms"], b"res master", transcript_hash(*st["transcript"]))
        nonce, identity = secrets.token_bytes(8), secrets.token_bytes(16)
        self.tickets[identity] = resumption_psk(rms, nonce)
        body = (7200).to_bytes(4, "big") + bytes([len(nonce)]) + nonce + len(identity).to_bytes(2, "big") + identity + (1024).to_bytes(4, "big")
        return protect(st["s_ap"], 0, handshake(NEW_SESSION_TICKET, body))


# ---------------------------------------------------------------- the client


class Client:
    def __init__(self, trusted: Dict[str, bytes]) -> None:
        self.trusted = trusted  # server name -> Ed25519 public key (stands in for certificate validation)
        self.state: dict = {}

    def hello(self, ticket: Optional[Ticket] = None, early_data: Optional[bytes] = None) -> Tuple[bytes, Optional[bytes]]:
        x = secrets.token_bytes(32)
        flags = (1 if ticket else 0) | (2 if ticket and early_data is not None else 0)
        body = secrets.token_bytes(32) + x25519(x, BASE_U) + bytes([flags])
        early_record = None
        if ticket is None:
            ch = handshake(CLIENT_HELLO, body)  # @line L1
            es = early_secret(None)
        else:
            body += len(ticket.identity).to_bytes(2, "big") + ticket.identity
            partial = handshake(CLIENT_HELLO, body + bytes(HASH_LEN))[:-HASH_LEN]  # the length counts the binder
            es = early_secret(ticket.psk)
            binder = verify_data(derive_secret(es, b"res binder", EMPTY_HASH), transcript_hash(partial))
            ch = partial + binder
            if early_data is not None:
                c_e = derive_secret(es, b"c e traffic", transcript_hash(ch))  # @line L2
                early_record = protect(c_e, 0, early_data)
        self.state = dict(x=x, ch=ch, es=es, psk=ticket is not None)
        return ch, early_record

    def handle(self, server_name: str, sh: bytes, records: List[bytes]) -> bytes:
        st = self.state
        sy = sh[36:68]
        if bool(sh[68]) != st["psk"]:
            raise HandshakeError("illegal_parameter: PSK mode")
        hs = handshake_secret(st["es"], x25519(st["x"], sy))  # @line L10
        th = transcript_hash(st["ch"], sh)
        c_hs, s_hs = derive_secret(hs, b"c hs traffic", th), derive_secret(hs, b"s hs traffic", th)
        msgs = [unprotect(s_hs, i, r) for i, r in enumerate(records)]
        transcript = [st["ch"], sh, msgs[0]]
        st["early_accepted"] = msgs[0][4] == 1
        rest = msgs[1:]
        if not st["psk"]:
            cert, cv = rest[0], rest[1]
            name, _, key = cert[4:].partition(b"\x00")
            if name.decode() != server_name or self.trusted.get(server_name) != key:  # @line L11
                raise HandshakeError("bad_certificate")
            transcript.append(cert)
            if not ed25519_verify(key, cv_content(transcript_hash(*transcript)), cv[4:]):
                raise HandshakeError("decrypt_error: bad CertificateVerify")
            transcript.append(cv)
            rest = rest[2:]
        fin = rest[0]
        if fin != handshake(FINISHED, verify_data(s_hs, transcript_hash(*transcript))):  # @line L12
            raise HandshakeError("decrypt_error: bad server Finished")
        transcript.append(fin)
        ms = master_secret(hs)
        th_sf = transcript_hash(*transcript)
        cfin = handshake(FINISHED, verify_data(c_hs, th_sf))  # @line L13
        st.update(c_hs=c_hs, s_hs=s_hs, c_ap=derive_secret(ms, b"c ap traffic", th_sf), s_ap=derive_secret(ms, b"s ap traffic", th_sf), ms=ms, transcript=transcript + [cfin], sid=sh[4:36])
        return protect(c_hs, 0, cfin)

    def take_ticket(self, record: bytes) -> Ticket:
        st = self.state
        nst = unprotect(st["s_ap"], 0, record)[4:]
        n = nst[4]
        nonce = nst[5:5 + n]
        ilen = int.from_bytes(nst[5 + n:7 + n], "big")
        identity = nst[7 + n:7 + n + ilen]
        max_early = int.from_bytes(nst[7 + n + ilen:11 + n + ilen], "big")
        rms = derive_secret(st["ms"], b"res master", transcript_hash(*st["transcript"]))
        return Ticket(identity, resumption_psk(rms, nonce), max_early)


def connect(client: Client, server: Server, name: str, ticket: Optional[Ticket] = None, early: Optional[bytes] = None) -> Tuple[dict, dict, Ticket]:
    """Run one handshake. Returns the client state, the server session state and the new ticket."""
    ch, early_record = client.hello(ticket, early)
    sh, *records = server.respond(ch, early_record)
    cfin = client.handle(name, sh, records)
    nst = server.finish(sh[4:36], cfin)
    return client.state, server.sessions[sh[4:36]], client.take_ticket(nst)
