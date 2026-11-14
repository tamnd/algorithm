# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sreedhar-cssa-translation/. The authors are listed in prov/N0QEY1.jsonl.
"""Translation out of SSA form by Sreedhar, Ju, Gillies and Santhanam (1999).

The input is a strict SSA program in the toy IR. Phi-functions come first in
each block and have one operand for each predecessor. Method I puts a copy on
every resource of every phi-function. Method III uses liveness and
interference to copy only the resources that need it. Both give conventional
SSA form: no two names in one phi congruence class interfere. Then each class
gets one variable and the phi-functions are dropped. No edge is split.

A phi-function reads its operand for the predecessor p at the end of p, so
that operand is live out of p. A copy for the operand from p goes at the end
of p, before the terminator. A copy for the target goes right after the
phi-functions of its block. Two names interfere when one is live just after
the definition of the other. Liveness and interference are computed again
for each phi-function; the paper updates them in place instead.

The four cases of Method III look only at pairs of resources whose classes
interfere already. A copy gives a resource a new name, and that name can
interfere with the class of a resource that was left alone. So a closing
step also copies every resource whose class is live where a copied resource
gets its new name. Constant operands always get a copy.
"""

import toyir
from toyir import Block, Program


class Classes:
    """Union-find over names. The sets are the phi congruence classes."""

    def __init__(self):
        self.parent = {}
        self.members = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.members[x] = {x}
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        return root

    def of(self, x):
        return self.members[self.find(x)]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra
            self.members[ra] |= self.members.pop(rb)


class _State:
    """The program while copies go in: phi-functions, body and terminator
    of each block, kept apart."""

    def __init__(self, prog):
        pred = toyir.preds(prog)
        self.params = list(prog.params)
        self.order = list(prog.blocks)
        self.phis, self.body, self.top, self.term, self.succ = {}, {}, {}, {}, {}
        self.names = set(prog.params)
        for label, b in prog.blocks.items():
            k = 0
            while k < len(b.instrs) and b.instrs[k][0] == "phi":
                k += 1
            for ins in b.instrs:
                if ins[0] not in ("phi", "const", "copy", "op"):
                    raise ValueError("unsupported instruction %r" % (ins,))
                self.names.add(ins[1])
            if any(ins[0] == "phi" for ins in b.instrs[k:]):
                raise ValueError("phi after a non-phi instruction in %s" % label)
            for ins in b.instrs[:k]:
                if set(ins[2]) != set(pred[label]):
                    raise ValueError("phi %s needs one operand per predecessor" % ins[1])
            self.phis[label] = [[ins[1], dict(ins[2])] for ins in b.instrs[:k]]
            self.body[label] = list(b.instrs[k:])
            self.top[label] = 0  # copies for targets placed so far
            self.term[label] = b.term
            self.succ[label] = toyir.succs(prog, label)
        self.serial = 0
        self.copies = 0

    def fresh(self, base):
        while True:
            self.serial += 1
            name = "%s_%d" % (base, self.serial)
            if name not in self.names:
                self.names.add(name)
                return name

    def slots(self, label, k):
        """The resources of the k-th phi of label: (None, target) first, then
        (pred, operand) for each predecessor."""
        dest, ops = self.phis[label][k]
        return [(None, dest)] + list(ops.items())

    def program(self):
        blocks = {}
        for label in self.order:
            phis = [("phi", d, dict(ops)) for d, ops in self.phis[label]]
            blocks[label] = Block(phis + list(self.body[label]), self.term[label])
        return Program(list(self.params), blocks)


def liveness(st):
    """live_out[b], and after[b]: the names live just after the phis of b."""
    up, kill = {}, {}
    for b in st.order:
        u, d = set(), set()
        for ins in st.body[b]:
            u |= {a for a in toyir.uses(ins) if a not in d}
            d.add(ins[1])
        u |= {a for a in toyir.term_uses(st.term[b]) if a not in d}
        up[b], kill[b] = u, d
    live_in = {b: set() for b in st.order}
    live_out = {b: set() for b in st.order}
    after = {b: set() for b in st.order}
    changed = True
    while changed:
        changed = False
        for b in reversed(st.order):
            out = set()
            for s in st.succ[b]:
                out |= live_in[s]
                out |= {ops[b] for _, ops in st.phis[s] if isinstance(ops[b], str)}
            aft = up[b] | (out - kill[b])
            inn = aft - {d for d, _ in st.phis[b]}
            if out != live_out[b] or inn != live_in[b]:
                changed = True
            live_out[b], after[b], live_in[b] = out, aft, inn
    return live_out, after


def interference(st, live_out, after):
    """Name -> the names that interfere with it."""
    g = {}

    def add(a, b):
        if a != b:
            g.setdefault(a, set()).add(b)
            g.setdefault(b, set()).add(a)

    for b in st.order:
        live = set(live_out[b]) | set(toyir.term_uses(st.term[b]))
        for ins in reversed(st.body[b]):
            for x in live:
                add(ins[1], x)
            live.discard(ins[1])
            live |= set(toyir.uses(ins))
        for d, _ in st.phis[b]:
            for x in live:
                add(d, x)
    for p in st.params:
        for x in after[st.order[0]]:
            add(p, x)
    return g


