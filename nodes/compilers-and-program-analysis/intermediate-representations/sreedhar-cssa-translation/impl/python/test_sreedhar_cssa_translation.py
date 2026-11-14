# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sreedhar-cssa-translation/. The authors are listed in prov/N0QEY1.jsonl.

import random

import toyir
from sreedhar_cssa_translation import rename_classes, sreedhar_out_of_ssa, to_cssa

LOST_COPY = """
# params: n
B1:
  x.1 = 1
  jump B2
B2:
  x.2 = phi [B1: x.1, B2: x.3]
  x.3 = x.2 + 1
  t.1 = x.3 < n
  br t.1 B2 B3
B3:
  ret x.2
"""

SWAP = """
# params: n
B1:
  a.1 = 1
  b.1 = 2
  i.1 = 1
  jump B2
B2:
  a.2 = phi [B1: a.1, B2: b.2]
  b.2 = phi [B1: b.1, B2: a.2]
  i.2 = phi [B1: i.1, B2: i.3]
  i.3 = i.2 + 1
  t.1 = i.2 < n
  br t.1 B2 B3
B3:
  r.1 = a.2 * 10
  r.2 = r.1 + b.2
  ret r.2
"""

DIAMOND = """
# params: c
B1:
  br c B2 B3
B2:
  x.1 = 1
  jump B4
B3:
  x.2 = 2
  jump B4
B4:
  x.3 = phi [B2: x.1, B3: x.2]
  ret x.3
"""


# ------------------------------------------------------- building TSSA input


def _rename(ins, m, d):
    if ins[0] == "const":
        return ("const", d, ins[2])
    if ins[0] == "copy":
        return ("copy", d, m(ins[2]))
    return ("op", d, ins[2], m(ins[3]), m(ins[4]))


def _rename_term(t, m):
    return (t[0], m(t[1])) + tuple(t[2:]) if t[0] in ("br", "ret") else t


def maximal_ssa(prog):
    """SSA form with a phi-function for every variable at the top of every
    block but the entry. A variable that is not a parameter starts as v.0 = 0
    at the top of the entry. This form is conventional."""
    pred = toyir.preds(prog)
    names = set(prog.params)
    for b in prog.blocks.values():
        for ins in b.instrs:
            names.add(ins[1])
            names.update(toyir.uses(ins))
        names.update(toyir.term_uses(b.term))
    names = sorted(names)
    count = {}
    end = {}
    blocks = {}
    for label, b in prog.blocks.items():
        instrs = []
        if label == prog.entry:
            cur = {}
            for v in names:
                if v in prog.params:
                    cur[v] = v
                else:
                    cur[v] = v + ".0"
                    instrs.append(("const", v + ".0", 0))
        else:
            cur = {v: "%s.%s" % (v, label) for v in names}
        for ins in b.instrs:
            v = ins[1]
            count[v] = count.get(v, 0) + 1
            d = "%s.%d" % (v, count[v])
            instrs.append(_rename(ins, lambda a: cur[a] if isinstance(a, str) else a, d))
            cur[v] = d
        end[label] = cur
        blocks[label] = toyir.Block(instrs, _rename_term(b.term, lambda a: cur[a] if isinstance(a, str) else a))
    for label, b in blocks.items():
        if label != prog.entry:
            phis = [("phi", "%s.%s" % (v, label), {p: end[p][v] for p in pred[label]}) for v in names]
            b.instrs[0:0] = phis
    return toyir.Program(list(prog.params), blocks)


