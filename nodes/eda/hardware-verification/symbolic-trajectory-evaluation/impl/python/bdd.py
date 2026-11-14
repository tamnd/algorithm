# SPDX-License-Identifier: MIT
# Shared helper of the hv2 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""A small reduced ordered BDD package with a unique table and an ITE cache.

A node is an integer. The terminals are 0 (false) and 1 (true). A variable is a
non-negative integer, and a smaller integer is nearer the root. Every inner node
is a triple (var, lo, hi) with lo != hi, and the unique table keeps one node per
triple, so two BDDs of the same manager are equal functions exactly when they
are the same integer.
"""

from __future__ import annotations

from typing import Iterable, Optional

FALSE = 0
TRUE = 1
_TERMINAL_VAR = 1 << 30


class BDD:
    """One manager. All BDDs that are combined must come from the same manager."""

    def __init__(self) -> None:
        self._var: list[int] = [_TERMINAL_VAR, _TERMINAL_VAR]
        self._lo: list[int] = [0, 1]
        self._hi: list[int] = [0, 1]
        self._unique: dict[tuple[int, int, int], int] = {}
        self._ite_cache: dict[tuple[int, int, int], int] = {}

    # -- construction -------------------------------------------------------
    def mk(self, v: int, lo: int, hi: int) -> int:
        """The node (v, lo, hi), reduced: equal children give the child."""
        if lo == hi:
            return lo
        key = (v, lo, hi)
        n = self._unique.get(key)
        if n is None:
            n = len(self._var)
            self._var.append(v)
            self._lo.append(lo)
            self._hi.append(hi)
            self._unique[key] = n
        return n

    def var(self, v: int) -> int:
        """The BDD of the single variable v."""
        return self.mk(v, FALSE, TRUE)

    def top(self, f: int) -> int:
        return self._var[f]

    def low(self, f: int) -> int:
        return self._lo[f]

    def high(self, f: int) -> int:
        return self._hi[f]

    def _cof(self, f: int, v: int, b: int) -> int:
        if self._var[f] != v:
            return f
        return self._hi[f] if b else self._lo[f]

    def ite(self, f: int, g: int, h: int) -> int:
        """If f then g else h, by Shannon expansion on the top variable."""
        if f == TRUE:
            return g
        if f == FALSE:
            return h
        if g == h:
            return g
        if g == TRUE and h == FALSE:
            return f
        key = (f, g, h)
        r = self._ite_cache.get(key)
        if r is not None:
            return r
        v = min(self._var[f], self._var[g], self._var[h])
        lo = self.ite(self._cof(f, v, 0), self._cof(g, v, 0), self._cof(h, v, 0))
        hi = self.ite(self._cof(f, v, 1), self._cof(g, v, 1), self._cof(h, v, 1))
        r = self.mk(v, lo, hi)
        self._ite_cache[key] = r
        return r

    def neg(self, f: int) -> int:
        return self.ite(f, FALSE, TRUE)

    def conj(self, f: int, g: int) -> int:
        return self.ite(f, g, FALSE)

    def disj(self, f: int, g: int) -> int:
        return self.ite(f, TRUE, g)

    def xor(self, f: int, g: int) -> int:
        return self.ite(f, self.neg(g), g)

    def xnor(self, f: int, g: int) -> int:
        return self.ite(f, g, self.neg(g))

    def restrict(self, f: int, v: int, b: int) -> int:
        """f with the variable v set to the constant b."""
        memo: dict[int, int] = {}

        def go(n: int) -> int:
            if n <= 1 or self._var[n] > v:
                return n
            if n in memo:
                return memo[n]
            if self._var[n] == v:
                r = self._hi[n] if b else self._lo[n]
            else:
                r = self.mk(self._var[n], go(self._lo[n]), go(self._hi[n]))
            memo[n] = r
            return r

        return go(f)

    def exists(self, f: int, vs: Iterable[int]) -> int:
        """Existential quantification of the variables vs."""
        for v in sorted(set(vs), reverse=True):
            f = self.disj(self.restrict(f, v, 0), self.restrict(f, v, 1))
        return f

    # -- queries ------------------------------------------------------------
    def evaluate(self, f: int, assignment: dict[int, int]) -> int:
        """The value of f at a point; a missing variable counts as 0."""
        while f > 1:
            f = self._hi[f] if assignment.get(self._var[f], 0) else self._lo[f]
        return f

    def size(self, f: int) -> int:
        """The number of nodes of f, terminals included."""
        seen: set[int] = set()
        stack = [f]
        while stack:
            n = stack.pop()
            if n in seen:
                continue
            seen.add(n)
            if n > 1:
                stack.append(self._lo[n])
                stack.append(self._hi[n])
        return len(seen)

    def support(self, f: int) -> set[int]:
        out: set[int] = set()
        seen: set[int] = set()
        stack = [f]
        while stack:
            n = stack.pop()
            if n <= 1 or n in seen:
                continue
            seen.add(n)
            out.add(self._var[n])
            stack.append(self._lo[n])
            stack.append(self._hi[n])
        return out

    def sat_one(self, f: int) -> Optional[dict[int, int]]:
        """One point where f is 1 (variables not on the path are left out), or None."""
        if f == FALSE:
            return None
        out: dict[int, int] = {}
        while f > 1:
            if self._lo[f] != FALSE:
                out[self._var[f]] = 0
                f = self._lo[f]
            else:
                out[self._var[f]] = 1
                f = self._hi[f]
        return out
