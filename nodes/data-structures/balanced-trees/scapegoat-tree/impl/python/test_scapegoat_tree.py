# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scapegoat-tree/. The authors are listed in prov/096NRC.jsonl.

import math
import random
from fractions import Fraction

import pytest

from scapegoat_tree import Node, ScapegoatTree, build, flatten


def shape(t):
    if t is None:
        return None
    if t.left is None and t.right is None:
        return t.key
    return (shape(t.left), t.key, shape(t.right))


def test_page_example():
    s = ScapegoatTree()
    for k in [1, 2, 3, 4]:
        s.insert(k)
    assert shape(s.root) == (None, 1, (None, 2, (None, 3, 4)))
    assert s.rebuilt == 0
    s.insert(5)
    # node 2 is the scapegoat; its subtree 2..5 is rebuilt with root 4
    assert shape(s.root) == (None, 1, ((2, 3, None), 4, 5))
    assert s.rebuilt == 4
    s.check_invariant()
    s.delete(1)
    assert (s.n, s.q) == (4, 5)
    assert shape(s.root) == ((2, 3, None), 4, 5)
    s.delete(5)  # 3 < (2/3) * 5, so the whole tree is rebuilt
    assert (s.n, s.q) == (3, 3)
    assert shape(s.root) == (2, 3, 4)
    s.check_invariant()


def test_build_takes_the_middle():
    nodes = [Node(k) for k in range(6)]
    t = build(nodes, 0, 6)
    assert shape(t) == ((0, 1, 2), 3, (4, 5, None))
    assert [x.key for x in flatten(t)] == list(range(6))


def test_edge_cases():
    s = ScapegoatTree()
    assert not s.delete(1)
    assert s.height() == -1
    assert s.insert(7) and not s.insert(7)
    assert s.delete(7) and len(s) == 0 and s.root is None
    s.check_invariant()
    with pytest.raises(ValueError):
        ScapegoatTree(Fraction(1, 2))


@pytest.mark.parametrize("alpha", [Fraction(2, 3), Fraction(4, 7), Fraction(9, 10)])
def test_sorted_input_and_amortized_work(alpha):
    n = 3000
    s = ScapegoatTree(alpha)
    for k in range(n):
        s.insert(k)
        if k % 97 == 0:
            assert s.height() <= math.log(s.q) / math.log(1 / alpha) + 1e-9
    s.check_invariant()
    # total rebuild work is O(n log n); the constant depends on alpha
    assert s.rebuilt <= 4 * n * math.log2(n) / (2 * float(alpha) - 1)


def test_random_against_set():
    rng = random.Random(1993)
    for case in range(600):
        alpha = rng.choice([Fraction(2, 3), Fraction(3, 5), Fraction(3, 4), Fraction(5, 6)])
        s = ScapegoatTree(alpha)
        ref = set()
        for _ in range(rng.randint(0, 80)):
            k = rng.randint(0, 40)
            if rng.random() < 0.6:
                assert s.insert(k) == (k not in ref)
                ref.add(k)
            else:
                assert s.delete(k) == (k in ref)
                ref.discard(k)
            s.check_invariant()
        assert s.keys() == sorted(ref)
        for k in range(-1, 42):
            assert (k in s) == (k in ref)
