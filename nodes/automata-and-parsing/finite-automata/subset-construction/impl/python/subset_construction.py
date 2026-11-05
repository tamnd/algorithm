# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subset-construction/. The authors are listed in prov/19CF15.jsonl.

from collections import deque
from collections.abc import Iterable, Mapping

EPS = ""  # the label of an epsilon-move

State = int
Delta = Mapping[tuple[State, str], Iterable[State]]


def close(states: Iterable[State], delta: Delta) -> frozenset[State]:
    """Return the epsilon-closure of a set of states.

    The closure holds each state that a path of epsilon-moves reaches from the set.
    It uses an explicit stack, so deep chains of epsilon-moves need no recursion.
    Cost: O(n + m_eps), with m_eps the number of epsilon-moves.
    """
    c = set(states)  # @line L11
    k = list(c)
    while k:  # @line L12
        q = k.pop()  # @line L13
        for r in delta.get((q, EPS), ()):  # @line L14
            if r not in c:
                c.add(r)
                k.append(r)
    return frozenset(c)  # @line L15


def subset_construction(
    alphabet: Iterable[str],
    delta: Delta,
    start: State,
    accepting: Iterable[State],
) -> tuple[list[frozenset[State]], list[dict[str, int]], set[int]]:
    """Build a complete DFA with the same language as an NFA.

    The NFA has the transitions delta[(q, a)] -> states, where a == "" marks an
    epsilon-move, the start state `start` and the accepting states `accepting`.
    The DFA states are the reachable sets of NFA states. The result is
    (subsets, table, final): DFA state i is the set subsets[i], its move on a is
    table[i][a], the start is state 0, and `final` holds the accepting states.
    The empty set, when it is reachable, is the dead state, so the DFA is complete.
    Cost: O(N * sigma * (n + m)) time for N DFA states, so O(2^n * sigma * (n + m)).
    """
    sigma = list(dict.fromkeys(alphabet))
    acc = set(accepting)
    s0 = close([start], delta)  # @line L1
    index: dict[frozenset[State], int] = {s0: 0}  # @line L2
    subsets: list[frozenset[State]] = [s0]
    table: list[dict[str, int]] = [{}]
    work = deque([s0])
    while work:  # @line L3
        s = work.popleft()  # @line L4
        i = index[s]
        for a in sigma:  # @line L5
            step = {r for q in s for r in delta.get((q, a), ())}
            t = close(step, delta)  # @line L6
            if t not in index:  # @line L7
                index[t] = len(subsets)
                subsets.append(t)
                table.append({})
                work.append(t)
            table[i][a] = index[t]  # @line L8
    final = {i for i, s in enumerate(subsets) if s & acc}  # @line L9
    return subsets, table, final  # @line L10
