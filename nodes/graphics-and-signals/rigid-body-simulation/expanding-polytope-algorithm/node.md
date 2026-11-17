---
tag: PP6HVM
kind: algorithm
slug: expanding-polytope-algorithm
name: Expanding polytope algorithm
aliases:
- EPA
area: graphics-and-signals/rigid-body-simulation
level: core
summary: Find the penetration depth and normal of two overlapping convex shapes by growing a polytope inside their Minkowski difference from the final GJK simplex.
solves: [penetration-depth]
model: real-ram
complexity:
  vars: {n: the number of vertices of A, m: the number of vertices of B, k: the number of rounds}
  time: {call: O(k (k + n + m)), rounds_worst: O(n m), heap_call: O(k log k + k (n + m))}
  space: {extra: O(k)}
properties: {deterministic: true, online: false, recursive: false, exact: false}
history:
  year: 2001
  people: [Gino van den Bergen]
  note: Van den Bergen described EPA as a way to get the penetration depth from the last simplex of GJK, and it became the usual companion of GJK in physics engines.
prereqs: [gjk-algorithm, penetration-depth, support-function, convex-polygon]
see_also: [v-clip, lin-canny-closest-features, separating-axis-theorem, minkowski-sum, convex-hull, contact-manifold, collision-impulse, conservative-advancement]
sources:
  - book: isbn:9781558608016
    title: Gino van den Bergen, Collision Detection in Interactive 3D Environments, Morgan Kaufmann, 2003
    locator: the material on penetration depth and the expanding polytope algorithm
  - paper: doi:10.1007/BF01190153
    title: David Dobkin, John Hershberger, David Kirkpatrick and Subhash Suri, Computing the intersection-depth of polyhedra, Algorithmica 9(6), 1993, 518 to 533
    locator: the definition of the intersection depth as the shortest translation that separates two convex polyhedra
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 9, Convex-based Methods (GJK, support mappings and the Minkowski difference)
---

The expanding polytope algorithm (EPA) computes the [penetration depth](/penetration-depth/) of two convex shapes that overlap: the length of the shortest translation that separates them, and its direction. It works on the [Minkowski difference](/minkowski-sum/) $A - B$, which contains the origin when the shapes overlap. The depth is the distance from the origin to the boundary of $A - B$. EPA starts from the simplex in which the [GJK algorithm](/gjk-algorithm/) found the origin, and it grows this polytope inside $A - B$ toward the boundary face that is closest to the origin. It only needs the [support functions](/support-function/) of the shapes, so it works for polytopes and for curved convex shapes. It needs a tolerance, and it is not exact.

## In plain words

Two convex objects overlap. You want the shortest push that separates them.

Build a new shape from all the differences of a point of one object and a point of the other. The objects overlap when this shape covers the center point. The shortest push is the distance from the center to the edge of this shape.

You cannot build the whole shape, but you can ask for its farthest point in any direction. Start from a small triangle inside it that covers the center. Take the side of the triangle that is nearest to the center. Ask for the farthest point of the shape in the outward direction of that side. If that point is far past the side, add it, and the inner shape grows. If it is almost on the side, that side is part of the edge, and its distance is the push.

## The problem

The input is two convex shapes $A$ and $B$, given by support functions $s_A(u)$ and $s_B(u)$ that return a point of the shape that is extreme in the direction $u$, and a tolerance $\varepsilon \ge 0$. The support function of $M = A - B$ is $s_M(u) = s_A(u) - s_B(-u)$. If $A$ and $B$ overlap, the output is a depth $d$ and a unit normal, such that moving $A$ by about $d$ along the normal makes the shapes touch, and two witness points on $A$ and $B$. This page works in 2D, where the polytope is a polygon and its faces are edges. In 3D the polytope has triangle faces, and an insertion replaces all faces that the new point can see.

## The algorithm

