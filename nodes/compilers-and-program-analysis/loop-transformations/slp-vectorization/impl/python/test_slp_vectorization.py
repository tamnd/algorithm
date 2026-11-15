# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slp-vectorization/. The authors are listed in prov/VMGC16.jsonl.

import random

from slp_vectorization import (
    run_scalar,
    run_vector,
    schedule,
    show,
    slp_vectorize,
    unrolled_example,
)


def touched(st):
    """Brute force, written apart from the module: (reads, write) as sets."""
    kind, tgt, arg = st
    if kind == "load":
        return {("mem",) + tuple(arg)}, ("var", tgt)
    if kind == "store":
        r = {("var", arg)} if isinstance(arg, str) else set()
        return r, ("mem",) + tuple(tgt)
    return {("var", a) for a in arg[1:] if isinstance(a, str)}, ("var", tgt)


def brute_deps(block):
    deps = set()
    for s in range(len(block)):
        rs, ws = touched(block[s])
        for t in range(s + 1, len(block)):
            rt, wt = touched(block[t])
            if ws == wt or ws in rt or wt in rs:
                deps.add((s, t))
    return deps


def brute_paths(n, deps):
    succ = {}
    for s, t in deps:
        succ.setdefault(s, []).append(t)
    paths = set()
    for s in range(n):
        todo, seen = list(succ.get(s, [])), set()
        while todo:
            t = todo.pop()
            if t not in seen:
                seen.add(t)
                paths.add((s, t))
                todo.extend(succ.get(t, []))
    return paths


def names_and_cells(block):
    names, cells = set(), set()
    for st in block:
        rs, w = touched(st)
        for loc in rs | {w}:
            (names if loc[0] == "var" else cells).add(loc[1:] if loc[0] == "mem" else loc[1])
    return names, cells


def random_state(block, rng):
    names, cells = names_and_cells(block)
    env = {x: rng.randint(-9, 9) for x in names}
    mem = {c: rng.randint(-9, 9) for c in cells}
    return env, mem


def check(block, code, vl):
    flat = sorted(s for item in code for s in item)
    assert flat == list(range(len(block)))
    deps = brute_deps(block)
    paths = brute_paths(len(block), deps)
    where = {s: k for k, item in enumerate(code) for s in item}
    for s, t in deps:
        assert where[s] < where[t], (s, t)
    packs = 0
    for item in code:
        assert 1 <= len(item) <= vl
        if len(item) == 1:
            continue
        packs += 1
        sts = [block[s] for s in item]
        k = sts[0][0]
        for st in sts:
            assert st[0] == k
            if k == "load":
                assert st[2][0] == sts[0][2][0]
            elif k == "store":
                assert st[1][0] == sts[0][1][0]
            else:
                assert st[2][0] == sts[0][2][0]
        for a in item:
            for b in item:
                assert (a, b) not in paths
        for x, y in zip(sts, sts[1:]):
            if k == "load":
                assert y[2] == (x[2][0], x[2][1] + 1)
            if k == "store":
                assert y[1] == (x[1][0], x[1][1] + 1)
    return packs


