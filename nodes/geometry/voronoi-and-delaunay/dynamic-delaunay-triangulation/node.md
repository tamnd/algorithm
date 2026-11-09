---
tag: C56FEE
kind: problem
slug: dynamic-delaunay-triangulation
name: Dynamic Delaunay triangulation
aliases:
- dynamic Voronoi diagram
- fully dynamic Delaunay triangulation
- Delaunay triangulation with insertions and deletions
area: geometry/voronoi-and-delaunay
level: advanced
summary: Maintain the Delaunay triangulation under point insertions and deletions.
prereqs: [delaunay-triangulation, delaunay-triangulation-construction, edge-flip, in-circle-test]
see_also: [bowyer-watson-algorithm, lawson-flip-algorithm, randomized-incremental-construction, backwards-analysis, triangle-walk-point-location, planar-point-location, voronoi-diagram-construction, local-delaunay-criterion]
sources:
  - paper: doi:10.1007/BF01758770
    title: L. J. Guibas, D. E. Knuth and M. Sharir, Randomized incremental construction of Delaunay and Voronoi diagrams, Algorithmica 7, 1992
    locator: insertion by flips, the history DAG for point location, and the O(n log n) expected total time in random order
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Sections 9.3 and 9.4 (insertion with flips, the history structure and the expected number of structural changes)
  - paper: "O. Devillers, The Delaunay hierarchy, International Journal of Foundations of Computer Science 13(2), 2002"
    locator: the hierarchy of random samples for point location and its expected O(log n) query time
  - paper: "L. P. Chew, Building Voronoi diagrams for convex polygons in linear expected time, Technical Report PCS-TR90-147, Dartmouth College, 1990"
    locator: the randomized retriangulation of the hole left by a deleted point in expected time linear in its degree
---

The dynamic Delaunay triangulation problem asks to keep the [Delaunay triangulation](/delaunay-triangulation/) of a changing set $P$ of points in the plane, under insertions and deletions of points, so that after each operation the triangulation, or its dual Voronoi diagram, is correct. An insertion finds the triangle that holds the new point and repairs the triangulation around it with [edge flips](/edge-flip/) or a cavity; a deletion removes the triangles of the point and fills the hole. One operation can change $\Theta(n)$ triangles in the worst case, but in a random order of insertions the expected change is $O(1)$ per insertion, and with a good point location structure the expected time is $O(\log n)$ per insertion.

## In plain words

You keep a set of dots joined into Delaunay triangles, and dots come and go. When a new dot arrives, find the triangle it falls in. Every triangle whose circle now holds the new dot is wrong, and these wrong triangles form one connected hole around the new dot. Join the new dot to the rim of the hole.

When a dot leaves, its triangles go with it and leave a hole shaped like a star around the place where it was. Fill the hole with new triangles that pass the empty circle test.

Most of the time only a few triangles change. The slow part is often to find where the new dot falls.

## Definition

**State.** A finite set $P$ of $n$ distinct points $p = (x, y)$, usually with integer or rational coordinates, and a Delaunay triangulation $T$ of $P$, stored with adjacency, for example as a [quad-edge structure](/quad-edge-data-structure/).

**Operations.**

1. $\mathrm{insert}(q)$ for $q \notin P$: change $T$ into a Delaunay triangulation of $P \cup \{q\}$.
2. $\mathrm{delete}(q)$ for $q \in P$: change $T$ into a Delaunay triangulation of $P \setminus \{q\}$.
3. Often also $\mathrm{locate}(x)$: return the triangle of $T$ that holds the point $x$, or the nearest point of $P$ to $x$.

Notation: $n = |P|$, $h$ is the number of points on the boundary of the convex hull, $k$ is the degree of the inserted or deleted point after or before the operation, $\mathrm{orient}(a, b, c)$ is positive for a counterclockwise turn, and $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside their circle.

**What changes.** After $\mathrm{insert}(q)$, the triangles of $T$ whose open circumdisc holds $q$ are exactly the triangles that are removed; they form a star-shaped region around $q$, and the new triangles are the ones that join $q$ to the boundary edges of that region ([Bowyer-Watson](/bowyer-watson-algorithm/)). So the number of changed triangles is $\Theta(k)$, where $k$ is the degree of $q$ in the new triangulation. Deletion is the reverse: the $k$ triangles around $q$ are removed and the star-shaped polygon they leave is triangulated by a Delaunay triangulation of its $k$ vertices; that is the same as the triangles of the new triangulation inside the polygon.

**Degenerate input.** With four or more points on one empty circle the triangulation is not unique. Operations that use the strict in-circle test keep one of the Delaunay triangulations, so after a deletion and a new insertion of the same point the triangulation can differ from the one before, while still being Delaunay. Points on the hull with collinear neighbours need care in insertion outside the hull; many programs add three far points or a point at infinity to avoid it.

## Variants

