# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/system-dependence-graph-slicing/. The authors are listed in prov/6EV9PV.jsonl.

import random

import toyir
from system_dependence_graph_slicing import (
    DEF,
    ENTRY,
    REF,
    block_control_deps,
    build_sdg,
    call_sites,
    ipdom,
    reachability_slice,
    reaching_definitions,
    sdg_slice,
    start_nodes,
    statements,
    statements_of,
    summary_edges,
)

MAIN = """
# params: n
B1:
  s = 0
  i = 0
  jump B2
B2:
  t = i < n
  br t B3 B4
B3:
  s = call add(s, i)
  i = call add(i, 1)
  jump B2
B4:
  ret i
"""

ADD = """
# params: a, b
B1:
  r = a + b
  ret r
"""


def page_system():
    return {"main": toyir.parse(MAIN), "add": toyir.parse(ADD)}


def test_page_example():
    system = page_system()
    for n in range(0, 6):
        assert toyir.run(system["main"], [n], funcs=system) == ("ret", n)
    crit = ("main", "B4", 0, {"i"})
    S = statements_of(sdg_slice(system, crit))
    assert S == {
        ("main", "B1", 1), ("main", "B2", 0), ("main", "B2", 1), ("main", "B3", 1),
        ("add", "B1", 0), ("add", "B1", 1),
    }
    # Without calling context, the slice also takes the statements of s.
    R = statements_of(reachability_slice(system, crit))
    assert R == S | {("main", "B1", 0), ("main", "B3", 0)}
    # The summary edges of the page: each argument reaches the result.
    sdg = build_sdg(system)
    summ = {(m, n) for n, ps in sdg.items() for kind, m in ps if kind == "summary"}
    assert summ == {
        (("ain", "main", "B3", j, k), ("aout", "main", "B3", j)) for j in (0, 1) for k in (0, 1)
    }


# ------------------------------------------------------------ random systems


def random_system(rng, nprocs):
    """F0 is main. Each Fj with j >= 1 gets one or two call sites in
    procedures Fi with i < j, so there is no recursion and every procedure
    is called from main."""
    names = ["F%d" % j for j in range(nprocs)]
    system = {}
    for f in names:
        system[f] = toyir.random_program(rng, rng.randint(2, 4), rng.randint(1, 4), rng.random() < 0.5)
    for j in range(1, nprocs):
        for _ in range(rng.randint(1, 2)):
            prog = system[names[rng.randrange(j)]]
            xs = [x for x in sorted({ins[1] for b in prog.blocks.values() for ins in b.instrs}) if x.startswith("x")]
            xs = sorted(set(xs) | set(prog.params))
            lab = rng.choice(list(prog.blocks))
            b = prog.blocks[lab]
            # In the entry block, the call goes after the definitions of the locals.
            lo = len(b.instrs) if lab == prog.entry else 0
            pos = rng.randint(lo, len(b.instrs))
            args = [rng.choice(xs) if rng.random() < 0.8 else rng.randint(-2, 5) for _ in range(2)]
            b.instrs.insert(pos, ("call", rng.choice(xs), names[j], args))
    main = system.pop("F0")
    return dict([("main", main)] + list(system.items()))


def random_criterion(rng, system):
    P = rng.choice(list(system))
    prog = system[P]
    lab, i = rng.choice(statements(prog))
    names = sorted({v for n in statements(prog) for v in DEF(prog, n)} | set(prog.params))
    return (P, lab, i, set(rng.sample(names, rng.randint(1, min(2, len(names))))))


def test_random_systems_run():
    rng = random.Random(11)
    ok = 0
    for _ in range(100):
        system = random_system(rng, rng.randint(2, 4))
        out = toyir.run(system["main"], [rng.randint(-3, 6), rng.randint(-3, 6)], funcs=system)
        assert out[0] in ("ret", "trap")
        ok += out[0] == "ret"
    assert ok > 50


# --------------------------- reference 1: the graph with one copy per context


def contexts_of(system):
    """For each procedure, its calling contexts: strings of call sites from
    main."""
    sites = call_sites(system)
    out = {f: [] for f in system}

    def walk(f, ctx):
        out[f].append(ctx)
        for g in system:
            for site in sites[g]:
                if site[0] == f:
                    walk(g, ctx + (site,))

    walk("main", ())
    return out


