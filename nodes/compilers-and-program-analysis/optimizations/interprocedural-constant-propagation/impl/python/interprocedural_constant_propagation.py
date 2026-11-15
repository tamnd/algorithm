# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interprocedural-constant-propagation/. The authors are listed in prov/D7W565.jsonl.
"""Interprocedural constant propagation with jump functions, on the toy IR.

A whole program is a dict from procedure name to toyir.Program. The
procedures may use const, copy, op and call instructions. Without memory
instructions, a callee cannot change a variable of its caller, so a local
analysis of each procedure is enough to describe its call sites.

Step 1 runs a forward constant analysis inside each procedure. A formal q
starts as the symbol ("formal", q), which stands for the value that q had
when the procedure was entered. The value of each argument at each call site
is the jump function of that argument: ("const", k), ("formal", q) or BOT.

Step 2 propagates values over the call graph with a worklist. VAL[f][p] is
TOP (no call seen yet), ("const", k) or BOT. The formals of the main
procedure start at BOT, all others at TOP.

Step 3 gives each procedure with a constant formal p = k a new entry block
that sets p = k and jumps to the old entry. Later local passes can then fold
the constant into the body.
"""

from collections import deque

import toyir

TOP = ("top",)
BOT = ("bot",)

ALLOWED = ("const", "copy", "op", "call")


def meet(a, b):
    """The meet of two lattice values: TOP is the identity, two equal
    values stay, and two different values give BOT."""
    if a == TOP:
        return b
    if b == TOP:
        return a
    return a if a == b else BOT


def check(procs, main):
    if main not in procs:
        raise ValueError("no procedure %r" % main)
    for f, prog in procs.items():
        for blk in prog.blocks.values():
            for ins in blk.instrs:
                if ins[0] not in ALLOWED:
                    raise ValueError("%s: instruction %r is not supported" % (f, ins[0]))
                if ins[0] == "call":
                    if ins[2] not in procs:
                        raise ValueError("%s calls an unknown procedure %r" % (f, ins[2]))
                    if len(ins[3]) != len(procs[ins[2]].params):
                        raise ValueError("%s calls %s with a wrong number of arguments" % (f, ins[2]))


# ------------------------------------------------------- the local analysis


def _value(state, a):
    if isinstance(a, int):
        return ("const", a)
    return state[a]


def _step(state, ins):
    k = ins[0]
    if k == "const":
        state[ins[1]] = ("const", ins[2])
    elif k == "copy":
        state[ins[1]] = _value(state, ins[2])
    elif k == "op":
        a, b = _value(state, ins[3]), _value(state, ins[4])
        if a[0] == "const" and b[0] == "const":
            try:
                state[ins[1]] = ("const", toyir._binop(ins[2], a[1], b[1]))
            except toyir._Trap:
                state[ins[1]] = BOT
        else:
            state[ins[1]] = BOT
    elif k == "call":
        state[ins[1]] = BOT
    else:
        raise ValueError("bad instruction: %r" % (ins,))


def _names(prog):
    out = set(prog.params)
    for blk in prog.blocks.values():
        for ins in blk.instrs:
            out.add(toyir.defs(ins))
            out.update(toyir.uses(ins))
        out.update(toyir.term_uses(blk.term))
    return out


def local_states(prog):
    """The state at the start of each block that the analysis reaches. A
    state maps each name to ("const", k), ("formal", q) or BOT. Every edge
    is taken as possible, so a block is reached when the CFG reaches it."""
    params = set(prog.params)
    start = {x: ("formal", x) if x in params else BOT for x in _names(prog)}
    state_in = {prog.entry: start}
    work = deque([prog.entry])
    queued = {prog.entry}
    while work:
        label = work.popleft()
        queued.discard(label)
        s = dict(state_in[label])
        for ins in prog.blocks[label].instrs:
            _step(s, ins)
        for t in toyir.succs(prog, label):
            if t not in state_in:
                new = dict(s)
            else:
                old = state_in[t]
                new = {x: meet(old[x], s[x]) for x in old}
                if new == old:
                    continue
            state_in[t] = new
            if t not in queued:
                work.append(t)
                queued.add(t)
    return state_in


def jump_functions(prog):
    """The call sites of prog in reached blocks, as tuples (label, index,
    callee, jumps), where jumps holds the jump function of each argument."""
    state_in = local_states(prog)
    sites = []
    for label, blk in prog.blocks.items():
        if label not in state_in:
            continue
        s = dict(state_in[label])
        for i, ins in enumerate(blk.instrs):
            if ins[0] == "call":
                sites.append((label, i, ins[2], [_value(s, a) for a in ins[3]]))
            _step(s, ins)
    return sites


def evaluate(jump, val_f):
    """The value of a jump function, given the values of the caller's formals."""
    if jump[0] == "formal":
        return val_f[jump[1]]
    return jump


# ------------------------------------------------------- the main algorithm


def _fresh_label(prog, base):
    label, k = base, 0
    while label in prog.blocks:
        k += 1
        label = "%s%d" % (base, k)
    return label


def specialize(prog, val_f):
    """A copy of prog that sets each constant formal at a new entry block."""
    consts = [(p, val_f[p][1]) for p in prog.params if val_f[p][0] == "const"]
    blocks = {}
    if consts:
        label = _fresh_label(prog, "ipcp.entry")
        blocks[label] = toyir.Block([("const", p, k) for p, k in consts], ("jump", prog.entry))
    for label, blk in prog.blocks.items():
        blocks[label] = toyir.Block([tuple(ins) for ins in blk.instrs], blk.term)
    return toyir.Program(list(prog.params), blocks)


def ipcp(procs, main="main"):
    """Returns (val, out). val[f][p] is TOP, ("const", k) or BOT for each
    formal p of each procedure f, and out is the transformed program."""
    check(procs, main)
    sites = {f: jump_functions(prog) for f, prog in procs.items()}  # @line L1
    val = {f: {p: TOP for p in prog.params} for f, prog in procs.items()}  # @line L2
    for p in procs[main].params:  # @line L3
        val[main][p] = BOT
    reached = {main}  # @line L4
    work = deque([main])
    queued = {main}
    while work:  # @line L5
        f = work.popleft()  # @line L6
        queued.discard(f)
        for _, _, g, jumps in sites[f]:  # @line L7
            if g not in reached:  # @line L8
                reached.add(g)
                if g not in queued:
                    work.append(g)
                    queued.add(g)
            for p, jump in zip(procs[g].params, jumps):  # @line L9
                v = evaluate(jump, val[f])  # @line L10
                new = meet(val[g][p], v)
                if new != val[g][p]:  # @line L11
                    val[g][p] = new
                    if g not in queued:
                        work.append(g)
                        queued.add(g)
    out = {f: specialize(prog, val[f]) for f, prog in procs.items()}  # @line L12
    return val, out  # @line L13


def show_value(v):
    if v == TOP:
        return "⊤"
    if v == BOT:
        return "⊥"
    if v[0] == "formal":
        return v[1]
    return str(v[1])
