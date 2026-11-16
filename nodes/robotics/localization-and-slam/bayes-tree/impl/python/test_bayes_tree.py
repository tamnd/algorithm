# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayes-tree/. The authors are listed in prov/XZ2CJC.jsonl.

import random

import pytest

from bayes_tree import BayesTree, LinearFactor, eliminate


def scalar(blocks, b):
    return LinearFactor({k: [[a]] for k, a in blocks.items()}, [b])


def kaess_example():
    """Poses x1, x2, x3 and landmarks l1, l2 on a line, unit noise."""
    return [
        scalar({"x1": 1.0}, 0.0),
        scalar({"x1": -1.0, "x2": 1.0}, 1.0),
        scalar({"x2": -1.0, "x3": 1.0}, 1.0),
        scalar({"x1": -1.0, "l1": 1.0}, 2.1),
        scalar({"x2": -1.0, "l1": 1.0}, 0.9),
        scalar({"x3": -1.0, "l2": 1.0}, 1.0),
    ]


def random_graph(rng, n, extra):
    """A connected random graph of variables of size 1 or 2 with an anchor on variable 0."""
    dims = {v: rng.choice([1, 2]) for v in range(n)}

    def block(v, rows):
        return [[rng.uniform(-1.0, 1.0) for _ in range(dims[v])] for _ in range(rows)]

    def factor(keys):
        rows = max(dims[k] for k in keys) + rng.choice([0, 1])
        return LinearFactor({k: block(k, rows) for k in keys}, [rng.uniform(-2.0, 2.0) for _ in range(rows)])

    fs = [LinearFactor({0: [[2.0 if i == j else 0.0 for j in range(dims[0])] for i in range(dims[0])]}, [0.5] * dims[0])]
    for v in range(1, n):
        fs.append(factor([rng.randrange(v), v]))
    for _ in range(extra):
        a, b = rng.sample(range(n), 2)
        fs.append(factor([a, b]))
    return fs, dims


def dense(factors, keys, dims):
    pos, n = {}, 0
    for k in keys:
        pos[k] = n
        n += dims[k]
    lam = [[0.0] * n for _ in range(n)]
    eta = [0.0] * n
    for f in factors:
        for u in f.keys:
            for w in f.keys:
                for i in range(dims[u]):
                    for j in range(dims[w]):
                        lam[pos[u] + i][pos[w] + j] += sum(f.blocks[u][r][i] * f.blocks[w][r][j] for r in range(len(f.b)))
            for i in range(dims[u]):
                eta[pos[u] + i] += sum(f.blocks[u][r][i] * f.b[r] for r in range(len(f.b)))
    return lam, eta, pos


def gauss(a, b):
    n = len(a)
    m = [list(a[r]) + [b[r]] for r in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            for k in range(c, n + 1):
                m[r][k] -= f * m[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][k] * x[k] for k in range(r + 1, n))) / m[r][r]
    return x


def check_against_dense(tree, factors, dims, tol=1e-8):
    keys = sorted(dims, key=repr)
    lam, eta, pos = dense(factors, keys, dims)
    ref = gauss(lam, eta)
    got = tree.solve()
    for k in keys:
        for i in range(dims[k]):
            assert abs(got[k][i] - ref[pos[k] + i]) < tol
    # the conditionals, read as factors, give the same Lambda and eta (R^T R = Lambda)
    conds = [cond.as_factor() for c in tree.cliques() for cond in c.conds.values()]
    tl, te, _ = dense(conds, keys, dims)
    assert max(abs(x - y) for r1, r2 in zip(lam, tl) for x, y in zip(r1, r2)) < tol
    assert max(abs(x - y) for x, y in zip(eta, te)) < tol


def check_invariants(tree, variables):
    seen = {}
    for c in tree.cliques():
        for v in c.frontals:
            seen[v] = seen.get(v, 0) + 1
            assert tree.clique_of[v] is c
        if c.parent is None:
            assert c.sep == [] and c in tree.roots
        else:
            assert c in c.parent.children
            assert set(c.sep) <= c.parent.variables()
        for i, v in enumerate(c.frontals):
            assert set(c.conds[v].parents) <= set(c.frontals[i + 1:]) | set(c.sep)
    assert seen == {v: 1 for v in variables}


