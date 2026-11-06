# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shared-packed-parse-forest/. The authors are listed in prov/86960D.jsonl.

import itertools
import math
import random

from shared_packed_parse_forest import SPPF


def grammar(text):
    prods = []
    for rule in text.split(";"):
        a, rhs = rule.split("->")
        for alt in rhs.split("|"):
            prods.append((a.strip(), tuple(x for x in alt.split() if x != "eps")))
    return prods


def spans(prods, w):
    """Oracle: the set of (X, i, j) with nonterminal X =>* w[i:j], by a least fixpoint."""
    nts = {a for a, _ in prods}
    n, known = len(w), set()
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            for i in range(n + 1):
                for j in range(i, n + 1):
                    if (a, i, j) not in known and splits(rhs, i, j, w, nts, known):
                        known.add((a, i, j))
                        changed = True
    return known


def splits(rhs, i, j, w, nts, known):
    """All boundary lists i = b0 <= ... <= bm = j with rhs[t] deriving w[b_t:b_t+1]."""
    out = []
    for cut in itertools.combinations_with_replacement(range(i, j + 1), max(len(rhs) - 1, 0)):
        b = [i, *cut, j] if rhs else [i, j]
        if not rhs:
            if i == j:
                out.append([i])
            continue
        ok = True
        for t, x in enumerate(rhs):
            if x in nts:
                ok = (x, b[t], b[t + 1]) in known
            else:
                ok = b[t + 1] == b[t] + 1 and w[b[t]] == x
            if not ok:
                break
        if ok:
            out.append(b)
    return out


def oracle(prods, start, w):
    """Brute force: (cyclic?, number of trees or inf, set of cycle-free trees)."""
    nts = {a for a, _ in prods} | {start}
    known = spans(prods, w)
    n = len(w)
    if (start, 0, n) not in known:
        return False, 0, set()
    # graph on triples, found by trying every split of every production
    edges = {}
    for a, i, j in known:
        for p, (b, rhs) in enumerate(prods):
            if b != a:
                continue
            for bd in splits(rhs, i, j, w, nts, known):
                edges.setdefault((a, i, j), []).append((p, bd))
    reach, todo = {(start, 0, n)}, [(start, 0, n)]
    while todo:
        u = todo.pop()
        for p, bd in edges.get(u, ()):
            for t, x in enumerate(prods[p][1]):
                if x in nts and (x, bd[t], bd[t + 1]) not in reach:
                    reach.add((x, bd[t], bd[t + 1]))
                    todo.append((x, bd[t], bd[t + 1]))
    # cycle among reachable triples: repeatedly remove triples with no successor left
    succ = {u: {(x, bd[t], bd[t + 1]) for p, bd in edges.get(u, ())
                for t, x in enumerate(prods[p][1]) if x in nts} for u in reach}
    alive = set(reach)
    changed = True
    while changed:
        changed = False
        for u in list(alive):
            if not (succ[u] & alive):
                alive.discard(u)
                changed = True
    cyclic = bool(alive)

    def enum(x, i, j, path, budget=[0]):
        if x not in nts:
            return [x]
        if (x, i, j) in path:
            return []
        out = []
        for p, bd in edges.get((x, i, j), ()):
            rhs = prods[p][1]
            parts = [enum(y, bd[t], bd[t + 1], path | {(x, i, j)}) for t, y in enumerate(rhs)]
            for combo in itertools.product(*parts):
                out.append((x, combo))
                budget[0] += 1
                if budget[0] > 20000:
                    raise OverflowError
        return out

    try:
        free = enum(start, 0, n, frozenset())
    except OverflowError:
        free = None
    if cyclic:
        return True, math.inf, free
    return False, None if free is None else len(free), free


def tree_ok(tree, prods, start, w):
    pset = set(prods)
    if tree[0] != start:
        return False
    leaves, stack = [], [tree]
    while stack:
        t = stack.pop()
        if isinstance(t, str):
            leaves.append(t)
            continue
        a, kids = t
        if (a, tuple(k if isinstance(k, str) else k[0] for k in kids)) not in pset:
            return False
        stack.extend(reversed(kids))
    return leaves == list(w)


def random_grammar(rng):
    names = ["S", "A", "B"][: rng.randint(1, 3)]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            k = rng.choice([0, 1, 1, 2, 2, 3])
            prods.append((a, tuple(rng.choice(names + ["a", "b", "a"]) for _ in range(k))))
    return list(dict.fromkeys(prods))


