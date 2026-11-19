# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phonetic-decision-tree-state-tying/. The authors are listed in prov/7CSFNE.jsonl.

import math
import random

import pytest

from phonetic_decision_tree_state_tying import (
    State,
    best_question,
    build_tree,
    classify,
    log_likelihood,
    merge_leaves,
    pool,
    stats_from_frames,
    tie,
)

VOWELS = {"aa", "ae", "iy", "uw"}
NASALS = {"m", "n"}
STOPS = {"p", "t", "k"}
PHONES = sorted(VOWELS | NASALS | STOPS)
QUESTIONS = [
    ("L_vowel", "L", VOWELS),
    ("L_nasal", "L", NASALS),
    ("L_stop", "L", STOPS),
    ("R_vowel", "R", VOWELS),
    ("R_nasal", "R", NASALS),
    ("R_stop", "R", STOPS),
] + [("L_" + p, "L", {p}) for p in PHONES] + [("R_" + p, "R", {p}) for p in PHONES]


def make_states(rng, mean_of, n_states=24, d=2, sd=0.5, contexts=None):
    if contexts is None:
        contexts = rng.sample([(l, r) for l in PHONES for r in PHONES], n_states)
    states, frames = [], {}
    for l, r in contexts:
        mu = mean_of(l, r)
        fr = [[rng.gauss(mu[k], sd) for k in range(d)] for _ in range(rng.randint(30, 60))]
        name = l + "-ae+" + r
        N, mean, var = stats_from_frames(fr)
        states.append(State(name, l, r, N, mean, var))
        frames[name] = fr
    return states, frames


def gauss_loglik(frames):
    """The log likelihood of the frames under their own ML diagonal Gaussian, summed frame by frame."""
    _, mean, var = stats_from_frames(frames)
    return math.fsum(
        -0.5 * (math.log(2 * math.pi * var[k]) + (f[k] - mean[k]) ** 2 / var[k]) for f in frames for k in range(len(f))
    )


def planted(l, r):
    return [3.0 if l in VOWELS else 0.0, 1.5 if r in NASALS else 0.0]


def test_pooled_statistics_match_the_frames():
    rng = random.Random(1)
    states, frames = make_states(rng, planted)
    for _ in range(20):
        sub = rng.sample(states, rng.randint(1, 8))
        N, mean, var = pool(sub)
        N2, mean2, var2 = stats_from_frames([f for s in sub for f in frames[s.name]])
        assert N == N2
        assert mean == pytest.approx(mean2, abs=1e-9)
        assert var == pytest.approx(var2, abs=1e-9)
        # the closed form of L(S) equals the sum of the Gaussian log densities of the frames
        assert log_likelihood(sub) == pytest.approx(gauss_loglik([f for s in sub for f in frames[s.name]]), abs=1e-6)


def test_best_question_against_brute_force_from_frames():
    rng = random.Random(2)
    for trial in range(15):
        states, frames = make_states(random.Random(100 + trial), planted, n_states=rng.randint(4, 16))
        all_frames = [f for s in states for f in frames[s.name]]
        base = gauss_loglik(all_frames)
        brute = []
        for q in QUESTIONS:
            yes = [f for s in states if (s.left if q[1] == "L" else s.right) in q[2] for f in frames[s.name]]
            no = [f for s in states if (s.left if q[1] == "L" else s.right) not in q[2] for f in frames[s.name]]
            if len(yes) >= 40 and len(no) >= 40:
                brute.append((gauss_loglik(yes) + gauss_loglik(no) - base, q[0]))
        got = best_question(states, QUESTIONS, min_occ=40)
        if not brute:
            assert got is None
            continue
        g, name = max(brute, key=lambda t: t[0])
        assert got[0] == pytest.approx(g, abs=1e-6)
        assert got[1][0] == name


def test_gain_is_never_negative():
    rng = random.Random(3)
    states, _ = make_states(rng, lambda l, r: [rng.uniform(-1, 1), rng.uniform(-1, 1)])
    for _ in range(200):
        sub = rng.sample(states, rng.randint(2, 12))
        q = rng.choice(QUESTIONS)
        yes = [s for s in sub if (s.left if q[1] == "L" else s.right) in q[2]]
        no = [s for s in sub if s not in yes]
        if yes and no:
            assert log_likelihood(yes) + log_likelihood(no) - log_likelihood(sub) >= -1e-9


