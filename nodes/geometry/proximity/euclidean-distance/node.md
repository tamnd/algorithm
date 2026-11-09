---
tag: SXWVA7
kind: definition
slug: euclidean-distance
name: Euclidean distance and squared distance
aliases:
- Euclidean metric
- L2 distance
- squared Euclidean distance
area: geometry/proximity
level: intro
summary: The straight-line distance between two points as the root of summed squared coordinate differences, with the squared version used to avoid roots.
prereqs: [point-and-vector, dot-product]
see_also: [proximity-problems, closest-pair-of-points, point-to-line-distance, point-to-segment-distance, metric-space, floating-point-arithmetic, orientation-test, hausdorff-distance]
sources:
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 5, Proximity, fundamental algorithms (the Euclidean metric as the distance of the proximity problems, and the comparison of distances without roots)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 1, Section 1.2, Degeneracies and Robustness (rounding errors in geometric tests and exact arithmetic)
  - paper: doi:10.1007/PL00009321
    title: Jonathan Richard Shewchuk, Adaptive precision floating-point arithmetic and fast robust geometric predicates, Discrete and Computational Geometry 18(3), 1997
    locator: Section 1 (why rounding makes geometric tests fail) and Section 4 (exact predicates as signs of polynomials)
---

The Euclidean distance between two points of $\mathbb{R}^d$ is the length of the straight segment between them: the square root of the sum of the squared coordinate differences. Its square, the *squared distance*, is a polynomial in the coordinates, so it is exact for integer or rational input, and it orders pairs of points in the same way as the distance. Algorithms for [proximity problems](/proximity-problems/) such as the [closest pair](/closest-pair-of-points/) compare squared distances and never take a root inside a comparison.

## Definition

Let $d \ge 1$ and let $p = (p_1, \ldots, p_d)$ and $q = (q_1, \ldots, q_d)$ be points of $\mathbb{R}^d$. In the plane we write $p = (x, y)$. The **squared Euclidean distance** is

$$\|p - q\|^2 = \sum_{i=1}^{d} (p_i - q_i)^2 = (p - q) \cdot (p - q),$$

the [dot product](/dot-product/) of the difference vector with itself. The **Euclidean distance** is its non-negative square root,

$$\|p - q\| = \sqrt{\sum_{i=1}^{d} (p_i - q_i)^2}.$$

We also write $|pq|$ for $\|p - q\|$. On this page and on the other pages of this area, $P$ is the input point set, $n = |P|$ and $d$ is the dimension.

**The metric axioms.** For all $p, q, r \in \mathbb{R}^d$:

1. $\|p - q\| \ge 0$, with equality if and only if $p = q$.
2. $\|p - q\| = \|q - p\|$.
3. $\|p - r\| \le \|p - q\| + \|q - r\|$ (the triangle inequality), with equality if and only if $q$ lies on the closed segment $pr$.

So $(\mathbb{R}^d, \|\cdot\|)$ is a [metric space](/metric-space/). Axioms 1 and 2 follow from the formula. For axiom 3, put $u = p - q$ and $w = q - r$. Then $\|u + w\|^2 = \|u\|^2 + 2\, u \cdot w + \|w\|^2 \le \|u\|^2 + 2 \|u\| \|w\| + \|w\|^2 = (\|u\| + \|w\|)^2$ by the Cauchy-Schwarz inequality $u \cdot w \le \|u\| \|w\|$. Equality holds if and only if $u \cdot w = \|u\| \|w\|$, that is, one of $u, w$ is a non-negative multiple of the other, which is the statement that $q$ is on the segment $pr$.

**Comparison by squares.** The map $t \mapsto t^2$ is strictly increasing on $[0, \infty)$. So for all points $p, q, r, s$:

$$\|p - q\| < \|r - s\| \iff \|p - q\|^2 < \|r - s\|^2,$$

and the same holds for $=$ and $>$. Each comparison of two distances is therefore the sign of a polynomial of degree 2 in the coordinates. With integer coordinates it needs only integer additions and multiplications. With coordinates of absolute value at most $M$, each squared difference is at most $(2M)^2$, so the squared distance is at most $4 d M^2$. In the plane with $M = 2^{31}$ this is $2^{65}$, which overflows a signed 64-bit integer. Python integers and `fractions.Fraction` have no such limit.

**The squared distance is not a metric.** It satisfies axioms 1 and 2 but not the triangle inequality, as the examples show. Use it to compare single distances, not to add them.

## Examples and non-examples

- **A 3, 4, 5 triangle.** For $p = (1, 2)$ and $q = (4, 6)$, $\|p - q\|^2 = 3^2 + 4^2 = 25$ and $\|p - q\| = 5$.
- **Three dimensions.** For $p = (1, 2, 3)$ and $q = (4, 6, 15)$, $\|p - q\|^2 = 9 + 16 + 144 = 169$ and $\|p - q\| = 13$.
- **A wrong answer from a float root.** Take $A = (0, 0)$, $B = (10^8, 1)$ and $C = (-10^8, 0)$. Then $|AB|^2 = 10^{16} + 1$ and $|AC|^2 = 10^{16}$, so $C$ is strictly nearer to $A$ than $B$ is. In IEEE double precision, `math.sqrt(10**16 + 1)` and `math.sqrt(10**16)` both return `100000000.0`, and `math.hypot` gives the same two values. A closest pair loop that tests `if dist < best` and meets the pair $(A, B)$ first keeps $(A, B)$, which is the wrong answer. The integer test $10^{16} < 10^{16} + 1$ is exact and keeps $(A, C)$.
- **A non-example: the squared distance fails the triangle inequality.** On a line take $p = 0$, $q = 1$ and $r = 2$. Then $\|p - r\|^2 = 4$, but $\|p - q\|^2 + \|q - r\|^2 = 2$.
- **A non-example: a sum of distances cannot be compared by one squaring.** To decide whether $\sqrt{2} + \sqrt{3} < \sqrt{10}$, square once: $5 + 2\sqrt{6}$ against $10$, that is, $2\sqrt{6}$ against $5$. Both sides are non-negative, so square again: $24 < 25$. Hence $\sqrt{2} + \sqrt{3} < \sqrt{10}$ (the values are about $3.1463$ and $3.1623$). Each new root in a sum needs another squaring and a sign case, and the degree doubles each time. This is why path lengths, as in a [geometric spanner](/geometric-spanner/) or a Euclidean shortest path, are much harder to compare exactly than single distances.
- **A non-example: the Manhattan distance.** $|p_1 - q_1| + |p_2 - q_2|$ is also a metric, but it is not the Euclidean distance: for $p = (1, 2)$ and $q = (4, 6)$ it is $7$, not $5$. Algorithms built on circles, such as the [Delaunay triangulation](/delaunay-triangulation/), change when the metric changes.

## Related definitions

- [Metric space](/metric-space/): a set with a distance that satisfies the three axioms above.
- [Dot product](/dot-product/) and [cross product](/cross-product/): the squared distance is a dot product, and the [distance from a point to a line](/point-to-line-distance/) is a cross product divided by a length.
- [Distance from a point to a segment](/point-to-segment-distance/) and the [Hausdorff distance](/hausdorff-distance/): distances from a point to a set, and between two sets, built on this one.
- [Orientation test](/orientation-test/): the other basic predicate of plane geometry, also a polynomial of degree 2 that is exact on integers.
- [Floating-point arithmetic](/floating-point-arithmetic/): the reason why roots and rounded squares give wrong comparisons.

## References
