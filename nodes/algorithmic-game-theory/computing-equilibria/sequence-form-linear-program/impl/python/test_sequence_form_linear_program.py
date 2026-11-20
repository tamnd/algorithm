# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequence-form-linear-program/. The authors are listed in prov/7V6BC9.jsonl.

import random
from fractions import Fraction
from itertools import permutations, product

from agtlp import lp_max
from sequence_form_linear_program import SequenceForm, behavior, solve

F = Fraction

# Player 1 plays L (payoff 1) or R; after R, player 2 picks a or b, and then player 1
# picks c or d without seeing that choice. Payoffs are to player 1.
PAGE_GAME = ("move", 1, "root", [
    ("L", ("leaf", 1)),
    ("R", ("move", 2, "p2", [
        ("a", ("move", 1, "late", [("c", ("leaf", 3)), ("d", ("leaf", 0))])),
        ("b", ("move", 1, "late", [("c", ("leaf", 0)), ("d", ("leaf", 2))])),
    ])),
])


def kuhn_poker():
    names = "JQK"
    deals = []
    for c1, c2 in permutations(range(3), 2):
        def show(stake, c1=c1, c2=c2):
            return ("leaf", stake if c1 > c2 else -stake)
        h1, h2 = names[c1], names[c2]
        root = ("move", 1, "1" + h1, [
            ("check", ("move", 2, "2" + h2 + "k", [
                ("check", show(1)),
                ("bet", ("move", 1, "1" + h1 + "kb", [("fold", ("leaf", -1)), ("call", show(2))])),
            ])),
            ("bet", ("move", 2, "2" + h2 + "b", [("fold", ("leaf", 1)), ("call", show(2))])),
        ])
        deals.append((F(1, 6), root))
    return ("chance", deals)


def expected(node, strat):
    """Expected payoff to player 1 when player p + 1 plays the behavior strategy strat[p]."""
    kind = node[0]
    if kind == "leaf":
        return F(node[1])
    if kind == "chance":
        return sum(F(p) * expected(child, strat) for p, child in node[1])
    _, player, h, moves = node
    probs = strat[player - 1][h]
    return sum(probs[a] * expected(child, strat) for a, child in moves if probs[a] != 0)


def pure_strategies(sf, p):
    hs = list(sf.infosets[p])
    for choice in product(*[sf.infosets[p][h][1] for h in hs]):
        yield {h: {a: F(int(a == c)) for a in sf.infosets[p][h][1]} for h, c in zip(hs, choice)}


def normal_form_value(tree, sf):
    """The value of the normal form of the tree, by an LP over the pure strategies."""
    rows = list(pure_strategies(sf, 0))
    cols = list(pure_strategies(sf, 1))
    M = [[expected(tree, (r, c)) for c in cols] for r in rows]
    m = len(rows)
    # maximize v+ - v- subject to v+ - v- - sum_i x_i M[i][j] <= 0, sum x = 1.
    c = [1, -1] + [0] * m
    A_ub = [[1, -1] + [-M[i][j] for i in range(m)] for j in range(len(cols))]
    status, _, value, _ = lp_max(c, A_ub, [0] * len(cols), [[0, 0] + [1] * m], [1])
    assert status == "optimal"
    return value


def check_plans(sf, x, y):
    for p, plan in ((0, x), (1, y)):
        rows = sf.E if p == 0 else sf.F
        vec = [plan[s] for s in sf.seqs[p]]
        assert all(v >= 0 for v in vec)
        assert [sum(a * b for a, b in zip(row, vec)) for row in rows] == [1] + [0] * (len(rows) - 1)


def check_optimal(tree, value, x, y):
    sf = SequenceForm(tree)
    check_plans(sf, x, y)
    bx, by = behavior(sf, 0, x), behavior(sf, 1, y)
    # x guarantees the value against every pure strategy of player 2, and y holds player 1 to it.
    assert min(expected(tree, (bx, s)) for s in pure_strategies(sf, 1)) == value
    assert max(expected(tree, (s, by)) for s in pure_strategies(sf, 0)) == value
    # The sequence form computes the same payoff as the tree.
    A = sf.matrix()
    xs = [x[s] for s in sf.seqs[0]]
    ys = [y[s] for s in sf.seqs[1]]
    assert sum(xs[i] * A[i][j] * ys[j] for i in range(len(xs)) for j in range(len(ys))) == value == expected(tree, (bx, by))
    return sf


