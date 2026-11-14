# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normalized-polish-expression/. The authors are listed in prov/77DCRE.jsonl.

import itertools
import random

import pytest

from normalized_polish_expression import (
    NormalizedPolishExpression,
    is_normalized,
    postorder,
)

SCHROEDER = [1, 2, 6, 22, 90, 394]  # large Schroeder numbers S_0 .. S_5


def shapes(n: int) -> list:
    """All full binary tree shapes with n leaves; a leaf is None."""
    if n == 1:
        return [None]
    out = []
    for k in range(1, n):
        for a in shapes(k):
            for b in shapes(n - k):
                out.append((a, b))
    return out


def label(shape, leaves, ops):
    """Put the leaves (in order) and the operators (in preorder) on a shape."""
    li = iter(leaves)
    oi = iter(ops)

    def rec(s):
        if s is None:
            return next(li)
        o = next(oi)
        return (o, rec(s[0]), rec(s[1]))

    return rec(shape)


def all_trees(n: int) -> list:
    """All slicing trees with leaves 1..n (each shape, leaf order and operators)."""
    out = []
    for s in shapes(n):
        for perm in itertools.permutations(range(1, n + 1)):
            for ops in itertools.product("HV", repeat=n - 1):
                out.append(label(s, perm, ops))
    return out


def skewed(t) -> bool:
    """True if no right child has the operator of its parent."""
    if not isinstance(t, tuple):
        return True
    o, a, b = t
    if isinstance(b, tuple) and b[0] == o:
        return False
    return skewed(a) and skewed(b)


def tree_eval(t, sizes, x=0, y=0, pos=None):
    """Recursive reference evaluation of a slicing tree."""
    if pos is None:
        pos = {}
    if not isinstance(t, tuple):
        pos[t] = (x, y)
        return sizes[t][0], sizes[t][1], pos
    o, a, b = t
    wa, ha, _ = tree_eval(a, sizes, x, y, pos)
    if o == "V":
        wb, hb, _ = tree_eval(b, sizes, x + wa, y, pos)
        return wa + wb, max(ha, hb), pos
    wb, hb, _ = tree_eval(b, sizes, x, y + ha, pos)
    return max(wa, wb), ha + hb, pos


def overlap(p, q) -> bool:
    return p[0] < q[2] and q[0] < p[2] and p[1] < q[3] and q[1] < p[3]


def test_example() -> None:
    e = NormalizedPolishExpression([1, 2, "V", 3, 4, "H", "V"])
    sizes = {1: (2, 3), 2: (3, 2), 3: (4, 1), 4: (2, 2)}
    w, h, pos = e.evaluate(sizes)
    assert (w, h) == (9, 3)
    assert pos == {1: (0, 0), 2: (2, 0), 3: (5, 0), 4: (5, 1)}
    assert e.to_tree() == ("V", ("V", 1, 2), ("H", 3, 4))


def test_validity_examples() -> None:
    assert is_normalized([1, 2, "V", 3, "V"])
    assert not is_normalized([1, 2, 3, "V", "V"])  # two V in a row
    assert not is_normalized([1, "V", 2])  # balloting fails
    assert not is_normalized([1, 2, "V", 1, "H"])  # repeated operand
    assert not is_normalized([1, 2])  # too few operators
    assert not is_normalized([])
    assert is_normalized([7])
    assert NormalizedPolishExpression.normalize([1, 2, 3, "V", "V"]).tokens == [1, 2, "V", 3, "V"]
    with pytest.raises(ValueError):
        NormalizedPolishExpression([1, 2, 3, "H", "H"])


def test_counts_and_validity_against_all_words() -> None:
    import math

    for n in range(1, 6):
        trees = all_trees(n)
        skew_words = {tuple(postorder(t)) for t in trees if skewed(t)}
        assert len(skew_words) == math.factorial(n) * SCHROEDER[n - 1]
        # Every word with operands 1..n once and n - 1 operators.
        found = set()
        for opos in itertools.combinations(range(2 * n - 1), n - 1):
            for perm in itertools.permutations(range(1, n + 1)):
                for ops in itertools.product("HV", repeat=n - 1):
                    w: list = [None] * (2 * n - 1)
                    for p, o in zip(opos, ops):
                        w[p] = o
                    it = iter(perm)
                    for i in range(2 * n - 1):
                        if w[i] is None:
                            w[i] = next(it)
                    if is_normalized(w):
                        found.add(tuple(w))
        assert found == skew_words


def test_tree_round_trip_and_normalize() -> None:
    rng = random.Random(1)
    for n in range(1, 6):
        trees = all_trees(n)
        classes = set()
        for t in trees:
            sizes = {b: (rng.randint(1, 9), rng.randint(1, 9)) for b in range(1, n + 1)}
            e = NormalizedPolishExpression.from_tree(t)
            e.check_invariant()
            classes.add(tuple(e.tokens))
            assert tree_eval(t, sizes) == e.evaluate(sizes)
            if skewed(t):
                assert e.tokens == postorder(t)
                assert e.to_tree() == t
        assert len(classes) == len({tuple(postorder(t)) for t in trees if skewed(t)})


def random_tree(rng: random.Random, leaves: list[int]):
    if len(leaves) == 1:
        return leaves[0]
    k = rng.randint(1, len(leaves) - 1)
    return (rng.choice("HV"), random_tree(rng, leaves[:k]), random_tree(rng, leaves[k:]))


def test_random_large_no_overlap() -> None:
    rng = random.Random(2)
    for _ in range(600):
        n = rng.randint(1, 40)
        leaves = list(range(n))
        rng.shuffle(leaves)
        t = random_tree(rng, leaves)
        sizes = {b: (rng.randint(1, 20), rng.randint(1, 20)) for b in leaves}
        e = NormalizedPolishExpression.from_tree(t)
        w, h, pos = e.evaluate(sizes)
        assert (w, h, pos) == tree_eval(t, sizes)
        rects = [(pos[b][0], pos[b][1], pos[b][0] + sizes[b][0], pos[b][1] + sizes[b][1]) for b in leaves]
        for r in rects:
            assert 0 <= r[0] and 0 <= r[1] and r[2] <= w and r[3] <= h
        for i in range(n):
            for j in range(i + 1, n):
                assert not overlap(rects[i], rects[j])
        assert w * h >= sum(a * b for a, b in sizes.values())
