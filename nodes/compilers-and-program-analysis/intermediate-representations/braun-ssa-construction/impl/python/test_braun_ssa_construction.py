# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/braun-ssa-construction/. The authors are listed in prov/T846M5.jsonl.

import random

import toyir
from braun_ssa_construction import braun_ssa, strip_versions

ODD_SUM = """
# params: n
B1:
  i = 0
  s = 0
  jump B2
B2:
  t1 = i < n
  br t1 B3 B6
B3:
  t2 = i % 2
  br t2 B4 B5
B4:
  s = s + i
  jump B5
B5:
  i = i + 1
  jump B2
B6:
  ret s
"""

ODD_SUM_SSA = """# params: n
B1:
  i.1 = 0
  s.1 = 0
  jump B2
B2:
  i.2 = phi [B1: i.1, B5: i.4]
  s.2 = phi [B1: s.1, B5: s.4]
  t1.1 = i.2 < n
  br t1.1 B3 B6
B3:
  t2.1 = i.2 % 2
  br t2.1 B4 B5
B4:
  s.3 = s.2 + i.2
  jump B5
B5:
  s.4 = phi [B3: s.2, B4: s.3]
  i.4 = i.2 + 1
  jump B2
B6:
  ret s.2
"""

# Two loops that enter each other: B2 and B3 form a cycle with two entries.
IRREDUCIBLE = """
# params: c, d
B1:
  x = 1
  br c B3 B2
B2:
  br d B3 B4
B3:
  y = x + 1
  br y B2 B4
B4:
  ret x
"""


# ------------------------------------------------------------ brute force


def graph(prog):
    return {label: toyir.succs(prog, label) for label in prog.blocks}


def _reach(succ, root, removed=None):
    if root == removed:
        return set()
    seen = {root}
    stack = [root]
    while stack:
        v = stack.pop()
        for w in succ[v]:
            if w != removed and w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def brute_dominators(succ, root):
    nodes = _reach(succ, root)
    dom = {v: set() for v in nodes}
    for d in nodes:
        left = _reach(succ, root, d)
        for v in nodes:
            if v not in left:
                dom[v].add(d)
    return dom


def brute_frontiers(succ, root):
    dom = brute_dominators(succ, root)
    df = {v: set() for v in dom}
    for p in dom:
        for y in succ[p]:
            for x in dom[p]:
                if not (x in dom[y] and x != y):
                    df[x].add(y)
    return df


def brute_idf(df, s):
    cur = set()
    while True:
        nxt = set()
        for x in set(s) | cur:
            nxt |= df[x]
        if nxt == cur:
            return cur
        cur = nxt


def brute_live_in(prog, v, start):
    """Is v read on some path from the top of start before any assignment?"""
    seen = set()
    stack = [start]
    while stack:
        b = stack.pop()
        if b in seen:
            continue
        seen.add(b)
        blk = prog.blocks[b]
        killed = False
        for ins in blk.instrs:
            if v in toyir.uses(ins):
                return True
            if ins[1] == v:
                killed = True
                break
        if killed:
            continue
        if v in toyir.term_uses(blk.term):
            return True
        stack.extend(toyir.succs(prog, b))
    return False


def pruned_minimal_phis(prog):
    """The phi-functions of pruned minimal SSA: v at y when y is in the
    iterated dominance frontier of the blocks that assign v and v is live on
    entry to y."""
    succ = graph(prog)
    df = brute_frontiers(succ, prog.entry)
    sites = {}
    for v in prog.params:
        sites[v] = {prog.entry}
    for label, b in prog.blocks.items():
        for ins in b.instrs:
            sites.setdefault(ins[1], {prog.entry}).add(label)
    out = set()
    for v, s in sites.items():
        for y in brute_idf(df, s):
            if brute_live_in(prog, v, y):
                out.add((y, v))
    return out


