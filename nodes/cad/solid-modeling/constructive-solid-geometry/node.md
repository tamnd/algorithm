---
tag: QD8QB3
kind: data-structure
slug: constructive-solid-geometry
name: Constructive solid geometry
aliases:
- CSG
- CSG tree
area: cad/solid-modeling
level: intro
summary: Represents a solid as a tree whose leaves are primitive solids and whose inner nodes are regularized union, intersection, difference and rigid motions.
model: word-ram
complexity:
  vars:
    n: the number of nodes of the tree
  time:
    worst: O(n)
  space:
    extra: Θ(n)
prereqs: [regularized-set-operations, r-set]
see_also: [set-membership-classification, csg-ray-casting, boundary-evaluation, boundary-representation, spatial-occupancy-enumeration, function-representation, brep-to-csg-conversion, solid-boolean-operations]
sources:
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the sections on representation schemes, their validity, unambiguity and uniqueness, and on CSG
  - paper: doi:10.1109/TC.1980.1675470
    title: Robert B. Tilove, Set membership classification, a unified approach to geometric intersection problems, IEEE Transactions on Computers C-29(10), 874 to 883, 1980
    locator: the classification of points and of other candidate sets against a CSG tree, and the neighbourhoods that the regularized operations need
  - paper: "Aristides A. G. Requicha and Robert B. Tilove, Mathematical foundations of constructive solid geometry, general topology of closed regular sets, Production Automation Project Technical Memorandum 27, University of Rochester, 1978"
    locator: the closed regular sets, the regularized operations and their Boolean algebra
  - book: isbn:9780881751086
    title: Martti Mäntylä, An Introduction to Solid Modeling, Computer Science Press, 1988
    locator: the chapter on constructive models, CSG trees and the algorithms on them
  - paper: doi:10.1109/PROC.1985.13108
    title: Aristides A. G. Requicha and Herbert B. Voelcker, Boolean operations in solid modeling, boundary evaluation and merging algorithms, Proceedings of the IEEE 73(1), 30 to 44, 1985
    locator: the sections on set membership classification and on neighbourhoods
---

Constructive solid geometry (CSG) describes a solid as a formula. The leaves of a tree are primitive solids, such as blocks, cylinders and spheres, and each inner node is a [regularized](/regularized-set-operations/) union, intersection or difference of its two children, or a rigid motion of its one child. A block with a pocket is the tree $A -^* S$: the block $A$ minus the box $S$ of the pocket. The tree is short and easy to edit, and it keeps the design history. But it does not list faces or edges: to answer a question about the solid, an algorithm must evaluate the tree. This page builds CSG trees of axis-aligned boxes with integer corners, and classifies a point as inside, on the boundary of or outside the regularized solid, with exact arithmetic.

## In plain words

Think of a workshop. You start from simple blocks, glue blocks together, cut one block out of another, and turn or move a block. A CSG tree writes down these steps as a recipe, not the shape that comes out.

To ask if a point is in the solid, put the question to each block in the recipe, and combine the answers with the same steps. For a point inside the material or out in the air, this is enough. For a point exactly on a surface, the plain answers can be wrong: a cut can remove the floor of a pocket from the solid, though the floor is part of the surface. The fix is to ask about the space very close to the point, in all directions, and to combine those answers.

## The abstract type

A CSG tree is built from these constructors:

- $\mathrm{BOX}(lo, hi)$: the closed box $[lo_x, hi_x] \times [lo_y, hi_y] \times [lo_z, hi_z]$, with $lo < hi$ on each axis.
- $A \cup^* B$, $A \cap^* B$ and $A -^* B$: the regularized operations of the two subtrees.
- $\mathrm{MOVE}(R, t, A)$: the set $\{R x + t : x \in A\}$, a rotation $R$ followed by a translation $t$.

The main query is $\mathrm{CLASSIFY}(T, p)$, which returns IN if $p$ is inside the solid of $T$, ON if it is on its boundary, and OUT if not. Other queries, such as ray casting for pictures and the volume, are built on classification, and the [set membership classification](/set-membership-classification/) page gives the general form for lines and surfaces.

The solid of a tree is the regularized value of its formula. By fact 7 of the [regularized set operations](/regularized-set-operations/) page, it does not matter whether each node regularizes or only the root does: $r(\Phi) = \Phi^*$. A CSG tree of [r-sets](/r-set/) is *valid* by construction, since the r-sets are closed under the regularized operations, and it is *unambiguous*, since a tree has one value. It is not *unique*: $A \cup^* B$, $B \cup^* A$ and $(A -^* B) \cup^* B$ are different trees for the same solid. To decide whether two trees give the same solid, a program must evaluate them, for example to B-reps, and compare the results.

## Representation

A tree node is one of:

