# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/predicate-pushdown/. The authors are listed in prov/75V2SP.jsonl.

import random
from collections import Counter

from predicate_pushdown import Join, LeftJoin, Pred, Proj, Rel, Sel, bag, evaluate, push_down, schema

R, S, T = Rel("R", ("a", "b")), Rel("S", ("c", "d")), Rel("T", ("e", "f"))


def eq(x, y):
    return Pred(frozenset({x, y}), lambda r: r[x] == r[y], f"{x}={y}")


def lt(x, k):
    return Pred(frozenset({x}), lambda r: r[x] < k, f"{x}<{k}")


def rand_db(rng):
    db = {}
    for rel in (R, S, T):
        db[rel.name] = [{a: rng.randrange(4) for a in rel.schema} for _ in range(rng.randrange(6))]
    return db


def rand_pred(rng, attrs):
    attrs = sorted(attrs)
    if rng.random() < 0.5:
        return lt(rng.choice(attrs), rng.randrange(1, 4))
    return eq(rng.choice(attrs), rng.choice(attrs))


def rand_tree(rng):
    rels = [R, S, T]
    rng.shuffle(rels)
    t = rels[0]
    for r in rels[1:]:
        left, right = (t, r) if rng.random() < 0.5 else (r, t)
        sch = schema(left) | schema(right)
        on = tuple(rand_pred(rng, sch) for _ in range(rng.randrange(3)))
        kind = LeftJoin if rng.random() < 0.4 else Join
        t = kind(on, left, right)
        if rng.random() < 0.3:
            t = Sel((rand_pred(rng, schema(t)),), t)
    if rng.random() < 0.3:
        keep = tuple(sorted(rng.sample(sorted(schema(t)), 4)))
        t = Proj(keep, t)
    top = tuple(rand_pred(rng, schema(t)) for _ in range(rng.randrange(4)))
    return Sel(top, t)


def selections_are_low(t, allowed=True):
    """Each Sel sits on a Rel, or above a LeftJoin with a predicate it may not cross."""
    if isinstance(t, Rel):
        return True
    if isinstance(t, Sel):
        c = t.child
        if isinstance(c, Rel):
            return True
        if isinstance(c, LeftJoin) and all(not p.attrs <= schema(c.left) for p in t.preds):
            return selections_are_low(c)
        return False
    if isinstance(t, Proj):
        return selections_are_low(t.child)
    return selections_are_low(t.left) and selections_are_low(t.right)


def test_pushdown_preserves_the_bag_on_random_inputs():
    rng = random.Random(11)
    for _ in range(600):
        tree = rand_tree(rng)
        pushed = push_down(tree)
        assert selections_are_low(pushed)
        db = rand_db(rng)
        s1, s2 = Counter(), Counter()
        assert bag(evaluate(tree, db, s1)) == bag(evaluate(pushed, db, s2))
        assert s2["join rows"] <= s1["join rows"]


def test_worked_example():
    # sigma_(a<10 and c<5 and b=c) (R x S)  becomes  sigma_(a<10) R  join_(b=c)  sigma_(c<5) S
    tree = Sel((lt("a", 10), lt("c", 5), eq("b", "c")), Join((), R, S))
    pushed = push_down(tree)
    assert isinstance(pushed, Join) and [p.name for p in pushed.preds] == ["b=c"]
    assert pushed.left == Sel((lt("a", 10),), R) and pushed.right == Sel((lt("c", 5),), S)
    rng = random.Random(5)
    db = {"R": [{"a": rng.randrange(100), "b": rng.randrange(20)} for _ in range(200)],
          "S": [{"c": rng.randrange(20), "d": rng.randrange(9)} for _ in range(200)]}
    s1, s2 = Counter(), Counter()
    out = evaluate(tree, db, s1)
    assert bag(out) == bag(evaluate(pushed, db, s2))
    assert len(out) == 24 and s1["join rows"] == 40000 and s2["join rows"] == 24
    assert len(evaluate(pushed.left, db)) == 13 and len(evaluate(pushed.right, db)) == 67


def test_where_on_null_supplying_side_is_not_pushed():
    # SELECT * FROM R LEFT JOIN S ON a = c WHERE d = 1
    tree = Sel((Pred(frozenset({"d"}), lambda r: r["d"] == 1, "d=1"),), LeftJoin((eq("a", "c"),), R, S))
    db = {"R": [{"a": 1, "b": 0}, {"a": 2, "b": 0}], "S": [{"c": 1, "d": 1}, {"c": 2, "d": 5}]}
    want = bag(evaluate(tree, db))
    assert want == bag([{"a": 1, "b": 0, "c": 1, "d": 1}])
    assert bag(evaluate(push_down(tree), db)) == want
    wrong = LeftJoin((eq("a", "c"),), R, Sel(tree.preds, S))
    assert bag(evaluate(wrong, db)) != want  # the a = 2 row comes back padded with nulls


def test_on_predicate_on_preserved_side_is_not_pushed():
    # R LEFT JOIN S ON a = c AND a > 1 keeps the row a = 1 with nulls.
    gt1 = Pred(frozenset({"a"}), lambda r: r["a"] > 1, "a>1")
    tree = LeftJoin((eq("a", "c"), gt1), R, S)
    db = {"R": [{"a": 1, "b": 0}, {"a": 2, "b": 0}], "S": [{"c": 1, "d": 0}, {"c": 2, "d": 0}]}
    assert bag(evaluate(push_down(tree), db)) == bag(evaluate(tree, db))
    wrong = LeftJoin((eq("a", "c"),), Sel((gt1,), R), S)
    assert bag(evaluate(wrong, db)) != bag(evaluate(tree, db))


def test_empty_and_no_predicates():
    assert push_down(R) == R
    assert push_down(Sel((), R)) == R
    assert evaluate(push_down(Sel((lt("a", 1),), R)), {"R": []}) == []
