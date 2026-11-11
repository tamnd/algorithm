# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/attribute-based-encryption/. The authors are listed in prov/Q5ZTFT.jsonl.
#
# Key-policy attribute-based encryption: the small-universe construction of Goyal, Pandey, Sahai
# and Waters (CCS 2006) with access trees of threshold gates. A key holds a policy tree; a
# ciphertext holds a set of attributes. Shamir sharing of the master value y goes down the tree,
# and decryption recombines e(P, P)^(s q_x(0)) with Lagrange coefficients in the exponent.
# The pairing is the modified reduced Tate pairing on y^2 = x^3 + x over F_p, p = 3 (mod 4).
# For study only. The curve is a toy and NOT secure, and the code is not constant time.
# Use a maintained ABE library (for example the schemes of the Charm framework) instead.

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
        e %= self.r  # elements of GT have order r
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
                G, Q, k = None, (x, pow(rhs, (p + 1) // 4, p)), self.cofactor
                while k:
                    if k & 1:
                        G = self.add(G, Q)
                    Q = self.add(Q, Q)
                    k >>= 1
                if G is not None:
                    return G
            x += 1

    def pairing(self, A, B):
        """e(A, B) = f_{r,A}(psi(B))^((p^2 - 1)/r), with psi(x, y) = (-x, i y)."""
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
        e = self.cofactor
        result = (1, 0)
        while e:
            if e & 1:
                result = self.f2_mul(result, g)
            g = self.f2_mul(g, g)
            e >>= 1
        return result


TOY = Curve(170141183460469232340429858148299309287, 9223372036854775837)


# ---- policies: ("attr", name) or ("thr", k, [children]); AND is n of n, OR is 1 of n ----


def attr(name: str):
    return ("attr", name)


def threshold(k: int, *children):
    if not 1 <= k <= len(children):
        raise ValueError("need 1 <= k <= number of children")
    return ("thr", k, list(children))


def AND(*children):
    return threshold(len(children), *children)


def OR(*children):
    return threshold(1, *children)


def satisfies(policy, attributes) -> bool:
    if policy[0] == "attr":
        return policy[1] in attributes
    return sum(satisfies(c, attributes) for c in policy[2]) >= policy[1]


def lagrange_at_zero(i: int, S, r: int) -> int:
    """Delta_{i,S}(0) = prod over j in S, j != i, of (0 - j)/(i - j) modulo r."""
    num, den = 1, 1
    for j in S:
        if j != i:
            num = num * (-j) % r
            den = den * (i - j) % r
    return num * pow(den, -1, r) % r


# ---- the scheme ----


def setup(C: Curve, universe, rng: random.Random):
    P = C.generator()
    t = {a: rng.randrange(1, C.r) for a in universe}
    y = rng.randrange(1, C.r)
    pk = {"P": P, "T": {a: C.mul(t[a], P) for a in universe}, "Y": C.f2_pow(C.pairing(P, P), y)}
    return pk, {"t": t, "y": y}


def keygen(C: Curve, pk, msk, policy, rng: random.Random):
    """Share y down the tree with fresh random polynomials; a leaf x for attribute a gets (q_x(0)/t_a) P."""
    leaves = []

    def share(node, secret):
        if node[0] == "attr":
            a = node[1]
            leaves.append((node, C.mul(secret * pow(msk["t"][a], -1, C.r), pk["P"])))
            return ("attr", a, len(leaves) - 1)
        k, children = node[1], node[2]
        coeffs = [secret] + [rng.randrange(C.r) for _ in range(k - 1)]
        out = []
        for index, child in enumerate(children, start=1):
            value = sum(c * pow(index, e, C.r) for e, c in enumerate(coeffs)) % C.r
            out.append(share(child, value))
        return ("thr", k, out)

    tree = share(policy, msk["y"])
    return {"tree": tree, "D": [d for _, d in leaves]}


def encrypt(C: Curve, pk, attributes, M, rng: random.Random):
    """M is an element of GT. The ciphertext is (gamma, M Y^s, {s T_a : a in gamma})."""
    s = rng.randrange(1, C.r)
    return {
        "attrs": frozenset(attributes),
        "E1": C.f2_mul(M, C.f2_pow(pk["Y"], s)),
        "E": {a: C.mul(s, pk["T"][a]) for a in attributes},
    }


def decrypt_node(C: Curve, key, ct, node):
    """Return e(P, P)^(s q_x(0)) for the node, or None if its subtree is not satisfied."""
    if node[0] == "attr":
        a, leaf = node[1], node[2]
        if a not in ct["attrs"]:
            return None
        return C.pairing(key["D"][leaf], ct["E"][a])
    k, children = node[1], node[2]
    found = {}
    for index, child in enumerate(children, start=1):
        value = decrypt_node(C, key, ct, child)
        if value is not None:
            found[index] = value
            if len(found) == k:
                break
    if len(found) < k:
        return None
    S = list(found)
    result = (1, 0)
    for i in S:
        result = C.f2_mul(result, C.f2_pow(found[i], lagrange_at_zero(i, S, C.r)))
    return result


def decrypt(C: Curve, key, ct):
    Ys = decrypt_node(C, key, ct, key["tree"])
    if Ys is None:
        return None
    return C.f2_mul(ct["E1"], C.f2_inv(Ys))


def collude(C: Curve, key1, leaf1: int, index1: int, key2, leaf2: int, index2: int, ct, a1, a2):
    """Two users pool one leaf each into a 2-of-2 gate: this does NOT give Y^s."""
    F1 = C.pairing(key1["D"][leaf1], ct["E"][a1])
    F2 = C.pairing(key2["D"][leaf2], ct["E"][a2])
    S = [index1, index2]
    Ys = C.f2_mul(C.f2_pow(F1, lagrange_at_zero(index1, S, C.r)), C.f2_pow(F2, lagrange_at_zero(index2, S, C.r)))
    return C.f2_mul(ct["E1"], C.f2_inv(Ys))
