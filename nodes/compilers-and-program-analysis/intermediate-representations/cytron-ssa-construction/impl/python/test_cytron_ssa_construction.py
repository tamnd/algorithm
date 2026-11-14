# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cytron-ssa-construction/. The authors are listed in prov/BVFDF2.jsonl.

import random

import toyir
from toyir import Block, Program
from cytron_ssa_construction import cytron_ssa, place_phis, strip_versions, variables

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
  t1.0 = 0
  t2.0 = 0
  i.1 = 0
  s.1 = 0
  jump B2
B2:
  i.2 = phi [B1: i.1, B5: i.3]
  s.2 = phi [B1: s.1, B5: s.4]
  t1.1 = phi [B1: t1.0, B5: t1.2]
  t2.1 = phi [B1: t2.0, B5: t2.2]
  t1.2 = i.2 < n
  br t1.2 B3 B6
B3:
  t2.2 = i.2 % 2
  br t2.2 B4 B5
B4:
  s.3 = s.2 + i.2
  jump B5
B5:
  s.4 = phi [B3: s.2, B4: s.3]
  i.3 = i.2 + 1
  jump B2
B6:
  ret s.2
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


def def_sites(prog):
    sites = {v: {prog.entry} for v in variables(prog)}
    for label, b in prog.blocks.items():
        for ins in b.instrs:
            sites[ins[1]].add(label)
    return sites


def brute_idf(df, s):
    cur = set()
    while True:
        nxt = set()
        for x in set(s) | cur:
            nxt |= df[x]
        if nxt == cur:
            return cur
        cur = nxt


def _paths_into(succ, x):
    """All non-empty paths from x that end at their first repeated node or
    earlier, as (end, set of nodes before the end). A path may end at x."""
    out = []

    def walk(v, seen):
        for w in succ[v]:
            out.append((w, frozenset(seen)))
            if w not in seen:
                seen.add(w)
                walk(w, seen)
                seen.remove(w)

    walk(x, {x})
    return out


def brute_join(succ, s):
    """J(S): nodes y with two non-empty paths from two different nodes of S
    that end at y and share no node but y."""
    ends = {x: {} for x in s}
    for x in s:
        for y, before in _paths_into(succ, x):
            if y in before and y != x:
                continue  # the path passed y before its end
            ends[x].setdefault(y, set()).add(before - {y})
    out = set()
    xs = sorted(s)
    for i, a in enumerate(xs):
        for b in xs[i + 1:]:
            for y in set(ends[a]) & set(ends[b]):
                if any(not (p & q) for p in ends[a][y] for q in ends[b][y]):
                    out.add(y)
    return out


def brute_iterated_join(succ, s):
    cur = set()
    while True:
        nxt = brute_join(succ, set(s) | cur)
        if nxt == cur:
            return cur
        cur = nxt


def trace(prog, args, skip=(), fuel=2000):
    """Run prog and record, for each executed non-phi instruction and
    terminator, the values of its operands. Instructions that define a name
    in skip are not recorded."""
    env = dict(zip(prog.params, args))
    label, prev, out = prog.entry, None, []
    while fuel > 0:
        fuel -= 1
        b = prog.blocks[label]
        phis = [ins for ins in b.instrs if ins[0] == "phi"]
        env.update([(ins[1], env[ins[2][prev]]) for ins in phis])
        k = 0
        for ins in b.instrs:
            if ins[0] == "phi":
                continue
            ops = [a if isinstance(a, int) else env[a] for a in toyir.uses(ins) + [x for x in ins[2:] if isinstance(x, int)]]
            if ins[1] not in skip:
                out.append((label, k, tuple(ops)))
                k += 1
            if ins[0] == "const":
                env[ins[1]] = ins[2]
            elif ins[0] == "copy":
                env[ins[1]] = ops[0]
            else:
                a = env[ins[3]] if isinstance(ins[3], str) else ins[3]
                c = env[ins[4]] if isinstance(ins[4], str) else ins[4]
                try:
                    env[ins[1]] = toyir._binop(ins[2], a, c)
                except toyir._Trap:
                    out.append(("trap",))
                    return out
        t = b.term
        if t[0] == "ret":
            out.append((label, "ret", env[t[1]] if isinstance(t[1], str) else t[1]))
            return out
        if t[0] == "jump":
            prev, label = label, t[1]
        else:
            c = env[t[1]] if isinstance(t[1], str) else t[1]
            out.append((label, "br", c))
            prev, label = label, (t[2] if c != 0 else t[3])
    out.append(("fuel",))
    return out


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


