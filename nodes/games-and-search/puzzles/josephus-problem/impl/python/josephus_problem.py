# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/josephus-problem/. The authors are listed in prov/8ZZ2XW.jsonl.
"""The Josephus problem: n people in a circle, numbered 1 to n; counting starts
at person 1, and every k-th person still in the circle is removed.

All survivor functions return the 1-indexed number of the last person left.
"""

from collections import deque


def simulate(n, k):
    """The full elimination order, by direct simulation on a queue. O(nk) time."""
    q = deque(range(1, n + 1))
    order = []
    while q:
        q.rotate(-(k - 1))
        order.append(q.popleft())
    return order


def survivor_recurrence(n, k):
    """J(1) = 0, J(i) = (J(i - 1) + k) mod i, in 0-indexed form. O(n) time."""
    j = 0
    for i in range(2, n + 1):
        j = (j + k) % i
    return j + 1


def survivor_k2(n):
    """Closed form for k = 2: n = 2^m + l with 0 <= l < 2^m gives 2l + 1."""
    m = n.bit_length() - 1
    return 2 * (n - (1 << m)) + 1


def rotate_left(n):
    """Move the leading 1 bit of n to the end: the k = 2 survivor as a bit rotation."""
    m = n.bit_length() - 1
    return ((n - (1 << m)) << 1) | 1


def survivor_concrete(n, k):
    """Concrete Mathematics, Section 3.3: D_0 = 1, D_j = ceil(k D_(j-1) / (k - 1)).

    The survivor is k n + 1 - D_j for the least j with D_j > (k - 1) n.
    The loop runs O(k log n) times. Needs k >= 2.
    """
    d = 1
    while d <= (k - 1) * n:
        d = -((-k * d) // (k - 1))
    return k * n + 1 - d


def survivor_fast(n, k):
    """O(k log n) recursion that removes about n/k people per round (0-indexed inside)."""

    def rec(n):
        if n == 1:
            return 0
        if k == 1:
            return n - 1
        if k > n:
            return (rec(n - 1) + k) % n
        removed = n // k
        r = rec(n - removed) - n % k
        if r < 0:
            r += n
        else:
            r += r // (k - 1)
        return r

    return rec(n) + 1


def order_fenwick(n, k):
    """The full elimination order in O(n log n) time with a Fenwick tree of the people left."""
    size = 1
    while size < n:
        size *= 2
    tree = [0] * (size + 1)
    for i in range(1, size + 1):
        if i <= n:
            tree[i] += 1
        j = i + (i & -i)
        if j <= size:
            tree[j] += tree[i]

    def take(rank):
        # find and remove the person with the given 1-based rank among those left
        pos = 0
        step = size
        while step:
            if pos + step <= size and tree[pos + step] < rank:
                pos += step
                rank -= tree[pos]
            step //= 2
        person = pos + 1
        i = person
        while i <= size:
            tree[i] -= 1
            i += i & -i
        return person

    order = []
    idx = 0
    for left in range(n, 0, -1):
        idx = (idx + k - 1) % left
        order.append(take(idx + 1))
    return order
