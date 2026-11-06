# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pratt-parsing/. The authors are listed in prov/G9PZT9.jsonl.

import itertools
import random
from functools import lru_cache

import pytest

from pratt_parsing import ParseError, PrattParser, leaves

PREFIX = {"-": 25}
INFIX = {"+": (10, 10), "-": (10, 10), "*": (20, 20), "/": (20, 20), "^": (30, 29)}
POSTFIX = {"!": 40}


def all_trees(p: PrattParser, toks):
    """Every tree of the ambiguous grammar
    E -> operand | ( E ) | pre E | E post | E in E, by enumeration over spans."""
    toks = tuple(toks)

    @lru_cache(maxsize=None)
    def trees(i, j):
        out = []
        if j == i + 1 and p.is_operand(toks[i]):
            out.append(toks[i])
        if j - i >= 3 and toks[i] == "(" and toks[j - 1] == ")":
            out += [("()", e) for e in trees(i + 1, j - 1)]
        if j - i >= 2 and toks[i] in p.prefix:
            out += [("pre", toks[i], e) for e in trees(i + 1, j)]
        if j - i >= 2 and toks[j - 1] in p.postfix:
            out += [("post", toks[j - 1], e) for e in trees(i, j - 1)]
        for k in range(i + 1, j - 1):
            if toks[k] in p.infix:
                for l in trees(i, k):
                    for r in trees(k + 1, j):
                        out.append(("in", toks[k], l, r))
        return tuple(out)

    return trees(0, len(toks)) if toks else ()


def valid(p: PrattParser, tree) -> bool:
    """The binding-power conditions, checked at every node.
    (A) a node that takes a left operand, with lbp l: l <= rbp(X) for every X
        on the right spine of the left operand;
    (B) a node with a right operand, with rbp r: lbp(Y) > r for every Y on the
        left spine of the right operand that takes a left operand."""

    def rbp(x):
        if isinstance(x, tuple) and x[0] == "in":
            return p.infix[x[1]][1]
        if isinstance(x, tuple) and x[0] == "pre":
            return p.prefix[x[1]]
        return None

    def right_spine(x):
        while isinstance(x, tuple) and x[0] in ("in", "pre"):
            yield x
            x = x[-1]

    def left_spine(x):
        while isinstance(x, tuple) and x[0] in ("in", "post"):
            yield x
            x = x[2]

    stack = [tree]
    while stack:
        x = stack.pop()
        if isinstance(x, str):
            continue
        kind = x[0]
        if kind in ("in", "post"):
            l = p.lbp(x[1])
            if any(l > rbp(y) for y in right_spine(x[2])):
                return False
        if kind in ("in", "pre"):
            r = rbp(x)
            if any(p.lbp(y[1]) <= r for y in left_spine(x[-1])):
                return False
        stack.extend([x[1]] if kind == "()" else x[2:])
    return True


def show(t) -> str:
    if isinstance(t, str):
        return t
    if t[0] == "()":
        return show(t[1])
    if t[0] == "pre":
        return f"({t[1]}{show(t[2])})"
    if t[0] == "post":
        return f"({show(t[2])}{t[1]})"
    return f"({show(t[2])} {t[1]} {show(t[3])})"


def check(p: PrattParser, toks) -> None:
    cands = [t for t in all_trees(p, toks) if valid(p, t)]
    try:
        got = p.parse(toks)
    except ParseError:
        assert not all_trees(p, toks), toks
        return
    assert leaves(got) == list(toks)
    assert cands == [got], (toks, got, cands)


