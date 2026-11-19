# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/confusion-network/. The authors are listed in prov/Q6R3VD.jsonl.

import itertools
import math
import random

import pytest

from confusion_network import EPS, Lattice, build, edit_distance, word_similarity

WORDS = ["a", "an", "and", "the", "then", "in"]


def random_lattice(rng: random.Random) -> Lattice:
    """A start node at time 0, a final node at time T, and middle nodes at random times."""
    T = rng.randint(3, 7)
    lat = Lattice()
    lat.add_node(0)
    end = lat.add_node(T)
    mids = [lat.add_node(rng.randint(1, T - 1)) for _ in range(rng.randint(1, 5))]
    lat.final = {end}

    def arc(u: int, v: int) -> None:
        span = lat.times[v] - lat.times[u]
        lat.add_arc(u, v, rng.choice(WORDS), -rng.uniform(0, 3) * span, -rng.uniform(0, 3))

    m = rng.choice(mids)
    arc(0, m)
    arc(m, end)
    nodes = list(range(len(lat.times)))
    for _ in range(rng.randint(2, 9)):
        u, v = rng.choice(nodes), rng.choice(nodes)
        if lat.times[u] < lat.times[v]:
            arc(u, v)
    return lat


def path_posteriors(lat: Lattice, lw: float):
    paths = list(lat.paths())
    logp = [sum(lat.score(k, lw) for k in p) / lw for p in paths]
    m = max(logp)
    z = m + math.log(sum(math.exp(x - m) for x in logp))
    return paths, [math.exp(x - z) for x in logp]


def page_example() -> Lattice:
    lat = Lattice()
    for t in [0, 30, 30, 60]:
        lat.add_node(t)
    lat.add_arc(0, 1, "a", -10.0, math.log(0.6))
    lat.add_arc(0, 2, "x", -9.0, math.log(0.4))
    lat.add_arc(1, 3, "b", -12.0, math.log(0.5))
    lat.add_arc(1, 3, "c", -10.0, math.log(0.5))
    lat.add_arc(2, 3, "b", -12.0, math.log(0.9))
    lat.final = {3}
    return lat


def test_page_example():
    cn = build(page_example(), lm_weight=10.0)
    assert len(cn.slots) == 2
    assert sorted(cn.slots[0]) == ["a", "x"] and sorted(cn.slots[1]) == ["b", "c"]
    assert cn.slots[0]["a"] == pytest.approx(0.6262, abs=1e-4)
    assert cn.slots[1]["b"] == pytest.approx(0.6557, abs=1e-4)
    assert all(e < 1e-12 for e in cn.eps)
    # The consensus "a b" differs from the best path "x b" and has fewer expected errors.
    assert cn.consensus() == ["a", "b"]
    assert cn.expected_errors(["a", "b"]) == pytest.approx(0.7181, abs=1e-4)
    assert cn.expected_errors(["x", "b"]) == pytest.approx(0.9705, abs=1e-4)
    assert cn.num_paths() == 4


def test_every_lattice_path_is_a_network_path_and_the_order_is_kept():
    rng = random.Random(51)
    for _ in range(60):
        lat = random_lattice(rng)
        cn = build(lat, lm_weight=rng.choice([1.0, 3.0]))
        for p in lat.paths():
            slots = [cn.slot_of[k] for k in p]
            assert slots == sorted(slots) and len(set(slots)) == len(slots)
            assert all(lat.arcs[k][2] in cn.slots[cn.slot_of[k]] for k in p)
        kept = sorted(cn.slot_of)
        for e in kept:
            for f in kept:
                if e != f and lat.arcs[e][1] == lat.arcs[f][0]:
                    assert cn.slot_of[e] < cn.slot_of[f]


def test_slot_posteriors_match_enumeration():
    rng = random.Random(52)
    for _ in range(60):
        lat = random_lattice(rng)
        lw = rng.choice([1.0, 3.0])
        cn = build(lat, lm_weight=lw)
        paths, prob = path_posteriors(lat, lw)
        n = len(cn.slots)
        expect = [dict() for _ in range(n)]
        missing = [0.0] * n
        for p, pr in zip(paths, prob):
            hit = set()
            for k in p:
                i = cn.slot_of[k]
                w = lat.arcs[k][2]
                expect[i][w] = expect[i].get(w, 0.0) + pr
                hit.add(i)
            for i in range(n):
                if i not in hit:
                    missing[i] += pr
        for i in range(n):
            assert set(expect[i]) == set(cn.slots[i])
            assert all(abs(expect[i][w] - cn.slots[i][w]) < 1e-9 for w in expect[i])
            assert sum(cn.slots[i].values()) <= 1.0 + 1e-9
            assert abs(cn.eps[i] - missing[i]) < 1e-9


def test_consensus_minimizes_slot_errors_which_bound_word_errors():
    rng = random.Random(53)
    for _ in range(40):
        lat = random_lattice(rng)
        cn = build(lat, lm_weight=2.0)
        best = cn.consensus_slots()
        choices = [sorted(s) + ([EPS] if e > 0.0 else []) for s, e in zip(cn.slots, cn.eps)]
        if cn.num_paths() <= 5000:
            low = min(cn.expected_errors(list(c)) for c in itertools.product(*choices))
            assert cn.expected_errors(best) <= low + 1e-12
        hyp = cn.consensus()
        for p in lat.paths():
            ref = [EPS] * len(cn.slots)
            for k in p:
                ref[cn.slot_of[k]] = lat.arcs[k][2]
            slot_errors = sum(1 for x, y in zip(best, ref) if x != y)
            assert slot_errors >= edit_distance(hyp, [w for w in ref if w != EPS])


def test_pruning_drops_unlikely_arcs():
    rng = random.Random(54)
    for _ in range(30):
        lat = random_lattice(rng)
        gamma = [math.exp(g) if g > float("-inf") else 0.0 for g in lat.log_posteriors(2.0)]
        cn = build(lat, lm_weight=2.0, theta=0.1)
        assert set(cn.slot_of) == {k for k, g in enumerate(gamma) if g > 0.1}
        assert all(e >= 0.0 for e in cn.eps)


def test_similarity_and_errors():
    assert word_similarity("then", "then") == 1.0
    assert word_similarity("the", "then") == pytest.approx(1 - 1 / 7)
    assert edit_distance(["a", "b"], ["b"]) == 1
    lat = Lattice()
    lat.add_node(0)
    lat.add_node(0)
    with pytest.raises(ValueError):
        lat.add_arc(0, 1, "a", 0.0, 0.0)
    lat2 = Lattice()
    lat2.add_node(0)
    lat2.add_node(1)
    lat2.final = {1}
    with pytest.raises(ValueError):
        build(lat2)
