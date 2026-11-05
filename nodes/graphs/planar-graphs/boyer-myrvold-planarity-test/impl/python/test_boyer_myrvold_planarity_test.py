# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boyer-myrvold-planarity-test/. The authors are listed in prov/1RE4H8.jsonl.

import random

import pytest

from boyer_myrvold_planarity_test import is_planar, kuratowski_subgraph, planar_embedding

def oracle_planar(n, edges):
    """Independent oracle for small graphs, by Kuratowski's theorem.

    Vertices of degree at most 2 are removed or suppressed (this keeps
    planarity in both directions). A graph with more than 3k - 6 edges is
    not planar. Otherwise the graph is non-planar exactly when it is K5 or
    K3,3, or when deleting some edge leaves a non-planar graph.
    """
    memo = {}

    def reduce(E):
        E = set(E)
        while True:
            nbr = {}
            for u, v in E:
                nbr.setdefault(u, []).append(v)
                nbr.setdefault(v, []).append(u)
            changed = False
            for x, nb in nbr.items():
                if len(nb) == 1:
                    E.discard((min(x, nb[0]), max(x, nb[0])))
                    changed = True
                    break
                if len(nb) == 2:
                    a, b = nb
                    E.discard((min(x, a), max(x, a)))
                    E.discard((min(x, b), max(x, b)))
                    E.add((min(a, b), max(a, b)))
                    changed = True
                    break
            if not changed:
                return frozenset(E), nbr

    def kuratowski_graph(E, nbr):
        V = list(nbr)
        if len(V) == 5 and len(E) == 10:
            return True
        if len(V) == 6 and len(E) == 9 and all(len(nbr[x]) == 3 for x in V):
            col = {V[0]: 0}
            st = [V[0]]
            while st:
                x = st.pop()
                for y in nbr[x]:
                    if y not in col:
                        col[y] = 1 - col[x]
                        st.append(y)
                    elif col[y] == col[x]:
                        return False
            return sum(col.values()) == 3
        return False

    def nonplanar(E):
        E, nbr = reduce(E)
        if E in memo:
            return memo[E]
        k = len(nbr)
        if k >= 3 and len(E) > 3 * k - 6:
            r = True
        elif k <= 4:
            r = False
        elif kuratowski_graph(E, nbr):
            r = True
        else:
            r = any(nonplanar(E - {e}) for e in E)
        memo[E] = r
        return r

    return not nonplanar(frozenset((min(u, v), max(u, v)) for u, v in edges))


def random_triangulation(n, rng):
    """Edges of a random plane triangulation on n >= 3 vertices."""
    faces = [(0, 1, 2), (0, 2, 1)]
    E = {(0, 1), (0, 2), (1, 2)}
    for v in range(3, n):
        i = rng.randrange(len(faces))
        a, b, c = faces[i]
        faces[i] = faces[-1]
        faces.pop()
        faces += [(a, b, v), (b, c, v), (c, a, v)]
        E |= {(min(a, v), max(a, v)), (min(b, v), max(b, v)), (min(c, v), max(c, v))}
    return E


def to_adj(n, edges, rng=None):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    if rng is not None:
        for a in adj:
            rng.shuffle(a)
    return adj