def programs(seed, count, nvars=6, nblocks=8):
    rng = random.Random(seed)
    for k in range(count):
        yield rng, toyir.random_program(rng, nvars, nblocks, acyclic=(k % 3 == 0))


# ------------------------------------------------------------------ tests


def test_page_example():
    prog = toyir.parse(ODD_SUM)
    ssa = cytron_ssa(prog)
    assert toyir.show(ssa) == ODD_SUM_SSA
    for n in range(-2, 12):
        assert toyir.run(ssa, [n]) == toyir.run(prog, [n])


def test_phis_at_iterated_frontier():
    for _, prog in programs(1, 300):
        succ = graph(prog)
        df = brute_frontiers(succ, prog.entry)
        phis = place_phis(prog)
        for v, s in def_sites(prog).items():
            want = brute_idf(df, s)
            got = {b for b, vs in phis.items() if v in vs}
            assert got == want
            assert all(phis[b].count(v) <= 1 for b in phis)


def test_iterated_frontier_is_the_join_set():
    # Minimality: a phi-function goes exactly where two definitions converge.
    for _, prog in programs(2, 150, nvars=4, nblocks=6):
        succ = graph(prog)
        df = brute_frontiers(succ, prog.entry)
        for v, s in def_sites(prog).items():
            j = brute_join(succ, s)
            assert brute_idf(df, s) == j
            assert brute_iterated_join(succ, s) == j


def test_ssa_is_single_assignment_and_strict():
    for _, prog in programs(3, 300):
        check_ssa(cytron_ssa(prog))


def test_every_use_reads_the_original_value():
    for rng, prog in programs(4, 300):
        ssa = cytron_ssa(prog)
        skip = {ins[1] for ins in ssa.blocks[ssa.entry].instrs if ins[1].endswith(".0")}
        for _ in range(4):
            args = [rng.randint(-3, 6), rng.randint(-3, 6)]
            assert trace(ssa, args, skip) == trace(prog, args)


def test_round_trip_outputs():
    for rng, prog in programs(5, 400):
        ssa = cytron_ssa(prog)
        back = strip_versions(ssa)
        for _ in range(5):
            args = [rng.randint(-4, 8), rng.randint(-4, 8)]
            want = toyir.run(prog, args)
            assert toyir.run(ssa, args) == want
            assert toyir.run(back, args) == want


def test_quadratic_family():
    for n in range(1, 10):
        blocks = {"E": Block([], ("jump", "h1"))}
        for i in range(1, n + 1):
            blocks["h%d" % i] = Block([], ("jump", "h%d" % (i + 1) if i < n else "l%d" % n))
        for i in range(n, 0, -1):
            nxt = "l%d" % (i - 1) if i > 1 else "X"
            blocks["l%d" % i] = Block([("const", "v%d" % i, i)], ("br", "c", "h%d" % i, nxt))
        blocks["X"] = Block([], ("ret", 0))
        prog = Program(["c"], blocks)
        phis = place_phis(prog)
        assert sum(len(vs) for vs in phis.values()) == n * (n + 1) // 2
        check_ssa(cytron_ssa(prog))
        assert toyir.run(cytron_ssa(prog), [0]) == ("ret", 0)


def test_rejects_phi_input():
    prog = toyir.parse("B1:\n  jump B2\nB2:\n  x = phi [B1: 1]\n  ret x\n")
    try:
        cytron_ssa(prog)
    except ValueError:
        return
    assert False