def _classes_interfere(a, b, g):
    return any(g.get(u, set()) & b for u in a)


def _insert(st, label, k, chosen):
    """Put a copy on each chosen resource of the k-th phi of label."""
    phi = st.phis[label][k]
    for i, (p, r) in enumerate(st.slots(label, k)):
        if i not in chosen:
            continue
        if p is None:
            new = st.fresh(r)
            st.body[label].insert(st.top[label], ("copy", r, new))
            st.top[label] += 1
            phi[0] = new
        else:
            new = st.fresh(r if isinstance(r, str) else "k")
            st.body[p].append(("const", new, r) if isinstance(r, int) else ("copy", new, r))
            phi[1][p] = new
        st.copies += 1


def _choose(st, label, k, classes):
    """Method III: the resources of one phi-function that need a copy."""
    live_out, after = liveness(st)  # @line L3
    g = interference(st, live_out, after)
    slots = st.slots(label, k)
    n = len(slots)
    # The names that a new copy name for slot i would interfere with. For an
    # operand from p: the names live just before the terminator of p. For
    # the target: the names live just after the phis, the other phi targets
    # (a dead one still writes its variable), and the targets of the copies
    # already placed after the phis.
    top = set(after[label]) | {d for d, _ in st.phis[label]}
    top |= {ins[1] for ins in st.body[label][: st.top[label]]}
    top.discard(slots[0][1])
    near = [top] + [live_out[p] | set(toyir.term_uses(st.term[p])) for p, _ in slots[1:]]

    def live_at(i):
        return near[i]

    chosen = {i for i in range(n) if not isinstance(slots[i][1], str)}  # @line L4
    deferred = {}
    for i in range(n):  # @line L5
        for j in range(i + 1, n):
            xi, xj = slots[i][1], slots[j][1]
            if not isinstance(xi, str) or not isinstance(xj, str) or xi == xj:
                continue
            ci, cj = classes.of(xi), classes.of(xj)
            if not _classes_interfere(ci, cj, g):  # @line L6
                continue
            need_i = bool(ci & live_at(j))  # @line L7
            need_j = bool(cj & live_at(i))
            if need_i:
                chosen.add(i)  # @line L8
            if need_j:
                chosen.add(j)  # @line L9
            if not need_i and not need_j:
                deferred.setdefault(i, set()).add(j)  # @line L10
                deferred.setdefault(j, set()).add(i)
    for i in sorted(deferred, key=lambda i: (-len(deferred[i]), i)):  # @line L11
        if i not in chosen and any(j not in chosen for j in deferred[i]):
            chosen.add(i)  # @line L12
    grown = True
    while grown:  # @line L13
        grown = False
        for i in sorted(chosen):
            for j in range(n):
                if j not in chosen and classes.of(slots[j][1]) & live_at(i):
                    chosen.add(j)  # @line L14
                    grown = True
    return chosen


def to_cssa(prog, method=3):
    """Copies that make prog conventional. Returns (program, number of copies)."""
    if method not in (1, 3):
        raise ValueError("method must be 1 or 3")
    st = _State(prog)
    classes = Classes()  # @line L1
    for label in st.order:
        for k in range(len(st.phis[label])):  # @line L2
            if method == 1:
                chosen = set(range(len(st.slots(label, k))))
            else:
                chosen = _choose(st, label, k, classes)
            _insert(st, label, k, chosen)  # @line L15
            names = [r for _, r in st.slots(label, k)]
            for r in names[1:]:
                classes.union(names[0], r)  # @line L16
    return st.program(), st.copies


def phi_classes(prog):
    """The phi congruence classes of prog, as a Classes object."""
    classes = Classes()
    for b in prog.blocks.values():
        for ins in b.instrs:
            if ins[0] == "phi":
                for a in ins[2].values():
                    if isinstance(a, str):
                        classes.union(ins[1], a)
    return classes


def rename_classes(cssa):
    """Give each phi congruence class one variable and drop the phi-functions
    and the copies x = x. Correct when cssa is conventional."""
    classes = phi_classes(cssa)  # @line L17
    params = set(cssa.params)
    rep = {}
    for root, members in classes.members.items():
        named = sorted(members & params) or sorted(members)
        for x in members:
            rep[x] = named[0]

    def m(a):
        return rep.get(a, a) if isinstance(a, str) else a

    blocks = {}
    for label, b in cssa.blocks.items():
        out = []
        for ins in b.instrs:
            if ins[0] == "phi":
                continue
            if ins[0] == "const":
                out.append(("const", m(ins[1]), ins[2]))
            elif ins[0] == "copy":
                if m(ins[1]) != m(ins[2]):
                    out.append(("copy", m(ins[1]), m(ins[2])))
            else:
                out.append(("op", m(ins[1]), ins[2], m(ins[3]), m(ins[4])))
        t = b.term
        if t[0] in ("br", "ret"):
            t = (t[0], m(t[1])) + tuple(t[2:])
        blocks[label] = Block(out, t)
    return Program(list(cssa.params), blocks)


def sreedhar_out_of_ssa(prog, method=3):
    """Translate prog out of SSA form. Returns (program, copies inserted)."""
    cssa, copies = to_cssa(prog, method)
    return rename_classes(cssa), copies
