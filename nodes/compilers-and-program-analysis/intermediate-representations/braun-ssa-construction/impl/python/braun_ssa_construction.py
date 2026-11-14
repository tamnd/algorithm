# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/braun-ssa-construction/. The authors are listed in prov/T846M5.jsonl.
"""SSA construction by the method of Braun, Buchwald, Hack, Leissa, Mallon
and Zwinkau (2013): local value numbering in each block, a lookup in the
predecessors when a block reads a variable it has not assigned, and removal
of trivial phi-functions as soon as they appear. No dominance information is
used.

The input is a toy IR program without phi-functions, whose names contain no
dot. The blocks are filled in reverse postorder, and a block is sealed as soon
as all its predecessors are filled. A copy x = y stays an instruction; it is
not folded into the value of y.

The output names the k-th value of v as v.k; the numbers have gaps where a
phi-function was removed. A parameter keeps its own name. A read with no
reaching definition gets v.0, defined by v.0 = 0 at the top of the entry.
"""

import toyir
from toyir import Block, Program


class _Phi:
    def __init__(self, name, block, var):
        self.name = name
        self.block = block
        self.var = var
        self.ops = {}  # predecessor -> value name
        self.complete = False


class BraunBuilder:
    """The state of one construction. Values are names; a removed
    phi-function forwards to the value that replaced it."""

    def __init__(self, prog):
        for b in prog.blocks.values():
            for ins in b.instrs:
                if ins[0] == "phi":
                    raise ValueError("the input already has phi-functions")
                x = toyir.defs(ins)
                if x is not None and "." in x:
                    raise ValueError("names must not contain a dot: %r" % x)
        self.prog = prog
        self.preds = toyir.preds(prog)
        self.current_def = {}  # (variable, block) -> value name
        self.incomplete = {label: {} for label in prog.blocks}
        self.sealed = set()
        self.filled = set()
        self.phis = {}  # name -> _Phi, only the phi-functions still alive
        self.users = {}  # name -> set of phi names that use it
        self.forward = {}  # name of a removed phi -> the value that replaced it
        self.counter = {}
        self.undefined = []
        self.trivial_checks = 0

    # -------------------------------------------------------------- values

    def resolve(self, a):
        if not isinstance(a, str):
            return a
        path = []
        while a in self.forward:
            path.append(a)
            a = self.forward[a]
        for p in path:
            self.forward[p] = a
        return a

    def fresh(self, v):
        self.counter[v] = self.counter.get(v, 0) + 1
        return "%s.%d" % (v, self.counter[v])

    def undef(self, v):
        name = v + ".0"
        if name not in self.undefined:
            self.undefined.append(name)
        return name

    def new_phi(self, block, v):
        phi = _Phi(self.fresh(v), block, v)
        self.phis[phi.name] = phi
        return phi.name

    # ---------------------------------------------- Algorithms 1, 2, 3, 4

    def write_variable(self, v, block, value):
        self.current_def[(v, block)] = value  # @line L1

    def read_variable(self, v, block):
        if (v, block) in self.current_def:
            return self.resolve(self.current_def[(v, block)])  # @line L2
        return self.read_variable_recursive(v, block)  # @line L3

    def read_variable_recursive(self, v, block):
        if block not in self.sealed:
            val = self.new_phi(block, v)  # @line L4
            self.incomplete[block][v] = val
        elif len(self.preds[block]) == 1:
            val = self.read_variable(v, self.preds[block][0])  # @line L5
        else:
            val = self.new_phi(block, v)  # @line L6
            self.write_variable(v, block, val)
            val = self.add_phi_operands(v, val)  # @line L7
        self.write_variable(v, block, val)  # @line L8
        return val

    def add_phi_operands(self, v, name):
        phi = self.phis[name]
        for p in self.preds[phi.block]:
            op = self.read_variable(v, p)  # @line L9
            phi.ops[p] = op
            self.users.setdefault(op, set()).add(name)
        phi.complete = True
        return self.try_remove_trivial_phi(name)  # @line L10

    def try_remove_trivial_phi(self, name):
        phi = self.phis.get(name)
        if phi is None or not phi.complete:
            # Removed already, or its operands are still being collected; it
            # is checked when the last operand is in.
            return self.resolve(name)
        self.trivial_checks += 1
        same = None
        for op in phi.ops.values():
            op = self.resolve(op)
            if op == same or op == name:
                continue  # @line L11
            if same is not None:
                return name  # it merges two values: not trivial
            same = op
        if same is None:
            same = self.undef(phi.var)  # @line L12
        self.replace(name, same)  # @line L13
        return same

    def replace(self, name, value):
        """Reroute every use of the phi-function name to value, delete the
        phi-function, then recheck the phi-functions that used it."""
        users = self.users.pop(name, set()) - {name}
        del self.phis[name]
        self.forward[name] = value
        if isinstance(value, str):
            self.users.setdefault(value, set()).update(users)
        for u in users:
            self.try_remove_trivial_phi(u)  # @line L14

    def seal_block(self, block):
        for v, name in list(self.incomplete[block].items()):
            self.add_phi_operands(v, name)  # @line L15
        self.incomplete[block] = {}
        self.sealed.add(block)

    # ------------------------------------------------------ the CFG walk

    def fill_block(self, label):
        out = []
        for ins in self.prog.blocks[label].instrs:
            k = ins[0]
            if k == "const":
                ins2 = ("const", None, ins[2])
            elif k == "copy":
                ins2 = ("copy", None, self.operand(ins[2], label))
            elif k == "op":
                ins2 = ("op", None, ins[2], self.operand(ins[3], label), self.operand(ins[4], label))
            else:
                raise ValueError("unsupported instruction: %r" % (ins,))
            name = self.fresh(ins[1])
            self.write_variable(ins[1], label, name)
            out.append(ins2[:1] + (name,) + ins2[2:])
        t = self.prog.blocks[label].term
        if t[0] == "br":
            t = ("br", self.operand(t[1], label), t[2], t[3])
        elif t[0] == "ret":
            t = ("ret", self.operand(t[1], label))
        self.filled.add(label)
        return out, t

    def operand(self, a, label):
        return self.read_variable(a, label) if isinstance(a, str) else a

    def maybe_seal(self, label):
        if label not in self.sealed and all(p in self.filled for p in self.preds[label]):
            self.seal_block(label)

    def build(self, minimize_sccs=False):
        prog = self.prog
        root = prog.entry
        if self.preds[root]:
            raise ValueError("the entry block must have no predecessors")
        succ = {label: toyir.succs(prog, label) for label in prog.blocks}
        order = _reverse_postorder(succ, root)
        reach = set(order)  # unreachable blocks are dropped
        self.preds = {b: [p for p in ps if p in reach] for b, ps in self.preds.items()}
        for p in prog.params:
            self.write_variable(p, root, p)
        bodies = {}
        for label in order:  # @line L16
            self.maybe_seal(label)
            bodies[label] = self.fill_block(label)
            for s in succ[label]:
                self.maybe_seal(s)  # @line L17
        for label in order:
            self.maybe_seal(label)
        if minimize_sccs:
            remove_redundant_phis(self, list(self.phis))
        return self.assemble(bodies)

    def assemble(self, bodies):
        r = self.resolve
        by_block = {label: [] for label in bodies}
        for phi in self.phis.values():
            by_block[phi.block].append(phi)
        blocks = {}
        for label in self.prog.blocks:
            if label not in bodies:
                continue  # unreachable from the entry
            head = []
            for phi in sorted(by_block[label], key=lambda q: _version_key(q.name)):
                head.append(("phi", phi.name, {p: r(phi.ops[p]) for p in self.preds[label]}))
            instrs, t = bodies[label]
            body = []
            for ins in instrs:
                if ins[0] == "const":
                    body.append(ins)
                elif ins[0] == "copy":
                    body.append(("copy", ins[1], r(ins[2])))
                else:
                    body.append(("op", ins[1], ins[2], r(ins[3]), r(ins[4])))
            if t[0] == "br":
                t = ("br", r(t[1]), t[2], t[3])
            elif t[0] == "ret":
                t = ("ret", r(t[1]))
            if label == self.prog.entry:
                head = [("const", name, 0) for name in self.undefined] + head
            blocks[label] = Block(head + body, t)
        return Program(list(self.prog.params), blocks)


