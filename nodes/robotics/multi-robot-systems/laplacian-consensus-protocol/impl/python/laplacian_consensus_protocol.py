# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplacian-consensus-protocol/. The authors are listed in prov/GHGHQ7.jsonl.

"""Laplacian consensus protocol x' = -L x and its sampled form x(k+1) = (I - eps L) x(k).

Agents are 0..r-1. An edge (i, j) or (i, j, w) means that agent i receives the
state of agent j with weight w > 0 (a_ij = w). For an undirected graph the edge
also gives a_ji = w. This is the convention of Olfati-Saber and Murray (2004):
the neighbors of i are the agents j with (i, j) in E.
"""

from typing import Sequence

Edge = tuple  # (i, j) or (i, j, w)


def adjacency(r: int, edges: Sequence[Edge], directed: bool = False) -> list[list]:
    """Return the weighted adjacency matrix A with A[i][j] = a_ij."""
    a = [[0] * r for _ in range(r)]
    for e in edges:
        i, j = e[0], e[1]
        w = e[2] if len(e) > 2 else 1
        if i == j:
            raise ValueError("self loops are not allowed")
        if w <= 0:
            raise ValueError("weights must be positive")
        a[i][j] += w
        if not directed:
            a[j][i] += w
    return a


def laplacian(r: int, edges: Sequence[Edge], directed: bool = False) -> list[list]:
    """Return L = D - A, where D holds the weighted in-degrees (row sums of A)."""
    a = adjacency(r, edges, directed)
    lap = [[-a[i][j] for j in range(r)] for i in range(r)]
    for i in range(r):
        lap[i][i] = sum(a[i])
    return lap


def neighbor_lists(r: int, edges: Sequence[Edge], directed: bool = False) -> list[list]:
    """Return, for each agent i, the list of pairs (j, a_ij) with a_ij > 0."""
    a = adjacency(r, edges, directed)
    return [[(j, a[i][j]) for j in range(r) if a[i][j] != 0] for i in range(r)]


def consensus_step(nbrs: list[list], x: Sequence, eps) -> list:
    """One synchronous round of the sampled protocol. Each agent reads only its neighbors."""
    new = []
    for i in range(len(x)):  # @line L3
        u = sum(w * (x[j] - x[i]) for j, w in nbrs[i])  # @line L4
        new.append(x[i] + eps * u)  # @line L5
    return new


def discrete_consensus(r: int, edges: Sequence[Edge], x0: Sequence, eps, steps: int,
                       directed: bool = False) -> list:
    """Run x(k+1) = (I - eps L) x(k) for the given number of rounds.

    The protocol is stable for 0 < eps < 1 / Delta, where Delta is the largest
    weighted in-degree. Works with float or fractions.Fraction values.
    """
    nbrs = neighbor_lists(r, edges, directed)  # @line L1
    x = list(x0)
    for _ in range(steps):  # @line L2
        x = consensus_step(nbrs, x, eps)  # @line L6
    return x  # @line L7


def switching_consensus(r: int, edge_sets: Sequence[Sequence[Edge]], x0: Sequence, eps,
                        steps: int, directed: bool = False) -> list:
    """Sampled protocol on a switching graph: round k uses edge_sets[k mod len(edge_sets)]."""
    lists = [neighbor_lists(r, es, directed) for es in edge_sets]
    x = list(x0)
    for k in range(steps):
        x = consensus_step(lists[k % len(lists)], x, eps)
    return x


def continuous_consensus(r: int, edges: Sequence[Edge], x0: Sequence[float], t: float,
                         dt: float, directed: bool = False) -> list[float]:
    """Integrate x' = -L x from 0 to t with the classic RK4 method and fixed step dt."""
    lap = laplacian(r, edges, directed)

    def f(x):
        return [-sum(lap[i][j] * x[j] for j in range(r)) for i in range(r)]

    x = [float(v) for v in x0]
    steps = max(1, round(t / dt))
    h = t / steps
    for _ in range(steps):
        k1 = f(x)
        k2 = f([x[i] + 0.5 * h * k1[i] for i in range(r)])
        k3 = f([x[i] + 0.5 * h * k2[i] for i in range(r)])
        k4 = f([x[i] + h * k3[i] for i in range(r)])
        x = [x[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(r)]
    return x


def max_degree(r: int, edges: Sequence[Edge], directed: bool = False):
    """Return Delta, the largest weighted in-degree."""
    return max(sum(row) for row in adjacency(r, edges, directed))
