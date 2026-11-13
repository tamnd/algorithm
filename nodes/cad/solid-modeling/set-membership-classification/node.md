---
tag: E1CR69
kind: algorithm
slug: set-membership-classification
name: Set membership classification
aliases:
- point membership classification
- Tilove classification
area: cad/solid-modeling
level: core
summary: Classifies a point, a curve or a surface against a CSG solid as in, on or out by classifying it at the leaves and combining the results up the tree.
model: real-ram
complexity:
  vars: {L: the number of primitives in the tree, m: the number of edges of all primitives}
  time: {worst: O(m + L^2)}
  space: {extra: O(L)}
properties: {online: false, deterministic: true, recursive: true}
history:
  year: 1980
  people: [Robert B. Tilove]
  note: Tilove defined set membership classification as one operation for many intersection problems of the PADL solid modeler at the University of Rochester.
prereqs: [constructive-solid-geometry, regularized-set-operations, r-set, orientation-test]
see_also: [boundary-evaluation, csg-ray-casting, vertex-neighborhood-classification, point-in-polygon, generalized-winding-number, solid-boolean-operations]
sources:
  - paper: doi:10.1109/TC.1980.1675470
    title: Robert B. Tilove, Set membership classification, a unified approach to geometric intersection problems, IEEE Transactions on Computers C-29(10), 874 to 883, 1980
    locator: the whole paper (the definition of the classification, the combine rules for the regularized operations, and the neighborhoods for the on parts)
  - paper: doi:10.1109/PROC.1985.13108
    title: Aristides A. G. Requicha and Herbert B. Voelcker, Boolean operations in solid modeling, boundary evaluation and merging algorithms, Proceedings of the IEEE 73(1), 30 to 44, 1985
    locator: the sections on set membership classification and on neighborhoods
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the sections on CSG and on the algorithms that use it
---

Set membership classification splits a candidate set $S$, such as a point, a segment or a face, into the part inside a solid $X$, the part on its boundary and the part outside. For a solid given by a [CSG tree](/constructive-solid-geometry/), it classifies $S$ against each primitive and then combines the results up the tree with the rules of the [regularized set operations](/regularized-set-operations/). Where $S$ lies on the boundary of two primitives, the three classes are not enough, and the algorithm combines *neighborhoods* instead. Tilove defined it in 1980, and it is the basic query of CSG modelers: [boundary evaluation](/boundary-evaluation/), [ray casting](/csg-ray-casting/) and interference tests all reduce to it.

## In plain words

A CSG solid is a recipe: take this box, add that cylinder, cut out this hole. To test a point, you ask each basic shape first. Then you go up the recipe: a point inside one of two added shapes is inside their sum, a point inside the cut is outside, and so on.

The hard case is a point on the skin of two shapes. Two boxes side by side share a wall. A point on that wall is on the skin of each box, but it is inside the joined solid. So "on the skin" is not enough information. The method keeps, for each such point, a small picture of which directions around it lead into the shape. To join two shapes it joins their pictures. The point is inside if every direction leads in, outside if none does, and on the skin otherwise.

## The problem

Let $X \subseteq E^3$ be an [r-set](/r-set/) and $S$ a candidate set. The classification of $S$ against $X$ is the triple

$$S \operatorname{in} X = S \cap \operatorname{int} X, \qquad S \operatorname{on} X = S \cap \partial X, \qquad S \operatorname{out} X = S \setminus X.$$

The three parts are disjoint and their union is $S$. Tilove regularizes each part in the topology of $S$, so that a segment is split into segments and isolated points are dropped. For a single point $p$ the answer is one of IN, ON and OUT. This is point membership classification. In this page $X$ is given by a CSG tree whose leaves are primitives and whose inner nodes are $\cup^*$, $\cap^*$ and $-^*$.

The classes of $S$ against $A$ and $B$ almost determine the class against $A \cup^* B$: IN against either child gives IN, and OUT against both gives OUT. The rule fails when $S$ is ON against both. Two squares that share an edge have a union in which the shared edge is IN. Two squares that overlap have a union in which the common part of their boundaries is ON. Intersection and difference have the same gap. The fix is the neighborhood.

**Neighborhood.** In the plane, the *neighborhood* of $p$ in $X$ is the set of directions $d$ with $p + \varepsilon d \in \operatorname{int} X$ for all small $\varepsilon > 0$. Near $p$ the boundary lines of the primitives through $p$ cut the disk into open sectors, so the neighborhood is a union of open sectors. It is stored as the list of breakpoint directions, sorted by angle, and one label per sector: in or out. For a point inside a polygon edge the neighborhood is a half-disk, and at a vertex it is a wedge. In space the neighborhood is a set of regions on a small sphere: a half-ball on a face, a wedge on an edge and a cone at a vertex.

