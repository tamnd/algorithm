# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slp-vectorization/. The authors are listed in prov/VMGC16.jsonl.
"""Superword-level parallelism (SLP) vectorization of one basic block.

A basic block is a list of statements in three-address form:

    ("load", x, (A, c))        x = A[c]
    ("store", (A, c), y)       A[c] = y
    ("op", x, (o, y, z))       x = y o z, with o in "+", "-", "*"

Here x, y, z are scalar names (y and z may also be int constants), A is an
array name and c is a constant index. The algorithm follows Larsen and
Amarasinghe (PLDI 2000): seed pairs from adjacent memory accesses, extend
the pairs along use-def and def-use chains, combine the pairs into groups of
at most VL statements, and schedule the groups in dependence order. A group
runs as one SIMD instruction: it reads the operands of all its lanes, then
writes all its results.
"""

OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b}


def reads(st):
    """Locations read by a statement: ("v", name) or ("m", array, index)."""
    kind, tgt, arg = st
    if kind == "load":
        return [("m",) + arg]
    if kind == "store":
        return [("v", arg)] if isinstance(arg, str) else []
    return [("v", a) for a in arg[1:] if isinstance(a, str)]


def writes(st):
    kind, tgt, arg = st
    return ("m",) + tgt if kind == "store" else ("v", tgt)


def dependences(block):
    """All pairs (s, t), s < t, where s and t touch one location and one writes it."""
    deps = set()
    for t in range(len(block)):
        rt, wt = set(reads(block[t])), writes(block[t])
        for s in range(t):
            rs, ws = set(reads(block[s])), writes(block[s])
            if ws == wt or ws in rt or wt in rs:
                deps.add((s, t))
    return deps


def reach(n, deps):
    """reach[s] is the set of statements t with a dependence path from s to t."""
    succ = [[] for _ in range(n)]
    for s, t in deps:
        succ[s].append(t)
    out = [set() for _ in range(n)]
    for s in range(n - 1, -1, -1):
        for t in succ[s]:
            out[s].add(t)
            out[s] |= out[t]
    return out


def isomorphic(a, b):
    if a[0] != b[0]:
        return False
    if a[0] == "load":
        return a[2][0] == b[2][0]
    if a[0] == "store":
        return a[1][0] == b[1][0]
    return a[2][0] == b[2][0]


def adjacent(a, b):
    """For memory statements: b accesses the cell right after the cell of a."""
    if a[0] == "load":
        (x, i), (y, j) = a[2], b[2]
    elif a[0] == "store":
        (x, i), (y, j) = a[1], b[1]
    else:
        return True
    return x == y and j == i + 1


class SLP:
    def __init__(self, block, vl=4):
        self.block = block
        self.vl = vl
        self.deps = dependences(block)
        self.reach = reach(len(block), self.deps)
        self.left, self.right = {}, {}

    def independent(self, s, t):
        return t not in self.reach[s] and s not in self.reach[t]

    def can_pack(self, s, t):
        b = self.block
        return (s != t and isomorphic(b[s], b[t]) and adjacent(b[s], b[t])
                and self.independent(s, t)
                and s not in self.left and t not in self.right)

    def add(self, s, t):
        self.left[s] = t
        self.right[t] = s

    def def_of(self, s, name):
        """The last statement before s that writes the scalar name, or None."""
        for p in range(s - 1, -1, -1):
            if writes(self.block[p]) == ("v", name):
                return p
        return None

    def uses_of(self, s):
        """(position, user) for each read of the scalar written by s, up to its next write."""
        st = self.block[s]
        if st[0] == "store":
            return []
        name, out = st[1], []
        for u in range(s + 1, len(self.block)):
            us = self.block[u]
            ops = [us[2]] if us[0] == "store" else list(us[2][1:]) if us[0] == "op" else []
            for pos, a in enumerate(ops):
                if a == name:
                    out.append((pos, u))
            if writes(us) == ("v", name):
                break
        return out

    def operands(self, s):
        st = self.block[s]
        if st[0] == "store":
            return [st[2]]
        if st[0] == "op":
            return list(st[2][1:])
        return []

    def seed(self):
        b = self.block
        mem = [s for s in range(len(b)) if b[s][0] in ("load", "store")]
        for s in mem:
            for t in mem:
                if self.can_pack(s, t):  # @line L1
                    self.add(s, t)

    def extend(self):
        work = sorted(self.left.items())  # @line L2
        while work:  # @line L3
            s, t = work.pop(0)
            for x, y in zip(self.operands(s), self.operands(t)):
                if isinstance(x, str) and isinstance(y, str):
                    ds, dt = self.def_of(s, x), self.def_of(t, y)
                    if ds is not None and dt is not None and self.can_pack(ds, dt):  # @line L4
                        self.add(ds, dt)
                        work.append((ds, dt))
            us, ut = self.uses_of(s), self.uses_of(t)
            for ps, u in us:
                for pt, v in ut:
                    if ps == pt and self.can_pack(u, v):  # @line L5
                        self.add(u, v)
                        work.append((u, v))

    def combine(self):
        """Join pairs (s, t), (t, u) into chains; cut a chain where a member
        depends on an earlier member or the length would pass VL."""
        groups, seen = [], set()
        starts = [s for s in sorted(self.left) if s not in self.right]
        cyc = [s for s in sorted(self.left) if s in self.right]
        for s in starts + cyc:
            if s in seen:
                continue
            chain = [s]
            seen.add(s)
            while chain[-1] in self.left and self.left[chain[-1]] not in seen:
                chain.append(self.left[chain[-1]])
                seen.add(chain[-1])
            cur = []
            for x in chain:
                if len(cur) == self.vl or not all(self.independent(x, y) for y in cur):
                    groups.append(cur)
                    cur = []
                cur.append(x)
            groups.append(cur)
        return [g for g in groups if len(g) > 1]

    def schedule(self, groups):
        """Emit the items in dependence order. Returns a list of lists of
        statement numbers; a list of length 1 is a scalar statement."""
        return schedule(self.block, self.deps, groups)

    def run(self):
        self.seed()
        self.extend()
        groups = self.combine()  # @line L6
        return self.schedule(groups)


