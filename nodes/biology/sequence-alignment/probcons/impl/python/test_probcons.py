# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probcons/. The authors are listed in prov/VPNKKD.jsonl.

import itertools
import random

from probcons import (GAP, P_DIFF, P_SAME, Q, TRANS, consistency, drop_gap_columns, expected_score,
                      guide_tree, mea_score, pair_score, posteriors, probcons, progressive, refine,
                      sp_score, transpose)

EPS = 1e-9


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


def path_probability(a, b):
    """Probability of one alignment under the pair-HMM, starting in M."""
    prob, state = 1.0, 0
    for x, y in zip(a, b):
        nxt = 0 if (x != GAP and y != GAP) else (1 if y == GAP else 2)
        prob *= TRANS[state][nxt] * (Q if nxt else (P_SAME if x == y else P_DIFF))
        state = nxt
    return prob


def matched(a, b):
    out, i, j = set(), 0, 0
    for x, y in zip(a, b):
        if x != GAP and y != GAP:
            out.add((i, j))
        i += x != GAP
        j += y != GAP
    return out


def is_alignment_of(rows, seqs):
    if len(rows) != len(seqs) or len({len(r) for r in rows}) > 1:
        return False
    if rows and any(all(r[p] == GAP for r in rows) for p in range(len(rows[0]))):
        return False
    return all(r.replace(GAP, "") == s for r, s in zip(rows, seqs))


def rand_seq(rng, lo, hi, alpha="ACGT"):
    return "".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi)))


def all_posteriors(seqs):
    post = {}
    for x in range(len(seqs)):
        for y in range(x + 1, len(seqs)):
            post[x, y] = posteriors(seqs[x], seqs[y])
            post[y, x] = transpose(post[x, y], len(seqs[x]), len(seqs[y]))
    return post


def test_example():
    seqs = ["GGAG", "GTGAG", "GTAG"]
    post = all_posteriors(seqs)
    e = {}
    for x, y in post:
        e[x, y] = mea_score(post[x, y], len(seqs[x]), len(seqs[y])) / min(len(seqs[x]), len(seqs[y]))
    tree = guide_tree(e, 3)
    assert tree == (0, (1, 2))
    plain = progressive(tree, seqs, post)
    assert [plain[i] for i in range(3)] == ["G-GAG", "GTGAG", "GT-AG"]
    rows = probcons(seqs)
    assert rows == ["GG-AG", "GTGAG", "GT-AG"]
    assert sp_score([plain[i] for i in range(3)]) == 3
    assert sp_score(rows) == exact_sp(seqs) == 4


def test_edges():
    assert probcons([]) == []
    assert probcons(["ACG"]) == ["ACG"]
    assert probcons(["AC", "AC", "AC"]) == ["AC", "AC", "AC"]
    assert is_alignment_of(probcons(["A", "", "AT"]), ["A", "", "AT"])


def test_posteriors_match_enumeration():
    rng = random.Random(1)
    for _ in range(60):
        s, t = rand_seq(rng, 0, 4), rand_seq(rng, 0, 4)
        alns = list(all_pair_alignments(s, t))
        probs = [path_probability(a, b) for a, b in alns]
        z = sum(probs)
        p = posteriors(s, t)
        for i in range(len(s)):
            for j in range(len(t)):
                want = sum(pr for (a, b), pr in zip(alns, probs) if (i, j) in matched(a, b)) / z
                assert abs(p[i][j] - want) < EPS


def test_mea_matches_enumeration():
    rng = random.Random(2)
    for _ in range(60):
        s, t = rand_seq(rng, 0, 4), rand_seq(rng, 0, 4)
        p = posteriors(s, t)
        want = max(sum(p[i][j] for i, j in matched(a, b)) for a, b in all_pair_alignments(s, t))
        assert abs(mea_score(p, len(s), len(t)) - want) < EPS


def test_consistency_matches_its_definition():
    rng = random.Random(3)
    for _ in range(20):
        seqs = [rand_seq(rng, 1, 4) for _ in range(rng.randint(2, 4))]
        post = all_posteriors(seqs)
        new = consistency(post, seqs)
        k = len(seqs)
        for x in range(k):
            for y in range(k):
                if x == y:
                    continue
                for i in range(len(seqs[x])):
                    for j in range(len(seqs[y])):
                        total = 0.0
                        for z in range(k):
                            for t in range(len(seqs[z])):
                                a = (1.0 if i == t else 0.0) if z == x else post[x, z][i][t]
                                b = (1.0 if t == j else 0.0) if z == y else post[z, y][t][j]
                                total += a * b
                        assert abs(new[x, y][i][j] - total / k) < EPS


def test_guide_tree_rule():
    e = {(0, 1): 0.9, (0, 2): 0.5, (1, 2): 0.7, (0, 3): 0.1, (1, 3): 0.2, (2, 3): 0.6}
    e.update({(b, a): v for (a, b), v in list(e.items())})
    # merge 0,1 (0.9); E(01, 2) = 0.9 * 0.6 = 0.54 < E(2, 3) = 0.6, so 2 and 3 merge next
    assert guide_tree(e, 4) == ((0, 1), (2, 3))


def test_two_sequences_are_mea_optimal():
    rng = random.Random(4)
    for _ in range(50):
        s, t = rand_seq(rng, 0, 4), rand_seq(rng, 0, 4)
        rows = probcons([s, t], rounds=5)
        assert is_alignment_of(rows, [s, t])
        post = consistency(consistency(all_posteriors([s, t]), [s, t]), [s, t])
        best = max(expected_score([a, b], post) for a, b in all_pair_alignments(s, t))
        assert abs(expected_score(rows, post) - best) < EPS


def test_refinement_is_monotone_and_three_sequences_bounded_by_exact():
    rng = random.Random(2024)
    for _ in range(25):
        seqs = [rand_seq(rng, 1, 4, "ACG") for _ in range(3)]
        post = consistency(consistency(all_posteriors(seqs), seqs), seqs)
        start = progressive((0, (1, 2)), seqs, post)
        score = expected_score([start[i] for i in range(3)], post)
        aln = start
        r = random.Random(7)
        for _ in range(5):
            aln = refine(aln, post, 1, r)
            new = expected_score([aln[i] for i in range(3)], post)
            assert new >= score - EPS
            score = new
        rows = probcons(seqs, rounds=10)
        assert is_alignment_of(rows, seqs)
        assert sp_score(rows) <= exact_sp(seqs)

        def col(v, m):
            res = [(i, v[i]) for i in range(3) if m[i]]
            return sum(post[a[0], b[0]][a[1]][b[1]] for x, a in enumerate(res) for b in res[x + 1:])

        assert expected_score(rows, post) <= lattice_max(seqs, col) + EPS


def test_drop_gap_columns():
    assert drop_gap_columns(["A-C", "--G"]) == ["AC", "-G"]
