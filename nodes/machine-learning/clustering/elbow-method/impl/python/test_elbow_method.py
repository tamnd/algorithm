# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elbow-method/. The authors are listed in prov/1YN38V.jsonl.

import random
from fractions import Fraction

from elbow_method import elbow_by_chord, wcss_1d_exact


def brute_wcss(xs, k):
    """The least within-cluster sum of squares over all labelings with exactly k clusters."""
    n = len(xs)
    best = None

    def cost(groups):
        tot = Fraction(0)
        for g in groups:
            if g:
                m = Fraction(sum(g), len(g))
                tot += sum((v - m) ** 2 for v in g)
        return tot

    def rec(i, groups):
        nonlocal best
        if i == n:
            if all(groups):
                c = cost(groups)
                if best is None or c < best:
                    best = c
            return
        for g in groups:
            g.append(xs[i])
            rec(i + 1, groups)
            g.pop()

    rec(0, [[] for _ in range(k)])
    return best


def test_exact_solver_against_brute_force() -> None:
    rng = random.Random(4)
    for _ in range(15):
        xs = [rng.randrange(20) for _ in range(rng.randrange(3, 8))]
        curve = wcss_1d_exact(xs, 3)
        for k in range(1, 4):
            assert curve[k - 1] == brute_wcss(xs, k)
        assert curve[0] >= curve[1] >= curve[2]


def test_hand_example() -> None:
    ks = [1, 2, 3, 4, 5, 6]
    ws = [100, 40, 15, 12, 10, 9]
    assert elbow_by_chord(ks, ws) == 3
    # The rule does not change when W is scaled or shifted.
    assert elbow_by_chord(ks, [7 * w + 3 for w in ws]) == 3


def test_three_groups_on_a_line() -> None:
    xs = [0, 1, 2, 3, 20, 21, 22, 23, 40, 41, 42, 43]
    ws = wcss_1d_exact(xs, 8)
    assert ws == [3215, 815, 15, 11, 7, 3, Fraction(5, 2), 2]
    assert elbow_by_chord(list(range(1, 9)), ws) == 3


def test_smooth_curve_has_no_stable_elbow() -> None:
    # W_k = 1/k has no bend; the chosen k moves with the range of k that is plotted.
    picks = {kmax: elbow_by_chord(list(range(1, kmax + 1)), [Fraction(1, k) for k in range(1, kmax + 1)])
             for kmax in (4, 6, 10, 20)}
    assert picks == {4: 2, 6: 2, 10: 3, 20: 4}