def fold(ssa, constants=False):
    """Copy folding and removal of trivial phi-functions, until nothing
    changes. This is what makes SSA form transformed. With constants=True,
    phi operands defined by a constant become that constant."""
    blocks = {label: toyir.Block(list(b.instrs), b.term) for label, b in ssa.blocks.items()}
    repl = {}

    def r(a):
        while isinstance(a, str) and a in repl:
            a = repl[a]
        return a

    changed = True
    while changed:
        changed = False
        for b in blocks.values():
            out = []
            for ins in b.instrs:
                if ins[0] == "copy":
                    repl[ins[1]] = r(ins[2])
                    changed = True
                    continue
                if ins[0] == "phi":
                    ops = {p: r(a) for p, a in ins[2].items()}
                    others = set(ops.values()) - {ins[1]}
                    if len(others) == 1:
                        repl[ins[1]] = others.pop()
                        changed = True
                        continue
                    ins = ("phi", ins[1], ops)
                out.append(ins)
            b.instrs = out
    const = {ins[1]: ins[2] for b in blocks.values() for ins in b.instrs if ins[0] == "const"}
    for b in blocks.values():
        out = []
        for ins in b.instrs:
            if ins[0] == "phi":
                ops = {p: r(a) for p, a in ins[2].items()}
                if constants:
                    ops = {p: const.get(a, a) for p, a in ops.items()}
                out.append(("phi", ins[1], ops))
            else:
                out.append(_rename(ins, r, ins[1]))
        b.instrs = out
        b.term = _rename_term(b.term, r)
    return toyir.Program(list(ssa.params), blocks)


# --------------------------------------------------------------- brute force


def _live_from(prog, succ, label, start, name):
    """Is name read on some path that starts at instruction start of label,
    before it is defined again? A phi operand is read at the end of its
    predecessor."""
    stack, seen = [(label, start)], set()
    while stack:
        b, i = stack.pop()
        if (b, i) in seen:
            continue
        seen.add((b, i))
        blk = prog.blocks[b]
        killed = False
        for ins in blk.instrs[i:]:
            if name in toyir.uses(ins):
                return True
            if ins[1] == name:
                killed = True
                break
        if killed:
            continue
        if name in toyir.term_uses(blk.term):
            return True
        for s in succ[b]:
            phis = [ins for ins in prog.blocks[s].instrs if ins[0] == "phi"]
            if any(ins[2][b] == name for ins in phis):
                return True
            if not any(ins[1] == name for ins in phis):
                stack.append((s, len(phis)))
    return False


def brute_interferes(prog):
    """A function telling whether two names interfere: one is live just after
    the definition of the other."""
    succ = {label: toyir.succs(prog, label) for label in prog.blocks}
    site = {p: (prog.entry, 0) for p in prog.params}
    for label, b in prog.blocks.items():
        nphi = sum(1 for ins in b.instrs if ins[0] == "phi")
        for k, ins in enumerate(b.instrs):
            site[ins[1]] = (label, nphi if ins[0] == "phi" else k + 1)

    def interferes(u, w):
        if u == w:
            return False
        return _live_from(prog, succ, *site[w], u) or _live_from(prog, succ, *site[u], w)

    return interferes


def brute_classes(prog):
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            x = parent[x]
        return x

    for b in prog.blocks.values():
        for ins in b.instrs:
            if ins[0] == "phi":
                for a in ins[2].values():
                    if isinstance(a, str):
                        parent[find(a)] = find(ins[1])
    out = {}
    for x in parent:
        out.setdefault(find(x), []).append(x)
    return list(out.values())


def is_conventional(prog):
    interferes = brute_interferes(prog)
    for cls in brute_classes(prog):
        for i, u in enumerate(cls):
            for w in cls[i + 1 :]:
                if interferes(u, w):
                    return False
    return all(isinstance(a, str) for b in prog.blocks.values() for ins in b.instrs if ins[0] == "phi" for a in ins[2].values())


def single_assignment(prog):
    seen = set(prog.params)
    for b in prog.blocks.values():
        for ins in b.instrs:
            if ins[1] in seen:
                return False
            seen.add(ins[1])
    return True


def tssa_programs(seed, count):
    rng = random.Random(seed)
    for k in range(count):
        prog = toyir.random_program(rng, 4, rng.randint(3, 7), acyclic=(k % 4 == 0))
        yield rng, prog, fold(maximal_ssa(prog), constants=(k % 2 == 1))


def phi_operands(prog):
    return sum(len(ins[2]) + 1 for b in prog.blocks.values() for ins in b.instrs if ins[0] == "phi")


# ------------------------------------------------------------------ tests


