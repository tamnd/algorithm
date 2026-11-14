---
tag: C1TYAG
kind: algorithm
slug: quadtree-mesh-generation
name: Quadtree mesh generation
aliases:
- Bern-Eppstein-Gilbert meshing
area: cad/mesh-generation-for-analysis
level: advanced
summary: Bern, Eppstein and Gilbert's triangulation of a planar point set from a balanced quadtree, with aspect ratio at most 4 and a size within a constant factor of the optimum.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {n: the number of input points, k: the number of output triangles}
  time: {worst: O(n log n + k)}
  space: {extra: O(k)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1990
  people: [Marshall Bern, David Eppstein, John Gilbert]
  note: Bern, Eppstein and Gilbert gave the quadtree method at FOCS 1990, with the journal version in 1994. It was the first mesh generator with both a bound on the element shape and a size within a constant factor of the optimum.
prereqs: [quadtree, mesh-generation, mesh-quality-measures]
see_also: [octree-mesh-generation, ruppert-algorithm, delaunay-refinement, chew-second-algorithm, mesh-sizing-function, advancing-front-mesh-generation, delaunay-triangulation, orientation-test]
sources:
  - paper: doi:10.1016/S0022-0000(05)80059-5
    title: Marshall Bern, David Eppstein and John Gilbert, Provably good mesh generation, Journal of Computer and System Sciences 48(3), 1994, 384 to 409
    locator: Section 2 (crowded boxes C1 to C3, warping, Lemma 1 with aspect ratio at most 4, Theorem 1, Corollaries 1 and 2), Section 3 (Theorem 2, no obtuse angles), Section 5 (Lemma 7, aspect ratio at most 5 and angles of at least 18.4 degrees for segments and polygons)
  - paper: doi:10.1109/FSCS.1990.89542
    title: Marshall Bern, David Eppstein and John Gilbert, Provably good mesh generation, Proceedings of the 31st Annual Symposium on Foundations of Computer Science (FOCS), 1990, 231 to 241
    locator: the conference version of the quadtree method (general locator)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, 3rd edition, Springer, 2008
    locator: Chapter 14, Quadtrees, Non-Uniform Mesh Generation (balanced quadtrees and the balancing step)
---

Quadtree mesh generation, in the form of Bern, Eppstein and Gilbert, triangulates a set of points in the plane. It refines a quadtree until each input point sits in a small box of its own with eight equal neighbors. It balances the tree so that boxes that share a side differ in size by at most a factor of 2. It moves the box corner nearest to each point onto the point and cuts every box into triangles by a fixed template. The result has every input point as a vertex, every triangle has aspect ratio at most 4, which gives every angle at least $\arcsin(1/4) \approx 14.48°$, and the number of triangles is within a constant factor of the least number that any triangulation with that aspect ratio can have. Both the shape bound and the size bound are proved results.

## In plain words

Put a big square around the points. Cut a square into four whenever it holds two points, or a point that has another point too near, or a point that has a cut square close by. Then cut more squares until no square has a much smaller square next to it. Now every point is alone in a small square. Pull the nearest square corner onto the point. Last, cut each square into triangles. A square that did not move gets a center point and becomes right isosceles triangles. A square with a moved corner gets one diagonal, the one that gives the better triangles. Small squares appear only near points that are close together, so the mesh is fine where it must be and coarse elsewhere.

## The problem

The input is a set $X$ of $n \ge 2$ distinct points in the plane. The output is a triangulation of a square $R$ that contains $X$, in which every point of $X$ is a vertex. The quality measure of the paper is the aspect ratio $A(abc)$ of a triangle: its longest side divided by the altitude onto that side. It is the measure of [mesh quality](/mesh-quality-measures/) that the size proofs use, and it controls the smallest angle $\theta$ through
$$\frac{1}{\sin \theta} \le A(abc) \le \frac{2}{\sin\theta}.$$
The goal has two parts. Every triangle must have $A \le 4$. The number of triangles must be at most a constant times the size of any triangulation of $X$ with the same aspect ratio bound. This page builds triangles in the root square only, so the points must be the only constraints. Polygons and segments need the variant of Section 5 of the paper.

The page makes two kinds of claim, and the reader must keep them apart.

- *Proved bound.* Every triangle has $A \le 4$, so every angle is at least $\arcsin(1/4) \approx 14.4775°$. This page proves it for its own templates (in `proofs/correctness.md`), following Lemma 1 of the paper.
- *Proved bound with an unknown constant.* The size is within a constant factor of the optimum (Theorem 1 and Corollary 1 of the paper). The paper proves that the constant exists but does not give its value. This page cites that result and does not prove it.

## The algorithm

A box of the tree is a square. Its *extended neighbors* are the boxes of the same size that share a side or a corner with it. A leaf $b$ of side $\ell$ is *crowded* if it holds at least one point and one of these holds:

- **C1.** $b$ holds two or more points.
- **C2.** $b$ holds one point $x$, and the nearest other point is closer than $2\sqrt2\,\ell$ to $x$.
- **C3.** A box of the same size near $b$ is split. The paper takes the 3 by 3 block of boxes around $b$ (the extended neighbors). This page takes the 5 by 5 block; the reason is below.

The tree is *balanced* if no side of a leaf has two or more box corners strictly inside it. Then two leaves that share part of a side differ in size by a factor of at most 2.

```pseudo id=main
QUADTREE-MESH(X)
L1  R ← the square of side 4L concentric with the bounding square of X (L = its side)
L2  T ← the quadtree whose only leaf is R
L3  repeat
L4      if some leaf b is crowded (C1, C2 or C3) then
L5          split b; split each extended neighbor of b, after first splitting coarser leaves so that it exists
L6      else if a leaf b that holds a point lacks an extended neighbor of its own size then
L7          split the coarser leaf that covers that neighbor
L8      else if a side of some leaf b has two or more box corners inside it then
L9          split b
L10     else stop
L11 for each x ∈ X: replace the corner of x's leaf nearest to x (ties: smallest x, then smallest y) by x
L12 for each leaf b:
L13     if no corner of b moved: add the center c of b and join c to every corner and side midpoint of b
L14     else: cut the moved quadrilateral by the diagonal whose two triangles have the smaller largest A
L15 return the triangles
```

The paper takes a root of twice the size of the bounding square and says that any root works if its side is a constant times the diameter of $X$ and its sides are far from the points. A root of side $4L$ keeps every point at distance $1.5L$ from the boundary, so every leaf that holds a point has all eight extended neighbors inside the root.

**Why the 5 by 5 block.** The paper states that only boxes with unsplit sides get a moved corner, so the diagonal template of L14 always applies. With the 3 by 3 block of C3, this is not always true. For the three points $(11, 19)$, $(12, 9)$ and $(19, 5)$, the point $(11, 19)$ moves the corner $(11.5, 19)$, and two of the four boxes at that corner have a split side, because the split comes from a box two places away. The test file checks this case. With the 5 by 5 block, every box that touches the moved corner has all its side neighbors inside the 5 by 5 block of the point's box, so none of them is split, and the diagonal template always applies. The size argument of the paper uses C3 only through a fixed neighborhood of each box, so a larger fixed block should change only its constant. This page does not redo that argument.

All tests are exact. Box corners are dyadic fractions of the root, and the only predicates are comparisons of squared distances and the sign of [ORIENT2D](/orientation-test/). The aspect ratio is a rational number, $A(abc) = \ell_{\max}^2 / (2\,\mathrm{area})$, so L14 compares fractions. With floating point, a point very close to a box side can be filed in the wrong box, and the tie in L11 can break two ways. Then two boxes can disagree about a moved corner and the mesh gets a hole. Exact arithmetic, as here, or a floating-point filter in the style of Shewchuk 1997 that falls back to exact arithmetic, removes the problem.

## Example

Take $X = \{(0,0), (4,0), (1,3)\}$. The bounding square has side $L = 4$, so the root has side 16 and its lower left corner is $(-6, -6.5)$. The squared nearest neighbor distances are 10 for $(0,0)$ and $(1,3)$ and 16 for $(4,0)$. Each round of the loop does all the splits of one rule. The numbers come from the implementation and the test file checks them.

| Round | Rule | Boxes | Width | Why |
|---|---|---|---|---|
| 1 | C1 | root | 16 | it holds all three points |
| 2 | C2 | 1, and its 3 extended neighbors | 8 | $10 < 8 \cdot 8^2 = 512$ |
| 3 | C2 | 3, with their neighbors | 4 | $10 < 128$ and $16 < 128$ |
| 4 | C2 | 3, with their neighbors | 2 | $10 < 32$ and $16 < 32$ |
| 5 | L6 | the box at $(0, 3.5)$ is made | 1 | the leaf of $(1,3)$ needs a neighbor there |
| 6 | L6 | the box at $(2, 3.5)$ is made | 1 | the same |
| 7 | balance | 3 boxes | 4 | each touches boxes of width 1 |

At width 1 the points stop: $10 \ge 8 \cdot 1^2$ and $16 \ge 8$, and no box in the 5 by 5 blocks is split. The tree has 109 leaves: 68 of width 1, 39 of width 2 and 2 of width 4. In L11, each point sits at the middle of the left side of its unit box, so two corners tie, and the rule picks the lower one: $(0, -0.5)$ moves to $(0, 0)$, $(4, -0.5)$ moves to $(4, 0)$, and $(1, 2.5)$ moves to $(1, 3)$.

| Triangles | Count | Aspect ratio $A$ | Smallest angle |
|---|---|---|---|
| unmoved boxes, center fan | 410 | 2 | 45° |
| moved boxes, diagonal away from the point | 6 | 2 | 45° |
| moved boxes, at the point | 6 | 5/4 | 53.13° |
| moved boxes, at the point | 6 | 3/2 | 45° |
| moved boxes, at the point | 6 | 5/2 | 26.57° |

The output has 232 vertices and 434 triangles, and the smallest angle is $\arctan(1/2) \approx 26.57°$, in the triangle $(0,0), (0, 0.5), (-1, 0.5)$. Most of the triangles are far from the points. The root of side $4L$ and the 5 by 5 block both add boxes; the paper notes that simple heuristics remove many of them afterwards without losing the bound.

## Correctness

The proof is in `proofs/correctness.md`. It has five parts.

1. *The loop stops.* Let $\delta$ be the smallest distance between two input points. The first box of the smallest size that is ever split was split by C1 or C2, because C3, L5, L6 and L9 all need an earlier split of a box of that size or smaller. C1 and C2 need side more than $\delta / (2\sqrt2)$. So all split boxes are at least that large, and there are finitely many of them.
2. *Balance and the neighbor property hold.* The loop stops only when L4, L6 and L8 find nothing. So the tree is balanced, every leaf with a point holds one point, has eight leaf neighbors of its size, and has no split box in its 5 by 5 block.
3. *The moves are consistent.* The moved corner $y$ of $x$ is within $\ell/\sqrt2$ of $x$. Two points cannot move the same corner, and no box gets two moved corners, because C2 keeps the other points at least $2\sqrt2\,\ell$ away. The tie rule removes the one equality case.
4. *Every triangle has $A \le 4$.* The center fan gives right isosceles triangles with $A = 2$. For a moved box, scale it to $[0,1]^2$ with the moved corner at the origin. The point lies in $[-\tfrac12, \tfrac12]^2$. If it lies in $[0, \tfrac12]^2$, the diagonal through the point gives $A \le 5/2$. Otherwise the other diagonal gives $A < 4$. L14 takes the better of the two.
5. *The triangles tile $R$.* All are counterclockwise, every inner edge is used once in each direction, and the other edges lie on the boundary of $R$. A covering count argument then shows that each point of $R$ lies in exactly one triangle.

Size optimality is not proved here. Theorem 1 of the paper shows $|QT(X)| \le c'' \cdot |T| \log A(T)$ for every triangulation $T$ that contains $X$, and Corollary 1 turns this into a constant factor of the optimum for any fixed aspect ratio bound $\alpha \ge 4$. Those results are for the 3 by 3 block of the paper; for the 5 by 5 block of this page they should hold with a larger constant, but this page does not prove it.

## Complexity

The paper's implementation runs in $O(n \log n + k)$ time, where $k$ is the output size, and this is optimal: sorting reduces to it, and the output must be written. Corollary 2 bounds the output: $k = O(n \log A(DT(X)))$, where $A(DT(X))$ is the worst aspect ratio in the Delaunay triangulation of $X$. The paper shows that this is tight: the points $(0, k\alpha)$ and $(1, k\alpha)$ for $k = 1, \dots, n/2$ need $\Omega(n \log A(DT(X)))$ triangles for any constant aspect ratio bound.

The implementation on this page is simpler and slower. Each round of the loop scans every leaf, and there are $O(k)$ rounds in the worst case, so it takes $O(k^2 (n + r^2))$ exact operations with $r = 2$ the reach of C3. That is enough for the small inputs of the tests. A fast version keeps a queue of leaves to check and finds neighbors by walking the tree.

## Properties

- **Exact.** Every decision is a comparison of rational numbers.
- **Deterministic.** Each round scans the leaves in a fixed order, and ties in L11 have a fixed rule.
- **Graded.** Box sizes follow the distance to the nearest other point, so the mesh is fine only where points are close.
- **Proved shape bound.** $A \le 4$ and angles of at least $14.48°$. The largest angle is below $180° - 2 \cdot 14.48°$, but the method does not try to bound it further.
- **Proved size bound with an unknown constant.** The constant $c''$ of Theorem 1 is not given as a number.

The proved constants are much worse than the measured ones. Over 60 random sets of 2 to 12 integer points in $[0, 40]^2$, the worst aspect ratio was $74/25 = 2.96$, against the proved 4, and the smallest angle was $22.29°$, against the proved $14.48°$. The largest angle was $104.0°$. The size constant is the larger gap: the proof gives no number, and in practice most of the triangles come from the root and the balance step, so a cleanup pass that merges boxes far from the points removes a large part of them.

## Variants and improvements

- **No obtuse angles.** Section 3 of the paper changes the templates near the points and gets a triangulation with no obtuse angle and aspect ratio at most 2, still within a constant of $|QT(X)|$ (Theorem 2). A non-obtuse triangulation is a [Delaunay triangulation](/delaunay-triangulation/) of its vertices. Theorem 3 drops the aspect ratio bound and gets $O(n)$ size.
- **Only acute angles.** Section 4 uses a strongly balanced quadtree and gets aspect ratio at most 5/3 with no obtuse angles (Theorem 4).
- **Segments and polygons.** Section 5 warps corners onto input segments. Lemma 7 gives $A \le 5$ and every new angle at least $18.4°$, which is $\arctan(1/3)$. Theorem 8 handles polygons whose interior angles are at least $\beta$, with angles at least $\min(18.4°, \beta)$.
- **Higher dimensions.** Section 6 uses a balanced $2^d$-tree and gets bounded aspect ratio with size $O(|T| \log A(T))$ (Theorem 9). In 3D this is the starting point of [octree mesh generation](/octree-mesh-generation/).
- **Delaunay refinement.** [Ruppert's algorithm](/ruppert-algorithm/) and [Chew's second algorithm](/chew-second-algorithm/) get better angle bounds (about $20.7°$ and $26.57°$) with fewer triangles in practice, at the cost of a less local construction.

## When to use it

Use it when a proof of both quality and size matters more than the triangle count, or when the mesh must line up with an axis aligned grid, for example to couple with a finite difference solver or an adaptive quadtree solver. Use [Delaunay refinement](/delaunay-refinement/) when you want fewer, better shaped triangles for the same input, and the [advancing front method](/advancing-front-mesh-generation/) when the boundary layer of the mesh must be smooth.

## Pitfalls

- **Rotation dependence.** The mesh depends on the axes. A rotated input gives a different mesh with a different size.
- **Many triangles away from the points.** The root and the balance step make a ring of boxes far from the data. Count the triangles before you compare with other methods.
- **Unsplit sides are not automatic.** With the 3 by 3 block of C3, a box with a moved corner can have a split side, and then the two-triangle template does not apply. This page uses a 5 by 5 block for that reason.
- **Ties.** A point at the center of its box, or on a midline, is equally close to two or four corners. Without a fixed tie rule, two neighboring boxes may choose different corners.
- **Floating point.** A point on a box side can be assigned to two boxes by rounding. Use exact or filtered predicates.
- **Aspect ratio is not the angle.** $A \le 4$ gives angles of at least $14.48°$, but a triangle with $A = 4$ may have its smallest angle far above that bound, since $A \le 2/\sin\theta$ also holds.

## Implementations

## History

Bern, Eppstein and Gilbert presented the method at FOCS 1990 and published the journal version in 1994. Earlier quadtree meshers, such as the one of Yerry and Shephard from 1983, were engineering methods with no guarantee. The paper gave the first proof that one method gets both bounded aspect ratio and a size within a constant factor of the optimum, and it ran in optimal time. Its warping idea, its balance condition and its size argument by charging boxes to triangles of an optimal mesh became standard tools. Mitchell and Vavasis carried the approach to three dimensions in 1992, and Ruppert's Delaunay refinement of 1993 to 1995 gave the same kind of size guarantee with better angles.

## References
