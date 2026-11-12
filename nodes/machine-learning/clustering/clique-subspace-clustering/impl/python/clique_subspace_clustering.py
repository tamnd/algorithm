# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clique-subspace-clustering/. The authors are listed in prov/M7PPXT.jsonl.
"""CLIQUE: grid-based subspace clustering (Agrawal, Gehrke, Gunopulos, Raghavan 1998).

Each attribute is cut into xi equal intervals. A unit in a subspace S is one
interval for each attribute of S, written as a sorted tuple of
(attribute, interval) pairs. A unit is dense when more than tau * N points
fall in it. Dense units are found bottom-up, one dimension per pass, with an
Apriori-style join and prune that relies on downward closure. A cluster is a
connected component of the dense units of one subspace, where two units are
adjacent when they share a face. Each cluster is described by a greedy cover
with maximal regions, a DNF expression.
"""

from fractions import Fraction
from itertools import combinations


def grid_cells(points, xi, bounds=None):
    """Interval index of each attribute of each point; the top value goes to the last interval."""
    d = len(points[0])
    if bounds is None:
        bounds = [(min(p[a] for p in points), max(p[a] for p in points)) for a in range(d)]
    cells = []
    for p in points:
        cell = []
        for a in range(d):
            lo, hi = bounds[a]
            if hi == lo:
                cell.append(0)
                continue
            if not lo <= p[a] <= hi:
                raise ValueError("point outside the bounds")
            cell.append(min(xi - 1, int((p[a] - lo) * xi // (hi - lo))))
        cells.append(tuple(cell))
    return cells


def _is_dense(count, n, tau):
    return count > Fraction(tau) * n


def count_units(cells, candidates):
    """One pass over the data: the number of points in each candidate unit."""
    by_subspace = {}
    for u in candidates:
        by_subspace.setdefault(tuple(a for a, _ in u), set()).add(u)
    counts = dict.fromkeys(candidates, 0)
    for cell in cells:
        for dims, units in by_subspace.items():
            key = tuple((a, cell[a]) for a in dims)
            if key in units:
                counts[key] += 1
    return counts


def join_and_prune(dense):
    """Candidates of dimension k from the dense units of dimension k - 1."""
    previous = sorted(dense)
    candidates = set()
    for i, u in enumerate(previous):
        for v in previous[i + 1:]:
            if u[:-1] != v[:-1]:
                break  # sorted, so no later v shares the prefix
            if u[-1][0] < v[-1][0]:  # @line L4
                c = u + (v[-1],)
                if all(c[:j] + c[j + 1:] in dense for j in range(len(c))):  # @line L5
                    candidates.add(c)
    return candidates


def dense_units(cells, tau):
    """All dense units in all subspaces, by levels. Returns a list U with U[k-1] the k-dimensional ones."""
    n = len(cells)
    d = len(cells[0])
    first = {((a, cell[a]),) for cell in cells for a in range(d)}
    counts = count_units(cells, first)
    level = {u for u, c in counts.items() if _is_dense(c, n, tau)}  # @line L2
    levels = []
    while level:  # @line L3
        levels.append(level)
        candidates = join_and_prune(level)
        counts = count_units(cells, candidates)
        level = {u for u, c in counts.items() if _is_dense(c, n, tau)}  # @line L6
    return levels


def dense_units_brute_force(cells, tau):
    """Every unit of every one of the 2^d - 1 subspaces, counted directly."""
    n = len(cells)
    d = len(cells[0])
    found = set()
    for k in range(1, d + 1):
        for dims in combinations(range(d), k):
            counts = {}
            for cell in cells:
                key = tuple((a, cell[a]) for a in dims)
                counts[key] = counts.get(key, 0) + 1
            found |= {u for u, c in counts.items() if _is_dense(c, n, tau)}
    return found


def adjacent(u, v):
    """Units of the same subspace that share a common face."""
    if tuple(a for a, _ in u) != tuple(a for a, _ in v):
        return False
    diffs = [abs(x - y) for (_, x), (_, y) in zip(u, v) if x != y]
    return diffs == [1]


def clusters_in_subspace(units):
    """Connected components of dense units of one subspace, by an explicit stack."""
    units = set(units)
    seen, comps = set(), []
    for s in sorted(units):
        if s in seen:
            continue
        comp, stack = [], [s]
        seen.add(s)
        while stack:
            u = stack.pop()
            comp.append(u)
            for j, (a, x) in enumerate(u):
                for y in (x - 1, x + 1):
                    v = u[:j] + ((a, y),) + u[j + 1:]
                    if v in units and v not in seen:
                        seen.add(v)
                        stack.append(v)
        comps.append(sorted(comp))
    return comps


def region_units(region):
    """All units in a region, a tuple of (attribute, low, high) with inclusive interval indices."""
    out = [()]
    for a, lo, hi in region:
        out = [u + ((a, x),) for u in out for x in range(lo, hi + 1)]
    return out


def _fits(region, cluster):
    return all(u in cluster for u in region_units(region))


def maximal_region(start, cluster):
    """Grow a box from a unit: along each attribute in turn, first up, then down."""
    region = [(a, x, x) for a, x in start]
    for j in range(len(region)):
        a, lo, hi = region[j]
        while _fits(region[:j] + [(a, lo, hi + 1)] + region[j + 1:], cluster):
            hi += 1
        while _fits(region[:j] + [(a, lo - 1, hi)] + region[j + 1:], cluster):
            lo -= 1
        region[j] = (a, lo, hi)
    return tuple(region)


def minimal_cover(cluster):
    """Greedy cover with maximal regions, then removal of redundant regions, smallest first."""
    cluster = set(cluster)
    regions, covered = [], set()
    for u in sorted(cluster):  # @line L9
        if u not in covered:
            r = maximal_region(u, cluster)
            regions.append(r)
            covered.update(region_units(r))
    size = {r: len(region_units(r)) for r in regions}
    keep = list(regions)
    for r in sorted(regions, key=lambda r: (size[r], r)):  # @line L10
        others = set()
        for s in keep:
            if s != r:
                others.update(region_units(s))
        if all(u in others for u in region_units(r)):
            keep.remove(r)
    return sorted(keep)


def describe(region, xi, bounds):
    """A region as a conjunction of value ranges (one DNF term)."""
    terms = []
    for a, lo, hi in region:
        low, high = bounds[a]
        width = Fraction(high - low) / xi
        terms.append((a, low + lo * width, low + (hi + 1) * width))
    return terms


def clique(points, xi, tau, bounds=None):
    """Return a list of (subspace, cluster units, DNF regions), one entry per cluster."""
    if xi < 1 or not 0 <= tau < 1:
        raise ValueError("need xi >= 1 and 0 <= tau < 1")
    cells = grid_cells(points, xi, bounds)  # @line L1
    by_subspace = {}
    for level in dense_units(cells, tau):
        for u in level:
            by_subspace.setdefault(tuple(a for a, _ in u), []).append(u)
    result = []
    for dims in sorted(by_subspace, key=lambda s: (len(s), s)):  # @line L7
        for comp in clusters_in_subspace(by_subspace[dims]):  # @line L8
            result.append((dims, comp, minimal_cover(comp)))
    return result


def points_in_cluster(cells, units):
    units = set(units)
    dims = tuple(a for a, _ in next(iter(units)))
    return [i for i, cell in enumerate(cells) if tuple((a, cell[a]) for a in dims) in units]
