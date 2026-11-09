---
tag: F65KA1
kind: algorithm
slug: hertel-mehlhorn
name: Hertel-Mehlhorn algorithm
aliases:
- Hertel-Mehlhorn convex decomposition
- Hertel-Mehlhorn heuristic
- removal of inessential diagonals
area: geometry/polygons
level: advanced
summary: Starts from a triangulation and removes diagonals, giving a convex partition at most 4 times the optimum.
solves: [convex-decomposition]
model: real-ram
complexity:
  vars: {n: the number of polygon vertices, r: the number of reflex vertices}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1983
  people: [Stefan Hertel, Kurt Mehlhorn]
  note: Hertel and Mehlhorn gave the method in their 1983 work on fast triangulation of simple polygons, with the journal version in Information and Control in 1985.
prereqs: [convex-decomposition, polygon-triangulation, doubly-connected-edge-list, orientation-test]
see_also: [convex-decomposition, ear-clipping, polygon-triangulation, monotone-polygon-partition, convex-polygon, minkowski-sum, triangulation-dual-tree, simple-polygon]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.5 (convex partitioning, essential diagonals, the lemma that a reflex vertex has at most two essential diagonals, and the bound of four times the optimum)
  - paper: "Stefan Hertel and Kurt Mehlhorn, Fast triangulation of the plane with respect to simple polygons, Information and Control 64, 1985, 52 to 76"
    locator: the convex partition from a triangulation by removing inessential diagonals
  - paper: "Bernard Chazelle and David P. Dobkin, Optimal convex decompositions, in Godfried T. Toussaint (editor), Computational Geometry, North-Holland, 1985, 63 to 133"
    locator: the lower bound of ceil(r/2) + 1 pieces, which also holds with Steiner points
---

The Hertel-Mehlhorn algorithm cuts a [simple polygon](/simple-polygon/) into [convex](/convex-polygon/) pieces. It starts from any [triangulation](/polygon-triangulation/) and visits the diagonals once each, in any order, deleting a diagonal whenever the two pieces on its sides merge into a convex polygon. Each test is two [orientation tests](/orientation-test/), so after the triangulation the algorithm takes $O(n)$ time. The result has at most $2r + 1$ pieces for $r$ reflex vertices, while every convex partition needs at least $\lceil r/2 \rceil + 1$, so the algorithm never uses more than four times the fewest possible pieces. It is the standard practical answer to the [convex decomposition](/convex-decomposition/) problem, whose exact algorithms take time cubic or worse in $r$.

## In plain words

Cut the polygon into triangles first. Then look at each cut between two triangles and ask whether the shape you get by removing that cut is still free of dents. If it is, remove the cut and treat the two pieces as one. If it is not, keep the cut forever.

A cut matters only at its two ends, because only the corners at the ends change when two pieces merge. A corner that points outward never causes a dent, so the cuts that survive all end at corners that point inward. Each such corner keeps at most two cuts. So the number of pieces is at most about twice the number of inward corners, which is never more than four times the best possible.

## The problem

**Input.** A simple polygon $P$ with vertices $v_0, \ldots, v_{n-1}$ in counterclockwise order, with exact coordinates, and a triangulation $T$ of $P$: $n - 2$ triangles with positive area, given as triples of vertex indices, whose sides are edges of $P$ and $n - 3$ diagonals. Vertices with a straight angle are allowed.

**Output.** A partition of $P$ into convex polygons, each given as a counterclockwise list of vertex indices, obtained from $T$ by deleting diagonals, such that every diagonal that remains is *essential*: deleting it would merge two pieces into a polygon with an angle greater than $\pi$.

**Notation.** For a diagonal $uv$ between pieces $A$ and $B$, let $x$ be the vertex before $u$ in $A$ and $y$ the vertex after $u$ in $B$. After the merge, the boundary at $u$ goes from $x$ to $u$ to $y$, so the merged angle at $u$ is at most $\pi$ exactly when $\operatorname{orient}(x, u, y) \ge 0$, and the same holds at $v$.

## The algorithm

The pieces are stored as cycles of half-edges, as in a [doubly connected edge list](/doubly-connected-edge-list/): each directed side $a \to b$ of a piece has pointers to the next and the previous side of the same piece. A diagonal $uv$ has two half-edges, $u \to v$ in one piece and $v \to u$ in the other.

