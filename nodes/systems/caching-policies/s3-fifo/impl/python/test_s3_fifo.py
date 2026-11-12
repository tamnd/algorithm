# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/s3-fifo/. The authors are listed in prov/5D8W5S.jsonl.

import random
from fractions import Fraction

from s3_fifo import S3FIFO, s3_fifo_hits


def naive_s3_fifo(trace, c, small, move_at):
    """Algorithm 1 again with plain lists, index 0 is the tail (oldest)."""
    S, M, G, freq, hits = [], [], [], {}, []
    main = (1 - small) * c
    g_cap = max(1, -(-main.numerator // main.denominator))

    def evict_m():
        while M:
            t = M.pop(0)
            if freq[t] > 0:
                freq[t] -= 1
                M.append(t)
            else:
                del freq[t]
                return

    def evict_s():
        while S:
            t = S.pop(0)
            if freq[t] >= move_at:
                freq[t] = 0
                M.append(t)
                if len(M) > main:
                    evict_m()
            else:
                del freq[t]
                G.append(t)
                if len(G) > g_cap:
                    G.pop(0)
                return

    for x in trace:
        if x in freq:
            freq[x] = min(freq[x] + 1, 3)
            hits.append(True)
            continue
        hits.append(False)
        while len(S) + len(M) >= c:
            if len(S) >= small * c:
                evict_s()
            else:
                evict_m()
        if x in G:
            G.remove(x)
            M.append(x)
        else:
            S.append(x)
        freq[x] = 0
    return hits


def traces():
    rng = random.Random(2023)
    for _ in range(60):
        u = rng.randint(2, 40)
        c = rng.randint(1, 12)
        small = rng.choice([Fraction(1, 10), Fraction(1, 4), Fraction(1, 2)])
        yield [rng.randrange(u) for _ in range(rng.randint(1, 300))], c, small, rng.choice([1, 2])


def check_invariants(a):
    assert len(a) <= a.c
    assert not (set(a.s) & set(a.m)) and not (set(a.g) & set(a.freq))
    assert set(a.freq) == set(a.s) | set(a.m)
    assert all(0 <= f <= 3 for f in a.freq.values()), "freq is capped at 3"
    assert len(a.g) <= a.g_cap


def test_worked_example():
    a = S3FIFO(4, Fraction(1, 4))
    rows = []
    for x in "ABAACDEFBGABEFJ":
        hit = a.access(x)
        rows.append((hit, a.evicted[:], list(a.s), list(a.m), list(a.g)))
    assert [r[0] for r in rows] == [False, False, True, True] + [False] * 6 + [True, True] + [False] * 3
    assert rows[6] == (False, ["B"], ["C", "D", "E"], ["A"], ["B"])
    assert rows[8] == (False, ["D"], ["E", "F"], ["A", "B"], ["C", "D"])
    assert rows[12] == (False, ["F"], ["G"], ["A", "B", "E"], ["D", "F"])
    assert rows[14] == (False, ["E"], ["J"], ["F", "A", "B"], ["D", "G"])
    assert a.freq == {"J": 0, "F": 0, "A": 0, "B": 0}


def test_invariants_after_every_request():
    for trace, c, small, move_at in traces():
        a = S3FIFO(c, small, move_at)
        for x in trace:
            before = x in a
            assert a.access(x) == before
            check_invariants(a)


def test_same_hits_as_naive_reference():
    for trace, c, small, move_at in traces():
        assert s3_fifo_hits(trace, c, small, move_at) == naive_s3_fifo(trace, c, small, move_at)


def test_one_hit_wonders_never_reach_m():
    a = S3FIFO(20)
    for x in range(1000):
        a.access(x)
        assert not a.m


def test_ghost_hit_goes_to_m():
    a = S3FIFO(10)
    for x in range(12):
        a.access(x)
    assert 0 in a.g
    a.access(0)
    assert 0 in a.m and 0 not in a.g


def test_more_space_can_mean_fewer_hits():
    assert sum(s3_fifo_hits("ABCDABECE", 2)) == 1
    assert sum(s3_fifo_hits("ABCDABECE", 3)) == 0


def test_default_split_is_ten_percent():
    a = S3FIFO(100)
    assert a.small == Fraction(1, 10) and a.g_cap == 90
