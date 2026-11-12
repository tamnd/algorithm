# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/junction-tree-algorithm/. The authors are listed in prov/RT2GC9.jsonl.

"""The junction tree algorithm for exact inference in discrete models.

A model is a list of factors over the variables 0 .. n-1, where variable v takes
the values 0 .. card[v]-1. A factor is a scope (a tuple of distinct variables)
and a table from assignments of the scope to nonnegative numbers. For a Bayesian
network, give one factor P(X | parents) per variable; the graph built in line L1
is then the moral graph.

The main function follows the Hugin architecture (Jensen, Lauritzen and Olesen
1990), in which a pass divides by the old separator table. shafer_shenoy computes
the same clique tables with the messages of Shafer and Shenoy (1990), which
never divide. Both do one collect pass to a root and one distribute pass back,
2(k - 1) messages for k cliques.
"""

from itertools import combinations, product
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple

Assignment = Tuple[int, ...]


class Factor(NamedTuple):
    scope: Tuple[int, ...]
    table: Dict[Assignment, object]


class Result(NamedTuple):
    cliques: List[Tuple[int, ...]]          # each clique as a sorted tuple of variables
    tree_edges: List[Tuple[int, int]]
    potentials: List[Dict[Assignment, object]]  # potentials[i][a] = P(C_i = a, e)
    evidence_probability: object            # P(e), or Z(e) for a Markov random field
    messages: int

    def clique_marginal(self, i: int) -> Dict[Assignment, object]:
        """P(C_i | e) as a dict from assignments of cliques[i] to probabilities."""
        return {a: p / self.evidence_probability for a, p in self.potentials[i].items()}

    def marginal(self, v: int) -> Dict[int, object]:
        """P(X_v | e), read from the smallest clique that holds v."""
        i = min((i for i, c in enumerate(self.cliques) if v in c), key=lambda i: len(self.cliques[i]))
        pos = self.cliques[i].index(v)
        out: Dict[int, object] = {}
        for a, p in self.potentials[i].items():
            out[a[pos]] = out.get(a[pos], 0) + p / self.evidence_probability
        return out


