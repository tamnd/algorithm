# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ide-framework/. The authors are listed in prov/60PTYF.jsonl.

import random

import toyir
from toyir import parse, random_program
from ide_framework import (
    BOT,
    BOTF,
    EXIT,
    ID,
    RET,
    TOP,
    TOPF,
    ZERO,
    Supergraph,
    apply,
    compose,
    ide,
    ide_framework,
    meet_fn,
    meet_val,
)

# The example of the page: add is linear in its first parameter, so each
# call with a constant first argument gives a constant, even though the
# first parameter is not a constant at the entry of add.
ADD = """
# params: a, b
B0:
  t = a * 3
  u = t + 1
  ret u
"""

MAIN = """
# params: n
B0:
  x = 2
  y = call add(x, n)
  z = call add(n, x)
  v = 4
  w = call add(v, y)
  ret w
"""


def add_module():
    return {"main": parse(MAIN), "add": parse(ADD)}


def leq(a, b):
    """a is below or equal to b in the value lattice."""
    return a == BOT or b == TOP or a == b


# ---------------------------------------------------- micro-function algebra

DOMAIN = list(range(-40, 41)) + [BOT]


def table(f):
    return [apply(f, l) for l in DOMAIN]


def random_fn(rng):
    r = rng.random()
    if r < 0.1:
        return BOTF
    if r < 0.3:
        return ("const", rng.randint(-10, 10))
    if r < 0.8:
        return ("line", rng.choice([-3, -2, -1, 1, 2, 3]), rng.randint(-6, 6))
    return ("point", rng.randint(-5, 5), rng.randint(-10, 10))


def canonical(f):
    if f[0] == "line":
        return f[1] != 0
    if f[0] == "point":
        return f[2] != BOT and f[2] != TOP
    return f[0] in ("top", "bot", "const")


def test_micro_functions() -> None:
    rng = random.Random(6001)
    for _ in range(800):
        f, g = random_fn(rng), random_fn(rng)
        m = meet_fn(f, g)
        assert canonical(m)
        assert table(m) == [meet_val(x, y) for x, y in zip(table(f), table(g))]
        assert meet_fn(g, f) == m
        c = compose(g, f)
        assert canonical(c)
        assert table(c) == [apply(g, apply(f, l)) for l in DOMAIN]
        # Distributive over the meet of two inputs.
        l1, l2 = rng.choice(DOMAIN), rng.choice(DOMAIN)
        assert apply(f, meet_val(l1, l2)) == meet_val(apply(f, l1), apply(f, l2))
        # The same table means the same tuple.
        if table(f) == table(g):
            assert f == g
    for f in [BOTF, ("const", 3), ("line", 2, 1), ("point", 1, 4)]:
        assert meet_fn(TOPF, f) == f and compose(f, TOPF) == TOPF and compose(TOPF, f) == TOPF
        assert compose(ID, f) == f and compose(f, ID) == f
        assert apply(f, TOP) == TOP
    # A chain of meets goes down at most three times from TOPF.
    for _ in range(400):
        f, steps = TOPF, 0
        for _ in range(8):
            g = meet_fn(f, random_fn(rng))
            if g != f:
                steps += 1
            f = g
        assert steps <= 3


# ------------------------------------------------------------ brute force


def step(env, flow):
    """Push an environment (fact -> value, TOP left out) over one edge."""
    out = {}
    for d, v in env.items():
        for d2, g in flow(d):
            out[d2] = meet_val(out.get(d2, TOP), apply(g, v))
    return out


def start_env(sg, seeds):
    env = {ZERO: BOT}
    for x in sg.module[sg.main].params:
        env[x] = (seeds or {}).get(x, BOT)
    return env


def mvp_by_paths(sg, seeds=None, cap=20000, max_depth=None):
    """The meet over all valid paths, by walking each valid path from the
    start of main with its own environment. At a call node the path either
    enters the callee or takes the call-to-return edge; at an exit it goes
    back to the call on top of its stack. Returns None after cap steps."""
    M = {n: {} for n in sg.nodes}
    todo = [(sg.start[sg.main], start_env(sg, seeds), ())]
    steps = 0
    while todo:
        n, env, stack = todo.pop()
        steps += 1
        if steps > cap:
            return None
        for d, v in env.items():
            M[n][d] = meet_val(M[n].get(d, TOP), v)
        if n in sg.callee:
            if max_depth is None or len(stack) < max_depth:
                todo.append((sg.start[sg.callee[n]], step(env, lambda d: sg.call_flow(n, d)), stack + (n,)))
            todo.append((sg.ret_site[n], step(env, lambda d: sg.c2r_flow(n, d)), stack))
        elif n[1] == EXIT:
            if stack:
                c = stack[-1]
                todo.append((sg.ret_site[c], step(env, lambda d: sg.ret_flow(c, d)), stack[:-1]))
        else:
            for m in sg.succ[n]:
                todo.append((m, step(env, lambda d: sg.normal_flow(n, m, d)), stack))
    for n in M:
        M[n].pop(ZERO, None)
    return M


