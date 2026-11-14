---
tag: B7AHTM
kind: algorithm
slug: rossignac-requicha-offsetting
name: Rossignac-Requicha offsetting
aliases:
- constant radius offsetting of CSG
area: cad/solid-modeling
level: advanced
summary: Grows a solid by r as the union of the solid with its faces, edges and vertices swept by r, shrinks it by the dual rule, and rounds or fillets by composing the two.
solves: [solid-offsetting]
model: real-ram
complexity:
  vars: {m: the number of boxes in the CSG tree of the planar version, t: the number of swept primitives that hold a query point on their boundary}
  time: {worst: O(m^3)}
  space: {extra: O(m^2)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1986
  people: [Jaroslaw R. Rossignac, Aristides A. G. Requicha]
  note: Rossignac and Requicha defined growing and shrinking of solids, wrote the grown solid as a union of the solid with offsets of its faces, edges and vertices, and defined rounding and filleting as a shrink followed by a grow and the reverse.
prereqs: [solid-offsetting, constructive-solid-geometry, set-membership-classification]
see_also: [regularized-set-operations, boundary-evaluation, vertex-neighborhood-classification, minkowski-sum, offset-surface, rolling-ball-blend, orientation-test, catastrophic-cancellation]
sources:
  - paper: doi:10.1016/0167-8396(86)90017-8
    title: Jaroslaw R. Rossignac and Aristides A. G. Requicha, Offsetting operations in solid modelling, Computer Aided Geometric Design 3(2), 129 to 148, 1986
    locator: the whole paper (the definitions of growing and shrinking, the decomposition of the grown solid into offsets of faces, edges and vertices, the evaluation for CSG solids, and rounding and filleting)
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the r-sets, the regularized operations and the CSG representation that the method builds on
  - paper: doi:10.1109/TC.1980.1675470
    title: Robert B. Tilove, Set membership classification, a unified approach to geometric intersection problems, IEEE Transactions on Computers C-29(10), 874 to 883, 1980
    locator: the classification of points and sets against a CSG tree, including the neighborhoods needed at boundary points
---

Rossignac and Requicha's method grows a solid $S$ by a distance $r$ without computing any offset surface. It uses the identity $S \uparrow r = S \cup (\partial S) \uparrow r$, and splits the boundary into its faces, edges and vertices, whose offsets are simple solids: a slab for a planar face, a cylinder for a straight edge and a ball for a vertex. The grown solid is therefore a union of known primitives, a [CSG](/constructive-solid-geometry/) tree that a modeler can classify and display at once. Shrinking is growing the complement, and rounding and filleting are a shrink followed by a grow and the reverse. Rossignac and Requicha gave the method in 1986, as part of their definition of [solid offsetting](/solid-offsetting/).

## In plain words

To coat a solid with a layer of thickness $r$, you do not need to move every face and then repair the gaps and overlaps. Instead, take the solid, and add to it a thick plate around every face, a round rod around every edge and a ball around every corner, all of thickness $r$. Where these pieces overlap does not matter: the coated solid is simply everything they cover together.

Shrinking works the other way round. A point stays in the shrunk solid when it is inside the solid and not inside any plate, rod or ball.

The only hard question is at the edge of the result, where you must decide whether a point is inside or exactly on the skin. There the method looks at all the pieces that touch the point and checks whether they close up around it.

## The problem

The input is a solid $S$ as a CSG tree and a distance $r > 0$. The output is a representation of the grown solid $S \uparrow r = \{x : \operatorname{dist}(x, S) \le r\}$ and of the regularized shrunk solid $\operatorname{cl}(\operatorname{int}(S \downarrow r))$, with $S \downarrow r = \{x : x + B_r \subseteq S\}$, as defined on the [solid offsetting](/solid-offsetting/) page. Here the output is a point membership classification, a function that returns *in*, *on* or *out* for each query point, which is the form a CSG system uses to render, to compute [mass properties](/mass-properties-of-solids/) and to evaluate a boundary. The implementation treats the planar case: $S$ is a CSG tree of closed axis-aligned rectangles with rational corners, the faces of $S$ are its boundary segments, and the edge and vertex offsets are rectangles and disks. Touching parts, holes that close exactly and walls of width exactly $2r$ are allowed inputs.

## The algorithm

```pseudo id=main
GROW(S, r)
L1  E, V ← the boundary edges and vertices of S        ▷ boundary evaluation
L2  T ← the union with the one member S
L3  for each edge e in E do add SLAB(e, r) to T        ▷ e swept by r on both sides
L4  for each vertex p in V do add DISK(p, r) to T
L5  return T
CLASSIFY(T, x)
L6  if x is in the interior of S or of a swept member then return in
L7  if x is in no member then return out
L8  if the members with x on their boundary cover a neighborhood of x then return in
L9  return on
SHRINK-CLASSIFY(S, r, x)
L10 if x is not in S then return out
L11 c ← CLASSIFY of x against the swept members of GROW(S, r) alone
L12 return in, on or out when c is out, on or in
```

In three dimensions, line L3 adds the offset of each face, which for a planar face is the prism swept by the face along its normal by $r$ on both sides; edges give cylinders of radius $r$ and vertices give balls of radius $r$. The faces of a B-rep are oriented by the right-hand rule so that their normals point out of the solid, but the swept members are symmetric, so the method needs no orientation. For curved faces the face offset is the region between the two offset surfaces at $\pm r$, which is no longer a primitive of a simple CSG system; this is the main limit of the method.

Line L1 is a [boundary evaluation](/boundary-evaluation/). For a tree of rectangles it is exact and short: the distinct $x$ and $y$ coordinates of the rectangles cut the plane into a grid, the center of each cell is classified against the tree with the [regularized set operations](/regularized-set-operations/), and the boundary is the set of grid edges between a cell inside and a cell outside, merged into maximal segments. The vertices are the ends of these segments.

Line L8 is a neighborhood classification, as in [vertex neighborhood classification](/vertex-neighborhood-classification/). A rectangle with $x$ on its boundary covers a closed cone of directions at $x$: a half plane on a side, a quadrant at a corner. A disk with $x$ on its circle and center $c$ covers only the open half plane of directions $v$ with $v \cdot (c - x) > 0$; along its tangent it misses a thin cusp. The test sorts the axis directions and the tangent directions of the disks by angle, and checks every open sector between two of them, every one of these directions, and the two thin germs on either side of each direction. A germ on the side of a tangent is covered only by a rectangle whose cone holds the whole germ, or by another disk that holds the tangent direction strictly.

Lines L10 to L12 use the dual rule. The swept members of $S$ and of the closure of its complement are the same, since the two sets have the same boundary, so a point of $S$ is in the interior of the shrunk solid exactly when it is in no swept member.

## Example

Let $S$ be the L shape $[0, 2] \times [0, 1] \cup [0, 1] \times [0, 2]$, the union of two rectangles. Line L1 finds six boundary edges, from $(0, 0)$ to $(2, 0)$, $(2, 0)$ to $(2, 1)$, $(1, 1)$ to $(2, 1)$, $(1, 1)$ to $(1, 2)$, $(0, 2)$ to $(1, 2)$ and $(0, 0)$ to $(0, 2)$, and six vertices, of which $(1, 1)$ is the reflex corner. For $r = 1/2$, lines L3 and L4 add six rectangles and six disks; for example the edge from $(1, 1)$ to $(2, 1)$ gives the rectangle $[1, 2] \times [1/2, 3/2]$.

| query point | members that hold it | result of CLASSIFY |
|---|---|---|
| $(5/2, 1/2)$ | the boundary of the slab $[3/2, 5/2] \times [0, 1]$ of the right edge | on, at L9: the slab covers only the half plane to the left |
| $(23/10, -2/5)$ | the circle of the disk at $(2, 0)$, since $(3/10)^2 + (4/10)^2 = 1/4$ | on, at L9: the rounded convex corner |
| $(3/2, 3/2)$ | the boundaries of the slabs $[1, 2] \times [1/2, 3/2]$ and $[1/2, 3/2] \times [1, 2]$ | on, at L9: the two cones leave the open quadrant up and to the right uncovered; this is the sharp concave corner of the grown solid |
| $(5/4, 5/4)$ | the interiors of both slabs and of the disk at $(1, 1)$ | in, at L6 |
| $(8/5, 8/5)$ | none: it is $\sqrt{0.72} > 1/2$ from $(1, 1)$ | out, at L7 |

The grown solid has rounded convex corners and one sharp concave corner, at $(3/2, 3/2)$, where the offset lines of the two edges at the reflex corner meet. Shrinking $S$ by $r = 1/4$ gives the L shape of arms $[1/4, 7/4] \times [1/4, 3/4]$ and $[1/4, 3/4] \times [1/4, 7/4]$, with sharp convex corners and a quarter circle of radius $1/4$ around the reflex corner $(1, 1)$. SHRINK-CLASSIFY returns on for $(1/4, 1/2)$ and $(3/2, 3/4)$, which lie on offset lines, and for $(17/20, 4/5)$, which is at distance exactly $1/4$ from $(1, 1)$. It returns out for $(9/10, 9/10)$, which is inside the disk at $(1, 1)$, and in for $(1/2, 1/2)$.

*Rounding and filleting by hand.* Rounding is $(S \downarrow r) \uparrow r$. Growing the shrunk L by $1/4$ rounds its five convex corners with quarter circles of radius $1/4$, and the quarter circle around $(1, 1)$ grows back to the sharp reflex corner. Each convex corner loses $r^2 - \pi r^2 / 4$, so the area drops by $5(1 - \pi/4)/16$. Filleting is $(S \uparrow r) \downarrow r$. Growing by $1/4$ makes the sharp concave corner at $(5/4, 5/4)$, and shrinking by $1/4$ turns it into a quarter circle of radius $1/4$ about $(5/4, 5/4)$ that meets the edges at $(5/4, 1)$ and $(1, 5/4)$. The convex corners stay sharp, and the area grows by $1/16 - \pi/64$.

*Growing does not commute with intersection.* For $A = [0, 1]^2$, $B = [2, 3] \times [0, 1]$ and $r = 3/4$, the set $A \cap B$ is empty, so $(A \cap B) \uparrow r$ is empty, but $(3/2, 1/2)$ is in both $A \uparrow r$ and $B \uparrow r$. So the method must grow the solid as a whole, from its boundary, and cannot grow the primitives of a tree with intersections or differences.

## Correctness

Every point of a swept member is within $r$ of a point of $\partial S \subseteq S$, so $T \subseteq S \uparrow r$. Conversely, if $x \notin S$ is within $r$ of $S$, its nearest point $y$ in $S$ lies on $\partial S$, on some edge $e$, and the nearest point of $e$ to $x$ is either inside $e$, so that $x$ is in the slab of $e$, or an end of $e$, so that $x$ is in a vertex disk. So $T = S \uparrow r$. For shrinking, the points of $S$ in no swept member are those at distance more than $r$ from $\partial S$, and the regularized shrink is the closure of that set, because the distance to the boundary has no local minimum at a positive value. The neighborhood test of line L8 is exact: if a sector, a direction or a germ is not covered, the proof constructs points arbitrarily close to $x$ that lie in no member, and if all are covered, a whole disk around $x$ is. The [full proof](proofs/correctness.md) gives the details. All tests compare rational numbers, so every decision is exact.

What is proved is the planar method on rectangle trees. The three-dimensional method rests on the same identity, with prisms, cylinders and balls as members, but the neighborhood test of line L8 for those members is not proved here.

## Complexity

The costs are in the [real RAM](/real-ram/), and with rational input every operation is exact. For a tree of $m$ rectangles, the grid has $O(m^2)$ cells, and classifying a cell against the tree costs $O(m)$, so line L1 costs $O(m^3)$. The boundary has $O(m^2)$ grid edges, so lines L3 and L4 add $O(m^2)$ members, and GROW costs $O(m^3)$ time and $O(m^2)$ space. A query costs $O(m^2)$ to test the members and, when $t$ members hold the point on their boundary, $O(t \log t)$ to sort the directions and $O(t^2)$ for the sector and germ checks. In three dimensions the number of members is the number of faces, edges and vertices of $S$, and the classification of a point costs time linear in that number, plus the cost of the neighborhood test at boundary points.

## Properties

- **No offset surfaces are intersected.** The grown solid is a union, so the trimming of offset faces that defeats B-rep offsetting does not arise; its boundary is evaluated only when needed.
- **Topology changes are automatic.** Parts that merge, holes that close and walls that vanish need no special case, because membership is decided point by point.
- **Exact.** With rational input and squared distances, every decision is a comparison of rational numbers, including the decisions at distance exactly $r$.
- **Grow and shrink together.** Both use the same members, so rounding and filleting cost two applications of the same machinery.
- **Not a boundary.** The output is a classification, not a B-rep. A B-rep of the result needs a boundary evaluation of the union, which brings back the intersections of the member surfaces.

## Variants and improvements

- **Curved faces.** For a face on a sphere, a cylinder or a torus, the face offset is bounded by offset surfaces of the same kind, so a CSG system with these primitives can still represent it. General curved faces need [offset surfaces](/offset-surface/) and approximation.
- **Pruning members.** A face, edge or vertex whose offset lies inside the union of the others can be dropped; for example, at a straight run of collinear edges the interior vertices add nothing. Spatial sorting of the members makes a query cheaper.
- **Distance fields.** A sampled [signed distance function](/signed-distance-function/) gives the same sets approximately, by thresholding the distance at $\pm r$, and is the usual choice for meshes and for 3D printing.
- **Rolling-ball blends.** A fillet of a single edge, not of the whole solid, is built by the [rolling-ball method](/rolling-ball-blend/), which traces the path of a ball of radius $r$ touching two faces; filleting by $(S \uparrow r) \downarrow r$ gives the same surface on that edge but changes all concave edges at once.
- **Minkowski sums.** Replacing the ball by another convex body gives the general [Minkowski sum](/minkowski-sum/), where the edge and vertex members become swept copies of that body.

## When to use it

Use the method when the solid is a CSG tree and the result is needed for classification: for clearance and interference checks, for display by ray casting, for tolerance zones and for mass properties of grown or shrunk parts. Use B-rep offsetting when a boundary representation of the offset is needed for further modeling, and accept its harder intersection and trimming steps. For one rounded edge, use a blend; for whole-solid rounding and filleting, use the compositions on this page.

## Pitfalls

- **Growing the leaves of the tree.** $(A \cup B) \uparrow r = A \uparrow r \cup B \uparrow r$, but no such identity holds for intersection or difference, as the example shows. Only a union tree can be grown by growing its leaves.
- **Missing the regularization.** A wall of width exactly $2r$ shrinks to a segment and a square of side $2r$ to a point; without regularization these lower-dimensional pieces stay in the result. Lines L10 to L12 remove them, because such points are covered by members on all sides.
- **Treating a disk like a half plane.** A disk covers the directions along its tangent only outside a thin cusp. In the L shape $[-2, 2] \times [0, 3]$ minus $[0, 2] \times [1, 3]$ with $r = 1/2$, the point $(0, 1/2)$ lies on the offset line $y = 1/2$ of the bottom edge and on the circle around the reflex corner $(0, 1)$, and it is a corner of the slab $[0, 2] \times [1/2, 3/2]$ of the edge from $(0, 1)$ to $(2, 1)$, which covers only the directions up and to the right. The three members leave no open sector uncovered, but points just above the line and to the left of the circle are in none of them, so $(0, 1/2)$ is on the shrunk solid. A test that only looks at sectors calls it out.
- **Rounding.** The decisions compare a squared distance with $r^2$; a point at distance exactly $r$ is a degenerate input, not a rare one, since tolerances and design rules put features at exact distances. Branching on the sign of a rounded difference of nearly equal numbers is an [orientation-test](/orientation-test/) style decision and can fail by [catastrophic cancellation](/catastrophic-cancellation/). The fix is exact rational arithmetic, as here, or a filter that falls back to exact arithmetic near zero.
- **Curved faces in a simple CSG system.** The offset of a curved face is not a slab, and replacing it by a slab of its tangent plane is wrong away from the point of tangency.

## Implementations

## History

Rossignac and Requicha's paper of 1986 defined growing and shrinking of r-sets, proved their main properties, wrote the grown solid as the union of the solid with offsets of its faces, edges and vertices, and showed how to evaluate it in a CSG modeler. It also defined rounding and filleting of a whole solid as $(S \downarrow r) \uparrow r$ and $(S \uparrow r) \downarrow r$, the opening and closing of mathematical morphology. The classification machinery it relies on comes from Requicha's theory of representations and Tilove's set membership classification, both of 1980.

## References
