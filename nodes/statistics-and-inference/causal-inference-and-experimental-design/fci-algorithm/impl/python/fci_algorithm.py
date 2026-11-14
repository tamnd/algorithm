# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fci-algorithm/. The authors are listed in prov/HH185A.jsonl.
"""The FCI algorithm: causal discovery with latent confounders.

The input is a set of observed nodes and a test ci(a, b, S). The output is a
partial ancestral graph (PAG). An edge between a and b has a mark at each
end. mark[(a, b)] is the mark at b on the edge between a and b:

    '>'  arrowhead: b is not an ancestor of a
    '-'  tail:      b is an ancestor of a
    'o'  circle:    the class does not agree

So a -> b has mark[(a, b)] == '>' and mark[(b, a)] == '-', a <-> b has '>'
at both ends, and a o-> b has mark[(b, a)] == 'o' and mark[(a, b)] == '>'.

The rules are R1 to R4 and R8 to R10 of Zhang (2008), which are complete when
there is no selection bias. This module assumes no selection bias.

It also contains m-separation for mixed graphs (directed and bidirected
edges), used as the oracle in the tests, and the construction of the
maximal ancestral graph (MAG) of a DAG with latent nodes.
"""

import itertools
from typing import NamedTuple


class FCIResult(NamedTuple):
    mark: dict       # (a, b) -> mark at b on the edge a *-* b
    sepset: dict     # frozenset({a, b}) -> separating set
    tests: int       # number of calls to the independence test
    pds_removed: list  # edges removed in the Possible-D-SEP phase


# ---------------------------------------------------------------------------
# Graph helpers for oracles


def ancestors_of(parents, nodes):
    seen = set(nodes)
    stack = list(nodes)
    while stack:
        v = stack.pop()
        for p in parents[v]:
            if p not in seen:
                seen.add(p)
                stack.append(p)
    return seen


def m_separated(mark, nodes, xs, ys, zs):
    """m-separation in a mixed graph given by end marks ('>' or '-').

    A walk is open if every collider is an ancestor of zs (or in zs) and every
    non-collider is outside zs. Such a walk exists exactly when an open path
    exists.
    """
    zs = set(zs)
    parents = {v: {u for u in nodes if mark.get((u, v)) == '>' and mark.get((v, u)) == '-'} for v in nodes}
    an_z = ancestors_of(parents, zs)
    nbrs = {v: [u for u in nodes if (u, v) in mark] for v in nodes}
    # state: (node, True if the edge used to reach node has an arrowhead at node)
    start = [(w, mark[(x, w)] == '>') for x in xs if x not in zs for w in nbrs[x]]
    seen = set()
    stack = []
    for st in start:
        if st not in seen:
            seen.add(st)
            stack.append(st)
    while stack:
        v, into = stack.pop()
        if v in ys:
            return False
        for w in nbrs[v]:
            collider = into and mark[(w, v)] == '>'
            if collider and v not in an_z:
                continue
            if not collider and v in zs:
                continue
            st = (w, mark[(v, w)] == '>')
            if st not in seen:
                seen.add(st)
                stack.append(st)
    return True


def m_oracle(mark, nodes):
    return lambda a, b, s: m_separated(mark, nodes, {a}, {b}, s)


def dag_marks(parents):
    """End marks of a DAG given as node -> set of parents."""
    mark = {}
    for v in parents:
        for p in parents[v]:
            mark[(p, v)] = '>'
            mark[(v, p)] = '-'
    return mark


def latent_oracle(parents, observed):
    """d-separation oracle of a DAG, for questions about observed nodes only."""
    nodes = list(parents)
    mark = dag_marks(parents)
    return lambda a, b, s: m_separated(mark, nodes, {a}, {b}, s)


def mag_of_dag(parents, observed):
    """The MAG over the observed nodes of a DAG with latent nodes (no selection).

    a and b are adjacent when no set of other observed nodes d-separates them.
    The edge is a -> b if a is an ancestor of b in the DAG, b -> a in the
    reverse case, and a <-> b otherwise.
    """
    ci = latent_oracle(parents, observed)
    obs = sorted(observed)
    mark = {}
    for a, b in itertools.combinations(obs, 2):
        rest = [v for v in obs if v not in (a, b)]
        if any(ci(a, b, set(s)) for k in range(len(rest) + 1) for s in itertools.combinations(rest, k)):
            continue
        if a in ancestors_of(parents, {b}):
            mark[(a, b)], mark[(b, a)] = '>', '-'
        elif b in ancestors_of(parents, {a}):
            mark[(a, b)], mark[(b, a)] = '-', '>'
        else:
            mark[(a, b)], mark[(b, a)] = '>', '>'
    return mark


# ---------------------------------------------------------------------------
# FCI


def adjacent(mark, a, b):
    return (a, b) in mark


def neighbours(mark, nodes, a):
    return [b for b in nodes if (a, b) in mark]