def context_step(sdg, n, ctx):
    """Parents of the copy of n in context ctx, in the expanded graph."""
    for kind, m in sdg[n]:
        if kind == "summary":
            continue
        if kind in ("call", "pin"):
            # Up from the callee, only to the call site on top of ctx.
            if ctx and m[1:4] == ctx[-1]:
                yield m, ctx[:-1]
        elif kind == "pout":
            # Down into the callee at the call site of n.
            yield m, ctx + (n[1:4],)
        else:
            yield m, ctx


def expanded_slice(system, crit):
    """Backward reachability from every copy of the criterion in the graph
    that has one copy of each procedure per calling context. Its paths are
    the realizable paths of the SDG."""
    sdg = build_sdg(system, summaries=False)
    st = start_nodes(system, crit, sdg)
    seen = {(m, ctx) for ctx in contexts_of(system)[crit[0]] for m in st}
    stack = list(seen)
    while stack:
        n, ctx = stack.pop()
        for nxt in context_step(sdg, n, ctx):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return {n for (n, _) in seen}


def test_slice_equals_realizable_paths():
    rng = random.Random(7)
    for trial in range(150):
        system = random_system(rng, rng.randint(2, 4))
        sdg = build_sdg(system)
        for _ in range(3):
            crit = random_criterion(rng, system)
            assert sdg_slice(system, crit, sdg) == expanded_slice(system, crit)


def test_context_matters():
    """On many random systems the plain reachability slice is larger."""
    rng = random.Random(8)
    larger = 0
    for trial in range(150):
        system = random_system(rng, rng.randint(2, 4))
        sdg = build_sdg(system)
        crit = random_criterion(rng, system)
        S = sdg_slice(system, crit, sdg)
        R = reachability_slice(system, crit, sdg)
        assert S <= R
        larger += statements_of(S) < statements_of(R)
    assert larger > 0


# ----------------------------------------- reference 2: inline the program text


def inline(system):
    """Inline every call. Returns (prog, origin, chain, points, prefix):
    origin maps each statement of prog to the statement (P, lab, i) it comes
    from, chain maps it to the call sites of its context, points maps
    (statement, context) to its first statement in prog, and prefix maps a
    context to the prefix of the names of that copy."""
    blocks = {}
    origin, chain, points, prefix = {}, {}, {}, {}
    count = [0]

    def emit(P, pre, ctx, ret_to):
        prog = system[P]
        prefix[ctx] = pre

        def ren(a):
            return a if isinstance(a, int) else pre + a

        def mov(x, a):
            return ("const", x, a) if isinstance(a, int) else ("copy", x, a)

        def close(label, ins_list, orig_list, term, term_orig):
            blocks[label] = toyir.Block(ins_list, term)
            for k, o in enumerate(orig_list + [term_orig]):
                origin[(label, k)] = o
                chain[(label, k)] = ctx
                points.setdefault((o, ctx), (label, k))

        for L, b in prog.blocks.items():
            cur = pre + L
            instrs, orig = [], []
            for i, ins in enumerate(b.instrs):
                s = (P, L, i)
                if ins[0] == "call":
                    _, x, f, args = ins
                    count[0] += 1
                    q = "k%d." % count[0]
                    callee = system[f]
                    for pname, a in zip(callee.params, args):
                        instrs.append(mov(q + pname, ren(a)))
                        orig.append(s)
                    # Each activation has fresh locals. A loop around the
                    # call must not carry them from one activation to the
                    # next, so the copy kills them first. These kills have
                    # no origin: they are not statements of the system.
                    locs = {ins2[1] for b2 in callee.blocks.values() for ins2 in b2.instrs}
                    for v in sorted(locs - set(callee.params)):
                        instrs.append(("const", q + v, 0))
                        orig.append(None)
                    post = "%s+%d" % (cur, i)
                    close(cur, instrs, orig, ("jump", q + callee.entry), s)
                    emit(f, q, ctx + (s,), (post, q + "$ret"))
                    cur, instrs, orig = post, [("copy", ren(x), q + "$ret")], [s]
                else:
                    if ins[0] == "const":
                        instrs.append(("const", ren(ins[1]), ins[2]))
                    elif ins[0] == "copy":
                        instrs.append(("copy", ren(ins[1]), ren(ins[2])))
                    else:
                        instrs.append(("op", ren(ins[1]), ins[2], ren(ins[3]), ren(ins[4])))
                    orig.append(s)
            t = b.term
            s = (P, L, len(b.instrs))
            if t[0] == "jump":
                close(cur, instrs, orig, ("jump", pre + t[1]), s)
            elif t[0] == "br":
                close(cur, instrs, orig, ("br", ren(t[1]), pre + t[2], pre + t[3]), s)
            elif ret_to is None:
                close(cur, instrs, orig, ("ret", ren(t[1])), s)
            else:
                instrs.append(mov(ret_to[1], ren(t[1])))
                orig.append(s)
                close(cur, instrs, orig, ("jump", ret_to[0]), s)

    emit("main", "", (), None)
    main = system["main"]
    ordered = {main.entry: blocks.pop(main.entry)}
    ordered.update(blocks)
    return toyir.Program(list(main.params), ordered), origin, chain, points, prefix


