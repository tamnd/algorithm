---
tag: T3DGB2
kind: data-structure
slug: gabriel-graph
name: Gabriel graph
aliases:
- GG
- Gabriel neighbourhood graph
area: geometry/proximity
level: advanced
summary: Edge between two points iff no other point lies inside the circle having them as diameter.
model: real-ram
complexity:
  vars: {n: the number of points, d: the degree of the queried vertex}
  time: {build: O(n^3), has_edge: O(1), neighbors: O(d)}
  space: {total: O(n)}
history:
  year: 1969
  people: [K. Ruben Gabriel, Robert R. Sokal]
  note: Gabriel and Sokal defined the graph in 1969 to decide which sampling localities count as neighbours in studies of geographic variation; Matula and Sokal proved its main properties in 1980.
prereqs: [proximity-graphs, dot-product, delaunay-triangulation]
see_also: [relative-neighborhood-graph, beta-skeleton, urquhart-graph, euclidean-minimum-spanning-tree, nearest-neighbor-graph, voronoi-diagram, geometric-spanner, planar-graph]
sources:
  - paper: doi:10.2307/2412323
    title: K. Ruben Gabriel and Robert R. Sokal, A new statistical approach to geographic variation analysis, Systematic Zoology 18(3), 1969, 259-278
    locator: the definition of Gabriel-connected localities by the empty circle on the segment as diameter
  - paper: doi:10.1111/j.1538-4632.1980.tb00031.x
    title: David W. Matula and Robert R. Sokal, Properties of Gabriel graphs relevant to geographic variation research and the clustering of points in the plane, Geographical Analysis 12(3), 1980, 205-222
    locator: the inclusions between the minimum spanning tree, the relative neighborhood graph, the Gabriel graph and the Delaunay triangulation, and the construction from the Voronoi diagram
  - paper: doi:10.1109/5.163414
    title: Jerzy W. Jaromczyk and Godfried T. Toussaint, Relative neighborhood graphs and their relatives, Proceedings of the IEEE 80(9), 1992, 1502-1517
    locator: the survey of the Gabriel graph, the relative neighborhood graph and beta-skeletons, with construction algorithms
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 9, Delaunay Triangulations (the empty-circle characterization of Delaunay edges, and the exercise asking to show that the Gabriel graph is a subgraph of the Delaunay triangulation)
  - paper: "Prosenjit Bose, Luc Devroye, William Evans and David Kirkpatrick, On the spanning ratio of Gabriel graphs and beta-skeletons, SIAM Journal on Discrete Mathematics 20(2), 2006, 412-427"
    locator: the worst-case spanning ratio of the Gabriel graph, of order the square root of n
---

The Gabriel graph of a set $P$ of points in the plane joins two points $p$ and $q$ when the closed disk with diameter $pq$ contains no other point of $P$. Equivalently, every other point $r$ sees the segment $pq$ at an acute angle: $(p - r) \cdot (q - r) > 0$. It sits in the middle of the chain of [proximity graphs](/proximity-graphs/): every Euclidean minimum spanning tree is inside the [relative neighborhood graph](/relative-neighborhood-graph/), which is inside the Gabriel graph, which is inside every [Delaunay triangulation](/delaunay-triangulation/). So it is planar, connected, and has at most $3n - 6$ edges. It can be read off a Delaunay triangulation in $O(n)$ time, so it costs $O(n \log n)$ to build; this page stores it as adjacency sets and builds it from the definition with an exact integer test.

## In plain words

Draw a circle that has two points as the ends of its diameter, the smallest circle through both. If no other point is inside the circle or on it, connect the two points.

Two points far apart need a big circle, and a big circle usually catches some other point, so long links are rare. Two close points with nobody between them always get a link.

The test does not need the circle. Stand at a third point and look at the two points: if the angle between them is a right angle or wider, the third point is in the circle and blocks the link. That angle test uses only multiplication and addition, so it is exact.

The links form a network without crossings that connects every point, with no more links than a triangulation has.

## The abstract type

A Gabriel graph is a static undirected graph on the vertex set $\{0, \ldots, n-1\}$, built from distinct points $p_0, \ldots, p_{n-1}$ in the plane:

