# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-log/. The authors are listed in prov/JEWV9G.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from sliding_window_log import SlidingWindowLog, SlidingWindowRing, fits, run


def random_times(rng, count, step_num, step_den):
    t, out = F(0), []
    for _ in range(count):
        t += F(rng.randint(0, step_num), rng.randint(1, step_den))
        out.append(t)
    return out


def test_page_example():
    times = [F(x) for x in ["8", "9", "9.5", "10", "10.5", "11", "12", "15", "18", "19", "21", "25", "28.5"]]
    assert run(times, 3, 10) == [True, True, True, False, False, False, False, False, True, True, True, False, True]


def test_bad_input():
    with pytest.raises(ValueError):
        SlidingWindowLog(0, 1)
    with pytest.raises(ValueError):
        SlidingWindowRing(1, 0)
    s = SlidingWindowLog(1, 10)
    s.allow(5)
    with pytest.raises(ValueError):
        s.allow(4)


def test_ring_agrees_and_log_is_small():
    rng = random.Random(12)
    for _ in range(500):
        n, w = rng.randint(1, 6), F(rng.randint(1, 15), rng.randint(1, 3))
        times = random_times(rng, rng.randint(1, 80), 4, 3)
        a, b = SlidingWindowLog(n, w), SlidingWindowRing(n, w)
        for t in times:
            assert a.allow(t) == b.allow(t)
            assert len(a.log) <= n


def test_exhaustive_sound_greedy_tight():
    """Every multiset of up to 6 integer times in 0..6: the output fits, a request passes iff it keeps
    the output fitting, and an input that fits passes whole."""
    for n, w in [(1, 2), (2, 3), (2, 4), (3, 4)]:
        for size in range(7):
            for times in itertools.combinations_with_replacement(range(7), size):
                dec = run(list(times), n, w)
                kept = []
                for t, ok in zip(times, dec):
                    assert ok == fits(kept + [t], n, w)
                    if ok:
                        kept.append(t)
                if fits(list(times), n, w):
                    assert all(dec)


def probe(times, n, w):
    """The probes of the memory lower bound: from the state after `times` (all in [0, w)), send a
    burst of n requests at time u, for each integer u in [w, 2w); record how many pass."""
    answers = []
    for u in range(w, 2 * w):
        s = SlidingWindowLog(n, w)
        for t in times:
            assert s.allow(t)
        answers.append(sum(s.allow(u) for _ in range(n)))
    return tuple(answers)


def test_memory_lower_bound_probe():
    """Distinct sets of n times in one window of m ticks give distinct answers, so the state needs
    at least log2 C(m, n) bits."""
    for m in range(2, 8):
        for n in range(1, m + 1):
            sets = list(itertools.combinations(range(m), n))
            answers = {probe(list(c), n, m) for c in sets}
            assert len(answers) == len(sets)
