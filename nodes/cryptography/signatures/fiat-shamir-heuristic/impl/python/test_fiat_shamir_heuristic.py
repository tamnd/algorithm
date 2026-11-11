# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fiat-shamir-heuristic/. The authors are listed in prov/PWQQZB.jsonl.

import random

from fiat_shamir_heuristic import (
    G,
    H,
    P,
    Q,
    challenge,
    forge_weak_dleq,
    move_to_related_key,
    prove_dleq,
    prove_dlog,
    sign_no_key_prefix,
    verify_dleq,
    verify_dlog,
    verify_no_key_prefix,
)


def dlog(base: int, target: int) -> int:
    """Brute force discrete log in the toy group, for the checks only."""
    acc = 1
    for i in range(Q):
        if acc == target:
            return i
        acc = acc * base % P
    raise ValueError("not in the group")


def test_group() -> None:
    assert pow(G, Q, P) == 1 and pow(H, Q, P) == 1
    assert G != 1 and H != 1


def test_honest_proofs_verify() -> None:
    rng = random.Random(1986)
    for strong in (True, False):
        for _ in range(100):
            x, k = rng.randrange(1, Q), rng.randrange(1, Q)
            assert verify_dlog(pow(G, x, P), prove_dlog(x, k, strong), strong)
            (u, v), proof = prove_dleq(x, k, strong)
            assert verify_dleq(u, v, proof, strong)


def test_worked_example() -> None:
    # The example of the page: x = 77, k = 500.
    proof = prove_dlog(77, 500)
    assert proof[0] == pow(G, 500, P)
    assert verify_dlog(pow(G, 77, P), proof)
    # A proof is bound to its statement: the same proof fails for another y.
    assert not verify_dlog(pow(G, 78, P), proof)


def test_weak_dleq_forgery() -> None:
    rng = random.Random(2012)
    forged = 0
    for _ in range(30):
        alpha, beta, s = rng.randrange(Q), rng.randrange(Q), rng.randrange(Q)
        if alpha == beta:
            continue
        a1, a2 = pow(G, alpha, P), pow(H, beta, P)
        if challenge(a1, a2) == 0:
            continue
        (u, v), proof = forge_weak_dleq(alpha, beta, s)
        # The statement is false: the two logarithms differ.
        assert dlog(G, u) != dlog(H, v)
        # The weak verifier accepts the false statement.
        assert verify_dleq(u, v, proof, strong=False)
        # The strong verifier, which hashes the statement, rejects it.
        assert not verify_dleq(u, v, proof, strong=True)
        forged += 1
    assert forged >= 25


def test_strong_proof_does_not_move_between_statements() -> None:
    rng = random.Random(3)
    moved = 0
    for _ in range(200):
        w, k = rng.randrange(1, Q), rng.randrange(1, Q)
        (u, v), proof = prove_dleq(w, k, strong=True)
        moved += verify_dleq(u, v * H % P, proof, strong=True)
    assert moved == 0


def test_related_key_attack_without_key_prefix() -> None:
    rng = random.Random(4)
    for _ in range(50):
        x, k, delta = rng.randrange(1, Q), rng.randrange(1, Q), rng.randrange(1, Q)
        y = pow(G, x, P)
        sig = sign_no_key_prefix(x, b"pay 5", k)
        assert verify_no_key_prefix(y, b"pay 5", sig)
        y2 = y * pow(G, delta, P) % P
        sig2 = move_to_related_key(sig, b"pay 5", delta)
        assert verify_no_key_prefix(y2, b"pay 5", sig2)
