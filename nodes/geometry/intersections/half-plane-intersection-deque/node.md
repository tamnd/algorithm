---
tag: EFZJWK
kind: algorithm
slug: half-plane-intersection-deque
name: Half-plane intersection by sorting and deque
aliases: [sort-and-deque-half-plane-intersection, angle sort half-plane intersection]
area: geometry/intersections
level: core
summary: Sort the half-planes by the angle of their boundary lines, then build the convex intersection with a deque that drops half-planes from both ends, in O(n log n) time.
solves: [half-plane-intersection]
model: real-ram
complexity:
  vars: {n: the number of half-planes}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1976
  people: [Michael Ian Shamos, Dan Hoey]
  note: The O(n log n) bound for half-plane intersection goes back to the divide-and-conquer method of Shamos and Hoey; the single sort followed by a linear deque pass became the usual form in programming contests in the 2000s.
prereqs: [half-plane-intersection, angular-sort, deque, cross-product, line-line-intersection]
see_also: [convex-polygon-intersection, polygon-kernel, convex-hull-trick, andrew-monotone-chain, seidel-linear-programming, linear-programming-problem, minkowski-sum-convex-polygons, convex-polygon]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 4, Section 4.2, Half-plane intersection (the O(n log n) divide-and-conquer method and the linear merge of two convex regions)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 7, Section 7.2.4, Intersection of half-planes (the Ω(n log n) lower bound and the reduction to convex hulls by duality)
  - paper: doi:10.1109/SFCS.1976.16
    title: Michael Ian Shamos and Dan Hoey, Geometric intersection problems, 17th Annual Symposium on Foundations of Computer Science (FOCS 1976), 208-215
    locator: the O(n log n) intersection of n half-planes
  - paper: doi:10.1145/322139.322142
    title: D. T. Lee and Franco P. Preparata, An optimal algorithm for finding the kernel of a polygon, Journal of the ACM 26(3), 1979, 415-421
    locator: the kernel as an intersection of half-planes, computed in linear time when the half-planes come in polygon order
---

The sort-and-deque method computes the intersection of $n$ closed half-planes in the plane in $\Theta(n \log n)$ time. It sorts the half-planes by the angle of their boundary lines, then makes one pass with a [deque](/deque/). Each new half-plane can cut off vertices at the back of the current chain and, after the chain turns around, at its front. After the sort, the pass takes only $O(n)$ time, and with exact [cross products](/cross-product/) the result is exact.

## In plain words

Each half-plane is "everything to the left of a directed line". Sort the lines by their direction, as a compass needle turns. Walk through them in this order and keep a list of the lines that still form the edges of the region.

When a new line comes, look at the last corner of the list. If the corner is not strictly on the good side of the new line, the last line in the list is no longer an edge, so remove it, and look at the corner before it. When the directions have turned far enough, the new line can also cut the first corner, so check the front of the list in the same way. Each line enters and leaves the list at most once, so the walk is fast. At the end, clean up the two ends, and the corners of the list are the answer.

## The problem

The input is a list of $n$ half-planes. A half-plane $h$ is given by a point $p_h$ and a non-zero direction $d_h$, and it is the closed set of points $x$ with $\operatorname{cross}(d_h, x - p_h) \ge 0$, the points on or to the left of the directed line. The output is the intersection $R$ of all half-planes, as its list of vertices in counterclockwise order, or the empty list if $R$ is empty or has zero area (a point or a segment). See [half-plane intersection](/half-plane-intersection/) for the problem and its variants.

Notation: $\operatorname{cross}(u, v) = u_x v_y - u_y v_x$. The angle of $h$ is the angle of $d_h$ in $[0, 2\pi)$. $\operatorname{meet}(g, h)$ is the common point of the two boundary lines. A point $x$ is strictly inside $h$ if $\operatorname{cross}(d_h, x - p_h) > 0$. The method assumes that $R$ is bounded. If it may not be, add the four sides of a large box first. Input coordinates are integers or rational numbers, and every vertex is an exact `Fraction`.

## The algorithm

