# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wagners-algorithm/. The authors are listed in prov/ZKP16F.jsonl.

import hashlib
import itertools
import random

from wagners_algorithm import k_tree, wagner4


def hlist(tag: int, size: int, n: int) -> list[int]:
    """List number tag: the first n bits of SHA-256(tag || j) for j < size."""
    out = []
    for j in range(size):
        d = hashlib.sha256(bytes([tag]) + j.to_bytes(4, "big")).digest()
        out.append(int.from_bytes(d[:5], "big") >> (40 - n))
    return out


def test_four_lists_30_bits() -> None:
    n = 30
    lists = [hlist(i, 1 << 11, n) for i in range(4)]
    sols = wagner4(*lists, n)
    assert len(sols) >= 1
    for i1, i2, i3, i4 in sols:
        assert lists[0][i1] ^ lists[1][i2] ^ lists[2][i3] ^ lists[3][i4] == 0


def test_four_lists_36_bits_at_the_bound() -> None:
    # list size 2^12 = 2^(n/3): expect about one solution; take a few instances
    n = 36
    found = 0
    for seed in range(3):
        lists = [hlist(4 * seed + i, 1 << 12, n) for i in range(4)]
        for i1, i2, i3, i4 in wagner4(*lists, n):
            assert lists[0][i1] ^ lists[1][i2] ^ lists[2][i3] ^ lists[3][i4] == 0
            found += 1
    assert found >= 1


def test_eight_lists() -> None:
    n = 32  # t = 3: lists of 2^(32/4) = 2^8, take 2^9 to get several solutions
    lists = [hlist(40 + i, 1 << 9, n) for i in range(8)]
    sols = k_tree(lists, n)
    assert sols
    for ix in sols:
        acc = 0
        for lst, i in zip(lists, ix):
            acc ^= lst[i]
        assert acc == 0


def test_against_brute_force() -> None:
    rng = random.Random(2002)
    for _ in range(500):
        n = rng.randrange(3, 9)
        sizes = [rng.randrange(1, 7) for _ in range(4)]
        lists = [[rng.randrange(1 << n) for _ in range(s)] for s in sizes]
        ell = -(-n // 3)
        low = (1 << ell) - 1
        want = {
            ix
            for ix in itertools.product(*(range(s) for s in sizes))
            if lists[0][ix[0]] ^ lists[1][ix[1]] ^ lists[2][ix[2]] ^ lists[3][ix[3]] == 0
            and (lists[0][ix[0]] ^ lists[1][ix[1]]) & low == 0
        }
        got = wagner4(*lists, n)
        assert len(got) == len(set(got))
        assert set(got) == want
        assert set(k_tree(lists, n)) == want


def test_two_lists_is_plain_birthday() -> None:
    a, b = [1, 5, 9, 12], [9, 3, 12, 12]
    assert sorted(k_tree([a, b], 4)) == [(2, 0), (3, 2), (3, 3)]
