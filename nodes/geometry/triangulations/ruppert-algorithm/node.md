---
tag: A2ZJPV
kind: algorithm
slug: ruppert-algorithm
name: Ruppert's algorithm
aliases:
- Ruppert's Delaunay refinement
- Ruppert's mesh generation algorithm
- Ruppert refinement
area: geometry/triangulations
level: advanced
summary: Delaunay refinement producing a triangulation with minimum angle about 20.7 degrees.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {n: the number of input vertices, m: the number of output vertices}
  time: {worst: O(m^2)}
  space: {extra: O(m)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1995
  people: [Jim Ruppert]
  note: Ruppert presented the algorithm at SODA 1993 and published the full version in the Journal of Algorithms in 1995. It was the first Delaunay refinement algorithm with a proof of both an angle bound and size-optimality for general planar straight-line graphs, and it became the basis of practical mesh generators such as Shewchuk's Triangle.
prereqs: [delaunay-refinement, delaunay-triangulation, bowyer-watson-algorithm, in-circle-test, circumcenter, conforming-delaunay-triangulation]
see_also: [chew-second-algorithm, mesh-generation, delaunay-refinement, conforming-delaunay-triangulation, constrained-delaunay-triangulation, steiner-points, max-min-angle-triangulation, lawson-flip-algorithm]
sources:
  - paper: doi:10.1006/jagm.1995.1021
    title: Jim Ruppert, A Delaunay refinement algorithm for quality 2-dimensional mesh generation, Journal of Algorithms 18(3), 548 to 585 (1995)
    locator: the algorithm with diametral circles, the termination proof through local feature size, and the size-optimality theorem
  - paper: "Jim Ruppert, A new and simple algorithm for quality 2-dimensional mesh generation, Proceedings of the Fourth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 1993), 83 to 92"
    locator: the conference version (pages to be checked)
  - paper: doi:10.1016/S0925-7721(01)00047-5
    title: Jonathan Richard Shewchuk, Delaunay refinement algorithms for triangular mesh generation, Computational Geometry 22(1-3), 21 to 74 (2002)
    locator: Section 3 (Ruppert's algorithm, insertion radius, the bound B at least the square root of 2 for input angles of at least 60 degrees, where Ruppert asked for 90, and the behavior in practice) and Section 6 (small input angles)
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: Chapter 6, two-dimensional Delaunay refinement and its analysis (ISBN to be checked)
  - paper: "Jonathan Richard Shewchuk, Triangle, engineering a 2D quality mesh generator and Delaunay triangulator, Applied Computational Geometry, Lecture Notes in Computer Science 1148, Springer, 203 to 222 (1996)"
    locator: the implementation of Ruppert's algorithm in Triangle (pages to be checked)
---

Ruppert's algorithm solves the quality [mesh generation](/mesh-generation/) problem in the plane by [Delaunay refinement](/delaunay-refinement/). It starts from the [Delaunay triangulation](/delaunay-triangulation/) of the input and repeats two rules. If a vertex lies in the closed disk whose diameter is a piece of an input segment, that piece is split at its midpoint. Otherwise, if some triangle is skinny, a vertex is inserted at its [circumcenter](/circumcenter/), unless that point would encroach a segment piece, in which case the piece is split instead. Ruppert proved that, when no two input segments meet at an angle smaller than $90°$, the process stops for every bound $B \ge \sqrt 2$ on the ratio of circumradius to shortest edge. Shewchuk later showed that input angles of at least $60°$ suffice for the same bound. The final mesh then has no angle smaller than $\arcsin(1 / (2B))$, which is about $20.7°$ for $B = \sqrt 2$, and for $B > \sqrt 2$ its size is within a constant factor of the optimum.

## In plain words

Start with a fair triangle mesh of the shape, with the outline and any inner lines built in. Then fix it one problem at a time.

The first kind of problem is a corner that sits too close to a piece of an outline. Draw a circle that has that piece as its diameter. If any other corner lies inside or on the circle, cut the piece in half and add the midpoint to the mesh.

The second kind of problem is a thin triangle. Put a new corner at the center of the circle through its three corners. If that new corner would itself crowd a piece of an outline, cut that piece in half instead and try again later.

Every new corner keeps a safe distance from the old ones, and the shape has finite room, so the fixing stops. At the end, no triangle is thin.

## The problem

The input is a planar straight-line graph: a domain $\Omega$ with its boundary edges, a set of segments and a set of points inside. The output is a triangulation of $\Omega$ whose vertices include the input points, in which every input segment is a union of edges, and in which every triangle has circumradius $R$ and shortest edge $\ell$ with $R \le B \ell$. Since $\ell = 2 R \sin \theta_{\min}$ by the law of sines, the bound means that every angle is at least $\arcsin(1 / (2B))$. New vertices, called [Steiner points](/steiner-points/), may be added.

The code works under exactly the hypotheses of the termination proof, in a simple setting. The domain is a strictly convex polygon given counterclockwise, with all angles at least $90°$. The segments and points lie strictly inside and touch neither each other nor the boundary, so no two features meet at an angle below $90°$. This is Ruppert's original hypothesis; the weaker one of Shewchuk, angles of at least $60°$, needs the extra case of incident segments in the proof. Coordinates are integers or `Fraction`s, and the bound is given as $B^2 \ge 2$.

## The algorithm

A segment is cut into **subsegments** by the vertices on it. A subsegment $ab$ is **encroached** by a vertex $p$ other than $a$ and $b$ when $p$ lies inside or on its **diametral circle**, the circle with diameter $ab$. This is the exact test $(a - p) \cdot (b - p) \le 0$. A triangle is **skinny** when $R > B \ell$.

```pseudo id=main
RUPPERT(Ω, S, Q, B)                        ▷ Ω convex with angles at least 90°, B at least √2
L1  T ← Delaunay triangulation of the corners of Ω; insert the end points of S and the points Q
    the subsegments are the edges of Ω and the segments of S
L2  loop
L3      if some subsegment s is encroached then
L4          split s: insert its midpoint m and replace s by its two halves
L5      else if some triangle t of T has R(t) > B ℓ(t) then
L6          c ← the circumcenter of t
L7          if c encroaches some subsegments then
L8              split each of them; keep t in the queue
            else
L9              insert c
        else
L10         return T and the subsegments

INSERT(q)                                  ▷ Bowyer and Watson
L11 find the triangle that contains q, by walking from the last triangle made
L12 collect the triangles whose open circumdisk contains q, searching outward from that triangle
L13 delete them and join q to every edge on the boundary of the hole
```

Three facts make the rules work together.

- **Unencroached subsegments are Delaunay edges.** If the closed diametral disk of $ab$ holds no other vertex, then the diametral circle is an empty circle through $a$ and $b$, so $ab$ is an edge of the Delaunay triangulation. So at the end every segment is a chain of mesh edges, and the mesh is a [conforming Delaunay triangulation](/conforming-delaunay-triangulation/).
- **Accepted circumcenters stay inside.** When no subsegment is encroached, the circumcenter of a triangle can only be separated from the triangle by a subsegment that it encroaches. So a circumcenter that passes line L7 lies in the domain.
- **New vertices are never close.** A circumcenter is at distance $R > \sqrt 2 \, \ell$ from every vertex, because the Delaunay circumdisk is empty. A midpoint is far from all vertices too, as the termination proof shows.

## Example

Take the box with corners $v_0 = (0, 0)$, $v_1 = (6, 0)$, $v_2 = (6, 4)$, $v_3 = (0, 4)$ and one input point $v_4 = (2, 1)$, with $B = \sqrt 2$. The first Delaunay triangulation has four triangles. The worst is $v_0 v_1 v_4$, with smallest angle $14.04°$ and $R^2 / \ell^2 = 4.25$. The point $v_4$ also encroaches the bottom edge, since $(0 - 2)(6 - 2) + (0 - 1)(0 - 1) = -7 \le 0$. The algorithm takes these steps:

| step | event | action |
|---|---|---|
| 1 | $v_4$ encroaches $v_0 v_1$ | split at $v_5 = (3, 0)$ |
| 2 | $v_4$ encroaches $v_0 v_5$, since $(-2)(1) + (-1)(-1) = -1$ | split at $v_6 = (3/2, 0)$ |
| 3 | $v_2 v_4 v_5$ is skinny, with $R^2 / \ell^2 = 625 / 196 \approx 3.19$; its circumcenter $(59/14, 31/14)$ encroaches the right and top edges | reject it |
| 4 | the right edge $v_1 v_2$ and the top edge $v_2 v_3$ | split at $v_7 = (6, 2)$ and $v_8 = (3, 4)$ |
| 5 | $v_4 v_5 v_7$ is skinny, with $R^2 = 221/50$, $\ell^2 = 2$, ratio $2.21$ | insert its circumcenter $v_9 = (39/10, 19/10)$ |

After step 5, no subsegment is encroached and no triangle is skinny. The mesh has 10 vertices, 8 of them on the boundary, and 10 triangles:

$$v_0 v_4 v_3,\ v_0 v_6 v_4,\ v_1 v_7 v_9,\ v_1 v_9 v_5,\ v_2 v_8 v_9,\ v_2 v_9 v_7,\ v_3 v_4 v_8,\ v_4 v_5 v_9,\ v_4 v_6 v_5,\ v_4 v_9 v_8 .$$

This matches the counts of a triangulation of $n = 10$ points with $h = 8$ on the hull: $2n - h - 2 = 10$ triangles and $3n - h - 3 = 19$ edges. The smallest angle is $26.57°$, in $v_0 v_6 v_4$, against the guaranteed $20.70°$. The largest ratio $R / \ell$ is about $1.118$, below $\sqrt 2 \approx 1.414$.

## Correctness

The [correctness proof](proofs/correctness.md) follows Ruppert's argument as presented by Shewchuk. The mesh stays a Delaunay triangulation of $\Omega$, because Bowyer and Watson's insertion keeps the Delaunay property and every inserted point lies in $\Omega$. The queues always hold every encroached subsegment and every skinny triangle. So at the end no subsegment is encroached, which makes every subsegment a Delaunay edge, and no triangle is skinny, which gives the angle bound.

Termination uses the **insertion radius** $r_v$ of a vertex, its distance to the nearest vertex when it is inserted, and the **local feature size** $\mathrm{lfs}(x)$, the radius of the smallest disk around $x$ that meets two disjoint input features. The proof shows that every vertex has $r_v \ge \min \mathrm{lfs}$. A circumcenter has $r_c = R > B \ell \ge \ell$, because its triangle is skinny. A midpoint split because of a rejected circumcenter has $r_m \ge R / \sqrt 2 > \ell$. A midpoint split because a vertex encroaches its subsegment has $r_m \ge \mathrm{lfs}(m)$, because with angles of at least $90°$ the encroaching vertex lies on a feature disjoint from the segment. With angles between $60°$ and $90°$, Shewchuk's version of the proof also allows a vertex on an incident segment at angle $\alpha$, and gets $r_m \ge r_p / (2 \cos \alpha) \ge r_p$. So vertices are well separated, and only finitely many fit in $\Omega$.

## Complexity

The number of output vertices $m$ is not a function of $n$ alone. It depends on the geometry, roughly as the integral of $1 / \mathrm{lfs}^2$ over the domain. Ruppert proved that for $B > \sqrt 2$ the number of triangles is within a constant factor of the smallest number in any mesh of the same input whose angles are bounded below by a constant; the factor depends on $B$. With $B = \sqrt 2$ exactly, the termination proof gives no such bound.

With a plain Delaunay structure, each insertion takes time proportional to the walk and the cavity, both $O(m)$ in the worst case, so the algorithm takes $O(m^2)$ time and $O(m)$ space. In practice cavities have constant size, and a good implementation spends most of its time on point location, which brings the running time close to $O(n \log n + m)$. Har-Peled and Üngör gave a variant with a proven $O(n \log n + m)$ bound.

The code also scans all subsegments after each insertion and all vertices when a subsegment is created, so it takes $O(m^2)$ time even on good inputs. Exact rational arithmetic adds the cost of growing denominators.

## Properties

- **Conforming Delaunay output.** The mesh is a true Delaunay triangulation of its vertices, not a constrained one, and the segments are unions of its edges.
- **Angle bound.** Every angle is at least $\arcsin(1/(2B))$, so at least about $20.7°$ for $B = \sqrt 2$. Since the angles sum to $180°$, every angle is also at most $180° - 2 \arcsin(1/(2B))$, about $138.6°$.
- **Grading.** For $B > \sqrt 2$, the edge lengths near every point $x$ are within constant factors of $\mathrm{lfs}(x)$. The mesh is fine near small features and coarse elsewhere.
- **Monotone progress.** Vertices are only added. The final mesh does not depend much on the order of the steps, but the exact vertex set does.
- **Deterministic.** With a fixed queue order, the output is a function of the input.

## Variants and improvements

- **[Chew's second algorithm](/chew-second-algorithm/)** (1993) works with a [constrained Delaunay triangulation](/constrained-delaunay-triangulation/). A circumcenter is rejected only when it is not visible from its triangle. It splits fewer segments and gives smaller meshes, and Shewchuk proved $B \ge \sqrt 5 / 2$, about $26.57°$, for input angles of at least $60°$.
- **Diametral lenses.** Encroachment is tested against a lens instead of a circle. The lens is narrower than the circle, so fewer vertices encroach and fewer segment splits are needed. As in Chew's algorithm, a subsegment that is not visible from the encroaching vertex is not encroached, and free vertices near the midpoint are deleted before a split. Shewchuk shows that its aggressiveness in splitting, and its proven angle bound, lie between those of Ruppert's algorithm and Chew's.
- **Concentric shells.** For inputs with small angles, Ruppert suggested splitting segments near a shared end point at powers of two from that point, so that adjacent segments do not encroach each other in a cycle. Shewchuk's **Terminator** adds rules that skip some splits near small angles, so that the algorithm always stops, leaving bad triangles only near those angles.
- **Off-centers.** Üngör inserts a point between the circumcenter and the shortest edge when the circumcenter would make the new triangles much smaller than needed. This gives smaller meshes for the same bound.
- **Three dimensions.** Shewchuk's tetrahedral refinement uses diametral spheres and a radius-edge bound of $2$, for inputs without acute angles. It does not remove slivers.

## When to use it

Use Ruppert's algorithm when a two-dimensional domain must be meshed with triangles of guaranteed quality, for example for the finite element method, and when a true Delaunay mesh is wanted. It is the algorithm behind the default refinement in Shewchuk's Triangle and in many other mesh generators. In practice the bound can be pushed well past the proven one: the algorithm usually stops for bounds up to about $33°$. For smaller meshes with the same angle bound, use [Chew's second algorithm](/chew-second-algorithm/) or the off-center variant. If the input has small angles, use a version with concentric shells or the Terminator, and accept bad triangles near those angles.

## Pitfalls

- **Small input angles.** The termination proof needs input angles of at least $60°$ (Ruppert asked for $90°$). If two segments meet at a smaller angle, they can encroach each other's subsegments forever. The code keeps Ruppert's hypothesis and rejects boundary angles below $90°$.
- **Bounds below the proof.** The proof needs $B \ge \sqrt 2$. Smaller values often work, but the algorithm can then run forever.
- **The order of the tests.** Line L5 must run only when no subsegment is encroached. Otherwise a circumcenter can fall outside the domain, or on the wrong side of a segment.
- **Rejected triangles.** After the subsegments are split, the skinny triangle may survive. It must go back into the queue, or it may stay skinny.
- **Open or closed disks.** With cocircular vertices, an open diametral disk can leave a subsegment that is not a Delaunay edge. Testing the closed disk avoids this.
- **Boundary insertion.** Midpoints on the boundary of a convex domain lie on hull edges, where the Bowyer and Watson cavity has a degenerate triangle that must be skipped.
- **Rounding.** Circumcenters computed in floating point can land on the wrong side of a segment. Robust predicates for orientation and the in-circle test, and care with the positions of new points, are needed in production code.

## Implementations

The Python version keeps a triangulation as a map from each directed edge to the apex of the triangle on its left. `Mesh.legalize_all` flips non-Delaunay edges for the first triangulation (L1), `Mesh.locate` walks to the triangle that contains a point (L11), and `Mesh.insert` collects the cavity by a search with the exact in-circle test (L12) and joins the new point to its boundary (L13). `ruppert` runs the main loop (L2 to L10) with a queue of encroached subsegments and a queue of possibly skinny triangles. It tests encroachment against the closed diametral disk and compares $R^2$ with $B^2 \ell^2$, so all tests are exact. `_check_input` enforces the hypotheses of the proof, and `ruppert` refuses $B^2 < 2$.

The tests check every output against brute force:

- the triangles are counterclockwise and their exact areas sum to the area of the domain
- there are $2n - h - 2$ triangles and $3n - h - 3$ edges, where $h$ counts the vertices on the boundary, and no two edges cross
- no vertex lies strictly inside the circumcircle of any triangle
- every triangle has $R^2 \le B^2 \ell^2$, and every angle satisfies $\sin^2 \ge 1 / (4 B^2)$
- every subsegment is a mesh edge whose closed diametral disk holds no other vertex, and the subsegments of each input segment form a chain from one end to the other

The inputs are the example, empty boxes, convex polygons with obtuse angles, interior segments and points, small features near the boundary, random domains, and $B = 2$.

## History

Delaunay refinement grew out of work on quality meshing in the late 1980s. Chew's first algorithm (1989) produced uniform meshes with angles of at least $30°$, and Bern, Eppstein and Gilbert (1990) gave the first provably good graded meshes, with quadtrees. Ruppert presented his algorithm at SODA 1993, and the journal version appeared in 1995. It combined the grading of the quadtree method with the simplicity of Delaunay insertion, and proved both termination and size-optimality. Chew's second algorithm appeared in 1993. Shewchuk implemented Ruppert's algorithm in Triangle in 1996, and his 2002 survey gave a unified analysis of both algorithms, including Chew's bound of $26.57°$ and methods for small input angles.

## References
