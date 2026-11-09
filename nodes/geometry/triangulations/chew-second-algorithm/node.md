---
tag: R64BJ4
kind: algorithm
slug: chew-second-algorithm
name: Chew's second algorithm
aliases:
- Chew's Delaunay refinement
- Chew's second mesh algorithm
- Chew's constrained Delaunay refinement
area: geometry/triangulations
level: advanced
summary: Constrained Delaunay refinement producing triangles with minimum angle 30 degrees.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {n: the number of input vertices, m: the number of vertices inserted}
  time: {worst: O(m^2)}
  space: {extra: O(m)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1993
  people: [L. Paul Chew]
  note: Chew presented the algorithm at the 1993 Symposium on Computational Geometry, in a paper on meshing curved surfaces. It refines a constrained Delaunay triangulation, splits a segment only when a circumcenter falls behind it, and deletes nearby free vertices before the split. Shewchuk's 2002 survey gave the analysis of the basic version with grading and size optimality.
prereqs: [delaunay-refinement, constrained-delaunay-triangulation, ruppert-algorithm, in-circle-test, circumcenter, edge-flip, ear-clipping]
see_also: [ruppert-algorithm, mesh-generation, delaunay-refinement, constrained-delaunay-triangulation, constrained-triangulation, steiner-points, max-min-angle-triangulation, lawson-flip-algorithm]
sources:
  - paper: "L. Paul Chew, Guaranteed-quality mesh generation for curved surfaces, Proceedings of the 9th Annual Symposium on Computational Geometry, 274 to 280 (1993)"
    locator: the algorithm on constrained Delaunay triangulations, the rejection of circumcenters that lie behind a segment, the deletion of vertices before a segment split, and the 30 degree bound
  - paper: doi:10.1016/S0925-7721(01)00047-5
    title: Jonathan Richard Shewchuk, Delaunay refinement algorithms for triangular mesh generation, Computational Geometry 22(1-3), 21 to 74 (2002)
    locator: Section 4 (Chew's second algorithm, its termination for B at least the square root of 5 over 2 with input angles of at least 60 degrees, grading and size optimality), Section 6.4 (diametral lenses), Section 7.3 (Chew's 30 degree bound)
  - paper: doi:10.1007/BF01553881
    title: L. Paul Chew, Constrained Delaunay triangulations, Algorithmica 4, 97 to 108 (1989)
    locator: the definition of constrained Delaunay triangulations and the local characterization by edges
  - paper: "L. Paul Chew, Guaranteed-quality triangular meshes, Technical Report TR 89-983, Department of Computer Science, Cornell University (1989)"
    locator: Chew's first algorithm, uniform meshes with angles of at least 30 degrees (report number to be checked)
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: Chapter 2 (the constrained Delaunay lemma) and Chapter 6 (two-dimensional Delaunay refinement) (ISBN to be checked)
---

Chew's second algorithm is a [Delaunay refinement](/delaunay-refinement/) method for quality [mesh generation](/mesh-generation/) in the plane. Unlike [Ruppert's algorithm](/ruppert-algorithm/), it works on a [constrained Delaunay triangulation](/constrained-delaunay-triangulation/), where segments block visibility. A skinny triangle gets a new vertex at its [circumcenter](/circumcenter/), unless a segment piece lies between the triangle and that point. Then the piece is split at its midpoint, and first every free vertex inside the circle with that piece as diameter, and visible from the midpoint, is deleted. Shewchuk proved that the basic algorithm stops for every bound $B \ge \sqrt 5 / 2$ on circumradius over shortest edge, which means angles of at least $\arcsin(1/\sqrt 5) \approx 26.57°$, when no two input segments meet at less than $60°$; for $B > \sqrt 5 / 2$ the mesh is also graded and within a constant factor of the smallest. Chew's own bound of $30°$ needs a different choice of the new point.

## In plain words

Start with a mesh of the shape where the outline and the inner lines are always kept as edges, and lines block the view like walls. Then fix thin triangles one at a time.

For a thin triangle, find the center of the circle through its corners. If you can walk from the triangle to that center without crossing a wall, put a new corner there.

If a wall is in the way, the triangle is too close to that wall. Cut the nearest such wall piece in half instead. Before adding the midpoint, remove the extra corners that sit inside the circle around that piece and can see its middle, so that the new corner does not land too close to them.

Walls are only cut when something really falls behind them, so fewer extra corners are needed than with similar methods.

## The problem

