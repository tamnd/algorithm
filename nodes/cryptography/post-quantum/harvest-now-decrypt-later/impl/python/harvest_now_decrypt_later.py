# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harvest-now-decrypt-later/. The authors are listed in prov/5T7EBA.jsonl.

"""Harvest now, decrypt later: Mosca's inequality and a toy recorder.

- mosca: Mosca's inequality x + y > z, where x is how long the data must stay
  secret, y is how long the migration takes, and z is the time until a
  quantum computer can break the public-key algorithm.
- exposed_window: the years (from now) in which new data is still encrypted
  with the old algorithm and must stay secret past the year z.
- Recorder: an adversary that stores toy sessions today and decrypts them
  later, after a leak of the server's long-term key or after a quantum
  computer arrives. Sessions use either static RSA key transport (as in
  TLS 1.2 RSA cipher suites) or ephemeral Diffie-Hellman with a signed
  server share (as in TLS 1.3).

The "quantum computer" here is a stand-in that factors and computes discrete
logarithms on toy parameters by classical search. The RSA is textbook RSA
with 16-bit primes and the group is a 31-bit prime field. For study only;
nothing here is secure or constant time. Use TLS 1.3 with a hybrid
post-quantum key exchange from a maintained library instead.
"""

import hashlib
import math
import random
from dataclasses import dataclass, field

# Toy parameters. P_DH = 2 Q_DH + 1 is a safe prime; G_DH = 4 has order Q_DH.
P_DH = 2147483783
Q_DH = 1073741891
G_DH = 4
RSA_P = 40009
RSA_Q = 40013
RSA_E = 65537


def mosca(x: float, y: float, z: float) -> bool:
    """Mosca's inequality: True if x + y > z, that is, if we must act now."""
    return x + y > z


def exposed_window(x: float, y: float, z: float):
    """The interval of creation times (years from now) of exposed data, or None.

    Data created at time t with the old algorithm must stay secret until
    t + x. It is exposed if t + x > z. Old algorithms stay in use until the
    migration ends at time y. So the exposed data is created in
    [max(0, z - x), y], which is not empty when x + y > z.
    """
    start = max(0.0, z - x)
    if start >= y:
        return None
    return (start, float(y))


def latest_start(x: float, y: float, z: float) -> float:
    """The latest year (from now) to start a migration of length y. Negative means late."""
    return z - x - y


def _keystream_xor(key: bytes, nonce: bytes, data: bytes) -> bytes:
    stream = hashlib.shake_256(key + nonce).digest(len(data))
    return bytes(a ^ b for a, b in zip(data, stream))


def _kdf(secret: int) -> bytes:
    return hashlib.sha256(secret.to_bytes(16, "big")).digest()


@dataclass
class Server:
    """A server with a long-term RSA key (used for key transport or for signing)."""

    n: int = RSA_P * RSA_Q
    e: int = RSA_E
    d: int = field(default=0, repr=False)

    def __post_init__(self) -> None:
        phi = (RSA_P - 1) * (RSA_Q - 1)
        assert math.gcd(self.e, phi) == 1
        self.d = pow(self.e, -1, phi)

    def sign(self, value: int) -> int:
        h = int.from_bytes(hashlib.sha256(value.to_bytes(16, "big")).digest(), "big") % self.n
        return pow(h, self.d, self.n)


@dataclass(frozen=True)
class Transcript:
    """What a passive adversary sees on the wire for one session."""

    kind: str  # "rsa-transport" or "ephemeral-dh"
    nonce: bytes
    public: tuple  # (rsa ciphertext,) or (client share, server share, signature)
    ciphertext: bytes


def session_rsa_transport(server: Server, message: bytes, rng: random.Random, nonce: bytes) -> Transcript:
    """The client picks a session key and encrypts it to the server's static RSA key."""
    k = rng.randrange(2, server.n)
    c = pow(k, server.e, server.n)
    return Transcript("rsa-transport", nonce, (c,), _keystream_xor(_kdf(k), nonce, message))


def session_ephemeral_dh(server: Server, message: bytes, rng: random.Random, nonce: bytes) -> Transcript:
    """Both sides pick fresh exponents, the server signs its share, and both erase the exponents."""
    a = rng.randrange(1, Q_DH)
    b = rng.randrange(1, Q_DH)
    A, B = pow(G_DH, a, P_DH), pow(G_DH, b, P_DH)
    shared = pow(B, a, P_DH)
    assert shared == pow(A, b, P_DH)
    sig = server.sign(B)
    return Transcript("ephemeral-dh", nonce, (A, B, sig), _keystream_xor(_kdf(shared), nonce, message))


def quantum_factor(n: int) -> int:
    """Stand-in for Shor's algorithm: a factor of n by trial division (toy n only)."""
    for f in range(3, math.isqrt(n) + 1, 2):
        if n % f == 0:
            return f
    raise ValueError("no factor")


def quantum_dlog(h: int) -> int:
    """Stand-in for Shor's algorithm: x with G_DH^x = h, by baby-step giant-step."""
    m = math.isqrt(Q_DH) + 1
    table = {}
    e = 1
    for j in range(m):
        table.setdefault(e, j)
        e = e * G_DH % P_DH
    giant = pow(G_DH, -m, P_DH)
    y = h
    for i in range(m + 1):
        if y in table:
            return (i * m + table[y]) % Q_DH
        y = y * giant % P_DH
    raise ValueError("no logarithm")


@dataclass
class Recorder:
    """A passive adversary that stores transcripts now and tries to decrypt them later."""

    transcripts: list = field(default_factory=list)
    rsa_private: int = 0  # 0 means unknown
    has_quantum: bool = False

    def record(self, t: Transcript) -> None:
        self.transcripts.append(t)

    def leak_long_term_key(self, server: Server) -> None:
        """A future compromise of the server reveals its long-term private key."""
        self.rsa_private = server.d

    def get_quantum_computer(self, server: Server) -> None:
        """A future quantum computer: factor the server key and solve discrete logs."""
        self.has_quantum = True
        f = quantum_factor(server.n)
        phi = (f - 1) * (server.n // f - 1)
        self.rsa_private = pow(server.e, -1, phi)

    def decrypt(self, t: Transcript, server: Server):
        """The plaintext of a recorded session, or None if the adversary cannot get the key."""
        if t.kind == "rsa-transport":
            if not self.rsa_private:
                return None
            k = pow(t.public[0], self.rsa_private, server.n)
            return _keystream_xor(_kdf(k), t.nonce, t.ciphertext)
        if t.kind == "ephemeral-dh":
            if not self.has_quantum:
                return None  # the signing key does not help: the exponents were erased
            A, B, _ = t.public
            a = quantum_dlog(A)
            return _keystream_xor(_kdf(pow(B, a, P_DH)), t.nonce, t.ciphertext)
        raise ValueError(t.kind)

    def exposed(self, server: Server) -> list:
        """All plaintexts the adversary can read now."""
        out = []
        for t in self.transcripts:
            m = self.decrypt(t, server)
            if m is not None:
                out.append(m)
        return out
