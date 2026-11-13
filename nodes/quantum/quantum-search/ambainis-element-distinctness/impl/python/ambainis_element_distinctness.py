# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ambainis-element-distinctness/. The authors are listed in prov/VT4428.jsonl.
"""Ambainis's quantum walk for element k-distinctness (Algorithm 2 of the paper), simulated.

The input is a list x of N values. A basis state is |S, y>: S is a set of r indices and y is
an index outside S. The data register holds the values x_i for i in S; it is a function of S,
so the simulation does not store it, but it counts every query that writes or erases it.

Two simulations are given.
  run_full: the whole state vector on N + ceil(log2 N) qubits (qsim). Qubit i (i < N) is 1 if
    i is in S; the qubits from N upward hold y, least significant bit first.
  run_reduced: the (2k+1)-dimensional subspace of Lemma 1 of the paper. It needs the promise
    that there is at most one set of k equal values, and it works for large N.
"""

import math
import random
from functools import lru_cache

from qsim import apply_diagonal, apply_permutation, probabilities


def t2_steps(r: int, k: int) -> int:
    """t2 = ceil(pi sqrt(r) / (3 sqrt(k))), the walk steps between two phase flips."""
    return math.ceil(math.pi * math.sqrt(r) / (3 * math.sqrt(k)))


def default_r(n: int, k: int) -> int:
    """r = floor(n^(k/(k+1))) in exact integers, kept in the range k <= r <= n - k - 1."""
    r = int(n ** (k / (k + 1)))
    while (r + 1) ** (k + 1) <= n**k:
        r += 1
    while r ** (k + 1) > n**k:
        r -= 1
    return max(k, min(n - k - 1, r))


def queries(r: int, t1: int, t2: int) -> int:
    """r queries for the setup and 2 queries for each walk step."""
    return r + 2 * t1 * t2


def has_k_collision(x: list, sub, k: int) -> bool:
    counts = {}
    for i in sub:
        counts[x[i]] = counts.get(x[i], 0) + 1
        if counts[x[i]] >= k:
            return True
    return False


def collision_sets(x: list, k: int) -> list[list[int]]:
    """Brute force: for each value that occurs at least k times, its list of positions."""
    pos = {}
    for i, v in enumerate(x):
        pos.setdefault(v, []).append(i)
    return [p for p in pos.values() if len(p) >= k]


# ---------- the full state vector ----------


def _members(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if mask >> i & 1]


def _reflect(state: list, n: int, size: int, inside: bool) -> list:
    """For each S with |S| = size, apply 2|u><u| - I to y, u uniform on S (inside) or on [n] - S."""
    out = list(state)
    for mask in range(1 << n):
        if bin(mask).count("1") != size:
            continue
        ys = [y for y in range(n) if bool(mask >> y & 1) == inside]
        idx = [mask | (y << n) for y in ys]
        mean = sum(state[i] for i in idx) / len(idx)
        for i in idx:
            out[i] = 2 * mean - state[i]
    return out


def _toggle_perm(n: int, ny: int) -> list[int]:
    """|S, y> -> |S xor {y}, y>: adds y to S or removes it. Identity when y >= n."""
    perm = []
    for idx in range(1 << (n + ny)):
        y = idx >> n
        perm.append(idx ^ (1 << y) if y < n else idx)
    return perm


def run_full(x: list, k: int, r: int, t1: int, t2: int):
    """Return (state, number of qubits for S, queries). The state lives on n + ny qubits."""
    n = len(x)
    ny = max(1, (n - 1).bit_length())
    dim = 1 << (n + ny)
    total = math.comb(n, r) * (n - r)
    state = [0j] * dim
    for mask in range(1 << n):  # @line L1
        if bin(mask).count("1") == r:
            for y in range(n):
                if not mask >> y & 1:
                    state[mask | (y << n)] = complex(1 / math.sqrt(total))
    # query x_i for every i in S: r queries
    q = r  # @line L2
    flip = [1.0] * dim
    for idx in range(dim):
        mask = idx & ((1 << n) - 1)
        if bin(mask).count("1") == r and has_k_collision(x, _members(mask, n), k):
            flip[idx] = -1.0
    perm = _toggle_perm(n, ny)
    for _ in range(t1):  # @line L3
        # the phase flip makes no query: the values of S are stored
        state = apply_diagonal(state, flip)  # @line L4
        for _ in range(t2):  # @line L5
            state = _reflect(state, n, r, inside=False)  # @line L6
            # add y to S, then query x_y into the new slot
            state = apply_permutation(state, perm)  # @line L7
            q += 1
            state = _reflect(state, n, r + 1, inside=True)  # @line L8
            # erase the slot of y with a query, then remove y from S
            q += 1  # @line L9
            state = apply_permutation(state, perm)
    return state, n, q


def success_full(x: list, k: int, r: int, t1: int, t2: int) -> float:
    state, n, _ = run_full(x, k, r, t1, t2)
    p = probabilities(state)
    low = (1 << n) - 1
    return sum(pi for idx, pi in enumerate(p) if pi and has_k_collision(x, _members(idx & low, n), k))


