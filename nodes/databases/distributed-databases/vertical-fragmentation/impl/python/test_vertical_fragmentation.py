# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertical-fragmentation/. The authors are listed in prov/XEF5EY.jsonl.

import random
from collections import Counter
from functools import reduce

import pytest

import dbrel
from vertical_fragmentation import fragment, is_complete, is_disjoint, is_key, reconstruct, with_tuple_id

EMP = ("eno", "name", "salary", "dept")
EMP_ROWS = Counter({(1, "Ann", 5000, "R&D"): 1, (2, "Bo", 4000, "Sales"): 1,
                    (3, "Cy", None, "R&D"): 1, (4, "Di", 4000, None): 1})


def rel(schema, rows):
    return dbrel.Relation(schema, rows)


def ref_reconstruct(frags, schema):
    """The join of the fragments by the reference operator."""
    return reduce(dbrel.natural_join, (rel(fs, rows) for fs, rows in frags)).reorder(schema)


def test_page_example():
    frags = fragment(EMP, EMP_ROWS, ("eno",), [("name", "dept"), ("salary",)])
    assert [fs for fs, _ in frags] == [("eno", "name", "dept"), ("eno", "salary")]
    assert is_complete(EMP, frags) and is_disjoint(("eno",), frags)
    assert reconstruct(frags, ("eno",), EMP) == EMP_ROWS
    assert ref_reconstruct(frags, EMP) == rel(EMP, EMP_ROWS)


def test_page_example_without_the_key():
    # Fragments that share only dept, which is not a key: the join adds rows that were never in EMP.
    frags = [(("name", "dept"), Counter({("Ann", "R&D"): 1, ("Cy", "R&D"): 1})),
             (("dept", "salary"), Counter({("R&D", 5000): 1, ("R&D", None): 1}))]
    joined = ref_reconstruct(frags, ("name", "dept", "salary"))
    assert len(joined) == 4  # two of them are spurious


def random_keyed(rng, attrs, n):
    keys = rng.sample(range(100), n)
    rows = Counter()
    for k in keys:
        rows[(k,) + tuple(rng.choice([None, 0, 1, 2]) for _ in attrs)] += 1
    return ("K",) + tuple(attrs), rows


def random_groups(rng, attrs):
    attrs = list(attrs)
    rng.shuffle(attrs)
    cuts = sorted(rng.sample(range(1, len(attrs)), rng.randint(0, len(attrs) - 1))) if len(attrs) > 1 else []
    bounds = [0] + cuts + [len(attrs)]
    return [tuple(attrs[bounds[i]:bounds[i + 1]]) for i in range(len(bounds) - 1)]


@pytest.mark.parametrize("seed", range(80))
def test_lossless_with_a_key(seed):
    rng = random.Random(seed)
    attrs = [f"A{i}" for i in range(rng.randint(1, 5))]
    schema, rows = random_keyed(rng, attrs, rng.randint(0, 12))
    groups = random_groups(rng, attrs)
    assert is_key(schema, rows, ("K",))
    frags = fragment(schema, rows, ("K",), groups)
    assert is_complete(schema, frags) and is_disjoint(("K",), frags)
    for fs, f in frags:
        assert rel(fs, f) == dbrel.project(rel(schema, rows), fs)
    assert reconstruct(frags, ("K",), schema) == rows
    assert ref_reconstruct(frags, schema) == rel(schema, rows)


@pytest.mark.parametrize("seed", range(60))
def test_bag_without_a_key_needs_a_tuple_id(seed):
    rng = random.Random(1000 + seed)
    r = dbrel.random_relation(rng, ("A", "B", "C"), rng.randint(1, 12), domain=2)
    frags = fragment(r.schema, r.rows, ("A",), [("B",), ("C",)])
    joined = reconstruct(frags, ("A",), r.schema)
    assert rel(r.schema, joined) == ref_reconstruct(frags, r.schema)
    # Without a key the join holds every row of R, but it can hold more rows or more copies.
    assert all(joined[t] >= c for t, c in r.rows.items())
    tschema, trows = with_tuple_id(r.schema, r.rows)
    assert is_key(tschema, trows, ("tid",))
    tfrags = fragment(tschema, trows, ("tid",), [("A", "B"), ("C",)])
    back = reconstruct(tfrags, ("tid",), tschema)
    assert back == trows
    assert dbrel.project(rel(tschema, back), r.schema) == r


def test_lossy_case_occurs():
    r = Counter({(0, 0, 0): 1, (0, 1, 1): 1})
    frags = fragment(("A", "B", "C"), r, ("A",), [("B",), ("C",)])
    assert reconstruct(frags, ("A",), ("A", "B", "C")) == Counter({(0, 0, 0): 1, (0, 0, 1): 1,
                                                                   (0, 1, 0): 1, (0, 1, 1): 1})


def test_null_in_the_key_loses_the_row():
    r = Counter({(None, 1, 2): 1, (5, 1, 2): 1})
    assert not is_key(("K", "A", "B"), r, ("K",))
    frags = fragment(("K", "A", "B"), r, ("K",), [("A",), ("B",)])
    assert reconstruct(frags, ("K",), ("K", "A", "B")) == Counter({(5, 1, 2): 1})


def test_rules():
    frags = fragment(EMP, EMP_ROWS, ("eno",), [("name",), ("name", "salary")])
    assert not is_disjoint(("eno",), frags) and not is_complete(EMP, frags)
    assert reconstruct(frags, ("eno",), ("eno", "name", "salary")) == dbrel.project(rel(EMP, EMP_ROWS),
                                                                                  ("eno", "name", "salary")).rows
