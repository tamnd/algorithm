# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lr-parsing/. The authors are listed in prov/R5HRV8.jsonl.

import itertools
import random

import pytest

from lr_parsing import ParseError, build_table, lr_parse

EXPR = [
    ("E", ("E", "+", "T")),
    ("E", ("T",)),
    ("T", ("T", "*", "F")),
    ("T", ("F",)),
    ("F", ("(", "E", ")")),
    ("F", ("id",)),
]


def lang_upto(prods, max_len):
    """Oracle: for each nonterminal, the strings of length <= max_len that it derives."""
    nts = {a for a, _ in prods}
    lang = {a: set() for a in nts}

    def of(x):
        return lang[x] if x in nts else {(x,)}

    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            cur = {()}
            for x in rhs:
                cur = {u + v for u in cur for v in of(x) if len(u) + len(v) <= max_len}
                if not cur:
                    break
            if not cur <= lang[a]:
                lang[a] |= cur
                changed = True
    return lang


def prefix_lang(prods, max_len):
    """Oracle: for each nonterminal, the prefixes of length <= max_len of the strings it derives.

    Every nonterminal must be productive, so that each symbol after a prefix can be completed.
    """
    nts = {a for a, _ in prods}
    full = lang_upto(prods, max_len)
    pre = {a: set() for a in nts}

    def full_of(x):
        return full[x] if x in nts else {(x,)}

    def pre_of(x):
        return pre[x] if x in nts else {(), (x,)}

    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            new = {()}
            cur = {()}
            for x in rhs:
                new |= {u + v for u in cur for v in pre_of(x) if len(u) + len(v) <= max_len}
                cur = {u + v for u in cur for v in full_of(x) if len(u) + len(v) <= max_len}
            if not new <= pre[a]:
                pre[a] |= new
                changed = True
    return pre


def productive_only(prods):
    """Remove the productions that use a nonterminal deriving no terminal string."""
    nts = {a for a, _ in prods}
    good = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            if a not in good and all(x in good or x not in nts for x in rhs):
                good.add(a)
                changed = True
    return [(a, r) for a, r in prods if a in good and all(x in good or x not in nts for x in r)]


def check_tree(prods, start, tree, tokens):
    """Iteratively check that tree is a parse tree of tokens with root start."""
    nts = {a for a, _ in prods}
    rules = set(prods)
    assert isinstance(tree, tuple) and tree[0] == start
    leaves = []
    todo = [tree]
    while todo:
        t = todo.pop()
        if isinstance(t, str):
            assert t not in nts
            leaves.append(t)
            continue
        a, kids = t
        labels = tuple(k if isinstance(k, str) else k[0] for k in kids)
        assert (a, labels) in rules
        todo.extend(reversed(kids))
    assert leaves == list(tokens)


def random_grammar(rng, n_nt, terms, eps_prob=0.2):
    names = ["S", "A", "B", "C"][:n_nt]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            k = 0 if rng.random() < eps_prob else rng.randint(1, 3)
            prods.append((a, tuple(rng.choice(names + terms) for _ in range(k))))
    return prods



def tree_counts(prods, s):
    """Oracle: number of parse trees of s from each nonterminal, saturated at 2."""
    nts = {a for a, _ in prods}
    n = len(s)
    cnt = {}

    def get(x, i, j):
        if x not in nts:
            return 1 if j == i + 1 and s[i] == x else 0
        return cnt.get((x, i, j), 0)

    changed = True
    while changed:
        changed = False
        for i in range(n + 1):
            for j in range(i, n + 1):
                for a, rhs in prods:
                    ways = {i: 1}
                    for x in rhs:
                        nxt = {}
                        for m, c in ways.items():
                            for e in range(m, j + 1):
                                g = get(x, m, e)
                                if g:
                                    nxt[e] = min(2, nxt.get(e, 0) + c * g)
                        ways = nxt
                    cnt.setdefault(("rule", a, rhs, i, j), 0)
                    v = min(2, ways.get(j, 0))
                    if v != cnt[("rule", a, rhs, i, j)]:
                        cnt[("rule", a, rhs, i, j)] = v
                        changed = True
                for a in nts:
                    v = min(2, sum(cnt.get(("rule", b, r, i, j), 0) for b, r in prods if b == a))
                    if v != cnt.get((a, i, j), 0):
                        cnt[(a, i, j)] = v
                        changed = True
    return lambda a: cnt.get((a, 0, n), 0)


def is_ll1(prods, start):
    """Oracle: the LL(1) test with nullable, FIRST and FOLLOW sets (prods productive)."""
    nts = {a for a, _ in prods}
    null, first, follow = set(), {a: set() for a in nts}, {a: set() for a in nts}
    follow[start].add("$")

    def fo(alpha):
        out = set()
        for x in alpha:
            if x not in nts:
                return out | {x}, False
            out |= first[x]
            if x not in null:
                return out, False
        return out, True

    changed = True
    while changed:
        changed = False
        for a, r in prods:
            f, nl = fo(r)
            if nl and a not in null:
                null.add(a)
                changed = True
            if not f <= first[a]:
                first[a] |= f
                changed = True
            for i, x in enumerate(r):
                if x in nts:
                    g, rn = fo(r[i + 1:])
                    if rn:
                        g = g | follow[a]
                    if not g <= follow[x]:
                        follow[x] |= g
                        changed = True
    seen = {}
    for p, (a, r) in enumerate(prods):
        f, nl = fo(r)
        for t in f | (follow[a] if nl else set()):
            if seen.setdefault((a, t), p) != p:
                return False
    return True


