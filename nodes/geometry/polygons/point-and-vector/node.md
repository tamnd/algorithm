---
tag: KWRFF4
kind: concept
slug: point-and-vector
name: Point and vector
aliases:
- point and vector in the plane
- position and displacement
area: geometry/polygons
level: intro
summary: Basic geometric objects representing a position in the plane and a displacement, with coordinate arithmetic such as addition, subtraction and scaling.
prereqs: []
see_also: [dot-product, cross-product, oriented-triangle-area, geometry-primitives, vector-rotation, point-projection-and-reflection, euclidean-distance, convex-combination]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1 (the integer point type of the C code, and the vector differences used to compute the area of a triangle and of a polygon)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 1, Section 1.2, Degeneracies and Robustness
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition, MIT Press, 2009
    locator: Section 33.1, Line-segment properties (points as vectors from the origin, and the cross product of two vectors)
---

A point is a position in the plane, given by two coordinates $p = (x, y)$, and a vector is a displacement, the difference $q - p$ of two points. Points and vectors use the same pair of numbers in a program, but they obey different rules: a vector can be added to a point or to a vector, two points can only be subtracted, and only vectors can be scaled. All the [geometry primitives](/geometry-primitives/), such as the [dot product](/dot-product/), the [cross product](/cross-product/) and the [orientation test](/orientation-test/), are formulas on these coordinates.

## In plain words

A point says where something is. A vector says how to move: so many steps to the right and so many steps up. If you take two points and ask "how do I get from the first to the second", the answer is a vector. If you start at a point and follow a vector, you arrive at a new point. You can follow two moves one after the other, which adds two vectors, and you can make a move twice as long, which scales a vector. It makes no sense to add two places, in the same way that it makes no sense to add two street addresses. A program stores both kinds of object as a pair of numbers, so the programmer must keep the difference in mind.

## The idea

We work in the plane $\mathbb{R}^2$. On the geometry pages of this site the notation is:

| Symbol | Meaning |
|---|---|
| $P$ | the input point set |
| $n$ | the input size |
| $h$ | the output size, named on each page |
| $d$ | the dimension, here $d = 2$ |
| $p = (x, y)$ | a point |
| $\operatorname{orient}(p, q, r)$ | the sign of $(q - p) \times (r - p)$, positive for a counterclockwise turn |

**Operations.** Let $p = (p_x, p_y)$ and $q = (q_x, q_y)$ be points, let $u = (u_x, u_y)$ and $v = (v_x, v_y)$ be vectors, and let $c \in \mathbb{R}$.

- Point minus point: $q - p = (q_x - p_x,\ q_y - p_y)$, a vector.
- Point plus vector: $p + u = (p_x + u_x,\ p_y + u_y)$, a point.
- Vector plus vector: $u + v = (u_x + v_x,\ u_y + v_y)$, a vector. With the zero vector $0 = (0, 0)$ and $-u = (-u_x, -u_y)$, the vectors form the vector space $\mathbb{R}^2$.
- Scaling: $c\,u = (c u_x,\ c u_y)$.
- Length: $|u| = \sqrt{u_x^2 + u_y^2}$, and the [Euclidean distance](/euclidean-distance/) of two points is $|q - p|$.

The points form an *affine space*: there is no special point, and the sum of two points has no meaning, because it changes when the origin moves. What is allowed is an *affine combination* $\sum_i \lambda_i p_i$ with $\sum_i \lambda_i = 1$, which equals $p_1 + \sum_{i \ge 2} \lambda_i (p_i - p_1)$ and so does not depend on the origin. With all $\lambda_i \ge 0$ it is a [convex combination](/convex-combination/). The midpoint $\frac12 p + \frac12 q$ and the point $p + t(q - p) = (1 - t)p + tq$ of the segment $pq$ at parameter $t \in [0, 1]$ are the common cases.

