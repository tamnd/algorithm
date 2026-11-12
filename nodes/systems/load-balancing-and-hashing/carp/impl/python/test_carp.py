# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/carp/. The authors are listed in prov/VTZKC2.jsonl.

import random
from collections import Counter

from carp import Carp, combined_hash, exact_shares, member_hash, multipliers, rotl, url_hash


def urls(rng: random.Random, n: int) -> list[str]:
    return ["http://www.example.com/%016x" % rng.getrandbits(64) for _ in range(n)]


def test_hash_basics():
    assert rotl(1, 19) == 1 << 19
    assert rotl(1 << 31, 21) == 1 << 20
    assert url_hash("") == 0
    assert url_hash("a") == 97
    # "ab": h = 97, then 97 + rotl(97, 19) + 98
    assert url_hash("ab") == (97 + (97 << 19) + 98) & 0xFFFFFFFF
    h = 97
    h = (h + h * 0x62531965) & 0xFFFFFFFF
    assert member_hash("a") == rotl(h, 21)


def test_route_is_the_highest_score():
    rng = random.Random(1)
    names = ["cache-a", "cache-b", "cache-c"]
    c = Carp(names, [0.2, 0.3, 0.5])
    for u in urls(rng, 300):
        scores = [combined_hash(url_hash(u), member_hash(m)) * x for m, x in zip(names, c.x)]
        assert c.route(u) == names[scores.index(max(scores))]


def test_multipliers_give_the_load_factors_exactly():
    assert multipliers([0.25] * 4) == [1.0] * 4
    for loads in [[0.1, 0.2, 0.3, 0.4], [0.5, 0.25, 0.25], [0.05, 0.95], [0.4, 0.1, 0.1, 0.3, 0.1]]:
        sh = exact_shares(multipliers(loads))
        for s, p in zip(sh, loads):
            assert abs(s - p) < 1e-9


def test_simulated_shares_follow_the_load_factors():
    rng = random.Random(2)
    us = urls(rng, 40000)
    for names in [["cache-a", "cache-b", "cache-c", "cache-d"], ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4"]]:
        for loads in [[0.25] * 4, [0.1, 0.2, 0.3, 0.4]]:
            c = Carp(names, loads)
            cnt = Counter(c.route(u) for u in us)
            for m, p in zip(names, loads):
                assert abs(cnt[m] - p * len(us)) < 0.03 * len(us)


def test_similar_member_names_can_give_uneven_shares():
    rng = random.Random(2)
    us = urls(rng, 40000)
    names = ["proxy%d.example.com" % i for i in range(1, 5)]
    cnt = Counter(Carp(names).route(u) for u in us)
    assert max(cnt.values()) / min(cnt.values()) > 1.3


def test_equal_weights_move_only_the_keys_of_a_changed_member():
    rng = random.Random(3)
    us = urls(rng, 5000)
    names = ["cache-a", "cache-b", "cache-c", "cache-d"]
    full = Carp(names)
    less = Carp(names[:2] + names[3:])
    for u in us:
        a, b = full.route(u), less.route(u)
        if a != "cache-c":
            assert a == b
        else:
            assert b != "cache-c"


def test_unequal_weights_move_keys_between_other_members():
    rng = random.Random(4)
    us = urls(rng, 20000)
    names = ["cache-a", "cache-b", "cache-c", "cache-d"]
    full = Carp(names, [0.1, 0.2, 0.3, 0.4])
    less = Carp(names[:3], [1 / 6, 2 / 6, 3 / 6])
    between = sum(1 for u in us if full.route(u) != "cache-d" and full.route(u) != less.route(u))
    assert between > 0
