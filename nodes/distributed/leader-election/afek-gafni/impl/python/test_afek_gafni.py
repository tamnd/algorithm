# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/afek-gafni/. The authors are listed in prov/51R5KB.jsonl.

import random

from afek_gafni import afek_gafni_sync, log2_ceil


def runs(max_n: int, per_n: int):
    for n in range(1, max_n + 1):
        for s in range(per_n):
            rng = random.Random(500 * n + s)
            ids = rng.sample(range(1, 20 * n + 20), n)
            initiators = rng.sample(range(n), rng.randint(1, n))
            yield n, ids, initiators, s


def test_largest_initiator_is_the_only_leader():
    for n, ids, initiators, s in runs(40, 25):
        res = afek_gafni_sync(n, ids, initiators, s)
        assert res["leaders"] == [max(initiators, key=lambda v: ids[v])]


def test_rounds_are_exact():
    for n, ids, initiators, s in runs(40, 10):
        res = afek_gafni_sync(n, ids, initiators, s)
        if n > 1:
            assert res["phases"] == log2_ceil(n)
            assert res["rounds"] == 4 * log2_ceil(n) + 1


def test_survivors_halve():
    for n, ids, initiators, s in runs(40, 25):
        res = afek_gafni_sync(n, ids, initiators, s)
        for i, alive in enumerate(res["survivors"]):
            if 2 ** (i + 1) <= n:
                assert alive * 2 ** (i + 1) <= n


def test_message_bound():
    for n, ids, initiators, s in runs(60, 10):
        res = afek_gafni_sync(n, ids, initiators, s)
        election = res["messages"] - res["counts"]["LEADER"]
        assert election <= 4 * n * log2_ceil(n)
        assert res["counts"]["LEADER"] == (n - 1 if n > 1 else 0)


def test_page_example():
    n = 8
    ids = [3, 7, 2, 8, 5, 1, 6, 4]
    # Cyclic ports: process v tries v + 1, v + 2, ... in this order.
    orig = random.Random.shuffle

    def cyclic(self, lst):
        v = (set(range(n)) - set(lst)).pop()
        lst[:] = sorted(lst, key=lambda w: (w - v) % n)

    random.Random.shuffle = cyclic
    try:
        res = afek_gafni_sync(n, ids)
    finally:
        random.Random.shuffle = orig
    assert res["leaders"] == [3]
    assert res["survivors"] == [3, 1, 1]
    assert res["counts"] == {"CAP": 18, "Q": 6, "ANS": 6, "ACC": 12, "REJ": 6, "LEADER": 7}
    assert res["rounds"] == 13


def test_larger_network():
    rng = random.Random(11)
    n = 1024
    ids = rng.sample(range(10**7), n)
    res = afek_gafni_sync(n, ids, None, 11)
    assert res["leaders"] == [max(range(n), key=lambda v: ids[v])]
    assert res["messages"] - (n - 1) <= 4 * n * 10
