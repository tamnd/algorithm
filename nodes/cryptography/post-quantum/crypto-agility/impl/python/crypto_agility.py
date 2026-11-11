# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crypto-agility/. The authors are listed in prov/YNGHPQ.jsonl.

"""Cryptographic agility: an algorithm registry, negotiation, and downgrade detection.

- Registry: algorithms by code point, with a status (approved, deprecated,
  disallowed) that a policy change can update without code changes.
- negotiate: the server picks the first algorithm in its own preference
  order that the client offered and the policy allows.
- handshake: a toy handshake with an active attacker who may remove
  algorithms from the client's offer. Three protections are compared:
  none; a MAC over the transcript under the session key (TLS 1.2 Finished);
  and a server signature over the transcript (TLS 1.3 CertificateVerify).
  The MAC fails when the attacker can break the downgraded algorithm and so
  learn the session key, as in FREAK and Logjam. The signature does not.
- inventory: a small cryptographic bill of materials (CBOM) summary.

The "signature" is an HMAC under a long-term key that the client is assumed
to know; it stands in for a public-key signature. For study only; nothing
here is secure or constant time. Real protocols should use a maintained TLS
library, which implements RFC 8446 negotiation and downgrade protection.
"""

import hashlib
import hmac
from dataclasses import dataclass, field

APPROVED = "approved"
DEPRECATED = "deprecated"
DISALLOWED = "disallowed"


@dataclass
class Algorithm:
    """One registry entry."""

    name: str
    code_point: int
    status: str = APPROVED
    quantum_safe: bool = False
    breakable_now: bool = False  # an attacker can recover session keys today


@dataclass
class Registry:
    """Algorithms by code point. Policy changes the status, not the code."""

    entries: dict = field(default_factory=dict)

    def register(self, alg: Algorithm) -> None:
        if alg.code_point in self.entries:
            raise ValueError(f"code point {alg.code_point:#06x} already used")
        self.entries[alg.code_point] = alg

    def set_status(self, code_point: int, status: str) -> None:
        if status not in (APPROVED, DEPRECATED, DISALLOWED):
            raise ValueError(status)
        self.entries[code_point].status = status

    def get(self, code_point: int):
        return self.entries.get(code_point)

    def allowed(self, code_point: int) -> bool:
        alg = self.get(code_point)
        return alg is not None and alg.status != DISALLOWED


def tls_groups() -> Registry:
    """A registry with some TLS 1.3 named groups and one invented weak group.

    The code points of x25519, secp256r1, ffdhe2048, SecP256r1MLKEM768 and
    X25519MLKEM768 are the IANA TLS Supported Groups values. The weak group
    0xff01 is invented here to model a 512-bit export group (Logjam).
    """
    r = Registry()
    r.register(Algorithm("X25519MLKEM768", 0x11EC, quantum_safe=True))
    r.register(Algorithm("SecP256r1MLKEM768", 0x11EB, quantum_safe=True))
    r.register(Algorithm("x25519", 0x001D))
    r.register(Algorithm("secp256r1", 0x0017))
    r.register(Algorithm("ffdhe2048", 0x0100))
    r.register(Algorithm("toy-export-dh-512", 0xFF01, status=DEPRECATED, breakable_now=True))
    return r


def negotiate(registry: Registry, offer: list, server_preference: list):
    """The first code point in server order that was offered and is allowed, or None."""
    offered = set(offer)
    for cp in server_preference:
        if cp in offered and registry.allowed(cp):
            return cp
    return None


def transcript_hash(offer: list, chosen) -> bytes:
    """Hash of the offer, in order, and of the choice."""
    h = hashlib.sha256()
    for cp in offer:
        h.update(cp.to_bytes(2, "big"))
    h.update(b"|")
    h.update((chosen if chosen is not None else 0xFFFF).to_bytes(2, "big"))
    return h.digest()


@dataclass
class HandshakeResult:
    chosen: object
    detected: bool


def handshake(
    registry: Registry,
    client_offer: list,
    server_preference: list,
    protection: str,
    strip=None,
    server_key: bytes = b"server long-term key",
) -> HandshakeResult:
    """Run one handshake. strip, if given, is the set of code points the attacker removes.

    protection is "none", "session-mac" or "signed-transcript".
    """
    sent = [cp for cp in client_offer if registry.allowed(cp)]
    received = [cp for cp in sent if not strip or cp not in strip]
    chosen = negotiate(registry, received, server_preference)
    if chosen is None:
        return HandshakeResult(None, False)
    client_view = transcript_hash(sent, chosen)
    server_view = transcript_hash(received, chosen)
    if protection == "none":
        return HandshakeResult(chosen, False)
    if protection == "session-mac":
        session_key = hashlib.sha256(b"toy session key" + chosen.to_bytes(2, "big")).digest()
        server_mac = hmac.new(session_key, server_view, hashlib.sha256).digest()
        if registry.get(chosen).breakable_now:
            # The attacker breaks the weak exchange, learns the session key,
            # and rewrites the server's MAC to match the client's transcript.
            server_mac = hmac.new(session_key, client_view, hashlib.sha256).digest()
        expected = hmac.new(session_key, client_view, hashlib.sha256).digest()
        return HandshakeResult(chosen, not hmac.compare_digest(server_mac, expected))
    if protection == "signed-transcript":
        signature = hmac.new(server_key, server_view, hashlib.sha256).digest()
        expected = hmac.new(server_key, client_view, hashlib.sha256).digest()
        return HandshakeResult(chosen, not hmac.compare_digest(signature, expected))
    raise ValueError(protection)


def inventory(registry: Registry, usages: list) -> dict:
    """Summarize (system, code point) usages: counts by status and quantum safety."""
    out = {"total": 0, "quantum_vulnerable": 0, APPROVED: 0, DEPRECATED: 0, DISALLOWED: 0, "unknown": 0}
    for _, cp in usages:
        out["total"] += 1
        alg = registry.get(cp)
        if alg is None:
            out["unknown"] += 1
            continue
        out[alg.status] += 1
        if not alg.quantum_safe:
            out["quantum_vulnerable"] += 1
    return out