def random_block(rng):
    lanes = rng.randint(2, 5)
    template, tvars = [], []
    for j in range(rng.randint(2, 6)):
        r = rng.random()
        if r < 0.4 or len(tvars) < 1:
            template.append(("load", f"t{j}", (rng.choice("ABC"), rng.randint(0, 4))))
            tvars.append(f"t{j}")
        elif r < 0.8:
            a = rng.choice(tvars)
            b = rng.choice(tvars + [rng.randint(1, 3)])
            template.append(("op", f"t{j}", (rng.choice("+-*"), a, b)))
            tvars.append(f"t{j}")
        else:
            template.append(("store", (rng.choice("ABC"), rng.randint(0, 4)), rng.choice(tvars)))

    def inst(st, k):
        kind, tgt, arg = st
        if kind == "load":
            return ("load", f"{tgt}_{k}", (arg[0], arg[1] + k))
        if kind == "store":
            return ("store", (tgt[0], tgt[1] + k), f"{arg}_{k}")
        o, a, b = arg
        nm = lambda x: f"{x}_{k}" if isinstance(x, str) else x
        return ("op", f"{tgt}_{k}", (o, nm(a), nm(b)))

    lane_code = [[inst(st, k) for st in template] for k in range(lanes)]
    block = []
    if rng.random() < 0.5:
        for code in lane_code:
            block += code
    else:
        pos = [0] * lanes
        while any(pos[k] < len(lane_code[k]) for k in range(lanes)):
            k = rng.choice([k for k in range(lanes) if pos[k] < len(lane_code[k])])
            block.append(lane_code[k][pos[k]])
            pos[k] += 1
    for _ in range(rng.randint(0, 2)):
        p = rng.randrange(len(block))
        kind, tgt, arg = block[p]
        if kind == "op":
            block[p] = (kind, rng.choice([tgt, "t0_0"]), (rng.choice("+-*"),) + arg[1:])
        elif kind == "load":
            block[p] = (kind, tgt, (arg[0], rng.randint(0, 6)))
        else:
            block[p] = (kind, (rng.choice("ABC"), rng.randint(0, 6)), arg)
    return block


def test_unrolled_loop():
    b = unrolled_example()
    code = slp_vectorize(b)
    assert show(b, code) == [
        "<b0, b1, b2, b3> = B[0:4]",
        "<c0, c1, c2, c3> = C[0:4]",
        "<m0, m1, m2, m3> = <b0, b1, b2, b3> * <c0, c1, c2, c3>",
        "<d0, d1, d2, d3> = D[0:4]",
        "<s0, s1, s2, s3> = <m0, m1, m2, m3> + <d0, d1, d2, d3>",
        "A[0:4] = <s0, s1, s2, s3>",
    ]
    assert check(b, code, 4) == 6
    rng = random.Random(4)
    env, mem = random_state(b, rng)
    assert run_vector(b, code, env, mem) == run_scalar(b, env, mem)
    # With two lanes the same block gives two groups per operation.
    code2 = slp_vectorize(b, vl=2)
    assert len(code2) == 12 and check(b, code2, 2) == 12
    assert run_vector(b, code2, env, mem) == run_scalar(b, env, mem)


def test_dependent_chain_is_not_packed():
    # a = A[0]; b = a + 1; A[1] = b; c = A[1]; d = c + 1; A[2] = d
    b = [("load", "a", ("A", 0)), ("op", "b", ("+", "a", 1)), ("store", ("A", 1), "b"),
         ("load", "c", ("A", 1)), ("op", "d", ("+", "c", 1)), ("store", ("A", 2), "d")]
    code = slp_vectorize(b)
    assert code == [[0], [1], [2], [3], [4], [5]]


def test_cycle_between_groups_is_split():
    # Groups {0, 3} and {1, 2} wait for each other: 0 -> 2 and 1 -> 3.
    b = [("store", ("A", 0), "p"), ("store", ("B", 0), "r"),
         ("load", "x", ("A", 0)), ("load", "y", ("B", 0))]
    deps = brute_deps(b)
    code = schedule(b, deps, [[0, 3], [1, 2]])
    assert code == [[0], [1, 2], [3]]
    env, mem = {"p": 5, "r": 7}, {("A", 0): 1, ("B", 0): 2}
    assert run_vector(b, code, env, mem) == run_scalar(b, env, mem)


def test_random_blocks():
    rng = random.Random(2000)
    total_packs = 0
    for trial in range(400):
        block = random_block(rng)
        for vl in (2, 4):
            code = slp_vectorize(block, vl)
            total_packs += check(block, code, vl)
            for _ in range(3):
                env, mem = random_state(block, rng)
                assert run_vector(block, code, env, mem) == run_scalar(block, env, mem)
    assert total_packs > 500


def test_wrong_grouping_is_caught():
    # Packing two dependent statements into one instruction changes the result,
    # which is why the algorithm needs independence.
    b = [("op", "x", ("+", "a", 1)), ("op", "y", ("+", "x", 1))]
    env = {"a": 3, "x": 0}
    assert run_vector(b, [[0, 1]], env, {}) != run_scalar(b, env, {})
    assert slp_vectorize(b) == [[0], [1]]
