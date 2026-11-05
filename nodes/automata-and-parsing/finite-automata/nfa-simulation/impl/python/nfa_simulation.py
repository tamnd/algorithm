# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nfa-simulation/. The authors are listed in prov/B4QP59.jsonl.

from collections.abc import Iterable, Mapping

EPS = ""  # the label of an epsilon-move

State = int
Delta = Mapping[tuple[State, str], Iterable[State]]


def close(states: Iterable[State], delta: Delta) -> set[State]:
    """Return the epsilon-closure of a set of states.

    The closure holds each state that a path of epsilon-moves reaches from the set.
    It uses an explicit stack, so long chains of epsilon-moves need no recursion.
    Cost: O(n + m_eps), with m_eps the number of epsilon-moves.
    """
    c = set(states)  # @line L9
    k = list(c)
    while k:  # @line L10
        q = k.pop()  # @line L11
        for r in delta.get((q, EPS), ()):  # @line L12
            if r not in c:
                c.add(r)
                k.append(r)
    return c  # @line L13


def nfa_simulation(
    delta: Delta,
    start: State,
    accepting: Iterable[State],
    word: Iterable[str],
    trace: list[frozenset[State]] | None = None,
) -> bool:
    """Decide whether an NFA accepts a word, by tracking the set of active states.

    The NFA has the transitions delta[(q, a)] -> states, where a == "" marks an
    epsilon-move, the start state `start` and the accepting states `accepting`.
    It need not be complete. If `trace` is a list, the active set after the start
    and after each symbol is appended to it.
    Cost: O(l * (n + m)) time and O(n) extra space for a word of length l.
    """
    acc = set(accepting)
    s = close([start], delta)  # @line L1
    if trace is not None:
        trace.append(frozenset(s))
    for a in word:  # @line L2
        t: set[State] = set()  # @line L3
        for q in s:  # @line L4
            t.update(delta.get((q, a), ()))  # @line L5
        s = close(t, delta)  # @line L6
        if trace is not None:
            trace.append(frozenset(s))
        if not s:  # @line L7
            return False
    return not s.isdisjoint(acc)  # @line L8
