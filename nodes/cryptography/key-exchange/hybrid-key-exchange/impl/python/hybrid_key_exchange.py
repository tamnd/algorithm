# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-key-exchange/. The authors are listed in prov/TTAAD5.jsonl.
"""A hybrid key exchange: X25519 plus a toy lattice KEM, joined by a KDF.

The client sends a KEM public key and an X25519 share. The server
encapsulates to the KEM key and sends the ciphertext and its own X25519
share. Each side has two shared secrets. The combiner concatenates them
(KEM secret first, as in X25519MLKEM768) and feeds the result, with the
transcript, to HKDF-SHA-256. The final key stays secret while either
component stays secret.

The KEM here is a toy: a small FrodoKEM-style LWE scheme without the
Fujisaki-Okamoto transform (so it is only IND-CPA at best) and with a
dimension far too small for security. It stands in for ML-KEM-768, which
this module does not implement. The X25519 part is a compact copy of the
RFC 7748 function.

For study only. The code is not constant time. Do not use it to protect
real data. Use X25519MLKEM768 in a TLS library (BoringSSL, OpenSSL 3.5 or
later, rustls), or ML-KEM and X25519 from a FIPS 140 validated module.

Cost: one X25519 key pair and one X25519 shared secret per side; the toy KEM
costs O(n^2 m) operations mod 2^15 for dimension n and m = 8 columns; the
combiner is two HMAC calls.
"""

import hashlib
import hmac
import random
import secrets
from typing import Optional

# ------------------------------------------------------------ X25519 (RFC 7748)

_P = 2**255 - 19
_A24 = 121665


def _clamp(k: bytes) -> int:
    b = bytearray(k)
    b[0] &= 248
    b[31] &= 127
    b[31] |= 64
    return int.from_bytes(b, "little")


def x25519(k: bytes, u: bytes) -> bytes:
    """X25519(k, u) of RFC 7748 Section 5 (Montgomery ladder on u only)."""
    if len(k) != 32 or len(u) != 32:
        raise ValueError("X25519 takes 32-byte inputs")
    n = _clamp(k)
    x1 = int.from_bytes(u, "little") & ((1 << 255) - 1)
    x2, z2, x3, z3, swap = 1, 0, x1, 1, 0
    for t in range(254, -1, -1):
        bit = (n >> t) & 1
        swap ^= bit
        if swap:
            x2, x3, z2, z3 = x3, x2, z3, z2
        swap = bit
        a, b = (x2 + z2) % _P, (x2 - z2) % _P
        aa, bb = a * a % _P, b * b % _P
        e = (aa - bb) % _P
        c, d = (x3 + z3) % _P, (x3 - z3) % _P
        da, cb = d * a % _P, c * b % _P
        x3 = (da + cb) ** 2 % _P
        z3 = x1 * (da - cb) ** 2 % _P
        x2 = aa * bb % _P
        z2 = e * (aa + _A24 * e) % _P
    if swap:
        x2, z2 = x3, z3
    return (x2 * pow(z2, _P - 2, _P) % _P).to_bytes(32, "little")


def x25519_base(k: bytes) -> bytes:
    return x25519(k, (9).to_bytes(32, "little"))


# ------------------------------------------------------------ toy LWE KEM

N = 64  # LWE dimension (FrodoKEM-640 uses 640)
NBAR = 8  # columns; NBAR * NBAR entries carry 2 message bits each
LOGQ = 15
QMOD = 1 << LOGQ
BITS_PER_ENTRY = 2
MU_BYTES = NBAR * NBAR * BITS_PER_ENTRY // 8  # 16 bytes = 128 message bits

Mat = list[list[int]]


def _gen_a(seed: bytes) -> Mat:
    """The public matrix A, n x n mod q, expanded from a 16-byte seed with SHAKE-128."""
    raw = hashlib.shake_128(b"A" + seed).digest(2 * N * N)
    vals = [int.from_bytes(raw[2 * i : 2 * i + 2], "little") % QMOD for i in range(N * N)]
    return [vals[r * N : (r + 1) * N] for r in range(N)]


def _small(rows: int, cols: int, rng: random.Random) -> Mat:
    """A matrix with entries in {-1, 0, 1} (a stand-in for the error distribution)."""
    return [[rng.choice((-1, 0, 0, 1)) for _ in range(cols)] for _ in range(rows)]


def _mul(x: Mat, y: Mat) -> Mat:
    yt = list(zip(*y))
    return [[sum(a * b for a, b in zip(row, col)) % QMOD for col in yt] for row in x]


def _add(x: Mat, y: Mat) -> Mat:
    return [[(a + b) % QMOD for a, b in zip(r, s)] for r, s in zip(x, y)]


def _sub(x: Mat, y: Mat) -> Mat:
    return [[(a - b) % QMOD for a, b in zip(r, s)] for r, s in zip(x, y)]


