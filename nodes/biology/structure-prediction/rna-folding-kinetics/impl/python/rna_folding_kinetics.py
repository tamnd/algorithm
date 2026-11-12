# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rna-folding-kinetics/. The authors are listed in prov/ZN8CDJ.jsonl.
"""RNA folding kinetics on the space of secondary structures.

The model:
  - allowed pairs AU, UA, GC, CG, GU, UG; at least m = 3 bases inside each pair; no pseudoknots;
  - integer energy E(P) = a * |P| - b * (number of stacked pairs), a small stand-in for the
    nearest-neighbor model (a pair costs entropy, a stack of two pairs gains energy);
  - moves add or remove one base pair (the move set of Kinfold without shift moves);
  - Metropolis rates k(P -> Q) = min(1, z ** (E(Q) - E(P))), with z = exp(-1/RT) in (0, 1).

The chain is a continuous-time Markov chain. Its stationary distribution is the Boltzmann
distribution pi(P) = z ** E(P) / Z, because the move set is symmetric and the rates satisfy
detailed balance. Exact computations use Fraction; the simulation uses floats.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from fractions import Fraction

PAIRS = frozenset({("A", "U"), ("U", "A"), ("G", "C"), ("C", "G"), ("G", "U"), ("U", "G")})


@dataclass(frozen=True)
class Model:
    m: int = 3  # hairpin minimum
    a: int = 1  # cost of each pair
    b: int = 3  # gain of each stack of two pairs


Structure = frozenset  # a set of pairs (i, j), 0-based, i < j


def energy(structure: Structure, model: Model = Model()) -> int:
    stacks = sum(1 for (i, j) in structure if (i + 1, j - 1) in structure)
    return model.a * len(structure) - model.b * stacks


def _partner(n: int, structure: Structure) -> list[int]:
    p = [-1] * n
    for i, j in structure:
        p[i], p[j] = j, i
    return p


def addable_pairs(s: str, structure: Structure, model: Model = Model()) -> list[tuple[int, int]]:
    """Pairs (i, j) that can be added to the structure without a shared base or a crossing."""
    n = len(s)
    p = _partner(n, structure)
    out = []
    for i in range(n):
        if p[i] != -1:
            continue
        # j must be in the same loop as i: walk right from i and jump over the helices inside.
        j = i + 1
        while j < n:
            if p[j] == -1:
                if j - i - 1 >= model.m and (s[i], s[j]) in PAIRS:
                    out.append((i, j))
                j += 1
            elif p[j] > j:  # opening base of a helix inside the same loop: jump over it
                j = p[j] + 1
            else:  # closing base of a pair that encloses i: the loop ends
                break
    return out


def neighbors(s: str, structure: Structure, model: Model = Model()) -> list[Structure]:
    """The move set: remove one pair, or add one pair."""
    out = [structure - {pr} for pr in sorted(structure)]
    out += [structure | {pr} for pr in addable_pairs(s, structure, model)]
    return out


def all_structures(s: str, model: Model = Model()) -> list[Structure]:
    """All secondary structures, found by a search over the move graph from the open chain."""
    start: Structure = frozenset()
    seen = {start}
    order = [start]
    stack = [start]
    while stack:
        cur = stack.pop()
        for nxt in neighbors(s, cur, model):
            if nxt not in seen:
                seen.add(nxt)
                order.append(nxt)
                stack.append(nxt)
    order.sort(key=lambda st: (len(st), sorted(st)))
    return order


def metropolis_rate(e_from: int, e_to: int, z: Fraction) -> Fraction:
    d = e_to - e_from
    return Fraction(1) if d <= 0 else z ** d


def rate_matrix(s: str, z: Fraction, model: Model = Model()):
    """States, their energies, and the rates as a dict {(x, y): k} over state indices."""
    states = all_structures(s, model)
    index = {st: x for x, st in enumerate(states)}
    energies = [energy(st, model) for st in states]
    rates = {}
    for x, st in enumerate(states):
        for nxt in neighbors(s, st, model):
            y = index[nxt]
            rates[(x, y)] = metropolis_rate(energies[x], energies[y], z)
    return states, energies, rates


def solve_exact(a: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    """Gaussian elimination over the rationals for a square nonsingular system."""
    n = len(a)
    mat = [row[:] + [rhs[r]] for r, row in enumerate(a)]
    for col in range(n):
        piv = next(r for r in range(col, n) if mat[r][col] != 0)
        mat[col], mat[piv] = mat[piv], mat[col]
        pv = mat[col][col]
        mat[col] = [v / pv for v in mat[col]]
        nz = [c for c in range(col, n + 1) if mat[col][c] != 0]  # the rows are sparse
        for r in range(n):
            if r != col and mat[r][col] != 0:
                f = mat[r][col]
                row = mat[r]
                for c in nz:
                    row[c] -= f * mat[col][c]
    return [mat[r][n] for r in range(n)]


def stationary_distribution(n_states: int, rates: dict) -> list[Fraction]:
    """Solve pi Q = 0 with sum(pi) = 1 for the generator Q of the chain."""
    out_rate = [Fraction(0)] * n_states
    for (x, _), k in rates.items():
        out_rate[x] += k
    # Equations: for each y, sum_x pi_x Q[x][y] = 0; replace the last one by sum pi = 1.
    a = [[Fraction(0)] * n_states for _ in range(n_states)]
    for (x, y), k in rates.items():
        a[y][x] += k
    for y in range(n_states):
        a[y][y] -= out_rate[y]
    a[-1] = [Fraction(1)] * n_states
    rhs = [Fraction(0)] * (n_states - 1) + [Fraction(1)]
    return solve_exact(a, rhs)


def boltzmann(energies: list[int], z: Fraction) -> list[Fraction]:
    w = [z ** e for e in energies]
    total = sum(w)
    return [x / total for x in w]


def mean_first_passage(n_states: int, rates: dict, target: int) -> list[Fraction]:
    """Exact expected time to reach the target from each state: (sum_y k_xy) tau_x - sum_y k_xy tau_y = 1."""
    others = [x for x in range(n_states) if x != target]
    pos = {x: r for r, x in enumerate(others)}
    a = [[Fraction(0)] * len(others) for _ in others]
    for (x, y), k in rates.items():
        if x == target:
            continue
        a[pos[x]][pos[x]] += k
        if y != target:
            a[pos[x]][pos[y]] -= k
    tau = solve_exact(a, [Fraction(1)] * len(others))
    out = [Fraction(0)] * n_states
    for x in others:
        out[x] = tau[pos[x]]
    return out


def gillespie(s: str, start: Structure, z: float, rng: random.Random, model: Model = Model(),
              t_max: float = math.inf, stop: Structure | None = None, max_steps: int = 10**6):
    """Simulate the chain (the stochastic simulation algorithm of Kinfold).

    Returns the trajectory [(time, structure), ...]. It ends at t_max, at the structure stop,
    or after max_steps moves.
    """
    t, cur = 0.0, start
    traj = [(t, cur)]
    e_cur = energy(cur, model)
    for _ in range(max_steps):
        if stop is not None and cur == stop:
            break
        moves = neighbors(s, cur, model)
        es = [energy(q, model) for q in moves]
        ks = [1.0 if e <= e_cur else z ** (e - e_cur) for e in es]
        total = sum(ks)
        if total == 0.0:
            break
        t += rng.expovariate(total)
        if t > t_max:
            break
        r = rng.random() * total
        acc = 0.0
        pick = len(moves) - 1
        for idx, k in enumerate(ks):
            acc += k
            if r < acc:
                pick = idx
                break
        cur, e_cur = moves[pick], es[pick]
        traj.append((t, cur))
    return traj


def local_minima(states: list, energies: list[int], adj: list[list[int]]) -> list[int]:
    """States with no neighbor of lower energy, and no neighbor of equal energy with a smaller index."""
    out = []
    for x in range(len(states)):
        if all(energies[y] > energies[x] or (energies[y] == energies[x] and y > x) for y in adj[x]):
            out.append(x)
    return out


def adjacency(s: str, states: list, model: Model = Model()) -> list[list[int]]:
    index = {st: x for x, st in enumerate(states)}
    return [[index[q] for q in neighbors(s, st, model)] for st in states]


def barrier_tree(states: list, energies: list[int], adj: list[list[int]]):
    """Flooding with union-find, in order of energy (ties by index).

    Returns (minima, merges). Each merge (saddle_energy, lower_min, upper_min) says that the basin
    of upper_min joins the basin of lower_min at the given saddle energy. The barrier of upper_min
    is saddle_energy - E(upper_min).
    """
    order = sorted(range(len(states)), key=lambda x: (energies[x], x))
    parent = list(range(len(states)))
    rep = {}  # root -> the lowest minimum of its basin (first state added)
    added = [False] * len(states)
    minima, merges = [], []

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for x in order:
        added[x] = True
        roots = sorted({find(y) for y in adj[x] if added[y]}, key=lambda r: (energies[rep[r]], rep[r]))
        if not roots:
            minima.append(x)
            rep[x] = x
            continue
        top = roots[0]
        parent[x] = top
        for r in roots[1:]:
            merges.append((energies[x], rep[top], rep[r]))
            parent[r] = top
    return minima, merges


def saddle_energy_bfs(energies: list[int], adj: list[list[int]], a: int, b: int) -> int:
    """Lowest threshold t such that a and b are joined by a path of states with energy <= t."""
    for t in sorted(set(energies)):
        if energies[a] > t or energies[b] > t:
            continue
        seen = {a}
        stack = [a]
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y not in seen and energies[y] <= t:
                    seen.add(y)
                    stack.append(y)
        if b in seen:
            return t
    raise ValueError("the move graph is not connected")


def to_dot_bracket(n: int, structure: Structure) -> str:
    out = ["."] * n
    for i, j in structure:
        out[i], out[j] = "(", ")"
    return "".join(out)
