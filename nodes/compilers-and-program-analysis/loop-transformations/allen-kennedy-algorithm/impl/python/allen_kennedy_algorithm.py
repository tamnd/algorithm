# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/allen-kennedy-algorithm/. The authors are listed in prov/WZS56G.jsonl.
"""Allen-Kennedy vector code generation (codegen) on a chain of loops.

A program is one chain of loops: loop 1 holds loop 2, which holds loop 3,
and so on up to depth n. Loop l runs its index from bounds[l-1][0] to
bounds[l-1][1], both included. The statements are listed in text order.
Statement S sits at depth d (it is inside loops 1 to d) and has the form

    W[f(i)] = c0 + c1 * R1[g1(i)] + ... + e . i     (mod MOD)

where every subscript is affine in the d indices of S. The statements with
a depth of l + 1 or more must be contiguous in the text for every l, so that
the loops form one chain.

The dependence graph has an edge (S, T, level) for each pair of instances
S(i) before T(j) that touch the same cell, at least one of them a write.
The level is the first loop where i and j differ, or LI = n + 1 for a
loop-independent dependence. codegen(R, k) follows the page: it takes the
strongly connected components of the edges of level k or more inside R, in
topological order; a cyclic component becomes a sequential loop at level k
with a recursive call at level k + 1, and an acyclic one (a single
statement) becomes a vector statement over the loops k to depth(S).
"""

from itertools import product

MOD = (1 << 61) - 1


class Stmt:
    """A statement W[f(i)] = c0 + sum(c_r * R_r[g_r(i)]) + e . i."""

    def __init__(self, name, depth, write, reads, coefs, const=1, idx_coefs=None):
        self.name = name
        self.depth = depth
        self.write = write          # (array, [(coeffs, const), ...])
        self.reads = reads          # list of (array, [(coeffs, const), ...])
        self.coefs = coefs          # one integer per read
        self.const = const
        self.idx_coefs = idx_coefs or [0] * depth

    def cell(self, acc, it):
        arr, subs = acc
        return (arr,) + tuple(sum(a * x for a, x in zip(co, it)) + c for co, c in subs)

    def value(self, mem, it, init):
        v = self.const + sum(e * x for e, x in zip(self.idx_coefs, it))
        for co, acc in zip(self.coefs, self.reads):
            v += co * read(mem, self.cell(acc, it), init)
        return v % MOD


class Program:
    def __init__(self, bounds, stmts):
        self.bounds = bounds        # list of (lo, hi) per loop level
        self.stmts = stmts
        self.n = len(bounds)
        check_chain(self)


def check_chain(prog):
    """The statements of depth > l form one contiguous run, for each l."""
    for l in range(prog.n):
        pos = [p for p, s in enumerate(prog.stmts) if s.depth > l]
        if pos and pos[-1] - pos[0] + 1 != len(pos):
            raise ValueError("the loops do not form one chain")


def read(mem, cell, init):
    if cell not in mem:
        mem[cell] = init(cell)
    return mem[cell]


def instances(prog):
    """All statement instances (s, it) in the order of the sequential program."""
    out = []

    def body(level, prefix, ids):
        p = 0
        while p < len(ids):
            s = ids[p]
            if prog.stmts[s].depth == level:
                out.append((s, prefix))
                p += 1
            else:
                q = p
                while q < len(ids) and prog.stmts[ids[q]].depth > level:
                    q += 1
                lo, hi = prog.bounds[level]
                for v in range(lo, hi + 1):
                    body(level + 1, prefix + (v,), ids[p:q])
                p = q

    body(0, (), list(range(len(prog.stmts))))
    return out


def accesses(prog, inst):
    s, it = inst
    st = prog.stmts[s]
    for acc in st.reads:
        yield st.cell(acc, it), False
    yield st.cell(st.write, it), True


