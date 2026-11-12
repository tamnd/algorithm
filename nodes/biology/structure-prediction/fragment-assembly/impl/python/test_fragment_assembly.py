# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fragment-assembly/. The authors are listed in prov/B7NM52.jsonl.
import itertools
import math
import random

from fragment_assembly import (
    accept,
    build,
    fragment_assembly,
    full_library,
    pick_fragments,
    score,
)


def energy_direct(seq, coords):
    """HP energy by a loop over all pairs; None when a site is used twice."""
    n = len(coords)
    for i in range(n):
        for j in range(i + 1, n):
            if coords[i] == coords[j]:
                return None
    c = 0
    for i in range(n):
        for j in range(i + 2, n):
            if seq[i] == seq[j] == "H":
                if abs(coords[i][0] - coords[j][0]) + abs(coords[i][1] - coords[j][1]) == 1:
                    c += 1
    return -c


def brute_optimum(seq):
    """Minimum energy over all 3^(n-2) words, that is, over every self-avoiding fold."""
    best = None
    for t in itertools.product("LSR", repeat=len(seq) - 2):
        e = energy_direct(seq, build("".join(t)))
        if e is not None and (best is None or e < best):
            best = e
    return best


DB = [
    ("HHPHPPPPHH", "LLRLSLLR"), ("PHPPHPPHHP", "LRRLRRSL"), ("HHHHPHPHHP", "LLSLSLSS"),
    ("PHPHHPPHPH", "LLSLRRSR"), ("HPHPPHPPPP", "LSLLRLSL"), ("HPHPPHPPHP", "LLSLSRRL"),
    ("HHPPPHPHPP", "LLSLSLSS"), ("HHHHHHPPPP", "LLSLSLSS"),
]


def test_build_is_a_lattice_walk():
    coords = build("LSR")
    assert coords == [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)]
    for w in ("", "S", "LLLL", "RRSLL"):
        c = build(w)
        assert len(c) == len(w) + 2
        assert all(abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1 for a, b in zip(c, c[1:]))


def test_score_against_direct_calculation():
    rng = random.Random(11)
    for _ in range(600):
        n = rng.randint(3, 12)
        seq = "".join(rng.choice("HP") for _ in range(n))
        w = "".join(rng.choice("LSR") for _ in range(n - 2))
        assert score(seq, w) == energy_direct(seq, build(w))


def test_collision_is_rejected():
    assert score("HHHHH", "LLL") is None  # the fifth residue lands on the first
    assert not accept(0, None, 5.0, 0.0)


def test_acceptance_against_formula():
    for e_old in (-3, 0, 2):
        for e_new in (-4, -3, -1, 0, 3):
            for temp in (0.1, 0.5, 1.0, 2.0):
                p = 1.0 if e_new <= e_old else math.exp(-(e_new - e_old) / temp)
                for u in (0.0, 0.01, 0.3, 0.5, 0.9, 0.999):
                    assert accept(e_old, e_new, temp, u) == (u < p or e_new <= e_old)


def test_acceptance_rate_matches_probability():
    rng = random.Random(3)
    trials = 20000
    hits = sum(accept(-2, -1, 0.8, rng.random()) for _ in range(trials))
    assert abs(hits / trials - math.exp(-1 / 0.8)) < 0.015


def test_pick_fragments_shape_and_order():
    seq = "HPHPPHHPHH"
    lib = pick_fragments(seq, DB, 3, 4)
    assert sorted(lib) == list(range(6))
    assert all(len(v) == 4 and all(len(f) == 3 for f in v) for v in lib.values())
    for j, frags in lib.items():
        # best distance of each distinct fragment, by a direct scan of the database
        dist = {}
        for s, w in DB:
            for a in range(len(w) - 2):
                d = sum(x != y for x, y in zip(seq[j:j + 5], s[a:a + 5]))
                dist[w[a:a + 3]] = min(d, dist.get(w[a:a + 3], 99))
        chosen = max(dist[f] for f in frags)
        others = [d for f, d in dist.items() if f not in frags]
        assert not others or chosen <= min(others)
        assert [dist[f] for f in frags] == sorted(dist[f] for f in frags)


def test_worked_example():
    seq = "HPHPPHHPHH"
    lib3 = pick_fragments(seq, DB, 3, 4)
    lib1 = full_library(10, 1)
    e, w = fragment_assembly(seq, [(3, lib3, 1500), (1, lib1, 500)], 2.0, 0.1, random.Random(0))
    assert (e, w) == (-4, "LRLLSSLL")
    assert brute_optimum(seq) == -4
    assert energy_direct(seq, build(w)) == e


def test_reaches_brute_force_optimum_with_full_library():
    rng = random.Random(5)
    for trial in range(12):
        n = rng.randint(5, 10)
        seq = "".join(rng.choice("HP") for _ in range(n))
        k = min(3, n - 2)
        stages = [(k, full_library(n, k), 1500), (1, full_library(n, 1), 800)]
        e, w = fragment_assembly(seq, stages, 2.0, 0.1, random.Random(trial))
        assert e == brute_optimum(seq)
        assert energy_direct(seq, build(w)) == e


def test_result_is_valid_and_deterministic():
    rng = random.Random(8)
    for trial in range(20):
        n = rng.randint(3, 12)
        seq = "".join(rng.choice("HP") for _ in range(n))
        k = min(2, n - 2)
        stages = [(k, full_library(n, k), 200)]
        a = fragment_assembly(seq, stages, 1.5, 0.2, random.Random(trial))
        b = fragment_assembly(seq, stages, 1.5, 0.2, random.Random(trial))
        assert a == b
        assert energy_direct(seq, build(a[1])) == a[0]
        assert a[0] <= 0


def test_constant_temperature_samples_boltzmann():
    # full library of 1-letter fragments is a symmetric proposal, so the chain
    # is a Metropolis chain whose stationary law is exp(-E/T) on valid folds
    seq = "HPPHH"
    temp = 0.7
    valid = {}
    for t in itertools.product("LSR", repeat=3):
        w = "".join(t)
        e = energy_direct(seq, build(w))
        if e is not None:
            valid[w] = e
    z = sum(math.exp(-e / temp) for e in valid.values())
    p_low = sum(math.exp(-e / temp) for e in valid.values() if e == -1) / z
    rng = random.Random(42)
    lib = full_library(5, 1)
    w, e = "SSS", 0
    low = 0
    steps = 60000
    for _ in range(steps):
        j = rng.randrange(3)
        w2 = w[:j] + rng.choice(lib[j]) + w[j + 1:]
        e2 = score(seq, w2)
        if accept(e, e2, temp, rng.random()):
            w, e = w2, e2
        low += e == -1
    assert abs(low / steps - p_low) < 0.02
