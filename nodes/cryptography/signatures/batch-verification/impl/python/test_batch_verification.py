# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/batch-verification/. The authors are listed in prov/VY28AZ.jsonl.

import random

from batch_verification import (
    G,
    P,
    Q,
    batch_verify,
    cancel_two,
    keygen,
    multi_exp,
    naive_batch_verify,
    sign,
    verify,
)


def make_batch(seed: int, count: int):
    rng = random.Random(seed)
    items = []
    for i in range(count):
        x, y = keygen(rng)
        msg = b"message %d" % i
        items.append((y, msg, sign(x, msg, rng)))
    return items


def test_multi_exp() -> None:
    rng = random.Random(3)
    bases = [pow(G, rng.randrange(Q), P) for _ in range(5)]
    exps = [rng.randrange(Q) for _ in range(5)]
    want = 1
    for b, e in zip(bases, exps):
        want = want * pow(b, e, P) % P
    assert multi_exp(bases, exps) == want


def test_good_batch_passes() -> None:
    items = make_batch(1, 20)
    assert all(verify(*it) for it in items)
    assert batch_verify(items, random.Random(2))
    assert naive_batch_verify(items)


def test_cancelling_bad_signatures_fool_the_naive_batch() -> None:
    items = cancel_two(make_batch(4, 10), 2, 7, delta=99)
    assert not verify(*items[2]) and not verify(*items[7])
    assert naive_batch_verify(items)  # the errors cancel in the plain sum
    # The weighted test passes only if z_2 = z_7 mod q, about 1 time in q = 1019
    # here; in a real group of order about 2^252 this is 2^(-l) for l <= 252.
    rng = random.Random(5)
    assert sum(batch_verify(items, rng) for _ in range(200)) <= 2


def test_error_is_about_two_to_the_minus_l() -> None:
    # One bad signature (s + delta); with weights of l = 4 binary digits the
    # bad batch passes only when its weight z is 0 mod q, so with probability 1/16.
    items = make_batch(6, 5)
    y, m, (r, s) = items[3]
    items[3] = (y, m, (r, (s + 1) % Q))
    rng = random.Random(1998)
    trials = 4000
    passed = sum(batch_verify(items, rng, l=4) for _ in range(trials))
    assert abs(passed / trials - 1 / 16) < 0.02
    assert passed / trials <= 2**-4 + 0.02


def test_out_of_range_values_are_rejected() -> None:
    items = make_batch(8, 3)
    y, m, (r, s) = items[0]
    items[0] = (y, m, (r, s + Q))
    assert not batch_verify(items, random.Random(9))
    items[0] = (y, m, (P - 1, s))  # P - 1 has order 2, not in the group
    assert not batch_verify(items, random.Random(9))
