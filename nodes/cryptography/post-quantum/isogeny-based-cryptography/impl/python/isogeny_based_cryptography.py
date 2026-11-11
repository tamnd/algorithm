# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isogeny-based-cryptography/. The authors are listed in prov/BZ6XVD.jsonl.

"""A toy supersingular 2-isogeny graph and a Charles-Goren-Lauter hash walk.

- Fp2: the field F_{p^2} = F_p[i] / (i^2 + 1), for a prime p = 3 mod 4.
- Curve: short Weierstrass curves y^2 = x^3 + a x + b over F_{p^2}, affine
  points, with None as the point at infinity.
- velu: the isogeny with a given finite kernel, by Velu's formulas in the form
  of Washington, Elliptic Curves, Theorem 12.16.
- two_isogeny_graph: the graph of supersingular j-invariants over F_{p^2}
  with an edge for each 2-isogeny, found from E0 : y^2 = x^3 + x.
- cgl_hash: the hash of Charles, Goren and Lauter (2009), a walk without
  backtracking where each message bit picks one of the two forward edges.

The prime is p = 431, a toy size: the graph has 37 vertices, so collisions
are easy to find. Real proposals use p of 256 bits or more. For study only,
not constant time; there is no maintained library for the CGL hash, so use
SHA-2 or SHA-3 from a standard library for hashing.
"""

import random


class Fp2:
    """An element a + b i of F_{p^2}, with i^2 = -1."""

    __slots__ = ("a", "b", "p")

    def __init__(self, a: int, b: int, p: int) -> None:
        self.a, self.b, self.p = a % p, b % p, p

    def _c(self, o):
        return o if isinstance(o, Fp2) else Fp2(o, 0, self.p)

    def __add__(self, o):
        o = self._c(o)
        return Fp2(self.a + o.a, self.b + o.b, self.p)

    __radd__ = __add__

    def __sub__(self, o):
        o = self._c(o)
        return Fp2(self.a - o.a, self.b - o.b, self.p)

    def __rsub__(self, o):
        return self._c(o) - self

    def __neg__(self):
        return Fp2(-self.a, -self.b, self.p)

    def __mul__(self, o):
        o = self._c(o)
        return Fp2(self.a * o.a - self.b * o.b, self.a * o.b + self.b * o.a, self.p)

    __rmul__ = __mul__

    def inv(self):
        n = (self.a * self.a + self.b * self.b) % self.p
        if n == 0:
            raise ZeroDivisionError("inverse of 0")
        ni = pow(n, -1, self.p)
        return Fp2(self.a * ni, -self.b * ni, self.p)

    def __truediv__(self, o):
        return self * self._c(o).inv()

    def __rtruediv__(self, o):
        return self._c(o) * self.inv()

    def __pow__(self, e: int):
        r, x = Fp2(1, 0, self.p), self
        if e < 0:
            x, e = x.inv(), -e
        while e:
            if e & 1:
                r = r * x
            x = x * x
            e >>= 1
        return r

    def __eq__(self, o):
        o = self._c(o)
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def is_zero(self) -> bool:
        return self.a == 0 and self.b == 0

    def key(self) -> int:
        """An integer that orders the field elements."""
        return self.a + self.b * self.p

    def __repr__(self) -> str:
        return f"{self.a}+{self.b}i" if self.b else f"{self.a}"


