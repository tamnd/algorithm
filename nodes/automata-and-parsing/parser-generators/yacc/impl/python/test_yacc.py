# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yacc/. The authors are listed in prov/NSTRHE.jsonl.

import itertools
import random

from yacc import END, ERROR, Yacc

M = 10007

PREC = [("nonassoc", ["<"]), ("left", ["+", "-"]), ("left", ["*"]), ("right", ["^"]), ("right", ["NEG"])]
BINARY = {
    "+": lambda a, b: (a + b) % M,
    "-": lambda a, b: (a - b) % M,
    "*": lambda a, b: (a * b) % M,
    "^": lambda a, b: (2 * a + 3 * b) % M,  # any operation that is not associative will do
    "<": lambda a, b: int(a < b),
}


def expr_productions():
    prods = [("E", ("E", op, "E"), (lambda v, f=f: f(v[0], v[2]))) for op, f in BINARY.items()]
    prods.append(("E", ("-", "E"), (lambda v: (-v[1]) % M), "NEG"))
    prods.append(("E", ("(", "E", ")"), (lambda v: v[1])))
    prods.append(("E", ("num",)))
    return prods


def stmt_productions():
    return [
        ("L", ("L", "S"), (lambda v: v[0] + [v[1]])),
        ("L", (), (lambda v: [])),
        ("S", ("E", ";")),
        ("S", (ERROR, ";"), (lambda v: "ERR")),
    ] + expr_productions()


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


def lalr_by_merging(prods):
    """Reference table: canonical LR(1) states merged by core; cells keyed by (LR(0) kernel, token)."""
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

    start = closure({(0, 0, END)})
    states = [start]
    seen = {start}
    cells = {}
    q = 0
    while q < len(states):
        st = states[q]
        k = kernel(st)
        for p, d, la in st:
            rhs = pa[p][1]
            if d == len(rhs):
                cells.setdefault((k, la), set()).add(("reduce", p))
                continue
            nxt = closure({(pp, dd + 1, ll) for pp, dd, ll in st
                           if dd < len(pa[pp][1]) and pa[pp][1][dd] == rhs[d]})
            if rhs[d] not in nts:
                cells.setdefault((k, rhs[d]), set()).add(("shift", kernel(nxt)))
            if nxt not in seen:
                seen.add(nxt)
                states.append(nxt)
        q += 1
    return cells


def is_prefix(prods, u):
    """Earley recognition of prefixes: True when u is a prefix of some sentence (reduced grammar)."""
    nts = {a for a, _ in prods}
    nullable = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            if a not in nullable and all(x in nullable for x in rhs):
                nullable.add(a)
                changed = True
    start = prods[0][0]
    sets = [set((p, 0, 0) for p, (a, _) in enumerate(prods) if a == start)]
    for j in range(len(u) + 1):
        todo = list(sets[j])
        while todo:
            p, d, i = todo.pop()
            rhs = prods[p][1]
            new = []
            if d < len(rhs) and rhs[d] in nts:
                new += [(q, 0, j) for q, (b, _) in enumerate(prods) if b == rhs[d]]
                if rhs[d] in nullable:
                    new.append((p, d + 1, i))
            elif d == len(rhs):
                a = prods[p][0]
                new += [(pp, dd + 1, ii) for pp, dd, ii in list(sets[i])
                        if dd < len(prods[pp][1]) and prods[pp][1][dd] == a]
            for item in new:
                if item not in sets[j]:
                    sets[j].add(item)
                    todo.append(item)
        if j == len(u):
            return bool(sets[j])
        nxt = set((p, d + 1, i) for p, d, i in sets[j]
                  if d < len(prods[p][1]) and prods[p][1][d] == u[j])
        if not nxt:
            return False
        sets.append(nxt)
    return True


def lang_upto(prods, max_len):
    nts = {a for a, _ in prods}
    lang = {a: set() for a in nts}
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            cur = {()}
            for x in rhs:
                src = lang[x] if x in nts else {(x,)}
                cur = {u + v for u in cur for v in src if len(u) + len(v) <= max_len}
            if not cur <= lang[a]:
                lang[a] |= cur
                changed = True
    return lang


