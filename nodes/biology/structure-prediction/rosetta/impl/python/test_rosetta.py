# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rosetta/. The authors are listed in prov/2J2HZZ.jsonl.
import itertools
import math
import random

from rosetta import (
    accept,
    backbone,
    centroid_score,
    full_atom_score,
    neighbours,
    pack,
    rosetta,
    side_chains,
)


def full_lib(n, k):
    words = ["".join(t) for t in itertools.product("LSR", repeat=k)]
    return {j: words for j in range(n - 1 - k)}


def fa_direct(seq, word, rot):
    """Full-atom score by a loop over all pairs of beads, with no hash map."""
    bb, sc = side_chains(word, rot)
    beads = bb + sc
    for a in range(len(beads)):
        for b in range(a + 1, len(beads)):
            if beads[a] == beads[b]:
                return None
    c = 0
    for i in range(len(sc)):
        for j in range(i + 1, len(sc)):
            if seq[i] == seq[j] == "H":
                if abs(sc[i][0] - sc[j][0]) + abs(sc[i][1] - sc[j][1]) == 1:
                    c += 1
    return -c


def cen_direct(seq, word):
    bb, _ = backbone(word)
    if len(set(bb)) != len(bb):
        return None
    c = 0
    for i in range(len(bb)):
        for j in range(i + 2, len(bb)):
            if seq[i] == seq[j] == "H" and abs(bb[i][0] - bb[j][0]) + abs(bb[i][1] - bb[j][1]) == 1:
                c += 1
    return -c


def brute_full_atom(seq):
    """Minimum full-atom score over every backbone word and every rotamer vector."""
    n = len(seq)
    best = None
    for t in itertools.product("LSR", repeat=n - 2):
        w = "".join(t)
        # rotamer 2 points back along the incoming bond, so it clashes for i >= 1
        for r0 in range(4):
            for rest in itertools.product((0, 1, 3), repeat=n - 1):
                e = fa_direct(seq, w, [r0, *rest])
                if e is not None and (best is None or e < best):
                    best = e
    return best


def test_rotamer_two_always_clashes_after_residue_zero():
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(3, 8)
        w = "".join(rng.choice("LSR") for _ in range(n - 2))
        rot = [rng.randrange(4) for _ in range(n)]
        i = rng.randrange(1, n)
        rot[i] = 2
        assert full_atom_score("H" * n, w, rot) is None


def test_scores_against_direct_calculation():
    rng = random.Random(2)
    for _ in range(600):
        n = rng.randint(3, 9)
        seq = "".join(rng.choice("HP") for _ in range(n))
        w = "".join(rng.choice("LSR") for _ in range(n - 2))
        rot = [rng.randrange(4) for _ in range(n)]
        assert centroid_score(seq, w) == cen_direct(seq, w)
        assert full_atom_score(seq, w, rot) == fa_direct(seq, w, rot)


def test_acceptance_against_formula():
    for d in (-2, 0, 1, 3):
        for temp in (0.1, 0.5, 2.0):
            p = 1.0 if d <= 0 else math.exp(-d / temp)
            for u in (0.0, 0.05, 0.4, 0.95):
                assert accept(0, d, temp, u) == (d <= 0 or u < p)
    assert not accept(0, None, 1.0, 0.0)


def test_pack_gives_a_valid_local_optimum():
    rng = random.Random(6)
    for _ in range(150):
        n = rng.randint(3, 8)
        seq = "".join(rng.choice("HP") for _ in range(n))
        w = "".join(rng.choice("LSR") for _ in range(n - 2))
        if centroid_score(seq, w) is None:
            continue
        rot = pack(seq, w)
        # does any clash-free rotamer vector exist? (exhaustive check)
        exists = any(
            full_atom_score(seq, w, [r0, *rest]) is not None
            for r0 in range(4) for rest in itertools.product((0, 1, 3), repeat=n - 1)
        )
        assert (rot is not None) == exists
        if rot is not None:
            e = full_atom_score(seq, w, rot)
            assert e is not None
            for i in range(n):
                for r in range(4):
                    e2 = full_atom_score(seq, w, rot[:i] + [r] + rot[i + 1:])
                    assert e2 is None or e2 >= e


def test_worked_example():
    seq = "HHPPHH"
    stages = [(3, full_lib(6, 3), 300), (1, full_lib(6, 1), 200)]
    e, w, rot = rosetta(seq, stages, 1500, random.Random(0))
    assert (e, w, rot) == (-3, "LRRL", [3, 3, 0, 1, 0, 3])
    assert brute_full_atom(seq) == -3
    assert centroid_score(seq, "SLLS") == -2 and centroid_score(seq, w) == -1


def test_reaches_brute_force_optimum():
    rng = random.Random(3)
    for trial in range(10):
        n = rng.randint(4, 6)
        seq = "".join(rng.choice("HP") for _ in range(n))
        k = min(3, n - 2)
        stages = [(k, full_lib(n, k), 300), (1, full_lib(n, 1), 200)]
        e, w, rot = rosetta(seq, stages, 1500, random.Random(trial))
        assert e == brute_full_atom(seq)
        assert fa_direct(seq, w, rot) == e


def test_output_is_a_local_minimum():
    rng = random.Random(4)
    for trial in range(15):
        n = rng.randint(3, 9)
        seq = "".join(rng.choice("HP") for _ in range(n))
        k = min(2, n - 2)
        e, w, rot = rosetta(seq, [(k, full_lib(n, k), 100)], 100, random.Random(trial))
        assert fa_direct(seq, w, rot) == e
        for w2, r2 in neighbours(w, rot):
            e2 = full_atom_score(seq, w2, r2)
            assert e2 is None or e2 >= e


def test_deterministic_with_seed():
    seq = "HPHHPPHH"
    stages = [(3, full_lib(8, 3), 200), (1, full_lib(8, 1), 100)]
    a = rosetta(seq, stages, 300, random.Random(11))
    b = rosetta(seq, stages, 300, random.Random(11))
    assert a == b
