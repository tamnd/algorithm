# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hotstuff/. The authors are listed in prov/XGV05H.jsonl.

import itertools

import hotstuff
from hotstuff import GENESIS, STRATEGIES, Net, check, run


def test_linear_messages_per_view():
    # Per view: n - 1 NEW-VIEW, 4 leader broadcasts and 3 vote phases to the
    # leader, each n - 1 messages. One more NEW-VIEW round after the last view.
    for n, f in ((4, 1), (7, 2), (10, 3)):
        res = run(n, f, set(), "silent", requests=4, gst=0, seed=0)
        assert check(res) == []
        assert res["sent"] == {"normal": 8 * (n - 1) * 4 + (n - 1), "timeout": 0}


def test_safety_and_liveness_all_traitor_sets():
    for n, f, seeds in ((4, 1, range(6)), (7, 2, range(2))):
        for gst in (60, 300):
            for faulty in itertools.combinations(range(n), f):
                for strat in STRATEGIES:
                    for seed in seeds:
                        res = run(n, f, set(faulty), strat, gst=gst, seed=seed)
                        assert check(res) == [], (n, gst, faulty, strat, seed)


def test_fork_attack_breaks_safety_without_the_lock(monkeypatch):
    # The faulty leader proposes a fork from genesis. With safeNode always
    # true, honest replicas vote for it and a later leader extends it.
    monkeypatch.setattr(hotstuff.Replica, "safe_node", lambda self, node, qc: True)
    hits = 0
    for faulty in range(4):
        for seed in range(3):
            res = run(4, 1, {faulty}, "fork", seed=seed, horizon=3000)
            hits += "safety" in check(res)
    assert hits > 0


def test_quorum_certificates_are_threshold_tokens():
    net = Net(4, 1, 0, 1, 1, 0)
    c = ("prepare", 1, ("r0", GENESIS))
    shares = [net.partial(i, c) for i in range(3)]
    assert net.combine(shares[:2]) is None  # n - f = 3 shares are needed
    assert net.combine(shares + [net.partial(3, ("prepare", 1, ("x", GENESIS)))]) is None
    assert net.combine([shares[0], shares[0], shares[1]]) is None  # one signer twice
    assert net.combine(shares[:2] + [("ps", 3, c)]) is None  # a forged share
    qc = net.combine(shares)
    assert net.ok(qc) and qc == ("qc", c)
