---
tag: PQTB3Y
kind: algorithm
slug: lin-canny-closest-features
name: Lin-Canny closest features algorithm
aliases:
- Lin-Canny algorithm
area: graphics-and-signals/rigid-body-simulation
level: advanced
summary: Track the closest pair of features of two convex polyhedra by walking Voronoi regions. Under coherent motion a call takes few steps, which is observed, not proved.
solves: [convex-collision-detection]
model: real-ram
complexity:
  vars: {n: the number of vertices of A, m: the number of vertices of B, s: the number of moves of one call}
  time: {call: O(s (n + m)), moves_worst: O(n m), step: O(1)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, recursive: false, exact: true}
history:
  year: 1991
  people: [Ming C. Lin, John F. Canny]
  note: Lin and Canny gave the closest feature walk for convex polyhedra at ICRA 1991. It became the narrow phase of I-COLLIDE (1995), and Mirtich's V-Clip (1998) fixed its problems with penetration and degenerate cases.
prereqs: [convex-polygon, point-to-segment-distance, voronoi-diagram]
see_also: [v-clip, gjk-algorithm, convex-collision-detection, sweep-and-prune, conservative-advancement, separating-axis-theorem, rotating-calipers, minkowski-sum]
sources:
  - paper: doi:10.1109/ROBOT.1991.131723
    title: Ming C. Lin and John F. Canny, A fast algorithm for incremental distance calculation, Proceedings of the 1991 IEEE International Conference on Robotics and Automation, 1008 to 1014
    locator: the features of a convex polyhedron, their Voronoi regions, the closest feature test, and the walk to a neighboring feature
  - paper: doi:10.1145/199404.199437
    title: Jonathan D. Cohen, Ming C. Lin, Dinesh Manocha and Madhav K. Ponamgi, I-COLLIDE, an interactive and exact collision detection system for large-scale environments, Proceedings of the 1995 Symposium on Interactive 3D Graphics, 189 to 196
    locator: the use of the closest feature walk with coherence as the exact test after sweep and prune
  - paper: doi:10.1145/285857.285860
    title: Brian Mirtich, V-Clip, fast and robust polyhedral collision detection, ACM Transactions on Graphics 17(3), 1998, 177 to 208
    locator: the discussion of the Lin-Canny algorithm, its tolerances, and its behavior when the polyhedra penetrate
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 9, Convex-based Methods (the closest-features algorithms)
---

The Lin-Canny algorithm finds the closest pair of features of two disjoint convex polyhedra. A feature is a vertex, an edge or a face. Each feature has a Voronoi region: the set of points outside the polyhedron whose closest point on it lies on that feature. Two features are a closest pair exactly when each one's closest point to the other lies in the other's region. The algorithm starts from the pair of the last time step, and while a test fails it moves to a neighboring feature that is closer. When objects move a little per step, the old pair is right or nearly right, and a call takes very few moves.

## In plain words

Two convex objects float near each other, and you want to know how near they are. Each corner, side and face of an object owns a zone of space around it: the points that are closest to that corner, side or face.

Pick one part of each object, maybe the pair you found a moment ago. Look at where the other part sits. If it is in the zone of your part, your part is the right one. If it is not, it has left the zone through one wall of it, and the neighbor on the other side of that wall is closer. Move to that neighbor and look again.

Each move makes the two parts closer, so the walk cannot go in circles. When the objects move slowly, the walk from the last answer is usually zero or one move long.

## The problem

The input is two convex polygons $A$ and $B$ with $n$ and $m$ vertices, strictly convex and in counterclockwise order, and a start pair of features $(f_A, f_B)$. This page works in 2D, where the features are the vertices and the closed edges. The method in the 1991 paper is for convex polyhedra in 3D, with faces as a third kind of feature. The output is a pair of features and points $p \in f_A$, $q \in f_B$ with $|p - q| = d(A, B)$, the distance between the polygons. The method needs $A \cap B = \emptyset$. The version here also detects and reports an intersection, but it does not measure it; see [penetration depth](/penetration-depth/).

The Voronoi regions in 2D are simple. For a vertex $a$ with neighbors $a^-$ and $a^+$, the region is the wedge between the outward normals of its two edges, bounded by the two lines through $a$ perpendicular to its edges. For an edge $e = [e_0, e_1]$ with outward normal $n_e$, the region is the half strip on the outer side of $e$, between the two lines through $e_0$ and $e_1$ perpendicular to $e$. Each boundary line of a region separates it from the region of a neighbor feature.

## The algorithm

