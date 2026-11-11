# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/password-authenticated-key-exchange/. The authors are listed in prov/EJCGN9.jsonl.
"""Two naive password protocols and the offline dictionary attacks that break
them. Both look like reasonable designs, and both fail the main goal of a
PAKE: the attacker must not be able to test password guesses offline.

* mac_protocol: plain Diffie-Hellman, and each side sends HMAC(H(pw), its
  share) to prove it knows the password. A passive eavesdropper tests every
  guess against one tag.
* exponent_protocol: Diffie-Hellman with the generator g^H(pw), so the
  password hash is a Diffie-Hellman exponent, plus a key-confirmation tag.
  An active attacker who plays the server in one run tests every guess.

The group is the subgroup of quadratic residues modulo a toy 128-bit safe
prime, and the parties are local simulations. The attacks run only on toy
parameters.

For study only. The code is not constant time, and it must not protect real
data.
"""

import hashlib
import hmac
import secrets

P = 255211775190703847597530955573826162347   # a toy safe prime, p = 2q + 1
Q = (P - 1) // 2
G = 4


def w_of(pw: bytes) -> int:
    """The password hash as a number in [1, q - 1]."""
    return 1 + int.from_bytes(hashlib.sha256(pw).digest(), "big") % (Q - 1)


def i2b(x: int) -> bytes:
    return x.to_bytes(16, "big")


def tag(key: bytes, *parts: int) -> bytes:
    return hmac.new(key, b"".join(i2b(p) for p in parts), hashlib.sha256).digest()


# ---------------------------------------------------------------- naive protocol 1: a MAC keyed by the password


def mac_protocol(pw: bytes, rng=secrets.randbelow):
    """Returns the transcript an eavesdropper sees: (X, tag_A, Y, tag_B)."""
    key = hashlib.sha256(pw).digest()
    x, y = 1 + rng(Q - 1), 1 + rng(Q - 1)
    X, Y = pow(G, x, P), pow(G, y, P)
    return X, tag(key, X), Y, tag(key, Y)


def passive_attack_on_mac(transcript, dictionary):
    """Test each guess against one recorded tag. No interaction is needed."""
    X, tag_a, _, _ = transcript
    return [pw for pw in dictionary if hmac.compare_digest(tag(hashlib.sha256(pw).digest(), X), tag_a)]


# ---------------------------------------------------------------- naive protocol 2: the password hash as an exponent


class ExponentClient:
    """The client of a run with generator g_pw = g^w. It confirms the key first."""

    def __init__(self, pw: bytes, rng=secrets.randbelow):
        self.gpw = pow(G, w_of(pw), P)
        self.x = 1 + rng(Q - 1)

    def first(self) -> int:
        return pow(self.gpw, self.x, P)            # X = g^(w x)

    def confirm(self, X: int, Y: int) -> bytes:
        K = pow(Y, self.x, P)
        return tag(hashlib.sha256(i2b(K)).digest(), X, Y)


def active_attack_on_exponent(dictionary, client: ExponentClient, rng=secrets.randbelow):
    """Play the server once with Y = g^y (no password), get the client's tag, then
    test every guess w' offline: if w' = w, then X^(y / w') = g^(x y) is the key."""
    X = client.first()
    y = 1 + rng(Q - 1)
    Y = pow(G, y, P)
    t = client.confirm(X, Y)
    found = []
    for pw in dictionary:
        K = pow(X, y * pow(w_of(pw), -1, Q) % Q, P)
        if hmac.compare_digest(tag(hashlib.sha256(i2b(K)).digest(), X, Y), t):
            found.append(pw)
    return found


def honest_exponent_run(pw_client: bytes, pw_server: bytes, rng=secrets.randbelow) -> bool:
    """An honest run: the server also uses g^w. Returns whether the tags match."""
    c = ExponentClient(pw_client, rng)
    X = c.first()
    y = 1 + rng(Q - 1)
    Y = pow(pow(G, w_of(pw_server), P), y, P)
    K = pow(X, y, P)
    return hmac.compare_digest(c.confirm(X, Y), tag(hashlib.sha256(i2b(K)).digest(), X, Y))
