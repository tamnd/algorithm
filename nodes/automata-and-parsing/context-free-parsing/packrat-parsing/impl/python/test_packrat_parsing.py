# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/packrat-parsing/. The authors are listed in prov/1PYY5B.jsonl.

import itertools
import random

import pytest

from packrat_parsing import ParseError, packrat_match, packrat_parse


def lit(a):
    return ("lit", a)


def ref(a):
    return ("ref", a)


def seq(*es):
    return ("seq",) + es


def alt(*es):
    return ("alt",) + es


def star(e):
    return ("star", e)


def neg(e):
    return ("not", e)


def amp(e):
    return ("and", e)


EPS = ("eps",)
ANY = ("any",)


class Diverges(Exception):
    pass


class OutOfFuel(Exception):
    pass


def oracle(grammar, start, tokens, fuel=200000):
    """The PEG semantics read off directly, by plain recursion and without any memo.

    Returns ("ok", end, children) or ("fail",), and the farthest failed token test.
    Raises Diverges when the semantics has no result (a call repeats itself, or a
    repetition matches the empty string).
    """
    n = len(tokens)
    far = [0]
    left = [fuel]
    stack = []

    def m(e, i):
        left[0] -= 1
        if left[0] < 0:
            raise OutOfFuel
        key = (id(e), i)
        if key in stack:
            raise Diverges
        stack.append(key)
        try:
            return step(e, i)
        finally:
            stack.pop()

    def step(e, i):
        k = e[0]
        if k == "lit" or k == "any":
            if i < n and (k == "any" or tokens[i] == e[1]):
                return i + 1, [tokens[i]]
            far[0] = max(far[0], i)
            return None
        if k == "eps":
            return i, []
        if k == "ref":
            r = m(grammar[e[1]], i)
            return None if r is None else (r[0], [(e[1], r[1])])
        if k == "seq":
            kids = []
            for c in e[1:]:
                r = m(c, i)
                if r is None:
                    return None
                i = r[0]
                kids += r[1]
            return i, kids
        if k == "alt":
            for c in e[1:]:
                r = m(c, i)
                if r is not None:
                    return r
            return None
        if k == "star":
            kids = []
            while True:
                r = m(e[1], i)
                if r is None:
                    return i, kids
                if r[0] == i:
                    raise Diverges
                i = r[0]
                kids += r[1]
        r = m(e[1], i)
        if (r is None) == (k == "not"):
            return i, []
        if k == "not":
            far[0] = max(far[0], i)
        return None

    r = m(grammar[start], 0)
    return r, far[0]


def expected(grammar, start, tokens):
    """The tree, or ("error", position), as packrat_parse should give it."""
    r, far = oracle(grammar, start, tokens)
    if r is None:
        return ("error", far)
    if r[0] < len(tokens):
        return ("error", max(far, r[0]))
    return (start, r[1])


def run(grammar, start, tokens):
    try:
        return packrat_parse(grammar, start, tokens)
    except ParseError as e:
        return ("error", e.position)


def leaves(t):
    out, work = [], [t]
    while work:
        x = work.pop()
        if isinstance(x, str):
            out.append(x)
        else:
            work.extend(reversed(x[1]))
    return out


# Ford's grammar for a^n b^n c^n, with the full-match check.
ABC = {
    "S": seq(amp(seq(ref("A"), lit("c"))), lit("a"), star(lit("a")), ref("B"), neg(ANY)),
    "A": seq(lit("a"), alt(ref("A"), EPS), lit("b")),
    "B": seq(lit("b"), alt(ref("B"), EPS), lit("c")),
}

# Expressions with repetition instead of left recursion.
EXPR = {
    "E": seq(ref("T"), star(seq(lit("+"), ref("T")))),
    "T": seq(ref("F"), star(seq(lit("*"), ref("F")))),
    "F": alt(seq(lit("("), ref("E"), lit(")")), lit("x")),
    "Top": seq(ref("E"), neg(ANY)),
}


def test_expression_tree():
    t = packrat_parse(EXPR, "Top", list("x+x*x"))
    assert t == ("Top", [("E", [("T", [("F", ["x"])]), "+",
                                ("T", [("F", ["x"]), "*", ("F", ["x"])])])])
    assert leaves(t) == list("x+x*x")


def test_expression_errors():
    for s, pos in [("x+", 2), ("x+*x", 2), ("(x", 2), ("x)", 1), ("", 0), ("xx", 1)]:
        with pytest.raises(ParseError) as err:
            packrat_parse(EXPR, "Top", list(s))
        assert err.value.position == pos, s
        assert ("error", pos) == expected(EXPR, "Top", list(s))


def test_anbncn():
    for m in range(0, 11):
        for w in itertools.product("abc", repeat=m):
            w = list(w)
            k = len(w) // 3
            want = k >= 1 and w == ["a"] * k + ["b"] * k + ["c"] * k
            assert (run(ABC, "S", w)[0] != "error") == want, w


def test_ordered_choice_and_greed():
    g = {"S": seq(alt(lit("a"), seq(lit("a"), lit("b"))), neg(ANY))}
    assert run(g, "S", ["a"])[0] == "S"
    assert run(g, "S", ["a", "b"]) == ("error", 1)
    g = {"S": seq(star(lit("a")), lit("a"))}
    for m in range(6):
        assert packrat_match(g, "S", ["a"] * m) is None