```pseudo id=main
EPA(sA, sB, ε)
L1  P ← the GJK triangle of support points of A - B that contains the origin, counterclockwise
L2  loop
L3      for each edge of P, compute its outward unit normal n and its distance r = n · p from the origin
L4      let [p, q] be the edge with the smallest r, with the normal n
L5      t ← sA(n) - sB(-n)
L6      if n · t - r ≤ ε then return the depth r, the normal -n and the witness points on [p, q]
L7      insert t between p and q in P
```

Each vertex of $P$ keeps the two points $a$ and $b$ that gave it, with $w = a - b$. At the end, the foot of the perpendicular from the origin to the edge $[p, q]$ is $\lambda$ of the way from $w_p$ to $w_q$, and the same $\lambda$ between $a_p$ and $a_q$, and between $b_p$ and $b_q$, gives the witness points. The GJK stage is the boolean form of GJK in 2D: it returns no triangle if the origin is outside $M$ or on its boundary, and then the shapes are disjoint or only touch.

## Example

Let $A$ be the rectangle with corners $(0, 0)$, $(4, 0)$, $(4, 3)$, $(0, 3)$, and $B$ the triangle $(3, 1)$, $(6, 2)$, $(4, 4)$. The corner $(3, 1)$ of $B$ is inside $A$.

The GJK stage returns the counterclockwise triangle $w_0 = (1, 2)$, $w_1 = (-6, 1)$, $w_2 = (1, -1)$. For example, $w_2 = (4, 0) - (3, 1)$ is the support point in the direction $(1, 0)$.

**Round 1.** The edges have the distances $13/\sqrt{50} \approx 1.838$ for $[w_0, w_1]$, $5/\sqrt{53} \approx 0.687$ for $[w_1, w_2]$ with the normal $(-2, -7)/\sqrt{53}$, and $1$ for $[w_2, w_0]$ with the normal $(1, 0)$. The closest edge is $[w_1, w_2]$. The support point in its normal direction is $t = (0, 0) - (4, 4) = (-4, -4)$, at the distance $36/\sqrt{53} \approx 4.945$. That is far past the edge, so line L7 inserts it, and $P$ is $(1, 2)$, $(-6, 1)$, $(-4, -4)$, $(1, -1)$.

**Round 2.** The new edges have the distances $28/\sqrt{29} \approx 5.20$ and $8/\sqrt{34} \approx 1.37$. Now the closest edge is $[w_2, w_0]$, the line $x = 1$, at the distance 1. The support point in the direction $(1, 0)$ is $(1, -1)$ again, so the gain is 0, and line L6 stops. The depth is 1 with the normal $(-1, 0)$: move $A$ one unit to the left, and its right side touches the corner $(3, 1)$ of $B$. The foot of the perpendicular is $(1, 0)$, at $\lambda = 1/3$ from $w_2$ to $w_0$, which gives the witness points $(4, 1)$ on $A$ and $(3, 1)$ on $B$.

The tests of this page compare the result with the hull of all $nm$ vertex differences on 500 random pairs. For two discs, which have no vertices, the number of rounds grows with the precision. With the radii 2 and 1.5 at the distance 1, the implementation took 10, 16, 24, 30 and 36 rounds for $\varepsilon = 10^{-2}$, $10^{-4}$, $10^{-6}$, $10^{-8}$ and $10^{-10}$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The invariant is that $P$ is a convex polygon that contains the origin, and that its vertices are support points of $M$, so $P \subseteq M$. An inserted point $t$ cannot be past the line of a neighbor edge, because the neighbor vertex is a support point for a direction in its normal cone. So the polygon stays convex. Since $P \subseteq M$, the smallest edge distance $r$ is at most the depth. At the stop, the support value in the direction $n$ is at most $r + \varepsilon$, and the depth is the smallest support value over all directions, so $r \le d \le r + \varepsilon$. For polygons, each round adds a new difference of two vertices, so EPA stops after at most $nm$ rounds, also with $\varepsilon = 0$.

