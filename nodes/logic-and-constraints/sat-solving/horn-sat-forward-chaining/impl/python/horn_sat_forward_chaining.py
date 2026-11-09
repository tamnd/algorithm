# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horn-sat-forward-chaining/. The authors are listed in prov/JGNV5C.jsonl.

"""Linear-time forward chaining for Horn-SAT (Dowling and Gallier, 1984).

A clause is a list of nonzero ints in DIMACS style. A Horn clause has at most
one positive literal. The variables are 1 .. n.
"""

from collections import deque


def horn_sat_forward_chaining(n: int, clauses: list[list[int]]) -> list[bool] | None:
    """Decide a Horn formula over the variables 1 .. n.

    Precondition: each clause has at most one positive literal (repeated
    copies of one positive literal count as one). Returns the least model as
    a list x of n booleans, where x[v - 1] is the value of the variable v, or
    None when the formula is unsatisfiable. Time Theta(n + |F|), where |F| is
    the number of literal occurrences.
    """
    head: list[int] = []
    for c in clauses:
        pos = {lit for lit in c if lit > 0}
        if len(pos) > 1:
            raise ValueError("not a Horn clause: " + repr(c))
        head.append(pos.pop() if pos else 0)  # 0 means: no positive literal
    val = [False] * (n + 1)  # @line L1
    count = [0] * len(clauses)  # @line L2
    occ: list[list[int]] = [[] for _ in range(n + 1)]
    for j, c in enumerate(clauses):
        for lit in c:
            if lit < 0:
                count[j] += 1
                occ[-lit].append(j)  # one entry for each occurrence
    queue = deque(j for j in range(len(clauses)) if count[j] == 0)  # @line L3
    while queue:  # @line L4
        j = queue.popleft()  # @line L5
        if head[j] == 0:  # @line L6
            return None
        h = head[j]  # @line L7
        if not val[h]:  # @line L8
            val[h] = True  # @line L9
            for d in occ[h]:  # @line L10
                count[d] -= 1  # @line L11
                if count[d] == 0:  # @line L12
                    queue.append(d)
    return val[1:]  # @line L13
