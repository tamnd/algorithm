# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chd-hashing/. The authors are listed in prov/X3MZCW.jsonl.

import random

P61 = (1 << 61) - 1  # a Mersenne prime, larger than every key


def poly_hash(c: tuple[int, int, int], p: int, x: int) -> int:
    """(c0 + c1 x + c2 x^2) mod p, a 3-wise independent hash over Z_p."""
    return (c[0] + (c[1] + c[2] * x) * x) % p


class CHD:
    """A perfect hash function from a static set of integer keys into [m].

    With m = n (the default) the function is minimal: a bijection from the
    keys onto [0, n). The key x goes to bucket g(x) in [r], and its slot is
    (f1(x) + d0 f2(x) + d1) mod m, where (d0, d1) is decoded from the
    displacement index sigma[g(x)]. Keys outside the set get some slot in [m].
    """

    def __init__(
        self,
        keys: list[int],
        rng: random.Random | None = None,
        m: int | None = None,
        lam: int = 5,
        p: int = P61,
    ) -> None:
        if len(set(keys)) != len(keys):
            raise ValueError("keys must be distinct")
        if any(not 0 <= x < p for x in keys):
            raise ValueError("key out of range")
        n = len(keys)
        self.n, self.p = n, p
        self.m = max(n, 1) if m is None else m
        if self.m < max(n, 1):
            raise ValueError("m must be at least the number of keys")
        self.r = max(1, -(-n // lam))  # ceil(n / lam) buckets
        self.rng = rng if rng is not None else random.Random()
        self.tries = 0
        while True:  # @line L1
            self.tries += 1
            self.coef = [tuple(self.rng.randrange(p) for _ in range(3)) for _ in range(3)]  # @line L2
            if self._build(keys):  # @line L10
                return  # @line L11

    # ----------------------------------------------------------- hashing
    def g(self, x: int) -> int:
        return poly_hash(self.coef[0], self.p, x) % self.r

    def f1(self, x: int) -> int:
        return poly_hash(self.coef[1], self.p, x) % self.m

    def f2(self, x: int) -> int:
        return poly_hash(self.coef[2], self.p, x) % self.m

    def slot(self, x: int, ell: int) -> int:
        """The slot of x under the displacement index ell."""
        d0, d1 = divmod(ell, self.m)
        return (self.f1(x) + d0 * self.f2(x) + d1) % self.m

    # ----------------------------------------------------------- build
    def _build(self, keys: list[int]) -> bool:
        m = self.m
        buckets: list[list[int]] = [[] for _ in range(self.r)]
        for x in keys:  # @line L3
            buckets[self.g(x)].append(x)
        used = [False] * m  # @line L4
        self.sigma = [0] * self.r
        order = sorted(range(self.r), key=lambda i: (-len(buckets[i]), i))
        for i in order:  # @line L5
            b = buckets[i]
            pre = [(self.f1(x), self.f2(x)) for x in b]
            ell = 0  # @line L6
            while ell < m * m:  # @line L7
                d0, d1 = divmod(ell, m)
                s = [(a + d0 * c + d1) % m for a, c in pre]
                if len(set(s)) == len(s) and not any(used[t] for t in s):
                    break
                ell += 1
            if ell == m * m:  # @line L8
                return False
            self.sigma[i] = ell  # @line L9
            for t in s:
                used[t] = True
        return True

    # ----------------------------------------------------------- query
    def __call__(self, x: int) -> int:
        i = self.g(x)  # @line L12
        d0, d1 = divmod(self.sigma[i], self.m)
        return (self.f1(x) + d0 * self.f2(x) + d1) % self.m  # @line L13

    def gamma_bits(self) -> int:
        """Bits of the Elias gamma codes of sigma[i] + 1: a simple measure of
        how well the displacement indices compress (no O(1) access)."""
        return sum(2 * (s + 1).bit_length() - 1 for s in self.sigma)