def test_page_example():
    sf = SequenceForm(PAGE_GAME)
    assert sf.seqs[0] == [(), (("root", "L"),), (("root", "R"),),
                          (("root", "R"), ("late", "c")), (("root", "R"), ("late", "d"))]
    assert sf.seqs[1] == [(), (("p2", "a"),), (("p2", "b"),)]
    assert sf.E == [[1, 0, 0, 0, 0], [1, -1, -1, 0, 0], [0, 0, 1, -1, -1]]
    assert sf.matrix() == [[0, 0, 0], [1, 0, 0], [0, 0, 0], [0, 3, 0], [0, 0, 2]]
    value, x, y = solve(PAGE_GAME)
    assert value == F(6, 5)
    assert [x[s] for s in sf.seqs[0]] == [1, 0, 1, F(2, 5), F(3, 5)]
    assert [y[s] for s in sf.seqs[1]] == [1, F(2, 5), F(3, 5)]
    check_optimal(PAGE_GAME, value, x, y)


def test_kuhn_poker():
    tree = kuhn_poker()
    value, x, y = solve(tree)
    assert value == F(-1, 18)
    sf = check_optimal(tree, value, x, y)
    assert len(sf.seqs[0]) == 13 and len(sf.seqs[1]) == 13  # 1 + 6 information sets * 2 actions
    # In every equilibrium player 1 never bets with Q at the root, and always calls a bet with K.
    b1 = behavior(sf, 0, x)
    assert b1["1Q"]["bet"] == 0 and b1["1Kkb"]["call"] == 1


def random_game(rng, max_pure):
    while True:
        sizes = {}

        def build(depth, hist, own):
            if depth == 0 or (hist and rng.random() < 0.2):
                return ("leaf", rng.randint(-6, 6))
            if rng.random() < 0.15:
                p = F(rng.randint(1, 3), 4)
                return ("chance", [(p, build(depth - 1, hist + ("c0",), own)),
                                   (1 - p, build(depth - 1, hist + ("c1",), own))])
            # Mostly alternate, so that a player often moves after moves that are hidden.
            last = next((e[0] for e in reversed(hist) if isinstance(e, tuple)), rng.randint(1, 2))
            player = 3 - last if rng.random() < 0.8 else last
            # The player sees the whole history or only their own moves; both keep perfect recall.
            h = (player, own[player - 1], hist if rng.random() < 0.3 else None)
            k = sizes.setdefault(h, rng.randint(2, 3))
            moves = []
            for t in range(k):
                nxt = list(own)
                nxt[player - 1] = own[player - 1] + ((h, t),)
                moves.append((t, build(depth - 1, hist + ((player, t),), tuple(nxt))))
            return ("move", player, h, moves)

        tree = build(rng.randint(2, 4), (), ((), ()))
        sf = SequenceForm(tree)
        counts = [1, 1]
        for p in range(2):
            for _, actions in sf.infosets[p].values():
                counts[p] *= len(actions)
        if max(counts) <= max_pure:
            return tree


def test_random_games_against_normal_form():
    rng = random.Random(2718)
    hidden = 0
    for _ in range(40):
        tree = random_game(rng, 24)
        value, x, y = solve(tree)
        sf = check_optimal(tree, value, x, y)
        assert value == normal_form_value(tree, sf)
        # Some information set has more than one node exactly when there are fewer
        # nonempty sequences than edges out of decision nodes.
        hidden += len(sf.seqs[0]) + len(sf.seqs[1]) - 2 < count_move_edges(tree)
    assert hidden >= 10


def count_move_edges(node):
    if node[0] == "leaf":
        return 0
    children = [c for _, c in node[-1]]
    return (node[0] == "move") * len(children) + sum(count_move_edges(c) for c in children)


def test_sequence_counts_are_linear():
    # k parallel information sets after a chance move: 2^k pure strategies, 1 + 2k sequences.
    k = 6
    tree = ("chance", [(F(1, k), ("move", 1, i, [(0, ("move", 2, "q", [(0, ("leaf", i)), (1, ("leaf", -i))])),
                                                 (1, ("move", 2, "q", [(0, ("leaf", -1)), (1, ("leaf", 1))]))]))
                       for i in range(k)])
    sf = SequenceForm(tree)
    assert len(sf.seqs[0]) == 1 + 2 * k and len(sf.seqs[1]) == 3
    value, x, y = solve(tree)
    check_optimal(tree, value, x, y)


def test_rejects_imperfect_recall():
    # Player 1 forgets the first own move: the set "h" is reached after (L) and after (R).
    tree = ("move", 1, "first", [
        ("L", ("move", 1, "h", [("a", ("leaf", 1)), ("b", ("leaf", 0))])),
        ("R", ("move", 1, "h", [("a", ("leaf", 0)), ("b", ("leaf", 1))])),
    ])
    try:
        SequenceForm(tree)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_rejects_bad_information_sets():
    for tree in (
        ("move", 1, "h", [("a", ("move", 2, "h", [("x", ("leaf", 0))]))]),
        ("chance", [(F(1, 2), ("move", 1, "h", [("a", ("leaf", 0))])),
                    (F(1, 2), ("move", 1, "h", [("b", ("leaf", 0))]))]),
    ):
        try:
            SequenceForm(tree)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")
