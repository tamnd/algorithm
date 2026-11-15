# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/copy-propagation/. The authors are listed in prov/3N51WA.jsonl.
"""Copy propagation on the toy IR, for programs that are not in SSA form.

available_copies(prog) solves the forward must problem of available copies
and returns the sets on entry to each block. propagate(prog) replaces each
use of a name u by y when the copy u = y is available at the use, following
chains of copies, and returns (new program, number of uses replaced).
remove_dead_copies(prog) deletes the copies whose destination is dead.
copy_propagation(prog) repeats propagate until a round changes nothing, then
removes dead copies. Programs with phi-functions are rejected: in SSA form
every copy can be propagated without any analysis.
"""

import toyir


def _check(prog):
    for blk in prog.blocks.values():
        for ins in blk.instrs:
            if ins[0] == "phi":
                raise ValueError("copy propagation here works on programs without phi-functions")


def address_taken(prog):
    """The names whose address is taken by an addr instruction. A store or a
    call may change them, and a load or a call may read them."""
    return {ins[2] for blk in prog.blocks.values() for ins in blk.instrs if ins[0] == "addr"}


def _is_copy(ins):
    return ins[0] == "copy" and isinstance(ins[2], str) and ins[2] != ins[1]


def transfer(ins, s, taken):
    """The available copies after ins, given the set s before it."""
    if ins[0] in ("store", "call") and taken:  # @line L19
        s = {(x, y) for (x, y) in s if x not in taken and y not in taken}
    d = toyir.defs(ins)
    if d is not None:  # @line L20
        s = {(x, y) for (x, y) in s if x != d and y != d}
    if _is_copy(ins):  # @line L21
        s = s | {(ins[1], ins[2])}
    return s  # @line L22


def _rpo(prog):
    seen = {prog.entry}
    post = []
    stack = [(prog.entry, iter(toyir.succs(prog, prog.entry)))]
    while stack:
        v, it = stack[-1]
        w = next(it, None)
        if w is None:
            post.append(v)
            stack.pop()
        elif w not in seen:
            seen.add(w)
            stack.append((w, iter(toyir.succs(prog, w))))
    return post[::-1]


def available_copies(prog):
    _check(prog)
    taken = address_taken(prog)
    universe = set()
    for blk in prog.blocks.values():  # @line L14
        for ins in blk.instrs:
            if _is_copy(ins):
                universe.add((ins[1], ins[2]))
    pred = toyir.preds(prog)
    order = _rpo(prog)
    out = {b: set(universe) for b in prog.blocks}  # @line L15
    # A block that the entry does not reach never runs: no copy needs to be
    # available there, and its OUT stays at the top value, the full set.
    inn = {b: set() for b in prog.blocks}
    changed = True
    while changed:  # @line L16
        changed = False
        for b in order:
            if b == prog.entry:  # @line L17
                s = set()
            else:
                s = set(universe)
                for p in pred[b]:
                    s &= out[p]
            inn[b] = s
            for ins in prog.blocks[b].instrs:  # @line L18
                s = transfer(ins, s, taken)
            if s != out[b]:
                out[b] = s
                changed = True
    return inn


def _resolve(a, s):
    """Follow the available copies from name a. The available copies at a
    point never form a cycle, so this ends."""
    if not isinstance(a, str):
        return a
    src = dict(s)
    while a in src:  # @line L8
        a = src[a]
    return a


def _rewrite(ins, s):
    k = ins[0]
    r = lambda a: _resolve(a, s)
    if k == "copy":
        return ("copy", ins[1], r(ins[2]))
    if k == "op":
        return ("op", ins[1], ins[2], r(ins[3]), r(ins[4]))
    if k == "load":
        return ("load", ins[1], r(ins[2]))
    if k == "store":
        return ("store", r(ins[1]), r(ins[2]))
    if k == "call":
        return ("call", ins[1], ins[2], [r(a) for a in ins[3]])
    return ins


def _rewrite_term(t, s):
    if t[0] == "br":
        return ("br", _resolve(t[1], s), t[2], t[3])
    if t[0] == "ret":
        return ("ret", _resolve(t[1], s))
    return t


def propagate(prog):
    """One round: analyse, then rewrite every use. Returns (program, count)."""
    inn = available_copies(prog)  # @line L2
    taken = address_taken(prog)
    blocks = {}
    count = 0  # @line L3
    for b, blk in prog.blocks.items():  # @line L4
        s = inn[b]  # @line L5
        new = []
        for ins in blk.instrs:  # @line L6
            ins2 = _rewrite(ins, s)  # @line L7
            if ins2 != ins:  # @line L9
                count += 1
            new.append(ins2)
            s = transfer(ins2, s, taken)  # @line L10
        term = _rewrite_term(blk.term, s)
        if term != blk.term:
            count += 1
        blocks[b] = toyir.Block(new, term)
    return toyir.Program(list(prog.params), blocks), count


def live_out(prog):
    """Live variable analysis: the names live at the end of each block."""
    uses, defs = {}, {}
    for b, blk in prog.blocks.items():
        u, d = set(), set()
        for ins in blk.instrs:
            for a in toyir.uses(ins):
                if a not in d:
                    u.add(a)
            x = toyir.defs(ins)
            if x is not None:
                d.add(x)
        for a in toyir.term_uses(blk.term):
            if a not in d:
                u.add(a)
        uses[b], defs[b] = u, d
    lin = {b: set() for b in prog.blocks}
    lout = {b: set() for b in prog.blocks}
    changed = True
    while changed:
        changed = False
        for b in reversed(list(prog.blocks)):
            o = set()
            for w in toyir.succs(prog, b):
                o |= lin[w]
            i = uses[b] | (o - defs[b])
            if o != lout[b] or i != lin[b]:
                lout[b], lin[b] = o, i
                changed = True
    return lout


def remove_dead_copies(prog):
    """Delete the copies x = y with x dead after them, and x = x, until none
    is left. Copies to an address-taken name are kept, because a load or a
    call may read them through a pointer."""
    _check(prog)
    taken = address_taken(prog)
    blocks = {b: toyir.Block(list(blk.instrs), blk.term) for b, blk in prog.blocks.items()}
    prog = toyir.Program(list(prog.params), blocks)
    while True:
        lout = live_out(prog)
        removed = 0
        for b, blk in prog.blocks.items():
            live = set(lout[b]) | set(toyir.term_uses(blk.term))
            keep = []
            for ins in reversed(blk.instrs):
                x = toyir.defs(ins)
                dead_copy = ins[0] == "copy" and x not in taken and (x not in live or ins[2] == x)
                if dead_copy:
                    removed += 1
                    continue
                keep.append(ins)
                if x is not None:
                    live.discard(x)
                live |= set(toyir.uses(ins))
            blk.instrs = keep[::-1]
        if not removed:
            return prog


def copy_propagation(prog, max_rounds=None):
    """Propagate until a round changes nothing (at most max_rounds rounds,
    by default one more than the number of instructions), then remove the
    dead copies. Returns (program, number of rounds)."""
    if max_rounds is None:
        max_rounds = 1 + sum(len(blk.instrs) + 1 for blk in prog.blocks.values())
    rounds = 0
    while rounds < max_rounds:  # @line L1
        prog, count = propagate(prog)
        rounds += 1
        if count == 0:  # @line L11
            break
    prog = remove_dead_copies(prog)  # @line L12
    return prog, rounds  # @line L13
