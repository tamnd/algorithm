# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horizon-effect/. The authors are listed in prov/86NNG4.jsonl.

"""The horizon effect on small game trees.

A game is given by `kids[n]`, a list of (child, is_capture) pairs, and
`static[n]`, the static score for the side to move at n. Values are negamax
values. `limited_value` is a search with a fixed depth, with or without a
quiescence search of the captures at the frontier, and `exact_value` searches
the whole tree. The two built-in trees show the two forms of the effect that
the page describes.
"""

import random
from typing import Dict, List, Tuple

Kids = Dict[str, List[Tuple[str, bool]]]
Static = Dict[str, int]


def exact_value(kids: Kids, static: Static, n: str) -> int:
    """Negamax value of the whole finite tree below n. Cost: one visit per node."""
    ch = kids.get(n, [])
    if not ch:
        return static[n]
    return max(-exact_value(kids, static, c) for c, _ in ch)


def quiesce_value(kids: Kids, static: Static, n: str) -> int:
    """Value of the capture-or-stop game at n: stand pat, or a capture."""
    return max([static[n]] + [-quiesce_value(kids, static, c) for c, cap in kids.get(n, []) if cap])


def limited_value(kids: Kids, static: Static, n: str, depth: int, quiescence: bool) -> int:
    """Negamax value to `depth` plies; the frontier gets the static score, or the
    quiescence value when `quiescence` is true. Cost: O(b^depth) without quiescence."""
    ch = kids.get(n, [])
    if not ch:
        return static[n]
    if depth == 0:
        return quiesce_value(kids, static, n) if quiescence else static[n]
    return max(-limited_value(kids, static, c, depth - 1, quiescence) for c, _ in ch)


def root_choice(kids: Kids, static: Static, root: str, depth: int, quiescence: bool) -> Tuple[str, int]:
    """The first move with the best value of a depth-limited search, and the value."""
    best, bv = "", -10**9
    for c, _ in kids[root]:
        v = -limited_value(kids, static, c, depth - 1, quiescence)
        if v > bv:
            best, bv = c, v
    return best, bv


def capture_past_horizon() -> Tuple[Kids, Static]:
    """White's QxP wins a pawn, but the rook takes the queen one ply later."""
    kids: Kids = {
        "A": [("QxP", True), ("quiet", False)],
        "QxP": [("RxQ", True), ("QxP-quiet", False)],
        "quiet": [("quiet-reply", False)],
        "RxQ": [("RxQ-end", False)],
        "QxP-quiet": [("QxP-end", False)],
        "quiet-reply": [("quiet-end", False)],
    }
    static: Static = {"A": 0, "QxP": -1, "quiet": 0, "RxQ": -8, "QxP-quiet": 1,
                      "quiet-reply": 0, "RxQ-end": 8, "QxP-end": -1, "quiet-end": 0}
    return kids, static


def delaying_sacrifice() -> Tuple[Kids, Static]:
    """The negative horizon effect. The white queen is lost in every line. Move
    "let" lets Black take it at once. Move "sac" first gives a pawn, so the
    queen is taken two plies later, past the horizon of a depth-2 search."""
    kids: Kids = {
        "R": [("let", False), ("sac", False)],
        "let": [("let-RxQ", True)],
        "let-RxQ": [("let-a", False)],
        "let-a": [("let-b", False)],
        "sac": [("sac-PxP", True)],
        "sac-PxP": [("sac-a", False)],
        "sac-a": [("sac-RxQ", True)],
        "sac-RxQ": [("sac-b", False)],
    }
    static: Static = {"R": 0, "let": 0, "let-RxQ": -9, "let-a": 9, "let-b": -9,
                      "sac": 0, "sac-PxP": -1, "sac-a": 1, "sac-RxQ": -10, "sac-b": 10}
    return kids, static


def random_material_tree(rng: random.Random, b: int, height: int, capture_p: float = 0.35) -> Tuple[Kids, Static]:
    """A random tree in which a capture wins 1, 3, 3, 5 or 9 points and a quiet
    move changes the score by -1, 0 or +1. Node names are paths of digits."""
    kids: Kids = {}
    static: Static = {"r": 0}
    frontier = ["r"]
    for _ in range(height):
        nxt = []
        for n in frontier:
            row = []
            for i in range(b):
                cap = rng.random() < capture_p
                gain = rng.choice((1, 3, 3, 5, 9)) if cap else rng.randint(-1, 1)
                c = f"{n}{i}"
                static[c] = -(static[n] + gain)
                row.append((c, cap))
            kids[n] = row
            nxt.extend(c for c, _ in row)
        frontier = nxt
    return kids, static


def wrong_choices(seed: int, trees: int, b: int, height: int, depth: int) -> Tuple[int, int]:
    """Count the trees in which the root move of a depth-limited search is worse
    than the best move by the exact value: (without quiescence, with quiescence)."""
    rng = random.Random(seed)
    plain = quiet = 0
    for _ in range(trees):
        kids, static = random_material_tree(rng, b, height)
        best = exact_value(kids, static, "r")
        for flag in (False, True):
            move, _ = root_choice(kids, static, "r", depth, flag)
            if -exact_value(kids, static, move) < best:
                if flag:
                    quiet += 1
                else:
                    plain += 1
    return plain, quiet