The input is a planar straight-line graph: a domain $\Omega$ with its boundary edges, a set of segments and a set of points inside. The output is a triangulation of $\Omega$ whose vertices include the input points, in which every input segment is a union of edges, and in which every triangle has circumradius $R$ and shortest edge $\ell$ with $R \le B \ell$. By the law of sines, $\ell = 2 R \sin \theta_{\min}$, so the bound means that every angle is at least $\arcsin(1/(2B))$. New vertices, called [Steiner points](/steiner-points/), may be added, and here some of them may also be removed again.

The code works under the hypotheses of the termination proof, in a simple setting. The domain is a strictly convex polygon given counterclockwise, with all angles at least $60°$. The segments and points lie strictly inside and touch neither each other nor the boundary. Coordinates are integers or `Fraction`s, and the bound is given as $B^2 \ge 5/4$.

## The algorithm

A segment is cut into **subsegments** by the vertices on it. A point $u$ **sees** a vertex $w$ when the open segment $uw$ meets no subsegment except $uw$ itself. A triangle is **constrained Delaunay** when no vertex seen from its interior lies strictly inside its circumcircle. Input vertices and midpoints of subsegments are kept forever. The circumcenters, called **free vertices**, may be deleted.

```pseudo id=main
CHEW(Ω, S, Q, B)                           ▷ Ω convex with angles at least 60°, B at least √5/2
L1  T ← constrained Delaunay triangulation of the corners of Ω, the end points of S and the points Q, with the segments as edges
L2  while some triangle t of T has R(t) > B ℓ(t) do
L3      c ← the circumcenter of t; x ← the centroid of t
L4      if the closed segment from x to c meets no subsegment then
L5          insert c
        else
L6          s ← the subsegment that the segment from x to c meets first; m ← its midpoint
L7          delete every free vertex strictly inside the diametral circle of s that sees m
L8          insert m, replacing s by its two halves; keep t in the queue
L9  return T and the subsegments

INSERT(q)
L10 find the triangle that contains q
L11 split it into three, or split the triangles on both sides of the edge that contains q
L12 flip every edge that is not a subsegment and whose opposite vertex is inside the circumcircle

DELETE(v)
L13 remove the triangles around v, triangulate the hole by ear clipping, and flip as in L12
```

Four facts make the rules work together.

- **The mesh stays constrained Delaunay.** Lawson's flips stop, and a triangulation in which every edge that is not a subsegment is locally Delaunay has only constrained Delaunay triangles. Subsegments are edges by construction, so no extra check is needed for them.
- **A visible circumcenter is far from every vertex it sees.** If nothing blocks the way from $t$ to $c$, then $c$ lies in the domain, and no vertex that $c$ sees is closer than $R$. Vertices hidden behind a segment may be closer, but they will not be joined to $c$.
- **A blocked circumcenter puts the triangle near the segment.** If a subsegment $ab$ lies in the way, all three corners of $t$ lie in the half of the diametral disk of $ab$ on the side of $t$. So $ab$ is not much longer than the triangle's short edges.
- **Deletion prevents short edges.** After the free vertices near the midpoint are deleted, the midpoint sees only vertices at distance at least half of $|ab|$, or input and segment vertices, which are far for other reasons.

## Example

