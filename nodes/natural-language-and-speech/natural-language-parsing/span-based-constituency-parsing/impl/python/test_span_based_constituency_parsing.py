# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/span-based-constituency-parsing/. The authors are listed in prov/M9QEWS.jsonl.

import itertools
import math
import random

from span_based_constituency_parsing import (EMPTY, chart_parse, hinge_loss, labeled_spans,
                                             loss_augmented_scores, to_tree, top_down_greedy,
                                             tree_score)

LABELS = ["", "S", "NP", "VP"]


def bracketings(i, j):
    """All binary trees over the span (i, j), each as a list of its 2(j - i) - 1 spans."""
    if j - i == 1:
        return [[(i, j)]]
    out = []
    for k in range(i + 1, j):
        for left in bracketings(i, k):
            for right in bracketings(k, j):
                out.append([(i, j)] + left + right)
    return out


def brute_force(n, ls, ss=None):
    """Best score over all binary trees and all labelings, by full enumeration
    of the labels when the tree is small, and per-span max otherwise."""
    ss = ss or {}
    best = -math.inf
    for tree in bracketings(0, n):
        if len(tree) <= 5:
            for labs in itertools.product(*[range(len(ls[s])) for s in tree]):
                v = sum(ls[s][lab] + ss.get(s, 0.0) for s, lab in zip(tree, labs))
                best = max(best, v)
        else:
            best = max(best, sum(max(ls[s]) + ss.get(s, 0.0) for s in tree))
    return best


def random_scores(rng, n, n_labels, with_span=True):
    ls = {(i, j): [rng.choice([-2, -1, 0, 1, 2, 3]) + rng.random() for _ in range(n_labels)]
          for i in range(n) for j in range(i + 1, n + 1)}
    ss = {(i, j): rng.uniform(-2, 2) for i in range(n) for j in range(i + 1, n + 1)} if with_span else None
    return ls, ss


def is_binary_tree(n, spans):
    s = {(i, j) for i, j, _ in spans}
    if len(spans) != 2 * n - 1 or len(s) != len(spans) or (0, n) not in s:
        return False
    for i in range(n):
        if (i, i + 1) not in s:
            return False
    for i, j in s:
        if j - i > 1 and sum(1 for k in range(i + 1, j) if (i, k) in s and (k, j) in s) != 1:
            return False
    return True


def test_catalan_counts() -> None:
    assert [len(bracketings(0, n)) for n in range(1, 8)] == [1, 1, 2, 5, 14, 42, 132]


def example_scores():
    # She enjoys playing tennis: spans (i, j) with the label scores of
    # (empty, S, NP, VP) and a span score.
    ls = {
        (0, 1): [0.0, -2.0, 2.0, -1.0], (1, 2): [1.0, -2.0, -1.0, 0.0],
        (2, 3): [1.0, -1.0, -1.0, 0.0], (3, 4): [0.0, -2.0, 2.0, -1.0],
        (0, 2): [0.0, -1.0, -1.0, -1.0], (1, 3): [0.5, -2.0, -2.0, 0.0],
        (2, 4): [0.0, -1.0, 0.0, 1.5], (0, 3): [0.0, -1.0, -2.0, -2.0],
        (1, 4): [0.0, -1.0, -2.0, 2.0], (0, 4): [-1.0, 3.0, -1.0, 0.0],
    }
    ss = {(0, 1): 0.0, (1, 2): 0.0, (2, 3): 0.0, (3, 4): 0.0,
          (0, 2): 0.8, (1, 3): 0.5, (2, 4): 0.0, (0, 3): 0.0, (1, 4): 1.0, (0, 4): 0.0}
    return ls, ss


def test_example() -> None:
    ls, ss = example_scores()
    score, spans = chart_parse(4, ls, ss)
    assert math.isclose(score, 13.5)
    assert set(spans) == {(0, 4, 1), (0, 1, 2), (1, 4, 3), (1, 2, 0), (2, 4, 3), (2, 3, 0), (3, 4, 2)}
    assert labeled_spans(spans) == {(0, 4, 1), (0, 1, 2), (1, 4, 3), (2, 4, 3), (3, 4, 2)}
    assert to_tree(4, spans, LABELS) == ("S", [("NP", [0]), ("VP", [1, ("VP", [2, ("NP", [3])])])])
    g_score, g_spans = top_down_greedy(4, ls, ss)
    assert set(g_spans) == {(0, 4, 1), (0, 1, 2), (1, 4, 3), (1, 3, 0), (1, 2, 0), (2, 3, 0), (3, 4, 2)}
    assert math.isclose(g_score, 13.0)
    assert to_tree(4, g_spans, LABELS) == ("S", [("NP", [0]), ("VP", [1, 2, ("NP", [3])])])
    assert brute_force(4, ls, ss) == score


