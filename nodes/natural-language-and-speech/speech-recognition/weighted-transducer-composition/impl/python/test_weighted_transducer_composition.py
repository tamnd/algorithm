# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-transducer-composition/. The authors are listed in prov/BWQJKE.jsonl.

import math
import random

from nlslog import LOG_COST, TROPICAL, Semiring
from weighted_transducer_composition import EPS, Wfst, compose, relation


def random_acyclic(rng: random.Random, n: int, labels_in, labels_out, p_arc: float = 0.5) -> Wfst:
    t = Wfst()
    for _ in range(n):
        t.add_state()
    for i in range(n):
        for j in range(i + 1, n):
            for _ in range(2):
                if rng.random() < p_arc:
                    t.add_arc(i, rng.choice(labels_in), rng.choice(labels_out), rng.randint(0, 6) * 0.5, j)
    t.set_final(n - 1, rng.randint(0, 3) * 0.5)
    if rng.random() < 0.5:
        t.set_final(rng.randrange(n - 1), rng.randint(0, 3) * 0.5)
    return t


def random_cyclic(rng: random.Random, n: int, labels_in, labels_out, m: int) -> Wfst:
    t = Wfst()
    for _ in range(n):
        t.add_state()
    for _ in range(m):
        t.add_arc(rng.randrange(n), rng.choice(labels_in), rng.choice(labels_out), rng.randint(0, 6) * 0.5, rng.randrange(n))
    t.set_final(rng.randrange(n), rng.randint(0, 3) * 0.5)
    return t


def brute_compose(r1, r2, sr: Semiring):
    out = {}
    for (x, y), w1 in r1.items():
        for (y2, z), w2 in r2.items():
            if y == y2:
                out[(x, z)] = sr.plus(out.get((x, z), sr.zero), sr.times(w1, w2))
    return out


def same(r1, r2, sr: Semiring, tol: float = 1e-9) -> bool:
    keys = set(r1) | set(r2)
    for k in keys:
        a, b = r1.get(k, sr.zero), r2.get(k, sr.zero)
        if a == b:
            continue
        if math.isinf(a) or math.isinf(b) or abs(a - b) > tol:
            return False
    return True


def one_arc(i, o, w=0.0) -> Wfst:
    t = Wfst()
    t.add_state()
    t.add_state()
    t.add_arc(0, i, o, w, 1)
    t.set_final(1)
    return t


def test_filter_counts_one_path():
    t1 = one_arc("a", EPS)
    t2 = one_arc(EPS, "c")
    key = (("a",), ("c",))
    for sr in (TROPICAL, LOG_COST):
        t, pairs = compose(t1, t2, sr)
        assert relation(t, sr)[key] == 0.0
        assert sorted(pairs) == [(0, 0, 0), (0, 1, 2), (1, 0, 1), (1, 1, 0)]
        assert t.num_arcs() == 3
    # Without the filter there are three paths: t1 first, t2 first, or both at once.
    t, _ = compose(t1, t2, LOG_COST, filter=False)
    assert abs(relation(t, LOG_COST)[key] - (-math.log(3))) < 1e-12
    t, _ = compose(t1, t2, TROPICAL, filter=False)
    assert relation(t, TROPICAL)[key] == 0.0


def test_random_acyclic_with_epsilons_matches_brute_force():
    rng = random.Random(7)
    for case in range(60):
        sr = LOG_COST if case % 2 else TROPICAL
        t1 = random_acyclic(rng, rng.randint(2, 5), ["a", "b", EPS], ["x", "y", EPS])
        t2 = random_acyclic(rng, rng.randint(2, 5), ["x", "y", EPS], ["u", "v", EPS])
        t, _ = compose(t1, t2, sr)
        assert same(relation(t, sr), brute_compose(relation(t1, sr), relation(t2, sr), sr), sr)


def test_no_filter_is_wrong_in_log_but_right_in_tropical():
    rng = random.Random(11)
    wrong = 0
    for _ in range(40):
        t1 = random_acyclic(rng, 4, ["a", "b"], ["x", EPS])
        t2 = random_acyclic(rng, 4, ["x", EPS], ["u", "v"])
        ref_t = brute_compose(relation(t1, TROPICAL), relation(t2, TROPICAL), TROPICAL)
        t, _ = compose(t1, t2, TROPICAL, filter=False)
        assert same(relation(t, TROPICAL), ref_t, TROPICAL)
        ref_l = brute_compose(relation(t1, LOG_COST), relation(t2, LOG_COST), LOG_COST)
        t, _ = compose(t1, t2, LOG_COST, filter=False)
        wrong += not same(relation(t, LOG_COST), ref_l, LOG_COST)
    assert wrong > 0


def test_epsilon_free_size_bound_and_cyclic_strings():
    rng = random.Random(3)
    for case in range(40):
        sr = LOG_COST if case % 2 else TROPICAL
        t1 = random_cyclic(rng, rng.randint(1, 4), ["a", "b"], ["x", "y"], rng.randint(1, 7))
        t2 = random_cyclic(rng, rng.randint(1, 4), ["x", "y"], ["u", "v"], rng.randint(1, 7))
        t, pairs = compose(t1, t2, sr)
        assert t.num_states() <= t1.num_states() * t2.num_states()
        assert t.num_arcs() <= t1.num_arcs() * t2.num_arcs()
        assert all(f == 0 for _, _, f in pairs)
        # Without epsilons a pair of strings of length k uses paths of exactly k arcs.
        got = relation(t, sr, max_arcs=4)
        ref = brute_compose(relation(t1, sr, max_arcs=4), relation(t2, sr, max_arcs=4), sr)
        assert same(got, ref, sr)


def test_associative():
    rng = random.Random(5)
    for _ in range(20):
        t1 = random_acyclic(rng, 3, ["a", "b"], ["x", EPS])
        t2 = random_acyclic(rng, 3, ["x", EPS], ["u", EPS])
        t3 = random_acyclic(rng, 3, ["u", EPS], ["z"])
        left, _ = compose(compose(t1, t2, LOG_COST)[0], t3, LOG_COST)
        right, _ = compose(t1, compose(t2, t3, LOG_COST)[0], LOG_COST)
        assert same(relation(left, LOG_COST), relation(right, LOG_COST), LOG_COST)


def test_no_match_gives_empty_relation():
    t, _ = compose(one_arc("a", "x", 1.0), one_arc("y", "b", 2.0))
    assert relation(t) == {}
    assert t.num_states() == 1 and t.num_arcs() == 0


def test_weights_add_on_a_match():
    t, _ = compose(one_arc("a", "x", 1.5), one_arc("x", "b", 2.0))
    assert relation(t) == {(("a",), ("b",)): 3.5}
