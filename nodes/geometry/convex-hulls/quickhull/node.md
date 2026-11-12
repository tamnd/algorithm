---
tag: QJNWCK
kind: algorithm
slug: quickhull
name: Quickhull
aliases:
- quickhull algorithm
- QuickHull
area: geometry/convex-hulls
level: core
summary: Recursively discards points inside the hull edge found by the farthest point; O(nh) time, Θ(n^2) in the worst case, and fast on typical random inputs.
solves: [convex-hull-problem]
model: real-ram
complexity:
  vars: {n: the number of input points, h: the number of hull vertices}
  time: {best: Θ(n), worst: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: true, output-sensitive: true}
history:
  year: 1977
  people: [William F. Eddy, A. Bykat]
  note: Eddy published the planar method in ACM Transactions on Mathematical Software in 1977, Bykat gave the same recursion in 1978, and Barber, Dobkin and Huhdanpaa extended it to d dimensions as Qhull in 1996.
prereqs: [convex-hull-problem, orientation-test]
see_also: [graham-scan, jarvis-march, andrew-monotone-chain, divide-and-conquer-convex-hull, kirkpatrick-seidel, chan-algorithm, convex-hull-3d, quicksort]
sources:
  - paper: doi:10.1145/355759.355766
    title: William F. Eddy, A new convex hull algorithm for planar sets, ACM Transactions on Mathematical Software 3(4), 1977
    locator: the whole paper (the farthest point split and the recursion on the two outer sets)
  - paper: doi:10.1145/235815.235821
    title: C. Bradford Barber, David P. Dobkin and Hannu Huhdanpaa, The Quickhull algorithm for convex hulls, ACM Transactions on Mathematical Software 22(4), 1996
    locator: the whole paper (Quickhull in d dimensions with outside sets, and its relation to randomized incremental methods)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 3, the QUICKHULL procedure and its quadratic worst case
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 3, the QuickHull algorithm
---

Quickhull computes the [convex hull](/convex-hull/) of $n$ points in the plane in the style of [quicksort](/quicksort/). The line through the leftmost and rightmost points splits the input in two. On each side it takes the point farthest from the line, which is a hull vertex, throws away the points inside the triangle it forms, and recurses on the two outer groups. Each hull vertex costs at most one pass over the input, so the time is $O(nh)$ for $h$ hull vertices; it is $\Theta(n^2)$ on bad inputs but usually fast in practice, and its $d$-dimensional form is the Qhull program.

## In plain words

Find the leftmost and the rightmost point. Both are corners of the hull. Draw the line between them. It cuts the points into a group below and a group above.

Take the group below. The point that is farthest below the line must also be a corner. Join it to the two ends of the line to make a triangle. Every point inside that triangle cannot be a corner, so drop it. The points that are left fall into two smaller groups, one outside each new side of the triangle. Do the same thing to each group, and stop when a group is empty.

Do the same for the group above the first line. Listed in order, the corners give the hull, going counterclockwise.

When the farthest point splits each group into two balanced halves, this is fast. When it cuts off only one point each time, it is slow.

## The problem

The input is a finite list $P$ of points $p = (x, y)$, with repeats allowed. The output is the list of the vertices of $\operatorname{conv}(P)$ (its [extreme points](/extreme-point/)) in counterclockwise order, starting at the lexicographically smallest point. A point in the middle of a hull edge is not reported. With all points on one line the output is the two end points.

Notation: $n = |P|$, and $h$ is the number of hull vertices. $\mathrm{orient}(p, q, r)$ is the sign of

$$D(p, q, r) = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x),$$

positive for a left (counterclockwise) turn and zero for collinear points; see [orientation test](/orientation-test/). A point $r$ is **right of** $p \to q$ when $D(p, q, r) < 0$, and $|D(p, q, r)|$ is $|q - p|$ times the distance from $r$ to the line $pq$. So for a fixed pair $p, q$, the most negative $D$ marks the farthest point on the right. Points are compared lexicographically. No general position is assumed: ties in distance and collinear points are handled by the rules below.

## The algorithm

```pseudo id=main
QUICKHULL(P)
L1  S ← the distinct points of P
L2  if |S| ≤ 2 then return the points of S in lexicographic order
L3  a ← the lexicographically smallest point of S; b ← the largest
L4  R ← {r ∈ S : orient(a, b, r) < 0}; U ← {r ∈ S : orient(b, a, r) < 0}
L5  return [a] + FIND-HULL(a, b, R) + [b] + FIND-HULL(b, a, U)

FIND-HULL(p, q, X)
L6  if X is empty then return the empty list
L7  c ← the point of X with the smallest D(p, q, c), ties broken by the largest projection onto q − p
L8  X1 ← {r ∈ X : orient(p, c, r) < 0}
L9  X2 ← {r ∈ X : orient(c, q, r) < 0}
L10 return FIND-HULL(p, c, X1) + [c] + FIND-HULL(c, q, X2)
```

