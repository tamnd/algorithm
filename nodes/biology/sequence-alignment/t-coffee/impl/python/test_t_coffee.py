# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-coffee/. The authors are listed in prov/RYMMF1.jsonl.

import itertools
import random
from fractions import Fraction

from t_coffee import (GAP, extend_library, global_pairs, library_score, local_pairs,
                      neighbor_joining_order, pair_score, primary_library, sp_score, t_coffee)


def lattice_max(seqs, column_score):
    """Oracle: the best total of column_score over all alignments, by DP over the k-dimensional lattice."""
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
            c = column_score(v, m)
            if best[v] + c > best.get(w, -10 ** 9):
                best[w] = best[v] + c
    return best[tuple(lens)]


def exact_sp(seqs):
    def col(v, m):
        c = [seqs[i][v[i]] if m[i] else GAP for i in range(len(seqs))]
        return sum(pair_score(c[i], c[j]) for i in range(len(c)) for j in range(i + 1, len(c)))
    return lattice_max(seqs, col)


def exact_library(seqs, ext):
    def col(v, m):
        res = [(i, v[i]) for i in range(len(seqs)) if m[i]]
        return sum(ext.get((res[a], res[b]), 0) for a in range(len(res)) for b in range(a + 1, len(res)))
    return lattice_max(seqs, col)


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


def score_of_pairs(s, t, pairs):
    """Score of the alignment that matches exactly these pairs and gaps the rest, compactly."""
    if not pairs:
        return 0
    (p0, q0), (p1, q1) = pairs[0], pairs[-1]
    total = sum(pair_score(s[p], t[q]) for p, q in pairs)
    for (a, b), (c, d) in zip(pairs, pairs[1:]):
        total -= 2 * ((c - a - 1) + (d - b - 1))
    return total


def is_alignment_of(rows, seqs):
    if len(rows) != len(seqs) or len({len(r) for r in rows}) > 1:
        return False
    if rows and any(all(r[p] == GAP for r in rows) for p in range(len(rows[0]))):
        return False
    return all(r.replace(GAP, "") == s for r, s in zip(rows, seqs))


def rand_seq(rng, lo, hi, alpha="ACGT"):
    return "".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi)))


def test_example():
    seqs = ["AGGC", "AGC", "AGCC"]
    w = primary_library(seqs)
    assert w[(0, 1), (1, 1)] == 100 and w[(0, 2), (1, 1)] == 100
    ext = extend_library(w, seqs)
    assert ext[(0, 1), (1, 1)] == 275 and ext[(0, 2), (1, 1)] == 100
    rows = t_coffee(seqs)
    assert rows == ["AGGC", "AG-C", "AGCC"]
    assert sp_score(rows) == exact_sp(seqs) == 4
    assert sp_score(["AGGC", "A-GC", "AGCC"]) == 2


def test_edges():
    assert t_coffee([]) == []
    assert t_coffee(["ACG"]) == ["ACG"]
    assert t_coffee(["AC", "AC", "AC"]) == ["AC", "AC", "AC"]
    assert is_alignment_of(t_coffee(["A", "", "AT"]), ["A", "", "AT"])
    assert is_alignment_of(t_coffee(["AAAA", "CCCC"]), ["AAAA", "CCCC"])


def test_global_and_local_pairs_are_optimal():
    rng = random.Random(1)
    for _ in range(150):
        s, t = rand_seq(rng, 0, 4), rand_seq(rng, 0, 4)
        best = max(sum(pair_score(x, y) for x, y in zip(a, b)) for a, b in all_pair_alignments(s, t))
        g = global_pairs(s, t)
        unmatched = len(s) + len(t) - 2 * len(g)
        assert sum(pair_score(s[p], t[q]) for p, q in g) - 2 * unmatched == best
        best_local = 0
        for i in range(len(s)):
            for i2 in range(i + 1, len(s) + 1):
                for j in range(len(t)):
                    for j2 in range(j + 1, len(t) + 1):
                        for a, b in all_pair_alignments(s[i:i2], t[j:j2]):
                            best_local = max(best_local, sum(pair_score(x, y) for x, y in zip(a, b)))
        lp = local_pairs(s, t)
        assert all(a < c and b < d for (a, b), (c, d) in zip(lp, lp[1:]))
        assert score_of_pairs(s, t, lp) == best_local


