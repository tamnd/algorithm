---
tag: 2PAHW7
kind: problem
slug: convex-collision-detection
name: Convex collision detection
aliases:
- convex-polytope-overlap-test
- convex overlap test
area: geometry/intersections
level: advanced
summary: Decide whether two convex polygons or polytopes overlap, and often also compute their distance or a separating plane; linear time is easy and logarithmic time is possible with arrays.
prereqs: [separating-axis-theorem, minkowski-sum, convex-polygon-intersection]
see_also: [gjk-algorithm, chazelle-dobkin-algorithm, convex-polyhedra-intersection, collision-detection, bounding-volume-hierarchy, seidel-linear-programming, megiddo-fixed-dimension-lp, rotating-calipers]
sources:
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 5, Section 5.2.1, Separating-axis test, and Chapter 9, Convexity-based methods (linear programming, the GJK algorithm and the hierarchical polyhedron representation)
  - paper: doi:10.1016/0146-664X(82)90023-5
    title: Joseph O'Rourke, Chi-Bin Chien, Thomas Olson and David Naddor, A new linear algorithm for intersecting convex polygons, Computer Graphics and Image Processing 19(4), 1982
    locator: the linear-time advance rule on the two boundaries, which also decides whether the polygons meet
  - paper: doi:10.1145/7531.24036
    title: Bernard Chazelle and David P. Dobkin, Intersection of convex objects in two and three dimensions, Journal of the ACM 34(1), 1987
    locator: the O(log n) test for two convex polygons given as vertex arrays, and the polylogarithmic tests for polyhedra
  - paper: doi:10.1016/0304-3975(82)90120-7
    title: David P. Dobkin and David G. Kirkpatrick, Fast detection of polyhedral intersection, Theoretical Computer Science 27(3), 1983
    locator: the hierarchical representation of a convex polyhedron and the polylogarithmic intersection test of two preprocessed polyhedra
  - paper: doi:10.1109/56.2083
    title: Elmer G. Gilbert, Daniel W. Johnson and S. Sathiya Keerthi, A fast procedure for computing the distance between complex objects in three-dimensional space, IEEE Journal of Robotics and Automation 4(2), 1988
    locator: the distance algorithm on the Minkowski difference with support mappings
---

Convex collision detection asks whether two convex objects, usually convex polygons in the plane or convex polyhedra in space, have a common point. Because the objects are convex, the answer has short certificates: a common point if they meet, and a separating line or plane if they do not, by the [separating axis theorem](/separating-axis-theorem/). The problem is the inner step of physics engines, robot motion planners and CAD checks, where it runs millions of times, so the algorithms aim at constant work per test in practice. The classical bounds are linear time for two polygons given by their vertex lists, and logarithmic time when the vertices are in arrays that allow random access.

## In plain words

Two convex shapes either share some space, or you can slide a flat sheet between them. A convex shape has no dents, so the sheet always fits if they do not touch. Collision detection is the job of finding out which case you have.

A program can check a short list of directions and look for a gap between the shadows of the two shapes. It can also walk along the two outlines at the same time. A third way searches a combined shape, made of all the differences of a point of one shape and a point of the other, for the zero point. Shapes that touch at a single point count as meeting.

## Definition

**Input.** Two convex sets $P, Q \subset \mathbb{R}^d$, usually with $d = 2$ or $3$, each given as a convex polygon by its vertices in counterclockwise order, as a convex polyhedron by a boundary structure, or as a finite point set whose convex hull is meant.

**Output.** "Yes" if $P \cap Q \ne \emptyset$, and "no" otherwise. Many versions also ask for a witness: a common point, or a separating hyperplane $\{x : u \cdot x = t\}$ with $u \cdot p < t < u \cdot q$ for all $p \in P$, $q \in Q$; or for the distance $\min |p - q|$ and the penetration depth.

**Notation.** $m$ and $k$ are the numbers of vertices of $P$ and $Q$, and $n = m + k$. $P - Q = \{p - q\}$ is the Minkowski difference; $P \cap Q \ne \emptyset$ if and only if $0 \in P - Q$.

**Model.** The [real RAM](/real-ram/) with exact predicates. Sublinear bounds assume that the vertices of a polygon are stored in an array, so that the $i$-th vertex can be read in $O(1)$ time.

## Variants

- **Boolean test or witness.** The witness is a common point or a separating axis; a stored axis can be tried first in the next time step.
- **Distance.** For disjoint objects compute $\min |p - q|$ and the closest pair; for overlapping objects compute the penetration depth, the length of the shortest translation that makes them disjoint.
- **Static or preprocessed.** With preprocessing of each object alone, such as the hierarchy of Dobkin and Kirkpatrick, later tests between any two objects in any position can be fast.
- **Moving objects.** Continuous collision detection asks for the first time of contact along given motions.
- **Many objects.** A broad phase with [bounding boxes](/axis-aligned-bounding-box/) or a [bounding volume hierarchy](/bounding-volume-hierarchy/) picks candidate pairs, and this problem is the narrow phase for each pair.
- **Computing the intersection.** Computing the shape $P \cap Q$ itself is [convex polygon intersection](/convex-polygon-intersection/) or [convex polyhedra intersection](/convex-polyhedra-intersection/).

