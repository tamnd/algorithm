# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incompressibility-argument/. The authors are listed in prov/DZF65X.jsonl.

import itertools
import random
import zlib

from incompressibility_argument import (
    all_strings, count_shorter, is_injective, max_compressed_by, max_compressed_by_prefix_free,
    search_injection_into_shorter, shorter_strings,
)


def test_counts() -> None:
    for n in range(0, 12):
        assert len(all_strings(n)) == 2 ** n
        assert len(shorter_strings(n)) == count_shorter(n) == 2 ** n - 1


def test_no_injection_into_shorter_strings_exhaustive() -> None:
    # The search visits every partial injection: sum over i of 7!/(7 - i)! = 13700 for n = 3.
    expected_nodes = {1: 1 + 1, 2: 1 + 3 + 6 + 6, 3: 13700}
    for n in (1, 2, 3):
        found, nodes = search_injection_into_shorter(n)
        assert found is None
        assert nodes == expected_nodes[n]


def test_every_injective_map_into_short_strings_has_a_long_image() -> None:
    # Enumerate every injective map from {0,1}^n into the strings of length at most n.
    for n in (1, 2):
        sources = all_strings(n)
        targets = shorter_strings(n + 1)
        maps = 0
        for image in itertools.permutations(targets, len(sources)):
            maps += 1
            assert max(len(y) for y in image) >= n
            for c in range(1, n + 1):
                assert sum(len(y) <= n - c for y in image) <= max_compressed_by(n, c)
        assert maps == {1: 3 * 2, 2: 7 * 6 * 5 * 4}[n]


def test_fraction_bounds() -> None:
    for n in range(1, 30):
        for c in range(1, n + 1):
            assert max_compressed_by(n, c) < 2 ** (n - c + 1)
            assert max_compressed_by_prefix_free(n, c) / 2 ** n == 2.0 ** -c


def test_greedy_map_reaches_the_bound() -> None:
    # Send the strings, in some order, to the shortest strings first. Exactly 2^(n-c+1) - 1 get length <= n - c.
    for n in range(1, 10):
        targets = shorter_strings(n + 1)
        image = dict(zip(all_strings(n), targets))
        assert is_injective(image.__getitem__, all_strings(n))
        for c in range(1, n + 1):
            assert sum(len(y) <= n - c for y in image.values()) == max_compressed_by(n, c)


def test_prefix_free_bound_with_random_codes() -> None:
    # A prefix-free set has at most 2^m words of length <= m (Kraft), so the bound 2^(n-c) holds.
    rng = random.Random(1)
    for _ in range(200):
        leaves = [""]
        for _ in range(rng.randint(1, 40)):
            leaves.append(leaves.pop(rng.randrange(len(leaves))) + "0")
            leaves.append(leaves[-1][:-1] + "1")
        for m in range(0, 12):
            assert sum(len(w) <= m for w in leaves) <= 2 ** m


def test_zlib_expands_random_bytes() -> None:
    rng = random.Random(2)
    for size in (0, 1, 100, 1000, 10000):
        data = rng.randbytes(size)
        out = zlib.compress(data, 9)
        assert len(out) > len(data)
        assert zlib.decompress(out) == data


def test_zlib_shrinks_regular_input() -> None:
    data = b"\x00" * 10000
    assert len(zlib.compress(data, 9)) < 100