def test_extension_matches_its_definition():
    rng = random.Random(2)
    for _ in range(30):
        seqs = [rand_seq(rng, 1, 4) for _ in range(rng.randint(2, 4))]
        w = primary_library(seqs)
        ext = extend_library(w, seqs)
        res = [(i, p) for i in range(len(seqs)) for p in range(len(seqs[i]))]
        for x in res:
            for y in res:
                if x[0] >= y[0]:
                    continue
                want = w.get((x, y), 0) + sum(min(w.get((x, z), 0), w.get((z, y), 0))
                                              for z in res if z[0] not in (x[0], y[0]))
                assert ext.get((x, y), 0) == want == ext.get((y, x), 0)


def test_neighbor_joining_recovers_additive_splits():
    rng = random.Random(3)
    for _ in range(40):
        k = rng.randint(3, 7)
        # random unrooted binary tree by inserting leaves on random edges
        edges = {(0, 1): rng.randint(1, 5), (0, 2): rng.randint(1, 5), (0, 3): rng.randint(1, 5)} if k >= 3 else {}
        leaf_node = {0: 1, 1: 2, 2: 3}
        nxt = 4
        for leaf in range(3, k):
            (a, b), ln = rng.choice(sorted(edges.items()))
            del edges[a, b]
            mid, tip = nxt, nxt + 1
            nxt += 2
            edges[a, mid] = edges[mid, b] = ln
            edges[mid, tip] = rng.randint(1, 5)
            leaf_node[leaf] = tip
        adj = {}
        for (a, b), ln in edges.items():
            adj.setdefault(a, []).append((b, ln))
            adj.setdefault(b, []).append((a, ln))

        def dists(src):
            out, stack = {src: 0}, [src]
            while stack:
                u = stack.pop()
                for v, ln in adj[u]:
                    if v not in out:
                        out[v] = out[u] + ln
                        stack.append(v)
            return out

        d = [[Fraction(dists(leaf_node[i])[leaf_node[j]]) for j in range(k)] for i in range(k)]
        full = frozenset(range(k))

        def norm(s):
            return min(s, full - s, key=lambda x: sorted(x))

        true_splits = set()
        for (a, b) in edges:
            side = dists_without(adj, a, b)
            leaves = frozenset(i for i in range(k) if leaf_node[i] in side)
            if 1 < len(leaves) < k - 1:
                true_splits.add(norm(leaves))
        got = set()

        def walk(t):
            if isinstance(t, int):
                return frozenset([t])
            s = walk(t[0]) | walk(t[1])
            if 1 < len(s) < k - 1:
                got.add(norm(s))
            return s

        walk(neighbor_joining_order(d))
        assert got == true_splits


def dists_without(adj, a, b):
    """Nodes reachable from b without using the edge (a, b)."""
    seen, stack = {b}, [b]
    while stack:
        u = stack.pop()
        for v, _ in adj[u]:
            if v not in seen and not (u == b and v == a):
                seen.add(v)
                stack.append(v)
    return seen


def test_two_sequences_maximize_the_library_score():
    rng = random.Random(4)
    for _ in range(60):
        s, t = rand_seq(rng, 0, 5), rand_seq(rng, 0, 5)
        ext = extend_library(primary_library([s, t]), [s, t])
        rows = t_coffee([s, t])
        assert is_alignment_of(rows, [s, t])
        best = max(library_score([a, b], ext) for a, b in all_pair_alignments(s, t))
        assert library_score(rows, ext) == best


def test_three_sequences_against_exact_optima():
    rng = random.Random(2024)
    for _ in range(30):
        seqs = [rand_seq(rng, 1, 4, "ACG") for _ in range(3)]
        rows = t_coffee(seqs)
        assert is_alignment_of(rows, seqs)
        assert sp_score(rows) <= exact_sp(seqs)
        ext = extend_library(primary_library(seqs), seqs)
        assert library_score(rows, ext) <= exact_library(seqs, ext)
