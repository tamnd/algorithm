# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aziz-mackenzie-protocol/. The authors are listed in prov/3197Z9.jsonl.
"""A toy version of the Aziz-Mackenzie protocol, for three agents only.

This is a toy. It keeps the recursion of the page: give out parts of the
leftover in envy-free rounds until some agent dominates every other agent,
then remove that agent and divide the leftover among the others in the same
way. It does not implement the core protocol or the other sub-protocols of
Aziz and Mackenzie, so it has none of their bounds. With three agents a
round is the first stage of the Selfridge-Conway procedure, with the cutter
taking turns. With two agents a round is divide and choose, which leaves
nothing over. The toy cannot force domination with three agents, so after
max_rounds rounds it divides the leftover with the second stage of the
Selfridge-Conway procedure, which is envy-free because the cutter of the
last round dominates the agent that took the trimmed piece.
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


def dominates_value(own: Fraction, other: Fraction, leftover: Fraction) -> bool:
    """V_i(X_i) - V_i(X_j) >= V_i(R)."""
    return own - other >= leftover


def dominates(oracle: Oracle, i: int, j: int, alloc: dict[int, Piece], rest: Piece) -> bool:
    return dominates_value(piece_eval(oracle, i, alloc[i]), piece_eval(oracle, i, alloc[j]),
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


def cut_and_choose(oracle: Oracle, rest: Piece, cutter: int, chooser: int) -> dict[int, Piece]:
    """Divide and choose on the leftover: it gives out all of it."""
    a, b = split_prefix(oracle, cutter, rest, piece_eval(oracle, cutter, rest) / 2)
    if piece_eval(oracle, chooser, a) >= piece_eval(oracle, chooser, b):
        return {chooser: a, cutter: b}
    return {chooser: b, cutter: a}


def finish_stage_two(oracle: Oracle, alloc: dict[int, Piece], rest: Piece, cutter: int,
                     taker: int) -> None:
    """Stage two of Selfridge-Conway: needs that cutter dominates taker."""
    other = 3 - cutter - taker
    third = piece_eval(oracle, other, rest) / 3
    a, more = split_prefix(oracle, other, rest, third)
    b, c = split_prefix(oracle, other, more, third)
    parts = [a, b, c]
    for agent in (taker, cutter):
        vals = [piece_eval(oracle, agent, part) for part in parts]
        alloc[agent].extend(parts.pop(vals.index(max(vals))))
    alloc[other].extend(parts[0])


class _Run:
    def __init__(self, oracle: Oracle, max_rounds: int) -> None:
        self.oracle = oracle
        self.max_rounds = max_rounds
        self.rounds = 0
        self.alloc: dict[int, Piece] = {i: [] for i in range(oracle.n)}

    def dominator(self, agents: list[int], rest: Piece) -> int | None:
        for i in agents:
            if all(dominates(self.oracle, i, j, self.alloc, rest) for j in agents if j != i):
                return i
        return None

    def divide(self, agents: list[int], rest: Piece) -> None:
        if len(agents) == 1:
            self.alloc[agents[0]].extend(rest)  # @line L1
            return
        last: tuple[int, int] | None = None
        turn = 0
        while True:  # @line L2
            if len(agents) == 2:
                give = cut_and_choose(self.oracle, rest, agents[turn % 2], agents[(turn + 1) % 2])  # @line L3
                rest = []
            else:
                if self.rounds == self.max_rounds and last is not None:
                    finish_stage_two(self.oracle, self.alloc, rest, *last)
                    return
                cutter = agents[turn % 3]
                a, b = [x for x in agents if x != cutter]
                trimmer, chooser = (a, b) if (turn // 3) % 2 == 0 else (b, a)
                give, rest, taker = trimming_round(self.oracle, rest, cutter, trimmer, chooser)  # @line L3
                # the toy has no sub-protocols for domination; it only records
                # that the cutter now dominates the taker of the trimmed piece
                last = (cutter, taker)  # @line L5
            for agent, piece in give.items():
                self.alloc[agent].extend(piece)  # @line L4
            self.rounds += 1
            turn += 1
            i = self.dominator(agents, rest)  # @line L6
            if i is not None:
                break
        self.divide([x for x in agents if x != i], rest)  # @line L7


def aziz_mackenzie_toy(oracle: Oracle, max_rounds: int = 40) -> tuple[dict[int, Piece], int]:
    """Return an envy-free division of [0, 1] among three agents and the number of rounds."""
    if oracle.n != 3:
        raise ValueError("this toy is for three agents")
    if max_rounds < 1:
        raise ValueError("max_rounds must be at least 1")
    run = _Run(oracle, max_rounds)
    run.divide([0, 1, 2], [(Fraction(0), Fraction(1))])
    return run.alloc, run.rounds
