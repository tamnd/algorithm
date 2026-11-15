# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/supremal-controllable-sublanguage/. The authors are listed in prov/1CMXJG.jsonl.

"""The supremal controllable sublanguage of a regular specification.

An automaton is a dict with the keys "init" (the initial state), "delta"
(a dict that maps (state, event) to the next state, so the automaton is
deterministic and partial) and "marked" (a set of states). The plant is G,
the specification is H, and K = Lm(H) & Lm(G) is the target language.

supremal_controllable(g, h, uncontrollable) returns a trim automaton A with
Lm(A) = sup C(K) and L(A) = prefix(sup C(K)), where sup C is taken with
respect to L(G) and the set of uncontrollable events. The states of A are
pairs (h, g) of the product H x G. If sup C(K) is empty, A has no states and
its "init" is None.

Cost, with N = |Q_H| |Q_G| product states and an alphabet of size E: the
product takes O(N E) dict operations, one round of the loop takes O(N E),
and there are at most N + 1 rounds, so O(N^2 E) in total.
"""

from collections import deque
from typing import Hashable, Iterable

Automaton = dict


def out_edges(delta: dict) -> dict:
    """Map each state to a dict {event: next state}."""
    out: dict = {}
    for (q, e), r in delta.items():
        out.setdefault(q, {})[e] = r
    return out


def product(h: Automaton, g: Automaton) -> Automaton:
    """The accessible part of H x G, synchronized on every event."""
    eh, eg = out_edges(h["delta"]), out_edges(g["delta"])
    init = (h["init"], g["init"])
    states = {init}
    delta = {}
    queue = deque([init])
    while queue:
        x = queue.popleft()
        for e, g2 in eg.get(x[1], {}).items():
            h2 = eh.get(x[0], {}).get(e)
            if h2 is None:
                continue
            y = (h2, g2)
            delta[(x, e)] = y
            if y not in states:
                states.add(y)
                queue.append(y)
    marked = {x for x in states if x[0] in h["marked"] and x[1] in g["marked"]}
    return {"init": init, "states": states, "delta": delta, "marked": marked}


def trim(states: set, out: dict, init: Hashable, marked: set) -> set:
    """The states of `states` that are accessible from init and coaccessible to a marked state, inside `states`."""
    if init not in states:
        return set()
    acc = {init}
    stack = [init]
    while stack:
        x = stack.pop()
        for y in out.get(x, {}).values():
            if y in states and y not in acc:
                acc.add(y)
                stack.append(y)
    back: dict = {}
    for x in acc:
        for y in out.get(x, {}).values():
            if y in acc:
                back.setdefault(y, []).append(x)
    co = {x for x in acc if x in marked}
    stack = list(co)
    while stack:
        y = stack.pop()
        for x in back.get(y, []):
            if x not in co:
                co.add(x)
                stack.append(x)
    return co


def restrict(a: Automaton, states: set) -> Automaton:
    """The sub-automaton of a on the given states."""
    delta = {(x, e): y for (x, e), y in a["delta"].items() if x in states and y in states}
    init = a["init"] if a["init"] in states else None
    return {"init": init, "states": set(states), "delta": delta, "marked": a["marked"] & states}


def supremal_controllable(g: Automaton, h: Automaton, uncontrollable: Iterable) -> Automaton:
    """A trim automaton for sup C(Lm(H) & Lm(G)) with respect to L(G) and the uncontrollable events."""
    unc = set(uncontrollable)
    a = product(h, g)  # @line L1
    out = out_edges(a["delta"])
    plant = out_edges(g["delta"])
    states = set(a["states"])
    while True:  # @line L2
        changed = False  # @line L3
        for x in list(states):  # @line L4
            for e in plant.get(x[1], {}):
                if e in unc and out.get(x, {}).get(e) not in states:  # @line L5
                    states.discard(x)
                    changed = True
                    break
        kept = trim(states, out, a["init"], a["marked"])  # @line L6
        if kept != states:
            states = kept
            changed = True
        if not changed:  # @line L7
            break
    return restrict(a, states)  # @line L8


def disabled_events(sup: Automaton, g: Automaton) -> dict:
    """For each state (h, g) of sup, the events that G allows at g and the supervisor disables."""
    plant = out_edges(g["delta"])
    out = out_edges(sup["delta"])
    return {x: {e for e in plant.get(x[1], {}) if e not in out.get(x, {})} for x in sup["states"]}
