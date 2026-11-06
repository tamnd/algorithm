# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shunting-yard-algorithm/. The authors are listed in prov/2TMV07.jsonl.

import itertools
import random

import pytest

from shunting_yard_algorithm import evaluate_postfix, shunting_yard

# The unambiguous precedence grammar that defines the meaning of an expression.
GRAMMAR = [
    ("E", ("E", "+", "T")), ("E", ("E", "-", "T")), ("E", ("T",)),
    ("T", ("T", "*", "F")), ("T", ("T", "/", "F")), ("T", ("F",)),
    ("F", ("P", "^", "F")), ("F", ("P",)),
    ("P", ("(", "E", ")")), ("P", ("a",)), ("P", ("b",)),
]
NTS = {"E", "T", "F", "P"}


def spans(w):
    """Least fixpoint of the facts 'A derives w[i:j]' (an independent oracle)."""
    n = len(w)
    known = set()

    def ends_of(rhs, i, j):
        ends = {i}
        for x in rhs:
            nxt = set()
            for p in ends:
                if x in NTS:
                    nxt |= {q for q in range(p, j + 1) if (x, p, q) in known}
                elif p < j and w[p] == x:
                    nxt.add(p + 1)
            ends = nxt
        return ends

    changed = True
    while changed:
        changed = False
        for a, rhs in GRAMMAR:
            for i in range(n + 1):
                for j in range(i, n + 1):
                    if (a, i, j) not in known and j in ends_of(rhs, i, j):
                        known.add((a, i, j))
                        changed = True
    return known


def grammar_tree(w):
    """The unique parse tree of w, as nested (op, left, right) tuples, or None."""
    known = spans(w)
    n = len(w)
    if ("E", 0, n) not in known:
        return None

    def build(a, i, j):
        for lhs, rhs in GRAMMAR:
            if lhs != a:
                continue
            for cut in itertools.product(range(i, j + 1), repeat=len(rhs) - 1):
                bounds = (i,) + cut + (j,)
                if any(bounds[k] > bounds[k + 1] for k in range(len(rhs))):
                    continue
                ok = True
                for x, p, q in zip(rhs, bounds, bounds[1:]):
                    if x in NTS:
                        ok = ok and (x, p, q) in known
                    else:
                        ok = ok and q == p + 1 and w[p] == x
                if not ok:
                    continue
                if len(rhs) == 3 and rhs[1] in "+-*/^":
                    return (rhs[1], build(rhs[0], bounds[0], bounds[1]), build(rhs[2], bounds[2], bounds[3]))
                if rhs[0] == "(":
                    return build("E", bounds[1], bounds[2])
                if rhs[0] in NTS:
                    return build(rhs[0], i, j)
                return w[i]
        raise AssertionError("no split")

    return build("E", 0, n)


def test_example() -> None:
    toks = "a + b * ( c - d ) ^ e ^ f - g".split()
    assert shunting_yard(toks) == "a b c d - e f ^ ^ * + g -".split()


def test_associativity_and_precedence() -> None:
    assert shunting_yard("a - b - c".split()) == "a b - c -".split()
    assert shunting_yard("a ^ b ^ c".split()) == "a b c ^ ^".split()
    assert shunting_yard("a + b * c".split()) == "a b c * +".split()
    assert shunting_yard("( a + b ) * c".split()) == "a b + c *".split()
    assert shunting_yard(["x"]) == ["x"]
    assert shunting_yard("( ( x ) )".split()) == ["x"]


@pytest.mark.parametrize("bad", ["", "+", "a +", "+ a", "a b", "( a", "a )", "( )", ") a (", "a ( b )", "a + * b", "( a + ) b"])
def test_rejects_malformed(bad: str) -> None:
    with pytest.raises(ValueError):
        shunting_yard(bad.split())


def random_tree(rng, depth):
    if depth == 0 or rng.random() < 0.3:
        return rng.choice("abcdxyz")
    return (rng.choice("+-*/^"), random_tree(rng, depth - 1), random_tree(rng, depth - 1))


PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}


def infix(tree, rng):
    """Print a tree with the parentheses it needs, plus some extra ones."""
    if isinstance(tree, str):
        s = [tree]
    else:
        op, l, r = tree
        ls, rs = infix(l, rng), infix(r, rng)
        lneed = not isinstance(l, str) and (PREC[l[0]] < PREC[op] or (PREC[l[0]] == PREC[op] and op == "^"))
        rneed = not isinstance(r, str) and (PREC[r[0]] < PREC[op] or (PREC[r[0]] == PREC[op] and op != "^"))
        s = (["("] + ls + [")"] if lneed else ls) + [op] + (["("] + rs + [")"] if rneed else rs)
    if rng.random() < 0.1:
        s = ["("] + s + [")"]
    return s


def postorder(tree):
    out, stack = [], [(tree, False)]
    while stack:
        t, done = stack.pop()
        if isinstance(t, str):
            out.append(t)
        elif done:
            out.append(t[0])
        else:
            stack.append((t, True))
            stack.append((t[2], False))
            stack.append((t[1], False))
    return out


def test_random_trees() -> None:
    rng = random.Random(1961)
    for _ in range(1500):
        tree = random_tree(rng, rng.randint(0, 5))
        toks = infix(tree, rng)
        post = shunting_yard(toks)
        assert post == postorder(tree)
        assert evaluate_postfix(post) == tree


def test_random_token_strings_against_grammar() -> None:
    rng = random.Random(42)
    alphabet = ["a", "b", "+", "-", "*", "^", "(", ")"]
    for _ in range(1500):
        w = [rng.choice(alphabet) for _ in range(rng.randint(0, 9))]
        expected = grammar_tree(w)
        if expected is None:
            with pytest.raises(ValueError):
                shunting_yard(w)
        else:
            assert evaluate_postfix(shunting_yard(w)) == expected


def test_all_short_strings() -> None:
    alphabet = ["a", "-", "^", "(", ")"]
    for n in range(0, 6):
        for w in itertools.product(alphabet, repeat=n):
            w = list(w)
            expected = grammar_tree(w)
            if expected is None:
                with pytest.raises(ValueError):
                    shunting_yard(w)
            else:
                assert evaluate_postfix(shunting_yard(w)) == expected


def test_long_input() -> None:
    n = 20000
    toks = ["("] * n + ["a"] + [")"] * n
    assert shunting_yard(toks) == ["a"]
    toks = ["a"] + ["^", "a"] * n
    assert shunting_yard(toks) == ["a"] * (n + 1) + ["^"] * n
