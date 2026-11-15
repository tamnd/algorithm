# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-conditional-constant-propagation/. The authors are listed in prov/WNK50T.jsonl.

import random

import toyir
from toyir import Block, Program, edges, parse, random_program, run, show, succs
from sparse_conditional_constant_propagation import (
    BOT,
    TOP,
    fold,
    is_const,
    meet,
    rewrite,
    sccp,
    sparse_conditional_constant_propagation,
    to_ssa,
)

# The example of the page: the branch that sets i = 2 never runs, but only
# a method that ignores it while it looks at the loop can see that.
LOOP = """
# params: n
entry:
  i = 1
  k = 0
  jump head
head:
  c = i == 1
  br c same other
same:
  jump latch
other:
  i = 2
  jump latch
latch:
  k = k + 1
  t = k < n
  br t head exit
exit:
  ret i
"""

# A branch on a constant: simple constant propagation alone gives y = BOT.
KNOWN = """
# params: a
entry:
  x = 1
  c = x == 1
  br c then else
then:
  y = 2
  jump join
else:
  y = a
  jump join
join:
  z = y + 1
  ret z
"""


# ------------------------------------------------ shared abstract semantics


def evaluate(ins, V, live):
    """The value of one instruction under the values V, where a phi reads
    only the operands of the predecessors p with live(p) true."""
    k = ins[0]

    def val(a):
        return a if isinstance(a, int) else V[a]

    if k == "phi":
        new = TOP
        for p, a in ins[2].items():
            if live(p):
                new = meet(new, val(a))
        return new
    if k == "const":
        return ins[2]
    if k == "copy":
        return val(ins[2])
    if k == "op":
        return fold(ins[2], val(ins[3]), val(ins[4]))
    return BOT


def allowed(prog, b, V):
    """The successors that the terminator of b may take under V."""
    t = prog.blocks[b].term
    if t[0] == "br":
        c = t[1] if isinstance(t[1], int) else V[t[1]]
        if c == TOP:
            return []
        if c != BOT:
            return [t[2] if c != 0 else t[3]]
    return succs(prog, b)


def initial(prog):
    V = {p: BOT for p in prog.params}
    for blk in prog.blocks.values():
        for ins in blk.instrs:
            V[ins[1]] = TOP
    return V


def naive_gfp(prog):
    """Iterate the combined map Phi(V, E) from (all TOP, no edge) until it
    stops: E grows by the edges the terminators allow, V goes down."""
    V = initial(prog)
    E = {(None, prog.entry)}
    while True:
        R = {b for _, b in E}
        newE = {(None, prog.entry)} | {(b, s) for b in R for s in allowed(prog, b, V)}
        newV = dict(V)
        for b, blk in prog.blocks.items():
            for ins in blk.instrs:
                newV[ins[1]] = evaluate(ins, V, lambda p, b=b: (p, b) in E) if b in R else TOP
        if newV == V and newE == E:
            return V, E
        V, E = newV, newE


# --------------------------------------- simple constant propagation and DBE


def cp_values(prog):
    """Simple constant propagation on SSA form: every edge counts."""
    V = initial(prog)
    changed = True
    while changed:
        changed = False
        for blk in prog.blocks.values():
            for ins in blk.instrs:
                new = evaluate(ins, V, lambda p: True)
                if new != V[ins[1]]:
                    V[ins[1]] = new
                    changed = True
    return V


def cp_pass(prog):
    """Replace every name with a constant value by the constant. A branch
    keeps its form, with a literal condition."""
    V = cp_values(prog)

    def opnd(a):
        return V[a] if isinstance(a, str) and is_const(V[a]) else a

    blocks = {}
    for b, blk in prog.blocks.items():
        phis, folded, rest = [], [], []
        for ins in blk.instrs:
            k, x = ins[0], ins[1]
            if is_const(V[x]):
                (folded if k == "phi" else rest).append(("const", x, V[x]))
            elif k == "phi":
                phis.append(("phi", x, {p: opnd(a) for p, a in ins[2].items()}))
            elif k == "copy":
                rest.append(("copy", x, opnd(ins[2])))
            else:
                rest.append(("op", x, ins[2], opnd(ins[3]), opnd(ins[4])))
        t = blk.term
        if t[0] in ("br", "ret"):
            t = (t[0], opnd(t[1])) + t[2:]
        blocks[b] = Block(phis + folded + rest, t)
    return Program(list(prog.params), blocks)


def dbe_pass(prog):
    """Dead branch elimination: a branch on a literal becomes a jump, then
    the blocks that the entry no longer reaches and their phi operands go."""
    terms = {}
    for b, blk in prog.blocks.items():
        t = blk.term
        if t[0] == "br" and isinstance(t[1], int):
            t = ("jump", t[2] if t[1] != 0 else t[3])
        terms[b] = t
    tmp = Program(list(prog.params), {b: Block([], terms[b]) for b in prog.blocks})
    seen, stack = {prog.entry}, [prog.entry]
    while stack:
        for s in succs(tmp, stack.pop()):
            if s not in seen:
                seen.add(s)
                stack.append(s)
    live_edges = {e for e in edges(tmp) if e[0] in seen}
    blocks = {}
    for b, blk in prog.blocks.items():
        if b not in seen:
            continue
        instrs = []
        for ins in blk.instrs:
            if ins[0] == "phi":
                ins = ("phi", ins[1], {p: a for p, a in ins[2].items() if (p, b) in live_edges})
            instrs.append(ins)
        blocks[b] = Block(instrs, terms[b])
    return Program(list(prog.params), blocks)


