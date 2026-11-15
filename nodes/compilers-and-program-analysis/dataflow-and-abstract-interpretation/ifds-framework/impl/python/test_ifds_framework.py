# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ifds-framework/. The authors are listed in prov/K1QASX.jsonl.

import random

import toyir
from toyir import parse, random_program
from ifds_framework import EXIT, RET, ZERO, Supergraph, ifds, ifds_framework

# The example of the page: id is called twice, once with the secret and
# once with a constant. Only the first result may depend on the secret.
ID = """
# params: a
B0:
  ret a
"""

MAIN = """
# params: secret
B0:
  x = call id(secret)
  y = call id(0)
  ret y
"""


def id_module():
    return {"main": parse(MAIN), "id": parse(ID)}


# ------------------------------------------------------------ brute force


def apply(fn, facts):
    """Apply a flow function given pointwise to a set of facts. ZERO is
    always in the set, as on every path of the exploded supergraph."""
    out = {ZERO}
    for d in facts:
        out.update(fn(d))
    return frozenset(out)


def mvp_by_paths(sg, seeds, cap=20000, max_depth=None):
    """The meet over all valid paths, by walking every valid path from the
    start of main one by one. A path is a list of nodes; its state is the
    set of facts and the stack of open calls. At a call node the path
    either enters the callee or takes the call-to-return edge. At an exit
    it returns to the call on top of the stack. The result at a node is the
    union of the facts at the node over all paths that reach it. Returns
    None when more than cap steps are needed. With max_depth, calls deeper
    than that are not entered, which gives a subset of the valid paths."""
    M = {n: set() for n in sg.nodes}
    start = (sg.start[sg.main], frozenset(list(seeds) + [ZERO]), ())
    todo = [start]
    steps = 0
    while todo:
        n, facts, stack = todo.pop()
        steps += 1
        if steps > cap:
            return None
        M[n].update(facts)
        if n in sg.callee:
            q = sg.callee[n]
            if max_depth is None or len(stack) < max_depth:
                todo.append((sg.start[q], apply(lambda d: sg.call_flow(n, d), facts), stack + (n,)))
            todo.append((sg.ret_site[n], apply(lambda d: sg.c2r_flow(n, d), facts), stack))
        elif n[1] == EXIT:
            if stack:
                c = stack[-1]
                todo.append((sg.ret_site[c], apply(lambda d: sg.ret_flow(c, d), facts), stack[:-1]))
        else:
            for m in sg.succ[n]:
                todo.append((m, apply(lambda d: sg.normal_flow(n, m, d), facts), stack))
    for n in M:
        M[n].discard(ZERO)
    return M


def mfp_supergraph(sg, seeds):
    """The context-insensitive solution: the supergraph is one big graph,
    and every exit flows back to every caller."""
    IN = {n: set() for n in sg.nodes}
    IN[sg.start[sg.main]] = set(seeds)
    work = list(sg.nodes)
    queued = set(work)

    def add(m, facts):
        if not facts <= IN[m]:
            IN[m] |= facts
            if m not in queued:
                queued.add(m)
                work.append(m)

    while work:
        n = work.pop()
        queued.discard(n)
        X = IN[n]
        if n in sg.callee:
            q = sg.callee[n]
            add(sg.start[q], set(apply(lambda d: sg.call_flow(n, d), X)) - {ZERO})
            add(sg.ret_site[n], set(apply(lambda d: sg.c2r_flow(n, d), X)) - {ZERO})
            out = set(apply(lambda d: sg.ret_flow(n, d), IN[sg.exit[q]])) - {ZERO}
            add(sg.ret_site[n], out)
        elif n[1] == EXIT:
            for c in sg.callers[n[0]]:
                out = set(apply(lambda d: sg.ret_flow(c, d), X)) - {ZERO}
                add(sg.ret_site[c], out)
        else:
            for m in sg.succ[n]:
                add(m, set(apply(lambda d: sg.normal_flow(n, m, d), X)) - {ZERO})
    return IN


# ------------------------------------------------------- tainted execution


class Frame:
    def __init__(self, p, env, taint):
        self.p = p
        self.env = env
        self.taint = taint
        self.label = None
        self.pc = 0
        self.dest = None


