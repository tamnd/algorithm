# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-predicate-detection/. The authors are listed in prov/E1GYTY.jsonl.

"""possibly(phi) and definitely(phi) for a recorded computation, by a level by
level search of the lattice of consistent cuts (Cooper and Marzullo 1991),
and a check by enumeration of every run.

A computation is a list of event lists; an event is ("int",), ("send", m, dst)
or ("recv", m, src). A cut k holds the first k_i events of process i. phi is a
function of the cut.
"""

import itertools
from typing import Callable, Iterator

Cut = tuple[int, ...]
Phi = Callable[[Cut], bool]


def send_positions(comp: list[list[tuple]]) -> dict[int, tuple[int, int]]:
    """Message id -> (sender, 1-based index of the send event)."""
    out = {}
    for i, evs in enumerate(comp):
        for a, e in enumerate(evs, 1):
            if e[0] == "send":
                out[e[1]] = (i, a)
    return out


def successors(comp: list[list[tuple]], sends: dict, cut: Cut) -> Iterator[Cut]:
    """The consistent cuts that hold one more event than `cut`."""
    for i, k in enumerate(cut):
        if k == len(comp[i]):
            continue
        e = comp[i][k]
        if e[0] == "recv":
            src, a = sends[e[1]]
            if cut[src] < a:
                continue  # the send is not in the cut yet
        yield cut[:i] + (k + 1,) + cut[i + 1 :]


def possibly(comp: list[list[tuple]], phi: Phi) -> bool:
    sends = send_positions(comp)
    level = {tuple(0 for _ in comp)}  # @line L1
    while level:
        if any(phi(c) for c in level):  # @line L2
            return True
        level = {s for c in level for s in successors(comp, sends, c)}  # @line L3
    return False


def definitely(comp: list[list[tuple]], phi: Phi) -> bool:
    sends = send_positions(comp)
    final = tuple(len(p) for p in comp)
    init = tuple(0 for _ in comp)
    if phi(init):
        return True
    # level holds the cuts that a path reaches without meeting phi.
    level = {init}  # @line L4
    while level:
        if final in level:  # @line L5
            return False
        level = {s for c in level for s in successors(comp, sends, c) if not phi(s)}  # @line L6
    return True  # @line L7


def runs(comp: list[list[tuple]]) -> Iterator[list[Cut]]:
    """Every sequence of cuts from the initial cut to the final cut (exponential)."""
    sends = send_positions(comp)
    final = tuple(len(p) for p in comp)

    def go(path: list[Cut]) -> Iterator[list[Cut]]:
        if path[-1] == final:
            yield list(path)
            return
        for s in successors(comp, sends, path[-1]):
            path.append(s)
            yield from go(path)
            path.pop()

    yield from go([tuple(0 for _ in comp)])


def possibly_brute(comp: list[list[tuple]], phi: Phi) -> bool:
    return any(phi(c) for r in runs(comp) for c in r)


def definitely_brute(comp: list[list[tuple]], phi: Phi) -> bool:
    return all(any(phi(c) for c in r) for r in runs(comp))


# --- the reduction from SAT ----------------------------------------------------

Clause = list[int]  # literal v > 0 is x_v, v < 0 is not x_v; variables 1..k


def sat_instance(cnf: list[Clause], k: int) -> tuple[list[list[tuple]], Phi]:
    """k processes, no messages, one event each. x_v is true when process v - 1
    has done its event. Every cut is consistent, so possibly(phi) holds iff
    the formula is satisfiable."""
    comp = [[("int",)] for _ in range(k)]

    def phi(cut: Cut) -> bool:
        val = lambda lit: (cut[abs(lit) - 1] == 1) == (lit > 0)
        return all(any(val(lit) for lit in cl) for cl in cnf)

    return comp, phi


def satisfiable(cnf: list[Clause], k: int) -> bool:
    return any(all(any((bits[abs(l) - 1] == 1) == (l > 0) for l in cl) for cl in cnf) for bits in itertools.product((0, 1), repeat=k))


def unsat_instance(cnf: list[Clause], k: int) -> tuple[list[list[tuple]], Phi]:
    """2k + 1 processes, no messages, one event each. Process 2(v - 1) is T_v,
    process 2(v - 1) + 1 is F_v, and the last process is the pivot P. A run
    avoids phi iff, when P runs, exactly one of T_v and F_v has run for each v
    and the assignment x_v = (T_v has run) satisfies the formula. So
    definitely(phi) holds iff the formula is unsatisfiable."""
    comp = [[("int",)] for _ in range(2 * k + 1)]
    pivot = 2 * k

    def phi(cut: Cut) -> bool:
        pairs = [(cut[2 * v], cut[2 * v + 1]) for v in range(k)]
        if cut[pivot] == 0:
            return any(t == 1 and f == 1 for t, f in pairs)  # a pair is done too early
        if any(t == 0 and f == 0 for t, f in pairs):
            return True  # a pair has no value when P runs
        if all(t + f == 1 for t, f in pairs):
            val = lambda lit: (pairs[abs(lit) - 1][0] == 1) == (lit > 0)
            return not all(any(val(lit) for lit in cl) for cl in cnf)
        return False

    return comp, phi