def test_kaess_example_has_the_expected_cliques():
    tree = BayesTree.build(kaess_example(), order=["l1", "l2", "x1", "x2", "x3"])
    (root,) = tree.roots
    assert root.frontals == ["x2", "x3"] and root.sep == []
    kids = sorted((c.frontals, c.sep) for c in root.children)
    assert kids == [(["l1", "x1"], ["x2"]), (["l2"], ["x3"])]
    sol = tree.solve()
    # odometry says x2 - x1 = 1, the landmark says 1.2: three unit residuals share 0.2
    want = {"x1": 0.0, "x2": 1.0 + 0.2 / 3, "x3": 2.0 + 0.2 / 3, "l1": 2.1 - 0.2 / 3, "l2": 3.0 + 0.2 / 3}
    assert all(abs(sol[k][0] - want[k]) < 1e-12 for k in want)


def test_tree_solve_and_square_root_information_match_the_dense_system():
    rng = random.Random(11)
    for _ in range(25):
        n = rng.randint(2, 12)
        fs, dims = random_graph(rng, n, rng.randint(0, 2 * n))
        tree = BayesTree.build(fs)
        check_invariants(tree, dims)
        check_against_dense(tree, fs, dims)


def test_any_order_gives_the_same_solution():
    rng = random.Random(12)
    fs, dims = random_graph(rng, 9, 10)
    ref = BayesTree.build(fs).solve()
    for _ in range(5):
        order = list(dims)
        rng.shuffle(order)
        tree = BayesTree.build(fs, order)
        check_invariants(tree, dims)
        sol = tree.solve()
        assert max(abs(a - b) for k in dims for a, b in zip(sol[k], ref[k])) < 1e-8


def test_updates_keep_the_tree_equal_to_the_full_system():
    rng = random.Random(13)
    fs, dims = random_graph(rng, 30, 20)
    tree = BayesTree.build(fs[:5])
    have = list(fs[:5])
    for i in range(5, len(fs), 3):
        batch = fs[i:i + 3]
        tree.update(batch)
        have += batch
        part = {k for f in have for k in f.keys}
        check_invariants(tree, part)
        check_against_dense(tree, have, {k: dims[k] for k in part})


def test_adding_odometry_at_the_newest_pose_touches_only_the_root():
    fs = kaess_example()
    tree = BayesTree.build(fs, order=["l1", "l2", "x1", "x2", "x3"])
    (old_root,) = tree.roots
    kids = list(old_root.children)
    new = scalar({"x3": -1.0, "x4": 1.0}, 1.0)
    removed, made = tree.update([new])
    assert (removed, made) == (1, 2)
    (root,) = tree.roots
    assert root.frontals == ["x3", "x4"]
    # the two old children are the same objects, moved under the new cliques
    assert all(k in tree.cliques() for k in kids)
    assert tree.clique_of["x1"].parent is tree.clique_of["x2"]
    assert tree.clique_of["l2"].parent is root
    dims = {v: 1 for v in ["x1", "x2", "x3", "x4", "l1", "l2"]}
    check_invariants(tree, dims)
    check_against_dense(tree, fs + [new], dims)


def test_chain_updates_eliminate_a_bounded_number_of_cliques():
    fs = [scalar({0: 1.0}, 0.0)]
    tree = BayesTree.build(fs)
    for t in range(1, 40):
        removed, made = tree.update([scalar({t - 1: -1.0, t: 1.0}, 1.0)])
        assert removed == 1 and made <= 2
    sol = tree.solve()
    assert all(abs(sol[t][0] - t) < 1e-9 for t in range(40))


def test_missing_anchor_is_rank_deficient():
    fs = [scalar({"a": -1.0, "b": 1.0}, 1.0)]
    with pytest.raises(ValueError):
        eliminate(fs, ["a", "b"])
