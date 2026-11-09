---
tag: 5F7BZ4
kind: data-structure
slug: relative-neighborhood-graph
name: Relative neighborhood graph
aliases:
- RNG
- relative neighbourhood graph
area: geometry/proximity
level: advanced
summary: Edge between two points iff no third point is closer to both of them than they are to each other.
model: real-ram
complexity:
  vars: {n: the number of points, d: the degree of the queried vertex}
  time: {build: O(n^3), has_edge: O(1), neighbors: O(d)}
  space: {total: O(n)}
history:
  year: 1980
  people: [Godfried T. Toussaint]
  note: Toussaint defined the relative neighborhood graph in 1980 as a model of perceived neighbourhood and proved that it contains the minimum spanning tree and lies in the Delaunay triangulation; Supowit gave an O(n log n) algorithm in 1983.
prereqs: [proximity-graphs, euclidean-distance, gabriel-graph]
see_also: [urquhart-graph, beta-skeleton, euclidean-minimum-spanning-tree, delaunay-triangulation, nearest-neighbor-graph, minimum-spanning-tree, single-linkage-clustering, planar-graph]
sources:
  - paper: doi:10.1016/0031-3203(80)90066-7
    title: Godfried T. Toussaint, The relative neighbourhood graph of a finite planar set, Pattern Recognition 12(4), 1980, 261-268
    locator: the definition by the empty lune, the inclusions between the minimum spanning tree, the relative neighbourhood graph and the Delaunay triangulation, and the first algorithms
  - paper: doi:10.1145/2402.322386
    title: Kenneth J. Supowit, The relative neighborhood graph, with an application to minimum spanning trees, Journal of the ACM 30(3), 1983, 428-448
    locator: the O(n log n) construction in the plane and the use of the graph to compute minimum spanning trees
  - paper: doi:10.1109/5.163414
    title: Jerzy W. Jaromczyk and Godfried T. Toussaint, Relative neighborhood graphs and their relatives, Proceedings of the IEEE 80(9), 1992, 1502-1517
    locator: the survey of the graph, its relatives, the constructions from the Delaunay triangulation, and higher dimensions
  - paper: "Andrzej Lingas, A linear-time construction of the relative neighborhood graph from the Delaunay triangulation, Computational Geometry: Theory and Applications 4(4), 1994, 199-208"
    locator: the O(n) filter of the Delaunay edges
---

The relative neighborhood graph (RNG) of a set $P$ of points joins $p$ and $q$ when no third point is closer to both of them than they are to each other: there is no $r$ with $\max(\|p - r\|, \|q - r\|) < \|p - q\|$. The forbidden region, the intersection of the two open disks of radius $\|p - q\|$ around $p$ and around $q$, is called the lune of $p$ and $q$. Toussaint (1980) introduced the graph as a model of which points a person sees as neighbours. In the chain of [proximity graphs](/proximity-graphs/) it lies between the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) and the [Gabriel graph](/gabriel-graph/): it contains every minimum spanning tree and is contained in every [Delaunay triangulation](/delaunay-triangulation/). Supowit (1983) builds it in $O(n \log n)$ time; this page stores it as adjacency sets and builds it from the definition with exact squared distances.

## In plain words

Two points are neighbours unless a third point is closer to each of them than they are to each other. If you and a friend both live closer to a third person than to each other, the third person is "between" you, and you are not direct neighbours.

The test only compares distances, so it can use squared distances and stay exact on whole numbers.

The result is a sparse network without crossings that connects every point. It keeps the links of the cheapest network that connects all the points, plus a few more, so it shows the shape of a cluster without the long cross links a triangulation has.

## The abstract type

A relative neighborhood graph is a static undirected graph on the vertex set $\{0, \ldots, n-1\}$, built from distinct points $p_0, \ldots, p_{n-1}$:

- `build(P)`: compute the graph.
- `has_edge(i, j)`: whether $\{i, j\}$ is an edge.
- `neighbors(i)`: the vertices adjacent to $i$.

The edge set is $\{\{i, j\} : \max(\|p_i - p_k\|^2, \|p_j - p_k\|^2) \ge \|p_i - p_j\|^2 \text{ for every } k \ne i, j\}$. The lune is open: a point at distance exactly $\|p_i - p_j\|$ from one end does not block the edge.

## Representation

A hash set of neighbours per vertex, $adj[0..n-1]$, with each edge stored at both ends, and the list of points. The graph is planar, so the total size is $O(n)$.

## Operations

```pseudo id=main
BUILD(P)
L1  for each pair i < j do
L2    d ← ‖P[i] − P[j]‖²
L3    empty ← true
L4    for each k ∉ {i, j} do
L5      if max(‖P[i] − P[k]‖², ‖P[j] − P[k]‖²) < d then
L6        empty ← false; break
L7    if empty then add j to adj[i] and i to adj[j]

HAS-EDGE(i, j)
L8  return j ∈ adj[i]

NEIGHBORS(i)
L9  return adj[i]
```

Line L5 is the lune test. All three quantities are squared distances, which are exact on integer or rational input; comparing squares gives the same answer as comparing distances.

## Example

$P = \{(1,3), (1,11), (2,8), (5,1), (9,6), (11,1), (11,4)\}$, the same set as on the [Gabriel graph](/gabriel-graph/) page. Every RNG edge is a Gabriel edge, so only the 8 Gabriel edges need the lune test. The table gives, for each, the third point $r$ with the smallest $\max(\|pr\|^2, \|qr\|^2)$.

