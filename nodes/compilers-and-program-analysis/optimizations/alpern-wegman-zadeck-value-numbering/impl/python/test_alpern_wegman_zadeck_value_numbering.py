# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alpern-wegman-zadeck-value-numbering/. The authors are listed in prov/1FT49Y.jsonl.

import itertools
import random

import toyir
from alpern_wegman_zadeck_value_numbering import (
    awz,
    congruence,
    dominates,
    dominators,
    to_ssa,
    value_graph,
)

# The example of the page: i and j step together, so a and b are equal.
PAGE = """
# params: n
entry:
  i = 1
  j = 1
  s = 0
  jump loop
loop:
  a = i * 4
  b = j * 4
  s = s + a
  s = s + b
  i = i + 1
  j = j + 1
  c = i <= n
  br c loop exit
exit:
  ret s
"""

PAGE_AFTER = """# params: n
entry:
  jump loop
loop:
  i.1 = phi [entry: 1, loop: i.2]
  s.1 = phi [entry: 0, loop: s.3]
  j.1 = i.1
  a.1 = i.1 * 4
  b.1 = a.1
  s.2 = s.1 + a.1
  s.3 = s.2 + b.1
  i.2 = i.1 + 1
  j.2 = i.2
  c.1 = i.2 <= n
  br c.1 loop exit
exit:
  ret s.3
"""

# Two branches compute the same sum, and the phis that merge them are
# congruent. The two divisions are congruent, but neither dominates the
# other, so both stay.
DIAMOND = """
# params: x, y, p
entry:
  br p left right
left:
  u = x + y
  v = x + y
  q = x / y
  jump join
right:
  u = y
  v = y
  jump join
join:
  w = u - v
  r = x / y
  ret w
"""


# ------------------------------------------------------------------ helpers


def trace(prog, args, fuel=20000):
    """Run prog like toyir.run and also return the number of op
    instructions run and the environment at the end of each block, as a
    list of (label, env). Programs here have no memory operations."""
    env = dict(zip(prog.params, args))
    label, prev, ops, ends = prog.entry, None, 0, []
    while True:
        blk = prog.blocks[label]
        incoming = []
        rest = []
        for ins in blk.instrs:
            if ins[0] == "phi":
                incoming.append((ins[1], val(env, ins[2][prev])))
                fuel -= 1
            else:
                rest.append(ins)
        for x, v in incoming:
            env[x] = v
        for ins in rest:
            fuel -= 1
            if fuel < 0:
                return ("fuel",), ops, ends
            if ins[0] == "const":
                env[ins[1]] = ins[2]
            elif ins[0] == "copy":
                env[ins[1]] = val(env, ins[2])
            else:
                ops += 1
                try:
                    env[ins[1]] = toyir._binop(ins[2], val(env, ins[3]), val(env, ins[4]))
                except toyir._Trap:
                    return ("trap",), ops, ends
        fuel -= 1
        if fuel < 0:
            return ("fuel",), ops, ends
        ends.append((label, dict(env)))
        t = blk.term
        if t[0] == "ret":
            return ("ret", val(env, t[1])), ops, ends
        if t[0] == "jump":
            prev, label = label, t[1]
        else:
            prev, label = label, (t[2] if val(env, t[1]) != 0 else t[3])


def val(env, a):
    return a if isinstance(a, int) else env[a]


def shadowed(prog):
    """Add a shadow v_s of every variable v that is computed by the same
    instructions, so that v_s and v always hold the same value."""
    def sh(a):
        return a if isinstance(a, int) else a + "_s"

    blocks = {}
    for label, blk in prog.blocks.items():
        out = []
        if label == prog.entry:
            out += [("copy", sh(p), p) for p in prog.params]
        for ins in blk.instrs:
            out.append(ins)
            if ins[0] == "const":
                out.append(("const", sh(ins[1]), ins[2]))
            elif ins[0] == "copy":
                out.append(("copy", sh(ins[1]), sh(ins[2])))
            else:
                out.append(("op", sh(ins[1]), ins[2], sh(ins[3]), sh(ins[4])))
        blocks[label] = toyir.Block(out, blk.term)
    return toyir.Program(list(prog.params), blocks)


def programs(seed, count):
    rng = random.Random(seed)
    for k in range(count):
        p = toyir.random_program(rng, rng.randint(2, 5), rng.randint(1, 7), k % 2 == 0)
        yield rng, (shadowed(p) if k % 3 == 0 else p)


