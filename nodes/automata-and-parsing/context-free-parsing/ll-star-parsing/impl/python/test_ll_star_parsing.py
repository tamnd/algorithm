# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ll-star-parsing/. The authors are listed in prov/DGJMDA.jsonl.

import itertools
import random

import pytest

from ll_star_parsing import AllStarParser, ParseError, ll_star_parse


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


def left_recursive_oracle(prods):
    """Brute force: rewrite only the first symbol of sentential forms, from each A."""
    nts = {a for a, _ in prods}
    nullable = {a for a, ws in lang_upto(prods, 0).items() if () in ws}
    for a in nts:
        seen = set()
        todo = [rhs for x, rhs in prods if x == a]
        while todo:
            f = todo.pop()
            if f in seen or len(f) > 12:
                continue
            seen.add(f)
            if not f or f[0] not in nts:
                continue
            if f[0] == a:
                return True
            for x, rhs in prods:
                if x == f[0]:
                    todo.append(rhs + f[1:])
            if f[0] in nullable:
                todo.append(f[1:])
    return False


def expected(prods, start, w):
    """("ok",) if w is in the language, else ("error", k) with k the longest viable prefix."""
    good = productive_only(prods)
    m = len(w)
    if tuple(w) in lang_upto(good, m).get(start, set()):
        return ("ok",)
    pre = prefix_lang(good, m).get(start, set())
    k = 0
    while k < m and tuple(w[: k + 1]) in pre:
        k += 1
    return ("error", k)


def run(parser, w):
    try:
        t = parser.parse(w)
    except ParseError as e:
        return ("error", e.position), None
    return ("ok",), t


# The example of the page: the choice at S needs to read past every a.
EX = [("S", ("A", "c")), ("S", ("A", "d")), ("A", ("a", "A")), ("A", ("b",))]


def test_example_of_the_page():
    p = AllStarParser(EX, "S")
    t = p.parse(list("aabd"))
    assert t == ("S", [("A", ["a", ("A", ["a", ("A", ["b"])])]), "d"])
    assert p.stats == {"decisions": 4, "ll_fallbacks": 0, "max_lookahead": 4}
    s0 = p.dfa_start["S"]
    assert s0 == frozenset({(0, ("a", "A", "c")), (0, ("b", "c")),
                            (1, ("a", "A", "d")), (1, ("b", "d"))})
    s1 = p.dfa_edges[s0]["b"]
    assert p.dfa_edges[s0]["a"] == s0
    assert s1 == frozenset({(0, ("c",)), (1, ("d",))})
    assert p.dfa_edges[s1]["d"] == frozenset({(1, ())})
    for w in ["abc", "bd", "aaaaaaabc"]:
        check_tree(EX, "S", p.parse(list(w)), list(w))
    with pytest.raises(ParseError) as err:
        p.parse(list("aab"))
    assert err.value.position == 3
    with pytest.raises(ParseError) as err:
        p.parse(list("aaba"))
    assert err.value.position == 3


def test_long_lookahead_is_not_ll_k():
    p = AllStarParser(EX, "S")
    for k in range(1, 60):
        w = ["a"] * k + ["b", "d" if k % 2 else "c"]
        check_tree(EX, "S", p.parse(w), w)
    assert p.stats["max_lookahead"] == 61
    assert len(p.dfa_edges) <= 6


def test_full_context_fallback():
    g = [("S", ("x", "A", "a")), ("S", ("y", "A", "b")), ("A", ("a",)), ("A", ())]
    p = AllStarParser(g, "S")
    for w, ok in [("xa", True), ("xaa", True), ("ya", False), ("yb", True), ("yab", True),
                  ("xab", False), ("x", False)]:
        got, t = run(p, list(w))
        assert got == expected(g, "S", list(w)), w
        assert (got == ("ok",)) == ok
        if ok:
            check_tree(g, "S", t, list(w))
    assert p.stats["ll_fallbacks"] >= 2


def test_ambiguous_grammars():
    g = [("S", ("i", "S")), ("S", ("i", "S", "e", "S")), ("S", ("x",))]
    t = ll_star_parse(g, "S", list("iixex"))
    check_tree(g, "S", t, list("iixex"))
    g = [("S", ("A",)), ("S", ("B",)), ("A", ("a",)), ("B", ("a",))]
    assert ll_star_parse(g, "S", ["a"]) == ("S", [("A", ["a"])])
    g = [("S", ("a", "A")), ("S", ("a", "B")), ("A", ()), ("A", ("b",)), ("B", ()), ("B", ("c",))]
    assert ll_star_parse(g, "S", ["a"]) == ("S", ["a", ("A", [])])
    assert ll_star_parse(g, "S", ["a", "c"]) == ("S", ["a", ("B", ["c"])])
    g = [("S", ("S", "S")), ("S", ("a",))]
    with pytest.raises(ValueError):
        AllStarParser(g, "S")


def test_left_recursion_is_rejected():
    for g in ([("E", ("E", "+", "x")), ("E", ("x",))],
              [("S", ("A", "S", "b")), ("S", ("c",)), ("A", ())],
              [("S", ("A", "a")), ("A", ("B",)), ("B", ("S",)), ("B", ("b",))]):
        with pytest.raises(ValueError):
            AllStarParser(g, g[0][0])


def test_empty_input_and_empty_language():
    g = [("S", ("a", "S")), ("S", ())]
    assert ll_star_parse(g, "S", []) == ("S", [])
    g = [("S", ("a", "S"))]
    with pytest.raises(ParseError) as err:
        ll_star_parse(g, "S", [])
    assert err.value.position == 0


def test_deep_input_without_recursion():
    n = 100000
    g = [("S", ("a", "S", "b")), ("S", ())]
    p = AllStarParser(g, "S")
    t = p.parse(["a"] * n + ["b"] * n)
    depth, x = 0, t
    while x[1]:
        depth += 1
        x = x[1][1]
    assert depth == n
    with pytest.raises(ParseError) as err:
        p.parse(["a"] * n + ["b"] * (n - 1))
    assert err.value.position == 2 * n - 1


def test_random_against_brute_force():
    rng = random.Random(20111014)
    checked = accepted = rejected_grammars = 0
    for _ in range(1000):
        g = random_grammar(rng, rng.randint(1, 4), ["a", "b"], eps_prob=0.25)
        if rng.random() < 0.3:
            g.append((rng.choice(["S", "A"]), (rng.choice(["S", "A"]),)))
        if left_recursive_oracle(productive_only(g)):
            with pytest.raises(ValueError):
                AllStarParser(g, "S")
            rejected_grammars += 1
            continue
        p = AllStarParser(g, "S")
        words = [list(w) for m in range(6) for w in itertools.product("ab", repeat=m)]
        for w in words:
            want = expected(g, "S", w)
            got, t = run(p, w)
            assert got == want, (g, w)
            if t is not None:
                check_tree(g, "S", t, w)
                accepted += 1
            checked += 1
        for w in rng.sample(words, 8):
            assert run(AllStarParser(g, "S"), w)[0] == expected(g, "S", w)
    assert checked >= 20000 and accepted >= 600 and rejected_grammars >= 100
