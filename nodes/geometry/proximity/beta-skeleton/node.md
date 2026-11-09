---
tag: 8WP4AF
kind: data-structure
slug: beta-skeleton
name: Beta-skeleton
aliases:
- beta skeleton
- lune-based beta-skeleton
area: geometry/proximity
level: research
summary: Parametric family of proximity graphs that interpolates between the Gabriel graph and the lune-based graph.
model: real-ram
complexity:
  vars: {n: the number of points, d: the degree of the queried vertex, m: the number of edges}
  time: {build: O(n^3), has_edge: O(1), neighbors: O(d)}
  space: {total: O(n + m)}
history:
  year: 1985
  people: [David G. Kirkpatrick, John D. Radke]
  note: Kirkpatrick and Radke introduced beta-skeletons in 1985 as a one-parameter family of empty-region graphs for describing the shape of a point set, containing the Gabriel graph and the relative neighborhood graph as special cases.
prereqs: [gabriel-graph, relative-neighborhood-graph, dot-product, cross-product]
see_also: [proximity-graphs, urquhart-graph, delaunay-triangulation, geometric-spanner, euclidean-minimum-spanning-tree, planar-graph]
sources:
  - paper: "David G. Kirkpatrick and John D. Radke, A framework for computational morphology, in Godfried T. Toussaint (editor), Computational Geometry, Machine Intelligence and Pattern Recognition 2, North-Holland, 1985, 217-248"
    locator: the definition of the lune-based and circle-based beta-neighbourhoods and the resulting family of graphs
  - paper: doi:10.1109/5.163414
    title: Jerzy W. Jaromczyk and Godfried T. Toussaint, Relative neighborhood graphs and their relatives, Proceedings of the IEEE 80(9), 1992, 1502-1517
    locator: the section on beta-skeletons, their inclusions, and construction algorithms
  - paper: "David Eppstein, Beta-skeletons have unbounded dilation, Computational Geometry: Theory and Applications 23(1), 2002, 43-52"
    locator: the construction showing that beta-skeletons for beta greater than 1 are not spanners with bounded stretch
  - paper: "Prosenjit Bose, Luc Devroye, William Evans and David Kirkpatrick, On the spanning ratio of Gabriel graphs and beta-skeletons, SIAM Journal on Discrete Mathematics 20(2), 2006, 412-427"
    locator: bounds on the spanning ratio of beta-skeletons as a function of beta
---

A $\beta$-skeleton of a point set $P$ joins two points $p$ and $q$ when a region $R_\beta(p, q)$ attached to the segment $pq$ contains no other point. The parameter $\beta > 0$ sets the size of the region. In the lune-based version of Kirkpatrick and Radke (1985), for $\beta \ge 1$ the region is the intersection of two disks of radius $\beta \|pq\| / 2$ that touch $p$ and $q$ from the inside, and for $\beta < 1$ it is the lens between two circles through $p$ and $q$. A larger $\beta$ means a larger region and fewer edges. The value $\beta = 1$ gives the [Gabriel graph](/gabriel-graph/), and $\beta = 2$ gives the [relative neighborhood graph](/relative-neighborhood-graph/). So the family is a dial that moves the [proximity graph](/proximity-graphs/) from almost complete (small $\beta$) to empty (large $\beta$). This page builds it from the definition with an exact test for rational $\beta$.

## In plain words

For every pair of points, draw a shape around the segment between them. If no other point falls in the shape, connect the pair.

A knob, called beta, sets how fat the shape is. At beta 1 the shape is the circle that has the segment as its diameter. At beta 2 it is the almond shape where two big circles, one around each point, overlap. Below 1 the shape is a thin lens hugging the segment, so almost every pair gets connected. Above 2 the shape is wide, and even close pairs get blocked.

Turning the knob up only removes links, never adds them. Small values give a dense, crossing graph; values between 1 and 2 give a sparse network without crossings; large values break the points into pieces.

## The abstract type

A static undirected graph on $\{0, \ldots, n-1\}$, built from distinct points $p_0, \ldots, p_{n-1}$ and a rational $\beta > 0$, with a flag that says whether the region is open or closed:

