# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fixed-parameter-mec/. The authors are listed in prov/W2Z7FH.jsonl.

import itertools
import random

from fixed_parameter_mec import active_sets, column_costs, mec_cost, whatshap_mec

# Fig. 1 of Patterson et al. (2015), with columns renumbered from 0.
PAPER_FRAGS = [{0: 0}, {0: 1, 1: 0}, {0: 1, 1: 1}, {1: 0}]
PAPER_WEIGHTS = [{0: 5}, {0: 3, 1: 2}, {0: 6, 1: 1}, {1: 2}]


def brute_mec(fragments, m, weights=None, all_het=False):
    """Least MEC cost over all haplotype pairs (h1, h2), or all (h1, complement) pairs."""
    haps = list(itertools.product((0, 1), repeat=m))
    best = None
    for h1 in haps:
        partners = [tuple(1 - a for a in h1)] if all_het else haps
        for h2 in partners:
            c = mec_cost(fragments, h1, h2, weights)
            if best is None or c < best:
                best = c
    return best


def random_fragments(rng, n, m, max_len, hole_rate):
    frags = []
    for _ in range(n):
        start = rng.randrange(m)
        end = min(m, start + rng.randint(1, max_len))
        f = {j: rng.randint(0, 1) for j in range(start, end) if j == start or rng.random() >= hole_rate}
        frags.append(f)
    return frags


def test_paper_example_first_column():
    A = active_sets(PAPER_FRAGS, 2)
    assert A == [[0, 1, 2], [1, 2, 3]]
    delta, _, _ = column_costs(PAPER_FRAGS, PAPER_WEIGHTS, A[0], 0, False)
    # mask bit t = 1 puts the t-th active fragment in S.
    assert delta[0b000] == 5  # ({f0, f1, f2}, {})
    assert delta[0b100] == 3  # ({f0, f1}, {f2})
    assert delta[0b010] == 5  # ({f0, f2}, {f1})
    assert delta[0b001] == 0  # ({f1, f2}, {f0})


def test_paper_example_optimum():
    cost, h1, h2, side = whatshap_mec(PAPER_FRAGS, 2, PAPER_WEIGHTS)
    assert cost == 1
    assert mec_cost(PAPER_FRAGS, h1, h2, PAPER_WEIGHTS) == 1
    assert side[1] == side[2] == side[3] != side[0]
    assert brute_mec(PAPER_FRAGS, 2, PAPER_WEIGHTS) == 1


def test_conflict_free_input_costs_zero():
    h = [0, 1, 1, 0, 1, 0]
    g = [1 - a for a in h]
    frags = [{0: 0, 1: 1, 2: 1}, {2: 0, 3: 1, 4: 0}, {3: 0, 4: 1, 5: 0}, {0: 1, 5: 1}]
    cost, h1, h2, _ = whatshap_mec(frags, 6, all_het=True)
    assert cost == 0
    assert {tuple(h1), tuple(h2)} == {tuple(h), tuple(g)}


def test_against_brute_force_unweighted():
    rng = random.Random(7)
    for _ in range(60):
        m = rng.randint(1, 5)
        frags = random_fragments(rng, rng.randint(1, 7), m, 4, 0.2)
        cost, h1, h2, _ = whatshap_mec(frags, m)
        assert cost == brute_mec(frags, m)
        assert mec_cost(frags, h1, h2) == cost


def test_against_brute_force_weighted_and_all_het():
    rng = random.Random(11)
    for _ in range(60):
        m = rng.randint(1, 7)
        frags = random_fragments(rng, rng.randint(1, 8), m, 5, 0.3)
        weights = [{j: rng.randint(1, 9) for j in f} for f in frags]
        for all_het in (False, True):
            cost, h1, h2, _ = whatshap_mec(frags, m, weights, all_het)
            assert cost == brute_mec(frags, m, weights, all_het)
            assert mec_cost(frags, h1, h2, weights) == cost
            if all_het:
                assert all(a != b for a, b in zip(h1, h2))


def test_all_het_twelve_columns():
    rng = random.Random(12)
    m = 12
    frags = random_fragments(rng, 14, m, 5, 0.25)
    cost, h1, h2, _ = whatshap_mec(frags, m, all_het=True)
    assert cost == brute_mec(frags, m, all_het=True)


def test_side_matches_cost():
    rng = random.Random(3)
    for _ in range(30):
        m = rng.randint(2, 6)
        frags = random_fragments(rng, 6, m, 4, 0.2)
        cost, h1, h2, side = whatshap_mec(frags, m)
        total = 0
        for f, s in zip(frags, side):
            hap = h2 if s else h1
            total += sum(1 for j, a in f.items() if hap[j] != a)
        assert total == cost


def test_recovers_simulated_haplotypes():
    rng = random.Random(2015)
    m = 40
    h = [rng.randint(0, 1) for _ in range(m)]
    g = [1 - a for a in h]
    frags = []
    for _ in range(60):
        start = rng.randrange(m - 3)
        end = min(m, start + rng.randint(4, 8))
        src = h if rng.random() < 0.5 else g
        frags.append({j: (1 - src[j]) if rng.random() < 0.03 else src[j] for j in range(start, end)})
    cost, h1, h2, _ = whatshap_mec(frags, m, all_het=True)
    assert {tuple(h1), tuple(h2)} == {tuple(h), tuple(g)}
    assert cost <= mec_cost(frags, h, g)
    assert max(len(a) for a in active_sets(frags, m)) <= 16


def test_empty_and_gap_columns():
    assert whatshap_mec([], 0) == (0, [], [], [])
    frags = [{0: 1}, {0: 0}, {3: 1}, {3: 1}]
    cost, h1, h2, _ = whatshap_mec(frags, 4)
    assert cost == 0
    assert {h1[0], h2[0]} == {0, 1}