def orient_unshielded_colliders(mark, nodes, sepset):
    for c in nodes:
        for a, b in itertools.combinations(neighbours(mark, nodes, c), 2):
            if not adjacent(mark, a, b) and c not in sepset[frozenset((a, b))]:
                mark[(a, c)] = '>'
                mark[(b, c)] = '>'


def possible_d_sep(mark, nodes, a):
    """Nodes b with a path from a on which every inner triple <x, y, z> has y a
    collider or x, z adjacent."""
    out = set()
    seen = set()
    stack = []
    for w in neighbours(mark, nodes, a):
        seen.add((a, w))
        stack.append((a, w))
    while stack:
        x, y = stack.pop()
        out.add(y)
        for z in neighbours(mark, nodes, y):
            if z == x or z == a:
                continue
            collider = mark[(x, y)] == '>' and mark[(z, y)] == '>'
            if (collider or adjacent(mark, x, z)) and (y, z) not in seen:
                seen.add((y, z))
                stack.append((y, z))
    out.discard(a)
    return out


def is_pd_edge(mark, u, v):
    """The edge u *-* v can be read as u -> v: no arrowhead at u, no tail at v."""
    return mark[(v, u)] != '>' and mark[(u, v)] != '-'


def uncovered_pd_paths(mark, nodes, a, b):
    """All uncovered potentially directed paths from a to b."""
    out = []

    def extend(path):
        u = path[-1]
        if u == b:
            out.append(list(path))
            return
        for v in neighbours(mark, nodes, u):
            if v in path or not is_pd_edge(mark, u, v):
                continue
            if len(path) >= 2 and adjacent(mark, path[-2], v):
                continue
            path.append(v)
            extend(path)
            path.pop()

    extend([a])
    return out


def discriminating_thetas(mark, nodes, b, c):
    """Pairs (theta, alpha) where some path <theta, ..., alpha, b, c> is
    discriminating for b: every inner node before b is a collider on the path
    and a parent of c, and theta is not adjacent to c."""
    found = []

    def is_parent(x, y):
        return mark.get((x, y)) == '>' and mark.get((y, x)) == '-'

    def extend(path):
        # path = [b, alpha, ..., x], read backwards from b; x must be a collider and a parent of c
        x = path[-1]
        for w in neighbours(mark, nodes, x):
            if w in path or w == c or mark[(w, x)] != '>':
                continue
            if not adjacent(mark, w, c):
                found.append((w, path[1]))
            elif is_parent(w, c) and mark[(x, w)] == '>':
                path.append(w)
                extend(path)
                path.pop()

    for alpha in neighbours(mark, nodes, b):
        if alpha != c and mark[(b, alpha)] == '>' and is_parent(alpha, c):
            extend([b, alpha])
    return found


