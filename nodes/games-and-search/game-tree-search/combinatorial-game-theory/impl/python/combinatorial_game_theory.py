# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/combinatorial-game-theory/. The authors are listed in prov/JY9MWF.jsonl.

"""Short partisan games as pairs (left options, right options), with sums,
negation, outcome classes by search, and comparison through the rule
G >= H exactly when Left wins G - H whenever Right moves first.

A game is a Game(L, R) where L and R are frozensets of games. Equal games
in this sense are not merged; equality of values is tested with eq."""

from functools import lru_cache
from typing import Dict, FrozenSet, Iterable, Tuple


class Game:
    __slots__ = ("left", "right", "_h")

    def __init__(self, left: Iterable["Game"] = (), right: Iterable["Game"] = ()):
        self.left: FrozenSet[Game] = frozenset(left)
        self.right: FrozenSet[Game] = frozenset(right)
        self._h = hash((self.left, self.right))

    def __hash__(self) -> int:
        return self._h

    def __eq__(self, other) -> bool:  # structural identity, not value equality
        return isinstance(other, Game) and self.left == other.left and self.right == other.right

    def __add__(self, other: "Game") -> "Game":
        return add(self, other)

    def __neg__(self) -> "Game":
        return neg(self)

    def __sub__(self, other: "Game") -> "Game":
        return add(self, neg(other))


@lru_cache(maxsize=None)
def add(g: Game, h: Game) -> Game:
    left = {add(gl, h) for gl in g.left} | {add(g, hl) for hl in h.left}
    right = {add(gr, h) for gr in g.right} | {add(g, hr) for hr in h.right}
    return Game(left, right)


@lru_cache(maxsize=None)
def neg(g: Game) -> Game:
    return Game({neg(gr) for gr in g.right}, {neg(gl) for gl in g.left})


@lru_cache(maxsize=None)
def left_first_wins(g: Game) -> bool:
    """Left moves first and wins: some left option is not a win for Right moving first."""
    return any(not right_first_wins(gl) for gl in g.left)


@lru_cache(maxsize=None)
def right_first_wins(g: Game) -> bool:
    return any(not left_first_wins(gr) for gr in g.right)


def outcome(g: Game) -> str:
    """'L' (Left wins), 'R' (Right wins), 'N' (first player wins) or 'P'
    (second player wins), under normal play."""
    lf, rf = left_first_wins(g), right_first_wins(g)
    if lf and not rf:
        return "L"
    if rf and not lf:
        return "R"
    return "N" if lf else "P"


def ge(g: Game, h: Game) -> bool:
    return not right_first_wins(g - h)


def eq(g: Game, h: Game) -> bool:
    return outcome(g - h) == "P"


def lt(g: Game, h: Game) -> bool:
    return ge(h, g) and not ge(g, h)


def fuzzy(g: Game, h: Game) -> bool:
    return outcome(g - h) == "N"


ZERO = Game()
STAR = Game({ZERO}, {ZERO})
ONE = Game({ZERO}, ())
MINUS_ONE = Game((), {ZERO})
TWO = Game({ONE}, ())
HALF = Game({ZERO}, {ONE})
QUARTER = Game({ZERO}, {HALF})
UP = Game({ZERO}, {STAR})
DOWN = Game({STAR}, {ZERO})
PLUS_MINUS_ONE = Game({ONE}, {MINUS_ONE})


def nimber(n: int) -> Game:
    heaps = []
    for k in range(n):
        heaps.append(Game(heaps[:k], heaps[:k]))
    return Game(heaps, heaps)


def integer(n: int) -> Game:
    g = ZERO
    for _ in range(abs(n)):
        g = Game({g}, ()) if n > 0 else Game((), {g})
    return g


# Domineering: Left places vertical dominoes, Right horizontal ones.

@lru_cache(maxsize=None)
def domineering(cells: FrozenSet[Tuple[int, int]]) -> Game:
    left, right = set(), set()
    for (r, c) in cells:
        if (r + 1, c) in cells:
            left.add(domineering(cells - {(r, c), (r + 1, c)}))
        if (r, c + 1) in cells:
            right.add(domineering(cells - {(r, c), (r, c + 1)}))
    return Game(left, right)


def board(rows: int, cols: int) -> FrozenSet[Tuple[int, int]]:
    return frozenset((r, c) for r in range(rows) for c in range(cols))
