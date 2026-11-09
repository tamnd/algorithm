---
tag: PDWJDT
kind: algorithm
slug: guibas-stolfi-algorithm
name: Guibas-Stolfi divide-and-conquer Delaunay
aliases:
- Guibas-Stolfi algorithm
- divide-and-conquer Delaunay triangulation
- Lee-Schachter algorithm
area: geometry/voronoi-and-delaunay
level: advanced
summary: Divide-and-conquer O(n log n) construction of the Delaunay triangulation using the quad-edge structure.
solves: [delaunay-triangulation-construction]
model: real-ram
complexity:
  vars: {n: the number of input points}
  time: {worst: O(n log n)}
  space: {extra: O(n)}
properties: {online: false, deterministic: true, recursive: true}
history:
  year: 1985
  people: [Leonidas Guibas, Jorge Stolfi]
  note: Lee and Schachter gave the divide-and-conquer Delaunay method in 1980; Guibas and Stolfi gave it its standard form in 1985, with the quad-edge structure and the in-circle test only.
prereqs: [delaunay-triangulation, quad-edge-data-structure, in-circle-test, orientation-test]
see_also: [dwyer-algorithm, fortunes-algorithm, bowyer-watson-algorithm, voronoi-diagram, divide-and-conquer-convex-hull, merge-sort, lexicographic-order, voronoi-construction-lower-bound]
sources:
  - paper: doi:10.1145/282918.282923
    title: L. Guibas and J. Stolfi, Primitives for the manipulation of general subdivisions and the computation of Voronoi diagrams, ACM Transactions on Graphics 4(2), 1985
    locator: the part on the quad-edge structure and its operators, and the part on the divide-and-conquer Delaunay algorithm with its merge loop
  - paper: doi:10.1007/BF00977785
    title: D. T. Lee and B. J. Schachter, Two algorithms for constructing a Delaunay triangulation, International Journal of Computer and Information Sciences 9, 1980
    locator: the divide-and-conquer algorithm and its O(n log n) bound
  - paper: doi:10.1007/BF01840356
    title: R. A. Dwyer, A faster divide-and-conquer algorithm for constructing Delaunay triangulations, Algorithmica 2, 1987
    locator: the comparison of cuts and the use of the Guibas-Stolfi merge
---

The Guibas-Stolfi algorithm builds the [Delaunay triangulation](/delaunay-triangulation/) of $n$ points in $O(n \log n)$ worst-case time. It sorts the points, splits them into a left half and a right half, triangulates each half recursively, and then merges the two triangulations. The merge first finds the lower common tangent of the two halves and then zips the halves together from bottom to top, adding one cross edge per step and deleting the old edges that fail the [in-circle test](/in-circle-test/). The triangulation is stored in the [quad-edge structure](/quad-edge-data-structure/), and the only predicates are the [orientation test](/orientation-test/) and the in-circle test.

## In plain words

Sort the points from left to right and cut the list in the middle. Triangulate each part with the same method, then join the parts.

Find the lowest line that touches both parts, so that all points are above it or on it. Draw that line as the first joining edge. Then build up, like a zip. At each step, look at the best next point on the left side and on the right side. A left edge that would block the new triangle is removed. Of the two candidates, take the one whose circle with the current edge holds no other candidate. Draw the new joining edge and repeat. Stop when no point is above the current edge.

Each step either adds a joining edge or removes an old edge, so the work of putting the parts together is proportional to their size.

## The problem

The input is a finite list $P$ of points $p = (x, y)$ with integer coordinates; repeats are allowed. The output is the list of triangles of a Delaunay triangulation of the distinct points of $P$: a [triangulation](/triangulation-of-point-set/) in which no point lies strictly inside the circumcircle of a triangle. Each triangle is a counterclockwise triple. If all points lie on one line, the output is empty.

Notation: $n = |P|$, $h$ is the number of convex hull vertices, $\prec$ is the [lexicographic order](/lexicographic-order/) on $(x, y)$, $\mathrm{orient}(a, b, c)$ is the sign of $(b - a) \times (c - a)$ (positive for a counterclockwise turn), and for counterclockwise $a, b, c$, $\mathrm{incircle}(a, b, c, d)$ is positive when $d$ is strictly inside the circle through $a, b, c$, zero on it and negative outside. A point is *valid* when it is strictly to the right of the current base edge basel, that is, above it in the merge.

Edges of the quad-edge structure are directed. $\mathrm{Onext}(e)$ is the next edge counterclockwise around the origin of $e$, $\mathrm{Oprev}(e)$ the next one clockwise, $\mathrm{Sym}(e)$ the reverse edge, $\mathrm{Lnext}(e)$ the next edge around the face to the left of $e$, and $\mathrm{Rprev}(e)$ the next edge counterclockwise out of the destination of $e$. Connect$(a, b)$ adds an edge from the destination of $a$ to the origin of $b$. Duplicates are removed and collinear points are allowed. The correctness proof assumes that no four points lie on one circle; with cocircular points the code returns one of the Delaunay triangulations.

