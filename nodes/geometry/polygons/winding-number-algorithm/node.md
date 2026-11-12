---
tag: CSD45Q
kind: algorithm
slug: winding-number-algorithm
name: Winding number algorithm
aliases:
- winding number test
- Sunday's winding number algorithm
area: geometry/polygons
level: core
summary: Sums the signed crossings of a ray from the query point with the polygon edges; the sum is the winding number, and a nonzero value means inside. O(n) per query.
solves: [point-in-polygon]
model: real-ram
complexity:
  vars: {n: the number of polygon vertices}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 2001
  people: [Kai Hormann, Alexander Agathos, Dan Sunday]
  note: The winding number is a classical notion of topology and complex analysis. Hormann and Agathos (2001) showed that the ray crossing count with signs computes it exactly for arbitrary polygons, and Sunday published the same signed crossing test as code the same year.
prereqs: [point-in-polygon, polygon, orientation-test, crossing-number-algorithm]
see_also: [crossing-number-algorithm, point-in-convex-polygon, shoelace-formula, polygon-orientation, simple-polygon, vatti-clipping, polygon-clipping, jordan-curve-theorem]
sources:
  - paper: doi:10.1016/S0925-7721(01)00012-8
    title: Kai Hormann and Alexander Agathos, The point in polygon problem for arbitrary polygons, Computational Geometry 20(3), 131 to 144 (2001)
    locator: Sections 2 and 3 (the even-odd rule and the winding number, the relation between angle summation and signed crossings, and the handling of special cases)
  - url: https://geomalgorithms.com/a03-_inclusion.html
    title: Dan Sunday, Inclusion of a point in a polygon, geomalgorithms.com (2001)
    locator: the winding number section and the code wn_PnPoly, with the upward and downward edge rule
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 7, Section 7.4, Point in polygon (the ray crossing test and its special cases)
---

The winding number algorithm decides where a point $q$ lies with respect to a closed [polygon](/polygon/) by computing the winding number of the polygon around $q$: the number of times the boundary turns counterclockwise around $q$, minus the number of clockwise turns. It does not add angles. It walks the edges once and counts the edges that cross a horizontal ray from $q$, with $+1$ for an upward edge that passes to the right of $q$ and $-1$ for a downward one. It solves the [point in polygon](/point-in-polygon/) problem in $\Theta(n)$ time with exact [orientation tests](/orientation-test/), and unlike the [crossing number](/crossing-number-algorithm/) it also gives the right answer for self-intersecting polygons under the nonzero rule.

## In plain words

Stand at the query point and watch a person walk once around the polygon. Count how many full turns you make to keep facing the walker: counterclockwise turns count plus one, clockwise turns minus one. That count is the winding number. Outside a simple shape it is zero, and inside it is one.

You do not need to measure angles. Draw a line from your position to the right. Each time the walker crosses that line going up, add one. Each time the walker crosses it going down, subtract one. The total is the same count of turns.

The crossing number test only checks whether the count of crossings is odd. For a star drawn with one stroke, the middle is crossed twice in the same direction, so the even-odd test calls it outside, but the winding number calls it inside.

## The problem

The input is a closed polygon $P$ with vertices $v_0, \ldots, v_{n-1}$ (the edge $v_{n-1} v_0$ closes it) and a query point $q$. The polygon may self-intersect and may have repeated vertices, collinear vertices and horizontal edges. The output is BOUNDARY if $q$ lies on an edge, and otherwise the winding number

$$\operatorname{wind}(P, q) = \frac{1}{2\pi} \sum_{i=0}^{n-1} \varphi_i, \qquad \varphi_i \in (-\pi, \pi) \text{ the signed angle from } v_i - q \text{ to } v_{i+1} - q.$$

The nonzero rule calls $q$ inside when $\operatorname{wind}(P, q) \ne 0$; the even-odd rule calls it inside when $\operatorname{wind}(P, q)$ is odd. For a [simple polygon](/simple-polygon/), $\operatorname{wind}(P, q) = \pm 1$ inside and $0$ outside, so both rules agree.

Notation: $n$ is the number of vertices; $q = (x(q), y(q))$; $\mathrm{orient}(a, b, q)$ is positive when $q$ lies to the left of the directed line $ab$. No general position is assumed.

## The algorithm