## The algorithm

```pseudo id=main
CLASSIFY(p, T)                          ▷ the neighborhood of p in the solid of T
L1  if T is a primitive then
L2      return LEAF-NEIGHBORHOOD(p, T)
L3  N1 ← CLASSIFY(p, T.left), N2 ← CLASSIFY(p, T.right)
L4  return COMBINE(N1, N2, T.op)

COMBINE(N1, N2, op)
L5  D ← the breakpoints of N1 and N2, sorted by angle, one per direction
L6  for each sector σ between consecutive directions of D do
L7      d ← a direction strictly inside σ
L8      label(σ) ← op(d ∈ N1, d ∈ N2)
L9  remove each breakpoint with equal labels on both sides, return (D, labels)

PMC(p, T)                               ▷ point membership classification
L10 N ← CLASSIFY(p, T)
L11 if every sector of N is in then return IN
L12 if no sector of N is in then return OUT
L13 return ON
```

LEAF-NEIGHBORHOOD for a convex polygon evaluates the sign of each edge line at $p$ with the [orientation test](/orientation-test/). If one sign is negative, $p$ is outside and the neighborhood is empty. If all are positive, it is the full disk. Otherwise the edges with sign $0$ pass through $p$: their directions $\pm e$ are the breakpoints, and a sector is in when its sample direction is on the inner side of each such edge. A convex polygon has at most two edges through $p$, so a leaf has at most four breakpoints.

Line L7 picks the sample for the sector from $u$ counterclockwise to $v$. It is $u + v$ when the sector is less than a half turn, $u$ turned by a quarter turn when it is exactly a half turn, and $-(u + v)$ when it is more. With rational breakpoints the sample is rational, so every test is exact.

**Segments and faces.** To classify a segment, split it at its crossings with the edge lines of all primitives. On each open piece, every primitive gives the same neighborhood at every point, so one point of the piece classifies it, and so does each split point. Tilove merges the sorted piece lists of the two children at each node instead, which gives the same parts. In space the same scheme splits a face along its intersection curves with the other faces.

## Example

Let $Q_1 = [0, 2] \times [0, 2]$, $Q_2 = [2, 4] \times [0, 2]$ and the triangle $R$ with vertices $(1, 1)$, $(3, 1)$ and $(2, 3)$. The solid is $X = (Q_1 \cup^* Q_2) -^* R$. Classify $p = (2, 1)$. It lies on the shared edge of the squares and on the bottom edge of the triangle.

| node | breakpoints | in sectors | class of $p$ |
|---|---|---|---|
| $Q_1$ | up, down | the left half | ON |
| $Q_2$ | up, down | the right half | ON |
| $Q_1 \cup^* Q_2$ | none | the whole disk | IN |
| $R$ | right, left | the upper half | ON |
| $X$ | right, left | the lower half | ON |

At the union node, line L5 gives the two breakpoints up and down, line L8 labels both half-disks in, and line L9 removes both breakpoints. So the shared edge vanishes, and the union is IN at $p$ even though both children say ON. The difference keeps the lower half-disk, so $p$ is on the boundary of $X$, where the bottom of the triangle cuts into the rectangle.

Other points: $(2, 1/2)$ is IN (the shared edge below the triangle is not boundary), $(2, 2)$ is OUT (it is inside $R$), $(1, 1)$ is ON (a corner of the notch), and $(2, 3)$ is OUT.

Now classify the segment from $(2, -1)$ to $(2, 3)$, which runs up the shared edge, with parameter $t \in [0, 1]$. It is OUT for $t < 1/4$, ON at $t = 1/4$ (the point $(2, 0)$), IN for $1/4 < t < 1/2$, ON at $t = 1/2$ (the point $(2, 1)$), and OUT for $t > 1/2$, where it is inside the triangle or above the rectangle. A classifier with only three classes at the leaves would report the part from $(2, 0)$ to $(2, 1)$ as ON, because it is on the boundary of both squares.

## Correctness

Fix $p$ and let $\Lambda$ be the finite set of edge lines of all primitives that pass through $p$. For a small enough $\varepsilon$, the disk of radius $\varepsilon$ around $p$ meets no other edge line, so each open sector of the disk cut by $\Lambda$ lies wholly inside or wholly outside each primitive. On such a sector the regularized result equals the plain set formula of the tree (fact 7 of [regularized set operations](/regularized-set-operations/)). COMBINE evaluates that formula at one direction of each sector, so by induction on the tree CLASSIFY returns the exact neighborhood. A closed regular set is the closure of its interior, so $p$ is in its interior exactly when all sectors are in, and outside it exactly when none is. The [full proof](proofs/correctness.md) gives the details.

