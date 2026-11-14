# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-flow-sensitive-pointer-analysis/. The authors are listed in prov/9J9RX5.jsonl.

import random

import ptsgen
from sparse_flow_sensitive_pointer_analysis import andersen, is_heap, reachable, sparse_fs

EMPTY = frozenset()


def dense(stmts, succ, aux):
    """The dense flow-sensitive reference: a full map from every name to its
    set before and after every reachable node, by round-robin iteration. A
    store writes the locations that its pointer may point to here, with a
    strong update for one location that is not a heap name. A store whose
    pointer points to nothing cannot run; it gives the empty set to the
    locations it may write by the auxiliary analysis aux."""
    nodes = reachable(succ)
    names = ptsgen.variables(stmts)
    preds = {n: [] for n in nodes}
    for n in nodes:
        for m in succ[n]:
            preds[m].append(n)
    IN = {n: {v: EMPTY for v in names} for n in nodes}
    OUT = {n: {v: EMPTY for v in names} for n in nodes}
    changed = True
    while changed:
        changed = False
        for n in nodes:
            inn = {v: frozenset().union(*(OUT[p][v] for p in preds[n])) for v in names}
            out = dict(inn)
            kind, x, y = stmts[n]
            if kind == "addr":
                out[x] = frozenset([y])
            elif kind == "copy":
                out[x] = inn[y]
            elif kind == "load":
                out[x] = frozenset().union(*(inn[b] for b in inn[y]))
            elif not inn[x]:
                for b in aux[x]:
                    out[b] = EMPTY
            elif len(inn[x]) == 1 and not is_heap(next(iter(inn[x]))):
                out[next(iter(inn[x]))] = inn[y]
            else:
                for b in inn[x]:
                    out[b] = inn[b] | inn[y]
            if inn != IN[n] or out != OUT[n]:
                IN[n], OUT[n] = inn, out
                changed = True
    return IN, OUT


def line(succ_count):
    return [[i + 1] for i in range(succ_count - 1)] + [[]]


PAGE = [
    ("addr", "p", "a"),
    ("addr", "x", "p"),
    ("load", "t", "x"),
    ("addr", "q", "b"),
    ("store", "x", "q"),
    ("load", "r", "x"),
    ("copy", "s", "p"),
]


def test_page_example_strong_update():
    succ = line(len(PAGE))
    ins, outs, users = sparse_fs(PAGE, succ)
    assert outs[(2, "t")] == {"a"}
    assert outs[(4, "p")] == {"b"}
    assert outs[(5, "r")] == {"b"}
    assert outs[(6, "s")] == {"b"}
    assert users[(0, "p")] == [2, 4]
    assert users[(4, "p")] == [5, 6]
    aux = andersen(PAGE)
    assert aux["t"] == aux["r"] == {"a", "b"}


def test_heap_location_gets_a_weak_update():
    stmts = [("addr", "q0", "a"), ("addr", "x", "h1"), ("store", "x", "q0"), ("addr", "q", "b"), ("store", "x", "q"), ("load", "r", "x")]
    _, outs, _ = sparse_fs(stmts, line(len(stmts)))
    assert outs[(5, "r")] == {"a", "b"}


def test_branches_join():
    stmts = [("addr", "x", "p"), ("addr", "q", "a"), ("addr", "q", "b"), ("store", "x", "q"), ("load", "r", "x")]
    succ = [[1, 2], [3], [3], [4], []]
    ins, outs, _ = sparse_fs(stmts, succ)
    assert ins[(3, "q")] == {"a", "b"}
    assert outs[(4, "r")] == {"a", "b"}


def test_unreachable_nodes_are_ignored():
    stmts = [("addr", "p", "a"), ("addr", "p", "b"), ("copy", "r", "p")]
    succ = [[2], [2], []]
    ins, outs, _ = sparse_fs(stmts, succ)
    assert ins[(2, "p")] == {"a"}
    assert (1, "p") not in outs


def random_cfg(rng, nvars, nnodes):
    stmts = []
    for kind, x, y in ptsgen.random_program(rng, nvars, nnodes):
        if kind == "addr" and rng.random() < 0.35:
            y = "h%d" % rng.randint(1, 2)
        stmts.append((kind, x, y))
    succ = []
    for i in range(nnodes):
        out = []
        if i + 1 < nnodes and rng.random() < 0.85:
            out.append(i + 1)
        if rng.random() < 0.3:
            out.append(rng.randrange(nnodes))
        succ.append(sorted(set(out)))
    return stmts, succ


def programs(seed, count, nvars=(2, 8), nnodes=(1, 25)):
    rng = random.Random(seed)
    for _ in range(count):
        yield rng, random_cfg(rng, rng.randint(*nvars), rng.randint(*nnodes))


def test_sparse_equals_dense():
    for _, (stmts, succ) in programs(2011, 400):
        aux = andersen(stmts)
        IN, OUT = dense(stmts, succ, aux)
        ins, outs, _ = sparse_fs(stmts, succ)
        for (u, w), s in ins.items():
            assert s == IN[u][w], (ptsgen.show(stmts), succ, u, w)
        for (d, v), s in outs.items():
            assert s == OUT[d][v], (ptsgen.show(stmts), succ, d, v)


def test_dense_is_inside_andersen():
    strict = 0
    for _, (stmts, succ) in programs(2004, 300):
        aux = andersen(stmts)
        assert aux == ptsgen.least_solution(stmts)
        IN, OUT = dense(stmts, succ, aux)
        for n in IN:
            for w, s in IN[n].items():
                assert s <= aux[w]
                strict += s < aux[w]
    assert strict > 0


def run(stmts, succ, rng, steps=60):
    """One random walk from the entry. Each execution of x = &h with a heap
    name h makes a fresh object (h, k). Yields (node, memory) before each
    node. A load or store through a pointer with no value stops the walk."""
    mem = {}
    n, fresh = 0, 0
    for _ in range(steps):
        yield n, dict(mem)
        kind, x, y = stmts[n]
        if kind == "addr":
            if is_heap(y):
                fresh += 1
                mem[x] = (y, fresh)
            else:
                mem[x] = y
        elif kind == "copy":
            mem[x] = mem.get(y)
        elif kind == "load":
            if mem.get(y) is None:
                return
            mem[x] = mem.get(mem[y])
        else:
            if mem.get(x) is None:
                return
            mem[mem[x]] = mem.get(y)
        if not succ[n]:
            return
        n = rng.choice(succ[n])


def name(loc):
    return loc if isinstance(loc, str) else loc[0]


def test_sound_against_concrete_runs():
    checked = 0
    for rng, (stmts, succ) in programs(2003, 300):
        aux = andersen(stmts)
        IN, _ = dense(stmts, succ, aux)
        ins, _, _ = sparse_fs(stmts, succ)
        for _ in range(5):
            for n, mem in run(stmts, succ, rng):
                for loc, val in mem.items():
                    if val is not None:
                        assert name(val) in IN[n][name(loc)], (ptsgen.show(stmts), succ)
                        if (n, name(loc)) in ins:
                            assert name(val) in ins[(n, name(loc))]
                            checked += 1
    assert checked > 500
