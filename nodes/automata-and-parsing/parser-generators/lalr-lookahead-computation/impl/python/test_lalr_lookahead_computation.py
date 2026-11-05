# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lalr-lookahead-computation/. The authors are listed in prov/VAAJVS.jsonl.

import random

from lalr_lookahead_computation import END, digraph, lalr_lookaheads

# ---------------------------------------------------------------- oracles


def reduce_grammar(prods):
    """Drop unproductive and unreachable nonterminals; None if the start symbol is unproductive."""
    nts = {a for a, _ in prods}
    productive = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            if a not in productive and all(x not in nts or x in productive for x in rhs):
                productive.add(a)
                changed = True
    start = prods[0][0]
    if start not in productive:
        return None
    prods = [(a, r) for a, r in prods if a in productive and all(x not in nts or x in productive for x in r)]
    reach = {start}
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            if a in reach:
                for x in rhs:
                    if x in nts and x not in reach:
                        reach.add(x)
                        changed = True
    return [(a, r) for a, r in prods if a in reach]


def merged_lr1_lookaheads(prods):
    """Reference: canonical LR(1) states merged by core.

    Returns {(LR(0) kernel, production): lookaheads} for every completed item,
    with production numbers of the augmented grammar (0 is S' -> S).
    """
    s0 = prods[0][0]
    pa = [(s0 + "'", (s0,))] + list(prods)
    nts = {a for a, _ in pa}
    nullable = set()
    first = {a: set() for a in nts}
    changed = True
    while changed:
        changed = False
        for a, rhs in pa:
            if a not in nullable and all(x in nullable for x in rhs):
                nullable.add(a)
                changed = True
            for x in rhs:
                add = first[x] if x in nts else {x}
                if not add <= first[a]:
                    first[a] |= add
                    changed = True
                if x not in nullable:
                    break

    def closure(items):
        out = set(items)
        todo = list(items)
        while todo:
            p, d, la = todo.pop()
            rhs = pa[p][1]
            if d < len(rhs) and rhs[d] in nts:
                las = set()
                for x in rhs[d + 1:]:
                    las |= first[x] if x in nts else {x}
                    if x not in nullable:
                        break
                else:
                    las.add(la)
                for j, (b, _) in enumerate(pa):
                    if b == rhs[d]:
                        for t in las:
                            if (j, 0, t) not in out:
                                out.add((j, 0, t))
                                todo.append((j, 0, t))
        return frozenset(out)

    def kernel(state):
        return frozenset((p, d) for p, d, _ in state if d > 0 or p == 0)

    states = [closure({(0, 0, END)})]
    seen = set(states)
    result = {}
    q = 0
    while q < len(states):
        st = states[q]
        k = kernel(st)
        for p, d, la in st:
            rhs = pa[p][1]
            if d == len(rhs):
                if p != 0:
                    result.setdefault((k, p), set()).add(la)
                continue
            nxt = closure({(pp, dd + 1, ll) for pp, dd, ll in st if dd < len(pa[pp][1]) and pa[pp][1][dd] == rhs[d]})
            if nxt not in seen:
                seen.add(nxt)
                states.append(nxt)
        q += 1
    return result


def mine_by_kernel(res):
    return {(res.kernels[q], p): set(v) for (q, p), v in res.la.items()}


def reach_union(nodes, rel, base):
    """Reference for digraph: the union of base over every node reachable from x, by search."""
    out = {}
    for x in nodes:
        seen = {x}
        todo = [x]
        acc = set()
        while todo:
            y = todo.pop()
            acc |= set(base[y])
            for z in rel[y]:
                if z not in seen:
                    seen.add(z)
                    todo.append(z)
        out[x] = frozenset(acc)
    return out


def fixpoint(nodes, rel, base):
    """Second reference: iterate F(x) = base(x) united with F(y) for x rel y until nothing changes."""
    f = {x: set(base[x]) for x in nodes}
    changed = True
    while changed:
        changed = False
        for x in nodes:
            for y in rel[x]:
                if not f[y] <= f[x]:
                    f[x] |= f[y]
                    changed = True
    return {x: frozenset(s) for x, s in f.items()}


def random_grammar(rng, names=("S", "A", "B", "C"), terms=("a", "b", "c")):
    names = list(names[: rng.randint(1, len(names))])
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            if rng.random() < 0.25:
                rhs = ()
            else:
                rhs = tuple(rng.choice(names + list(terms)) for _ in range(rng.randint(1, 3)))
            if (a, rhs) not in prods:
                prods.append((a, rhs))
    return prods


def symbol(res, p):
    return res.productions[p][0]


# ---------------------------------------------------------------- tests

POINTER = [("S", ("L", "=", "R")), ("S", ("R",)), ("L", ("*", "R")), ("L", ("id",)), ("R", ("L",))]


def test_worked_example_pointer_grammar():
    res = lalr_lookaheads(POINTER)
    assert len(res.kernels) == 10
    assert sorted(res.transitions) == [(0, "L"), (0, "R"), (0, "S"), (4, "L"), (4, "R"), (6, "L"), (6, "R")]
    assert res.dr[(0, "L")] == {"="} and res.dr[(0, "S")] == {END}
    assert sorted(res.includes[(4, "R")]) == [(0, "L"), (4, "L"), (6, "L")]
    assert res.includes[(4, "L")] == [(4, "R")]
    assert res.follow[(0, "L")] == {"=", END}
    assert res.follow[(4, "L")] == res.follow[(4, "R")] == {"=", END}
    assert res.follow[(6, "L")] == {END}
    # state 2 = {S -> L . = R, R -> L .}: the reduction R -> L has lookahead $ only, so no conflict on =
    assert res.kernels[2] == frozenset({(1, 1), (5, 1)})
    assert res.la[(2, 5)] == {END}
    assert res.la[(7, 5)] == {"=", END}
    assert res.la[(5, 4)] == {"=", END}
    assert res.la[(9, 1)] == {END}
    assert mine_by_kernel(res) == merged_lr1_lookaheads(POINTER)


