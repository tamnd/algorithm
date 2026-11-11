# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proxy-signature/. The authors are listed in prov/HJZ5RV.jsonl.
"""A Schnorr proxy signature with delegation by warrant.

The original signer A (key y_a = g^x_a) delegates to the proxy B (key
y_b = g^x_b) with a warrant w that names A, B, the messages B may sign and an
expiry time. This is partial delegation with warrant in the Schnorr form of
Kim, Park and Won (ICICS 1997), with separate hash domains for delegation and
proxy signing. It is close to the Triple Schnorr scheme of Boldyreva, Palacio
and Warinschi, but it is not claimed to be identical to it:

    delegate:   K = g^k,  s_w = x_a * H1(w, K) + k          (sent to B)
    proxy key:  x_p = s_w + x_b,  y_p = y_a^H1(w, K) * K * y_b
    proxy sign: a Schnorr signature with x_p on (w, K, m)

The verifier recomputes y_p from public data, so it needs no secret of A or
B. A alone does not know x_b and B alone does not know s_w without A, so only
B can sign, and only with A's consent. The verifier checks the warrant before
the signature, so B can sign only what the warrant allows.

The group is a toy: p = 2039 = 2q + 1, q = 1019, and g = 4 generates the
subgroup of order q. For study only: the code is not constant time and the
parameters give no security.
"""

import hashlib
import random
import secrets
from dataclasses import dataclass

P, Q, G = 2039, 1019, 4


def _hash(*parts: bytes) -> int:
    return int.from_bytes(hashlib.sha256(b"|".join(parts)).digest(), "big") % Q


def keygen(rng: random.Random | None = None) -> tuple[int, int]:
    rng = rng or secrets.SystemRandom()
    x = rng.randrange(1, Q)
    return x, pow(G, x, P)


def in_group(y: int) -> bool:
    return 1 < y < P and pow(y, Q, P) == 1


@dataclass(frozen=True)
class Warrant:
    delegator: int  # y_a
    proxy: int  # y_b
    scope: bytes  # B may sign only messages that start with this prefix
    expires: int  # last time at which B may sign

    def encode(self) -> bytes:
        return b"%d;%d;%s;%d" % (self.delegator, self.proxy, self.scope.hex().encode(), self.expires)

    def allows(self, msg: bytes, now: int) -> bool:
        return msg.startswith(self.scope) and now <= self.expires


@dataclass(frozen=True)
class Delegation:
    warrant: Warrant
    K: int
    s_w: int


@dataclass(frozen=True)
class ProxySignature:
    warrant: Warrant
    K: int
    R: int
    z: int


def h_w(w: Warrant, K: int) -> int:
    return _hash(b"PROXY-WARRANT", w.encode(), b"%d" % K)


def h_m(w: Warrant, K: int, R: int, msg: bytes) -> int:
    return _hash(b"PROXY-SIGN", w.encode(), b"%d" % K, b"%d" % R, msg)


def delegate(x_a: int, w: Warrant, k: int | None = None) -> Delegation:
    """A signs the warrant. The result goes to B over a private channel."""
    if pow(G, x_a, P) != w.delegator:
        raise ValueError("x_a is not the delegator's key")
    k = secrets.randbelow(Q - 1) + 1 if k is None else k  # @line L1
    K = pow(G, k, P)
    return Delegation(w, K, (x_a * h_w(w, K) + k) % Q)  # @line L2


def public_proxy_key(w: Warrant, K: int) -> int:
    return pow(w.delegator, h_w(w, K), P) * K * w.proxy % P


def proxy_key(x_b: int, d: Delegation) -> int:
    """B checks the delegation and forms the proxy secret key."""
    w = d.warrant
    if pow(G, x_b, P) != w.proxy:
        raise ValueError("x_b is not the proxy named in the warrant")
    if pow(G, d.s_w, P) != pow(w.delegator, h_w(w, d.K), P) * d.K % P:  # @line L3
        raise ValueError("the delegation is not signed by the delegator")
    return (d.s_w + x_b) % Q  # @line L4


def proxy_sign(x_p: int, d: Delegation, msg: bytes, now: int, r: int | None = None) -> ProxySignature:
    if not d.warrant.allows(msg, now):  # @line L5
        raise ValueError("the warrant does not allow this message")
    r = secrets.randbelow(Q - 1) + 1 if r is None else r  # @line L6
    R = pow(G, r, P)
    return ProxySignature(d.warrant, d.K, R, (r + h_m(d.warrant, d.K, R, msg) * x_p) % Q)  # @line L7


def verify(y_a: int, msg: bytes, sig: ProxySignature, now: int) -> bool:
    """Check that sig is a proxy signature on msg on behalf of y_a, valid at time now."""
    w = sig.warrant
    if w.delegator != y_a or not all(in_group(v) for v in (w.delegator, w.proxy, sig.K, sig.R)):
        return False
    if not w.allows(msg, now):  # @line L8
        return False
    y_p = public_proxy_key(w, sig.K)  # @line L9
    e = h_m(w, sig.K, sig.R, msg)
    return 0 <= sig.z < Q and pow(G, sig.z, P) == sig.R * pow(y_p, e, P) % P  # @line L10
