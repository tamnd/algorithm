# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selfridge-conway-procedure/. The authors are listed in prov/9GXB9K.jsonl.

from fractions import Fraction

from agtcake import Oracle

Interval = tuple[Fraction, Fraction]
Piece = list[Interval]


def _best(oracle: Oracle, i: int, pieces: list[Interval]) -> int:
    """Return the index of the piece agent i values most (ties: the smallest index).

    One eval query per piece.
    """
    vals = [oracle.eval_query(i, a, b) for a, b in pieces]
    top = max(vals)
    return vals.index(top)


def selfridge_conway(oracle: Oracle) -> dict[int, Piece]:
    """The Selfridge-Conway procedure for three agents.

    Agents 0, 1 and 2 of the code are agents 1, 2 and 3 of the page: agent 0
    cuts, agent 1 trims and agent 2 chooses first. The result maps each agent
    to its piece, a list of at most two intervals.
    """
    if oracle.n != 3:
        raise ValueError("the Selfridge-Conway procedure is for three agents")
    third = Fraction(1, 3)
    c = oracle.cut_query(0, 0, third)  # @line L1
    d = oracle.cut_query(0, c, third)
    pieces: list[Interval] = [(Fraction(0), c), (c, d), (d, Fraction(1))]
    vals = [oracle.eval_query(1, a, b) for a, b in pieces]  # @line L2
    order = sorted(range(3), key=lambda j: (-vals[j], j))
    p, q = order[0], order[1]
    trimmings: Interval | None
    if vals[p] > vals[q]:  # @line L3
        a, b = pieces[p]
        x = oracle.cut_query(1, a, vals[q])  # @line L4
        pieces[p] = (a, x)
        trimmings = (x, b)
    else:
        trimmings = None  # @line L5
    alloc: dict[int, Piece] = {}
    left = [0, 1, 2]
    j3 = left[_best(oracle, 2, [pieces[j] for j in left])]  # @line L6
    alloc[2] = [pieces[j3]]
    left.remove(j3)
    if p in left:  # @line L7
        j2 = p
    elif vals[left[0]] >= vals[left[1]]:
        j2 = left[0]  # agent 1 knows these values from line L2
    else:
        j2 = left[1]
    alloc[1] = [pieces[j2]]
    left.remove(j2)
    alloc[0] = [pieces[left[0]]]  # @line L8
    if trimmings is None:  # @line L9
        return alloc
    t = 2 if j3 == p else 1  # @line L10
    u = 3 - t
    a, b = trimmings
    w = oracle.eval_query(u, a, b) / 3  # @line L11
    y = oracle.cut_query(u, a, w)
    z = oracle.cut_query(u, y, w)
    parts: list[Interval] = [(a, y), (y, z), (z, b)]
    for agent in (t, 0):  # @line L12
        k = _best(oracle, agent, parts)
        alloc[agent].append(parts.pop(k))
    alloc[u].append(parts[0])
    return alloc