def test_planted_tree():
    states, _ = make_states(random.Random(4), planted, n_states=40)
    root, leaves = build_tree(states, QUESTIONS, threshold=50.0, min_occ=100)
    assert root.question[0] == "L_vowel"
    assert {root.yes.question[0], root.no.question[0]} == {"R_nasal"}
    assert len(leaves) == 4
    # the likelihood of the leaves is the root likelihood plus the gains of the splits
    total = sum(log_likelihood(leaf.states) for leaf in leaves)
    gains = root.gain + root.yes.gain + root.no.gain
    assert total == pytest.approx(log_likelihood(states) + gains, abs=1e-6)
    # each leaf is pure in the two planted features
    for leaf in leaves:
        assert len({(s.left in VOWELS, s.right in NASALS) for s in leaf.states}) == 1


def test_unseen_triphone_goes_to_the_right_leaf():
    states, _ = make_states(random.Random(4), planted, n_states=40)
    root, _ = build_tree(states, QUESTIONS, threshold=50.0, min_occ=100)
    seen = {(s.left, s.right) for s in states}
    unseen = [(l, r) for l in PHONES for r in PHONES if (l, r) not in seen]
    assert unseen
    for l, r in unseen:
        leaf = classify(root, l, r)
        assert all((s.left in VOWELS, s.right in NASALS) == (l in VOWELS, r in NASALS) for s in leaf.states)


def test_min_occupancy_blocks_small_leaves():
    states, _ = make_states(random.Random(5), planted, n_states=10)
    big = best_question(states, QUESTIONS, min_occ=10 ** 6)
    assert big is None
    root, leaves = build_tree(states, QUESTIONS, threshold=0.0, min_occ=100)
    assert all(sum(s.occ for s in leaf.states) >= 100 for leaf in leaves)


def test_greedy_misses_an_xor_context():
    # The mean depends on (left is a vowel) xor (right is a nasal), and every
    # left context occurs with two nasals and two other phones on the right. No
    # single question changes the mean, so a greedy tree with a high threshold
    # stops at the root, while the two-level tree that it cannot see gains a lot.
    def xor(l, r):
        return [2.0 if (l in VOWELS) != (r in NASALS) else 0.0, 0.0]

    contexts = [(l, r) for l in ("aa", "iy", "p", "t") for r in ("m", "n", "k", "uw")]
    states, _ = make_states(random.Random(6), xor, contexts=contexts)
    first = best_question(states, QUESTIONS, min_occ=100)
    yes, no = [s for s in states if s.left in VOWELS], [s for s in states if s.left not in VOWELS]
    two_level = sum(
        log_likelihood([s for s in side if (s.right in NASALS) == flag]) for side in (yes, no) for flag in (True, False)
    ) - log_likelihood(states)
    assert two_level > 4 * first[0]
    root, leaves = build_tree(states, QUESTIONS, threshold=first[0] + 1.0, min_occ=100)
    assert len(leaves) == 1


def test_merge_joins_leaves_from_different_branches():
    rng = random.Random(7)
    means = [[0.0, 0.0], [3.0, 0.0], [0.0, 0.0], [3.0, 0.0]]
    clusters = []
    for c, mu in enumerate(means):
        cl = []
        for k in range(3):
            fr = [[rng.gauss(mu[0], 0.5), rng.gauss(mu[1], 0.5)] for _ in range(50)]
            N, mean, var = stats_from_frames(fr)
            cl.append(State("c%d_%d" % (c, k), "x", "y", N, mean, var))
        clusters.append(cl)
    merged = merge_leaves(clusters, threshold=30.0)
    groups = sorted(sorted({s.name[:2] for s in cl}) for cl in merged)
    assert groups == [["c0", "c2"], ["c1", "c3"]]


def test_tie_maps_every_state():
    states, _ = make_states(random.Random(8), planted, n_states=30)
    root, index = tie(states, QUESTIONS, threshold=50.0, min_occ=100)
    assert set(index) == {s.name for s in states}
    assert len(set(index.values())) == 4
