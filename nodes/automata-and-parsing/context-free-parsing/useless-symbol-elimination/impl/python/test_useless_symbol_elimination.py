# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/useless-symbol-elimination/. The authors are listed in prov/09FBBP.jsonl.

import itertools
import random

from useless_symbol_elimination import (
    eliminate_useless,
    generating_set,
    nonterminal_set,
    reachable_set,
)

NTS = ["S", "A", "B", "C", "D"]


def grammar(text):
    prods = []
    for rule in text.split(";"):
        a, rhs = rule.split("->")
        for alt in rhs.split("|"):
            prods.append((a.strip(), tuple(x for x in alt.split() if x != "eps")))
    return prods


def spans(prods, nts, w):
    """Independent oracle: the set of (X, i, j) with X =>* w[i:j], by a least fixpoint."""
    n, known = len(w), set()

    def ends(rhs, i, j):
        cur = {i}
        for x in rhs:
            nxt = set()
            for p in cur:
                if x in nts:
                    nxt |= {q for q in range(p, j + 1) if (x, p, q) in known}
                elif p < j and w[p] == x:
                    nxt.add(p + 1)
            cur = nxt
        return cur

    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            for i in range(n + 1):
                for j in range(i, n + 1):
                    if (a, i, j) not in known and j in ends(rhs, i, j):
                        known.add((a, i, j))
                        changed = True
    return known


def derives(prods, nts, start, w):
    return (start, 0, len(w)) in spans(prods, nts, w)


def naive_useful(prods, nts, start):
    """Reference: repeated full passes for generating, then for reachable."""
    gen, rank = set(), {}
    rnd = 0
    while True:
        rnd += 1
        new = {a for a, rhs in prods if a not in gen and all(x not in nts or x in gen for x in rhs)}
        if not new:
            break
        for a in new:
            rank[a] = rnd
        gen |= new
    p1 = [(a, rhs) for a, rhs in prods if a in gen and all(x not in nts or x in gen for x in rhs)]
    reach = {start}
    while True:
        new = {x for a, rhs in p1 if a in reach for x in rhs if x in nts and x not in reach}
        if not new:
            break
        reach |= new
    return gen, rank, p1, reach


def witness_tree(prods, nts, start, target, rank, keep):
    """Build a parse tree of a terminal string from start that contains target,
    using only the productions in keep. A tree is (symbol, rhs, children)."""
    best = {}
    for a, rhs in keep:
        if all(x not in nts or rank[x] < rank[a] for x in rhs):
            best.setdefault(a, rhs)
    parent, order = {start: None}, [start]
    for a in order:
        for rhs in (r for b, r in keep if b == a):
            for k, x in enumerate(rhs):
                if x in nts and x not in parent:
                    parent[x] = (a, rhs, k)
                    order.append(x)
    assert target in parent

    def gen_tree(a):
        root = [a, best[a], []]
        stack = [root]
        while stack:
            node = stack.pop()
            for x in node[1]:
                if x in nts:
                    child = [x, best[x], []]
                    node[2].append(child)
                    stack.append(child)
                else:
                    node[2].append(x)
        return root

    tree = gen_tree(target)
    x = target
    while parent[x] is not None:
        a, rhs, k = parent[x]
        kids = [tree if i == k else (gen_tree(y) if y in nts else y) for i, y in enumerate(rhs)]
        tree, x = [a, rhs, kids], a
    return tree


def check_tree(prods, nts, tree, target):
    """The tree uses productions of prods, has terminal leaves, and contains target."""
    seen, out, stack = False, [], [tree]
    pset = set(prods)
    while stack:
        node = stack.pop()
        if isinstance(node, str):
            assert node not in nts
            out.append(node)
            continue
        a, rhs, kids = node
        seen = seen or a == target
        assert (a, tuple(rhs)) in pset
        assert tuple(k if isinstance(k, str) else k[0] for k in kids) == tuple(rhs)
        stack.extend(reversed(kids))
    assert seen
    return tuple(out)