def test_random_grammars_against_brute_force():
    rng = random.Random(2008)
    stats = {"checked": 0, "cyclic": 0, "ambiguous": 0, "unique": 0, "none": 0, "empty_word": 0}
    kinds = {"eps": 0, "unit": 0, "left": 0}
    for _ in range(400):
        g = random_grammar(rng)
        start = g[0][0]
        nts = {a for a, _ in g}
        kinds["eps"] += any(not r for _, r in g)
        kinds["unit"] += any(len(r) == 1 and r[0] in nts for _, r in g)
        kinds["left"] += any(r and r[0] == a for a, r in g)
        for n in range(5):
            for w in itertools.product("ab", repeat=n):
                w = list(w)
                f = SPPF(g, start, w)
                cyclic, count, free = oracle(g, start, w)
                stats["checked"] += 1
                assert f.is_cyclic() == cyclic, (g, w)
                if count == 0:
                    assert f.root is None and f.count() == 0 and f.one_tree() is None
                    assert not f.is_ambiguous()
                    stats["none"] += 1
                    continue
                stats["empty_word"] += n == 0
                one = f.one_tree()
                assert tree_ok(one, g, start, w) and f.contains(one), (g, w)
                if free is not None:
                    for t in free:
                        assert f.contains(t), (g, w, t)
                if cyclic:
                    assert f.count() == math.inf and f.is_ambiguous()
                    stats["cyclic"] += 1
                    continue
                if count is None:
                    continue
                assert f.count() == count, (g, w)
                assert f.is_ambiguous() == (count > 1)
                stats["ambiguous" if count > 1 else "unique"] += 1
                if count <= 300:
                    ts = f.trees()
                    assert len(set(ts)) == len(ts) == count
                    assert set(ts) == set(free) and len(set(free)) == len(free)
                # size bounds of the binarized forest
                sym, mid, packed = f.size()
                size_g = sum(len(r) + 1 for _, r in g)
                assert sym <= (len(nts) + 2) * (n + 1) ** 2
                assert packed <= size_g * (n + 1) ** 2 * (n + 2)
    assert stats["checked"] >= 10000
    assert min(stats.values()) >= 100, stats
    assert min(kinds.values()) >= 50, kinds


def test_contains_rejects_wrong_trees():
    rng = random.Random(7)
    g = grammar("E -> E + E | E * E | id")
    w = ["id", "+", "id", "*", "id", "+", "id"]
    f = SPPF(g, "E", w)
    assert f.count() == 5  # the Catalan number C_3
    other = SPPF(g, "E", ["id", "*", "id", "+", "id", "*", "id"])
    for t in other.trees():
        assert not f.contains(t)
    for t in f.trees():
        assert f.contains(t)
    # relabel one internal node: no longer a tree of the forest
    for _ in range(50):
        t = f.tree(rng.randrange(5))
        bad = ("T", t[1])
        assert not f.contains(bad)


def test_page_example():
    g = grammar("E -> E + E | id")
    w = ["id", "+", "id", "+", "id"]
    f = SPPF(g, "E", w)
    assert f.count() == 2 and f.is_ambiguous()
    root = ("sym", "E", 0, 5)
    assert sorted(f.packed[root]) == [
        (0, 2, ("mid", 0, 2, 0, 2), ("sym", "E", 2, 5)),
        (0, 4, ("mid", 0, 2, 0, 4), ("sym", "E", 4, 5)),
    ]
    sym, mid, packed = f.size()
    assert (sym, mid, packed) == (11, 3, 10)
    left = ("E", (("E", (("E", ("id",)), "+", ("E", ("id",)))), "+", ("E", ("id",))))
    right = ("E", (("E", ("id",)), "+", ("E", (("E", ("id",)), "+", ("E", ("id",))))))
    assert set(f.trees()) == {left, right}


def test_catalan_growth_with_cubic_size():
    g = grammar("S -> S S | a")
    for n in range(1, 16):
        f = SPPF(g, "S", ["a"] * n)
        assert f.count() == math.comb(2 * (n - 1), n - 1) // n
        sym, mid, packed = f.size()
        assert sym == n * (n + 1) // 2 + n
        assert packed == n + (n - 1) * n * (n + 1) // 6


def test_cycles_epsilon_and_empty_input():
    f = SPPF(grammar("S -> S | a"), "S", ["a"])
    assert f.is_cyclic() and f.count() == math.inf
    assert f.one_tree() == ("S", ("a",))
    f = SPPF(grammar("S -> S S | eps"), "S", [])
    assert f.is_cyclic() and f.one_tree() == ("S", ())
    f = SPPF(grammar("S -> A A; A -> a | eps"), "S", [])
    assert f.count() == 1 and f.trees() == [("S", (("A", ()), ("A", ())))]
    f = SPPF(grammar("S -> A A; A -> a | eps"), "S", ["a"])
    assert f.count() == 2
    f = SPPF(grammar("S -> a"), "S", [])
    assert f.root is None and f.count() == 0 and f.trees() == []
    f = SPPF(grammar("S -> S a | eps"), "S", [])
    assert f.count() == 1


def test_long_input_iterative():
    n = 3000
    f = SPPF(grammar("S -> a S | a"), "S", ["a"] * n)
    assert f.count() == 1
    t = f.tree(0)
    assert f.contains(t) and f.one_tree() == t
    depth = 0
    while not isinstance(t, str) and len(t[1]) == 2:
        t = t[1][1]
        depth += 1
    assert depth == n - 1
