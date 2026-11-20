# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brams-taylor-procedure/. The authors are listed in prov/MN3VTM.jsonl.
"""A toy version of the Brams-Taylor procedure, for three agents only.

This is a toy. It keeps the outer loop of the page: for each ordered pair
(i, j) it runs rounds on the leftover until agent i has an irrevocable
advantage over agent j, and then it gives the last leftover to any agent.
It does not implement the sub-protocols of Brams and Taylor for n agents.
Each round is the first stage of the Selfridge-Conway procedure, with agent
i as the cutter, so the toy works for three agents only. A round gives i an
advantage over the agent that takes the trimmed piece, but it cannot choose
that agent, so the loop has no bound in general. After max_rounds rounds the
toy stops the loop and divides the leftover with the second stage of the
Selfridge-Conway procedure, which is envy-free because the cutter of the
last round has an irrevocable advantage over the taker of its trimmed piece.
"""

from fractions import Fraction

from agtcake import Oracle

Interval = tuple[Fraction, Fraction]
Piece = list[Interval]


def piece_eval(oracle: Oracle, i: int, piece: Piece) -> Fraction:
    """V_i(piece), with one eval query per interval."""
    return sum((oracle.eval_query(i, a, b) for a, b in piece), Fraction(0))


def split_prefix(oracle: Oracle, i: int, piece: Piece, t: Fraction) -> tuple[Piece, Piece]:
    """Split a piece into a prefix of value t to agent i and the rest.

    The intervals of the piece are in increasing order. Needs t <= V_i(piece).
    """
    head: Piece = []
    rest: Piece = []
    left = t
    for idx, (a, b) in enumerate(piece):
        v = oracle.eval_query(i, a, b)
        if v <= left and left > 0:
            head.append((a, b))
            left -= v
            continue
        x = oracle.cut_query(i, a, left) if left > 0 else a
        if x > a:
            head.append((a, x))
        if b > x:
            rest.append((x, b))
        rest.extend(piece[idx + 1:])
        break
    return head, rest


def has_advantage(own: Fraction, other: Fraction, leftover: Fraction) -> bool:
    """V_i(X_i) - V_i(X_j) >= V_i(R): agent i cannot come to envy agent j."""
    return own - other >= leftover


def advantage(oracle: Oracle, i: int, j: int, alloc: dict[int, Piece], rest: Piece) -> bool:
    return has_advantage(piece_eval(oracle, i, alloc[i]), piece_eval(oracle, i, alloc[j]),
                         piece_eval(oracle, i, rest))


def trimming_round(oracle: Oracle, rest: Piece, cutter: int, trimmer: int,
                   chooser: int) -> tuple[dict[int, Piece], Piece, int]:
    """Stage one of Selfridge-Conway on the leftover.

    Returns the three pieces given out, the new leftover (the trimmings) and
    the agent that took the trimmed piece.
    """
    third = piece_eval(oracle, cutter, rest) / 3
    p0, more = split_prefix(oracle, cutter, rest, third)
    p1, p2 = split_prefix(oracle, cutter, more, third)
    pieces = [p0, p1, p2]
    vals = [piece_eval(oracle, trimmer, p) for p in pieces]
    order = sorted(range(3), key=lambda k: (-vals[k], k))
    p, q = order[0], order[1]
    trimmings: Piece = []
    if vals[p] > vals[q]:
        pieces[p], trimmings = split_prefix(oracle, trimmer, pieces[p], vals[q])
    left = [0, 1, 2]
    cv = [piece_eval(oracle, chooser, pieces[k]) for k in left]
    c = cv.index(max(cv))
    left.remove(c)
    if p in left:
        t = p
    else:
        t = left[0] if vals[left[0]] >= vals[left[1]] else left[1]
    left.remove(t)
    give = {chooser: pieces[c], trimmer: pieces[t], cutter: pieces[left[0]]}
    taker = chooser if c == p else trimmer
    return give, trimmings, taker


def finish_stage_two(oracle: Oracle, alloc: dict[int, Piece], rest: Piece, cutter: int,
                     taker: int) -> None:
    """Stage two of Selfridge-Conway: needs that cutter has an advantage over taker."""
    other = 3 - cutter - taker
    third = piece_eval(oracle, other, rest) / 3
    a, more = split_prefix(oracle, other, rest, third)
    b, c = split_prefix(oracle, other, more, third)
    parts = [a, b, c]
    for agent in (taker, cutter):
        vals = [piece_eval(oracle, agent, part) for part in parts]
        alloc[agent].extend(parts.pop(vals.index(max(vals))))
    alloc[other].extend(parts[0])


def brams_taylor_toy(oracle: Oracle, max_rounds: int = 40) -> tuple[dict[int, Piece], int]:
    """Return an envy-free division of [0, 1] among three agents and the number of rounds."""
    if oracle.n != 3:
        raise ValueError("this toy is for three agents")
    if max_rounds < 1:
        raise ValueError("max_rounds must be at least 1")
    alloc: dict[int, Piece] = {0: [], 1: [], 2: []}
    rest: Piece = [(Fraction(0), Fraction(1))]  # @line L1
    rounds = 0
    last = (0, 1)
    for i in range(3):
        for j in range(3):  # @line L2
            if i == j:
                continue
            k = 3 - i - j
            while not advantage(oracle, i, j, alloc, rest):  # @line L3
                if rounds == max_rounds:
                    finish_stage_two(oracle, alloc, rest, *last)
                    return alloc, rounds
                trimmer, chooser = (j, k) if rounds % 2 == 0 else (k, j)  # @line L4
                # i gains over the taker of the trimmed piece, not always over j
                give, trimmings, taker = trimming_round(oracle, rest, i, trimmer, chooser)  # @line L5
                for agent, piece in give.items():
                    alloc[agent].extend(piece)  # @line L6
                rest = trimmings  # @line L7
                last = (i, taker)
                rounds += 1
    alloc[0].extend(rest)  # @line L8
    return alloc, rounds  # @line L9
