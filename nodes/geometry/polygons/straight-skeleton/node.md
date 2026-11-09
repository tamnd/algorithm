---
tag: 53FE21
kind: concept
slug: straight-skeleton
name: Straight skeleton
aliases:
- straight skeleton of polygon
- angular bisector network
- roof model of a polygon
area: geometry/polygons
level: research
summary: A roof-like skeleton of a polygon formed by inward wavefront propagation of edges at constant speed.
prereqs: [simple-polygon, medial-axis]
see_also: [medial-axis, voronoi-diagram, offset-curve, polygon-with-holes, convex-polygon, euler-formula]
sources:
  - paper: doi:10.3217/jucs-001-12-0752
    title: Oswin Aichholzer, Franz Aurenhammer, David Alberts and Bernd Gärtner, A novel type of skeleton for polygons, Journal of Universal Computer Science 1(12), 752 to 761 (1995)
    locator: the whole paper (the wavefront definition, edge and split events, the tree structure with n − 2 nodes and 2n − 3 arcs, the roof interpretation, and a wavefront simulation algorithm)
  - paper: "David Eppstein and Jeff Erickson, Raising roofs, crashing cycles, and playing pool: applications of a data structure for finding pairwise interactions, Discrete and Computational Geometry 22(4), 569 to 592 (1999)"
    locator: the first subquadratic algorithm for the straight skeleton, and its reduction to motorcycle graphs
  - paper: "Siu-Wing Cheng and Antoine Vigneron, Motorcycle graphs and straight skeletons, Algorithmica 47(2), 159 to 182 (2007)"
    locator: the randomized algorithm through the motorcycle graph of the reflex vertices
  - paper: "Alok Aggarwal, Leonidas J. Guibas, James Saxe and Peter W. Shor, A linear-time algorithm for computing the Voronoi diagram of a convex polygon, Discrete and Computational Geometry 4, 591 to 604 (1989)"
    locator: the medial axis of a convex polygon in O(n) time, which is also its straight skeleton
---

The straight skeleton of a [simple polygon](/simple-polygon/) is the set of paths traced by its vertices when every edge moves inward, parallel to itself, at the same constant speed. As the edges move, the polygon shrinks, edges shorten and vanish, and reflex corners run into the far side and split the polygon in two; the process ends when nothing is left. For a polygon with $n$ vertices in general position the result is a tree of straight segments with the $n$ vertices as leaves, $n - 2$ inner nodes and $2n - 3$ arcs. It was introduced by Aichholzer, Aurenhammer, Alberts and Gärtner in 1995 as a straight-line alternative to the [medial axis](/medial-axis/), which has curved arcs near reflex vertices. Lifting each point to the time at which the wavefront reaches it gives a roof over the polygon with all faces at the same slope, which is how hip roofs are designed.

## In plain words

Pour water around a flat island and let it rise, so that every straight piece of the coast moves inward at the same speed and stays straight. The corners of the coast slide along lines that split their angles in half. When a short piece of coast shrinks to nothing, its two neighbors meet. When a corner that points into the island reaches the coast on the other side, the island splits into two islands.

Draw the path of every corner on the map until the island is gone. These paths form the straight skeleton. It looks like the ridges of a roof seen from above: each piece of coast gets one roof face, and all faces are equally steep. Unlike the classic skeleton made of the centers of the largest circles that fit inside, it uses only straight lines.

## The idea

Let $P$ be a simple polygon with edges $e_0, \ldots, e_{n-1}$ in counterclockwise order. At time $t \ge 0$, the **wavefront** $P(t)$ is the polygon whose edges lie on the lines of the edges of $P$, each moved inward by distance $t$, with the combinatorics updated by the events below. Between events, each vertex of $P(t)$ moves on the bisector of the angle between its two edges, with speed $1/\sin(\alpha/2)$ for the interior angle $\alpha$; reflex vertices, where $\alpha > \pi$, move into the interior as well.

- **Edge event.** An edge of the wavefront shrinks to length 0. Its two end points meet, and the two neighboring edges become adjacent.
- **Split event.** A reflex vertex reaches the interior of an edge of the wavefront that is not its neighbor. The wavefront splits into two polygons, which then shrink on their own.

The process stops when every part has vanished. The **straight skeleton** $S(P)$ is the union of the segments traced by the wavefront vertices; its **nodes** are the events and its **arcs** are the traced segments. Each edge $e_i$ sweeps a **face** $f(e_i)$, the set of points that the moving copy of $e_i$ passes over.

**Facts proved by Aichholzer et al.** Each face $f(e_i)$ is connected and is bounded by $e_i$ and a path in $S(P)$ between the ends of $e_i$; the faces of all edges partition $P$. With this, Euler's formula gives the counts. Consider the plane graph whose vertices are the $n$ polygon vertices and the $I$ skeleton nodes, and whose edges are the $n$ polygon edges and the $A$ arcs. It has $n + 1$ faces, the $n$ faces $f(e_i)$ and the outside, so by [Euler's formula](/euler-formula/)

$$(n + I) - (n + A) + (n + 1) = 2, \qquad A = n + I - 1.$$

So the skeleton, a connected graph with $n + I$ vertices and $n + I - 1$ arcs, is a tree. In general position every node has degree 3 and every polygon vertex is a leaf, so $n + 3I = 2A = 2(n + I - 1)$, which gives $I = n - 2$ inner nodes and $A = 2n - 3$ arcs.