def min_fill_order(n: int, edges: Sequence[Tuple[int, int]]) -> List[int]:
    """A greedy order: next, the vertex whose elimination adds the fewest fill edges."""
    adj = {v: set() for v in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    order = []
    while adj:
        def fill(v: int) -> int:
            return sum(1 for a, b in combinations(adj[v], 2) if b not in adj[a])
        v = min(adj, key=lambda v: (fill(v), v))
        nb = adj.pop(v)
        for a, b in combinations(nb, 2):
            adj[a].add(b)
            adj[b].add(a)
        for a in nb:
            adj[a].discard(v)
        order.append(v)
    return order


def build_junction_tree(n: int, edges: Sequence[Tuple[int, int]],
                        order: Sequence[int]) -> Tuple[List[Tuple[int, ...]], List[Tuple[int, int]]]:
    """Triangulate along the order, keep the maximal cliques, join them by a maximum
    weight spanning tree with the separator sizes as weights (Kruskal)."""
    adj = {v: set() for v in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    cliques: List[frozenset] = []
    for v in order:
        bag = frozenset(adj[v] | {v})
        nb = adj.pop(v)
        for a, b in combinations(nb, 2):
            adj[a].add(b)
            adj[b].add(a)
        for a in nb:
            adj[a].discard(v)
        if not any(bag <= c for c in cliques):
            cliques.append(bag)
    k = len(cliques)
    pairs = sorted(((len(cliques[i] & cliques[j]), i, j) for i, j in combinations(range(k), 2)),
                   key=lambda t: (-t[0], t[1], t[2]))
    parent = list(range(k))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tree = []
    for _, i, j in pairs:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj
            tree.append((i, j))
    return [tuple(sorted(c)) for c in cliques], tree


def project(scope: Sequence[int], table: Dict[Assignment, object], sub: Sequence[int]) -> Dict[Assignment, object]:
    """Sum the table over the variables of scope that are not in sub."""
    idx = [list(scope).index(v) for v in sub]
    out: Dict[Assignment, object] = {}
    for a, val in table.items():
        b = tuple(a[i] for i in idx)
        out[b] = out[b] + val if b in out else val
    return out


def multiply_in(scope: Sequence[int], table: Dict[Assignment, object], f: Factor) -> None:
    """table <- table * f, where the scope of f lies inside scope."""
    idx = [list(scope).index(v) for v in f.scope]
    for a in table:
        table[a] = table[a] * f.table[tuple(a[i] for i in idx)]


def _setup(factors: Sequence[Factor], card: Sequence[int], evidence: Dict[int, int],
           order: Optional[Sequence[int]]):
    n = len(card)
    edges = sorted({(min(u, v), max(u, v)) for f in factors for u, v in combinations(f.scope, 2)})  # @line L1
    if order is None:
        order = min_fill_order(n, edges)
    if sorted(order) != list(range(n)):
        raise ValueError("the order must hold each variable once")
    cliques, tree = build_junction_tree(n, edges, order)  # @line L2
    # Evidence enters as indicator factors: 1 on the observed value, 0 elsewhere.
    indicators = [Factor((v,), {(x,): int(x == val) for x in range(card[v])}) for v, val in evidence.items()]
    home = []
    for f in list(factors) + indicators:
        s = set(f.scope)
        home.append((min((i for i, c in enumerate(cliques) if s <= set(c)), key=lambda i: len(cliques[i])), f))
    nb: Dict[int, List[int]] = {i: [] for i in range(len(cliques))}
    for i, j in tree:
        nb[i].append(j)
        nb[j].append(i)
    # A breadth-first order from the root 0; parent[i] is the next clique toward the root.
    bfs, parent = [0], {0: None}
    for x in bfs:
        for y in nb[x]:
            if y not in parent:
                parent[y] = x
                bfs.append(y)
    return cliques, tree, home, nb, bfs, parent, _one(factors)


def _one(factors: Sequence[Factor]) -> object:
    """The number 1 in the type of the factor entries (x ** 0), so Fractions stay exact."""
    for f in factors:
        for val in f.table.values():
            return val ** 0
    return 1


def _finish(cliques, tree, phi, messages) -> Result:
    pe = sum(phi[0].values())
    if pe == 0:
        raise ValueError("the evidence has probability zero")
    return Result(cliques, tree, phi, pe, messages)


def junction_tree_algorithm(factors: Sequence[Factor], card: Sequence[int], evidence: Dict[int, int],
                            order: Optional[Sequence[int]] = None) -> Result:
    """Hugin propagation. After the two passes, potentials[i] = P(C_i, e) for each clique."""
    cliques, tree, home, nb, bfs, parent, one = _setup(factors, card, evidence, order)
    phi = [{a: one for a in product(*(range(card[v]) for v in c))} for c in cliques]  # @line L3
    sep = {}
    for i, j in tree:
        s = tuple(sorted(set(cliques[i]) & set(cliques[j])))
        sep[frozenset((i, j))] = (s, {a: one for a in product(*(range(card[v]) for v in s))})
    for i, f in home:  # @line L4
        multiply_in(cliques[i], phi[i], f)
    messages = 0

    def send(i: int, j: int) -> None:
        s, old = sep[frozenset((i, j))]
        new = project(cliques[i], phi[i], s)  # @line L8
        idx = [cliques[j].index(v) for v in s]
        for a, val in phi[j].items():  # @line L9
            if val != 0:  # 0 / 0 = 0: a zero entry stays zero
                b = tuple(a[t] for t in idx)
                phi[j][a] = val * new[b] / old[b]
        sep[frozenset((i, j))] = (s, new)  # @line L10

    for i in reversed(bfs[1:]):  # @line L5
        send(i, parent[i])
        messages += 1
    for i in bfs[1:]:  # @line L6
        send(parent[i], i)
        messages += 1
    return _finish(cliques, tree, phi, messages)  # @line L7


def shafer_shenoy(factors: Sequence[Factor], card: Sequence[int], evidence: Dict[int, int],
                  order: Optional[Sequence[int]] = None) -> Result:
    """The Shafer-Shenoy architecture: the message from i to j is the sum over C_i - S_ij
    of psi_i times the messages into i from all neighbours except j. No division."""
    cliques, tree, home, nb, bfs, parent, one = _setup(factors, card, evidence, order)
    psi = [{a: one for a in product(*(range(card[v]) for v in c))} for c in cliques]
    for i, f in home:
        multiply_in(cliques[i], psi[i], f)
    msg: Dict[Tuple[int, int], Factor] = {}

    def send(i: int, j: int) -> None:
        t = dict(psi[i])
        for k in nb[i]:
            if k != j:
                multiply_in(cliques[i], t, msg[k, i])
        s = tuple(sorted(set(cliques[i]) & set(cliques[j])))
        msg[i, j] = Factor(s, project(cliques[i], t, s))

    for i in reversed(bfs[1:]):
        send(i, parent[i])
    for i in bfs[1:]:
        send(parent[i], i)
    phi = []
    for i in range(len(cliques)):
        t = dict(psi[i])
        for k in nb[i]:
            multiply_in(cliques[i], t, msg[k, i])
        phi.append(t)
    return _finish(cliques, tree, phi, len(msg))


def sprinkler_network() -> Tuple[List[Factor], List[int]]:
    """The cloudy, sprinkler, rain, wet grass network: C=0, S=1, R=2, W=3."""
    from fractions import Fraction as F
    ps1 = {0: F(1, 2), 1: F(1, 10)}
    pr1 = {0: F(1, 5), 1: F(4, 5)}
    pw1 = {(0, 0): F(0), (0, 1): F(9, 10), (1, 0): F(9, 10), (1, 1): F(99, 100)}
    pc = Factor((0,), {(0,): F(1, 2), (1,): F(1, 2)})
    ps = Factor((1, 0), {(s, c): ps1[c] if s else 1 - ps1[c] for s in (0, 1) for c in (0, 1)})
    pr = Factor((2, 0), {(r, c): pr1[c] if r else 1 - pr1[c] for r in (0, 1) for c in (0, 1)})
    pw = Factor((3, 1, 2), {(w, s, r): pw1[s, r] if w else 1 - pw1[s, r]
                            for w in (0, 1) for s in (0, 1) for r in (0, 1)})
    return [pc, ps, pr, pw], [2, 2, 2, 2]
