# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anatomy-bucketization/. The authors are listed in prov/Y4WDK2.jsonl.

import heapq
from collections import Counter, deque
from collections.abc import Hashable, Sequence
from fractions import Fraction

Row = Sequence[Hashable]


def anatomize_groups(values: Sequence[Hashable], l: int) -> list[list[int]]:
    """Partition the positions 0..n-1 into l-diverse groups by their sensitive values.

    Precondition: l >= 1 and at most n / l positions share a value (the
    eligibility condition); otherwise ValueError is raised. Each group gets at
    least l positions, all with distinct values. Ties between buckets of the
    same size go to the value that appears first, and each bucket gives up its
    oldest position first. Cost: O(n log m) time and O(n) extra space for n
    values with m distinct ones.
    """
    if l < 1:
        raise ValueError("l must be at least 1")
    n = len(values)
    groups: list[list[int]] = []  # @line L1
    index: dict[Hashable, int] = {}
    queues: list[deque[int]] = []
    for i, v in enumerate(values):  # @line L2
        if v not in index:
            index[v] = len(queues)
            queues.append(deque())
        queues[index[v]].append(i)
    if queues and l * max(len(q) for q in queues) > n:
        raise ValueError("not eligible: more than n / l tuples share a sensitive value")
    heap = [(-len(q), k) for k, q in enumerate(queues)]
    heapq.heapify(heap)
    while len(heap) >= l:  # @line L3
        group: list[int] = []  # @line L4
        chosen = [heapq.heappop(heap) for _ in range(l)]  # @line L5
        for neg_size, k in chosen:  # @line L6
            group.append(queues[k].popleft())  # @line L7
            if neg_size + 1 < 0:
                heapq.heappush(heap, (neg_size + 1, k))
        groups.append(group)
    seen = [{values[i] for i in g} for g in groups]
    for _, k in sorted(heap, key=lambda e: e[1]):  # @line L8
        i = queues[k].popleft()  # @line L9
        v = values[i]
        target = next(j for j, vs in enumerate(seen) if v not in vs)  # @line L10
        groups[target].append(i)  # @line L11
        seen[target].add(v)
    return groups


def anatomize(
    table: Sequence[Row], qi: Sequence[int], s: int, l: int
) -> tuple[list[tuple[Hashable, ...]], list[tuple[int, Hashable, int]]]:
    """Return the quasi-identifier table and the sensitive table of an anatomized release.

    A QIT row is the quasi-identifier values of a tuple followed by its group
    id (from 1). An ST row is (group id, value, count). Inside each group the
    rows are sorted, so the row order does not link a QIT row to an ST row.
    Precondition: as for anatomize_groups, and the values of each column are
    mutually comparable. Cost: O(n log n) time, O(n) extra space.
    """
    groups = anatomize_groups([row[s] for row in table], l)
    qit: list[tuple[Hashable, ...]] = []
    st: list[tuple[int, Hashable, int]] = []
    for j, g in enumerate(groups, start=1):  # @line L12
        qit.extend((*key, j) for key in sorted(tuple(table[i][a] for a in qi) for i in g))  # @line L13
        counts = Counter(table[i][s] for i in g)
        st.extend((j, v, c) for v, c in sorted(counts.items()))  # @line L14
    return qit, st  # @line L15


def reconstruction_error(groups: Sequence[Sequence[Hashable]]) -> Fraction:
    """Return the RCE of Xiao and Tao for groups given as lists of sensitive values.

    For a tuple with value v in group G, the error is (1 - c(v)/|G|)^2 plus the
    sum of c(u)^2 / |G|^2 over the other values u of G. Cost: O(n) for n tuples
    when each group has O(1) distinct values, O(sum of |G| m_G) in general.
    """
    total = Fraction(0)
    for g in groups:
        size = len(g)
        counts = Counter(g)
        for v in g:
            err = (1 - Fraction(counts[v], size)) ** 2
            err += sum((Fraction(c * c, size * size) for u, c in counts.items() if u != v), Fraction(0))
            total += err
    return total
