# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/disk-scheduling/. The authors are listed in prov/683RCB.jsonl.

import math
import random
from itertools import permutations

from disk_scheduling import brute_force_optimum, fcfs_cost, head_movement, offline_optimum, optimal_order

QUEUE = [98, 183, 37, 122, 14, 124, 65, 67]


def test_textbook_queue() -> None:
    assert fcfs_cost(QUEUE, 53) == 640
    assert offline_optimum(QUEUE, 53) == 208
    assert brute_force_optimum(QUEUE, 53) == 208
    assert optimal_order(QUEUE, 53) == [37, 14, 65, 67, 98, 122, 124, 183]


def test_edges() -> None:
    assert offline_optimum([], 5) == 0
    assert optimal_order([], 5) == []
    assert offline_optimum([5], 5) == 0
    assert offline_optimum([9], 5) == 4
    assert offline_optimum([7, 9], 5) == 4  # head below the range: one sweep
    assert offline_optimum([1, 3], 5) == 4  # head above the range
    assert offline_optimum([4, 4, 4], 5) == 1
    assert head_movement([1, 9, 1], 5) == 4 + 8 + 8


def test_formula_against_all_orders() -> None:
    rng = random.Random(2026)
    for _ in range(400):
        n = rng.randrange(0, 8)
        c = rng.choice([10, 50, 200])
        req = [rng.randrange(c) for _ in range(n)]
        head = rng.randrange(c)
        best = brute_force_optimum(req, head) if req else 0
        assert offline_optimum(req, head) == best
        order = optimal_order(req, head)
        assert sorted(order) == sorted(req)
        assert head_movement(order, head) == best
    for _ in range(4):
        req = [rng.randrange(200) for _ in range(8)]
        head = rng.randrange(200)
        assert offline_optimum(req, head) == brute_force_optimum(req, head)


def test_concave_seek_time_changes_the_optimum() -> None:
    def seek(d):
        return 0.0 if d == 0 else 1 + math.sqrt(d)

    def time(order, head):
        return sum(seek(abs(b - a)) for a, b in zip([head, *order], order))

    req, head = [0, 4, 10], 3
    best = min(permutations(req), key=lambda p: time(p, head))
    assert best == (4, 0, 10)  # two reversals
    assert time(best, head) < min(time([0, 4, 10], head), time([4, 10, 0], head))
    assert head_movement(best, head) == 15 > offline_optimum(req, head) == 13


def test_fcfs_is_not_optimal_in_general() -> None:
    rng = random.Random(5)
    worse = 0
    for _ in range(200):
        req = [rng.randrange(100) for _ in range(6)]
        head = rng.randrange(100)
        assert fcfs_cost(req, head) >= offline_optimum(req, head)
        worse += fcfs_cost(req, head) > offline_optimum(req, head)
    assert worse > 150
