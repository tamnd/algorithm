# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alphatensor/. The authors are listed in prov/1MB9PX.jsonl.

"""TensorGame, the single-player game that AlphaTensor plays, with exact checking.

The state is a residual tensor S, starting at the matrix multiplication tensor
<n, m, p>. A move picks factors u, v, w with entries in a small set F and
replaces S by S - u (x) v (x) w. The game ends when S = 0, after t moves,
which gives a bilinear algorithm with t multiplications, or when the move
limit is reached. AlphaTensor chooses moves by Monte Carlo tree search
guided by a neural network; here the policy is any function passed in. The
module also has the verification of a decomposition, the bilinear algorithm
it defines, and a flip graph random walk, which is a different search method
(Kauers and Moosbauer) used here to find a rank 7 scheme over GF(2) in
milliseconds.

Index conventions: u is an n x m matrix of coefficients of A, v an m x p
matrix of coefficients of B, and w an n x p matrix that says how much of the
product goes into each entry of C. The tensor entry at
((i, j), (j, k), (i, k)) is 1 and all others are 0.
"""

import random
from fractions import Fraction
from typing import Callable, Optional

Mat = list[list[int]]
Factor = tuple[Mat, Mat, Mat]
Tensor = list[list[list[int]]]
Policy = Callable[[Tensor, int], Factor]

DEFAULT_F = (-2, -1, 0, 1, 2)


def matmul_tensor(n: int, m: int, p: int) -> Tensor:
    """The tensor <n, m, p> as an (nm) x (mp) x (np) array of 0s and 1s."""
    t = [[[0] * (n * p) for _ in range(m * p)] for _ in range(n * m)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                t[i * m + j][j * p + k][i * p + k] = 1
    return t


def _flat(a: Mat) -> list[int]:
    return [x for row in a for x in row]


def _norm(x: int, mod: Optional[int]) -> int:
    return x % mod if mod is not None else x


def _is_zero(s: Tensor) -> bool:
    return all(x == 0 for plane in s for row in plane for x in row)


def _slice_rank(mat: list[list[int]], mod: Optional[int]) -> int:
    rows = [[Fraction(x) for x in r] for r in mat] if mod is None else [[x % mod for x in r] for r in mat]
    rank, cols = 0, len(rows[0]) if rows else 0
    for c in range(cols):
        piv = next((r for r in range(rank, len(rows)) if rows[r][c] != 0), None)
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        inv = 1 / rows[rank][c] if mod is None else pow(rows[rank][c], -1, mod)
        for r in range(len(rows)):
            if r != rank and rows[r][c] != 0:
                f = rows[r][c] * inv
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[rank])]
                if mod is not None:
                    rows[r] = [a % mod for a in rows[r]]
        rank += 1
    return rank


def rank_upper_bound(s: Tensor, mod: Optional[int] = None) -> int:
    """gamma(S): the sum of the ranks of the slices S[a], an upper bound on the tensor rank of S."""
    return sum(_slice_rank(plane, mod) for plane in s)


def alphatensor(
    target: Tensor,
    policy: Policy,
    limit: int,
    mod: Optional[int] = None,
    coeffs: tuple[int, ...] = DEFAULT_F,
) -> tuple[Optional[list[Factor]], int]:
    """Play TensorGame on target with the given policy and at most limit moves.

    Returns (factors, reward). If the residual reaches 0 after t moves,
    factors is the list of t moves, a rank t decomposition of target, and the
    reward is -t. Otherwise factors is None and the reward is
    -limit - rank_upper_bound(residual). With mod set, arithmetic is in Z/mod.
    Each factor entry must lie in coeffs. Cost: limit moves, each O(d) for a
    tensor with d entries, plus the calls to policy.
    """
    s = [[[_norm(x, mod) for x in row] for row in plane] for plane in target]  # @line L1
    t = 0
    factors: list[Factor] = []
    while not _is_zero(s) and t < limit:  # @line L2
        u, v, w = policy(s, t)  # @line L3
        fu, fv, fw = _flat(u), _flat(v), _flat(w)
        if len(fu) != len(s) or len(fv) != len(s[0]) or len(fw) != len(s[0][0]):
            raise ValueError("factor shapes do not match the tensor")
        if any(x not in coeffs for x in fu + fv + fw):
            raise ValueError("factor entry outside the coefficient set")
        for a, x in enumerate(fu):  # @line L4
            if x:
                for b, y in enumerate(fv):
                    if y:
                        row = s[a][b]
                        for c, z in enumerate(fw):
                            if z:
                                row[c] = _norm(row[c] - x * y * z, mod)
        factors.append((u, v, w))
        t += 1
    if _is_zero(s):  # @line L5
        return factors, -t
    return None, -t - rank_upper_bound(s, mod)  # @line L6


