# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/version-space-algebra/. The authors are listed in prov/4T1SEM.jsonl.

import random

from version_space_algebra import (
    EMPTY, OPS, TERMINALS, Join, Leaf, build, count, dag_size, evaluate, intersect,
    make_leaf, make_union, programs, size, smallest, synthesize,
)


def all_programs(max_size):
    """Brute force: every program of size <= max_size, listed by size."""
    by_size = {1: list(TERMINALS)}
    for s in range(3, max_size + 1, 2):
        out = []
        for s1 in range(1, s - 1, 2):
            for p in by_size[s1]:
                for q in by_size[s - 1 - s1]:
                    for op in OPS:
                        out.append((op, p, q))
        by_size[s] = out
    return [p for s in sorted(by_size) for p in by_size[s]]


ALL7 = all_programs(7)


def consistent(examples, max_size, pool=ALL7):
    return {p for p in pool if size(p) <= max_size and all(evaluate(p, i) == o for i, o in examples)}


def random_example(rng, max_size):
    inp = (rng.randint(-3, 3), rng.randint(-3, 3))
    if rng.random() < 0.8:
        p = rng.choice([q for q in ALL7 if size(q) <= max_size])
        return inp, evaluate(p, inp)
    return inp, rng.randint(-20, 20)


def test_brute_force_counts():
    assert len(ALL7) == 4 + 48 + 1152 + 34560


def test_single_example_equals_enumeration():
    rng = random.Random(1)
    for max_size in (1, 3, 5, 7):
        for _ in range(4):
            ex = random_example(rng, max_size)
            root = build(ex[0], ex[1], max_size)
            listed = list(programs(root))
            want = consistent([ex], max_size)
            assert len(listed) == len(set(listed))
            assert set(listed) == want
            assert count(root) == len(want)


def test_intersection_equals_enumeration():
    rng = random.Random(2)
    for max_size in (3, 5, 7):
        for _ in range(4):
            target = rng.choice([q for q in ALL7 if size(q) <= max_size])
            examples = []
            for _ in range(rng.randint(2, 3)):
                inp = (rng.randint(-3, 3), rng.randint(-3, 3))
                examples.append((inp, evaluate(target, inp)))
            root = synthesize(examples, max_size)
            want = consistent(examples, max_size)
            assert target in want
            listed = list(programs(root))
            assert len(listed) == len(set(listed)) == count(root)
            assert set(listed) == want
            best = smallest(root)
            assert size(best) == min(size(p) for p in want)
            assert all(evaluate(best, i) == o for i, o in examples)


def test_pairwise_intersection():
    rng = random.Random(3)
    for _ in range(6):
        e1 = random_example(rng, 5)
        e2 = random_example(rng, 5)
        a = build(e1[0], e1[1], 5)
        b = build(e2[0], e2[1], 5)
        r = intersect(a, b)
        want = consistent([e1], 5) & consistent([e2], 5)
        assert set(programs(r)) == want
        assert count(r) == len(want)
        if not want:
            assert r is EMPTY


def test_count_without_enumeration_size_9():
    # Compare the count of size 9 with a count over the brute force of the values only.
    inp, out = (1, 2), 3
    vals = {1: {}}
    for t in TERMINALS:
        v = evaluate(t, inp)
        vals[1][v] = vals[1].get(v, 0) + 1
    for s in range(3, 10, 2):
        table = {}
        for s1 in range(1, s - 1, 2):
            for a, ca in vals[s1].items():
                for b, cb in vals[s - 1 - s1].items():
                    for op in OPS:
                        v = {"+": a + b, "-": a - b, "*": a * b}[op]
                        table[v] = table.get(v, 0) + ca * cb
        vals[s] = table
    want = sum(vals[s].get(out, 0) for s in vals)
    root = build(inp, out, 9)
    assert count(root) == want
    # The size-7 part agrees with the explicit enumeration.
    assert count(build(inp, out, 7)) == len(consistent([(inp, out)], 7))


def test_compact_representation():
    # A chain of k joins over a two-program leaf holds 2^(k+1) programs in k + 1 nodes.
    leaf = make_leaf(["x", "y"])
    n = leaf
    for _ in range(10):
        n = Join("+", leaf, n)
    nodes, _ = dag_size(n)
    assert nodes == 11
    assert count(n) == 2 ** 11
    # The version space of one example holds far more programs than it has nodes and edges.
    root = build((1, 2), 3, 11)
    nodes, edges = dag_size(root)
    assert count(root) > 100 * (nodes + edges)


def test_union_and_join_semantics():
    a = make_leaf(["x", "1"])
    b = make_leaf(["y"])
    u = make_union([Join("+", a, b), Join("*", a, b)])
    assert set(programs(u)) == {("+", "x", "y"), ("+", "1", "y"), ("*", "x", "y"), ("*", "1", "y")}
    v = make_union([Join("+", make_leaf(["x"]), b), make_leaf(["x"])])
    assert set(programs(intersect(u, v))) == {("+", "x", "y")}
    assert intersect(Join("+", a, b), Leaf(frozenset(["x"]))) is EMPTY
    assert intersect(Join("+", a, b), Join("-", a, b)) is EMPTY


def test_no_consistent_program():
    examples = [((0, 0), 1000)]
    assert synthesize(examples, 5) is EMPTY
    assert smallest(EMPTY) is None
    assert count(EMPTY) == 0
