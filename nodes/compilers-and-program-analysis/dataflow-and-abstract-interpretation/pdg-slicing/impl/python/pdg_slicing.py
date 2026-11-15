# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pdg-slicing/. The authors are listed in prov/8QKCJ8.jsonl.
"""Slicing by backward reachability in the program dependence graph.

A statement is a pair (label, i): instruction i of block label, or the
terminator of the block when i == len(instrs). A slicing criterion is
(label, i, V): the values of the names in V at the point just before
statement (label, i).

build_pdg(prog) returns the control and data parents of every statement.
The node ENTRY stands for the start of the program and for the definitions
of the parameters. pdg_slice(prog, crit) returns the set of statements that
reach the criterion in the graph. executable_slice turns that set into a
runnable toy IR program, and observe runs a program and records the values
of some names each time control reaches a point.

The programs use only x = k, x = y and x = a op b, with the terminators jump,
br and ret, and every block must reach a ret.
"""

import toyir

ENTRY = "<entry>"
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


def terminator(prog, lab):
    return (lab, len(prog.blocks[lab].instrs))


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
    return {lab: max(pdom[lab] - {lab}, key=lambda x: len(pdom[x])) for lab in prog.blocks}


# -------------------------------------------------------------- the PDG


def block_control_deps(prog, ip=None):
    """For each block, the blocks whose branch it is control dependent on,
    plus ENTRY for the blocks that run on every run. This is the walk of
    Ferrante, Ottenstein and Warren up the post-dominator tree."""
    if ip is None:
        ip = ipdom(prog)
    cd = {lab: set() for lab in prog.blocks}
    for a in prog.blocks:
        if prog.blocks[a].term[0] != "br":
            continue
        for b in toyir.succs(prog, a):
            y = b
            while y != ip[a]:
                cd[y].add(a)
                y = ip[y]
    # The edges START -> entry and START -> EXIT: ipdom(START) is EXIT.
    y = prog.entry
    while y != EXIT:
        cd[y].add(ENTRY)
        y = ip[y]
    return cd


def reaching_definitions(prog):
    """IN set of every statement: pairs (d, x) where d is a statement that
    defines x, or ENTRY for a parameter x, and some path from just after d
    reaches the statement with no other definition of x."""
    nodes = statements(prog)
    IN = {n: set() for n in nodes}
    first = (prog.entry, 0)
    IN[first] = {(ENTRY, x) for x in prog.params}
    work = list(nodes)
    while work:
        n = work.pop()
        d = DEF(prog, n)
        out = {(s, x) for (s, x) in IN[n] if x not in d} | {(n, x) for x in d}
        for m in stmt_succs(prog, n):
            if not out <= IN[m]:
                IN[m] |= out
                work.append(m)
    return IN


def build_pdg(prog):
    """Control parents and data parents of every statement."""
    ip = ipdom(prog)
    cd = block_control_deps(prog, ip)
    rd = reaching_definitions(prog)
    control, data = {}, {}
    for n in statements(prog):
        control[n] = {a if a == ENTRY else terminator(prog, a) for a in cd[n[0]]}
        data[n] = {(s, x) for (s, x) in rd[n] if x in REF(prog, n)}
    return {"control": control, "data": data, "rd": rd, "ipdom": ip}


def parents(pdg, n):
    return pdg["control"][n] | {s for (s, _) in pdg["data"][n]}


# -------------------------------------------------------------- slicing


def pdg_slice(prog, crit, pdg=None):
    """The statements that reach the criterion in the PDG. The criterion
    acts as a node at the point p that reads the names of V."""
    if pdg is None:
        pdg = build_pdg(prog)  # @line L1
    lab, i, V = crit
    p = (lab, i)
    start = {s for (s, x) in pdg["rd"][p] if x in V}  # @line L2
    start |= pdg["control"][p]  # @line L3
    start.discard(ENTRY)
    S = set(start)  # @line L4
    work = list(start)
    while work:  # @line L5
        z = work.pop()  # @line L6
        for x in parents(pdg, z):  # @line L7
            if x != ENTRY and x not in S:  # @line L8
                S.add(x)
                work.append(x)
    return S  # @line L9


def executable_slice(prog, crit, S, ip=None):
    """The projection of the program on S: instructions outside S are
    deleted, a branch outside S becomes a jump to its immediate
    post-dominator (or ret 0 when that is EXIT), jumps stay, and a ret keeps
    its operand only at the criterion point for a name of V."""
    if ip is None:
        ip = ipdom(prog)
    plab, pi, V = crit
    blocks = {}
    for lab, b in prog.blocks.items():
        n = len(b.instrs)
        instrs = [ins for i, ins in enumerate(b.instrs) if (lab, i) in S]
        t = b.term
        if t[0] == "br" and (lab, n) not in S:
            t = ("ret", 0) if ip[lab] == EXIT else ("jump", ip[lab])
        elif t[0] == "ret" and isinstance(t[1], str) and not ((lab, n) == (plab, pi) and t[1] in V):
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
