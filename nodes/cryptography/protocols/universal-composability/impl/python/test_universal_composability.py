# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/universal-composability/. The authors are listed in prov/R8F0AW.jsonl.
# There are no official test vectors for UC proofs. These tests compute exact
# distinguishing advantages of a few fixed environments on toy one-byte
# protocols. Passing them does not prove UC security.

from fractions import Fraction

from universal_composability import (
    advantage,
    env_correct,
    env_low_bit,
    env_xor,
    prob_ideal,
    prob_real,
)


def test_one_session_cannot_be_told_apart() -> None:
    for m in (0, 7, 200):
        for env in (env_low_bit, env_correct):
            assert advantage(env, [m], shared_key=False) == 0
            assert advantage(env, [m], shared_key=True) == 0


def test_fresh_keys_compose() -> None:
    msgs = [0x41, 0x42]
    assert advantage(env_xor, msgs, shared_key=False) == 0
    assert advantage(env_correct, msgs, shared_key=False) == 0


def test_shared_key_breaks_under_composition() -> None:
    # Each session alone is perfectly secure, but two sessions that share a
    # key are not: Z sees c1 XOR c2 = m1 XOR m2 in the real world, while the
    # simulator, who never learns m1 or m2, matches it with probability 1/256.
    msgs = [0x41, 0x42]
    assert prob_real(env_xor, msgs, shared_key=True) == 1
    assert prob_ideal(env_xor, msgs) == Fraction(1, 256)
    assert advantage(env_xor, msgs, shared_key=True) == Fraction(255, 256)


def test_receiver_is_always_correct() -> None:
    assert prob_real(env_correct, [9, 10], shared_key=True) == 1
    assert prob_ideal(env_correct, [9, 10]) == 1