| pair | $d = \|pq\|^2$ | minimizing $r$ | $\max(\|pr\|^2, \|qr\|^2)$ | RNG edge? |
| --- | --- | --- | --- | --- |
| $(1,3)$, $(2,8)$ | 26 | $(5,1)$ | 58 | yes |
| $(1,3)$, $(5,1)$ | 20 | $(2,8)$ | 58 | yes |
| $(1,11)$, $(2,8)$ | 10 | $(1,3)$ | 64 | yes |
| $(2,8)$, $(9,6)$ | 53 | $(5,1)$ | 58 | yes |
| $(5,1)$, $(9,6)$ | 41 | $(11,1)$ | 36 | no |
| $(5,1)$, $(11,1)$ | 36 | $(9,6)$ | 41 | yes |
| $(9,6)$, $(11,4)$ | 8 | $(11,1)$ | 29 | yes |
| $(11,1)$, $(11,4)$ | 9 | $(9,6)$ | 29 | yes |

The pair $(5,1)$, $(9,6)$ is a Gabriel edge, since $(11,1)$ is outside its diametral disk, but $(11,1)$ is at squared distance 36 from $(5,1)$ and 29 from $(9,6)$, both less than 41, so it lies in the lune. The RNG has 7 edges on 7 points and one cycle, $(2,8)$, $(9,6)$, $(11,4)$, $(11,1)$, $(5,1)$, $(1,3)$; removing its longest edge, $(2,8)$, $(9,6)$ with squared length 53, gives the minimum spanning tree.

## Correctness

Line L5 succeeds exactly when $p_k$ is in the open lune, because comparing squared distances is the same as comparing distances, and line L7 stores the edge exactly when no point succeeded. The two inclusions come from short exchange arguments. If $r$ is in the lune of an edge $pq$ of a minimum spanning tree, then $pr$ or $qr$ reconnects the two halves of the tree after deleting $pq$ and is shorter, so the tree was not minimum. If $r$ is in the diametral disk of $pq$, the angle at $r$ is at least a right angle, so $\|pq\|^2 \ge \|pr\|^2 + \|qr\|^2$ and $r$ is in the lune; hence every RNG edge is a Gabriel edge. The full proof is in the correctness proof below.

## Complexity

| operation | time | notes |
| --- | --- | --- |
| BUILD, this page | $O(n^3)$ | $\binom{n}{2}$ pairs, $O(n)$ lune tests each |
| BUILD, Supowit | $O(n \log n)$ | worst case, in the plane |
| BUILD from a Delaunay triangulation | $O(n)$ | after the triangulation (Lingas) |
| HAS-EDGE | $O(1)$ expected | hash set lookup |
| NEIGHBORS | $O(d)$ | $d$ the degree |
| space | $O(n)$ | planar, at most $3n - 6$ edges |

## Variants

- **From the Gabriel graph or the Delaunay triangulation.** Since RNG $\subseteq$ GG $\subseteq$ DT, it suffices to test the $O(n)$ Delaunay edges. Testing each against all points costs $O(n^2)$; Supowit's sweep and Lingas's filter reduce this to $O(n \log n)$ and $O(n)$ after triangulation.
- **The [Urquhart graph](/urquhart-graph/).** Removing the longest edge of each Delaunay triangle gives a graph that contains the RNG and is often equal to it; it was proposed as a fast approximation.
- **[Beta-skeletons](/beta-skeleton/).** The lune-based $\beta$-skeleton with $\beta = 2$ is the RNG; larger $\beta$ gives sparser graphs, and $\beta = 1$ gives the Gabriel graph.
- **Other metrics and dimensions.** The definition uses only distances, so it applies in any metric space. The minimum spanning tree inclusion holds in every metric, while planarity is special to the Euclidean plane.

## When to use it

Use the RNG as a sparse, connected, planar backbone that reflects the shape of a point set: cluster analysis and shape description in pattern recognition, neighbour selection in spatial statistics, and topology control in wireless networks, where each node keeps only the links not dominated by a shorter common neighbour. It is also a step toward the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/): the tree can be found by running [Kruskal's algorithm](/kruskal/) on the RNG edges only. When you need guaranteed short paths, use a [geometric spanner](/geometric-spanner/) instead.

## Pitfalls

- **Open versus closed lune.** Ties are common on integer input. For $(0,0)$, $(5,0)$, $(3,4)$, the squared distances are 25, 25 and 20. With the open lune of this page all three edges stay. With a closed lune, $(3,4)$ blocks $(0,0)$, $(5,0)$ and $(5,0)$ blocks $(0,0)$, $(3,4)$, which isolates $(0,0)$: the closed version can be disconnected, and the minimum spanning tree inclusion fails.
- **Square roots.** Comparing $\sqrt{\cdot}$ values in floating point can merge two different distances; compare the squared integers.
- **Assuming it is a tree.** The RNG often has cycles, as in the example; it is the minimum spanning tree only for special inputs.
- **Duplicate points.** The definition needs distinct points; the code rejects duplicates.

## Implementations

## History

Toussaint introduced the relative neighborhood graph in 1980 in Pattern Recognition, motivated by the way people perceive the shape of a dot pattern, and proved the inclusions MST $\subseteq$ RNG $\subseteq$ DT. Urquhart (1980) suggested approximating it by the Delaunay triangulation with the longest edge of each triangle removed. Supowit (1983) gave the first $O(n \log n)$ algorithm in the plane, and Lingas (1994) showed how to filter it out of the Delaunay triangulation in linear time. Jaromczyk and Toussaint surveyed the graph and its relatives in 1992.

## References
