---
tag: GNAQSY
kind: algorithm
slug: tarjan-van-wyk-triangulation
name: Tarjan and Van Wyk polygon triangulation
aliases:
- Tarjan-Van Wyk algorithm
- O(n log log n) polygon triangulation
area: geometry/triangulations
level: research
summary: Triangulates a simple polygon in O(n log log n) time.
solves: [polygon-triangulation]
model: real-ram
complexity:
  vars: {n: the number of polygon vertices}
  time: {worst: O(n log log n)}
  space: {extra: O(n)}
properties: {online: false, deterministic: true, recursive: true}
history:
  year: 1988
  people: [Robert E. Tarjan, Christopher J. Van Wyk]
  note: Tarjan and Van Wyk computed the horizontal visibility map of a simple polygon in O(n log log n) time with a divide and conquer on the boundary, Jordan sorting and finger search trees. This was the first triangulation algorithm faster than sorting, and it answered the question left open by Garey, Johnson, Preparata and Tarjan in 1978.
prereqs: [polygon-triangulation, trapezoidal-map, monotone-polygon-triangulation, simple-polygon, jordan-curve-theorem, orientation-test]
see_also: [seidel-polygon-triangulation, chazelle-polygon-triangulation, monotone-polygon-partition, ear-clipping, polygon-simplicity-test, polygon-with-holes-triangulation, planar-subdivision, triangulation-dual-tree]
sources:
  - paper: "Robert E. Tarjan and Christopher J. Van Wyk, An O(n log log n)-time algorithm for triangulating a simple polygon, SIAM Journal on Computing 17(1), 143 to 178 (1988), doi:10.1137/0217010 (DOI to be checked); erratum in SIAM Journal on Computing 17(5), 1061 (1988)"
    locator: the visibility map computation, its analysis, and the consequences for simplicity testing
  - paper: "Kurt Hoffman, Kurt Mehlhorn, Pierre Rosenstiehl and Robert E. Tarjan, Sorting Jordan sequences in linear time using level-linked search trees, Information and Control 68(1 to 3), 170 to 184 (1986)"
    locator: Jordan sorting, the main subroutine (pages to be checked)
  - paper: "Alain Fournier and Delfin Y. Montuno, Triangulating simple polygons and equivalent problems, ACM Transactions on Graphics 3(2), 153 to 174 (1984)"
    locator: the linear-time reduction from triangulation to the trapezoidal decomposition and back
  - paper: "David G. Kirkpatrick, Maria M. Klawe and Robert E. Tarjan, Polygon triangulation in O(n log log n) time with simple data structures, Discrete and Computational Geometry 7, 329 to 346 (1992)"
    locator: the same bound without finger search trees (pages to be checked)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 2, the survey of triangulation algorithms and their time bounds
---