def mfp_supergraph(sg, seeds=None):
    """Context-insensitive constant propagation on the supergraph: every
    exit flows back to every caller."""
    IN = {n: {} for n in sg.nodes}
    work, queued = [], set()

    def add(m, env):
        changed = False
        for d, v in env.items():
            new = meet_val(IN[m].get(d, TOP), v)
            if new != IN[m].get(d, TOP):
                IN[m][d] = new
                changed = True
        if changed and m not in queued:
            queued.add(m)
            work.append(m)

    add(sg.start[sg.main], start_env(sg, seeds))
    while work:
        n = work.pop()
        queued.discard(n)
        env = IN[n]
        if n in sg.callee:
            q = sg.callee[n]
            add(sg.start[q], step(env, lambda d: sg.call_flow(n, d)))
            add(sg.ret_site[n], step(env, lambda d: sg.c2r_flow(n, d)))
            add(sg.ret_site[n], step(IN[sg.exit[q]], lambda d: sg.ret_flow(n, d)))
        elif n[1] == EXIT:
            for c in sg.callers[n[0]]:
                if ZERO in IN[c]:
                    add(sg.ret_site[c], step(env, lambda d: sg.ret_flow(c, d)))
        else:
            for m in sg.succ[n]:
                add(m, step(env, lambda d: sg.normal_flow(n, m, d)))
    for n in IN:
        IN[n].pop(ZERO, None)
    return IN


def run_recorded(module, main, args, fuel=3000):
    """Run the module and record the variables before each node. Returns
    the outcome, in the form of toyir.run, and a list of (node, env)."""
    seen = []
    stack = []
    p = main
    prog = module[p]
    env = dict(zip(prog.params, args))
    label, pc, dest = prog.entry, 0, None

    def tick():
        nonlocal fuel
        if fuel <= 0:
            raise toyir._Fuel()
        fuel -= 1

    def val(a):
        return a if isinstance(a, int) else env[a]

    try:
        while True:
            blk = module[p].blocks[label]
            called = False
            while pc < len(blk.instrs):
                ins = blk.instrs[pc]
                seen.append(((p, label, pc), dict(env)))
                tick()
                k = ins[0]
                if k == "const":
                    env[ins[1]] = ins[2]
                elif k == "copy":
                    env[ins[1]] = val(ins[2])
                elif k == "op":
                    env[ins[1]] = toyir._binop(ins[2], val(ins[3]), val(ins[4]))
                else:
                    q = module[ins[2]]
                    stack.append((p, label, pc + 1, ins[1], env))
                    env = dict(zip(q.params, [val(a) for a in ins[3]]))
                    p, label, pc = ins[2], q.entry, 0
                    called = True
                    break
                pc += 1
            if called:
                continue
            seen.append(((p, label, len(blk.instrs)), dict(env)))
            tick()
            t = blk.term
            if t[0] == "jump":
                label, pc = t[1], 0
                continue
            if t[0] == "br":
                label, pc = (t[2] if val(t[1]) != 0 else t[3]), 0
                continue
            v = val(t[1])
            seen.append(((p, EXIT, 0), dict(env, **{RET: v})))
            if not stack:
                return ("ret", v), seen
            p, label, pc, dest, env = stack.pop()
            env[dest] = v
    except toyir._Trap:
        return ("trap",), seen
    except toyir._Fuel:
        return ("fuel",), seen


# ---------------------------------------------------------- random modules


def random_module(rng, recursive=False):
    """Three procedures f0, f1 and f2 from random_program, with two to four
    calls x = call fj(a, b) added. Without recursion, fi only calls fj with
    j > i. A call in B0 goes after the constants that start B0."""
    names = ["f0", "f1", "f2"]
    module = {f: random_program(rng, 4, rng.randint(2, 4), True) for f in names}
    xs = ["x%d" % i for i in range(4)]
    for _ in range(rng.randint(2, 4)):
        i = rng.randrange(0, 3 if recursive else 2)
        j = rng.randrange(0, 3) if recursive else rng.randrange(i + 1, 3)
        prog = module[names[i]]
        label = rng.choice(list(prog.blocks))
        instrs = prog.blocks[label].instrs
        lo = 2 if label == prog.entry else 0
        pos = rng.randint(lo, len(instrs))
        args = [rng.choice(xs) if rng.random() < 0.6 else rng.randint(0, 5) for _ in range(2)]
        instrs.insert(pos, ("call", rng.choice(xs), names[j], args))
    return module


def bound_checks(sg, stats):
    D1 = max(len(f) for f in sg.facts.values()) + 1
    N = len(sg.nodes)
    assert stats["path_edges"] <= N * D1 * D1
    assert stats["jump_changes"] <= 3 * stats["path_edges"]
    assert stats["pops"] <= stats["jump_changes"]
    assert stats["summary_changes"] <= 3 * len(sg.callee) * D1 * D1
    assert stats["value_changes"] <= 2 * N * D1
    assert stats["meets"] <= 3 * sg.num_edges() * 3 * D1 ** 3