## Examples

Let $P$ be the triangle $(0, 0), (4, 0), (0, 4)$.

| $Q$ | axis $u = (1, 1)$: $P$ | axis $u = (1, 1)$: $Q$ | answer |
| --- | --- | --- | --- |
| $(3, 3), (5, 3), (3, 5)$ | $[0, 4]$ | $[6, 8]$ | disjoint, $u$ separates |
| $(2, 2), (4, 2), (2, 4)$ | $[0, 4]$ | $[4, 6]$ | touching at $(2, 2)$ |
| $(1, 1), (3, 1), (1, 3)$ | $[0, 4]$ | $[2, 4]$ | overlapping |

In the first row the edge normal $(1, 1)$ of the hypotenuse $x + y = 4$ of $P$ gives the gap from $4$ to $6$, so the line $x + y = 5$ separates. In the second row the intervals share only the value $4$, and the vertex $(2, 2)$ of $Q$ is on the hypotenuse, so the closed triangles meet with depth $0$. In the third row the vertex $(1, 1)$ of $Q$ is inside $P$, and no edge normal of $P$ or $Q$ shows a gap; the smallest overlap is $2 / \sqrt{2} = \sqrt{2}$ along $(1, 1)$, which is the penetration depth.

## Known algorithms

**Separating axis test.** For polygons, try the $n$ edge normals and project both polygons on each, in $O(n^2)$ total, or in $O(n)$ with a merged angular walk over the normals as in [rotating calipers](/rotating-calipers/). For two boxes in 3D, 15 axes suffice. This is the common method for small polygons and for boxes.

**Boundary walk.** The algorithm of O'Rourke, Chien, Olson and Naddor (1982) walks along both boundaries with an advance rule and finds a crossing or a containment in $O(n)$ time. It decides the problem and computes $P \cap Q$ in the same pass.

**Linear programming.** A common point is a feasible point of the $m + k$ half-plane constraints of $P$ and $Q$, and a separating line is a feasible point of a dual system. In fixed dimension, [Megiddo's method](/megiddo-fixed-dimension-lp/) or [Seidel's randomized method](/seidel-linear-programming/) solve it in $O(n)$ time, even when the input is two unordered point sets and the hulls are not known.

**Logarithmic search for polygons.** Chazelle and Dobkin (1987) test two convex polygons given as vertex arrays in $O(\log m + \log k)$ time, by a [prune-and-search](/prune-and-search/) on the two boundaries that discards a constant fraction of one chain in each step; see the [Chazelle-Dobkin algorithm](/chazelle-dobkin-algorithm/).

**Hierarchies for polyhedra.** Dobkin and Kirkpatrick (1983) store a convex polyhedron as a sequence of nested simpler polyhedra with $O(\log n)$ levels and test two such polyhedra in polylogarithmic time; Chazelle and Dobkin give polylogarithmic bounds as well.

**GJK.** The [Gilbert-Johnson-Keerthi algorithm](/gjk-algorithm/) (1988) uses only the support functions of the two objects and walks a simplex in $P - Q$ toward the origin. It computes the distance and works for any convex shapes with a support function, such as polytopes, spheres and capsules, which makes it the standard narrow-phase method in physics engines.

## Bounds

For two unordered point sets of total size $n$, any algorithm must read every point, so $\Omega(n)$ time is needed, and linear programming gives $O(n)$ in fixed dimension: the bound is $\Theta(n)$. For two convex polygons stored as arrays, the Chazelle-Dobkin method takes $O(\log n)$ time, so the input does not need to be read in full. For preprocessed polyhedra the time is polylogarithmic in the number of vertices. In practice the work per test is often $O(1)$, because a stored separating axis or the last GJK simplex is still valid in the next frame.

## Reductions

- **To a point test.** $P \cap Q \ne \emptyset$ if and only if $0 \in P - Q$, and the [Minkowski sum](/minkowski-sum-convex-polygons/) of two convex polygons has at most $m + k$ edges and is computable in $O(n)$ time.
- **To linear programming.** Feasibility of the $m + k$ inequalities of $P$ and $Q$ is a linear program in $d$ variables.
- **From point in convex polygon.** If $Q$ is a single point, the problem is to locate the point against the convex polygon $P$, so any lower bound for that test applies.
- **To distance computation.** The objects meet if and only if their distance is $0$; GJK solves the distance problem and gets the decision as a special case.

## Applications

- **Physics engines and games.** Rigid bodies are convex hulls or unions of convex pieces, and the narrow phase runs this test for every candidate pair in every frame.
- **Robotics.** Motion planners check a robot model against obstacles at many configurations, and distance queries give the clearance.
- **Computer-aided design.** Interference checks of parts in an assembly, often on convex decompositions.
- **Computational geometry.** A step of algorithms for polygon separability, for [convex hull](/convex-hull/) merging and for linear separability of two point classes.

## References