def dependence_pairs(prog):
    """Brute force: every dependent pair of instances (src, snk), src first."""
    seq = instances(prog)
    by_cell = {}
    for pos, inst in enumerate(seq):
        for cell, w in accesses(prog, inst):
            by_cell.setdefault(cell, []).append((pos, inst, w))
    pairs = set()
    for lst in by_cell.values():
        for a in range(len(lst)):
            for b in range(a + 1, len(lst)):
                pa, ia, wa = lst[a]
                pb, ib, wb = lst[b]
                if (wa or wb) and pa != pb:
                    pairs.add((ia, ib) if pa < pb else (ib, ia))
    return pairs


def level_of(prog, src, snk):
    """First loop level where the common indices differ, or n + 1 (loop independent)."""
    (s, i), (t, j) = src, snk
    c = min(prog.stmts[s].depth, prog.stmts[t].depth)
    for l in range(c):
        if i[l] != j[l]:
            return l + 1
    return prog.n + 1


def dependence_graph(prog, pairs=None):
    """Edges (s, t, level) of the statement-level dependence graph."""
    if pairs is None:
        pairs = dependence_pairs(prog)
    return {(a[0], b[0], level_of(prog, a, b)) for a, b in pairs}


def tarjan_scc(nodes, succ):
    """Strongly connected components (Tarjan); returns a list of lists."""
    index, low, on, stack, comps = {}, {}, set(), [], []
    counter = [0]

    def visit(v):
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on.add(v)
        for w in succ.get(v, ()):
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            comps.append(sorted(comp))

    for v in nodes:
        if v not in index:
            visit(v)
    return comps


def topo_components(nodes, edges):
    """SCCs in a topological order of the condensation, ties by text order."""
    succ = {}
    for a, b in edges:
        succ.setdefault(a, []).append(b)
    comps = tarjan_scc(sorted(nodes), succ)
    where = {v: c for c, comp in enumerate(comps) for v in comp}
    indeg = [0] * len(comps)
    out = [set() for _ in comps]
    for a, b in edges:
        ca, cb = where[a], where[b]
        if ca != cb and cb not in out[ca]:
            out[ca].add(cb)
            indeg[cb] += 1
    ready = sorted((comps[c][0], c) for c in range(len(comps)) if indeg[c] == 0)
    order = []
    while ready:
        _, c = ready.pop(0)
        order.append(comps[c])
        for d in out[c]:
            indeg[d] -= 1
            if indeg[d] == 0:
                ready.append((comps[d][0], d))
                ready.sort()
    return order


def codegen(prog, graph, region=None, k=1):
    """Allen-Kennedy codegen(R, k). Returns a list of nodes:
    ("loop", k, children) is a sequential loop at level k, and
    ("vec", s, k) runs statement s as a vector statement over loops k to depth(s)."""
    if region is None:
        region = list(range(len(prog.stmts)))
    rs = set(region)
    edges = [(a, b) for a, b, lev in graph if a in rs and b in rs and lev >= k]  # @line L1
    comps = topo_components(region, edges)  # @line L2
    code = []
    for comp in comps:  # @line L3
        if len(comp) > 1 or (comp[0], comp[0]) in edges:  # @line L4
            assert all(prog.stmts[s].depth >= k for s in comp)
            inner = codegen(prog, graph, comp, k + 1)  # @line L6
            code.append(("loop", k, inner))  # @line L5
        else:  # @line L7
            s = comp[0]  # @line L8
            code.append(("vec", s, k))  # @line L9
    return code


def vector_levels(code, out=None):
    """For each statement, the level k at which it is vectorized."""
    if out is None:
        out = {}
    for node in code:
        if node[0] == "loop":
            vector_levels(node[2], out)
        else:
            out[node[1]] = node[2]
    return out


def run_sequential(prog, init):
    mem = {}
    for s, it in instances(prog):
        st = prog.stmts[s]
        v = st.value(mem, it, init)
        mem[st.cell(st.write, it)] = v
    return mem


