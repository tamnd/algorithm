# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clustal/. The authors are listed in prov/CZRQ68.jsonl.

import itertools
import random
from fractions import Fraction

from clustal import (GAP, clustal, dna_score, midpoint_root, neighbor_joining, nw,
                     sequence_weights, sp_score)


def exact_sp(seqs, score=dna_score):
    """Oracle: the maximum SP score, by dynamic programming over the k-dimensional lattice."""
    k = len(seqs)
    lens = [len(s) for s in seqs]
    best = {tuple([0] * k): 0}
    moves = [m for m in itertools.product((0, 1), repeat=k) if any(m)]
    for v in sorted(itertools.product(*[range(n + 1) for n in lens]), key=sum):
        if v not in best:
            continue
        for m in moves:
            w = tuple(a + b for a, b in zip(v, m))
            if any(w[i] > lens[i] for i in range(k)):
                continue
            col = [seqs[i][v[i]] if m[i] else GAP for i in range(k)]
            c = sum(score(col[i], col[j]) for i in range(k) for j in range(i + 1, k))
            if best[v] + c > best.get(w, -10**9):
                best[w] = best[v] + c
    return best[tuple(lens)]


def all_pair_alignments(s, t):
    if not s and not t:
        yield "", ""
        return
    if s and t:
        for a, b in all_pair_alignments(s[1:], t[1:]):
            yield s[0] + a, t[0] + b
    if s:
        for a, b in all_pair_alignments(s[1:], t):
            yield s[0] + a, GAP + b
    if t:
        for a, b in all_pair_alignments(s, t[1:]):
            yield GAP + a, t[0] + b


def is_alignment_of(rows, seqs):
    if len(rows) != len(seqs) or len({len(r) for r in rows}) > 1:
        return False
    if rows and any(all(r[p] == GAP for r in rows) for p in range(len(rows[0]))):
        return False
    return all(r.replace(GAP, "") == s for r, s in zip(rows, seqs))


def tree_distance(adj, a, b):
    dist, stack = {a: Fraction(0)}, [a]
    while stack:
        u = stack.pop()
        for v, ln in adj[u].items():
            if v not in dist:
                dist[v] = dist[u] + ln
                stack.append(v)
    return dist[b]


def random_additive(rng, n):
    """Leaf distances of a random tree with positive integer branch lengths."""
    adj = {0: {}, 1: {}}
    adj[0][1] = adj[1][0] = Fraction(rng.randint(1, 5))
    leaves, nxt = [0, 1], 2
    while len(leaves) < n:
        u = rng.choice([x for x in adj])
        v = rng.choice(list(adj[u]))
        ln = adj[u].pop(v)
        adj[v].pop(u)
        mid, leaf = nxt, nxt + 1
        nxt += 2
        cut = Fraction(rng.randint(1, 4))
        adj[mid] = {u: cut, v: ln + cut, leaf: Fraction(rng.randint(1, 5))}
        adj[u][mid] = cut
        adj[v][mid] = ln + cut
        adj[leaf] = {mid: adj[mid][leaf]}
        leaves.append(leaf)
    return [[tree_distance(adj, a, b) for b in leaves] for a in leaves]


def test_example():
    seqs = ["ACGTTGCA", "ACGTGCA", "AGGTTGCA", "ACTTGA"]
    rows = clustal(seqs)
    assert rows == ["ACGTTGCA", "AC-GTGCA", "AGGTTGCA", "AC-TTG-A"]
    assert sp_score(rows) == 14
    assert exact_sp(seqs) == 15
    assert sp_score(["ACGTTGCA", "ACG-TGCA", "AGGTTGCA", "AC-TTG-A"]) == 15


def test_edges():
    assert clustal([]) == []
    assert clustal(["ACG"]) == ["ACG"]
    assert clustal(["AC", "AC", "AC"]) == ["AC", "AC", "AC"]
    rows = clustal(["", "A", "AA"])
    assert is_alignment_of(rows, ["", "A", "AA"])


def test_nw_against_enumeration():
    rng = random.Random(1)
    for _ in range(200):
        s = "".join(rng.choice("AC") for _ in range(rng.randint(0, 4)))
        t = "".join(rng.choice("AC") for _ in range(rng.randint(0, 4)))
        best = max(sum(dna_score(x, y) for x, y in zip(a, b)) for a, b in all_pair_alignments(s, t))
        sc, a, b = nw(s, t, dna_score)
        assert sc == best == sum(dna_score(x, y) for x, y in zip(a, b))


def test_neighbor_joining_recovers_additive_distances():
    rng = random.Random(5)
    for _ in range(40):
        n = rng.randint(2, 7)
        d = random_additive(rng, n)
        adj = neighbor_joining(d)
        for a in range(n):
            for b in range(n):
                assert tree_distance(adj, a, b) == d[a][b]


def test_midpoint_and_weights():
    rng = random.Random(9)
    for _ in range(40):
        n = rng.randint(2, 6)
        d = random_additive(rng, n)
        adj = neighbor_joining(d)
        root, children, up = midpoint_root(adj, list(range(n)))
        depth = {}

        def walk(x, acc):
            depth[x] = acc
            for y in children[x]:
                walk(y, acc + up[y])

        walk(root, Fraction(0))
        diam = max(d[a][b] for a in range(n) for b in range(n))
        assert max(depth[x] for x in range(n)) == diam / 2
        assert len(children[root]) == 2
        w = sequence_weights(root, children, up, list(range(n)))
        assert all(w[x] > 0 for x in range(n))
        assert sum(w[x] for x in range(n)) == sum(up[x] for x in up if x != root)


def test_two_sequences_equal_needleman_wunsch():
    rng = random.Random(3)
    for _ in range(100):
        s = "".join(rng.choice("ACGT") for _ in range(rng.randint(0, 6)))
        t = "".join(rng.choice("ACGT") for _ in range(rng.randint(0, 6)))
        rows = clustal([s, t])
        assert is_alignment_of(rows, [s, t]) or not (s or t)
        assert sp_score(rows) == nw(s, t, dna_score)[0]


def test_three_sequences_against_exact_sp():
    rng = random.Random(2024)
    for _ in range(80):
        seqs = ["".join(rng.choice("ACG") for _ in range(rng.randint(1, 5))) for _ in range(3)]
        rows = clustal(seqs)
        assert is_alignment_of(rows, seqs)
        assert sp_score(rows) <= exact_sp(seqs)
