# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pbft/. The authors are listed in prov/VDRRCB.jsonl.

import itertools

from pbft import STRATEGIES, Net, check, run


def test_normal_case_message_count():
    # Per request: n - 1 pre-prepares, (n - 1)^2 prepares, n(n - 1) commits.
    # One checkpoint after 4 requests: n(n - 1) messages.
    for n, f in ((4, 1), (7, 2), (10, 3)):
        res = run(n, f, set(), "silent", requests=4, gst=0, seed=0)
        assert check(res, f) == []
        assert res["sent"] == {"normal": 4 * 2 * n * (n - 1) + n * (n - 1), "view": 0}
        assert all(len(log) == 4 for log in res["logs"].values())


def test_silent_primary_causes_one_view_change():
    # n - 1 honest VIEW-CHANGE broadcasts and one NEW-VIEW to n - 1 replicas.
    for n, f in ((4, 1), (7, 2), (10, 3)):
        res = run(n, f, {0}, "silent", requests=4, gst=0, seed=0)
        assert check(res, f) == []
        assert set(res["views"].values()) == {1}
        assert res["sent"]["view"] == (n - 1) ** 2 + (n - 1)


def test_safety_and_liveness_all_traitor_sets():
    cases = [(4, 1, s) for s in range(4)] + [(7, 2, 0)]
    for n, f, seed in cases:
        for faulty in itertools.combinations(range(n), f):
            for strat in STRATEGIES:
                res = run(n, f, set(faulty), strat, seed=seed)
                assert check(res, f) == [], (n, faulty, strat, seed)
                assert res["done_at"] is not None


def test_commits_after_late_gst():
    for seed in range(3):
        for strat in STRATEGIES:
            res = run(4, 1, {seed % 4}, strat, gst=300, seed=seed, horizon=6000)
            assert check(res, 1) == []
            assert res["done_at"] is not None


def test_signatures_are_unforgeable_tokens():
    net = Net(4, 0, 1, 1, 0)
    real = net.sign(1, ("P", 0, 1, "r0", 1))
    assert net.ok(real)
    assert not net.ok(("sig", 2, ("P", 0, 1, "r0", 2)))  # never signed by 2
    assert not net.ok(("sig", 1, ("P", 0, 1, "r1", 1)))  # changed content
