---
tag: SVW2VD
kind: algorithm
slug: point-to-line-distance
name: Distance from a point to a line
aliases:
- point-line distance
- perpendicular distance to a line
area: geometry/proximity
level: intro
summary: Algorithm that computes the shortest distance from a point to a line using the line equation or a cross product.
model: real-ram
complexity:
  vars: {d: the dimension}
  time: {worst: Θ(d)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
prereqs: [euclidean-distance, cross-product, dot-product]
see_also: [point-to-segment-distance, point-projection-and-reflection, line-representation, line-equation-from-segment, orientation-test, oriented-triangle-area]
sources:
  - book: isbn:9781558605947
    title: Philip J. Schneider and David H. Eberly, Geometric Tools for Computer Graphics, Morgan Kaufmann, 2003
    locator: Chapter 6, Distance in 2D, Section 6.1 (distance from a point to a line, a ray and a segment, with the projection parameter)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 33, Section 33.1 (cross products, and the cross product as twice a signed triangle area)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1 (the area of a triangle as a determinant, and the left-of test built on it)
---

The distance from a point $p$ to the line through two distinct points $a$ and $b$ is the length of the perpendicular from $p$ to the line. In the plane it equals $|(b - a) \times (p - a)| / \|b - a\|$, the absolute value of a [cross product](/cross-product/) divided by a length, and its square is a rational function of the coordinates. So with integer input the squared distance is an exact fraction, and only the final report needs a root. In any dimension the squared distance is $\|w\|^2 - (w \cdot u)^2 / \|u\|^2$ with $u = b - a$ and $w = p - a$.

## In plain words

Draw a straight line through two pins, and put a third pin somewhere else. The shortest way from the third pin to the line meets the line at a right angle. Its length is the answer.

There is a quick way to get it. The three pins make a triangle. The area of that triangle is half of the base times the height. The base is the gap between the two pins on the line, and the height is exactly the distance you want. The area comes from a cross product, which uses only multiplications and subtractions. So the height is twice the area divided by the base. If you keep the result squared, you never need a square root, and with whole-number coordinates the answer is an exact fraction.

## The problem

**Input.** Points $a \ne b$ and $p$ in the plane, with coordinates $p = (x, y)$ that are integers or rationals.

**Output.** The squared distance $\delta^2 = \min_{t \in \mathbb{R}} \|p - (a + t(b - a))\|^2$ from $p$ to the line $\ell(a, b) = \{a + t(b - a) : t \in \mathbb{R}\}$, as an exact rational number, and the foot $f$ of the perpendicular, the point of $\ell$ where the minimum is reached. The distance itself is $\delta = \sqrt{\delta^2}$.

The cross product of $u = (u_x, u_y)$ and $w = (w_x, w_y)$ is the scalar $u \times w = u_x w_y - u_y w_x$. Its sign is the [orientation test](/orientation-test/) $\mathrm{orient}(a, b, p)$ when $u = b - a$ and $w = p - a$: positive when $p$ is to the left of the directed line from $a$ to $b$.

## The algorithm

```pseudo id=main
POINT-LINE-DISTANCE-SQUARED(p, a, b)       ▷ squared distance from p to the line through a and b
L1  if a = b then error "the two points do not define a line"
L2  u ← b − a
L3  w ← p − a
L4  c ← u_x · w_y − u_y · w_x                ▷ the cross product u × w
L5  t ← (w · u) / (u · u)                    ▷ the parameter of the foot
L6  f ← a + t · u                             ▷ the foot of the perpendicular
L7  return (c² / (u · u), f)
```

Line L4 computes twice the signed area of the triangle $a, b, p$. Line L7 divides its square by the squared base length $u \cdot u$, which is the squared height. Lines L5 and L6 compute the foot by projecting $w$ on $u$. All operations are additions, multiplications and one division, so with `fractions.Fraction` the result is exact. The distance is $\sqrt{c^2 / (u \cdot u)} = |c| / \|u\|$; take this root only to print the result, never to compare two distances.

**The line equation form.** A line given as $\{(x, y) : \alpha x + \beta y + \gamma = 0\}$ with $(\alpha, \beta) \ne (0, 0)$ has the squared distance

$$\delta^2 = \frac{(\alpha x_0 + \beta y_0 + \gamma)^2}{\alpha^2 + \beta^2}$$

from $p = (x_0, y_0)$. The line through $a$ and $b$ is $\alpha = u_y$, $\beta = -u_x$, $\gamma = u_x a_y - u_y a_x$, and then $\alpha x_0 + \beta y_0 + \gamma = -(u \times w)$, so the two forms agree. See [line representation](/line-representation/) and [line equation from a segment](/line-equation-from-segment/).

**Any dimension.** In $\mathbb{R}^d$ there is no scalar cross product, but line L7 can return $\|w\|^2 - (w \cdot u)^2 / (u \cdot u)$ instead. In the plane the two values are equal by Lagrange's identity $(u \cdot u)(w \cdot w) - (u \cdot w)^2 = (u \times w)^2$.

## Example

Take $a = (1, 1)$ and $b = (7, 9)$, so $u = (6, 8)$ and $u \cdot u = 100$. The line is $4x - 3y - 1 = 0$.

| step | $p = (8, 2)$ | $p = (2, 7)$ |
| --- | --- | --- |
| L3: $w = p - a$ | $(7, 1)$ | $(1, 6)$ |
| L4: $c = 6 w_y - 8 w_x$ | $6 - 56 = -50$ | $36 - 8 = 28$ |
| L5: $t = (w \cdot u)/100$ | $50/100 = 1/2$ | $54/100 = 27/50$ |
| L6: $f = a + t u$ | $(4, 5)$ | $(106/25, 133/25) = (4.24, 5.32)$ |
| L7: $c^2 / 100$ | $2500/100 = 25$ | $784/100 = 196/25$ |
| distance | $5$ | $14/5 = 2.8$ |
| line form $\lvert 4x - 3y - 1 \rvert / 5$ | $25/5 = 5$ | $14/5 = 2.8$ |

The sign of $c$ says that $(8, 2)$ is to the right of the directed line from $a$ to $b$ and $(2, 7)$ is to the left. For $p = (8, 2)$ the check $\|p - f\|^2 = 4^2 + (-3)^2 = 25$ agrees with line L7.

## Correctness

Write the points of the line as $a + t u$. The squared distance from $p$ to such a point is the quadratic $g(t) = \|w - t u\|^2 = \|w\|^2 - 2t\,(w \cdot u) + t^2 \|u\|^2$. Its leading coefficient $\|u\|^2$ is positive because $a \ne b$, so $g$ has exactly one minimum, at $t^* = (w \cdot u)/\|u\|^2$, with value $\|w\|^2 - (w \cdot u)^2/\|u\|^2$. Lines L5 and L6 compute $t^*$ and the foot $f = a + t^* u$. Lagrange's identity turns the minimum value into $(u \times w)^2 / \|u\|^2$, which is line L7. The vector $p - f = w - t^* u$ is orthogonal to $u$, so the foot is the perpendicular foot. The full proof, with the identity expanded, is in the correctness proof below.

## Complexity

In the plane the algorithm does a fixed number of arithmetic operations: 2 multiplications for the cross product, 2 for $w \cdot u$, 2 for $u \cdot u$, 2 for the foot, one square and two divisions. So it takes $\Theta(1)$ time on the [real RAM](/real-ram/). In $\mathbb{R}^d$ the dot products take $\Theta(d)$ time, and the space is $\Theta(1)$ beyond the input.

With integer coordinates of absolute value at most $M$, $|c| \le 8M^2$ and $u \cdot u \le 8M^2$, so the numerator $c^2$ fits in about $4 \lg M + 6$ binary digits. In a fixed-width language, 32-bit coordinates already need 128-bit products for $c^2$. Two squared distances $c_1^2 / D_1$ and $c_2^2 / D_2$ can be compared without division as $c_1^2 D_2$ against $c_2^2 D_1$.

## Properties

- **Exact on rational input.** Every step is a field operation. The only irrational value is the final root, and comparisons never need it.
- **Signed distance.** $c / \|u\|$ is the signed distance: positive on the left of the directed line, negative on the right, zero on the line. Its sign is the [orientation test](/orientation-test/) and needs no division.
- **Invariant under the choice of points.** Any two distinct points of the same line give the same result: replacing $a, b$ by other points of the line multiplies $c$ and $\|u\|$ by the same factor.
- **The foot is the projection.** Line L6 is the orthogonal [projection of a point](/point-projection-and-reflection/) on a line.

## Variants and improvements

- **Segment and ray.** Clamp $t$ to $[0, 1]$ for a segment, or to $[0, \infty)$ for a ray, before line L6. This is the [distance from a point to a segment](/point-to-segment-distance/).
- **Many points against one line.** Precompute $\alpha, \beta, \gamma$ and $\alpha^2 + \beta^2$ once. Then each point costs two multiplications for the signed numerator.
- **Distance between two lines in three dimensions.** For skew lines with directions $u_1, u_2$, the distance is $|(a_2 - a_1) \cdot (u_1 \times u_2)| / \|u_1 \times u_2\|$, with the vector cross product.
- **Plane in three dimensions.** For the plane $\alpha x + \beta y + \gamma z + \eta = 0$ the same quotient formula holds with three terms in the numerator and in the denominator.

## When to use it

Use the cross product form when the line is given by two points, which is the usual case in geometry code. Use the line equation form when many points are tested against the same line, for example in the [Ramer-Douglas-Peucker](/polygon-simplification/) simplification, or in a fitting step. Use the [segment version](/point-to-segment-distance/) whenever the object is bounded: the line distance can be much smaller than the distance to the segment.

## Pitfalls

- **Taking the root too early.** Code that returns `abs(c) / math.hypot(ux, uy)` and then compares two such values can tie or reverse two distances that differ in the exact numbers, as on the page on [Euclidean distance](/euclidean-distance/). Return $c^2 / (u \cdot u)$ from line L7 and compare by cross-multiplication.
- **A degenerate line.** If $a = b$ then $u \cdot u = 0$ and line L7 divides by zero. Line L1 must reject the input, or the caller must use the point distance $\|p - a\|$.
- **Using the segment formula for a line, or the reverse.** The two agree only when $0 \le t \le 1$. For $a = (0, 0)$, $b = (1, 0)$ and $p = (3, 4)$ the line distance is $4$, but the segment distance is $\sqrt{20}$.
- **Integer division.** In a language with integer division, `c * c / dot(u, u)` truncates. Keep the numerator and the denominator, or use a rational type.

## Implementations

## History

The quotient formula for the distance from a point to a line $\alpha x + \beta y + \gamma = 0$ is part of classical analytic geometry. The cross product form, with the area of the triangle as a determinant, is the form that computational geometry texts use, because it shares its arithmetic with the orientation test.

## References
