---
tag: Y3M61K
kind: algorithm
slug: volume-decomposition-feature-recognition
name: Volume decomposition feature recognition
aliases:
- cell-based feature recognition
- delta volume decomposition
area: cad/solid-modeling
level: advanced
summary: Recognises machining features by splitting the removal volume, stock minus part, into cells and merging the cells into feature volumes such as slots, steps and pockets.
solves: [feature-recognition]
model: word-ram
complexity:
  vars: {n: the number of vertices of the part, m: the number of maximal rectangles of the removal area, k: the size of a minimum cover}
  time: {worst: "O(n^4 + m^k n^2)"}
  space: {extra: "O(m n^2)"}
properties: {deterministic: true, recursive: true, exact: true}
history:
  year: 1995
  people: [Hiroshi Sakurai]
  note: Sakurai decomposed the delta volume of a polyhedral part into maximal convex cells by cutting it with the planes of faces at concave edges, and composed the cells into feature volumes.
prereqs: [feature-recognition, regularized-set-operations, rectilinear-polygon]
see_also: [feature-interaction, alternating-sum-of-volumes, hint-based-feature-recognition, set-cover, maximal-rectangle-binary-matrix, two-dimensional-prefix-sums, brep-to-csg-conversion, computer-aided-process-planning]
sources:
  - paper: doi:10.1016/0010-4485(95)00007-0
    title: Hiroshi Sakurai, Volume decomposition and feature recognition, part 1, polyhedral objects, Computer-Aided Design 27(11), 833 to 843, 1995
    locator: the decomposition of the delta volume into maximal convex cells by the half spaces of faces at concave edges, and the composition of cells into features
  - paper: "Hiroshi Sakurai and Parag Dave, Volume decomposition and feature recognition, part II, curved objects, Computer-Aided Design 28(6/7), 519 to 537, 1996"
    locator: the extension of the cell decomposition to parts with curved faces
  - paper: "Yoonhwan Woo and Hiroshi Sakurai, Recognition of maximal features by volume decomposition, Computer-Aided Design 34(3), 195 to 207, 2002"
    locator: maximal volumes from extended faces of the delta volume, and the three steps of decomposition, selection and conversion into maximal features
  - paper: "Yuan-Jye Tseng and Sanjay B. Joshi, Recognizing multiple interpretations of interacting machining features, Computer-Aided Design 26(9), 667 to 688, 1994"
    locator: the decomposition of the removal volume into blocks and the generation of several feature interpretations by combining them
  - paper: doi:10.1109/70.897789
    title: JungHyun Han, Mike Pratt and William C. Regli, Manufacturing feature recognition from solid models, a status report, IEEE Transactions on Robotics and Automation 16(6), 782 to 796, 2000
    locator: the section on volumetric decomposition methods, cell-based decomposition and convex decomposition
---

Volume decomposition recognises machining features from the material that has to be removed, not from the faces of the part. Given a part $P$ and its stock $W$, the removal volume, or *delta volume*, is $D = W -^* P$. The method cuts $D$ into cells by extending the faces of the part, merges the cells into large simple volumes, and picks a set of those volumes that covers $D$. Each chosen volume is a feature, such as a slot, a step or a pocket, depending on which of its sides lie on the boundary of the stock. Because it works on volumes, the method copes with [interacting features](/feature-interaction/) whose faces are split or partly missing. It also gives an exact certificate: the part equals the stock minus the union of the features. Sakurai gave the cell decomposition in 1995, and Woo and Sakurai refined it into maximal features in 2002. This page gives the method for a rectilinear polygon in the plane. There it is exact and short, and the page proves that the output expression equals the part.

## In plain words

You have a block of metal, and the drawing of the finished part. Everything that is in the block but not in the part must be cut away. Volume decomposition looks at that waste material and asks how to describe it as a few simple shapes, each of which a cutter could remove in one go.

To do it, it extends every face of the part across the whole block, like slicing a cake along every edge line. The slices that are waste get glued back together into the biggest boxes that stay inside the waste. Then it keeps the fewest boxes that together cover all the waste.

Each box is a feature. A box open at the top is a slot or a pocket. A box open on two sides is a step. Subtract the boxes from the block and you get the part back exactly.

