# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/allen-kennedy-algorithm/. The authors are listed in prov/WZS56G.jsonl.

import random

from allen_kennedy_algorithm import (
    MOD,
    Program,
    Stmt,
    book_example,
    codegen,
    dependence_graph,
    dependence_pairs,
    run_code,
    run_sequential,
    show,
    vector_levels,
)


def init_value(cell):
    v = 7
    for x in cell:
        v = (v * 1000003 + (ord(x) if isinstance(x, str) else x + 50)) % MOD
    return v


def random_program(rng):
    n = rng.randint(1, 3)
    bounds = [(rng.randint(0, 1), rng.randint(2, 3)) for _ in range(n)]
    while True:
        r = rng.randint(1, 4)
        depths = [rng.randint(1, n) for _ in range(r)]
        ok = True
        for l in range(n):
            pos = [p for p, d in enumerate(depths) if d > l]
            if pos and pos[-1] - pos[0] + 1 != len(pos):
                ok = False
        if ok:
            break
    arrays = {"A": rng.randint(1, 2), "B": rng.randint(1, 2), "C": 1}

    def access(d):
        arr = rng.choice("ABC")
        subs = []
        for _ in range(arrays[arr]):
            co = [0] * d
            if rng.random() < 0.85:
                co[rng.randrange(d)] = rng.choice([1, 1, 1, -1, 2])
            subs.append((tuple(co), rng.randint(-1, 1)))
        return (arr, subs)

    stmts = []
    for s, d in enumerate(depths):
        reads = [access(d) for _ in range(rng.randint(0, 2))]
        coefs = [rng.randrange(1, MOD) for _ in reads]
        idx = [rng.randrange(MOD) for _ in range(d)]
        stmts.append(Stmt(f"S{s + 1}", d, access(d), reads, coefs, rng.randrange(MOD), idx))
    return Program(bounds, stmts)


def on_cycle(graph, s, m):
    """Brute force: is s reachable from itself through edges of level >= m?"""
    succ = {}
    for a, b, lev in graph:
        if lev >= m:
            succ.setdefault(a, set()).add(b)
    seen, todo = set(), list(succ.get(s, ()))
    while todo:
        v = todo.pop()
        if v == s:
            return True
        if v not in seen:
            seen.add(v)
            todo.extend(succ.get(v, ()))
    return False


def ordered_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in ordered_partitions(rest):
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]
        for i in range(len(part) + 1):
            yield part[:i] + [[first]] + part[i:]


def all_codes(prog, region, k):
    """Every code of the model: loop distribution and statement order at each
    level, each piece a sequential loop at level k or a one-statement vector."""
    out = []
    for part in ordered_partitions(region):
        choices = []
        for block in part:
            opts = []
            if len(block) == 1:
                opts.append(("vec", block[0], k))
            if all(prog.stmts[s].depth >= k for s in block):
                for inner in all_codes(prog, sorted(block), k + 1):
                    opts.append(("loop", k, inner))
            choices.append(opts)
        combos = [[]]
        for opts in choices:
            combos = [c + [o] for c in combos for o in opts]
        out.extend(combos)
    return out


def keeps_all(prog, code, pairs):
    steps = {}
    run_code(prog, code, init_value, steps)
    return all(steps[a] < steps[b] for a, b in pairs)


def test_book_example():
    prog = book_example()
    code = codegen(prog, dependence_graph(prog))
    assert show(prog, code) == [
        "for i = 1 to 4:",
        "  for j = 1 to 4:",
        "    S2: B[j] = A[j][2]",
        "    vector (k): S3: A[j+1][k] = B[j] + C[j][k]",
        "  vector (j): S4: Y[i+j] = A[j+1][2]",
        "vector (i): S1: X[i] = Y[i] + 10",
    ]
    assert run_code(prog, code, init_value) == run_sequential(prog, init_value)


