# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ssapre/. The authors are listed in prov/H6X0KK.jsonl.
"""SSAPRE (Chow, Chan, Kennedy, Liu, Lo and Tu) on the toy IR.

ssapre(prog) takes a program with const, copy and op instructions only. It
removes unreachable blocks, gives the entry no predecessor, and splits every
critical edge with a new block that only jumps. Then it gives each variable
SSA versions (minimal SSA, kept on the side; the program itself is not
rewritten into SSA form). An expression is the lexical triple (op, a, b) of
an op instruction. For each expression, the six steps of SSAPRE build a
sparse graph of its occurrences and decide where to compute it.

The output keeps one plain temporary t for each expression instead of the
SSA versions h1, h2, ... of the paper and their phis. The toy IR has
variables that can be assigned more than once, so this is the same program
that out-of-SSA translation would give, and t = e always stores the current
value of e.

plan(p) returns the occurrence graph of each expression of a normalized
program, so the tests and the page can look at the flags.
"""

import toyir


# ------------------------------------------------------------------- graph


def normalize(prog):
    """A copy of prog without unreachable blocks, with an entry that has no
    predecessor, and with every critical edge split. An edge A -> B is
    critical if A has two successors and B has two predecessors. The new
    block on the edge only jumps to B."""
    for blk in prog.blocks.values():
        for ins in blk.instrs:
            if ins[0] not in ("const", "copy", "op"):
                raise ValueError("ssapre handles const, copy and op only: %r" % (ins,))
    reach = {prog.entry}
    stack = [prog.entry]
    while stack:
        b = stack.pop()
        for s in toyir.succs(prog, b):
            if s not in reach:
                reach.add(s)
                stack.append(s)
    taken = set(prog.blocks)

    def fresh(base):
        name = base
        while name in taken:
            name += "_"
        taken.add(name)
        return name

    blocks = {}
    if any(prog.entry in toyir.succs(prog, b) for b in reach):
        blocks[fresh("start")] = toyir.Block([], ("jump", prog.entry))
    for label, blk in prog.blocks.items():
        if label in reach:
            blocks[label] = toyir.Block(list(blk.instrs), blk.term)
    p = toyir.Program(list(prog.params), blocks)
    npred = {b: len(ps) for b, ps in toyir.preds(p).items()}
    out = {}
    for label, blk in p.blocks.items():
        out[label] = blk
        t = blk.term
        if t[0] == "br" and t[2] != t[3]:
            targets = []
            for s in (t[2], t[3]):
                if npred[s] > 1:
                    mid = fresh(label + "_" + s)
                    out[mid] = toyir.Block([], ("jump", s))
                    targets.append(mid)
                else:
                    targets.append(s)
            blk.term = ("br", t[1], targets[0], targets[1])
    return toyir.Program(list(prog.params), out)


def expression(ins):
    """The expression (op, a, b) that an instruction computes, or None."""
    if ins is not None and ins[0] == "op":
        return (ins[2], ins[3], ins[4])
    return None


def names_of(prog):
    out = set(prog.params)
    for blk in prog.blocks.values():
        for ins in blk.instrs:
            out.add(ins[1])
            out.update(toyir.uses(ins))
        out.update(toyir.term_uses(blk.term))
    return out


def reverse_postorder(prog):
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


def dominators(prog):
    """The immediate dominator of each block and the children of each block
    in the dominator tree, by the iterative method of Cooper, Harvey and
    Kennedy. The entry is its own immediate dominator."""
    order = reverse_postorder(prog)
    num = {b: i for i, b in enumerate(order)}
    pred = toyir.preds(prog)
    idom = {order[0]: order[0]}

    def meet(x, y):
        while x != y:
            while num[x] > num[y]:
                x = idom[x]
            while num[y] > num[x]:
                y = idom[y]
        return x

    changed = True
    while changed:
        changed = False
        for b in order[1:]:
            new = None
            for p in pred[b]:
                if p in idom:
                    new = p if new is None else meet(p, new)
            if idom.get(b) != new:
                idom[b] = new
                changed = True
    children = {b: [] for b in order}
    for b in order[1:]:
        children[idom[b]].append(b)
    return idom, children


def frontiers(prog, idom):
    df = {b: set() for b in prog.blocks}
    for b, ps in toyir.preds(prog).items():
        if len(ps) >= 2:
            for p in ps:
                r = p
                while r != idom[b]:
                    df[r].add(b)
                    r = idom[r]
    return df