def apply_rules(mark, nodes, sepset):
    """Zhang's rules R1 to R4 and R8 to R10, until none applies."""
    changed = True
    while changed:  # @line L9
        changed = False
        for b in nodes:
            for c in neighbours(mark, nodes, b):
                for a in neighbours(mark, nodes, b):
                    if a == c:
                        continue
                    # R1: a *-> b o-* c, a and c not adjacent: b -> c
                    if mark[(a, b)] == '>' and mark[(c, b)] == 'o' and not adjacent(mark, a, c):  # @line L10
                        mark[(c, b)], mark[(b, c)] = '-', '>'
                        changed = True
                    # R2: a -> b *-> c or a *-> b -> c, and a *-o c: a *-> c
                    if adjacent(mark, a, c) and mark[(a, c)] == 'o':  # @line L10
                        if (mark[(b, a)] == '-' and mark[(a, b)] == '>' and mark[(b, c)] == '>') or \
                           (mark[(a, b)] == '>' and mark[(c, b)] == '-' and mark[(b, c)] == '>'):
                            mark[(a, c)] = '>'
                            changed = True
        # R3: a *-> b <-* c, a *-o d o-* c, a and c not adjacent, d *-o b: d *-> b
        for b in nodes:
            for a, c in itertools.combinations(neighbours(mark, nodes, b), 2):  # @line L10
                if adjacent(mark, a, c) or mark[(a, b)] != '>' or mark[(c, b)] != '>':
                    continue
                for d in neighbours(mark, nodes, b):
                    if d in (a, c) or not adjacent(mark, a, d) or not adjacent(mark, c, d):
                        continue
                    if mark[(a, d)] == 'o' and mark[(c, d)] == 'o' and mark[(d, b)] == 'o':
                        mark[(d, b)] = '>'
                        changed = True
        # R4: discriminating path <theta, ..., alpha, b, c> for b with b o-* c
        for b in nodes:
            for c in neighbours(mark, nodes, b):
                if mark[(c, b)] != 'o':
                    continue
                for theta, alpha in discriminating_thetas(mark, nodes, b, c):  # @line L10
                    if mark[(c, b)] != 'o':
                        break
                    if b in sepset.get(frozenset((theta, c)), set()):
                        mark[(c, b)], mark[(b, c)] = '-', '>'
                    else:
                        mark[(alpha, b)] = mark[(b, alpha)] = '>'
                        mark[(c, b)] = mark[(b, c)] = '>'
                    changed = True
        # Tail rules on edges a o-> c
        for a in nodes:
            for c in neighbours(mark, nodes, a):
                if not (mark[(c, a)] == 'o' and mark[(a, c)] == '>'):
                    continue
                tail = False
                # R8: a -> b -> c or a -o b -> c
                for b in neighbours(mark, nodes, a):  # @line L11
                    if b != c and adjacent(mark, b, c) and mark[(b, a)] == '-' and mark[(a, b)] in ('>', 'o') \
                            and mark[(c, b)] == '-' and mark[(b, c)] == '>':
                        tail = True
                # R9: uncovered p.d. path <a, b, theta, ..., c> with b and c not adjacent
                if not tail:
                    for b in neighbours(mark, nodes, a):  # @line L11
                        if b == c or adjacent(mark, b, c) or not is_pd_edge(mark, a, b):
                            continue
                        for p in uncovered_pd_paths(mark, nodes, b, c):
                            if a not in p and not adjacent(mark, a, p[1]):
                                tail = True
                                break
                        if tail:
                            break
                # R10: b -> c <- t, uncovered p.d. paths from a to b and to t whose
                # second nodes are distinct and not adjacent
                if not tail:
                    into_c = [b for b in neighbours(mark, nodes, c) if b != a and mark[(c, b)] == '-' and mark[(b, c)] == '>']
                    for b, t in itertools.combinations(into_c, 2):  # @line L11
                        mus = {p[1] for p in uncovered_pd_paths(mark, nodes, a, b) if c not in p}
                        oms = {p[1] for p in uncovered_pd_paths(mark, nodes, a, t) if c not in p}
                        if any(mu != om and not adjacent(mark, mu, om) for mu in mus for om in oms):
                            tail = True
                            break
                if tail:
                    mark[(c, a)] = '-'
                    changed = True
    return mark  # @line L12


def fci(nodes, ci):
    """Run FCI with the independence test ci(a, b, S). Returns an FCIResult."""
    nodes = sorted(nodes)
    adj = {v: set(nodes) - {v} for v in nodes}
    sepset = {}
    tests = 0
    k = 0
    while any(len(adj[a]) - 1 >= k for a in nodes):  # @line L1
        for a in nodes:
            for b in sorted(adj[a]):
                if b not in adj[a] or len(adj[a]) - 1 < k:
                    continue
                for s in itertools.combinations(sorted(adj[a] - {b}), k):
                    tests += 1
                    if ci(a, b, set(s)):  # @line L1
                        adj[a].discard(b)
                        adj[b].discard(a)
                        sepset[frozenset((a, b))] = set(s)
                        break
        k += 1
    mark = {(a, b): 'o' for a in nodes for b in adj[a]}  # @line L2
    orient_unshielded_colliders(mark, nodes, sepset)  # @line L3
    pds = {a: possible_d_sep(mark, nodes, a) for a in nodes}
    removed = []
    for a, b in itertools.combinations(nodes, 2):
        if not adjacent(mark, a, b):
            continue
        done = False
        for x in (a, b):  # @line L4
            cand = sorted(pds[x] - {a, b})
            for size in range(len(cand) + 1):
                for s in itertools.combinations(cand, size):  # @line L5
                    tests += 1
                    if ci(a, b, set(s)):  # @line L6
                        del mark[(a, b)]
                        del mark[(b, a)]
                        sepset[frozenset((a, b))] = set(s)
                        removed.append((a, b))
                        done = True
                        break
                if done:
                    break
            if done:
                break
    for e in mark:
        mark[e] = 'o'  # @line L7
    orient_unshielded_colliders(mark, nodes, sepset)  # @line L8
    apply_rules(mark, nodes, sepset)
    return FCIResult(mark, sepset, tests, removed)


def edge_string(mark, a, b):
    """Text form such as 'A o-> B' of the edge between a and b."""
    left = {'>': '<', '-': '-', 'o': 'o'}[mark[(b, a)]]
    right = {'>': '>', '-': '-', 'o': 'o'}[mark[(a, b)]]
    return f"{a} {left}-{right} {b}"


def pag_edges(mark):
    return sorted(edge_string(mark, a, b) for (a, b) in mark if str(a) < str(b))


if __name__ == "__main__":
    # A -> B <- L -> C <- D with L hidden.
    g = {"A": set(), "L": set(), "D": set(), "B": {"A", "L"}, "C": {"L", "D"}}
    obs = ["A", "B", "C", "D"]
    res = fci(obs, latent_oracle(g, obs))
    print(pag_edges(res.mark), "tests", res.tests)
