# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miller-algorithm/. The authors are listed in prov/7N5369.jsonl.
#
# Miller's algorithm for f_{r,P}(Q) on E: y^2 = x^3 + a*x + b over F_p, with P in E(F_p) and Q in
# E(F_p2), F_p2 = F_p[i] with i^2 = -1 (so p = 3 mod 4 and the embedding degree is k = 2).
# It gives the reduced Tate pairing f_{r,P}(Q)^((p^2 - 1)/r) and the Weil pairing.
# For study only. The curves here are toys and NOT secure, and the code is not constant time.
# Use a maintained pairing library (blst or MCL for BLS12-381) instead.

# ---- F_p2 arithmetic; elements are pairs (u, v) meaning u + v*i ----


class Fp2:
    def __init__(self, p: int):
        if p % 4 != 3:
            raise ValueError("F_p[i] is a field only when p = 3 (mod 4)")
        self.p = p

    def e(self, u, v=0):
        return (u % self.p, v % self.p)

    def add(self, x, y):
        return ((x[0] + y[0]) % self.p, (x[1] + y[1]) % self.p)

    def sub(self, x, y):
        return ((x[0] - y[0]) % self.p, (x[1] - y[1]) % self.p)

    def mul(self, x, y):
        p = self.p
        return ((x[0] * y[0] - x[1] * y[1]) % p, (x[0] * y[1] + x[1] * y[0]) % p)

    def inv(self, x):
        p = self.p
        n = (x[0] * x[0] + x[1] * x[1]) % p
        if n == 0:
            raise ZeroDivisionError("zero in F_p2")
        t = pow(n, p - 2, p)
        return (x[0] * t % p, -x[1] * t % p)

    def div(self, x, y):
        return self.mul(x, self.inv(y))

    def pow(self, x, n: int):
        result = (1, 0)
        while n:
            if n & 1:
                result = self.mul(result, x)
            x = self.mul(x, x)
            n >>= 1
        return result

    def conj(self, x):
        """The Frobenius x -> x^p, which maps i to -i."""
        return (x[0], -x[1] % self.p)


class Curve:
    """E: y^2 = x^3 + a x + b over F_p, points over F_p2 as ((u, v), (u, v)), None is infinity."""

    def __init__(self, p: int, a: int, b: int, r: int):
        self.F = Fp2(p)
        self.p, self.r = p, r
        self.a, self.b = self.F.e(a), self.F.e(b)

    def point(self, x, y):
        F = self.F
        X = x if isinstance(x, tuple) else F.e(x)
        Y = y if isinstance(y, tuple) else F.e(y)
        if not self.on_curve((X, Y)):
            raise ValueError("not on the curve")
        return (X, Y)

    def on_curve(self, T) -> bool:
        if T is None:
            return True
        F = self.F
        x, y = T
        rhs = F.add(F.add(F.mul(F.mul(x, x), x), F.mul(self.a, x)), self.b)
        return F.mul(y, y) == rhs

    def neg(self, T):
        return None if T is None else (T[0], self.F.sub((0, 0), T[1]))

    def slope(self, T, U):
        """The slope of the line through T and U (the tangent if T = U), or None if it is vertical."""
        F = self.F
        if T[0] == U[0]:
            if T[1] != U[1] or T[1] == (0, 0):
                return None
            num = F.add(F.mul(F.e(3), F.mul(T[0], T[0])), self.a)
            return F.div(num, F.mul(F.e(2), T[1]))
        return F.div(F.sub(U[1], T[1]), F.sub(U[0], T[0]))

    def add(self, T, U):
        F = self.F
        if T is None:
            return U
        if U is None:
            return T
        lam = self.slope(T, U)
        if lam is None:
            return None
        x3 = F.sub(F.sub(F.mul(lam, lam), T[0]), U[0])
        return (x3, F.sub(F.mul(lam, F.sub(T[0], x3)), T[1]))

    def mul(self, n: int, T):
        result = None
        while n:
            if n & 1:
                result = self.add(result, T)
            T = self.add(T, T)
            n >>= 1
        return result

    # ---- line functions ----

    def line(self, T, U, Q):
        """l_{T,U}(Q): the line through T and U (tangent if T = U), at Q."""
        F = self.F
        lam = self.slope(T, U)
        if lam is None:  # vertical line x - x_T
            return F.sub(Q[0], T[0])
        return F.sub(F.sub(Q[1], T[1]), F.mul(lam, F.sub(Q[0], T[0])))

    def vertical(self, V, Q):
        """v_V(Q) = x_Q - x_V, and 1 when V is the point at infinity."""
        return (1, 0) if V is None else self.F.sub(Q[0], V[0])

    def miller(self, P, Q, n: int, denominators: bool = True):
        """f_{n,P}(Q), where f_{n,P} has divisor n(P) - ([n]P) - (n - 1)(O)."""
        F = self.F
        T = P  # @line L1
        f = (1, 0)
        for bit in bin(n)[3:]:  # @line L2
            num = self.line(T, T, Q)  # @line L3
            T2 = self.add(T, T)
            den = self.vertical(T2, Q) if denominators else (1, 0)
            f = F.div(F.mul(F.mul(f, f), num), den)
            T = T2  # @line L4
            if bit == "1":  # @line L5
                num = self.line(T, P, Q)  # @line L6
                TP = self.add(T, P)
                den = self.vertical(TP, Q) if denominators else (1, 0)
                f = F.div(F.mul(f, num), den)
                T = TP  # @line L7
        return f  # @line L8

    def final_exponentiation(self, f):
        """f^((p^2 - 1)/r) as (conj(f)/f)^((p + 1)/r): one inversion and a short power."""
        F = self.F
        return F.pow(F.div(F.conj(f), f), (self.p + 1) // self.r)

    def tate(self, P, Q, fast: bool = True):
        """The reduced Tate pairing t_r(P, Q) = f_{r,P}(Q)^((p^2 - 1)/r)."""
        if P is None or Q is None:
            return (1, 0)
        if fast:
            # Denominator elimination: when x_Q lies in F_p, every vertical line value x_Q - x_V lies
            # in F_p, and the final exponentiation sends it to 1. Otherwise keep the denominators.
            keep = Q[0][1] != 0
            return self.final_exponentiation(self.miller(P, Q, self.r, denominators=keep))
        f = self.miller(P, Q, self.r)
        return self.F.pow(f, (self.p * self.p - 1) // self.r)  # @line L9

    def weil(self, P, Q):
        """e_r(P, Q) = (-1)^r f_{r,P}(Q) / f_{r,Q}(P) (Miller 2004), for P and Q of order r, not multiples."""
        F = self.F
        w = F.div(self.miller(P, Q, self.r), self.miller(Q, P, self.r))
        return w if self.r % 2 == 0 else F.sub((0, 0), w)

    def distortion(self, T):
        """(x, y) -> (-x, i y), an endomorphism of y^2 = x^3 + a x when b = 0."""
        F = self.F
        return (F.sub((0, 0), T[0]), F.mul((0, 1), T[1]))