def check_sound(module, V, rng, fuel=3000):
    for _ in range(3):
        args = [rng.randint(-6, 9), rng.randint(-6, 9)]
        out, seen = run_recorded(module, "f0", args, fuel)
        assert out == toyir.run(module["f0"], args, fuel=fuel, funcs=module)
        for n, env in seen:
            for x, v in env.items():
                assert x in V[n], (n, x)
                assert V[n][x] == BOT or V[n][x] == v, (n, x, V[n][x], v)


# ------------------------------------------------------------------- tests


def test_add_example() -> None:
    module = add_module()
    sg = Supergraph(module, "main")
    V, stats = ide(sg)
    end = ("main", EXIT, 0)
    assert V[end] == {"n": BOT, "x": 2, "y": 7, "z": BOT, "v": 4, "w": 13, RET: 13}
    assert V[("add", "B0", 0)] == {"a": BOT, "b": BOT}
    # The summary of add maps a to RET by l -> 3l + 1. The first argument
    # is 2 at the first call and 4 at the third, so y = 7 and w = 13.
    M = mvp_by_paths(sg)
    assert M == V
    MFP = mfp_supergraph(sg)
    assert MFP[end]["y"] == BOT and MFP[end]["w"] == BOT
    bound_checks(sg, stats)
    assert run_recorded(module, "main", [5])[0] == ("ret", 13)


def test_seeded_main() -> None:
    module = add_module()
    sg = Supergraph(module, "main")
    V, _ = ide(sg, {"n": 5})
    end = ("main", EXIT, 0)
    assert V[end]["z"] == 16 and V[end]["w"] == 13
    assert V[("add", "B0", 0)]["a"] == BOT
    assert mvp_by_paths(sg, {"n": 5}) == V


def test_point_function() -> None:
    # Two branches give u = 3a + 1 and u = a + 5. The meet of the two
    # lines is the point function 2 -> 7, so a call with a = 2 gives 7 and
    # any other argument gives BOT.
    f = parse("# params: a, b\nB0:\n  br b L R\nL:\n  t = a * 3\n  u = t + 1\n  jump J\nR:\n  u = a + 5\n  jump J\nJ:\n  ret u\n")
    main = parse("# params: n\nB0:\n  x = 2\n  y = call f(x, n)\n  z = call f(3, n)\n  ret y\n")
    module = {"main": main, "f": f}
    sg = Supergraph(module, "main")
    V, _ = ide(sg)
    end = ("main", EXIT, 0)
    assert V[end]["y"] == 7 and V[end]["z"] == BOT
    assert mvp_by_paths(sg) == V


def test_recursion_keeps_linear_relation() -> None:
    # The analysis does not follow the branch, so it sees every depth d. At
    # depth d the base case returns k - d, and each of the d returns adds
    # 1, so down(k) returns k on every valid path. The summary of down is
    # the identity, and b = 3.
    down = parse("# params: k\nB0:\n  c = k < 1\n  br c done more\nmore:\n  j = k - 1\n  r = call down(j)\n  s = r + 1\n  ret s\ndone:\n  ret k\n")
    main = parse("# params: n\nB0:\n  a = 3\n  b = call down(a)\n  ret b\n")
    module = {"main": main, "down": down}
    V = ide_framework(module, "main")
    assert V[("main", EXIT, 0)]["b"] == 3
    MFP = mfp_supergraph(Supergraph(module, "main"))
    assert MFP[("main", EXIT, 0)]["b"] == BOT


def test_random_acyclic_modules() -> None:
    rng = random.Random(6101)
    srng = random.Random(6201)
    compared = strict = 0
    for _ in range(300):
        module = random_module(rng)
        sg = Supergraph(module, "f0")
        V, stats = ide(sg)
        bound_checks(sg, stats)
        M = mvp_by_paths(sg)
        if M is not None:
            compared += 1
            assert V == M
        MFP = mfp_supergraph(sg)
        for n in sg.nodes:
            assert set(MFP[n]) == set(V[n])
            assert all(leq(MFP[n][d], V[n][d]) for d in V[n])
        if any(MFP[n] != V[n] for n in sg.nodes):
            strict += 1
        check_sound(module, V, srng)
    assert compared >= 290
    assert strict >= 12


def test_random_recursive_modules() -> None:
    rng = random.Random(6102)
    srng = random.Random(6202)
    compared = 0
    for _ in range(100):
        module = random_module(rng, recursive=True)
        sg = Supergraph(module, "f0")
        V, stats = ide(sg)
        bound_checks(sg, stats)
        MFP = mfp_supergraph(sg)
        for n in sg.nodes:
            assert set(MFP[n]) == set(V[n])
            assert all(leq(MFP[n][d], V[n][d]) for d in V[n])
        # Paths with at most three open calls are some of the valid paths,
        # so their meet is above or equal to the result.
        M = mvp_by_paths(sg, cap=5000, max_depth=3)
        if M is not None:
            compared += 1
            for n in sg.nodes:
                assert set(M[n]) <= set(V[n])
                assert all(leq(V[n][d], M[n][d]) for d in M[n])
        check_sound(module, V, srng, fuel=400)
    assert compared >= 85


def test_bad_input() -> None:
    bad = {"main": parse("# params: a\nB0:\n  x = call nope(a)\n  ret x\n")}
    try:
        Supergraph(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("unknown callee accepted")