def replay(factors: list[Factor]) -> Policy:
    """A policy that plays a fixed list of moves, as in a demonstration game."""
    return lambda state, t: factors[t]


def verify(factors: list[Factor], n: int, m: int, p: int, mod: Optional[int] = None) -> bool:
    """True when sum of u (x) v (x) w equals <n, m, p>, over Z or over Z/mod."""
    acc = [[[0] * (n * p) for _ in range(m * p)] for _ in range(n * m)]
    for u, v, w in factors:
        fu, fv, fw = _flat(u), _flat(v), _flat(w)
        for a, x in enumerate(fu):
            for b, y in enumerate(fv):
                for c, z in enumerate(fw):
                    acc[a][b][c] += x * y * z
    t = matmul_tensor(n, m, p)
    return all(
        _norm(acc[a][b][c] - t[a][b][c], mod) == 0
        for a in range(n * m)
        for b in range(m * p)
        for c in range(n * p)
    )


STRASSEN: list[Factor] = [
    ([[1, 0], [0, 1]], [[1, 0], [0, 1]], [[1, 0], [0, 1]]),
    ([[0, 0], [1, 1]], [[1, 0], [0, 0]], [[0, 0], [1, -1]]),
    ([[1, 0], [0, 0]], [[0, 1], [0, -1]], [[0, 1], [0, 1]]),
    ([[0, 0], [0, 1]], [[-1, 0], [1, 0]], [[1, 0], [1, 0]]),
    ([[1, 1], [0, 0]], [[0, 0], [0, 1]], [[-1, 1], [0, 0]]),
    ([[-1, 0], [1, 0]], [[1, 1], [0, 0]], [[0, 0], [0, 1]]),
    ([[0, 1], [0, -1]], [[0, 0], [1, 1]], [[1, 0], [0, 0]]),
]


def _schoolbook(a: Mat, b: Mat, rows: int, inner: int, cols: int, mod: Optional[int]) -> Mat:
    c = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for k in range(inner):
            x = a[i][k]
            if x:
                for j in range(cols):
                    c[i][j] += x * b[k][j]
    return [[_norm(x, mod) for x in row] for row in c]


