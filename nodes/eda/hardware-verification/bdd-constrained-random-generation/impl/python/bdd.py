# SPDX-License-Identifier: MIT
# Shared helper of the hv3 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""A small reduced ordered BDD package with a unique table.

Variables are 0 .. n-1, and variable i is at level i, so the order is fixed.
Node 0 is the constant 0 and node 1 the constant 1; both are at level n.
Every other node is a triple (var, lo, hi) with lo != hi, stored once.
"""


class BDD:
    def __init__(self, n):
        if n < 0:
            raise ValueError("the number of variables must be nonnegative")
        self.n = n
        self._var = [n, n]      # level of each node
        self._lo = [0, 1]
        self._hi = [0, 1]
        self._unique = {}
        self._cache = {}

    # structure

    def level(self, u):
        return self._var[u]

    def low(self, u):
        return self._lo[u]

    def high(self, u):
        return self._hi[u]

    def is_terminal(self, u):
        return u <= 1

    def mk(self, i, lo, hi):
        """The node for (if x_i then hi else lo), reduced and shared."""
        if not 0 <= i < self.n:
            raise ValueError("no variable %r" % (i,))
        if lo == hi:
            return lo
        if self._var[lo] <= i or self._var[hi] <= i:
            raise ValueError("children must be below the variable")
        key = (i, lo, hi)
        u = self._unique.get(key)
        if u is None:
            u = len(self._var)
            self._var.append(i)
            self._lo.append(lo)
            self._hi.append(hi)
            self._unique[key] = u
        return u

    def var(self, i):
        return self.mk(i, 0, 1)

    def nvar(self, i):
        return self.mk(i, 1, 0)

    # operations

    def ite(self, f, g, h):
        """If f then g else h, by Shannon expansion on the top variable."""
        if f == 1:
            return g
        if f == 0:
            return h
        if g == h:
            return g
        if g == 1 and h == 0:
            return f
        key = (f, g, h)
        r = self._cache.get(key)
        if r is not None:
            return r
        i = min(self._var[f], self._var[g], self._var[h])
        f0, f1 = self._cof(f, i)
        g0, g1 = self._cof(g, i)
        h0, h1 = self._cof(h, i)
        r = self.mk(i, self.ite(f0, g0, h0), self.ite(f1, g1, h1))
        self._cache[key] = r
        return r

    def _cof(self, u, i):
        if self._var[u] == i:
            return self._lo[u], self._hi[u]
        return u, u

    def NOT(self, f):
        return self.ite(f, 0, 1)

    def AND(self, f, g):
        return self.ite(f, g, 0)

    def OR(self, f, g):
        return self.ite(f, 1, g)

    def XOR(self, f, g):
        return self.ite(f, self.NOT(g), g)

    # inspection

    def evaluate(self, u, x):
        """The value of the function of node u at the assignment x (a sequence of bits)."""
        while u > 1:
            u = self._hi[u] if x[self._var[u]] else self._lo[u]
        return u

    def nodes(self, u):
        """The nodes reachable from u, children before parents."""
        order, seen, stack = [], set(), [(u, False)]
        while stack:
            v, done = stack.pop()
            if done:
                order.append(v)
                continue
            if v in seen:
                continue
            seen.add(v)
            stack.append((v, True))
            if v > 1:
                stack.append((self._hi[v], False))
                stack.append((self._lo[v], False))
        return order
