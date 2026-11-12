# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robson-bound/. The authors are listed in prov/71MSB3.jsonl.

import random

from robson_bound import (
    end,
    first_fit,
    game_min_heap,
    is_free,
    power_sizes,
    robson_power_of_two,
    segregated_policy,
    two_size_adversary,
    worst_heap,
)


def test_formula_values() -> None:
    assert robson_power_of_two(4, 2) == 5
    assert robson_power_of_two(8, 2) == 11
    assert robson_power_of_two(8, 4) == 13
    assert robson_power_of_two(8, 8) == 13
    assert robson_power_of_two(1024, 1024) == 1024 * 6 - 1023


def test_formula_matches_exact_game() -> None:
    for m, n in [(2, 2), (4, 2), (4, 4), (6, 2), (8, 2)]:
        assert game_min_heap(m, n) == robson_power_of_two(m, n)


def test_first_fit_worst_cases() -> None:
    assert worst_heap(4, 2, first_fit)[0] == 6
    assert worst_heap(6, 2, first_fit)[0] == 9
    assert worst_heap(8, 2, first_fit)[0] == 12
    assert worst_heap(8, 4, first_fit)[0] == 16
    size, path = worst_heap(4, 2, first_fit)
    assert size == 6 and path[-1] == ("alloc", 2, 4)


def test_segregated_worst_case_is_the_upper_bound() -> None:
    for m, n in [(4, 2), (4, 4), (8, 2)]:
        k = n.bit_length() - 1
        assert worst_heap(m, n, segregated_policy(m))[0] <= m * (k + 1)


def random_policy(rng: random.Random, window: int):
    def place(state, s):
        free = []
        p = 0
        while len(free) < window:
            if is_free(state, p, s):
                free.append(p)
            p += 1
        return rng.choice(free)

    return place


def test_adversary_beats_every_policy() -> None:
    rng = random.Random(7)
    for trial in range(500):
        m = rng.choice([4, 8, 12, 16])
        place = random_policy(rng, rng.randint(1, 6))
        assert two_size_adversary(place, m) >= 3 * m // 2 - 1
    for m in [4, 8, 12]:
        assert two_size_adversary(first_fit, m) >= 3 * m // 2 - 1
        assert two_size_adversary(segregated_policy(m), m) >= 3 * m // 2 - 1


def test_random_runs_stay_within_bounds() -> None:
    rng = random.Random(11)
    for trial in range(500):
        m = rng.choice([4, 8, 16])
        n = rng.choice([s for s in [2, 4, 8] if m % s == 0])
        seg = segregated_policy(m)
        k = n.bit_length() - 1
        a = b = ()
        for _ in range(40):
            live = sum(s for _, s in a)
            s = rng.choice(power_sizes(n))
            if a and (live + s > m or rng.random() < 0.4):
                i = rng.randrange(len(a))
                a = a[:i] + a[i + 1:]
                b = b[:i] + b[i + 1:]
                continue
            p, q = first_fit(a, s), seg(b, s)
            assert is_free(a, p, s) and is_free(b, q, s)
            a = a + ((p, s),)
            b = b + ((q, s),)
            assert end(b) <= m * (k + 1)