| node | fields |
|---|---|
| box | $lo$, $hi$: integer corners |
| operation | the kind (union, intersection or difference) and the two children |
| motion | a rotation $R$ by quarter turns, an integer translation $t$, and the child |

Here the rotations are the 24 rotations of the cube, the signed permutation matrices with determinant 1. With these, every face of every primitive stays on an axis plane $x_j = c$ with an integer $c$. A tree can also be a directed acyclic graph, where one subtree is used several times; the queries below work the same way on it.

## Operations

The idea is to classify the 8 open octants at $p$ instead of $p$ itself. For $s \in \{-1, +1\}^3$, let the octant $O_s$ be the set of points $p + \varepsilon s'$ for small $\varepsilon > 0$ and $s'$ with the signs of $s$. All faces are on axis planes, so for small $\varepsilon$ each octant lies inside or outside each primitive as a whole. MASK($T$, $p$) is the set of octants that lie inside the ordinary (not regularized) value of $T$.

```pseudo id=main
MASK(T, p)                              ▷ the octants s ∈ {−1, +1}³ near p that are inside T
L1  if T = BOX(lo, hi): return {s : for each axis j, lo_j < p_j < hi_j, or p_j = lo_j and s_j = +1, or p_j = hi_j and s_j = −1}
L2  if T = MOVE(R, t, A): return {s : Rᵀ s ∈ MASK(A, Rᵀ(p − t))}
L3  a ← MASK(left(T), p); b ← MASK(right(T), p)
L4  if T is a union: return a ∪ b
L5  if T is an intersection: return a ∩ b
L6  return a \ b                        ▷ difference

CLASSIFY(T, p)
L7  m ← MASK(T, p)
L8  if m = ∅ then return OUT
L9  if m has all 8 octants then return IN
L10 return ON
```

A mask is an 8-bit word, so lines L4 to L6 are one OR, AND or AND NOT. Line L2 moves the point and the 8 directions back into the frame of the child, and $R^{-1} = R^T$ for a rotation. All values are integers or fractions, so all tests are exact.

**Why the octants are enough.** At a point $p$, the axis planes through $p$ cut a small ball around $p$ into 8 open octants and some pieces of planes. Each octant is wholly inside or wholly outside each primitive, so the ordinary formula gives one answer for each whole octant, and this answer is the regularized one, because the octants are open. The interior of the solid near $p$ is the union of the inside octants and the plane pieces between them, so $p$ is in the closure of the interior exactly when at least one octant is inside. If all 8 are inside, the whole ball is inside, and $p$ is an interior point.

**Points in general position.** If $p$ is on no face plane, then $p$ and all its octants are on the same side of each primitive, so the mask is all or nothing, and CLASSIFY is the ordinary formula at $p$. This is the cheap test that many programs use. It is right almost everywhere, and wrong exactly where it matters for a boundary model.

For general primitives, such as cylinders and tilted planes, the octants are not enough, because a face can pass between two octants. Then a classifier keeps a *neighbourhood* of $p$, the set of directions at $p$ that point into the solid, and combines neighbourhoods with the same Boolean operations. Tilove gives this method, and the [set membership classification](/set-membership-classification/) page describes it.

## Example

Take the block $A = [0, 4] \times [0, 4] \times [0, 2]$ and the pocket $S = [1, 3] \times [1, 3] \times [1, 3]$, and let $T = A -^* S$, a block with a square pocket of depth 1 in its top. The table gives the number of inside octants of each node, the size of its mask, and the result:

| point | where | octants in $A$ | octants in $S$ | octants in $T$ | CLASSIFY | ordinary formula |
|---|---|---|---|---|---|---|
| $(2, 2, \tfrac12)$ | under the pocket | 8 | 0 | 8 | IN | in |
| $(2, 2, 1)$ | the floor of the pocket | 8 | 4 | 4 | ON | not in |
| $(2, 2, \tfrac32)$ | in the pocket | 8 | 8 | 0 | OUT | not in |
| $(1, 1, 1)$ | a lower corner of the pocket | 8 | 1 | 7 | ON | not in |
| $(1, 2, 2)$ | the rim of the pocket | 4 | 4 | 2 | ON | not in |
| $(0, 0, 0)$ | a corner of the block | 1 | 0 | 1 | ON | in |

At $(2, 2, 1)$, the point is on the closed box $S$, so the ordinary difference removes it. But the floor of the pocket is part of the surface of the solid, and the 4 octants below it are inside. At $(1, 2, 2)$ on the rim, only the 2 octants with $s_x = -1$ and $s_z = -1$ are inside: the edge of the rim is convex. At $(1, 1, 1)$, 7 of the 8 octants are inside, which is a concave corner.

## Correctness

