# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/single-peaked-recognition/. The authors are listed in prov/HW79QR.jsonl.
"""Recognize single-peaked profiles and find an axis, in O(m n) time.

The candidates are 0, ..., m - 1 and a profile is a sequence of n rankings, each a tuple of all
m candidates, best first. The algorithm builds the axis from the two ends inward: at each
step the candidates that some voter ranks last among the unplaced ones must go to the free
ends. This is the algorithm of Doignon and Falmagne (1994) and Escoffier, Lang and Ozturk
(2008) in the form of Elkind, Lackner and Peters (survey, Algorithm 1).

Free choices are made in a fixed way: the smaller candidate goes to the left.
"""

from typing import Optional, Sequence

Ranking = Sequence[int]


def single_peaked_axis(profile: Sequence[Ranking], m: int) -> Optional[tuple]:
    """Return an axis (a tuple of all m candidates, left to right) on which every ranking of
    the profile is single-peaked, or None if there is no such axis."""
    n = len(profile)
    if n == 0:
        return tuple(range(m))
    pos = []
    for r in profile:  # @line L1
        p = [0] * m
        for k, a in enumerate(r):
            p[a] = k
        pos.append(p)
    top = [0] * n
    bot = [m - 1] * n
    placed = [False] * m
    left, right = [], []  # @line L2
    rest = m
    while rest >= 2:  # @line L3
        B = {profile[i][bot[i]] for i in range(n)}  # @line L4
        if len(B) >= 3:  # @line L5
            return None
        B = sorted(B)
        if not right:  # @line L6
            left.append(B[0])  # @line L7
            if len(B) == 2:
                right.append(B[1])
        else:  # @line L8
            l, r = left[-1], right[-1]  # @line L9
            to_left, to_right = set(), set()
            for x in B:
                for i in range(n):
                    if profile[i][top[i]] == x:
                        continue
                    p = pos[i]
                    if p[r] < p[x] < p[l]:
                        to_left.add(x)  # @line L10
                    if p[l] < p[x] < p[r]:
                        to_right.add(x)  # @line L11
            if len(to_left) >= 2 or len(to_right) >= 2 or to_left & to_right:  # @line L12
                return None
            free = [x for x in B if x not in to_left and x not in to_right]  # @line L13
            for x in free:
                if not to_left:
                    to_left.add(x)
                else:
                    to_right.add(x)
            left.extend(to_left)  # @line L14
            right.extend(to_right)
        for x in B:  # @line L15
            placed[x] = True
        rest -= len(B)
        if rest == 0:
            break
        for i in range(n):
            r = profile[i]
            while placed[r[bot[i]]]:
                bot[i] -= 1
            while placed[r[top[i]]]:
                top[i] += 1
    middle = [a for a in range(m) if not placed[a]]
    return tuple(left + middle + right[::-1])  # @line L16


def is_single_peaked(profile: Sequence[Ranking], m: int) -> bool:
    """Return True if the profile is single-peaked on some axis."""
    return single_peaked_axis(profile, m) is not None