## Complexity

The costs are in the [real RAM](/real-ram/) with exact predicates. Let the tree have $L$ primitives with $m$ edges in all.

- **Leaves.** LEAF-NEIGHBORHOOD costs $O(k)$ for a polygon of $k$ edges, so $O(m)$ for all leaves.
- **Inner nodes.** A node has at most as many breakpoints as its leaves together, so at most $4L$. With a linear merge of the two sorted lists in line L5 and a joint scan in line L8, each of the $L - 1$ inner nodes costs $O(L)$. The total is $O(m + L^2)$ for a point.
- **Easy points.** If $p$ lies on no edge line, every neighborhood is the full or the empty disk, and the cost is $O(m)$.
- **Segments.** A segment has $O(m)$ split points. Merging the sorted piece lists up the tree costs $O(L m)$ after the leaves, plus $O(m \log m)$ to sort the crossings.

Real modelers prune the tree with a bounding box per subtree: a point outside the box of a subtree is OUT for that subtree with no further work.

## Properties

- **Exact under exact predicates.** All branches use the signs of $2 \times 2$ determinants of rational data, so with exact arithmetic the class is right for every input, including points at vertices and on shared edges.
- **Regularized by construction.** The class depends only on the interiors of the primitives near $p$, so it is the class against the regularized result and never against a dangling edge.
- **General primitives.** Any primitive with a neighborhood oracle works. Non-convex polygons, disks and, in space, half-spaces and quadrics fit the same scheme.

## Variants and improvements

- **Point membership for a B-rep.** For a solid given by its boundary, there is no tree. Cast a ray and count crossings ([point in polygon](/point-in-polygon/) in the plane), or use the [generalized winding number](/generalized-winding-number/) for a surface with gaps.
- **Neighborhoods in space.** Requicha and Voelcker (1985) describe the neighborhoods of points on faces, edges and vertices that the boundary evaluation of PADL-2 used. [Vertex neighborhood classification](/vertex-neighborhood-classification/) uses the same idea on B-reps.
- **Rays.** Classifying a ray is the one-dimensional case, where the neighborhoods are intervals. That is [CSG ray casting](/csg-ray-casting/).
- **Interference.** Two solids interfere when $A \cap^* B$ is not empty. A modeler tests this by classifying faces of one solid against the other, and it needs the neighborhoods for solids that only touch, where the regularized intersection is empty.

## When to use it

Use it in a CSG modeler for every query that needs the solid itself: point tests, rendering by rays, boundary evaluation, interference and mass properties by sampling. Use the three-class rules alone when the inputs are in [general position](/general-position/), and keep neighborhoods for the case where a candidate lies on two boundaries at once. For a solid stored only as a B-rep, use a ray or winding number test instead.

## Pitfalls

- **Classes in place of neighborhoods.** If line L2 returns only IN, ON or OUT, a node must guess the result of ON against ON. For two squares that share an edge it then reports the shared edge as ON, and boundary evaluation keeps a face inside the solid. Line L2 must return the sectors, and line L8 must combine sectors.
- **The sample of a wide sector.** If line L7 always takes $u + v$, then for a sector of more than a half turn the sample lies in the opposite sector, and the labels are swapped. Use $-(u + v)$ there, and a quarter turn of $u$ for an exact half turn.
- **Duplicate directions.** Line L5 must merge breakpoints that point the same way, such as $(1, 0)$ and $(2, 0)$. If both stay, the sector between them is empty, and line L7 returns a sample from the wrong side.
- **Rounded predicates.** In floating point, a point computed as an intersection is a little off the edge line, so LEAF-NEIGHBORHOOD misses a tight edge and returns the full or the empty disk. The class is then IN or OUT where it should be ON. See the [geometric robustness problem](/geometric-robustness-problem/). Use exact or filtered predicates, as in [exact geometric computation](/exact-geometric-computation/).

## Implementations

## History

Tilove gave the definition and the combine rules in 1980, as part of the work on the PADL modelers in the Production Automation Project at the University of Rochester. Requicha surveyed the CSG representation and its algorithms in the same year. Requicha and Voelcker (1985) described how classification with neighborhoods drives boundary evaluation and the merging of boundaries.

## References