def multiply_with(
    factors: list[Factor],
    shape: tuple[int, int, int],
    a: Mat,
    b: Mat,
    cols: int,
    mod: Optional[int] = None,
    cutoff: int = 1,
) -> Mat:
    """Multiply a (r x s) by b (s x cols) with the bilinear scheme for <n, m, p>, recursively.

    The scheme must be valid over the ring used: a scheme found over GF(2)
    is only valid with mod = 2 (or another power of 2 in special cases).
    Sides are padded with zeros to multiples of the block shape at each
    level. When a side is at most cutoff the schoolbook loop is used.
    Recursion depth is O(log of the largest side).
    """
    n, m, p = shape
    r, s = len(a), len(b)
    if min(r, s, cols) <= cutoff or max(n, m, p) == 1:
        return _schoolbook(a, b, r, s, cols, mod)
    rr, ss, cc = -(-r // n), -(-s // m), -(-cols // p)  # block sizes; at least one side shrinks

    def block(mat: Mat, bi: int, bj: int, h: int, wd: int) -> Mat:
        return [
            [mat[bi * h + x][bj * wd + y] if bi * h + x < len(mat) and bj * wd + y < len(mat[0]) else 0 for y in range(wd)]
            for x in range(h)
        ]

    ab = [[block(a, i, j, rr, ss) for j in range(m)] for i in range(n)]
    bb = [[block(b, j, k, ss, cc) for k in range(p)] for j in range(m)]
    cb = [[[[0] * cc for _ in range(rr)] for _ in range(p)] for _ in range(n)]
    for u, v, w in factors:
        left = [[sum(u[i][j] * ab[i][j][x][y] for i in range(n) for j in range(m)) for y in range(ss)] for x in range(rr)]
        right = [[sum(v[j][k] * bb[j][k][x][y] for j in range(m) for k in range(p)) for y in range(cc)] for x in range(ss)]
        prod = multiply_with(factors, shape, left, right, cc, mod, cutoff)
        for i in range(n):
            for k in range(p):
                if w[i][k]:
                    blk = cb[i][k]
                    for x in range(rr):
                        for y in range(cc):
                            blk[x][y] += w[i][k] * prod[x][y]
    out = [[0] * cols for _ in range(r)]
    for i in range(n):
        for k in range(p):
            for x in range(rr):
                for y in range(cc):
                    gi, gj = i * rr + x, k * cc + y
                    if gi < r and gj < cols:
                        out[gi][gj] = _norm(cb[i][k][x][y], mod)
    return out


def _bits_to_mat(bits: int, rows: int, cols: int) -> Mat:
    return [[(bits >> (x * cols + y)) & 1 for y in range(cols)] for x in range(rows)]


def flip_graph_search(n: int, m: int, p: int, target_rank: int, seed: int, max_steps: int = 100000) -> Optional[list[Factor]]:
    """Random walk on the flip graph over GF(2), from the standard nmp-term scheme.

    A flip takes two terms that share a factor, a (x) b (x) c + a (x) b' (x) c',
    and rewrites them as a (x) (b + b') (x) c + a (x) b' (x) (c + c'), which has
    the same sum over GF(2). A reduction merges two terms that share two
    factors. Returns a scheme valid over GF(2) with at most target_rank terms,
    or None if max_steps flips do not reach it.
    """
    rng = random.Random(seed)
    terms = [(1 << (i * m + j), 1 << (j * p + k), 1 << (i * p + k)) for i in range(n) for j in range(m) for k in range(p)]

    def reduce(ts: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
        ts = [t for t in ts if all(t)]
        merged = True
        while merged:
            merged = False
            for i in range(len(ts)):
                for j in range(i + 1, len(ts)):
                    for pos in range(3):
                        o1, o2 = [q for q in range(3) if q != pos]
                        if ts[i][o1] == ts[j][o1] and ts[i][o2] == ts[j][o2]:
                            new = list(ts[i])
                            new[pos] ^= ts[j][pos]
                            ts = [ts[k] for k in range(len(ts)) if k not in (i, j)]
                            if new[pos]:
                                ts.append(tuple(new))  # type: ignore[arg-type]
                            merged = True
                            break
                    if merged:
                        break
                if merged:
                    break
        return ts

    terms = reduce(terms)
    for _ in range(max_steps):
        if len(terms) <= target_rank:
            break
        pairs = []
        for pos in range(3):
            groups: dict[int, list[int]] = {}
            for idx, t in enumerate(terms):
                groups.setdefault(t[pos], []).append(idx)
            pairs += [(pos, i, j) for g in groups.values() for i in g for j in g if i != j]
        if not pairs:
            return None
        pos, i, j = rng.choice(pairs)
        o1, o2 = [q for q in range(3) if q != pos]
        s, t = list(terms[i]), list(terms[j])
        s[o1] ^= t[o1]
        t[o2] ^= s[o2]
        terms[i], terms[j] = tuple(s), tuple(t)  # type: ignore[assignment]
        terms = reduce(terms)
    if len(terms) > target_rank:
        return None
    return [(_bits_to_mat(a, n, m), _bits_to_mat(b, m, p), _bits_to_mat(c, n, p)) for a, b, c in terms]