## The algorithm

```pseudo id=main
GUIBAS-STOLFI(P)
L1  S ← the distinct points of P sorted by ≺; return the triangles of BUILD(S)
BUILD(s), which returns the handles (le, re)
L2  if |s| ≤ 3 then
L3      make an edge, a path or a triangle; return its two hull handles
L4  (ldo, ldi) ← BUILD(the first ⌊|s|/2⌋ points of s)
L5  (rdi, rdo) ← BUILD(the other points of s)
L6  move ldi by Lnext and rdi by Rprev to the lower common tangent; basel ← Connect(Sym(rdi), ldi)
L7  loop
L8      lcand ← Onext(Sym(basel)); if valid, delete it while Onext(lcand) is strictly inside the circle of basel and lcand
L9      rcand ← Oprev(basel); if valid, delete it while Oprev(rcand) is strictly inside the circle of basel and rcand
L10     if neither lcand nor rcand is valid then exit the loop
L11     if lcand is not valid, or rcand is valid and its end is strictly inside the circle of basel and lcand, then basel ← Connect(rcand, Sym(basel)) else basel ← Connect(Sym(basel), Sym(lcand))
L12 return (ldo, rdo), with each handle replaced by the base edge when its old origin was a tangent point
```

- **Line L1** sorts and removes duplicates. Sorting by $x$ and then $y$ makes every point of the left half lexicographically smaller than every point of the right half, so the convex hulls of the halves are disjoint, even when many points have the same $x$.
- **Line L3.** Two points give one edge. Three points give a path if they are collinear, and a counterclockwise triangle otherwise. The handle le is the counterclockwise hull edge out of the smallest point, and re is the clockwise hull edge out of the largest point.
- **Line L6** walks the two hulls toward each other. If the origin of rdi is strictly left of ldi, ldi moves on; else if the origin of ldi is strictly right of rdi, rdi moves on. The walk stops at the lower common tangent, and the new edge basel goes from the right tangent point to the left one.
- **Line L8.** lcand is the first edge counterclockwise after basel out of its left end. While the next edge around that point ends strictly inside the circle through basel and lcand, the edge lcand cannot be Delaunay, so it is deleted.
- **Line L9** is the mirror image at the right end of basel, with Oprev.
- **Line L11** keeps the candidate whose circle with basel holds the other candidate on its boundary or outside. The new cross edge becomes basel.
- **Line L12.** The outer handles only change when a half had its extreme point on the tangent, and then the base edge is the right hull edge.

## Example

Take the six points, already sorted, $(0,1), (2,0), (3,6) \mid (4,5), (5,5), (6,2)$. Each half is one triangle. The lower common tangent is $(2,0)$ to $(6,2)$, so line L6 makes basel $= (6,2) \to (2,0)$.

| step | lcand at (2,0) | rcand at (6,2) | action |
| --- | --- | --- | --- |
| 1 | (3,6), next (0,1) is outside | (4,5), next (5,5) is outside | (4,5) is inside the circle of (2,0) (6,2) (3,6); add (4,5)-(2,0) |
| 2 | (3,6), next (0,1) is inside: delete (2,0)-(3,6); then (0,1) | (5,5) is not valid | add (4,5)-(0,1) |
| 3 | (3,6) | (5,5) is not valid | add (4,5)-(3,6) |
| 4 | (0,1) is not valid | (5,5) | add (5,5)-(3,6) |
| 5 | nothing valid | nothing valid | stop |

In step 1 the circle through $(2,0), (6,2), (3,6)$ has center $(67/22, 32/11)$ and squared radius $4625/484$, and $(4,5)$ is at squared distance $2557/484$, so the right candidate wins. In step 2 the basel is $(4,5) \to (2,0)$ and the circle through $(2,0), (4,5), (3,6)$ has center $(17/14, 45/14)$ and squared radius $1073/98$; the point $(0,1)$ is at squared distance $625/98$, so the left edge $(2,0)$-$(3,6)$ is deleted. The result has the five triangles

$$(0,1)(2,0)(4,5),\quad (0,1)(4,5)(3,6),\quad (2,0)(6,2)(4,5),\quad (3,6)(4,5)(5,5),\quad (4,5)(6,2)(5,5).$$