## The problem

The input is a simple rectilinear polygon $P$, given as a list of vertices with integer coordinates, the 2D section of a prismatic part. The stock $W$ is the bounding box of $P$, so $D = W -^* P$ is the area to remove. The output is a list of axis-parallel rectangles $R_1, \dots, R_k$, each with the sides of $W$ it touches, such that

1. each $R_i$ lies in $D$ and is maximal: no larger axis-parallel rectangle inside $D$ contains it,
2. $R_1 \cup \dots \cup R_k = D$, so $P = W -^* (R_1 \cup \dots \cup R_k)$,
3. $k$ is as small as possible.

A rectangle that touches the top side of $W$ can be cut from the top. One that touches two adjacent sides is a step. One that touches no side is an undercut, like the wide head of a T-slot under its narrow neck. No tool moving along an axis from outside can reach it, and the method reports it with no open sides.

## The algorithm

Line L1 builds the grid from all vertex coordinates. Every edge of $P$ lies on a grid line, so each open grid cell lies wholly inside or wholly outside $P$, and line L2 classifies it by its centre. Lines L3 and L4 list the maximal blocks of cells in $D$. A block is a range of cell columns times a range of cell rows. It is kept if all its cells are in $D$ and it cannot grow by one row or column of cells on any side. Line L5 is a depth-first [branch and bound](/depth-first-branch-and-bound/) for the smallest [set cover](/set-cover/) of the $D$ cells by maximal blocks. It always branches on the first uncovered cell, since some chosen block must contain it.

```pseudo id=main
RECOGNIZE(P)
L1  xs, ys ← the sorted distinct x and y coordinates of the vertices of P; W ← [xs_first, xs_last] × [ys_first, ys_last]
L2  D ← the grid cells whose centre is not inside P
    B ← empty list
    for each block of cells [i0, i1) × [j0, j1) of the grid do
L3      if the block holds a cell not in D then skip it
L4      if the block grown by one row or column on some side lies in D then skip it
        append the block to B
    cover ← MIN-COVER(D, B)
L6  return W and the rectangles of cover, each with its sides that lie on the boundary of W

MIN-COVER(D, B)
    best ← B
    SEARCH(chosen, covered):
        if |chosen| ≥ |best| then return
        c ← the first cell of D in sorted order that is not in covered
        if there is no such c then best ← chosen and return
L5      for each block b of B that contains c do SEARCH(chosen + [b], covered ∪ cells(b))
    SEARCH([], ∅) and return best
```

A [2D prefix sum](/two-dimensional-prefix-sums/) over the $D$ cells answers "are all cells of this block in $D$?" in constant time, which makes lines L3 and L4 cost $O(1)$ per block. The maximal blocks are the maximal all-ones submatrices of the cell matrix, the objects of the [maximal rectangle](/maximal-rectangle-binary-matrix/) problem.

## Example

Take the block $[0, 8] \times [0, 6]$ with a stepped slot cut into its top: a wide upper slot $[2, 6] \times [4, 6]$ and a narrow lower slot $[3, 5] \times [2, 4]$ below it. The part has the 12 vertices
$$(0,0), (8,0), (8,6), (6,6), (6,4), (5,4), (5,2), (3,2), (3,4), (2,4), (2,6), (0,6).$$

| step | result |
|---|---|
| grid lines (L1) | $x \in \{0, 2, 3, 5, 6, 8\}$, $y \in \{0, 2, 4, 6\}$, so $5 \times 3 = 15$ cells |
| delta cells (L2) | $[2,3] \times [4,6]$, $[3,5] \times [4,6]$, $[5,6] \times [4,6]$, $[3,5] \times [2,4]$ |
| maximal blocks (L3, L4) | $R_1 = [2, 6] \times [4, 6]$ and $R_2 = [3, 5] \times [2, 6]$ |
| cover (L5) | both are needed: the cell $[2,3] \times [4,6]$ is only in $R_1$, and $[3,5] \times [2,4]$ is only in $R_2$ |
| features (L6) | $R_1$ open at the top, a wide shallow slot; $R_2$ open at the top, a narrow deep slot |

