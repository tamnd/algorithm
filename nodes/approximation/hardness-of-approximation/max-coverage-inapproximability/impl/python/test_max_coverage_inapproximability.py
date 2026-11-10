# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/max-coverage-inapproximability/. The authors are listed in prov/7DN3DJ.jsonl.

import math
import random

from max_coverage_inapproximability import (
    cover_in_rounds,
    covered,
    exact_oracle,
    greedy_oracle,
    min_cover,
    rounds_needed,
)


def random_system(rng, n, m, p=0.3):
    sets = [set(e for e in range(n) if rng.random() < p) for _ in range(m)]
    for e in range(n):
        if not any(e in s for s in sets):
            sets[rng.randrange(m)].add(e)
    return [frozenset(s) for s in sets]


def test_rounds_needed() -> None:
    assert rounds_needed(1, 0.5) == 1
    assert rounds_needed(8, 0.5) == 4
    assert rounds_needed(7, 0.5) == 3
    for n in range(1, 200):
        for alpha in (0.3, 1 - 1 / math.e, 0.7):
            t = rounds_needed(n, alpha)
            assert (1 - alpha) ** t * n < 1 <= (1 - alpha) ** (t - 1) * n


def test_each_round_covers_alpha_of_the_rest() -> None:
    rng = random.Random(1)
    for _ in range(60):
        n, m = rng.randint(3, 9), rng.randint(3, 7)
        sets = random_system(rng, n, m)
        k = min_cover(n, sets)
        alpha_k = 1 - (1 - 1 / k) ** k
        remaining = frozenset(range(n))
        while remaining:
            # The k optimal sets cover all remaining elements, so OPT of the round is len(remaining).
            assert covered(sets, exact_oracle(sets, k, remaining), remaining) == len(remaining)
            got = covered(sets, greedy_oracle(sets, k, remaining), remaining)
            assert got >= alpha_k * len(remaining) - 1e-9
            remaining = remaining - frozenset().union(*(sets[j] for j in greedy_oracle(sets, k, remaining)))


def test_cover_size_bound() -> None:
    rng = random.Random(2)
    for _ in range(80):
        n, m = rng.randint(3, 12), rng.randint(3, 8)
        sets = random_system(rng, n, m)
        k = min_cover(n, sets)
        alpha = 1 - (1 - 1 / k) ** k if k > 1 else 1 - 1e-12
        t = rounds_needed(n, alpha)
        cover = cover_in_rounds(n, sets, k, greedy_oracle, t)
        assert cover is not None and len(cover) <= k * t
        assert covered(sets, cover, frozenset(range(n))) == n
        assert cover_in_rounds(n, sets, k, exact_oracle, 1) is not None