def sqrt_fp(c: int, p: int):
    """A square root of c mod p (p = 3 mod 4), or None."""
    c %= p
    if c == 0:
        return 0
    if pow(c, (p - 1) // 2, p) != 1:
        return None
    return pow(c, (p + 1) // 4, p)


def sqrt_fp2(z: Fp2):
    """A square root of z in F_{p^2} (p = 3 mod 4), or None."""
    p, u, v = z.p, z.a, z.b
    if v == 0:
        r = sqrt_fp(u, p)
        if r is not None:
            return Fp2(r, 0, p)
        return Fp2(0, sqrt_fp(-u, p), p)
    n = sqrt_fp(u * u + v * v, p)
    if n is None:
        return None
    half = pow(2, -1, p)
    for s in (n, -n):
        x = sqrt_fp((u + s) * half, p)
        if x:
            return Fp2(x, v * pow(2 * x, -1, p), p)
    return None


class Curve:
    """y^2 = x^3 + a x + b over F_{p^2}."""

    def __init__(self, a: Fp2, b: Fp2) -> None:
        self.a, self.b, self.p = a, b, a.p

    def rhs(self, x: Fp2) -> Fp2:
        return x * x * x + self.a * x + self.b

    def j(self) -> Fp2:
        a3 = self.a * self.a * self.a * 4
        return 1728 * a3 / (a3 + self.b * self.b * 27)

    def add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        if P[0] == Q[0]:
            if (P[1] + Q[1]).is_zero():
                return None
            lam = (P[0] * P[0] * 3 + self.a) / (P[1] * 2)
        else:
            lam = (Q[1] - P[1]) / (Q[0] - P[0])
        x = lam * lam - P[0] - Q[0]
        return (x, lam * (P[0] - x) - P[1])

    def mul(self, k: int, P):
        R = None
        while k:
            if k & 1:
                R = self.add(R, P)
            P = self.add(P, P)
            k >>= 1
        return R

    def random_point(self, rng: random.Random):
        p = self.p
        while True:
            x = Fp2(rng.randrange(p), rng.randrange(p), p)
            y = sqrt_fp2(self.rhs(x))
            if y is not None:
                return (x, y)


def velu(E: Curve, K, order: int):
    """Velu: the codomain and the map of the isogeny with kernel generated by K."""
    pts, Q = [], K
    for _ in range(order - 1):
        pts.append(Q)
        Q = E.add(Q, K)
    assert Q is None, "K does not have the given order"
    S, seen = [], set()
    for Q in pts:  # the points of order 2, and one point of each pair {Q, -Q}
        if (Q[0].key(), Q[1].key()) in seen:
            continue
        seen.add((Q[0].key(), Q[1].key()))
        seen.add((Q[0].key(), (-Q[1]).key()))
        S.append(Q)
    data, v, w = [], Fp2(0, 0, E.p), Fp2(0, 0, E.p)
    for Q in S:
        gx = Q[0] * Q[0] * 3 + E.a
        gy = Q[1] * -2
        vq = gx if Q[1].is_zero() else gx * 2
        uq = gy * gy
        v, w = v + vq, w + uq + Q[0] * vq
        data.append((Q, gx, gy, vq, uq))
    E2 = Curve(E.a - v * 5, E.b - w * 7)

    def phi(P):
        if P is None:
            return None
        x, y = P
        X, Y = x, y
        for Q, gx, gy, vq, uq in data:
            d = x - Q[0]
            if d.is_zero():
                return None
            di = d.inv()
            di2 = di * di
            X = X + vq * di + uq * di2
            Y = Y - (uq * y * 2 * di2 * di + vq * (y - Q[1]) * di2 - gx * gy * di2)
        return (X, Y)

    return E2, phi


def two_torsion(E: Curve, rng: random.Random) -> list:
    """The three points of order 2 of a supersingular curve with E(F_{p^2}) = (Z/(p+1))^2."""
    p = E.p
    odd = p + 1
    while odd % 2 == 0:
        odd //= 2
    while True:
        R = E.mul(odd, E.random_point(rng))
        if R is not None:
            break
    while E.mul(2, R) is not None:
        R = E.mul(2, R)
    x0 = R[0]
    # x^3 + a x + b = (x - x0)(x^2 + x0 x + x0^2 + a)
    s = sqrt_fp2(x0 * x0 - (x0 * x0 + E.a) * 4)
    half = Fp2(pow(2, -1, p), 0, p)
    xs = [x0, (-x0 + s) * half, (-x0 - s) * half]
    return [(x, Fp2(0, 0, p)) for x in xs]


def phi2(X, Y):
    """The classical modular polynomial of level 2."""
    return (
        X**3 + Y**3 - X * X * Y * Y
        + 1488 * (X * X * Y + X * Y * Y)
        - 162000 * (X * X + Y * Y)
        + 40773375 * X * Y
        + 8748000000 * (X + Y)
        - 157464000000000
    )


def two_isogeny_graph(p: int = 431, seed: int = 1):
    """The supersingular 2-isogeny graph over F_{p^2}, by breadth-first search from j = 1728.

    Returns (adj, curves): adj maps each j-invariant to the list of the three
    j-invariants of its 2-isogenous curves (with multiplicity), and curves maps
    each j-invariant to one curve with that j-invariant.
    """
    rng = random.Random(seed)
    E0 = Curve(Fp2(1, 0, p), Fp2(0, 0, p))
    curves = {E0.j(): E0}
    adj = {}
    todo = [E0.j()]
    while todo:
        j = todo.pop()
        E = curves[j]
        nb = []
        for T in two_torsion(E, rng):
            E2, _ = velu(E, T, 2)
            j2 = E2.j()
            nb.append(j2)
            if j2 not in curves:
                curves[j2] = E2
                todo.append(j2)
        adj[j] = nb
    return adj, curves


def cgl_hash(bits, adj: dict, start: Fp2, previous: Fp2) -> Fp2:
    """The Charles-Goren-Lauter hash of a bit string, as a j-invariant.

    The walk starts at start, as if it came from previous. At each step it
    drops one edge back to the vertex it came from, sorts the two other
    neighbours, and takes the one picked by the next bit.
    """
    here, back = start, previous
    for bit in bits:
        forward = list(adj[here])
        forward.remove(back)
        forward.sort(key=lambda z: z.key())
        here, back = forward[bit], here
    return here