```pseudo id=main
LIN-CANNY(A, B, fA, fB)
L1  loop
L2      if fA and fB are vertices a and b then
L3          if b violates a plane of VR(a) then fA ← the edge of A behind that plane; continue
L4          if a violates a plane of VR(b) then fB ← the edge of B behind that plane; continue
L5          return (fA, fB, a, b)
L6      if one feature is a vertex v and the other an edge e then
L7          if v is beyond an end plane of VR(e) then e ← the vertex at that end; continue
L8          if v is on the inner side of the line of e or on it then
L9              k ← the edge of the polygon of e with the largest signed distance to v
L10             if that distance ≤ 0 then return INTERSECTING
L11             e ← k; continue
L12         q ← the point of e closest to v
L13         if q violates a plane of VR(v) then v ← the edge behind that plane; continue
L14         return (fA, fB, v, q)
L15     fA and fB are edges: if they intersect then return INTERSECTING
L16     replace the pair by the vertex-edge pair with the smallest distance among the four ends
```

A plane of $VR(a)$ is violated by $x$ when $(x - a) \cdot (a^{\pm} - a) > 0$. The end plane of $VR(e)$ at $e_0$ is violated when $(v - e_0) \cdot (e_1 - e_0) < 0$. Line L8 is the case where the vertex is behind the edge, inside its supporting line. There no neighbor of $e$ is closer in a simple way, so this version searches all edges of the polygon of $e$ in lines L9 to L11. In 2D the edge with the largest signed distance always holds the closest point (Lemma 3 of the proof). Line L16 uses the fact that two disjoint segments always have a closest pair with an end point of one of them.

All tests are signs of dot products and cross products of input points and of projected points, so with integer or rational input the method is exact. The implementation compares squared signed distances with their sign, so it needs no square root.

## Example

Let $A$ be the rectangle with vertices $a_0 = (0, 0)$, $a_1 = (4, 0)$, $a_2 = (4, 3)$, $a_3 = (0, 3)$, and let $B$ be the triangle $b_0 = (7, 1)$, $b_1 = (10, 2)$, $b_2 = (8, 5)$. Edge $i$ goes from vertex $i$ to vertex $i + 1$, so $A$'s edge $e_1$ is the right side $x = 4$, and $B$'s edge $e_0$ is $[b_0, b_1]$. Start from the pair $(a_0, b_1)$.

| move | state | test that fails | new state | feature distance after |
|---|---|---|---|---|
| 1 | $a_0$, $b_1$ | L3: $(b_1 - a_0) \cdot (a_3 - a_0) = (10, 2) \cdot (0, 3) = 6 > 0$ | $e_3$ of $A$, $b_1$ | 10 |
| 2 | $e_3$, $b_1$ | L8: $b_1$ is on the inner side of $e_3$ (the line $x = 0$) | L9: signed distances of $b_1$ to the edges of $A$ are $-2, 6, -1, -10$, so $e_1$ | 6 |
| 3 | $e_1$, $b_1$ | L13: $q = (4, 2)$, and $(q - b_1) \cdot (b_0 - b_1) = (-6, 0) \cdot (-3, -1) = 18 > 0$ | $e_1$, $e_0$ of $B$ | 3 |
| 4 | $e_1$, $e_0$ | L16: the ends give distances $\sqrt{10}$ ($a_1$), $\sqrt{13}$ ($a_2$), $3$ ($b_0$), $6$ ($b_1$) | $e_1$, $b_0$ | 3 |
| 5 | $e_1$, $b_0$ | none: $b_0 \in VR(e_1)$, $q = (4, 1)$, and $q \in VR(b_0)$ | return | 3 |

The start distance is $|a_0 - b_1| = \sqrt{104} \approx 10.2$. The answer is the edge $x = 4$ of $A$ and the vertex $(7, 1)$ of $B$, with closest points $(4, 1)$ and $(7, 1)$ and distance 3, which a brute force over all vertex-edge pairs confirms. The feature distance goes down at moves 1, 2 and 3, and at move 4 it stays at 3 while the dimension goes down. Move 2 is the escape of lines L9 to L11. A walk that only looked at the neighbors of $e_3$ would go to $a_0$ or $a_3$, which are not closer to $b_1$.

The next call, after $B$ moves a little, starts from $(e_1, b_0)$ and returns at once if $b_0$ is still in the half strip of $e_1$ and its closest point is still in the wedge of $b_0$. In the test of this page, a quadrilateral $B$ goes 200 steps of length $1/2$ around a pentagon $A$. The walk that starts from the previous answer took 1.235 moves per call on average (162 calls needed one pass and no move), against 6.29 from the fixed start $(a_0, b_0)$. This is a measurement on one small scene, not a bound.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It has three parts.

