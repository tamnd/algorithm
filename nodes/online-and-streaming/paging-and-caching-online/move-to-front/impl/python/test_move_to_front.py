# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/move-to-front/. The authors are listed in prov/XGK3CR.jsonl.

import itertools
import random

from move_to_front import move_to_front


def inversions(a, b):
    """Number of pairs ordered differently in the lists a and b (Kendall tau distance)."""
    pos = {x: i for i, x in enumerate(b)}
    seq = [pos[x] for x in a]
    return sum(1 for i, j in itertools.combinations(range(len(seq)), 2) if seq[i] > seq[j])


def opt_list_update(start, requests):
    """Optimal offline cost with paid exchanges (cost 1 each) and free exchanges.

    Before each access the list may be rearranged with paid exchanges, which costs the
    number of inversions. After the access the item may move forward for free.
    A dynamic program over all permutations; for short lists only.
    """
    perms = [tuple(p) for p in itertools.permutations(start)]
    best = {tuple(start): 0}
    for x in requests:
        nxt = {}
        for p in perms:
            pre = min(c + inversions(q, p) for q, c in best.items())
            i = p.index(x)
            for j in range(i + 1):
                after = p[:j] + (x,) + p[j:i] + p[i + 1:]
                val = pre + i + 1
                if after not in nxt or val < nxt[after]:
                    nxt[after] = val
        best = nxt
    return min(best.values())


def static_cost(order, requests):
    pos = {x: i + 1 for i, x in enumerate(order)}
    return sum(pos[x] for x in requests)


def test_example() -> None:
    cost, lst = move_to_front(["a", "b", "c", "d"], ["c", "c", "d", "a", "c", "b"])
    assert cost == 3 + 1 + 4 + 3 + 3 + 4
    assert lst == ["b", "c", "a", "d"]


def test_two_competitive_against_offline_optimum() -> None:
    rng = random.Random(1985)
    for _ in range(200):
        n = rng.randint(1, 4)
        start = list(range(n))
        requests = [rng.randrange(n) for _ in range(rng.randint(0, 8))]
        mtf, _ = move_to_front(start, requests)
        opt = opt_list_update(start, requests)
        assert mtf <= 2 * opt - len(requests)
        assert mtf * n <= (2 * n - 1) * opt


def test_against_every_static_order() -> None:
    rng = random.Random(1976)
    for _ in range(200):
        n = rng.randint(1, 5)
        start = list(range(n))
        requests = [rng.randrange(n) for _ in range(rng.randint(0, 30))]
        mtf, _ = move_to_front(start, requests)
        for order in itertools.permutations(start):
            s = static_cost(order, requests)
            assert mtf <= 2 * s + inversions(start, list(order)) - len(requests)


def test_best_static_order_is_by_frequency() -> None:
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randint(1, 5)
        requests = [rng.randrange(n) for _ in range(rng.randint(0, 30))]
        by_freq = sorted(range(n), key=lambda x: -requests.count(x))
        best = min(static_cost(p, requests) for p in itertools.permutations(range(n)))
        assert static_cost(by_freq, requests) == best


def test_lower_bound_sequence() -> None:
    # The adversary always asks for the last item; MTF then pays n per access.
    for n in (2, 3, 4):
        start = list(range(n))
        lst, requests = list(start), []
        for _ in range(10):
            requests.append(lst[-1])
            _, lst = move_to_front(lst, [lst[-1]])
        mtf, _ = move_to_front(start, requests)
        m = len(requests)
        assert mtf == n * m
        opt = opt_list_update(start, requests)
        # Some static order costs at most the average (n + 1) / 2 per access.
        assert 2 * opt <= m * (n + 1) + n * (n - 1)
        assert mtf * (n + 1) >= 2 * n * (opt - n * (n - 1) // 2)


def test_edges() -> None:
    assert move_to_front([], []) == (0, [])
    assert move_to_front([7], [7, 7]) == (2, [7])
    try:
        move_to_front([1, 1], [1])
    except ValueError:
        pass
    else:
        raise AssertionError("repeated items must be rejected")
