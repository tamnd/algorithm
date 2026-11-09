---
tag: HSYKXN
kind: problem
slug: polygon-simplicity-test
name: Polygon simplicity test
aliases:
- self-intersection test for polygons
- simple polygon test
- polygon self-intersection detection
area: geometry/polygons
level: core
summary: Decide whether a polygon is simple, i.e. has no self-intersections.
prereqs: [polygon, segment-intersection-detection, orientation-test]
see_also: [simple-polygon, shamos-hoey-algorithm, segment-intersection-detection, bentley-ottmann-algorithm, polygon-triangulation, sweep-line-technique, winding-number-algorithm, shoelace-formula]
sources:
  - paper: doi:10.1109/SFCS.1976.16
    title: Michael Ian Shamos and Dan Hoey, Geometric intersection problems, 17th Annual Symposium on Foundations of Computer Science (FOCS 1976), 208-215
    locator: the sweep for detecting an intersection among n segments, and its application to testing whether a polygon is simple
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 7, Section 7.2.3, Intersection of line segments (the sweep and the simplicity test of a polygon as a corollary)
  - paper: doi:10.1007/BF02574703
    title: Bernard Chazelle, Triangulating a simple polygon in linear time, Discrete and Computational Geometry 6(5), 485 to 524 (1991)
    locator: the linear-time triangulation, which also detects a polygon that is not simple
---

A polygon simplicity test decides whether a closed polygon, given by its vertex list $v_0, \ldots, v_{n-1}$, is a [simple polygon](/simple-polygon/): whether its boundary never touches or crosses itself, except that consecutive edges share their common vertex. Many polygon algorithms, from [triangulation](/polygon-triangulation/) to [clipping](/polygon-clipping/), require a simple polygon and give wrong output silently on any other input, so the test is the usual first check. It is [segment intersection detection](/segment-intersection-detection/) on the $n$ edges with one change, that neighboring edges are allowed to meet at their shared vertex, and the same sweep line solves it in $O(n \log n)$ time.

## In plain words

Draw the polygon with a pen, from corner to corner, and back to the start. The polygon is simple when the pen never comes back to a point it already drew, except at the very end. Every corner is visited once, two lines that meet at a corner do not fold back over each other, and two lines that are not neighbors never touch or cross.

Checking every pair of lines is slow for big polygons. A faster check moves a vertical line from left to right across the drawing, keeps the lines it cuts in order from bottom to top, and checks each line only against its neighbors in that order. The first place where the drawing touches itself is always next to such a check.

## Definition

**Input.** A list $P = (v_0, \ldots, v_{n-1})$ of points in $\mathbb{R}^2$. The edges are $e_i = v_i v_{i+1}$, indices mod $n$. Edges $e_i$ and $e_{i+1}$ are *neighbors*; for $n \ge 4$, every other pair is non-neighboring.

**Output.** "Simple" exactly when all of these hold:

1. $n \ge 3$ and the vertices are pairwise distinct;
2. each two neighboring edges $e_{i-1}$ and $e_i$ meet only in $v_i$;
3. each two non-neighboring edges are disjoint.

Then the boundary is a closed Jordan curve, and the [Jordan curve theorem](/jordan-curve-theorem/) gives it an inside and an outside. Condition 2 fails exactly when $v_{i-1}$, $v_i$, $v_{i+1}$ are collinear and the two edges point the same way from $v_i$, that is, $\mathrm{orient}(v_{i-1}, v_i, v_{i+1}) = 0$ and $(v_{i-1} - v_i) \cdot (v_{i+1} - v_i) > 0$. Three collinear vertices in order, with the middle one between the others, are allowed: the polygon goes straight on there.

**Model.** The sweep uses only comparisons of coordinates and the [orientation test](/orientation-test/), on the [real RAM](/real-ram/). With integer coordinates every test is the sign of an integer, and no intersection point is ever computed.

## Variants