def run_tainted(module, main, args, tainted, fuel=3000):
    """Run the module and track which values depend on the tainted
    arguments, following data flow only. Returns the outcome, in the form
    of toyir.run, and the list of (node, tainted facts) seen before each
    node runs. The fuel is counted as in toyir.run."""
    seen = []
    prog = module[main]
    fr = Frame(main, dict(zip(prog.params, args)), {x for x, t in zip(prog.params, tainted) if t})
    fr.label = prog.entry
    stack = []

    def val(fr, a):
        if isinstance(a, int):
            return a, False
        return fr.env[a], a in fr.taint

    def tick():
        nonlocal fuel
        if fuel <= 0:
            raise toyir._Fuel()
        fuel -= 1

    try:
        while True:
            blk = module[fr.p].blocks[fr.label]
            called = False
            while fr.pc < len(blk.instrs):
                ins = blk.instrs[fr.pc]
                seen.append(((fr.p, fr.label, fr.pc), frozenset(fr.taint)))
                tick()
                k, x = ins[0], ins[1]
                if k == "const":
                    v, t = ins[2], False
                elif k == "copy":
                    v, t = val(fr, ins[2])
                elif k == "op":
                    a, ta = val(fr, ins[3])
                    b, tb = val(fr, ins[4])
                    v, t = toyir._binop(ins[2], a, b), ta or tb
                else:
                    vals = [val(fr, a) for a in ins[3]]
                    q = module[ins[2]]
                    fr.dest = x
                    fr.pc += 1
                    stack.append(fr)
                    env = {pn: v for pn, (v, _t) in zip(q.params, vals)}
                    taint = {pn for pn, (_v, t) in zip(q.params, vals) if t}
                    fr = Frame(ins[2], env, taint)
                    fr.label = q.entry
                    called = True
                    break
                fr.env[x] = v
                if t:
                    fr.taint.add(x)
                else:
                    fr.taint.discard(x)
                fr.pc += 1
            if called:
                continue
            seen.append(((fr.p, fr.label, len(blk.instrs)), frozenset(fr.taint)))
            tick()
            term = blk.term
            if term[0] == "jump":
                fr.label, fr.pc = term[1], 0
                continue
            if term[0] == "br":
                v, _t = val(fr, term[1])
                fr.label, fr.pc = (term[2] if v != 0 else term[3]), 0
                continue
            v, t = val(fr, term[1])
            seen.append(((fr.p, EXIT, 0), frozenset(fr.taint | ({RET} if t else set()))))
            if not stack:
                return ("ret", v), seen
            fr = stack.pop()
            fr.env[fr.dest] = v
            if t:
                fr.taint.add(fr.dest)
            else:
                fr.taint.discard(fr.dest)
    except toyir._Trap:
        return ("trap",), seen
    except toyir._Fuel:
        return ("fuel",), seen


# ---------------------------------------------------------- random modules


def random_module(rng, recursive=False):
    """Three procedures f0, f1 and f2 from random_program, with two to four
    calls x = call fj(a, b) added. Without recursion, fi only calls fj with
    j > i. A call in B0 goes after the constants that start B0, so every
    name is defined before it is read."""
    names = ["f0", "f1", "f2"]
    module = {}
    for f in names:
        module[f] = random_program(rng, 4, rng.randint(2, 4), True)
    xs = ["x%d" % i for i in range(4)]
    for _ in range(rng.randint(2, 4)):
        i = rng.randrange(0, 3 if recursive else 2)
        j = rng.randrange(0, 3) if recursive else rng.randrange(i + 1, 3)
        prog = module[names[i]]
        label = rng.choice(list(prog.blocks))
        instrs = prog.blocks[label].instrs
        lo = 2 if label == prog.entry else 0
        pos = rng.randint(lo, len(instrs))
        args = [rng.choice(xs) if rng.random() < 0.85 else rng.randint(0, 5) for _ in range(2)]
        instrs.insert(pos, ("call", rng.choice(xs), names[j], args))
    return module


def bound_checks(sg, stats):
    D1 = max(len(f) for f in sg.facts.values()) + 1
    N = len(sg.nodes)
    E = sg.num_edges()
    assert stats["path_edges"] <= N * D1 * D1
    assert stats["pops"] == stats["path_edges"]
    assert stats["summary_edges"] <= len(sg.callee) * D1 * D1
    assert stats["flow"] <= 3 * E * D1 ** 3


def arg_lists(rng):
    out = [[0, 0], [1, 2], [-3, 7]]
    for _ in range(3):
        out.append([rng.randint(-6, 9), rng.randint(-6, 9)])
    return out


# ------------------------------------------------------------------- tests