**Translation invariance.** Each predicate used on these pages (orientation, in-circle, the comparison of two distances) is computed from differences of points only. So moving all points by the same vector does not change any answer. A program can use this to move the origin to one of the input points, which keeps the numbers small.

**Representation.** In code a point and a vector are both a pair of numbers. Three choices matter:

- *Integer coordinates.* Sums, differences and products of integers are exact. If each coordinate has absolute value at most $B$, a difference has absolute value at most $2B$ and a cross product or dot product of two differences at most $8B^2$. With $B = 2^{30}$ the bound $8B^2 = 2^{63}$ is one more than the largest signed 64-bit integer, so with 64-bit integers the safe rule is $B < 2^{30}$. Python integers have no limit.
- *Rational coordinates.* `fractions.Fraction` keeps exact values when an algorithm makes new points, for example an intersection point of two segments.
- *Floating point.* Doubles are fast but round each operation. Equality tests and signs of small results are then not reliable, see [floating-point arithmetic](/floating-point-arithmetic/) and [catastrophic cancellation](/catastrophic-cancellation/). Python's `complex` type stores two doubles, so it rounds integer coordinates above $2^{53}$.

The cost model of the algorithm pages is the [real RAM](/real-ram/): each arithmetic operation and each comparison on real numbers costs one step. With integer input and predicates of fixed degree, each number that a predicate computes is only a constant factor longer than the input numbers, so the step count of the real RAM is also a fair count for exact integer code.

## Examples

**Differences and lengths.** Take $p = (2, 1)$, $q = (5, 5)$ and $r = (6, 2)$. Then $u = q - p = (3, 4)$ and $v = r - p = (4, 1)$. The length of $u$ is $\sqrt{9 + 16} = 5$, so $|pq| = 5$. The length of $v$ is $\sqrt{17}$, which is irrational, so code that compares distances compares the squares $25$ and $17$ instead, and stays exact.

**A point on a segment.** The point of $pq$ at $t = \frac13$ is $p + \frac13 (3, 4) = (3, \frac73)$. The coordinates are rational, so a `Fraction` holds the point exactly, while a double holds $\frac73$ only approximately.

**The same answer after a move.** Move all three points by $(-2, -1)$, which puts $p$ at the origin. The vectors $u$ and $v$ do not change, so the dot product $u \cdot v = 3 \cdot 4 + 4 \cdot 1 = 16$ and the cross product $u \times v = 3 \cdot 1 - 4 \cdot 4 = -13$ do not change either. The negative cross product says that $r$ is to the right of the directed line from $p$ to $q$.

**A non-example: the sum of two points.** The "sum" $p + q = (7, 6)$ depends on the origin. After the move above it is $(0, 0) + (3, 4) = (3, 4)$, which is $(5, 5)$ in the old coordinates, not $(7, 6)$. Code that adds two points is almost always a bug, unless the weights sum to 1, as in the midpoint.

**A rounding example.** In double precision, $0.1 + 0.2 = 0.3$ is false, because the left side is larger by about $5.6 \cdot 10^{-17}$. Points read from a file with decimal coordinates can therefore be "collinear" on paper and not collinear in the program. Scaling the decimal input to integers, or reading it into `Fraction`, avoids this.

## Where it is used

- The [dot product](/dot-product/) and the [cross product](/cross-product/) of two vectors give angles, projections, signed areas and turns.
- The [oriented area of a triangle](/oriented-triangle-area/) and the [orientation test](/orientation-test/) use the differences $q - p$ and $r - p$.
- [Vector rotation](/vector-rotation/), [point projection and reflection](/point-projection-and-reflection/) and [Euclidean distance](/euclidean-distance/) are formulas on vectors.
- The parametric form $p + t(q - p)$ is the base of [segment intersection](/segment-intersection-point/), of [polygon clipping](/polygon-clipping/) and of the [crossing number algorithm](/crossing-number-algorithm/).
- The [Minkowski sum](/minkowski-sum/) of two sets is the set of all sums $a + b$, where one operand is read as a set of vectors.

## References
