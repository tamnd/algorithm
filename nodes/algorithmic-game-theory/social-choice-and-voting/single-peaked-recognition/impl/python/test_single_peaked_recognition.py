# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/single-peaked-recognition/. The authors are listed in prov/HW79QR.jsonl.

import itertools
import random

from agtprefs import all_profiles, all_rankings, is_single_peaked_on, random_profile
from single_peaked_recognition import is_single_peaked, single_peaked_axis


def brute_axes(profile, m):
    return [ax for ax in itertools.permutations(range(m)) if is_single_peaked_on(profile, ax)]


def random_sp_ranking(rng, axis):
    """Build a ranking single-peaked on axis from the bottom: take one end of the rest each time."""
    lo, hi = 0, len(axis) - 1
    worst_first = []
    while lo < hi:
        if rng.random() < 0.5:
            worst_first.append(axis[lo])
            lo += 1
        else:
            worst_first.append(axis[hi])
            hi -= 1
    worst_first.append(axis[lo])
    return tuple(reversed(worst_first))


def check(profile, m):
    axis = single_peaked_axis(profile, m)
    exists = bool(brute_axes(profile, m))
    assert (axis is not None) == exists, (profile, axis)
    if axis is not None:
        assert sorted(axis) == list(range(m))
        assert is_single_peaked_on(profile, axis)


def test_every_profile_with_three_candidates():
    for n in range(1, 4):
        for P in all_profiles(3, n):
            check(P, 3)


def test_every_profile_of_two_voters_with_four_candidates():
    for P in all_profiles(4, 2):
        check(P, 4)


def test_random_single_peaked_profiles_are_recognized():
    rng = random.Random(1)
    for _ in range(300):
        m = rng.randint(2, 6)
        axis = tuple(rng.sample(range(m), m))
        P = tuple(random_sp_ranking(rng, axis) for _ in range(rng.randint(1, 6)))
        check(P, m)
        assert is_single_peaked(P, m)


def test_random_profiles_agree_with_brute_force():
    rng = random.Random(2)
    for _ in range(300):
        m = rng.randint(3, 6)
        n = rng.randint(1, 4)
        if rng.random() < 0.5:
            P = random_profile(rng, m, n)
        else:
            axis = tuple(rng.sample(range(m), m))
            P = [random_sp_ranking(rng, axis) for _ in range(n)]
            i = rng.randrange(n)
            r = list(P[i])
            a, b = rng.sample(range(m), 2)
            r[a], r[b] = r[b], r[a]
            P[i] = tuple(r)
            P = tuple(P)
        check(P, m)


def test_count_of_single_peaked_rankings_on_one_axis():
    for m in range(1, 7):
        axis = tuple(range(m))
        assert sum(1 for r in all_rankings(m) if is_single_peaked_on((r,), axis)) == 2 ** (m - 1)


def test_condorcet_cycle_is_not_single_peaked():
    assert single_peaked_axis(((0, 1, 2), (1, 2, 0), (2, 0, 1)), 3) is None


def test_worked_example():
    # a, b, c, d, e = 0, 1, 2, 3, 4
    P = ((4, 3, 1, 2, 0), (4, 3, 2, 1, 0), (3, 4, 2, 0, 1))
    assert single_peaked_axis(P, 5) == (0, 2, 3, 4, 1)
    assert brute_axes(P, 5) == [(0, 2, 3, 4, 1), (0, 2, 4, 3, 1), (1, 3, 4, 2, 0), (1, 4, 3, 2, 0)]


def test_edge_cases():
    assert single_peaked_axis((), 3) == (0, 1, 2)
    assert single_peaked_axis(((0,),), 1) == (0,)
    assert single_peaked_axis(((1, 0),), 2) in ((0, 1), (1, 0))


def test_larger_profile():
    rng = random.Random(3)
    m = 40
    axis = tuple(rng.sample(range(m), m))
    P = tuple(random_sp_ranking(rng, axis) for _ in range(300))
    found = single_peaked_axis(P, m)
    assert found is not None and is_single_peaked_on(P, found)
    Q = P[:-1] + (tuple(rng.sample(range(m), m)),)
    found = single_peaked_axis(Q, m)
    if found is not None:
        assert is_single_peaked_on(Q, found)
