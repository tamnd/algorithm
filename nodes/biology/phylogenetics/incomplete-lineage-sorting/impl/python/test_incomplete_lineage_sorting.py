# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incomplete-lineage-sorting/. The authors are listed in prov/W29D9B.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction as F

from incomplete_lineage_sorting import (
    anomaly_bound,
    canon,
    caterpillar_four,
    gene_tree_distribution,
    lineage_count_probability,
    simulate_gene_tree,
    three_taxon,
    unrooted_split,
)

QS = [F(0), F(1, 10), F(1, 2), F(9, 10), F(99, 100)]


def test_lineage_count_probabilities() -> None:
    for q in QS:
        assert lineage_count_probability(2, 1, q) == 1 - q
        assert lineage_count_probability(2, 2, q) == q
        assert lineage_count_probability(3, 3, q) == q ** 3
        assert lineage_count_probability(3, 2, q) == F(3, 2) * (q - q ** 3)
        for i in range(1, 7):
            assert sum(lineage_count_probability(i, j, q) for j in range(1, i + 1)) == 1


def test_three_taxa_exact() -> None:
    for q in QS[1:]:
        dist = gene_tree_distribution((("A", "B", q), "C", None))
        match, other = three_taxon(q)
        assert dist[canon((("A", "B"), "C"))] == match
        assert dist[canon((("A", "C"), "B"))] == other
        assert dist[canon((("B", "C"), "A"))] == other
        assert match > other  # no anomalous gene tree for three taxa


def test_four_taxa_closed_form_exact() -> None:
    for qy in QS[1:]:
        for qx in QS[1:]:
            dist = gene_tree_distribution(((("A", "B", qy), "C", qx), "D", None))
            assert len(dist) == 15 and sum(dist.values()) == 1
            match, sym = caterpillar_four(qy, qx)
            assert dist[canon(((("A", "B"), "C"), "D"))] == match
            assert dist[canon((("A", "B"), ("C", "D")))] == sym


def test_anomaly_zone() -> None:
    for x in (0.05, 0.1, 0.2):
        a = anomaly_bound(x)
        for y, anomalous in ((a * 0.9, True), (a * 1.1, False)):
            match, sym = caterpillar_four(math.exp(-y), math.exp(-x))
            assert (sym > match) == anomalous
    assert anomaly_bound(0.3) < 0  # no anomaly for an old branch of 0.3 units
    match, sym = caterpillar_four(math.exp(-0.05), math.exp(-0.05))
    assert sym > match


def test_unrooted_quartets_never_anomalous() -> None:
    four = {"A", "B", "C", "D"}
    ab = frozenset([frozenset("AB"), frozenset("CD")])
    for qy in QS[1:]:
        for qx in QS[1:]:
            for species, q in (
                (((("A", "B", qy), "C", qx), "D", None), qy),
                ((("A", "B", qy), ("C", "D", qx), None), qy * qx),
            ):
                split = Counter()
                for tree, p in gene_tree_distribution(species).items():
                    split[unrooted_split(tree, four)] += p
                assert split[ab] == 1 - 2 * q / 3
                assert all(v == q / 3 for k, v in split.items() if k != ab)


def test_simulation_matches_exact() -> None:
    rng = random.Random(31)
    y, x, reps = 0.1, 0.1, 20000
    species = ((("A", "B", y), "C", x), "D", None)
    counts = Counter(simulate_gene_tree(species, rng) for _ in range(reps))
    exact = gene_tree_distribution(((("A", "B", math.exp(-y)), "C", math.exp(-x)), "D", None))
    for tree, p in exact.items():
        assert abs(counts[tree] / reps - p) < 4 * math.sqrt(p * (1 - p) / reps)
