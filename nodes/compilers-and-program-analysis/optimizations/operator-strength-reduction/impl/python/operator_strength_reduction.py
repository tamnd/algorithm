# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/operator-strength-reduction/. The authors are listed in prov/VGSWKK.jsonl.
"""Operator strength reduction on SSA form (Cooper, Simpson and Vick) for
the toy IR.

osr(prog) takes a program in strict SSA form: every name has one
definition, phi-functions stand at the tops of blocks, every use is
dominated by its definition, no name is address-taken, every block is
reachable and the entry block has no predecessor. It returns a new
program in which every candidate

    x = iv * rc,  x = rc * iv,  x = iv + rc,  x = rc + iv,  x = iv - rc

is a copy of a new induction variable that the loop updates by adds. iv is
an induction variable: a member of a strongly connected component (SCC) of
the SSA graph made only of phis, copies and adds or subtracts of region
constants. rc is a region constant for the loop: an integer, a parameter,
or a name whose definition lies in a block that strictly dominates the
header of the SCC.

After the reduction the pass rewrites comparisons of an induction variable
with a region constant into comparisons of a reduced one (linear function
test replacement), and deletes the instructions that no effect, branch or
return needs.

The toy IR has unbounded integers, so the identities that the rewrite uses
hold exactly. With fixed-width integers that wrap, the rewrite of the
candidates is still correct, but replacing a test with < or <= needs a
proof that no value in the new test wraps.
"""

import toyir

COMMUTATIVE = ("+", "*")
COMPARE = ("<", "<=", "==", "!=")


def may_trap(ins):
    """True if the operation can trap in the toy IR."""
    if ins[0] != "op":
        return False
    op, b = ins[2], ins[4]
    if op in ("/", "%"):
        return not (isinstance(b, int) and b != 0)
    if op in ("<<", ">>"):
        return not (isinstance(b, int) and 0 <= b <= 63)
    return False


def _copy_program(prog):
    blocks = {}
    for label, blk in prog.blocks.items():
        instrs = [(ins[0], ins[1], dict(ins[2])) if ins[0] == "phi" else ins for ins in blk.instrs]
        blocks[label] = toyir.Block(instrs, blk.term)
    return toyir.Program(list(prog.params), blocks)


