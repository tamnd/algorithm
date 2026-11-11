# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-distribution-center/. The authors are listed in prov/ZVT3WS.jsonl.
"""A small key distribution center (KDC) and a pairwise-key network, with
counters for the keys that each design stores and the messages that each
session costs.

KDC flow (a minimal Needham-Schroeder or Kerberos style flow, without the
handshake that each real protocol adds):
    1. A -> KDC : A, B, N_A
    2. KDC -> A : Seal(K_A, K_AB || B || N_A || expiry), ticket
                  with ticket = Seal(K_B, K_AB || A || expiry)
    3. A -> B   : ticket

The AEAD is a study construction: encrypt-then-MAC with an HMAC-SHA256
key stream in counter mode and an HMAC-SHA256 tag. It is not a standard
AEAD.

For study only. The code is not constant time and must not protect real
data. Use a real Kerberos implementation (MIT Kerberos, Heimdal, Active
Directory) or a standard AEAD from a FIPS 140 validated module or libsodium.
"""

import hashlib
import hmac
import json
import secrets
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------- study AEAD


class AuthError(Exception):
    pass


def _prf(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha256).digest()


def seal(key: bytes, plaintext: bytes, ad: bytes = b"") -> bytes:
    """Return nonce (12 bytes) || ciphertext || tag (16 bytes)."""
    nonce = secrets.token_bytes(12)
    ke, km = _prf(key, b"enc"), _prf(key, b"mac")
    stream = b"".join(_prf(ke, nonce + i.to_bytes(4, "big")) for i in range(len(plaintext) // 32 + 1))
    ct = bytes(x ^ y for x, y in zip(plaintext, stream))
    tag = _prf(km, len(ad).to_bytes(8, "big") + ad + nonce + ct)[:16]
    return nonce + ct + tag


def open_sealed(key: bytes, box: bytes, ad: bytes = b"") -> bytes:
    if len(box) < 28:
        raise AuthError("short")
    nonce, ct, tag = box[:12], box[12:-16], box[-16:]
    ke, km = _prf(key, b"enc"), _prf(key, b"mac")
    if not hmac.compare_digest(tag, _prf(km, len(ad).to_bytes(8, "big") + ad + nonce + ct)[:16]):
        raise AuthError("bad tag")
    stream = b"".join(_prf(ke, nonce + i.to_bytes(4, "big")) for i in range(len(ct) // 32 + 1))
    return bytes(x ^ y for x, y in zip(ct, stream))


def enc_json(key: bytes, obj: dict) -> bytes:
    return seal(key, json.dumps(obj, sort_keys=True).encode())


def dec_json(key: bytes, box: bytes) -> dict:
    return json.loads(open_sealed(key, box))


# ---------------------------------------------------------------- the KDC network


class KDC:
    """Shares one long-term key with each registered user and issues session keys."""

    def __init__(self) -> None:
        self.long_term: Dict[str, bytes] = {}
        self.messages = 0
        self.up = True

    def register(self, name: str) -> bytes:
        k = secrets.token_bytes(32)
        self.long_term[name] = k  # in practice, this key reaches the user over a secure channel
        return k

    def request(self, a: str, b: str, nonce: str, now: int, lifetime: int = 3600) -> Tuple[bytes, bytes]:
        """Message 2: the reply to A, which holds A's copy of K_AB and the ticket for B."""
        if not self.up:
            raise ConnectionError("KDC unreachable")
        self.messages += 2  # message 1 arrives, message 2 leaves
        if a not in self.long_term or b not in self.long_term:
            raise KeyError("unknown principal")
        k_ab = secrets.token_bytes(32).hex()
        expiry = now + lifetime
        ticket = enc_json(self.long_term[b], {"key": k_ab, "peer": a, "expiry": expiry})
        reply = enc_json(self.long_term[a], {"key": k_ab, "peer": b, "nonce": nonce, "expiry": expiry})
        return reply, ticket


class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self.long_term: Dict[str, bytes] = {}  # one key per party that this user shares a key with
        self.sessions: Dict[str, bytes] = {}

    def stored_keys(self) -> int:
        return len(self.long_term)


def kdc_session(kdc: KDC, a: User, b: User, now: int) -> bytes:
    """Run messages 1 to 3. Returns the session key that both A and B now hold."""
    nonce = secrets.token_hex(8)
    reply, ticket = kdc.request(a.name, b.name, nonce, now)
    r = dec_json(a.long_term["KDC"], reply)
    if r["nonce"] != nonce or r["peer"] != b.name:
        raise AuthError("stale or wrong reply")
    kdc.messages += 1  # message 3: A -> B
    accept_ticket(b, a.name, ticket, now)
    a.sessions[b.name] = bytes.fromhex(r["key"])
    return a.sessions[b.name]


def accept_ticket(b: User, claimed_sender: str, ticket: bytes, now: int) -> bytes:
    """B opens a ticket, checks the sender name and the expiry, and stores the key."""
    t = dec_json(b.long_term["KDC"], ticket)
    if t["expiry"] < now or t["peer"] != claimed_sender:
        raise AuthError("bad ticket")
    b.sessions[claimed_sender] = bytes.fromhex(t["key"])
    return b.sessions[claimed_sender]


def build_kdc_network(n: int) -> Tuple[KDC, List[User]]:
    kdc = KDC()
    users = [User(f"U{i}") for i in range(n)]
    for u in users:
        u.long_term["KDC"] = kdc.register(u.name)
    return kdc, users


def build_pairwise_network(n: int) -> List[User]:
    """Each pair shares its own long-term key, set up in advance."""
    users = [User(f"U{i}") for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            k = secrets.token_bytes(32)
            users[i].long_term[users[j].name] = k
            users[j].long_term[users[i].name] = k
    return users


def cost_table(n: int, sessions: int) -> Dict[str, Dict[str, int]]:
    """Counts for both designs, for n users and the given number of sessions."""
    kdc, users = build_kdc_network(n)
    for s in range(sessions):
        a, b = users[s % n], users[(s + 1) % n]
        kdc_session(kdc, a, b, now=1000 + s)
    pair = build_pairwise_network(n)
    distinct_pair_keys = len({k for u in pair for k in u.long_term.values()})
    return {
        "kdc": {
            "keys_total": len(kdc.long_term),
            "keys_at_center": len(kdc.long_term),
            "keys_per_user": max(u.stored_keys() for u in users),
            "messages": kdc.messages,
            "keys_to_add_user": 1,
        },
        "pairwise": {
            "keys_total": distinct_pair_keys,
            "keys_at_center": 0,
            "keys_per_user": max(u.stored_keys() for u in pair),
            "messages": 0,
            "keys_to_add_user": n,
        },
    }


def read_recorded_ticket(stolen_database: Dict[str, bytes], receiver: str, ticket: bytes) -> Optional[bytes]:
    """What an attacker with a copy of the KDC database learns from a recorded ticket."""
    try:
        return bytes.fromhex(dec_json(stolen_database[receiver], ticket)["key"])
    except (KeyError, AuthError):
        return None
