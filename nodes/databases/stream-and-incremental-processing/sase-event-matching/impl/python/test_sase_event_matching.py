# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sase-event-matching/. The authors are listed in prov/482Z67.jsonl.

import itertools
import random

import pytest

from sase_event_matching import Event, Reorder, SaseMatcher, run


def stream_of(spec):
    """spec: a string such as 'a1 b2 c4'; type letter, then timestamp."""
    return [Event(tok[0], int(tok[1:]), eid=i) for i, tok in enumerate(spec.split())]


def ids(matches):
    return sorted(tuple(e.eid for e in m) for m in matches)


def brute_force(events, types, window, partition=False, negated=None, predicate=None):
    """Every increasing index tuple that fits the pattern, from scratch."""
    events = sorted(events, key=lambda e: (e.ts, e.eid))
    negated = negated or {}
    out = []
    for idx in itertools.combinations(range(len(events)), len(types)):
        seq = [events[i] for i in idx]
        if any(e.type != t for e, t in zip(seq, types)):
            continue
        if seq[-1].ts - seq[0].ts > window:
            continue
        if partition and len({e.key for e in seq}) > 1:
            continue
        bad = False
        for i, t in negated.items():
            for j in range(idx[i - 1] + 1, idx[i]):
                n = events[j]
                if n.type == t and (not partition or n.key == seq[0].key):
                    bad = True
        if bad or (predicate is not None and not predicate(tuple(seq))):
            continue
        out.append(tuple(e.eid for e in seq))
    return sorted(out)


def random_events(rng, n, types="abcx", keys=(1, 2), span=30):
    ts = sorted(rng.randrange(span) for _ in range(n))
    return [Event(rng.choice(types), t, rng.choice(keys), rng.randint(0, 9), eid=i) for i, t in enumerate(ts)]


def test_page_example():
    ev = stream_of("a1 b2 a3 c4 b5 c6 c9")
    m = SaseMatcher(["a", "b", "c"], window=5)
    got = []
    for e in ev:
        got.append(ids(m.push(e)))
    # c4 ends a1 b2 c4; c6 ends a1 b2, a1 b5, a3 b5; c9 ends nothing within 5
    assert got == [[], [], [], [(0, 1, 3)], [], [(0, 1, 5), (0, 4, 5), (2, 4, 5)], []]
    neg = SaseMatcher(["a", "c"], window=5, negated={1: "b"})
    assert ids(run(neg, ev)) == [(2, 3)]


def test_rip_pointers_and_pruning():
    ev = stream_of("a1 b2 a3 c4 b5 c6 c9")
    m = SaseMatcher(["a", "b", "c"], window=5)
    for e in ev[:5]:
        m.push(e)
    st = m.parts[None]
    assert [(x[0].eid, x[1]) for x in st[1].entries] == [(1, 0), (4, 1)]
    m.push(ev[5])
    m.push(ev[6])  # now = 9: entries before ts 4 are gone
    assert [x[0].eid for x in st[0].entries] == []
    assert st[0].base == 2
    assert [x[0].eid for x in st[1].entries] == [4]


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_random_matches_brute_force(seed):
    rng = random.Random(seed)
    for _ in range(40):
        k = rng.randint(1, 3)
        types = [rng.choice("abc") for _ in range(k)]
        window = rng.randint(0, 12)
        partition = rng.random() < 0.5
        negated = {}
        if k >= 2 and rng.random() < 0.5:
            negated = {rng.randint(1, k - 1): rng.choice("abx")}
        predicate = None
        if rng.random() < 0.3:
            predicate = lambda s: s[0].value <= s[-1].value
        ev = random_events(rng, rng.randint(0, 22))
        m = SaseMatcher(types, window, partition, negated, predicate)
        emitted = []
        for e in ev:
            for match in m.push(e):
                assert match[-1] is e  # each match is reported when its last event arrives
                emitted.append(match)
        assert ids(emitted) == brute_force(ev, types, window, partition, negated, predicate)


def test_out_of_order_with_reorder_buffer():
    rng = random.Random(77)
    for _ in range(30):
        ev = random_events(rng, rng.randint(1, 25))
        D = rng.randint(1, 4)
        # shuffle within a bounded delay: an event arrives less than D time units late
        arrival = sorted(ev, key=lambda e: e.ts + rng.random() * D)
        types, window = ["a", "b", "c"], 10
        m = SaseMatcher(types, window, partition=True)
        assert ids(run(m, arrival, delay=D)) == brute_force(ev, types, window, partition=True)


def test_reorder_releases_in_order():
    rng = random.Random(5)
    ev = random_events(rng, 40)
    arrival = sorted(ev, key=lambda e: e.ts + rng.random() * 3)
    buf = Reorder(3)
    out = []
    for e in arrival:
        out.extend(buf.push(e))
    out.extend(buf.flush())
    assert [e.eid for e in out] == [e.eid for e in ev]


def test_construction_visits_are_bounded_by_matches():
    """Each visited entry lies on a match path or is one failed probe per entry on one."""
    rng = random.Random(8)
    for _ in range(20):
        ev = random_events(rng, 30, types="abc", keys=(1,), span=40)
        m = SaseMatcher(["a", "b", "c"], window=8)
        total = 0
        for e in ev:
            before = m.visits
            matches = m.push(e)
            total += len(matches)
            assert m.visits - before <= 3 * 3 * len(matches) + 3
        assert total == len(brute_force(ev, ["a", "b", "c"], 8))


def test_errors():
    with pytest.raises(ValueError):
        SaseMatcher([], 3)
    with pytest.raises(ValueError):
        SaseMatcher(["a", "b"], 3, negated={0: "x"})
    m = SaseMatcher(["a"], 3)
    m.push(Event("a", 5))
    with pytest.raises(ValueError):
        m.push(Event("a", 4))
