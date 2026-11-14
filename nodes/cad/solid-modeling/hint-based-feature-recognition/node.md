---
tag: 0YXFJ0
kind: algorithm
slug: hint-based-feature-recognition
name: Hint-based feature recognition
aliases:
- Vandenbrande-Requicha feature recognition
area: cad/solid-modeling
level: advanced
summary: Vandenbrande and Requicha's method that searches the B-rep for traces of features, such as opposing parallel faces, then completes and verifies each feature volume.
solves: [feature-recognition]
model: word-ram
complexity:
  vars: {n: the number of vertices of the part}
  time: {worst: "O(n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1993
  people: [Jan H. Vandenbrande, Aristides A. G. Requicha]
  note: Vandenbrande and Requicha recognized machining features from the partial traces that interacting features leave on the boundary, completed each trace into the largest compatible feature volume, and kept it only if it passed tests of validity and accessibility.
prereqs: [feature-recognition, feature-interaction, boundary-representation]
see_also: [volume-decomposition-feature-recognition, alternating-sum-of-volumes, attributed-adjacency-graph, accessibility-cone, undercut-detection, setup-planning, generate-and-test, two-dimensional-prefix-sums]
sources:
  - paper: doi:10.1109/34.250845
    title: Jan H. Vandenbrande and Aristides A. G. Requicha, Spatial reasoning for the automatic recognition of machinable features in solid models, IEEE Transactions on Pattern Analysis and Machine Intelligence 15(12), 1269 to 1285, 1993
    locator: the whole paper (hints as partial traces of features, their completion into the largest compatible volumes, and the tests that a completed volume is machinable and does not intrude into the part)
  - paper: doi:10.1109/38.656791
    title: JungHyun Han and Aristides A. G. Requicha, Feature recognition from CAD models, IEEE Computer Graphics and Applications 18(2), 80 to 94, 1998
    locator: the extension of the hint-based approach, with hints processed in order of promise and the completion and verification of each feature
  - paper: doi:10.1007/BF01638098
    title: William C. Regli, Satyandra K. Gupta and Dana S. Nau, Extracting alternative machining features, an algorithmic approach, Research in Engineering Design 7(3), 173 to 192, 1995
    locator: the generation of alternative machining feature volumes from traces in the boundary of the part
  - paper: doi:10.1109/70.897789
    title: JungHyun Han, Mike Pratt and William C. Regli, Manufacturing feature recognition from solid models, a status report, IEEE Transactions on Robotics and Automation 16(6), 782 to 796, 2000
    locator: the section on hint-based reasoning, beside graph-based and volumetric methods
---

Hint-based feature recognition looks for *traces* of features on the boundary of a part, not for complete feature patterns. A trace, or *hint*, is a small configuration of faces that a feature always leaves behind, even when other features cut into it. Two opposite parallel walls suggest a slot. A cylindrical face suggests a hole. A floor face with walls suggests a pocket. Each hint is *completed* into the largest feature volume that agrees with it, and the volume is then *verified*: it must not cut into the part, and a tool must be able to reach it. Vandenbrande and Requicha introduced the method in 1993. It was a response to [feature interaction](/feature-interaction/), which destroys the face patterns that graph methods look for but rarely destroys every trace. This page gives an exact version for rectilinear polygons in the plane. The hints are the pieces of the part's boundary, each with its outward normal. Completion sweeps a piece to the stock and widens the sweep, and pieces that cannot be reached are dropped. The page proves that the features cover exactly the reachable part of the removal area. The leftovers are undercuts, and with them the part equals the stock minus the features.

## In plain words

A detective doesn't need the whole footprint. A heel mark is enough to say "someone stood here", and then the detective works out the rest.

Hint-based recognition treats the faces of a part the same way. A flat floor with material below it says "something was cut here, from above". So the program pushes that floor straight up until it leaves the block. If the push hits material, no cutter from above could have made that floor, so the clue is dropped. If not, the program widens the shape sideways as far as the empty space allows. That shape is a feature, a slot or a step. Clues that are partly hidden, like a floor split in two by a deeper cut, still work, because each piece of the floor gives the same answer.

## The problem

The input is a simple rectilinear polygon $P$ with integer vertices, the section of a prismatic part. The stock $W$ is its bounding box, and $D = W -^* P$ is the area to remove. The cutter moves along the four axis directions. A point of $D$ is *reachable from side* $s$ if the straight segment from it to the side $s$ of $W$ does not pass through the interior of $P$. The output is a list of rectangles in $D$, each with the sides of $W$ it lies on and the sides it is reached from, such that:

1. the reachable features cover exactly the reachable points of $D$,
2. the remaining points of $D$ are covered by rectangles marked as undercuts,
3. $P = W -^* (\text{union of all rectangles})$.

## The algorithm

Line L1 builds the grid of all vertex coordinates. Every edge of $P$ lies on a grid line, so each cell lies wholly in $P$ or wholly in $D$. Line L2 enumerates the hints. A hint is a unit piece of the boundary between a cell of $P$ and a cell $c$ of $D$, and its normal $s$ points from $P$ into $D$. The piece is a floor if $s$ is up, a wall if $s$ is sideways. Line L3 sweeps $c$ in direction $s$ to the side of the stock. If the strip holds a cell of $P$, the face cannot be reached from side $s$, and the hint is dropped. Line L4 widens the strip across $s$, one row or column at a time, while the new cells are all in $D$. Line L5 records the block and the side it is reached from, so a block found from several hints is kept once. Line L6 handles the cells of $D$ that no completed block covers, if there are any. In each row it takes the maximal run of $D$ cells around them and marks it as an undercut.

```pseudo id=main
HINT-RECOGNIZE(P)
L1  build the grid of the vertex coordinates of P; D ← the cells not in P; W ← the bounding box
    F ← an empty map from blocks to sets of sides
L2  for each cell c of D and side s such that the neighbour of c opposite to s is a cell of P do
        strip ← the cells from c to the side s of W
L3      if strip holds a cell of P then continue
L4      widen strip across s, one row or column at a time, while the new cells are in D
L5      add s to F[strip]
L6  for each row, record as an undercut every maximal run of D cells in it
        that holds a cell covered by no block of F
L7  return W and every block, with its open sides, its kind and the sides it is reached from
```

A [2D prefix sum](/two-dimensional-prefix-sums/) over the cells of $D$ answers "are all cells of this block in $D$?" in constant time, which makes lines L3 and L4 cheap. The kind follows from the open sides: one open side is a slot, and two are a step. Opposite open sides would need a whole row or column of $D$ cells, and that never happens with the bounding box as stock (see Correctness).

## Example

Take the block $[0, 8] \times [0, 6]$ with a stepped slot cut into its top: a wide upper slot $[2, 6] \times [4, 6]$ over a narrow lower slot $[3, 5] \times [2, 4]$. The vertices are
$$(0,0), (8,0), (8,6), (6,6), (6,4), (5,4), (5,2), (3,2), (3,4), (2,4), (2,6), (0,6).$$
The grid lines are $x \in \{0, 2, 3, 5, 6, 8\}$ and $y \in \{0, 2, 4, 6\}$. The floor of the upper slot is split by the lower slot into two pieces, $[2, 3]$ and $[5, 6]$ at $y = 4$. A face-based recognizer that expects one floor between two walls does not find the upper slot. The seven hints are:

| hint | normal | strip to the stock | result |
|---|---|---|---|
| floor piece $[2,3]$ at $y = 4$ | up | $[2,3] \times [4,6]$, empty | widened to $[2,6] \times [4,6]$, a slot |
| floor piece $[5,6]$ at $y = 4$ | up | $[5,6] \times [4,6]$, empty | widened to $[2,6] \times [4,6]$, the same slot |
| wall at $x = 2$, $y \in [4,6]$ | right | runs into $[6,8] \times [4,6]$ | dropped |
| wall at $x = 6$, $y \in [4,6]$ | left | runs into $[0,2] \times [4,6]$ | dropped |
| floor $[3,5]$ at $y = 2$ | up | $[3,5] \times [2,6]$, empty | cannot widen, $[3,5] \times [2,6]$, a slot |
| wall at $x = 3$, $y \in [2,4]$ | right | runs into $[5,6] \times [2,4]$ | dropped |
| wall at $x = 5$, $y \in [2,4]$ | left | runs into $[2,3] \times [2,4]$ | dropped |

So there are two features, the wide slot $[2,6] \times [4,6]$ and the deep narrow slot $[3,5] \times [2,6]$, both reached from the top. They overlap in $[3,5] \times [4,6]$, and $P = W -^* (\text{their union})$. Each piece of the split floor alone recovers the whole upper slot. That is the point of a hint.

If the slot is a T-slot instead, with a neck $[3,5] \times [4,6]$ and a wider head $[1,7] \times [2,4]$, the floor of the head gives the slot $[3,5] \times [2,6]$. The cells $[1,3] \times [2,4]$ and $[5,7] \times [2,4]$ cannot be reached from any side. Line L6 takes the run of $D$ cells around them in their row, $[1,7] \times [2,4]$, and marks it as an undercut.

## Correctness

The proof file proves the following.

1. **Cells are pure**, as in [volume decomposition](/volume-decomposition-feature-recognition/): edges of $P$ lie on grid lines, so a cell is wholly inside or outside $P$.
2. **Every row and every column holds a cell of $P$.** $P$ is connected and $W$ is its bounding box, so $P$ spans the full range of $x$ and of $y$, and it has interior points in every open column and row.
3. **Completed blocks are reachable.** A block from line L5 lies in $D$ and reaches the side $s$ of $W$. Each of its cells has its whole strip to side $s$ inside the block, so every point of the block is reachable from $s$.
4. **Every reachable cell is covered.** Take a cell $c$ of $D$ reachable from side $s$. Walk from $c$ in the direction opposite to $s$. By 2, the walk meets a cell of $P$. The last cell of $D$ before it carries a hint with normal $s$. The hint's strip contains $c$ and stays in $D$, so it passes line L3, and its block covers $c$.
5. **Undercut runs touch no side of the stock.** A run from line L6 holds a cell that, by 4, is not reachable. If the run reached the left or right side of $W$, it would contain that cell's strip to the side, and the cell would be reachable. If it lay in the top or bottom row, every cell of it would be reachable through that side. So undercut runs have no open side.
6. **The expression is exact.** All blocks lie in $D$, and together they cover every cell of $D$. So their union is $D$, and $W -^* D = P$.

The tests check these claims against oracles built from the generating cells, not from the code. Half the random parts are grown polyominoes and half are blocks with winding tunnels carved in from the boundary, which make undercuts. For 600 parts and over 23,000 rational points, the tests check three things. Membership in the stock minus the features equals membership in the part. A point of $D$ lies in a reachable feature exactly when a brute-force scan along the four axis directions says its cell is reachable. No feature reaches into the part or outside the stock. Undercuts occur in 51 of the 600 parts. Hand cases cover a slot, the stepped slot, the T-slot, a corner with two steps, and a plus shape with four steps.

## Complexity

For $n$ vertices the grid has $O(n^2)$ cells and $O(n^2)$ hints. With prefix sums, line L3 is $O(1)$. Line L4 widens by at most $O(n)$ rows or columns at $O(1)$ each. So the hints cost $O(n^3)$ in all. To find the cells left over, the cells of each distinct block are marked. Two blocks reached from the same side that share their inner edge line, the line of the hint, are equal or disjoint. So the blocks with a given side and inner line hold $O(n^2)$ cells, and over the $O(n)$ lines and four sides, the marking costs $O(n^3)$. Line L6 scans each row once, in $O(n^2)$. Building the grid costs $O(n^3)$ with a point-in-polygon test per cell. The total is $O(n^3)$ time and $O(n^2)$ space.

In 3D the costs are of another kind. Hints are found by matching small face patterns. Completion and verification need [Boolean operations](/regularized-set-operations/) and tests of tool access, which dominate the running time. The number of hints is linear in the number of faces, and each hint's completion depends on how far it can grow.

## Properties

- **Robust to interaction.** A hint needs only a piece of one face. A feature whose faces are split, shortened or partly removed still leaves pieces, and any one of them suffices.
- **Exact here.** Integer coordinates, exact cell centres and constant-time block tests. No tolerances.
- **Redundant and overlapping.** Many hints give the same feature, and features overlap. Neither is an error, since machining removes material once, but the output is not a minimum set. A minimum is the business of [volume decomposition](/volume-decomposition-feature-recognition/).
- **Generate and test.** The method is a [generate-and-test](/generate-and-test/) search. Hints generate candidates, completion makes them as large as allowed, and verification rejects bad ones. Adding a feature type means adding a hint pattern, a completion rule and a test.

## Variants and improvements

- **Hint patterns in 3D.** Vandenbrande and Requicha's hints include opposing parallel planar faces for slots, a cylindrical face for a hole, and a floor face for a pocket. Completion extends the hint to the largest volume of that feature type that does not intrude into the part. Verification checks that the volume is machinable, for example that a tool can approach along an axis.
- **Rating hints.** Han and Requicha extended the approach so that hints are ordered by how promising they are, and the strongest are completed first. Weak hints are processed only if needed, which saves work on large parts.
- **Alternative interpretations.** Regli, Gupta and Nau generate the feature volumes that traces support and keep the alternatives, so that a process planner can choose. This page keeps every reachable block found from some hint.
- **Combined recognizers.** Many systems use graph matching for isolated features, hints for interacting ones, and a volumetric pass for what remains. The undercut pass of line L6 is a small instance of that.
- **Accessibility beyond axes.** Here a feature is reached only along the four axes. With more tool directions, as in five-axis machining, the test becomes an [accessibility cone](/accessibility-cone/) computation.

## When to use it

Use hint-based recognition for machined parts with many interacting features, where whole face patterns break. It also suits recognizers that grow by adding feature types one at a time. It works well when the hints of each feature type are clear and few, as for holes, slots and pockets. Pure graph matching on the [attributed adjacency graph](/attributed-adjacency-graph/) is faster for isolated features. When a provably minimal or unique decomposition is wanted, use [volume decomposition](/volume-decomposition-feature-recognition/) or the [alternating sum of volumes](/alternating-sum-of-volumes/). When undercuts matter, combine the result with [undercut detection](/undercut-detection/) and [setup planning](/setup-planning/).

## Pitfalls

- **Dropping a hint too early.** A wall hint whose strip runs into the part is not reachable from that side, but the same feature is usually found from another hint, such as its floor. Do not report a feature missing until every hint of the area has been tried, or the reachable area is checked as in claim 4.
- **Completing too far.** A completion that grows through the part gives a volume that would cut the part. Every growth step must check that the new cells lie in $D$, as line L4 does.
- **Counting features by hints.** Several hints complete to the same volume. Deduplicate by volume, as line L5 does with the map, or the planner machines the same slot twice.
- **Ignoring leftovers.** Hints can miss regions that no tool reaches along an axis, such as the head of a T-slot. Without line L6 the expression is no longer exact, and the part would keep material that should be removed. Report undercuts explicitly.
- **Taking the bounding box for granted.** With a stock larger than the bounding box, a row or column can be all $D$. Then a cell can be reachable with no hint on its line. Add the faces of the stock as hints, or start the walk of claim 4 from the stock.

## Implementations

## History

Early feature recognizers matched rules or graphs against the faces of a part, and they failed when features interacted. Vandenbrande, in his thesis work with Requicha at the University of Southern California, proposed in the late 1980s to recognize features from hints and to complete and verify each candidate volume. The 1993 paper in IEEE Transactions on Pattern Analysis and Machine Intelligence is the standard reference. Regli, Gupta and Nau gave an algorithmic treatment of trace-based extraction of alternative features in 1995. Han and Requicha extended the hint-based approach in the 1990s, and the survey of Han, Pratt and Regli in 2000 placed hint-based reasoning beside graph-based and volumetric recognition.

## References
