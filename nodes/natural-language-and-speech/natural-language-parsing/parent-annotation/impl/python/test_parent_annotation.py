# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parent-annotation/. The authors are listed in prov/SJCKA7.jsonl.

import random
from fractions import Fraction

from parent_annotation import annotate, read_tree, rules, strip, tree_probability, treebank_pcfg

TREEBANK = [
    "(S (NP (PRP she)) (VP (VBD saw) (NP (DT the) (NN cat))))",
    "(S (NP (PRP he)) (VP (VBD fed) (NP (DT the) (NN dog))))",
    "(S (NP (DT the) (NN dog)) (VP (VBD saw) (NP (PRP her))))",
    "(S (NP (PRP they)) (VP (VBD left)))",
]


def test_annotate_example() -> None:
    t = read_tree(TREEBANK[0])
    assert annotate(t) == ("S^ROOT", [("NP^S", [("PRP", "she")]),
                                      ("VP^S", [("VBD", "saw"), ("NP^VP", [("DT", "the"), ("NN", "cat")])])])
    assert annotate(t, tags=True)[1][0] == ("NP^S", [("PRP^NP", "she")])
    assert strip(annotate(t)) == t
    assert strip(annotate(t, tags=True)) == t


def test_treebank_estimates() -> None:
    trees = [read_tree(s) for s in TREEBANK]
    q = treebank_pcfg(trees)
    assert q[("NP", ("PRP",))] == Fraction(4, 7)
    assert q[("NP", ("DT", "NN"))] == Fraction(3, 7)
    assert q[("VP", ("VBD", "NP"))] == Fraction(3, 4)
    qa = treebank_pcfg([annotate(t) for t in trees])
    assert qa[("NP^S", ("PRP",))] == Fraction(3, 4)
    assert qa[("NP^VP", ("PRP",))] == Fraction(1, 3)
    assert qa[("NP^VP", ("DT", "NN"))] == Fraction(2, 3)
    # every left-hand side sums to 1
    for grammar in (q, qa):
        sums = {}
        for (a, _), p in grammar.items():
            sums[a] = sums.get(a, 0) + p
        assert all(v == 1 for v in sums.values())
    # the tree probabilities of the page
    subj = read_tree("(S (NP (PRP she)) (VP (VBD saw) (NP (DT the) (NN cat))))")
    obj = read_tree("(S (NP (DT the) (NN cat)) (VP (VBD saw) (NP (PRP her))))")
    # the plain grammar cannot tell a pronoun subject from a pronoun object
    assert tree_probability(subj, q) == tree_probability(obj, q) == Fraction(3, 392)
    assert tree_probability(annotate(subj), qa) == Fraction(1, 64)
    assert tree_probability(annotate(obj), qa) == Fraction(1, 384)
    # a tree with a rule that is not in the treebank gets probability 0
    assert tree_probability(read_tree("(S (NP (PRP they)) (VP (VBD left)))"), q) == Fraction(1, 112)
    assert tree_probability(annotate(read_tree("(S (VP (VBD left)) (NP (PRP they)))")), qa) == Fraction(0)


def random_tree(rng: random.Random, depth: int):
    labels = ["S", "NP", "VP", "PP", "SBAR"]
    if depth == 0 or rng.random() < 0.3:
        return (rng.choice(["NN", "VB", "DT", "IN"]), rng.choice(["a", "b", "c"]))
    return (rng.choice(labels), [random_tree(rng, depth - 1) for _ in range(rng.randint(1, 3))])


def count_nodes(t) -> int:
    n, stack = 0, [t]
    while stack:
        u = stack.pop()
        n += 1
        if not isinstance(u[1], str):
            stack.extend(u[1])
    return n


def test_random_round_trip() -> None:
    rng = random.Random(1998)
    for _ in range(500):
        t = random_tree(rng, 5)
        a = annotate(t, root_parent="TOP")
        assert strip(a) == t
        assert count_nodes(a) == count_nodes(t)
        # the label of each annotated rule's children names the rule's own original label
        for lhs, rhs in rules(a):
            base = lhs.split("^")[0]
            for c in rhs:
                if "^" in c:
                    assert c.split("^", 1)[1] == base
        # the annotated grammar maps onto the plain one: the rule counts agree after stripping
        plain = sorted(rules(t))
        assert sorted((l.split("^")[0], tuple(c.split("^")[0] for c in r)) for l, r in rules(a)) == plain


def test_deep_tree() -> None:
    t = ("NN", "x")
    for _ in range(5000):
        t = ("NP", [t])
    a = annotate(t)
    assert a[0] == "NP^ROOT" and a[1][0][0] == "NP^NP"
    assert strip(a) == t


def test_errors() -> None:
    for bad in ["", "(S", "(S (NP x) y)", "(S (NP (NN x))) (S (NN y))", "( (NN x))", "(S )"]:
        try:
            read_tree(bad)
        except ValueError:
            continue
        raise AssertionError("accepted %r" % bad)
    try:
        annotate(("NP^S", [("NN", "x")]))
    except ValueError:
        return
    raise AssertionError("a label with the separator was accepted")