def run_code(prog, code, init, steps=None):
    """Run generated code. A vector statement reads all its operands, then
    writes all its results. If steps is a dict, it records for each instance
    the number of the step (vector statement execution) that ran it."""
    mem = {}
    counter = [0]

    def run(nodes, prefix):
        for node in nodes:
            if node[0] == "loop":
                lo, hi = prog.bounds[node[1] - 1]
                for v in range(lo, hi + 1):
                    run(node[2], prefix + (v,))
            else:
                s, k = node[1], node[2]
                st = prog.stmts[s]
                ranges = [range(lo, hi + 1) for lo, hi in prog.bounds[k - 1:st.depth]]
                its = [prefix[:k - 1] + rest for rest in product(*ranges)]
                vals = [st.value(mem, it, init) for it in its]
                for it, v in zip(its, vals):
                    mem[st.cell(st.write, it)] = v
                if steps is not None:
                    for it in its:
                        steps[(s, it)] = counter[0]
                counter[0] += 1

    run(code, ())
    return mem


NAMES = "ijklmn"


def show_sub(co, c, vec_from):
    terms = []
    for l, a in enumerate(co):
        if a:
            v = NAMES[l]
            terms.append((v if a == 1 else "-" + v if a == -1 else f"{a}*{v}"))
    s = "+".join(terms).replace("+-", "-")
    if c or not s:
        s = (s + ("+" if c > 0 and s else "") + str(c)) if s else str(c)
    return s


def show(prog, code, indent=0):
    """Print generated code; a vector statement lists its vector indices."""
    lines = []
    pad = "  " * indent
    for node in code:
        if node[0] == "loop":
            l = node[1]
            lo, hi = prog.bounds[l - 1]
            lines.append(f"{pad}for {NAMES[l - 1]} = {lo} to {hi}:")
            lines.extend(show(prog, node[2], indent + 1))
        else:
            s, k = node[1], node[2]
            st = prog.stmts[s]

            def acc(a):
                arr, subs = a
                return arr + "".join("[" + show_sub(co, c, k) + "]" for co, c in subs)

            parts = [acc(r) for r in st.reads] + ([str(st.const)] if st.const else [])
            rhs = " + ".join(parts) or "0"
            vec = ",".join(NAMES[l] for l in range(k - 1, st.depth))
            head = f"vector ({vec}): " if vec else ""
            lines.append(f"{pad}{head}{st.name}: {acc(st.write)} = {rhs}")
    return lines


def sub(coeffs, const):
    return (tuple(coeffs), const)


def book_example(N=2, size=4):
    """The imperfect nest of the page (a small copy of Allen and Kennedy's example):

    for i: S1: X[i] = Y[i] + 10
           for j: S2: B[j] = A[j][N]
                  for k: S3: A[j+1][k] = B[j] + C[j][k]
                  S4: Y[i+j] = A[j+1][N]
    """
    b = [(1, size)] * 3
    s1 = Stmt("S1", 1, ("X", [sub([1], 0)]), [("Y", [sub([1], 0)])], [1], 10)
    s2 = Stmt("S2", 2, ("B", [sub([0, 1], 0)]), [("A", [sub([0, 1], 0), sub([0, 0], N)])], [1], 0)
    s3 = Stmt("S3", 3, ("A", [sub([0, 1, 0], 1), sub([0, 0, 1], 0)]),
              [("B", [sub([0, 1, 0], 0)]), ("C", [sub([0, 1, 0], 0), sub([0, 0, 1], 0)])], [1, 1], 0)
    s4 = Stmt("S4", 2, ("Y", [sub([1, 1], 0)]), [("A", [sub([0, 1], 1), sub([0, 0], N)])], [1], 0)
    return Program(b, [s1, s2, s3, s4])


if __name__ == "__main__":
    prog = book_example()
    g = dependence_graph(prog)
    for e in sorted(g):
        print(prog.stmts[e[0]].name, "->", prog.stmts[e[1]].name, "level", e[2])
    print("\n".join(show(prog, codegen(prog, g))))
