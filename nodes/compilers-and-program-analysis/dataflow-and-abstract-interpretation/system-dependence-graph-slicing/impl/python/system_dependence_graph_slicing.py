# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/system-dependence-graph-slicing/. The authors are listed in prov/6EV9PV.jsonl.
"""Interprocedural slicing with the system dependence graph of Horwitz,
Reps and Binkley, with summary edges built by the method of Reps, Horwitz,
Sagiv and Rosay.

A system is a dict from procedure name to a toy IR Program; "main" is the
procedure where runs start. Procedures use x = k, x = y, x = a op b and
x = call f(a, b, ...), with jump, br and ret. Parameters are passed by
value and the only result of a call is the value of its ret. Recursion is
allowed; the tests use systems without it, so that they can compare with
inlining.

Nodes of the SDG are tuples:

    ("s", P, lab, i)        statement i of block lab of P (the terminator
                            when i == len(instrs)); for a call this is the
                            call node
    ("entry", P)            the entry node of P
    ("fin", P, k)           formal-in node of parameter k of P
    ("fout", P)             formal-out node: the value that P returns
    ("ain", P, lab, i, k)   actual-in node of argument k of a call site
    ("aout", P, lab, i)     actual-out node: the value the call site gets

build_sdg(system) returns the graph as a dict from node to a list of
(kind, parent) pairs, where kind is "control", "data", "call" (call node
to entry), "pin" (actual-in to formal-in), "pout" (formal-out to
actual-out) or "summary". sdg_slice(system, crit) returns the set of nodes
of the slice; statements_of maps that set to statements (P, lab, i).
"""

import toyir

ENTRY = "<entry>"
EXIT = "<exit>"


# --------------------------------------------- one procedure, as on the PDG page


def statements(prog):
    return [(lab, i) for lab, b in prog.blocks.items() for i in range(len(b.instrs) + 1)]


def stmt_succs(prog, node):
    lab, i = node
    if i < len(prog.blocks[lab].instrs):
        return [(lab, i + 1)]
    return [(s, 0) for s in toyir.succs(prog, lab)]


def DEF(prog, node):
    lab, i = node
    b = prog.blocks[lab]
    if i == len(b.instrs):
        return set()
    ins = b.instrs[i]
    if ins[0] not in ("const", "copy", "op", "call"):
        raise ValueError("unsupported instruction: %r" % (ins,))
    return {ins[1]}


def REF(prog, node):
    lab, i = node
    b = prog.blocks[lab]
    if i == len(b.instrs):
        return set(toyir.term_uses(b.term))
    return set(toyir.uses(b.instrs[i]))


def instr_at(prog, node):
    lab, i = node
    b = prog.blocks[lab]
    return b.instrs[i] if i < len(b.instrs) else None


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


def block_control_deps(prog, ip):
    """For each block, the branch blocks it is control dependent on, plus
    ENTRY for the blocks that every run of the procedure passes."""
    cd = {lab: set() for lab in prog.blocks}
    for a in prog.blocks:
        if prog.blocks[a].term[0] != "br":
            continue
        for b in toyir.succs(prog, a):
            y = b
            while y != ip[a]:
                cd[y].add(a)
                y = ip[y]
    y = prog.entry
    while y != EXIT:
        cd[y].add(ENTRY)
        y = ip[y]
    return cd


def reaching_definitions(prog):
    """IN set of every statement: pairs (d, x), with d a statement or ENTRY
    (for a parameter x)."""
    nodes = statements(prog)
    IN = {n: set() for n in nodes}
    IN[(prog.entry, 0)] = {(ENTRY, x) for x in prog.params}
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


# ------------------------------------------------------------------ the SDG


def call_sites(system):
    """Dict from procedure name to the list of call sites (P, lab, i)."""
    sites = {f: [] for f in system}
    for P, prog in system.items():
        for n in statements(prog):
            ins = instr_at(prog, n)
            if ins is not None and ins[0] == "call":
                if ins[2] not in system:
                    raise ValueError("unknown procedure %r" % ins[2])
                if len(ins[3]) != len(system[ins[2]].params):
                    raise ValueError("wrong number of arguments at %r" % ((P,) + n,))
                sites[ins[2]].append((P,) + n)
    return sites


def _def_node(P, prog, d, x):
    """The SDG node that stands for definition d of x."""
    if d == ENTRY:
        return ("fin", P, prog.params.index(x))
    ins = instr_at(prog, d)
    if ins[0] == "call":
        return ("aout", P) + d
    return ("s", P) + d


