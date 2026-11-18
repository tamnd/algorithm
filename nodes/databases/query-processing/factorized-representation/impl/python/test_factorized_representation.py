# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/factorized-representation/. The authors are listed in prov/7ZFJ86.jsonl.

import random

import dbrel
from factorized_representation import FTree, count, factorize, from_join, path_condition, size, tuples, valid

# Example 1.1 of Olteanu and Zavodny (2015): all (a, b, c) with 1 <= a < b < c <= 5.
R11 = dbrel.Relation(("a", "b", "c"),
                     [(a, b, c) for a in range(1, 6) for b in range(1, 6) for c in range(1, 6) if a < b < c], "set")


def join(rels: list, attrs: tuple) -> dbrel.Relation:
    db = {"R%d" % i: r for i, r in enumerate(rels)}
    expr = ("scan", "R0")
    for i in range(1, len(rels)):
        expr = ("join", expr, ("scan", "R%d" % i))
    return dbrel.evaluate(expr, db, "set").reorder(attrs)


def path_sizes(ftree: FTree, rel: dbrel.Relation) -> int:
    """The sum over the attributes A of the number of distinct values of the path to A."""
    return sum(len(dbrel.project(rel, ftree.path(a))) for a in ftree.attrs)


def test_example_1_1() -> None:
    star = FTree([("b", None), ("a", "b"), ("c", "b")])
    e = factorize(star, R11)
    assert count(e) == len(R11) == 10 and 3 * len(R11) == 30
    assert size(e) == 15 == path_sizes(star, R11)
    assert e[0][1] == (3, ([(1, ()), (2, ())], [(4, ()), (5, ())]))
    chain = FTree([("a", None), ("b", "a"), ("c", "b")])
    assert size(factorize(chain, R11)) == 3 + 6 + 10
    try:
        factorize(FTree([("a", None), ("b", "a"), ("c", "a")]), R11)
    except ValueError:
        pass
    else:
        raise AssertionError("b < c ties b and c, so they cannot be siblings below a")


def test_join_example() -> None:
    r = dbrel.Relation(("A", "B"), [(1, 1), (1, 2), (1, 3), (2, 4)], "set")
    s = dbrel.Relation(("A", "C"), [(1, 5), (1, 6), (2, 7)], "set")
    tree = FTree([("A", None), ("B", "A"), ("C", "A")])
    e = from_join(tree, [r, s])
    assert e == ([(1, ([(1, ()), (2, ()), (3, ())], [(5, ()), (6, ())])), (2, ([(4, ())], [(7, ())]))],)
    assert count(e) == 7 and size(e) == 9 == 2 + 4 + 3
    assert sorted(tuples(tree, e)) == join([r, s], tree.attrs).sorted_rows()


def test_gap_grows_with_n() -> None:
    n = 60
    r = dbrel.Relation(("A", "B"), [(0, i) for i in range(n)], "set")
    s = dbrel.Relation(("A", "C"), [(0, i) for i in range(n)], "set")
    e = from_join(FTree([("A", None), ("B", "A"), ("C", "A")]), [r, s])
    assert count(e) == n * n and size(e) == 2 * n + 1


def random_tree(rng: random.Random, attrs: list) -> FTree:
    order = attrs[:]
    rng.shuffle(order)
    nodes = []
    for i, a in enumerate(order):
        nodes.append((a, None if i == 0 or rng.random() < 0.2 else order[rng.randrange(i)]))
    return FTree(nodes)


def test_random_joins_against_dbrel() -> None:
    rng = random.Random(5)
    checked = 0
    for trial in range(600):
        rels = []
        for _ in range(rng.randrange(1, 5)):
            schema = tuple(rng.sample("ABCDE", rng.randrange(1, 4)))
            rels.append(dbrel.random_relation(rng, schema, rng.randrange(0, 9), range(3), "set"))
        attrs = sorted({a for r in rels for a in r.schema})
        tree = random_tree(rng, attrs)
        if not valid(tree, [r.schema for r in rels]):
            try:
                from_join(tree, rels)
            except ValueError:
                continue
            raise AssertionError("an invalid f-tree was accepted")
        checked += 1
        e = from_join(tree, rels)
        q = join(rels, tree.attrs)
        out = list(tuples(tree, e))
        assert len(out) == len(set(out)) == count(e)
        assert set(out) == set(q.rows)
        assert size(e) == path_sizes(tree, q)
        assert e == factorize(tree, q)
    assert checked > 150


def test_factorize_random_relations() -> None:
    rng = random.Random(6)
    accepted = 0
    for trial in range(400):
        rel = dbrel.random_relation(rng, ("A", "B", "C", "D"), rng.randrange(0, 12), range(2), "set")
        tree = random_tree(rng, ["A", "B", "C", "D"])
        # The relation factorizes over the tree when it is the join of its projections on the root-to-leaf paths.
        leaves = [a for a in tree.attrs if not tree.kids[a]]
        splits = join([dbrel.project(rel, tree.path(a)) for a in leaves], tree.attrs) == rel.reorder(tree.attrs)
        try:
            e = factorize(tree, rel)
        except ValueError:
            assert not splits
            continue
        assert splits
        accepted += 1
        assert set(tuples(tree, e)) == set(rel.reorder(tree.attrs).rows) and count(e) == len(rel)
        assert size(e) == path_sizes(tree, rel)
    assert accepted > 50


def test_path_condition_and_edges() -> None:
    tree = FTree([("A", None), ("B", "A"), ("C", "A")])
    assert path_condition(tree, [("A", "B"), ("A", "C")])
    assert not path_condition(tree, [("B", "C")])
    assert not valid(tree, [("A", "B")])
    assert not valid(FTree([]), [])
    empty = dbrel.Relation(("A", "B"), [], "set")
    full = dbrel.Relation(("A", "C"), [(1, 2)], "set")
    e = from_join(tree, [empty, full])
    assert e == ([],) and count(e) == 0 and size(e) == 0 and list(tuples(tree, e)) == []
    # A value of A that has a B but no C is pruned.
    r = dbrel.Relation(("A", "B"), [(1, 1), (2, 2)], "set")
    assert from_join(tree, [r, full]) == ([(1, ([(1, ())], [(2, ())]))],)
    forest = FTree([("A", None), ("C", None)])
    e = from_join(forest, [dbrel.Relation(("A",), [(1,), (2,)], "set"), dbrel.Relation(("C",), [(3,)], "set")])
    assert count(e) == 2 and size(e) == 3
    for bad in ([("A", None), ("A", None)], [("B", "A"), ("A", None)]):
        try:
            FTree(bad)
        except ValueError:
            continue
        raise AssertionError("a malformed f-tree was accepted")
