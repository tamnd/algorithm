# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/uct/. The authors are listed in prov/TGTRKB.jsonl.

import math
import random

from uct import ucb1, uct

# Move 0 looks good on average (3/4) but MIN answers with 0; move 1 is worth 1/2 for sure.
TRAP = [[1.0, 1.0, 1.0, 0.0], [0.5, 0.5]]


def minimax(t, depth=0):
    """Exact value to player 0: the reference for the convergence tests."""
    if not isinstance(t, list):
        return t
    vals = [minimax(c, depth + 1) for c in t]
    return max(vals) if depth % 2 == 0 else min(vals)


def random_tree(rng, depth):
    if depth == 0:
        return rng.choice([0.0, 1.0]) if rng.random() < 0.5 else round(rng.random(), 2)
    return [random_tree(rng, depth - 1) for _ in range(rng.randint(2, 3))]


def check_random_trees(seed, depths, count, iterations, stochastic, gap):
    rng = random.Random(seed)
    tested = 0
    for k in range(count):
        t = random_tree(rng, rng.randint(*depths))
        vals = [minimax(c, 1) for c in t]
        best = max(vals)
        second = max([v for v in vals if v < best], default=None)
        if second is not None and best - second < gap:
            continue
        tested += 1
        move, _ = uct(t, iterations, random.Random(k), stochastic=stochastic)
        assert vals[move] == best, (k, vals)
    return tested


def test_one_level_is_ucb1():
    rng = random.Random(2002)
    for k in range(300):
        probs = [rng.random() for _ in range(rng.randint(2, 5))]
        trace = []
        uct(probs, 300, random.Random(k), stochastic=True, trace=trace)
        assert trace == ucb1(probs, 300, random.Random(k))


def test_trap_tree():
    means = []
    for n in (100, 1000, 10000):
        move, table = uct(TRAP, n, random.Random(0))
        root = table[()]
        assert move == 1 and sum(root.counts) == root.n == n
        assert root.mean(1) == 0.5
        means.append(root.mean(0))
    # The estimate of move 0 falls toward its minimax value 0 (measured 0.3, 0.195, 0.15): the
    # bad replies of MIN are still tried, but only about log n times each.
    assert means[0] > means[1] > means[2] > 0


def test_failure_probability_falls():
    wrong = {n: sum(uct(TRAP, n, random.Random(s), stochastic=True)[0] != 1 for s in range(100)) for n in (20, 300)}
    # Measured with Bernoulli leaves: 46 wrong root moves in 100 runs after 20 iterations, none after 100 or 300.
    assert wrong[20] >= 20
    assert wrong[300] == 0


def test_worse_arm_is_pulled_logarithmically():
    pulls = {}
    for n in (1000, 4000):
        pulls[n] = sum(ucb1([0.9, 0.6], n, random.Random(s)).count(1) for s in range(50)) / 50
        trace = []
        uct([0.9, 0.6], n, random.Random(7), stochastic=True, trace=trace)
        assert trace.count(1) < n / 4
    # Theorem 1 of Auer et al. bounds the expected count by 8 ln n / gap^2 + 1 + pi^2 / 3.
    assert pulls[1000] <= 8 * math.log(1000) / 0.3 ** 2 + 1 + math.pi ** 2 / 3
    assert pulls[4000] < 2 * pulls[1000]


def test_root_estimate_converges_to_the_minimax_value():
    rng = random.Random(2006)
    for k in range(20):
        t = random_tree(rng, 2)
        v = minimax(t)
        move, table = uct(t, 5000, random.Random(k))
        assert abs(table[()].mean(move) - v) <= 0.05


def test_random_trees_converge_to_the_minimax_move():
    # Depth 1 to 3, best root move ahead by 0.2 or more: 400 iterations. 374 of the 500 trees pass the filter.
    assert check_random_trees(2006, (1, 3), 500, 400, False, 0.2) >= 300


def test_deeper_random_trees():
    # Depth 4, up to 81 leaves: 3000 iterations. 25 of the 40 trees pass the filter.
    assert check_random_trees(2012, (4, 4), 40, 3000, False, 0.2) >= 20


def test_stochastic_leaves():
    # Bernoulli leaves, depth 1 or 2, best root move ahead by 0.3 or more in expectation:
    # 2000 iterations. 102 of the 150 trees pass the filter.
    assert check_random_trees(1993, (1, 2), 150, 2000, True, 0.3) >= 80
