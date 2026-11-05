---
tag: W3DZD3
kind: definition
slug: hive-graph
name: Hive graph
area: searching/fractional-cascading
level: research
summary: Planar map of horizontal segments, refined by vertical edges so each face is a rectangle with at most one extra vertex per horizontal side; used by Chazelle for segment intersection.
prereqs: [planar-subdivision, planar-point-location, orthogonal-segment-intersection, fractional-cascading-bridge]
see_also: [catalog-graph, multiple-list-search, trapezoidal-map, vertical-ray-shooting, orthogonal-point-enclosure, segment-tree]
sources:
  - paper: "Bernard Chazelle, Filtering search: a new approach to query-answering, SIAM Journal on Computing 15(3) (1986)"
    locator: pages 703 to 724, Section 4.1 (The hive-graph), Lemma 2 and Figures 2 to 4
  - paper: doi:10.1007/BF01840441
    title: Bernard Chazelle and Leonidas J. Guibas, Fractional cascading II, Applications, Algorithmica 1 (1986)
    locator: pages 163 to 191 (geometric applications of fractional cascading, including orthogonal segment intersection)
  - paper: doi:10.1007/BF01840440
    title: Bernard Chazelle and Leonidas J. Guibas, Fractional cascading I, A data structuring technique, Algorithmica 1 (1986)
    locator: pages 133 to 162
---

A hive graph is a planar subdivision built from a set of horizontal segments: it refines their vertical adjacency map by extra vertical edges until each face is a rectangle with at most one extra vertex on each horizontal side. Chazelle introduced it in his paper on filtering search (1986) to report the $k$ segments that cross a vertical query segment in $O(\log n + k)$ time with $O(n)$ space. Its construction copies every other vertical edge down through a segment, which is the sampling idea that [fractional cascading](/fractional-cascading-bridge/) turns into a general technique on [catalog graphs](/catalog-graph/).

## Definition

Let $S$ be a set of $n$ horizontal segments in the plane that meet only at their endpoints.

**Vertical adjacency map.** For each endpoint $M$ of a segment of $S$, draw the longest vertical segment, ray or line through $M$ that does not cross a segment of $S$ except possibly at an endpoint. The segments of $S$ and these vertical pieces form a [planar subdivision](/planar-subdivision/) $G(S)$, the vertical adjacency map of Lipski and Preparata. Each bounded face of $G(S)$ is an axis-parallel rectangle. The map has $O(n)$ vertices, edges and faces, since each endpoint adds at most two vertical edges and two new vertices.

**Extra vertex.** For a rectangular face $F$ of a subdivision whose edges are horizontal and vertical, a vertex on a horizontal side of $F$ that is not a corner of $F$ is an *extra* vertex of that side. A side with $j$ extra vertices consists of $j + 1$ edges.

**Hive graph.** A hive graph of $S$ is a planar subdivision $H$ such that

1. $H$ is obtained from $G(S)$ by adding vertical edges only, each of which lies on the vertical line through an endpoint of a segment of $S$;
2. each face of $H$ is an axis-parallel rectangle, possibly unbounded;
3. each horizontal side of each face has at most one extra vertex.

So each face has at most 6 edges: its 4 corners or fewer, and at most 2 extra vertices. A hive graph is not unique; the definition only fixes the properties.

**Chazelle's lemma.** Each set $S$ of $n$ horizontal segments has a hive graph with $O(n)$ vertices, and it can be computed in $O(n \log n)$ time (Lemma 2 of the filtering search paper). The construction sweeps a horizontal line from top to bottom and *combs* the map: at each segment $s$, among the vertical edges that end on top of $s$ and lie between two consecutive vertical edges below $s$, every other one is extended down to the next segment. A second sweep from bottom to top does the same for the lower sides.

**The query.** To report the segments of $S$ that a vertical query segment $q$ crosses, locate the lower endpoint of $q$ in $H$ by [planar point location](/planar-point-location/) in $O(\log n)$ time, and walk up along $q$ face by face. Each face that the walk crosses is left through its top side, which lies on a segment of $S$ that $q$ crosses, and the face has at most 6 edges, so the walk spends $O(1)$ time per reported segment. The total is $O(\log n + k)$, with the segments reported in order of height.

## Examples and non-examples

**An anomaly and its repair.** Let $S$ hold seven segments: $s_b$ at height 0 from $x = -1$ to $x = 17$, $s_m$ at height 5 from $x = 0$ to $x = 16$, and four short segments at height 6 with the $x$-ranges $[1, 3]$, $[5, 7]$, $[9, 11]$ and $[13, 15]$. In $G(S)$, the 8 endpoints of the short segments send vertical edges down to $s_m$. So the face $[0, 16] \times [0, 5]$, just below $s_m$, has 8 extra vertices on its top side, at $x = 1, 3, 5, \ldots, 15$. A walk up through this face would have to step along up to 9 edges of its top side to find the place where $q$ leaves it, while it reports only one segment. The face below $s_b$ also has the 6 extra vertices $x = 0, 3, 7, 11, 15, 16$ on its top side once the face above is repaired.

The combing step at $s_m$ extends every other edge, at $x = 3, 7, 11, 15$, down to $s_b$. This splits the bad face into $[0,3]$, $[3,7]$, $[7,11]$, $[11,15]$ and $[15,16]$ (times $[0, 5]$), whose top sides have the single extra vertices $1$, $5$, $9$, $13$ and none. The step at $s_b$ then extends the edges at $x = 3, 11, 16$ down to $-\infty$, which leaves the faces $[-1, 3]$, $[3, 11]$, $[11, 16]$ and $[16, 17]$ below $s_b$ with one extra vertex each at most ($0$, $7$, $15$ and none). No face has an extra vertex on a lower side, so the result is a hive graph with 7 more vertical edges than $G(S)$.

**The vertical adjacency map itself.** If no face of $G(S)$ has two extra vertices on one horizontal side, then $G(S)$ is already a hive graph. This holds for a set of segments with pairwise disjoint $x$-ranges, since then no vertical edge ends on a segment from above or below.

**Non-example: the trapezoidal map.** The [trapezoidal map](/trapezoidal-map/) of the same segments is the vertical adjacency map, so in the example above it is not a hive graph. It supports point location, but a walk along a vertical query can take time linear in $n$ with no output.

**Non-example: a full refinement.** Extending every vertical edge through every segment until it meets nothing gives faces with no extra vertices at all, but it can have $\Theta(n^2)$ vertices: $n/2$ long segments stacked over each other and $n/2$ short segments above them send $n$ vertical lines through about $n/2$ segments each. The hive graph keeps only every other edge at each level, so it stays linear.

## Related definitions

- [Orthogonal segment intersection](/orthogonal-segment-intersection/): the reporting problem that the hive graph solves.
- [Catalog graph](/catalog-graph/) and [fractional cascading bridge](/fractional-cascading-bridge/): the general form of the sampling idea, by Chazelle and Guibas.
- [Multiple list search](/multiple-list-search/): the problem of locating one key in many sorted lists. A vertical query in the hive graph locates its $x$-coordinate among the vertical edges on each segment it crosses.
- [Planar point location](/planar-point-location/) and [vertical ray shooting](/vertical-ray-shooting/): the first step of the query.
- [Orthogonal point enclosure](/orthogonal-point-enclosure/): rectangle stabbing in the plane, for which Chazelle also used the hive graph to reach $O(n)$ space and $O(\log n + k)$ query time.

## References
