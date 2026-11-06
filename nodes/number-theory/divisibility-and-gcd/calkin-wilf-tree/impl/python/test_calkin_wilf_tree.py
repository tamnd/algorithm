# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/calkin-wilf-tree/. The authors are listed in prov/R06GGM.jsonl.

import math
import random
from fractions import Fraction

import pytest

from calkin_wilf_tree import at, children, depth, fusc, index_of, next_node, parent


def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def brute_fusc(limit: int) -> list[int]:
    f = [0, 1] + [0] * limit
    for n in range(2, limit + 1):
        f[n] = f[n // 2] if n % 2 == 0 else f[n // 2] + f[n // 2 + 1]
    return f


def brute_levels(levels: int) -> list[tuple[int, int]]:
    """Breadth-first list of the first levels, built from the child rule."""
    order = [(1, 1)]
    i = 0
    while len(order) < (1 << levels) - 1:
        a, b = order[i]
        order.append((a, a + b))
        order.append((a + b, b))
        i += 1
    return order


def cf_terms(a: int, b: int) -> list[int]:
    terms = []
    while b:
        terms.append(a // b)
        a, b = b, a % b
    return terms


def test_example() -> None:
    assert [at(n) for n in range(1, 16)] == [
        (1, 1), (1, 2), (2, 1), (1, 3), (3, 2), (2, 3), (3, 1),
        (1, 4), (4, 3), (3, 5), (5, 2), (2, 5), (5, 3), (3, 4), (4, 1),
    ]
    assert index_of(3, 5) == 10
    assert index_of(5, 2) == 11
    assert index_of(11, 7) == 37
    assert children(3, 5) == ((3, 8), (8, 5))
    assert parent(3, 5) == (3, 2)
    assert parent(1, 1) is None
    assert next_node(3, 5) == (5, 2)
    assert next_node(4, 1) == (1, 5)


def test_against_breadth_first_construction() -> None:
    order = brute_levels(13)
    f = brute_fusc(len(order) + 2)
    for n, node in enumerate(order, start=1):
        assert at(n) == node
        assert index_of(*node) == n
        assert at(n) == (f[n], f[n + 1])
        assert fusc(n) == f[n]
        if n < len(order):
            assert next_node(*node) == order[n]
        if n > 1:
            assert parent(*node) == order[n // 2 - 1]
            assert children(*order[n // 2 - 1])[n % 2] == node


def test_every_reduced_fraction_once() -> None:
    seen = set()
    for a in range(1, 80):
        for b in range(1, 80):
            if math.gcd(a, b) != 1:  # reference only
                with pytest.raises(ValueError):
                    index_of(a, b)
                continue
            n = index_of(a, b)
            assert n not in seen
            seen.add(n)
            assert at(n) == (a, b)
            assert depth(a, b) == sum(cf_terms(a, b)) - 1


def test_newman_formula_on_fractions() -> None:
    x = Fraction(1)
    for n in range(1, 3000):
        assert (x.numerator, x.denominator) == at(n)
        x = 1 / (2 * math.floor(x) - x + 1)


def test_powers_of_two_and_edges() -> None:
    for k in range(0, 200):
        assert at(1 << k) == (1, k + 1)
        assert at((1 << (k + 1)) - 1) == (k + 1, 1)
        assert index_of(k + 1, 1) == (1 << (k + 1)) - 1
        assert index_of(1, k + 1) == 1 << k


def test_invalid_inputs() -> None:
    for a, b in [(0, 1), (1, 0), (0, 0), (-1, 2), (2, -3), (-1, -1)]:
        with pytest.raises(ValueError):
            index_of(a, b)
        with pytest.raises(ValueError):
            children(a, b)
        with pytest.raises(ValueError):
            next_node(a, b)
    for n in (0, -1, -(10**20)):
        with pytest.raises(ValueError):
            at(n)
    with pytest.raises(ValueError):
        fusc(-1)
    with pytest.raises(ValueError):
        parent(4, 4)
    with pytest.raises(ValueError):
        index_of(6, 4)
    assert index_of(1, 1) == 1
    assert fusc(0) == 0


def test_fibonacci_and_large_values() -> None:
    for k in range(2, 300):
        a, b = fib(k + 1), fib(k)
        n = index_of(a, b)
        assert at(n) == (a, b)
        assert n.bit_length() - 1 == sum(cf_terms(a, b)) - 1
    rng = random.Random(99)
    done = 0
    while done < 600:
        digits = rng.choice([1, 3, 10, 50, 300, 400])
        a = rng.randrange(1, 10**digits)
        b = rng.randrange(1, 10**digits)
        if math.gcd(a, b) != 1:  # reference only
            continue
        terms = cf_terms(a, b)
        if sum(terms) > 100000:
            continue
        n = index_of(a, b)
        assert at(n) == (a, b)
        p = parent(a, b)
        if p is not None:
            assert index_of(*p) == n // 2
        left, right = children(a, b)
        assert index_of(*left) == 2 * n
        assert index_of(*right) == 2 * n + 1
        assert at(n + 1) == next_node(a, b)
        done += 1


def test_odd_length_continued_fraction_rule() -> None:
    # The index read from its lowest digit is 1^{a0} 0^{a1} 1^{a2} ... for the
    # continued fraction [a0; a1, ..., ak] of odd length.
    for n in range(1, 5000):
        a, b = at(n)
        terms = cf_terms(a, b)
        if len(terms) % 2 == 0:
            terms = terms[:-1] + [terms[-1] - 1, 1]
        digits = "".join(("1" if i % 2 == 0 else "0") * t for i, t in enumerate(terms))
        assert int(digits[::-1], 2) == n
