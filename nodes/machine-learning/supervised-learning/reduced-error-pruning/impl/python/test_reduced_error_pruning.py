# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reduced-error-pruning/. The authors are listed in prov/QKQX68.jsonl.

import random

from reduced_error_pruning import (Node, errors_of, greedy_best_first, grow_id3, number,
                                   quinlan_iterative, reduced_error_prune)


def all_prunings(t):
    """Every pruned tree of t as the set of its internal node ids."""
    out = [frozenset()]
    if t.is_leaf():
        return out
    combos = [frozenset({t.id})]
    for u in t.children.values():
        combos = [s | s2 for s in combos for s2 in all_prunings(u)]
    return out + combos


def internal_kept(t, cut):
    if t.is_leaf() or t.id in cut:
        return frozenset()
    return frozenset({t.id}).union(*(internal_kept(u, cut) for u in t.children.values()))


def cut_from_kept(nodes, kept):
    return {t.id for t in nodes if not t.is_leaf() and t.id not in kept}


def random_tree(rng, depth, arity, attrs=3):
    label = rng.choice("ab")
    if depth == 0 or rng.random() < 0.3:
        return Node(label)
    a = rng.randrange(attrs)
    vals = rng.sample([0, 1, 2], rng.choice(arity))  # some values may have no branch
    return Node(label, a, {v: random_tree(rng, depth - 1, arity, attrs) for v in vals})


def check_against_all_prunings(rng, depth, arity):
    for trial in range(300):
        root = random_tree(rng, depth, arity)
        nodes = number(root)
        m = rng.randint(0, 25)
        X = [tuple(rng.randint(0, 2) for _ in range(3)) for _ in range(m)]
        y = [rng.choice("ab") for _ in range(m)]
        cut, err = reduced_error_prune(root, X, y)
        kept = internal_kept(root, cut)
        P = all_prunings(root)
        errs = {s: errors_of(root, cut_from_kept(nodes, s), X, y) for s in P}
        best = min(errs.values())
        assert err == best == errors_of(root, cut, X, y)
        winners = [s for s in P if errs[s] == best]
        assert kept in winners and all(kept <= s for s in winners)  # the smallest most accurate tree
        assert internal_kept(root, quinlan_iterative(root, X, y)) == kept


def test_binary_trees_against_all_prunings():
    check_against_all_prunings(random.Random(1987), 4, [2])


def test_multiway_trees_against_all_prunings():
    check_against_all_prunings(random.Random(27), 3, [2, 3])


def test_page_example():
    # Validation counts (a, b) per node; a node labeled a errs on the b cases and vice versa.
    a21, a22 = Node("b"), Node("a")
    a2 = Node("b", 2, {0: a21, 1: a22})
    a1 = Node("a")
    A = Node("a", 1, {0: a1, 1: a2})
    B = Node("b", 2, {0: Node("b"), 1: Node("a")})
    root = Node("a", 0, {0: A, 1: B})
    X = ([(0, 0, 0)] * 5 + [(0, 1, 0)] * 3 + [(1, 0, 0)] * 4 + [(1, 0, 1)] * 2)
    y = (["a"] * 5 + ["a", "b", "b"] + ["a", "b", "b", "b"] + ["a", "b"])
    nodes = number(root)
    assert errors_of(root, set(), X, y) == 3
    cut, err = reduced_error_prune(root, X, y)
    assert err == 3
    assert cut >= {a2.id, B.id} and A.id not in cut and root.id not in cut


def test_greedy_variant_can_be_worse():
    # t has two subtrees whose current errors are 3 but whose best errors are 1, and a pure leaf.
    def sub():
        return Node("a", 1, {0: Node("b"), 1: Node("a")})
    u1, u2, w = sub(), sub(), Node("b")
    t = Node("a", 0, {0: u1, 1: u2, 2: w})
    X = ([(0, 0)] * 2 + [(0, 1)] * 3 + [(1, 0)] * 2 + [(1, 1)] * 3 + [(2, 0)])
    y = (["a", "a"] + ["a", "a", "b"] + ["a", "a"] + ["a", "a", "b"] + ["b"])
    number(t)
    assert errors_of(t, set(), X, y) == 6
    cut, err = reduced_error_prune(t, X, y)
    assert err == 2 and t.id not in cut
    g = greedy_best_first(t, X, y)
    assert errors_of(t, g, X, y) == 3 and t.id in g


def test_grow_and_prune_on_noisy_data():
    rng = random.Random(7)

    def sample(n):
        X = [tuple(rng.randint(0, 2) for _ in range(5)) for _ in range(n)]
        y = [("p" if x[0] == 0 else "n") if rng.random() < 0.8 else rng.choice("pn") for x in X]
        return X, y

    Xt, yt = sample(200)
    Xv, yv = sample(100)
    Xs, ys = sample(1000)
    root = grow_id3(Xt, yt, range(5))
    nodes = number(root)
    cut, err = reduced_error_prune(root, Xv, yv)
    assert err <= errors_of(root, set(), Xv, yv)
    assert sum(1 for t in nodes if t.is_leaf()) > 3
    kept = internal_kept(root, cut)
    assert len(kept) < sum(1 for t in nodes if not t.is_leaf())
    assert errors_of(root, cut, Xs, ys) < errors_of(root, set(), Xs, ys)