Take the box with corners $v_0 = (0, 0)$, $v_1 = (6, 0)$, $v_2 = (6, 4)$, $v_3 = (0, 4)$ and one input point $v_4 = (2, 1)$, with $B^2 = 5/4$. This is the input of the example of [Ruppert's algorithm](/ruppert-algorithm/). The first triangulation has four triangles, the worst being $v_0 v_1 v_4$ with $R^2 / \ell^2 = 4.25$. The algorithm takes these steps:

| step | skinny triangle | $R^2 / \ell^2$ | circumcenter | action |
|---|---|---|---|---|
| 1 | $v_0 v_1 v_4$ | $17/4 = 4.25$ | $(3, -7/2)$, below the bottom edge | split $v_0 v_1$ at $v_5 = (3, 0)$; nothing to delete |
| 2 | $v_2 v_4 v_5$ | $625/196 \approx 3.19$ | $(59/14, 31/14)$, visible | insert it as a free vertex $f$ |
| 3 | $v_2 v_3 f$ | $2053/1250 \approx 1.64$ | $(3, 73/14)$, above the top edge | delete $f$, which lies inside the circle on $v_2 v_3$ and sees its midpoint; split at $v_6 = (3, 4)$ |
| 4 | $v_4 v_5 v_6$ | $5/2$ | $(4, 2)$, visible | insert $v_7 = (4, 2)$ |

At step 2, Ruppert's algorithm rejects the same circumcenter because it lies in the diametral circles of the right and top edges, and splits both. Chew's algorithm accepts it, because no segment lies between it and its triangle, and later removes it when it gets in the way of a split. After step 4 no triangle is skinny. The mesh has 8 vertices, 6 of them on the boundary, and 8 triangles:

$$v_0 v_4 v_3,\ v_0 v_5 v_4,\ v_1 v_2 v_7,\ v_1 v_7 v_5,\ v_2 v_6 v_7,\ v_3 v_4 v_6,\ v_4 v_5 v_7,\ v_4 v_7 v_6 .$$

This matches the counts for $n = 8$ points with $h = 6$ on the hull: $2n - h - 2 = 8$ triangles and $3n - h - 3 = 15$ edges. The smallest angle is $26.57°$ and the largest ratio $R / \ell$ is $\sqrt 5 / 2 \approx 1.118$, exactly at the bound. Ruppert's algorithm with $B = \sqrt 2$ gives 10 triangles here.

## Correctness

The [correctness proof](proofs/correctness.md) follows Shewchuk's analysis, with the deletions and the visibility arguments written out. The mesh stays a triangulation of $\Omega$ made of constrained Delaunay triangles, with the subsegments as edges, and the queue always holds every skinny triangle. So at the end every segment is a chain of edges and every triangle has $R \le B \ell$.

Termination uses the **insertion radius** $r_v$ of a vertex, its distance to the nearest vertex it sees right after its insertion, and the **local feature size** $\lambda = \min \mathrm{lfs}$. The proof shows that midpoints have $r_v \ge \lambda$ and free vertices have $r_v \ge \lambda / \cos \theta$, where $\sin \theta = 1/(2B)$.

- A circumcenter has $r_c \ge R > B \ell \ge B \lambda$, and $B \cos \theta \ge 1$ exactly when $B^2 \ge 5/4$.
- For a midpoint $m$ of a subsegment of half length $h$, the corners of the skinny triangle lie in the half disk, so its shortest edge satisfies $\ell < h / \cos \theta$. If the younger end of that edge is free, this gives $h > \lambda$. It cannot be an end point of the subsegment, because the deletion at that end point's own split would have removed the other end of the edge. Input and segment vertices near $m$ lie on other features, or on a neighboring boundary edge at an angle of at least $60°$, and are at distance at least $\lambda$.

So subsegments never get shorter than $\lambda$, splits and deletions are finitely many, and between splits only finitely many vertices fit in the domain.

## Complexity

The number of output vertices depends on the geometry, not on $n$ alone, as for Ruppert's algorithm. For $B > \sqrt 5 / 2$, Shewchuk proved that the mesh is graded, with edge lengths near each point within constant factors of the local feature size, and that the number of triangles is within a constant factor of the smallest number in any mesh of the same input with the same kind of angle bound. With $B = \sqrt 5 / 2$ exactly, the proof gives termination only.

Let $m$ count every vertex inserted, including those deleted later. With a plain triangulation structure, an insertion or a deletion costs $O(m)$ for point location and flips in the worst case, so the algorithm takes $O(m^2)$ time and $O(m)$ space. The code also scans all subsegments for every skinny triangle and every candidate for deletion, which keeps it at $O(m^2)$ on good inputs too. Deletions are rare in practice: they happen only at segment splits.

## Properties

- **Constrained Delaunay output.** The mesh is a constrained Delaunay triangulation of its vertices, not always a Delaunay one. A vertex hidden behind a segment may lie inside a circumcircle.
- **Angle bound.** Every angle is at least $\arcsin(1/(2B))$, so at least about $26.57°$ for $B = \sqrt 5 / 2$, and at most $180° - 2 \arcsin(1/(2B))$, about $126.9°$.
- **Fewer segment splits.** A subsegment is split only when a circumcenter lies behind it, which implies that a vertex of the triangle encroaches its diametral circle. So it never splits a subsegment that Ruppert's algorithm would keep, and it often keeps one that Ruppert's would split.
- **Non-monotone.** Free vertices may be deleted, so the vertex set does not only grow.
- **Deterministic.** With a fixed queue order, the output is a function of the input.

## Variants and improvements

- **Chew's $30°$ bound.** Chew proved termination for angles up to $30°$, that is $B = 1$, by moving the inserted point when a circumcenter is close to a segment; Shewchuk discusses this in Section 7.3 of his survey. That bound comes with no guarantee of grading or size optimality.
- **[Ruppert's algorithm](/ruppert-algorithm/).** Works on a true Delaunay triangulation and splits a subsegment whenever a vertex lies in its diametral circle. Its proven bound is $B \ge \sqrt 2$, about $20.7°$, and its output is Delaunay.
- **Diametral lenses.** A hybrid of the two tests encroachment with a lens, narrower than the diametral circle, and deletes free vertices before a split as Chew does. Its aggressiveness and its proven angle bound lie between those of Ruppert's and Chew's algorithms.
- **Off-centers.** Üngör inserts a point between the circumcenter and the shortest edge, which gives smaller meshes for the same bound.
- **Small input angles.** With input angles below $60°$, Shewchuk's modifications protect the sharp corners and leave bad triangles only near them.

## When to use it

Use Chew's second algorithm when a two-dimensional domain must be meshed with a guaranteed angle bound and a constrained Delaunay mesh is acceptable, which is the case for most finite element and finite volume uses. It gives a better proven bound than Ruppert's algorithm, and when segments are long compared to the local feature size it gives clearly fewer triangles: Shewchuk reports 423 triangles against 559 for one input with the same angle bound. If the application needs a truly Delaunay mesh, for example to use its Voronoi dual, use [Ruppert's algorithm](/ruppert-algorithm/). If segments are short, the two give nearly the same mesh.

## Pitfalls

- **Small input angles.** The proof needs input angles of at least $60°$. At a sharper corner, splits on the two sides can feed each other forever. The code rejects such inputs.
- **Bounds below the proof.** The basic algorithm is proven only for $B \ge \sqrt 5 / 2$. Larger angle bounds often work in practice, but can loop.
- **Visibility, not distance.** The test of line L4 is whether a subsegment lies between the triangle and the circumcenter, not whether the circumcenter is near a subsegment. A circumcenter next to a segment but on the triangle's side is accepted.
- **The first subsegment only.** When several subsegments lie between the triangle and its circumcenter, split only the first one met. The others may be far from the triangle, and splitting them can create short edges.
- **Deleting the wrong vertices.** Only free vertices strictly inside the diametral circle that see the midpoint are deleted. Deleting an input vertex or a segment vertex would change the input or break a segment.
- **Rejected triangles.** After a split the skinny triangle may survive. It must go back into the queue.
- **Hidden vertices.** Because the output is only constrained Delaunay, a test that checks the empty circle against all vertices will fail. Check visibility from the triangle, or check the local condition on edges that are not subsegments.
- **Rounding.** Circumcenters computed in floating point can land on the wrong side of a segment, which changes the decision of line L4. Robust predicates are needed in production code.

## Implementations

The Python version keeps a triangulation as a map from each directed edge to the apex of the triangle on its left, with a set of constrained edges for the subsegments. `Mesh.locate` finds the triangle that contains a point (L10), `Mesh.insert` splits it or the two triangles beside an edge (L11), and `Mesh.legalize` flips edges that are not subsegments and fail the exact in-circle test (L12). `Mesh.delete` removes a free vertex and triangulates its hole by ear clipping (L13), and `Mesh.insert_segment` recovers an interior segment for the first triangulation (L1). `chew` runs the main loop (L2 to L9) with a queue of possibly skinny triangles. It finds the first subsegment met by the segment from the centroid to the circumcenter with `first_meet`, and tests visibility from the midpoint with `open_meets`. All tests are exact. `_check_input` enforces the hypotheses of the proof, and `chew` refuses $B^2 < 5/4$.

The tests check every output against brute force:

- the triangles are counterclockwise and their exact areas sum to the area of the domain
- there are $2n - h - 2$ triangles and $3n - h - 3$ edges, where $h$ counts the vertices on the boundary, and no two edges cross
- every subsegment is a mesh edge, and the subsegments of each input segment form a chain from one end to the other
- no vertex strictly inside a circumcircle is seen from the triangle's centroid, and every edge that is not a subsegment is locally Delaunay
- every triangle has $R^2 \le B^2 \ell^2$, and every angle satisfies $\sin^2 \ge 1 / (4 B^2)$

The inputs are the example, empty boxes and polygons with corners between $60°$ and $90°$, interior segments and points, small features, random parallelograms, $B^2 = 2$, and an input whose output is not Delaunay.

## History

Chew's first algorithm, in a 1989 Cornell technical report, produced meshes of uniform density with angles of at least $30°$, by cutting segments into pieces of nearly equal length before refining. His second algorithm appeared at the 1993 Symposium on Computational Geometry, in a paper on meshes for curved surfaces. It replaced the uniform splitting by splits on demand, which allows graded meshes. Ruppert's algorithm, published at the same time, used diametral circles on a Delaunay triangulation instead. Shewchuk's 2002 survey analyzed both in a common framework: it showed that Chew's algorithm, in its basic form, terminates for $B \ge \sqrt 5 / 2$ with input angles of at least $60°$, with grading and size optimality for larger $B$, and it compared the two in practice. Shewchuk's mesh generator Triangle builds on ideas from both algorithms.

## References
