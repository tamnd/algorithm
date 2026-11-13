# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hex-game/. The authors are listed in prov/S7E34P.jsonl.

"""Hex on an n x n rhombus, with an exhaustive solver for small boards.

Cell (r, c) has index r * n + c. Red moves first and joins the top row
(r = 0) to the bottom row (r = n - 1); Blue joins the left column (c = 0)
to the right column (c = n - 1). Cell (r, c) touches the six cells
(r - 1, c), (r - 1, c + 1), (r, c - 1), (r, c + 1), (r + 1, c - 1) and
(r + 1, c). A position is a pair of bitmasks (red, blue)."""

from functools import lru_cache
from typing import Dict, List, Optional, Tuple

STEPS = ((-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0))


@lru_cache(maxsize=None)
def neighbors(n: int) -> Tuple[Tuple[int, ...], ...]:
    out = []
    for r in range(n):
        for c in range(n):
            out.append(tuple((r + dr) * n + c + dc for dr, dc in STEPS if 0 <= r + dr < n and 0 <= c + dc < n))
    return tuple(out)


def connects(n: int, stones: int, red: bool) -> bool:
    """True when the stones join the two sides of their owner: top to bottom
    for Red, left to right for Blue. Depth-first search over the stones."""
    nb = neighbors(n)
    start = range(n) if red else range(0, n * n, n)
    stack = [s for s in start if stones >> s & 1]
    seen = 0
    for s in stack:
        seen |= 1 << s
    while stack:
        v = stack.pop()
        r, c = divmod(v, n)
        if (r if red else c) == n - 1:
            return True
        for w in nb[v]:
            if stones >> w & 1 and not seen >> w & 1:
                seen |= 1 << w
                stack.append(w)
    return False


def winner(n: int, red: int, blue: int) -> Optional[str]:
    """'R', 'B' or None. Both cannot hold on a legal position."""
    if connects(n, red, True):
        return "R"
    if connects(n, blue, False):
        return "B"
    return None


def full_board_winners(n: int, red: int) -> Tuple[bool, bool]:
    """On a full board where red holds the cells in the mask and Blue holds
    the rest, return (Red connects, Blue connects)."""
    blue = ((1 << (n * n)) - 1) & ~red
    return connects(n, red, True), connects(n, blue, False)


def _order(n: int) -> List[int]:
    """Cells sorted by distance from the center: good moves come first."""
    mid = (n - 1) / 2
    return sorted(range(n * n), key=lambda v: abs(v // n - mid) + abs(v % n - mid))


def solver(n: int):
    """Return mover_wins(red, blue): True when the player to move wins.
    Red is to move when both colors have the same number of stones. The
    memo holds every solved position."""
    cells = _order(n)
    memo: Dict[Tuple[int, int], bool] = {}

    def mover_wins(red: int, blue: int) -> bool:
        key = (red, blue)
        if key in memo:
            return memo[key]
        red_turn = bin(red).count("1") == bin(blue).count("1")
        empty = [v for v in cells if not (red | blue) >> v & 1]
        result = False
        for v in empty:
            if red_turn:
                nr, nb = red | 1 << v, blue
                if connects(n, nr, True) or not mover_wins(nr, nb):
                    result = True
                    break
            else:
                nr, nb = red, blue | 1 << v
                if connects(n, nb, False) or not mover_wins(nr, nb):
                    result = True
                    break
        memo[key] = result
        return result

    return mover_wins


def first_player_wins(n: int) -> bool:
    return solver(n)(0, 0)


def winning_openings(n: int) -> List[Tuple[int, int]]:
    """All first moves of Red that win, as (row, column)."""
    mover_wins = solver(n)
    return [divmod(v, n) for v in range(n * n) if not mover_wins(1 << v, 0)]


def play_out(n: int, rng) -> Tuple[int, int, str]:
    """Fill the board by random moves to the end, without stopping at a win,
    and return the full board and its winner."""
    order = list(range(n * n))
    rng.shuffle(order)
    red = blue = 0
    for i, v in enumerate(order):
        if i % 2 == 0:
            red |= 1 << v
        else:
            blue |= 1 << v
    w = winner(n, red, blue)
    assert w is not None
    return red, blue, w
