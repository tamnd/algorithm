---
tag: B7FYY7
kind: algorithm
slug: medial-surface-of-a-solid
name: Medial surface of a solid
aliases:
- 3D medial axis of a polyhedron
- Sherbrooke-Patrikalakis-Brisson medial axis
area: cad/solid-modeling
level: advanced
summary: Computes the centres of maximal inscribed balls of a polyhedral solid, a complex of sheets, seams and junctions, by tracing seams from junction to junction as Sherbrooke, Patrikalakis and Brisson did.
model: real-ram
complexity:
  vars: {n: the number of faces of the polyhedron, k: the largest number of faces that are nearest to one point}
  time: {worst: "O(k^3 n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1996
  people: [Evan C. Sherbrooke, Nicholas M. Patrikalakis, Erik Brisson]
  note: Sherbrooke, Patrikalakis and Brisson computed the medial axis transform of general polyhedral solids, with nonconvex vertices and edges, by classifying medial points and tracing the seams between junctions.
prereqs: [medial-axis, convex-polytope, boundary-representation]
see_also: [straight-skeleton, voronoi-diagram, midsurface-extraction, medial-axis-decomposition-meshing, casting-hot-spot-detection, shape-diameter-function, solid-offsetting, simplex-method]
sources:
  - paper: doi:10.1109/2945.489386
    title: Evan C. Sherbrooke, Nicholas M. Patrikalakis and Erik Brisson, An algorithm for the medial axis transform of 3D polyhedral solids, IEEE Transactions on Visualization and Computer Graphics 2(1), 44 to 61, 1996
    locator: the classification of medial points into sheets, seams and junctions, the tracing of seams between junctions, and the examples on convex and nonconvex polyhedra with holes
  - paper: doi:10.1016/j.cagd.2003.07.008
    title: Tim Culver, John Keyser and Dinesh Manocha, Exact computation of the medial axis of a polyhedron, Computer Aided Geometric Design 21(1), 65 to 98, 2004
    locator: the exact computation of seams and junctions with algebraic numbers and its comparison with floating-point tracing
  - paper: doi:10.1145/376957.376986
    title: Nina Amenta, Sunghee Choi and Ravi Krishna Kolluri, The power crust, Proceedings of the Sixth ACM Symposium on Solid Modeling and Applications, 2001
    locator: the approximation of the medial axis by the Voronoi poles of a dense boundary sample
---

The medial surface of a solid $P$ in $\mathbb{R}^3$ is the set of interior points that have two or more nearest points on the boundary, or, up to closure, the set of centres of the maximal balls inside $P$. It is the three-dimensional [medial axis](/medial-axis/): together with the radius of the ball at each point, the *medial axis transform*, it determines the solid, since $P$ is the union of its maximal balls. In the plane the medial axis of a polygon is a graph of curves. In space it is a two-dimensional complex. Its *sheets* are surfaces where two boundary elements are nearest. Its *seams* are curves where three or more sheets meet. Its *junctions* are points where seams meet. For a polyhedron the sheets are pieces of planes and quadric surfaces; curved sheets come only from reflex edges and reflex vertices. Sherbrooke, Patrikalakis and Brisson computed this complex for general polyhedra by tracing the seams from junction to junction and then filling in the sheets. This page states their method and implements its core step exactly for convex polyhedra, where every sheet is flat and the trace becomes a walk on the edges of a four-dimensional polytope.

## In plain words

Blow up a balloon inside a solid until it touches the walls. If it touches two walls at once, its centre is on the medial surface. Move the balloon around, keeping it as big as it can be, and its centre draws a set of thin sheets inside the solid, like the walls of a honeycomb.

Where three walls are touched at once, the centre runs along a line, a seam where sheets meet. Where four are touched, the seams meet at a point, a junction.

The method starts at the corners of the solid, where several faces meet. From each corner it follows a seam inward until the balloon touches one more wall. That point is a junction, and new seams leave from it. When every seam has been followed, the sheets are the flat or curved pieces between the seams.

## The problem

**Input.** A polyhedral solid $P$: a bounded closed set with a boundary made of planar polygons. For the implemented case $P$ is convex, given as $P = \{x : n_i \cdot x \le b_i,\ i = 1, \ldots, n\}$ with unit normals $n_i$, one for each facet. The normals have rational coordinates, such as $(1, 2, 2)/3$, so every quantity below is rational.

**Output.** The medial surface as a cell complex: the junctions, each with its radius and its set of nearest boundary elements; the seams, as curves between junctions with the elements nearest along them; and the sheets, as regions bounded by seams and by the edges of $P$.

**Definitions.** For $x \in P$, $\rho(x)$ is the distance from $x$ to the boundary of $P$. A ball $B(x, r) \subseteq P$ is *maximal* if no other ball inside $P$ contains it. The *medial surface* $M(P)$ is the closure of the set of interior points with at least two nearest boundary points. The *medial axis transform* is the map $x \mapsto \rho(x)$ on $M(P)$.

For a convex $P$, the distance to the plane of facet $i$ is $d_i(x) = b_i - n_i \cdot x$, and $\rho(x) = \min_i d_i(x)$. The set $T(x)$ of facets that attain the minimum is the *tie set* of $x$. Then $x$ is in a sheet when $|T(x)| = 2$, on a seam when $|T(x)| \ge 3$, and a junction when the seams through $x$ end there.

## The algorithm

```pseudo id=main
TRACE-SEAMS(P)
L1  Q ← the vertices of P                        ▷ seams start on the boundary
L2  J ← an empty map from points to (radius, tie set)
L3  while Q is not empty do
L4      x ← POP(Q)
L5      if x is in J then continue
L6      (ρ, T) ← the distance from x to the boundary and the faces that attain it; J[x] ← (ρ, T)
L7      for each triple i, j, k in T and each sign of w = ±(n_i − n_j) × (n_i − n_k) do
L8          r ← max of n_l · w over l in T; S ← the faces l in T with n_l · w = r
L9          if i is not in S, or ρ = 0 and r ≥ 0, then skip this w    ▷ not a seam, or leaves P
L10         t* ← the least t > 0 at which a face outside S is as near as S, or ρ / r if r > 0 and that is less
L11         y ← x + t* w; record the seam (x, y, S); push y on Q
L12 return J and the seams
```

Along $x + t w$ the faces of $S$ are at distance $\rho - t r$ and stay nearest; the faces of $T$ outside $S$ fall behind at once, since their $n_l \cdot w$ is smaller. A face $l$ outside $T$ catches up at $t = (d_l(x) - \rho) / (n_l \cdot w - r)$ when $n_l \cdot w > r$, and line L10 takes the first such event. If $r > 0$ the seam runs toward the boundary and reaches it at $t = \rho / r$, at a vertex of $P$. The sheets are not traced. The sheet of two faces $i$ and $j$ is the convex polygon spanned by the traced points whose tie set contains both, because its corners are junctions or vertices of $P$.

**The general case.** For a nonconvex polyhedron, Sherbrooke, Patrikalakis and Brisson use the same plan with more kinds of boundary elements: faces, reflex edges and reflex vertices. A point of a seam is equidistant from three elements, so a seam is a curve on which a system of polynomial equations holds, and a junction solves a system with one more equation. The method finds the junctions at the vertices of the solid, traces each seam numerically from one junction to the next, and stops it where a fourth element becomes as near. It then forms each sheet from the cycle of seams and boundary edges around it. Two complications do not occur in the convex case. A nearest element must be checked against the whole boundary, not only against the planes. And seams are curved, so the trace steps along them and solves for the junction at the end.

## Example

Let $P = [0, 4] \times [0, 2] \times [0, 2]$, with faces 0 to 5 on the planes $x = 4$, $x = 0$, $y = 2$, $y = 0$, $z = 2$ and $z = 0$. The trace starts at the 8 corners.

| step | point $x$ | $\rho$ | tie set $T$ | seams found |
|---|---|---|---|---|
| corner | $(0,0,0)$ | 0 | $\{1, 3, 5\}$ | $w = (1,1,1)$, $r = -1$: faces 2 and 4 catch up at $t = 1$, so the seam ends at $(1,1,1)$ |
| junction | $(1,1,1)$ | 1 | $\{1, 2, 3, 4, 5\}$ | 4 seams back to the corners at $x = 0$, and $w = (2,0,0)$ with $S = \{2,3,4,5\}$, $r = 0$: face 0 catches up at $t = 1$, at $(3,1,1)$ |
| junction | $(3,1,1)$ | 1 | $\{0, 2, 3, 4, 5\}$ | the seam back to $(1,1,1)$ and 4 seams to the corners at $x = 4$ |

The result has 2 junctions and 9 seams: 8 from the corners, each with 3 nearest faces and a radius that grows from 0 to 1, and the middle seam from $(1,1,1)$ to $(3,1,1)$, with 4 nearest faces and a constant radius 1. The 12 sheets belong to the 12 pairs of adjacent faces. The 8 sheets between an end face and a side face are triangles, such as $(0,2,0), (0,2,2), (1,1,1)$ for faces 1 and 2. The 4 sheets between two side faces are trapezoids, such as $(0,2,2), (4,2,2), (3,1,1), (1,1,1)$ for faces 2 and 4. The opposite faces $y = 0$ and $y = 2$ are both nearest only along the middle seam, so they have no sheet of their own. For the cube $[0,2]^3$ the two junctions merge into the centre, whose tie set has all 6 faces, and only the 8 corner seams remain.

## Correctness

For a convex $P$ and an interior $x$, the ball $B(x, \rho(x))$ lies in every half-space, so it lies in $P$. Its foot on each nearest plane is a boundary point, and every nearest boundary point is such a foot. So the nearest boundary points match the faces of $T(x)$ one to one, and $x$ is on the medial surface exactly when $|T(x)| \ge 2$.

The trace is a walk on a polytope. Lift $P$ to
$$\hat{P} = \{(x, r) \in \mathbb{R}^4 : r \ge 0,\ n_i \cdot x + r \le b_i \text{ for every facet } i\},$$
the region under the graph of $\rho$. The upper boundary of $\hat{P}$ is the graph of $\rho$. Its 2-faces project to the sheets, its edges off the floor $r = 0$ project to the seams, and its vertices project to the junctions and to the vertices of $P$. Lines L7 to L9 find every edge of $\hat{P}$ at a vertex, except the edges in the floor. Line L10 finds the far end of each edge. Every junction is reached because of a simplex method argument. A vertex of $\hat{P}$ with $r > 0$ does not minimize $r$, so it has an edge on which $r$ decreases. Following such edges reaches a vertex of $P$ in the floor, and the trace explores this path in reverse. The full proof is in the proof file.

These facts are checked by the tests, with Fraction. Random convex polyhedra are built from the 6 axis planes and 2 to 6 planes whose normals come from Pythagorean quadruples. On each one the tests check four things. A point on a traced seam has exactly the seam's faces as nearest; this is checked at over 500 rational points. The junctions equal those of a brute force, which solves $b_l - n_l \cdot x = \rho$ for every 4 faces. For every triple of faces, the traced seams that contain it tile exactly the interval of the bisector line on which the three are nearest. And on the bisector plane of two faces, a rational point is in the polygon of the traced sheet corners exactly when both faces are nearest.

## Complexity

- **The size of the output.** $\hat{P}$ is a polytope in $\mathbb{R}^4$ with at most $n + 1$ facets. By the upper bound theorem of McMullen it has $O(n^2)$ vertices and $O(n^2)$ edges, so the medial surface of a convex polyhedron with $n$ faces has $O(n^2)$ junctions, seams and sheets. This is proved, not measured.
- **The trace.** Each traced point costs $O(n)$ for its tie set at line L6. It tries $O(k^3)$ triples at line L7, and each triple costs $O(n)$ for the event search at line L10. Over $O(n^2)$ points that is $O(k^3 n^3)$ time. If no five faces are nearest to one point, $k \le 4$ and the bound is $O(n^3)$. The space is $O(n^2)$ for the map $J$ and the seams.
- **The input step.** The code finds the vertices and the facets of $P$ from its half-spaces by brute force, in $O(n^4)$ time. A B-rep gives them directly.
- **The general case.** For a nonconvex polyhedron the medial surface is part of the Voronoi diagram of the faces, edges and vertices, and its size can grow faster than quadratically in $n$. The cost of the method of Sherbrooke, Patrikalakis and Brisson depends on the number of seams and on the numerical trace of each, through its step size and tolerance; this page states no worst-case bound for it.

## Properties

- **Exact in the convex case.** Each junction solves a linear system, and each seam end is a ratio of rational numbers, so the code computes every point with Fraction. In the general case the junctions are algebraic numbers. Floating-point tracing can then miss a short seam or join two seams that should stay apart, and Culver, Keyser and Manocha compute them exactly for this reason.
- **Degenerate ties.** A point with five or more nearest faces, such as the centre of a cube, needs no special case. Line L8 groups all faces that stay nearest in a direction, and a seam with four or more nearest faces, such as the middle seam of the example, is traced once.
- **Not stable.** As in the plane, a small change to the solid can add a large sheet. A tiny bump on a face of a cube adds sheets that reach from the bump to the middle of the cube. Applications usually prune sheets whose radius changes fast relative to their size.
- **Homotopy.** The medial surface of a bounded open set has the same homotopy type as the set, so it keeps the handles and cavities of the solid.
- **The convex case is the 3D straight skeleton.** For a convex polyhedron the medial surface is the trace of the faces as they move inward at unit speed, the three-dimensional analogue of the [straight skeleton](/straight-skeleton/) of a convex polygon.

## Variants and improvements

- **Exact computation.** Culver, Keyser and Manocha compute the seams and junctions of a general polyhedron with exact algebraic arithmetic, which removes the failures of floating-point tracing at the cost of much slower arithmetic.
- **From the Voronoi diagram of samples.** Sample the boundary densely and compute the [Voronoi diagram](/voronoi-diagram/) of the samples. Its poles, the Voronoi vertices far from the sample, approximate the medial surface, and the power crust of Amenta, Choi and Kolluri uses them to rebuild the surface and the medial axis together. This works on any input but gives only an approximation, with spurious sheets that must be pruned.
- **From a voxel grid.** A [distance transform](/distance-transform/) on voxels and a thinning step give a discrete medial surface. It is simple and robust, but its accuracy is limited by the voxel size.
- **Shrinking balls.** For each boundary sample, shrink a ball tangent at the sample until it touches the boundary at one more point. Its centre is a medial point, and [mid-surface extraction](/midsurface-extraction/) uses this to reduce thin solids.
- **Curved solids.** For solids bounded by NURBS surfaces, seams are traced by solving systems of equations on the surfaces, with the same plan of junctions, seams and sheets.

## When to use it

Use the medial surface when the question is about local thickness or shape. Examples are [hot spots in castings](/casting-hot-spot-detection/), where the largest inscribed balls show the last metal to solidify; thin walls in molded and printed parts; the reduction of thin solids to shells by [mid-surface extraction](/midsurface-extraction/); and the split of a solid into simple pieces for [meshing](/medial-axis-decomposition-meshing/). Use the exact convex trace when the solid or its pieces are convex polyhedra, and tracing with exact arithmetic for general polyhedra when the topology of the result matters. When only an approximate skeleton is needed, as in shape matching or animation, sampled or voxel methods are simpler and more robust. For thickness at single points, a [shape diameter function](/shape-diameter-function/) is cheaper still.

## Pitfalls

- **Distance to planes, not to faces.** In a nonconvex solid, the nearest point of a face plane may lie off the face, and a far face can be nearer than its plane suggests. The rule $\rho = \min_i d_i$ holds only for convex solids.
- **Redundant planes.** A plane that touches $P$ only at a vertex or an edge is at distance 0 there and would join the tie sets. Use only the planes of the facets, as the code does.
- **Only one sign of the seam direction.** The cross product gives the line of a seam, not its side. Test both signs and reject the one that leaves the solid or loses one of the three faces, as line L9 does.
- **Missing seams in floating point.** A junction with five or more nearest elements splits into several close junctions under rounding, and short seams appear or vanish. Use exact arithmetic or merge junctions closer than a tolerance, and accept that the topology may then be wrong.
- **Expecting a curve skeleton.** The medial surface of a solid is two-dimensional. A long square bar has four strips that run from its long edges to its axis, not a single curve, so curve skeletons need a further reduction.

## Implementations

## History

Blum introduced the medial axis in 1967 for shapes in the plane, and the definition carries over to any dimension. For polyhedra, Milenkovic computed the Voronoi diagram of a polyhedron by tracing in 1993. Sherbrooke, Patrikalakis and Brisson gave a conference version of their algorithm at the ACM Symposium on Solid Modeling and Applications in 1995 and the full algorithm in 1996. It handles polyhedra of any genus with nonconvex vertices and edges and finds the medial axis transform with its radius function. Culver, Keyser and Manocha made the computation exact in 1999 and 2004. From the late 1990s, approximations from boundary samples, such as the power crust of Amenta, Choi and Kolluri in 2001, became the usual choice for meshes and scanned shapes. Exact tracing remained the method for CAD solids with few faces.

## References