def cp_dbe_fixpoint(prog, order):
    """Apply the passes in the given order (a string over "C" and "D", then
    repeated) until neither pass changes the program."""
    passes = {"C": cp_pass, "D": dbe_pass}
    quiet = set()
    i = 0
    while len(quiet) < 2:
        name = order[i % len(order)]
        new = passes[name](prog)
        if show(new) == show(prog):
            quiet.add(name)
        else:
            quiet = set()
            prog = new
        i += 1
    return prog


# ---------------------------------------------------------- concrete runs


def trace(prog, args, fuel=5000):
    """Run an SSA program. Returns (outcome, assignments, blocks, edges)."""
    env = dict(zip(prog.params, args))
    assigned, blocks, taken = [], set(), set()
    label, prev = prog.entry, None
    try:
        while fuel > 0:
            blocks.add(label)
            taken.add((prev, label))
            blk = prog.blocks[label]
            incoming = []
            for ins in blk.instrs:
                fuel -= 1

                def val(a):
                    return a if isinstance(a, int) else env[a]

                if ins[0] == "phi":
                    incoming.append((ins[1], val(ins[2][prev])))
                    continue
                for x, v in incoming:
                    env[x] = v
                    assigned.append((x, v))
                incoming = []
                if ins[0] == "const":
                    v = ins[2]
                elif ins[0] == "copy":
                    v = val(ins[2])
                else:
                    v = toyir._binop(ins[2], val(ins[3]), val(ins[4]))
                env[ins[1]] = v
                assigned.append((ins[1], v))
            for x, v in incoming:
                env[x] = v
                assigned.append((x, v))
            t = blk.term
            if t[0] == "ret":
                return ("ret", t[1] if isinstance(t[1], int) else env[t[1]]), assigned, blocks, taken
            prev = label
            if t[0] == "jump":
                label = t[1]
            else:
                c = t[1] if isinstance(t[1], int) else env[t[1]]
                label = t[2] if c != 0 else t[3]
        return ("fuel",), assigned, blocks, taken
    except toyir._Trap:
        return ("trap",), assigned, blocks, taken


def arg_list(rng):
    fixed = [(0, 0), (1, 0), (0, 1), (2, 3), (3, -1), (5, 5)]
    return fixed + [(rng.randint(-6, 6), rng.randint(-6, 6)) for _ in range(4)]


# ------------------------------------------------------------------ checks


def check_fixed_point(prog, value, executable, visited):
    """(value, executable) is a fixed point of the combined map."""
    entry_edge = (None, prog.entry)
    assert {b for _, b in executable} == visited
    want = {entry_edge} | {(b, s) for b in visited for s in allowed(prog, b, value)}
    assert executable == want
    for b, blk in prog.blocks.items():
        for ins in blk.instrs:
            if b in visited:
                assert value[ins[1]] == evaluate(ins, value, lambda p, b=b: (p, b) in executable)
                assert value[ins[1]] != TOP  # strict SSA: nothing reachable stays TOP
            else:
                assert value[ins[1]] == TOP


def check_bounds(prog, value, executable, stats):
    nedges = len(edges(prog)) + 1
    assert stats["flow_pops"] == len(executable) <= nedges
    assert all(c <= 2 for c in stats["changes"].values())
    assert all(c <= 2 for c in stats["ssa_pushes"].values())
    ssa_edges = 0
    for blk in prog.blocks.values():
        ssa_edges += sum(len(set(toyir.uses(ins))) for ins in blk.instrs) + len(toyir.term_uses(blk.term))
    assert stats["ssa_pops"] == sum(stats["ssa_pushes"].values()) <= 2 * ssa_edges


def check_sound(ssa, value, executable, visited, args):
    out, assigned, blocks, taken = trace(ssa, args)
    for x, v in assigned:
        assert value[x] == BOT or value[x] == v, (x, value[x], v)
    assert blocks <= visited
    assert taken <= executable
    return out


def compare_with_cp_dbe(ssa, value, visited):
    """SCCP knows at least what any order of CP and DBE steps knows.
    Returns True when SCCP knows strictly more."""
    win = False
    for order in ("CD", "DC", "CCD", "DDC"):
        res = cp_dbe_fixpoint(ssa, order)
        assert visited <= set(res.blocks)
        known = {}
        for blk in res.blocks.values():
            for ins in blk.instrs:
                if ins[0] == "const":
                    known[ins[1]] = ins[2]
        for x, k in known.items():
            assert value[x] == TOP or value[x] == k
        sccp_known = {x for x, v in value.items() if v != BOT}
        defined = {ins[1] for blk in res.blocks.values() for ins in blk.instrs}
        if visited < set(res.blocks) or (sccp_known & defined) - set(known):
            win = True
    return win, res


