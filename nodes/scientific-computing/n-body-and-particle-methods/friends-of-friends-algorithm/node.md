---
tag: HXVJ9V
kind: algorithm
slug: friends-of-friends-algorithm
name: Friends-of-friends algorithm
aliases:
- friends-of-friends halo finder
area: scientific-computing/n-body-and-particle-methods
level: core
summary: Groups simulation particles into halos by linking every pair closer than a linking length and taking the connected components.
model: word-ram
complexity:
  vars: {N: the number of particles, P: the number of pairs in neighboring grid cells}
  time: {average: "O(N + P α(N)) expected", worst: "Θ(N^2)"}
  space: {extra: "Θ(N)"}
properties: {deterministic: true}
history:
  year: 1982
  people: [John P. Huchra, Margaret J. Geller, Marc Davis, George Efstathiou, Carlos S. Frenk, Simon D. M. White]
  note: Huchra and Geller found groups of galaxies by linking neighbors in 1982, and Davis, Efstathiou, Frenk and White used the method on the particles of cosmological simulations in 1985.
prereqs: [disjoint-set, connected-components, uniform-grid]
see_also: [single-linkage-clustering, dbscan, fixed-radius-near-neighbors, spatial-hashing, linked-cell-list, breadth-first-search, gravitational-n-body-problem, kd-tree]
sources:
  - paper: doi:10.1086/160000
    title: "John P. Huchra and Margaret J. Geller, Groups of galaxies. I. Nearby groups, Astrophysical Journal 257, 1982, 423-437"
    locator: the linking of galaxies into groups
  - paper: doi:10.1086/163168
    title: "Marc Davis, George Efstathiou, Carlos S. Frenk and Simon D. M. White, The evolution of large-scale structure in a universe dominated by cold dark matter, Astrophysical Journal 292, 1985, 371-394"
    locator: the friends-of-friends groups of the simulation particles
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 4th edition, MIT Press, 2022
    locator: Chapter 19 (data structures for disjoint sets)
---

The friends-of-friends (FoF) algorithm finds groups of points that are linked by chains of close neighbors. Two points are friends when their distance is at most a linking length $b$, and a group is a set of points in which any two are joined by a chain of friends: the groups are the [connected components](/connected-components/) of the graph of friend pairs. In cosmology the points are the particles of a simulation, the groups with enough members are the dark matter halos, and $b$ is usually $0.2$ times the mean distance between particles. The efficient method puts the points in a [grid](/uniform-grid/) of cells of side $b$, tests only pairs in neighboring cells, and merges the groups with a [disjoint-set](/disjoint-set/) forest. FoF is the same clustering as [single linkage](/single-linkage-clustering/) cut at the height $b$, and as [DBSCAN](/dbscan/) with a minimum of one neighbor.

## In plain words

Pick a distance. Any two points closer than that distance are friends. A friend of a friend is in the same group, and so is a friend of that one, and so on. A group is everything that you can reach by jumping from friend to friend.

To find the groups fast, draw a grid of boxes as wide as the distance. A friend of a point is always in the same box or in a box next to it, so only those boxes need to be checked. Each time two friends are found, their groups are joined. The groups do not have a fixed shape: a long thin chain of points is one group.

## The problem

The input is $N$ points $\mathbf{x}_1, \ldots, \mathbf{x}_N \in \mathbb{R}^D$, a linking length $b > 0$ and a minimum size $n_{\min} \ge 1$. Let $F$ be the graph with an edge between $i \ne j$ when $|\mathbf{x}_i - \mathbf{x}_j| \le b$. The output is the list of connected components of $F$ with at least $n_{\min}$ points. In cosmology $b$ is given as a fraction of the mean distance $\bar{\ell} = (V / N)^{1/3}$ of $N$ particles in a volume $V$, and halos need $n_{\min}$ of about 20 or more particles.

## The algorithm

```pseudo id=main
FOF(x, b, n_min)
L1  for i ← 1 to N do add i to the list of cell ⌊x_i / b⌋ of a hash grid
L2  for i ← 1 to N do MAKE-SET(i)
L3  for i ← 1 to N do
L4      for each offset o ∈ {-1, 0, 1}^D do
L5          for each j in the cell ⌊x_i / b⌋ + o with j > i do
L6              if |x_i - x_j| ≤ b then UNION(i, j)
L7  group the points by FIND(i)
L8  return the groups with at least n_min points

    FIND(i):
L9      while parent(i) ≠ i do parent(i) ← parent(parent(i)); i ← parent(i)
    UNION(i, j):
L10     link the root of the smaller set below the root of the larger one
```

Line L1 builds a [spatial hash](/spatial-hashing/) of the cells that hold points, so empty cells cost nothing. Lines L4 and L5 visit the $3^D$ cells around the cell of $i$; the test $j > i$ makes each pair count once. Lines L9 and L10 are the disjoint-set forest with path halving and union by size.

## Example

Take six points on a line: $0$, $0.15$, $0.3$, $1.0$, $1.1$ and $2.5$, with $b = 0.2$. The cells of side $0.2$ are $0, 0, 1, 5, 5, 12$.