```pseudo id=main
HERTEL-MEHLHORN(V[0 .. n − 1], T)
L1  for each triangle (a, b, c) of T, counterclockwise: make half-edges a→b, b→c, c→a and link them in a cycle by next and prev
L2  for each diagonal {u, v} of T, with half-edges h = u→v and t = v→u do
L3      α ← orient(tail(prev(h)), u, head(next(t)))       ▷ the angle at u after the merge
L4      β ← orient(tail(prev(t)), v, head(next(h)))       ▷ the angle at v after the merge
L5      if α ≥ 0 and β ≥ 0 then
L6          link prev(h) to next(t) and prev(t) to next(h); delete h and t
L7  return the cycles of next as the pieces
```

Line L1 turns each triangle into a cycle of three half-edges. Lines L3 and L4 look at the two ends of the diagonal: $\operatorname{tail}(\operatorname{prev}(h))$ is the vertex before $u$ in the piece of $h$, and $\operatorname{head}(\operatorname{next}(t))$ is the vertex after $u$ in the piece of $t$. Line L5 accepts a straight angle, so a merged piece may have straight vertices; it is still convex. Line L6 splices the two cycles into one in constant time. A diagonal that fails the test at line L5 is never looked at again.

## Example

Take the hexagon $P = (5,6), (3,5), (2,5), (1,2), (3,1), (4,5)$, with vertices $v_0, \ldots, v_5$. Its turns $\operatorname{orient}(v_{i-1}, v_i, v_{i+1})$ are $1, -1, 3, 7, 9, -3$, so $v_1 = (3,5)$ and $v_5 = (4,5)$ are reflex and $r = 2$. Ear clipping gives the triangles $v_5 v_0 v_1$, $v_1 v_2 v_3$, $v_5 v_1 v_3$ and $v_3 v_4 v_5$, with the diagonals $v_1 v_5$, $v_1 v_3$ and $v_3 v_5$, which the algorithm visits in that order.

| step | diagonal | $\alpha$ at $u$ | $\beta$ at $v$ | action | pieces |
|---|---|---|---|---|---|
| start | | | | | $v_5 v_0 v_1$, $v_1 v_2 v_3$, $v_5 v_1 v_3$, $v_3 v_4 v_5$ |
| 1 | $v_1 v_5$ | $\operatorname{orient}(v_0, v_1, v_3) = 4$ | $\operatorname{orient}(v_3, v_5, v_0) = 0$ | delete | $v_0 v_1 v_3 v_5$, $v_1 v_2 v_3$, $v_3 v_4 v_5$ |
| 2 | $v_1 v_3$ | $\operatorname{orient}(v_0, v_1, v_2) = -1$ | | keep | unchanged |
| 3 | $v_3 v_5$ | $\operatorname{orient}(v_1, v_3, v_4) = 8$ | $\operatorname{orient}(v_4, v_5, v_0) = -3$ | keep | unchanged |

The result has three convex pieces: $v_0 v_1 v_3 v_5$, $v_1 v_2 v_3$ and $v_3 v_4 v_5$. In step 1 the angle at $v_5$ becomes exactly $\pi$, as $v_3 = (1,2)$, $v_5 = (4,5)$ and $v_0 = (5,6)$ lie on the line $y = x + 1$. In step 2 the merge would make the reflex angle at $v_1$ whole again.

The same triangulation in the order $v_1 v_3$, $v_3 v_5$, $v_1 v_5$ gives a different answer. The tests give $\operatorname{orient}(v_5, v_1, v_2) = 0$ and $\operatorname{orient}(v_2, v_3, v_5) = 6$, so $v_1 v_3$ is deleted; then $\operatorname{orient}(v_2, v_3, v_4) = 7$ and $\operatorname{orient}(v_4, v_5, v_1) = 4$, so $v_3 v_5$ is deleted; and $v_1 v_5$ is kept, with $\operatorname{orient}(v_0, v_1, v_2) = -1$. The two pieces $v_0 v_1 v_5$ and $v_1 v_2 v_3 v_4 v_5$ are optimal, since the diagonal $v_1 v_5$ resolves both reflex vertices.

## Correctness

The [proof](proofs/correctness.md) keeps the invariant that the cycles are the pieces of $P$ cut along the diagonals not yet deleted, and that every piece is convex. Two pieces on the sides of a diagonal meet exactly in that diagonal, and only the angles at its two endpoints change in a merge; they are the sums of the two old angles, and lines L3 to L5 test exactly whether both sums are at most $\pi$. A simple polygon with no angle above $\pi$ is convex, so the merged piece is convex. A diagonal that is kept stays essential, because later merges only make the pieces next to it larger. At a reflex vertex the pieces split the angle into sectors, a diagonal there is essential only when the two sectors next to it sum to more than $\pi$, and three such diagonals would need sectors summing to more than $2\pi$. A diagonal between two convex vertices is never essential. So at most $2r$ diagonals remain.

