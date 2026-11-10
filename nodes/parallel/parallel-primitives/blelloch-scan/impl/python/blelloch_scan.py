# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blelloch-scan/. The authors are listed in prov/GXQF52.jsonl.

"""The Blelloch scan (up-sweep and down-sweep), simulated round by round.

The updates of one round touch distinct cells and read no cell that the
same round writes, so running them in a loop gives the same result as
running them at the same time.
"""

from typing import Callable, TypeVar

T = TypeVar("T")


class Stats:
    """Counters: combines (work), rounds, and the longest chain of combines."""

    def __init__(self) -> None:
        self.work = 0
        self.rounds = 0
        self.chain = 0


def blelloch_scan(
    op: Callable[[T, T], T], identity: T, a: list[T], stats: Stats | None = None
) -> tuple[list[T], T]:
    """Return (exclusive scan of a, total of a)."""
    st = stats if stats is not None else Stats()
    n = len(a)
    if n == 0:  # @line L1
        return [], identity
    m = 1 << (n - 1).bit_length()  # @line L2
    x = list(a) + [identity] * (m - n)
    depth = [0] * m  # combines on the longest chain into each cell
    h = 1
    while h < m:  # @line L3: up-sweep, h = 2^d
        st.rounds += 1
        for i in range(0, m, 2 * h):  # @line L4
            left, right = i + h - 1, i + 2 * h - 1
            x[right] = op(x[left], x[right])  # @line L5
            depth[right] = max(depth[left], depth[right]) + 1
            st.work += 1
        h *= 2
    total = x[m - 1]  # @line L6
    x[m - 1] = identity
    depth[m - 1] = 0
    h = m // 2
    while h >= 1:  # @line L7: down-sweep
        st.rounds += 1
        for i in range(0, m, 2 * h):  # @line L8
            left, right = i + h - 1, i + 2 * h - 1
            t, dt = x[left], depth[left]  # @line L9
            x[left], depth[left] = x[right], depth[right]  # @line L10
            x[right] = op(x[right], t)  # @line L11: parent on the left
            depth[right] = max(depth[right], dt) + 1
            st.work += 1
        h //= 2
    st.chain = max(depth)  # over all m cells of the padded tree
    return x[:n], total  # @line L12


def down_sweep_swapped(op: Callable[[T, T], T], identity: T, a: list[T]) -> list[T]:
    """A wrong variant that sets the right child to leftsum ⊕ parent.

    It is correct for a commutative operator only.
    """
    n = len(a)
    if n == 0:
        return []
    m = 1 << (n - 1).bit_length()
    x = list(a) + [identity] * (m - n)
    h = 1
    while h < m:
        for i in range(0, m, 2 * h):
            x[i + 2 * h - 1] = op(x[i + h - 1], x[i + 2 * h - 1])
        h *= 2
    x[m - 1] = identity
    h = m // 2
    while h >= 1:
        for i in range(0, m, 2 * h):
            left, right = i + h - 1, i + 2 * h - 1
            t = x[left]
            x[left] = x[right]
            x[right] = op(t, x[right])
        h //= 2
    return x[:n]
