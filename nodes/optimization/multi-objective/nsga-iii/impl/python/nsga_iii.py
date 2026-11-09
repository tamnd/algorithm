# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nsga-iii/. The authors are listed in prov/YWZJB7.jsonl.

"""NSGA-III of Deb and Jain (2014).

All objectives are minimized. Survival keeps whole fronts while they fit and
fills the rest of the population from the next front by reference lines:
the images are normalized, each one is attached to its nearest reference line,
and the lines with the fewest attached members get new members first.
The code works with floats or with Fraction images.
"""

import math
import random
from fractions import Fraction
from typing import Callable, Sequence

Vector = Sequence[float]
BIG = 10**6  # 1 / w_i for the small weights of the achievement function


def dominates(a: Vector, b: Vector) -> bool:
    """Return True when a dominates b (minimization)."""
    strict = False
    for u, v in zip(a, b):
        if u > v:
            return False
        if u < v:
            strict = True
    return strict


def fast_non_dominated_sort(images: Sequence[Vector]) -> list[list[int]]:
    """Return the fronts F1, F2, ... as lists of indices. O(p N^2) time."""
    n = len(images)
    beats: list[list[int]] = [[] for _ in range(n)]
    count = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if dominates(images[i], images[j]):
                beats[i].append(j)
                count[j] += 1
            elif dominates(images[j], images[i]):
                beats[j].append(i)
                count[i] += 1
    fronts = [[i for i in range(n) if count[i] == 0]]
    while fronts[-1]:
        nxt = []
        for i in fronts[-1]:
            for j in beats[i]:
                count[j] -= 1
                if count[j] == 0:
                    nxt.append(j)
        fronts.append(nxt)
    fronts.pop()
    return fronts


def das_dennis(p: int, h: int) -> list[tuple[Fraction, ...]]:
    """All points of the unit simplex in R^p whose coordinates are multiples of 1/h, for h >= 1."""
    out = []

    def rec(prefix: list[int], left: int) -> None:
        if len(prefix) == p - 1:
            out.append(tuple(Fraction(v, h) for v in prefix + [left]))
            return
        for v in range(left + 1):
            rec(prefix + [v], left - v)

    rec([], h)
    return out


def solve(a: list[list], b: list) -> list | None:
    """Solve a x = b by Gaussian elimination with partial pivoting; None if singular."""
    m = len(b)
    rows = [list(a[i]) + [b[i]] for i in range(m)]
    for c in range(m):
        piv = max(range(c, m), key=lambda r: abs(rows[r][c]))
        if abs(rows[piv][c]) < 1e-12:
            return None
        rows[c], rows[piv] = rows[piv], rows[c]
        for r in range(m):
            if r != c and rows[r][c] != 0:
                q = rows[r][c] / rows[c][c]
                rows[r] = [u - q * v for u, v in zip(rows[r], rows[c])]
    return [rows[i][m] / rows[i][i] for i in range(m)]


def normalize(images: Sequence[Vector], members: Sequence[int]) -> tuple[dict[int, tuple], list]:
    """Translate by the ideal point of the members and divide by the hyperplane intercepts.

    Return the normalized image of each member and the intercepts. When the
    extreme points do not span a hyperplane with positive intercepts, the
    intercepts are the largest translated values, and 1 where that is 0.
    """
    p = len(images[members[0]])
    ideal = [min(images[i][m] for i in members) for m in range(p)]
    shifted = {i: tuple(images[i][m] - ideal[m] for m in range(p)) for i in members}
    extremes = []
    for j in range(p):
        def asf(i: int) -> float:
            s = shifted[i]
            return max(s[m] if m == j else s[m] * BIG for m in range(p))

        extremes.append(shifted[min(members, key=asf)])
    inv = solve([list(e) for e in extremes], [1] * p)
    if inv is not None and all(v > 0 for v in inv):
        cuts = [1 / v for v in inv]
    else:
        cuts = []
        for m in range(p):
            top = max(shifted[i][m] for i in members)
            cuts.append(top if top > 0 else 1)
    return {i: tuple(s[m] / cuts[m] for m in range(p)) for i, s in shifted.items()}, cuts


def perpendicular_sq(s: Vector, w: Vector):
    """Squared distance from s to the line through 0 and w."""
    ww = sum(v * v for v in w)
    sw = sum(u * v for u, v in zip(s, w))
    return sum(u * u for u in s) - sw * sw / ww


def associate(norm: dict[int, tuple], refs: Sequence[Vector]) -> tuple[dict[int, int], dict[int, float]]:
    """Nearest reference line of each member (smallest index on ties) and the squared distance."""
    line, dist = {}, {}
    for i, s in norm.items():
        best = min(range(len(refs)), key=lambda j: (perpendicular_sq(s, refs[j]), j))
        line[i], dist[i] = best, perpendicular_sq(s, refs[best])
    return line, dist


def niching(k: int, last: Sequence[int], line: dict, dist: dict, rho: list[int], rng: random.Random) -> list[int]:
    """Add k members of the last front, in order, by the niche counts rho (changed in place)."""
    added: list[int] = []
    left = set(last)
    excluded: set[int] = set()
    while len(added) < k:  # @line L11
        low = min(rho[j] for j in range(len(rho)) if j not in excluded)
        j = rng.choice([j for j in range(len(rho)) if j not in excluded and rho[j] == low])  # @line L12
        cand = sorted(i for i in left if line[i] == j)  # @line L13
        if not cand:
            excluded.add(j)  # @line L14
            continue
        pick = min(cand, key=lambda i: dist[i]) if rho[j] == 0 else rng.choice(cand)  # @line L15
        added.append(pick)
        left.discard(pick)
        rho[j] += 1
    return added