def measure_full(x: list, k: int, r: int, t1: int, t2: int, rng: random.Random):
    """Run, measure S, and check it classically. Returns (a k-collision or None, queries)."""
    state, n, q = run_full(x, k, r, t1, t2)
    p = probabilities(state)
    idx = rng.choices(range(len(p)), weights=p)[0]  # @line L10
    s = _members(idx & ((1 << n) - 1), n)
    pos = {}
    for i in s:
        pos.setdefault(x[i], []).append(i)
        if len(pos[x[i]]) == k:
            return pos[x[i]], q
    return None, q  # @line L11


# ---------- the (2k+1)-dimensional subspace ----------


def type_counts(n: int, k: int, r: int) -> dict:
    """Number of basis states |S, y> of each type (j, l) in H (|S| = r, y not in S)."""
    c = {}
    for j in range(k + 1):
        base = math.comb(k, j) * math.comb(n - k, r - j)
        c[(j, 0)] = base * (n - k - r + j)
        if j < k:
            c[(j, 1)] = base * (k - j)
    return c


def _block(v0: float, v1: float, a0: int, a1: int):
    """2|u><u| - I restricted to span(uniform on a0 points, uniform on a1 points)."""
    m = a0 + a1
    g = 2 * math.sqrt(a0 * a1) / m
    return (2 * a0 / m - 1) * v0 + g * v1, g * v0 + (2 * a1 / m - 1) * v1


def reduced_step(v: dict, n: int, k: int, r: int) -> dict:
    """One walk step (steps 1 to 6 of Algorithm 1 of the paper) on the type amplitudes."""
    w = {}
    for j in range(k + 1):  # diffuse y over [n] - S: k - j points of K, n - r - k + j others
        if j == k:
            w[(k, 0)] = v[(k, 0)]
        else:
            w[(j, 0)], w[(j, 1)] = _block(v[(j, 0)], v[(j, 1)], n - r - k + j, k - j)
    h = {}  # add y to S: (j, 0) -> (j, 0), (j, 1) -> (j + 1, 1)
    for (j, l), a in w.items():
        h[(j + l, l)] = a
    for j in range(k + 1):  # diffuse y over S: j points of K, r + 1 - j others
        if j == 0:
            continue
        h[(j, 0)], h[(j, 1)] = _block(h[(j, 0)], h[(j, 1)], r + 1 - j, j)
    out = {}  # remove y from S: (j, 0) -> (j, 0), (j, 1) -> (j - 1, 1)
    for (j, l), a in h.items():
        out[(j - l, l)] = a
    return out


def start_vector(n: int, k: int, r: int) -> dict:
    c = type_counts(n, k, r)
    total = math.comb(n, r) * (n - r)
    return {t: math.sqrt(m / total) for t, m in c.items()}


def run_reduced(n: int, k: int, r: int, t1: int, t2: int) -> dict:
    """Type amplitudes after Algorithm 2, for an input with exactly one set of k equal values."""
    if not k <= r <= n - k - 1:
        raise ValueError("need k <= r <= n - k - 1")
    v = start_vector(n, k, r)
    for _ in range(t1):
        v[(k, 0)] = -v[(k, 0)]
        for _ in range(t2):
            v = reduced_step(v, n, k, r)
    return v


def success_reduced(n: int, k: int, r: int, t1: int, t2: int) -> float:
    """The probability that the measured S contains the k-collision."""
    return run_reduced(n, k, r, t1, t2)[(k, 0)] ** 2


@lru_cache(maxsize=None)
def best_t1(n: int, k: int, r: int) -> int:
    """The t1 in 1 .. ceil(1.5 / alpha) that maximizes the success probability under the promise.

    alpha = <psi_good|psi_start>. Lemma 3 of the paper says that some t1 = O(1 / alpha) works.
    The choice depends on n, k and r only, not on the input, so it is classical preprocessing.
    """
    t2 = t2_steps(r, k)
    alpha = math.sqrt(math.comb(n - k, r - k) / math.comb(n, r))
    v = start_vector(n, k, r)
    best, arg = -1.0, 0
    for t in range(1, math.ceil(1.5 / alpha) + 1):
        v[(k, 0)] = -v[(k, 0)]
        for _ in range(t2):
            v = reduced_step(v, n, k, r)
        if v[(k, 0)] ** 2 > best:
            best, arg = v[(k, 0)] ** 2, t
    return arg


def k_distinctness(x: list, k: int, rng: random.Random, r=None):
    """Return (a k-collision or None, queries) under the promise of at most one k-collision.

    The state is taken from the reduced model; S is then drawn uniformly inside its type.
    """
    n = len(x)
    sets = collision_sets(x, k)
    if len(sets) > 1 or any(len(p) > k for p in sets):
        raise ValueError("Algorithm 2 needs at most one set of k equal values")
    r = default_r(n, k) if r is None else r
    t1, t2 = best_t1(n, k, r), t2_steps(r, k)
    q = queries(r, t1, t2)
    if not sets:  # the phase flip never acts; any measured S has no k-collision
        return None, q
    p = success_reduced(n, k, r, t1, t2)
    if rng.random() < p:
        return sorted(sets[0]), q
    return None, q