**The roof.** Lift each point $q \in P$ to the height $t(q)$ at which the wavefront reaches it. Inside the face $f(e_i)$, the point was reached by the copy of $e_i$, so $t(q)$ is the distance from $q$ to the line of $e_i$, and the lifted face is a plane piece at slope $45°$. The surface is a roof whose ridges and valleys project to the arcs of $S(P)$. In a nonconvex polygon, $t(q)$ is in general larger than the distance from $q$ to $\partial P$, since near a reflex vertex the vertex is nearer than any edge line.

**Convex polygons.** For a [convex polygon](/convex-polygon/), the distance from an interior point to $\partial P$ is the smallest distance to an edge line, so $P(t) = \{q : d(q, \partial P) \ge t\}$, the wavefront has only edge events, and $S(P)$ is the set of points with two or more nearest edges: the straight skeleton equals the medial axis. For nonconvex polygons they differ. The medial axis has parabolic arcs, of points equidistant from a reflex vertex and an edge, while the skeleton has a straight arc from each reflex vertex.

**Wavefront and offsets.** $P(t)$ is the mitered inward offset of $P$ by $t$: the offset whose corners stay sharp, as opposed to the rounded offset $\{q : d(q, \partial P) \ge t\}$ given by the medial axis. Outward offsets are the wavefront of the outside, and give the exterior skeleton.

**Degenerate input.** Several events can happen at one time and place, for example two reflex vertices meeting each other (a vertex event) or edges that collapse together, as in a rectangle. Then nodes have degree more than 3, which counts as several degree 3 nodes joined by arcs of length 0. Parallel edges that meet head on need a rule, since their moving lines coincide.

**Algorithms and known bounds.**

| setting | time | source |
| --- | --- | --- |
| general, simulation of the wavefront | $O(n^2 \log n)$ | Aichholzer et al., 1995 |
| general, first subquadratic | $O(n^{17/11 + \varepsilon})$ | Eppstein and Erickson, 1999 |
| simple polygons with $r$ reflex vertices, randomized | $O(n \log^2 n + r^{3/2} \log r)$ | Cheng and Vigneron, 2007 |
| convex polygons | $O(n)$ | through the medial axis, Aggarwal et al., 1989 |

The size of the output is $\Theta(n)$, which is the only lower bound stated here. The difficulty is the split events: the edge events alone can be simulated with a priority queue of collapse times in $O(n \log n)$ time, which already solves convex polygons. The split events are governed by the **motorcycle graph**, in which each reflex vertex rides along its bisector until it hits the track of another; Eppstein and Erickson and later Cheng and Vigneron reduce the skeleton to computing it.

## Examples

- **A triangle.** For $(0,0), (4,0), (0,3)$ the three bisectors meet at the incenter $(1,1)$, at time 1, the inradius. The skeleton has one node and three arcs, matching $n - 2 = 1$ and $2n - 3 = 3$.
- **A rectangle.** For $(0,0), (4,0), (4,2), (0,2)$ the four corners move along $45°$ bisectors. At time 1 both short edges shrink to points, at $(1,1)$ and $(3,1)$, and the two long edges meet along the segment between them, which is the ridge. The skeleton has the 2 nodes $(1,1)$ and $(3,1)$ and 5 arcs: four from the corners and the ridge. The faces of the long edges are trapezoids of area 3, those of the short edges are triangles of area 1, and $3 + 3 + 1 + 1 = 8$ is the area of the rectangle. The roof is a hip roof of height 1.
- **An L-shape.** For $(0,0), (4,0), (4,2), (2,2), (2,4), (0,4)$, with two arms of width 2, the reflex vertex $(2,2)$ moves toward $(1,1)$ at speed $\sqrt2$, and the corner $(0,0)$ moves to the same point. At time 1, the right arm collapses to $(3,1)$, the top arm to $(1,3)$, and the whole wavefront to the segments from $(1,1)$ to $(3,1)$ and to $(1,3)$. The skeleton has 8 arcs, the six from the vertices and these two ridges, and the node $(1,1)$ has degree 4, a degenerate case of the $2n - 3 = 9$ arcs in general position. The medial axis of this shape near $(2,2)$ is curved instead.

## Where it is used

- **Roof design.** The roof interpretation gives the hip roof over a building outline, with all faces at the same slope, and the weighted straight skeleton (edges at different speeds) gives roofs with different slopes.
- **Offsetting.** The mitered [offset curves](/offset-curve/) of a polygon at all distances are read off the skeleton, used for tool paths in machining and for shrinking or growing outlines.
- **Shape description.** Like the [medial axis](/medial-axis/), the skeleton is a thin graph that captures the shape of a region, for example the center lines of roads or rivers, without the curved arcs and with $O(n)$ straight segments.
- **Folding and cutting.** The fold-and-cut problem, folding a sheet of paper flat so that one straight cut produces a given polygon, has a solution based on the straight skeleton (Demaine, Demaine and Lubiw).
- **Terrains.** Lifting a polygon by its roof gives a terrain with prescribed slopes, and the faces of the skeleton cut the polygon into $n$ pieces, one per edge, each monotone in the direction of its edge.
- **Polygons with holes.** The definition works unchanged, with the wavefronts of the outer boundary and the holes moving into the region; the skeleton then has cycles around the holes.

## References