## Complexity

A round costs $O(|P|)$ to find the closest edge and $O(n + m)$ for a support query by a linear scan. After $k$ rounds, $|P| = k + 2$, so a call costs $O(k(k + n + m))$. With the edges in a priority queue by distance, as in the 3D form, the search for the closest edge costs $O(\log k)$. The proof bounds $k$ by $nm$ for polygons, and for curved shapes $k$ depends on $\varepsilon$. In practice EPA starts from the GJK simplex, close to the answer, and $k$ is small. This is observed, not proved. The extra space is $O(k)$.

## Properties

- **Bracket.** With exact arithmetic the result satisfies $r \le d \le r + \varepsilon$, and with $\varepsilon = 0$ on polytopes it is the exact depth.
- **Support functions only.** EPA works on any convex shape with a support function, as GJK does: polygons, discs, capsules and their Minkowski sums.
- **A tolerance.** For curved shapes $\varepsilon$ must be positive. In floating point a positive $\varepsilon$ also stops rounds that gain nothing because of rounding.
- **Witness points.** The result gives a contact normal and a point on each shape, which a simulator can use for a [contact manifold](/contact-manifold/).

## Variants and improvements

- **3D.** The polytope has triangle faces. An insertion removes all faces that the new point sees and connects the horizon edges to it. The start simplex must be a tetrahedron that contains the origin. If GJK stops with a smaller simplex, it must be blown up first, with extra support points.
- **A priority queue of faces.** Keep the faces in a heap by their distance, and skip the faces that were removed. This is the usual form in engines.
- **Dual expansion.** Kim, Lin and Manocha (2002) walk on the Gauss maps of two convex polytopes to estimate the depth incrementally from the previous time step.
- **Separating axes.** For boxes and other polytopes with few face normals, the [separating axis theorem](/separating-axis-theorem/) gives the depth as the smallest overlap over the candidate axes, with no iteration.
- **Avoid the depth.** [Conservative advancement](/conservative-advancement/) and other [continuous collision detection](/continuous-collision-detection/) methods stop the motion before the overlap, so only a distance is needed.

## When to use it

Use EPA after GJK reports an overlap of two convex shapes and you need the penetration depth and normal, for example to push the bodies apart or to make a contact. It is the standard choice for general convex shapes in physics engines. For boxes, use the separating axis tests. For deep overlaps of nonconvex shapes, split them into convex pieces first, because the depth of a nonconvex pair is not the depth of its convex hulls.

## Pitfalls

- **Degenerate faces.** In 3D, nearly flat or very thin faces give normals with a large error, and the polytope can lose its convexity. Check the orientation of each new face, and stop with the best face so far if a check fails.
- **The origin on the boundary.** When the shapes just touch, GJK can stop with the origin on an edge of the simplex or with a flat simplex. The depth is then 0, and the normal must come from the face, not from the origin.
- **The tolerance.** With $\varepsilon = 0$ on curved shapes the loop does not stop in exact arithmetic. In floating point it may stop only because the gain rounds to 0. Use a relative tolerance and a limit on the rounds.
- **The sign of the normal.** The normal points from $B$ to $A$ in this page. Mixing up $A - B$ and $B - A$ pushes the bodies into each other.
- **Large depths.** The penetration depth is not continuous in time: a small motion can flip the normal to another face. A simulator that uses it for deep contacts can push a body out of the wrong side.

## Implementations

## History

Cameron and Culley studied the penetration depth of convex polytopes in the 1980s, and Dobkin, Hershberger, Kirkpatrick and Suri (1993) analyzed its exact computation for convex polyhedra. Van den Bergen described EPA in 2001 as a way to get the depth from the last simplex of GJK with support functions only, and it is in his 2003 book. It became the usual companion of GJK in game and physics engines, which run GJK for the distance and EPA when the shapes overlap.

## References
