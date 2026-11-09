---
tag: XMCR03
kind: data-structure
slug: urquhart-graph
name: Urquhart graph
aliases:
- UG
area: geometry/proximity
level: research
summary: Delaunay triangulation with the longest edge of every triangle removed; sits between the RNG and the Delaunay graph.
model: real-ram
complexity:
  vars: {n: the number of points, d: the degree of the queried vertex}
  time: {build: O(n^4), has_edge: O(1), neighbors: O(d)}
  space: {total: O(n)}
history:
  year: 1980
  people: [R. B. Urquhart]
  note: Urquhart proposed in 1980 to compute the relative neighborhood graph by deleting the longest edge of each Delaunay triangle; the result was later shown to be a different graph that only contains the RNG, and it now carries his name.
prereqs: [delaunay-triangulation, relative-neighborhood-graph]
see_also: [gabriel-graph, proximity-graphs, beta-skeleton, euclidean-minimum-spanning-tree, in-circle-test, general-position, planar-graph]
sources:
  - paper: "R. B. Urquhart, Algorithms for computation of relative neighbourhood graph, Electronics Letters 16(14), 1980, 556-557"
    locator: the proposal to remove the longest edge of every Delaunay triangle
  - paper: doi:10.1016/0031-3203(80)90066-7
    title: Godfried T. Toussaint, The relative neighbourhood graph of a finite planar set, Pattern Recognition 12(4), 1980, 261-268
    locator: the relative neighbourhood graph and its inclusion in the Delaunay triangulation
  - paper: doi:10.1109/5.163414
    title: Jerzy W. Jaromczyk and Godfried T. Toussaint, Relative neighborhood graphs and their relatives, Proceedings of the IEEE 80(9), 1992, 1502-1517
    locator: the discussion of the longest-edge heuristic and the difference between its output and the relative neighborhood graph
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 9, Delaunay Triangulations (the empty-circle characterization and the O(n log n) expected construction)
---

The Urquhart graph of a point set is its [Delaunay triangulation](/delaunay-triangulation/) with the longest side of every triangle removed. Urquhart (1980) proposed it as a fast way to compute the [relative neighborhood graph](/relative-neighborhood-graph/): if a side $pq$ is the longest in a Delaunay triangle $pqr$, then $r$ is closer to both $p$ and $q$ than they are to each other, so $pq$ cannot be an RNG edge. That argument shows only one direction. An RNG edge test can fail because of a point that is not the third corner of a triangle on $pq$, so the Urquhart graph contains the RNG and can be strictly larger. It is therefore its own member of the family of [proximity graphs](/proximity-graphs/), with $\text{RNG} \subseteq \text{UG} \subseteq \text{DT}$, computable in $O(n)$ time from the triangulation.

## In plain words

Start from the Delaunay triangulation, the triangulation whose triangles are as fat as possible. In every triangle, find the longest side and delete it.

The deleted side is always a "bad" link in the sense of the relative neighborhood graph: the opposite corner of the triangle is closer to both ends than they are to each other. So everything that survives in the true neighbor graph also survives here.

The shortcut misses some bad links, because a link can be spoiled by a point that is not a corner of the triangles beside it. So this graph is a quick stand-in for the neighbour graph, often equal to it, sometimes with a few extra links.

## The abstract type

A static undirected graph on $\{0, \ldots, n-1\}$, built from distinct points $p_0, \ldots, p_{n-1}$ with no four on a circle:

- `build(P)`: compute the graph.
- `has_edge(i, j)`: whether $\{i, j\}$ is an edge.
- `neighbors(i)`: the vertices adjacent to $i$.

When a triangle has two longest sides of equal length, this page removes neither. With that rule, every RNG edge is kept even when there are ties.

## Representation

The list of points, the list of Delaunay triangles as index triples, and a hash set of neighbours per vertex. All three have size $O(n)$.

## Operations

```pseudo id=main
BUILD(P)
L1  T ← the Delaunay triangles of P
L2  E ← the sides of the triangles in T (the sorted path if P is collinear)
L3  for each triangle t in T do
L4    if the longest side e of t is strictly longer than the other two then
L5      remove e from E
L6  store E in adj, each edge at both ends

HAS-EDGE(i, j)
L7  return j ∈ adj[i]

NEIGHBORS(i)
L8  return adj[i]
```

The implementation computes line L1 by brute force: a triple is kept when its circumcircle has no other point inside or on it, decided by the exact [in-circle test](/in-circle-test/). This takes $O(n^4)$ time and is meant as a reference; any $O(n \log n)$ Delaunay algorithm can replace it. It rejects inputs with four cocircular points, for which the triangulation and hence the graph is not unique. Line L4 compares squared lengths.

## Example

$P = \{(1,3), (1,11), (2,8), (5,1), (9,6), (11,1), (11,4)\}$, the set used on the [Gabriel graph](/gabriel-graph/) and RNG pages. Its Delaunay triangulation has 12 edges and 6 triangles.

