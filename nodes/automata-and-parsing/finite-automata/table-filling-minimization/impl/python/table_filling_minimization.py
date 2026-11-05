# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/table-filling-minimization/. The authors are listed in prov/ZY1X60.jsonl.

from collections import deque
from collections.abc import Hashable, Iterable, Mapping

State = Hashable
Dfa = Mapping[tuple[State, str], State]


def table_filling_minimization(
    alphabet: Iterable[str],
    delta: Dfa,
    start: State,
    accepting: Iterable[State],
) -> tuple[list[list[State]], list[dict[str, int]], set[int]]:
    """Minimize a complete DFA by marking the pairs of distinguishable states.

    The DFA has the moves delta[(q, a)] -> state, the start state `start` and the
    accepting states `accepting`; it must have a move for each reachable state and
    symbol. Unreachable states are dropped. The result is (blocks, table, final):
    state i of the minimal DFA is the class blocks[i] of equivalent input states,
    its move on a is table[i][a], the start is state 0, and `final` holds the
    accepting states. The classes are listed in breadth-first order from the start.
    Cost: O(sigma * n^2) time and space for n reachable states.
    """
    sigma = list(dict.fromkeys(alphabet))
    acc = set(accepting)
    # L1: the reachable states, numbered 0..r-1 in breadth-first order
    num: dict[State, int] = {start: 0}  # @line L1
    states: list[State] = [start]
    work = deque([start])
    while work:
        q = work.popleft()
        for a in sigma:
            t = delta[(q, a)]
            if t not in num:
                num[t] = len(states)
                states.append(t)
                work.append(t)
    r = len(states)
    nxt = [[num[delta[(q, a)]] for a in sigma] for q in states]
    fin = [q in acc for q in states]

    def key(i: int, j: int) -> int:
        return i * r + j if i < j else j * r + i

    marked = bytearray(r * r)  # @line L2
    waiting: list[list[int]] = [[] for _ in range(r * r)]
    stack: list[int] = []  # @line L3
    for i in range(r):  # @line L4
        for j in range(i + 1, r):
            if fin[i] != fin[j]:
                marked[key(i, j)] = 1
                stack.append(key(i, j))
    for i in range(r):  # @line L5
        for j in range(i + 1, r):
            for c in range(len(sigma)):
                x, y = nxt[i][c], nxt[j][c]
                if x != y:
                    waiting[key(x, y)].append(key(i, j))
    while stack:  # @line L6
        rs = stack.pop()  # @line L7
        for pq in waiting[rs]:  # @line L8
            if not marked[pq]:
                marked[pq] = 1  # @line L9
                stack.append(pq)
    rep = list(range(r))  # @line L10
    for i in range(r):
        for j in range(i):
            if not marked[key(i, j)]:
                rep[i] = rep[j]
                break
    ids: dict[int, int] = {}  # @line L11
    blocks: list[list[State]] = []
    for i in range(r):
        if rep[i] not in ids:
            ids[rep[i]] = len(blocks)
            blocks.append([])
        blocks[ids[rep[i]]].append(states[i])
    table = [dict.fromkeys(sigma, 0) for _ in blocks]
    for i in range(r):
        for c, a in enumerate(sigma):
            table[ids[rep[i]]][a] = ids[rep[nxt[i][c]]]
    final = {ids[rep[i]] for i in range(r) if fin[i]}
    return blocks, table, final  # @line L12
