# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/oblivious-transfer/. The authors are listed in prov/H3BHXZ.jsonl.
# There are no official test vectors for these OT protocols. The tests check
# correctness for both choice bits, and that the receiver's message has the
# same distribution for both choice bits (a chi-square test on toy groups).

import random
from collections import Counter

from oblivious_transfer import (
    SMALL_GROUP,
    TOY_GROUP,
    RSAKey,
    egl_malicious_receiver,
    egl_rsa_ot,
    is_probable_prime,
    rsa_keygen,
    simplest_ot,
)


def chi2_two_samples(a: Counter, b: Counter, bins: list) -> float:
    """Chi-square statistic for equal distributions of two samples of equal size."""
    return sum((a[k] - b[k]) ** 2 / (a[k] + b[k]) for k in bins if a[k] + b[k] > 0)


def test_toy_groups_are_safe_prime_groups() -> None:
    for grp in (SMALL_GROUP, TOY_GROUP):
        assert is_probable_prime(grp.p) and is_probable_prime(grp.q)
        assert grp.p == 2 * grp.q + 1
        assert grp.contains(grp.g) and grp.g != 1


def test_egl_correct_for_both_choices() -> None:
    rng = random.Random(1985)
    key = rsa_keygen(32, rng)
    assert pow(pow(12345, key.e, key.n), key.d, key.n) == 12345
    for _ in range(300):
        m0, m1 = rng.randrange(key.n), rng.randrange(key.n)
        for b in (0, 1):
            t = egl_rsa_ot(m0, m1, b, key, rng)
            assert t.output == (m1 if b else m0)


def test_egl_receiver_message_does_not_depend_on_choice() -> None:
    # N = 61 * 53 = 3233, e = 17, d = 413 (the classic toy key).
    key = RSAKey(3233, 17, 413)
    rng = random.Random(7)
    samples = {0: Counter(), 1: Counter()}
    for b in (0, 1):
        for _ in range(20000):
            v = egl_rsa_ot(5, 9, b, key, rng).v
            samples[b][v * 16 // 3233] += 1
    # 16 bins: 15 degrees of freedom, 0.999 quantile about 37.7.
    assert chi2_two_samples(samples[0], samples[1], list(range(16))) < 37.7


def test_egl_malicious_receiver_learns_a_relation() -> None:
    # Semi-honest EGL gives no protection against a receiver who picks v.
    rng = random.Random(11)
    key = rsa_keygen(32, rng)
    for _ in range(50):
        m0, m1 = rng.randrange(key.n), rng.randrange(key.n)
        c = rng.randrange(2, 1000)
        assert egl_malicious_receiver(m0, m1, c, key, rng) == (m0 - c * m1) % key.n


def test_simplest_ot_correct_for_both_choices() -> None:
    rng = random.Random(2015)
    for grp in (SMALL_GROUP, TOY_GROUP):
        for _ in range(100):
            m0 = rng.getrandbits(256).to_bytes(32, "big")
            m1 = rng.getrandbits(256).to_bytes(32, "big")
            for c in (0, 1):
                t = simplest_ot(m0, m1, c, grp, rng)
                assert t.output == (m1 if c else m0)
                assert t.output != (m0 if c else m1)


def test_simplest_ot_receiver_message_does_not_depend_on_choice() -> None:
    rng = random.Random(3)
    m = bytes(32)
    samples = {0: Counter(), 1: Counter()}
    for c in (0, 1):
        for _ in range(20000):
            samples[c][simplest_ot(m, m, c, SMALL_GROUP, rng).B % 16] += 1
    assert chi2_two_samples(samples[0], samples[1], list(range(16))) < 37.7


def test_simplest_ot_rejects_bad_group_element() -> None:
    bad = SMALL_GROUP.p - 1  # -1 has order 2, so it is not in the subgroup
    assert not SMALL_GROUP.contains(bad)
    assert not SMALL_GROUP.contains(0)
