# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boutons-theorem/. The authors are listed in prov/9301CP.jsonl.

"""Bouton's theorem for Nim, as executable statements. normal_p and
misere_p are the sets of losing positions that the theorem names, and
label_by_search labels every position by backward induction, so the tests
can compare the two and check each lemma of the proof on its own."""

from functools import reduce
from itertools import product
from typing import Dict, Iterator, List, Sequence, Tuple

Position = Tuple[int, ...]


def nim_sum(heaps: Sequence[int]) -> int:
    return reduce(lambda a, b: a ^ b, heaps, 0)


def moves(heaps: Sequence[int]) -> Iterator[Position]:
    for i, a in enumerate(heaps):
        for b in range(a):
            yield tuple(heaps[:i]) + (b,) + tuple(heaps[i + 1:])


def normal_p(heaps: Sequence[int]) -> bool:
    """The theorem's set P: nim-sum 0."""
    return nim_sum(heaps) == 0


def misere_p(heaps: Sequence[int]) -> bool:
    """The theorem's set M of misere losses for the player to move."""
    if any(h >= 2 for h in heaps):
        return nim_sum(heaps) == 0
    return sum(heaps) % 2 == 1


def winning_moves(heaps: Sequence[int]) -> List[Tuple[int, int]]:
    """Moves (index, new size) that reach nim-sum 0."""
    x = nim_sum(heaps)
    return [(i, a ^ x) for i, a in enumerate(heaps) if a ^ x < a]


def label_by_search(k: int, top: int, misere: bool = False) -> Dict[Position, bool]:
    """Map each position with k heaps of sizes 0..top to True when the
    player to move loses. Positions are visited in order of their total, so
    every option is labeled before the position itself."""
    positions = sorted(product(range(top + 1), repeat=k), key=sum)
    lose: Dict[Position, bool] = {}
    for p in positions:
        opts = list(moves(p))
        if not opts:
            lose[p] = not misere  # no move: a loss in normal play, a win in misere play
        else:
            lose[p] = all(not lose[q] for q in opts)
    return lose