- **With a witness.** Return two edges that meet, or the repeated vertex. The sweep finds one at no extra cost, and the implementation returns it.
- **Weakly simple polygons.** Allow the boundary to touch itself without crossing, for example a polygon with a slit or two parts joined at a vertex. These arise as limits of simple polygons and as outputs of clipping; deciding weak simplicity is harder, and needs a careful analysis of the touching points.
- **Collinear vertices forbidden.** Some programs also reject three consecutive collinear vertices; this is a local test in $O(n)$.
- **Several contours.** For a [polygon with holes](/polygon-with-holes/), test all contours together: no two edges of different contours may meet, and the holes must lie inside the outer boundary.
- **Orientation.** Once the polygon is known to be simple, the sign of the [shoelace formula](/shoelace-formula/) gives its orientation.

## Examples

- **Simple.** The concave pentagon $(0,0), (6,0), (6,4), (3,1), (0,4)$ is simple. So is $(0,0), (3,0), (3,3), (0,3), (0,2), (1,2), (1,1), (0,1)$, with a square notch on its left side: the edges $(0,3)$-$(0,2)$ and $(0,1)$-$(0,0)$ lie on one line but do not meet.
- **Bowtie.** $(0,0), (2,2), (2,0), (0,2)$ is not simple: the non-neighboring edges $e_0$ and $e_2$ cross at $(1,1)$.
- **Vertex on an edge.** $(0,0), (4,0), (4,4), (2,0), (0,4)$ is not simple: the vertex $v_3 = (2,0)$ lies on the edge $e_0$. The two edges touch without crossing, and a test for proper crossings only would miss it.
- **Fold.** $(0,0), (4,0), (2,0), (2,3)$ is not simple: the neighboring edges $e_0$ and $e_1$ overlap along $(2,0)$-$(4,0)$.
- **Repeated vertex.** $(0,0), (4,0), (4,4), (0,0), (0,4)$ visits $(0,0)$ twice. Every pair of edges touches only at end points, but the boundary is a figure eight, not a Jordan curve.
- **Small $n$.** No list with $n \le 2$ is simple, and a triangle is simple exactly when its vertices are not collinear.

## Known algorithms

| algorithm | time | idea |
| --- | --- | --- |
| all pairs | $\Theta(n^2)$ | check the three conditions for each pair of edges |
| sweep line (Shamos-Hoey, 1976) | $O(n \log n)$ | test only edges that become neighbors in the vertical order |
| linear-time triangulation (Chazelle, 1991) | $O(n)$ | run the triangulation, which detects a polygon that is not simple |

The sweep is the method used in practice. It processes the vertices in lexicographic order of $(x, y)$, and keeps the *status*, the edges cut by the sweep line, ordered from bottom to top. Each edge $e$ is stored with its two ends in lexicographic order, $l(e) < r(e)$, so it enters the status at $l(e)$ and leaves at $r(e)$.

```pseudo id=main
SIMPLE(P)                                   ▷ P = v[0 .. n − 1], edge i joins v[i] and v[i + 1]
L1  if n < 3 then return false
L2  if two vertices are equal then return false
L3  if some v[i] has its two edges collinear and pointing the same way then return false
L4  for each vertex p in lexicographic order do        ▷ the two edges at p are e and e′
L5      find the block B of status edges whose line passes through p, by two binary searches
L6      if B contains an edge other than e and e′ then return false        ▷ p lies on a non-neighbor
L7      delete the edges of B from the status                                ▷ the edges that end at p
L8      insert the edges that start at p at the place of B, the lower one first
L9      test the new pairs of status neighbors, skipping polygon neighbors; if two meet then return false
L10 return true
```

