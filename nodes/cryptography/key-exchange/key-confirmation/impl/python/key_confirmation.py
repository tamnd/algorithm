# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-confirmation/. The authors are listed in prov/YSM480.jsonl.
"""Key confirmation in two standard forms, and what it does and does not catch.

1. NIST SP 800-56A Rev. 3, Section 5.9: the derived keying material is split
   into MacKey || KeyData. The provider P sends
       MacTag = T_bits( HMAC(MacKey, message_string || ID_P || ID_R || EphemData_P || EphemData_R || Text) )
   with message_string "KC_1_U" / "KC_1_V" (unilateral) or "KC_2_U" / "KC_2_V"
   (bilateral). MacKey is erased after use.
2. TLS 1.3 Finished (RFC 8446, Section 4.4.4):
       finished_key = HKDF-Expand-Label(BaseKey, "finished", "", Hash.length)
       verify_data  = HMAC(finished_key, Transcript-Hash(messages so far))

A toy handshake then shows the two lessons:
- a MAC over the whole transcript catches a change to any message, even one
  that the signature does not cover and that leaves the shared key the same;
- key confirmation alone is not authentication: a man in the middle who runs
  one unauthenticated DH exchange with each side passes both confirmations.

The group is the subgroup of prime order q of Z_p^* for a 256-bit safe prime.
For study only. This code is not constant time apart from the final tag
compare, and it must not protect real data. Use TLS 1.3 through a vetted
library (OpenSSL, BoringSSL, rustls) or a FIPS 140 validated module.
"""

from __future__ import annotations

import hashlib
import hmac

P = 0xC00000000000000000000000000000000000000000000000000000000000A0EB
Q = (P - 1) // 2
G = 4


def b32(x: int) -> bytes:
    return x.to_bytes(32, "big")


def lp(data: bytes) -> bytes:
    """Datalen || Data with a 4-byte big-endian length, as SP 800-56A allows."""
    return len(data).to_bytes(4, "big") + data


# ------------------------------------------------------------ HKDF (RFC 5869) and the TLS 1.3 label


def hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
    return hmac.new(salt, ikm, hashlib.sha256).digest()


def hkdf_expand(prk: bytes, info: bytes, length: int) -> bytes:
    out, block, i = b"", b"", 1
    while len(out) < length:
        block = hmac.new(prk, block + info + bytes([i]), hashlib.sha256).digest()
        out, i = out + block, i + 1
    return out[:length]


def hkdf_expand_label(secret: bytes, label: str, context: bytes, length: int) -> bytes:
    """RFC 8446, Section 7.1: HkdfLabel = uint16 length || <"tls13 " + label> || <context>."""
    full = b"tls13 " + label.encode()
    info = length.to_bytes(2, "big") + bytes([len(full)]) + full + bytes([len(context)]) + context
    return hkdf_expand(secret, info, length)


def tls13_finished(base_key: bytes, transcript_hash: bytes) -> bytes:
    """verify_data of a TLS 1.3 Finished message with SHA-256. Cost: four HMAC calls."""
    finished_key = hkdf_expand_label(base_key, "finished", b"", 32)
    return hmac.new(finished_key, transcript_hash, hashlib.sha256).digest()


# ------------------------------------------------------------ SP 800-56A Rev. 3, Section 5.9


def split_dkm(dkm: bytes, mac_key_len: int) -> tuple[bytes, bytes]:
    """MacKey || KeyData = DerivedKeyingMaterial."""
    return dkm[:mac_key_len], dkm[mac_key_len:]


def mac_tag(mac_key: bytes, message_string: bytes, id_p: bytes, id_r: bytes, eph_p: bytes, eph_r: bytes, text: bytes = b"", tag_bits: int = 128) -> bytes:
    """MacTag_P = T_bits(HMAC-SHA-256(MacKey, MacData_P)). The standard needs tag_bits >= 64."""
    if message_string not in (b"KC_1_U", b"KC_1_V", b"KC_2_U", b"KC_2_V"):
        raise ValueError("unknown message_string")
    if not 64 <= tag_bits <= 256 or tag_bits % 8:
        raise ValueError("MacTagBits must be a whole number of bytes from 64 to 256")
    mac_data = message_string + lp(id_p) + lp(id_r) + lp(eph_p) + lp(eph_r) + text
    return hmac.new(mac_key, mac_data, hashlib.sha256).digest()[: tag_bits // 8]


def check_tag(expected: bytes, received: bytes) -> bool:
    """Compare in constant time: a plain == leaks the length of the matching prefix."""
    return hmac.compare_digest(expected, received)


# ------------------------------------------------------------ a toy handshake with Finished messages


def schnorr_sign(sk: int, msg: bytes) -> tuple[int, int]:
    k = int.from_bytes(hashlib.sha256(b"k" + b32(sk) + msg).digest(), "big") % Q or 1
    e = int.from_bytes(hashlib.sha256(b32(pow(G, k, P)) + msg).digest(), "big") % Q
    return e, (k + e * sk) % Q


def schnorr_verify(pk: int, msg: bytes, sig: tuple[int, int]) -> bool:
    e, s = sig
    r = pow(G, s, P) * pow(pk, Q - e, P) % P
    return int.from_bytes(hashlib.sha256(b32(r) + msg).digest(), "big") % Q == e


def client_hello(nonce: bytes, suites: list[str], x: int) -> dict:
    return {"nonce": nonce, "suites": list(suites), "X": pow(G, x, P)}


def server_hello(ch: dict, y: int, server_sk: int | None) -> dict:
    """The server picks the first suite it likes. Its signature covers only (client nonce, Y)."""
    choice = next(s for s in ("strong", "weak") if s in ch["suites"])
    y_pub = pow(G, y, P)
    sig = schnorr_sign(server_sk, ch["nonce"] + b32(y_pub)) if server_sk else None
    return {"suite": choice, "Y": y_pub, "sig": sig}


def encode(msg: dict) -> bytes:
    return repr(sorted(msg.items())).encode()


def keys_and_finished(z: int, ch: dict, sh: dict) -> tuple[bytes, bytes, bytes]:
    """Traffic secret from Z; Finished tags over the hash of (ClientHello, ServerHello) as each side saw them."""
    secret = hkdf_extract(b"\x00" * 32, b32(z))
    th = hashlib.sha256(encode(ch) + encode(sh)).digest()
    server_fin = tls13_finished(hkdf_expand_label(secret, "s hs traffic", th, 32), th)
    client_fin = tls13_finished(hkdf_expand_label(secret, "c hs traffic", th, 32), th)
    app_key = hkdf_expand_label(secret, "app", th, 32)
    return app_key, server_fin, client_fin
