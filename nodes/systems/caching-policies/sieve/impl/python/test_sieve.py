# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sieve/. The authors are listed in prov/JP6T1M.jsonl.

import random

from sieve import Sieve, sieve_hits


def naive_sieve(trace, c):
    """Algorithm 1 with a Python list, index 0 is the tail. The hand is an index or None."""
    q, bit, hand, hits = [], {}, None, []
    for x in trace:
        if x in bit:
            bit[x] = True
            hits.append(True)
            continue
        hits.append(False)
        if len(q) == c:
            i = 0 if hand is None else hand
            while bit[q[i]]:
                bit[q[i]] = False
                i = i + 1 if i + 1 < len(q) else 0
            del bit[q[i]]
            q.pop(i)
            hand = i if i < len(q) else None
        q.append(x)
        bit[x] = False
    return hits


def clock_hits(trace, c):
    """CLOCK, as FIFO-Reinsertion: a retained object goes back to the head."""
    q, bit, hits = [], {}, []
    for x in trace:
        if x in bit:
            bit[x] = True
            hits.append(True)
            continue
        hits.append(False)
        if len(q) == c:
            while bit[q[0]]:
                y = q.pop(0)
                bit[y] = False
                q.append(y)
            del bit[q.pop(0)]
        q.append(x)
        bit[x] = False
    return hits


def traces():
    rng = random.Random(2024)
    for _ in range(80):
        u = rng.randint(2, 30)
        yield [rng.randrange(u) for _ in range(rng.randint(1, 300))], rng.randint(1, 10)


def test_worked_example_and_contrast_with_clock():
    trace = "DCADBECD"
    a = Sieve(3)
    rows = []
    for x in trace:
        hit = a.access(x)
        rows.append((hit, a.evicted, a.order(), a.hand))
    assert [r[1] for r in rows] == [None, None, None, None, "C", "A", "B", None]
    assert rows[6][2:] == (["D", "E", "C"], "E")
    assert rows[7][0] and a.visited["D"]
    assert sum(sieve_hits(trace, 3)) == 2
    assert sum(clock_hits(trace, 3)) == 1


def test_same_hits_as_naive_reference():
    for trace, c in traces():
        assert sieve_hits(trace, c) == naive_sieve(trace, c)


def test_structure_after_every_request():
    for trace, c in traces():
        a = Sieve(c)
        for x in trace:
            before = x in a
            assert a.access(x) == before
            order = a.order()
            assert len(order) == len(a) <= c
            assert set(order) == set(a.visited)
            assert a.hand is None or a.hand in a.visited
            if order:
                assert order[-1] == a.head and order[0] == a.tail
            if before:
                assert a.visited[x], "a hit only sets the bit"
            else:
                assert a.head == x and not a.visited[x], "new objects enter unvisited at the head"


def test_hand_skips_new_objects_only_once():
    # A visited object keeps its place. After the hand passes it, the hand
    # works on the newer objects in front of it.
    a = Sieve(4)
    for x in "ABCD":
        a.access(x)
    a.access("A")
    a.access("E")
    assert a.order() == ["A", "C", "D", "E"] and a.hand == "C"


def test_quick_demotion_of_new_objects():
    # Objects behind the hand keep their place. When new objects arrive one
    # at a time, the hand chases them and evicts them, not the old ones.
    c = 8
    a = Sieve(c)
    hot = list(range(4))
    for x in hot * 2:
        a.access(x)
    for x in range(100, 100 + 3 * c):
        a.access(x)
        assert a.evicted is None or a.evicted >= 100
    assert all(h in a for h in hot)


def test_more_space_can_mean_fewer_hits():
    assert sum(sieve_hits("AABBCDC", 2)) == 3
    assert sum(sieve_hits("AABBCDC", 3)) == 2


def test_no_ghost_so_a_returning_object_is_new():
    a = Sieve(2)
    for x in "ABC":
        a.access(x)
    assert "A" not in a
    assert a.access("A") is False and a.visited["A"] is False