- `build(P)`: compute the graph.
- `has_edge(i, j)`: whether $\{i, j\}$ is an edge.
- `neighbors(i)`: the vertices adjacent to $i$.

The edge set is $\{\{i, j\} : (p_i - p_k) \cdot (p_j - p_k) > 0 \text{ for every } k \ne i, j\}$. The disk is closed: a point on the circle blocks the edge.

## Representation

One hash set of neighbours per vertex, $adj[0..n-1]$, and the list of points. The edge $\{i, j\}$ is stored twice, as $j \in adj[i]$ and $i \in adj[j]$. Since the graph is planar, the total size is $O(n)$.

## Operations

```pseudo id=main
BUILD(P)
L1  for each pair i < j do
L2    empty ← true
L3    for each k ∉ {i, j} do
L4      if (P[i] − P[k]) · (P[j] − P[k]) ≤ 0 then
L5        empty ← false; break
L6    if empty then add j to adj[i] and i to adj[j]

HAS-EDGE(i, j)
L7  return j ∈ adj[i]

NEIGHBORS(i)
L8  return adj[i]
```

Line L4 is the whole geometric test. With $m$ the midpoint of $p_i p_j$, the identity $(p_i - r) \cdot (p_j - r) = \|m - r\|^2 - \|p_i - p_j\|^2/4$ shows that the dot product is at most $0$ exactly when $r$ is in the closed disk. On integer coordinates it is exact, with no square root and no division.

## Example

$P = \{(1,3), (1,11), (2,8), (5,1), (9,6), (11,1), (11,4)\}$, in general position. Its Delaunay triangulation has 12 edges. The table lists them with the third point that gives the smallest dot product in line L4.

| pair | $\|pq\|^2$ | minimizing $r$ | $(p - r) \cdot (q - r)$ | Gabriel edge? |
| --- | --- | --- | --- | --- |
| $(1,3)$, $(1,11)$ | 64 | $(2,8)$ | $-14$ | no |
| $(1,3)$, $(2,8)$ | 26 | $(1,11)$ | $24$ | yes |
| $(1,3)$, $(5,1)$ | 20 | $(2,8)$ | $32$ | yes |
| $(1,11)$, $(2,8)$ | 10 | $(1,3)$ | $40$ | yes |
| $(1,11)$, $(9,6)$ | 89 | $(2,8)$ | $-13$ | no |
| $(2,8)$, $(5,1)$ | 58 | $(1,3)$ | $-6$ | no |
| $(2,8)$, $(9,6)$ | 53 | $(1,3)$ | $23$ | yes |
| $(5,1)$, $(9,6)$ | 41 | $(11,4)$ | $6$ | yes |
| $(5,1)$, $(11,1)$ | 36 | $(11,4)$ | $9$ | yes |
| $(5,1)$, $(11,4)$ | 45 | $(11,1)$ | $0$ | no, $(11,1)$ is on the circle |
| $(9,6)$, $(11,4)$ | 8 | $(11,1)$ | $15$ | yes |
| $(11,1)$, $(11,4)$ | 9 | $(9,6)$ | $14$ | yes |

The other 9 pairs are not Delaunay edges, and each has a negative dot product with some point, for example $-6$ for $(1,3)$, $(9,6)$ with $r = (5,1)$. So the Gabriel graph has 8 edges. Dropping $(5,1)$, $(9,6)$, whose lune contains $(11,1)$, gives the 7-edge relative neighborhood graph, and dropping also $(2,8)$, $(9,6)$, the longest edge on the cycle through $(1,3)$ and $(5,1)$, gives the minimum spanning tree.

## Correctness

Line L4 rejects the pair exactly when some other point lies in the closed disk with diameter $p_i p_j$, by the identity above, and line L6 stores the pair exactly when no point was rejected. The containments $\text{MST} \subseteq \text{RNG} \subseteq \text{GG} \subseteq \text{DT}$ follow from two facts. If $r$ is in the disk, the angle at $r$ is at least a right angle, so $\|pq\|^2 \ge \|pr\|^2 + \|qr\|^2$, and $r$ is strictly closer to both ends than they are to each other, which blocks the RNG edge. And the disk with diameter $pq$ is an empty closed disk with $p$ and $q$ on its boundary, which is the empty-circle condition for a Delaunay edge. The full proof is in the correctness proof below.

