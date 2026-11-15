# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weiser-slicing/. The authors are listed in prov/S2FQ4Y.jsonl.
"""Weiser's slicing algorithm on the toy IR.

A statement is a pair (label, i): instruction i of block label, or the
terminator of the block when i == len(instrs). A slicing criterion is
(label, i, V): the values of the names in V at the point just before
statement (label, i).

weiser_slice(prog, crit) returns a dict with the slice S (a set of
statements), the relevant sets R, the branch set B and the number of rounds.
executable_slice(prog, crit) returns the slice as a runnable toy IR program,
and slice_point(prog, crit, S) gives the criterion point inside it.
observe(prog, args, point, names) runs a program and records the values of
names each time control reaches point.

The programs use only x = k, x = y and x = a op b, with the terminators jump,
br and ret, and every block must reach a ret.
"""

import toyir

EXIT = "<exit>"


# ------------------------------------------------------------ statements


def statements(prog):
    return [(lab, i) for lab, b in prog.blocks.items() for i in range(len(b.instrs) + 1)]


def stmt_succs(prog, node):
    lab, i = node
    b = prog.blocks[lab]
    if i < len(b.instrs):
        return [(lab, i + 1)]
    return [(s, 0) for s in toyir.succs(prog, lab)]


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


# ------------------------------------------------------- post-dominators


def postdominators(prog):
    """Post-dominator sets of the blocks, with a virtual EXIT after every
    ret, by the iterative set method."""
    labels = list(prog.blocks)
    succ = {lab: (toyir.succs(prog, lab) or [EXIT]) for lab in labels}
    reach = {EXIT}
    changed = True
    while changed:
        changed = False
        for lab in labels:
            if lab not in reach and any(s in reach for s in succ[lab]):
                reach.add(lab)
                changed = True
    if len(reach) != len(labels) + 1:
        raise ValueError("every block must reach a ret")
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
    return pdom


def ipdom(prog):
    """Immediate post-dominator of each block (EXIT for a ret block)."""
    pdom = postdominators(prog)
    out = {}
    for lab in prog.blocks:
        strict = pdom[lab] - {lab}
        # The immediate one is post-dominated by all the others.
        out[lab] = max(strict, key=lambda x: len(pdom[x]))
    return out


def influence(prog, lab, ip=None):
    """INFL of the branch ending block lab: the blocks reachable from its
    successors without passing through its immediate post-dominator."""
    if ip is None:
        ip = ipdom(prog)
    stop = ip[lab]
    seen = set()
    stack = [s for s in toyir.succs(prog, lab) if s != stop]
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        stack.extend(s for s in toyir.succs(prog, x) if s != stop and s not in seen)
    return seen


# --------------------------------------------------------------- slicing


def relevant_sets(prog, seeds):
    """Least solution of R(n) = seeds(n) together with, for each successor m,
    (R(m) - DEF(n)), plus REF(n) when DEF(n) meets R(m)."""
    nodes = statements(prog)
    R = {n: set(seeds.get(n, ())) for n in nodes}  # @line L13
    pred = {n: [] for n in nodes}
    for n in nodes:
        for m in stmt_succs(prog, n):
            pred[m].append(n)
    D = {n: DEF(prog, n) for n in nodes}
    U = {n: REF(prog, n) for n in nodes}
    work = list(nodes)  # @line L14
    while work:  # @line L15
        m = work.pop()  # @line L16
        for n in pred[m]:  # @line L17
            new = R[m] - D[n]  # @line L18
            if D[n] & R[m]:  # @line L19
                new |= U[n]
            if not new <= R[n]:  # @line L20
                R[n] |= new
                work.append(n)
    return R  # @line L21


