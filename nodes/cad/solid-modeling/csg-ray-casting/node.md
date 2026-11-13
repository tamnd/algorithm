---
tag: K0WQSY
kind: algorithm
slug: csg-ray-casting
name: CSG ray casting
aliases:
- Roth ray casting of CSG
area: cad/solid-modeling
level: core
summary: Renders or measures a CSG solid by intersecting each ray with the primitives and combining the resulting in and out intervals by the Boolean operations of the tree.
model: real-ram
complexity:
  vars: {L: the number of primitives, m: the number of faces of all primitives, h: the height of the tree}
  time: {worst: O(m + L h)}
  space: {extra: O(L)}
properties: {online: false, deterministic: true, recursive: true}
history:
  year: 1982
  people: [Scott D. Roth]
  note: Roth described ray casting as the base of a CSG solid modeler at General Motors Research, for line drawings, shaded pictures and volume computation.
prereqs: [constructive-solid-geometry, regularized-set-operations, ray-casting, interval-merging]
see_also: [set-membership-classification, ray-object-intersection, ray-plane-intersection, slab-method, bounding-volume-hierarchy, boundary-evaluation, mass-properties-of-solids]
sources:
  - paper: doi:10.1016/0146-664X(82)90169-1
    title: Scott D. Roth, Ray casting for modeling solids, Computer Graphics and Image Processing 18(2), 109 to 144, 1982
    locator: the whole paper (rays against primitives, the combination of the ray intervals by the tree, pictures and volumes)
  - paper: doi:10.1109/TC.1980.1675470
    title: Robert B. Tilove, Set membership classification, a unified approach to geometric intersection problems, IEEE Transactions on Computers C-29(10), 874 to 883, 1980
    locator: the classification of a line segment against a CSG tree, of which the ray is the one-dimensional case
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the sections on CSG representations and the algorithms that evaluate them
---

CSG ray casting finds where a ray meets a solid given by a [CSG tree](/constructive-solid-geometry/). It intersects the ray with each primitive, which gives for each leaf a list of parameter intervals where the ray is inside, and then combines the lists up the tree with the union, intersection and difference of intervals. The first interval end at or after the ray origin is the visible point, and the sum of the interval lengths is the length of the ray inside the solid. Roth made it the base of a solid modeler in 1982, and it is the one-dimensional case of [set membership classification](/set-membership-classification/).

## In plain words

Shoot a straight line through a CSG solid. For each basic shape, find where the line goes in and where it comes out. That gives, for each shape, a few stretches of the line that are inside it.

Now follow the recipe of the solid. For an added shape, join its stretches with the others. For a shape that is cut away, remove its stretches. For a shape that must be common to two parts, keep only the overlap. At the end you have the stretches of the line that are inside the whole solid.

The start of the first stretch in front of the eye is the point that you see, so one line per pixel draws a picture. The total length of the stretches, summed over a grid of parallel lines, estimates the volume. No surface of the solid is ever computed.

## The problem

The input is a CSG tree whose leaves are primitives and whose inner nodes are $\cup^*$, $\cap^*$ and $-^*$, and a ray $o + t d$ with $d \ne 0$. The output is the set of $t \in \mathbb{R}$ with $o + t d$ in the solid, as a sorted list of disjoint closed intervals of positive length. Often only the *first hit* is needed: the least $t \ge 0$ in that set. This page treats the whole line; a ray is the part with $t \ge 0$.

## The algorithm

```pseudo id=main
CAST(o, d, T)                           ▷ sorted disjoint closed intervals of t
L1  if T is a primitive then
L2      return the intervals of o + t d inside T, without those of length 0
L3  A ← CAST(o, d, T.left), B ← CAST(o, d, T.right)
L4  return MERGE(A, B, T.op)

MERGE(A, B, op)
L5  E ← the end points of A and B, sorted, without repeats
L6  for each pair e_j < e_{j+1} of consecutive points of E do
L7      if op(the midpoint is inside A, the midpoint is inside B) then
L8          add [e_j, e_{j+1}], joined with the last interval if that one ends at e_j

FIRST-HIT(o, d, T)
L9  R ← CAST(o, d, T)
L10 for each [t0, t1] in R, in order do
L11     if t1 ≥ 0 then return max(t0, 0)
L12 return none
```

