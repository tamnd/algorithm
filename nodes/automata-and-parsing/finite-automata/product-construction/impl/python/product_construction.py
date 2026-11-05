# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/product-construction/. The authors are listed in prov/2Q2G89.jsonl.

from collections import deque
from collections.abc import Callable, Hashable, Iterable, Mapping

State = Hashable
Dfa = Mapping[tuple[State, str], State]


def product_construction(
    alphabet: Iterable[str],
    delta1: Dfa,
    start1: State,
    final1: Iterable[State],
    delta2: Dfa,
    start2: State,
    final2: Iterable[State],
    op: Callable[[bool, bool], bool],
) -> tuple[list[tuple[State, State]], list[dict[str, int]], set[int]]:
    """Build the reachable product of two complete DFAs over one alphabet.

    Each DFA is given by its moves delta[(q, a)] -> state, its start state and its
    accepting states; it must have a move for every reachable state and symbol.
    A pair (p, q) is accepting when op(p in final1, q in final2) is true, so
    op = and gives the intersection, or the union, (x and not y) the difference.
    The result is (pairs, table, final): product state i is the pair pairs[i], its
    move on a is table[i][a], the start is state 0, `final` holds the accepting ones.
    Cost: O(N * sigma) time and space for N <= n1 * n2 reachable pairs.
    """
    sigma = list(dict.fromkeys(alphabet))
    f1, f2 = set(final1), set(final2)
    s = (start1, start2)  # @line L1
    index: dict[tuple[State, State], int] = {s: 0}  # @line L2
    pairs: list[tuple[State, State]] = [s]
    table: list[dict[str, int]] = [{}]
    work = deque([s])
    while work:  # @line L3
        p, q = work.popleft()  # @line L4
        i = index[(p, q)]
        for a in sigma:  # @line L5
            t = (delta1[(p, a)], delta2[(q, a)])  # @line L6
            if t not in index:  # @line L7
                index[t] = len(pairs)
                pairs.append(t)
                table.append({})
                work.append(t)
            table[i][a] = index[t]  # @line L8
    final = {i for i, (p, q) in enumerate(pairs) if op(p in f1, q in f2)}  # @line L9
    return pairs, table, final  # @line L10