def reducible(prog):
    """Hecht and Ullman's T1 and T2: remove self-loops, and merge a node
    with a single predecessor into it. The graph is reducible exactly when
    this ends in one node."""
    succ = {v: set(ws) for v, ws in graph(prog).items()}
    changed = True
    while changed:
        changed = False
        for v in succ:
            succ[v].discard(v)
        pred = {v: set() for v in succ}
        for v, ws in succ.items():
            for w in ws:
                pred[w].add(v)
        for w in list(succ):
            if w != prog.entry and len(pred[w]) == 1:
                (p,) = pred[w]
                succ[p] |= succ[w]
                succ[p].discard(w)
                del succ[w]
                changed = True
                break
    return len(succ) == 1


def phi_set(ssa):
    return {(label, ins[1].rpartition(".")[0]) for label, b in ssa.blocks.items() for ins in b.instrs if ins[0] == "phi"}


def check_ssa(ssa):
    """Single assignment, one operand per incoming edge, and strictness."""
    succ = graph(ssa)
    pred = toyir.preds(ssa)
    dom = brute_dominators(succ, ssa.entry)
    where = {p: (ssa.entry, -1) for p in ssa.params}
    for label, b in ssa.blocks.items():
        for k, ins in enumerate(b.instrs):
            assert ins[1] not in where, "two definitions of %s" % ins[1]
            where[ins[1]] = (label, k)

    def dominates(d, block, pos):
        b, k = d
        return (b in dom[block] and b != block) or (b == block and k < pos)

    for label, b in ssa.blocks.items():
        seen_other = False
        for k, ins in enumerate(b.instrs):
            if ins[0] == "phi":
                assert not seen_other
                assert set(ins[2]) == set(pred[label])
                for p, a in ins[2].items():
                    if isinstance(a, str):
                        assert dominates(where[a], p, len(ssa.blocks[p].instrs))
            else:
                seen_other = True
                for a in toyir.uses(ins):
                    assert dominates(where[a], label, k)
        for a in toyir.term_uses(b.term):
            assert dominates(where[a], label, len(b.instrs))


def check_pruned_and_no_trivial(ssa):
    """Every phi-function transitively feeds a non-phi use, and none of them
    merges only itself and one other value."""
    phis = {ins[1]: ins for b in ssa.blocks.values() for ins in b.instrs if ins[0] == "phi"}
    useful, work = set(), []
    for b in ssa.blocks.values():
        for ins in b.instrs:
            if ins[0] != "phi":
                work += toyir.uses(ins)
        work += toyir.term_uses(b.term)
    while work:
        a = work.pop()
        if a not in useful:
            useful.add(a)
            if a in phis:
                work += [x for x in phis[a][2].values() if isinstance(x, str)]
    for x, ins in phis.items():
        assert x in useful, "dead phi %s" % x
        others = set(ins[2].values()) - {x}
        assert len(others) >= 2, "trivial phi %s" % x


def trace(prog, args, fuel=2000):
    """The operand values of every executed non-phi instruction and
    terminator, in order."""
    env = dict(zip(prog.params, args))
    label, prev, out = prog.entry, None, []
    while fuel > 0:
        fuel -= 1
        b = prog.blocks[label]
        phis = [ins for ins in b.instrs if ins[0] == "phi"]
        env.update([(ins[1], env[ins[2][prev]]) for ins in phis])
        for ins in b.instrs:
            if ins[0] == "phi":
                continue
            if ins[0] == "const" and ins[1].endswith(".0"):
                env[ins[1]] = ins[2]
                continue
            if ins[0] == "const":
                vals = [ins[2]]
            elif ins[0] == "copy":
                vals = [env[ins[2]]]
            else:
                vals = [ins[2]] + [env[a] if isinstance(a, str) else a for a in ins[3:]]
            out.append((label, tuple(vals)))
            if ins[0] == "const":
                env[ins[1]] = ins[2]
            elif ins[0] == "copy":
                env[ins[1]] = vals[0]
            else:
                try:
                    env[ins[1]] = toyir._binop(ins[2], vals[1], vals[2])
                except toyir._Trap:
                    out.append(("trap",))
                    return out
        t = b.term
        if t[0] == "jump":
            prev, label = label, t[1]
            continue
        c = env[t[1]] if isinstance(t[1], str) else t[1]
        out.append((label, t[0], c))
        if t[0] == "ret":
            return out
        prev, label = label, (t[2] if c != 0 else t[3])
    out.append(("fuel",))
    return out


