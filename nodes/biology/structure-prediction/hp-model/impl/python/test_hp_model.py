# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hp-model/. The authors are listed in prov/HVWK9P.jsonl.
import itertools
import random

import pytest

from hp_model import (
    canonical_walks,
    count_saws,
    fold_exact,
    hp_energy,
    is_self_avoiding,
    unit_steps,
)


def all_walks_brute(n, dim):
    """Every walk from the origin with n vertices: all (2 dim)^(n-1) step words, filtered."""
    origin = tuple([0] * dim)
    for word in itertools.product(unit_steps(dim), repeat=max(n - 1, 0)):
        walk = [origin]
        for d in word:
            walk.append(tuple(a + b for a, b in zip(walk[-1], d)))
        if len(set(walk)) == n:
            yield walk


def brute_fold(seq, dim):
    """Minimum energy and the number of optimal walks (not reduced by symmetry)."""
    best, count = 1, 0
    for walk in all_walks_brute(len(seq), dim):
        e = hp_energy(seq, walk)
        if e < best:
            best, count = e, 1
        elif e == best:
            count += 1
    return best, count


def contacts_brute(seq, walk):
    """H-H contacts by a double loop over all pairs, with no hash map."""
    c = 0
    for i in range(len(walk)):
        for j in range(i + 2, len(walk)):
            if seq[i] == seq[j] == "H":
                if sum(abs(a - b) for a, b in zip(walk[i], walk[j])) == 1:
                    c += 1
    return -c


# OEIS A001411 and A001412
SQUARE = [1, 4, 12, 36, 100, 284, 780, 2172, 5916, 16268, 44100, 120292, 324932]
CUBIC = [1, 6, 30, 150, 726, 3534, 16926, 81390]


def test_square_lattice_counts():
    assert [count_saws(m, 2) for m in range(len(SQUARE))] == SQUARE


def test_cubic_lattice_counts():
    assert [count_saws(m, 3) for m in range(len(CUBIC))] == CUBIC


def test_canonical_walks_cover_every_walk_once():
    for dim, n in ((2, 8), (3, 5)):
        total = sum(w for _, w in canonical_walks(n, dim))
        assert total == sum(1 for _ in all_walks_brute(n, dim))
        for walk, _ in canonical_walks(n, dim):
            assert is_self_avoiding(walk)


def test_worked_example():
    seq = "HPHPPHHPHH"
    e, classes, fold = fold_exact(seq)
    assert (e, classes) == (-4, 3)
    assert is_self_avoiding(fold) and hp_energy(seq, fold) == -4
    assert brute_fold(seq, 2) == (-4, 24)
    hist = {}
    for walk, w in canonical_walks(len(seq)):
        k = hp_energy(seq, walk)
        hist[k] = hist.get(k, 0) + w
    assert hist == {-4: 24, -3: 136, -2: 1024, -1: 5792, 0: 9292}


def test_edge_cases():
    assert fold_exact("H")[:2] == (0, 1)
    assert fold_exact("HH")[:2] == (0, 1)
    assert fold_exact("HPPH")[:2] == (-1, 1)  # the square: one contact
    assert fold_exact("PPPPPP")[0] == 0
    assert fold_exact("HHHH")[:2] == (-1, 1)
    with pytest.raises(ValueError):
        fold_exact("")
    with pytest.raises(ValueError):
        fold_exact("HXP")


def test_odd_separation_rule_on_square_lattice():
    # residues i and j can touch on Z^2 only when j - i is odd
    assert fold_exact("HPH")[0] == 0
    assert fold_exact("HPPPH")[0] == 0
    assert fold_exact("HPPPPH")[0] == -1
    assert fold_exact("HPPPPPH")[0] == 0


def test_energy_against_pair_loop():
    rng = random.Random(7)
    for walk, _ in itertools.islice(canonical_walks(9, 2), 0, 3000, 7):
        seq = "".join(rng.choice("HP") for _ in range(9))
        assert hp_energy(seq, walk) == contacts_brute(seq, walk)


def test_random_sequences_against_brute_force_2d():
    rng = random.Random(2024)
    for _ in range(40):
        n = rng.randint(2, 8)
        seq = "".join(rng.choice("HP") for _ in range(n))
        e, classes, fold = fold_exact(seq, 2)
        be, bcount = brute_fold(seq, 2)
        assert e == be
        assert hp_energy(seq, fold) == e
        weighted = sum(w for walk, w in canonical_walks(n, 2) if hp_energy(seq, walk) == e)
        assert weighted == bcount
        assert classes <= bcount


def test_random_sequences_against_brute_force_3d():
    rng = random.Random(99)
    for _ in range(12):
        n = rng.randint(2, 6)
        seq = "".join(rng.choice("HP") for _ in range(n))
        assert fold_exact(seq, 3)[0] == brute_fold(seq, 3)[0]


def test_many_small_inputs_exhaustive():
    # every HP string of length up to 7: exact search equals brute force
    cache = {n: list(all_walks_brute(n, 2)) for n in range(1, 8)}
    count = 0
    for n in range(1, 8):
        for t in itertools.product("HP", repeat=n):
            seq = "".join(t)
            best = min(hp_energy(seq, w) for w in cache[n])
            assert fold_exact(seq)[0] == best
            count += 1
    assert count == 254


def test_longer_chain_energy_is_valid():
    seq = "HHPPHPPHPPHH"
    e, classes, fold = fold_exact(seq)
    assert (e, classes) == (-5, 1)
    assert is_self_avoiding(fold) and contacts_brute(seq, fold) == e
