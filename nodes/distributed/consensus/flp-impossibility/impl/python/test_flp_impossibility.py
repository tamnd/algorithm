# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flp-impossibility/. The authors are listed in prov/1ADEFK.jsonl.

from itertools import product

from flp_impossibility import (
    blocked,
    decisions,
    events,
    follow_p0,
    initial,
    lemma2,
    majority_of_all,
    majority_of_some,
    reachable,
    replay,
    search,
    step,
    valence,
)

N = 3
INPUTS = list(product([0, 1], repeat=N))


def test_waiting_for_n_minus_1_breaks_agreement() -> None:
    res = search((1, 1, 0), majority_of_some)
    assert res is not None and res[0] == "agreement"
    evs = res[1]
    # The bad schedule needs no crash: a slow message is enough.
    assert not any(e[0] == "crash" for e in evs)
    assert decisions(replay((1, 1, 0), majority_of_some, evs)) == {0, 1}


def test_waiting_for_n_minus_1_has_a_bivalent_start() -> None:
    kind, j = lemma2(N, majority_of_some)
    assert kind == "bivalent"
    assert valence(initial(tuple(1 if i < j else 0 for i in range(N))), majority_of_some) == {0, 1}


def test_safe_protocols_never_disagree() -> None:
    for rule in (majority_of_all, follow_p0):
        for inputs in INPUTS:
            for c in reachable(inputs, rule):
                assert len(decisions(c)) <= 1


def test_safe_protocols_decide_without_a_crash() -> None:
    # Every failure-free run that has no work left has all processes decided.
    for rule in (majority_of_all, follow_p0):
        for inputs in INPUTS:
            for c in reachable(inputs, rule, max_crashes=0):
                if not events(c, 0):
                    assert all(s[3] is not None for s in c[0])
                    assert not blocked(c)


def test_one_crash_blocks_the_safe_protocols() -> None:
    for rule in (majority_of_all, follow_p0):
        for inputs in INPUTS:
            res = search(inputs, rule)
            assert res is not None and res[0] == "blocked"
            evs = res[1]
            assert sum(e[0] == "crash" for e in evs) == 1
            assert blocked(replay(inputs, rule, evs))


def test_a_crash_looks_like_a_delay() -> None:
    # Remove the crash from the blocking run: the rest is a prefix of a
    # failure-free run in which the same processes are undecided.
    for rule in (majority_of_all, follow_p0):
        evs = search((0, 1, 1), rule)[1]
        crash = next(e for e in evs if e[0] == "crash")
        c1 = replay((0, 1, 1), rule, evs)
        c0 = replay((0, 1, 1), rule, [e for e in evs if e != crash], max_crashes=0)
        p = crash[1]
        for q in range(N):
            if q != p:
                assert c0[0][q] == c1[0][q] and c0[0][q][3] is None


def test_crash_in_the_middle_of_a_broadcast() -> None:
    # p0 sends its value to p1, then crashes before it sends to p2.
    c = initial((1, 0, 0))
    c = step(c, ("send", 0), follow_p0)
    c = step(c, ("crash", 0), follow_p0)
    c = step(c, ("recv", (1, 0, 1)), follow_p0)
    for e in [("send", 1), ("send", 1), ("send", 2), ("send", 2)]:
        c = step(c, e, follow_p0)
    while events(c, 1):
        e = next(e for e in events(c, 1) if e[0] != "crash")
        c = step(c, e, follow_p0)
    assert c[0][0][3] == 1 and c[0][1][3] == 1 and c[0][2][3] is None
    assert blocked(c)


def test_lemma2_dichotomy_on_safe_protocols() -> None:
    # All initial configurations are univalent, so a silent process blocks.
    assert lemma2(N, follow_p0) == ("silent-run-undecided", 0)
    assert lemma2(N, majority_of_all) == ("silent-run-undecided", 1)


def test_commutativity_of_disjoint_steps() -> None:
    # Lemma 1 of FLP on one example: steps of different processes commute.
    for rule in (majority_of_some, majority_of_all, follow_p0):
        c = initial((1, 0, 1))
        c = step(c, ("send", 0), rule)
        c = step(c, ("send", 2), rule)
        e1, e2 = ("recv", (1, 0, 1)), ("send", 2)
        assert step(step(c, e1, rule), e2, rule) == step(step(c, e2, rule), e1, rule)
