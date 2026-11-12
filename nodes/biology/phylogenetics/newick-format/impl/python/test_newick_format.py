# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newick-format/. The authors are listed in prov/TR7EXK.jsonl.

import random

import pytest

from newick_format import Node, leaves, parse, to_newick


def shape(v: Node):
    """The tree without labels and lengths, as nested tuples."""
    return tuple(shape(c) for c in v.children)


def test_felsenstein_examples():
    t = parse("(B,(A,C,E),D);")
    assert leaves(t) == ["B", "A", "C", "E", "D"]
    assert shape(t) == ((), ((), (), ()), ())

    t = parse("(B:6.0,(A:5.0,C:3.0,E:4.0)Ancestor1:5.0,D:11.0);")
    mid = t.children[1]
    assert mid.label == "Ancestor1" and mid.length == 5.0
    assert [c.length for c in mid.children] == [5.0, 3.0, 4.0]
    assert t.children[2].length == 11.0

    t = parse("A;")
    assert t.label == "A" and t.is_leaf()

    t = parse("(,(,,),);")
    assert shape(t) == ((), ((), (), ()), ())
    assert leaves(t) == ["", "", "", "", ""]

    t = parse("(Alpha,Beta,Gamma,Delta,,Epsilon,,,);")
    assert len(t.children) == 9


def test_quotes_underscores_comments_and_blanks():
    t = parse("('Homo sapiens':0.1,Pan_troglodytes:0.2,'it''s [x]':3)root;")
    assert leaves(t) == ["Homo sapiens", "Pan troglodytes", "it's [x]"]
    assert t.label == "root"
    t2 = parse(" ( A [a comment] : 1.5 ,\n B:2e-1 ) ; ")
    assert leaves(t2) == ["A", "B"]
    assert t2.children[0].length == 1.5 and t2.children[1].length == 0.2


def test_printer_quotes_when_needed():
    t = Node(children=[Node("a b"), Node("x_y"), Node("it's"), Node("p:q", 1.0)])
    s = to_newick(t)
    assert s == "(a_b,'x_y','it''s','p:q':1.0);"
    assert parse(s) == t


@pytest.mark.parametrize(
    "bad",
    ["(A,B)", "(A,B;", "A,B);", "(A,B));", "(A:1:2,B);", "(A:x,B);", "(A B,C);", "(A,B);C", "('A,B);", "(A,[B);", "(A,B)C(D);"],
)
def test_errors(bad):
    with pytest.raises(ValueError):
        parse(bad)


LABEL_CHARS = "ab_ ():;,[]'xyz-."


def random_tree(rng: random.Random, n: int) -> Node:
    """A random tree with n leaves, random degrees, random labels and lengths."""
    nodes = [Node(label="".join(rng.choice(LABEL_CHARS) for _ in range(rng.randint(0, 4)))) for _ in range(n)]
    while len(nodes) > 1:
        k = min(len(nodes), rng.randint(2, 4))
        rng.shuffle(nodes)
        kids, nodes = nodes[:k], nodes[k:]
        for c in kids:
            if rng.random() < 0.7:
                c.length = rng.choice([0.0, 1.0, 0.5, rng.random() * 10, rng.randint(0, 100) * 1e-3])
        parent = Node(label=rng.choice(["", "", "anc", "node 7"]), children=kids)
        nodes.append(parent)
    return nodes[0]


def test_round_trip_random():
    rng = random.Random(1986)
    for _ in range(400):
        t = random_tree(rng, rng.randint(1, 25))
        s = to_newick(t)
        t2 = parse(s)
        assert t2 == t
        assert to_newick(t2) == s


def test_deep_tree_has_no_recursion():
    depth = 20000
    s = "(" * depth + "A" + "".join(f",B{i})" for i in range(depth)) + ";"
    t = parse(s)
    assert len(leaves(t)) == depth + 1
    assert to_newick(t) == s
