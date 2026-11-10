# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epstein-levin-eptas-bin-packing/. The authors are listed in prov/XKC6Z1.jsonl.

import random
from fractions import Fraction
from itertools import combinations_with_replacement
from math import comb, floor

from epstein_levin_eptas_bin_packing import (RobustPacking, closest, matrix, max_subdeterminant, min_bins, patterns,
                                             round_up)

F = Fraction

# (eps, item sizes); the sizes below eps / 4 are small items.
CASES = [
    (F(1, 2), [F(3, 10), F(9, 20), F(3, 5), F(1, 20), F(1, 10)]),
    (F(1), [F(3, 5), F(9, 10), F(1, 5), F(1, 10)]),
    (F(1, 3), [F(3, 10), F(3, 5), F(1, 20)]),
]


def brute_opt(sizes):
    """The least number of unit bins, by a subset DP that keeps (bins, load of the last bin) as small as possible."""
    n = len(sizes)
    if n == 0:
        return 0
    best = [None] * (1 << n)
    best[0] = (1, F(0))
    for mask in range(1 << n):
        b, load = best[mask]
        for i in range(n):
            if mask >> i & 1:
                continue
            nxt = (b, load + sizes[i]) if load + sizes[i] <= 1 else (b + 1, sizes[i])
            t = mask | 1 << i
            if best[t] is None or nxt < best[t]:
                best[t] = nxt
    return best[-1][0]


def items_of(rp):
    return sorted(x for b in rp.bins for x in [s for s, _ in b["large"]] + b["small"])


def test_example():
    rp = RobustPacking(F(1, 2))
    seq = [F(9, 20), F(3, 5), F(3, 5), F(9, 20)]
    recs = [rp.add(s) for s in seq]
    assert [r["opened"] for r in recs] == [1, 0, 1, 0]
    assert [r["repacked"] for r in recs] == [0, 1, 0, 2]
    assert [r["moved"] for r in recs] == [0, F(9, 20), 0, F(33, 20)]
    assert sorted(tuple(s for s, _ in b["large"]) for b in rp.bins) == [(F(9, 20), F(9, 20)), (F(3, 5), F(3, 5))]
    assert len(rp.bins) == 2 and brute_opt(seq) == 3
    assert recs[-1]["d"] == 7 and recs[-1]["distance"] == 1


def test_round_up():
    for eps in (F(1), F(1, 2), F(1, 3), F(1, 5)):
        q = 1 + eps / 4
        for k in range(1, 41):
            s = eps / 4 + (1 - eps / 4) * F(k, 40)
            r = round_up(s, eps)
            assert s <= r < s * q
            assert r <= 1


def test_patterns_and_count_bound():
    for eps, sizes in CASES:
        cap = 1 + eps
        classes = sorted({round_up(s, eps) for s in sizes if s >= eps / 4}, reverse=True)
        pats = patterns(classes, cap)
        assert pats[0] == ()
        q = floor(cap / (eps / 4))
        expect = {()}
        for k in range(1, q + 1):
            for p in combinations_with_replacement(classes, k):
                if sum(p) <= cap:
                    expect.add(tuple(sorted(p, reverse=True)))
        assert {tuple(sorted(p, reverse=True)) for p in pats} == expect and len(pats) == len(expect)
        assert len(pats) <= comb(len(classes) + q, q)


def test_min_bins_and_closest_against_enumeration():
    eps = F(1, 2)
    classes = sorted({round_up(s, eps) for s in (F(3, 10), F(9, 20), F(3, 5))}, reverse=True)
    pats = patterns(classes, 1 + eps)
    vectors = {p: tuple(p.count(c) for c in classes) for p in pats}
    rng = random.Random(7)
    for _ in range(25):
        counts = {c: rng.randint(0, 2) for c in classes}
        target = tuple(counts[c] for c in classes)
        bins = rng.randint(1, 4)
        sols, stack = [], [(0, (0,) * len(classes), 0, {})]
        while stack:
            i, have, used, y = stack.pop()
            if i == len(pats):
                if have == target and used == bins:
                    sols.append(y)
                continue
            for v in range(bins - used + 1):
                h = tuple(a + v * b for a, b in zip(have, vectors[pats[i]]))
                if any(a > t for a, t in zip(h, target)):
                    break
                stack.append((i + 1, h, used + v, {**y, pats[i]: v} if v else y))
        # The empty pattern pads, so a solution with exactly `bins` bins exists iff the least number is at most bins.
        assert (min_bins(pats, classes, counts) <= bins) == bool(sols)
        if sols:
            assert min_bins(pats, classes, counts) == min(sum(y.values()) - y.get((), 0) for y in sols)
        old = {p: rng.randint(0, 1) for p in rng.sample(pats, 3)}
        found = closest(pats, counts, bins, old, 10)
        if not sols:
            assert found is None
            continue
        dist = lambda y: max(abs(y.get(p, 0) - old.get(p, 0)) for p in pats)
        assert found is not None and found in [{p: v for p, v in y.items() if v} for y in sols]
        assert dist(found) == min(dist(y) for y in sols)


def test_against_opt_and_proximity_bounds():
    rng = random.Random(2006)
    seen_repack = 0
    for eps, sizes in CASES:
        for _ in range(6):
            rp, seq = RobustPacking(eps), []
            for _ in range(9):
                s = rng.choice(sizes)
                seq.append(s)
                before = len(rp.bins)
                rec = rp.add(s)
                assert len(rp.bins) <= brute_opt(seq)
                assert all(rp.load(b) <= rp.cap for b in rp.bins)
                assert items_of(rp) == sorted(seq)
                assert all(tuple(c for _, c in b["large"]) == b["pattern"] for b in rp.bins)
                if not rec["large"]:
                    continue
                d, delta = rec["d"], rec["delta"]
                if rec["distance"] is None:
                    assert rec["opened"] == 1 and len(rp.bins) == before + 1
                else:
                    assert rec["distance"] <= 3 * d * delta
                    assert rec["repacked"] <= d * rec["distance"] <= 3 * d * d * delta
                    assert rec["moved"] <= rec["repacked"] * rp.cap
                    assert rec["moved"] / s <= 4 * (1 + eps) * 3 * d * d * delta / eps
                    seen_repack = max(seen_repack, rec["repacked"])
    assert seen_repack >= 1


def test_new_bin_only_when_rounded_problem_needs_it():
    """When a large item opens a bin, the rounded items do not fit in the old number of bins of size 1 + eps."""
    eps, sizes = CASES[0]
    rng = random.Random(11)
    for _ in range(6):
        rp, seq = RobustPacking(eps), []
        for _ in range(8):
            s = rng.choice(sizes)
            seq.append(s)
            before = len(rp.bins)
            rec = rp.add(s)
            if rec["large"] and rec["distance"] is None:
                counts = {c: 0 for c in rp.classes}
                for b in rp.bins:
                    for _, c in b["large"]:
                        counts[c] += 1
                assert min_bins(patterns(rp.classes, rp.cap), rp.classes, counts) > before
                assert brute_opt(seq) >= before + 1


def test_subdeterminant_values():
    eps = F(1, 2)
    classes = sorted({round_up(s, eps) for s in (F(3, 10), F(9, 20), F(3, 5))}, reverse=True)
    pats = patterns(classes, 1 + eps)
    a = matrix(classes, pats)
    assert len(pats) == 18 and max_subdeterminant(a) == 24
    assert all(max(abs(x) for x in row) <= floor((1 + eps) / (eps / 4)) for row in a)
