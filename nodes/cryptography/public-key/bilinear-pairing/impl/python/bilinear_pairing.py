# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bilinear-pairing/. The authors are listed in prov/VJKYK9.jsonl.
#
# A symmetric (Type 1) pairing on the supersingular curve E: y^2 = x^3 + x over F_p with
# p = 3 (mod 4): the modified reduced Tate pairing e(P, Q) = t_r(P, psi(Q)) with the distortion
# map psi(x, y) = (-x, i*y). #E(F_p) = p + 1 and the embedding degree is 2, so GT lies in F_p2.
# For study only. The parameters are toys and NOT secure (a 128-bit p gives a discrete
# logarithm problem in F_p2 of 256 binary digits), and the code is not constant time. Use a
# maintained library for BLS12-381, such as blst or MCL, instead.

import hashlib


class Curve:
    """E: y^2 = x^3 + x over F_p, with a prime r dividing p + 1. Points are (x, y) or None."""

    def __init__(self, p: int, r: int):
        if p % 4 != 3 or (p + 1) % r != 0:
            raise ValueError("need p = 3 (mod 4) and r | p + 1")
        self.p, self.r = p, r
        self.cofactor = (p + 1) // r

    # ---- F_p2 = F_p[i] with i^2 = -1; (a, b) means a + b*i ----

    def f2_mul(self, x, y):
        p = self.p
        return ((x[0] * y[0] - x[1] * y[1]) % p, (x[0] * y[1] + x[1] * y[0]) % p)

    def f2_inv(self, x):
        p = self.p
        n = (x[0] * x[0] + x[1] * x[1]) % p
        t = pow(n, p - 2, p)
        return (x[0] * t % p, -x[1] * t % p)

    def f2_pow(self, x, e):
        result = (1, 0)
        while e:
            if e & 1:
                result = self.f2_mul(result, x)
            x = self.f2_mul(x, x)
            e >>= 1
        return result

    # ---- the curve ----

    def on_curve(self, Q) -> bool:
        if Q is None:
            return True
        x, y = Q
        return (y * y - x * x * x - x) % self.p == 0

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
        """k*Q by double and add. Not constant time."""
        result = None
        if k < 0:
            k, Q = -k, (Q[0], -Q[1] % self.p) if Q else None
        while k:
            if k & 1:
                result = self.add(result, Q)
            Q = self.add(Q, Q)
            k >>= 1
        return result

    def points_of_order_r(self):
        """All points of G1 = E(F_p)[r] (small p only)."""
        p, out = self.p, []
        for x in range(p):
            rhs = (x * x * x + x) % p
            for y in range(p):
                if y * y % p == rhs:
                    Q = self.mul(self.cofactor, (x, y))
                    if Q is not None and Q not in out:
                        out.append(Q)
        return out

    def generator(self):
        """The cofactor multiple of the point with the smallest x >= 1 that gives a point of order r."""
        p, x = self.p, 1
        while True:
            rhs = (x * x * x + x) % p
            if rhs and pow(rhs, (p - 1) // 2, p) == 1:
                y = pow(rhs, (p + 1) // 4, p)
                G = self.mul(self.cofactor, (x, y))
                if G is not None:
                    return G
            x += 1

    def hash_to_g1(self, data: bytes):
        """A toy try-and-increment hash to G1. It is not the hash to curve of RFC 9380."""
        p, ctr = self.p, 0
        while True:
            h = hashlib.sha256(b"toy-H1" + ctr.to_bytes(4, "big") + data).digest()
            h += hashlib.sha256(b"toy-H1b" + ctr.to_bytes(4, "big") + data).digest()
            x = int.from_bytes(h, "big") % p
            rhs = (x * x * x + x) % p
            if rhs and pow(rhs, (p - 1) // 2, p) == 1:
                y = pow(rhs, (p + 1) // 4, p)
                Q = self.mul(self.cofactor, (x, y if h[-1] & 1 == 0 else -y % p))
                if Q is not None:
                    return Q
            ctr += 1

    # ---- the pairing ----

    def distortion(self, Q):
        """psi(x, y) = (-x, i*y), a point of E(F_p2) that is not in E(F_p)."""
        x, y = Q
        return ((-x % self.p, 0), (0, y))

    def miller(self, A, B):
        """f_{r,A} at psi(B), with the vertical lines left out (their values lie in F_p)."""
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
                if xt == A[0]:  # T = -A: the line is vertical; skip it
                    T = None
                    continue
                lam = (A[1] - yt) * pow(A[0] - xt, p - 2, p) % p
                f = self.f2_mul(f, ((lam * (xq + xt) - yt) % p, yq))
                T = self.add(T, A)
        return f

    def pairing(self, A, B):
        """e(A, B) = f_{r,A}(psi(B))^((p^2 - 1)/r), the modified reduced Tate pairing on G1 x G1."""
        if A is None or B is None:
            return (1, 0)
        f = self.miller(A, B)
        g = self.f2_mul((f[0], -f[1] % self.p), self.f2_inv(f))  # f^(p - 1) = conj(f)/f
        return self.f2_pow(g, self.cofactor)  # then to the power (p + 1)/r


# The toy curve of the tests: r is the smallest prime above 2^63 and p = c*r - 1 has 128 binary digits.
TOY = Curve(170141183460469232340429858148299309287, 9223372036854775837)
# The hand-sized curve of the worked example: #E(F_11) = 12 and r = 3.
TINY = Curve(11, 3)


def gt_bytes(z) -> bytes:
    return z[0].to_bytes(16, "big") + z[1].to_bytes(16, "big")
