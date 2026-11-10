# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transposition-rule/. The authors are listed in prov/T7XGDD.jsonl.

import itertools
import random

from transposition_rule import transposition_rule


def inversions(a, b):
    pos = {x: i for i, x in enumerate(b)}
    seq = [pos[x] for x in a]
    return sum(1 for i, j in itertools.combinations(range(len(seq)), 2) if seq[i] > seq[j])


def opt_list_update(start, requests):
    """Optimal offline cost with paid and free exchanges, by a dynamic program over permutations."""
    perms = [tuple(p) for p in itertools.permutations(start)]
    best = {tuple(start): 0}
    for x in requests:
        nxt = {}
        for p in perms:
            pre = min(c + inversions(q, p) for q, c in best.items())
            i = p.index(x)
            for j in range(i + 1):
                after = p[:j] + (x,) + p[j:i] + p[i + 1:]
                if after not in nxt or pre + i + 1 < nxt[after]:
                    nxt[after] = pre + i + 1
        best = nxt
    return min(best.values())


def bad_sequence(n, m):
    """Alternate the last two items of the list 0, 1, ..., n - 1, m times in all."""
    return [n - 1 if t % 2 == 0 else n - 2 for t in range(m)]


def test_example() -> None:
    cost, lst = transposition_rule(["a", "b", "c", "d"], ["c", "c", "d", "a", "c", "b"])
    assert cost == 3 + 2 + 4 + 2 + 2 + 4
    assert lst == ["c", "a", "b", "d"]


def test_bad_sequence_costs_n_per_access() -> None:
    for n in range(2, 8):
        start = list(range(n))
        m = 40
        cost, lst = transposition_rule(start, bad_sequence(n, m))
        assert cost == n * m
        assert lst == start


def test_bad_sequence_against_optimum() -> None:
    # The optimum moves both items to the front and then pays about 1.5 per access.
    for n in range(2, 6):
        start = list(range(n))
        for m in (2, 6, 12):
            opt = opt_list_update(start, bad_sequence(n, m))
            assert opt <= 2 * n + 3 * (m - 2) // 2 + 1
    n, m = 5, 12
    cost, _ = transposition_rule(list(range(n)), bad_sequence(n, m))
    opt = opt_list_update(list(range(n)), bad_sequence(n, m))
    assert cost == 60 and opt == 24
    assert cost > 2 * opt


def test_ratio_grows_with_n() -> None:
    m = 2000
    ratios = []
    for n in (4, 8, 16, 32):
        cost, _ = transposition_rule(list(range(n)), bad_sequence(n, m))
        upper_opt = 2 * n + 3 * (m - 2) // 2 + 1
        ratios.append(cost / upper_opt)
    assert all(a < b for a, b in zip(ratios, ratios[1:]))
    assert ratios[-1] > 2 * 32 / 3 * 0.95


def test_stays_within_n_times_optimum() -> None:
    rng = random.Random(5)
    for _ in range(150):
        n = rng.randint(1, 4)
        start = list(range(n))
        requests = [rng.randrange(n) for _ in range(rng.randint(0, 8))]
        cost, _ = transposition_rule(start, requests)
        assert cost <= n * opt_list_update(start, requests)


def test_edges() -> None:
    assert transposition_rule([], []) == (0, [])
    assert transposition_rule([1, 2], [2, 2]) == (3, [2, 1])
