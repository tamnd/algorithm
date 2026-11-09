---
tag: A5A8FP
kind: definition
slug: convex-polygon
name: Convex polygon
aliases:
- convex polygonal region
- strictly convex polygon
area: geometry/polygons
level: intro
summary: A simple polygon whose interior is a convex set, so every interior angle is at most 180 degrees.
prereqs: [convex-set, orientation-test]
see_also: [simple-polygon, convex-hull, point-in-convex-polygon, minkowski-sum-convex-polygons, rotating-calipers, convex-polygon-intersection, convex-decomposition, star-shaped-polygon]
sources:
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 1 (polygons, simple and convex) and Chapter 2, Section 2.2 (point location in a convex polygon by binary search)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.1 (polygons, simple polygons, convex vertices and reflex vertices) and Chapter 3 (convex hulls)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 1, Section 1.1 (convex sets and the convex hull as a convex polygon) and Chapter 13, Section 13.3 (Minkowski sums of convex polygons)
  - book: "Peter Schorn and Frederick Fisher, Testing the convexity of a polygon, in Paul S. Heckbert (editor), Graphics Gems IV, Academic Press, 1994"
    locator: the whole article (the test by the signs of turns and the count of direction changes)
---

A convex polygon is a [simple polygon](/simple-polygon/) whose closed region is a [convex set](/convex-set/): the segment between any two of its points stays in it. Equivalently, every interior angle is at most $180°$, and the polygon lies on one side of the line through each of its edges. Convex polygons are the polygons for which most questions are easy: a [point location query](/point-in-convex-polygon/) takes $O(\log n)$ time, the [Minkowski sum](/minkowski-sum-convex-polygons/) of two of them takes linear time, and [rotating calipers](/rotating-calipers/) find the diameter and the width in linear time.

## Definition

**Notation.** A polygon is a cyclic sequence of points $v_0, \ldots, v_{n-1}$, $n \ge 3$, indices modulo $n$, with edges $e_i = v_{i+1} - v_i$. A point is $p = (x, y)$, and $\operatorname{orient}(p, q, r)$ is the sign of $(q - p) \times (r - p)$, positive for a counterclockwise turn. The turn at $v_i$ is $t_i = e_{i-1} \times e_i$, and $\operatorname{orient}(v_{i-1}, v_i, v_{i+1}) = \operatorname{sign}(t_i)$.

**Definition.** A simple polygon $Q$ with closed region $R$ (the boundary and the bounded part of its complement, which exists by the [Jordan curve theorem](/jordan-curve-theorem/)) is *convex* if $R$ is a convex set. It is *strictly convex* if, in addition, no three consecutive vertices are collinear, so that every vertex is a corner of $R$.

**Equivalent conditions.** For a simple polygon in counterclockwise order, these are equivalent:

1. $R$ is convex.
2. Every interior angle is at most $\pi$, that is, $t_i \ge 0$ for each $i$.
3. For each edge $v_i v_{i+1}$, every vertex $v_j$ satisfies $\operatorname{orient}(v_i, v_{i+1}, v_j) \ge 0$.
4. $R$ is the intersection of the $n$ closed half-planes to the left of the edge lines.
5. $R$ is the [convex hull](/convex-hull/) of the vertices.

In a strictly convex polygon the inequalities in 2 and 3 are strict for $j \ne i, i+1$, and the vertices are exactly the [extreme points](/extreme-point/) of $R$.