def survival(images: Sequence[Vector], n: int, refs: Sequence[Vector], rng: random.Random, trace: dict | None = None) -> list[int]:
    """Indices of the n members of R kept by NSGA-III."""
    fronts = fast_non_dominated_sort(images)  # @line L4
    s: list[int] = []
    l = 0
    while len(s) < n:  # @line L5
        s.extend(fronts[l])
        l += 1
    if len(s) == n:  # @line L6
        return s
    last = fronts[l - 1]
    kept = s[: len(s) - len(last)]  # @line L7
    norm, cuts = normalize(images, s)  # @line L8
    line, dist = associate(norm, refs)  # @line L9
    rho = [0] * len(refs)
    for i in kept:  # @line L10
        rho[line[i]] += 1
    if trace is not None:
        trace.update(norm=norm, cuts=cuts, line=line, dist=dist, rho=list(rho), last=list(last))
    added = niching(n - len(kept), last, line, dist, rho, rng)
    if trace is not None:
        trace["added"] = added
    return kept + added


def nsga_iii_loop(
    pop: list,
    f: Callable,
    make_offspring: Callable[[list, random.Random], list],
    n: int,
    refs: Sequence[Vector],
    generations: int,
    rng: random.Random,
    on_generation: Callable[[list, list], None] | None = None,
) -> list:
    """Run NSGA-III from a population of n pairs (x, f(x)). Return the first front of the last population."""
    for _ in range(generations):  # @line L2
        parents = [pop[rng.randrange(n)][0] for _ in range(n)]  # @line L3
        off = [(x, tuple(f(x))) for x in make_offspring(parents, rng)][:n]
        union = pop + off
        keep = survival([y for _, y in union], n, refs, rng)
        pop = [union[i] for i in keep]
        if on_generation is not None:
            on_generation(pop, union)
    first = fast_non_dominated_sort([y for _, y in pop])[0]  # @line L16
    return [pop[i] for i in first]


def sbx(x1: Vector, x2: Vector, eta: float, lower: Vector, upper: Vector, rng: random.Random):
    """Simulated binary crossover of two real vectors, each variable with probability 1/2, then clipping."""
    c1, c2 = list(x1), list(x2)
    for i in range(len(x1)):
        if rng.random() < 0.5:
            u = rng.random()
            beta = (2 * u) ** (1 / (eta + 1)) if u <= 0.5 else (1 / (2 * (1 - u))) ** (1 / (eta + 1))
            a, b = x1[i], x2[i]
            c1[i] = 0.5 * ((1 + beta) * a + (1 - beta) * b)
            c2[i] = 0.5 * ((1 - beta) * a + (1 + beta) * b)
        c1[i] = min(upper[i], max(lower[i], c1[i]))
        c2[i] = min(upper[i], max(lower[i], c2[i]))
    return tuple(c1), tuple(c2)


def polynomial_mutation(x: Vector, eta: float, pm: float, lower: Vector, upper: Vector, rng: random.Random):
    """Polynomial mutation of each variable with probability pm, then clipping."""
    out = list(x)
    for i in range(len(x)):
        if rng.random() < pm:
            u = rng.random()
            delta = (2 * u) ** (1 / (eta + 1)) - 1 if u < 0.5 else 1 - (2 * (1 - u)) ** (1 / (eta + 1))
            out[i] = min(upper[i], max(lower[i], x[i] + delta * (upper[i] - lower[i])))
    return tuple(out)


def nsga_iii(
    f: Callable[[Vector], Vector],
    n: int,
    p: int,
    h: int,
    lower: Sequence[float],
    upper: Sequence[float],
    generations: int,
    rng: random.Random,
    eta_c: float = 30.0,
    eta_m: float = 20.0,
    on_generation: Callable[[list, list], None] | None = None,
) -> list:
    """Real-coded NSGA-III in the box [lower, upper] with the Das and Dennis points of h divisions."""
    d = len(lower)
    refs = [tuple(float(v) for v in w) for w in das_dennis(p, h)]

    def make_offspring(parents, r):
        out = []
        for k in range(0, len(parents), 2):
            u, v = parents[k], parents[(k + 1) % len(parents)]
            u, v = sbx(u, v, eta_c, lower, upper, r)
            out.append(polynomial_mutation(u, eta_m, 1 / d, lower, upper, r))
            out.append(polynomial_mutation(v, eta_m, 1 / d, lower, upper, r))
        return out

    pop = []
    for _ in range(n):  # @line L1
        x = tuple(rng.uniform(lower[i], upper[i]) for i in range(d))
        pop.append((x, tuple(f(x))))
    return nsga_iii_loop(pop, f, make_offspring, n, refs, generations, rng, on_generation)


def dtlz2(x: Vector, p: int = 3) -> tuple:
    """DTLZ2 with p objectives; the front is the part of the unit sphere in the positive orthant."""
    g = sum((v - 0.5) ** 2 for v in x[p - 1 :])
    out = []
    for m in range(p):
        val = 1 + g
        for v in x[: p - 1 - m]:
            val *= math.cos(v * math.pi / 2)
        if m > 0:
            val *= math.sin(x[p - 1 - m] * math.pi / 2)
        out.append(val)
    return tuple(out)