```pseudo id=main
WINDING-NUMBER(P, q)                       ▷ P = v[0 .. n − 1], a closed polygon
L1  w ← 0
L2  for i ← 0 to n − 1 do
L3      a ← v[i], b ← v[(i + 1) mod n]
L4      if q lies on the closed segment ab then return BOUNDARY
L5      if y(a) ≤ y(q) < y(b) then if orient(a, b, q) > 0 then w ← w + 1      ▷ upward, q to its left
L6      else if y(b) ≤ y(q) < y(a) then if orient(a, b, q) < 0 then w ← w − 1  ▷ downward, q to its right
L7  return w
```

- **Line L4** makes the boundary case explicit and exact. Many programs skip it; then a point on the boundary gets an arbitrary answer.
- **Lines L5 and L6** use a half-open rule: an edge counts as crossing the ray when one endpoint is at or below the height of $q$ and the other is strictly above. This is the same as moving the ray up by an infinitely small amount. A vertex exactly at the height of $q$ is then above the ray for both of its edges, or below for both, and it is never counted twice or once by mistake. A horizontal edge never counts.
- **The side test** replaces the computation of the crossing point. An upward edge crosses the ray to the right of $q$ exactly when $q$ is to the left of the edge. So the algorithm uses only additions, multiplications and sign tests, and no division.

## Example

Take the pentagram drawn with one stroke, $v_0 = (0,10)$, $v_1 = (-6,-8)$, $v_2 = (10,3)$, $v_3 = (-10,3)$, $v_4 = (6,-8)$, and the query point $q = (0,0)$ in its center.

| $i$ | edge | direction at height 0 | $\mathrm{orient}(a, b, q)$ | change | $w$ |
|---|---|---|---|---|---|
| 0 | (0,10) to (−6,−8) | down | 60 | none, $q$ is to the left | 0 |
| 1 | (−6,−8) to (10,3) | up | 62 | $+1$ | 1 |
| 2 | (10,3) to (−10,3) | does not cross | | | 1 |
| 3 | (−10,3) to (6,−8) | down | 62 | none | 1 |
| 4 | (6,−8) to (0,10) | up | 60 | $+1$ | 2 |

So $\operatorname{wind}(P, q) = 2$. The nonzero rule says inside, and the even-odd rule says outside, because the count is even. For the point $(0, 7)$ in the top spike the result is 1, and for $(12, 0)$ it is 0. The point $(0, 3)$ lies on the edge from $v_2$ to $v_3$, so line L4 returns BOUNDARY.

The point $q = (-12, 3)$ shows the half-open rule. Its ray runs along the horizontal edge $v_2 v_3$ and through the vertices $v_2$ and $v_3$. Edge 1 ends at height 3 and edge 3 starts at height 3, so for both the vertex at height 3 counts as above, and neither edge crosses. Edge 2 is horizontal. Edge 0 counts $-1$ and edge 4 counts $+1$, so $w = 0$, which is right: the point is outside.

## Correctness

**Theorem.** For a closed polygon $P$ and a point $q$, WINDING-NUMBER$(P, q)$ returns BOUNDARY exactly when $q$ lies on $P$, and otherwise returns $\operatorname{wind}(P, q)$.

The proof is in [proofs/correctness.md](proofs/correctness.md). Seen from a point $p$ off the edge, the direction to a point moving along one edge turns by less than $\pi$, so it passes the direction of the ray at most once. Write the angle sum with angles measured in $(0, 2\pi)$ from the ray. Then the terms telescope, and only the jumps of $\pm 2\pi$ at the crossings remain. This gives $\operatorname{wind}(P, p) = U - D$ for a ray that meets no vertex, where $U$ and $D$ count the upward and the downward crossings. The half-open rule of lines L5 and L6 counts exactly the crossings of the ray from a point $q'$ slightly above $q$, and the winding number is the same at $q$ and $q'$ because it is continuous and integer-valued off the polygon.

## Complexity

- **Time.** Each pass of the loop does one boundary test and at most one orientation test, a constant number of exact operations. So the time is $\Theta(n)$ in the worst case on the [real RAM](/real-ram/), and also $\Theta(n)$ when $q$ is not on the boundary, since every edge is read.
- **Space.** $\Theta(1)$ extra: the counter $w$ and the current edge.
- **Optimality.** For one query on an arbitrary polygon, $\Omega(n)$ is necessary: a vertex that is not read could be moved to change the answer. For many queries on the same polygon, preprocessing helps: [planar point location](/planar-point-location/) gives $O(\log n)$ per query, and [point in convex polygon](/point-in-convex-polygon/) gives $O(\log n)$ with no preprocessing beyond the vertex array.
- **Size of the numbers.** On integer coordinates of absolute value at most $M$, each orientation test has absolute value at most $8M^2$, and $|w| \le n/2$.

