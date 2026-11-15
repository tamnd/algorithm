# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pdg-slicing/. The authors are listed in prov/8QKCJ8.jsonl.

import random

import toyir
from pdg_slicing import (
    DEF,
    ENTRY,
    REF,
    EXIT,
    build_pdg,
    executable_slice,
    ipdom,
    observe,
    pdg_slice,
    slice_point,
    statements,
    stmt_succs,
    terminator,
)

# The sum and product program of the page.
PAGE = """
B1:
  i = 1
  s = 0
  p = 1
  jump B2
B2:
  t = i <= n
  br t B3 B6
B3:
  p = p * i
  u = i % 2
  br u B4 B5
B4:
  s = s + i
  jump B5
B5:
  i = i + 1
  jump B2
B6:
  ret s
"""

# A loop with a "continue": B4 is the jump back to the loop test.
CONTINUE = """
B1:
  i = 0
  c = 0
  jump B2
B2:
  t = i < n
  br t B3 B6
B3:
  i = i + 1
  r = i % 3
  br r B5 B4
B4:
  jump B2
B5:
  c = c + 1
  jump B2
B6:
  ret c
"""


def test_page_example():
    prog = toyir.parse(PAGE)
    pdg = build_pdg(prog)
    assert pdg["control"][("B3", 0)] == {("B2", 1)}
    assert pdg["control"][("B2", 0)] == {ENTRY, ("B2", 1)}
    assert pdg["control"][("B4", 0)] == {("B3", 2)}
    assert pdg["data"][("B3", 0)] == {(("B1", 0), "i"), (("B5", 0), "i"), (("B1", 2), "p"), (("B3", 0), "p")}
    assert pdg["data"][("B2", 0)] == {(("B1", 0), "i"), (("B5", 0), "i"), (ENTRY, "n")}
    S = pdg_slice(prog, ("B6", 0, {"p"}), pdg)
    assert S == {("B1", 0), ("B1", 2), ("B2", 0), ("B2", 1), ("B3", 0), ("B5", 0)}
    S2 = pdg_slice(prog, ("B6", 0, {"s"}), pdg)
    assert len(S2) == 8 and ("B1", 2) not in S2 and ("B3", 0) not in S2
    # The slice of a statement used as the criterion node itself.
    S3 = pdg_slice(prog, ("B5", 0, {"i"}), pdg)
    assert S3 == {("B1", 0), ("B2", 0), ("B2", 1), ("B5", 0)}
    sl = executable_slice(prog, ("B6", 0, {"p"}), S)
    point = slice_point(prog, ("B6", 0, {"p"}), S)
    for n in range(-2, 9):
        assert observe(prog, [n], ("B6", 0), ["p"])[1] == observe(sl, [n], point, ["p"])[1]


def _postdominates(prog, y, x):
    if x == y:
        return True
    seen = {x}
    stack = [x]
    while stack:
        a = stack.pop()
        s = toyir.succs(prog, a)
        if not s:
            return False
        for b in s:
            if b != y and b not in seen:
                seen.add(b)
                stack.append(b)
    return True


def _control_deps(prog):
    labels = list(prog.blocks)
    return {
        x: {
            y
            for y in labels
            for s in toyir.succs(prog, x)
            if _postdominates(prog, y, s) and not (y != x and _postdominates(prog, y, x))
        }
        for x in labels
    }


def _def_clear_reach(prog, start, x, target):
    seen = set()
    stack = [start]
    while stack:
        n = stack.pop()
        if n == target:
            return True
        if n in seen or x in DEF(prog, n):
            continue
        seen.add(n)
        stack.extend(stmt_succs(prog, n))
    return False


