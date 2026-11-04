# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dijkstra-two-stack-evaluation/. The authors are listed in prov/9KN9AK.jsonl.

import random
from fractions import Fraction

import pytest

from dijkstra_two_stack_evaluation import evaluate


def test_page_example() -> None:
    e = "( 1 + ( ( 2 + 3 ) * ( 4 * 5 ) ) )".split()
    assert len(e) == 17
    assert evaluate(e) == 101
    assert evaluate("1 + 2 + 3 ) * 4 * 5 ) ) )".split()) == 101


def test_order_of_operands() -> None:
    assert evaluate("( 7 - 2 )".split()) == 5
    assert evaluate("( 7 / 2 )".split()) == Fraction(7, 2)
    assert evaluate(["42"]) == 42


def test_malformed() -> None:
    with pytest.raises(ValueError):
        evaluate("( 1 + 2 * 3 )".split())
    with pytest.raises(ValueError):
        evaluate("1 + 2 ) )".split())
    with pytest.raises(ValueError):
        evaluate([])


def build(rng: random.Random, depth: int) -> tuple[list[str], Fraction]:
    if depth == 0 or rng.random() < 0.3:
        x = rng.randrange(1, 10)
        return [str(x)], Fraction(x)
    op = rng.choice("+-*/")
    left, a = build(rng, depth - 1)
    right, b = build(rng, depth - 1)
    if op == "/" and b == 0:
        op = "+"
    v = {"+": a + b, "-": a - b, "*": a * b, "/": a / b if b else a}[op]
    return ["("] + left + [op] + right + [")"], v


def test_random_against_recursive_value() -> None:
    rng = random.Random(1961)
    for _ in range(800):
        toks, v = build(rng, rng.randrange(0, 6))
        assert evaluate(toks) == v
        assert evaluate([t for t in toks if t != "("]) == v