def schedule(block, deps, groups):
    group_of = {}
    for g in groups:
        for s in g:
            group_of[s] = list(g)
    preds = {t: set() for t in range(len(block))}
    for s, t in deps:
        preds[t].add(s)
    done, out = set(), []
    while len(done) < len(block):  # @line L7
        pick = None
        for s in range(len(block)):  # @line L8
            if s in done:
                continue
            item = group_of.get(s, [s])
            if all(p in done or p in item for x in item for p in preds[x]):
                pick = item
                break
        if pick is None:  # @line L10
            first = min(s for s in range(len(block)) if s not in done)
            for x in group_of.pop(first):
                group_of.pop(x, None)
            continue
        out.append(pick)  # @line L9
        done.update(pick)
    return out


def slp_vectorize(block, vl=4):
    return SLP(block, vl).run()


def value(arg, env):
    return arg if isinstance(arg, int) else env[arg]


def run_scalar(block, env, mem):
    env, mem = dict(env), dict(mem)
    for st in block:
        exec_items([st], env, mem)
    return env, mem


def exec_items(stmts, env, mem):
    """Run statements as one SIMD instruction: read every lane, then write."""
    vals = []
    for kind, tgt, arg in stmts:
        if kind == "load":
            vals.append(mem[arg])
        elif kind == "store":
            vals.append(value(arg, env))
        else:
            vals.append(OPS[arg[0]](value(arg[1], env), value(arg[2], env)))
    for (kind, tgt, arg), v in zip(stmts, vals):
        if kind == "store":
            mem[tgt] = v
        else:
            env[tgt] = v


def run_vector(block, code, env, mem):
    env, mem = dict(env), dict(mem)
    for item in code:
        exec_items([block[s] for s in item], env, mem)
    return env, mem


def unrolled_example(n=4):
    """A[i] = B[i] * C[i] + D[i] for i = 0 .. n-1, unrolled into three-address code."""
    block = []
    for i in range(n):
        block += [("load", f"b{i}", ("B", i)), ("load", f"c{i}", ("C", i)),
                  ("op", f"m{i}", ("*", f"b{i}", f"c{i}")), ("load", f"d{i}", ("D", i)),
                  ("op", f"s{i}", ("+", f"m{i}", f"d{i}")), ("store", ("A", i), f"s{i}")]
    return block


def show(block, code):
    lines = []
    for item in code:
        sts = [block[s] for s in item]
        kind = sts[0][0]
        if len(item) == 1:
            k, t, a = sts[0]
            if k == "load":
                lines.append(f"{t} = {a[0]}[{a[1]}]")
            elif k == "store":
                lines.append(f"{t[0]}[{t[1]}] = {a}")
            else:
                lines.append(f"{t} = {a[1]} {a[0]} {a[2]}")
        elif kind == "load":
            a = sts[0][2]
            lines.append(f"<{', '.join(s[1] for s in sts)}> = {a[0]}[{a[1]}:{a[1] + len(sts)}]")
        elif kind == "store":
            t = sts[0][1]
            lines.append(f"{t[0]}[{t[1]}:{t[1] + len(sts)}] = <{', '.join(str(s[2]) for s in sts)}>")
        else:
            o = sts[0][2][0]
            lhs = ", ".join(s[1] for s in sts)
            ys = ", ".join(str(s[2][1]) for s in sts)
            zs = ", ".join(str(s[2][2]) for s in sts)
            lines.append(f"<{lhs}> = <{ys}> {o} <{zs}>")
    return lines


if __name__ == "__main__":
    b = unrolled_example()
    print("\n".join(show(b, slp_vectorize(b))))
