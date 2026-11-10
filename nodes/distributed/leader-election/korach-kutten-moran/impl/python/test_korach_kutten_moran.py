# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/korach-kutten-moran/. The authors are listed in prov/KB0GBC.jsonl.

import random

from korach_kutten_moran import harmonic, kkm_complete


def runs(max_n: int, per_n: int):
    for n in range(1, max_n + 1):
        for s in range(per_n):
            rng = random.Random(1000 * n + s)
            ids = rng.sample(range(1, 50 * n + 50), n)
            k = rng.randint(1, n)
            initiators = rng.sample(range(n), k)
            yield n, ids, initiators, s


def test_exactly_one_leader():
    for n, ids, initiators, s in runs(16, 60):
        for sync in (False, True):
            res = kkm_complete(n, ids, initiators, s, sync)
            assert len(res["leaders"]) == 1


def test_leader_has_the_largest_final_pair():
    for n, ids, initiators, s in runs(14, 40):
        res = kkm_complete(n, ids, initiators, s)
        (leader,) = res["leaders"]
        best = max(res["levels"], key=lambda c: (res["levels"][c], ids[c]))
        assert leader == best
        assert res["levels"][leader] == n - 1


def test_levels_obey_the_disjoint_domains_bound():
    for n, ids, initiators, s in runs(16, 40):
        res = kkm_complete(n, ids, initiators, s)
        levels = list(res["levels"].values())
        for j in range(n):
            assert (j + 1) * sum(1 for lev in levels if lev >= j) <= n


def test_message_bound():
    for n, ids, initiators, s in runs(20, 30):
        for sync in (False, True):
            res = kkm_complete(n, ids, initiators, s, sync)
            assert res["messages"] <= 4 * n * harmonic(n)
            if sync:
                assert res["time"] <= res["messages"]


def test_one_initiator_uses_few_messages():
    rng = random.Random(7)
    for n in range(2, 30):
        ids = rng.sample(range(1000), n)
        res = kkm_complete(n, ids, [rng.randrange(n)], n)
        # One candidate: 2 messages per node, no queries are needed.
        assert res["messages"] == 2 * (n - 1)


def test_all_start_larger_network():
    rng = random.Random(3)
    n = 300
    ids = rng.sample(range(10**6), n)
    res = kkm_complete(n, ids, list(range(n)), 3)
    assert len(res["leaders"]) == 1
    assert res["messages"] <= 4 * n * harmonic(n)
