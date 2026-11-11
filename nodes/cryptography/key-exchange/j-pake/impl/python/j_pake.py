# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/j-pake/. The authors are listed in prov/KK5EW8.jsonl.
"""J-PAKE (Hao and Ryan 2008; RFC 8236, Section 2) over a prime-order
subgroup of Z_p^*, with Schnorr non-interactive zero-knowledge proofs as in
RFC 8235, Section 2 and 3 (the Fiat-Shamir form, each hashed item prefixed
by its 4-byte length).

The group is the subgroup of quadratic residues modulo the 1024-bit safe
prime of RFC 5054, Appendix A: p = 2q + 1 and g = 4 of prime order q. The
final key confirmation is a simple HMAC over the transcript with role
labels, in the spirit of RFC 8236, Section 5, not its exact byte format.

For study only. The code is not constant time, and it must not protect real
data.

Lines marked L1 to L11 match the pseudocode on the page.
"""

import hashlib
import hmac
import secrets

P = int(
    "EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C"
    "9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE4"
    "8E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B29"
    "7BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9A"
    "FD5138FE8376435B9FC61D2FC0EB06E3",
    16,
)
Q = (P - 1) // 2
G = 4
NBYTES = 128


class JPakeError(ValueError):
    pass


def i2b(x: int) -> bytes:
    return x.to_bytes(NBYTES, "big")


def in_group(X: int) -> bool:
    return 1 < X < P and pow(X, Q, P) == 1


def h_items(*items: bytes) -> int:
    return int.from_bytes(hashlib.sha256(b"".join(len(i).to_bytes(4, "big") + i for i in items)).digest(), "big")


# ---------------------------------------------------------------- Schnorr NIZK (RFC 8235, Section 2)


def zkp_prove(gen: int, x: int, X: int, user: bytes, other: bytes = b"", rng=secrets.randbelow):
    v = rng(Q)                                                    # @line L8
    V = pow(gen, v, P)
    c = h_items(i2b(gen), i2b(V), i2b(X), user, other) % Q        # @line L9
    r = (v - x * c) % Q                                           # @line L10
    return V, r


def zkp_verify(gen: int, X: int, proof, user: bytes, other: bytes = b"") -> bool:
    V, r = proof
    if not in_group(X) or not in_group(V):
        return False
    c = h_items(i2b(gen), i2b(V), i2b(X), user, other) % Q
    return V == pow(gen, r, P) * pow(X, c, P) % P                 # @line L11


# ---------------------------------------------------------------- the two rounds (RFC 8236, Section 2)


def password_to_s(pw: bytes) -> int:
    s = int.from_bytes(hashlib.sha256(pw).digest(), "big") % Q
    if s == 0:
        raise JPakeError("s must not be 0 mod q")
    return s


class Party:
    def __init__(self, name: bytes, peer: bytes, pw: bytes, rng=secrets.randbelow):
        self.name, self.peer, self.s, self.rng = name, peer, password_to_s(pw), rng

    def round1(self):
        self.x1 = self.rng(Q)                                     # @line L1
        self.x2 = 1 + self.rng(Q - 1)
        self.G1, self.G2 = pow(G, self.x1, P), pow(G, self.x2, P)
        return dict(G1=self.G1, G2=self.G2,                       # @line L2
                    zkp1=zkp_prove(G, self.x1, self.G1, self.name, rng=self.rng),
                    zkp2=zkp_prove(G, self.x2, self.G2, self.name, rng=self.rng))

    def round2(self, m1: dict):
        G3, G4 = m1["G1"], m1["G2"]
        if not (zkp_verify(G, G3, m1["zkp1"], self.peer) and zkp_verify(G, G4, m1["zkp2"], self.peer)):   # @line L3
            raise JPakeError("bad round 1 proof")
        if G4 == 1:
            raise JPakeError("G4 must not be 1")
        self.G3, self.G4 = G3, G4
        gen = self.G1 * G3 * G4 % P
        e = self.x2 * self.s % Q
        A = pow(gen, e, P)                                        # @line L4
        return dict(A=A, zkp=zkp_prove(gen, e, A, self.name, rng=self.rng))

    def finish(self, m2: dict) -> bytes:
        gen = self.G1 * self.G2 * self.G3 % P
        if not zkp_verify(gen, m2["A"], m2["zkp"], self.peer):    # @line L5
            raise JPakeError("bad round 2 proof")
        t = pow(self.G4, self.x2 * self.s % Q, P)
        K = pow(m2["A"] * pow(t, P - 2, P) % P, self.x2, P)       # @line L6
        return hashlib.sha256(b"JPAKE study key" + i2b(K)).digest()   # @line L7


def confirm_tag(key: bytes, me: bytes, peer: bytes) -> bytes:
    return hmac.new(key, b"KC_1_" + me + b"|" + peer, hashlib.sha256).digest()


def run(pw_a: bytes, pw_b: bytes, rng=secrets.randbelow):
    """One J-PAKE run with key confirmation. Returns (key_A, key_B, confirmed)."""
    alice, bob = Party(b"alice", b"bob", pw_a, rng), Party(b"bob", b"alice", pw_b, rng)
    a1, b1 = alice.round1(), bob.round1()
    a2, b2 = alice.round2(b1), bob.round2(a1)
    ka, kb = alice.finish(b2), bob.finish(a2)
    ok = hmac.compare_digest(confirm_tag(ka, b"alice", b"bob"), confirm_tag(kb, b"alice", b"bob"))
    return ka, kb, ok