def test_example() -> None:
    p = PrattParser(PREFIX, INFIX, POSTFIX)
    t = p.parse("- a ^ b * c + d !".split())
    assert show(t) == "(((-(a ^ b)) * c) + (d!))"
    assert show(p.parse("a - b - c".split())) == "((a - b) - c)"
    assert show(p.parse("a ^ b ^ c".split())) == "(a ^ (b ^ c))"
    assert show(p.parse("a - - b * c".split())) == "(a - ((-b) * c))"
    assert show(p.parse("( a + b ) * c".split())) == "((a + b) * c)"
    for bad in ["", "a +", "+ a", "a b", "( a", "a )", "a ( b )", "!"]:
        with pytest.raises(ParseError):
            p.parse(bad.split())
    for s in ["- a ^ b * c + d !", "a - - b * c", "( - a ) ! ^ b", "a * - b + c"]:
        check(p, s.split())


def test_low_prefix() -> None:
    # A prefix operator that binds loosely takes everything to its right.
    p = PrattParser({"not": 5}, {"and": (10, 10), "==": (20, 20)}, {})
    assert show(p.parse("not a == b and c".split())) == "(not((a == b) and c))"
    assert show(p.parse("a and not b == c".split())) == "(a and (not(b == c)))"
    check(p, "a == not b and c".split())


def random_tables(rng):
    ops = ["+", "-", "*", "!", "~"]
    prefix, infix, postfix = {}, {}, {}
    for o in ops:
        role = rng.choice(["pre", "in", "post", "pre+in", "pre+post", "in", "none"])
        if "pre" in role:
            prefix[o] = rng.randint(0, 4)
        if "in" in role:
            l = rng.randint(1, 4)
            infix[o] = (l, rng.choice([l, l - 1, rng.randint(0, 4)]))
        if "post" in role:
            postfix[o] = rng.randint(1, 4)
    return PrattParser(prefix, infix, postfix)


def random_expression(rng, p: PrattParser, size: int) -> list[str]:
    """The tokens of a random tree of the ambiguous grammar with size operators."""
    if size == 0:
        return [rng.choice(["a", "b"])]
    kinds = ["()"] + ["pre"] * bool(p.prefix) + ["post"] * bool(p.postfix) + ["in"] * 2 * bool(p.infix)
    kind = rng.choice(kinds)
    if kind == "()":
        return ["("] + random_expression(rng, p, size - 1) + [")"]
    if kind == "pre":
        return [rng.choice(sorted(p.prefix))] + random_expression(rng, p, size - 1)
    if kind == "post":
        return random_expression(rng, p, size - 1) + [rng.choice(sorted(p.postfix))]
    k = rng.randint(0, size - 1)
    return random_expression(rng, p, k) + [rng.choice(sorted(p.infix))] + random_expression(rng, p, size - 1 - k)


def test_random_against_enumeration() -> None:
    rng = random.Random(1973)
    pool = ["a", "b", "(", ")", "+", "-", "*", "!", "~"]
    checked = accepted = ambiguous = 0
    for _ in range(300):
        p = random_tables(rng)
        for _ in range(25):
            if rng.random() < 0.3:
                toks = [rng.choice(pool) for _ in range(rng.randint(0, 8))]
            else:
                toks = random_expression(rng, p, rng.randint(0, 5))
            check(p, toks)
            checked += 1
            accepted += p.recognize(toks)
            ambiguous += len(all_trees(p, toks)) > 1
    assert checked >= 500 and accepted >= 3000 and ambiguous >= 1000


def test_all_short_strings() -> None:
    p = PrattParser({"-": 2}, {"-": (1, 1), "*": (3, 3), "^": (4, 3)}, {"!": 2})
    count = 0
    for n in range(0, 6):
        for toks in itertools.product(["a", "(", ")", "-", "*", "^", "!"], repeat=n):
            check(p, list(toks))
            count += 1
    assert count > 15000


def test_deep_nesting() -> None:
    p = PrattParser(PREFIX, INFIX, POSTFIX)
    n = 5000
    assert p.recognize(["("] * n + ["a"] + [")"] * n)
    assert p.recognize(["-"] * n + ["a"])
    toks = ["a"] + ["^", "a"] * n
    t = p.parse(toks)
    assert leaves(t) == toks
    assert not p.recognize(["("] * n + ["a"])