def _brute_parents(prog):
    """Data and control parents straight from the definitions."""
    nodes = statements(prog)
    cd = _control_deps(prog)
    first = (prog.entry, 0)
    out = {}
    for n in nodes:
        ps = set()
        for s in nodes:
            for x in DEF(prog, s) & REF(prog, n):
                if any(_def_clear_reach(prog, m, x, n) for m in stmt_succs(prog, s)):
                    ps.add(s)
        for x in prog.blocks:
            if n[0] in cd[x]:
                ps.add(terminator(prog, x))
        out[n] = ps
        # Parameters: defined at ENTRY, before the first statement.
        params = {x for x in REF(prog, n) & set(prog.params) if _def_clear_reach(prog, first, x, n)}
        out[n, "params"] = params
    return out


def _brute_slice(prog, crit, par):
    lab, i, V = crit
    p = (lab, i)
    nodes = statements(prog)
    cd = _control_deps(prog)
    K = set()
    for s in nodes:
        for x in DEF(prog, s) & V:
            if any(_def_clear_reach(prog, m, x, p) for m in stmt_succs(prog, s)):
                K.add(s)
    for x in prog.blocks:
        if lab in cd[x]:
            K.add(terminator(prog, x))
    stack = list(K)
    while stack:
        n = stack.pop()
        for s in par[n]:
            if s not in K:
                K.add(s)
                stack.append(s)
    return K


def _random_criterion(rng, prog):
    nodes = statements(prog)
    lab, i = rng.choice(nodes)
    names = sorted({v for n in nodes for v in DEF(prog, n)} | set(prog.params))
    return (lab, i, set(rng.sample(names, rng.randint(1, min(2, len(names))))))


def test_pdg_edges_match_definitions():
    rng = random.Random(3)
    for trial in range(150):
        prog = toyir.random_program(rng, rng.randint(2, 4), rng.randint(1, 7), trial % 2 == 0)
        pdg = build_pdg(prog)
        par = _brute_parents(prog)
        cd = _control_deps(prog)
        ip = ipdom(prog)
        always = set()
        y = prog.entry
        while y != EXIT:
            always.add(y)
            y = ip[y]
        for n in statements(prog):
            data = {s for (s, _) in pdg["data"][n] if s != ENTRY}
            ctrl = pdg["control"][n] - {ENTRY}
            assert data | ctrl == par[n]
            assert ctrl == {terminator(prog, x) for x in prog.blocks if n[0] in cd[x]}
            assert {x for (s, x) in pdg["data"][n] if s == ENTRY} == par[n, "params"]
            # ENTRY controls exactly the blocks that every run passes.
            assert (ENTRY in pdg["control"][n]) == (n[0] in always)


def test_slice_equals_bruteforce_reachability():
    rng = random.Random(5)
    for trial in range(250):
        prog = toyir.random_program(rng, rng.randint(2, 4), rng.randint(1, 7), trial % 2 == 0)
        par = _brute_parents(prog)
        for _ in range(3):
            crit = _random_criterion(rng, prog)
            assert pdg_slice(prog, crit) == _brute_slice(prog, crit, par)


