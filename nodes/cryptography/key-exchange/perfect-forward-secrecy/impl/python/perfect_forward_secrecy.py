# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/perfect-forward-secrecy/. The authors are listed in prov/8KQ7AG.jsonl.
"""Forward secrecy in code: RSA key transport against signed ephemeral Diffie-Hellman.

Each handshake below produces a transcript (what a passive recorder sees) and a
session key. The record is then encrypted under the key. Later the server's
long-term RSA key leaks. The functions named attack_* take the transcript, the
record and the leaked key, and try to read the record.

- RSA key transport: the client encrypts a random premaster secret to the
  server's RSA key. The leaked key decrypts it, so old records open.
- Signed ephemeral DH: the server signs its fresh Y with the RSA key; the key
  comes from g^(xy). The leaked key only signs; it gives nothing about x or y.
- A two-message implicitly authenticated protocol, K = H(Y^a, B^x, Y^x): it
  has weak forward secrecy, but an active attacker who chose x itself opens the
  session after it corrupts A (Krawczyk 2005).
- Session tickets: a resumption secret encrypted under a ticket key; a leaked
  ticket key opens the PSK-only resumed sessions.

All parameters are toys: textbook RSA with 1024-bit N and a 256-bit prime
order group. For study only. This code is not constant time, it branches on
secret data, and it must not protect real data. Use TLS 1.3 through a vetted
library (OpenSSL, BoringSSL, rustls, or a FIPS 140 validated module).
"""

from __future__ import annotations

import hashlib
import hmac

# ------------------------------------------------------------ toy primitives

# A safe prime p = 2q + 1 with 256 binary digits; g = 4 has order q.
P = 0xC00000000000000000000000000000000000000000000000000000000000A0EB
Q = (P - 1) // 2
G = 4

# Textbook RSA with two 512-bit primes. Toy only: real RSA needs OAEP or PSS.
RSA_P = 2**511 + 2**509 + 0x3063
RSA_Q = 2**511 + 2**507 + 0x10B2B
RSA_N = RSA_P * RSA_Q
RSA_E = 65537
RSA_D = pow(RSA_E, -1, (RSA_P - 1) * (RSA_Q - 1))


def b32(x: int) -> bytes:
    return x.to_bytes(32, "big")


def kdf(label: bytes, *parts: bytes) -> bytes:
    """A 32-byte key from HMAC-SHA-256 keyed by the label over the length-prefixed parts."""
    data = b"".join(len(p).to_bytes(4, "big") + p for p in parts)
    return hmac.new(label, data, hashlib.sha256).digest()


def stream_xor(key: bytes, nonce: bytes, data: bytes) -> bytes:
    """A toy stream cipher: SHA-256 in counter mode. Stands in for an AEAD."""
    out = bytearray()
    for i in range(0, len(data), 32):
        block = hashlib.sha256(key + nonce + i.to_bytes(8, "big")).digest()
        out += bytes(a ^ b for a, b in zip(data[i : i + 32], block))
    return bytes(out)


def rsa_sign(d: int, msg: bytes) -> int:
    """Textbook RSA signature on SHA-256(msg). Toy only."""
    return pow(int.from_bytes(hashlib.sha256(msg).digest(), "big"), d, RSA_N)


def rsa_verify(msg: bytes, sig: int) -> bool:
    return pow(sig, RSA_E, RSA_N) == int.from_bytes(hashlib.sha256(msg).digest(), "big")


# ------------------------------------------------------------ RSA key transport (no forward secrecy)


def rsa_transport_handshake(nc: bytes, ns: bytes, premaster: bytes) -> tuple[dict, bytes]:
    """Client sends C = pm^e mod N; both sides derive K = KDF(pm, nc, ns). Returns (transcript, key)."""
    c = pow(int.from_bytes(premaster, "big"), RSA_E, RSA_N)
    key = kdf(b"rsa-kt", premaster, nc, ns)
    return {"nc": nc, "ns": ns, "c": c}, key


def attack_rsa_transport(transcript: dict, record: bytes, leaked_d: int) -> bytes:
    """Decrypt the recorded premaster with the leaked private key, then the record."""
    pm = pow(transcript["c"], leaked_d, RSA_N).to_bytes(32, "big")
    key = kdf(b"rsa-kt", pm, transcript["nc"], transcript["ns"])
    return stream_xor(key, transcript["nc"], record)


# ------------------------------------------------------------ signed ephemeral DH (forward secret)