```pseudo id=main
HALF-PLANE-INTERSECTION(H)
L1  sort H by angle; for each angle keep only the half-plane whose line is furthest to the left
L2  Q ← empty deque
L3  for each h in H in order do
L4      while |Q| ≥ 2 and meet(Q[-2], Q[-1]) is not strictly inside h do pop the back of Q
L5      while |Q| ≥ 2 and meet(Q[0], Q[1]) is not strictly inside h do pop the front of Q
L6      if Q is not empty and cross(d of Q[-1], d of h) ≤ 0 then return the empty list
L7      push h at the back of Q
L8  repeat: if |Q| ≥ 3 and meet(Q[-2], Q[-1]) is not strictly inside Q[0] then pop the back of Q
L9          else if |Q| ≥ 3 and meet(Q[0], Q[1]) is not strictly inside Q[-1] then pop the front of Q, else stop
L10 if |Q| < 3 or cross(d of Q[-1], d of Q[0]) ≤ 0 then return the empty list
L11 return the points meet(Q[i], Q[i + 1]) for i = 0, ..., |Q| - 1, indices modulo |Q|
```

The angle sort of line L1 is exact. It puts the directions in the upper half first, then the lower half, and orders two directions in the same half by the sign of their cross product, as in an [angular sort](/angular-sort/). Line L6 stops when two neighbors in the deque turn by $\pi$ or more: then the half-planes so far leave no bounded region with an interior. Lines L8 and L9 repeat until neither end can be cut by the other end. Because the test "strictly inside" is strict, a vertex that only touches a line is removed, and the output has no repeated and no collinear vertices.

## Example

Take eight half-planes, named by their inequalities: $a: y \ge 0$, $a': y \ge 1$, $f: y \ge x - 2$, $b: x \le 4$, $c: x + y \le 7$, $d: y \le 4$, $e: x \ge 0$ and $g: x + y \ge 5$. Their directions have angles $0, 0, \pi/4, \pi/2, 3\pi/4, \pi, 3\pi/2, 7\pi/4$. Line L1 keeps $a'$, the stronger of $a$ and $a'$.

