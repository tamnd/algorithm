# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/session-window/. The authors are listed in prov/9SPQ0S.jsonl.

import random

from session_window import SessionWindows, sessions_batch, sessions_by_key


def brute_sessions(times, gap):
    """Sessions from the definition: link two items whose proto-windows overlap, take components."""
    n = len(times)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(n):
        for j in range(n):
            a, b = sorted((times[i], times[j]))
            if b < a + gap:  # [a, a+g) and [b, b+g) overlap
                parent[find(i)] = find(j)
    comps = {}
    for i in range(n):
        comps.setdefault(find(i), []).append(times[i])
    return sorted((min(c), max(c) + gap, len(c)) for c in comps.values())


def test_dataflow_example():
    # 13:02, 13:20 and 13:57 in minutes, gap 30 minutes.
    t = [13 * 60 + 2, 13 * 60 + 20, 13 * 60 + 57]
    assert sessions_batch(t, 30) == [(13 * 60 + 2, 13 * 60 + 50, 2), (13 * 60 + 57, 14 * 60 + 27, 1)]


def test_page_example_and_late_item():
    s = SessionWindows(5)
    for t in (1, 3, 9, 13, 20):
        s.insert(t)
    assert s.sessions() == [(1, 8, 2), (9, 18, 2), (20, 25, 1)]
    assert s.insert(16) == (9, 25, 4)
    assert s.sessions() == [(1, 8, 2), (9, 25, 4)]


def test_batch_and_online_match_definition():
    rng = random.Random(5)
    for _ in range(400):
        gap = rng.randint(1, 6)
        times = [rng.randint(0, 40) for _ in range(rng.randint(1, 14))]
        expected = brute_sessions(times, gap)
        assert sessions_batch(times, gap) == expected
        for _ in range(3):
            order = times[:]
            rng.shuffle(order)
            s = SessionWindows(gap)
            for t in order:
                s.insert(t)
            assert s.sessions() == expected


def test_keys_are_separate():
    rng = random.Random(6)
    for _ in range(100):
        gap = rng.randint(1, 5)
        events = [(rng.choice("abc"), rng.randint(0, 30)) for _ in range(rng.randint(1, 20))]
        got = sessions_by_key(events, gap)
        for key in set(k for k, _ in events):
            assert got[key] == brute_sessions([t for k, t in events if k == key], gap)
