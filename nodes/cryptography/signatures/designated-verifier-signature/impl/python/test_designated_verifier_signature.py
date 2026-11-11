# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/designated-verifier-signature/. The authors are listed in prov/FAQZXV.jsonl.
"""Tests for the OR-proof designated verifier signature on the toy group p = 2039."""

import random
from collections import Counter
from dataclasses import replace

from designated_verifier_signature import G, P, Q, Signature, keygen, signer_coins, simulate, simulator_coins, sign, verify

X_S, Y_S = keygen(random.Random(1))
X_V, Y_V = keygen(random.Random(2))


def test_group() -> None:
    assert P == 2 * Q + 1 and pow(G, Q, P) == 1 and G != 1


def test_signature_verifies() -> None:
    rng = random.Random(3)
    for i in range(20):
        msg = b"offer %d" % i
        sig = sign(X_S, Y_V, msg, coins=(rng.randrange(Q), rng.randrange(Q), rng.randrange(Q)))
        assert verify(Y_S, Y_V, msg, sig)
        assert not verify(Y_S, Y_V, msg + b"!", sig)
        assert not verify(Y_S, Y_S, msg, sig)


def test_signature_is_bound_to_the_designated_verifier() -> None:
    _, y_w = keygen(random.Random(4))
    msg = b"for V only"
    sig = sign(X_S, Y_V, msg)
    assert verify(Y_S, Y_V, msg, sig)
    assert not verify(Y_S, y_w, msg, sig)


def test_verifier_can_simulate_alone() -> None:
    msg = b"S agreed to pay 100"
    fake = simulate(Y_S, X_V, msg)
    assert verify(Y_S, Y_V, msg, fake)


def test_transcripts_are_identical_in_distribution() -> None:
    """Each valid signature comes from exactly one choice of signer coins and
    from exactly one choice of simulator coins, so the two outputs have the
    same uniform distribution over valid signatures."""
    msg = b"m"
    rng = random.Random(5)
    for _ in range(30):
        real = sign(X_S, Y_V, msg, coins=(rng.randrange(Q), rng.randrange(Q), rng.randrange(Q)))
        assert simulate(Y_S, X_V, msg, coins=simulator_coins(real, X_V)) == real
        fake = simulate(Y_S, X_V, msg, coins=(rng.randrange(Q), rng.randrange(Q), rng.randrange(Q)))
        assert sign(X_S, Y_V, msg, coins=signer_coins(fake, X_S)) == fake


def test_simple_statistics_match() -> None:
    msg = b"stats"
    rng = random.Random(6)
    n = 4000
    real = Counter(sign(X_S, Y_V, msg, coins=(rng.randrange(Q), rng.randrange(Q), rng.randrange(Q))).c_s % 4 for _ in range(n))
    fake = Counter(simulate(Y_S, X_V, msg, coins=(rng.randrange(Q), rng.randrange(Q), rng.randrange(Q))).c_s % 4 for _ in range(n))
    for r in range(4):
        assert abs(real[r] - fake[r]) < 200


def test_outsider_cannot_forge() -> None:
    rng = random.Random(7)
    fakes = [Signature(*(rng.randrange(Q) for _ in range(4))) for _ in range(40)]
    assert not any(verify(Y_S, Y_V, b"m", f) for f in fakes)
    sig = sign(X_S, Y_V, b"m")
    assert not verify(Y_S, Y_V, b"m", replace(sig, c_s=(sig.c_s + 1) % Q))