class Dominators:
    """Immediate dominators by the iterative algorithm of Cooper, Harvey and
    Kennedy, with a reverse postorder of the blocks."""

    def __init__(self, prog):
        order, seen = [], {prog.entry}
        stack = [(prog.entry, iter(toyir.succs(prog, prog.entry)))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                order.append(v)
                stack.pop()
            elif w not in seen:
                seen.add(w)
                stack.append((w, iter(toyir.succs(prog, w))))
        missing = [b for b in prog.blocks if b not in seen]
        if missing:
            raise ValueError("block %r is unreachable" % missing[0])
        self.rpo = order[::-1]
        self.num = {b: i for i, b in enumerate(self.rpo)}
        post = {b: i for i, b in enumerate(order)}
        preds = toyir.preds(prog)
        idom = {prog.entry: prog.entry}

        def intersect(a, b):
            while a != b:
                while post[a] < post[b]:
                    a = idom[a]
                while post[b] < post[a]:
                    b = idom[b]
            return a

        changed = True
        while changed:
            changed = False
            for v in self.rpo[1:]:
                new = None
                for p in preds[v]:
                    if p in idom:
                        new = p if new is None else intersect(p, new)
                if idom.get(v) != new:
                    idom[v] = new
                    changed = True
        self.idom = idom
        self.depth = {}
        for v in self.rpo:
            self.depth[v] = 0 if v == prog.entry else self.depth[idom[v]] + 1

    def dominates(self, a, b):
        """True if block a dominates block b. None stands for the place
        before the entry, where the parameters are defined."""
        if a is None:
            return True
        if b is None:
            return False
        while self.depth[b] > self.depth[a]:
            b = self.idom[b]
        return a == b


def check_ssa(prog):
    """Raise ValueError unless prog is in strict SSA form with no
    address-taken names. Returns the Dominators and the defining block of
    each name (None for a parameter)."""
    dom = Dominators(prog)
    where = {p: None for p in prog.params}
    pos = {}
    for label, blk in prog.blocks.items():
        seen_other = False
        for i, ins in enumerate(blk.instrs):
            if ins[0] == "addr":
                raise ValueError("SSA names may not be address-taken: %s" % ins[2])
            if ins[0] == "phi":
                if seen_other:
                    raise ValueError("phi after a non-phi instruction in %r" % label)
            else:
                seen_other = True
            x = toyir.defs(ins)
            if x is None:
                continue
            if x in where:
                raise ValueError("name %r has two definitions" % x)
            where[x] = label
            pos[x] = i
    preds = toyir.preds(prog)
    if preds[prog.entry]:
        raise ValueError("the entry block has a predecessor")

    def check(a, label, i):
        if a not in where:
            raise ValueError("name %r is never defined" % a)
        d = where[a]
        if d == label and i is not None and pos[a] >= i:
            raise ValueError("use of %r before its definition in %r" % (a, label))
        if not dom.dominates(d, label):
            raise ValueError("use of %r in %r is not dominated by its definition" % (a, label))

    for label, blk in prog.blocks.items():
        for i, ins in enumerate(blk.instrs):
            if ins[0] == "phi":
                if set(ins[2]) != set(preds[label]):
                    raise ValueError("phi %s does not match the predecessors of %r" % (ins[1], label))
                for p, a in ins[2].items():
                    if isinstance(a, str):
                        check(a, p, None)
            else:
                for a in toyir.uses(ins):
                    check(a, label, i)
        for a in toyir.term_uses(blk.term):
            check(a, label, None)
    return dom, where


def ssa_sccs(prog, where):
    """The SCCs of the SSA graph by Tarjan's algorithm, without recursion.
    A node is a defined name, and its edges go to the defined names that its
    definition reads. An SCC comes out after every SCC it can reach, so the
    operands of a definition are always handled before it."""
    defn = {}
    for blk in prog.blocks.values():
        for ins in blk.instrs:
            x = toyir.defs(ins)
            if x is not None:
                defn[x] = ins
    succ = {x: [a for a in toyir.uses(ins) if where.get(a) is not None] for x, ins in defn.items()}
    index, low, on, st, out = {}, {}, set(), [], []
    counter = 0
    for root in defn:
        if root in index:
            continue
        index[root] = low[root] = counter
        counter += 1
        st.append(root)
        on.add(root)
        work = [(root, iter(succ[root]))]
        while work:
            v, it = work[-1]
            w = next(it, None)
            if w is not None:
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    st.append(w)
                    on.add(w)
                    work.append((w, iter(succ[w])))
                elif w in on:
                    low[v] = min(low[v], index[w])
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = st.pop()
                    on.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                out.append(comp)
    return out


class OSR:
    def __init__(self, prog):
        self.dom, self.where = check_ssa(prog)
        self.prog = _copy_program(prog)
        self.header = {}  # name -> header block of its induction variable, or None
        self.table = {}  # (op, o1, o2) -> name or int
        self.red = {}  # induction variable -> list of (op, rc, reduced name)
        self.used = set(self.where)
        self.counter = 0
        self.replaced = 0
        self.tests = 0

    # ----------------------------------------------------------- helpers

    def fresh(self):
        while True:
            self.counter += 1
            name = "osr%d" % self.counter
            if name not in self.used:
                self.used.add(name)
                return name

    def find(self, x):
        label = self.where[x]
        for i, ins in enumerate(self.prog.blocks[label].instrs):
            if toyir.defs(ins) == x:
                return label, i
        raise KeyError(x)

    def definition(self, x):
        label, i = self.find(x)
        return self.prog.blocks[label].instrs[i]

    def is_iv(self, o):
        return isinstance(o, str) and self.header.get(o) is not None

    def is_rc(self, o, h):
        """o is a region constant for the loop with header h."""
        if isinstance(o, int):
            return True
        d = self.where[o]
        return d is None or (d != h and self.dom.dominates(d, h))

    def candidate(self, ins):
        if ins[0] != "op" or ins[2] not in ("*", "+", "-"):
            return None
        op, a, b = ins[2], ins[3], ins[4]
        if self.is_iv(a) and self.is_rc(b, self.header[a]):
            return op, a, b
        if op in COMMUTATIVE and self.is_iv(b) and self.is_rc(a, self.header[b]):
            return op, b, a
        return None

    # ------------------------------------------------------- the algorithm

    def run(self):
        for comp in ssa_sccs(self.prog, self.where):  # @line L2
            if len(comp) > 1:  # @line L3
                self.classify(comp)
            else:
                n = comp[0]
                c = self.candidate(self.definition(n))
                if c is not None:  # @line L4
                    self.replace(n, *c)
                else:
                    self.header[n] = None  # @line L5
        self.replace_tests()  # @line L6
        self.dead_code()  # @line L7
        return self.prog

    def classify(self, comp):
        members = set(comp)
        h = min((self.where[n] for n in comp), key=self.dom.num.__getitem__)  # @line L8
        ok = True
        for n in comp:
            ins = self.definition(n)
            if not self.dom.dominates(h, self.where[n]):
                ok = False
            elif ins[0] == "phi":
                ok = ok and all(o in members or self.is_rc(o, h) for o in ins[2].values())
            elif ins[0] == "copy":
                ok = ok and ins[2] in members
            elif ins[0] == "op" and ins[2] in ("+", "-"):
                a, b = ins[3], ins[4]
                left = a in members and b not in members and self.is_rc(b, h)
                right = ins[2] == "+" and b in members and a not in members and self.is_rc(a, h)
                ok = ok and (left or right)
            else:
                ok = False
        if ok:  # @line L9
            for n in comp:
                self.header[n] = h  # @line L10
            return
        for n in comp:  # @line L11
            self.header[n] = None
        for n in comp:
            c = self.candidate(self.definition(n))
            if c is not None:  # @line L12
                self.replace(n, *c)

    def replace(self, n, op, iv, rc):
        result = self.reduce(op, iv, rc)  # @line L13
        label, i = self.find(n)
        self.prog.blocks[label].instrs[i] = ("copy", n, result)  # @line L14
        self.header[n] = self.header[iv]
        self.replaced += 1

    def reduce(self, op, iv, rc):
        key = (op, iv, rc)
        if key in self.table:  # @line L15
            return self.table[key]
        result = self.fresh()  # @line L16
        self.table[key] = result
        h = self.header[iv]
        self.header[result] = h
        self.red.setdefault(iv, []).append((op, rc, result))
        ins = self.definition(iv)  # @line L17
        is_phi = ins[0] == "phi"

        def operand(o):  # @line L18
            if isinstance(o, str) and self.header.get(o) == h:
                return self.reduce(op, o, rc)  # @line L19
            if op == "*" or is_phi:
                return self.apply(op, o, rc)  # @line L20
            return o

        if is_phi:
            new = ("phi", result, {p: operand(o) for p, o in ins[2].items()})
        elif ins[0] == "copy":
            new = ("copy", result, operand(ins[2]))
        else:
            new = ("op", result, ins[2], operand(ins[3]), operand(ins[4]))
        label, i = self.find(iv)
        self.prog.blocks[label].instrs.insert(i + 1, new)  # @line L21
        self.where[result] = label
        return result  # @line L22

    def apply(self, op, o1, o2):
        for key in [(op, o1, o2)] + ([(op, o2, o1)] if op in COMMUTATIVE else []):
            if key in self.table:  # @line L23
                return self.table[key]
        if self.is_iv(o1) and self.is_rc(o2, self.header[o1]):  # @line L24
            return self.reduce(op, o1, o2)
        if op in COMMUTATIVE and self.is_iv(o2) and self.is_rc(o1, self.header[o2]):  # @line L25
            return self.reduce(op, o2, o1)
        if isinstance(o1, int) and isinstance(o2, int):  # @line L26
            return toyir._binop(op, o1, o2)
        if op == "*" and (o1 == 0 or o2 == 0):
            return 0
        if (op == "*" and o1 == 1) or (op == "+" and o1 == 0):
            return o2
        if (op == "*" and o2 == 1) or (op in ("+", "-") and o2 == 0):
            return o1
        result = self.fresh()  # @line L27
        self.table[(op, o1, o2)] = result
        blocks = [self.where[o] for o in (o1, o2) if isinstance(o, str)]
        d = blocks[0]
        for b in blocks[1:]:
            if self.dom.dominates(d, b):
                d = b
            elif not self.dom.dominates(b, d):
                raise AssertionError("the operands of a region constant are not on one dominator chain")
        if d is None:
            d = self.prog.entry
        self.prog.blocks[d].instrs.append(("op", result, op, o1, o2))  # @line L28
        self.where[result] = d
        self.header[result] = None
        return result  # @line L29

    # ------------------------------------------ test replacement and cleanup

    def replace_tests(self):
        """Linear function test replacement: in x = a cmp b with a an
        induction variable and b a region constant for its header, follow
        the reductions of a while one keeps the comparison the same."""
        for label in list(self.prog.blocks):
            instrs = self.prog.blocks[label].instrs
            for i in range(len(instrs)):
                ins = instrs[i]
                if ins[0] != "op" or ins[2] not in COMPARE:
                    continue
                x, cmp, a, b = ins[1], ins[2], ins[3], ins[4]
                changed = False
                while True:
                    if self.is_iv(a) and self.is_rc(b, self.header[a]):
                        iv, other, iv_left = a, b, True
                    elif self.is_iv(b) and self.is_rc(a, self.header[b]):
                        iv, other, iv_left = b, a, False
                    else:
                        break
                    step = None
                    for op, rc, r in self.red.get(iv, []):
                        if op in ("+", "-"):
                            step = (op, rc, r, False)
                            break
                        if op == "*" and isinstance(rc, int) and rc != 0:
                            step = (op, rc, r, rc < 0 and cmp in ("<", "<="))
                            break
                    if step is None:
                        break
                    op, rc, r, swap = step
                    o = self.apply(op, other, rc)
                    a, b = (r, o) if iv_left else (o, r)
                    if swap:
                        a, b = b, a
                    changed = True
                if changed:
                    instrs[i] = ("op", x, cmp, a, b)
                    self.tests += 1

    def dead_code(self):
        """Delete the phis, copies, constants and operations that cannot trap
        and that nothing needed reads. Marking from the needed statements
        also removes dead cycles, such as an induction variable that only
        its own update reads."""

        def removable(ins):
            return ins[0] in ("const", "copy", "phi") or (ins[0] == "op" and not may_trap(ins))

        defn = {}
        live, work = set(), []
        for blk in self.prog.blocks.values():
            for ins in blk.instrs:
                x = toyir.defs(ins)
                if x is not None:
                    defn[x] = ins
                if not removable(ins):
                    work.extend(toyir.uses(ins))
            work.extend(toyir.term_uses(blk.term))
        while work:
            x = work.pop()
            if x in live or x not in defn:
                continue
            live.add(x)
            work.extend(toyir.uses(defn[x]))
        for blk in self.prog.blocks.values():
            blk.instrs = [ins for ins in blk.instrs if not removable(ins) or ins[1] in live]


def osr(prog, stats=None):
    """Operator strength reduction. Returns a new program. If stats is a
    dict, it receives the number of replaced candidates and replaced
    tests."""
    o = OSR(prog)  # @line L1
    out = o.run()
    if stats is not None:
        stats["replaced"] = o.replaced
        stats["tests"] = o.tests
    return out