The result is $P = W -^* ([2, 6] \times [4, 6] \cup [3, 5] \times [2, 6])$. The areas check: $8 + 8 - 4 = 12 = 4 \cdot 2 + 2 \cdot 2$. The two features overlap in $[3, 5] \times [4, 6]$. That overlap is the point of maximal volumes. The narrow slot is reported at its full depth from the top, where a cutter enters, and not as the closed box $[3, 5] \times [2, 4]$ floating under the wide slot. A face-based recognizer sees the floor of the wide slot split in two by the narrow one, and has to work to find either feature.

A second case shows a corner. For the part with vertices $(0,0), (6,0), (6,1), (5,1), (5,3), (3,3), (3,4), (0,4)$, the delta area is an L shape at the top right. Its maximal rectangles are $[3, 6] \times [3, 4]$ and $[5, 6] \times [1, 4]$, both open on the right and on the top, so both are steps. They overlap in the corner square $[5, 6] \times [3, 4]$, which either step can take.

A T-slot shows the third kind. Cut a neck $[3, 5] \times [4, 6]$ into the top of $[0, 8] \times [0, 6]$, with a head $[1, 7] \times [2, 4]$ under it. The cover is $[3, 5] \times [2, 6]$, open at the top, and the head $[1, 7] \times [2, 4]$, which has no open side. The expression is still exact, but the head is an undercut.

## Correctness

The proof file proves that the output is right, in four steps.

1. **Cells are pure.** Every edge of $P$ lies on a grid line, so an open cell meets no point of the boundary of $P$. A connected set that misses the boundary lies in the interior or in the exterior. So the centre test of line L2 classifies the whole cell.
2. **Blocks lie in $D$, and the cover is $D$.** Line L3 keeps only blocks of $D$ cells, and MIN-COVER returns blocks that contain every $D$ cell. So the union of the output rectangles is the closure of the union of the $D$ cells, which is $D$. Taking the regularized difference from $W$ gives $P$. For a point $p$ on no grid line, this means $p \in P$ exactly when $p$ is inside $W$ and inside none of the $R_i$.
3. **Maximal means maximal in $D$.** Any rectangle with nonempty interior that lies in $D$ only meets $D$ cells, so the smallest block of cells containing it lies in $D$. So a block that cannot grow by one row or column is not contained in any larger rectangle in $D$.
4. **The cover is minimum among all rectangles.** By step 3, any family of rectangles whose union is $D$ can be replaced, one for one, by maximal blocks with the same union. So the fewest maximal blocks is the fewest rectangles of any kind. The search finds it, because any cover contains a block through the first uncovered cell, and the bound only cuts branches that cannot beat the best cover found.

The tests check all of this against an oracle that does not use the code under test. They generate random simple rectilinear polygons, as polyominoes with no holes and no pinch points, traced into vertex lists and mapped onto random integer coordinates. The oracle answers membership from the generating cells. For 300 random parts, the expression of the output agrees with the oracle at 60 random points with denominator 97 and at four points next to every vertex, over 18,000 points in all. Every block is checked to lie in $D$ and to be blocked on all four sides, for 200 parts. The cover size equals a brute-force minimum over all subsets of the maximal blocks for 250 parts, and also for 400 random cell sets that are not delta areas. In 140 of those 400 sets some maximal block is redundant, which is where the search matters. The polygon cases rarely have one.

## Complexity

A part with $n$ vertices has at most $n/2$ distinct $x$ and $n/2$ distinct $y$ coordinates, so the grid has $c = O(n^2)$ cells. Line L2 runs a point-in-polygon test per cell, $O(n)$ each, for $O(n^3)$. Lines L3 and L4 look at $O(n^4)$ blocks at $O(1)$ each with prefix sums. MIN-COVER branches over at most $m$ blocks per level, for at most $k$ levels, and each search node finds the first uncovered cell in $O(n^2)$. So the worst case is $O(n^4 + m^k n^2)$ time, and the stored cell sets of the blocks take $O(m n^2)$ space.