## Properties

- **Exact.** All tests are signs of degree 2 polynomials in the input, so integers and `fractions.Fraction` give exact answers.
- **Orientation aware.** Reversing the vertex order negates the winding number. For a simple polygon, the sign inside is the [orientation](/polygon-orientation/).
- **Same cost as the crossing number.** For a simple polygon, $\operatorname{wind}(P, q) \bmod 2$ is the crossing parity, so this test gives the same answer as the crossing number test, at the same cost.
- **Defines fill rules.** The nonzero and the even-odd rules of graphics libraries, and of [Vatti clipping](/vatti-clipping/), are both functions of the winding number.

## Variants and improvements

- **Angle summation.** Add the angles $\varphi_i$ with `atan2` and divide by $2\pi$. This is the definition, but it needs floating-point trigonometry and a rounding step, and it is much slower.
- **Quadrant counting.** Track the quadrant of $v_i - q$ around $q$, and add or subtract a quarter turn when it changes. It avoids trigonometry; Hormann and Agathos derive the signed crossing test from this idea.
- **Even-odd from the same loop.** Return $w \bmod 2$, or count all crossings without sign, to get the [crossing number](/crossing-number-algorithm/).
- **Many query points.** Sort the queries by $y$ and sweep, or build a [slab structure](/slab-method-point-location/) or a [trapezoidal map](/trapezoidal-map/) of the edges, to answer each query in $O(\log n)$ time.
- **Area of the winding number.** The [shoelace formula](/shoelace-formula/) integrates the winding number over the plane, so it is the area version of this test.

## When to use it

Use the winding number when the polygon may self-intersect and the nonzero rule is wanted, as in font outlines, vector graphics paths and the inputs of [polygon clipping](/polygon-clipping/). Use it also when you need the orientation of the region around $q$, not only inside or outside. For a simple polygon it costs the same as the crossing number, so many libraries use it there too. For a [convex polygon](/convex-polygon/) and many queries, binary search in $O(\log n)$ is faster.

## Pitfalls

- **Counting a vertex on the ray twice.** With closed tests $y(a) \le y(q) \le y(b)$ in lines L5 and L6, a vertex at the height of $q$ is counted by both of its edges, and the count is off by one when the boundary passes through the ray there. The half-open test $y(a) \le y(q) < y(b)$ fixes this.
- **Counting horizontal edges.** A horizontal edge at the height of $q$ is part of the ray. With the half-open rule it meets neither condition. A test that counts it when $q$ is to its left gives a wrong count.
- **Using the wrong side test.** Testing $\mathrm{orient}(a, b, q) > 0$ for downward edges in line L6, instead of $< 0$, counts crossings to the left of $q$ for those edges, and the sum is meaningless. An upward edge to the right of $q$ has $q$ on its left; a downward edge to the right of $q$ has $q$ on its right.
- **Ignoring the boundary.** Without line L4, a point on an edge gets the value for a point just above it or just below it, depending on the edge. When the boundary matters, test it explicitly.
- **Floating-point crossing points.** Computing the $x$ of the crossing with a division, then comparing it with $x(q)$, can give the wrong side for a point very near an edge. The orientation test with exact arithmetic has no such error.
- **Even-odd and nonzero confusion.** For a self-intersecting polygon the two rules differ, as in the center of the pentagram. Choose the rule on purpose; SVG, PostScript and font formats name the rule they use.

## Implementations

The Python version returns `None` for a point on the boundary and the winding number otherwise, and a wrapper applies the nonzero or the even-odd rule. The tests check the pentagram example, rays through vertices and along horizontal edges, boundary points with fractional coordinates, polygons with zero, one and two vertices, a square traced twice, and about 3000 random queries on random self-intersecting polygons on small grids against two independent oracles: the floating-point angle sum, and an exact signed count along a downward vertical ray. On random simple polygons the winding number is also compared with the crossing parity.

## History

The winding number of a closed curve around a point is a classical notion of topology and complex analysis. The ray crossing test for simple polygons goes back at least to Shimrat's Algorithm 112 of 1962; see the [crossing number algorithm](/crossing-number-algorithm/). Hormann and Agathos showed in 2001 that the winding number of an arbitrary polygon can be computed by the same kind of ray test, with signs, and they treated the special cases of vertices and edges on the ray. Sunday published the upward and downward edge rule as code in the same year.

## References
