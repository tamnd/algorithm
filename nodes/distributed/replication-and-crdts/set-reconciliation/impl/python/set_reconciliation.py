# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/set-reconciliation/. The authors are listed in prov/ACGS5S.jsonl.

"""Two ways to reconcile sets A (at Alice) and B (at Bob) of integers in [1, u).

1. Characteristic polynomial interpolation (Minsky, Trachtenberg and Zippel 2003).
   Alice sends chi_A(z) = prod_{x in A} (z - x) at m points and |A|. Bob
   divides by chi_B at the same points, fits the ratio P/Q with monic P, Q,
   checks it at extra points, and finds A \\ B and B \\ A as the roots of P and Q.
   Works whenever m >= |A xor B|; arithmetic is in GF(p), p = 2^61 - 1.

2. Invertible Bloom lookup table, the difference digest of Eppstein, Goodrich,
   Uyeda and Varghese (2011). Each side inserts its set into a table of cells
   (count, keySum, hashSum); Bob subtracts Alice's table from his own and peels
   the cells that hold one element. Succeeds with high probability when the
   table has somewhat more than 1.222 d cells for k = 3.
"""

import hashlib
import random
from math import comb, log2

P = (1 << 61) - 1


# ---------- polynomials over GF(P), lists of coefficients, lowest first ----------

def trim(a: list[int]) -> list[int]:
    while a and a[-1] == 0:
        a.pop()
    return a


def pmul(a: list[int], b: list[int]) -> list[int]:
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % P
    return out


def pdivmod(a: list[int], b: list[int]) -> tuple[list[int], list[int]]:
    a = trim(a[:])
    inv = pow(b[-1], P - 2, P)
    q = [0] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b) and a:
        c = a[-1] * inv % P
        s = len(a) - len(b)
        q[s] = c
        for i, y in enumerate(b):
            a[s + i] = (a[s + i] - c * y) % P
        trim(a)
    return trim(q), a


def monic(a: list[int]) -> list[int]:
    inv = pow(a[-1], P - 2, P)
    return [x * inv % P for x in a]


def pgcd(a: list[int], b: list[int]) -> list[int]:
    a, b = trim(a[:]), trim(b[:])
    while b:
        a, b = b, pdivmod(a, b)[1]
    return monic(a)


def peval(a: list[int], z: int) -> int:
    r = 0
    for c in reversed(a):
        r = (r * z + c) % P
    return r


def ppowmod(base: list[int], e: int, mod: list[int]) -> list[int]:
    result, base = [1], pdivmod(base, mod)[1]
    while e:
        if e & 1:
            result = pdivmod(pmul(result, base), mod)[1]
        base = pdivmod(pmul(base, base), mod)[1]
        e >>= 1
    return result