def iterated(df, start):
    """DF+ of a set of blocks."""
    out = set()
    work = list(start)
    while work:
        b = work.pop()
        for y in df[b]:
            if y not in out:
                out.add(y)
                work.append(y)
    return out


def variable_versions(prog, idom, children, df):
    """Minimal SSA for the variables, kept on the side. Returns phis, a dict
    from each variable to the set of blocks with a phi for it, and ver_in, a
    dict from each block to the version of every variable at its top, after
    its phis. A version is ("entry", v), ("phi", block, v) or
    ("def", block, i)."""
    names = sorted(names_of(prog))
    defs = {v: {prog.entry} for v in names}
    for b, blk in prog.blocks.items():
        for ins in blk.instrs:
            defs[ins[1]].add(b)
    phis = {v: iterated(df, defs[v]) for v in names}
    at = {b: [v for v in names if b in phis[v]] for b in prog.blocks}
    ver_in = {}
    todo = [(prog.entry, {v: ("entry", v) for v in names})]
    while todo:
        b, cur = todo.pop()
        cur = dict(cur)
        for v in at[b]:
            cur[v] = ("phi", b, v)
        ver_in[b] = dict(cur)
        for i, ins in enumerate(prog.blocks[b].instrs):
            cur[ins[1]] = ("def", b, i)
        for c in children[b]:
            todo.append((c, cur))
    return phis, ver_in


# ------------------------------------------------------- occurrence graph


class Phi:
    """A Φ for the expression at the top of a block."""

    def __init__(self, block, vers):
        self.block = block
        self.vers = vers  # the versions of the operands at the top of the block
        self.version = None
        self.ops = {}  # predecessor label -> Operand
        self.down_safe = True
        self.can_be_avail = True
        self.later = True

    @property
    def will_be_avail(self):
        return self.can_be_avail and not self.later  # @line L9


class Real:
    """A real occurrence x = a op b at node (block, index)."""

    def __init__(self, node, vers, version, defn):
        self.node = node
        self.vers = vers
        self.version = version
        self.defn = defn  # the occurrence on top of the stack with the same version, or None
        self.src = None  # the occurrence whose value this one uses
        self.save = False


class Operand:
    """The operand of a Φ that comes from one predecessor."""

    def __init__(self, defn, real):
        self.defn = defn  # None is ⊥
        self.real = real  # has_real_use
        self.insert = False


def rename(prog, e, phi_blocks, ver_in, children):
    """Give versions to the occurrences of e by a preorder walk of the
    dominator tree with a stack of occurrences. Returns the Φs (by block) and
    the real occurrences (in preorder)."""
    names = [x for x in e[1:]]
    tracked = {x for x in names if isinstance(x, str)}

    def key(cur):
        return tuple(cur[x] if isinstance(x, str) else x for x in names)

    phis = {b: Phi(b, key(ver_in[b])) for b in prog.blocks if b in phi_blocks}
    reals = []
    stack = []
    count = 0
    todo = [("enter", prog.entry)]
    while todo:
        item = todo.pop()
        if item[0] == "exit":
            del stack[item[1]:]
            continue
        b = item[1]
        todo.append(("exit", len(stack)))
        for c in reversed(children[b]):
            todo.append(("enter", c))
        cur = {x: ver_in[b][x] for x in tracked}
        if b in phis:
            f = phis[b]
            f.version = count
            count += 1
            stack.append(f)
        blk = prog.blocks[b]
        for i, ins in enumerate(blk.instrs):
            if expression(ins) == e:
                vs = key(cur)
                top = stack[-1] if stack else None
                if top is not None and top.vers == vs:
                    r = Real((b, i), vs, top.version, top)
                else:
                    if isinstance(top, Phi):
                        top.down_safe = False  # killed before a real use
                    r = Real((b, i), vs, count, None)
                    count += 1
                reals.append(r)
                stack.append(r)
            if ins[1] in tracked:
                cur[ins[1]] = ("def", b, i)
        vs = key(cur)
        top = stack[-1] if stack else None
        live = top is not None and top.vers == vs
        for s in toyir.succs(prog, b):
            if s in phis:
                if live:
                    phis[s].ops[b] = Operand(top, isinstance(top, Real))
                else:
                    phis[s].ops[b] = Operand(None, False)
                    if isinstance(top, Phi):
                        top.down_safe = False
        if blk.term[0] == "ret" and isinstance(top, Phi):
            top.down_safe = False  # reaches the exit without a real use
    return phis, reals


