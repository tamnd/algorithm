# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/benes-network-routing/. The authors are listed in prov/ZPDNJR.jsonl.

import itertools
import math
import random

from benes_network_routing import first_switches_straight, realizes, route, stage_count, switch_count


def test_all_permutations_of_4_and_8() -> None:
    for n in (2, 4, 8):
        for perm in itertools.permutations(range(n)):
            net = route(list(perm))
            assert realizes(net, list(perm))
            assert first_switches_straight(net)


def test_random_permutations_up_to_4096() -> None:
    rng = random.Random(1)
    for k in range(1, 13):
        n = 1 << k
        for _ in range(20 if n <= 256 else 3):
            perm = list(range(n))
            rng.shuffle(perm)
            net = route(perm)
            assert realizes(net, perm)
            assert switch_count(net) == n * k - n // 2
            assert first_switches_straight(net)


def test_counts() -> None:
    for k in range(1, 11):
        n = 1 << k
        assert stage_count(n) == 2 * k - 1
        # Waksman: one switch fewer in each subnetwork with N >= 4.
        waksman = (n * k - n // 2) - (n // 2 - 1)
        assert waksman == n * k - n + 1
        # Every rearrangeable network of 2 x 2 switches needs log2(N!) switches.
        assert n * k - n // 2 >= math.ceil(math.log2(math.factorial(n)))


def test_example_from_the_page() -> None:
    perm = [5, 7, 2, 4, 0, 6, 1, 3]
    net = route(perm)
    assert net[1] == [0, 0, 1, 0]
    assert net[4] == [1, 0, 1, 0]
    assert realizes(net, perm)
    assert realizes(net[2], [2, 1, 3, 0])  # the upper subnetwork
    assert realizes(net[3], [3, 2, 0, 1])  # the lower subnetwork