def test_id_example() -> None:
    module = id_module()
    sg = Supergraph(module, "main")
    X, stats = ifds(sg)
    assert X[("id", "B0", 0)] == {"a"}
    assert X[("id", EXIT, 0)] == {"a", RET}
    assert X[("main", "B0", 1)] == {"secret", "x"}
    assert X[("main", "B0", 2)] == {"secret", "x"}
    assert X[("main", EXIT, 0)] == {"secret", "x"}
    # The context-insensitive solution leaks the secret into y.
    MFP = mfp_supergraph(sg, ["secret"])
    assert MFP[("main", "B0", 2)] == {"secret", "x", "y"}
    assert MFP[("main", EXIT, 0)] == {"secret", "x", "y", RET}
    assert mvp_by_paths(sg, ["secret"]) == X
    # Summary edges: secret to x and ZERO to ZERO at s1, and only ZERO to
    # ZERO at s2, since the argument of s2 is a constant.
    assert stats["summary_edges"] == 3
    bound_checks(sg, stats)
    assert run_tainted(module, "main", [5], [True])[0] == ("ret", 0)


def test_wrapper_chain() -> None:
    # The secret goes in through two levels of calls and comes back only on
    # the path where it went in.
    inner = parse("# params: a, b\nB0:\n  t = a + 1\n  ret t\n")
    outer = parse("# params: u, v\nB0:\n  r = call inner(u, v)\n  s = call inner(v, u)\n  ret r\n")
    main = parse("# params: p, q\nB0:\n  m = call outer(p, q)\n  n = call outer(q, p)\n  ret n\n")
    module = {"main": main, "outer": outer, "inner": inner}
    X = ifds_framework(module, "main", ["p"])
    assert X[("main", "B0", 1)] == {"p", "m"}
    assert X[("main", EXIT, 0)] == {"p", "m"}
    assert X[("outer", "B0", 1)] == {"u", "v", "r"}
    assert X[("outer", "B0", 2)] == {"u", "v", "r", "s"}
    sg = Supergraph(module, "main")
    assert mvp_by_paths(sg, ["p"]) == X
    MFP = mfp_supergraph(sg, ["p"])
    assert "n" in MFP[("main", EXIT, 0)]


def test_random_acyclic_modules() -> None:
    rng = random.Random(4101)
    compared = strict = runs = 0
    for _ in range(400):
        module = random_module(rng)
        sg = Supergraph(module, "f0")
        X, stats = ifds(sg)
        bound_checks(sg, stats)
        M = mvp_by_paths(sg, ["x0"])
        if M is not None:
            compared += 1
            assert X == M
        MFP = mfp_supergraph(sg, ["x0"])
        assert all(X[n] <= MFP[n] for n in sg.nodes)
        if any(X[n] != MFP[n] for n in sg.nodes):
            strict += 1
        for args in arg_lists(rng):
            out, seen = run_tainted(module, "f0", args, [True, False])
            assert out == toyir.run(module["f0"], args, fuel=3000, funcs=module)
            runs += 1
            for n, t in seen:
                assert t <= X[n], (n, t, X[n])
    assert compared >= 380
    assert strict >= 15
    assert runs == 2400


def test_random_recursive_modules() -> None:
    rng = random.Random(4102)
    for _ in range(150):
        module = random_module(rng, recursive=True)
        sg = Supergraph(module, "f0")
        X, stats = ifds(sg)
        bound_checks(sg, stats)
        MFP = mfp_supergraph(sg, ["x0"])
        assert all(X[n] <= MFP[n] for n in sg.nodes)
        # Valid paths with at most three open calls are a subset of all
        # valid paths, so their union must be inside the result.
        M = mvp_by_paths(sg, ["x0"], cap=20000, max_depth=3)
        if M is not None:
            assert all(M[n] <= X[n] for n in sg.nodes)
        for args in arg_lists(rng):
            out, seen = run_tainted(module, "f0", args, [True, False], fuel=400)
            assert out == toyir.run(module["f0"], args, fuel=400, funcs=module)
            for n, t in seen:
                assert t <= X[n]


def test_seeds_and_zero() -> None:
    # With no seed, nothing is tainted, but ZERO still reaches every node
    # that some valid path reaches.
    module = id_module()
    sg = Supergraph(module, "main")
    X, stats = ifds(sg, seeds=[])
    assert all(not v for v in X.values())
    assert stats["path_edges"] == len(sg.nodes)
    # Both parameters as seeds: the union of the two single-seed results.
    rng = random.Random(4103)
    for _ in range(60):
        module = random_module(rng)
        sg = Supergraph(module, "f0")
        A, _ = ifds(sg, ["x0"])
        B, _ = ifds(sg, ["x1"])
        AB, _ = ifds(sg, ["x0", "x1"])
        assert all(AB[n] == A[n] | B[n] for n in sg.nodes)


def test_bad_input() -> None:
    bad = {"main": parse("# params: a\nB0:\n  x = call nope(a)\n  ret x\n")}
    try:
        Supergraph(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("unknown callee accepted")
    bad = {"main": parse("# params: a\nB0:\n  RET = a\n  ret a\n")}
    try:
        Supergraph(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("reserved name accepted")
