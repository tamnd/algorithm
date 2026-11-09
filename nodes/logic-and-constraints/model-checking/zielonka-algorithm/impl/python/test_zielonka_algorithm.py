# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zielonka-algorithm/. The authors are listed in prov/X0EDJD.jsonl.

import itertools
import random

import pytest

from zielonka_algorithm import attractor, zielonka

# The worked example of the page.
EXAMPLE = {
    "a": (0, 3, ["b"]),
    "b": (1, 2, ["a", "c"]),
    "c": (0, 1, ["c", "d"]),
    "d": (1, 4, ["e"]),
    "e": (0, 0, ["d", "f"]),
    "f": (1, 5, ["b", "f"]),
}


def random_game(rng: random.Random, n: int, d: int) -> dict:
    game = {}
    for v in range(n):
        k = rng.randint(1, min(3, n))
        game[v] = (rng.randint(0, 1), rng.randint(0, d), rng.sample(range(n), k))
    return game


def bad_cycle_reachable(game, vertices, choice, player, start) -> bool:
    """Is there a cycle with a max priority of the wrong parity for `player`,
    reachable from start, when `player` plays `choice` and the opponent is free?
    A play that leaves `vertices` also counts as a failure."""

    def succ(v):
        return [choice[v]] if game[v][0] == player else game[v][2]

    reach, stack = {start}, [start]
    while stack:
        v = stack.pop()
        for w in succ(v):
            if w not in vertices:
                return True
            if w not in reach:
                reach.add(w)
                stack.append(w)
    for v in reach:
        q = game[v][1]
        if q % 2 == player:
            continue
        # a cycle through v that uses only priorities <= q
        seen, stack = set(), [w for w in succ(v) if game[w][1] <= q]
        while stack:
            w = stack.pop()
            if w == v:
                return True
            if w in seen:
                continue
            seen.add(w)
            stack.extend(x for x in succ(w) if game[x][1] <= q)
    return False


def brute_force(game) -> tuple[set, set]:
    """Winning regions found by trying every positional strategy of each player."""
    regions = []
    for player in (0, 1):
        mine = [v for v in game if game[v][0] == player]
        won = set()
        for picks in itertools.product(*(game[v][2] for v in mine)):
            choice = dict(zip(mine, picks))
            for v in game:
                if v not in won and not bad_cycle_reachable(game, set(game), choice, player, v):
                    won.add(v)
        regions.append(won)
    return regions[0], regions[1]


def small_progress_measures(game) -> set:
    """Jurdzinski's small progress measures, max-parity version. Returns W0."""
    odd = sorted({q for (_, q, _) in game.values() if q % 2 == 1}, reverse=True)
    cap = {q: sum(1 for (_, p, _) in game.values() if p == q) for q in odd}
    top = None  # the value T

    def prog(m, p):
        if m is top:
            return top
        t = [m[k] if q >= p else 0 for k, q in enumerate(odd)]
        if p % 2 == 0:
            return tuple(t)
        for k in range(len(odd) - 1, -1, -1):
            if odd[k] < p:
                continue
            if t[k] < cap[odd[k]]:
                t[k] += 1
                return tuple(t)
            t[k] = 0
        return top

    def key(m):
        return (1,) if m is top else (0, *m)

    rho = {v: tuple(0 for _ in odd) for v in game}
    changed = True
    while changed:
        changed = False
        for v, (owner, p, succ) in game.items():
            vals = [prog(rho[w], p) for w in succ]
            new = min(vals, key=key) if owner == 0 else max(vals, key=key)
            if key(new) > key(rho[v]):
                rho[v] = new
                changed = True
    return {v for v in game if rho[v] is not top}


def check_strategy(game, w0, w1, strat) -> None:
    for player, region in ((0, w0), (1, w1)):
        choice = {}
        for v in region:
            if game[v][0] == player:
                assert strat[v] in game[v][2]
                choice[v] = strat[v]
        for v in region:
            assert not bad_cycle_reachable(game, region, choice, player, v)


def test_example() -> None:
    w0, w1, strat = zielonka(EXAMPLE)
    assert w0 == {"c", "d", "e"}
    assert w1 == {"a", "b", "f"}
    assert strat["e"] == "d" and strat["c"] == "d" and strat["b"] == "a"
    check_strategy(EXAMPLE, w0, w1, strat)
    assert brute_force(EXAMPLE) == (w0, w1)


def test_attractor_example() -> None:
    assert attractor(EXAMPLE, set(EXAMPLE), {"f"}, 1) == ({"f"}, {})
    attr, strat = attractor(EXAMPLE, set(EXAMPLE), {"c"}, 1)
    assert attr == {"a", "b", "c", "f"} and strat == {"b": "c", "f": "b"}
    attr, strat = attractor(EXAMPLE, set(EXAMPLE), {"d"}, 0)
    assert attr == {"c", "d", "e"} and strat == {"c": "d", "e": "d"}


def test_edges() -> None:
    assert zielonka({}) == (set(), set(), {})
    assert zielonka({0: (0, 0, [0])})[:2] == ({0}, set())
    assert zielonka({0: (0, 1, [0])})[:2] == (set(), {0})
    # all priorities equal and even: player 0 wins everywhere
    g = {v: (v % 2, 2, [(v + 1) % 4]) for v in range(4)}
    assert zielonka(g)[:2] == (set(range(4)), set())
    with pytest.raises(ValueError):
        zielonka({0: (0, 0, [])})
    with pytest.raises(ValueError):
        zielonka({0: (0, 0, [1])})


def test_against_brute_force_and_spm() -> None:
    rng = random.Random(2024)
    for trial in range(600):
        n = rng.randint(1, 6)
        game = random_game(rng, n, rng.randint(0, 5))
        w0, w1, strat = zielonka(game)
        assert w0 | w1 == set(game) and not (w0 & w1)
        assert brute_force(game) == (w0, w1), (trial, game)
        assert small_progress_measures(game) == w0
        check_strategy(game, w0, w1, strat)


def test_larger_against_spm() -> None:
    rng = random.Random(7)
    for _ in range(60):
        game = random_game(rng, 40, 8)
        w0, w1, strat = zielonka(game)
        assert small_progress_measures(game) == w0
        check_strategy(game, w0, w1, strat)
