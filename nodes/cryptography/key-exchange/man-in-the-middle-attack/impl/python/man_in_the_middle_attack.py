# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/man-in-the-middle-attack/. The authors are listed in prov/0ZCK64.jsonl.
"""A man-in-the-middle attack on unauthenticated Diffie-Hellman, and two defences.

Alice and Bob run Diffie-Hellman over a network that Mallory controls. Mallory
swaps each public value for her own, so she shares one key with Alice and
another with Bob, and relays (and can change) every message. The module
also shows two defences on the same simulated network: a short
authentication string (SAS) that the users compare out of band, and a
signature by Bob on the exchanged values under a key that Alice already
trusts (a toy Schnorr signature).

The group is a toy 47-bit safe-prime group, far too small for real use.

For study only. The code is not constant time, and all parties are local
simulations. Do not use it to protect real data. Use TLS 1.3, Noise, or the
authenticated key exchange of a maintained library (libsodium, the Python
package cryptography) instead.

Cost: each party does two exponentiations; Mallory does four, and two
symmetric operations per relayed message.
"""

import hashlib
import random
from dataclasses import dataclass, field
from typing import Callable, Optional

P = 140737488356903  # a toy safe prime, p = 2q + 1
Q = (P - 1) // 2
G = 2  # generates the subgroup of order q, since p = 7 mod 8


def _kdf(z: int) -> bytes:
    return hashlib.sha256(b"key" + z.to_bytes(8, "big")).digest()


def toy_encrypt(key: bytes, nonce: int, data: bytes) -> bytes:
    """XOR with a SHA-256 keystream (no integrity). Also decrypts."""
    stream = b""
    counter = 0
    while len(stream) < len(data):
        stream += hashlib.sha256(key + nonce.to_bytes(8, "big") + counter.to_bytes(4, "big")).digest()
        counter += 1
    return bytes(a ^ b for a, b in zip(data, stream))


def sas(key: bytes) -> str:
    """A short authentication string: 20 bits of a hash of the key, as 5 hex digits."""
    return hashlib.sha256(b"sas" + key).hexdigest()[:5]


# ------------------------------------------------------------ toy Schnorr signature


def _challenge(r: int, msg: bytes) -> int:
    return int.from_bytes(hashlib.sha256(r.to_bytes(8, "big") + msg).digest(), "big") % Q


def schnorr_keygen(rng: random.Random) -> tuple[int, int]:
    s = rng.randrange(1, Q)
    return s, pow(G, s, P)


def schnorr_sign(s: int, msg: bytes, rng: random.Random) -> tuple[int, int]:
    k = rng.randrange(1, Q)
    r = pow(G, k, P)
    return r, (k + _challenge(r, msg) * s) % Q


def schnorr_verify(y: int, msg: bytes, sig: tuple[int, int]) -> bool:
    r, z = sig
    return pow(G, z, P) == r * pow(y, _challenge(r, msg), P) % P


# ------------------------------------------------------------ network and parties


@dataclass
class Network:
    """Delivers each message, but first hands it to the adversary hook, if any."""

    hook: Optional[Callable[[str, object], object]] = None
    seen: list[tuple[str, object]] = field(default_factory=list)

    def send(self, label: str, msg: object) -> object:
        self.seen.append((label, msg))
        return self.hook(label, msg) if self.hook else msg


class Mallory:
    """The adversary in the middle. She swaps public values and relays messages."""

    def __init__(self, rng: random.Random) -> None:
        self.rng = rng
        self.m1 = rng.randrange(1, Q)  # used toward Bob
        self.m2 = rng.randrange(1, Q)  # used toward Alice
        self.key_alice_pub: int = 0
        self.key_alice: bytes = b""
        self.key_bob: bytes = b""
        self.read: list[bytes] = []

    def hook(self, label: str, msg: object) -> object:
        if label == "A":  # @line L1
            self.key_alice_pub = msg
            return pow(G, self.m1, P)
        if label == "B":  # @line L2
            b_pub = msg[0] if isinstance(msg, tuple) else msg
            self.key_alice = _kdf(pow(self.key_alice_pub, self.m2, P))  # @line L3
            self.key_bob = _kdf(pow(b_pub, self.m1, P))  # @line L4
            fake = pow(G, self.m2, P)
            return (fake, *msg[1:]) if isinstance(msg, tuple) else fake
        if label == "data":  # @line L5
            nonce, ct = msg
            plain = toy_encrypt(self.key_alice, nonce, ct)
            self.read.append(plain)
            plain = plain.replace(b"Alice", b"Mallory")
            return (nonce, toy_encrypt(self.key_bob, nonce, plain))
        return msg


def unauthenticated_dh(net: Network, rng: random.Random) -> tuple[bytes, bytes]:
    """Plain Diffie-Hellman over net. Returns the keys of Alice and Bob."""
    a = rng.randrange(1, Q)
    b = rng.randrange(1, Q)
    a_seen_by_bob = net.send("A", pow(G, a, P))
    b_seen_by_alice = net.send("B", pow(G, b, P))
    return _kdf(pow(b_seen_by_alice, a, P)), _kdf(pow(a_seen_by_bob, b, P))


def send_message(net: Network, k_sender: bytes, k_receiver: bytes, text: bytes, nonce: int) -> bytes:
    """Alice encrypts text under her key; Bob decrypts what arrives under his key."""
    got_nonce, ct = net.send("data", (nonce, toy_encrypt(k_sender, nonce, text)))
    return toy_encrypt(k_receiver, got_nonce, ct)


def signed_dh(net: Network, bob_long_term: tuple[int, int], rng: random.Random) -> tuple[bytes, bytes]:
    """Bob signs (A, B) with a key Alice trusts. Alice raises ValueError if the check fails."""
    s_bob, y_bob = bob_long_term
    a = rng.randrange(1, Q)
    b = rng.randrange(1, Q)
    big_a = pow(G, a, P)
    a_seen_by_bob = net.send("A", big_a)
    big_b = pow(G, b, P)
    transcript = a_seen_by_bob.to_bytes(8, "big") + big_b.to_bytes(8, "big")
    b_seen, r, z = net.send("B", (big_b, *schnorr_sign(s_bob, transcript, rng)))
    expected = big_a.to_bytes(8, "big") + b_seen.to_bytes(8, "big")
    if not schnorr_verify(y_bob, expected, (r, z)):
        raise ValueError("Bob's signature does not cover the values Alice saw")
    return _kdf(pow(b_seen, a, P)), _kdf(pow(a_seen_by_bob, b, P))
