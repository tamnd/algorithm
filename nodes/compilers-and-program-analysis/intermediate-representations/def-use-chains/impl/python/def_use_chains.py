# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/def-use-chains/. The authors are listed in prov/XZ8C52.jsonl.
"""Def-use and use-def chains for a toy IR program.

A definition site is a tuple (label, i, x): instruction i of block label
defines the name x. A parameter x is the site (entry, -1, x): it is defined
on the way into the program, before the first instruction of the entry
block. A use site is (label, i, x): instruction i of block label reads x,
where i = len(instrs) stands for the terminator.

chains(prog) returns (du, ud). du maps every definition site to the sorted
list of use sites it reaches, and ud maps every use site to the sorted list
of definition sites that reach it. A definition d of x reaches a use u of x
if some path in the control flow graph goes from just after d to u and
does not define x again on the way. A phi operand that comes from the
predecessor p is used at the end of p. A store *p = a defines no name, so
names whose address is taken get incomplete chains (see the page).

reaching(prog) returns the sets IN and OUT of reaching definitions per
block, found by round-robin iteration in reverse postorder.
"""

import toyir


def _order(prog):
    """The labels in reverse postorder from the entry, then the labels that
    the entry does not reach, in program order."""
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
    rest = [lab for lab in prog.blocks if lab not in seen]
    return post[::-1] + rest


def reaching(prog):
    """Return (IN, OUT, passes): dicts from label to a frozenset of
    definition sites, and the number of passes of the iteration."""
    entry = prog.entry
    preds = toyir.preds(prog)
    gen = {}
    kill = {}
    for lab, block in prog.blocks.items():  # @line L1
        last = {}
        for i, ins in enumerate(block.instrs):
            x = toyir.defs(ins)
            if x is not None:
                last[x] = (lab, i, x)
        gen[lab] = frozenset(last.values())
        kill[lab] = frozenset(last)
    params = frozenset((entry, -1, x) for x in prog.params)
    out = {lab: gen[lab] for lab in prog.blocks}  # @line L2
    into = {}
    order = _order(prog)
    passes = 0
    changed = True
    while changed:  # @line L3
        changed = False
        passes += 1
        for lab in order:  # @line L4
            s = set(params) if lab == entry else set()  # @line L5
            for p in preds[lab]:
                s |= out[p]
            into[lab] = frozenset(s)
            new = gen[lab] | frozenset(d for d in s if d[2] not in kill[lab])  # @line L6
            if new != out[lab]:
                out[lab] = new
                changed = True  # @line L7
    return into, out, passes


def chains(prog):
    into, out, _ = reaching(prog)
    preds = toyir.preds(prog)
    du = {}
    ud = {}
    for x in prog.params:
        du[(prog.entry, -1, x)] = set()
    for lab, block in prog.blocks.items():
        for i, ins in enumerate(block.instrs):
            x = toyir.defs(ins)
            if x is not None:
                du[(lab, i, x)] = set()

    def link(defs, use):
        ud.setdefault(use, set()).update(defs)
        for d in defs:
            du[d].add(use)

    for lab, block in prog.blocks.items():  # @line L8
        live = {}
        for d in into[lab]:  # @line L9
            live.setdefault(d[2], set()).add(d)
        n = len(block.instrs)
        for i in range(n + 1):  # @line L10
            if i == n:
                for x in toyir.term_uses(block.term):
                    link(live.get(x, ()), (lab, i, x))
                break
            ins = block.instrs[i]
            if ins[0] == "phi":
                for p, a in ins[2].items():
                    if p not in preds[lab]:
                        raise ValueError("phi in %s names %r, which is not a predecessor" % (lab, p))
                    if isinstance(a, str):
                        link([d for d in out[p] if d[2] == a], (lab, i, a))
            else:
                for x in toyir.uses(ins):
                    link(live.get(x, ()), (lab, i, x))  # @line L11
            x = toyir.defs(ins)
            if x is not None:
                live[x] = {(lab, i, x)}  # @line L12
    du = {d: sorted(us) for d, us in du.items()}  # @line L13
    ud = {u: sorted(ds) for u, ds in ud.items()}
    return du, ud
