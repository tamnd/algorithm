# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-class-group-algorithm/. The authors are listed in prov/FFWYTM.jsonl.
"""The quantum class group algorithm for an imaginary quadratic discriminant, simulated on a small state vector.

The class group Cl(D) of a negative discriminant D is the group of classes of primitive positive definite
forms (a, b, c) = a x^2 + b xy + c y^2 with b^2 - 4ac = D, under composition. Each class has exactly one
reduced form, so a form is a unique encoding of its class. The prime forms of norm at most sqrt(|D|/3)
generate the group, because every class has a reduced form with a <= sqrt(|D|/3).

The quantum part finds the order r_i of each generator g_i by order finding, then solves the hidden subgroup
problem of f(x) = g_1^x_1 ... g_k^x_k on Z_r1 x ... x Z_rk. Fourier sampling gives uniform elements of the
dual of the relation subgroup. The classical part computes the lattice of relations from the samples with
integer linear algebra, checks every basis vector, and reads the group structure off the Smith normal form.

Each register holds a value below r_i in ceil(log2 r_i) qubits, and the Fourier transform of Z_r acts on the
first r basis states (qubit 0 is the least significant bit). The target register holds a code of the reduced
form. A real circuit holds the form itself and composes forms in polynomial time.
"""

import math
import random
from fractions import Fraction

from qsim import apply_oracle, apply_register_unitary, basis_state, fourier_matrix, marginal, padded, probabilities, registers, sample


# ---------------------------------------------------------------- binary quadratic forms


def xgcd(a: int, b: int) -> tuple[int, int, int]:
    """(g, u, v) with u a + v b = g = gcd(a, b) >= 0."""
    u0, v0, u1, v1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    if a < 0:
        a, u0, v0 = -a, -u0, -v0
    return a, u0, v0


def reduce_form(a: int, b: int, c: int) -> tuple[int, int, int]:
    """The reduced form equivalent to the positive definite form (a, b, c)."""
    D = b * b - 4 * a * c
    while True:
        k = (a - b) // (2 * a)  # move b into (-a, a]
        b += 2 * a * k
        c = (b * b - D) // (4 * a)
        if a > c:
            a, b, c = c, -b, a
            continue
        if a == c and b < 0:
            b = -b
        return a, b, c


def identity_form(D: int) -> tuple[int, int, int]:
    b = D % 2
    return 1, b, (b - D) // 4


def inverse(f: tuple) -> tuple[int, int, int]:
    a, b, c = f
    return reduce_form(a, -b, c)