# ------------------------------------------------- Algorithm 5 (Section 3.2)


def remove_redundant_phis(builder, names):
    """Replace every strongly connected set of phi-functions that has only
    one value coming in from outside by that value."""
    names = [n for n in names if n in builder.phis]
    for scc in _phi_sccs(builder, names):  # @line L18
        _process_scc(builder, scc)


def _process_scc(builder, scc):
    scc = [n for n in scc if n in builder.phis]
    if len(scc) <= 1:
        return  # a single phi-function is handled by the trivial test
    members = set(scc)
    inner, outer = [], set()
    for n in scc:
        is_inner = True
        for op in builder.phis[n].ops.values():
            op = builder.resolve(op)
            if op not in members:
                outer.add(op)  # @line L19
                is_inner = False
        if is_inner:
            inner.append(n)
    if len(outer) == 1:
        value = outer.pop()
        for n in scc:
            if n in builder.phis:
                builder.replace(n, value)  # @line L20
    elif len(outer) > 1:
        remove_redundant_phis(builder, inner)  # @line L21


def _phi_sccs(builder, names):
    """Tarjan's algorithm on the graph phi -> operand phi, restricted to
    names. A component comes out after every component it reads from, so the
    operands are simplified first."""
    allowed = set(names)
    index, low, on_stack, stack, out = {}, {}, set(), [], []
    counter = [0]

    def edges(n):
        return [o for o in (builder.resolve(x) for x in builder.phis[n].ops.values()) if o in allowed]

    for start in names:
        if start in index:
            continue
        index[start] = low[start] = counter[0]
        counter[0] += 1
        stack.append(start)
        on_stack.add(start)
        work = [(start, iter(edges(start)))]
        while work:
            v, it = work[-1]
            w = next(it, None)
            if w is None:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        x = stack.pop()
                        on_stack.discard(x)
                        comp.append(x)
                        if x == v:
                            break
                    out.append(comp)
            elif w not in index:
                index[w] = low[w] = counter[0]
                counter[0] += 1
                stack.append(w)
                on_stack.add(w)
                work.append((w, iter(edges(w))))
            elif w in on_stack:
                low[v] = min(low[v], index[w])
    return out


