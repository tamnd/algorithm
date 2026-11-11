# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coffman-conditions/. The authors are listed in prov/90K4PA.jsonl.

"""Resources with several units, as processes in procsim.

A resource type r has sim.v["avail"][r] free units, and sim.v["held"][p][r]
counts the units that process p holds. Acquiring one unit is one atomic
step that blocks while no unit is free. Precondition of each build: none.
Cost: each exhaustive search here visits fewer than 1000 states.
"""

from typing import Callable, Iterator

from procsim import Sim


def _fits(r: str) -> Callable[[Sim], bool]:
    return lambda s: s.v["avail"][r] > 0


def _take(me: str, r: str) -> Callable[[Sim], None]:
    def f(s: Sim) -> None:
        s.v["avail"][r] -= 1
        s.v["held"][me][r] = s.v["held"][me].get(r, 0) + 1
    return f


def _give(me: str, r: str) -> Callable[[Sim], None]:
    def f(s: Sim) -> None:
        s.v["avail"][r] += 1
        s.v["held"][me][r] -= 1
    return f


def user(sim: Sim, me: str, needs: list[str]) -> Iterator[tuple]:
    """Take one unit of each type in the list, in order, then release them all."""
    for r in needs:
        yield ("when", _fits(r), _take(me, r), r)  # the fourth item names the request
    for r in reversed(needs):
        yield ("atomic", _give(me, r))


def build(units: dict[str, int], programs: dict[str, list[str]]) -> Sim:
    s = Sim()
    s.v["avail"] = dict(units)
    s.v["held"] = {p: {} for p in programs}
    for p, needs in programs.items():
        s.spawn(p, user, needs)
    return s


def wait_for_graph(s: Sim) -> dict[str, set[str]]:
    """p -> q when p is blocked on a type of which q holds a unit."""
    g: dict[str, set[str]] = {p: set() for p in s.procs}
    for p in s.blocked():
        r = s.procs[p].op[3]
        g[p] = {q for q, h in s.v["held"].items() if q != p and h.get(r, 0) > 0}
    return g


def has_cycle(g: dict[str, set[str]]) -> bool:
    """Iterative depth-first search for a cycle. Cost: O(V + E)."""
    color = {v: 0 for v in g}
    for s0 in g:
        if color[s0]:
            continue
        color[s0] = 1
        stack = [(s0, iter(sorted(g[s0])))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                color[v] = 2
                stack.pop()
            elif color[w] == 1:
                return True
            elif color[w] == 0:
                color[w] = 1
                stack.append((w, iter(sorted(g[w]))))
    return False


TWO_UNITS = ({"R1": 2, "R2": 2},
             {"p1": ["R1", "R2"], "p2": ["R2", "R1"], "p3": ["R1"], "p4": ["R2"]})
ONE_UNIT = ({"R1": 1, "R2": 1}, {"p1": ["R1", "R2"], "p2": ["R2", "R1"]})
