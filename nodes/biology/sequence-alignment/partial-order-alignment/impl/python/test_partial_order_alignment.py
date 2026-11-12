# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-order-alignment/. The authors are listed in prov/K4CMRB.jsonl.

import itertools
import random

from partial_order_alignment import (GAP, INDEL, POGraph, align_to_graph, fuse, pair_score,
                                     partial_order_alignment, sp_score)


def nw(s: str, t: str) -> int:
    """Reference: Needleman-Wunsch score with the same linear scores."""
    f = [[INDEL * (i + j) if i == 0 or j == 0 else 0 for j in range(len(t) + 1)] for i in range(len(s) + 1)]
    for i in range(1, len(s) + 1):
        for j in range(1, len(t) + 1):
            f[i][j] = max(f[i - 1][j - 1] + pair_score(s[i - 1], t[j - 1]), f[i - 1][j] + INDEL, f[i][j - 1] + INDEL)
    return f[len(s)][len(t)]


def exact_sp(seqs):
    """Reference: the best SP score by DP over the k-dimensional lattice."""
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
            c = sum(pair_score(col[i], col[j]) for i in range(k) for j in range(i + 1, k))
            if best[v] + c > best.get(w, -10 ** 9):
                best[w] = best[v] + c
    return best[tuple(lens)]


def source_sink_paths(g: POGraph):
    """Brute force: every path from a node without predecessors to a node without successors."""
    def walk(v):
        if not g.succs[v]:
            yield [v]
            return
        for w in g.succs[v]:
            for rest in walk(w):
                yield [v] + rest
    for v in range(len(g.base)):
        if not g.preds[v]:
            yield from walk(v)


def is_alignment_of(rows, seqs):
    if len(rows) != len(seqs) or len({len(r) for r in rows}) > 1:
        return False
    if rows and any(all(r[p] == GAP for r in rows) for p in range(len(rows[0]))):
        return False
    return all(r.replace(GAP, "") == s for r, s in zip(rows, seqs))


def check_graph(g: POGraph, seqs):
    # each sequence is spelled by its path, and its path follows edges labeled with it
    for sid, (path, s) in enumerate(zip(g.paths, seqs)):
        assert "".join(g.base[v] for v in path) == s
        for a, b in zip(path, path[1:]):
            assert sid in g.labels[a, b]
    # the column order is a topological order: every edge goes to a later column
    pos = {c: i for i, c in enumerate(g.columns)}
    for (a, b) in g.labels:
        assert pos[g.col_of[a]] < pos[g.col_of[b]]
    # a column never holds two nodes with the same letter
    for c, vs in g.members.items():
        letters = [g.base[v] for v in vs]
        assert len(letters) == len(set(letters))


def rand_seq(rng, lo, hi, alpha="ACGT"):
    return "".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi)))


def mutate(rng, base):
    s = list(base)
    for _ in range(rng.randint(0, 2)):
        op = rng.random()
        if s and op < 0.4:
            s[rng.randrange(len(s))] = rng.choice("ACGT")
        elif s and op < 0.7:
            del s[rng.randrange(len(s))]
        else:
            s.insert(rng.randint(0, len(s)), rng.choice("ACGT"))
    return "".join(s)


def test_example():
    seqs = ["ACGT", "AGGTT", "ACGTT"]
    rows, g = partial_order_alignment(seqs)
    assert rows == ["ACG-T", "AGGTT", "ACGTT"]
    assert len(g.base) == 6
    a, c, t1 = g.paths[0][0], g.paths[0][1], g.paths[0][3]
    assert g.paths[2][:2] == [a, c]                # the third sequence uses C from the first
    assert g.paths[2][3:] == g.paths[1][3:]        # and the extra T from the second
    assert g.paths[2][4] == t1
    sub = POGraph()
    for s in seqs[:2]:
        fuse(sub, s, align_to_graph(sub, s)[1] if sub.base else [(None, j) for j in range(len(s))])
    assert align_to_graph(sub, seqs[2])[0] == 5   # all five letters match a path
    assert sp_score(rows) == exact_sp(seqs) == 5


def test_edges():
    assert partial_order_alignment([])[0] == []
    assert partial_order_alignment(["ACG"])[0] == ["ACG"]
    assert partial_order_alignment(["AC", "AC", "AC"])[0] == ["AC", "AC", "AC"]
    assert len(partial_order_alignment(["AC", "AC", "AC"])[1].base) == 2
    for seqs in (["", "AT"], ["AT", ""], ["A", "", "AT"], ["", ""]):
        rows, g = partial_order_alignment(seqs)
        assert is_alignment_of(rows, seqs)


def test_graph_dp_matches_brute_force_over_paths():
    rng = random.Random(1)
    for _ in range(150):
        base = rand_seq(rng, 1, 5)
        seqs = [mutate(rng, base) for _ in range(rng.randint(1, 4))]
        seqs = [s or "A" for s in seqs]
        _, g = partial_order_alignment(seqs)
        y = mutate(rng, base)
        score, pairs = align_to_graph(g, y)
        want = max(nw("".join(g.base[v] for v in p), y) for p in source_sink_paths(g))
        assert score == want
        # the traceback follows edges, uses every letter of y once, and has the reported score
        nodes = [v for v, _ in pairs if v is not None]
        assert all(b in g.succs[a] for a, b in zip(nodes, nodes[1:]))
        assert not g.preds[nodes[0]] and not g.succs[nodes[-1]]
        assert [j for _, j in pairs if j is not None] == list(range(len(y)))
        got = sum(pair_score(GAP if v is None else g.base[v], GAP if j is None else y[j]) for v, j in pairs)
        assert got == score


def test_single_path_graph_equals_needleman_wunsch():
    rng = random.Random(2)
    for _ in range(200):
        s, t = rand_seq(rng, 1, 7), rand_seq(rng, 0, 7)
        g = POGraph()
        fuse(g, s, [(None, j) for j in range(len(s))])
        assert align_to_graph(g, t)[0] == nw(s, t)
        rows, _ = partial_order_alignment([s, t])
        assert is_alignment_of(rows, [s, t])
        assert sp_score(rows) == nw(s, t)


def test_valid_output_and_graph_invariants():
    rng = random.Random(3)
    for _ in range(150):
        base = rand_seq(rng, 0, 8)
        seqs = [mutate(rng, base) for _ in range(rng.randint(1, 6))]
        rows, g = partial_order_alignment(seqs)
        assert is_alignment_of(rows, seqs)
        check_graph(g, seqs)
        assert len(g.base) <= sum(len(s) for s in seqs)


def test_identical_sequences_share_all_nodes():
    rng = random.Random(4)
    for _ in range(30):
        s = rand_seq(rng, 1, 8)
        rows, g = partial_order_alignment([s] * 4)
        assert rows == [s] * 4
        assert len(g.base) == len(s)


def test_three_sequences_bounded_by_exact():
    rng = random.Random(5)
    hits = 0
    for _ in range(60):
        base = rand_seq(rng, 2, 5)
        seqs = [mutate(rng, base) for _ in range(3)]
        rows, _ = partial_order_alignment(seqs)
        assert is_alignment_of(rows, seqs)
        best = exact_sp(seqs)
        assert sp_score(rows) <= best
        hits += sp_score(rows) == best
    assert hits > 0
