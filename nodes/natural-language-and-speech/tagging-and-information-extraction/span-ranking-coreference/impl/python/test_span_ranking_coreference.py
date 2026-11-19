# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/span-ranking-coreference/. The authors are listed in prov/YCRS0W.jsonl.

import math
import random
from itertools import product

from span_ranking_coreference import (EPS, all_spans, candidates, crosses, decode, gold_sets,
                                      loss_and_grad, prune, resolve, scores)

# The example of the page: "Alice met Bob and she smiled", n = 6, L = 2, lambda = 0.75.
N = 6
ALICE, METBOB, BOB, SHE, ALICEMET = (0, 1), (1, 3), (2, 3), (4, 5), (0, 2)
SM = {s: -3.0 for s in all_spans(6, 2)}
SM.update({ALICE: 2.0, SHE: 1.8, METBOB: 1.6, ALICEMET: 1.55, BOB: 1.5})
GOLD = [[ALICE, SHE]]


def example_pairs():
    sa = {(s, t): 0.0 for s in all_spans(6, 2) for t in all_spans(6, 2)}
    sa[(SHE, ALICE)] = 1.0
    sa[(SHE, BOB)] = -2.5
    sa[(SHE, METBOB)] = -5.0
    sa[(BOB, ALICE)] = -4.0
    sa[(BOB, METBOB)] = -5.0
    sa[(METBOB, ALICE)] = -5.0
    return sa


def test_spans_and_crossing():
    assert len(all_spans(6, 2)) == 11
    assert len(all_spans(5, 5)) == 15
    assert crosses((0, 2), (1, 3)) and crosses((1, 3), (0, 2))
    assert not crosses((0, 2), (2, 3)) and not crosses((0, 3), (1, 2)) and not crosses((0, 1), (0, 2))


def test_page_example():
    spans = prune(N, SM, 2, 0.75)
    assert spans == [ALICE, METBOB, BOB, SHE]  # "Alice met" crosses "met Bob" and is skipped
    sa = example_pairs()
    cands3 = candidates(spans, 3)
    assert cands3 == [[], [0], [1, 0], [2, 1, 0]]
    row = scores(spans, cands3, SM, sa)[3]
    assert [round(x, 9) for x in row] == [0.0, 0.8, -1.6, 4.8]
    ante, pred = decode(spans, cands3, SM, sa)
    assert ante == [EPS, EPS, EPS, ALICE]
    assert pred == [[ALICE, SHE]]
    loss, _, _ = loss_and_grad(spans, cands3, SM, sa, GOLD)
    assert abs(loss - 0.811329) < 1e-6
    # K = 2: "she" no longer sees "Alice", links to "Bob", and its gold set becomes the dummy.
    cands2 = candidates(spans, 2)
    ante, pred = decode(spans, cands2, SM, sa)
    assert ante == [EPS, EPS, EPS, BOB]
    assert gold_sets(spans, cands2, GOLD)[3] == [0]
    loss, _, _ = loss_and_grad(spans, cands2, SM, sa, GOLD)
    assert abs(loss - 2.015326) < 1e-6


def brute_loss(spans, cands, s_m, s_a, clusters):
    """- log of the sum, over all full antecedent assignments consistent with gold, of their probability."""
    sc = scores(spans, cands, s_m, s_a)
    gold = gold_sets(spans, cands, clusters)
    probs = []
    for row in sc:
        z = sum(math.exp(x) for x in row)
        probs.append([math.exp(x) / z for x in row])
    total = 0.0
    for ys in product(*[range(len(r)) for r in sc]):
        if all(y in g for y, g in zip(ys, gold)):
            p = 1.0
            for i, y in enumerate(ys):
                p *= probs[i][y]
            total += p
    return -math.log(total)


def random_doc(rng, n=7, width=3):
    s_m = {s: rng.uniform(-2, 2) for s in all_spans(n, width)}
    spans = prune(n, s_m, width, 0.8)
    cands = candidates(spans, 3)
    s_a = {}
    for i, cs in enumerate(cands):
        for j in cs:
            s_a[(spans[i], spans[j])] = rng.uniform(-2, 2)
    pool = spans[:]
    rng.shuffle(pool)
    clusters = [pool[0:2], pool[2:5], [(0, n)]]  # (0, n) is wider than L, so never a candidate
    return spans, cands, s_m, s_a, clusters


