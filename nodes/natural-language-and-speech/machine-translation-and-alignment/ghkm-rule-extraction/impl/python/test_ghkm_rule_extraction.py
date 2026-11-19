# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ghkm-rule-extraction/. The authors are listed in prov/6NN595.jsonl.

import random

import pytest

from ghkm_rule_extraction import (
    Node,
    brute_force_frontier,
    derive,
    extract_minimal_rules,
    frontier_nodes,
    parse,
    preorder,
    tree_string,
)


def test_example() -> None:
    root, words = parse("(S (NP (PRP he)) (VP (AUX does) (RB not) (VB go)))")
    f = "il ne va pas".split()
    links = {(1, 1), (2, 3), (3, 4), (4, 3)}
    frontier, span, comp = frontier_nodes(root, len(f), links)
    by_label = {n.label: n for n in preorder(root)}
    assert span[by_label["RB"]] == {2, 4} and comp[by_label["RB"]] == {1, 3}
    assert span[by_label["AUX"]] == set()
    assert {n.label for n in frontier} == {"S", "NP", "PRP", "VP", "VB"}
    rules = [(r.lhs, " ".join(r.rhs)) for r in extract_minimal_rules(root, words, f, links)]
    assert rules == [
        ("S(x0:NP x1:VP)", "x0 x1"),
        ("NP(x0:PRP)", "x0"),
        ("PRP(he)", "il"),
        ("VP(AUX(does) RB(not) x0:VB)", "ne x0 pas"),
        ("VB(go)", "va"),
    ]


def test_unaligned_source_word() -> None:
    root, words = parse("(S (NP (DT the) (NN house)) (VP (VBZ is) (JJ small)))")
    f = "das haus ist ja klein".split()
    links = {(1, 1), (2, 2), (3, 3), (5, 4)}
    rules = {r.node.label: (r.lhs, " ".join(r.rhs)) for r in extract_minimal_rules(root, words, f, links)}
    # "ja" (position 4) lies inside the closure [3, 5] of the VP, so the VP rule takes it
    assert rules["VP"] == ("VP(x0:VBZ x1:JJ)", "x0 ja x1")
    assert rules["S"] == ("S(x0:NP x1:VP)", "x0 x1")
    # an unaligned word outside every closure goes to the root
    f2 = "also das haus ist klein".split()
    links2 = {(2, 1), (3, 2), (4, 3), (5, 4)}
    rules2 = {r.node.label: " ".join(r.rhs) for r in extract_minimal_rules(root, words, f2, links2)}
    assert rules2["S"] == "also x0 x1"


def test_crossing_alignment_blocks_frontier() -> None:
    root, words = parse("(S (A a) (B b) (C c))")
    f = ["p", "q", "r"]
    links = {(1, 1), (2, 3), (3, 2)}
    frontier, _, _ = frontier_nodes(root, 3, links)
    assert {n.label for n in frontier} == {"S", "A", "B", "C"}
    rules = {r.node.label: " ".join(r.rhs) for r in extract_minimal_rules(root, words, f, links)}
    assert rules["S"] == "x0 x2 x1"
    # a one-to-many link whose closure holds a word of a sibling removes A
    links = {(1, 1), (2, 2), (3, 1)}
    frontier, _, _ = frontier_nodes(root, 3, links)
    assert {n.label for n in frontier} == {"S", "B"}
    rules = [(r.lhs, " ".join(r.rhs)) for r in extract_minimal_rules(root, words, f, links)]
    assert rules == [("S(A(a) x0:B C(c))", "p x0 r"), ("B(b)", "q")]


def test_bad_input() -> None:
    root, words = parse("(S (A a))")
    with pytest.raises(ValueError):
        extract_minimal_rules(root, words, ["p"], {(2, 1)})
    with pytest.raises(ValueError):
        extract_minimal_rules(root, words, ["p"], {(1, 2)})
    assert extract_minimal_rules(root, words, ["p"], set()) == []


def random_tree(rng: random.Random, positions: list[int]) -> Node:
    if len(positions) == 1:
        n = Node(rng.choice("PQ"), [positions[0]])
        return Node(rng.choice("UV"), [n]) if rng.random() < 0.2 else n
    parts = rng.randint(2, min(3, len(positions)))
    cuts = sorted(rng.sample(range(1, len(positions)), parts - 1))
    groups = [positions[a:b] for a, b in zip([0] + cuts, cuts + [len(positions)])]
    return Node(rng.choice("XYZ"), [random_tree(rng, g) for g in groups])


def test_random_against_definition() -> None:
    rng = random.Random(2004)
    checked = 0
    for _ in range(500):
        n_e, m = rng.randint(1, 6), rng.randint(1, 6)
        root = random_tree(rng, list(range(1, n_e + 1)))
        words = [f"e{i}" for i in range(1, n_e + 1)]
        f = [f"f{j}" for j in range(1, m + 1)]
        links = {(j, i) for j in range(1, m + 1) for i in range(1, n_e + 1) if rng.random() < 0.3}
        frontier, _, _ = frontier_nodes(root, m, links)
        assert frontier == brute_force_frontier(root, m, links)
        rules = extract_minimal_rules(root, words, f, links)
        if not links:
            assert rules == []
            continue
        assert rules[0].node is root
        rule_of = {r.node: r for r in rules}
        for r in rules:
            names = [s for s in r.rhs if s.startswith("x")]
            assert sorted(names) == [f"x{k}" for k in range(len(r.variables))]
        tree, source = derive(rule_of, root, words)
        assert tree == tree_string(root, words)
        assert source == f
        checked += 1
    assert checked > 300