def test_lost_copy():
    ssa = toyir.parse(LOST_COPY)
    assert not is_conventional(ssa)
    # Renaming without copies loses the old value of x: 3 instead of 2.
    assert toyir.run(ssa, [3]) == ("ret", 2)
    assert toyir.run(rename_classes(ssa), [3]) == ("ret", 3)
    cssa, copies = to_cssa(ssa)
    assert copies == 1
    assert is_conventional(cssa)
    out = rename_classes(cssa)
    assert toyir.show(out) == (
        "# params: n\nB1:\n  x.1 = 1\n  jump B2\nB2:\n  x.2 = x.1\n  x.1 = x.2 + 1\n"
        "  t.1 = x.1 < n\n  br t.1 B2 B3\nB3:\n  ret x.2\n"
    )
    for n in range(-1, 8):
        assert toyir.run(out, [n]) == toyir.run(ssa, [n])


def test_swap():
    ssa = toyir.parse(SWAP)
    assert not is_conventional(ssa)
    assert toyir.run(rename_classes(ssa), [2]) == ("ret", 22)
    out, copies = sreedhar_out_of_ssa(ssa)
    assert copies == 5
    _, copies1 = sreedhar_out_of_ssa(ssa, method=1)
    assert copies1 == 9
    assert [toyir.run(out, [n])[1] for n in range(1, 6)] == [12, 21, 12, 21, 12]
    for n in range(-1, 8):
        assert toyir.run(out, [n]) == toyir.run(ssa, [n])


def test_conventional_input_needs_no_copies():
    ssa = toyir.parse(DIAMOND)
    out, copies = sreedhar_out_of_ssa(ssa)
    assert copies == 0
    assert toyir.show(out) == "# params: c\nB1:\n  br c B2 B3\nB2:\n  x.1 = 1\n  jump B4\nB3:\n  x.1 = 2\n  jump B4\nB4:\n  ret x.1\n"
    rng = random.Random(11)
    for k in range(40):
        prog = toyir.random_program(rng, 4, rng.randint(3, 6), acyclic=(k % 3 == 0))
        ssa = maximal_ssa(prog)
        assert is_conventional(ssa)
        out, copies = sreedhar_out_of_ssa(ssa)
        assert copies == 0
        for _ in range(3):
            args = [rng.randint(-3, 6), rng.randint(-3, 6)]
            assert toyir.run(out, args) == toyir.run(prog, args)


def test_result_is_conventional():
    transformed = 0
    for _, prog, ssa in tssa_programs(1, 60):
        transformed += not is_conventional(ssa)
        for method in (1, 3):
            cssa, _ = to_cssa(ssa, method)
            assert single_assignment(cssa)
            assert is_conventional(cssa)
    assert transformed > 20


def test_same_results_as_the_original_program():
    for rng, prog, ssa in tssa_programs(2, 80):
        out1, _ = sreedhar_out_of_ssa(ssa, method=1)
        out3, _ = sreedhar_out_of_ssa(ssa, method=3)
        for out in (out1, out3):
            assert not any(ins[0] == "phi" for b in out.blocks.values() for ins in b.instrs)
        for _ in range(4):
            args = [rng.randint(-3, 6), rng.randint(-3, 6)]
            want = toyir.run(prog, args)
            assert toyir.run(ssa, args) == want
            assert toyir.run(out1, args) == want
            assert toyir.run(out3, args) == want


def test_method_three_copies_at_most_method_one():
    fewer = 0
    for _, _, ssa in tssa_programs(3, 60):
        _, c1 = to_cssa(ssa, method=1)
        _, c3 = to_cssa(ssa, method=3)
        assert c1 == phi_operands(ssa)
        assert c3 <= c1
        fewer += c3 < c1
    assert fewer > 30


def test_rejects_bad_input():
    bad = [
        "B1:\n  jump B2\nB2:\n  y = 1\n  x = phi [B1: 1]\n  ret x\n",
        "# params: c\nB1:\n  br c B2 B3\nB2:\n  jump B3\nB3:\n  x = phi [B2: 1]\n  ret x\n",
    ]
    for text in bad:
        try:
            to_cssa(toyir.parse(text))
        except ValueError:
            continue
        assert False, text
    try:
        to_cssa(toyir.parse(DIAMOND), method=2)
    except ValueError:
        return
    assert False