def test_loss_against_enumeration():
    rng = random.Random(1)
    for _ in range(30):
        spans, cands, s_m, s_a, clusters = random_doc(rng)
        loss = loss_and_grad(spans, cands, s_m, s_a, clusters)[0]
        assert abs(loss - brute_loss(spans, cands, s_m, s_a, clusters)) < 1e-9


def test_gradient_finite_differences():
    rng = random.Random(2)
    h = 1e-6
    for _ in range(5):
        spans, cands, s_m, s_a, clusters = random_doc(rng)
        _, d_m, d_a = loss_and_grad(spans, cands, s_m, s_a, clusters)
        for s in spans:
            up, dn = dict(s_m), dict(s_m)
            up[s] += h
            dn[s] -= h
            num = (loss_and_grad(spans, cands, up, s_a, clusters)[0]
                   - loss_and_grad(spans, cands, dn, s_a, clusters)[0]) / (2 * h)
            assert abs(num - d_m[s]) < 1e-5
        for key in s_a:
            up, dn = dict(s_a), dict(s_a)
            up[key] += h
            dn[key] -= h
            num = (loss_and_grad(spans, cands, s_m, up, clusters)[0]
                   - loss_and_grad(spans, cands, s_m, dn, clusters)[0]) / (2 * h)
            assert abs(num - d_a[key]) < 1e-5


def test_pruning_properties():
    rng = random.Random(3)
    for _ in range(50):
        n = rng.randint(1, 8)
        w = rng.randint(1, 4)
        s_m = {s: rng.uniform(-1, 1) for s in all_spans(n, w)}
        kept = prune(n, s_m, w, 0.6)
        assert len(kept) <= math.floor(0.6 * n + 1e-9)
        assert kept == sorted(kept)
        assert not any(crosses(s, t) for s in kept for t in kept)
        # A span that was skipped although it scores above a kept span crosses a kept span.
        low = min((s_m[s] for s in kept), default=None)
        for s in all_spans(n, w):
            if s not in kept and low is not None and s_m[s] > low:
                assert any(crosses(s, t) for t in kept)


def test_decode_is_joint_argmax():
    rng = random.Random(4)
    for _ in range(20):
        spans, cands, s_m, s_a, _ = random_doc(rng, n=6, width=2)
        ante, pred = decode(spans, cands, s_m, s_a)
        sc = scores(spans, cands, s_m, s_a)
        best, arg = None, None
        for ys in product(*[range(len(r)) for r in sc]):
            v = sum(r[y] - math.log(sum(math.exp(x) for x in r)) for r, y in zip(sc, ys))
            if best is None or v > best + 1e-12:
                best, arg = v, ys
        got = [0 if a is EPS else cands[i].index(spans.index(a)) + 1 for i, a in enumerate(ante)]
        assert tuple(got) == arg
        # The clusters are the connected components of the antecedent links.
        seen = [s for c in pred for s in c]
        assert len(seen) == len(set(seen))
        for i, a in enumerate(ante):
            if a is not EPS:
                assert any(spans[i] in c and a in c for c in pred)


def test_large_scores_stay_finite():
    spans = [(0, 1), (1, 2)]
    cands = candidates(spans, 1)
    s_m = {(0, 1): 400.0, (1, 2): 400.0}
    s_a = {((1, 2), (0, 1)): 100.0}
    try:
        math.exp(900.0)
        raised = False
    except OverflowError:
        raised = True
    assert raised  # the plain softmax would overflow
    loss, d_m, _ = loss_and_grad(spans, cands, s_m, s_a, [[(0, 1), (1, 2)]])
    assert loss == 0.0 and d_m[(1, 2)] == 0.0
    loss, _, _ = loss_and_grad(spans, cands, s_m, s_a, [])
    assert abs(loss - 900.0) < 1e-9


def test_resolve_pipeline():
    spans, ante, pred, loss = resolve(N, SM, example_pairs(), 2, 0.75, 3, GOLD)
    assert spans == [ALICE, METBOB, BOB, SHE]
    assert pred == [[ALICE, SHE]]
    assert abs(loss - 0.811329) < 1e-6