def random_grammar(rng):
    k = rng.randint(1, 5)
    nts = NTS[:k]
    with_rules = [a for a in nts if a == "S" or rng.random() < 0.85]
    prods = set()
    for a in with_rules:
        for _ in range(rng.randint(1, 3)):
            n = rng.choice([0, 1, 1, 2, 2, 3])
            rhs = tuple(rng.choice(nts + ["a", "b"]) for _ in range(n))
            if rng.random() < 0.1:
                rhs = (a,) + rhs  # left recursion
            prods.add((a, rhs))
    prods = sorted(prods)
    rng.shuffle(prods)
    return prods, set(nts)


def test_textbook_example_and_order():
    g = grammar("S -> A B | a; A -> b")
    assert eliminate_useless(g, "S", ["B"]) == [("S", ("a",))]
    # the other order (reachable first, then generating) leaves A -> b
    nts = nonterminal_set(g, "S", ["B"])
    reach = reachable_set(g, "S", nts)
    first = [(a, r) for a, r in g if a in reach]
    gen = generating_set(first, nts)
    wrong = [(a, r) for a, r in first if a in gen and all(x not in nts or x in gen for x in r)]
    assert wrong == [("S", ("a",)), ("A", ("b",))]


def test_page_example():
    g = grammar("S -> A B | C a; A -> a A | b; B -> B b; C -> c | D; D -> d D; E -> e S")
    nts = nonterminal_set(g, "S")
    assert generating_set(g, nts) == {"S", "A", "C", "E"}
    out = eliminate_useless(g, "S")
    assert out == grammar("S -> C a; C -> c")
    assert reachable_set(grammar("S -> C a; A -> a A | b; C -> c; E -> e S"), "S", nts) == {"S", "C"}


def test_empty_language():
    assert eliminate_useless(grammar("S -> A; A -> a A"), "S") == []
    assert eliminate_useless([], "S") == []
    assert eliminate_useless(grammar("S -> S a"), "S") == []
    # a start symbol with only the empty production keeps it
    assert eliminate_useless(grammar("S -> eps | A; A -> A"), "S") == [("S", ())]


def test_declared_nonterminal_without_productions():
    g = grammar("S -> X a | b")
    # without the declaration, X is a terminal and S -> X a stays
    assert eliminate_useless(g, "S") == g
    assert eliminate_useless(g, "S", ["X"]) == [("S", ("b",))]


def test_random_against_oracles():
    rng = random.Random(20261106)
    words = [w for n in range(5) for w in itertools.product("ab", repeat=n)]
    comparisons = 0
    for trial in range(900):
        prods, declared = random_grammar(rng)
        nts = nonterminal_set(prods, "S", declared)
        out = eliminate_useless(prods, "S", declared)
        gen, rank, p1, reach = naive_useful(prods, nts, "S")
        assert generating_set(prods, nts) == gen
        expected = [(a, r) for a, r in p1 if a in reach]
        assert out == expected
        comparisons += 1
        # every kept nonterminal is useful: an explicit tree from S through it
        kept_nts = {a for a, _ in out}
        for x in kept_nts:
            tree = witness_tree(prods, nts, "S", x, rank, out)
            leaves = check_tree(out, nts, tree, x)
            assert derives(prods, nts, "S", leaves)
            comparisons += 1
        # the language is unchanged on all short strings
        for w in words if trial < 300 else words[:15]:
            assert derives(prods, nts, "S", w) == derives(out, nts, "S", w)
            comparisons += 1
        # trimming twice changes nothing
        assert eliminate_useless(out, "S", declared) == out
    assert comparisons >= 500


def test_long_chain_without_recursion():
    n = 100000
    prods = [(f"N{i}", (f"N{i + 1}", "a")) for i in range(n)] + [(f"N{n}", ("b",))]
    prods.append((f"N{n}", (f"M{0}",)))  # M0 has no production: not generating
    out = eliminate_useless(prods, "N0", ["M0"])
    assert len(out) == n + 1 and (f"N{n}", ("M0",)) not in out
    prods2 = [(f"N{i}", (f"N{i + 1}",)) for i in range(n)]  # never reaches a terminal
    assert eliminate_useless(prods2, "N0", [f"N{n}"]) == []
