# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subgame-perfect-equilibrium/. The authors are listed in prov/E96CN1.jsonl.

import random
from fractions import Fraction as F
from itertools import product

from subgame_perfect_equilibrium import (
    all_pure_profiles,
    backward_induction,
    is_nash_in_subgame,
    is_subgame_perfect,
    move_nodes,
    play_value,
)

# The entry game: player 0 chooses Out (0, 2) or In; after In, player 1
# chooses Fight (-1, -1) or Accommodate (1, 1).
ENTRY = {
    0: ("move", 0, [("Out", 1), ("In", 2)]),
    1: ("leaf", (F(0), F(2))),
    2: ("move", 1, [("Fight", 3), ("Accommodate", 4)]),
    3: ("leaf", (F(-1), F(-1))),
    4: ("leaf", (F(1), F(1))),
}


def test_entry_game() -> None:
    value, profile, calls = backward_induction(ENTRY)
    assert profile == {0: "In", 2: "Accommodate"}
    assert value[0] == (1, 1)
    assert calls == 5
    nash = [p for p in all_pure_profiles(ENTRY) if is_nash_in_subgame(ENTRY, p, 0)]
    assert sorted((p[0], p[2]) for p in nash) == [("In", "Accommodate"), ("Out", "Fight")]
    spe = [p for p in all_pure_profiles(ENTRY) if is_subgame_perfect(ENTRY, p)]
    assert spe == [{0: "In", 2: "Accommodate"}]


def centipede(stages: int):
    # At stage k the mover can take, ending the game, or pass. Taking at stage
    # k gives the mover k + 2 and the other k; passing at the last stage gives
    # both stages.
    tree = {}
    for k in range(stages):
        mover = k % 2
        take = 2 * k + 1
        nxt = 2 * k + 2 if k + 1 < stages else 2 * stages
        tree[2 * k] = ("move", mover, [("Take", take), ("Pass", nxt)])
        pay = [F(k), F(k)]
        pay[mover] = F(k + 2)
        tree[take] = ("leaf", tuple(pay))
    tree[2 * stages] = ("leaf", (F(stages), F(stages)))
    return tree


def test_centipede_takes_at_once() -> None:
    tree = centipede(6)
    value, profile, _ = backward_induction(tree)
    assert all(a == "Take" for a in profile.values())
    assert value[0] == (2, 0)
    assert is_subgame_perfect(tree, profile)


def random_tree(rng, depth, players, generic, chance_prob):
    tree = {}
    counter = [0]
    used = [set() for _ in range(players)]

    def new_id():
        counter[0] += 1
        return counter[0] - 1

    def payoff(i):
        if not generic:
            return F(rng.randint(0, 1))
        while True:
            v = rng.randint(-50, 50)
            if v not in used[i]:
                used[i].add(v)
                return F(v)

    def build(d):
        h = new_id()
        if d == 0 or (d < depth and rng.random() < 0.25):
            tree[h] = ("leaf", tuple(payoff(i) for i in range(players)))
            return h
        if rng.random() < chance_prob:
            k = rng.randint(2, 3)
            w = [rng.randint(1, 4) for _ in range(k)]
            probs = [F(x, sum(w)) for x in w]
            tree[h] = ("chance", [(p, build(d - 1)) for p in probs])
            return h
        i = rng.randrange(players)
        k = rng.randint(2, 3)
        tree[h] = ("move", i, [(a, build(d - 1)) for a in range(k)])
        return h

    build(depth)
    return tree


def small_random_tree(rng, generic, chance_prob):
    while True:
        tree = random_tree(rng, 3, rng.randint(2, 3), generic, chance_prob)
        if 1 <= len(move_nodes(tree)) <= 5:
            return tree


def all_tie_breaks(tree, h=0):
    # Every (value, partial profile) that backward induction can return at h
    # under some rule for breaking ties.
    node = tree[h]
    if node[0] == "leaf":
        return [(tuple(node[1]), {})]
    if node[0] == "chance":
        options = [all_tie_breaks(tree, c) for _, c in node[1]]
        out = []
        for pick in product(*options):
            n = len(pick[0][0])
            v = tuple(sum((p * r[0][k] for (p, _), r in zip(node[1], pick)), F(0)) for k in range(n))
            prof = {}
            for r in pick:
                prof.update(r[1])
            out.append((v, prof))
        return out
    _, i, moves = node
    options = [all_tie_breaks(tree, c) for _, c in moves]
    out = []
    for pick in product(*options):
        best = max(r[0][i] for r in pick)
        for (a, _), r in zip(moves, pick):
            if r[0][i] == best:
                prof = {}
                for s in pick:
                    prof.update(s[1])
                prof[h] = a
                out.append((r[0], prof))
    return out


def test_generic_payoffs_give_a_unique_spe() -> None:
    rng = random.Random(1)
    for _ in range(25):
        tree = small_random_tree(rng, generic=True, chance_prob=0.0)
        value, profile, calls = backward_induction(tree)
        assert calls == len(tree)
        spe = [p for p in all_pure_profiles(tree) if is_subgame_perfect(tree, p)]
        assert spe == [profile]
        assert play_value(tree, profile) == value[0]


def test_ties_and_chance_match_brute_force() -> None:
    rng = random.Random(2)
    several = 0
    for _ in range(25):
        tree = small_random_tree(rng, generic=False, chance_prob=0.3)
        value, profile, _ = backward_induction(tree)
        assert is_subgame_perfect(tree, profile)
        assert play_value(tree, profile) == value[0]
        spe = [p for p in all_pure_profiles(tree) if is_subgame_perfect(tree, p)]
        breaks = [p for _, p in all_tie_breaks(tree)]
        key = lambda p: tuple(sorted(p.items()))
        assert sorted(map(key, spe)) == sorted(set(map(key, breaks)))
        several += len(spe) > 1
    assert several >= 5  # with ties, a game can have several pure SPE