## Complexity

| operation | time | notes |
| --- | --- | --- |
| BUILD, this page | $O(n^3)$ | $\binom{n}{2}$ pairs, $O(n)$ tests each |
| BUILD from a Delaunay triangulation | $O(n \log n)$ | $O(n)$ after the triangulation |
| HAS-EDGE | $O(1)$ expected | hash set lookup |
| NEIGHBORS | $O(d)$ | $d$ the degree |
| space | $O(n)$ | at most $3n - 6$ edges |

The cubic build is the definition and is meant as a reference; for more than a few hundred points use the Delaunay filter below.

## Variants

- **Build from the Delaunay triangulation.** A Delaunay edge $pq$ is a Gabriel edge if and only if each vertex $r$ opposite to $pq$ in a triangle on $pq$ has $(p - r) \cdot (q - r) > 0$. The reason: if $r$ is outside the closed disk $D$ with diameter $pq$, then on $r$'s side of the line $pq$, $D$ lies inside the empty circumcircle of $pqr$, so no point there is in $D$. Checking the at most two opposite vertices per edge takes $O(n)$ after the $O(n \log n)$ triangulation. Matula and Sokal phrase the same test with the [Voronoi diagram](/voronoi-diagram/): $pq$ is a Gabriel edge exactly when it crosses the Voronoi edge between the cells of $p$ and $q$. The tests check this filter against the definition.
- **[Beta-skeletons](/beta-skeleton/).** The disk-based $\beta$-skeleton for $\beta = 1$ is the Gabriel graph; $\beta = 2$ in the lune version gives the relative neighborhood graph.
- **Higher dimensions.** The same dot product test defines the Gabriel graph in $\mathbb{R}^d$ with the closed ball on $pq$ as diameter. It is still a subgraph of the Delaunay graph, by the same empty-ball argument, but it is no longer planar, and the cubic build of this page works unchanged.
- **Open disk.** Some authors use the open disk. The two versions differ only when a point lies exactly on a circle, as $(11,1)$ does in the example.

## When to use it

Use the Gabriel graph when you need a sparse planar graph that connects points to their natural neighbours, contains a minimum spanning tree, and is computed by a simple local test: neighbourhood structure in spatial statistics and geographic variation studies, clustering by cutting long edges, and topology control in wireless networks, where a node can decide its Gabriel edges from the positions of its neighbours alone. Use the [Delaunay triangulation](/delaunay-triangulation/) when you need a triangulation or a [spanner](/geometric-spanner/) with bounded stretch, and the [relative neighborhood graph](/relative-neighborhood-graph/) for an even sparser graph.

## Pitfalls

- **Open versus closed disk.** With integer input, points on the circle are common, as in the right angle at $(11,1)$ in the example. Decide which convention you need; this page uses the closed disk, so line L4 tests $\le 0$.
- **Computing the circle in floating point.** Comparing the distance to the midpoint with half the length rounds the center and the radius. The dot product test has no division and no root, so it is exact on integers.
- **Duplicate points.** Two equal points give a disk of radius $0$ that contains each of them; the definition breaks down, and the code rejects duplicates.
- **Assuming bounded stretch.** The Gabriel graph is connected but not a constant spanner: Bose, Devroye, Evans and Kirkpatrick showed that the shortest path can be of order $\sqrt n$ times the straight-line distance.
- **Equating it with the Delaunay graph.** On four cocircular points such as the corners of a square, the Gabriel graph is the four sides: each diagonal has the other two corners on its circle. A Delaunay triangulation must still add one diagonal.

## Implementations

## History

Gabriel and Sokal introduced the graph in 1969 in Systematic Zoology, to decide which pairs of sampling sites should count as neighbours when testing for geographic variation. Matula and Sokal (1980) proved that it contains the minimum spanning tree and the relative neighborhood graph and is contained in the Delaunay triangulation, and showed how to obtain it from the Voronoi diagram. Toussaint's relative neighborhood graph (1980) and the $\beta$-skeletons of Kirkpatrick and Radke (1985) place it in a family of graphs defined by empty regions, surveyed by Jaromczyk and Toussaint in 1992.

## References
