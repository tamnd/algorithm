# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tendermint/. The authors are listed in prov/66KH53.jsonl.

import itertools

from tendermint import STRATEGIES, Net, Proc, check, run


def test_three_message_delays_with_a_correct_proposer():
    res = run(4, 1, set(), "silent", heights=1, gst=0, delta=1)
    assert check(res) == []
    assert res["time"] == 3  # proposal, prevote, precommit
    assert all(d == {0: "v0.0"} for d in res["decisions"].values())


def test_safety_and_liveness_all_traitor_sets():
    for n, f, seeds in ((4, 1, range(4)), (7, 2, range(1))):
        for gst in (60, 300):
            for faulty in itertools.combinations(range(n), f):
                for strat in STRATEGIES:
                    for seed in seeds:
                        res = run(n, f, set(faulty), strat, gst=gst, seed=seed)
                        assert check(res) == [], (n, gst, faulty, strat, seed)


def lock_attack(lock):
    """A hand-made asynchronous schedule with n = 4 and p1 Byzantine. In round
    0, p0 decides v; p2 is locked on v; p3 saw no polka. In round 1 the
    faulty proposer p1 proposes a fresh w. Messages that are not delivered
    here are delayed past the end of the trace, which asynchrony allows."""
    net = Net(4, 10**9, 1, 1, 0)
    P = [Proc(i, 4, 1, net, byz=("fresh" if i == 1 else None), lock=lock) for i in range(4)]
    net.honest_ids = {0, 2, 3}
    for i in (0, 2, 3):
        P[i].start_round(0)
        P[i].evaluate()
    v, w = "v0.0", "w"

    def tok(i, *content):
        t = ("sig", i, content)
        if i == 1:
            net.tokens.add(t)  # the faulty process signs what it likes
        assert t in net.tokens  # an honest process really sent it
        return t

    def give(dst, *toks):
        for t in toks:
            P[dst].receive(t[1], t)

    def wait(i, until):
        net.now = until
        P[i].tick()

    give(2, tok(0, "PROPOSAL", 0, 0, v, -1))
    give(0, tok(2, "PREVOTE", 0, 0, v), tok(1, "PREVOTE", 0, 0, v))  # p0 sees a polka
    give(2, tok(0, "PREVOTE", 0, 0, v), tok(1, "PREVOTE", 0, 0, v))  # p2 locks on v
    give(0, tok(2, "PRECOMMIT", 0, 0, v), tok(1, "PRECOMMIT", 0, 0, v))
    assert P[0].decision == {0: v}
    assert (P[2].locked_value, P[2].locked_round) == (v, 0)
    wait(3, 12)  # p3 never got the proposal: prevote nil
    give(3, tok(1, "PREVOTE", 0, 0, None), tok(0, "PREVOTE", 0, 0, v))
    wait(3, 24)  # no polka at p3: precommit nil
    give(2, tok(3, "PRECOMMIT", 0, 0, None), tok(1, "PRECOMMIT", 0, 0, None))
    wait(2, 36)  # p2 goes to round 1
    give(3, tok(2, "PRECOMMIT", 0, 0, v), tok(1, "PRECOMMIT", 0, 0, None))
    wait(3, 48)  # p3 goes to round 1
    prop = tok(1, "PROPOSAL", 0, 1, w, -1)
    give(2, prop)
    give(3, prop)
    x2 = w if not lock else None  # the lock makes p2 prevote nil
    give(2, tok(1, "PREVOTE", 0, 1, w), tok(3, "PREVOTE", 0, 1, w))
    give(3, tok(1, "PREVOTE", 0, 1, w), tok(2, "PREVOTE", 0, 1, x2))
    if not lock:
        give(2, tok(1, "PRECOMMIT", 0, 1, w), tok(3, "PRECOMMIT", 0, 1, w))
        give(3, tok(1, "PRECOMMIT", 0, 1, w), tok(2, "PRECOMMIT", 0, 1, w))
    return {i: dict(P[i].decision) for i in (0, 2, 3)}


def test_lock_attack_replayed():
    assert lock_attack(False) == {0: {0: "v0.0"}, 2: {0: "w"}, 3: {0: "w"}}
    assert lock_attack(True) == {0: {0: "v0.0"}, 2: {}, 3: {}}
