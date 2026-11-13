# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-tree-search/. The authors are listed in prov/73PV1J.jsonl.

import random

from monte_carlo_tree_search import Nim, TreeGame, flat_monte_carlo, mcts

# The page example: move 0 looks good on average but MIN can answer with 0; move 1 is worth 1/2.
TRAP = [[1.0, 1.0, 1.0, 0.0], [0.5, 0.5]]


def minimax(t, depth=0):
    """Exact value to player 0, the reference for every convergence test."""
    if not isinstance(t, list):
        return t
    vals = [minimax(c, depth + 1) for c in t]
    return max(vals) if depth % 2 == 0 else min(vals)


def random_tree(rng, depth):
    if depth == 0:
        return rng.choice([0.0, 1.0]) if rng.random() < 0.5 else round(rng.random(), 2)
    return [random_tree(rng, depth - 1) for _ in range(rng.randint(2, 3))]


def count_nodes(node):
    return 1 + sum(count_nodes(c) for c in node.children)


def nim_sum(heaps):
    x = 0
    for h in heaps:
        x ^= h
    return x


def test_trap_tree_mcts_beats_flat_monte_carlo():
    for seed in range(50):
        move, root = mcts(TreeGame(TRAP), (), 50, random.Random(seed))
        assert move == 1
        assert root.visits == 50 and sum(ch.visits for ch in root.children) == 50
    for seed in range(20):
        assert flat_monte_carlo(TreeGame(TRAP), (), 400, random.Random(seed)) == 0


def test_tree_statistics():
    rng = random.Random(3)
    for _ in range(30):
        t = random_tree(rng, 3)
        n = rng.randint(1, 60)
        _, root = mcts(TreeGame(t), (), n, random.Random(n))
        # One node is added per iteration until the tree is complete.
        assert count_nodes(root) <= n + 1
        assert root.visits == n
        stack = [root]
        while stack:
            v = stack.pop()
            assert 0 <= v.wins <= v.visits
            if v.children:
                assert sum(c.visits for c in v.children) in (v.visits, v.visits - 1)
            stack.extend(v.children)


def test_single_move_and_immediate_win():
    assert mcts(TreeGame([[0.3]]), (), 5, random.Random(0))[0] == 0
    # In Nim with one heap the winning move takes everything.
    for seed in range(10):
        assert mcts(Nim(), ((5,), 0), 300, random.Random(seed))[0] == (0, 5)


def test_nim_finds_a_winning_move():
    nim = Nim()
    # Measured: (2, 3, 4) needs about 3000 playouts; 1000 playouts give a winning move only 4 times in 10.
    for heaps, playouts, seeds in [((1, 2), 1000, 10), ((2, 3), 1000, 10), ((1, 2, 4), 1000, 10), ((2, 3, 4), 3000, 5)]:
        assert nim_sum(heaps) != 0
        for seed in range(seeds):
            move, _ = mcts(nim, (heaps, 0), playouts, random.Random(seed))
            after, _ = nim.play((heaps, 0), move)
            assert nim_sum(after) == 0, (heaps, seed, move)


def test_player_one_at_the_root():
    # Search from depth 1, where player 1 moves. The leaves are payoffs to player 0, so player 1
    # minimizes: the children of t1 are worth 0.9, 0.1 and 0.5 to player 0.
    t1 = [[0.9, 0.95], [0.1, 0.2], [0.5, 0.6]]
    for seed in range(10):
        move, _ = mcts(TreeGame([t1]), (0,), 500, random.Random(seed))
        assert move == 1


def check_random_trees(seed, depths, count, playouts):
    rng = random.Random(seed)
    tested = 0
    for k in range(count):
        t = random_tree(rng, rng.randint(*depths))
        vals = [minimax(c, 1) for c in t]
        best = max(vals)
        second = max([v for v in vals if v < best], default=None)
        if second is not None and best - second < 0.2:
            continue
        tested += 1
        move, _ = mcts(TreeGame(t), (), playouts, random.Random(k))
        assert vals[move] == best
    return tested


def test_random_trees_converge_to_the_minimax_move():
    # Trees of depth 1 to 3 (at most 27 leaves) whose best root move is ahead by 0.2 or more:
    # 400 playouts each. 374 of the 500 trees pass the filter.
    assert check_random_trees(2006, (1, 3), 500, 400) >= 300


def test_deeper_random_trees_need_more_playouts():
    # Depth 4 (up to 81 leaves): 400 playouts can fail (both root moves got 200 visits on one tree
    # with seed 2006), so these get 3000 playouts. 25 of the 40 trees pass the filter.
    assert check_random_trees(2012, (4, 4), 40, 3000) >= 20