def random_grammar(rng):
    names = ["S", "A", "B"][: rng.randint(1, 3)]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            rhs = () if rng.random() < 0.2 else tuple(rng.choice(names + ["a", "b"]) for _ in range(rng.randint(1, 3)))
            if (a, rhs) not in prods:
                prods.append((a, rhs))
    return prods


def tree_yield_ok(tree, prods, w):
    """Check that tree = (p, children) is a derivation tree of w (iteratively)."""
    nts = {a for a, _ in prods}
    out = []
    stack = [(tree, prods[0][0])]
    while stack:
        node, sym = stack.pop()
        if sym not in nts:
            if node != sym:
                return False
            out.append(node)
            continue
        p, kids = node
        if prods[p - 1][0] != sym or len(kids) != len(prods[p - 1][1]):
            return False
        for kid, s in reversed(list(zip(kids, prods[p - 1][1]))):
            stack.append((kid, s))
    return tuple(out) == tuple(w)


LEVEL = {"<": (1, "nonassoc"), "+": (2, "left"), "-": (2, "left"), "*": (3, "left"), "^": (4, "right")}
NEG = 5


def all_trees(toks):
    """Every parse tree of toks for the ambiguous expression grammar, bottom-up over intervals."""
    n = len(toks)
    trees = {}
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length
            out = []
            if length == 1 and toks[i][0] == "num":
                out.append(("num", toks[i][1]))
            if toks[i][0] == "-" and length >= 2:
                out += [("neg", t) for t in trees[(i + 1, j)]]
            if toks[i][0] == "(" and toks[j - 1][0] == ")" and length >= 3:
                out += [("par", t) for t in trees[(i + 1, j - 1)]]
            for k in range(i + 1, j - 1):
                if toks[k][0] in BINARY:
                    for left in trees[(i, k)]:
                        for right in trees[(k + 1, j)]:
                            out.append(("bin", toks[k][0], left, right))
            trees[(i, j)] = out
    return trees.get((0, n), [])


def respects_precedence(tree):
    stack = [tree]
    while stack:
        t = stack.pop()
        if t[0] == "num":
            continue
        if t[0] in ("neg", "par"):
            if t[0] == "neg" and t[1][0] == "bin" and LEVEL[t[1][1]][0] <= NEG:
                return False
            stack.append(t[1])
            continue
        _, op, left, right = t
        lv, assoc = LEVEL[op]
        if left[0] == "bin":
            l2 = LEVEL[left[1]][0]
            if l2 < lv or (l2 == lv and assoc != "left"):
                return False
        if left[0] == "neg" and NEG < lv:
            return False
        if right[0] == "bin":
            r2 = LEVEL[right[1]][0]
            if r2 < lv or (r2 == lv and assoc != "right"):
                return False
        stack += [left, right]
    return True


def evaluate(tree):
    """Value of an expression tree, computed with an explicit stack."""
    out = {}
    stack = [(tree, False)]
    while stack:
        t, done = stack.pop()
        if t[0] == "num":
            out[id(t)] = t[1]
        elif not done:
            stack.append((t, True))
            stack += [(c, False) for c in t[1:] if isinstance(c, tuple)]
        elif t[0] == "neg":
            out[id(t)] = (-out[id(t[1])]) % M
        elif t[0] == "par":
            out[id(t)] = out[id(t[1])]
        else:
            out[id(t)] = BINARY[t[1]](out[id(t[2])], out[id(t[3])])
    return out[id(tree)]


def random_expression(rng, depth):
    if depth == 0 or rng.random() < 0.3:
        return [("num", rng.randrange(10))]
    r = rng.random()
    if r < 0.15:
        return [("-", "-")] + random_expression(rng, depth - 1)
    if r < 0.25:
        return [("(", "(")] + random_expression(rng, depth - 1) + [(")", ")")]
    op = rng.choice(list(BINARY))
    return random_expression(rng, depth - 1) + [(op, op)] + random_expression(rng, depth - 1)


# ---------------------------------------------------------------- worked examples


