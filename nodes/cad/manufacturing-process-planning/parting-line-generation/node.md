---
tag: D4D190
kind: algorithm
slug: parting-line-generation
name: Parting line generation
aliases:
- parting curve computation
area: cad/manufacturing-process-planning
level: advanced
summary: Finds the curve on a part where the two mold halves meet, from the silhouette in the parting direction, chosen to be flat and to avoid undercuts.
model: real-ram
complexity:
  vars: {N: "total number of vertex places in all faces (twice the number of edges)"}
  time: {worst: "O(N)"}
  space: {extra: "O(N)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 2002
  people: [M. W. Fu, A. Y. C. Nee, J. Y. H. Fuh]
  note: Parting lines were found from the silhouette of the part in the parting direction in mold CAD systems of the 1990s. Fu, Nee and Fuh (2002) classify the faces by their visibility in the parting direction and choose among the edge loops by their projected area.
prereqs: [mold-parting-direction, silhouette-edge]
see_also: [silhouette-curve-of-a-surface, undercut-detection, draft-angle-analysis, accessibility-cone, convex-polytope, back-face-culling, doubly-connected-edge-list, manufacturability-analysis]
sources:
  - paper: doi:10.1016/S0010-4485(01)00117-8
    title: M. W. Fu, A. Y. C. Nee and J. Y. H. Fuh, The application of surface visibility and moldability to parting line generation, Computer-Aided Design 34(6), 2002, 469 to 480
    locator: the classification of the faces by their orientation to the parting direction, the edge loops between the classes, and the choice of a 3D parting line from the projected areas of the loops
  - paper: doi:10.1016/S0278-6125(97)88401-4
    title: Optimum parting line design of molded and cast parts for manufacturability, Journal of Manufacturing Systems 16(1), 1997
    locator: the choice of a parting line among candidates by manufacturing criteria (authors and pages not confirmed here)
  - paper: doi:10.1016/S0010-4485(01)00119-1
    title: Hee-Kap Ahn, Mark de Berg, Prosenjit Bose, Siu-Wing Cheng, Dan Halperin, Jiri Matousek and Otfried Schwarzkopf, Separating an object from its cast, Computer-Aided Design 34(8), 2002, 547 to 559
    locator: the two-piece cast model, in which the parting surface splits the part into the faces seen from +d and from -d, and the test of one direction
---

Parting line generation finds, for a part and a chosen parting direction $d$, the closed curves on the part where the two halves of a mold meet. One half of the mold moves along $+d$ and the other along $-d$. Each face of the part must be formed by the half that it faces, so the faces split into *upper* faces, with $n \cdot d > 0$, and *lower* faces, with $n \cdot d < 0$, and the parting line runs along the edges between the two sets. For a polyhedral part these are the [silhouette edges](/silhouette-edge/) for the direction $d$. The algorithm on this page computes the face signs exactly, finds the edges between an upper and a lower face, and chains them into oriented loops in $O(N)$ time. On a convex polyhedron in general position the result is one simple closed cycle, and the page proves this. On other parts there can be several loops, and the planner must choose among them or change the part. This page differs from [mold parting direction](/mold-parting-direction/), which chooses $d$, and from [undercut detection](/undercut-detection/), which finds the faces that neither half can release.

## In plain words

A plastic or cast part is made in a mold with two halves that come apart. Each surface of the part must be formed by the half on its side, so that the half can pull away. Surfaces that face up go to the upper half, and surfaces that face down go to the lower half. The line where the two kinds of surfaces meet is where the halves touch. That is the parting line.

The algorithm looks at each face once to see which way it faces. Then it walks around the region of upward faces and records its border, one loop at a time. On a simple convex part there is exactly one loop. On a part with holes or pockets there can be more, and the designer must choose.

## The problem

**Input.** A closed, oriented polyhedral surface (a [manifold mesh](/manifold-mesh/)): vertices with integer coordinates and faces as lists of vertex indices, counterclockwise seen from outside, each edge in exactly two faces. A parting direction $d \ne 0$ with integer coordinates. A rule `zero_side` that puts each face with $n \cdot d = 0$ on the lower side (the default) or the upper side.

**Output.** The boundary of the union $U$ of the upper faces, as a list of closed loops of vertices. Each loop is oriented with the upper faces on its left, seen from outside, and each edge between an upper and a lower face is in exactly one loop.

**Faces with $n \cdot d = 0$.** A vertical face has zero draft and can go to either half. The rule `zero_side` makes the choice explicit. With the default, the loops run along the top edges of vertical walls. With the other choice, they run along the bottom edges. A real design gives such faces a draft first (see [draft angle analysis](/draft-angle-analysis/)).

## The algorithm

The algorithm uses the half-edges of the mesh, as in a [doubly connected edge list](/doubly-connected-edge-list/). The *twin* of the half-edge $(u, v)$ is $(v, u)$, which lies in the other face of the edge. For a half-edge $h$ of a face $f$, $\mathrm{succ}(h)$ is the next half-edge of $f$.

```pseudo id=main
PARTING-LOOPS(V, F, d, zero_side)
L1  for each face f: n_f ← Newell normal of f; s_f ← sign(n_f · d), or zero_side if n_f · d = 0
L2  for each half-edge h = (u, v) of each face f: face[h] ← f; succ[h] ← the half-edge after h in f
L3  B ← the half-edges h = (u, v) of upper faces whose twin (v, u) lies in a lower face
L4  for each h ∈ B: g ← succ[h]
L5      while the twin of g lies in an upper face: g ← succ[twin of g]
L6      next[h] ← g
L7  for each h ∈ B not yet used: follow next from h until it returns, mark the half-edges used, and record their start vertices as one loop
L8  return the loops
```

**Line L1.** The Newell normal of a face with vertices $p_0, \dots, p_{k-1}$ has the components $\sum_i (y_i - y_{i+1})(z_i + z_{i+1})$ and the two cyclic shifts of it. For a planar face it is the outward normal times twice the area. On integer input it is an integer vector, so the sign of $n_f \cdot d$ is exact. A normal from the first three vertices fails on a face whose first three vertices are collinear, and a floating point normal can give the wrong sign on a face that is almost vertical.

**Lines L4 to L6.** Let $h = (u, v)$ be a boundary half-edge in the upper face $f$. The next boundary half-edge starts at $v$. Line L4 takes the half-edge of $f$ that leaves $v$. If its twin is in an upper face $f'$, the boundary does not go that way, and line L5 crosses into $f'$ and takes the half-edge of $f'$ that leaves $v$. This turns around $v$ through the upper faces, until it reaches a half-edge whose other side is lower. At a vertex where the upper region touches itself, with two boundary arcs through one vertex, the turn takes the first exit in the order around $v$, so the loops never cross.

## Example

The square pyramid with base $[-1, 1]^2$ at $z = 0$ and apex $(0, 0, 2)$, and $d = (1, 0, 1)$. The vertices are $0 = (-1, -1, 0)$, $1 = (1, -1, 0)$, $2 = (1, 1, 0)$, $3 = (-1, 1, 0)$ and $4 = (0, 0, 2)$.

| face | vertices | Newell normal | $n \cdot d$ | side |
|---|---|---|---|---|
| base | 0, 3, 2, 1 | $(0, 0, -8)$ | $-8$ | lower |
| $-y$ | 0, 1, 4 | $(0, -4, 2)$ | $2$ | upper |
| $+x$ | 1, 2, 4 | $(4, 0, 2)$ | $6$ | upper |
| $+y$ | 2, 3, 4 | $(0, 4, 2)$ | $2$ | upper |
| $-x$ | 3, 0, 4 | $(-4, 0, 2)$ | $-2$ | lower |

Line L3 finds the half-edges $(0, 1)$, $(4, 0)$ in face $-y$, $(1, 2)$ in face $+x$, and $(2, 3)$, $(3, 4)$ in face $+y$. Lines L4 to L6:

| $h$ | first $g$ (L4) | turns at L5 | $\mathrm{next}[h]$ |
|---|---|---|---|
| $(0, 1)$ | $(1, 4)$, twin in $+x$ | $(1, 2)$, twin in base | $(1, 2)$ |
| $(1, 2)$ | $(2, 4)$, twin in $+y$ | $(2, 3)$, twin in base | $(2, 3)$ |
| $(2, 3)$ | $(3, 4)$, twin in $-x$ | none | $(3, 4)$ |
| $(3, 4)$ | $(4, 2)$, twin in $+x$ | $(4, 1)$, twin in $-y$; then $(4, 0)$, twin in $-x$ | $(4, 0)$ |
| $(4, 0)$ | $(0, 1)$, twin in base | none | $(0, 1)$ |

Line L7 gives one loop $0, 1, 2, 3, 4$: three edges of the base and two slanted edges to the apex. The loop is not planar, so the mold needs a stepped parting surface. Its projection along $d$ is the boundary of the projection of the pyramid, as the theorem below says. The tests check this example, a box with vertical walls under both `zero_side` rules, and random cases.

## Correctness

**Theorem 1.** PARTING-LOOPS returns loops in which every edge between an upper and a lower face occurs exactly once, oriented with the upper face on its left, and every loop is closed.

The sign at line L1 is exact. Line L3 keeps exactly one half-edge of each edge between an upper and a lower face: the half-edge in the upper face. The turn at lines L4 to L6 ends, because the edge $\{u, v\}$ of $h$ has a lower face on its other side, so the turn around $v$ meets a lower face before it can come back to $f$. The map $\mathrm{next}$ is a bijection of $B$: the turn the other way around $u$ undoes it. So $\mathrm{next}$ is a permutation of the finite set $B$, its cycles are closed, and line L7 records each cycle once.

**Theorem 2.** Let $P$ be a convex polyhedron and $d$ a direction with $n_f \cdot d \ne 0$ for every face. Then the silhouette edges form one simple closed cycle, and PARTING-LOOPS returns exactly one loop, with no repeated vertex.

The proof projects along $d$. The projection maps the union $U$ of the upper faces one to one onto the projected polygon $Q$, because each line parallel to $d$ leaves $P$ through an upper face and meets no other upper face. Each silhouette edge lies in a [supporting plane](/supporting-hyperplane/) of $P$ that is parallel to $d$, so it projects into the boundary of $Q$. A point of $U$ off the silhouette has only upper faces around it, so no supporting plane parallel to $d$ passes through it, and it projects into the interior of $Q$. So the projection maps the silhouette onto the boundary of the convex polygon $Q$, a simple closed curve, without folds. The [silhouette edge](/silhouette-edge/) page proves the weaker fact that the edges form closed loops on any closed mesh. The full proofs are below.

## Complexity

Let $N$ be the sum of the face sizes, which is $2E$ for $E$ edges. Line L1 costs $O(N)$, line L2 builds two hash maps of $N$ entries, and line L3 is one pass. In lines L4 to L6, the turns around a vertex $v$ that start from different boundary half-edges cover disjoint runs of upper faces around $v$, so the total number of steps at line L5 is at most the sum of the vertex degrees, $O(N)$. Line L7 visits each half-edge of $B$ once. So the time is $O(N)$ expected with hashing, or $O(N)$ worst case with a mesh structure that stores the twins. The extra space is $O(N)$. On integer input with coordinates of $b$ bits, the Newell normal has $O(b)$ bits more, so each operation is constant time on the real RAM.

## Properties

- **Exact.** The face signs come from integer arithmetic, so a face that is almost vertical gets the right side.
- **Local.** The side of a face depends only on its normal, not on the rest of the part. So the loops are candidates, not a check that the halves can come apart: a face can face up and still be blocked by another part of the part. That is an undercut.
- **Deterministic.** The loops come out in the order of their first boundary half-edge in the face list.
- **One loop for convex parts.** By Theorem 2. For a non-convex part the number of loops is not fixed: a part with a through hole along $d$ has at least two.

## Variants and improvements

- **Smooth surfaces.** On a NURBS or other smooth part, the parting line is the [silhouette curve](/silhouette-curve-of-a-surface/) where $n \cdot d = 0$, traced as a curve on each face. This page covers polyhedra and tessellated parts.
- **Choosing among loops.** Fu, Nee and Fuh classify the faces by their visibility and moldability for the parting direction, and among the edge loops they choose the one with the largest projected area on the plane normal to $d$ as the main parting line. The other loops are inner parting lines, for example around a through hole, where a core closes the hole.
- **Flat parting lines.** A planar parting line makes a cheap mold. When a loop runs along vertical faces, the zero-draft faces can move to the other side, which moves the loop down the wall, and the planner chooses the position that makes the loop flat or stepped least often.
- **Parting surface.** The mold also needs a parting surface, which extends the parting line outward to the edge of the mold block. A flat loop gives a flat surface. A loop like the one in the example needs a ruled or stepped surface.
- **Choice of the direction.** The direction $d$ comes first, from [mold parting direction](/mold-parting-direction/). Ahn and coauthors test one direction for a two-piece cast and find all valid directions of a polyhedron. The algorithm on this page then gives the line for the chosen direction.
- **Undercuts.** If a face is blocked from both $+d$ and $-d$, no choice of loop helps. [Undercut detection](/undercut-detection/) finds such faces, and the mold needs side cores.

## When to use it

Use it after the parting direction is fixed, on a tessellated part or a polyhedral model, to get the candidate parting lines in linear time. Use exact integer or rational coordinates, or snap the input to a grid, so that faces close to vertical get a reliable side. Do not use the loops as a proof that the mold works. Check undercuts and draft separately.

## Pitfalls

- **Vertical faces.** A face with $n \cdot d = 0$ must go to one side by a fixed rule. A test with a tolerance puts some vertical faces up and some down at random, and the loops then zigzag over the walls.
- **Pinched loops.** At a vertex where the upper region touches itself, two boundary arcs meet. A chaining rule that takes any boundary edge at $v$ can join the arcs into a loop that crosses itself. Lines L4 to L6 turn around $v$ in the order of the faces, which gives non-crossing loops. In the random terrain tests of the implementation, several loops repeat a vertex for this reason.
- **Open or bad meshes.** An edge with one face, or two faces that use the same half-edge, breaks the twin map. The implementation raises an error instead of returning wrong loops.
- **Orientation.** If the faces are clockwise from outside, all normals flip, and the upper and lower sides swap. A test of the signed volume finds this.

## Implementations

## History

The two-piece mold model, with the faces of a part split by their direction relative to the parting direction, is the base of the geometric work on casting by Bose, Bremner and van Kreveld (1997) and by Ahn and coauthors, first at SoCG 1997 and in Computer-Aided Design in 2002. In mold CAD, parting lines were derived from the silhouette in the parting direction. Weinstein and Manoochehri (1997) chose among parting lines by manufacturing criteria. Fu, Nee and Fuh (2002) classified the faces by visibility and moldability and chose the 3D parting line among the edge loops by their projected area.

## References