def weiser_slice(prog, crit):
    lab, i, V = crit
    point = (lab, i)
    nodes = statements(prog)
    ip = ipdom(prog)  # @line L1
    branches = [(b, len(blk.instrs)) for b, blk in prog.blocks.items() if blk.term[0] == "br"]  # @line L2
    infl = {br: influence(prog, br[0], ip) for br in branches}  # @line L3
    B = set()  # @line L4
    rounds = 0
    while True:  # @line L5 L11
        rounds += 1
        seeds = {point: set(V)}  # @line L6
        for br in B:
            seeds.setdefault(br, set()).update(REF(prog, br))
        R = relevant_sets(prog, seeds)  # @line L7
        S = {n for n in nodes if any(DEF(prog, n) & R[m] for m in stmt_succs(prog, n))} | B  # @line L8
        hit = {x for (x, _) in S | {point}}
        newB = {br for br in branches if infl[br] & hit}  # @line L9
        if newB == B:  # @line L10
            return {"S": S, "R": R, "B": B, "rounds": rounds}  # @line L12
        B = newB


def executable_slice(prog, crit, result=None):
    """Delete the statements outside the slice. A branch outside the slice
    becomes a jump to its immediate post-dominator (or ret 0 when that is
    EXIT); jumps stay; a ret keeps its operand only if it is relevant."""
    if result is None:
        result = weiser_slice(prog, crit)
    S, R = result["S"], result["R"]
    ip = ipdom(prog)
    blocks = {}
    for lab, b in prog.blocks.items():
        n = len(b.instrs)
        instrs = [ins for i, ins in enumerate(b.instrs) if (lab, i) in S]
        t = b.term
        if t[0] == "br" and (lab, n) not in S:
            t = ("ret", 0) if ip[lab] == EXIT else ("jump", ip[lab])
        elif t[0] == "ret" and isinstance(t[1], str) and t[1] not in R[(lab, n)]:
            t = ("ret", 0)
        blocks[lab] = toyir.Block(instrs, t)
    return toyir.Program(list(prog.params), blocks)


def slice_point(prog, crit, S):
    """The criterion point in the executable slice."""
    lab, i, _ = crit
    return (lab, sum(1 for j in range(i) if (lab, j) in S))


# --------------------------------------------------------------- running


class _Trap(Exception):
    pass


def _binop(op, a, b):
    if op in ("/", "%"):
        if b == 0:
            raise _Trap()
        q = abs(a) // abs(b)
        if (a < 0) != (b < 0):
            q = -q
        return q if op == "/" else a - b * q
    if op in ("<<", ">>"):
        if b < 0 or b > 63:
            raise _Trap()
        return a << b if op == "<<" else a >> b
    return {
        "+": lambda: a + b, "-": lambda: a - b, "*": lambda: a * b,
        "&": lambda: a & b, "|": lambda: a | b, "^": lambda: a ^ b,
        "<": lambda: int(a < b), "<=": lambda: int(a <= b),
        "==": lambda: int(a == b), "!=": lambda: int(a != b),
    }[op]()


def observe(prog, args, point, names, fuel=10000):
    """Run prog like toyir.run. Return (outcome, obs), where obs has one
    tuple of the values of names (None if undefined) for each time control
    is about to run the statement at point."""
    env = dict(zip(prog.params, args))
    plab, pi = point
    obs = []

    def val(a):
        if isinstance(a, int):
            return a
        if a not in env:
            raise toyir.UndefinedName(a)
        return env[a]

    lab = prog.entry
    while True:
        b = prog.blocks[lab]
        n = len(b.instrs)
        for i in range(n + 1):
            if lab == plab and i == pi:
                obs.append(tuple(env.get(v) for v in names))
            if fuel <= 0:
                return ("fuel",), obs
            fuel -= 1
            if i == n:
                break
            ins = b.instrs[i]
            if ins[0] == "const":
                env[ins[1]] = ins[2]
            elif ins[0] == "copy":
                env[ins[1]] = val(ins[2])
            else:
                try:
                    env[ins[1]] = _binop(ins[2], val(ins[3]), val(ins[4]))
                except _Trap:
                    return ("trap",), obs
        t = b.term
        if t[0] == "jump":
            lab = t[1]
        elif t[0] == "br":
            lab = t[2] if val(t[1]) != 0 else t[3]
        else:
            return ("ret", val(t[1])), obs