- `build(P, β, closed)`: compute the graph.
- `has_edge(i, j)`: whether $\{i, j\}$ is an edge.
- `neighbors(i)`: the vertices adjacent to $i$.

With $w = q - p$, the region for $\beta \ge 1$ is the intersection of the disks of radius $\beta \|w\|/2$ centered at $p + \frac{\beta}{2} w$ and $q - \frac{\beta}{2} w$; each disk has $p$ or $q$ on its boundary. For $0 < \beta < 1$ it is the intersection of the two disks of radius $\|w\|/(2\beta)$ whose circles pass through both $p$ and $q$.

## Representation

The points, $\beta$, the flag, and a hash set of neighbours per vertex, each edge stored at both ends. For $\beta > 1$, and for the closed region at $\beta = 1$, the graph is a subgraph of the Gabriel graph, so it is planar with $O(n)$ edges; for small $\beta$ it can have $\Theta(n^2)$ edges: if no three points are on a line, every other point sees $pq$ at an angle less than $\pi$, so a small enough $\beta$ gives the complete graph.

## Operations

```pseudo id=main
BUILD(P, β)
L1  for each pair i < j do
L2    empty ← true
L3    for each k ∉ {i, j} do
L4      if IN-REGION(P[i], P[j], P[k], β) then
L5        empty ← false; break
L6    if empty then add j to adj[i] and i to adj[j]

IN-REGION(p, q, r, β)
L7  if β ≥ 1 then
L8    c1 ← p + (β/2)(q − p); c2 ← q + (β/2)(p − q); ρ² ← (β/2)² ‖q − p‖²
L9    return ‖r − c1‖² < ρ² and ‖r − c2‖² < ρ²
L10 u ← p − r; v ← q − r
L11 return u · v < 0 and (u · v)² > (1 − β²) ‖u‖² ‖v‖²

HAS-EDGE(i, j)
L12 return j ∈ adj[i]

NEIGHBORS(i)
L13 return adj[i]
```

The closed variant replaces $<$ by $\le$ in lines L9 and L11. Line L11 is the lens test without square roots: the lens is the set of points that see $pq$ at an angle larger than $\pi - \arcsin \beta$, and squaring the cosine condition gives a polynomial inequality. For rational $\beta$ and rational coordinates every quantity is rational, so the test is exact.

## Example

$P = \{(1,3), (1,11), (2,8), (5,1), (9,6), (11,1), (11,4)\}$, the set used on the Gabriel graph and RNG pages, with open regions unless stated:

| $\beta$ | edges | what changes |
| --- | --- | --- |
| $9/10$ | 11 | contains $(1,3)$, $(9,6)$ and $(2,8)$, $(5,1)$, which cross: not planar |
| $1$, open | 9 | the open Gabriel graph; also keeps $(5,1)$, $(11,4)$, since $(11,1)$ is only on its circle |
| $1$, closed | 8 | the Gabriel graph |
| $3/2$ | 8 | same as the Gabriel graph here |
| $2$ | 7 | the RNG; $(5,1)$, $(9,6)$ is blocked by $(11,1)$ |
| $5/2$ | 5 | loses $(2,8)$, $(9,6)$ and $(5,1)$, $(11,1)$: two components |
| $10$ | 4 | three components |

Each row is a subgraph of the row above it. For instance, at $\beta = 5/2$ the pair $(2,8)$, $(9,6)$ with $w = (7,-2)$ is blocked by $(5,1)$: the first condition of the region reads $\|r - p\|^2 = 58 < \frac{5}{2}\,(r - p) \cdot w = \frac{5}{2} \cdot 35 = 87.5$, and the second reads $\|r - q\|^2 = 41 < \frac{5}{2}\,(r - q) \cdot (p - q) = \frac{5}{2} \cdot 18 = 45$.

## Correctness

For $\beta \ge 1$, expanding $\|r - c_1\|^2 < \rho^2$ gives the equivalent form $\|r - p\|^2 < \beta\,(r - p) \cdot (q - p)$, and similarly for $c_2$, used in the example. For $\beta < 1$, a circle through $p$ and $q$ with center at signed distance $t$ from the midpoint $m$ contains $r$ exactly when $(p - r) \cdot (q - r) < 2ts$, where $s$ is the signed height of $r$ above the line $pq$; taking both circles and replacing $|s|$ by the cross product gives line L11. Both forms show that the region grows with $\beta$, so the skeletons shrink as $\beta$ grows. BUILD applies the test to every pair and third point. The full proof is in the correctness proof below.