Line L2 depends on the primitive. For a convex polyhedron $\{x : a_i \cdot x \le b_i\}$ it is the [slab method](/slab-method/): each plane bounds $t$ from one side, at $t = (b_i - a_i \cdot o)/(a_i \cdot d)$, and the interval is from the largest lower bound to the smallest upper bound. A sphere or another quadric gives a quadratic in $t$ and up to two interval ends ([ray-sphere intersection](/ray-sphere-intersection/)). A torus gives a quartic. Only this step depends on the kind of surface, which is why Roth's method extends to new primitives with little work.

MERGE is the regularized set operation on the line. Between two consecutive end points, membership in $A$ and in $B$ is constant, so one midpoint decides each open piece. Line L8 makes the result closed and joins pieces that touch, so that no interval of length $0$ appears and no false end point stays between two touching pieces. A merge of the two sorted lists in one pass, with a flag for each list, needs no midpoints and gives the same result.

## Example

Let $A = [0, 1]^3$ and $B = [1, 2] \times [0, 1]^2$ be two unit cubes that share the face $x = 1$, and let $C = [3/2, 5/2] \times [1/4, 3/4]^2$ be a box that cuts a notch into the end of $B$. The solid is $(A \cup^* B) -^* C$. Cast the ray $o = (-1, 1/2, 1/2)$, $d = (1, 0, 0)$, so the point at parameter $t$ has $x = t - 1$.

| node | intervals of $t$ |
|---|---|
| $A$ | $[1, 2]$ |
| $B$ | $[2, 3]$ |
| $A \cup^* B$ | $[1, 3]$ |
| $C$ | $[5/2, 7/2]$ |
| $(A \cup^* B) -^* C$ | $[1, 5/2]$ |

At the union, $E = \{1, 2, 3\}$. Both pieces $(1, 2)$ and $(2, 3)$ are inside, and line L8 joins them, so the shared face at $t = 2$ leaves no trace. At the difference, $E = \{1, 3, 5/2, 7/2\}$ sorted to $1, 5/2, 3, 7/2$. Only $(1, 5/2)$ is inside $A \cup^* B$ and outside $C$. The first hit is $t = 1$, the point $(0, 1/2, 1/2)$ on the left face of $A$, and the ray is inside the solid for a length of $3/2$.

Two more cases. For $A \cap^* B$ the lists $[1, 2]$ and $[2, 3]$ meet only at $t = 2$, so MERGE returns nothing: the touching cubes have an empty regularized intersection. The ray $o = (1, -1, 1/2)$, $d = (-1, 1, 0)$ meets $A$ only at $t = 1$, at the point $(0, 0, 1/2)$ on an edge. Line L2 gets the interval $[1, 1]$ of length $0$ and drops it, so the ray misses $A$.

## Correctness

Assume that the ray does not lie in the plane or on the surface of a face of a primitive. Then the ray crosses the boundaries of the primitives at finitely many parameters, and each open piece between two consecutive crossings lies inside or outside each primitive. On such a piece the regularized solid is all of the piece or none of it, by the same argument as for [set membership classification](/set-membership-classification/). MERGE evaluates the operation on each piece, so by induction on the tree CAST returns the closure of the union of the inside pieces, which is the set of $t$ with $o + t d$ in the solid. The [full proof](proofs/correctness.md) gives the details and the case of a ray in a face plane.

## Complexity

The costs are in the [real RAM](/real-ram/) with exact arithmetic on the ray parameters.

- **Leaves.** A convex polyhedron with $k$ faces costs $O(k)$, so all leaves cost $O(m)$. A convex primitive gives at most one interval.
- **Inner nodes.** A node has at most as many interval ends as the leaves below it have, so at most $2 \ell$ for $\ell$ convex leaves. A linear merge costs $O(\ell)$. Each leaf is below at most $h$ nodes, so all merges cost $O(L h)$, which is $O(L^2)$ for a tree of height $L - 1$ and $O(L \log L)$ for a balanced tree.
- **A picture.** An image of $P$ pixels casts $P$ rays, for $O(P (m + L h))$ in all.