def _encode(mu: bytes) -> Mat:
    bits = int.from_bytes(mu, "little")
    vals = [((bits >> (2 * i)) & 3) * (QMOD >> BITS_PER_ENTRY) for i in range(NBAR * NBAR)]
    return [vals[r * NBAR : (r + 1) * NBAR] for r in range(NBAR)]


def _decode(m: Mat) -> bytes:
    bits = 0
    flat = [v for row in m for v in row]
    for i, v in enumerate(flat):
        k = ((v * (1 << BITS_PER_ENTRY) + QMOD // 2) >> LOGQ) & 3
        bits |= k << (2 * i)
    return bits.to_bytes(MU_BYTES, "little")


def _ser(m: Mat) -> bytes:
    return b"".join(v.to_bytes(2, "little") for row in m for v in row)


def kem_keygen(rng: random.Random) -> tuple[tuple[bytes, Mat], Mat]:
    """Public key (seed, B = A S + E) and secret key S."""
    seed = rng.randbytes(16)
    s, e = _small(N, NBAR, rng), _small(N, NBAR, rng)
    return (seed, _add(_mul(_gen_a(seed), s), e)), s


def kem_encaps(pk: tuple[bytes, Mat], rng: random.Random) -> tuple[tuple[Mat, Mat], bytes]:
    """Ciphertext (B' = S' A + E', V = S' B + E'' + Encode(mu)) and secret SHA-256(mu | ct)."""
    seed, b = pk
    mu = rng.randbytes(MU_BYTES)
    s1, e1, e2 = _small(NBAR, N, rng), _small(NBAR, N, rng), _small(NBAR, NBAR, rng)
    b1 = _add(_mul(s1, _gen_a(seed)), e1)
    v = _add(_add(_mul(s1, b), e2), _encode(mu))
    return (b1, v), hashlib.sha256(mu + _ser(b1) + _ser(v)).digest()


def kem_decaps(sk: Mat, ct: tuple[Mat, Mat]) -> bytes:
    """mu = Decode(V - B' S), then the secret SHA-256(mu | ct)."""
    b1, v = ct
    mu = _decode(_sub(v, _mul(b1, sk)))
    return hashlib.sha256(mu + _ser(b1) + _ser(v)).digest()


# ------------------------------------------------------------ the combiner


def combine(ss_pq: bytes, ss_ec: bytes, transcript: bytes) -> bytes:
    """K = HKDF-SHA-256 with IKM = ss_pq | ss_ec and info = label | SHA-256(transcript)."""
    prk = hmac.new(bytes(32), ss_pq + ss_ec, "sha256").digest()  # HKDF-Extract, zero salt
    info = b"toy hybrid v1" + hashlib.sha256(transcript).digest()
    return hmac.new(prk, info + b"\x01", "sha256").digest()  # HKDF-Expand, L = 32


def client_hello(rng: random.Random) -> tuple[bytes, dict]:
    """The client share: KEM public key and X25519 public key (KEM first)."""
    pk, sk = kem_keygen(rng)  # @line L1
    x = rng.randbytes(32)
    share = pk[0] + _ser(pk[1]) + x25519_base(x)  # @line L2
    return share, {"pk": pk, "sk": sk, "x": x}


def server_reply(client_share: bytes, client_pk: tuple[bytes, Mat], rng: random.Random) -> tuple[bytes, bytes, dict]:
    """The server share (KEM ciphertext, X25519 public key) and the server key."""
    ct, ss_pq = kem_encaps(client_pk, rng)  # @line L3
    y = rng.randbytes(32)
    ss_ec = x25519(y, client_share[-32:])
    if ss_ec == bytes(32):
        raise ValueError("X25519 output is all zero")
    share = _ser(ct[0]) + _ser(ct[1]) + x25519_base(y)  # @line L4
    key = combine(ss_pq, ss_ec, client_share + share)  # @line L6
    return share, key, {"ct": ct, "ss_pq": ss_pq, "ss_ec": ss_ec}


def client_finish(state: dict, client_share: bytes, server_share: bytes, ct: tuple[Mat, Mat]) -> bytes:
    """The client recovers both secrets and runs the same combiner."""
    ss_pq = kem_decaps(state["sk"], ct)  # @line L5
    ss_ec = x25519(state["x"], server_share[-32:])
    if ss_ec == bytes(32):
        raise ValueError("X25519 output is all zero")
    return combine(ss_pq, ss_ec, client_share + server_share)  # @line L6


def run(seed: Optional[int] = None) -> tuple[bytes, bytes, dict]:
    """One full exchange on a local simulated link. Returns both keys and the server's secrets."""
    rng = random.Random(seed) if seed is not None else secrets.SystemRandom()
    share_c, state = client_hello(rng)
    share_s, key_s, secrets_s = server_reply(share_c, state["pk"], rng)
    key_c = client_finish(state, share_c, share_s, secrets_s["ct"])
    return key_c, key_s, {**secrets_s, "transcript": share_c + share_s}