def complete(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


K33 = [(a, b) for a in range(3) for b in range(3, 6)]
PETERSEN = ([(i, (i + 1) % 5) for i in range(5)] + [(i, i + 5) for i in range(5)]
            + [(5 + i, 5 + (i + 2) % 5) for i in range(5)])
OCTAHEDRON = [(i, j) for i in range(6) for j in range(i + 1, 6) if j != i + 3]


def subdivide(n, edges, k):
    """Replace every edge by a path with k inner vertices."""
    out = []
    for u, v in edges:
        prev = u
        for _ in range(k):
            out.append((prev, n))
            prev = n
            n += 1
        out.append((prev, v))
    return n, out


def random_case(rng):
    """A small random graph near the planarity threshold."""
    n = rng.randint(1, 9)
    if n >= 3 and rng.random() < 0.6:
        E = {e for e in random_triangulation(n, rng) if rng.random() < 0.85}
        for _ in range(rng.randint(0, 3)):
            u, v = rng.sample(range(n), 2)
            E.add((min(u, v), max(u, v)))
    else:
        p = rng.random()
        E = {(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p}
    perm = list(range(n))
    rng.shuffle(perm)
    return n, [(perm[u], perm[v]) for u, v in E]


def is_plane_rotation(adj, rot):
    """True if rot is a rotation system of adj whose faces satisfy Euler's
    formula n - m + f = 1 + c on every component (isolated vertices count
    one face each), that is, a planar embedding."""
    n = len(adj)
    if len(rot) != n:
        return False
    for v in range(n):
        if sorted(rot[v]) != sorted(adj[v]):
            return False
    pos = [{w: i for i, w in enumerate(r)} for r in rot]
    seen = set()
    faces = 0
    for v in range(n):
        for w in rot[v]:
            if (v, w) in seen:
                continue
            faces += 1
            a, b = v, w
            while (a, b) not in seen:
                seen.add((a, b))
                r = rot[b]
                a, b = b, r[(pos[b][a] + 1) % len(r)]
    comp = [-1] * n
    c = 0
    for s in range(n):
        if comp[s] == -1:
            comp[s] = c
            st = [s]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if comp[y] == -1:
                        comp[y] = c
                        st.append(y)
            c += 1
    m = sum(len(a) for a in adj) // 2
    isolated = sum(1 for v in range(n) if not adj[v])
    return n - m + faces + isolated == 2 * c


def is_kuratowski(adj, K):
    """True if the edge list K is a subgraph of adj that is a subdivision
    of K5 or K3,3."""
    nbr = {}
    for u, v in K:
        if v not in adj[u]:
            return False
        nbr.setdefault(u, set()).add(v)
        nbr.setdefault(v, set()).add(u)
    changed = True
    while changed:
        changed = False
        for x in list(nbr):
            if len(nbr[x]) == 2:
                a, b = nbr[x]
                if b in nbr[a]:
                    return False
                nbr[a].discard(x)
                nbr[b].discard(x)
                nbr[a].add(b)
                nbr[b].add(a)
                del nbr[x]
                changed = True
                break
    V = list(nbr)
    m = sum(len(s) for s in nbr.values()) // 2
    if any(len(nbr[x]) < 3 for x in V):
        return False
    if len(V) == 5 and m == 10:
        return True
    if len(V) == 6 and m == 9:
        col = {V[0]: 0}
        st = [V[0]]
        while st:
            x = st.pop()
            for y in nbr[x]:
                if y not in col:
                    col[y] = 1 - col[x]
                    st.append(y)
                elif col[y] == col[x]:
                    return False
        return sum(col.values()) == 3
    return False


@pytest.mark.parametrize("n,edges,expected", [
    (0, [], True),
    (1, [], True),
    (2, [(0, 1)], True),
    (3, [], True),
    (5, [(0, 1), (1, 2), (1, 3), (3, 4)], True),
    (4, complete(4), True),
    (5, complete(5), False),
    (6, K33, False),
    (6, K33[:-1], True),
    (5, complete(5)[:-1], True),
    (10, PETERSEN, False),
    (6, OCTAHEDRON, True),
])
def test_small_cases(n, edges, expected):
    adj = to_adj(n, edges)
    rot = planar_embedding(adj)
    assert (rot is not None) is expected
    assert is_planar(adj) is expected
    if expected:
        assert is_plane_rotation(adj, rot)
        assert kuratowski_subgraph(adj) is None
    else:
        assert is_kuratowski(adj, kuratowski_subgraph(adj))


def test_k4_rotation():
    rot = planar_embedding(to_adj(4, complete(4)))
    assert is_plane_rotation(to_adj(4, complete(4)), rot)
    assert len(rot) == 4 and all(len(r) == 3 for r in rot)


def test_random_against_oracle():
    rng = random.Random(2004)
    seen = [0, 0]
    for _ in range(1500):
        n, edges = random_case(rng)
        expected = oracle_planar(n, edges)
        seen[expected] += 1
        adj = to_adj(n, edges, rng)
        rot = planar_embedding(adj)
        assert (rot is not None) is expected, (n, edges)
        if expected:
            assert is_plane_rotation(adj, rot), (n, edges)
    assert min(seen) > 150


def test_certificates_on_medium_graphs():
    rng = random.Random(41)
    seen = [0, 0]
    for _ in range(150):
        n = rng.randint(10, 40)
        E = {e for e in random_triangulation(n, rng) if rng.random() < rng.choice([0.7, 1.0])}
        for _ in range(rng.choice([0, 1, 3])):
            u, v = rng.sample(range(n), 2)
            E.add((min(u, v), max(u, v)))
        adj = to_adj(n, E, rng)
        rot = planar_embedding(adj)
        seen[rot is not None] += 1
        if rot is not None:
            assert is_plane_rotation(adj, rot)
        else:
            assert is_kuratowski(adj, kuratowski_subgraph(adj))
    assert min(seen) > 20


def test_disconnected_and_cut_vertices():
    adj = to_adj(9, [(0, 1), (1, 2)] + [(u + 4, v + 4) for u, v in complete(5)])
    assert planar_embedding(adj) is None
    chain = []
    for b in range(50):
        chain += [(3 * b + u, 3 * b + v) for u, v in complete(4)]
    adj = to_adj(151, chain)
    assert is_plane_rotation(adj, planar_embedding(adj))


def test_large_inputs():
    rng = random.Random(5)
    n = 30000
    E = random_triangulation(n, rng)
    adj = to_adj(n, E, rng)
    assert is_plane_rotation(adj, planar_embedding(adj))
    u, v = 0, n - 1
    while (min(u, v), max(u, v)) in E:
        v -= 1
    E.add((min(u, v), max(u, v)))
    assert planar_embedding(to_adj(n, E, rng)) is None
    n = 200000
    adj = to_adj(n, [(i, (i + 1) % n) for i in range(n)])
    assert is_plane_rotation(adj, planar_embedding(adj))
    k = 150
    grid = [(i * k + j, i * k + j + 1) for i in range(k) for j in range(k - 1)]
    grid += [(i * k + j, (i + 1) * k + j) for i in range(k - 1) for j in range(k)]
    adj = to_adj(k * k, grid, rng)
    assert is_plane_rotation(adj, planar_embedding(adj))


def test_long_subdivisions():
    n, E = subdivide(6, K33, 2000)
    assert planar_embedding(to_adj(n, E)) is None
    n, E = subdivide(5, complete(5)[:-1], 2000)
    adj = to_adj(n, E)
    assert is_plane_rotation(adj, planar_embedding(adj))


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        planar_embedding([[0]])
    with pytest.raises(ValueError):
        planar_embedding([[1, 1], [0, 0]])
    with pytest.raises(ValueError):
        planar_embedding([[1], []])
    with pytest.raises(ValueError):
        planar_embedding([[3]])