def test_powers_of_two():
    g = {"S": alt(seq(lit("a"), ref("S"), lit("a")), lit("a")), "Top": seq(ref("S"), neg(ANY))}
    ok = [m for m in range(1, 70) if run(g, "Top", ["a"] * m)[0] == "Top"]
    assert ok == [1, 3, 7, 15, 31, 63]


def test_example_of_the_page():
    g = {"S": alt(seq(ref("A"), lit("b")), seq(ref("A"), lit("c"))),
         "A": alt(seq(lit("a"), ref("A")), lit("a"))}
    stats = {}
    t = packrat_parse(g, "S", list("aac"), stats)
    assert t == ("S", [("A", ["a", ("A", ["a"])]), "c"])
    assert stats["evaluations"] == 20 and stats["expressions"] == 12


def test_exponential_backtracking_becomes_linear():
    for k in range(1, 16):
        g = {"A0": lit("a")}
        for j in range(1, k + 1):
            g[f"A{j}"] = alt(seq(ref(f"A{j - 1}"), lit("x")), seq(ref(f"A{j - 1}"), lit("y")))
        w = ["a"] + ["y"] * k
        stats = {}
        t = packrat_parse(g, f"A{k}", w, stats)
        assert leaves(t) == w
        assert stats["evaluations"] <= stats["expressions"] * (len(w) + 1)
        if k <= 10:
            assert expected(g, f"A{k}", w) == t


def test_left_recursion_and_empty_star_are_reported():
    g = {"E": alt(seq(ref("E"), lit("+"), lit("x")), lit("x"))}
    with pytest.raises(ValueError):
        packrat_parse(g, "E", list("x+x"))
    g = {"S": star(alt(lit("a"), EPS))}
    with pytest.raises(ValueError):
        packrat_parse(g, "S", list("aa"))
    with pytest.raises(ValueError):
        packrat_parse({"S": ref("T")}, "S", [])


def test_deep_input_without_recursion():
    n = 100000
    g = {"S": alt(seq(lit("("), ref("S"), lit(")")), EPS), "Top": seq(ref("S"), neg(ANY))}
    t = packrat_parse(g, "Top", ["("] * n + [")"] * n)
    depth, x = 0, t[1][0]
    while x[1]:
        depth += 1
        x = x[1][1]
    assert depth == n
    with pytest.raises(ParseError) as err:
        packrat_parse(g, "Top", ["("] * n + [")"] * (n - 1))
    assert err.value.position == 2 * n - 1
    g = {"L": star(seq(lit("a"), ref("I"))), "I": alt(lit("b"), EPS)}
    t = packrat_parse(g, "L", ["a", "b"] * n)
    assert len(t[1]) == 2 * n


def test_shared_empty_subtrees():
    g = {"B0": EPS, "S": star(seq(lit("a"), ref("B40")))}
    for j in range(1, 41):
        g[f"B{j}"] = seq(ref(f"B{j - 1}"), ref(f"B{j - 1}"))
    stats = {}
    t = packrat_parse(g, "S", ["a"] * 50, stats)
    seen, work = set(), [t]
    while work:
        x = work.pop()
        if not isinstance(x, str) and id(x) not in seen:
            seen.add(id(x))
            work.extend(x[1])
    assert len(t[1]) == 100 and len(seen) <= stats["expressions"] * 51


def random_expr(rng, names, depth):
    r = rng.random()
    if depth == 0 or r < 0.3:
        c = rng.random()
        if c < 0.55:
            return lit(rng.choice("abc"))
        if c < 0.8:
            return ref(rng.choice(names))
        if c < 0.9:
            return EPS
        return ANY
    k = rng.choice(["seq", "seq", "alt", "alt", "star", "not", "and"])
    if k in ("seq", "alt"):
        return (k,) + tuple(random_expr(rng, names, depth - 1) for _ in range(rng.randint(1, 3)))
    return (k, random_expr(rng, names, depth - 1))


def test_random_against_semantics():
    rng = random.Random(20021004)
    inputs = [list(w) for m in range(5) for w in itertools.product("abc", repeat=m)]
    checked = accepted = diverged = 0
    for _ in range(700):
        names = [f"N{j}" for j in range(rng.randint(1, 4))]
        g = {a: random_expr(rng, names, 3) for a in names}
        if rng.random() < 0.5:
            g["Top"] = seq(ref(names[0]), neg(ANY))
            start = "Top"
        else:
            start = names[0]
        ws = inputs + [[rng.choice("abc") for _ in range(rng.randint(5, 9))] for _ in range(10)]
        for w in ws:
            try:
                want = expected(g, start, w)
            except OutOfFuel:
                continue
            except Diverges:
                with pytest.raises(ValueError):
                    packrat_parse(g, start, w)
                diverged += 1
                continue
            got = run(g, start, w)
            assert got == want, (g, start, w)
            if got[0] != "error":
                assert leaves(got) == w
                accepted += 1
                stats = {}
                packrat_parse(g, start, w, stats)
                assert stats["evaluations"] <= stats["expressions"] * (len(w) + 1)
            checked += 1
    assert checked >= 500 and accepted >= 500 and diverged >= 50
