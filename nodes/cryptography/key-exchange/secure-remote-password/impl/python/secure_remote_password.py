# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/secure-remote-password/. The authors are listed in prov/KNRW9R.jsonl.
"""SRP-6a as in RFC 5054, Sections 2.4 to 2.6, with SHA-1 and the 1024-bit group.

SHA-1 is used here only because the RFC 5054 Appendix B test vector uses it.
SHA-1 is broken for collision resistance (Stevens et al. 2017, Leurent and
Peyrin 2020); a new design would use SHA-256 or better, and a CFRG-selected
PAKE (OPAQUE or CPace) rather than SRP.

For study only. The code is not constant time (Python ints are not), and it
must not protect real data. Use a maintained library instead.

Lines marked L1 to L16 match the pseudocode on the page.
"""

import hashlib
import secrets

# RFC 5054, Appendix A, 1024-bit group. The prime N is a safe prime, g = 2.
N_1024 = int(
    "EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C"
    "9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE4"
    "8E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B29"
    "7BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9A"
    "FD5138FE8376435B9FC61D2FC0EB06E3",
    16,
)
G_1024 = 2


def H(*parts: bytes) -> bytes:
    """SHA-1 of the concatenation of the parts."""
    h = hashlib.sha1()
    for p in parts:
        h.update(p)
    return h.digest()


def to_bytes(x: int) -> bytes:
    """The implicit conversion of RFC 5054 Section 2.1: big-endian, no leading zero byte."""
    return x.to_bytes(max(1, (x.bit_length() + 7) // 8), "big")


def pad(x: int, N: int) -> bytes:
    """PAD(x): big-endian, left-padded with zeros to the byte length of N."""
    return x.to_bytes((N.bit_length() + 7) // 8, "big")


def b2i(b: bytes) -> int:
    return int.from_bytes(b, "big")


def multiplier(N: int = N_1024, g: int = G_1024) -> int:
    """k = SHA1(N | PAD(g)), the SRP-6a multiplier."""
    return b2i(H(to_bytes(N), pad(g, N)))                             # @line L1


def private_key(salt: bytes, user: bytes, password: bytes) -> int:
    """x = SHA1(s | SHA1(I | ":" | P))."""
    return b2i(H(salt, H(user, b":", password)))                      # @line L2


def verifier(salt: bytes, user: bytes, password: bytes, N: int = N_1024, g: int = G_1024) -> int:
    """v = g^x mod N. The server stores (I, s, v), not the password."""
    return pow(g, private_key(salt, user, password), N)               # @line L3


def scrambler(A: int, B: int, N: int = N_1024) -> int:
    """u = SHA1(PAD(A) | PAD(B))."""
    return b2i(H(pad(A, N), pad(B, N)))


class SRPError(ValueError):
    """An abort of the protocol: a bad public value or a failed proof."""


def client_public(a: int, N: int = N_1024, g: int = G_1024) -> int:
    return pow(g, a, N)                                               # @line L4


def server_public(b: int, v: int, N: int = N_1024, g: int = G_1024) -> int:
    """B = (k v + g^b) mod N."""
    k = multiplier(N, g)
    return (k * v + pow(g, b, N)) % N                                 # @line L5


def client_premaster(user: bytes, password: bytes, salt: bytes, a: int, B: int,
                     N: int = N_1024, g: int = G_1024) -> int:
    """S = (B - k g^x)^(a + u x) mod N, as computed by the client."""
    if B % N == 0:                                                    # @line L6
        raise SRPError("B mod N = 0")
    A = pow(g, a, N)
    u = scrambler(A, B, N)                                            # @line L7
    if u == 0:
        raise SRPError("u = 0")
    k = multiplier(N, g)
    x = private_key(salt, user, password)
    base = (B - k * pow(g, x, N)) % N                                 # @line L8
    return pow(base, a + u * x, N)                                    # @line L9


def server_premaster(A: int, b: int, v: int, N: int = N_1024, g: int = G_1024) -> int:
    """S = (A v^u)^b mod N, as computed by the server."""
    if A % N == 0:                                                    # @line L10
        raise SRPError("A mod N = 0")
    B = server_public(b, v, N, g)
    u = scrambler(A, B, N)                                            # @line L11
    if u == 0:
        raise SRPError("u = 0")
    return pow(A * pow(v, u, N) % N, b, N)                            # @line L12


def session_key(S: int, N: int = N_1024) -> bytes:
    """K = H(S). RFC 5054 feeds PAD-free S to the TLS PRF instead; this is the simple form."""
    return H(to_bytes(S))                                             # @line L13


def client_proof(A: int, B: int, K: bytes, N: int = N_1024) -> bytes:
    """M1 = H(A | B | K), the client evidence message of Wu 1998 (not the RFC 2945 form)."""
    return H(pad(A, N), pad(B, N), K)                                 # @line L14


def server_proof(A: int, M1: bytes, K: bytes, N: int = N_1024) -> bytes:
    """M2 = H(A | M1 | K)."""
    return H(pad(A, N), M1, K)                                        # @line L15


def run(user: bytes, password_client: bytes, password_server: bytes,
        N: int = N_1024, g: int = G_1024, rng=secrets.randbits):
    """One full run with registration and login. Returns (K_client, K_server).

    Raises SRPError if the server rejects the client proof (a wrong password).
    """
    salt = rng(128).to_bytes(16, "big")
    v = verifier(salt, user, password_server, N, g)        # registration
    a = rng(256) or 1
    b = rng(256) or 1
    A = client_public(a, N, g)
    B = server_public(b, v, N, g)
    Kc = session_key(client_premaster(user, password_client, salt, a, B, N, g), N)
    Ks = session_key(server_premaster(A, b, v, N, g), N)
    M1 = client_proof(A, B, Kc, N)
    if M1 != client_proof(A, B, Ks, N):                                # @line L16
        raise SRPError("client proof does not verify")
    M2 = server_proof(A, M1, Ks, N)
    if M2 != server_proof(A, M1, Kc, N):
        raise SRPError("server proof does not verify")
    return Kc, Ks
