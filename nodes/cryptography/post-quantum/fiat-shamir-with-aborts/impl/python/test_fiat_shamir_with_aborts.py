# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fiat-shamir-with-aborts/. The authors are listed in prov/NJ9J4P.jsonl.
# There are no standard vectors for the 2012 toy scheme. These tests check
# the scheme on toy parameters and show the leak that rejection prevents.

import math
import random

from fiat_shamir_with_aborts import Lyu12, estimate_secret


def test_sign_and_verify():
    sch = Lyu12(n=4, m=16, k=8, kappa=4, seed=1)
    rng = random.Random(2)
    for i in range(20):
        msg = b"msg %d" % i
        z, c, _ = sch.sign(msg, rng)
        assert sch.verify(msg, (z, c))
        assert not sch.verify(msg + b"x", (z, c))


def test_expected_repetitions_is_about_m():
    sch = Lyu12(n=2, m=8, k=4, kappa=2, seed=3)
    rng = random.Random(4)
    tries = [sch.sign(b"%d" % i, rng)[2] for i in range(1500)]
    mean = sum(tries) / len(tries)
    # M = exp(1 + 1/288) = 2.727; the rejection rule accepts with probability 1/M on average
    assert abs(sch.M - 2.727) < 0.01
    assert abs(mean - sch.M) < 0.25


def _pairs(sch, rng, count, reject):
    out = []
    while len(out) < count:
        c = [0] * sch.k
        i = rng.randrange(sch.k)
        c[i] = rng.choice((-1, 1))
        res = sch.respond(c, rng, reject)
        if res is not None:
            out.append((res, c))
    return out


def test_without_rejection_the_secret_leaks():
    # toy sizes: kappa = 1, so c = +-e_i and z = y +- (column i of S)
    sch = Lyu12(n=2, m=4, k=2, kappa=1, seed=5)
    est = estimate_secret(_pairs(sch, random.Random(6), 60000, reject=False), sch.m, sch.k)
    assert [[round(x) for x in row] for row in est] == sch.s


def test_with_rejection_the_estimate_is_noise():
    sch = Lyu12(n=2, m=4, k=2, kappa=1, seed=5)
    est = estimate_secret(_pairs(sch, random.Random(7), 60000, reject=True), sch.m, sch.k)
    flat = [x for row in est for x in row]
    # the accepted z follows D_sigma^m whatever c is, so E[z c^T] is zero
    noise = sch.sigma / math.sqrt(60000 / sch.k)
    assert max(abs(x) for x in flat) < 5 * noise
    assert all(round(x) == 0 for x in flat)