def roots(f: list[int], rng: random.Random) -> list[int] | None:
    """The roots of a monic f that splits into distinct linear factors over GF(P)
    (Cantor-Zassenhaus with random shifts). None if f does not split so."""
    f = monic(trim(f[:]))
    if len(f) == 1:
        return []
    # f splits into distinct linear factors iff f divides z^P - z
    zp = ppowmod([0, 1], P, f)
    zp += [0] * (2 - len(zp))
    zp[1] = (zp[1] - 1) % P
    if pdivmod(zp, f)[1]:  # (z^P - z) mod f
        return None
    out: list[int] = []
    stack = [f]
    while stack:
        g = stack.pop()
        if len(g) == 2:
            out.append((-g[0]) % P)
            continue
        while True:  # split g by gcd(g, (z + a)^((P-1)/2) - 1) for a random a
            h = ppowmod([rng.randrange(P), 1], (P - 1) // 2, g) or [0]
            h[0] = (h[0] - 1) % P
            h = trim(h)
            d = pgcd(g, h) if h else g
            if 1 < len(d) < len(g):
                stack += [d, pdivmod(g, d)[0]]
                break
    return sorted(out)


def solve_mod(rows: list[list[int]], rhs: list[int], ncols: int) -> list[int] | None:
    """One solution of a linear system over GF(P), free variables set to 0."""
    m = [r[:] + [b] for r, b in zip(rows, rhs)]
    piv_cols: list[int] = []
    r = 0
    for c in range(ncols):
        pr = next((i for i in range(r, len(m)) if m[i][c]), None)
        if pr is None:
            continue
        m[r], m[pr] = m[pr], m[r]
        inv = pow(m[r][c], P - 2, P)
        m[r] = [x * inv % P for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c]:
                f = m[i][c]
                m[i] = [(x - f * y) % P for x, y in zip(m[i], m[r])]
        piv_cols.append(c)
        r += 1
    if any(row[-1] for row in m[r:]):
        return None  # inconsistent
    x = [0] * ncols
    for i, c in enumerate(piv_cols):
        x[c] = m[i][-1]
    return x


# ---------- characteristic polynomial interpolation ----------

def points(m: int) -> list[int]:
    return [P - 1 - i for i in range(m)]  # never an element: elements are below u << P


def cpi_sketch(s: set[int], m: int, extra: int = 2) -> dict:
    """Alice's message: chi_S at m + extra points, and |S|."""
    zs = points(m + extra)
    vals = []
    for z in zs:
        v = 1
        for x in s:
            v = v * (z - x) % P
        vals.append(v)
    return {"m": m, "size": len(s), "vals": vals}


def cpi_reconcile(msg: dict, b: set[int], seed: int = 0) -> tuple[set[int], set[int]] | None:
    """Bob's side. Returns (A minus B, B minus A), or None if m was too small."""
    delta = msg["size"] - len(b)
    m = msg["m"] - (msg["m"] - delta) % 2  # |A xor B| has the parity of delta
    if m < abs(delta):
        return None
    da, db = (m + delta) // 2, (m - delta) // 2  # degree bounds of P = chi_{A-B}, Q = chi_{B-A}
    zs = points(len(msg["vals"]))
    ratio = []
    for z, va in zip(zs, msg["vals"]):
        vb = 1
        for x in b:
            vb = vb * (z - x) % P
        ratio.append(va * pow(vb, P - 2, P) % P)
    rows, rhs = [], []
    for z, f in zip(zs[:m], ratio[:m]):
        # sum_j p_j z^j - f sum_j q_j z^j = f z^db - z^da
        rows.append([pow(z, j, P) for j in range(da)] + [(-f * pow(z, j, P)) % P for j in range(db)])
        rhs.append((f * pow(z, db, P) - pow(z, da, P)) % P)
    sol = solve_mod(rows, rhs, da + db)
    if sol is None:
        return None
    pp = sol[:da] + [1]
    qq = sol[da:] + [1]
    g = pgcd(pp, qq)
    pp, qq = pdivmod(pp, g)[0], pdivmod(qq, g)[0]
    for z, f in zip(zs[m:], ratio[m:]):  # points not used by the system
        if peval(pp, z) != f * peval(qq, z) % P:
            return None
    rng = random.Random(seed)
    ra, rb = roots(pp, rng), roots(qq, rng)
    if ra is None or rb is None:
        return None
    return set(ra), set(rb)


# ---------- invertible Bloom lookup table ----------

def _h(x: int, salt: int) -> int:
    return int.from_bytes(hashlib.blake2b(x.to_bytes(8, "big"), digest_size=8,
                                          salt=salt.to_bytes(16, "big")).digest(), "big")


class IBLT:
    """k = 3 hash functions, each into its own third of the cells."""

    K = 3

    def __init__(self, cells: int) -> None:
        self.sub = max(1, -(-cells // self.K))
        self.n = self.sub * self.K
        self.count = [0] * self.n
        self.key = [0] * self.n
        self.chk = [0] * self.n

    def cells_of(self, x: int) -> list[int]:
        return [i * self.sub + _h(x, i) % self.sub for i in range(self.K)]

    def update(self, x: int, sign: int) -> None:
        c = _h(x, 99)
        for i in self.cells_of(x):
            self.count[i] += sign
            self.key[i] ^= x
            self.chk[i] ^= c

    @classmethod
    def of(cls, s: set[int], cells: int) -> "IBLT":
        t = cls(cells)
        for x in s:
            t.update(x, 1)
        return t

    def subtract(self, other: "IBLT") -> "IBLT":
        t = IBLT(self.n)
        t.count = [a - b for a, b in zip(self.count, other.count)]
        t.key = [a ^ b for a, b in zip(self.key, other.key)]
        t.chk = [a ^ b for a, b in zip(self.chk, other.chk)]
        return t

    def pure(self, i: int) -> bool:
        return self.count[i] in (1, -1) and self.chk[i] == _h(self.key[i], 99)

    def peel(self) -> tuple[set[int], set[int]] | None:
        """List the contents of a difference table: (elements with count +1,
        elements with count -1). None if peeling gets stuck."""
        plus: set[int] = set()
        minus: set[int] = set()
        queue = [i for i in range(self.n) if self.pure(i)]
        while queue:
            i = queue.pop()
            if not self.pure(i):
                continue
            x, sign = self.key[i], self.count[i]
            (plus if sign == 1 else minus).add(x)
            for j in self.cells_of(x):
                self.count[j] -= sign
                self.key[j] ^= x
                self.chk[j] ^= _h(x, 99)
                if self.pure(j):
                    queue.append(j)
        if any(self.count) or any(self.key) or any(self.chk):
            return None
        return plus, minus


def iblt_reconcile(a: set[int], b: set[int], cells: int) -> tuple[set[int], set[int]] | None:
    """Alice sends IBLT(A); Bob subtracts IBLT(B) and peels."""
    return IBLT.of(a, cells).subtract(IBLT.of(b, cells)).peel()


# ---------- bounds and helpers ----------

def lower_bound_bits(u: int, d: int) -> float:
    """log2 of the number of sets within distance d of a given set, the bits that
    any one-way protocol must send in the worst case."""
    return log2(sum(comb(u, i) for i in range(d + 1)))


def random_pair(rng: random.Random, n: int, d: int, u: int = 1 << 32) -> tuple[set[int], set[int]]:
    """Two sets that share n - d elements; d elements are in exactly one of them."""
    xs = rng.sample(range(1, u), n)
    common, rest = xs[:n - d], xs[n - d:]
    k = rng.randint(0, d)
    a = set(common) | set(rest[:k])
    b = set(common) | set(rest[k:d])
    return a, b
