---
tag: FCMSRJ
kind: algorithm
slug: chazelle-dobkin-algorithm
name: Chazelle-Dobkin convex intersection algorithm
aliases:
- chazelle-dobkin-convex-intersection
area: geometry/intersections
level: research
summary: Test whether two preprocessed convex objects meet in sublinear time by prune and search, O(log(p+q)) for convex polygons and O(log^3 N) for convex polyhedra.
solves: [convex-collision-detection]
model: real-ram
complexity:
  vars: {p: the number of vertices of P, q: the number of vertices of Q}
  time: {worst: O(log p + log q)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1980
  people: [Bernard Chazelle, David P. Dobkin]
  note: "Chazelle and Dobkin announced the sublinear tests at STOC 1980 under the title Detection is easier than computation, and published the full version in the Journal of the ACM in 1987."
prereqs: [convex-collision-detection, convex-polygon, prune-and-search]
see_also: [convex-polygon-intersection, convex-polyhedra-intersection, point-in-convex-polygon, separating-axis-theorem, gjk-algorithm, binary-search, andrew-monotone-chain, rotating-calipers]
sources:
  - paper: doi:10.1145/7531.24036
    title: Bernard Chazelle and David P. Dobkin, Intersection of convex objects in two and three dimensions, Journal of the ACM 34(1), 1987, 1-27
    locator: the logarithmic tests for a point, a line and a convex polygon against a convex polygon, and the polylogarithmic tests for convex polyhedra
  - paper: doi:10.1016/0304-3975(82)90120-7
    title: David P. Dobkin and David G. Kirkpatrick, Fast detection of polyhedral intersection, Theoretical Computer Science 27(3), 1983
    locator: the hierarchical representation of a convex polyhedron and the sublinear tests built on it
  - paper: doi:10.1016/0196-6774(85)90007-0
    title: David P. Dobkin and David G. Kirkpatrick, A linear algorithm for determining the separation of convex polyhedra, Journal of Algorithms 6(3), 1985
    locator: the linear-time computation of the separation of two convex polyhedra with the hierarchical representation
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 7, Intersections (intersection of convex polygons and the detection problems)
---

The Chazelle-Dobkin algorithm decides whether two convex objects meet without looking at most of their boundary. For two convex polygons $P$ and $Q$ with $p$ and $q$ vertices, stored in arrays, it answers in $O(\log p + \log q)$ time, far below the $O(p + q)$ needed to compute $P \cap Q$. The method is prune and search: compare the middle vertex of a boundary piece of $P$ with the middle vertex of a piece of $Q$, use the slopes there to show that one half of one piece cannot matter, and drop it. Chazelle and Dobkin gave such tests for points, lines, planes, polygons and polyhedra in two and three dimensions, with $O(\log^3 N)$ time for two convex polyhedra of $N$ vertices in total. The polygon test on this page is a compact version of their slope search, written for the yes or no question.

## In plain words

Think of two convex shapes drawn on paper, each split into a top edge line and a bottom edge line. The two shapes overlap exactly when the top of the first shape reaches the bottom of the second somewhere, and the top of the second reaches the bottom of the first somewhere.

So the question becomes: does the gap between one top line and one bottom line ever close? This gap first grows and then shrinks, like a hill. To find its highest point, look at the middle corner of each line. The way the lines tilt there tells which side of the hill is uphill, so half of the corners of one line can be thrown away. Repeating this halving finds the top of the hill after a few dozen steps, even for shapes with millions of corners.

## The problem

The input is two convex polygons in the plane, each of them possibly a point or a segment, with vertex coordinates in a field such as the rationals. Each polygon is given by its upper and lower chain: the vertices of the top boundary and of the bottom boundary, each sorted by $x$ in an array. The output is whether the closed polygons share a point. This is the planar case of [convex collision detection](/convex-collision-detection/).

The chains are preprocessing: from a counterclockwise vertex array they are two subarrays between the leftmost and the rightmost vertex, and from an unsorted point set they come from the [monotone chain hull](/andrew-monotone-chain/) in $O(n \log n)$ time. After that the polygons can be tested against each other many times, in any relative position.

## The algorithm

Let $U_P$, $L_P$, $U_Q$, $L_Q$ be the chains, read as functions of $x$: $U$ is concave, $L$ is convex, and the polygon is the region between them. The polygons meet exactly when $U_P - L_Q$ is nonnegative somewhere on the common $x$-range and $U_Q - L_P$ is nonnegative somewhere; this is Lemma 1 of the proof, and it needs only the fact that the two gaps add up to two nonnegative heights. Each gap $g = u - l$ is concave and piecewise linear, so the question is whether its maximum is at least $0$.

```pseudo id=main
CONVEX-MEET(P, Q)
L1  (U_P, L_P), (U_Q, L_Q) ← the chains of P and Q, built once in advance
L2  return GAP(U_P, L_Q) and GAP(U_Q, L_P)
GAP(u, l)                                 ▷ is u − l ≥ 0 somewhere?
L3  [lo, hi] ← the common x-range of u and l; if lo > hi then return false
L4  I ← the vertices of u with lo < x < hi; J ← the vertices of l with lo < x < hi
L5  [wl, wr] ← [lo, hi]                   ▷ the window that holds a maximum of g
L6  while I and J are nonempty: let a, b be the medians of I and J; from the edge slopes at a and b decide on which side of a or b the maximum lies; drop that half of I or J and move wl or wr
L7  if I is nonempty: l is a line on [wl, wr]; binary search I by the sign of g just right of each vertex, moving wl and wr
L8  if J is nonempty: u is a line on [wl, wr]; binary search J in the same way
L9  return max(g(wl), g(wr)) ≥ 0          ▷ g is linear on the final window
```

Line L6 does the real pruning. Write $s_u(i)$ for the slope of the edge of $u$ that starts at vertex $i$, and the same for $l$. If the median vertex $a$ of $u$ is left of the median vertex $b$ of $l$, then just right of $a$ the gap has slope at least $s_u(i) - s_l(j - 1)$, because the edge of $l$ there is at most edge $j - 1$ and convex slopes increase. If this number is positive, the gap is still rising at $a$, so the maximum is right of $a$, and all vertices of $u$ up to $a$ can go. If it is not positive, then just left of $b$ the gap has slope at most $s_u(i) - s_l(j - 1) \le 0$, so the gap is already falling at $b$, and all vertices of $l$ from $b$ on can go. The case $a > b$ is the mirror image, and $a = b$ compares the two right slopes directly. Every pass halves one of the two vertex sets, which gives $O(\log p + \log q)$ passes. When one set is empty, its chain is a single line over the window, and lines L7 and L8 finish with an ordinary [binary search](/binary-search/) over the other chain.

## Example

$P$ has the vertices $(0, 0), (2, 3), (4, 4), (6, 4), (8, 3), (10, 0), (5, -2)$, so $U_P = (0, 0), (2, 3), (4, 4), (6, 4), (8, 3), (10, 0)$. $Q$ has the vertices $(1, 8), (3, 6), (5, 5), (7, 5), (9, 7), (5, 10)$, so $L_Q = (1, 8), (3, 6), (5, 5), (7, 5), (9, 7)$. The first call is GAP$(U_P, L_Q)$ on $[lo, hi] = [1, 9]$, with $I = \{(2, 3), (4, 4), (6, 4), (8, 3)\}$ and $J = \{(3, 6), (5, 5), (7, 5)\}$.

| line | $a$ in $I$ | $b$ in $J$ | slopes | decision | window |
| --- | --- | --- | --- | --- | --- |
| L5 | | | | | $[1, 9]$ |
| L6 | $(4, 4)$ | $(5, 5)$ | $s_u = 0$ right of $a$, $s_l = -1/2$ left of $b$ | $0 + 1/2 > 0$: rising at $4$, drop $(2, 3), (4, 4)$ | $[4, 9]$ |
| L6 | $(6, 4)$ | $(5, 5)$ | $s_u = 0$ left of $a$, $s_l = 0$ right of $b$ | $0 - 0 \le 0$: not rising at $6$, drop $(6, 4), (8, 3)$ | $[4, 6]$ |
| L8 | | $(5, 5)$ | $u$ has slope $0$ on $[4, 6]$, $s_l = 0$ right of $b$ | $0 - 0 \le 0$: set $wr = 5$ | $[4, 5]$ |
| L8 | | $(3, 6)$ | | left of the window, drop | $[4, 5]$ |
| L9 | | | | $g(4) = 4 - 11/2 = -3/2$, $g(5) = 4 - 5 = -1$ | |

The maximum of the gap is $-1 < 0$, so the top of $P$ stays below the bottom of $Q$ everywhere, and CONVEX-MEET returns false without the second call. Moving $Q$ down by $1$ changes the last row to $g(5) = 0$, and the second call GAP$(U_Q, L_P)$ is true at once, so the answer becomes true: the polygons then share the segment from $(5, 4)$ to $(6, 4)$. An exact test reports this touching contact; a test with a tolerance or with floating point slopes may report either answer.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Lemma 1 reduces the meeting of the polygons to two gap questions; the step that needs care is that the two sets where the gaps are nonnegative must overlap, since the sum of the gaps is the sum of two vertical heights. For each gap, the invariant says that the window $[wl, wr]$ contains a maximum of $g$, because $g$ is rising at $wl$ and not rising at $wr$, and that every vertex inside the window is still in $I$ or $J$. The slope comparisons of line L6 keep the invariant by the monotonicity of the slopes of a concave and a convex chain. At the end no vertex lies inside the window, $g$ is linear there, and its maximum is at an end of the window.

## Complexity

Each pass of lines L6, L7 and L8 does $O(1)$ slope computations and removes at least half of $I$ or $J$, so a call of GAP has at most $\lceil \log_2(p + 1) \rceil + \lceil \log_2(q + 1) \rceil$ passes. Lines L4, L7, L8 and L9 add a constant number of binary searches for an $x$-coordinate. So the test runs in $O(\log p + \log q) = O(\log(p + q))$ time with $O(1)$ extra space, after $O(p + q)$ preprocessing from counterclockwise arrays. The tests on this page count the steps and stay below $40 \log_2 n$ for $n$ up to $4096$. Random access to the vertex arrays is essential: with linked lists the same method takes linear time.

## Properties

- **Exact.** All comparisons are signs of slope differences and of $g$, rational in the input, so with integer or `Fraction` coordinates the test is exact, including all touching cases.
- **Sublinear.** The test reads only $O(\log(p + q))$ vertices, which is possible only because the boundary is already sorted; computing $P \cap Q$ needs $\Theta(p + q)$ in the worst case.
- **Relative position free.** The preprocessing of $P$ and of $Q$ is independent, so one polygon can be tested against many translates or other polygons.
- **Degenerate inputs.** Points, segments and vertical edges are covered: a vertical segment has one-vertex chains, and vertical edges of a polygon are implicit at the ends of the chains.

## Variants and improvements

- **Point and line queries.** A point against a convex polygon is a [binary search](/point-in-convex-polygon/) in $O(\log n)$. A line against a convex polygon is two extreme-vertex searches in $O(\log n)$. These are the simplest tests of Chazelle and Dobkin.
- **Separation and distance.** The distance between two convex polygons, and a separating line when they are disjoint, can also be found in $O(\log p + \log q)$ time by a similar search on the two boundaries; Dobkin and Kirkpatrick treat the separation of polyhedra with their hierarchy.
- **Convex polyhedra.** In three dimensions Chazelle and Dobkin test two convex polyhedra in $O(\log^3 N)$ time after preprocessing. With the hierarchical representation of Dobkin and Kirkpatrick, a sequence of $O(\log N)$ simpler and simpler polyhedra, the time was reduced in later work to $O(\log^2 N)$ and then to $O(\log N)$.
- **Polyhedron against a line or a plane.** These take $O(\log N)$ with the hierarchy, as does testing a point.
- **Computing the intersection.** If the full polygon $P \cap Q$ is needed, use the linear-time [convex polygon intersection](/convex-polygon-intersection/) of O'Rourke, Chien, Olson and Naddor; in three dimensions the [convex polyhedra intersection](/convex-polyhedra-intersection/) of Chazelle.

## When to use it

Use the logarithmic test when many pairs of large convex polygons are tested and their sorted boundaries are stored, as in some collision and visibility programs, or when a test is a step inside a larger algorithm that cannot afford linear time. For small polygons, or a single test, the [separating axis theorem](/separating-axis-theorem/) in $O(p + q)$ or [GJK](/gjk-algorithm/) is simpler and fast in practice. When the objects move a little between queries, GJK or [rotating calipers](/rotating-calipers/) with a warm start is usually better.

## Pitfalls

- **One gap test is not enough.** Line L2 needs both calls. With $P = [0, 2] \times [3, 5]$ and $Q = [0, 2] \times [0, 1]$, the top of $P$ is above the bottom of $Q$ everywhere, but $Q$ lies below $P$; only the second call, $U_Q - L_P = 1 - 3 < 0$, shows that they are disjoint.
- **One-sided slopes at line L6.** At a vertex the gap has two slopes. The pruning must use the right slope to drop vertices to the left and a left slope to drop vertices to the right, with the bound for the other chain taken on the correct side. In the case $a < b$, the slope of the edge of $l$ that starts at $b$ says nothing about the gap at $a$; the bound must use edge $j - 1$, the last edge of $l$ that can lie right of $a$.
- **Equal $x$-coordinates.** When the two medians have the same $x$, both chains bend there, and line L6 must compare the slopes of the edges on the same side; a program that treats the case like $a < b$ reads an edge that does not exist or the wrong one.
- **End vertices at line L4.** The vertices at $lo$ and $hi$ must not enter $I$ or $J$, since one of their edges lies outside the common range; including them leads to out-of-range slopes when the ranges end at a vertex.
- **Strict and weak signs.** Line L6 drops the left part only when the slope is strictly positive, and line L9 accepts $\max g = 0$. Changing either sign gives wrong answers for polygons that touch at a vertex or along an edge, which random integer inputs produce often.
- **Floating point.** With floating point slopes, a touching contact as in the example can be reported either way. Use exact rationals or compare cross products of integers.

## Implementations

## History

Chazelle and Dobkin presented their logarithmic and polylogarithmic intersection tests at STOC 1980 under the title "Detection is easier than computation", and the full paper "Intersection of convex objects in two and three dimensions" appeared in the Journal of the ACM in 1987. The title states the point of the work: deciding whether two convex objects meet can be exponentially faster than computing their intersection. Dobkin and Kirkpatrick introduced the hierarchical representation of convex polyhedra in 1983 and used it for fast detection and for the separation of polygons and polyhedra in 1985; later work by the same authors and others improved the polyhedra test to logarithmic time. The prune-and-search scheme of the polygon test is the same as in the search for common tangents and in Megiddo's linear programming.

## References
