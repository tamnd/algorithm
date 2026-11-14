# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequence-pair/. The authors are listed in prov/9NWMQZ.jsonl.

import itertools
import math
import random

import pytest

from sequence_pair import SequencePair


def overlap(a, b) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def rects(x, y, w, h):
    return {b: (x[b], y[b], x[b] + w[b], y[b] + h[b]) for b in x}


def best_packing_area(w: dict, h: dict) -> int:
    """Least bounding-box area of a packing, by brute force over positions.

    A packing can be pushed left and down without growing, until every x is a
    sum of widths of other blocks and every y a sum of heights; so these
    positions are enough.
    """
    blocks = list(w)

    def sums(vals):
        s = {0}
        for v in vals:
            s |= {t + v for t in s}
        return sorted(s)

    cand = {b: [(px, py) for px in sums([w[c] for c in blocks if c != b]) for py in sums([h[c] for c in blocks if c != b])] for b in blocks}
    best = [sum(w.values()) * max(h.values())]
    placed: list = []

    def rec(k: int, wid: int, hei: int) -> None:
        if wid * hei >= best[0]:
            return
        if k == len(blocks):
            best[0] = wid * hei
            return
        b = blocks[k]
        for px, py in cand[b]:
            r = (px, py, px + w[b], py + h[b])
            if any(overlap(r, q) for q in placed):
                continue
            placed.append(r)
            rec(k + 1, max(wid, r[2]), max(hei, r[3]))
            placed.pop()

    rec(0, 0, 0)
    return best[0]


def test_pinwheel_example() -> None:
    sp = SequencePair([5, 1, 3, 4, 2], [1, 2, 3, 5, 4])
    w = {1: 1, 2: 2, 3: 1, 4: 1, 5: 2}
    h = {1: 2, 2: 1, 3: 1, 4: 2, 5: 1}
    width, height, x, y = sp.pack(w, h)
    assert (width, height) == (3, 3)
    assert {b: (x[b], y[b]) for b in w} == {1: (0, 0), 2: (1, 0), 3: (1, 1), 4: (2, 1), 5: (0, 2)}
    assert sp.pack_by_graphs(w, h) == (width, height, x, y)
    assert sp.relation(1, 3) == "left" and sp.relation(2, 3) == "below" and sp.relation(5, 1) == "above"
    assert sp.relation(4, 5) == "right"


def test_bad_input_and_moves() -> None:
    with pytest.raises(ValueError):
        SequencePair([1, 2], [1, 3])
    sp = SequencePair([1, 2, 3], [3, 2, 1])
    sp.swap_in_plus(1, 3)
    assert sp.plus == [3, 2, 1]
    sp.check_invariant()
    sp.swap_in_both(1, 2)
    assert sp.plus == [3, 1, 2] and sp.minus == [3, 1, 2]
    sp.check_invariant()
    assert SequencePair([], []).pack({}, {}) == (0, 0, {}, {})


def test_random_against_graphs_and_no_overlap() -> None:
    rng = random.Random(11)
    for _ in range(800):
        n = rng.randint(1, 12)
        plus = list(range(n))
        minus = list(range(n))
        rng.shuffle(plus)
        rng.shuffle(minus)
        sp = SequencePair(plus, minus)
        w = {b: rng.randint(1, 9) for b in plus}
        h = {b: rng.randint(1, 9) for b in plus}
        res = sp.pack(w, h)
        assert res == sp.pack_by_graphs(w, h)
        width, height, x, y = res
        r = rects(x, y, w, h)
        for a, b in itertools.combinations(plus, 2):
            assert not overlap(r[a], r[b])
            rel = sp.relation(a, b)
            if rel == "left":
                assert r[a][2] <= r[b][0]
            elif rel == "right":
                assert r[b][2] <= r[a][0]
            elif rel == "below":
                assert r[a][3] <= r[b][1]
            else:
                assert r[b][3] <= r[a][1]
        assert width == max(q[2] for q in r.values()) and height == max(q[3] for q in r.values())


def test_count_and_best_over_all_pairs() -> None:
    rng = random.Random(12)
    for trial in range(40):
        n = 3 if trial < 25 else 4
        top = 5 if n == 3 else 3
        w = {b: rng.randint(1, top) for b in range(n)}
        h = {b: rng.randint(1, top) for b in range(n)}
        pairs = [(p, m) for p in itertools.permutations(range(n)) for m in itertools.permutations(range(n))]
        assert len(pairs) == math.factorial(n) ** 2
        best = None
        for p, m in pairs:
            width, height, _, _ = SequencePair(list(p), list(m)).pack(w, h)
            if best is None or width * height < best:
                best = width * height
        assert best == best_packing_area(w, h)