# -------------------------------------------------------------------- tests


def test_loop_example() -> None:
    prog = parse(LOOP)
    ssa = to_ssa(prog)
    value, executable, visited, stats = sccp(ssa)
    check_fixed_point(ssa, value, executable, visited)
    assert "other" not in visited
    head_phi = [ins for ins in ssa.blocks["head"].instrs if ins[0] == "phi" and ins[1].startswith("i.")]
    assert len(head_phi) == 1 and value[head_phi[0][1]] == 1
    assert ssa.blocks["exit"].term[0] == "ret" and value[ssa.blocks["exit"].term[1]] == 1
    new, _ = sparse_conditional_constant_propagation(prog)
    assert "other" not in new.blocks and new.blocks["exit"].term == ("ret", 1)
    for n in range(-2, 6):
        assert run(prog, [n]) == run(new, [n]) == ("ret", 1)
    # Simple CP and DBE, in any order, keep i as BOT: SCCP wins.
    win, res = compare_with_cp_dbe(ssa, value, visited)
    assert win and "other" in res.blocks
    cp = cp_values(ssa)
    assert cp[head_phi[0][1]] == BOT


def test_known_branch() -> None:
    prog = parse(KNOWN)
    ssa = to_ssa(prog)
    value, executable, visited, _ = sccp(ssa)
    assert visited == {"entry", "then", "join"}
    z = ssa.blocks["join"].term[1]
    assert value[z] == 3
    cp = cp_values(ssa)
    assert cp[z] == BOT  # simple CP alone meets 2 with a
    win, res = compare_with_cp_dbe(ssa, value, visited)
    assert not win  # here CP then DBE then CP reaches the same result
    assert res.blocks["join"].term == ("ret", 3)


def test_lattice_and_fold() -> None:
    assert meet(TOP, 4) == 4 and meet(4, 4) == 4 and meet(4, 5) == BOT
    assert meet(BOT, TOP) == BOT
    assert fold("+", TOP, BOT) == TOP and fold("*", BOT, 0) == BOT
    assert fold("/", 7, 0) == BOT and fold("<<", 1, 64) == BOT
    assert fold("/", -7, 2) == -3 and fold("%", -7, 2) == -1


def random_cases(seed, count, acyclic):
    rng = random.Random(seed)
    for _ in range(count):
        prog = random_program(rng, 6, 8, acyclic)
        yield rng, prog


def test_random_programs() -> None:
    wins = 0
    total = 0
    for acyclic in (True, False):
        for rng, prog in random_cases(11 if acyclic else 12, 150, acyclic):
            ssa = to_ssa(prog)
            value, executable, visited, stats = sccp(ssa)
            check_fixed_point(ssa, value, executable, visited)
            check_bounds(ssa, value, executable, stats)
            assert naive_gfp(ssa) == (value, executable)
            new = rewrite(ssa, value, executable, visited)
            win, res = compare_with_cp_dbe(ssa, value, visited)
            # Without loops the combined map has one fixed point, so the
            # passes reach the SCCP result; a strict win needs a loop.
            assert not (acyclic and win)
            wins += win
            total += 1
            for args in arg_list(rng):
                want = run(prog, list(args))
                assert want[0] != "fuel"
                assert run(ssa, list(args)) == want
                assert run(new, list(args)) == want
                assert run(res, list(args)) == want
                assert check_sound(ssa, value, executable, visited, args) == want
    assert wins >= 5, wins


def test_strict_wins_with_constant_branches() -> None:
    """Programs whose branches test constants: SCCP is never worse than any
    CP and DBE order, and it is strictly better on some of them."""
    rng = random.Random(21)
    wins = 0
    for _ in range(120):
        prog = random_program(rng, 6, 8, False)
        for blk in prog.blocks.values():
            t = blk.term
            if t[0] == "br" and t[1] in ("x0", "x1") and rng.random() < 0.7:
                blk.term = ("br", rng.choice(["x2", "x3", "x4", "x5"]), t[2], t[3])
        ssa = to_ssa(prog)
        value, executable, visited, stats = sccp(ssa)
        check_bounds(ssa, value, executable, stats)
        win, res = compare_with_cp_dbe(ssa, value, visited)
        wins += win
        for args in arg_list(rng)[:4]:
            want = run(prog, list(args))
            assert run(res, list(args)) == want
            assert check_sound(ssa, value, executable, visited, args) == want
    assert wins >= 3, wins


def test_ssa_form() -> None:
    rng = random.Random(5)
    for _ in range(60):
        prog = random_program(rng, 5, 7, False)
        ssa = to_ssa(prog)
        names = [ins[1] for blk in ssa.blocks.values() for ins in blk.instrs]
        assert len(names) == len(set(names))
        assert all("." in x for x in names)
        assert set(ssa.blocks) == set(prog.blocks)
