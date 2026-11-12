# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rna-folding-kinetics/. The authors are listed in prov/ZN8CDJ.jsonl.

import itertools
import random
from fractions import Fraction

from rna_folding_kinetics import (PAIRS, Model, adjacency, all_structures, barrier_tree, boltzmann, energy,
                                  gillespie, local_minima, mean_first_passage, neighbors, rate_matrix,
                                  saddle_energy_bfs, stationary_distribution, to_dot_bracket)


def brute_structures(s, m=3):
    """All sets of allowed pairs with the hairpin minimum, no shared base and no crossing."""
    n = len(s)
    cand = [(i, j) for i in range(n) for j in range(i + m + 1, n) if (s[i], s[j]) in PAIRS]
    out = set()
    for r in range(n // 2 + 1):
        for sub in itertools.combinations(cand, r):
            used = [x for p in sub for x in p]
            if len(used) != len(set(used)):
                continue
            if any(i < k < j < l for (i, j) in sub for (k, l) in sub):
                continue
            out.add(frozenset(sub))
    return out


def random_seq(rng, n):
    return "".join(rng.choice("ACGU") for _ in range(n))


def small_seqs(rng, count, max_states):
    out = []
    while len(out) < count:
        s = random_seq(rng, rng.randrange(5, 12))
        if len(all_structures(s)) <= max_states:
            out.append(s)
    return out


def test_structures_match_brute_force():
    rng = random.Random(11)
    for s in ["GGGAAACCC", "GCAAAGCAAAGC", "AAAAAAA"] + [random_seq(rng, rng.randrange(1, 11)) for _ in range(40)]:
        assert set(all_structures(s)) == brute_structures(s)


def test_move_set_is_symmetric_and_changes_one_pair():
    rng = random.Random(3)
    for s in ["GGGAAACCC"] + small_seqs(rng, 10, 60):
        sts = set(all_structures(s))
        for p in sts:
            for q in neighbors(s, p):
                assert q in sts
                assert len(p ^ q) == 1
                assert p in neighbors(s, q)


def test_stationary_distribution_is_boltzmann():
    rng = random.Random(2024)
    seqs = ["GGGAAACCC"] + small_seqs(rng, 6, 35)
    for s in seqs:
        for z in [Fraction(1, 2), Fraction(1, 3), Fraction(4, 5)]:
            states, energies, rates = rate_matrix(s, z)
            pi = stationary_distribution(len(states), rates)
            assert pi == boltzmann(energies, z)
            for (x, y), k in rates.items():  # detailed balance
                assert pi[x] * k == pi[y] * rates[(y, x)]


def test_barrier_tree_matches_threshold_search():
    rng = random.Random(17)
    seqs = ["GGGAAACCC", "GGCAAAGCCAAAGGC", "GGCCAAAGGCCAAAGGCC"] + small_seqs(rng, 15, 300)
    for s in seqs:
        for model in [Model(), Model(a=2, b=3), Model(a=1, b=1)]:
            states = all_structures(s, model)
            es = [energy(st, model) for st in states]
            adj = adjacency(s, states, model)
            minima, merges = barrier_tree(states, es, adj)
            assert minima == sorted(local_minima(states, es, adj), key=lambda x: (es[x], x))
            assert len(merges) == len(minima) - 1
            for e, lo, up in merges:
                assert (es[lo], lo) < (es[up], up)
                assert e == saddle_energy_bfs(es, adj, lo, up)
            for a, b in itertools.combinations(minima[:6], 2):
                # the saddle of two minima is the highest merge on the tree path between them
                assert saddle_energy_bfs(es, adj, a, b) >= max(es[a], es[b])


def test_page_example():
    s, z = "GGGAAACCC", Fraction(1, 2)
    states, energies, rates = rate_matrix(s, z)
    assert len(states) == 20
    assert sum(z ** e for e in energies) == Fraction(91, 4)
    mfe = min(range(len(states)), key=lambda x: energies[x])
    assert to_dot_bracket(9, states[mfe]) == "(((...)))" and energies[mfe] == -3
    pi = stationary_distribution(len(states), rates)
    assert pi[mfe] == Fraction(32, 91)
    adj = adjacency(s, states)
    minima, merges = barrier_tree(states, energies, adj)
    assert [to_dot_bracket(9, states[x]) for x in minima] == ["(((...)))", "((....)).", ".((....))", "........."]
    assert [e for e, _, _ in merges] == [1, 1, 1]
    tau = mean_first_passage(len(states), rates, mfe)
    assert tau[0] == Fraction(11375, 929)


def test_gillespie_first_passage_and_occupancy():
    s, z = "GGGAAACCC", Fraction(1, 2)
    states, energies, rates = rate_matrix(s, z)
    mfe = min(range(len(states)), key=lambda x: energies[x])
    tau = float(mean_first_passage(len(states), rates, mfe)[0])
    rng = random.Random(7)
    runs = 2000
    mean = sum(gillespie(s, frozenset(), float(z), rng, stop=states[mfe])[-1][0] for _ in range(runs)) / runs
    assert abs(mean - tau) < 0.05 * tau
    # time average along one long trajectory approaches the Boltzmann distribution
    t_max = 20000.0
    traj = gillespie(s, frozenset(), float(z), rng, t_max=t_max)
    occ = {}
    for (t0, st), (t1, _) in zip(traj, traj[1:] + [(t_max, None)]):
        occ[st] = occ.get(st, 0.0) + (t1 - t0)
    pi = boltzmann(energies, z)
    for x, st in enumerate(states):
        assert abs(occ.get(st, 0.0) / t_max - float(pi[x])) < 0.02
