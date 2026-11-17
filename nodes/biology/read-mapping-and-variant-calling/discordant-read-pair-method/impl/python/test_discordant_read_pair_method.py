# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discordant-read-pair-method/. The authors are listed in prov/47N3AD.jsonl.

import math
import random

from discordant_read_pair_method import call_svs, classify, cluster, library_stats, span

L, MU, SIGMA = 50, 300.0, 30.0

# The sample genome as pieces of the reference (lo, hi, orientation); orientation 0 is new
# sequence that is not in the reference. The pieces give a deletion of [5000, 6000), an
# inversion of [12000, 14000), a tandem duplication of [20000, 21500) and an insertion of
# 150 new bases at 25000.
DONOR = [(0, 5000, 1), (6000, 12000, 1), (12000, 14000, -1), (14000, 21500, 1),
         (20000, 25000, 1), (0, 150, 0), (25000, 30000, 1)]


def map_read(x, strand, pieces):
    """The reference start and strand of the sample read [x, x + L), or None if it is not inside one piece."""
    lo = 0
    for rlo, rhi, o in pieces:
        hi = lo + rhi - rlo
        if lo <= x and x + L <= hi:
            if o == 0:
                return None
            if o == 1:
                return rlo + x - lo, strand
            return rhi - (x - lo) - L, "-" if strand == "+" else "+"
        lo = hi
    return None


def simulate_pairs(rng, pieces, n):
    """n fragments of the sample genome. Draw order for each: the length by rng.gauss, then the start
    by rng.randrange. Pairs with a mate across a piece boundary are dropped (a mapper would clip them)."""
    total = sum(hi - lo for lo, hi, _ in pieces)
    pairs = []
    for _ in range(n):
        f = round(rng.gauss(MU, SIGMA))
        s = rng.randrange(total - f)
        a = map_read(s, "+", pieces)
        b = map_read(s + f - L, "-", pieces)
        if a is None or b is None:
            continue
        (p1, s1), (p2, s2) = sorted([a, b])
        pairs.append((p1, s1, p2, s2))
    return pairs


def brute_components(pairs, d):
    n = len(pairs)
    seen, comps = [False] * n, []
    for i in range(n):
        if seen[i]:
            continue
        stack, comp = [i], []
        seen[i] = True
        while stack:
            a = stack.pop()
            comp.append(a)
            for b in range(n):
                if not seen[b] and abs(pairs[a][0] - pairs[b][0]) <= d and abs(pairs[a][2] - pairs[b][2]) <= d:
                    seen[b] = True
                    stack.append(b)
        comps.append(frozenset(comp))
    return set(comps)


def test_classify():
    assert classify((1000, "+", 1250, "-"), L, MU, SIGMA) == ""
    assert classify((1000, "+", 2250, "-"), L, MU, SIGMA) == "DEL"
    assert classify((1000, "+", 1100, "-"), L, MU, SIGMA) == "INS"
    assert classify((1000, "+", 2250, "+"), L, MU, SIGMA) == "INV"
    assert classify((1000, "-", 2250, "-"), L, MU, SIGMA) == "INV"
    assert classify((1000, "-", 2250, "+"), L, MU, SIGMA) == "DUP"
    # The threshold is mu + 3 sigma = 390 on the span.
    assert span((0, "+", 340, "-"), L) == 390
    assert classify((0, "+", 340, "-"), L, MU, SIGMA) == ""
    assert classify((0, "+", 341, "-"), L, MU, SIGMA) == "DEL"


def test_cluster_against_brute_force():
    rng = random.Random(1)
    for _ in range(40):
        n = rng.randint(0, 25)
        pairs = []
        for _ in range(n):
            p1 = rng.randrange(2000)
            pairs.append((p1, "+", p1 + rng.randrange(1500), "-"))
        d = rng.choice([50, 200, 400])
        got = {frozenset(c) for c in cluster(pairs, d)}
        assert got == brute_components(pairs, d)


def test_library_stats():
    rng = random.Random(3)
    spans = [round(rng.gauss(MU, SIGMA)) for _ in range(2000)]
    mu, sigma = library_stats(spans)
    # The median has standard error about 1.2533 sigma / sqrt(n); z = 4.
    assert abs(mu - MU) <= 4 * 1.2533 * SIGMA / math.sqrt(2000)
    assert abs(sigma - SIGMA) <= 0.1 * SIGMA


def test_example_deletion():
    pairs = [(100, "+", 1240, "-"), (130, "+", 1255, "-"), (160, "+", 1290, "-"),
             (140, "+", 360, "-"), (2000, "+", 3500, "-")]
    calls = call_svs(pairs, L, MU, SIGMA)
    assert calls == [{"type": "DEL", "strands": "+-", "support": 3, "left": 210, "right": 1240, "size": 880.0}]


def test_simulated_sample():
    rng = random.Random(2009)
    pairs = simulate_pairs(rng, DONOR, 3000)
    noise = []
    for _ in range(15):
        p1 = rng.randrange(30000)
        noise.append((p1, rng.choice("+-"), p1 + rng.randrange(5000, 20000), rng.choice("+-")))
    calls = call_svs(pairs + noise, L, MU, SIGMA)
    kinds = [(c["type"], c["strands"]) for c in calls]
    assert kinds == [("DEL", "+-"), ("DUP", "-+"), ("INS", "+-"), ("INV", "++"), ("INV", "--")]
    dele, dup, ins, inv_l, inv_r = calls
    assert dele["left"] <= 5000 and dele["right"] >= 6000
    assert 5000 - dele["left"] <= MU + 3 * SIGMA
    # Only fragments with both mates outside the deletion count, so long fragments are favored:
    # for normal lengths the mean of the selected lengths is mu + sigma^2 / (mu - 2 L).
    bias = SIGMA ** 2 / (MU - 2 * L)
    assert abs(dele["size"] - (1000 + bias)) <= 4 * 1.2533 * SIGMA / math.sqrt(dele["support"]) + 1
    assert 20000 <= dup["left"] and dup["right"] <= 21500
    assert ins["left"] <= 25000 <= ins["right"]
    # The same bias, with mu - 2 L - 150 start positions, makes an insertion look smaller.
    ins_bias = SIGMA ** 2 / (MU - 2 * L - 150)
    assert abs(ins["size"] - (150 - ins_bias)) <= 4 * 1.2533 * SIGMA / math.sqrt(ins["support"]) + 1
    assert inv_l["left"] <= 12000 and inv_l["right"] <= 14000
    assert inv_r["left"] >= 12000 and inv_r["right"] >= 14000
    # An insertion of 150 bases leaves room for few spanning fragments: about F - 2 L - 150 start
    # positions each, against F - 2 L for a deletion.
    assert ins["support"] < min(c["support"] for c in calls if c is not ins)
    for c in calls:
        assert c["support"] >= (3 if c is ins else 10)


def test_no_calls_without_variants():
    rng = random.Random(5)
    pairs = simulate_pairs(rng, [(0, 30000, 1)], 2000)
    assert call_svs(pairs, L, MU, SIGMA) == []
