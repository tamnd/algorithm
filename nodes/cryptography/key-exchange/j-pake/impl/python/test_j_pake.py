# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/j-pake/. The authors are listed in prov/KK5EW8.jsonl.
#
# RFC 8236 has no test vectors for the finite-field version. These tests
# check the group, the Schnorr proofs, agreement and the wrong-password case.

import random

import pytest

from j_pake import G, P, Q, JPakeError, Party, in_group, run, zkp_prove, zkp_verify


def miller_rabin(n: int, rounds: int = 20) -> bool:
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    rng = random.Random(n)
    for _ in range(rounds):
        x = pow(rng.randrange(2, n - 1), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def seeded(seed: int):
    r = random.Random(seed)
    return lambda n: r.randrange(n)


def test_group_has_prime_order_q():
    assert miller_rabin(P) and miller_rabin(Q)
    assert in_group(G) and pow(G, Q, P) == 1


def test_schnorr_nizk():
    rng = seeded(1)
    x = rng(Q)
    X = pow(G, x, P)
    proof = zkp_prove(G, x, X, b"alice", rng=rng)
    assert zkp_verify(G, X, proof, b"alice")
    assert not zkp_verify(G, X, proof, b"bob")                 # bound to the user name
    assert not zkp_verify(G, X * G % P, proof, b"alice")       # bound to the statement
    assert not zkp_verify(G, P - X, proof, b"alice")           # outside the subgroup


def test_agreement():
    ka, kb, ok = run(b"1234", b"1234", seeded(2))
    assert ka == kb and ok


def test_wrong_password_fails_confirmation():
    ka, kb, ok = run(b"1234", b"1235", seeded(3))
    assert ka != kb and not ok


def test_replayed_proof_from_the_other_side_is_rejected():
    rng = seeded(4)
    alice, bob = Party(b"alice", b"bob", b"pw", rng), Party(b"bob", b"alice", b"pw", rng)
    a1 = alice.round1()
    bob.round1()
    with pytest.raises(JPakeError):
        alice.round2(a1)          # Alice's own round 1 sent back: the proofs carry the name "alice"
