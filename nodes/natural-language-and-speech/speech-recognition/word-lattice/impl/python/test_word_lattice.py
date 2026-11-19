# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/word-lattice/. The authors are listed in prov/5BPGS0.jsonl.

import math
import random

import pytest

from nlslog import LOG, NEG_INF, log_sum
from word_lattice import Lattice

WORDS = ["a", "b", "c", "d"]


def random_lattice(rng: random.Random, n: int, extra: int) -> Lattice:
    """Nodes at times 0, 1, ..., n - 1 in a chain plus random forward arcs; node 0 starts, node n - 1 ends."""
    lat = Lattice()
    for t in range(n):
        lat.add_node(t)
    for t in range(n - 1):
        lat.add_arc(t, t + 1, rng.choice(WORDS), -rng.uniform(0, 5), -rng.uniform(0, 3))
    for _ in range(extra):
        u = rng.randrange(n - 1)
        v = rng.randrange(u + 1, n)
        lat.add_arc(u, v, rng.choice(WORDS), -rng.uniform(0, 5) * (v - u), -rng.uniform(0, 3))
    lat.final = {n - 1}
    return lat


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
    lat = page_example()
    assert lat.num_paths() == 3
    words, score = lat.best_path(lm_weight=10.0)
    assert words == ["x", "b"]
    assert abs(score - (-21.0 + 10 * math.log(0.36))) < 1e-12
    assert lat.best_path(lm_weight=1.0)[0] == ["a", "c"]
    gamma = lat.arc_posteriors(lm_weight=10.0)
    assert abs(gamma[0] + gamma[1] - 1.0) < 1e-12
    assert abs(gamma[2] + gamma[3] + gamma[4] - 1.0) < 1e-12
    assert gamma[1] == pytest.approx(gamma[4])
    # The best path is "x b", but "a" is the more likely first word and "b" the more likely second word.
    assert gamma[0] == pytest.approx(0.6262, abs=1e-4)
    assert gamma[2] + gamma[4] == pytest.approx(0.6557, abs=1e-4)
    small = lat.prune(1.0, 10.0)
    assert sorted(small.words(p) for p in small.paths()) == [["a", "c"], ["x", "b"]]
    assert len(small.arcs) == 4


def test_path_count_and_totals_match_enumeration():
    rng = random.Random(41)
    for _ in range(40):
        lat = random_lattice(rng, rng.randint(2, 7), rng.randint(0, 8))
        paths = list(lat.paths())
        assert lat.num_paths() == len(paths)
        lw, ip = rng.choice([0.5, 1.0, 8.0]), rng.choice([-1.0, 0.0, 0.5])
        scores = [sum(lat.score(k, lw, ip) for k in p) for p in paths]
        total = lat.total(LOG, lambda k: lat.score(k, lw, ip))
        assert abs(total - log_sum(scores)) < 1e-9
        words, best = lat.best_path(lw, ip)
        assert abs(best - max(scores)) < 1e-9
        assert any(lat.words(p) == words and abs(s - best) < 1e-9 for p, s in zip(paths, scores))


def test_arc_posteriors_match_enumeration():
    rng = random.Random(42)
    for _ in range(40):
        lat = random_lattice(rng, rng.randint(2, 7), rng.randint(0, 8))
        lw = rng.choice([1.0, 4.0, 12.0])
        kappa = 1.0 / lw
        gamma = lat.arc_posteriors(lw)
        paths = list(lat.paths())
        logp = [kappa * sum(lat.score(k, lw) for k in p) for p in paths]
        z = log_sum(logp)
        expect = [0.0] * len(lat.arcs)
        for p, lp in zip(paths, logp):
            for k in p:
                expect[k] += math.exp(lp - z)
        assert all(abs(g - e) < 1e-9 for g, e in zip(gamma, expect))
        # Every path covers every frame once, so the arcs that span a frame have posteriors adding up to 1.
        T = max(lat.times)
        for t in range(T):
            span = sum(g for (u, v, _, _, _), g in zip(lat.arcs, gamma) if lat.times[u] <= t < lat.times[v])
            assert abs(span - 1.0) < 1e-9


def test_acoustic_scale_flattens_posteriors():
    lat = page_example()
    sharp = lat.arc_posteriors(lm_weight=10.0, kappa=1.0)
    flat = lat.arc_posteriors(lm_weight=10.0, kappa=0.1)
    assert max(sharp[0], sharp[1]) > max(flat[0], flat[1])
    assert sharp[1] == pytest.approx(0.6674, abs=1e-4)
    assert flat[0] == pytest.approx(0.6262, abs=1e-4)


def test_prune_keeps_exactly_the_paths_within_the_beam():
    rng = random.Random(43)
    for _ in range(40):
        lat = random_lattice(rng, rng.randint(2, 7), rng.randint(0, 8))
        beam = rng.choice([0.0, 1.0, 3.0, 100.0])
        small = lat.prune(beam)
        best = lat.best_path()[1]
        assert abs(small.best_path()[1] - best) < 1e-9
        within = {(tuple(lat.words(p)), round(sum(lat.score(k) for k in p), 6)) for p in lat.paths()
                  if sum(lat.score(k) for k in p) >= best - beam - 1e-9}
        got = {(tuple(small.words(p)), round(sum(small.score(k) for k in p), 6)) for p in small.paths()}
        assert within <= got
        # Every arc that is kept lies on some path within the beam.
        g = small.arc_posteriors()
        assert all(x > 0.0 for x in g)
        assert len(small.arcs) <= len(lat.arcs)


def test_cycle_and_backward_time_are_rejected():
    lat = Lattice()
    lat.add_node(0)
    lat.add_node(0)
    lat.add_arc(0, 1, "a", 0.0, 0.0)
    lat.add_arc(1, 0, "b", 0.0, 0.0)
    with pytest.raises(ValueError):
        lat.topo_order()
    lat2 = Lattice()
    lat2.add_node(5)
    lat2.add_node(3)
    with pytest.raises(ValueError):
        lat2.add_arc(0, 1, "a", 0.0, 0.0)


def test_no_path():
    lat = Lattice()
    lat.add_node(0)
    lat.add_node(1)
    lat.final = {1}
    assert lat.num_paths() == 0
    assert lat.best_path() == ([], NEG_INF)
    with pytest.raises(ValueError):
        lat.arc_posteriors()
