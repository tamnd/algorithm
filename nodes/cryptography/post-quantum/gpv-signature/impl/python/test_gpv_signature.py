# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gpv-signature/. The authors are listed in prov/ZA5GEM.jsonl.
# GPV has no standard test vectors. These tests check the scheme on toy
# parameters and run the Nguyen and Regev attack on a toy GGH-style signer.

import math
import random

from gpv_signature import GPV, GGHToySigner, attack_ggh


def test_trapdoor_basis_is_in_the_kernel_and_has_full_volume():
    sch = GPV(seed=1)
    for col in sch.basis:
        assert sch.mul_a(col) == [0] * sch.n
    # the Gram-Schmidt norms multiply to det(Lambda^perp(A)) = q^n
    log_det = sum(0.5 * math.log(sum(x * x for x in v)) for v in sch.gs)
    assert abs(log_det - sch.n * math.log(sch.q)) < 1e-6


def test_sign_and_verify():
    sch = GPV(seed=2)
    rng = random.Random(3)
    for i in range(20):
        msg = b"message %d" % i
        sig = sch.sign(msg, rng)
        assert sch.verify(msg, sig)
        assert not sch.verify(msg + b"!", sig)


def test_signature_is_short_compared_with_a_trivial_preimage():
    sch = GPV(seed=4)
    rng = random.Random(5)
    salt, x = sch.sign(b"hello", rng)
    assert math.sqrt(sum(v * v for v in x)) <= sch.beta
    # a forged vector with the right syndrome but not short is rejected
    t = sch.any_preimage(sch.hash_to_syndrome(b"hello", salt))
    big = [v + (sch.q if i == 0 else 0) for i, v in enumerate(t)]
    assert sch.mul_a(big) == sch.hash_to_syndrome(b"hello", salt)
    assert not sch.verify(b"hello", (salt, big))


def test_nguyen_regev_recovers_ggh_toy_key():
    rng = random.Random(2006)
    signer = GGHToySigner(4, rng)
    rows = attack_ggh(signer, 10000, rng)
    secret = {tuple(r) for r in signer.b} | {tuple(-x for x in r) for r in signer.b}
    assert all(tuple(r) in secret for r in rows)
    # the n recovered rows are distinct up to sign: the whole basis is found
    assert len({min(tuple(r), tuple(-x for x in r)) for r in rows}) == 4