def test_calculator_conflicts_are_settled_by_precedence():
    y = Yacc([("E", ("E", "+", "E"), lambda v: v[0] + v[2]),
              ("E", ("E", "*", "E"), lambda v: v[0] * v[2]),
              ("E", ("(", "E", ")"), lambda v: v[1]),
              ("E", ("num",))],
             [("left", ["+"]), ("left", ["*"])])
    assert len(y.kernels) == 10
    raw_conflicts = {k: v for k, v in y.raw.items() if len(v) > 1}
    assert len(raw_conflicts) == 4
    assert y.resolved_by_precedence == 4 and y.conflicts == []
    plus_state = y.goto[(y.goto[(y.goto[(0, "E")], "+")], "E")]
    times_state = y.goto[(y.goto[(y.goto[(0, "E")], "*")], "E")]
    assert y.action[(plus_state, "+")] == ("reduce", 1)
    assert y.action[(plus_state, "*")][0] == "shift"
    assert y.action[(times_state, "+")] == ("reduce", 2)
    assert y.action[(times_state, "*")] == ("reduce", 2)
    r = y.parse([("num", 2), "+", ("num", 3), "*", ("num", 4)])
    assert r.accepted and r.value == 14 and r.errors == []
    assert y.parse([("num", 2), "*", ("num", 3), "+", ("num", 4)]).value == 10


def test_without_precedence_the_defaults_apply():
    y = Yacc([("E", ("E", "+", "E"), lambda v: v[0] + v[2]),
              ("E", ("E", "*", "E"), lambda v: v[0] * v[2]),
              ("E", ("num",))])
    assert len(y.conflicts) == 4 and all(c.kind == "shift/reduce" for c in y.conflicts)
    # shift everywhere makes both operators right-associative with equal precedence
    assert y.parse([("num", 2), "*", ("num", 3), "+", ("num", 4)]).value == 14


def test_dangling_else_shifts():
    y = Yacc([("S", ("if", "S"), lambda v: ("if", v[1])),
              ("S", ("if", "S", "else", "S"), lambda v: ("ifelse", v[1], v[3])),
              ("S", ("a",))])
    assert [(c.kind, c.token) for c in y.conflicts] == [("shift/reduce", "else")]
    r = y.parse(["if", "if", "a", "else", "a"])
    assert r.value == ("if", ("ifelse", "a", "a"))


def test_reduce_reduce_takes_the_earlier_rule():
    y = Yacc([("S", ("A",)), ("S", ("B",)), ("A", ("x",), lambda v: "A"), ("B", ("x",), lambda v: "B")])
    assert [(c.kind, c.token, c.chosen) for c in y.conflicts] == [("reduce/reduce", END, ("reduce", 3))]
    assert y.parse(["x"]).value == "A"


def test_nonassoc_makes_chains_an_error():
    y = Yacc(expr_productions(), PREC)
    assert y.conflicts == []
    ok = y.parse([("num", 1), "<", ("num", 2)])
    assert ok.accepted and ok.value == 1
    bad = y.parse([("num", 1), "<", ("num", 2), "<", ("num", 3)])
    assert not bad.accepted and bad.errors == [3]


def test_error_recovery_trace():
    y = Yacc(stmt_productions(), PREC)
    assert y.conflicts == []
    toks = [("num", 1), "+", ";", ("num", 3), ("num", 4), ";", ("num", 2), ";", ("num", 5), "*", ("num", 6), ";"]
    r = y.parse(toks)
    assert r.accepted
    assert r.value == ["ERR", "ERR", 2, 30]
    # the second error comes 2 shifts after the recovery from the first, so it is not reported
    assert r.errors == [2]
    spaced = toks[:3] + [("num", 7), ";"] + toks[3:]
    assert y.parse(spaced).value == ["ERR", 7, "ERR", 2, 30]
    assert y.parse(spaced).errors == [2, 6]
    assert not y.parse([("num", 1), "+"]).accepted


def test_empty_input_epsilon_and_left_recursion():
    y = Yacc([("L", ("L", "x"), lambda v: v[0] + 1), ("L", (), lambda v: 0)])
    assert y.conflicts == []
    assert y.parse([]).value == 0
    assert y.parse(["x"] * 50).value == 50
    assert y.parse(["y"]).errors == [0]
    r = Yacc([("S", ("a",))]).parse([])
    assert not r.accepted and r.errors == [0]


def test_deep_input_has_no_recursion_limit():
    y = Yacc([("E", ("(", "E", ")"), lambda v: v[1] + 1), ("E", ("num",), lambda v: 0)])
    n = 20000
    assert y.parse(["("] * n + [("num", 0)] + [")"] * n).value == n