*Proof.* Write $V$ for the vertex set and $\ell_i$, $H_i$ for the line through $v_i v_{i+1}$ and the closed half-plane to its left; for counterclockwise order the region $R$ is to the left of each edge near that edge. (5 $\Rightarrow$ 1) A convex hull is convex. (1 $\Rightarrow$ 5) $R$ is convex and contains $V$, so it contains the hull of $V$. Conversely, if $x \in R$ were outside the hull, a line would separate $x$ from the hull, and the ray from $x$ away from the hull would never meet the boundary, which lies in the hull; so $x$ would be in the unbounded part of the complement, a contradiction. (1 $\Rightarrow$ 3) Let $m$ be the midpoint of the edge $v_i v_{i+1}$. If some $v_j$ were strictly to the right of $\ell_i$, the hull of $v_j$ and a small disk in $R$ just left of $m$ would lie in $R$ and contain a neighborhood of $m$, but $m$ is on the boundary of $R$. (3 $\Rightarrow$ 2) If $t_i < 0$, then $v_{i+1}$ is strictly to the right of $\ell_{i-1}$. (2 $\Rightarrow$ 1) This is the second half of the proof of the test below, which uses only that the polygon is simple with all $t_i \ge 0$. (3 $\Rightarrow$ 4) By 3 and 5, $R \subseteq \bigcap_i H_i$. Let $x \notin R$ and let $y$ be an interior point of $R$; the segment $yx$ leaves $R$ at a boundary point $z$ on some edge line $\ell_j$. As $y$ is interior and $R \subseteq H_j$, $y$ is strictly left of $\ell_j$, so $x$, which lies beyond $z$ on the ray from $y$, is strictly right of $\ell_j$ and not in $\bigcap_i H_i$. (4 $\Rightarrow$ 1) An intersection of half-planes is convex. $\square$

**An exact test for a vertex sequence.** The input is a cyclic sequence with $v_i \ne v_{i+1}$, not known to be simple. Define $\operatorname{half}(e) = 0$ if $e_y > 0$ or ($e_y = 0$ and $e_x > 0$), and $\operatorname{half}(e) = 1$ otherwise; it says whether the direction of $e$ has angle in $[0, \pi)$ or in $[\pi, 2\pi)$. Then the sequence is a convex polygon in counterclockwise order if and only if

- (a) $t_i \ge 0$ for each $i$,
- (b) $e_{i-1} \cdot e_i > 0$ whenever $t_i = 0$ (a straight vertex, not a reversal),
- (c) some $t_i > 0$, and
- (d) exactly one index $i$ has $\operatorname{half}(e_i) = 1$ and $\operatorname{half}(e_{i+1}) = 0$.

For clockwise order, reverse the sequence first. The test reads each vertex a constant number of times, so it takes $\Theta(n)$ time, and with integer coordinates it uses only integer predicates of degree 2.

*Proof.* Let $\theta_i$ be an angle of $e_i$, chosen so that $\delta_i = \theta_{i+1} - \theta_i$ is the turning angle at $v_{i+1}$. Conditions (a) and (b) say exactly that each $\delta_i \in [0, \pi)$. The directions return to the start after $n$ steps, so $\sum_i \delta_i = 2\pi k$ for an integer $k$, and (c) gives $k \ge 1$. *Count of wraps.* An index $i$ has $\operatorname{half}(e_i) = 1$ and $\operatorname{half}(e_{i+1}) = 0$ if and only if the interval $(\theta_i, \theta_{i+1}]$ contains a multiple of $2\pi$: the step is less than $\pi$, so the only way to go from $[\pi, 2\pi)$ to $[0, \pi)$ modulo $2\pi$ is to pass a multiple of $2\pi$, and a step of less than $\pi$ that passes $2\pi m$ starts in $(2\pi m - \pi, 2\pi m)$ and ends in $[2\pi m, 2\pi m + \pi)$. The intervals $(\theta_i, \theta_{i+1}]$ cover $(\theta_0, \theta_0 + 2\pi k]$ without overlap, which holds exactly $k$ multiples of $2\pi$. So (d) says $k = 1$.

