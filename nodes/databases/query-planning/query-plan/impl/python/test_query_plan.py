# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/query-plan/. The authors are listed in prov/MHRFHJ.jsonl.

from math import factorial

from query_plan import (
    bushy_trees,
    catalan,
    count_bushy,
    count_left_deep,
    is_left_deep,
    is_right_deep,
    is_zigzag,
    leaves,
    left_deep_trees,
    show,
)

RELS = "ABCDEF"


def test_counts_match_formulas():
    for n in range(1, 7):
        rels = RELS[:n]
        bushy = list(bushy_trees(rels))
        assert len(bushy) == len(set(bushy)) == count_bushy(n)
        assert count_bushy(n) == factorial(n) * catalan(n - 1)
        left = list(left_deep_trees(rels))
        assert len(left) == len(set(left)) == count_left_deep(n)
        assert set(left) == {t for t in bushy if is_left_deep(t)}
        assert sum(is_right_deep(t) for t in bushy) == factorial(n)
        if n >= 2:
            assert sum(is_zigzag(t) for t in bushy) == factorial(n) * 2 ** (n - 2)


def test_known_values():
    assert [count_bushy(n) for n in range(1, 8)] == [1, 2, 12, 120, 1680, 30240, 665280]
    assert [count_left_deep(n) for n in range(1, 8)] == [1, 2, 6, 24, 120, 720, 5040]


def test_each_tree_uses_each_relation_once():
    for t in bushy_trees("ABCDE"):
        assert sorted(leaves(t)) == list("ABCDE")


def test_shapes():
    t = (("A", "B"), "C")
    assert is_left_deep(t) and not is_right_deep(t) and is_zigzag(t)
    t = ("A", ("B", "C"))
    assert is_right_deep(t) and not is_left_deep(t)
    t = (("A", "B"), ("C", "D"))
    assert not is_zigzag(t) and not is_left_deep(t) and not is_right_deep(t)
    assert show(t) == "((A ⋈ B) ⋈ (C ⋈ D))"
    assert is_left_deep(("A", "B")) and is_right_deep(("A", "B"))
