# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jonker-volgenant-algorithm/. The authors are listed in prov/TN0EFM.jsonl.

from collections import deque


def jonker_volgenant_algorithm(
    cost: list[list[float]], reduction_passes: int = 2
) -> tuple[list[int], list[float], list[float]]:
    """Minimum-cost perfect assignment of an n x n cost matrix (LAPJV, dense form).

    The graph is the complete bipartite graph of rows and columns, with weights
    cost[i][j], which may be negative. Returns (x, u, v): x[i] is the column of
    row i, and u, v are dual values with u[i] + v[j] <= cost[i][j] for all i, j,
    and equality on the pairs (i, x[i]). The total cost is sum(u) + sum(v).
    reduction_passes is the number of passes of augmenting row reduction (2 in
    the paper); 0 skips it, and the augmentation phase then does all the work.
    Time O(n^3), extra space O(n). Exact for integer costs.
    """
    n = len(cost)
    if any(len(row) != n for row in cost):
        raise ValueError("the cost matrix must be square")
    if n == 0:
        return [], [], []
    if n == 1:
        return [0], [cost[0][0]], [0]
    c = cost
    x: list[int] = [-1] * n  # @line L1
    y: list[int] = [-1] * n
    v: list[float] = [0] * n
    times = [0] * n

    # Column reduction.
    for j in range(n - 1, -1, -1):  # @line L2
        i_min = min(range(n), key=lambda i: c[i][j])  # @line L3
        v[j] = c[i_min][j]
        times[i_min] += 1
        if x[i_min] < 0:  # @line L4
            x[i_min] = j
            y[j] = i_min

    # Reduction transfer.
    free: list[int] = []
    for i in range(n):  # @line L5
        if times[i] == 0:
            free.append(i)
        elif times[i] == 1:
            j1 = x[i]
            v[j1] -= min(c[i][j] - v[j] for j in range(n) if j != j1)  # @line L6

    # Augmenting row reduction, two passes, at most 2n bids per pass.
    for _ in range(reduction_passes):  # @line L7
        todo = deque(free)
        free = []
        bids = 0
        while todo:
            i = todo.popleft()  # @line L8
            if bids >= 2 * n:
                free.append(i)
                continue
            bids += 1
            j1, j2 = -1, -1
            a = b = None
            for j in range(n):
                h = c[i][j] - v[j]
                if a is None or h < a:
                    b, j2 = a, j1
                    a, j1 = h, j
                elif b is None or h < b:
                    b, j2 = h, j
            i0 = y[j1]
            if a < b:  # @line L9
                v[j1] -= b - a
            elif i0 >= 0:
                j1 = j2
                i0 = y[j1]
            x[i] = j1  # @line L10
            y[j1] = i
            if i0 >= 0:
                x[i0] = -1
                if a < b:
                    todo.appendleft(i0)
                else:
                    free.append(i0)

    # Augmentation by shortest paths.
    d: list[float] = [0] * n
    pred = [0] * n
    for f in free:  # @line L11
        for j in range(n):  # @line L12
            d[j] = c[f][j] - v[j]
            pred[j] = f
        cols = list(range(n))  # cols[:low] scanned, cols[low:up] at distance mu, cols[up:] the rest
        low = up = 0
        mu: float = 0
        end = -1
        while end < 0:  # @line L13
            if low == up:
                mu = min(d[cols[k]] for k in range(low, n))  # @line L14
                for k in range(low, n):
                    j = cols[k]
                    if d[j] == mu:
                        cols[k], cols[up] = cols[up], j
                        up += 1
                for k in range(low, up):  # @line L15
                    if y[cols[k]] < 0:
                        end = cols[k]
                        break
                if end >= 0:
                    break
            j1 = cols[low]  # @line L16
            low += 1
            i = y[j1]
            base = c[i][j1] - v[j1] - mu
            k = up
            while k < n:  # @line L17
                j = cols[k]
                h = c[i][j] - v[j] - base
                if h < d[j]:
                    d[j] = h
                    pred[j] = i
                    if h == mu:
                        if y[j] < 0:
                            end = j
                            break
                        cols[k], cols[up] = cols[up], j
                        up += 1
                k += 1
        for k in range(low):  # @line L18
            j = cols[k]
            v[j] += d[j] - mu
        while True:  # @line L19
            i = pred[end]
            y[end] = i
            end, x[i] = x[i], end
            if i == f:
                break
    u = [c[i][x[i]] - v[x[i]] for i in range(n)]
    return x, u, v  # @line L20
