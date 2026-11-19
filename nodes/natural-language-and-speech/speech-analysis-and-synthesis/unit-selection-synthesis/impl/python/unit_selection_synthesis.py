# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unit-selection-synthesis/. The authors are listed in prov/V4WYB0.jsonl.

"""Unit selection by dynamic programming over target and join costs, after
Hunt and Black (1996).

A target is the specification of one unit of the utterance to synthesize:
its phone, a target F0 (Hz), a target duration (ms) and the phones to its left
and right. A database unit is a stretch of recorded speech with the same
fields, plus the utterance it comes from, its position in that utterance,
and the spectral vectors at its start and its end.

    target cost  TC(t, u) = w_f0 |t.f0 - u.f0| + w_dur |t.dur - u.dur|
                            + w_ctx ([t.left != u.left] + [t.right != u.right])
    join cost    JC(u, v) = 0 if v follows u directly in the same recording,
                            else w_spec ||u.end - v.start||^2 + w_jf0 |u.f0 - v.f0|

Only units with the phone of the target are candidates. The best sequence
minimizes the sum of the target costs and the join costs, which is a
shortest path in a layered graph, found by Viterbi in the tropical semiring
(min, +). A beam keeps only the best candidates of each layer, which is
faster but can miss the optimum.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

INF = float("inf")


@dataclass(frozen=True)
class Target:
    phone: str
    f0: float
    dur: float
    left: str = ""
    right: str = ""


@dataclass(frozen=True)
class Unit:
    utt: int
    idx: int
    phone: str
    f0: float
    dur: float
    left: str = ""
    right: str = ""
    start: Tuple[float, ...] = field(default=())
    end: Tuple[float, ...] = field(default=())


DEFAULT_WEIGHTS = {"f0": 1.0, "dur": 1.0, "ctx": 1.0, "spec": 1.0, "jf0": 1.0}


def target_cost(t: Target, u: Unit, w: Dict[str, float] = DEFAULT_WEIGHTS) -> float:
    if t.phone != u.phone:
        return INF
    ctx = (t.left != u.left) + (t.right != u.right)
    return w["f0"] * abs(t.f0 - u.f0) + w["dur"] * abs(t.dur - u.dur) + w["ctx"] * ctx


def join_cost(u: Unit, v: Unit, w: Dict[str, float] = DEFAULT_WEIGHTS) -> float:
    if u.utt == v.utt and v.idx == u.idx + 1:
        return 0.0
    spec = sum((a - b) * (a - b) for a, b in zip(u.end, v.start))
    return w["spec"] * spec + w["jf0"] * abs(u.f0 - v.f0)


def candidates(targets: Sequence[Target], units: Sequence[Unit]) -> List[List[Unit]]:
    """The candidate lists U_1 .. U_n, each in database order."""
    return [[u for u in units if u.phone == t.phone] for t in targets]  # @line L1


def total_cost(targets, seq, w=DEFAULT_WEIGHTS) -> float:
    """The cost of a given unit sequence: all target costs plus all join costs."""
    c = sum(target_cost(t, u, w) for t, u in zip(targets, seq))
    c += sum(join_cost(a, b, w) for a, b in zip(seq, seq[1:]))
    return c


def select_units(targets: Sequence[Target], units: Sequence[Unit], w: Dict[str, float] = DEFAULT_WEIGHTS,
                 beam: Optional[int] = None):
    """Return (units, cost) of a sequence of least total cost, or raise ValueError
    if some target has no candidate.

    Tie rule: in lines L5 and L8 the first minimizer in database order wins.
    With beam = K, only the K cheapest units of each layer (ties to the earlier
    unit) are extended; the result is then not always optimal.
    """
    n = len(targets)
    if n == 0:
        return [], 0.0
    U = candidates(targets, units)
    if any(not layer for layer in U):
        raise ValueError("a target has no candidate unit")
    if beam is not None and beam < 1:
        raise ValueError("the beam must be at least 1")
    C = [[target_cost(targets[0], u, w) for u in U[0]]]  # @line L2
    B: List[List[int]] = [[-1] * len(U[0])]
    alive = _prune(C[0], beam)
    for i in range(1, n):  # @line L3
        row, back = [], []
        for u in U[i]:  # @line L4
            best_j, best = -1, INF
            for j in alive:  # @line L5
                c = C[i - 1][j] + join_cost(U[i - 1][j], u, w)
                if c < best or best_j == -1:
                    best_j, best = j, c
            row.append(best + target_cost(targets[i], u, w))  # @line L6
            back.append(best_j)
        C.append(row)
        B.append(back)
        alive = _prune(row, beam)  # @line L7
    k = min(alive, key=lambda j: (C[n - 1][j], j))  # @line L8
    cost = C[n - 1][k]
    path = [k]
    for i in range(n - 1, 0, -1):  # @line L9
        k = B[i][k]
        path.append(k)
    path.reverse()
    return [U[i][path[i]] for i in range(n)], cost  # @line L10


def _prune(row: List[float], beam: Optional[int]) -> List[int]:
    """The indices kept for the next layer, in increasing order."""
    order = list(range(len(row)))
    if beam is None or beam >= len(row):
        return order
    return sorted(sorted(order, key=lambda j: (row[j], j))[:beam])