# ---------------------------------------------------------------- random tests


def test_lalr_table_matches_merged_lr1_on_random_grammars():
    rng = random.Random(11)
    compared = 0
    for _ in range(700):
        g = reduce_grammar(random_grammar(rng))
        if g is None:
            continue
        y = Yacc(g)
        ref = lalr_by_merging(g)
        mine = {}
        for (s, t), acts in y.raw.items():
            mine[(y.kernels[s], t)] = {(a[0], y.kernels[a[1]]) if a[0] == "shift" else a for a in acts}
        assert mine == ref, g
        compared += 1
    assert compared >= 500


def test_conflict_free_tables_parse_the_language_and_find_errors_early():
    rng = random.Random(5)
    checked = 0
    for _ in range(900):
        g = reduce_grammar(random_grammar(rng))
        if g is None:
            continue
        prods = [(a, rhs, (lambda v, p=p: (p, tuple(v)))) for p, (a, rhs) in enumerate(g, start=1)]
        y = Yacc(prods)
        if y.conflicts:
            continue
        lang = lang_upto(g, 5)[g[0][0]]
        for n in range(6):
            for w in itertools.product("ab", repeat=n):
                r = y.parse(list(w))
                assert r.accepted == (w in lang), (g, w)
                if r.accepted:
                    assert tree_yield_ok(r.value, g, w)
                else:
                    first_bad = next(i for i in range(n + 1) if not is_prefix(g, w[: i + 1]) or i == n)
                    assert r.errors == [first_bad], (g, w)
                checked += 1
    assert checked >= 500


def test_precedence_matches_the_unique_disambiguated_tree():
    rng = random.Random(9)
    y = Yacc(expr_productions(), PREC)
    for _ in range(1500):
        if rng.random() < 0.7:
            toks = random_expression(rng, rng.randint(1, 3))
        else:
            toks = [rng.choice([("num", 1), ("num", 2), ("+", "+"), ("*", "*"), ("-", "-"), ("<", "<"),
                                ("^", "^"), ("(", "("), (")", ")")]) for _ in range(rng.randint(0, 7))]
        if len(toks) > 11:
            continue
        good = [t for t in all_trees(toks) if respects_precedence(t)]
        assert len(good) <= 1, toks
        r = y.parse(toks)
        assert r.accepted == bool(good), toks
        if good:
            assert r.value == evaluate(good[0]), toks


def test_error_recovery_matches_statement_by_statement_oracle():
    rng = random.Random(13)
    y = Yacc(stmt_productions(), PREC)
    for _ in range(800):
        toks = []
        for _ in range(rng.randint(0, 4)):
            if rng.random() < 0.6:
                seg = random_expression(rng, 2)
            else:
                seg = [rng.choice([("num", 3), ("+", "+"), ("*", "*"), ("(", "("), (")", ")")])
                       for _ in range(rng.randint(0, 3))]
            toks += seg + [(";", ";")]
        if rng.random() < 0.2:
            toks += [("num", 1)]
        segments = [[]]
        for t in toks:
            if t[0] == ";":
                segments.append([])
            else:
                segments[-1].append(t)
        expect = []
        any_bad = False
        for seg in segments[:-1]:
            good = [t for t in all_trees(seg) if respects_precedence(t)] if len(seg) <= 11 else None
            if good is None:
                break
            if good:
                expect.append(evaluate(good[0]))
            else:
                expect.append("ERR")
                any_bad = True
        else:
            r = y.parse(toks)
            if segments[-1]:
                assert not r.accepted and r.errors, toks
            else:
                assert r.accepted and r.value == expect, toks
                assert bool(r.errors) == any_bad, toks


def test_unary_minus_needs_prec():
    with_prec = Yacc(expr_productions(), PREC)
    without = Yacc([p[:3] for p in expr_productions()], PREC)
    toks = [("-", "-"), ("num", 2), ("^", "^"), ("num", 3)]
    assert with_prec.parse(toks).value == (2 * (M - 2) + 3 * 3) % M  # (-2) ^ 3
    assert without.parse(toks).value == (-(2 * 2 + 3 * 3)) % M  # -(2 ^ 3)