Tarjan and Van Wyk's algorithm solves the [polygon triangulation](/polygon-triangulation/) problem in $O(n \log \log n)$ deterministic time. It was the first method faster than $O(n \log n)$, and so it showed that triangulating a simple polygon is easier than sorting. The algorithm does not build triangles directly. It computes the **horizontal visibility map** of the polygon, which is the [trapezoidal map](/trapezoidal-map/) of its edges, by divide and conquer on the boundary. Its main tools are Jordan sorting and finger search trees. A triangulation then follows from the map in linear time. The method is long and intricate, and it was superseded in 1991 by [Chazelle's linear-time algorithm](/chazelle-polygon-triangulation/) in theory and by [Seidel's randomized algorithm](/seidel-polygon-triangulation/) in practice. The code on this page implements the pipeline around it: it computes the same visibility map with a simple $O(n \log n)$ sweep and then runs the linear-time stage that turns the map into triangles.

## In plain words

From every corner of a shape, shine a flashlight to the left and to the right, but only into the shape. Each beam stops at the first wall it hits. The beams cut the shape into thin slabs with flat tops and bottoms. Once you know where every beam lands, finishing the triangulation is easy and fast: each slab tells you whether to join its top corner to its bottom corner, and the pieces that result can be cut into triangles in one pass from top to bottom.

So the whole difficulty is finding where the beams land. The obvious way sorts the corners by height, which takes a little more than linear time. Tarjan and Van Wyk found the landing points without a full sort. They used the fact that the boundary of the shape is one connected curve that never crosses itself.

## The problem

The input is a simple polygon $P$ with vertices $v_0, \ldots, v_{n-1}$ in counterclockwise order. Edge $i$ joins $v_i$ and $v_{i+1}$, with indices modulo $n$. The output is a list of $n - 2$ triangles, as counterclockwise index triples, with disjoint interiors and union $P$.

"Above" compares points by $(y, x)$ in lexicographic order. This is a symbolic shear that gives every vertex its own height, so equal $y$ coordinates need no special case. A **chord** at a vertex $v$ is the horizontal segment from $v$ to the first edge it meets, drawn only when it starts into the interior. The set of all chords is the **visibility map**, and it cuts $P$ into trapezoids. The code assumes distinct vertices with no three collinear.

## The algorithm

**What Tarjan and Van Wyk compute.** Their algorithm computes the visibility map of $P$ on both sides of the boundary, inside and outside. It works by divide and conquer on the boundary. The boundary is cut into chains, the visibility information of the chains is computed, and then it is combined. Combining needs to know, for a horizontal line, the order along the line of the points where the line meets the boundary, when only their order along the boundary is known. This is **Jordan sorting**. Hoffman, Mehlhorn, Rosenstiehl and Tarjan solved it in linear time with level-linked search trees, using the fact that the boundary is a [Jordan curve](/jordan-curve-theorem/), so the crossings nest like parentheses. Finger search trees make each search cost the logarithm of the distance from the last position rather than of the whole size. The analysis that sums these costs over the recursion gives $O(n \log \log n)$. The details take most of a long paper and are not reproduced here.

**From the map to triangles.** Given the visibility map, a triangulation follows in linear time, as shown by Fournier and Montuno and by Chazelle and Incerpi. Each inside trapezoid has a top vertex and a bottom vertex. When the two are not adjacent on the polygon, the segment between them is a diagonal. These diagonals cut $P$ into [monotone pieces](/monotone-polygon/), and each piece is triangulated by the stack method of [monotone triangulation](/monotone-polygon-triangulation/).

The pseudocode is the pipeline implemented here. Lines L1 to L6 compute the visibility map by a sweep, which is the step that Tarjan and Van Wyk do in $O(n \log \log n)$ time instead. Lines L7 to L14 are the linear-time stage they rely on.

```pseudo id=main
TRIANGULATE-BY-VISIBILITY(P)              ▷ P simple, counterclockwise, no three vertices collinear
L1  sort the vertices from top to bottom; A ← empty list of edges, ordered left to right
L2  for each vertex v in this order do
L3      remove from A the edges whose lower end point is v
L4      binary search A for the position of v
L5      record the edges just left and just right of v, for each ray at v that starts into the interior
L6      insert into A, at that position, the edges whose upper end point is v, ordered left to right
L7  for each edge s directed downward do      ▷ the interior is east of s
        list its upper end, the vertices whose chords end on s from top to bottom, and its lower end
L8      each consecutive pair (t, b) of the list is the top and bottom vertex of one inside trapezoid
L9  for each trapezoid whose top t and bottom b are not adjacent on P do add the diagonal tb
L10 for each face Q of P cut by the diagonals do                       ▷ Q is monotone
        u[1 .. m] ← the vertices of Q from top to bottom; S ← stack (u[1], u[2])
        for j ← 3 to m − 1 do
L11         if u[j] and top(S) lie on different chains then
                pop every vertex s of S except the bottom one, output (u[j], s, the vertex under s)
                S ← stack (u[j − 1], u[j])
            else
L12             last ← pop(S)
                while S is not empty and the corner at last between top(S) and u[j] is strictly convex do
                    output (u[j], last, top(S)); last ← pop(S)
                push last; push u[j]
L13     pop the vertices of S and output the fan from u[m]
L14 return all triangles output for all faces
```

Line L5 decides which rays at $v$ start into the interior from the neighbors $u$ before and $w$ after $v$. If the boundary runs downward through $v$, the interior is east and only the right ray counts. If it runs upward, only the left ray counts. If both neighbors are below or both above, both rays count when the angle at $v$ is reflex and neither counts when it is convex.

Line L7 works because the interior of a counterclockwise polygon lies to the left of each directed edge. So a downward edge has the interior to its east, and it is the left wall of every trapezoid that touches it. The chords that end on it come from the east and split it into the left sides of those trapezoids.

## Example

Take the notched rectangle $v_0 = (0, 0)$, $v_1 = (6, 0)$, $v_2 = (6, 4)$, $v_3 = (4, 4)$, $v_4 = (3, 1)$, $v_5 = (2, 4)$, $v_6 = (0, 4)$. In the $(y, x)$ order the sweep meets $v_2, v_3, v_5, v_6, v_4, v_1, v_0$. The chords are:

| vertex | kind | left chord ends on | right chord ends on |
|---|---|---|---|
| $v_1$ | boundary runs upward | $v_6 v_0$ | none |
| $v_3$ | boundary runs downward | none | $v_1 v_2$ |
| $v_4$ | reflex, both neighbors above | $v_6 v_0$ | $v_1 v_2$ |
| $v_6$ | boundary runs downward | none | $v_4 v_5$ |

The vertices $v_0$, $v_2$ and $v_5$ have no chords, because both of their neighbors lie on the same side and their angles are convex. There are 5 chords, so there are 6 trapezoids. The downward edges are $v_2 v_3$, $v_3 v_4$, $v_5 v_6$ and $v_6 v_0$. On $v_6 v_0$ the list is $v_6, v_4, v_1, v_0$, giving the trapezoids $(v_6, v_4)$, $(v_4, v_1)$ and $(v_1, v_0)$. Each of the other three downward edges gives one trapezoid between its own end points. Only $(v_6, v_4)$ and $(v_4, v_1)$ join vertices that are not adjacent, so the diagonals are $v_4 v_6$ and $v_1 v_4$. The stack phase then gives the triangles $(v_0, v_1, v_4)$, $(v_0, v_4, v_6)$, $(v_4, v_2, v_3)$, $(v_1, v_2, v_4)$ and $(v_4, v_5, v_6)$, whose doubled areas $6 + 12 + 6 + 12 + 6$ add up to the doubled area 42 of the polygon.

## Correctness

The [correctness proof](proofs/correctness.md) of the pipeline has five steps:

- The test for which rays start into the interior is correct.
- The sweep list stays sorted, so the binary search finds the nearest edges.
- Reading consecutive chord ends along each downward edge lists every inside trapezoid exactly once.
- The top and bottom of a trapezoid are adjacent exactly when they lie on the same wall, so the added segments are non-crossing diagonals, and the faces they cut out have no interior cusp.
- The stack phase is correct.

The correctness of Tarjan and Van Wyk's $O(n \log \log n)$ map computation is proved in their paper. Since it produces the same visibility map, the rest of the argument is unchanged.

## Complexity

The algorithm of Tarjan and Van Wyk takes $O(n \log \log n)$ time and $O(n)$ space in the worst case, and the conversion to triangles adds $O(n)$. The implementation on this page sorts the vertices, so its sweep takes $O(n \log n)$ comparisons, and inserting into a Python list costs up to $O(n)$ per vertex in memory moves. For simplicity it also sorts the chord ends along each edge, the neighbors of each vertex, and the vertices of each piece. A linked visibility map gives all of these orders directly, and then lines L7 to L14 take $O(n)$ time.

## Properties

- The algorithm is deterministic and uses only comparisons and orientation tests, so it works exactly on integer or rational coordinates.
- Besides the inside map, Tarjan and Van Wyk compute the outside map. The paper lists a test of whether a polygon is simple, in the same time bound, among the consequences.
- The visibility map is unique, so every method that computes it gives the same diagonals and the same pieces.

## Variants and improvements

- **Simpler data structures.** Kirkpatrick, Klawe and Tarjan (1992) gave another $O(n \log \log n)$ algorithm that avoids finger search trees.
- **Linear time.** Chazelle (1991) computed the visibility map in deterministic $O(n)$ time. Amato, Goodrich and Ramos (2001) gave a randomized algorithm with expected $O(n)$ time.
- **Randomized.** Clarkson, Tarjan and Van Wyk (1989) gave a Las Vegas algorithm with expected $O(n \log^* n)$ time, and Seidel (1991) gave a much simpler one with the same bound.
- **Shape-sensitive bounds.** Hertel and Mehlhorn's sweep takes $O(n + r \log r)$ time for $r$ reflex vertices. Chazelle and Incerpi gave $O(n \log s)$, where $s$ measures how often the boundary winds around.

## When to use it

This algorithm is of historical and theoretical interest. It showed that triangulation is easier than sorting, and its ideas fed into later algorithms. In practice, [ear clipping](/ear-clipping/), the [monotone partition sweep](/monotone-polygon-partition/) or [Seidel's algorithm](/seidel-polygon-triangulation/) is shorter and fast. The pipeline in the code is a good way to compute a triangulation when a trapezoidal map is wanted anyway, for example for point location.

## Pitfalls

- The $O(n \log \log n)$ bound belongs to the map computation. A sweep that sorts the vertices is $\Omega(n \log n)$ in the comparison model, however fast the later stages are.
- The rays that count are the ones that start into the interior. Recording the outside rays as well gives the outside map, which has a different count of trapezoids.
- With the $(y, x)$ order, a horizontal edge is slightly tilted. Its two trapezoids of zero height are real faces of the map, and dropping them breaks the matching of left and right walls.
- When two edges start at the same vertex, their order in the sweep list comes from the orientation of their lower end points, not from those points' $x$ coordinates.

## Implementations

The Python version follows the pseudocode. `sweep_visibility` computes the chords (L1 to L6), `trapezoids` reads off the inside trapezoids and matches their left and right walls (L7, L8), `diagonals` picks the diagonals (L9), `faces` traces the pieces, and `triangulate_monotone` runs the stack algorithm (L10 to L13). It does not implement Jordan sorting or the divide and conquer of Tarjan and Van Wyk.

The tests compare the sweep with a brute-force visibility map, which compares every pair of candidate edges for every vertex. They check that the number of trapezoids is one more than the number of chords, and that the exact areas of the trapezoids sum to the area of the polygon. They also check that every piece is monotone, and they validate every triangulation: $n - 2$ counterclockwise triangles, exact area sum, $n - 3$ diagonals, no crossings, and every diagonal midpoint strictly inside. The inputs are random simple polygons, combs and their quarter turns, convex polygons, polygons with horizontal edges, large integers and `Fraction` coordinates.

## History

Garey, Johnson, Preparata and Tarjan gave an $O(n \log n)$ triangulation in 1978 and asked whether sorting is necessary. In 1984 Fournier and Montuno, and Chazelle and Incerpi, showed that triangulation and the trapezoidal decomposition can be converted into each other in linear time. So the question became how fast the visibility map can be found. Jordan sorting in linear time appeared in 1986. Tarjan and Van Wyk combined it with finger search trees to compute the map in $O(n \log \log n)$ time, published in the SIAM Journal on Computing in 1988. Their result stood as the best deterministic bound until Chazelle's linear-time algorithm of 1991.

## References
