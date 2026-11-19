# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/head-rules/. The authors are listed in prov/EXAQEX.jsonl.

import random

from head_rules import (COLLINS, base_label, head_child, np_head, read_tree,
                        to_dependencies, words)


def deps(s):
    return to_dependencies(read_tree(s))


def test_klein_manning_figure() -> None:
    # Klein and Manning (2004), Figure 1: Factory payrolls fell in September.
    s = "(S (NP (NN Factory) (NNS payrolls)) (VP (VBD fell) (PP (IN in) (NP (NN September)))))"
    assert deps(s) == [0, 2, 3, 0, 3, 4]


def test_page_example() -> None:
    s = ("(S (NP-SBJ (DT The) (NN company)) (VP (MD will) (VP (VB sell) "
         "(NP (PRP$ its) (NNS assets)) (PP (TO to) (NP (NNS investors))))) (. .))")
    t = read_tree(s)
    assert words(t) == ["The", "company", "will", "sell", "its", "assets", "to", "investors", "."]
    assert to_dependencies(t) == [0, 2, 3, 0, 3, 6, 4, 4, 7, 3]


def test_np_rule() -> None:
    assert np_head(["DT", "JJ", "NN"]) == 2
    assert np_head(["NP", "PP"]) == 0
    assert np_head(["NNP", "POS"]) == 1
    assert np_head(["NP", "NN"]) == 1
    assert np_head(["CD", "NNS"]) == 1
    assert np_head(["DT", "CD"]) == 1
    assert np_head(["DT", "JJ"]) == 1
    assert np_head(["DT", "DT"]) == 1
    assert np_head(["NN", "NN", "PP"]) == 1
    assert np_head(["NP", ",", "NP", ","]) == 0
    # possessive: John 's dog. The inner NP is headed by 's, the outer by dog.
    assert deps("(NP (NP (NNP John) (POS 's)) (NN dog))") == [0, 2, 3, 0]


def test_table_rules() -> None:
    assert head_child("PP", ["IN", "NP"]) == 0
    assert head_child("PP", ["TO", "NP"]) == 0
    assert head_child("PP", ["NP", "IN"]) == 1
    assert head_child("SBAR", ["IN", "S"]) == 0
    assert head_child("SBAR", ["WHNP", "S"]) == 0
    assert head_child("VP", ["MD", "VP"]) == 0
    assert head_child("VP", ["VB", "NP", "PP"]) == 0
    assert head_child("VP", ["ADVP", "VBD", "NP"]) == 1
    assert head_child("S", ["NP-SBJ", "VP", "."]) == 1
    assert head_child("ADVP", ["RB", "RB"]) == 1  # right to left
    assert head_child("ADJP", ["RB", "JJ"]) == 1
    # priority beats position: S lists VP before NP
    assert head_child("S", ["VP", "NP"]) == 0
    assert head_child("VP", ["NN", "VBD"]) == 1
    # no match: the first child in the scan direction
    assert head_child("ADJP", [",", "CC"]) == 0
    assert head_child("ADVP", [",", "CC"]) == 1
    assert head_child("FRAG", ["NP", "PP", "."]) == 2
    assert head_child("PRN", ["-LRB-", "NP", "-RRB-"]) == 0
    # unknown label: leftmost
    assert head_child("ZZZ", ["A", "B", "C"]) == 0
    # single child
    assert head_child("NP", ["PRP"]) == 0


def test_labels() -> None:
    assert base_label("NP-SBJ-1") == "NP"
    assert base_label("PP-LOC=2") == "PP"
    assert base_label("-NONE-") == "-NONE-"
    assert base_label("-LRB-") == "-LRB-"
    assert head_child("PP-LOC", ["IN", "NP-1"]) == 0


def test_custom_table() -> None:
    table = {"PP": ("left", ("NP",))}
    assert head_child("PP", ["IN", "NP"], table) == 1
    assert deps("(PP (IN in) (NP (NN May)))") == [0, 0, 1]
    assert to_dependencies(read_tree("(PP (IN in) (NP (NN May)))"), table) == [0, 2, 0]


LABELS = sorted(COLLINS) + ["NP", "NP", "NX", "ZZ"]
TAGS = ["NN", "NNS", "NNP", "VB", "VBD", "MD", "IN", "TO", "DT", "JJ", "RB", "CD", "POS", ",", ".", "CC"]


def random_tree(rng, n):
    """A random tree with n words (preterminals) and random labels."""
    nodes = [(rng.choice(TAGS), "w") for _ in range(n)]
    while len(nodes) > 1:
        a = rng.randrange(len(nodes))
        b = rng.randrange(a + 1, min(len(nodes), a + 4) + 1)
        kids = nodes[a:b]
        nodes[a:b] = [(rng.choice(LABELS), kids)]
        if rng.random() < 0.2:
            nodes[a] = (rng.choice(LABELS), [nodes[a]])  # a unary node
    if not isinstance(nodes[0][1], list):
        nodes[0] = ("S", [nodes[0]])
    return nodes[0]


def reference(t, start, h):
    """Recursive reference: return the head word of t, whose first word is start."""
    if isinstance(t[1], str):
        return start
    heads = []
    pos = start
    for c in t[1]:
        heads.append(reference(c, pos, h))
        pos += len(words(c))
    c = head_child(t[0], [k[0] for k in t[1]])
    for k, x in enumerate(heads):
        if k != c:
            h[x] = heads[c]
    return heads[c]


def spans(t, start, out):
    """Collect the (first word, last word) of every internal node."""
    n = len(words(t))
    if not isinstance(t[1], str):
        out.append((start, start + n - 1))
        pos = start
        for c in t[1]:
            spans(c, pos, out)
            pos += len(words(c))
    return out


def ancestors(h, i):
    out = set()
    while i != 0:
        i = h[i]
        if i in out or len(out) > len(h):
            raise AssertionError("cycle")
        out.add(i)
    return out


def test_random_trees() -> None:
    rng = random.Random(7)
    for trial in range(600):
        n = rng.randint(1, 12)
        t = random_tree(rng, n)
        h = to_dependencies(t)
        assert len(h) == n + 1
        ref = [0] * (n + 1)
        root = reference(t, 1, ref)
        ref[root] = 0
        assert h == ref
        # a tree: one root word and no cycle
        assert sum(1 for i in range(1, n + 1) if h[i] == 0) == 1
        anc = {i: ancestors(h, i) for i in range(1, n + 1)}
        # projective: every word strictly between a head and its dependent is
        # a descendant of the head
        for d in range(1, n + 1):
            if h[d] == 0:
                continue
            lo, hi = sorted((d, h[d]))
            for x in range(lo + 1, hi):
                assert h[d] in anc[x]
        # every constituent is a subtree: exactly one word of its span has
        # its head outside the span
        for a, b in spans(t, 1, []):
            outside = [i for i in range(a, b + 1) if not a <= h[i] <= b]
            assert len(outside) == 1


def test_deep_tree() -> None:
    # a right-branching tree 3000 levels deep: the walk is iterative
    t = ("NN", "w")
    for _ in range(3000):
        t = ("NP", [("DT", "w"), t])
    h = to_dependencies(t)
    assert h[3001] == 0
    assert all(h[i] == 3001 for i in range(1, 3001))


def test_read_tree_errors() -> None:
    for bad in ["(S (NP", "(S (NN a b))", "(S (NN a)) x", "NN"]:
        try:
            read_tree(bad)
        except (ValueError, IndexError):
            continue
        raise AssertionError(bad)
