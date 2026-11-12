# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wireless-link-scheduling/. The authors are listed in prov/R3ET6W.jsonl.

import random
from fractions import Fraction

from wireless_link_scheduling import (
    greedy_maximal_schedule,
    is_independent,
    max_weight_schedule,
    node_exclusive_conflicts,
    sinr_feasible,
    weight_of,
)


def brute_force(conflict: list, w: list):
    best = (0, 0)
    for mask in range(1 << len(w)):
        if is_independent(conflict, mask):
            best = max(best, (weight_of(w, mask), mask), key=lambda x: x[0])
    return best


def random_conflict_graph(rng: random.Random, m: int, p: float) -> list:
    conflict = [0] * m
    for a in range(m):
        for b in range(a + 1, m):
            if rng.random() < p:
                conflict[a] |= 1 << b
                conflict[b] |= 1 << a
    return conflict


def test_exact_schedule_matches_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(150):
        m = rng.randint(1, 11)
        conflict = random_conflict_graph(rng, m, rng.choice([0.2, 0.4, 0.7]))
        w = [Fraction(rng.randint(0, 20)) for _ in range(m)]
        got_w, got_m = max_weight_schedule(conflict, w)
        assert is_independent(conflict, got_m)
        assert weight_of(w, got_m) == got_w
        assert got_w == brute_force(conflict, w)[0]


def test_greedy_is_a_maximal_independent_set() -> None:
    rng = random.Random(2)
    for _ in range(200):
        m = rng.randint(1, 12)
        conflict = random_conflict_graph(rng, m, 0.3)
        w = [rng.randint(1, 9) for _ in range(m)]
        g = greedy_maximal_schedule(conflict, w)
        assert is_independent(conflict, g)
        for v in range(m):
            if not g >> v & 1:
                assert conflict[v] & g  # no link can be added


def test_path_example() -> None:
    # Network a-b-c-d with links ab, bc, cd and weights 2, 3, 2.
    conflict = node_exclusive_conflicts([("a", "b"), ("b", "c"), ("c", "d")])
    w = [2, 3, 2]
    assert weight_of(w, greedy_maximal_schedule(conflict, w)) == 3
    assert max_weight_schedule(conflict, w) == (4, 0b101)


def test_greedy_gets_half_under_node_exclusive_interference() -> None:
    # Under node-exclusive interference a schedule is a matching, and the
    # greedy matching has at least half of the maximum weight.
    rng = random.Random(3)
    worst = Fraction(1)
    for _ in range(150):
        n = rng.randint(2, 7)
        links = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < 0.5]
        if not links or len(links) > 14:
            continue
        conflict = node_exclusive_conflicts(links)
        w = [rng.randint(1, 30) for _ in links]
        opt, _ = max_weight_schedule(conflict, w)
        got = weight_of(w, greedy_maximal_schedule(conflict, w))
        assert 2 * got >= opt
        worst = min(worst, Fraction(got, opt))
    assert worst < 1  # greedy is not always optimal


def test_greedy_can_be_far_off_on_a_general_conflict_graph() -> None:
    # A star conflict graph: the centre (weight 11) conflicts with 10 leaves
    # of weight 10 each. Greedy takes the centre; the optimum takes the leaves.
    m = 11
    conflict = [0] * m
    for leaf in range(1, m):
        conflict[0] |= 1 << leaf
        conflict[leaf] |= 1
    w = [11] + [10] * 10
    assert weight_of(w, greedy_maximal_schedule(conflict, w)) == 11
    assert max_weight_schedule(conflict, w)[0] == 100


def test_sinr_is_not_pairwise() -> None:
    # Three links, own gain 1, cross gain 1/2, noise 1/10, threshold 1.
    # Every pair is feasible, but the three together are not, so no
    # conflict graph describes this model.
    cross = Fraction(1, 2)
    gain = [[1 if k == l else cross for l in range(3)] for k in range(3)]
    power = [1, 1, 1]
    noise, beta = Fraction(1, 10), 1
    for pair in (0b011, 0b101, 0b110):
        assert sinr_feasible(pair, gain, power, noise, beta)
    assert not sinr_feasible(0b111, gain, power, noise, beta)