def _dynamic_closure(prog, args, crit, ip, fuel=2000):
    """Statements that the criterion depends on in the run on args, by data
    dependence (the last write of each name read) and dynamic control
    dependence (the latest branch instance whose immediate post-dominator
    has not been entered since)."""
    plab, pi, V = crit
    env = dict(zip(prog.params, args))
    stmt_of = []  # instance -> statement
    deps = []  # instance -> parent instances
    last = {}
    open_br = []  # [instance, ipdom block, open]
    roots = set()
    lab = prog.entry
    ctrl = None
    while fuel > 0:
        b = prog.blocks[lab]
        n = len(b.instrs)
        for i in range(n + 1):
            fuel -= 1
            if (lab, i) == (plab, pi):
                roots |= {last[x] for x in V if x in last}
                if ctrl is not None:
                    roots.add(ctrl)
            node = (lab, i)
            par = {last[x] for x in REF(prog, node) if x in last}
            if ctrl is not None:
                par.add(ctrl)
            k = len(stmt_of)
            stmt_of.append(node)
            deps.append(par)
            if i < n:
                ins = b.instrs[i]
                vals = {x: env[x] for x in REF(prog, node)}
                if ins[0] == "const":
                    v = ins[2]
                elif ins[0] == "copy":
                    v = vals[ins[2]]
                else:
                    a = ins[3] if isinstance(ins[3], int) else vals[ins[3]]
                    c = ins[4] if isinstance(ins[4], int) else vals[ins[4]]
                    if ins[2] in ("/", "%") and c == 0 or ins[2] in ("<<", ">>") and not 0 <= c <= 63:
                        fuel = 0
                        break
                    v = toyir._binop(ins[2], a, c)
                env[ins[1]] = v
                last[ins[1]] = k
                continue
            t = b.term
            if t[0] == "ret":
                fuel = 0
                break
            if t[0] == "br":
                c = t[1] if isinstance(t[1], int) else env[t[1]]
                nxt = t[2] if c != 0 else t[3]
                open_br.append([k, ip[lab], True])
            else:
                nxt = t[1]
            for e in open_br:
                if e[1] == nxt:
                    e[2] = False
            live = [e[0] for e in open_br if e[2]]
            ctrl = live[-1] if live else None
            lab = nxt
    seen = set(roots)
    stack = list(roots)
    while stack:
        k = stack.pop()
        for q in deps[k]:
            if q not in seen:
                seen.add(q)
                stack.append(q)
    return {stmt_of[k] for k in seen}


def test_slice_contains_dynamic_dependences():
    rng = random.Random(17)
    smaller = 0
    for trial in range(300):
        prog = toyir.random_program(rng, rng.randint(2, 5), rng.randint(2, 8), trial % 2 == 0)
        ip = ipdom(prog)
        crit = _random_criterion(rng, prog)
        S = pdg_slice(prog, crit)
        for _ in range(4):
            args = [rng.randint(-5, 9), rng.randint(-5, 9)]
            dyn = _dynamic_closure(prog, args, crit, ip)
            assert dyn <= S
            smaller += dyn < S
    assert smaller > 0


def test_projection_keeps_criterion_values():
    rng = random.Random(2024)
    runs = 0
    for trial in range(300):
        prog = toyir.random_program(rng, rng.randint(2, 5), rng.randint(1, 8), trial % 2 == 0)
        crit = _random_criterion(rng, prog)
        S = pdg_slice(prog, crit)
        sl = executable_slice(prog, crit, S)
        point = slice_point(prog, crit, S)
        names = sorted(crit[2])
        for _ in range(8):
            args = [rng.randint(-5, 9), rng.randint(-5, 9)]
            o1, ob1 = observe(prog, args, crit[:2], names)
            assert o1 == toyir.run(prog, args)
            o2, ob2 = observe(sl, args, point, names)
            if o1[0] == "ret":
                assert o2[0] == "ret" and ob2 == ob1
            else:
                assert ob2[: len(ob1)] == ob1
            runs += 1
    assert runs == 2400


def test_jumps_are_not_in_the_slice():
    prog = toyir.parse(CONTINUE)
    crit = ("B6", 0, {"c"})
    S = pdg_slice(prog, crit)
    # Every statement but the jumps and the ret is in the slice.
    assert S == {n for n in statements(prog) if n not in {("B1", 2), ("B4", 0), ("B5", 1), ("B6", 0)}}
    sl = executable_slice(prog, crit, S)
    point = slice_point(prog, crit, S)
    # Deleting the "continue" as in source text: B4 falls into B5.
    broken = toyir.parse(CONTINUE)
    broken.blocks["B4"].term = ("jump", "B5")
    for n in range(0, 10):
        want = observe(prog, [n], ("B6", 0), ["c"])[1]
        assert observe(sl, [n], point, ["c"])[1] == want
        assert want == [(sum(1 for i in range(1, n + 1) if i % 3),)]
    assert observe(broken, [6], ("B6", 0), ["c"])[1] == [(6,)]
    assert observe(prog, [6], ("B6", 0), ["c"])[1] == [(4,)]