The exponential part is honest. A minimum cover of a rectilinear polygon by rectangles is NP-hard in general, and the cover step is a [set cover](/set-cover/). In practice the delta area of a part splits into a few separate regions with few maximal rectangles each, and the search is fast. In the tests the largest instance from a part had 8 maximal blocks. The 3D methods use heuristics or [greedy set cover](/greedy-set-cover/) for this step, or keep all covers as alternative interpretations.

## Properties

- **Exact.** Integer coordinates, rational cell centres, and a proof that the expression equals the part. No tolerances.
- **Interpretation-free in the union.** By the first fact of [feature interaction](/feature-interaction/), every cover gives the same part. Which minimum cover is returned depends on the order of the search, so the features can differ between equally small answers.
- **Maximal features overlap.** The chosen rectangles are maximal, so they often overlap. That suits machining, where a region cut twice costs a little time but a region missed is an error.
- **Independent of the boundary data structure.** Only the vertex list is used. A face-based method needs the adjacency of faces and their convexity.

## Variants and improvements

- **Maximal convex cells.** Sakurai's 3D method cuts the delta volume with the planes of faces at concave edges, the only faces that can split it into convex pieces. The cells are then merged into the largest convex unions, the maximal convex cells, and features are composed from those.
- **Maximal volumes.** Woo and Sakurai extend the faces of the delta volume to form large, simple maximal volumes. They then select a cover and convert each volume into a maximal feature, a type that machining can use directly. This page follows that pattern in 2D.
- **Multiple interpretations.** Tseng and Joshi composed the blocks of the removal volume in several ways and returned every interpretation. A process planner then picks the one with the best tool sequence.
- **Curved faces.** Sakurai and Dave extended cell decomposition to cylinders and other curved faces, where extending a face is no longer a plane cut.
- **Fast cells.** Cutting by all face planes makes many cells, and building them dominates the cost. Later work, such as Woo's fast cell-based decomposition of 2003, aims to reduce the number of cells and the time to build them.

## When to use it

Use volume decomposition for prismatic parts machined from a block, when features interact and face patterns break, and when a certificate is wanted that the features remove exactly the right material. It suits 2.5D milling, where each feature is a prism along the tool axis. For simple parts with isolated features, a graph method such as the [attributed adjacency graph](/attributed-adjacency-graph/) is faster and gives named feature types directly. For parts with free-form faces, the cell count can grow fast. The related [alternating sum of volumes](/alternating-sum-of-volumes/) decomposes by convex hulls instead of cells, and [hint-based recognition](/hint-based-feature-recognition/) grows features from traces.

## Pitfalls

- **Too many cells.** Extending every face across the whole stock makes $O(n^2)$ cells in 2D and $O(n^3)$ in 3D, most of them in $P$. Extend only the faces that can split $D$, those at concave edges, as Sakurai does.
- **Classifying cells near the boundary.** The centre test is exact only when every boundary edge lies on a grid line. With floating point and nearly equal coordinates, a cell can be a sliver of width $10^{-12}$ that is misclassified. Snap or merge coordinates first.
- **Inaccessible regions.** A rectangle that touches no side of $W$ cannot be cut along an axis from outside. Since $P$ is simple, every connected piece of $D$ reaches the boundary of $W$, but a single rectangle need not. The head of a T-slot is a maximal rectangle with no open side. Such features need a special tool or another setup, and a planner must not treat them as plain pockets.
- **Minimum is not best.** The fewest features may not be the cheapest to machine. A cover with one extra feature can avoid a deep narrow cut. Treat the cover as one interpretation among several.
- **Exponential search.** Without a bound on the number of maximal blocks, the exact cover can explode. Fall back to a greedy cover and report it as such.

## Implementations

## History

Volumetric feature recognition began with the alternating sums of convex hulls of Woo in 1982 and the work of Kim in the early 1990s. Cell-based methods came next. Tseng and Joshi decomposed the removal volume into blocks and generated multiple interpretations of interacting features in 1994. Sakurai published the decomposition of polyhedral delta volumes into maximal convex cells in 1995, and with Dave extended it to curved objects in 1996. Woo and Sakurai's maximal volumes of 2002 reduced the number of interpretations and the work. The survey of Han, Pratt and Regli in 2000 placed these methods beside graph-based and hint-based recognition, and found that each handles some interactions that the others miss.

## References