def compose(f: tuple, g: tuple) -> tuple[int, int, int]:
    """Gauss composition of two primitive forms of the same discriminant, reduced (Dirichlet's method)."""
    a1, b1, c1 = f
    a2, b2, c2 = g
    D = b1 * b1 - 4 * a1 * c1
    beta = (b1 + b2) // 2
    e1, u1, v1 = xgcd(a1, a2)
    e, s, w = xgcd(e1, beta)  # e = s (u1 a1 + v1 a2) + w beta
    u, v = s * u1, s * v1
    a3 = a1 * a2 // (e * e)
    B = (u * a1 * b2 + v * a2 * b1 + w * (b1 * b2 + D) // 2) // e
    B %= 2 * a3
    return reduce_form(a3, B, (B * B - D) // (4 * a3))


def power(f: tuple, n: int) -> tuple[int, int, int]:
    D = f[1] * f[1] - 4 * f[0] * f[2]
    if n < 0:
        f, n = inverse(f), -n
    out = identity_form(D)
    while n:
        if n & 1:
            out = compose(out, f)
        f = compose(f, f)
        n >>= 1
    return out


def product(gens: list, x) -> tuple[int, int, int]:
    D = gens[0][1] ** 2 - 4 * gens[0][0] * gens[0][2]
    out = identity_form(D)
    for g, e in zip(gens, x):
        out = compose(out, power(g, e))
    return out


def is_prime(p: int) -> bool:
    return p >= 2 and all(p % d for d in range(2, math.isqrt(p) + 1))


def prime_form(D: int, p: int):
    """The reduced form (p, b, c) for a prime p with b^2 = D (mod 4p), or None if p is inert."""
    for b in range(D % 2, 2 * p + 1, 2):
        if (b * b - D) % (4 * p) == 0:
            return reduce_form(p, b, (b * b - D) // (4 * p))
    return None


# ---------------------------------------------------------------- references


def reduced_forms(D: int) -> list[tuple[int, int, int]]:
    """The reference: all reduced primitive forms of discriminant D < 0, by brute force."""
    out = []
    a = 1
    while 3 * a * a <= -D:
        for b in range(-a + 1, a + 1):
            if (b * b - D) % (4 * a) == 0:
                c = (b * b - D) // (4 * a)
                if c >= a and not (b < 0 and a == c) and math.gcd(math.gcd(a, abs(b)), c) == 1:
                    out.append((a, b, c))
        a += 1
    return out


def kronecker(D: int, n: int) -> int:
    """The Kronecker symbol (D / n) for n > 0."""
    r = 1
    while n % 2 == 0:
        n //= 2
        if D % 2 == 0:
            return 0
        if D % 8 in (3, 5):
            r = -r
    a = D % n
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                r = -r
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            r = -r
        a %= n
    return r if n == 1 else 0


def dirichlet_class_number(D: int) -> int:
    """The reference for a fundamental D < -4: h = -(1/|D|) sum_{a=1}^{|D|} (D/a) a."""
    s = -sum(kronecker(D, a) * a for a in range(1, -D))
    assert s % (-D) == 0
    return s // (-D)


def element_orders(D: int) -> list[int]:
    """The reference: the sorted orders of all classes, by repeated composition."""
    e = identity_form(D)
    out = []
    for f in reduced_forms(D):
        g, k = f, 1
        while g != e:
            g, k = compose(g, f), k + 1
        out.append(k)
    return sorted(out)


def orders_of_structure(ds: list[int]) -> list[int]:
    """The sorted orders of all elements of Z_d1 x ... x Z_dk."""
    out = [1]
    for d in ds:
        out = [math.lcm(o, d // math.gcd(d, t)) for o in out for t in range(d)]
    return sorted(out)


# ---------------------------------------------------------------- the quantum part


def bits(r: int) -> int:
    return max(1, (r - 1).bit_length())


def order_distribution(g: tuple, t: int, h_bound: int) -> dict:
    """The distribution of one run of order finding for the form g, with a t-qubit input register."""
    D = g[1] ** 2 - 4 * g[0] * g[2]
    q = 1 << t
    vals = [power(g, x) for x in range(q)]
    codes: dict = {}
    for v in vals:
        codes.setdefault(v, len(codes))
    rx, ry = registers(t, bits(h_bound))
    s = basis_state(t + bits(h_bound), 0)
    F = fourier_matrix(q)
    s = apply_register_unitary(s, F, rx)
    s = apply_oracle(s, [rx], ry, lambda x: codes[vals[x]])
    s = apply_register_unitary(s, F, rx)
    return {c: p for (c,), p in marginal(probabilities(s), [rx]).items()}


def find_order(g: tuple, rng: random.Random, t: int, h_bound: int) -> int:
    """Order finding: the lcm of the convergent denominators below 2^(t/2), until g^r is the identity."""
    D = g[1] ** 2 - 4 * g[0] * g[2]
    e = identity_form(D)
    if g == e:
        return 1
    dist = order_distribution(g, t, h_bound)
    r = 1
    while power(g, r) != e:
        c = sample(dist, rng)
        s = Fraction(c, 1 << t).limit_denominator(h_bound).denominator
        r = math.lcm(r, s)
    for p in range(2, r + 1):  # a bad sample can give a multiple of the order, so remove extra factors
        while r % p == 0 and power(g, r // p) == e:
            r //= p
    return r


def hsp_distribution(gens: list, orders: list[int]) -> dict:
    """The exact distribution of y from a state-vector simulation of lines L5 to L8."""
    sizes = [bits(r) for r in orders]
    domain = [()]
    for r in orders:
        domain = [x + (v,) for x in domain for v in range(r)]
    vals = {x: product(gens, x) for x in domain}
    codes: dict = {}
    for x in domain:
        codes.setdefault(vals[x], len(codes))
    tb = bits(len(codes))
    regs = registers(*sizes, tb)
    xr, tr = regs[:-1], regs[-1]
    s = basis_state(sum(sizes) + tb, 0)
    for r, reg in zip(orders, xr):
        s = apply_register_unitary(s, padded(fourier_matrix(r), 1 << len(reg)), reg)  # @line L5
    s = apply_oracle(s, xr, tr, lambda *x: codes[vals[x]] if all(v < r for v, r in zip(x, orders)) else 0)  # @line L6
    for r, reg in zip(orders, xr):
        s = apply_register_unitary(s, padded(fourier_matrix(r), 1 << len(reg)), reg)  # @line L7
    return marginal(probabilities(s), xr)  # @line L8 (the distribution of the measurement)


def dual_of_relations(gens: list, orders: list[int]) -> set:
    """The reference: the dual H^perp of the relation subgroup H of Z_r1 x ... x Z_rk, by brute force."""
    e = identity_form(gens[0][1] ** 2 - 4 * gens[0][0] * gens[0][2])
    domain = [()]
    for r in orders:
        domain = [x + (v,) for x in domain for v in range(r)]
    H = [x for x in domain if product(gens, x) == e]
    return {y for y in domain if all(sum(Fraction(a * b, r) for a, b, r in zip(x, y, orders)).denominator == 1 for x in H)}


# ---------------------------------------------------------------- integer linear algebra


def smith_form(A: list[list[int]]):
    """(d, W, Winv): U A W = diag(d) for some unimodular U, with W unimodular and Winv its inverse."""
    A = [row[:] for row in A]
    m, k = len(A), len(A[0])
    W = [[int(i == j) for j in range(k)] for i in range(k)]
    Wi = [[int(i == j) for j in range(k)] for i in range(k)]

    def col_add(j, t, c):  # column j += c * column t
        for row in A:
            row[j] += c * row[t]
        for row in W:
            row[j] += c * row[t]
        Wi[t] = [a - c * b for a, b in zip(Wi[t], Wi[j])]

    def col_swap(i, j):
        for M in (A, W):
            for row in M:
                row[i], row[j] = row[j], row[i]
        Wi[i], Wi[j] = Wi[j], Wi[i]

    d = []
    for t in range(min(m, k)):
        while True:
            piv = [(abs(A[i][j]), i, j) for i in range(t, m) for j in range(t, k) if A[i][j]]
            if not piv:
                return d + [0] * (k - len(d)), W, Wi
            _, i, j = min(piv)
            A[t], A[i] = A[i], A[t]
            col_swap(t, j)
            done = True
            for i in range(t + 1, m):
                q = A[i][t] // A[t][t]
                A[i] = [a - q * b for a, b in zip(A[i], A[t])]
                done &= A[i][t] == 0
            for j in range(t + 1, k):
                col_add(j, t, -(A[t][j] // A[t][t]))
                done &= A[t][j] == 0
            if not done:
                continue
            bad = [i for i in range(t + 1, m) for j in range(t + 1, k) if A[i][j] % A[t][t]]
            if bad:
                A[t] = [a + b for a, b in zip(A[t], A[bad[0]])]
                continue
            break
        if A[t][t] < 0:
            A[t] = [-a for a in A[t]]
        d.append(A[t][t])
    return d + [0] * (k - len(d)), W, Wi


def relation_lattice(Y: list, orders: list[int]) -> list[list[int]]:
    """Generators of L = {x in Z^k : sum_i x_i y_i / r_i is an integer for all y in Y}, by a kernel computation."""
    k = len(orders)
    M = math.lcm(*orders)
    rows = [[y[i] * (M // orders[i]) for i in range(k)] + [M * int(j == s) for j in range(len(Y))] for s, y in enumerate(Y)]
    if not rows:
        return [[int(i == j) for j in range(k)] for i in range(k)]
    d, W, _ = smith_form(rows)
    return [[W[i][j] for i in range(k)] for j in range(len(d)) if d[j] == 0]


# ---------------------------------------------------------------- the algorithm


def quantum_class_group(D: int, h_bound: int, rng: random.Random, max_samples: int = 100):
    """Return (invariants, generators, h, samples) for Cl(D) with D < 0 a discriminant.

    h_bound is an upper bound on the class number. It sets the size of the order finding register. A real
    run can use sqrt(|D|) ln|D|; the tests pass a smaller bound so that every simulation fits in 12 qubits.
    """
    bound = math.isqrt(-D // 3)
    gens = [f for p in range(2, bound + 1) if is_prime(p) and (f := prime_form(D, p)) is not None]  # @line L1
    if not gens:
        return [], [], 1, 0
    t = 2 * bits(h_bound) + 1
    orders = [find_order(g, rng, t, h_bound) for g in gens]  # @line L2
    gens, orders = [g for g, r in zip(gens, orders) if r > 1], [r for r in orders if r > 1]
    if not gens:
        return [], [], 1, 0
    e = identity_form(D)
    dist = hsp_distribution(gens, orders)
    Y = []  # @line L3
    for samples in range(1, max_samples + 1):  # @line L4
        Y.append(sample(dist, rng))  # @line L8
        L = relation_lattice(Y, orders)  # @line L9
        if all(product(gens, x) == e for x in L):  # @line L10
            break
    d, _, Wi = smith_form(L)  # @line L11
    inv = [(di, product(gens, Wi[i])) for i, di in enumerate(d) if di > 1]  # @line L12
    return [di for di, _ in inv], [g for _, g in inv], math.prod(di for di, _ in inv), samples  # @line L13
