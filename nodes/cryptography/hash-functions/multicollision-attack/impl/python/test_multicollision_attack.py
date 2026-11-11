# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multicollision-attack/. The authors are listed in prov/04D162.jsonl.

import random

import multicollision_attack as mc
from multicollision_attack import concat_collision, joux_multicollision, md_hash, messages


def test_256_messages_one_digest() -> None:
    n, t = 24, 8
    pairs = joux_multicollision(t, n)
    msgs = messages(pairs)
    assert len(msgs) == 1 << t
    assert len({tuple(m) for m in msgs}) == 1 << t
    assert len({md_hash(m, n) for m in msgs}) == 1


def test_cost_is_t_birthday_searches() -> None:
    calls = 0
    real = mc.toy_compress

    def counted(h, b, n, salt=0):
        nonlocal calls
        calls += 1
        return real(h, b, n, salt)

    mc.toy_compress = counted
    try:
        n, t = 20, 10
        joux_multicollision(t, n)
    finally:
        mc.toy_compress = real
    # each block collision costs about 1.25 * 2^(n/2) = 1280 calls on average
    assert calls < 3 * t * (1 << (n // 2))


def test_concatenated_hash_collision() -> None:
    n1 = n2 = 20
    m1, m2, t = concat_collision(n1, n2)
    assert m1 != m2 and len(m1) == len(m2) == t
    assert md_hash(m1, n1, 1) == md_hash(m2, n1, 1)
    assert md_hash(m1, n2, 2) == md_hash(m2, n2, 2)


def test_concatenation_with_unequal_sizes() -> None:
    m1, m2, _ = concat_collision(16, 24, salt1=5, salt2=6)
    assert m1 != m2
    assert md_hash(m1, 16, 5) == md_hash(m2, 16, 5)
    assert md_hash(m1, 24, 6) == md_hash(m2, 24, 6)


def test_random_subsets_collide() -> None:
    rng = random.Random(4)
    pairs = joux_multicollision(16, 16, salt=3)
    want = md_hash([p[0] for p in pairs], 16, 3)
    for _ in range(500):
        m = [p[rng.randrange(2)] for p in pairs]
        assert md_hash(m, 16, 3) == want
