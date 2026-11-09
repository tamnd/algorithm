# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/term-dag/. The authors are listed in prov/9PFAX5.jsonl.

import random

from term_dag import TermDAG

A = ("a",)


def subterms(t, acc):
    stack = [t]
    while stack:
        u = stack.pop()
        acc.add(u)
        if not isinstance(u, str):
            stack.extend(u[1:])
    return acc


def size(t):
    n, stack = 0, [t]
    while stack:
        u = stack.pop()
        n += 1
        if not isinstance(u, str):
            stack.extend(u[1:])
    return n


def random_term(rng, depth):
    r = rng.random()
    if depth == 0 or r < 0.25:
        return rng.choice(["x", "y", A, ("b",)])
    if r < 0.5:
        return ("g", random_term(rng, depth - 1))
    return ("f", random_term(rng, depth - 1), random_term(rng, depth - 1))


def test_example() -> None:
    d = TermDAG()
    t = ("f", ("g", "x", "x"), ("g", "x", "x"), "x")
    root = d.intern(t)
    assert d.dag_size() == 3
    assert d.tree_size(root) == 8
    assert d.unfold(root) == t
    assert d.children(root) == (1, 1, 0)
    assert d.symbol(1) == "g" and d.is_var(0)
    d.check_invariant()


def test_edges() -> None:
    d = TermDAG()
    assert d.dag_size() == 0
    x = d.var("x")
    assert d.var("x") == x and d.intern("x") == x
    a = d.intern(A)
    assert d.make_node("a") == a and d.tree_size(a) == 1
    # A variable and a constant with the same name are different nodes.
    assert d.make_node("x") != x
    # Same symbol, different arity.
    assert d.make_node("f", (a,)) != d.make_node("f", (a, a))
    d.check_invariant()


def test_exponential_sharing() -> None:
    for n in range(0, 60):
        d = TermDAG()
        node = d.var("x0")
        for _ in range(n):
            node = d.make_node("g", (node, node))
        assert d.dag_size() == n + 1
        assert d.tree_size(node) == 2 ** (n + 1) - 1
        if n <= 12:
            assert size(d.unfold(node)) == 2 ** (n + 1) - 1


def test_random_against_model() -> None:
    rng = random.Random(3030)
    for _ in range(100):
        d = TermDAG()
        seen = {}
        stored = set()
        for _ in range(rng.randint(1, 20)):
            t = random_term(rng, 4)
            node = d.intern(t)
            subterms(t, stored)
            if t in seen:
                assert seen[t] == node
            else:
                assert node not in seen.values()
                seen[t] = node
            assert d.unfold(node) == t
            assert d.tree_size(node) == size(t)
            assert d.dag_size() == len(stored)
            d.check_invariant()


def test_deep_term_without_recursion() -> None:
    d = TermDAG()
    t = "x"
    for _ in range(5000):
        t = ("g", t)
    node = d.intern(t)
    assert d.dag_size() == 5001 and d.tree_size(node) == 5001
    assert d.unfold(node) == t
