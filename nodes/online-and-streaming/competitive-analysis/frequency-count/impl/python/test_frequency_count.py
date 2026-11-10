# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frequency-count/. The authors are listed in prov/E8G97Z.jsonl.

import itertools
import random

from frequency_count import frequency_count


def inversions(a, b):
    """Number of pairs ordered differently in the lists a and b."""
    pos = {x: i for i, x in enumerate(b)}
    seq = [pos[x] for x in a]
    return sum(1 for i, j in itertools.combinations(range(len(seq)), 2) if seq[i] > seq[j])


def opt_list_update(start, requests):
    """Optimal offline cost with paid exchanges (cost 1 each) and free exchanges.

    A dynamic program over all permutations of the list; for short lists only.
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


def move_to_front_cost(start, requests):
    lst = list(start)
    cost = 0
    for x in requests:
        i = lst.index(x)
        cost += i + 1
        lst.insert(0, lst.pop(i))
    return cost, lst


def static_optimum(items, requests):
    """Cost of the best fixed list: the items sorted by decreasing frequency."""
    freq = {x: 0 for x in items}
    for x in requests:
        freq[x] += 1
    order = sorted(items, key=lambda x: -freq[x])
    pos = {x: i + 1 for i, x in enumerate(order)}
    return sum(pos[x] for x in requests)


def bad_round(n):
    """Item i of 1..n is requested n - i + 1 times, in the order 1, 2, ..., n."""
    return [i for i in range(1, n + 1) for _ in range(n - i + 1)]


def test_example() -> None:
    cost, lst, count = frequency_count(list("abcd"), list("ccdacb"))
    assert cost == 3 + 1 + 4 + 3 + 1 + 4 == 16
    assert lst == ["c", "d", "a", "b"]
    assert count == {"a": 1, "b": 1, "c": 3, "d": 1}
    assert move_to_front_cost(list("abcd"), list("ccdacb"))[0] == 18
    assert opt_list_update(list("abcd"), list("ccdacb")) == 14
    assert static_optimum(list("abcd"), list("ccdacb")) == 12


def test_bad_round_against_exact_optimum() -> None:
    for n in range(1, 8):
        items = list(range(1, n + 1))
        req = bad_round(n)
        cost, lst, _ = frequency_count(items, req)
        assert cost == n * (n + 1) * (n + 2) // 6
        assert lst == items
        assert move_to_front_cost(items, req)[0] == n * n
    for n in (3, 4):
        items = list(range(1, n + 1))
        assert opt_list_update(items, bad_round(n)) == n * n


def test_repeated_phase_is_not_competitive() -> None:
    for n in range(2, 9):
        items = list(range(1, n + 1))
        phase = bad_round(n) + [i for i in range(1, n + 1) for _ in range(i)]
        k = 5
        cost, lst, count = frequency_count(items, phase * k)
        assert cost == k * n * (n + 1) ** 2 // 2
        assert lst == items
        assert set(count.values()) == {k * (n + 1)}
        # Offline: move-to-front on the phase, then paid exchanges back to the start.
        mtf, end = move_to_front_cost(items, phase)
        assert mtf == (5 * n * n - n) // 2
        assert mtf + inversions(end, items) == 3 * n * n - n
    for n in (3, 4):
        items = list(range(1, n + 1))
        phase = bad_round(n) + [i for i in range(1, n + 1) for _ in range(i)]
        assert opt_list_update(items, phase * 2) <= 2 * (3 * n * n - n)


def test_sorted_by_count_and_pairwise() -> None:
    rng = random.Random(1976)
    for _ in range(300):
        n = rng.randint(1, 6)
        items = list(range(n))
        rng.shuffle(items)
        req = [rng.randrange(n) for _ in range(rng.randint(0, 25))]
        cost, lst, count = frequency_count(items, req)
        assert all(count[lst[i]] >= count[lst[i + 1]] for i in range(n - 1))
        for x, y in itertools.combinations(items, 2):
            proj = [z for z in req if z in (x, y)]
            start2 = [z for z in items if z in (x, y)]
            _, lst2, _ = frequency_count(start2, proj)
            assert (lst.index(x) < lst.index(y)) == (lst2.index(x) < lst2.index(y))


def test_within_twice_static_optimum() -> None:
    rng = random.Random(1985)
    for _ in range(500):
        n = rng.randint(1, 6)
        items = list(range(n))
        rng.shuffle(items)
        m = rng.randint(0, 30)
        req = [rng.randrange(n) for _ in range(m)]
        cost, _, _ = frequency_count(items, req)
        s = static_optimum(items, req)
        assert cost <= 2 * s - m + n * (n - 1) // 2
        assert cost <= n * m


def test_trailing_requests_reach_factor_two() -> None:
    for f in range(1, 20):
        req = ["x"] + ["y", "y", "x", "x"] * f
        cost, _, _ = frequency_count(["y", "x"], req)
        m = len(req)
        assert cost == 2 * m
        assert static_optimum(["y", "x"], req) - m == (m - 1) // 2


def test_competitive_against_exact_optimum_small() -> None:
    rng = random.Random(7)
    for _ in range(60):
        n = rng.randint(1, 4)
        items = list(range(n))
        req = [rng.randrange(n) for _ in range(rng.randint(1, 8))]
        cost, _, _ = frequency_count(items, req)
        assert cost <= n * opt_list_update(items, req)


def test_rejects_repeated_items() -> None:
    try:
        frequency_count([1, 1], [1])
    except ValueError:
        return
    raise AssertionError("expected ValueError")