def intra_slice(prog, starts, skip):
    """Backward reachability in the PDG of one procedure, from a set of
    points (lab, i, V). The statements of skip kill definitions but are not
    nodes of the graph."""
    ip = ipdom(prog)
    cd = block_control_deps(prog, ip)
    rd = reaching_definitions(prog)
    out = {ENTRY} | skip

    def term(a):
        return (a, len(prog.blocks[a].instrs))

    K = set()
    for (lab, i, V) in starts:
        K |= {d for (d, x) in rd[(lab, i)] if x in V and d not in out}
        K |= {term(a) for a in cd[lab] if a != ENTRY}
    stack = list(K)
    while stack:
        n = stack.pop()
        ps = {term(a) for a in cd[n[0]] if a != ENTRY}
        ps |= {d for (d, x) in rd[n] if x in REF(prog, n) and d not in out}
        for m in ps:
            if m not in K:
                K.add(m)
                stack.append(m)
    return K


def test_slice_equals_slice_of_inlined_program():
    rng = random.Random(23)
    for trial in range(120):
        system = random_system(rng, rng.randint(2, 4))
        prog, origin, chain, points, prefix = inline(system)
        args = [rng.randint(-3, 6), rng.randint(-3, 6)]
        assert toyir.run(prog, args) == toyir.run(system["main"], args, funcs=system)
        sdg = build_sdg(system)
        for _ in range(3):
            crit = random_criterion(rng, system)
            P, lab, i, V = crit
            starts, ctxs = [], []
            for (o, ctx), (L, k) in points.items():
                if o == (P, lab, i):
                    starts.append((L, k, {prefix[ctx] + v for v in V}))
                    ctxs.append(ctx)
            K = intra_slice(prog, starts, {n for n, o in origin.items() if o is None})
            # A statement of a callee runs only if its call runs, so the
            # call sites of its context count as well.
            want = {origin[n] for n in K}
            for n in K:
                want |= set(chain[n])
            for ctx in ctxs:
                want |= set(ctx)
            assert statements_of(sdg_slice(system, crit, sdg)) == want


# ------------------------------------------------- summary edges, directly


def same_level_path(sdg, src, dst):
    """Is there a path from src to dst in which every call or parameter-in
    edge is matched by the parameter-out edge of the same call site?"""
    start = (dst, ())
    seen = {start}
    stack = [start]
    while stack:
        n, ctx = stack.pop()
        if n == src and ctx == ():
            return True
        for nxt in context_step(sdg, n, ctx):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return False


def test_summary_edges_match_same_level_paths():
    rng = random.Random(31)
    for trial in range(150):
        system = random_system(rng, rng.randint(2, 4))
        sdg = build_sdg(system, summaries=False)
        want = set()
        for f, sites in call_sites(system).items():
            for k in range(len(system[f].params)):
                if same_level_path(sdg, ("fin", f, k), ("fout", f)):
                    want |= {(("ain",) + s + (k,), ("aout",) + s) for s in sites}
        assert summary_edges(system, sdg) == want
