# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gas-model/. The authors are listed in prov/Z8G7PR.jsonl.
"""A small simulator of the gather-apply-scatter (GAS) model on a vertex cut.

Each edge is placed on one of p machines. A vertex v spans the set A(v) of
machines that hold at least one of its edges. One machine of A(v) holds the
master copy of v; the others hold mirrors. The replication factor is
(1/|V|) * sum over v of |A(v)|.

One synchronous iteration on the active vertices:
  gather:  each machine sums gather() over its in-edges of v, using its local
           copy of the source value, and a mirror sends its partial sum to
           the master (1 word);
  apply:   the master combines the partial sums and computes the new value,
           then sends it to each mirror (|A(v)| - 1 words);
  scatter: each machine runs scatter() on its out-edges of v; the vertices it
           activates are reported to their masters (1 word for each machine
           and target, if the machine is not the master).
"""


class VertexCut:
    def __init__(self, n, edges, place):
        """edges is a list of (u, v, weight). place[i] is the machine of edge i."""
        self.n, self.edges, self.place = n, edges, place
        self.p = max(place, default=0) + 1
        self.span = [set() for _ in range(n)]
        for (u, v, _), m in zip(edges, place):
            self.span[u].add(m)
            self.span[v].add(m)
        self.master = []
        for v in range(n):
            if not self.span[v]:
                self.span[v].add(v % self.p)
            self.master.append(min(self.span[v]))

    def replication_factor(self):
        return sum(len(a) for a in self.span) / self.n


def random_cut(n, edges, p, rng):
    """Random edge placement (the randomized vertex cut of PowerGraph)."""
    return VertexCut(n, edges, [rng.randrange(p) for _ in edges])


def expected_replication(n, edges, p):
    """Theorem 5.2 of the PowerGraph paper: (p/|V|) * sum (1 - (1 - 1/p)^D[v])."""
    deg = [0] * n
    for u, v, _ in edges:
        deg[u] += 1
        deg[v] += 1
    return p / n * sum(1 - (1 - 1 / p) ** d for d in deg)


def cut_fraction(n, edges, p, rng):
    """Random vertex placement (an edge cut): the fraction of cut edges."""
    where = [rng.randrange(p) for _ in range(n)]
    return sum(where[u] != where[v] for u, v, _ in edges) / len(edges)


def run_gas(cut, prog, value, max_iters=1000):
    """prog has gather(edge_weight, source_value, source_outdeg), sum(a, b),
    apply(old, acc_or_None) -> new, and scatter(old, new) -> bool (activate
    the out-neighbours). Returns (values, log); each log entry is a dict of
    word counts for one iteration."""
    n, p = cut.n, cut.p
    outdeg = [0] * n
    for u, _, _ in cut.edges:
        outdeg[u] += 1
    copy = [dict() for _ in range(p)]  # the value of v as machine m sees it
    for v in range(n):
        for m in cut.span[v]:
            copy[m][v] = value[v]
    active = set(range(n))
    log = []
    it = 0
    while active and it < max_iters:
        it += 1
        # Gather: one partial sum for each (machine, target vertex).
        partial = {}
        for (u, v, w), m in zip(cut.edges, cut.place):
            if v in active:
                g = prog.gather(w, copy[m][u], outdeg[u])
                key = (m, v)
                partial[key] = g if key not in partial else prog.sum(partial[key], g)
        gather_words = sum(1 for (m, v) in partial if m != cut.master[v])
        acc = {}
        for (m, v), g in sorted(partial.items(), key=lambda kv: (kv[0][1], kv[0][0])):
            acc[v] = g if v not in acc else prog.sum(acc[v], g)
        # Apply at the master, then update the mirrors.
        new = {v: prog.apply(copy[cut.master[v]][v], acc.get(v)) for v in active}
        apply_words = sum(len(cut.span[v]) - 1 for v in active)
        old = {v: copy[cut.master[v]][v] for v in active}
        for v, x in new.items():
            for m in cut.span[v]:
                copy[m][v] = x
        # Scatter: activate the out-neighbours of vertices whose scatter says so.
        reports = set()
        for (u, v, w), m in zip(cut.edges, cut.place):
            if u in active and prog.scatter(old[u], new[u]):
                reports.add((m, v))
        scatter_words = sum(1 for (m, v) in reports if m != cut.master[v])
        active = {v for _, v in reports}
        log.append({"gather": gather_words, "apply": apply_words, "scatter": scatter_words})
    return [copy[cut.master[v]][v] for v in range(n)], log


class PageRank:
    """x_v = (1 - alpha)/n + alpha * sum over in-edges (u, v) of x_u / outdeg(u).
    It runs a fixed number of iterations with all vertices active."""

    def __init__(self, n, alpha):
        self.n, self.alpha = n, alpha

    def gather(self, w, xu, du):
        return xu / du

    def sum(self, a, b):
        return a + b

    def apply(self, old, acc):
        return (1 - self.alpha) / self.n + self.alpha * (acc if acc is not None else 0)

    def scatter(self, old, new):
        return True


class SSSP:
    """Shortest paths: gather min over in-edges of dist(u) + w."""

    def gather(self, w, du, _):
        return du + w

    def sum(self, a, b):
        return min(a, b)

    def apply(self, old, acc):
        return old if acc is None else min(old, acc)

    def scatter(self, old, new):
        return new < old


def run_pagerank(cut, alpha, iterations):
    """All vertices stay active when each vertex has an in-edge (the ring of
    demo_graph gives one), so this runs exactly `iterations` iterations."""
    zero = alpha - alpha  # 0 in the number type of alpha
    return run_gas(cut, PageRank(cut.n, alpha), [(zero + 1) / cut.n] * cut.n, max_iters=iterations)


def run_sssp(cut, source):
    """All vertices start active. The run stops when no value changes."""
    value = [float("inf")] * cut.n
    value[source] = 0
    return run_gas(cut, SSSP(), value)


def demo_graph(rng, n, extra):
    """A ring u -> u + 1 (so no vertex lacks an out-edge) plus random arcs."""
    edges = [(u, (u + 1) % n, rng.randint(1, 9)) for u in range(n)] if n > 1 else []
    seen = {(u, v) for u, v, _ in edges}
    for _ in range(extra):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v and (u, v) not in seen:
            seen.add((u, v))
            edges.append((u, v, rng.randint(1, 9)))
    return edges