| triangle | squared side lengths | removed side |
| --- | --- | --- |
| $(1,3)$, $(1,11)$, $(2,8)$ | 64, 26, 10 | $(1,3)$, $(1,11)$ |
| $(1,3)$, $(2,8)$, $(5,1)$ | 26, 20, 58 | $(2,8)$, $(5,1)$ |
| $(1,11)$, $(2,8)$, $(9,6)$ | 10, 89, 53 | $(1,11)$, $(9,6)$ |
| $(2,8)$, $(5,1)$, $(9,6)$ | 58, 53, 41 | $(2,8)$, $(5,1)$ again |
| $(5,1)$, $(9,6)$, $(11,4)$ | 41, 45, 8 | $(5,1)$, $(11,4)$ |
| $(5,1)$, $(11,1)$, $(11,4)$ | 36, 45, 9 | $(5,1)$, $(11,4)$ again |

Four distinct sides are removed, so the Urquhart graph has 8 edges. The RNG has 7: the edge $(5,1)$, $(9,6)$ survives here, since it is the shortest side of both its triangles, but $(11,1)$ lies in its lune, at squared distances 36 and 29, both less than 41. The point $(11,1)$ is not a corner of either triangle on that edge, so the longest-edge rule cannot see it. On this set the Urquhart graph equals the Gabriel graph; in general neither contains the other.

## Correctness

Line L1 gives the Delaunay triangles by the empty-circle characterization, and lines L3 to L5 remove exactly the unique longest side of each. The inclusion $\text{UG} \subseteq \text{DT}$ is immediate. For $\text{RNG} \subseteq \text{UG}$: a removed side $pq$ is strictly the longest in some Delaunay triangle $pqr$, so $r$ is strictly closer to $p$ and to $q$ than $\|pq\|$, which puts $r$ in the lune of $pq$; so no RNG edge is removed. Hence the graph is connected and planar. The full proof is in the correctness proof below.

## Complexity

| operation | time | notes |
| --- | --- | --- |
| BUILD, this page | $O(n^4)$ | brute-force Delaunay triangulation |
| BUILD with a fast triangulation | $O(n \log n)$ | the filter of lines L2 to L6 is $O(n)$ |
| HAS-EDGE | $O(1)$ expected | hash set lookup |
| NEIGHBORS | $O(d)$ | $d$ the degree |
| space | $O(n)$ | at most $2n$ triangles and $3n$ edges |

## Variants

- **Exact RNG from the triangulation.** To get the RNG itself, each Delaunay edge must be tested against all points that may lie in its lune, not only the two opposite corners. Lingas showed that this can still be done in $O(n)$ time after triangulation.
- **Removing sides by angle.** Removing instead every side whose opposite corner, in some triangle on it, sees it at a right or obtuse angle gives exactly the [Gabriel graph](/gabriel-graph/), by the Delaunay filter described there. The longest side of a triangle is opposite its largest angle, so the two rules agree on triangles with an obtuse angle and differ on acute ones.
- **[Beta-skeletons](/beta-skeleton/).** A one-parameter family through the Gabriel graph and the RNG, defined by empty regions instead of by triangles.

## When to use it

Use the Urquhart graph when a Delaunay triangulation is already available and a sparse, connected, planar neighbour graph that contains the RNG is enough: cluster detection by cutting long edges, mesh and shape simplification, and as a candidate set for the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/), which it always contains. When you need the exact RNG, add the full lune test.

## Pitfalls

- **Calling it the RNG.** The two graphs differ on some inputs, as in the example; in the tests, 12 of 500 random small sets give different graphs.
- **Ties in the longest side.** Removing both equal longest sides of an isosceles triangle can delete RNG edges, for example in the triangle $(0,0)$, $(5,0)$, $(4,3)$ with squared sides 25, 25 and 10; the RNG keeps all three sides. Remove a side only when it is strictly the longest.
- **Cocircular points.** Four or more points on a circle make the triangulation ambiguous, and different triangulations give different Urquhart graphs, for example the four corners of a square. The code rejects such input; a robust version needs a consistent tie-breaking rule such as symbolic perturbation.
- **Floating-point in-circle tests.** The triangulation depends on the sign of a determinant; computing it in floating point can produce a non-Delaunay triangle on nearly cocircular input. Use exact arithmetic or an adaptive predicate.

## Implementations

## History

Toussaint introduced the relative neighborhood graph in 1980 and proved that it lies in the Delaunay triangulation. In the same year Urquhart suggested computing it by deleting the longest edge of each Delaunay triangle, which would have given a fast algorithm. The method was later shown to produce a supergraph of the RNG that can differ from it, and the result became known as the Urquhart graph. The surveys of Jaromczyk and Toussaint (1992) treat it with the other relatives of the RNG.

## References
