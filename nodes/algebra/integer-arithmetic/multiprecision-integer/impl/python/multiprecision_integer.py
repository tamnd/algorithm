# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiprecision-integer/. The authors are listed in prov/WZN2G1.jsonl.

from __future__ import annotations


class MultiprecisionInteger:
    """A signed integer stored as a sign and an array of limbs in base 2^w.

    The limbs are least significant first. Invariant: the top limb is not zero,
    the value 0 has no limbs, and 0 is never negative. Costs are in limb
    operations: add and sub take O(m + n), mul takes O(m n), divmod_limb O(n).
    """

    def __init__(self, w: int = 8) -> None:
        """The value 0 in base 2^w, for w >= 1."""
        if w < 1:
            raise ValueError("the limb width w must be at least 1")
        self.w = w
        self.base = 1 << w
        self.neg = False
        self.limbs: list[int] = []

    # ---------------------------------------------------------------- conversion

    @classmethod
    def from_int(cls, x: int, w: int = 8) -> MultiprecisionInteger:
        """The value x in base 2^w. Cost O(n) limb operations for n limbs."""
        r = cls(w)
        r.neg = x < 0
        m = -x if x < 0 else x
        while m:
            r.limbs.append(m & (r.base - 1))
            m >>= w
        return r

    @classmethod
    def from_limbs(cls, neg: bool, limbs: list[int], w: int = 8) -> MultiprecisionInteger:
        """The value (-1)^neg * sum limbs[i] * 2^(w i), normalized."""
        r = cls(w)
        if any(not 0 <= d < r.base for d in limbs):
            raise ValueError("each limb must be in [0, 2^w)")
        r.limbs = _normalize(list(limbs))
        r.neg = neg and bool(r.limbs)
        return r

    def to_int(self) -> int:
        """The value as a Python int, by Horner's rule from the top limb."""
        v = 0
        for d in reversed(self.limbs):
            v = (v << self.w) | d
        return -v if self.neg else v

    def _new(self, neg: bool, limbs: list[int]) -> MultiprecisionInteger:
        r = MultiprecisionInteger(self.w)
        r.limbs = limbs
        r.neg = neg and bool(limbs)
        return r

    def _same_base(self, y: MultiprecisionInteger) -> None:
        if self.w != y.w:
            raise ValueError("both operands need the same limb width")

    # ---------------------------------------------------------------- operations

    def neg_(self) -> MultiprecisionInteger:
        """-x. Cost O(n) for the copy."""
        return self._new(not self.neg, list(self.limbs))

    def compare(self, y: MultiprecisionInteger) -> int:
        """The sign of x - y: -1, 0 or 1. Cost O(n), O(1) if the signs or lengths differ."""
        self._same_base(y)
        if self.neg != y.neg:
            return -1 if self.neg else 1
        c = _cmp_mag(self.limbs, y.limbs)
        return -c if self.neg else c

    def add(self, y: MultiprecisionInteger) -> MultiprecisionInteger:
        """x + y. Cost O(m + n) limb operations."""
        self._same_base(y)
        if self.neg == y.neg:  # @line L1
            return self._new(self.neg, _add_mag(self.limbs, y.limbs, self.base))  # @line L2
        c = _cmp_mag(self.limbs, y.limbs)  # @line L3
        if c == 0:
            return MultiprecisionInteger(self.w)  # @line L4: zero is never negative
        if c > 0:  # @line L5
            return self._new(self.neg, _sub_mag(self.limbs, y.limbs, self.base))
        return self._new(y.neg, _sub_mag(y.limbs, self.limbs, self.base))  # @line L6

    def sub(self, y: MultiprecisionInteger) -> MultiprecisionInteger:
        """x - y, as x + (-y). Cost O(m + n)."""
        return self.add(y.neg_())

    def mul(self, y: MultiprecisionInteger) -> MultiprecisionInteger:
        """x * y by the schoolbook method. Cost O(m n) limb operations."""
        self._same_base(y)
        a, b, base, w = self.limbs, y.limbs, self.base, self.w
        if not a or not b:
            return MultiprecisionInteger(self.w)
        c = [0] * (len(a) + len(b))
        for i, ai in enumerate(a):
            carry = 0
            for j, bj in enumerate(b):
                t = c[i + j] + ai * bj + carry  # at most (base - 1) * (base + 1) < base^2
                c[i + j] = t & (base - 1)
                carry = t >> w
            c[i + len(b)] = carry
        return self._new(self.neg != y.neg, _normalize(c))

    def divmod_limb(self, d: int) -> tuple[MultiprecisionInteger, int]:
        """(q, r) with |x| = q d + r and 0 <= r < d, for one limb 0 < d < 2^w.

        The quotient gets the sign of x, so q truncates toward zero. Cost O(n).
        """
        if not 0 < d < self.base:
            raise ValueError("the divisor must be one nonzero limb")
        q = [0] * len(self.limbs)
        r = 0
        for i in range(len(self.limbs) - 1, -1, -1):
            t = (r << self.w) | self.limbs[i]  # t < d * base
            q[i], r = t // d, t % d
        return self._new(self.neg, _normalize(q)), r

    def check_invariant(self) -> None:
        """Raise AssertionError if the representation is not normalized."""
        assert all(0 <= d < self.base for d in self.limbs)
        assert not self.limbs or self.limbs[-1] != 0
        assert self.limbs or not self.neg


# -------------------------------------------------------------------- magnitudes


def _normalize(a: list[int]) -> list[int]:
    """Drop the zero limbs at the top."""
    while a and a[-1] == 0:
        a.pop()
    return a


def _cmp_mag(a: list[int], b: list[int]) -> int:
    """Compare two normalized magnitudes: -1, 0 or 1."""
    if len(a) != len(b):
        return -1 if len(a) < len(b) else 1
    for i in range(len(a) - 1, -1, -1):
        if a[i] != b[i]:
            return -1 if a[i] < b[i] else 1
    return 0


def _add_mag(a: list[int], b: list[int], base: int) -> list[int]:
    """|a| + |b|, with one carry pass."""
    if len(a) < len(b):
        a, b = b, a
    s = []
    carry = 0  # @line L7
    for i in range(len(a)):  # @line L8
        t = a[i] + (b[i] if i < len(b) else 0) + carry  # @line L9
        if t >= base:  # @line L10
            s.append(t - base)
            carry = 1
        else:
            s.append(t)
            carry = 0
    if carry:  # @line L11
        s.append(1)
    return s  # @line L12


def _sub_mag(a: list[int], b: list[int], base: int) -> list[int]:
    """|a| - |b| for |a| >= |b|, with one borrow pass, normalized."""
    s = []
    borrow = 0  # @line L13
    for i in range(len(a)):  # @line L14
        t = a[i] - (b[i] if i < len(b) else 0) - borrow  # @line L15
        if t < 0:  # @line L16
            s.append(t + base)
            borrow = 1
        else:
            s.append(t)
            borrow = 0
    s = _normalize(s)  # @line L17
    return s  # @line L18
