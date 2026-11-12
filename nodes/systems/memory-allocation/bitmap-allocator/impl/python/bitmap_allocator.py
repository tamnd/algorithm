# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitmap-allocator/. The authors are listed in prov/GDECRB.jsonl.

"""A bitmap allocator over h units, with words of w = 64 bits.

USED has one bit per unit, 1 for a unit in use. START has one bit per unit,
1 for the first unit of an allocated block, so free(p) finds the end of the
block without a header. malloc(n) is first fit: it returns the lowest address
of n free units in a row. It works on whole words: a run that crosses a word
border is found with a trailing zero count, and a run inside one word is found
with the doubling trick r &= r >> s.
"""

W = 64
ALL = (1 << W) - 1


def tz(x: int) -> int:
    """Trailing zero count of a w-bit word; tz(0) = w."""
    if x == 0:
        return W
    return (x & -x).bit_length() - 1


def lz(x: int) -> int:
    """Leading zero count of a w-bit word; lz(0) = w."""
    return W - x.bit_length()


def run_of_ones(f: int, n: int) -> int:
    """Bit j of the result is 1 iff bits j .. j+n-1 of f are all 1 (1 <= n <= w)."""
    r = f
    m = n - 1  # shift still to apply
    s = 1
    while m > 0:
        t = min(s, m)
        r &= r >> t
        m -= t
        s *= 2
    return r


class BitmapAllocator:
    def __init__(self, h: int) -> None:
        if h < 1:
            raise ValueError("h must be at least 1")
        self.h = h
        self.nw = (h + W - 1) // W
        self.used = [0] * self.nw
        self.start = [0] * self.nw
        pad = self.nw * W - h
        if pad:  # units past the end count as used
            self.used[-1] = ALL ^ ((1 << (W - pad)) - 1)

    def _set_range(self, a: int, n: int, value: int) -> None:
        end = a + n
        while a < end:
            i, b = divmod(a, W)
            k = min(W - b, end - a)
            mask = ((1 << k) - 1) << b
            if value:
                self.used[i] |= mask
            else:
                self.used[i] &= ~mask
            a += k

    def _mark(self, a: int, n: int) -> int:
        self._set_range(a, n, 1)
        self.start[a // W] |= 1 << (a % W)
        return a

    def malloc(self, n: int) -> int | None:
        """First fit: the lowest address of n free units, or None."""
        if n < 1:
            raise ValueError("n must be at least 1")
        run = 0  # @line L1
        for i in range(self.nw):  # @line L2
            f = ALL ^ self.used[i]  # @line L3
            if run > 0 and run + tz(ALL ^ f) >= n:  # @line L4
                return self._mark(W * i - run, n)
            if n <= W:  # @line L5
                r = run_of_ones(f, n)
                if r:  # @line L6
                    return self._mark(W * i + tz(r), n)
            run = run + W if f == ALL else lz(ALL ^ f)  # @line L7
        return None  # @line L8

    def free(self, p: int) -> None:
        """Free the block that starts at p."""
        if not (0 <= p < self.h) or not (self.start[p // W] >> (p % W)) & 1:
            raise ValueError("p is not the start of an allocated block")
        self.start[p // W] &= ~(1 << (p % W))
        q = p  # @line L9
        i = p // W
        stop = (self.start[i] | (ALL ^ self.used[i])) >> (p % W)  # units that end the block
        if stop:
            q = p + tz(stop)
        else:
            i += 1
            while i < self.nw and not (self.start[i] | (ALL ^ self.used[i])):
                i += 1
            q = W * i + (tz(self.start[i] | (ALL ^ self.used[i])) if i < self.nw else 0)
        q = min(q, self.h)  # the padding past h is used but belongs to no block
        self._set_range(p, q - p, 0)  # @line L10

    def is_used(self, x: int) -> bool:
        return bool((self.used[x // W] >> (x % W)) & 1)
