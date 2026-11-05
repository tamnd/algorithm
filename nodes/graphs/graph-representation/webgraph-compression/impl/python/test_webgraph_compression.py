# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/webgraph-compression/. The authors are listed in prov/763NVN.jsonl.

import random

from webgraph_compression import copy_blocks, decode, encode, gamma, nu, nu_inv, split_intervals

EXAMPLE = [
    [13, 15, 16, 17, 18, 19, 23, 24, 203],
    [15, 16, 17, 22, 23, 24, 315, 316, 317, 3041],
    [],
    [],
    [16, 17, 18, 19, 20, 21, 22, 23, 24, 203, 315, 1034],
]


def test_codes() -> None:
    assert [gamma(k) for k in range(4)] == ["1", "010", "011", "00100"]
    assert [nu(x) for x in (0, -1, 1, -2, 2)] == [0, 1, 2, 3, 4]
    assert all(nu_inv(nu(x)) == x for x in range(-50, 50))


def test_example_parts() -> None:
    assert copy_blocks(EXAMPLE[0], set(EXAMPLE[1])) == [0, 1, 3, 2, 2]
    assert split_intervals([22, 315, 316, 317, 3041], 3) == ([(315, 3)], [22, 3041])


def test_example_round_trip_and_size() -> None:
    bits = encode(EXAMPLE)
    assert decode(bits) == EXAMPLE
    plain = sum(len(a) for a in EXAMPLE) * 12  # 12 bits per successor
    assert len(bits) < plain


def test_edge_cases() -> None:
    assert decode(encode([])) == []
    assert decode(encode([[]])) == [[]]
    assert decode(encode([[0]])) == [[0]]
    same = [[1, 2, 5, 9]] * 4
    assert decode(encode(same)) == same
    assert decode(encode(same, window=0)) == same


def test_random_round_trip() -> None:
    rng = random.Random(1999)
    for _ in range(600):
        n = rng.randrange(0, 15)
        adj = []
        for x in range(n):
            base = rng.choice([x, rng.randrange(n)])
            lst = {max(0, base + rng.randrange(-3, 6)) for _ in range(rng.randrange(0, 8))}
            if adj and rng.random() < 0.5:
                lst |= set(rng.sample(adj[-1], len(adj[-1]) // 2))
            adj.append(sorted(y % max(n, 1) for y in lst))
            adj[-1] = sorted(set(adj[-1]))
        w, lm = rng.randrange(0, 4), rng.randrange(1, 4)
        assert decode(encode(adj, window=w, lmin=lm), lmin=lm) == adj
