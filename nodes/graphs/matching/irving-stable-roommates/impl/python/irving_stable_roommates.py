# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/irving-stable-roommates/. The authors are listed in prov/Q2A2ZX.jsonl.


def irving_stable_roommates(prefs: list[list[int]]) -> list[int | None] | None:
    """A stable matching of a stable roommates instance, or None if none exists.

    The graph is general (not bipartite) and has no weights. The agents are
    0 .. n-1, and prefs[x] lists the agents that x finds acceptable, best first.
    Lists may be incomplete; a pair is usable only if each agent lists the other.
    Returns mate, where mate[x] is the partner of x or None if x is single, or
    None if the instance has no stable matching.
    Time O(n + n m), where m is the number of acceptable pairs; space O(n + m).
    """
    n = len(prefs)
    for x, lst in enumerate(prefs):
        if len(set(lst)) != len(lst) or any(not 0 <= y < n or y == x for y in lst):
            raise ValueError("each list must hold distinct agents other than its owner")
    listed = [set(lst) for lst in prefs]
    # lst[x] is the list of x, kept as a fixed array; alive marks the entries still in it.
    lst = [[y for y in prefs[x] if x in listed[y]] for x in range(n)]  # @line L1
    rank = [{y: i for i, y in enumerate(lst[x])} for x in range(n)]
    alive = [[True] * len(lst[x]) for x in range(n)]
    head = [0] * n
    tail = [len(lst[x]) - 1 for x in range(n)]
    size = [len(lst[x]) for x in range(n)]
    sec = [1] * n  # a pointer that only moves right, used by second()
    holder: list[int | None] = [None] * n  # @line L2
    free = list(range(n))
    in_phase_1 = True

    def delete(a: int, b: int) -> None:
        """Delete the pair {a, b} from both lists."""
        ia, ib = rank[a][b], rank[b][a]
        if not alive[a][ia]:
            return
        alive[a][ia] = alive[b][ib] = False
        for c in (a, b):
            size[c] -= 1
            while head[c] < len(lst[c]) and not alive[c][head[c]]:
                head[c] += 1
            while tail[c] >= 0 and not alive[c][tail[c]]:
                tail[c] -= 1
        if in_phase_1:
            if holder[a] == b:
                holder[a] = None
                free.append(b)
            if holder[b] == a:
                holder[b] = None
                free.append(a)

    def truncate(y: int, x: int) -> None:
        """Delete every entry after x on the list of y, by position, so x may be gone."""
        i = rank[y][x]
        while tail[y] > i:
            delete(y, lst[y][tail[y]])

    def first(x: int) -> int:
        return lst[x][head[x]]

    def last(x: int) -> int:
        return lst[x][tail[x]]

    def second(x: int) -> int:
        if sec[x] <= head[x]:
            sec[x] = head[x] + 1
        while not alive[x][sec[x]]:
            sec[x] += 1
        return lst[x][sec[x]]

    # Phase 1: proposals.
    while free:  # @line L3
        x = free.pop()  # @line L4
        if size[x] == 0:
            continue
        y = first(x)  # @line L5
        truncate(y, x)  # @line L6
        holder[y] = x  # @line L7
    in_phase_1 = False
    in_a = [size[x] > 0 for x in range(n)]  # @line L8
    empty_after_phase_1 = n - sum(in_a)
    stack: list[int] = []
    pos: dict[int, int] = {}
    start = 0

    # Phase 2: find and eliminate rotations.
    while True:  # @line L9
        cut = len(stack)  # @line L10
        for i, s in enumerate(stack):
            if size[s] < 2 or (i + 1 < len(stack) and last(second(s)) != stack[i + 1]):
                cut = i
                break
        for s in stack[cut:]:
            del pos[s]
        del stack[cut:]
        if not stack:  # @line L11
            while start < n and size[start] < 2:
                start += 1
            if start == n:
                break
            stack.append(start)
            pos[start] = 0
        while True:  # @line L12
            p = last(second(stack[-1]))
            if p in pos:
                break
            pos[p] = len(stack)
            stack.append(p)
        rho = stack[pos[p]:]  # @line L13
        for s in rho:
            del pos[s]
        del stack[len(stack) - len(rho):]
        pairs = [(x, second(x)) for x in rho]  # @line L14
        for x, y in pairs:
            truncate(y, x)
        if sum(1 for x in range(n) if size[x] == 0) > empty_after_phase_1:  # @line L15
            return None
    return [first(x) if in_a[x] else None for x in range(n)]  # @line L16
