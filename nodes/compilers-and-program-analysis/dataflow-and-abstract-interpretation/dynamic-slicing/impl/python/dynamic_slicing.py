# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-slicing/. The authors are listed in prov/1V18D7.jsonl.
"""Dynamic slicing on the toy IR, computed forward while the program runs.

A statement is a pair (label, i): instruction i of block label, or the
terminator of the block when i == len(instrs). A dynamic slicing criterion
is (label, i, q, V) together with an input: the values of the names in V
just before the q-th time the run on that input reaches statement
(label, i).

During the run, DS[x] is the set of statements that the current value of x
depends on, the statement that wrote it included. An open branch instance
keeps the same kind of set. A statement instance depends on the last write
of each name it reads (dynamic data dependence) and on the most recent
branch instance whose immediate post-dominator block has not been entered
since that branch ran (dynamic control dependence).

The programs use only x = k, x = y and x = a op b, with the terminators
jump, br and ret, and every block must reach a ret.
"""

import toyir

EXIT = "<exit>"


def statements(prog):
    return [(lab, i) for lab, b in prog.blocks.items() for i in range(len(b.instrs) + 1)]


def DEF(prog, node):
    lab, i = node
    b = prog.blocks[lab]
    if i == len(b.instrs):
        return set()
    ins = b.instrs[i]
    if ins[0] not in ("const", "copy", "op"):
        raise ValueError("unsupported instruction: %r" % (ins,))
    return {ins[1]}


def REF(prog, node):
    lab, i = node
    b = prog.blocks[lab]
    if i == len(b.instrs):
        return set(toyir.term_uses(b.term))
    return set(toyir.uses(b.instrs[i]))


def ipdom(prog):
    """Immediate post-dominator of each block, with a virtual EXIT after
    every ret."""
    labels = list(prog.blocks)
    succ = {lab: (toyir.succs(prog, lab) or [EXIT]) for lab in labels}
    full = set(labels) | {EXIT}
    pdom = {lab: set(full) for lab in labels}
    pdom[EXIT] = {EXIT}
    changed = True
    while changed:
        changed = False
        for lab in reversed(labels):
            new = {lab} | set.intersection(*(pdom[s] for s in succ[lab]))
            if new != pdom[lab]:
                pdom[lab] = new
                changed = True
    if any(EXIT not in pdom[lab] for lab in labels):
        raise ValueError("every block must reach a ret")
    return {lab: max(pdom[lab] - {lab}, key=lambda x: len(pdom[x])) for lab in labels}


def _value(env, a):
    return a if isinstance(a, int) else env[a]


def dynamic_slice(prog, args, crit, fuel=10000, ip=None):
    """The dynamic slice for criterion crit = (label, i, q, V) on the run of
    prog on args: a set of statements. Returns None if the run stops (ret,
    trap or no fuel left) before it reaches (label, i) for the q-th time."""
    plab, pi, q, V = crit
    if ip is None:
        ip = ipdom(prog)
    env = dict(zip(prog.params, args))
    empty = frozenset()
    DS = {x: empty for x in prog.params}  # @line L1
    open_br = []  # (block, its ipdom, slice of the branch instance)
    seen = 0
    lab = prog.entry
    while True:
        b = prog.blocks[lab]
        n = len(b.instrs)
        for i in range(n + 1):  # @line L2
            fuel -= 1
            if fuel < 0:
                return None
            C = open_br[-1][2] if open_br else empty  # @line L3
            if (lab, i) == (plab, pi):
                seen += 1
                if seen == q:  # @line L4
                    return set(C.union(*(DS.get(x, empty) for x in V)))  # @line L5
            node = (lab, i)
            T = C.union(*(DS[y] for y in REF(prog, node))) | {node}  # @line L6
            if i < n:
                ins = b.instrs[i]
                if ins[0] == "const":
                    v = ins[2]
                elif ins[0] == "copy":
                    v = _value(env, ins[2])
                elif ins[0] == "op":
                    try:
                        v = toyir._binop(ins[2], _value(env, ins[3]), _value(env, ins[4]))
                    except toyir._Trap:
                        return None
                else:
                    raise ValueError("unsupported instruction: %r" % (ins,))
                env[ins[1]] = v
                DS[ins[1]] = T  # @line L7
                continue
            t = b.term
            if t[0] == "ret":
                return None
            if t[0] == "br":
                nxt = t[2] if _value(env, t[1]) != 0 else t[3]
                open_br = [e for e in open_br if e[0] != lab]  # @line L8
                open_br.append((lab, ip[lab], T))
            else:
                nxt = t[1]
            open_br = [e for e in open_br if e[1] != nxt]  # @line L9
            lab = nxt
