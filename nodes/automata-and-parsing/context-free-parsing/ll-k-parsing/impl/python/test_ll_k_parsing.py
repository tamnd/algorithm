# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ll-k-parsing/. The authors are listed in prov/VNTPSZ.jsonl.

import itertools
import random

import pytest

from ll_k_parsing import ParseError, build_tables, first_k, llk_parse

EXPR = [
    ("E", ("T", "E'")),
    ("E'", ("+", "T", "E'")),
    ("E'", ()),
    ("T", ("F", "T'")),
    ("T'", ("*", "F", "T'")),
    ("T'", ()),
    ("F", ("(", "E", ")")),
    ("F", ("id",)),
]

# LL(2) but not strong LL(2): the context of A decides.
CLASSIC = [
    ("S", ("a", "A", "a", "a")),
    ("S", ("b", "A", "b", "a")),
    ("A", ("b",)),
    ("A", ()),
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



def first_k_oracle(prods, k):
    """FIRST_k from the brute-force languages: short sentences and length-k prefixes."""
    full = lang_upto(prods, k)
    pre = prefix_lang(prods, k)
    nts = {a for a, _ in prods}

    def of(form):
        fulls = {()}
        out = set()
        for x in form:
            px = pre[x] if x in nts else {(), (x,)}
            fx = full[x] if x in nts else {(x,)}
            out |= {u + v for u in fulls for v in px if len(u + v) == k}
            fulls = {u + v for u in fulls for v in fx if len(u + v) <= k}
        out |= fulls
        return out

    return of


def ll_k_by_definition(prods, start, k, depth=9, max_form=12):
    """Search the left-sentential forms w A alpha for two productions of A whose
    FIRST_k(beta alpha) meet. Returns False when it finds such a pair."""
    nts = {a for a, _ in prods}
    fk = first_k_oracle(prods, k)
    by = {}
    for a, r in prods:
        by.setdefault(a, []).append(r)
    seen = set()
    front = {(start,)}
    for _ in range(depth):
        nxt = set()
        for f in front:
            i = next((j for j, s in enumerate(f) if s in nts), None)
            if i is None:
                continue
            a, alpha = f[i], f[i + 1:]
            if (a, alpha) not in seen:
                seen.add((a, alpha))
                sets = [fk(r + alpha) for r in by[a]]
                for x, y in itertools.combinations(range(len(sets)), 2):
                    if sets[x] & sets[y]:
                        return False
            for r in by[a]:
                g = f[:i] + r + alpha
                if len(g) <= max_form:
                    nxt.add(g)
        front = nxt
    return True


def test_expression_grammar():
    toks = ["id", "+", "id", "*", "id"]
    tree = llk_parse(EXPR, "E", toks, 1)
    check_tree(EXPR, "E", tree, toks)
    tables = build_tables(EXPR, "E", 2)
    for toks, pos in [(["id", "+", ")"], 2), ([], 0), (["id", "id"], 1),
                      (["(", "id"], 2), (["id", "+"], 2), ([")"], 0)]:
        for k in (1, 2, 3):
            with pytest.raises(ParseError) as e:
                llk_parse(EXPR, "E", toks, k)
            assert e.value.position == pos
    tree = llk_parse(EXPR, "E", ["(", "id", ")"], 2, tables)
    check_tree(EXPR, "E", tree, ["(", "id", ")"])


def test_classic_needs_context():
    with pytest.raises(ValueError):
        build_tables(CLASSIC, "S", 1)
    tables = build_tables(CLASSIC, "S", 2)
    # A occurs in two contexts, so it has two tables.
    assert sorted(len(t) for (a, _), t in zip(tables.keys, tables.tables) if a == "A") == [2, 2]
    for s in ["abaa", "aaa", "bbba", "bba"]:
        check_tree(CLASSIC, "S", llk_parse(CLASSIC, "S", list(s), 2, tables), list(s))
    with pytest.raises(ParseError) as e:
        llk_parse(CLASSIC, "S", list("abba"), 2, tables)
    assert e.value.position == 2


def test_lookahead_hierarchy():
    for k in range(1, 5):
        g = [("S", ("a",) * k + ("b",)), ("S", ("a",) * k + ("c",))]
        with pytest.raises(ValueError):
            build_tables(g, "S", k)
        tables = build_tables(g, "S", k + 1)
        s = ["a"] * k + ["c"]
        check_tree(g, "S", llk_parse(g, "S", s, k + 1, tables), s)


def test_rejected_grammars():
    left = [("E", ("E", "+", "a")), ("E", ("a",))]
    amb = [("E", ("E", "+", "E")), ("E", ("a",))]
    cycle = [("S", ("A",)), ("S", ("a",)), ("A", ("S",))]
    dangling = [("S", ("i", "S")), ("S", ("i", "S", "e", "S")), ("S", ("x",))]
    for g in (left, amb, cycle, dangling):
        for k in (1, 2, 3):
            with pytest.raises(ValueError):
                build_tables(g, g[0][0], k)


def test_empty_input_and_nullable_start():
    g = [("S", ("a", "S", "b")), ("S", ())]
    for k in (1, 2):
        assert llk_parse(g, "S", [], k) == ("S", [])
        check_tree(g, "S", llk_parse(g, "S", list("aabb"), k), list("aabb"))
        with pytest.raises(ParseError) as e:
            llk_parse(g, "S", list("aab"), k)
        assert e.value.position == 3


def test_first_k_matches_oracle():
    rng = random.Random(7)
    for _ in range(300):
        g = productive_only(random_grammar(rng, rng.randint(1, 4), ["a", "b"]))
        if not g:
            continue
        for k in (1, 2, 3):
            fk = first_k_oracle(g, k)
            got = first_k(g, k)
            for a in got:
                assert got[a] == fk((a,))


def test_deep_input_has_no_recursion_limit():
    g = [("S", ("(", "S", ")")), ("S", ())]
    m = 100000
    toks = ["("] * m + [")"] * m
    tree = llk_parse(g, "S", toks, 2)
    depth = 0
    while tree[1]:
        tree = tree[1][1]
        depth += 1
    assert depth == m


def test_random_against_brute_force():
    rng = random.Random(2024)
    checked = grammars = rejected = 0
    max_len = 6
    for _ in range(3000):
        terms = ["a", "b", "c"][: rng.randint(1, 3)]
        g = productive_only(random_grammar(rng, rng.randint(1, 4), terms, eps_prob=0.25))
        if not g or g[0][0] != "S" or "S" not in {a for a, _ in g}:
            continue
        k = rng.randint(1, 3)
        oracle = ll_k_by_definition(g, "S", k)
        try:
            tables = build_tables(g, "S", k)
        except ValueError:
            assert not oracle
            rejected += 1
            continue
        assert oracle
        grammars += 1
        lang = lang_upto(g, max_len)["S"]
        pre = prefix_lang(g, max_len + 1)["S"]
        for m in range(max_len + 1):
            for s in itertools.product(terms, repeat=m):
                try:
                    tree = llk_parse(g, "S", list(s), k, tables)
                except ParseError as e:
                    assert s not in lang
                    pos = e.position
                    assert s[:pos] in pre
                    assert pos == m or s[: pos + 1] not in pre
                else:
                    assert s in lang
                    check_tree(g, "S", tree, s)
                checked += 1
    print(grammars, rejected, checked)
    assert grammars >= 500 and rejected >= 200 and checked >= 50000
