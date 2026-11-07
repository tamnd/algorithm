# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cuthill-mckee/. The authors are listed in prov/9BQFTQ.jsonl.

import random
from fractions import Fraction as F

from cuthill_mckee import (bandwidth, cuthill_mckee, graph_from_csr, graph_from_dense,
                           levels, permute, profile, pseudo_peripheral, reverse_cuthill_mckee)


def rand_graph(rng, n, p):
    nb = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                nb[i].add(j)
                nb[j].add(i)
    return [sorted(s) for s in nb]


def grid(k):
    adj = [[] for _ in range(k * k)]
    for i in range(k):
        for j in range(k):
            v = i * k + j
            if i + 1 < k:
                adj[v].append(v + k)
                adj[v + k].append(v)
            if j + 1 < k:
                adj[v].append(v + 1)
                adj[v + 1].append(v)
    return [sorted(a) for a in adj]


def components(adj, order):
    """Split order into its components (maximal runs closed under adjacency)."""
    f = {v: k for k, v in enumerate(order)}
    out, k = [], 0
    while k < len(order):
        comp = {order[k]}
        for lv in levels(adj, order[k]):
            comp.update(lv)
        out.append(order[k:k + len(comp)])
        assert set(out[-1]) == comp, "component not contiguous"
        k += len(comp)
    return out, f


def check_cm_structure(adj, order):
    """The characterization: inside each component, after the root, vertices
    appear sorted by (number of first numbered neighbour, degree, index)."""
    comps, f = components(adj, order)
    for comp in comps:
        keys = []
        for v in comp[1:]:
            parent = min(f[w] for w in adj[v])
            assert parent < f[v]
            keys.append((parent, len(adj[v]), v))
        assert keys == sorted(keys)
        lv = levels(adj, comp[0])
        # numbering follows the level structure
        pos = 0
        for level in lv:
            assert set(comp[pos:pos + len(level)]) == set(level)
            pos += len(level)
        bound = max([len(lv[i]) + len(lv[i + 1]) - 1 for i in range(len(lv) - 1)] + [0])
        sub_bw = max([abs(f[v] - f[w]) for v in comp for w in adj[v]] + [0])
        assert sub_bw <= bound


def test_page_example():
    adj = [[3, 5], [2, 4], [1, 5], [0, 4], [1, 3], [0, 2]]
    assert cuthill_mckee(adj) == [0, 3, 5, 4, 2, 1]
    assert bandwidth(adj, list(range(6))) == 5
    assert bandwidth(adj, cuthill_mckee(adj)) == 2
    assert pseudo_peripheral(adj, 0) == 0


def test_random_graphs_structure_and_permutation():
    rng = random.Random(9101)
    for t in range(500):
        n = rng.randint(1, 30)
        adj = rand_graph(rng, n, rng.choice([0.05, 0.1, 0.2, 0.5]))
        for peripheral in (True, False):
            order = cuthill_mckee(adj, peripheral=peripheral)
            assert sorted(order) == list(range(n))
            check_cm_structure(adj, order)


def test_reverse_never_increases_profile():
    # Liu and Sherman (1976): the envelope of RCM is at most that of CM.
    rng = random.Random(77)
    strict = 0
    for t in range(500):
        n = rng.randint(2, 25)
        adj = rand_graph(rng, n, rng.choice([0.08, 0.15, 0.3]))
        cm = cuthill_mckee(adj)
        rcm = reverse_cuthill_mckee(adj)
        assert rcm == cm[::-1]
        assert bandwidth(adj, rcm) == bandwidth(adj, cm)
        assert profile(adj, rcm) <= profile(adj, cm)
        strict += profile(adj, rcm) < profile(adj, cm)
    assert strict > 50


def test_fill_stays_in_envelope():
    # Cholesky (here exact LDL^T) of P A P^T has no fill outside the envelope.
    rng = random.Random(5)
    for t in range(60):
        n = rng.randint(2, 12)
        adj = rand_graph(rng, n, 0.25)
        a = [[F(0)] * n for _ in range(n)]
        for i in range(n):
            for j in adj[i]:
                a[i][j] = F(-1)
            a[i][i] = F(len(adj[i]) + 1)  # strictly diagonally dominant, SPD
        order = reverse_cuthill_mckee(adj)
        b = permute(a, order)
        first = [min([j for j in range(n) if b[i][j] != 0]) for i in range(n)]
        m = [row[:] for row in b]
        for k in range(n):
            for i in range(k + 1, n):
                l = m[i][k] / m[k][k]
                for j in range(k, n):
                    m[i][j] -= l * m[k][j]
                m[i][k] = l
        for i in range(n):
            for j in range(first[i]):
                assert m[i][j] == 0
        assert max(i - j for i in range(n) for j in range(i + 1) if m[i][j] != 0) <= bandwidth(adj, order)


def test_paths_cycles_grid():
    rng = random.Random(3)
    for n in range(2, 40):
        lab = list(range(n))
        rng.shuffle(lab)
        adj = [[] for _ in range(n)]
        for i in range(n - 1):
            adj[lab[i]].append(lab[i + 1])
            adj[lab[i + 1]].append(lab[i])
        adj = [sorted(x) for x in adj]
        assert bandwidth(adj, cuthill_mckee(adj)) == 1
        if n >= 3:
            adj[lab[0]].append(lab[-1])
            adj[lab[-1]].append(lab[0])
            adj = [sorted(x) for x in adj]
            assert bandwidth(adj, cuthill_mckee(adj)) == 2
    for k in (2, 3, 5, 8, 12):
        g = grid(k)
        o = cuthill_mckee(g)
        assert bandwidth(g, o) == k
        assert profile(g, o) <= profile(g, list(range(k * k)))


def test_star_is_a_bad_case():
    for n in (3, 5, 10, 21):
        adj = [list(range(1, n))] + [[0] for _ in range(n - 1)]
        o = cuthill_mckee(adj)
        assert bandwidth(adj, o) == n - 2
        best = [i for i in range(1, n)]
        mid = (n - 1) // 2
        opt = best[:mid] + [0] + best[mid:]
        assert bandwidth(adj, opt) == (n - 1 + 1) // 2


def test_degree_lower_bound():
    rng = random.Random(11)
    for t in range(200):
        n = rng.randint(2, 20)
        adj = rand_graph(rng, n, 0.3)
        d = max(len(x) for x in adj)
        assert bandwidth(adj, cuthill_mckee(adj)) >= (d + 1) // 2


def test_edge_cases_and_helpers():
    assert cuthill_mckee([]) == []
    assert cuthill_mckee([[]]) == [0]
    assert cuthill_mckee([[], [], []]) == [0, 1, 2]
    assert bandwidth([[], []], [1, 0]) == 0
    a = [[4, 1, 0, 0], [1, 4, 0, 2], [0, 0, 4, 0], [0, 2, 0, 4]]
    g = graph_from_dense(a)
    ptr, ind = [0], []
    for row in a:
        ind += [j for j, v in enumerate(row) if v]
        ptr.append(len(ind))
    assert graph_from_csr(4, ptr, ind) == g == [[1], [0, 3], [], [1]]
    assert cuthill_mckee(g, start=3, peripheral=False)[:3] == [3, 1, 0]
