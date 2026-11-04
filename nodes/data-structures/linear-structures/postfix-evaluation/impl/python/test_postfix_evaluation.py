# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/postfix-evaluation/. The authors are listed in prov/XVTXFV.jsonl.

import random
from fractions import Fraction
from functools import lru_cache

import pytest

from postfix_evaluation import DEFAULT_OPS, MalformedExpression, evaluate, postfix_eval


def test_example() -> None:
    assert evaluate("5 1 2 + 4 * + 3 -") == 14
    assert evaluate("3 4 + 2 *") == 14
    assert evaluate("3 4 2 * +") == 11


def test_edges() -> None:
    assert evaluate("7") == 7
    assert evaluate("-3") == -3
    assert evaluate("-3 neg") == 3
    assert evaluate("1 2 3 4 + + +") == 10
    assert evaluate("1 2 + 3 + 4 +") == 10
    big = 2**63 - 1
    assert evaluate(f"{big} {big} *") == big * big
    assert evaluate("1 3 /") == Fraction(1, 3)


def test_operand_order() -> None:
    assert evaluate("7 2 -") == 5
    assert evaluate("8 2 /") == 4
    assert evaluate("2 8 /") == Fraction(1, 4)


def test_malformed() -> None:
    for text in ["", "3 +", "3 4", "3 4 + +", "+", "3 x +", "1 2 3 +"]:
        with pytest.raises(MalformedExpression):
            evaluate(text)
    with pytest.raises(ZeroDivisionError):
        evaluate("1 0 /")


OPS = ["+", "-", "*", "neg"]


def oracle(tokens: tuple[str, ...]) -> Fraction | None:
    """Parse by trying every split (independent of the stack and of the counting test)."""

    @lru_cache(maxsize=None)
    def parse(i: int, j: int) -> Fraction | None:
        if j - i == 1 and tokens[i] not in DEFAULT_OPS:
            return Fraction(int(tokens[i]))
        if j - i < 2 or tokens[j - 1] not in DEFAULT_OPS:
            return None
        k, f = DEFAULT_OPS[tokens[j - 1]]
        if k == 1:
            a = parse(i, j - 1)
            return None if a is None else f(a)
        for c in range(i + 1, j - 1):
            a, b = parse(i, c), parse(c, j - 1)
            if a is not None and b is not None:
                return f(a, b)
        return None

    return parse(0, len(tokens)) if tokens else None


def random_tree_postfix(rng: random.Random, depth: int) -> list[str]:
    if depth == 0 or rng.random() < 0.3:
        return [str(rng.randint(-9, 9))]
    op = rng.choice(OPS)
    if op == "neg":
        return random_tree_postfix(rng, depth - 1) + [op]
    return random_tree_postfix(rng, depth - 1) + random_tree_postfix(rng, depth - 1) + [op]


def test_random_well_formed_against_oracle() -> None:
    rng = random.Random(1954)
    for _ in range(500):
        toks = random_tree_postfix(rng, rng.randint(0, 5))
        assert postfix_eval(toks) == oracle(tuple(toks))


def test_random_strings_against_oracle() -> None:
    rng = random.Random(1962)
    for _ in range(1000):
        toks = tuple(rng.choice(["1", "2", "-3", "+", "-", "*", "neg"]) for _ in range(rng.randint(0, 9)))
        want = oracle(toks)
        if want is None:
            with pytest.raises(MalformedExpression):
                postfix_eval(toks)
        else:
            assert postfix_eval(toks) == want