def test_reads_through_a_nullable_symbol():
    g = [("S", ("A", "B", "c")), ("A", ("a",)), ("B", ("b",)), ("B", ())]
    res = lalr_lookaheads(g)
    assert res.dr[(0, "A")] == {"b"}
    assert res.reads[(0, "A")] == [(2, "B")]
    assert res.read[(0, "A")] == {"b", "c"}
    assert res.la[(3, 2)] == {"b", "c"}  # A -> a .
    assert res.la[(2, 4)] == {"c"}  # B -> .
    assert mine_by_kernel(res) == merged_lr1_lookaheads(g)


def test_empty_language_word_epsilon_and_left_recursion():
    g = [("S", ())]
    res = lalr_lookaheads(g)
    assert res.la == {(0, 1): frozenset({END})}
    g = [("E", ("E", "+", "n")), ("E", ("n",))]
    res = lalr_lookaheads(g)
    assert mine_by_kernel(res) == merged_lr1_lookaheads(g)
    assert all(v == {"+", END} for v in res.la.values())


def test_ambiguous_grammar_keeps_both_lookaheads():
    g = [("E", ("E", "+", "E")), ("E", ("n",))]
    res = lalr_lookaheads(g)
    assert mine_by_kernel(res) == merged_lr1_lookaheads(g)
    # the completed item E -> E + E . sits beside the shift on +: a shift-reduce conflict
    q = next(q for (q, p) in res.la if p == 1)
    assert "+" in res.la[(q, 1)] and (q, "+") in res.goto


def test_digraph_against_reachability_on_random_graphs():
    rng = random.Random(3)
    for _ in range(800):
        n = rng.randint(0, 14)
        nodes = list(range(n))
        rel = {x: [] for x in nodes}
        for _ in range(rng.randint(0, 3 * n + 1)):
            if n:
                rel[rng.randrange(n)].append(rng.randrange(n))
        base = {x: {rng.randrange(6) for _ in range(rng.randint(0, 2))} for x in nodes}
        got = digraph(nodes, rel, base)
        assert got == reach_union(nodes, rel, base)
        assert got == fixpoint(nodes, rel, base)


def test_digraph_on_a_long_cycle_has_no_recursion_limit():
    n = 50000
    nodes = list(range(n))
    rel = {x: [x + 1] for x in range(n - 1)}
    rel[n - 1] = [0]
    base = {x: {x % 7} if x % 1000 == 0 else set() for x in nodes}
    got = digraph(nodes, rel, base)
    assert all(v == frozenset(range(7)) for v in got.values())
    rel[n - 1] = []
    got = digraph(nodes, rel, base)
    assert got[n - 1] == set() and got[0] == frozenset(range(7))


def test_long_unit_chain_grammar():
    k = 3000
    g = [(f"A{i}", (f"A{i + 1}",)) for i in range(k)] + [(f"A{k}", ("x",)), (f"A{k}", ())]
    res = lalr_lookaheads(g)
    assert all(v == {END} for v in res.la.values())
    assert len(res.la) == k + 2


def test_matches_merged_lr1_on_random_grammars():
    rng = random.Random(17)
    compared = 0
    with_epsilon = 0
    for _ in range(900):
        g = reduce_grammar(random_grammar(rng))
        if g is None:
            continue
        res = lalr_lookaheads(g)
        assert mine_by_kernel(res) == merged_lr1_lookaheads(g), g
        assert res.read == fixpoint(res.transitions, res.reads, res.dr)
        assert res.follow == fixpoint(res.transitions, res.includes, res.read)
        compared += 1
        with_epsilon += any(not rhs for _, rhs in g)
    assert compared >= 500 and with_epsilon >= 100


def test_lookaheads_lie_in_follow_and_reads_needs_nullable():
    rng = random.Random(29)
    checked = 0
    for _ in range(700):
        g = reduce_grammar(random_grammar(rng))
        if g is None:
            continue
        res = lalr_lookaheads(g)
        prods = res.productions
        nts = {a for a, _ in prods}
        # FOLLOW sets of the augmented grammar, by the usual fixed point
        nullable = set()
        first = {a: set() for a in nts}
        follow = {a: set() for a in nts}
        follow[prods[0][0]].add(END)
        changed = True
        while changed:
            changed = False
            for a, rhs in prods:
                if a not in nullable and all(x in nullable for x in rhs):
                    nullable.add(a)
                    changed = True
                for x in rhs:
                    add = first[x] if x in nts else {x}
                    if not add <= first[a]:
                        first[a] |= add
                        changed = True
                    if x not in nullable:
                        break
                trailer = set(follow[a])
                for x in reversed(rhs):
                    if x in nts:
                        if not trailer <= follow[x]:
                            follow[x] |= trailer
                            changed = True
                        trailer = trailer | first[x] if x in nullable else set(first[x])
                    else:
                        trailer = {x}
        for (q, p), las in res.la.items():
            assert las and las <= follow[symbol(res, p)]
        union = {}
        for (p, a) in res.transitions:
            union.setdefault(a, set()).update(res.follow[(p, a)])
        assert union == {a: follow[a] for a in nts if a != prods[0][0]}
        for (p, a), succ in res.reads.items():
            for (r, c) in succ:
                assert r == res.goto[(p, a)] and c in nullable
        checked += 1
    assert checked >= 500
