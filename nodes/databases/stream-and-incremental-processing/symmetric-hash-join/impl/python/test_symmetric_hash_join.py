# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symmetric-hash-join/. The authors are listed in prov/2VN9MN.jsonl.

import random
from collections import Counter

import dbrel
from symmetric_hash_join import R, S, SymmetricHashJoin, symmetric_hash_join


def oracle(schema_r, schema_s, r_rows, s_rows):
    rel = dbrel.natural_join(dbrel.Relation(schema_r, r_rows), dbrel.Relation(schema_s, s_rows))
    return rel.rows


def run_and_check(schema_r, schema_s, arrivals):
    """After every arrival, the output so far must equal the join of the prefixes."""
    join = SymmetricHashJoin(schema_r, schema_s)
    seen_r, seen_s, out = [], [], Counter()
    for side, t in arrivals:
        out.update(join.insert(side, t))
        (seen_r if side == R else seen_s).append(tuple(t))
        assert out == oracle(schema_r, schema_s, seen_r, seen_s)
    assert join.out_schema == dbrel.natural_join(
        dbrel.Relation(schema_r, []), dbrel.Relation(schema_s, [])).schema
    return join, out


def interleave(rng, r_rows, s_rows):
    tags = [R] * len(r_rows) + [S] * len(s_rows)
    rng.shuffle(tags)
    it = {R: iter(r_rows), S: iter(s_rows)}
    return [(side, next(it[side])) for side in tags]


def test_page_example() -> None:
    arrivals = [(R, (1, 10)), (S, (10, "p")), (R, (2, 20)), (S, (10, "q")), (R, (3, 10)), (S, (20, "r"))]
    steps = symmetric_hash_join(("A", "B"), ("B", "C"), arrivals)
    assert [len(x) for x in steps] == [0, 1, 0, 1, 2, 1]
    assert steps[4] == [(3, 10, "p"), (3, 10, "q")]
    run_and_check(("A", "B"), ("B", "C"), arrivals)


def test_hand_cases() -> None:
    # Empty inputs and one tuple.
    assert symmetric_hash_join(("A", "B"), ("B", "C"), []) == []
    assert symmetric_hash_join(("A", "B"), ("B", "C"), [(S, (1, 2))]) == [[]]
    # All tuples with the same key: every pair once, n * m in total.
    arr = [(R, (i, 0)) for i in range(4)] + [(S, (0, j)) for j in range(3)]
    join, out = run_and_check(("A", "B"), ("B", "C"), arr)
    assert sum(out.values()) == 12 and join.memory() == 7
    # Duplicates multiply.
    join, out = run_and_check(("A", "B"), ("B", "C"), [(R, (1, 5)), (R, (1, 5)), (S, (5, 7)), (S, (5, 7))])
    assert out == Counter({(1, 5, 7): 4})
    # NULL keys never match and are not stored.
    join, out = run_and_check(("A", "B"), ("B", "C"), [(R, (1, None)), (S, (None, 2)), (S, (3, 4))])
    assert not out and join.memory() == 1
    # No common attribute: the product.
    join, out = run_and_check(("A",), ("C",), [(R, (1,)), (S, (2,)), (R, (3,))])
    assert out == Counter({(1, 2): 1, (3, 2): 1})


def test_random_interleavings() -> None:
    schemas = [(("A", "B"), ("B", "C")), (("A", "B", "C"), ("B", "C", "D")), (("A",), ("A",))]
    for seed in range(60):
        rng = random.Random(seed)
        schema_r, schema_s = schemas[seed % len(schemas)]
        r_rel = dbrel.random_relation(rng, schema_r, rng.randrange(0, 25), 3, null_rate=0.1)
        s_rel = dbrel.random_relation(rng, schema_s, rng.randrange(0, 25), 3, null_rate=0.1)
        r_rows = r_rel.sorted_rows()
        s_rows = s_rel.sorted_rows()
        rng.shuffle(r_rows)
        rng.shuffle(s_rows)
        join, out = run_and_check(schema_r, schema_s, interleave(rng, r_rows, s_rows))
        # Memory holds every tuple whose key has no NULL.
        k_r = [schema_r.index(a) for a in join.common]
        k_s = [schema_s.index(a) for a in join.common]
        keep = sum(all(t[i] is not None for i in k_r) for t in r_rows)
        keep += sum(all(t[i] is not None for i in k_s) for t in s_rows)
        assert join.memory() == keep
        # The probes that find a match are exactly the output pairs.
        assert join.probes == sum(out.values())


def test_order_does_not_change_the_result() -> None:
    rng = random.Random(7)
    r_rows = dbrel.random_relation(rng, ("A", "B"), 20, 4).sorted_rows()
    s_rows = dbrel.random_relation(rng, ("B", "C"), 20, 4).sorted_rows()
    results = set()
    for _ in range(10):
        steps = symmetric_hash_join(("A", "B"), ("B", "C"), interleave(rng, r_rows, s_rows))
        results.add(frozenset(Counter(t for x in steps for t in x).items()))
    assert len(results) == 1
