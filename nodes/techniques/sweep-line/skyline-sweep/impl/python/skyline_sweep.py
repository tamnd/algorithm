# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skyline-sweep/. The authors are listed in prov/B8EJVN.jsonl.

import heapq


def get_skyline(buildings: list[list[int]]) -> list[list[int]]:
    """Return the skyline of the buildings as key points [x, h].

    Each building is [left, right, height] with left < right and height > 0.
    The result is the shortest list of points [x, h], sorted by x, such that
    the height of the outline is h on [x, next x) and 0 after the last point.
    Two consecutive points never have the same height.
    Cost: O(n log n) time and O(n) extra space for n buildings.
    """
    xs = sorted({b[0] for b in buildings} | {b[1] for b in buildings})  # @line L1
    order = sorted(buildings, key=lambda b: b[0])  # @line L2
    heap: list[tuple[int, int]] = []  # @line L3: entries (-height, right)
    i = 0
    out: list[list[int]] = []
    prev = 0
    for x in xs:  # @line L4
        while i < len(order) and order[i][0] == x:  # @line L5
            heapq.heappush(heap, (-order[i][2], order[i][1]))  # @line L6
            i += 1
        while heap and heap[0][1] <= x:  # @line L7
            heapq.heappop(heap)  # @line L8
        h = -heap[0][0] if heap else 0  # @line L9
        if h != prev:  # @line L10
            out.append([x, h])  # @line L11
            prev = h
    return out  # @line L12