- **Line L3.** The lexicographic minimum and maximum are always hull vertices. Using them, and not just the smallest and largest $x$, matters when several points share the extreme $x$.
- **Line L4.** $R$ holds the points strictly below the line from $a$ to $b$ (right of $a \to b$), $U$ those strictly above. Points on the line are dropped: they lie on the segment $ab$, so they are not vertices.
- **Line L7.** The farthest point $c$ is a hull vertex. If several points are equally far, they lie on a line parallel to $pq$, and only the two ends of that segment are vertices; the projection tie-break takes the end nearer to $q$. Taking a middle point would put a non-vertex in the output.
- **Lines L8 and L9.** A point of $X$ that is not right of $p \to c$ and not right of $c \to q$ lies in the triangle $p c q$ and is dropped. No point is right of both lines, so $X_1$ and $X_2$ are disjoint, and neither contains $c$.
- **Line L10.** The vertices right of $p \to c$ come before $c$ on the hull, and those right of $c \to q$ after it.

The implementation runs FIND-HULL with an explicit stack, because the recursion depth can reach $n - 2$.

## Example

Take the ten points $(0,0)$, $(4,0)$, $(2,1)$, $(5,3)$, $(2,2)$, $(3,5)$, $(0,4)$, $(1,2)$, $(2,4)$, $(4,4)$. Line L3 gives $a = (0,0)$ and $b = (5,3)$. Line L4 gives $R = \{(2,1), (4,0)\}$ and $U = \{(0,4), (1,2), (2,2), (2,4), (3,5), (4,4)\}$. The calls with a nonempty set are:

| call | $(p, q)$ | $X$ | $c$ | $D(p, q, c)$ | $X_1$ | $X_2$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | $(0,0), (5,3)$ | (2,1), (4,0) | (4,0) | −12 | empty | empty |
| 2 | $(5,3), (0,0)$ | (0,4), (1,2), (2,2), (2,4), (3,5), (4,4) | (0,4) | −20 | (2,4), (3,5), (4,4) | empty |
| 3 | $(5,3), (0,4)$ | (2,4), (3,5), (4,4) | (3,5) | −8 | empty | empty |

In call 1 the point $(2,1)$ falls inside the triangle $(0,0), (4,0), (5,3)$. In call 2 the triangle $(5,3), (0,0), (0,4)$ removes $(1,2)$ and $(2,2)$. In call 3 the triangle $(5,3), (3,5), (0,4)$ removes $(2,4)$, and $(4,4)$ lies on the side from $(5,3)$ to $(3,5)$, so $D((5,3), (3,5), (4,4)) = 0$ and it is dropped as well. The output is $(0,0), (4,0), (5,3), (3,5), (0,4)$, with $h = 5$. The sets $X$ of the three calls hold $2 + 6 + 3 = 11$ points in total.

## Correctness

**Theorem.** For every finite list $P$, QUICKHULL terminates and returns the vertices of $\operatorname{conv}(P)$, each once, in counterclockwise order from the lexicographically smallest point; for collinear input with at least two distinct points it returns the two end points.

The proof rests on one lemma: if $p$ and $q$ are hull vertices and $X$ is the set of input points right of $p \to q$, then FIND-HULL$(p, q, X)$ returns the hull vertices strictly right of $p \to q$, in counterclockwise order. These are the inner vertices of the hull boundary from $p$ to $q$. The point $c$ of line L7 is a vertex, because it is the only maximizer of a linear function close to the distance to the line. Because $p$ is a vertex, no input point can be right of $p \to c$ without also being right of $p \to q$ (otherwise $p$ would lie in a triangle of three other points). So $X_1$ is exactly the set of input points right of $p \to c$, and in the same way $X_2$ for $c \to q$. Induction on $|X|$ finishes the proof. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

All costs are on the [real RAM](/real-ram/), counting orientation tests.

- **One call.** A call of FIND-HULL on a set $X$ costs $O(|X|)$ besides its two recursive calls: one pass for line L7 and one each for lines L8 and L9.
- **Upper bound $O(nh)$.** Each call with $X \ne \emptyset$ outputs one hull vertex $c$, and each vertex is output once, so there are at most $h - 2$ such calls. Each has $|X| \le n$. Calls with $X = \emptyset$ cost $O(1)$, and there are at most $h$ of them, since the two call trees have $h - 2$ inner nodes with two children each. With lines L1 to L4, the total is $O(n + nh) = O(nh)$. A sharper count is the sum of $|X|$ over all calls: the sets at one level of the recursion tree are disjoint, so the work is $O(n)$ per level and $O(n \cdot \text{depth})$ in total.
- **Worst case $\Theta(n^2)$.** Take the points $(2^i, 4^i)$ for $i = 0, \ldots, n - 1$, which lie on the parabola $y = x^2$, so $h = n$. On the lower chain all $n - 2$ inner points are in $R$, and the farthest point from the chord is always the one next to the right end, so each call removes one point. The sum of $|X|$ is $(n - 1)(n - 2)/2$ and the depth is $n - 2$: for $n = 60$ the sets hold 1711 points in total.
- **Best case $\Theta(n)$.** With $h$ bounded, for example when four points of a square enclose all others, the work is $O(n)$.
- **Typical input.** On random inputs the splits are often balanced and $h$ is small, so the work is near $O(n \log n)$. For $n$ points with integer coordinates drawn uniformly from a square, one run gave a total size of the sets $X$ of 124 for $n = 100$, 1434 for $n = 1000$ and 13657 for $n = 10000$, with recursion depth at most 6. These are observations, not a bound.
- **Space.** $\Theta(n)$. The sets $X$ waiting on the stack at any time belong to disjoint parts of the hull boundary, so they are disjoint and hold at most $n$ points.