*If the conditions hold, the polygon is convex.* Turn the plane so that $x$ is not constant on any edge; this does not change the conditions. As $k = 1$ and the $\theta_i$ never decrease, the edges with $e_x > 0$ (angle in $(-\pi/2, \pi/2)$) form one cyclic block $L$, and the edges with $e_x < 0$ form the other block $U$. Along $L$, $x$ increases from the leftmost vertex $a$ to the rightmost vertex $b$, and the slopes never decrease, so $L$ is the graph of a convex piecewise linear function $f$ on $[a_x, b_x]$. Along $U$, read from left to right, the slopes never increase, so $U$ is the graph of a concave function $g$ on the same interval. Then $g - f$ is concave with $g - f = 0$ at both ends, so $g - f \ge 0$; and if $g - f$ were $0$ at an interior point, concavity would make it $0$ everywhere, so $f = g$ would be both convex and concave, hence linear, and all vertices would be collinear, against (c). So $f < g$ inside the interval, and the polygon is the boundary of $\{(x, y) : a_x \le x \le b_x,\ f(x) \le y \le g(x)\}$, traversed once. This set is convex because $f$ is convex and $g$ is concave, and its boundary is a simple closed curve.

*If the polygon is convex and counterclockwise, the conditions hold.* Each interior angle $\alpha_i$ is at most $\pi$, which gives (a), and $\alpha_i = \pi$ is a straight vertex, which gives (b). The interior angles of a simple polygon sum to $(n - 2)\pi$ (by a [triangulation](/polygon-triangulation/) into $n - 2$ triangles), so the turning angles $\pi - \alpha_i$ sum to $2\pi$. This gives $k = 1$, so (c) and (d). $\blacksquare$

## Examples and non-examples

**Convex, not strictly convex.** $(0,0), (2,0), (4,0), (4,4), (0,4)$ has turns $8, 0, 8, 16, 16$ (as values of $t_i$, starting at $v_0$) and one wrap. It is convex. The vertex $(2,0)$ is straight, so the polygon is not strictly convex, and an algorithm that needs strict convexity, such as [point in convex polygon](/point-in-convex-polygon/), must first drop that vertex.

**A triangle.** Every triangle with nonzero area is strictly convex, in one of the two orders.

**Non-example: a reflex vertex.** The L-shape $(0,0), (4,0), (4,2), (2,2), (2,4), (0,4)$ has turns $16, 8, 4, -4, 4, 8$. The negative turn at $(2,2)$ is a reflex vertex, and the segment from $(4,2)$ to $(2,4)$ leaves the region.

**Non-example: a pentagram.** $(0,3), (2,-3), (-3,1), (3,1), (-2,-3)$ has five turns of one sign ($-24, -22, -24, -24, -22$), so a test that checks only the signs accepts it. After reversal to counterclockwise order, the edge directions wrap twice, so condition (d) rejects it. It is not simple.

**Non-example: a reversal.** $(0,0), (2,0), (1,0), (1,1)$ has $t = 0$ at $(2,0)$ with $e_0 \cdot e_1 = -2 < 0$: the boundary goes back on itself. A test that treats every zero turn as harmless accepts it.

**Non-example: all collinear.** $(0,0), (1,0), (2,0)$ has all turns zero and a reversal at $(2, 0)$. It bounds no region.

## Related definitions

- [Convex set](/convex-set/) and [convex hull](/convex-hull/): a convex polygon is the convex hull of its vertices, and the hull of a finite set of points that are not all collinear is a convex polygon.
- [Simple polygon](/simple-polygon/) and [polygon](/polygon/): the larger classes.
- [Star-shaped polygon](/star-shaped-polygon/): a polygon whose [kernel](/polygon-kernel/) is not empty; a polygon is convex if and only if its kernel is the whole polygon.
- [Monotone polygon](/monotone-polygon/): a convex polygon is monotone in every direction.
- [Point in convex polygon](/point-in-convex-polygon/), [convex polygon intersection](/convex-polygon-intersection/), [Minkowski sum of convex polygons](/minkowski-sum-convex-polygons/), [polygon diameter](/polygon-diameter/) and [polygon width](/polygon-width/): operations that use convexity to run in logarithmic or linear time.
- [Convex decomposition](/convex-decomposition/): the partition of a polygon into convex pieces.

## References
