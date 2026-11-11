# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/preimage-finding/. The authors are listed in prov/HTNXXE.jsonl.

import random

from preimage_finding import ToyCipherHash, brute_force_preimage, mitm_preimage


def test_enc_dec_are_inverse() -> None:
    hf = ToyCipherHash(24)
    rng = random.Random(1)
    for _ in range(200):
        h, m = rng.getrandbits(24), rng.getrandbits(32)
        assert hf.dec(hf.enc(h, m), m) == h


def test_brute_force_16_bits() -> None:
    hf = ToyCipherHash(16)
    target = hf.digest(0xCAFE, 0xBEEF)
    hf.calls = 0
    m1, m2 = brute_force_preimage(hf, target, random.Random(2008))
    assert hf.digest(m1, m2) == target
    assert hf.calls > 1000  # the generic attack needs about 2 * 2^16 calls on average


def test_mitm_32_bits() -> None:
    hf = ToyCipherHash(32)
    target = hf.digest(0x01234567, 0x89ABCDEF)
    hf.calls = 0
    m1, m2, stored = mitm_preimage(hf, target, random.Random(2009))
    assert hf.digest(m1, m2) == target
    # about 2^16 forward calls and 2^16 backward calls, against 2^32 for brute force
    assert hf.calls < 1 << 19
    assert stored > 60000


def test_mean_mitm_cost_matches_model() -> None:
    hf = ToyCipherHash(24)
    rng = random.Random(7)
    total, runs = 0, 20
    for _ in range(runs):
        target = rng.getrandbits(24)
        hf.calls = 0
        m1, m2, _ = mitm_preimage(hf, target, rng)
        assert hf.digest(m1, m2) == target
        total += hf.calls - 2
    mean = total / runs
    # 2^12 forward calls; the backward phase needs about 2^24 / (forward table size) calls
    assert 4096 + 2000 < mean < 4096 + 12000


def test_feed_forward_blocks_mitm() -> None:
    hf = ToyCipherHash(16, feed_forward=True)
    try:
        mitm_preimage(hf, 0, random.Random(1))
    except ValueError:
        pass
    else:
        raise AssertionError("Davies-Meyer has no backward step")