def test_simple_cases():
    s = lambda co, c: (tuple(co), c)
    # A[i+1] = A[i] + B[i]: a flow cycle at level 1, so a sequential loop.
    rec = Program([(1, 5)], [Stmt("S1", 1, ("A", [s([1], 1)]), [("A", [s([1], 0)]), ("B", [s([1], 0)])], [1, 1], 0)])
    assert codegen(rec, dependence_graph(rec)) == [("loop", 1, [("vec", 0, 2)])]
    # S1: A[i] = B[i]; S2: C[i] = A[i-1]: no cycle, both vector, S1 first.
    two = Program([(1, 5)], [
        Stmt("S1", 1, ("A", [s([1], 0)]), [("B", [s([1], 0)])], [1], 0),
        Stmt("S2", 1, ("C", [s([1], 0)]), [("A", [s([1], -1)])], [1], 0)])
    assert codegen(two, dependence_graph(two)) == [("vec", 0, 1), ("vec", 1, 1)]
    # Backward carried dependence: S1 reads A[i+1], S2 writes A[i]. The
    # vector code must put S1 first; its read of A[i+1] precedes S2's write.
    back = Program([(1, 5)], [
        Stmt("S1", 1, ("B", [s([1], 0)]), [("A", [s([1], 1)])], [1], 0),
        Stmt("S2", 1, ("A", [s([1], 0)]), [("C", [s([1], 0)])], [1], 0)])
    code = codegen(back, dependence_graph(back))
    assert code == [("vec", 0, 1), ("vec", 1, 1)]
    assert run_code(back, code, init_value) == run_sequential(back, init_value)
    # S1: C[i] = A[i-1]; S2: A[i] = B[i]. The only edge goes from S2 to S1
    # (carried flow), so the topological order puts S2 first. Text order
    # would read A before it is written.
    rev = Program([(1, 5)], [
        Stmt("S1", 1, ("C", [s([1], 0)]), [("A", [s([1], -1)])], [1], 0),
        Stmt("S2", 1, ("A", [s([1], 0)]), [("B", [s([1], 0)])], [1], 0)])
    code = codegen(rev, dependence_graph(rev))
    assert code == [("vec", 1, 1), ("vec", 0, 1)]
    assert run_code(rev, code, init_value) == run_sequential(rev, init_value)
    wrong = [("vec", 0, 1), ("vec", 1, 1)]
    assert run_code(rev, wrong, init_value) != run_sequential(rev, init_value)


def test_random_programs_keep_every_dependence():
    rng = random.Random(1987)
    for _ in range(300):
        prog = random_program(rng)
        pairs = dependence_pairs(prog)
        graph = dependence_graph(prog, pairs)
        code = codegen(prog, graph)
        steps = {}
        mem = run_code(prog, code, init_value, steps)
        for a, b in pairs:
            assert steps[a] < steps[b], (a, b)
        assert mem == run_sequential(prog, init_value)


def test_vector_level_is_first_acyclic_level():
    rng = random.Random(9)
    for _ in range(300):
        prog = random_program(rng)
        graph = dependence_graph(prog)
        lv = vector_levels(codegen(prog, graph))
        for s, st in enumerate(prog.stmts):
            m = 1
            while m <= prog.n and on_cycle(graph, s, m):
                m += 1
            assert lv[s] == m
            assert m <= st.depth + 1


def test_maximal_among_all_distributions():
    rng = random.Random(2001)
    tried = 0
    while tried < 60:
        prog = random_program(rng)
        if len(prog.stmts) > 3 or prog.n > 2:
            continue
        tried += 1
        pairs = dependence_pairs(prog)
        best = vector_levels(codegen(prog, dependence_graph(prog, pairs)))
        found_legal = False
        for code in all_codes(prog, list(range(len(prog.stmts))), 1):
            if keeps_all(prog, code, pairs):
                found_legal = True
                lv = vector_levels(code)
                for s in lv:
                    assert lv[s] >= best[s]
        assert found_legal