def programs(seed, count, nvars=6, nblocks=8):
    rng = random.Random(seed)
    for k in range(count):
        yield rng, toyir.random_program(rng, nvars, nblocks, acyclic=(k % 3 == 0))


# ------------------------------------------------------------------ tests


def test_page_example():
    prog = toyir.parse(ODD_SUM)
    ssa = braun_ssa(prog)
    assert toyir.show(ssa) == ODD_SUM_SSA
    for n in range(-2, 12):
        assert toyir.run(ssa, [n]) == toyir.run(prog, [n])


def test_reducible_gives_pruned_minimal_ssa():
    # Braun et al., Section 4: pruned always, minimal on reducible graphs.
    seen = 0
    for _, prog in programs(1, 400):
        if reducible(prog):
            seen += 1
            assert phi_set(braun_ssa(prog)) == pruned_minimal_phis(prog)
    assert seen > 100


def test_scc_pass_gives_pruned_minimal_ssa_on_any_graph():
    irreducible = 0
    for _, prog in programs(2, 400):
        irreducible += not reducible(prog)
        assert phi_set(braun_ssa(prog, minimize_sccs=True)) == pruned_minimal_phis(prog)
    assert irreducible > 10


def test_irreducible_example():
    prog = toyir.parse(IRREDUCIBLE)
    assert not reducible(prog)
    plain = braun_ssa(prog)
    assert phi_set(plain) == {("B2", "x"), ("B3", "x"), ("B4", "x"), ("B2", "d"), ("B3", "d")}
    assert phi_set(braun_ssa(prog, minimize_sccs=True)) == set() == pruned_minimal_phis(prog)
    for c in (0, 1):
        for d in (0, 1):
            assert toyir.run(plain, [c, d]) == toyir.run(prog, [c, d])


def test_pruned_and_no_trivial_phis():
    for _, prog in programs(3, 300):
        for flag in (False, True):
            check_pruned_and_no_trivial(braun_ssa(prog, flag))


def test_ssa_is_single_assignment_and_strict():
    for _, prog in programs(4, 300):
        check_ssa(braun_ssa(prog))
        check_ssa(braun_ssa(prog, minimize_sccs=True))


def test_every_use_reads_the_original_value():
    for rng, prog in programs(5, 300):
        ssa = braun_ssa(prog)
        for _ in range(4):
            args = [rng.randint(-3, 6), rng.randint(-3, 6)]
            assert trace(ssa, args) == trace(prog, args)


def test_round_trip_outputs():
    for rng, prog in programs(6, 300):
        a = braun_ssa(prog)
        b = braun_ssa(prog, minimize_sccs=True)
        for _ in range(4):
            args = [rng.randint(-4, 8), rng.randint(-4, 8)]
            want = toyir.run(prog, args)
            assert toyir.run(a, args) == want
            assert toyir.run(b, args) == want
            assert toyir.run(strip_versions(a), args) == want
            assert toyir.run(strip_versions(b), args) == want


def test_read_before_write_gets_entry_definition():
    prog = toyir.parse("# params: c\nB1:\n  br c B2 B3\nB2:\n  x = 4\n  jump B3\nB3:\n  ret x\n")
    ssa = braun_ssa(prog)
    assert ssa.blocks["B1"].instrs[0] == ("const", "x.0", 0)
    check_ssa(ssa)
    assert toyir.run(ssa, [1]) == ("ret", 4)
    assert toyir.run(ssa, [0]) == ("ret", 0)


def test_rejects_phi_input():
    prog = toyir.parse("B1:\n  jump B2\nB2:\n  x = phi [B1: 1]\n  ret x\n")
    try:
        braun_ssa(prog)
    except ValueError:
        return
    assert False
