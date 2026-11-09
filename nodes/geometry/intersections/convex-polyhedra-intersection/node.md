---
tag: B7DXSM
kind: problem
slug: convex-polyhedra-intersection
name: Intersection of convex polyhedra
aliases:
- convex-polytope-intersection
- intersection of two convex polyhedra
area: geometry/intersections
level: research
summary: Compute or test the intersection of two convex polyhedra in three dimensions; Chazelle computes it in linear time, and preprocessed polyhedra can be tested in polylogarithmic time.
prereqs: [convex-polytope, convex-polygon-intersection, half-plane-intersection]
see_also: [convex-hull-3d, convex-collision-detection, chazelle-dobkin-algorithm, gjk-algorithm, separating-axis-theorem, megiddo-fixed-dimension-lp, doubly-connected-edge-list, linear-programming-problem]
sources:
  - paper: doi:10.1016/0304-3975(78)90051-8
    title: David E. Muller and Franco P. Preparata, Finding the intersection of two convex polyhedra, Theoretical Computer Science 7(2), 1978
    locator: the O(n log n) algorithm that finds a common interior point and then reduces the intersection to a convex hull by polarity
  - paper: doi:10.1137/0221041
    title: Bernard Chazelle, An optimal algorithm for intersecting three-dimensional convex polyhedra, SIAM Journal on Computing 21(4), 1992
    locator: the O(n) time algorithm using hierarchical representations of the two polyhedra
  - paper: doi:10.1007/s00454-016-9785-3
    title: Timothy M. Chan, A simpler linear-time algorithm for intersecting two convex polyhedra in three dimensions, Discrete and Computational Geometry 56(4), 2016, 860-865
    locator: the simpler linear-time algorithm and its comparison with the method of Chazelle
  - paper: doi:10.1016/0304-3975(82)90120-7
    title: David P. Dobkin and David G. Kirkpatrick, Fast detection of polyhedral intersection, Theoretical Computer Science 27(3), 1983
    locator: the hierarchical representation of a convex polyhedron with O(log n) levels and the polylogarithmic intersection test
  - paper: doi:10.1145/7531.24036
    title: Bernard Chazelle and David P. Dobkin, Intersection of convex objects in two and three dimensions, Journal of the ACM 34(1), 1987
    locator: the logarithmic test for convex polygons and the polylogarithmic tests for convex polyhedra
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 7, Intersections, the intersection of convex polyhedra (the Muller-Preparata method)
---

The intersection of two convex polyhedra $P$ and $Q$ in $\mathbb{R}^3$ is again a convex polyhedron, possibly empty. The problem asks for its boundary, as a list of vertices, edges and faces, or only for a yes or no answer to whether $P$ and $Q$ meet. Muller and Preparata (1978) computed the intersection in $O(n \log n)$ time for $n$ total vertices by reducing it to a convex hull. Chazelle (1992) gave an optimal $O(n)$ algorithm, and Chan (2016) a simpler one. The test version can be much faster: with the hierarchical representation of Dobkin and Kirkpatrick, two preprocessed polyhedra in any relative position can be tested in polylogarithmic time.

## In plain words

Take two convex solids, like two stones without dents, and push them into each other. The part they share is again a convex solid. You want to know its corners, edges and flat sides, or only whether the two solids share any space at all.

One method finds a point inside both, then turns the problem inside out with a trick called polarity: the shared solid becomes the hull of all the corners of two other solids, and hulls are a known job. Better methods use a ladder of simpler and simpler copies of each solid and climb down the ladder. They find the shared part in time that grows only in proportion to the number of corners.

## Definition

**Input.** Two convex polyhedra $P$ and $Q$ in $\mathbb{R}^3$, each given by a boundary structure, for example a [doubly connected edge list](/doubly-connected-edge-list/) of its vertices, edges and faces. $n$ is the total number of vertices.

**Output.** *Construction:* the boundary structure of $P \cap Q$, or "empty". *Detection:* whether $P \cap Q \ne \emptyset$. Some versions ask for a separating plane or the distance when the polyhedra are disjoint.

**Notation.** By Euler's formula a convex polyhedron with $v$ vertices has at most $3v - 6$ edges and $2v - 4$ faces, so $n$ also bounds the numbers of edges and faces up to a constant. Every vertex of $P \cap Q$ is a vertex of $P$ inside $Q$, a vertex of $Q$ inside $P$, or a crossing of an edge of one with a face of the other.

**Model.** The [real RAM](/real-ram/). The sublinear tests assume that the preprocessed hierarchy of each polyhedron is stored with random access.

## Variants

- **Planar case.** Two convex polygons, solved in $O(n)$ time by [convex polygon intersection](/convex-polygon-intersection/), and tested in $O(\log n)$ time by the [Chazelle-Dobkin algorithm](/chazelle-dobkin-algorithm/).
- **Detection only.** The [convex collision detection](/convex-collision-detection/) problem in three dimensions.
- **Many polyhedra.** The intersection of $m$ convex polyhedra is the intersection of all their face half-spaces, a half-space intersection problem.
- **Half-space form.** If $P$ and $Q$ are given as sets of half-spaces, $P \cap Q$ is the intersection of all of them; without the boundary structures this needs $\Omega(n \log n)$ in general.
- **Higher dimensions.** In $\mathbb{R}^d$ for $d \ge 4$ the output can be much larger than the input, and the problem becomes a general half-space intersection.