The bound $O(nh)$ is output-sensitive but not optimal. In the [algebraic decision tree](/algebraic-decision-tree/) model the planar hull needs $\Omega(n \log n)$ comparisons in the worst case ([lower bound](/convex-hull-lower-bound/)) and $\Omega(n \log h)$ with $h$ vertices ([output-sensitive lower bound](/convex-hull-output-sensitive-lower-bound/)). The [Kirkpatrick-Seidel algorithm](/kirkpatrick-seidel/) reaches $O(n \log h)$ by splitting at the median $x$ instead of at the farthest point.

## Properties

- **Exact with integer input.** Line L7 compares values of $D$ and dot products, both integer polynomials of degree 2 in the coordinates, so no division or square root is needed.
- **Output-sensitive, $O(nh)$.** Like the [Jarvis march](/jarvis-march/), but with each pass over a shrinking set instead of the whole input.
- **Strictly convex output.** Collinear points on hull edges are dropped at lines L4, L8 and L9, and the tie-break of line L7 never picks a middle point.
- **Divide and conquer without a merge.** The hard work is in the split, as in [quicksort](/quicksort/). The two halves are concatenated, not merged, unlike the [divide-and-conquer hull](/divide-and-conquer-convex-hull/).
- **Removes interior points early.** Most points inside the hull are dropped at the first few levels, which is why it is fast on typical data.

## Variants and improvements

- **Start from a quadrilateral.** Use the four points with the smallest and largest $x$ and $y$ and recurse on the four outer regions. This removes more interior points in the first pass (the Akl-Toussaint heuristic).
- **Higher dimensions (Qhull).** Barber, Dobkin and Huhdanpaa start from a simplex, give each facet an outside set of the points above it, and repeatedly add the farthest point of some outside set, as in the [beneath-beyond method](/beneath-beyond/). The new facets take over the outside points of the visible facets. In three dimensions see [3D convex hull](/convex-hull-3d/).
- **Median split.** Splitting $X$ at the median $x$ and finding the bridge over it by [prune and search](/prune-and-search/) gives the [Kirkpatrick-Seidel algorithm](/kirkpatrick-seidel/), $O(n \log h)$ in the worst case.

## When to use it

Use it for large inputs where most points are inside the hull, which is common for measured or random data, and when an $O(nh)$ worst case is acceptable. Its $d$-dimensional form, Qhull, is a standard tool for 3D and higher hulls. If the input may have many hull vertices, such as points on a circle, use [Andrew's monotone chain](/andrew-monotone-chain/) or the [Graham scan](/graham-scan/), which are $O(n \log n)$ for every input. For a guaranteed $O(n \log h)$ use [Chan's algorithm](/chan-algorithm/).

## Pitfalls

- **Ties at line L7.** If several points are equally far from the line, taking an arbitrary one can output a point in the middle of a hull edge. In the test case $(0,0)$, $(4,0)$, $(1,-2)$, $(2,-2)$, $(3,-2)$, $(2,1)$, the three points with $y = -2$ are all farthest below the chord from $(0,0)$ to $(4,0)$; only $(1,-2)$ and $(3,-2)$ are vertices.
- **Points on the lines.** Use strict tests in lines L4, L8 and L9. With $\le$, points on a hull edge, or $p$ and $q$ themselves, enter the next call, and the recursion may not shrink.
- **Extreme $x$ alone.** If $a$ is only "a point with the smallest $x$", it may be in the middle of a vertical hull edge and not a vertex. Use the lexicographic order.
- **Deep recursion.** The depth reaches $n - 2$ on inputs such as the parabola above. A recursive version in a language with a small call stack fails on such input; use an explicit stack.
- **Floating-point distances.** Computing distances as $|D| / |q - p|$ with a square root, or comparing near-equal floating values, can choose a wrong $c$ or misclassify a point near a line. Compare $D$ directly with exact arithmetic.
- **Duplicates.** Remove them in line L1, or a copy of $c$ can survive in $X_1$ or $X_2$ when the tests are not strict.

## Implementations

## History

William Eddy published the method in 1977 in ACM Transactions on Mathematical Software, and A. Bykat gave the same recursion independently in 1978 in Information Processing Letters. The name QUICKHULL, used in the 1985 textbook of Preparata and Shamos, refers to its likeness to quicksort, and that book also points out the quadratic worst case. Barber, Dobkin and Huhdanpaa extended it to any dimension in 1996 and released it as the Qhull program, which many numerical libraries use for hulls, Delaunay triangulations and Voronoi diagrams.

## References