def def_blocks(ssa):
    where = {p: ssa.entry for p in ssa.params}
    for b, blk in ssa.blocks.items():
        for ins in blk.instrs:
            where[ins[1]] = b
    return where


def classes(cls):
    out = {}
    for n, c in cls.items():
        out.setdefault(c, set()).add(n)
    return {frozenset(s) for s in out.values()}


def moore(nodes, label, children):
    """The naive refinement: split by (class, classes of the children)
    until nothing changes."""
    cls = {n: (label[n], len(children[n])) for n in nodes}
    while True:
        sig = {n: (cls[n], tuple(cls[c] for c in children[n])) for n in nodes}
        if len(set(sig.values())) == len(set(cls.values())):
            return cls
        cls = sig


def set_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in set_partitions(rest):
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]
        yield [[first]] + part


def random_graph(rng, n):
    nodes = list(range(n))
    label, children = {}, {}
    for v in nodes:
        k = rng.randint(0, 2)
        label[v] = rng.choice("ab") if k else rng.choice("xy")
        children[v] = tuple(rng.randrange(n) for _ in range(k))
    return nodes, label, children


def hash_numbering(ssa):
    """Pessimistic value numbering: visit the blocks in reverse postorder
    and give a phi a known number only if all its operands are numbered."""
    from alpern_wegman_zadeck_value_numbering import reverse_postorder

    num, table = {}, {}

    def of(a):
        if isinstance(a, int):
            return ("const", a)
        return num.get(a, ("fresh", a))

    for p in ssa.params:
        num[p] = ("param", p)
    for b in reverse_postorder(ssa):
        for ins in ssa.blocks[b].instrs:
            if ins[0] == "phi":
                if any(isinstance(a, str) and a not in num for a in ins[2].values()):
                    num[ins[1]] = ("fresh", ins[1])
                    continue
                key = ("phi", b) + tuple(of(a) for a in ins[2].values())
            else:
                key = ("op", ins[2], of(ins[3]), of(ins[4]))
            num[ins[1]] = table.setdefault(key, ("v", len(table)))
    return num


# -------------------------------------------------------------------- tests


def test_page_example():
    prog = toyir.parse(PAGE)
    out, cls = awz(prog)
    assert toyir.show(out) == PAGE_AFTER
    for n in (0, 1, 2, 5):
        assert toyir.run(out, [n]) == toyir.run(prog, [n])
    assert toyir.run(out, [3]) == ("ret", 48)
    _, before, _ = trace(to_ssa(prog), [3])
    _, after, _ = trace(out, [3])
    assert (before, after) == (21, 15)


def test_optimistic_finds_what_hashing_misses():
    ssa = to_ssa(toyir.parse(PAGE))
    _, cls = awz(toyir.parse(PAGE))
    assert cls["i.1"] == cls["j.1"] and cls["a.1"] == cls["b.1"]
    num = hash_numbering(ssa)
    assert num["i.1"] != num["j.1"] and num["a.1"] != num["b.1"]


def test_diamond():
    prog = toyir.parse(DIAMOND)
    ssa = to_ssa(prog)
    out, cls = awz(prog)
    assert cls["u.1"] == cls["v.1"] and cls["u.2"] == cls["v.2"]
    assert cls["q.1"] == cls["r.1"]
    assert cls["w.1"] != cls["u.2"]
    text = toyir.show(out)
    assert "v.1 = u.1" in text and "v.2 = u.2" in text
    assert "r.1 = x / y" in text
    for args in ([3, 4, 0], [3, 4, 1], [3, 0, 0], [3, 0, 1]):
        assert toyir.run(out, args) == toyir.run(prog, args) == toyir.run(ssa, args)


def test_same_outcome_on_random_programs():
    for rng, prog in programs(11, 300):
        out, _ = awz(prog)
        ssa = to_ssa(prog)
        for _ in range(8):
            args = [rng.randint(-4, 9), rng.randint(-4, 9)]
            want = toyir.run(prog, args)
            assert want[0] != "fuel"
            assert toyir.run(ssa, args) == want
            assert toyir.run(out, args) == want


def test_never_more_operations():
    for rng, prog in programs(12, 200):
        out, _ = awz(prog)
        for _ in range(6):
            args = [rng.randint(-4, 9), rng.randint(-4, 9)]
            r0, n0, _ = trace(prog, args)
            r1, n1, _ = trace(out, args)
            assert r0 == r1 == toyir.run(prog, args)
            assert n1 <= n0


