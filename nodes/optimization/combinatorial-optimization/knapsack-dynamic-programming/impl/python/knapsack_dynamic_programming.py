# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knapsack-dynamic-programming/. The authors are listed in prov/2ST7VJ.jsonl.


def knapsack_dynamic_programming(
    weights: list[int], values: list[int], capacity: int
) -> tuple[int, list[int]]:
    """Solve the 0-1 knapsack problem exactly by dynamic programming.

    Precondition: weights and values have the same length, every weight and
    the capacity are non-negative integers, and every value is a
    non-negative integer.

    Returns (best, chosen): the largest total value of a set of items whose
    total weight is at most capacity, and the 0-based indices of one such
    set, in increasing order.

    Cost: Theta(n W) time and Theta(n W) memory for the table, where n is
    the number of items and W the capacity.
    """
    n = len(weights)
    if len(values) != n:
        raise ValueError("weights and values must have the same length")
    if capacity < 0 or any(w < 0 for w in weights):
        raise ValueError("weights and capacity must be non-negative")
    cap = capacity
    # table[i][c]: best value with items 1..i (1-based) and capacity c.
    table = [[0] * (cap + 1)]  # @line L1
    for i in range(1, n + 1):  # @line L2
        w, v = weights[i - 1], values[i - 1]
        prev = table[i - 1]
        row = [0] * (cap + 1)
        for c in range(cap + 1):  # @line L3
            row[c] = prev[c]  # @line L4
            if w <= c and prev[c - w] + v > row[c]:  # @line L5
                row[c] = prev[c - w] + v  # @line L6
        table.append(row)
    chosen: list[int] = []
    c = cap  # @line L7
    for i in range(n, 0, -1):  # @line L8
        if table[i][c] != table[i - 1][c]:  # @line L9
            chosen.append(i - 1)  # @line L10
            c -= weights[i - 1]
    chosen.reverse()
    return table[n][cap], chosen  # @line L11


def knapsack_value(weights: list[int], values: list[int], capacity: int) -> int:
    """Return only the optimal value, with one row of Theta(W) memory.

    The inner loop runs over the capacities from high to low, so that each
    item is used at most once. Same precondition as above; Theta(n W) time.
    """
    row = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            if row[c - w] + v > row[c]:
                row[c] = row[c - w] + v
    return row[capacity]