First, if $x$ is in the Voronoi region of a feature $f$, the closest point of the polygon to $x$ is the closest point of $f$ to $x$. If two points $p \in A$ and $q \in B$ are each the closest point of their polygon to the other, then $|p - q|$ is the distance of the polygons, and the line through the middle perpendicular to $q - p$ separates them. So the two returns at L5 and L14 are correct.

Second, each move lowers the distance between the two current features, or keeps it and lowers the sum of their dimensions. Lines L3, L4, L11 and L13 lower the distance, and lines L7 and L16 keep it and go from an edge to a vertex. So no state repeats, and the walk ends after at most $4nm$ moves.

Third, the intersecting returns at L10 and L15 are correct, and if the polygons intersect, the first part rules out a return with a positive distance.

## Complexity

Each move costs $O(1)$, except the escape of lines L9 to L11, which costs $O(m)$ or $O(n)$. So a call with $s$ moves costs $O(s(n + m))$, and $O(s)$ if no escape happens. The proof bounds $s$ by $4nm$, so one call costs $O(nm(n + m))$ in the worst case. This bound is not tight, and it is not the point of the method.

The point is coherence. If the objects move little between calls, the old pair is still a closest pair or one or two moves away, and a call takes a few constant time tests. This is the reason for the near constant time per call that is reported for the method. It is a measured behavior for small motions, not a theorem: a fast rotation can move the closest pair far around the polygons. A call from scratch takes a number of moves that grows with the size of the polygons. The extra space is $O(1)$.

## Properties

- The answer is a pair of features, not only a distance. A simulator can use the features as a contact manifold when the distance is small.
- The method is exact with exact arithmetic. In floating point the region tests need tolerances, and wrong signs near the region boundaries can make the 3D version cycle.
- The method needs the full boundary structure: the neighbors of each vertex and edge, and in 3D the faces around each edge. [GJK](/gjk-algorithm/) needs only a support function.
- The original method assumes the objects are disjoint. When they penetrate, the 3D method can cycle or stop with a wrong pair, and it gives no penetration depth.

## Variants and improvements

- **V-Clip.** Mirtich (1998) clips edges against the Voronoi regions instead of testing points, needs no tolerances, and reports penetration. See [V-Clip](/v-clip/).
- **Hierarchical walks.** A walk from scratch on a large polytope can start on a coarse hierarchy of the polytope and refine, which makes the first call cheap.
- **Lookup tables.** For polytopes with many features, the start feature can come from a table indexed by the direction between the objects.
- **Use in a broad phase pipeline.** I-COLLIDE runs [sweep and prune](/sweep-and-prune/) on boxes and then the closest feature walk on the pairs that overlap. Nonconvex objects are split into convex parts, for example by [approximate convex decomposition](/approximate-convex-decomposition/).

## When to use it

Use the closest feature walk when you need the distance and the closest features of convex objects at every step of a simulation with small motions, for example in robot motion planning and rigid body simulation with distance queries. Use [V-Clip](/v-clip/) instead if the objects can penetrate or if your arithmetic is floating point. Use [GJK](/gjk-algorithm/) when the shapes are given by support functions, such as spheres, capsules or scaled hulls, or when you do not want to store the feature graph.

## Pitfalls

- **Penetration.** The walk assumes disjoint objects. Without the check of lines L10 and L15 it can stop at a pair with a positive distance between two features of objects that overlap, or loop.
- **A missing escape.** If line L8 is dropped, a vertex behind an edge sees no violated plane of $VR(e)$, and the walk can return a pair that is not closest. The local test is not enough on the inner side.
- **Collinear vertices.** The proof needs strict convexity. Three vertices on one line make an edge of zero turn, whose Voronoi regions are empty or degenerate. Remove such vertices when you build the polygon.
- **Clockwise input.** With clockwise order the outward normals point inward, and every test is wrong. Check the orientation once.
- **Tolerances in floating point.** A point on a region boundary can pass the test of one region and fail the test of the neighbor. Use the same comparison on both sides, or bound the number of moves and restart from a fresh pair, as the implementation does.

## Implementations

## History

Lin and Canny presented the closest feature walk at ICRA 1991, for distance computation and collision detection between convex polyhedra in robotics. Its use of coherence made it the exact test of I-COLLIDE by Cohen, Lin, Manocha and Ponamgi (1995), after a sweep and prune broad phase. Mirtich (1998) analyzed the cases where the method needs tolerances or fails, in particular penetration and degenerate configurations, and gave V-Clip, which handles them. GJK, with its support function interface, later became the more common choice in game engines.

## References
