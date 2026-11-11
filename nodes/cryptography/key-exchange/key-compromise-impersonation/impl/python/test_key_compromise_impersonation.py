# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-compromise-impersonation/. The authors are listed in prov/0KTA6M.jsonl.

import random

from key_compromise_impersonation import (
    G,
    P,
    Q,
    kci_mqv_attempt,
    kci_signed_dh,
    kci_static_dh,
    mqv_initiator,
    mqv_responder,
    sign,
    signed_dh_initiator,
    static_dh_initiator,
)


def keys(rng: random.Random):
    a, b = rng.randrange(1, Q), rng.randrange(1, Q)
    return a, b, pow(G, a, P), pow(G, b, P)


def test_static_dh_falls_to_kci() -> None:
    rng = random.Random(1)
    for _ in range(5):
        a, b, a_pub, b_pub = keys(rng)
        x, y = rng.randrange(1, Q), rng.randrange(1, Q)
        # Honest run: Bob would compute A^b; same key.
        assert static_dh_initiator(a, b_pub, x, pow(G, y, P)) == kci_static_dh(b, a_pub, pow(G, x, P), y)
        # Eve has only a. She answers Alice as "Bob" and knows the key Alice accepts.
        assert static_dh_initiator(a, b_pub, x, pow(G, y, P)) == kci_static_dh(a, b_pub, pow(G, x, P), y)


def test_signed_dh_resists_kci() -> None:
    rng = random.Random(2)
    for _ in range(5):
        a, b, a_pub, b_pub = keys(rng)
        x, y = rng.randrange(1, Q), rng.randrange(1, Q)
        x_pub, y_pub = pow(G, x, P), pow(G, y, P)
        honest = signed_dh_initiator(b_pub, x, y_pub, sign(b, x_pub.to_bytes(32, "big") + y_pub.to_bytes(32, "big") + b"A"))
        assert honest is not None
        y_eve, sig_eve = kci_signed_dh(a, x_pub, rng.randrange(1, Q))
        assert signed_dh_initiator(b_pub, x, y_eve, sig_eve) is None  # Alice rejects


def test_mqv_agrees_and_resists_the_direct_kci_attempt() -> None:
    rng = random.Random(3)
    for _ in range(5):
        a, b, a_pub, b_pub = keys(rng)
        x, y = rng.randrange(1, Q), rng.randrange(1, Q)
        k_alice = mqv_initiator(a, x, b_pub, pow(G, y, P))
        assert k_alice == mqv_responder(b, y, a_pub, pow(G, x, P))
        # Eve plays Bob with her own y and the stolen a.
        assert kci_mqv_attempt(a, pow(G, x, P), b_pub, y) != k_alice
        # With b (not a) the missing factor would be easy: that is ordinary knowledge of Bob's key.
        assert mqv_responder(b, y, a_pub, pow(G, x, P)) == k_alice