Practical renderers test each subtree against a bounding box first ([axis-aligned bounding box](/axis-aligned-bounding-box/), [bounding volume hierarchy](/bounding-volume-hierarchy/)). An empty subtree under a union is skipped, and an empty left side of an intersection or a difference ends the work at that node.

## Properties

- **No boundary evaluation.** The solid is rendered or measured from the tree alone. No surface of the result is ever built.
- **Exact for the classification.** With exact ray parameters, every interval end and every merge decision is exact. With quadrics the ends are roots of quadratics, and exact comparison needs algebraic numbers.
- **The normal comes from one primitive.** Each interval end is the end of one primitive interval, so the surface normal at a hit is the normal of that primitive. At an end that comes from a subtracted primitive, the normal must be reversed.
- **Parallel.** The rays are independent, so they can be cast at the same time.

## Variants and improvements

- **Volume and moments by rays.** Cast a grid of parallel rays with spacing $s$ and add $s^2$ times the length inside the solid for each ray. This is a quadrature for the [mass properties](/mass-properties-of-solids/) of the solid; its error depends on the grid, and random ray positions turn it into [Monte Carlo integration](/monte-carlo-integration/).
- **Ray representations and dexels.** Storing the intervals of a fixed grid of rays gives a ray representation of the solid. It is used for fast display and for the simulation of machining.
- **Ray tracing of CSG.** A ray tracer adds reflected and refracted rays at each hit. Each of them is cast with the same CAST.
- **Other surfaces.** Any surface with a ray intersection routine can bound a primitive, such as [implicit surfaces](/implicit-surface/) and [signed distance functions](/signed-distance-function/).

## When to use it

Use it to draw a CSG model without a boundary evaluation, for an interactive preview, or to estimate a volume or a center of mass of a CSG solid. It is also a robust way to test a point or a line against a CSG model, because each test involves only one primitive at a time. When the same model is drawn many times, or when exact faces are needed for machining or meshing, compute the boundary once with [boundary evaluation](/boundary-evaluation/).

## Pitfalls

- **Intervals of length zero.** If line L2 keeps $[1, 1]$ for a ray that grazes an edge, a later union shows a lone point as a hit, and a picture shows speckles along the silhouette edges. Drop such intervals at line L2 and at line L8.
- **Touching intervals not joined.** If line L8 adds $[1, 2]$ and $[2, 3]$ as two intervals, the shared face of two touching primitives stays as a false exit and entry at $t = 2$. The first hit is still right, but a count of surfaces, an x-ray picture or a later difference sees a face inside the solid.
- **Rounded ray parameters.** In floating point, the exit from $A$ and the entry into $B$ at a shared face are two separately rounded numbers. If the exit is a little larger, the intersection $A \cap^* B$ returns a sliver interval and a spurious surface. Compare with exact or filtered arithmetic ([geometric robustness problem](/geometric-robustness-problem/)), or move the coincident faces apart in the model.
- **A ray in a face plane.** For the ray $o = (1, -1, 1/2)$, $d = (0, 1, 0)$ in the shared face $x = 1$, both $A$ and $B$ give $[1, 2]$, so line L4 returns $[1, 2]$ for $A \cap^* B$, which is empty in space. The intervals on the line do not see from which side each solid touches the ray. Such rays form a set of measure zero, so a renderer can ignore them, but a point classifier cannot. Classify such a ray with neighborhoods, or perturb it.
- **Normals of subtracted faces.** At an interval end that comes from $C$ in $A -^* C$, the normal of $C$ points into the material of the result. Reverse it, or the shading is wrong on every cut face.

## Implementations

## History

Tilove's set membership classification of 1980 already classified line segments against a CSG tree. Scott Roth, at General Motors Research, made ray casting the base of a solid modeling system and published the method in 1982: it rendered line drawings and shaded pictures and computed volumes from the ray intervals.

## References
