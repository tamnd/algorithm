# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-tree-clocks/. The authors are listed in prov/MXR7AF.jsonl.

import random

from interval_tree_clocks import (
    IntervalTreeClock,
    depth,
    ev_cells,
    id_cells,
    is_normal_ev,
    is_normal_id,
    join_ev,
    leq,
    norm_ev_full,
    norm_id_full,
    random_event_tree,
    split,
    sum_id,
)


def test_paper_style_example() -> None:
    a = IntervalTreeClock()
    b = a.fork()
    assert (a.i, b.i) == ((1, 0), (0, 1))
    a.event()
    assert a.e == (0, 1, 0)
    b.event()
    b.event()
    assert b.e == (0, 0, 2)
    assert not a.leq(b) and not b.leq(a)  # concurrent
    c = b.fork()
    assert (b.i, c.i) == ((0, (1, 0)), (0, (0, 1)))
    a.join(b)
    assert a.i == (1, (1, 0)) and a.e == (1, 0, 1)  # (0, 1, 2) in normal form
    a.event()  # fill raises the left half to 2, the largest value it already knows
    assert a.e == 2
    assert c.leq(a) and not a.leq(c)


def test_normalization_idempotent_and_meaning_preserving() -> None:
    rng = random.Random(7)
    for _ in range(2000):
        t = random_event_tree(rng, 5)
        n1 = norm_ev_full(t)
        assert norm_ev_full(n1) == n1
        assert is_normal_ev(n1)
        d = depth(t)
        assert ev_cells(n1, d) == ev_cells(t, d)


def test_join_is_pointwise_max_and_leq_is_pointwise() -> None:
    rng = random.Random(8)
    for _ in range(2000):
        x = norm_ev_full(random_event_tree(rng, 4))
        y = norm_ev_full(random_event_tree(rng, 4))
        d = 5
        cx, cy = ev_cells(x, d), ev_cells(y, d)
        j = join_ev(x, y)
        assert is_normal_ev(j)
        assert ev_cells(j, d) == [max(p, q) for p, q in zip(cx, cy)]
        assert leq(x, y) == all(p <= q for p, q in zip(cx, cy))


def test_fork_gives_disjoint_ids_whose_union_is_the_original() -> None:
    rng = random.Random(9)
    ids = [1]
    for _ in range(600):
        i = rng.choice(ids)
        i1, i2 = split(i)
        d = max(depth(i), depth(i1), depth(i2))
        c, c1, c2 = id_cells(i, d), id_cells(i1, d), id_cells(i2, d)
        assert all(p + q == r for p, q, r in zip(c1, c2, c))
        if i != 0:
            assert any(c1) and any(c2)
        assert is_normal_id(i1) and is_normal_id(i2)
        assert sum_id(i1, i2) == i
        ids.extend(x for x in (i1, i2) if depth(x) < 10)
        if len(ids) > 40:
            ids = rng.sample(ids, 20)


def run_against_histories(rng: random.Random, steps: int) -> None:
    """Random fork, event, join and message steps, compared with causal histories."""
    live: list[tuple[IntervalTreeClock, frozenset]] = [(IntervalTreeClock(), frozenset())]
    snapshots: list[tuple[object, frozenset]] = [(0, frozenset())]
    fresh = 0
    for _ in range(steps):
        x = rng.random()
        k = rng.randrange(len(live))
        s, h = live[k]
        if x < 0.25 and len(live) < 8:
            t = s.fork()
            live.append((t, h))
        elif x < 0.6:
            old_e = s.e
            s.event()
            fresh += 1
            h = h | {fresh}
            live[k] = (s, h)
            d = max(depth(old_e), depth(s.e), depth(s.i))
            ids, before, after = id_cells(s.i, d), ev_cells(old_e, d), ev_cells(s.e, d)
            assert leq(old_e, s.e) and not leq(s.e, old_e)
            assert all(b == a for b, a, own in zip(before, after, ids) if not own)
        elif x < 0.8 and len(live) > 1:
            j = rng.choice([q for q in range(len(live)) if q != k])
            t, g = live[j]
            s.join(t)
            live[k] = (s, h | g)
            live.pop(j)
        elif len(live) > 1:
            # message: the sender does an event and sends a peek; the receiver joins and does an event
            j = rng.choice([q for q in range(len(live)) if q != k])
            s.event()
            fresh += 1
            h = h | {fresh}
            live[k] = (s, h)
            msg = s.peek()
            snapshots.append((s.e, h))
            t, g = live[j]
            t.join(msg)
            t.event()
            fresh += 1
            live[j] = (t, g | h | {fresh})
        # ids stay disjoint and cover the whole interval
        d = max(depth(c.i) for c, _ in live)
        cover = [sum(col) for col in zip(*(id_cells(c.i, d) for c, _ in live))]
        assert cover == [1] * (1 << d)
        for c, g in live:
            assert is_normal_id(c.i) and is_normal_ev(c.e)
        c, g = rng.choice(live)
        snapshots.append((c.e, g))
    for e1, h1 in snapshots:
        for e2, h2 in snapshots:
            assert leq(e1, e2) == (h1 <= h2)


def test_against_causal_histories() -> None:
    rng = random.Random(2008)
    for _ in range(500):
        run_against_histories(rng, rng.randint(0, 60))