| pair tested | distance | friends? | sets after the step |
|---|---|---|---|
| (0, 0.15) | 0.15 | yes | {0, 0.15}, {0.3}, {1.0}, {1.1}, {2.5} |
| (0, 0.3) | 0.3 | no | same |
| (0.15, 0.3) | 0.15 | yes | {0, 0.15, 0.3}, {1.0}, {1.1}, {2.5} |
| (1.0, 1.1) | 0.1 | yes | {0, 0.15, 0.3}, {1.0, 1.1}, {2.5} |

The point $2.5$ is in cell 12, and the cells 11 and 13 are empty, so it is tested against no other point. The groups are $\{0, 0.15, 0.3\}$, $\{1.0, 1.1\}$ and $\{2.5\}$; with $n_{\min} = 2$ the last one is dropped. The points $0$ and $0.3$ are $0.3 > b$ apart but are in one group through $0.15$: this chaining is the defining property of FoF.

## Correctness

If two points are at distance at most $b$, each coordinate differs by at most $b$, so their cells differ by at most 1 in each coordinate (Lemma 1 of the proof file). So lines L3 to L6 call UNION for every friend pair, and for no other pair (Lemma 2). A disjoint-set forest that has seen all edges of a graph has the connected components as its sets (Lemma 3). So line L7 gives the components of the friendship graph, as the definition asks.

## Complexity

In the [word RAM](/word-ram/) model, with a hash table of $O(1)$ expected time per access:

- Line L1 costs $O(N)$ expected time, and the table has at most $N$ cells.
- Lines L3 to L6 cost $O(3^D N + P)$, where $P$ is the number of pairs in neighboring cells, plus $O(P)$ disjoint-set operations of $O(\alpha(N))$ amortized time each.
- For points with a bounded number $q$ per cell, $P \le 3^D q N$, so the total is $O(N \alpha(N))$, close to linear. In a simulation, the dense centers of halos have many points per cell, and $P$ grows with their density.
- In the worst case all points lie in one cell, and $P = N(N-1)/2$. A [k-d tree](/kd-tree/) search does not improve this bound, because the friendship graph itself can have $\Theta(N^2)$ edges.
- The extra space is $\Theta(N)$ for the grid and the forest.

## Properties

- **Unique result.** The groups depend only on the points and $b$, not on the order of the points or of the unions (the components of a graph are unique).
- **No shape.** Groups follow any shape of the density, such as filaments, so two halos joined by a thin bridge of particles become one group.
- **Density threshold (heuristic).** A group of FoF with linking length $b$ is bounded, roughly, by a surface of constant density proportional to $b^{-3}$; for $b = 0.2 \bar{\ell}$ the groups have a mean density of very roughly a hundred or two hundred times the mean density.
- **Monotone in $b$.** A larger $b$ only merges groups; the groups for all $b$ form the tree of [single-linkage clustering](/single-linkage-clustering/).

## Variants and improvements

- **Periodic boxes.** Cosmological simulations are periodic: take the cell offsets and the distances modulo the box size ([periodic boundary conditions](/periodic-boundary-conditions/)).
- **Subhalo finders.** FoF finds the halos; methods such as SUBFIND then split each halo into bound substructures by density and by energy.
- **Phase-space FoF.** Link points that are close in both position and velocity, with two linking lengths.
- **Parallel FoF.** Each processor finds the groups of its domain, and groups that cross the boundaries are merged by a second union pass over the pairs that cross.
- **Tree or sorting instead of a grid.** A [k-d tree](/kd-tree/) with a range search of radius $b$ gives the same pairs and works well for very uneven densities.
- **Other uses.** The same algorithm finds clusters of atoms in [molecular dynamics](/molecular-dynamics/) and groups of galaxies in surveys (Huchra and Geller 1982), where the linking length must change with the distance from the observer.

## When to use it

Use FoF to find halos or groups when a single density scale defines them and the groups may have any shape. It is fast, has one parameter and gives a unique answer, so it is the first step of most halo catalogs. Use [DBSCAN](/dbscan/) when single noise points must not bridge clusters, and a spherical overdensity or a subhalo finder when the mass inside a radius is needed.

## Pitfalls

- **Bridging.** One chain of points can link two large groups. A larger $n_{\min}$ does not help; DBSCAN with a minimum of several neighbors, or a split by density, does.
- **Linking length in the wrong units.** $b = 0.2$ means $0.2 \bar{\ell}$, not $0.2$ length units.
- **Cell side smaller than $b$.** Then friends can be two or more cells apart, and searching only the neighboring cells misses them. The cell side must be at least $b$.
- **Rounding at the threshold.** A pair at distance exactly $b$ on paper can be just above $b$ after rounding; the result can change at such pairs.
- **Recursive search.** A depth-first search of the friend graph with recursion can run out of stack on large groups. Use the disjoint-set forest or an explicit queue.

## Implementations

## History

Huchra and Geller (1982) found groups of galaxies in a redshift survey by linking galaxies that are close in the sky and in redshift. Davis, Efstathiou, Frenk and White (1985) used the same linking on the particles of their simulations of cold dark matter, and the method has been the standard first halo finder of cosmological simulations since then. The linking length of $0.2$ of the mean separation became the common choice in later work.

## References