MASK($T$, $p$) is the set of octants at $p$ that lie inside the ordinary value of $T$. For a box this follows from line L1, axis by axis. For an operation it follows because an octant lies in $A \cup B$, $A \cap B$ or $A \setminus B$ exactly when it lies in $A$ or $B$, in both or in $A$ but not $B$, as each octant is wholly in or out of each set. For a motion, the point $p + \varepsilon s$ is in $\{Rx + t : x \in A\}$ exactly when $R^T(p - t) + \varepsilon R^T s$ is in $A$, and $R^T s$ is again a sign vector. Fact 7 of the regularized operations page says that the regularized value differs from the ordinary one only on the faces of the primitives, which have no volume, so the inside octants are the same for both. CLASSIFY then reads IN, ON or OUT from the mask as explained above. The recursion visits each node of the tree once, so it stops. The full proof is in the proof file.

The tests check CLASSIFY and MASK against a voxel brute force. All corners are integers, so the regularized solid is a union of closed unit cells, and a cell belongs to it exactly when its centre is in the ordinary formula. For random trees of depth 4 with motions, the tests compare the mask at points of the half-integer grid with the cells that the 8 points $p + s/4$ fall in, and the class at points on no plane with the ordinary formula.

## Complexity

Let $n$ be the number of nodes.

- CLASSIFY and MASK take $O(n)$ time: each node does a constant amount of work on 8-bit words and exact numbers. On a directed acyclic graph with shared subtrees, the time is linear in the size of the tree that the graph unfolds to, unless the masks are cached per node.
- The tree takes $\Theta(n)$ space.
- Classifying $q$ points takes $O(qn)$ time. Programs that classify many points, as in ray casting or volume estimation, prune the tree with bounding boxes: a subtree whose box does not contain $p$ gives the empty mask at once.

## Variants

- **General primitives.** Real CSG systems use half-spaces, cylinders, cones, spheres, tori and swept solids. Points in general position are classified by the sign of each surface function, and boundary points by neighbourhoods.
- **Ray casting.** [CSG ray casting](/csg-ray-casting/) classifies whole rays: it intersects the ray with each primitive and combines the intervals by the tree, which gives pictures and volumes.
- **Boundary evaluation.** [Boundary evaluation](/boundary-evaluation/) computes the [B-rep](/boundary-representation/) of the solid of a tree by classifying the faces of the primitives. The reverse, [B-rep to CSG conversion](/brep-to-csg-conversion/), finds a tree for a given B-rep.
- **Function representation.** In [F-rep](/function-representation/), each primitive is a real function, and union and intersection become max and min or smooth versions of them. The tree is the same, but the result is one function for the whole solid.
- **Voxels and octrees.** A tree can be converted to a [spatial occupancy enumeration](/spatial-occupancy-enumeration/) by classifying the cells, as the tests do.

## When to use it

Use CSG when solids are made from simple primitives and the design history matters: in mechanical design front ends, in parametric models whose dimensions change, in ray-traced pictures of designs and in teaching. CSG trees are small and always valid, and Booleans on them are free, since a Boolean is just a new node. Use a B-rep when the application needs the faces and edges themselves, for example for tool paths and drawings, and evaluate the tree to a B-rep once.

## Pitfalls

- **Ordinary operations at boundary points.** The ordinary formula at a point on a face can be wrong, as the floor of the pocket in the example shows. Classify the neighbourhood, not the point, or move the point off all faces first.
- **Coincident faces.** Many CSG models have faces of two primitives on the same plane, for example a pocket whose top is level with the top of the block. With floating-point faces, the two planes can differ by a rounding error, and a thin sheet or slot appears. Exact coordinates or a common tolerance avoid this.
- **Not unique.** Two trees can give the same solid. Do not compare solids by comparing trees, and do not expect a tree from a B-rep to be the tree the user built.
- **Dangling results are empty.** Two blocks that touch along a face have an empty regularized intersection, though the ordinary intersection is that face. A program that expects a face there gets nothing.
- **Unbounded primitives.** Half-spaces are useful leaves, but a tree that is not bounded is not an r-set, for example the complement of a block. Check that the root is bounded.

## Implementations

## History

Voelcker and Requicha's Production Automation Project at the University of Rochester developed CSG in the 1970s, with the PADL modelers as its systems. Requicha and Tilove gave the regularized operations in 1978. Requicha's survey of 1980 put CSG and the B-rep into one theory of representation schemes, with validity, unambiguity and uniqueness as properties of a scheme. In the same year, Tilove gave set membership classification, the method that classifies points, lines and faces against a tree with neighbourhoods. Roth's ray casting of 1982 made pictures of CSG trees, and boundary evaluation turned CSG trees into B-reps in the modelers of the 1980s.

## References