# ------------------------------------------------------------------ helpers


def _reverse_postorder(succ, root):
    seen = {root}
    out = []
    stack = [(root, iter(succ[root]))]
    while stack:
        v, it = stack[-1]
        w = next(it, None)
        if w is None:
            stack.pop()
            out.append(v)
        elif w not in seen:
            seen.add(w)
            stack.append((w, iter(succ[w])))
    out.reverse()
    return out


def _version_key(name):
    base, _, k = name.rpartition(".")
    return (base, int(k))


def braun_ssa(prog, minimize_sccs=False):
    """Return a new program in SSA form with the same behaviour. With
    minimize_sccs, run the Section 3.2 pass that removes redundant cycles of
    phi-functions, which irreducible control flow can leave."""
    return BraunBuilder(prog).build(minimize_sccs)


def strip_versions(prog):
    """Out of SSA for the output of braun_ssa: drop the phi-functions and map
    each name v.k back to v. This is correct because copies are not folded,
    so no two versions of one variable are live at the same point."""
    def base(a):
        return a.split(".")[0] if isinstance(a, str) else a

    blocks = {}
    for label, b in prog.blocks.items():
        instrs = []
        for ins in b.instrs:
            if ins[0] == "phi":
                continue
            if ins[0] == "const":
                instrs.append(("const", base(ins[1]), ins[2]))
            elif ins[0] == "copy":
                instrs.append(("copy", base(ins[1]), base(ins[2])))
            else:
                instrs.append(("op", base(ins[1]), ins[2], base(ins[3]), base(ins[4])))
        t = b.term
        if t[0] == "br":
            t = ("br", base(t[1]), t[2], t[3])
        elif t[0] == "ret":
            t = ("ret", base(t[1]))
        blocks[label] = Block(instrs, t)
    return Program(list(prog.params), blocks)
