---
tag: JTX14G
kind: algorithm
slug: jarvis-march
name: Jarvis march
aliases:
- gift wrapping
- Jarvis's march
- gift wrapping algorithm
- Chand-Kapur algorithm
area: geometry/convex-hulls
level: core
summary: Wraps the hull one vertex at a time, costing O(nh) for h hull vertices.
solves: [convex-hull-problem]
model: real-ram
complexity:
  vars: {n: the number of input points, h: the number of hull vertices}
  time: {best: Θ(n), worst: Θ(n h)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false, output-sensitive: true}
history:
  year: 1973
  people: [R. A. Jarvis, Donald R. Chand, Sham S. Kapur]
  note: Chand and Kapur described gift wrapping for hulls in any dimension in 1970, and Jarvis published the planar version in Information Processing Letters in 1973.
prereqs: [convex-hull-problem, orientation-test]
see_also: [graham-scan, andrew-monotone-chain, chan-algorithm, quickhull, kirkpatrick-seidel, convex-hull-3d, convex-hull-output-sensitive-lower-bound, facet]
sources:
  - paper: doi:10.1016/0020-0190(73)90020-3
    title: R. A. Jarvis, On the identification of the convex hull of a finite set of points in the plane, Information Processing Letters 2(1), 1973
    locator: the whole paper (the planar wrapping step and its O(nh) cost)
  - paper: doi:10.1145/321556.321564
    title: Donald R. Chand and Sham S. Kapur, An algorithm for convex polytopes, Journal of the ACM 17(1), 1970
    locator: the whole paper (gift wrapping in d dimensions, pivoting around ridges)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 3, Section 3.3.2 (the Jarvis march) and Section 3.4.1 (gift wrapping in higher dimensions)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 3, the gift wrapping algorithm in the plane, and Chapter 4, gift wrapping in three dimensions
---