- **Semi-dynamic, insertions only.** The randomized incremental method: insert all points in a random order. This is the usual way to build the triangulation in $O(n \log n)$ expected time.
- **Deletions only.** Remove points from a known triangulation, for example in mesh simplification.
- **Kinetic.** The points move continuously, and the triangulation is fixed by flips at the moments when four points become cocircular; the number of such events depends on the motion.
- **Constrained.** Insert and delete points and segments in a [constrained Delaunay triangulation](/constrained-delaunay-triangulation/).
- **Weighted and higher-dimensional.** The same operations in a [regular triangulation](/regular-triangulation/) or in [higher dimensions](/higher-dimensional-delaunay/); in a regular triangulation an inserted point can be hidden and change nothing.

## Examples

- **A point in a square.** $P = \{(0,0), (4,0), (4,3), (0,3)\}$ is cocircular, and $T$ uses one diagonal. Inserting $(2,1)$ removes both triangles, because $(2,1)$ is strictly inside the common circle, and creates the $4$ triangles from $(2,1)$ to the four sides. Deleting $(2,1)$ again leaves the square as the hole, and either diagonal is a correct answer.
- **A center point.** Let $P$ be the $12$ points of the circle $x^2 + y^2 = 25$ with integer coordinates. Every triangulation of them is Delaunay, with $10$ triangles. Inserting $(0, 0)$ removes all $10$ triangles and adds $12$, one for each side of the polygon, so one insertion changes $\Theta(n)$ triangles when the same pattern is used with more points on a circle.
- **A far point.** Inserting a point far outside the hull of $n$ points makes new triangles with the hull edges it sees, and can also remove triangles near the hull whose circles are large.

## Known algorithms

| method | time per operation | kind of bound | notes |
| --- | --- | --- | --- |
| insertion with flips (Lawson) or with a cavity (Bowyer-Watson) | $O(k)$ after location | worst case | $k$ can be $\Theta(n)$ |
| point location by a walk from the last triangle | $O(n)$ | worst case | simple; fast when points arrive in spatial order; see [triangle walk](/triangle-walk-point-location/) |
| random order with the history DAG (Guibas, Knuth and Sharir) | $O(\log n)$ | expected, random order | insertions only; total $O(n \log n)$ expected, by [backwards analysis](/backwards-analysis/) |
| jump and walk (Mücke, Saias and Zhu) | $O(n^{1/3})$ for location | expected, uniform random points | walk from the nearest of about $n^{1/3}$ sampled points |
| Delaunay hierarchy (Devillers) | $O(\log n)$ for location | expected over the random levels | supports insertions and deletions |
| deletion by repeated ear flips or by a full Delaunay of the hole | $O(k^2)$ or $O(k \log k)$ | worst case | the hole is star-shaped with $k$ vertices |
| deletion by Chew's randomized method | $O(k)$ | expected | Chew's method for the Delaunay triangulation of a convex polygon, applied to the hole |

The expected bound of $O(1)$ structural change per insertion in random order holds for any point set in general position: when the $i$-th point is inserted, it is a random one of the $i$ points present, and the sum of the degrees in a triangulation of $i$ points is less than $6i$, so its expected degree is less than $6$. This is the core of the analysis of [randomized incremental construction](/randomized-incremental-construction/).

## Bounds

- **Change per operation.** $\Theta(n)$ triangles can change in one operation, as in the center point example, so no method has $o(n)$ worst-case time per operation when the triangulation is kept explicitly.
- **Lower bound for insertions.** $n$ insertions followed by a walk over the result sort $n$ numbers placed on a parabola, so in the [algebraic decision tree](/algebraic-decision-tree/) model the insertions need $\Omega(n \log n)$ time in total, that is $\Omega(\log n)$ amortized per insertion ([Voronoi construction lower bound](/voronoi-construction-lower-bound/)).
- **Upper bounds.** Random-order insertions match this bound in expectation. For a bad order the total structural change can be quadratic: inserting the points $(k, k^2)$ in decreasing order of $k$ removes about $n^2/2$ triangles in total for $n = 50, 100, 200$. This is observed with the [Bowyer-Watson](/bowyer-watson-algorithm/) code, not proved here.
- **Nearest neighbour queries only.** If the triangulation itself is not needed, data structures for dynamic nearest neighbour queries reach polylogarithmic amortized time per operation, by working with the lifted 3D convex hull; this is a different problem.

## Reductions

- **To and from the dynamic Voronoi diagram.** Every change of the triangulation is a change of the dual diagram of the same size ([duality](/voronoi-delaunay-duality/)), so the two problems are the same.
- **To the dynamic lower convex hull in 3D.** By the [lifting map](/paraboloid-lifting-map/), insertion and deletion of points in the plane are insertion and deletion of points on the paraboloid, and the Delaunay triangulation is the lower hull.
- **Static construction.** $n$ insertions build the triangulation; in random order this is the standard $O(n \log n)$ expected method.

## Applications

- **Mesh generation and refinement.** [Delaunay refinement](/delaunay-refinement/) and [Ruppert's algorithm](/ruppert-algorithm/) insert circumcenters one by one into a constrained Delaunay triangulation.
- **Mesh simplification.** Deletion of points from terrain models.
- **Simulation.** Particle methods and moving meshes keep the Delaunay triangulation of points that move, with kinetic flips or with deletions and new insertions.
- **Interactive geometry.** Editors and geographic systems that add and remove sites and show the Voronoi diagram at once.

## References