def test_shadows_are_found():
    rng = random.Random(13)
    checked = 0
    for k in range(150):
        p = toyir.random_program(rng, rng.randint(2, 5), rng.randint(1, 7), k % 2 == 0)
        ssa = to_ssa(shadowed(p))
        _, cls = awz(shadowed(p))
        for blk in ssa.blocks.values():
            phi_of = {ins[1].partition(".")[0]: ins[1] for ins in blk.instrs if ins[0] == "phi"}
            for i, ins in enumerate(blk.instrs):
                base = ins[1].partition(".")[0]
                if not base.endswith("_s"):
                    continue
                # A shadow phi has the phi of its variable in the same block,
                # and a shadow op follows the op it copies.
                twin = phi_of[base[:-2]] if ins[0] == "phi" else blk.instrs[i - 1][1]
                assert cls[ins[1]] == cls[twin]
                checked += 1
    assert checked > 300


def test_congruent_names_hold_equal_values():
    for rng, prog in programs(14, 200):
        ssa = to_ssa(prog)
        nodes, label, children = value_graph(ssa)
        cls = congruence(nodes, label, children)
        idom = dominators(ssa)
        where = def_blocks(ssa)
        by = {}
        for n in where:
            by.setdefault(cls[n], []).append(n)
        for _ in range(6):
            args = [rng.randint(-4, 9), rng.randint(-4, 9)]
            _, _, ends = trace(ssa, args)
            for label_, env in ends:
                for names in by.values():
                    live = [n for n in names if dominates(idom, where[n], label_)]
                    assert len({env[n] for n in live}) <= 1


def herbrand_terms(ssa, path):
    """The Herbrand term of every name at the end of each block of a path:
    parameters are atoms, constants are integers, an op is a tuple."""
    env = {p: ("param", p) for p in ssa.params}
    out = []
    prev = None
    for label in path:
        blk = ssa.blocks[label]
        new = {}
        for ins in blk.instrs:
            if ins[0] == "phi":
                a = ins[2][prev]
                new[ins[1]] = a if isinstance(a, int) else env[a]
        env.update(new)
        for ins in blk.instrs:
            if ins[0] == "op":
                a, b = ins[3], ins[4]
                ta = a if isinstance(a, int) else env[a]
                tb = b if isinstance(b, int) else env[b]
                env[ins[1]] = (ins[2], ta, tb)
        out.append((label, dict(env)))
        prev = label
    return out


def test_congruence_implies_herbrand_equivalence():
    rng = random.Random(15)
    for k in range(150):
        p = toyir.random_program(rng, rng.randint(2, 4), rng.randint(2, 6), True)
        if k % 2 == 0:
            p = shadowed(p)
        ssa = to_ssa(p)
        nodes, label, children = value_graph(ssa)
        cls = congruence(nodes, label, children)
        idom = dominators(ssa)
        where = def_blocks(ssa)
        for path in toyir.paths(ssa):
            for lab, env in herbrand_terms(ssa, path):
                for x, y in itertools.combinations(sorted(where), 2):
                    if cls[x] == cls[y] and dominates(idom, where[x], lab) and dominates(idom, where[y], lab):
                        assert env[x] == env[y]


def test_hopcroft_equals_naive_refinement():
    rng = random.Random(16)
    for k in range(300):
        if k % 2:
            nodes, label, children = random_graph(rng, rng.randint(1, 30))
        else:
            p = toyir.random_program(rng, rng.randint(2, 5), rng.randint(1, 7), k % 4 == 0)
            nodes, label, children = value_graph(to_ssa(shadowed(p)))
        assert classes(congruence(nodes, label, children)) == classes(moore(nodes, label, children))


def test_coarsest_by_brute_force():
    rng = random.Random(17)
    for _ in range(60):
        nodes, label, children = random_graph(rng, rng.randint(1, 7))
        best = classes(congruence(nodes, label, children))
        found = False
        for part in set_partitions(nodes):
            c = {v: i for i, block in enumerate(part) for v in block}
            if any(label[u] != label[v] or len(children[u]) != len(children[v]) for block in part for u in block for v in block):
                continue
            ok = all(
                c[children[u][j]] == c[children[v][j]]
                for block in part
                for u in block
                for v in block
                for j in range(len(children[u]))
            )
            if not ok:
                continue
            # Every congruence refines the one AWZ finds.
            assert all(any(set(block) <= b for b in best) for block in part)
            found = found or {frozenset(block) for block in part} == best
        assert found
