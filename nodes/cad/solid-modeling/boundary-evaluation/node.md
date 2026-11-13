---
tag: G7ANN6
kind: algorithm
slug: boundary-evaluation
name: Boundary evaluation
aliases:
- CSG to B-rep conversion
area: cad/solid-modeling
level: core
summary: Computes the B-rep of a CSG solid by intersecting the faces of the primitives, classifying the pieces against the tree and keeping those on the boundary.
solves: [solid-boolean-operations]
model: real-ram
complexity:
  vars: {m: the number of faces of all primitives}
  time: {worst: O(m^4)}
  space: {extra: O(m^3)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1985
  people: [Aristides A. G. Requicha, Herbert B. Voelcker]
  note: Requicha and Voelcker described boundary evaluation of CSG solids by generating candidate faces and classifying them with neighborhoods, on top of Tilove's set membership classification.
prereqs: [constructive-solid-geometry, boundary-representation, regularized-set-operations, set-membership-classification]
see_also: [csg-ray-casting, vertex-neighborhood-classification, mesh-boolean-operations, mesh-arrangements, surface-surface-intersection, line-arrangement, brep-to-csg-conversion, mass-properties-of-solids]
sources:
  - paper: doi:10.1109/PROC.1985.13108
    title: Aristides A. G. Requicha and Herbert B. Voelcker, Boolean operations in solid modeling, boundary evaluation and merging algorithms, Proceedings of the IEEE 73(1), 30 to 44, 1985
    locator: the whole paper (the generate and classify scheme, the candidate faces, the classification with neighborhoods, and the merging of a new primitive into a B-rep)
  - paper: doi:10.1109/TC.1980.1675470
    title: Robert B. Tilove, Set membership classification, a unified approach to geometric intersection problems, IEEE Transactions on Computers C-29(10), 874 to 883, 1980
    locator: the classification of a face against a CSG tree, which is the classify step
  - paper: doi:10.1145/49155.51123
    title: Jaroslaw R. Rossignac and Herbert B. Voelcker, Active zones in CSG for accelerating boundary evaluation, redundancy elimination, interference detection, and shading algorithms, ACM Transactions on Graphics 8(1), 51 to 87, 1989
    locator: the definition of the active zone of a primitive and its use to skip classifications in boundary evaluation
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the sections on the conversion between representations, where boundary evaluation turns a CSG representation into a boundary representation
---

Boundary evaluation turns a solid given by a [CSG tree](/constructive-solid-geometry/) into a [boundary representation](/boundary-representation/). The boundary of the result lies on the faces of the primitives, so the algorithm *generates* candidates by cutting every face of every primitive along the surfaces of the other primitives, and then *classifies* each piece against the whole tree. A piece is kept when the solid lies on one side of it and not on the other, and it is oriented so that its normal points away from the solid. Requicha and Voelcker described this generate and classify scheme in 1985, with [set membership classification](/set-membership-classification/) as the classify step.

## In plain words

A CSG solid is a recipe of boxes, cylinders and other basic shapes that are added, cut away or intersected. Its skin is made of parts of the skins of the basic shapes. Boundary evaluation finds which parts.

First it cuts each face of each shape into pieces, wherever another shape's surface crosses it. Then it looks at each piece from both sides. Just in front of the piece, is that point in the final solid? And just behind it? If the answers are the same, the piece is inside the solid or outside it, and it is thrown away. If they differ, the piece is part of the skin.

The kept pieces are turned to face out of the solid. Two shapes that share a flat face give the same piece twice, so one copy is dropped. The kept pieces, glued at their edges, form the boundary model.

## The problem

The input is a CSG tree whose leaves $P_0, \ldots, P_{L-1}$ are primitives and whose inner nodes are $\cup^*$, $\cap^*$ and $-^*$. The output is a boundary representation of the solid $X$ of the tree: a set of oriented faces whose union is $\partial X$, with disjoint relative interiors, each face ordered counterclockwise around the normal that points out of $X$ (the right-hand rule). This is [solid Boolean operations](/solid-boolean-operations/) with CSG input. On this page the primitives are bounded convex polyhedra $P_i = \{x : a \cdot x \le b \text{ for } (a, b) \in H_i\}$ with nonempty interior, the faces are convex polygons, and the adjacency between faces is left to the B-rep structure.

## The algorithm

```pseudo id=main
BOUNDARY-EVALUATION(T)
L1  K ← empty list
L2  for each primitive P_i of T and each face f of P_i, with outward normal n do
L3      Q ← [f]
L4      for each plane π of each primitive P_j with j ≠ i do
L5          replace each polygon of Q that π cuts by its two parts
L6      for each piece g in Q do
L7          c ← the mean of the vertices of g          ▷ a point inside g
L8          if c is on the boundary of some P_j with j < i then skip g
L9          front ← T at c + εn, back ← T at c − εn    ▷ ε > 0 infinitely small
L10         if back and not front then append g to K
L11         else if front and not back then append g, reversed, to K
L12 return K
```

Line L9 evaluates the plain Boolean formula of the tree with the truth value of each leaf at the point just in front of $c$ or just behind it. A half-space $a \cdot x \le b$ contains $c + s \varepsilon n$ for all small $\varepsilon > 0$ when $a \cdot c < b$, or when $a \cdot c = b$ and $s \, (a \cdot n) < 0$. The pair (front, back) is the *neighborhood* of the face point $c$ in the sense of Requicha and Voelcker: the two half-balls on the two sides of the face. The classes in, on and out alone cannot decide a piece in the plane of a face of another primitive, and the neighborhood can.

Line L8 removes copies. Two primitives with coplanar faces give the same piece twice, once from each face, and the copy from the primitive of least index is the one that stays. The front and back of both copies agree, up to a swap when the normals are opposite, so either copy gives the same oriented face.

All signs are tests of a point against a plane, which is the [orientation test](/orientation-test/) in three dimensions. With integer or rational input, the cut points of line L5 are rational and every sign is exact.

## Example

Let $A = [0, 2]^3$ and $B = [1, 3]^3$ be two cubes that overlap in the unit cube $[1, 2]^3$, and let the solid be $A -^* B$, a cube of edge $2$ with a corner removed. The top face $z = 2$ of $A$, with $n = (0, 0, 1)$, is cut by the planes $x = 1$ and $y = 1$ of $B$ into four unit squares. The face $x = 1$ of $B$, with $n = (-1, 0, 0)$, is cut by the planes $y = 2$ and $z = 2$ of $A$ into four unit squares. The other planes of the two cubes miss these faces or are parallel to them.

| piece | center $c$ | front | back | action |
|---|---|---|---|---|
| top of $A$, $[0, 1] \times [0, 1]$ | $(1/2, 1/2, 2)$ | out of $A$: false | in $A$, out of $B$: true | keep |
| top of $A$, $[1, 2] \times [1, 2]$ | $(3/2, 3/2, 2)$ | out of $A$: false | in $A$ and $B$: false | drop |
| $x = 1$ of $B$, $y, z \in [1, 2]$ | $(1, 3/2, 3/2)$ | in $A$, out of $B$: true | in $A$ and $B$: false | keep, reversed |
| $x = 1$ of $B$, $y, z \in [2, 3]$ | $(1, 5/2, 5/2)$ | out of $A$: false | out of $A$: false | drop |

The third row is a face of the subtracted cube. Its normal $(-1, 0, 0)$ points into the material of $A -^* B$, so it is reversed to $(1, 0, 0)$, which points into the removed corner. In all, $A$ gives $21$ squares (four on each far face and three on each near face) and $B$ gives the $3$ squares of $[1, 2]^3$ that face $A$. The $24$ kept squares enclose the volume $8 - 1 = 7$, computed from them by the divergence theorem. The same pieces with other front and back rules give $42$ squares and volume $15$ for $A \cup^* B$, and $6$ squares and volume $1$ for $A \cap^* B$.

Touching cubes show the coplanar case. For $D = [0, 1]^3$ and $C = [1, 2] \times [0, 1]^2$, the face $x = 1$ of $D$ has front in $C$ and back in $D$. For $D \cup^* C$ both are true and the face is dropped, which leaves the $10$ outer squares of a box of volume $2$. For $D \cap^* C$ both are false, and the result is empty: the shared face is not a solid.

## Correctness

The boundary of the solid lies on the boundaries of the primitives, so it is covered by the faces and hence by the pieces. After line L5, no plane of another primitive crosses the inside of a piece, so on each side of a piece every primitive is all or nothing, and the regularized solid is all or nothing as well by fact 7 of the [regularized set operations](/regularized-set-operations/). So a piece is on the boundary exactly when front and back differ, and the side where the value is true is the side of the solid. Two pieces in one plane from two primitives are cells of the same arrangement, so they are equal or meet only at their edges, and line L8 keeps one copy. The [full proof](proofs/correctness.md) gives the lemmas and the orientation.

## Complexity

The costs are in the [real RAM](/real-ram/), with exact arithmetic on rational coordinates.

- **Generate.** The $m$ planes cut a face as an arrangement of at most $m$ lines in the plane of the face ([line arrangement](/line-arrangement/)), which has $O(m^2)$ cells of total size $O(m^2)$. Cutting all current pieces by one more plane costs their total size, so one face costs $O(m^3)$ and all faces cost $O(m^4)$.
- **Classify.** There are $O(m^3)$ pieces, and lines L8 and L9 test the center of each against all $m$ half-spaces, for $O(m^4)$.
- **Space.** One face holds $O(m^2)$ pieces at a time, and the output can have $O(m^3)$ pieces.

The bound is far from tight for real models, where most planes miss most faces. A practical version cuts a face only by the primitives whose bounding boxes meet it ([axis-aligned bounding box](/axis-aligned-bounding-box/)) and merges coplanar kept pieces into one face.

## Properties

- **Exact.** With rational input, every vertex is a rational point and every decision is an exact sign, so the output is the exact boundary.
- **Degenerate input needs no special case.** Coplanar faces, touching primitives and faces that meet along an edge are handled by the side tests and by line L8.
- **Not merged.** The output is a set of convex polygons. Neighboring coplanar pieces are not joined, and the faces may meet edge to edge or at T-junctions.
- **Local.** Each piece is classified on its own, so the pieces can be processed in parallel.

## Variants and improvements

- **Active zones.** Rossignac and Voelcker defined the active zone of a primitive: the region where a change of the primitive changes the solid. A face piece outside the active zone of its primitive cannot be on the boundary, so it needs no classification, and the zone also detects redundant primitives.
- **Merging.** Instead of evaluating the whole tree at once, the B-rep is built incrementally: the B-rep of the left subtree is combined with the next primitive by one Boolean operation on B-reps. That operation is [vertex neighborhood classification](/vertex-neighborhood-classification/) or another B-rep Boolean algorithm.
- **Curved primitives.** With quadrics or spline surfaces, line L5 cuts a face along an intersection curve, which needs [surface surface intersection](/surface-surface-intersection/), and the side tests use the surface normal.
- **Meshes.** For triangle meshes the same generate and classify idea works on the arrangement of the triangles ([mesh arrangements](/mesh-arrangements/), [mesh Boolean operations](/mesh-boolean-operations/)), with a winding number as the classifier.

## When to use it

Use boundary evaluation when a CSG model must be shown or used as faces and edges: for machining, meshing, drawing many times, or computing [mass properties](/mass-properties-of-solids/) by surface integrals. For one picture, a volume estimate or a point test, [CSG ray casting](/csg-ray-casting/) and set membership classification need no boundary at all. When the input is already two B-reps, a B-rep Boolean algorithm works on them directly.

## Pitfalls

- **Classifying the center only.** A piece in the plane of a face of another primitive is on that primitive for its center, so in, on and out cannot say whether it stays. In the touching cubes the shared face is on both primitives, and only the front and back values show that it is inside the union and outside the intersection.
- **Keeping both coplanar copies.** Without line L8, the faces of $A \cup^* E$ for $E = [1, 2] \times [0, 2]^2$ contain the face $x = 2$ twice, once from each box. The volume by the divergence theorem is then wrong, and a B-rep built from the list is not a manifold.
- **Forgetting to reverse.** Faces that come from a subtracted primitive must be reversed at line L11. Without this, every cut face of a difference has its normal into the solid.
- **Rounded cut points.** In floating point, a cut point of line L5 is rounded, and a later plane may then cut a piece that it only touches. The pieces of two faces no longer match along their common edge, and the side test of a thin piece can give the wrong sign. Use exact or filtered predicates; see the [geometric robustness problem](/geometric-robustness-problem/) and [exact geometric computation](/exact-geometric-computation/).

## Implementations

## History

Requicha's survey of 1980 described the conversion from a CSG representation to a boundary representation as one of the basic algorithms of a solid modeler. Tilove's set membership classification of the same year gave the classify step. Requicha and Voelcker published the generate and classify algorithms for boundary evaluation and merging in 1985, and Rossignac and Voelcker's active zones of 1989 cut the number of classifications.

## References
