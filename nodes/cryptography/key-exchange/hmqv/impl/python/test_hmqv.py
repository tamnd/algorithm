# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmqv/. The authors are listed in prov/294GKW.jsonl.

import hashlib
import random

from hmqv import G, P, Q, hbar, hmqv_key, hmqv_sigma, in_group, keypair


def test_agreement_and_direct_formula() -> None:
    rng = random.Random(1)
    for _ in range(10):
        (a, A), (b, B) = keypair(rng), keypair(rng)
        x, y = rng.randrange(1, Q), rng.randrange(1, Q)
        X, Y = pow(G, x, P), pow(G, y, P)
        ka = hmqv_key("alice", "bob", a, x, B, Y)
        kb = hmqv_key("bob", "alice", b, y, A, X)
        assert ka == kb and ka is not None
        d, e = hbar(X, "bob"), hbar(Y, "alice")
        assert 0 <= d < 2**128 and 0 <= e < 2**128
        assert hmqv_sigma("alice", "bob", a, x, B, Y) == pow(G, (x + d * a) * (y + e * b) % Q, P)


def test_invalid_values_are_rejected() -> None:
    rng = random.Random(2)
    (a, _), (_, B) = keypair(rng), keypair(rng)
    non_residue = next(v for v in range(2, 100) if pow(v, Q, P) != 1)
    for bad in (0, 1, P - 1, non_residue):
        assert hmqv_key("alice", "bob", a, 5, B, bad) is None
        assert hmqv_key("alice", "bob", a, 5, bad, pow(G, 7, P)) is None


def test_kaliski_construction_fails_against_hmqv() -> None:
    """The MQV unknown key-share attack: Eve makes (c, E = g^c) and X_e with X_e * E^d' = X * A^d.

    In MQV this makes B (talking to Eve) compute the same sigma as A (talking to B).
    In HMQV, B uses e = Hbar(Y, "eve") but A uses e = Hbar(Y, "alice"), so the values differ.
    """
    rng = random.Random(3)
    (a, A), (b, B) = keypair(rng), keypair(rng)
    x, y = rng.randrange(1, Q), rng.randrange(1, Q)
    X, Y = pow(G, x, P), pow(G, y, P)
    target = X * pow(A, hbar(X, "bob"), P) % P
    while True:
        u = rng.randrange(1, Q)
        x_e = target * pow(G, Q - u, P) % P
        d_e = hbar(x_e, "bob")
        if in_group(x_e) and d_e:
            break
    c = u * pow(d_e, -1, Q) % Q
    E = pow(G, c, P)
    assert x_e * pow(E, d_e, P) % P == target  # the combined values match, as in MQV
    sig_a = hmqv_sigma("alice", "bob", a, x, B, Y)
    sig_b = hmqv_sigma("bob", "eve", b, y, E, x_e)
    assert sig_a != sig_b


def test_two_message_protocols_have_only_weak_forward_secrecy() -> None:
    """The generic attack: Eve plays A with her own x', B completes; later a leaks, and Eve gets B's key."""
    rng = random.Random(4)
    (a, A), (b, B) = keypair(rng), keypair(rng)
    x_eve = rng.randrange(1, Q)
    X_eve = pow(G, x_eve, P)
    y = rng.randrange(1, Q)
    Y = pow(G, y, P)
    k_b = hmqv_key("bob", "alice", b, y, A, X_eve)  # B thinks it talks to A
    # Before the leak Eve cannot compute k_b. After a leaks:
    d, e = hbar(X_eve, "bob"), hbar(Y, "alice")
    sigma = pow(Y * pow(B, e, P) % P, (x_eve + d * a) % Q, P)
    assert hashlib.sha256(sigma.to_bytes(32, "big")).digest() == k_b
