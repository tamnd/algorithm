# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gll-parsing/. The authors are listed in prov/0BHT8C.jsonl.

import itertools
import random

from gll_parsing import gll

# ---------------------------------------------------------------- oracles


def derived_spans(prods, w):
    """D[A] = the set of (i, j) with A =>* w[i:j], by a fixed point over all substrings."""
    nts = {a for a, _ in prods}
    n = len(w)
    d = {a: set() for a in nts}

    def seq_spans(rhs, i):
        """The ends j such that rhs =>* w[i:j], with the current D."""
        cur = {i}
        for x in rhs:
            nxt = set()
            for k in cur:
                if x in nts:
                    nxt |= {j for (s, j) in d[x] if s == k}
                elif k < n and w[k] == x:
                    nxt.add(k + 1)
            cur = nxt
            if not cur:
                break
        return cur

    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            for i in range(n + 1):
                for j in seq_spans(rhs, i):
                    if (i, j) not in d[a]:
                        d[a].add((i, j))
                        changed = True
    return d, seq_spans


def called_pairs(prods, w):
    """The pairs (A, i) such that a top-down parser reaches a call of A at position i."""
    nts = {a for a, _ in prods}
    d, seq_spans = derived_spans(prods, w)
    called = {(prods[0][0], 0)}
    changed = True
    while changed:
        changed = False
        for (b, k) in list(called):
            for a, rhs in prods:
                if a != b:
                    continue
                for m, x in enumerate(rhs):
                    if x in nts:
                        for i in seq_spans(rhs[:m], k):
                            if (x, i) not in called:
                                called.add((x, i))
                                changed = True
    return called, d, seq_spans


def random_grammar(rng):
    names = ["S", "A", "B"][: rng.randint(1, 3)]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            if rng.random() < 0.25:
                rhs = ()
            else:
                rhs = tuple(rng.choice(names + ["a", "b"]) for _ in range(rng.randint(1, 3)))
            if (a, rhs) not in prods:
                prods.append((a, rhs))
    return prods


def oracle_gss_nodes(g, w):
    """The GSS nodes (p, m + 1, i) a correct GLL run must create: production p of a called
    nonterminal B at k, rhs[m] a nonterminal, and rhs[:m] deriving w[k:i]."""
    nts = {a for a, _ in g}
    called, d, seq_spans = called_pairs(g, w)
    out = set()
    for (b, k) in called:
        for p, (a, rhs) in enumerate(g):
            if a != b:
                continue
            for m, x in enumerate(rhs):
                if x in nts:
                    for i in seq_spans(rhs[:m], k):
                        out.add((p, m + 1, i))
    return out, d


def check_against_oracle(g, w):
    res = gll(g, w)
    nodes, d = oracle_gss_nodes(g, w)
    start = g[0][0]
    assert res.ends == {j for (i, j) in d[start] if i == 0}
    assert res.accepted == ((0, len(w)) in d[start])
    assert res.gss_nodes == len(nodes)
    for (a, i, j) in res.spans:  # sound
        assert (i, j) in d[a]
    for (p, m, i) in nodes:  # complete for every call the search made
        a = g[p][1][m - 1]
        assert {(a, i, j) for (s, j) in d[a] if s == i} <= res.spans
    return res


# ---------------------------------------------------------------- tests

EXPR = [("E", ("E", "+", "E")), ("E", ("n",))]


def test_worked_example_ambiguous_left_recursive():
    w = ["n", "+", "n", "+", "n"]
    res = gll(EXPR, w)
    assert res.accepted
    assert res.ends == {1, 3, 5}
    assert res.gss_nodes == 5
    assert {(a, i, j) for (a, i, j) in res.spans} == {
        ("E", 0, 1), ("E", 0, 3), ("E", 0, 5), ("E", 2, 3), ("E", 2, 5), ("E", 4, 5)}
    assert not gll(EXPR, ["n", "+"]).accepted
    assert not gll(EXPR, ["+", "n"]).accepted


def test_empty_input_and_epsilon():
    assert gll([("S", ())], []).accepted
    assert not gll([("S", ("a",))], []).accepted
    assert gll([("S", ("A", "A", "a")), ("A", ()), ("A", ("a",))], ["a"]).accepted
    assert not gll([("S", ("a",))], ["a", "a"]).accepted


def test_cyclic_and_hidden_left_recursion_terminate():
    g = [("S", ("S",)), ("S", ("S", "S")), ("S", ("a",)), ("S", ())]
    for m in range(6):
        assert gll(g, ["a"] * m).accepted
    assert not gll(g, ["b"]).accepted
    g = [("S", ("A", "S", "b")), ("S", ("a",)), ("A", ())]
    assert gll(g, ["a", "b", "b"]).accepted
    assert not gll(g, ["b"]).accepted


def test_long_inputs_have_no_recursion_limit():
    n = 20000
    w = ["n"] + ["+", "n"] * (n // 2)
    left = [("E", ("E", "+", "n")), ("E", ("n",))]
    res = gll(left, w)
    assert res.accepted and res.descriptors <= 2 * len(w)
    right = [("S", ("a", "S")), ("S", ("b",))]
    res = gll(right, ["a"] * n + ["b"])
    assert res.accepted and res.descriptors <= 4 * (n + 1)
    assert not gll(right, ["a"] * n).accepted


def test_matches_language_on_random_grammars_and_inputs():
    rng = random.Random(23)
    grammars = 0
    flags = {"eps": 0, "left": 0}
    for _ in range(600):
        g = random_grammar(rng)
        for m in range(0, 7):
            for w in itertools.product("ab", repeat=m):
                check_against_oracle(g, list(w))
        grammars += 1
        flags["eps"] += any(not r for _, r in g)
        flags["left"] += any(r and r[0] == a for a, r in g)
    assert grammars >= 500 and flags["eps"] >= 100 and flags["left"] >= 100


def test_random_longer_inputs():
    rng = random.Random(41)
    for _ in range(300):
        g = random_grammar(rng)
        w = [rng.choice("ab") for _ in range(rng.randint(5, 8))]
        check_against_oracle(g, w)


def test_size_bounds():
    """Descriptors are at most s^2 (n+1)^2 and GSS nodes at most s (n+1), s the number of slots."""
    rng = random.Random(5)
    for _ in range(300):
        g = random_grammar(rng)
        s = sum(len(r) + 1 for _, r in g)
        w = [rng.choice("ab") for _ in range(rng.randint(0, 8))]
        res = gll(g, w)
        n = len(w)
        assert res.gss_nodes <= s * (n + 1)
        assert res.descriptors <= s * (s * (n + 1) + 1) * (n + 1)
        assert res.gss_edges <= res.gss_nodes * (s * (n + 1) + 1)