def users(phis):
    out = {id(f): [] for f in phis.values()}
    for f in phis.values():
        for o in f.ops.values():
            if isinstance(o.defn, Phi):
                out[id(o.defn)].append((f, o))
    return out


def down_safety(phis):
    work = [f for f in phis.values() if not f.down_safe]
    while work:
        f = work.pop()
        for o in f.ops.values():
            g = o.defn
            if isinstance(g, Phi) and not o.real and g.down_safe:
                g.down_safe = False
                work.append(g)


def can_be_avail(phis, use):
    def reset(g):
        g.can_be_avail = False
        for f, o in use[id(g)]:
            if not o.real and not f.down_safe and f.can_be_avail:
                reset(f)

    for f in phis.values():
        if not f.down_safe and f.can_be_avail and any(o.defn is None for o in f.ops.values()):
            reset(f)


def later(phis, use):
    def reset(g):
        g.later = False
        for f, _ in use[id(g)]:
            if f.later:
                reset(f)

    for f in phis.values():
        f.later = f.can_be_avail
    for f in phis.values():
        if f.later and any(o.defn is not None and o.real for o in f.ops.values()):
            reset(f)


def finalize(phis, reals):
    """Decide which real occurrences reload t, which save it, and which Φ
    operands need an insertion."""
    for r in reals:
        d = r.defn
        if d is None or (isinstance(d, Phi) and not d.will_be_avail):
            r.src = r
        elif isinstance(d, Real):
            r.src = d.src
        else:
            r.src = d
        if r.src is not r and isinstance(r.src, Real):
            r.src.save = True
    for f in phis.values():
        if not f.will_be_avail:
            continue
        for o in f.ops.values():
            if o.defn is None or (not o.real and not o.defn.will_be_avail):
                o.insert = True
            elif isinstance(o.defn, Real) and isinstance(o.defn.src, Real):
                o.defn.src.save = True


def plan(p):
    """The occurrence graph of each expression of a normalized program, as a
    list of (e, phis, reals) in the order of first occurrence."""
    idom, children = dominators(p)  # @line L2
    df = frontiers(p, idom)
    var_phis, ver_in = variable_versions(p, idom, children, df)
    exprs = []
    where = {}
    for b, blk in p.blocks.items():
        for ins in blk.instrs:
            e = expression(ins)
            if e is not None:
                if e not in where:
                    exprs.append(e)
                    where[e] = set()
                where[e].add(b)
    out = []
    for e in exprs:  # @line L3
        phi_blocks = iterated(df, where[e])  # @line L4
        for x in e[1:]:
            if isinstance(x, str):
                phi_blocks |= var_phis[x]
        phis, reals = rename(p, e, phi_blocks, ver_in, children)  # @line L5
        down_safety(phis)  # @line L6
        use = users(phis)
        can_be_avail(phis, use)  # @line L7
        later(phis, use)  # @line L8
        finalize(phis, reals)  # @line L10
        out.append((e, phis, reals))
    return out


# -------------------------------------------------------------- transform


def code_motion(p, plans):
    taken = names_of(p)
    action = {}
    insert = {b: [] for b in p.blocks}
    for k, (e, phis, reals) in enumerate(plans):  # @line L11
        name = "pre.%d" % k
        while name in taken:
            name += "_"
        taken.add(name)
        for r in reals:
            if r.src is not r:
                action[r.node] = ("reload", name)
            elif r.save:
                action[r.node] = ("save", name)
        for f in phis.values():
            for pred, o in f.ops.items():
                if o.insert:
                    insert[pred].append(("op", name, e[0], e[1], e[2]))
    blocks = {}
    for b, blk in p.blocks.items():
        instrs = []
        for i, ins in enumerate(blk.instrs):
            act = action.get((b, i))
            if act is None:
                instrs.append(ins)
            elif act[0] == "reload":
                instrs.append(("copy", ins[1], act[1]))
            else:
                instrs.append(("op", act[1], ins[2], ins[3], ins[4]))
                instrs.append(("copy", ins[1], act[1]))
        blocks[b] = toyir.Block(instrs + insert[b], blk.term)
    return toyir.Program(list(p.params), blocks)


def ssapre(prog):
    """SSAPRE. Returns the new program. Its blocks are the blocks of
    normalize(prog), with the same terminators."""
    p = normalize(prog)  # @line L1
    plans = plan(p)
    return code_motion(p, plans)  # @line L12