def test_one_word() -> None:
    score, spans = chart_parse(1, {(0, 1): [0.5, 2.0]})
    assert score == 2.0 and spans == [(0, 1, 1)]
    assert to_tree(1, spans, ["", "NP"]) == ("NP", [0])
    # an empty root keeps a placeholder label
    assert to_tree(1, [(0, 1, 0)], ["X", "NP"]) == ("X", [0])


def test_random_against_brute_force() -> None:
    rng = random.Random(2017)
    for trial in range(700):
        n = rng.randint(1, 4 if trial % 7 else 7)
        n_labels = rng.randint(1, 3 if n <= 3 else 4)
        ls, ss = random_scores(rng, n, n_labels, with_span=trial % 2 == 0)
        score, spans = chart_parse(n, ls, ss)
        assert is_binary_tree(n, spans)
        assert math.isclose(tree_score(spans, ls, ss), score, rel_tol=1e-12, abs_tol=1e-12)
        assert math.isclose(brute_force(n, ls, ss), score, rel_tol=1e-12, abs_tol=1e-12)
        g_score, g_spans = top_down_greedy(n, ls, ss)
        assert is_binary_tree(n, g_spans)
        assert g_score <= score + 1e-12


def hamming(spans, gold):
    g = {(i, j): lab for i, j, lab in gold}
    return sum(1 for i, j, lab in spans if g.get((i, j), EMPTY) != lab)


def test_loss_augmented_decoding() -> None:
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(1, 5)
        ls, ss = random_scores(rng, n, 3)
        gold = rng.choice(bracketings(0, n))
        gold = [(i, j, rng.randrange(3)) for i, j in gold]
        aug = loss_augmented_scores(n, ls, gold)
        top, spans = chart_parse(n, aug, ss)
        brute = -math.inf
        for tree in bracketings(0, n):
            if len(tree) <= 5:  # every labeling
                for labs in itertools.product(range(3), repeat=len(tree)):
                    t = [(i, j, lab) for (i, j), lab in zip(tree, labs)]
                    brute = max(brute, tree_score(t, ls, ss) + hamming(t, gold))
            else:  # the best labeling of this bracketing, found by trying each label per span
                t = []
                for i, j in tree:
                    t.append(max(((i, j, lab) for lab in range(3)),
                                 key=lambda s: tree_score([s], ls, ss) + hamming([s], gold)))
                brute = max(brute, tree_score(t, ls, ss) + hamming(t, gold))
        assert math.isclose(top, brute, rel_tol=1e-12, abs_tol=1e-12)
        assert math.isclose(tree_score(spans, ls, ss) + hamming(spans, gold), top, abs_tol=1e-12)
        h = hinge_loss(n, ls, gold, ss)
        assert h >= 0.0
        assert math.isclose(h, max(0.0, brute - tree_score(gold, ls, ss)), abs_tol=1e-12)


def test_hinge_zero_with_margin() -> None:
    # gold labels beat every other label by more than 1 on every gold span,
    # and other spans have no chance: the hinge loss is 0
    n = 4
    gold = [(0, 4, 1), (0, 1, 2), (1, 4, 3), (1, 2, 0), (2, 4, 3), (2, 3, 0), (3, 4, 2)]
    ls = {(i, j): [0.0, 0.0, 0.0, 0.0] for i in range(n) for j in range(i + 1, n + 1)}
    ss = {(i, j): -10.0 for i in range(n) for j in range(i + 1, n + 1)}
    for i, j, lab in gold:
        ls[(i, j)][lab] = 5.0
        ss[(i, j)] = 0.0
    assert hinge_loss(n, ls, gold, ss) == 0.0
    assert set(chart_parse(n, ls, ss)[1]) == set(gold)


def test_long_sentence() -> None:
    rng = random.Random(9)
    n = 60
    ls, ss = random_scores(rng, n, 3)
    score, spans = chart_parse(n, ls, ss)
    assert is_binary_tree(n, spans)
    assert math.isclose(tree_score(spans, ls, ss), score, rel_tol=1e-12)
    tree = to_tree(n, spans, ["", "A", "B"])
    flat, stack = [], [tree]
    while stack:
        u = stack.pop()
        if isinstance(u, int):
            flat.append(u)
        else:
            stack.extend(reversed(u[1]))
    assert flat == list(range(n))


def test_bad_input() -> None:
    try:
        chart_parse(0, {})
    except ValueError:
        return
    raise AssertionError("n = 0 accepted")
