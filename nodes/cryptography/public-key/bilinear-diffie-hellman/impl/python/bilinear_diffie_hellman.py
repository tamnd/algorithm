# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bilinear-diffie-hellman/. The authors are listed in prov/42KE82.jsonl.
#
# The BDH and DBDH problems on a toy symmetric pairing, the reductions from CDH in G1 and in GT,
# and the pairing test that makes DDH easy in G1.
# The pairing is the modified reduced Tate pairing on y^2 = x^3 + x over F_p, p = 3 (mod 4),
# with the distortion map (x, y) -> (-x, i y). For study only: the curves are NOT secure and
# the code is not constant time. Use a maintained library for BLS12-381 (blst, MCL) instead.

import random


class Curve:
    """E: y^2 = x^3 + x over F_p with a prime r dividing p + 1. Points are (x, y) or None."""

    def __init__(self, p: int, r: int):
        if p % 4 != 3 or (p + 1) % r != 0:
            raise ValueError("need p = 3 (mod 4) and r | p + 1")
        self.p, self.r = p, r
        self.cofactor = (p + 1) // r

    def f2_mul(self, x, y):
        p = self.p
        return ((x[0] * y[0] - x[1] * y[1]) % p, (x[0] * y[1] + x[1] * y[0]) % p)

    def f2_inv(self, x):
        p = self.p
        t = pow((x[0] * x[0] + x[1] * x[1]) % p, p - 2, p)
        return (x[0] * t % p, -x[1] * t % p)

    def f2_pow(self, x, e):
        result = (1, 0)
        while e:
            if e & 1:
                result = self.f2_mul(result, x)
            x = self.f2_mul(x, x)
            e >>= 1
        return result

    def add(self, A, B):
        p = self.p
        if A is None:
            return B
        if B is None:
            return A
        (x1, y1), (x2, y2) = A, B
        if x1 == x2:
            if (y1 + y2) % p == 0:
                return None
            lam = (3 * x1 * x1 + 1) * pow(2 * y1, p - 2, p) % p
        else:
            lam = (y2 - y1) * pow(x2 - x1, p - 2, p) % p
        x3 = (lam * lam - x1 - x2) % p
        return (x3, (lam * (x1 - x3) - y1) % p)

    def mul(self, k: int, Q):
        k %= self.r  # points of G1 have order r
        result = None
        while k:
            if k & 1:
                result = self.add(result, Q)
            Q = self.add(Q, Q)
            k >>= 1
        return result

    def generator(self):
        p, x = self.p, 1
        while True:
            rhs = (x * x * x + x) % p
            if rhs and pow(rhs, (p - 1) // 2, p) == 1:
                y = pow(rhs, (p + 1) // 4, p)
                G = None
                Q, k = (x, y), self.cofactor
                while k:  # cofactor multiplication without the reduction modulo r
                    if k & 1:
                        G = self.add(G, Q)
                    Q = self.add(Q, Q)
                    k >>= 1
                if G is not None:
                    return G
            x += 1

    def pairing(self, A, B):
        """e(A, B) = f_{r,A}(psi(B))^((p^2 - 1)/r), a symmetric pairing on G1 x G1."""
        if A is None or B is None:
            return (1, 0)
        p = self.p
        xq, yq = B
        f, T = (1, 0), A
        for bit in bin(self.r)[3:]:
            xt, yt = T
            lam = (3 * xt * xt + 1) * pow(2 * yt, p - 2, p) % p
            f = self.f2_mul(self.f2_mul(f, f), ((lam * (xq + xt) - yt) % p, yq))
            T = self.add(T, T)
            if bit == "1":
                xt, yt = T
                if xt == A[0]:
                    T = None
                    continue
                lam = (A[1] - yt) * pow(A[0] - xt, p - 2, p) % p
                f = self.f2_mul(f, ((lam * (xq + xt) - yt) % p, yq))
                T = self.add(T, A)
        g = self.f2_mul((f[0], -f[1] % p), self.f2_inv(f))
        return self.f2_pow(g, self.cofactor)


TOY = Curve(170141183460469232340429858148299309287, 9223372036854775837)
TINY = Curve(59, 5)


# ---- the problems ----


def bdh_instance(C: Curve, rng: random.Random):
    """A BDH instance (P, aP, bP, cP) and its answer e(P, P)^(abc)."""
    P = C.generator()
    a, b, c = (rng.randrange(1, C.r) for _ in range(3))
    answer = C.f2_pow(C.pairing(P, P), a * b * c % C.r)
    return (P, C.mul(a, P), C.mul(b, P), C.mul(c, P)), answer


def dbdh_instance(C: Curve, rng: random.Random, real: bool):
    """(P, aP, bP, cP, Z) with Z = e(P, P)^(abc) if real, else e(P, P)^z for a random z."""
    (P, A, B, Cc), answer = bdh_instance(C, rng)
    Z = answer if real else C.f2_pow(C.pairing(P, P), rng.randrange(1, C.r))
    return P, A, B, Cc, Z


def ddh_test(C: Curve, P, A, B, D) -> bool:
    """Decide DDH in G1 with the pairing: D = abP if and only if e(A, B) = e(P, D)."""
    return C.pairing(A, B) == C.pairing(P, D)


def bdh_from_cdh_in_g1(C: Curve, cdh_g1, instance):
    """Solve BDH with an oracle that maps (aP, bP) to abP: e(abP, cP) = e(P, P)^(abc)."""
    P, A, B, Cc = instance
    return C.pairing(cdh_g1(A, B), Cc)


def bdh_from_cdh_in_gt(C: Curve, cdh_gt, instance):
    """Solve BDH with an oracle for CDH in GT, on g = e(P, P), g^(ab) = e(aP, bP), g^c = e(P, cP)."""
    P, A, B, Cc = instance
    return cdh_gt(C.pairing(P, P), C.pairing(A, B), C.pairing(P, Cc))


def bdh_by_discrete_log(C: Curve, instance):
    """Solve BDH on a tiny curve by finding a with a brute-force discrete logarithm in G1."""
    P, A, B, Cc = instance
    a = next(k for k in range(1, C.r) if C.mul(k, P) == A)
    return C.f2_pow(C.pairing(B, Cc), a)