## Complexity

- **Time.** Line L1 makes $3(n - 2)$ half-edges. The loop of lines L2 to L6 runs $n - 3$ times, once for each diagonal, and each iteration does two orientation tests and a constant number of pointer changes. Line L7 visits each remaining half-edge once. The total is $\Theta(n)$ after the triangulation.
- **Triangulation.** The whole convex partition costs the time to triangulate: $O(n \log n)$ by [monotone partition](/monotone-polygon-partition/), $O(n^2)$ by simple [ear clipping](/ear-clipping/), or $O(n)$ by Chazelle's algorithm.
- **Space.** $\Theta(n)$ for the half-edges.
- **Arithmetic.** Each test has degree 2 in the coordinates and is exact for integer and rational input.

## Properties

- **Approximation.** At most $2r + 1$ pieces, against at least $\lceil r/2 \rceil + 1$ for any convex partition, even one that uses Steiner points. Since $2r + 1 < 4(\lceil r/2 \rceil + 1)$, the result has fewer than four times the optimal number of pieces.
- **Any triangulation, any order.** The bound holds for every starting triangulation and every visiting order, but the result depends on both, as the example shows.
- **Single pass.** One pass over the diagonals is enough; no diagonal that is kept could be deleted later.
- **No new vertices.** The pieces use only vertices of $P$, and every cut is a diagonal of the triangulation.
- **Convex input.** A convex polygon comes out as one piece, from any triangulation, as every diagonal is inessential.
- **Not optimal.** Even the best order for a given triangulation may miss the optimum if the triangulation lacks the right diagonals.

## Variants and improvements

- **Better orders.** Visiting diagonals in a chosen order, for example longest first, or deleting first the diagonals whose merge leaves the largest margin below $\pi$, can give fewer pieces on some inputs, with the same bound.
- **Choosing the triangulation.** A triangulation that contains diagonals between pairs of reflex vertices, where possible, lets the algorithm keep one diagonal for two reflex vertices.
- **Optimal partitions.** For the exact optimum without Steiner points use the dynamic programming of Greene, Keil, or Keil and Snoeyink; with Steiner points, Chazelle and Dobkin's algorithm. See [convex decomposition](/convex-decomposition/).
- **Polygons with holes.** The same deletion works on a triangulation of a [polygon with holes](/polygon-with-holes/) and gives a convex partition, while the exact problem is NP-hard there.
- **Bounded piece size.** Physics engines that limit the number of vertices of a convex piece add a size test to line L5.
- **Three dimensions.** The analogous merge of tetrahedra across faces gives convex decompositions of polyhedra, but without a comparable guarantee.

## When to use it

Use it whenever a polygon must be split into convex pieces for a later step that is linear in each piece, such as [Minkowski sums](/minkowski-sum/), collision tests, or filling, and a few extra pieces are acceptable. It is simple, fast, exact and robust. If the number of pieces matters and $r$ is small, an optimal dynamic programming algorithm may be worth its cost.

## Pitfalls

- **Strict test.** Requiring $\alpha > 0$ and $\beta > 0$ keeps diagonals whose deletion would leave a straight angle. The result is still a convex partition, but with more pieces, and the bound $2r + 1$ can fail, because such a diagonal may have no reflex endpoint: in a square with an extra vertex in the middle of one side, triangulated by a fan from that vertex, the second diagonal would be kept, because its deletion leaves a straight angle at the extra vertex, and the result would have two pieces although $r = 0$.
- **Testing one end only.** The merge changes the angles at both endpoints of the diagonal; testing only $u$ can produce a nonconvex piece.
- **Wrong neighbors after merges.** The vertices in lines L3 and L4 must be read from the current cycles, not from the original triangles: after earlier merges, the vertex before $u$ in its piece may belong to a different triangle.
- **Orientation of the triangles.** A clockwise triangle reverses every test. Orient each triangle counterclockwise in line L1.
- **Degenerate triangles.** A triangulation with a zero area triangle, for example from ear clipping that clips a straight vertex, breaks the angle argument. The ear test must require a strictly convex vertex.

## Implementations

## History

Stefan Hertel and Kurt Mehlhorn described the method in their 1983 work on fast triangulation of simple polygons, published in full in Information and Control in 1985, as a way to turn their triangulation into a convex partition. The lower bound of $\lceil r/2 \rceil + 1$ pieces is due to Chazelle, in his thesis and in his work with Dobkin on optimal convex decompositions. O'Rourke's textbook made the method and its factor of four a standard part of the theory of polygon partitioning.

## References