- **Lines L1 to L3.** These are conditions 1 and 2. After line L2 every point of the plane is the end of at most two edges, the two edges at one vertex. After line L3 two neighboring edges meet only at their shared vertex, so line L9 can skip polygon neighbors.
- **Line L5.** For a status edge $t$, the sign of $-\mathrm{orient}(l(t), r(t), p)$ is $-1$, $0$ or $+1$ when $p$ is above, on, or below the line of $t$. Along a correctly ordered status it does not decrease, so binary search finds the block of edges through $p$.
- **Line L8.** If both edges at $p$ start there, the one with the smaller slope goes below: $e$ is below $e'$ when $\mathrm{orient}(p, r(e), r(e')) > 0$.
- **Line L9.** After the deletion and insertion, the new pairs of status neighbors are the pairs across the two ends of the inserted block, or the one pair across the gap if nothing was inserted. Each is tested with the exact segment test of [segment intersection point](/segment-intersection-point/).

**Why the sweep is correct.** It never rejects a simple polygon, because each rejection exhibits a pair of edges that violates the definition. Now let $P$ be not simple but pass lines L1 to L3, and let $x$ be the lexicographically smallest point that lies on two non-neighboring edges. Before the sweep reaches $x$, no two status edges meet, so the status is ordered correctly. If $x$ is a vertex, then at the event $x$ the edge through $x$ that is not at $x$ was inserted earlier and has not ended, so it lies in the block of line L5, and line L6 rejects. Otherwise $x$ is inside two edges, and these edges are not polygon neighbors, since neighbors meet only at vertices. Let $p$ be the last vertex before $x$. Among the status edges through $x$, two are consecutive in the status after $p$: an edge between them would have to end before $x$, which no edge does after $p$, or pass through $x$ itself. Those two edges became status neighbors at some event no later than $p$, at line L8 or after line L7, and line L9 tested them then. The same argument is the correctness proof of the [Shamos-Hoey algorithm](/shamos-hoey-algorithm/), with polygon neighbors excluded.

**Cost.** Sorting the vertices takes $O(n \log n)$ time, and each event does two binary searches, at most two deletions and two insertions, and at most two pair tests. With a balanced search tree for the status the sweep takes $O(n \log n)$ time and $O(n)$ space. The implementation keeps the status in a Python list, so an insertion also moves $O(n)$ references.

## Bounds

- **Lower bound.** Every algorithm must read all $2n$ coordinates in the worst case: for a convex polygon with $n \ge 4$ vertices, moving one coordinate of one vertex far enough toward the inside makes its edges cross other edges, so an algorithm that never reads that coordinate cannot tell the two inputs apart. So the problem needs $\Omega(n)$ time.
- **Upper bound.** $O(n)$ by Chazelle's triangulation, which either triangulates the polygon or finds that it is not simple. This algorithm is not practical.
- **The practical bound.** $O(n \log n)$ by the sweep. Unlike [segment intersection detection](/segment-intersection-detection/), which needs $\Omega(n \log n)$ in the algebraic decision tree model, the polygon version gets the edges in the order of a closed chain, and this extra structure is what the linear-time algorithm uses.

## Reductions

- **To segment intersection detection.** Remove a short piece at both ends of every edge, so that neighbors no longer touch, and ask whether any two of the shortened segments meet. This needs care with the length of the cut and with exact arithmetic; the direct rule of line L9, which skips polygon neighbors, is simpler.
- **From simplicity to triangulation.** Many [triangulation](/polygon-triangulation/) and [ear clipping](/ear-clipping/) programs assume a simple input. Running the test first turns their silent failures into an explicit answer.

## Applications

- **Input validation.** Check a polygon before [triangulating](/polygon-triangulation/) it, computing its [area](/polygon-area/) as the area it encloses, or testing [point in polygon](/point-in-polygon/) by crossing parity, all of which assume simplicity.
- **Geographic data.** A boundary of a land parcel or a country that crosses itself is an error in the data; validation tools for map formats run this test.
- **Drawing and modeling.** Interactive editors test whether a new vertex makes the outline cross itself, and fonts and vector graphics are checked before conversion to other formats.
- **Clipping.** Algorithms such as [Weiler-Atherton](/weiler-atherton-algorithm/) need simple input, and others such as [Vatti's](/vatti-clipping/) take any polygon and can be used to make it simple, as the union of the polygon with itself under a fill rule.

## References