def ephemeral_dh_handshake(nc: bytes, ns: bytes, x: int, y: int) -> tuple[dict, bytes]:
    """Client sends X = g^x; server sends Y = g^y and an RSA signature over (nc, ns, X, Y).

    Both derive K = KDF(g^(xy), nc, ns, X, Y), then erase x and y.
    """
    x_pub, y_pub = pow(G, x, P), pow(G, y, P)
    sig = rsa_sign(RSA_D, nc + ns + b32(x_pub) + b32(y_pub))
    if not rsa_verify(nc + ns + b32(x_pub) + b32(y_pub), sig):
        raise ValueError("signature check failed")
    z = pow(y_pub, x, P)
    key = kdf(b"dhe", b32(z), nc, ns, b32(x_pub), b32(y_pub))
    return {"nc": nc, "ns": ns, "X": x_pub, "Y": y_pub, "sig": sig}, key


def attack_ephemeral_dh(transcript: dict, record: bytes, leaked_d: int) -> bytes:
    """Run the RSA transport attack on the DH transcript: apply the leaked key to Y.

    The leaked key only signs; no value on the wire was encrypted to it. So the
    "decrypted" value is not g^(xy), and the record stays closed. Finding g^(xy)
    from X and Y is the computational Diffie-Hellman problem.
    """
    guess = pow(transcript["Y"], leaked_d, RSA_N) % P
    key = kdf(b"dhe", b32(guess), transcript["nc"], transcript["ns"], b32(transcript["X"]), b32(transcript["Y"]))
    return stream_xor(key, transcript["nc"], record)


def attack_with_unerased_ephemeral(transcript: dict, record: bytes, x: int) -> bytes:
    """If the client kept x in memory and it leaks, the session opens: erasure is part of forward secrecy."""
    z = pow(transcript["Y"], x, P)
    key = kdf(b"dhe", b32(z), transcript["nc"], transcript["ns"], b32(transcript["X"]), b32(transcript["Y"]))
    return stream_xor(key, transcript["nc"], record)


# ------------------------------------------------------------ two-message implicit authentication: weak PFS only


def implicit_key(a_id: bytes, b_id: bytes, t1: int, t2: int, t3: int) -> bytes:
    """K = H(A, B, Y^a, B^x, Y^x) in the order (g^(ay), g^(bx), g^(xy))."""
    return kdf(b"implicit", a_id, b_id, b32(t1), b32(t2), b32(t3))


def implicit_responder(b_sk: int, a_pub: int, x_pub: int, y: int) -> tuple[int, bytes]:
    """B's side: send Y = g^y and compute K from A^y, X^b and X^y."""
    y_pub = pow(G, y, P)
    return y_pub, implicit_key(b"A", b"B", pow(a_pub, y, P), pow(x_pub, b_sk, P), pow(x_pub, y, P))


def implicit_initiator(a_sk: int, b_pub: int, x: int, y_pub: int) -> bytes:
    """A's side: compute K from Y^a, B^x and Y^x."""
    return implicit_key(b"A", b"B", pow(y_pub, a_sk, P), pow(b_pub, x, P), pow(y_pub, x, P))


def attack_active_then_corrupt(x_chosen: int, y_pub: int, b_pub: int, leaked_a: int) -> bytes:
    """Krawczyk's generic attack: the attacker sent X = g^x as A, never finished, and later corrupts A."""
    return implicit_key(b"A", b"B", pow(y_pub, leaked_a, P), pow(b_pub, x_chosen, P), pow(y_pub, x_chosen, P))


# ------------------------------------------------------------ session tickets


def issue_ticket(stek: bytes, ticket_nonce: bytes, resumption_secret: bytes) -> bytes:
    """The server stores no state: the ticket is the resumption secret encrypted under the ticket key."""
    return stream_xor(stek, ticket_nonce, resumption_secret)


def resumed_key_psk_only(resumption_secret: bytes, nc: bytes, ns: bytes) -> bytes:
    """A PSK-only resumption: the key comes from the resumption secret and the nonces, with no new DH."""
    return kdf(b"psk-only", resumption_secret, nc, ns)


def attack_ticket_key(ticket: bytes, ticket_nonce: bytes, nc: bytes, ns: bytes, record: bytes, leaked_stek: bytes) -> bytes:
    """With the ticket key, decrypt the ticket seen on the wire, then derive the resumed session key."""
    rs = stream_xor(leaked_stek, ticket_nonce, ticket)
    return stream_xor(resumed_key_psk_only(rs, nc, ns), nc, record)
