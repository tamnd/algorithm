# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/second-preimage-finding/. The authors are listed in prov/033D0B.jsonl.

import random

from second_preimage_finding import (
    ToyMD,
    brute_force_second_preimage,
    expand,
    expandable_message,
    kelsey_schneier,
)


def test_brute_force_16_bits() -> None:
    md = ToyMD(16)
    msg = [0x12345678, 0x9ABCDEF0]
    sp = brute_force_second_preimage(md, msg)
    assert sp != msg and md.digest(sp) == md.digest(msg)


def test_expandable_message_every_length() -> None:
    md = ToyMD(20)
    k = 5
    pieces, h_end = expandable_message(md, md.iv, k)
    for length in range(k, k + (1 << k)):
        m = expand(pieces, length)
        assert len(m) == length
        assert md.chaining_values(m)[-1] == h_end


def test_kelsey_schneier_24_bits() -> None:
    rng = random.Random(2005)
    n, k = 24, 10
    md = ToyMD(n)
    target = [rng.getrandbits(32) for _ in range(1 << k)]
    md.calls = 0
    sp = kelsey_schneier(md, target, k)
    assert sp != target
    assert len(sp) == len(target)
    assert md.digest(sp) == md.digest(target)
    # cost near k 2^(n/2+1) + 2^(n-k+1) = 81920 + 32768, far below 2^24
    assert md.calls < 4 * (k * (1 << (n // 2 + 1)) + (1 << (n - k + 1)))


def test_short_target_uses_small_k() -> None:
    rng = random.Random(1)
    md = ToyMD(18)
    target = [rng.getrandbits(32) for _ in range(40)]
    sp = kelsey_schneier(md, target, 5)
    assert sp != target and md.digest(sp) == md.digest(target)