| step | new half-plane | pops | deque after the step |
| --- | --- | --- | --- |
| 1 | $a'$ | none | $a'$ |
| 2 | $f$ | none | $a', f$ |
| 3 | $b$ | none, $\operatorname{meet}(a', f) = (3, 1)$ is inside $b$ | $a', f, b$ |
| 4 | $c$ | none, $(4, 2)$ is inside $c$ | $a', f, b, c$ |
| 5 | $d$ | none, $(4, 3)$ is inside $d$ | $a', f, b, c, d$ |
| 6 | $e$ | none, $(3, 4)$ is inside $e$ | $a', f, b, c, d, e$ |
| 7 | $g$ | back: $e$, since $\operatorname{meet}(d, e) = (0, 4)$ has $x + y = 4 < 5$; front: $a'$, since $(3, 1)$ has $x + y = 4$ | $f, b, c, d, g$ |
| end | | none, $\operatorname{meet}(d, g) = (1, 4)$ is inside $f$ and $(4, 2)$ is inside $g$ | $f, b, c, d, g$ |

The output is $(4, 2), (4, 3), (3, 4), (1, 4), (7/2, 3/2)$: the meets of $f$ and $b$, $b$ and $c$, $c$ and $d$, $d$ and $g$, and $g$ and $f$. Step 7 shows both kinds of pops. The new half-plane $g$ cuts the corner $(0, 4)$ at the back and the corner $(3, 1)$ at the front, because its direction has turned by more than $\pi$ from the front.

## Correctness

The deque keeps three facts while the loop runs: its half-planes are in angle order with each turn between neighbors less than $\pi$; the meet of two neighbors is strictly inside the next one; and its intersection equals the intersection of the half-planes seen so far. A pop at the back removes a half-plane $e$ between $g$ and $h$ only when $g \cap h \subseteq e$, and a pop at the front needs $h$ to have turned more than $\pi$ past $e$, so again $e$ contains the rest. If $R$ has an interior, no half-plane that carries an edge of $R$ is ever popped, line L6 never stops the run, and at the end the deque is exactly the list of edge half-planes of $R$; their consecutive meets are the vertices. If $R$ has no interior, a non-empty output would be a polygon with an interior inside $R$, which is impossible. The full proof is in the correctness proof below.

## Complexity

- **Sort.** Line L1 takes $O(n \log n)$ time with exact comparisons.
- **Deque pass.** Each half-plane is pushed once and popped at most once, so lines L3 to L9 take $O(n)$ time in total, amortized over the pass.
- **Total.** $\Theta(n \log n)$ time and $\Theta(n)$ space on the [real RAM](/real-ram/). The sort is the only super-linear step, and it is needed: [half-plane intersection](/half-plane-intersection/) has an $\Omega(n \log n)$ lower bound in the algebraic decision tree model, by reduction from sorting through duality with the convex hull.
- **Exact arithmetic.** With integer input of $b$ digits, each test is a sign of a polynomial of low degree in the input, so the vertices have $O(b)$ digits.

## Properties

- **Exact.** All tests are signs of cross products of input values and of `Fraction` meets. There is no tolerance.
- **Robust to degeneracies.** Parallel lines with the same direction, lines through a common point and vertices that only touch a line are all handled by line L1 and by the strict tests.
- **Linear after sorting.** If the half-planes already come in angle order, for example the edges of a convex polygon, the pass is linear.
- **Output.** A convex polygon with no repeated and no collinear vertices, in counterclockwise order.

## Variants and improvements

- **Divide and conquer.** Split the half-planes into two halves, solve each one, and intersect the two convex results in linear time with [convex polygon intersection](/convex-polygon-intersection/). This is the method of de Berg et al. and has the same bound.
- **Duality.** A half-plane $y \le a x + b$ is a point $(a, -b)$ under point-line duality, and the boundary of an upper or lower envelope of lines is a [convex hull](/convex-hull/) of the dual points. So the upper and lower chains can be found with [Andrew's monotone chain](/andrew-monotone-chain/) and then cut against each other.
- **Feasibility only.** To test whether the intersection is empty, or to find the lowest point, use [Seidel's linear programming](/seidel-linear-programming/), in expected $O(n)$ time.
- **Polygon kernel.** The [kernel of a polygon](/polygon-kernel/) is the intersection of the half-planes of its edges. The edges come in boundary order, and Lee and Preparata find the kernel in $O(n)$ time without sorting.
- **Unbounded regions.** Without the bounding box, the method can be extended to report an unbounded region as a chain with two rays, at the cost of more cases.

## When to use it

Use it to intersect many half-planes when you need the whole region: the kernel of a polygon, the feasible region of a small linear program in two variables, the cell of a point in a Voronoi diagram computed from its bisectors, or the region of points that see a set of walls. It is short, linear after the sort, and exact with rational arithmetic. If you only need one optimal point, linear programming is simpler. If both inputs are already convex polygons, use [convex polygon intersection](/convex-polygon-intersection/) in linear time.

## Pitfalls

- **Tests that are not strict.** If lines L4, L5, L8 and L9 keep a vertex that lies exactly on the new line, the output has repeated or collinear vertices, and a region of zero area comes out as a flat polygon instead of the empty list.
- **No final cleanup.** Without the repeated tests of lines L8 and L9, the last half-planes can leave useless half-planes at the front, or the reverse, and line L11 returns extra vertices that are outside $R$.
- **Parallel lines with the same direction.** Line L1 must keep only the strongest of them. Two parallel neighbors in the deque have no meet, and line L4 then fails.
- **A float tolerance.** With floating-point numbers and a tolerance $\varepsilon$ in the tests of lines L4, L5, L8 and L9, nearly parallel lines give meets far away and wrong pops. Use exact integers or rationals, or [exact predicates](/shewchuk-expansion-sum/).
- **Unbounded input.** If $R$ is unbounded, the result of the pass is not defined; line L6 or line L10 can return the empty list for a region that is not empty. Add the four sides of a box that contains every vertex of interest.

## Implementations

## History

Shamos and Hoey (1976) showed that $n$ half-planes can be intersected in $O(n \log n)$ time, by divide and conquer with a linear-time merge of two convex polygons, and that this is optimal. Preparata and Shamos (1985) give the method and its lower bound by reduction from sorting. Lee and Preparata (1979) used half-plane intersection in boundary order to find the kernel of a polygon in linear time. The form with a single angle sort and a deque, which drops half-planes at both ends, became the standard method of programming contests in the 2000s; it is the incremental form of the same idea.

## References
