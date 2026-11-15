# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/team-draft-interleaving/. The authors are listed in prov/8FBQBW.jsonl.

from typing import Callable, Collection, Hashable, Sequence


def interleave(
    a: Sequence[Hashable], b: Sequence[Hashable], coin: Callable[[], int]
) -> tuple[list[Hashable], set[Hashable], set[Hashable]]:
    """Return the shown list and the teams of a and b for team-draft interleaving.

    Precondition: a and b have no repeated documents. coin() returns 0 or 1 and is
    called only when the two teams have the same size, once per round. The pointers
    ia and ib only move forward, so the time is O(len(a) + len(b)) with hash sets,
    and the extra space is O(len(a) + len(b)).
    """
    shown: list[Hashable] = []
    seen: set[Hashable] = set()
    team_a: set[Hashable] = set()
    team_b: set[Hashable] = set()  # @line L1
    ia, ib = 0, 0
    while True:
        while ia < len(a) and a[ia] in seen:
            ia += 1
        while ib < len(b) and b[ib] in seen:
            ib += 1
        if ia == len(a) or ib == len(b):  # @line L2
            break
        if len(team_a) < len(team_b) or (len(team_a) == len(team_b) and coin() == 1):  # @line L3
            d = a[ia]  # @line L4
            shown.append(d)  # @line L5
            seen.add(d)
            team_a.add(d)
        else:  # @line L6
            d = b[ib]  # @line L7
            shown.append(d)  # @line L8
            seen.add(d)
            team_b.add(d)
    return shown, team_a, team_b  # @line L9


def credit(team_a: Collection[Hashable], team_b: Collection[Hashable], clicked: Collection[Hashable]) -> int:
    """Return 1 if the clicks prefer a, -1 if they prefer b, and 0 for a tie.

    Precondition: team_a and team_b are disjoint sets. O(len(clicked)) time.
    """
    ha = sum(1 for d in clicked if d in team_a)  # @line L10
    hb = sum(1 for d in clicked if d in team_b)
    return (ha > hb) - (ha < hb)  # @line L11
