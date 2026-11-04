# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fenwick-tree/. The authors are listed in prov/T604D3.jsonl.


def lowbit(i: int) -> int:
    """The value of the lowest set bit of i, for i >= 1."""
    return i & -i


class FenwickTree:
    """Prefix sums over A[1..n] of integers with point updates.

    The positions are 1-based, as on the page. Each operation takes
    O(log n) time; build takes O(n) time. The extra space is n integers.
    """

    def __init__(self, n: int = 0) -> None:
        """Make the tree of an array of n zeros."""
        self.n = n
        self.t = [0] * (n + 1)

    @classmethod
    def build(cls, a: list[int]) -> "FenwickTree":
        """Make the tree of A[1..n] = a[0..n-1] in O(n) time."""
        f = cls(len(a))
        f.t[1:] = list(a)  # @line L10
        for i in range(1, f.n + 1):  # @line L11
            j = i + lowbit(i)  # @line L12
            if j <= f.n:  # @line L13
                f.t[j] += f.t[i]
        return f

    def add(self, i: int, delta: int) -> None:
        """Set A[i] <- A[i] + delta, for 1 <= i <= n."""
        if not 1 <= i <= self.n:
            raise IndexError(i)
        while i <= self.n:  # @line L1
            self.t[i] += delta  # @line L2
            i += lowbit(i)  # @line L3

    def prefix(self, i: int) -> int:
        """Return A[1] + ... + A[i], for 0 <= i <= n."""
        if not 0 <= i <= self.n:
            raise IndexError(i)
        s = 0  # @line L4
        while i > 0:  # @line L5
            s += self.t[i]  # @line L6
            i -= lowbit(i)  # @line L7
        return s  # @line L8

    def range_sum(self, l: int, r: int) -> int:
        """Return A[l] + ... + A[r], for 1 <= l <= r <= n."""
        return self.prefix(r) - self.prefix(l - 1)  # @line L9

    def search(self, s: int) -> int:
        """Return the least i with prefix(i) >= s, or n + 1 if there is none.

        Precondition: every A[k] is non-negative.
        """
        pos = 0  # @line L14
        step = 1 << (self.n.bit_length() - 1) if self.n > 0 else 0
        while step > 0:  # @line L15
            if pos + step <= self.n and self.t[pos + step] < s:  # @line L16
                pos += step  # @line L17
                s -= self.t[pos]
            step //= 2  # @line L18
        return pos + 1  # @line L19

    def check_invariant(self, a: list[int]) -> None:
        """Assert that T[i] is the sum of A over (i - lowbit(i), i]; a is 0-based."""
        for i in range(1, self.n + 1):
            assert self.t[i] == sum(a[i - lowbit(i) : i])
