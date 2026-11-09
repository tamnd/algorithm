# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimal-correction-subset/. The authors are listed in prov/W95AD0.jsonl.

"""Minimal correction subsets with a SAT oracle, and their duality with MUSes.

Clauses are lists of DIMACS ints. hard clauses always stay; soft clauses may
be removed. A correction set is a set of soft clauses whose removal leaves a
satisfiable formula. The functions return indices into soft, sorted.
"""


class Oracle:
    """A small DPLL solver that counts how often it is called."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, clauses: list[list[int]]) -> dict[int, bool] | None:
        self.calls += 1
        return _dpll([list(c) for c in clauses], {})


def _dpll(clauses: list[list[int]], assign: dict[int, bool]) -> dict[int, bool] | None:
    while True:
        unit = None
        rest: list[list[int]] = []
        for c in clauses:
            if any(assign.get(abs(a)) == (a > 0) for a in c):
                continue
            free = [a for a in c if abs(a) not in assign]
            if not free:
                return None
            if len(free) == 1:
                unit = free[0]
            rest.append(free)
        if unit is None:
            break
        assign = {**assign, abs(unit): unit > 0}
        clauses = rest
    if not rest:
        return assign
    v = abs(rest[0][0])
    for value in (rest[0][0] > 0, rest[0][0] < 0):
        model = _dpll(rest, {**assign, v: value})
        if model is not None:
            return model
    return None


def _satisfied(model: dict[int, bool], clause: list[int]) -> bool:
    # A variable the model does not mention is free; read it as false.
    return any(model.get(abs(a), False) == (a > 0) for a in clause)


def linear_mcs(soft: list[list[int]], hard: list[list[int]] = (),
               oracle: Oracle | None = None) -> list[int] | None:
    """Grow a satisfiable set K; the rest is an MCS. At most |U| + 1 calls."""
    sat = oracle or Oracle()
    hard = list(hard)
    model = sat(hard)  # @line L1
    if model is None:
        return None
    keep = {i for i, c in enumerate(soft) if _satisfied(model, c)}  # @line L2
    rest = [i for i in range(len(soft)) if i not in keep]
    for i in rest:  # @line L3
        if i in keep:
            continue
        model = sat(hard + [soft[j] for j in sorted(keep)] + [soft[i]])  # @line L4
        if model is not None:
            keep |= {j for j, c in enumerate(soft) if _satisfied(model, c)}  # @line L5
    return [i for i in range(len(soft)) if i not in keep]  # @line L6


def cld_mcs(soft: list[list[int]], hard: list[list[int]] = (),
            oracle: Oracle | None = None) -> list[int] | None:
    """Clause D: ask for a model that satisfies one more clause of U at a time."""
    sat = oracle or Oracle()
    hard = list(hard)
    model = sat(hard)
    if model is None:
        return None
    keep = {i for i, c in enumerate(soft) if _satisfied(model, c)}
    while True:
        rest = [i for i in range(len(soft)) if i not in keep]
        d = sorted({a for i in rest for a in soft[i]})  # the disjunction of U is one clause
        model = sat(hard + [soft[j] for j in sorted(keep)] + [d])
        if model is None:
            return rest
        keep |= {j for j, c in enumerate(soft) if _satisfied(model, c)}


def all_mcses(soft: list[list[int]], hard: list[list[int]] = (),
              oracle: Oracle | None = None) -> list[list[int]]:
    """Every MCS: block each one found by the clause that joins its clauses."""
    sat = oracle or Oracle()
    blocks: list[list[int]] = []
    out: list[list[int]] = []
    while True:
        mcs = cld_mcs(soft, list(hard) + blocks, sat)
        if mcs is None:
            return out
        out.append(mcs)
        blocks.append(sorted({a for i in mcs for a in soft[i]}))


def minimal_hitting_sets(sets: list[list[int]]) -> list[list[int]]:
    """Berge's algorithm: the minimal sets that meet every given set."""
    hs: list[frozenset[int]] = [frozenset()]
    for e in sets:
        grown = {t for t in hs if t & set(e)}
        grown |= {t | {x} for t in hs if not t & set(e) for x in e}
        hs = [t for t in grown if not any(u < t for u in grown)]
    return sorted(sorted(t) for t in hs)


def all_muses(soft: list[list[int]], hard: list[list[int]] = (),
              oracle: Oracle | None = None) -> list[list[int]]:
    """CAMUS-style: the MUSes are the minimal hitting sets of the MCSes."""
    return minimal_hitting_sets(all_mcses(soft, hard, oracle))