def build_sdg(system, summaries=True):
    """The SDG of the system: a dict from node to a list of (kind, parent)."""
    par = {}
    procs = {}

    def add(n, kind, m):
        par.setdefault(n, []).append((kind, m))

    for P, prog in system.items():
        ip = ipdom(prog)
        cd = block_control_deps(prog, ip)
        rd = reaching_definitions(prog)
        procs[P] = {"ipdom": ip, "rd": rd}
        entry = ("entry", P)
        par.setdefault(entry, [])
        for k in range(len(prog.params)):
            add(("fin", P, k), "control", entry)
        add(("fout", P), "control", entry)
        for n in statements(prog):
            node = ("s", P) + n
            par.setdefault(node, [])
            for a in cd[n[0]]:
                add(node, "control", entry if a == ENTRY else ("s", P, a, len(prog.blocks[a].instrs)))
            ins = instr_at(prog, n)
            if ins is not None and ins[0] == "call":
                for k, arg in enumerate(ins[3]):
                    ain = ("ain", P) + n + (k,)
                    add(ain, "control", node)
                    for (d, x) in rd[n]:
                        if x == arg:
                            add(ain, "data", _def_node(P, prog, d, x))
                add(("aout", P) + n, "control", node)
            else:
                refs = REF(prog, n)
                for (d, x) in rd[n]:
                    if x in refs:
                        add(node, "data", _def_node(P, prog, d, x))
                if ins is None and prog.blocks[n[0]].term[0] == "ret":
                    add(("fout", P), "data", node)
    for f, sites in call_sites(system).items():
        for (P, lab, i) in sites:
            add(("entry", f), "call", ("s", P, lab, i))
            for k in range(len(system[f].params)):
                add(("fin", f, k), "pin", ("ain", P, lab, i, k))
            add(("aout", P, lab, i), "pout", ("fout", f))
    if summaries:
        for (a, o) in summary_edges(system, par):
            add(o, "summary", a)
    return par


def summary_edges(system, par):
    """Pairs (actual-in, actual-out) such that a same-level realizable path
    runs from the matching formal-in to the formal-out of the callee. The
    work list holds path edges (v, w): w is the formal-out of the procedure
    of v and a same-level realizable path runs from v to w."""
    sites = call_sites(system)
    path = set()
    targets = {}  # v -> set of w with (v, w) in path
    work = []
    summary = set()
    sum_par = {}  # actual-out -> actual-ins with a summary edge to it

    def propagate(v, w):
        if (v, w) not in path:
            path.add((v, w))
            targets.setdefault(v, set()).add(w)
            work.append((v, w))

    for P in system:
        propagate(("fout", P), ("fout", P))  # @line L12
    while work:  # @line L13
        v, w = work.pop()  # @line L14
        if v[0] == "fin":  # @line L15
            Q, k = v[1], v[2]
            for (P, lab, i) in sites[Q]:  # @line L16
                a, o = ("ain", P, lab, i, k), ("aout", P, lab, i)
                if (a, o) not in summary:  # @line L17
                    summary.add((a, o))
                    sum_par.setdefault(o, []).append(a)
                    for x in list(targets.get(o, ())):
                        propagate(a, x)
        else:
            for kind, x in par.get(v, []):  # @line L18
                if kind in ("control", "data"):
                    propagate(x, w)
            for x in sum_par.get(v, []):
                propagate(x, w)
    return summary  # @line L19


# ------------------------------------------------------------------ slicing


def start_nodes(system, crit, sdg=None):
    """The parents of the criterion: the definitions of the names of V that
    reach the point, and the control parents of the statement there."""
    P, lab, i, V = crit
    prog = system[P]
    rd = reaching_definitions(prog)
    start = {_def_node(P, prog, d, x) for (d, x) in rd[(lab, i)] if x in V}
    if sdg is None:
        sdg = build_sdg(system)
    start |= {m for kind, m in sdg[("s", P, lab, i)] if kind == "control"}
    return start


def sdg_slice(system, crit, sdg=None):
    """The two passes of Horwitz, Reps and Binkley. crit is (P, lab, i, V):
    the values of V just before statement (lab, i) of procedure P, in every
    calling context."""
    if sdg is None:
        sdg = build_sdg(system)
    work = list(start_nodes(system, crit, sdg))  # @line L1
    S = set(work)
    while work:  # @line L2
        n = work.pop()  # @line L3
        for kind, m in sdg[n]:  # @line L4
            if kind != "pout" and m not in S:  # @line L5
                S.add(m)
                work.append(m)
    work = list(S)  # @line L6
    while work:  # @line L7
        n = work.pop()  # @line L8
        for kind, m in sdg[n]:  # @line L9
            if kind not in ("pin", "call") and m not in S:  # @line L10
                S.add(m)
                work.append(m)
    return S  # @line L11


def reachability_slice(system, crit, sdg=None):
    """Plain backward reachability over every edge but the summary edges.
    This ignores calling context and can be larger than sdg_slice."""
    if sdg is None:
        sdg = build_sdg(system)
    work = list(start_nodes(system, crit, sdg))
    S = set(work)
    while work:
        n = work.pop()
        for kind, m in sdg[n]:
            if kind != "summary" and m not in S:
                S.add(m)
                work.append(m)
    return S


def statements_of(S):
    """The statements (P, lab, i) among the nodes of S."""
    return {n[1:] for n in S if n[0] == "s"}