## Examples

**Two cubes.** $[0, 2]^3 \cap [1, 3]^3 = [1, 2]^3$. Its 8 vertices are the vertex $(2, 2, 2)$ of the first cube, the vertex $(1, 1, 1)$ of the second cube, and 6 crossings of edges of one cube with faces of the other, such as $(2, 1, 1)$ on the edge $x \in [1, 3]$, $y = z = 1$ of the second cube and the face $x = 2$ of the first.

**Cube and octahedron.** $P = [0, 2]^3$ and $Q = \{x : |x_1 - 1| + |x_2 - 1| + |x_3 - 1| \le 3/2\}$, an octahedron with the same center whose 6 vertices stick out through the 6 faces of the cube. Each face of the cube cuts off a corner of $Q$: on the face $x_1 = 2$ the intersection is the square $|x_2 - 1| + |x_3 - 1| \le 1/2$, with 4 vertices. So $P \cap Q$ has $6 \cdot 4 = 24$ vertices, $36$ edges and $8 + 6 = 14$ faces (8 hexagons from the faces of $Q$ and 6 squares from the faces of $P$), and $24 - 36 + 14 = 2$ as Euler's formula requires. It is a truncated octahedron; its volume is $\operatorname{vol}(Q) - 6 \cdot \tfrac{1}{12} = \tfrac{9}{2} - \tfrac{1}{2} = 4$, since each cut-off corner is a square pyramid of height $1/2$ with a square base of area $1/2$.

**Disjoint.** $[0, 1]^3$ and the tetrahedron with vertices $(2, 2, 2), (3, 2, 2), (2, 3, 2), (2, 2, 3)$: the plane $x_1 + x_2 + x_3 = 4.5$ separates them, since the cube has $x_1 + x_2 + x_3 \le 3$ and the tetrahedron has $x_1 + x_2 + x_3 \ge 6$.

## Known algorithms

**Brute force.** Clip $P$ by each face plane of $Q$ in turn, like the [Sutherland-Hodgman](/sutherland-hodgman/) method in three dimensions; each clip costs $O(n)$, so the total is $O(n^2)$.

**Muller and Preparata (1978).** First find a point $o$ in the interior of $P \cap Q$, or report that there is none. With $o$ as the origin, polarity maps each face plane of $P$ and $Q$ to a point, and $P \cap Q$ to the polar of the [convex hull](/convex-hull-3d/) of these points. A 3D hull takes $O(n \log n)$ time, which gives $O(n \log n)$ in total. The interior point can also be found by [linear programming](/megiddo-fixed-dimension-lp/) in $O(n)$ time.

**Chazelle (1992).** Using the Dobkin-Kirkpatrick hierarchies of both polyhedra, the algorithm builds the intersection from the coarsest levels down to the finest, and each step does work proportional to the size of a level. The level sizes decrease geometrically, so the total time is $O(n)$, which is optimal.

**Chan (2016).** A simpler linear-time algorithm, also based on hierarchies of the two polyhedra, with a short proof that avoids most of the case analysis of Chazelle's method.

**Detection with hierarchies.** Dobkin and Kirkpatrick (1983) preprocess each polyhedron in $O(n)$ time into a sequence of $O(\log n)$ nested polyhedra, each obtained by removing an independent set of low-degree vertices, and test two such polyhedra for intersection in polylogarithmic time. Chazelle and Dobkin (1987) give polylogarithmic tests by a different search. For detection without preprocessing, linear programming or [GJK](/gjk-algorithm/) take $O(n)$ time.

## Bounds

The construction needs $\Omega(n)$ time, since the output can have $\Theta(n)$ vertices and the input must be read, so Chazelle's $O(n)$ bound is optimal. The Muller-Preparata bound $O(n \log n)$ is optimal for the more general problem of intersecting $n$ half-spaces, which includes sorting, but the boundary structures of $P$ and $Q$ make the special case easier. The test with preprocessing breaks the linear bound: after $O(n)$ preprocessing, a query between two polyhedra in any relative position takes polylogarithmic time, and the logarithmic factors have been reduced in later work.

## Reductions

- **To half-space intersection.** $P \cap Q$ is the intersection of the $O(n)$ face half-spaces of $P$ and $Q$.
- **To convex hull by polarity.** With an interior point as origin, half-space intersection is dual to the convex hull of the polar points, which is the Muller-Preparata reduction.
- **To linear programming.** Detection, and finding an interior point, are linear programs in three variables.
- **From the planar case.** Two prisms over convex polygons intersect in the prism over the intersection of the polygons, so the 3D problem contains the 2D one.

## Applications

- **Solid modeling.** Boolean operations on convex parts, and on unions of convex pieces.
- **Collision detection and robotics.** Interference and distance tests between convex hulls of robot links and obstacles.
- **Computational geometry.** A step in divide-and-conquer methods for 3D convex hulls and for the intersection of many half-spaces, where two partial results are merged.
- **Linear programming.** The feasible region of two constraint sets is the intersection of their polyhedra.

## References