## Complexity

| operation | time | notes |
| --- | --- | --- |
| BUILD, this page | $O(n^3)$ | $\binom{n}{2}$ pairs, $O(n)$ exact tests each |
| BUILD for $1 \le \beta \le 2$ | $O(n^2)$ | test only the $O(n)$ Delaunay edges |
| HAS-EDGE | $O(1)$ expected | hash set lookup |
| NEIGHBORS | $O(d)$ | $d$ the degree |
| space | $O(n + m)$ | $m = O(n)$ for $\beta > 1$ |

For $\beta > 1$ the region contains the closed diametral disk except $p$ and $q$, so every edge is a Gabriel edge and hence a [Delaunay](/delaunay-triangulation/) edge; only those $O(n)$ candidates need testing. Faster algorithms filter the Delaunay edges further; see the survey of Jaromczyk and Toussaint.

## Variants

- **Circle-based skeletons.** For $\beta \ge 1$, Kirkpatrick and Radke also use the union, instead of the intersection, of the two disks of radius $\beta \|pq\|/2$ whose circles pass through both $p$ and $q$. The circle-based skeletons agree with the lune-based ones at $\beta = 1$ and give larger regions, hence sparser graphs, for $\beta > 1$.
- **Open versus closed regions.** The two differ only for points exactly on the boundary, which is common with integer input; the closed 1-skeleton is the Gabriel graph, while the open 2-skeleton is the RNG.
- **Other dimensions and metrics.** The lune definition uses only distances and extends to $\mathbb{R}^d$ and to other norms.
- **Shape reconstruction.** For points sampled densely from a smooth curve, suitable values of $\beta$ make the skeleton connect consecutive samples, which turns it into a curve reconstruction method.

## When to use it

Use a $\beta$-skeleton when you need a proximity graph whose density you can tune: shape description and curve reconstruction from samples, where $\beta$ trades fragmentation against spurious links, and empirical studies that compare neighbour definitions. For the two most used members, build the [Gabriel graph](/gabriel-graph/) or the [relative neighborhood graph](/relative-neighborhood-graph/) directly. When you need short paths, use a [geometric spanner](/geometric-spanner/): Eppstein showed that for $\beta > 1$ the stretch of a $\beta$-skeleton can be arbitrarily large.

## Pitfalls

- **Irrational centers for $\beta < 1$.** The two circles through $p$ and $q$ have centers at distance $\sqrt{\rho^2 - \|pq\|^2/4}$ from the midpoint, which is irrational in general. Computing them in floating point makes the test inexact; use the polynomial form of line L11.
- **The open 1-skeleton is not planar.** For the four corners of a square, each diagonal has the other two corners on its circle, outside the open disk, so both diagonals are edges and cross. Use the closed disk at $\beta = 1$, or any $\beta > 1$, for a planar graph.
- **Disconnection for large $\beta$.** Above $\beta = 2$ the region is larger than the RNG lune, and edges of the minimum spanning tree can disappear, as in the example. For the triangle $(0,0)$, $(4,0)$, $(2,3)$ the 3-skeleton has no edges at all.
- **Mixing up the two families.** The lune-based and circle-based skeletons coincide at $\beta = 1$ and nowhere else in general; the RNG is the lune-based 2-skeleton.

## Implementations

## History

Kirkpatrick and Radke introduced $\beta$-skeletons in 1985 in a volume edited by Toussaint, as part of a framework for computational morphology, the description of the shape of a dot pattern. The family placed the Gabriel graph (1969) and the relative neighborhood graph (1980) on a common scale. Jaromczyk and Toussaint surveyed the family and its algorithms in 1992. Later work studied how well the skeletons approximate distances: Eppstein (2002) showed that the stretch is unbounded for $\beta > 1$, and Bose, Devroye, Evans and Kirkpatrick (2006) bounded it for the Gabriel graph and smaller $\beta$.

## References