There are $h = 5$ hull vertices and $2n - 2 - h = 5$ triangles, as [Euler's formula](/euler-formula/) requires.

## Correctness

**Theorem.** If no four of the distinct points lie on one circle, GUIBAS-STOLFI terminates and returns the unique Delaunay triangulation of the points, or the empty list when they lie on one line.

Call $pq$ a Delaunay edge of a set $A$ if some circle through $p$ and $q$ has all other points of $A$ strictly outside. A Delaunay edge of $L \cup R$ between two points of $L$ is a Delaunay edge of $L$, so the merge only has to add cross edges and delete wrong edges. The proof has five parts. (1) The walk of line L6 never passes the tangent points and stops exactly at them, by an argument on the directions of the two hull chains. (2) The cross edges of the final triangulation are ordered from the tangent upward, and consecutive ones span one Delaunay triangle $t_i$. (3) No deletion in line L8 or line L9 removes a Delaunay edge; a pencil argument on the circles through the two ends of basel shows this. (4) In each pass, the deletions remove exactly the edges that cross the next cross edge, and line L11 picks the third vertex of $t_i$. (5) When no point is valid, every remaining edge is Delaunay, as an edge that is not Delaunay would cross a cross edge. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Merge.** The walk of line L6 moves each pointer forward along a hull chain and never past the tangent, so it takes $O(n)$ steps. Each pass of line L7 adds one edge, and each deletion removes one edge that was added before. A planar graph on $m$ points has at most $3m - 6$ edges, so the merge of $m$ points takes $O(m)$ time.
- **Worst case.** With $T(n) = 2T(n/2) + O(n)$, the [master theorem](/master-theorem/) gives $O(n \log n)$, plus $O(n \log n)$ for the sort, as for [merge sort](/merge-sort/). This bound is proved, and it is optimal in the [algebraic decision tree](/algebraic-decision-tree/) model by the [lower bound](/voronoi-construction-lower-bound/). The proof is in [the complexity proof](proofs/complexity/).
- **Space.** The quad-edge structure holds at most $3n - 6$ live edges. The code reuses the records of deleted edges, so the space is $O(n)$. The recursion depth is $O(\log n)$.

## Properties

- **Exact.** Only the orientation test (degree 2) and the in-circle test (degree 4) are used, on integers.
- **Deterministic.** The worst-case bound holds for every input; no randomness is used.
- **Offline.** All points must be known before the sort.
- **Degenerate input.** Collinear runs give paths in the base case and are handled by the strict tests. With four or more cocircular points, the strict tests of lines L8, L9 and L11 pick one of the Delaunay triangulations; tests on grids find a valid one each time, but this case is not covered by the proof.

## Variants and improvements

- **Dwyer's cuts.** [Dwyer's algorithm](/dwyer-algorithm/) first cuts the plane into vertical strips. It triangulates each strip with cuts by $y$ and then merges neighbouring strips, with the same merge. Its expected running time is $O(n \log \log n)$ for points that are uniform in a square.
- **Voronoi output.** The quad-edge structure stores the dual subdivision at the same time, so the [Voronoi diagram](/voronoi-diagram/) is available with no extra work.
- **Convex hull.** The merge contains the hull merge of [divide-and-conquer convex hull](/divide-and-conquer-convex-hull/): the tangent of line L6 is the lower bridge, and the last basel is the upper bridge.

## When to use it

Use it for a static set of points when a deterministic $O(n \log n)$ bound and exact predicates are needed. In practice it is among the fastest planar Delaunay methods. For points that arrive one at a time, use [Bowyer-Watson](/bowyer-watson-algorithm/) with a random insertion order. For the Voronoi diagram as a sweep, use [Fortune's algorithm](/fortunes-algorithm/).

## Pitfalls

- **Splitting by $x$ only in line L1.** If many points have the same $x$, a split by $x$ alone can put points with equal $x$ on both sides, and the hulls of the halves can overlap. Sort by $(x, y)$ and split by position.
- **Non-strict tests in line L6.** If the walk also moves when three points are on one line, it can move past a tangent point that lies between two other points on the tangent line, and basel then passes through a point. Move only on a strict turn.
- **Using $\ge 0$ in the tests of lines L8 and L9.** With cocircular points this deletes edges that are needed, and the zip can stop with a hole. Use strict tests.
- **Forgetting to update the handles in line L12.** If the extreme point of a half is a tangent point, the old handle is no longer a hull edge, and the next merge starts its walk on a wrong edge.
- **Not reusing deleted edge records.** Without a free list, the structure keeps all deleted edges and the memory grows to $O(n \log n)$.

## Implementations

## History

D. T. Lee and B. J. Schachter gave a divide-and-conquer Delaunay algorithm in 1980, with an $O(n \log n)$ bound. Leonidas Guibas and Jorge Stolfi published the standard form in 1985, in a paper that also introduced the quad-edge structure. Their merge uses only the in-circle test and the orientation test, and the code is short. Rex Dwyer showed in 1987 that a different order of cuts gives an expected $O(n \log \log n)$ time on uniform points. Tests by Su and Drysdale and by Shewchuk later found the divide-and-conquer method to be among the fastest in practice.

## References