The Jarvis march, or gift wrapping, computes the [convex hull](/convex-hull/) of $n$ points in the plane by walking around it. From a point known to be on the hull, it scans all points and picks the one that leaves every other point on its left; that point is the next hull vertex. It needs $n$ orientation tests per hull vertex, so it runs in $\Theta(nh)$ time for $h$ hull vertices. This is faster than sorting when $h$ is small, and it is the base step of [Chan's algorithm](/chan-algorithm/). The same pivoting idea, around edges instead of points, wraps hulls in three and more dimensions.

## In plain words

Think of the points as nails in a board. Tie a string to the leftmost nail and pull it tight downward. Now swing the string counterclockwise around the nail until it hits another nail. That nail is the next corner of the hull. Swing again around the new nail, and keep going until the string comes back to the start.

To find the next nail, the algorithm looks at every point and keeps the one that is farthest clockwise, so that no other point is to its right. If several points are in the same direction, it takes the farthest one, which skips the points in the middle of an edge.

Each corner costs one pass over all the points. With few corners, this is quick. With every point on the hull, it is slow: the number of passes equals the number of points.

## The problem

The input is a finite list $P$ of points $p = (x, y)$, with repeats allowed. The output is the list of the vertices of $\operatorname{conv}(P)$ in counterclockwise order, starting at the lexicographically smallest point. A point in the middle of a hull edge is not reported. With all points on one line the output is the two end points.

Notation: $n = |P|$, and $h$ is the number of hull vertices, the output size. $\mathrm{orient}(p, q, r)$ is the sign of

$$(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x),$$

positive for a left (counterclockwise) turn and zero for collinear points; see [orientation test](/orientation-test/). Points are compared lexicographically: $p < q$ when $p_x < q_x$, or $p_x = q_x$ and $p_y < q_y$. No general position is assumed in the plane. The three-dimensional version below assumes it.

## The algorithm

```pseudo id=main
JARVIS-MARCH(P)
L1  S ← the distinct points of P
L2  if |S| ≤ 1 then return S
L3  start ← the lexicographically smallest point of S
L4  hull ← empty list; p ← start
L5  repeat
L6      append p to hull
L7      q ← any point of S other than p
L8      for each r in S with r ≠ p do
L9          if orient(p, q, r) < 0, or orient(p, q, r) = 0 and |r − p| > |q − p| then q ← r
L10     p ← q
L11 until p = start
L12 return hull
```

- **Line L3.** The lexicographically smallest point is always a hull vertex, so the walk starts on the hull.
- **Line L9** is the wrapping step. If $r$ is to the right of the line from $p$ to $q$, the candidate $q$ cannot be the next vertex, and $r$ replaces it. If $r$ is on the line through $p$ and $q$, on the same side of $p$ as $q$, the farther of the two wins. Distances are compared as squared distances, so the test stays exact on integers.
- **Lines L10 and L11.** The chosen point becomes the new $p$, and the walk stops when it comes back to the start.

## Example

Take the ten points $(0,0)$, $(4,0)$, $(2,1)$, $(5,3)$, $(2,2)$, $(3,5)$, $(0,4)$, $(1,2)$, $(2,4)$, $(4,4)$, scanned in lexicographic order at line L8. The column "candidates" lists the initial $q$ of line L7 and then each point that replaced it at line L9.

| step | $p$ | candidates | next vertex | points on the edge line |
| --- | --- | --- | --- | --- |
| 1 | (0,0) | (0,4), (1,2), (2,1), (4,0) | (4,0) | none |
| 2 | (4,0) | (0,0), (0,4), (2,4), (3,5), (4,4), (5,3) | (5,3) | none |
| 3 | (5,3) | (0,0), (0,4), (2,4), (3,5) | (3,5) | (4,4), nearer, not taken |
| 4 | (3,5) | (0,0), (0,4) | (0,4) | none |
| 5 | (0,4) | (0,0) | (0,0) | none |

The walk returns to $(0,0)$ after $h = 5$ steps and outputs $(0,0), (4,0), (5,3), (3,5), (0,4)$. Each step made $n - 1 = 9$ orientation tests, 45 in total. In step 3 the point $(4,4)$ is collinear with $(5,3)$ and $(3,5)$, and the distance rule of line L9 keeps the farther point $(3,5)$.

## Correctness

**Theorem.** For every finite list $P$ with at least two distinct points, JARVIS-MARCH stops after exactly $h$ iterations and returns the $h$ vertices of $\operatorname{conv}(P)$, each once, in counterclockwise order from the lexicographically smallest point.

The key fact is the scan of line L8. When $p$ is a hull vertex, all other points lie in an open half-plane through $p$, so the orientation test compares their angles around $p$ consistently, and line L9 keeps the minimum of a total order: the smallest angle, and the farthest point on that ray. That point $q$ leaves every point on or to the left of the line from $p$ to $q$, with the collinear points on the segment, which makes $pq$ the hull edge after $p$. Induction over the steps follows the hull counterclockwise. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Per step.** Lines L7 to L9 make $|S| - 1$ orientation tests and at most as many distance comparisons: $\Theta(n)$ time.
- **Steps.** The loop of line L5 runs exactly $h$ times, so the total is $\Theta(nh)$ on the [real RAM](/real-ram/), for every input. Line L1 adds $O(n \log n)$ by sorting, or $O(n)$ expected with hashing.
- **Range.** The best case is $h = 3$ (or $h = 2$ for collinear input), $\Theta(n)$ time. The worst case is $h = n$, for example points on a circle or on the parabola $y = x^2$, $\Theta(n^2)$ time: for $n = 1000$ points $(i, i^2)$ the march makes about $10^6$ orientation tests.
- **Space.** $\Theta(n)$ for the distinct points and the output.

The march is **output-sensitive**, but not optimal: the lower bound for the planar hull with $h$ vertices is $\Omega(n \log h)$ in the [algebraic decision tree](/algebraic-decision-tree/) model ([output-sensitive lower bound](/convex-hull-output-sensitive-lower-bound/)), and [Chan's algorithm](/chan-algorithm/) and the [Kirkpatrick-Seidel algorithm](/kirkpatrick-seidel/) reach it. It beats an $O(n \log n)$ sort when $h$ is smaller than about $\log n$.

## Properties

- **Exact with integer input.** The predicates are the orientation test and the comparison of squared distances.
- **Output-sensitive.** The cost grows with $h$, not with the size of the input that is far inside.
- **No sort, no extra structure.** It reads the input repeatedly and keeps only the current point and the output, so it works in $O(1)$ extra space beyond the output if the input has no duplicates and can be read many times.
- **Strictly convex output.** The distance rule skips collinear points on hull edges.

## Variants and improvements

- **Gift wrapping in three dimensions.** Chand and Kapur pivot a plane around an edge instead of a line around a point. Assume general position: no four points coplanar. A facet $(a, b, c)$ is stored counterclockwise as seen from outside, so every other point $d$ has $\det(b - a, c - a, d - a) < 0$. To find the facet across the edge from $a$ to $b$, start with any third point $w$ and replace $w$ by $r$ whenever $\det(a - b, w - b, r - b) > 0$; the result gives the facet $(b, a, w)$. A breadth-first search over the edges, started from one facet, finds all facets. A first facet comes from one planar wrapping step in the projection to the $(x, y)$ plane (which gives a hull edge if no three projected points are collinear) and one pivot around that edge. Each facet costs $O(n)$ time, and a simplicial 3-polytope with $h$ vertices has $2h - 4$ facets ([facet](/facet/)), so the total is $O(nh)$. The implementation on this page has this version as `gift_wrapping_3d`, tested against the facet check of all triples and Euler's relation.
- **Higher dimensions.** The same pivot around ridges works in $\mathbb{R}^d$, in time proportional to $n$ times the number of facets for fixed $d$. The number of facets can be $\Theta(n^{\lfloor d/2 \rfloor})$ by the Upper Bound Theorem. See [3D convex hull](/convex-hull-3d/) and the [beneath-beyond method](/beneath-beyond/).
- **Chan's algorithm.** [Chan's algorithm](/chan-algorithm/) replaces the linear scan of line L8 by tangent queries to $\lceil n/m \rceil$ precomputed hulls of groups of size $m$, which gives $O(n \log h)$.
- **Upper hull only.** Starting at the leftmost point and stopping at the rightmost point gives the [upper or lower hull](/upper-and-lower-hull/).

## When to use it

Use it when the hull is expected to have very few vertices, when the input is too large to sort or store but can be read many times, or as the short reference implementation. For general input use [Andrew's monotone chain](/andrew-monotone-chain/), whose $O(n \log n)$ time does not degrade when all points are on the hull. For a guaranteed $O(n \log h)$ use [Chan's algorithm](/chan-algorithm/). In three dimensions gift wrapping is simple but slow; the randomized incremental method of [3D convex hull](/convex-hull-3d/) takes $O(n \log n)$ expected time.

## Pitfalls

- **Ignoring collinear candidates in line L9.** With only the test `orient(p, q, r) < 0`, a nearer collinear point can be chosen as the next vertex. The output then contains points in the middle of edges, or misses vertices, depending on the scan order. For three points $a < m < b$ on a line, scanned in that order, it returns $a, m$ instead of $a, b$. Keep the distance rule, or decide on purpose to keep collinear points and then take the nearest one.
- **Starting at a point that is not a hull vertex.** Line L3 must pick an extreme point, such as the lexicographic minimum. Starting at, say, the point with the smallest $x$ alone fails when several points share that $x$ and the start is in the middle of the vertical edge.
- **Duplicates.** If $S$ has two copies of $p$, line L9 sees $\mathrm{orient}(p, p, r) = 0$ and can step from $p$ to its copy. Remove duplicates in line L1.
- **Stopping on a step count.** Stop when the walk returns to the start (line L11), not after a fixed number of steps; with floating-point predicates the walk may not close, so use exact predicates.

## Implementations

## History

Donald Chand and Sham Kapur published gift wrapping for convex polytopes in any dimension in the Journal of the ACM in 1970, with a plane pivoting around ridges of the hull. R. A. Jarvis published the planar version in 1973, a year after Graham's scan, and pointed out that its cost depends on the number of hull vertices. It is the first output-sensitive hull algorithm. The planar output-sensitive optimum $O(n \log h)$ came in 1986 with Kirkpatrick and Seidel, and the simpler method of Chan in 1996 uses the Jarvis step on groups of points.

## References