def test_expression_grammar():
    table = build_table(EXPR, "E", 1)
    toks = ["id", "*", "(", "id", "+", "id", ")"]
    check_tree(EXPR, "E", lr_parse(table, toks), toks)
    for toks, pos in [(["id", "+", ")"], 2), ([], 0), (["id", "id"], 1),
                      (["(", "id"], 2), (["id", "+"], 2), ([")"], 0), (["id", ")"], 1)]:
        for k in (1, 2):
            with pytest.raises(ParseError) as e:
                lr_parse(build_table(EXPR, "E", k), toks)
            assert e.value.position == pos
    with pytest.raises(ValueError):
        build_table(EXPR, "E", 0)


def test_trace_counts():
    table = build_table(EXPR, "E", 1)
    assert len(table.states) == 22


def test_lookahead_hierarchy():
    for k in range(0, 4):
        g = [("S", ("A",) + ("b",) * k + ("c",)), ("S", ("B",) + ("b",) * k + ("d",)),
             ("A", ("a",)), ("B", ("a",))]
        for j in range(k + 1):
            with pytest.raises(ValueError):
                build_table(g, "S", j)
        table = build_table(g, "S", k + 1)
        s = ["a"] + ["b"] * k + ["d"]
        check_tree(g, "S", lr_parse(table, s), s)


def test_lr0_language_that_is_not_ll():
    g = [("S", ("A",)), ("S", ("B",)), ("A", ("a", "A", "b")), ("A", ("a", "b")),
         ("B", ("a", "B", "c")), ("B", ("a", "c"))]
    table = build_table(g, "S", 0)
    for s in ["ab", "aacc", "aaabbb"]:
        check_tree(g, "S", lr_parse(table, list(s)), list(s))
    with pytest.raises(ParseError) as e:
        lr_parse(table, list("aabc"))
    assert e.value.position == 3


def test_ambiguous_grammars_are_rejected():
    amb = [("E", ("E", "+", "E")), ("E", ("a",))]
    dangling = [("S", ("i", "S")), ("S", ("i", "S", "e", "S")), ("S", ("x",))]
    cycle = [("S", ("A",)), ("S", ("a",)), ("A", ("S",))]
    two_eps = [("S", ("A",)), ("S", ("B",)), ("A", ()), ("B", ())]
    for g in (amb, dangling, cycle, two_eps):
        for k in (0, 1, 2, 3):
            with pytest.raises(ValueError):
                build_table(g, "S" if g[0][0] == "S" else "E", k)


def test_empty_input_and_epsilon():
    g = [("S", ("A", "S", "b")), ("S", ()), ("A", ("a",)), ("A", ())]
    with pytest.raises(ValueError):
        build_table(g, "S", 1)
    g = [("S", ("a", "S", "b")), ("S", ())]
    for k in (1, 2):
        table = build_table(g, "S", k)
        assert lr_parse(table, []) == ("S", [])
        with pytest.raises(ParseError) as e:
            lr_parse(table, list("abb"))
        assert e.value.position == 2


def test_deep_inputs_have_no_recursion_limit():
    left = [("S", ("S", "a")), ("S", ("a",))]
    right = [("S", ("a", "S")), ("S", ("a",))]
    m = 100000
    for g in (left, right):
        tree = lr_parse(build_table(g, "S", 1), ["a"] * m)
        check_tree(g, "S", tree, ["a"] * m)


def test_random_against_brute_force():
    rng = random.Random(1965)
    checked = built = rejected = 0
    max_len = 6
    for _ in range(2500):
        terms = ["a", "b", "c"][: rng.randint(1, 3)]
        g = productive_only(random_grammar(rng, rng.randint(1, 4), terms, eps_prob=0.25))
        if not g or "S" not in {a for a, _ in g}:
            continue
        k = rng.randint(0, 2)
        try:
            table = build_table(g, "S", k)
        except ValueError:
            rejected += 1
            if k == 1:
                assert not is_ll1(g, "S")
            continue
        built += 1
        # LR(k) grammars are LR(k + 1), and they are unambiguous.
        build_table(g, "S", k + 1)
        for m in range(4):
            for s in itertools.product(terms, repeat=m):
                assert tree_counts(g, s)("S") <= 1
        lang = lang_upto(g, max_len)["S"]
        pre = prefix_lang(g, max_len + 1)["S"]
        for m in range(max_len + 1):
            for s in itertools.product(terms, repeat=m):
                try:
                    tree = lr_parse(table, list(s))
                except ParseError as e:
                    assert s not in lang
                    assert s[: e.position] in pre
                    assert e.position == m or s[: e.position + 1] not in pre
                else:
                    assert s in lang
                    check_tree(g, "S", tree, s)
                checked += 1
    print(built, rejected, checked)
    assert built >= 500 and rejected >= 200 and checked >= 50000
