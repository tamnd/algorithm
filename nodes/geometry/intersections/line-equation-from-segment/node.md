---
tag: 1VCZP5
kind: algorithm
slug: line-equation-from-segment
name: Equation of a line through a segment
aliases:
- Finding the equation of a line for a segment
- line through two points
area: geometry/intersections
level: intro
summary: Compute the coefficients A, B and C of the line A x + B y + C = 0 through the two end points of a segment, and normalize them so that equal lines get equal integer triples.
model: real-ram
complexity:
  vars: {U: the largest absolute value of a coordinate}
  time: {worst: O(log U)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1637
  people: [René Descartes, Pierre de Fermat]
  note: The equation of a straight line through two points belongs to the analytic geometry of Descartes and Fermat in the 1630s; the integer normalization by the greatest common divisor and a sign rule is a standard device of computational geometry code.
prereqs: [line-representation, cross-product, point-and-vector]
see_also: [line-line-intersection, orientation-test, point-to-line-distance, segment-intersection-point, half-plane-intersection, line-arrangement, floating-point-arithmetic]
sources:
  - url: https://cp-algorithms.com/geometry/segment-to-line.html
    title: cp-algorithms, Finding the equation of a line for a segment
    locator: the formulas A = y1 - y2, B = x2 - x1, C = -A x1 - B y1, the normalization by the gcd and the sign in the integer case, and the division by sqrt(A^2 + B^2) in the real case
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1 (the signed area of a triangle and the left-of test, which is the line equation through two points evaluated at a third)
---

The equation of the line through a segment $pq$ is $A x + B y + C = 0$ with $A = p_y - q_y$, $B = q_x - p_x$ and $C = -(A p_x + B p_y)$. The left side is the cross product $\operatorname{cross}(q - p, r - p)$ at the point $r = (x, y)$, so the same formula is the [orientation test](/orientation-test/). With integer end points the coefficients are integers, and dividing by their greatest common divisor and fixing the sign gives a canonical form, so that two segments on the same line give the same triple. The computation takes a constant number of arithmetic operations plus one gcd.

## In plain words

Two different points fix one straight line. You want a simple rule that tells, for any point, whether it is on that line. The rule has the form "A times the first coordinate, plus B times the second, plus C, equals zero".

The numbers A and B come from the differences of the coordinates of the two points, and C is chosen so that the first point fits. Then the second point fits too. The same line has many such rules, since you can multiply all three numbers by the same factor. To make the rule unique, divide the three whole numbers by their largest common divisor, and change all signs if the first one is negative.

## The problem

**Input.** Two distinct points $p = (p_x, p_y)$ and $q = (q_x, q_y)$ with integer coordinates of absolute value at most $U$.

**Output.** Integers $(A, B, C)$ with $(A, B) \ne (0, 0)$ such that the line through $p$ and $q$ is $\{(x, y) : A x + B y + C = 0\}$, in canonical form: $\gcd(|A|, |B|, |C|) = 1$, and $A > 0$, or $A = 0$ and $B > 0$.

**Notation.** $\operatorname{cross}(u, v) = u_x v_y - u_y v_x$, the [cross product](/cross-product/). A line is defined up to a nonzero factor, as on the [line representation](/line-representation/) page.

**Model.** The [real RAM](/real-ram/) for the arithmetic, which is exact here; the gcd costs $O(\log U)$ arithmetic steps by Euclid's algorithm.

## The algorithm

```pseudo id=main
LINE-THROUGH(p, q)                        ▷ integer points
L1  if p = q then error "the points must be distinct"
L2  A ← p_y − q_y, B ← q_x − p_x
L3  C ← −(A · p_x + B · p_y)
L4  g ← gcd(|A|, |B|, |C|), and A, B, C ← A / g, B / g, C / g
L5  if A < 0, or A = 0 and B < 0, then A, B, C ← −A, −B, −C
L6  return (A, B, C)
```

Lines L2 and L3 give the oriented form: $A x + B y + C = \operatorname{cross}(q - p, (x, y) - p)$, which is positive left of the direction from $p$ to $q$. Lines L4 and L5 throw the orientation away and make the triple unique. Since $\gcd(A, B)$ divides $C = -(A p_x + B p_y)$, the gcd of line L4 is in fact $\gcd(|A|, |B|)$. The implementation also has the oriented form alone, a version for points with `Fraction` coordinates that first clears the denominators, and the normalization of any integer triple.

## Example

| $p$ | $q$ | $(A, B, C)$ after L3 | $g$ | after L4 | after L5 | line |
| --- | --- | --- | --- | --- | --- | --- |
| $(1, 2)$ | $(4, 6)$ | $(-4, 3, -2)$ | 1 | $(-4, 3, -2)$ | $(4, -3, 2)$ | $4x - 3y + 2 = 0$ |
| $(2, 2)$ | $(6, 8)$ | $(-6, 4, 4)$ | 2 | $(-3, 2, 2)$ | $(3, -2, -2)$ | $3x - 2y - 2 = 0$ |
| $(3, 1)$ | $(3, 5)$ | $(-4, 0, 12)$ | 4 | $(-1, 0, 3)$ | $(1, 0, -3)$ | $x = 3$ |
| $(5, 2)$ | $(1, 2)$ | $(0, -4, 8)$ | 4 | $(0, -1, 2)$ | $(0, 1, -2)$ | $y = 2$ |

In the first row, the origin gives $-4 \cdot 0 + 3 \cdot 0 - 2 = -2 < 0$ in the oriented form after L3, so it lies to the right of the direction from $(1, 2)$ to $(4, 6)$. The segments from $(1, 2)$ to $(4, 6)$ and from $(7, 10)$ to $(-2, -2)$ lie on the same line, and both give $(4, -3, 2)$.

## Correctness

The point $p$ satisfies the equation by line L3. For $q$, $A q_x + B q_y + C = A (q_x - p_x) + B (q_y - p_y) = (p_y - q_y)(q_x - p_x) + (q_x - p_x)(q_y - p_y) = 0$. Since $p \ne q$, $(A, B) \ne (0, 0)$, so the equation describes a line, and it is the unique line through $p$ and $q$. Lines L4 and L5 multiply the triple by a nonzero factor, which does not change the line. The result is canonical: two triples of one line are proportional, two primitive integer triples can differ only by the factor $\pm 1$, and the sign rule of line L5 picks one of the two. The full proof is in the proof file.

## Complexity

Lines L1 to L3 and L5 take $O(1)$ arithmetic operations, and line L4 takes $O(\log U)$ steps of Euclid's algorithm, since $|A|, |B| \le 2U$. So the time is $O(\log U)$ and the extra space is $\Theta(1)$. Without the normalization, the oriented form takes $O(1)$ time. The coefficients are small: $|A|, |B| \le 2U$ and $|C| \le 2U^2$, since $C = \operatorname{cross}(p, q)$.

## Properties

- **Exact.** All values are integers, with no division except by the gcd, which is exact.
- **Symmetric.** The canonical form does not depend on the order of $p$ and $q$, or on which two points of the line are given.
- **Oriented form for free.** Before line L4, the sign of $A x + B y + C$ is the side of $(x, y)$ with respect to the directed segment.
- **Vertical lines.** They need no special case: $B = 0$.

## Variants and improvements

- **Unit normal form.** Divide by $\sqrt{A^2 + B^2}$ instead, so that $A^2 + B^2 = 1$ and $A x + B y + C$ is the signed distance to the line. This needs floating point and suits the [distance to a line](/point-to-line-distance/) and circle computations, but equal lines can then differ in the last bits, so comparisons need a tolerance.
- **Rational points.** Multiply the triple by the least common multiple of the denominators and normalize, as in the implementation.
- **Homogeneous coordinates.** The line through $(p_x : p_y : 1)$ and $(q_x : q_y : 1)$ is their cross product in $\mathbb{R}^3$, $(p_y - q_y,\ q_x - p_x,\ p_x q_y - p_y q_x)$, the same triple.
- **Point and direction.** Keep $p$ and $d = q - p$ instead; this is the form used for segment parameters.

## When to use it

Use the general form when you need to intersect lines, test sides, or store lines as keys of a hash table, for example to count the distinct lines through pairs of $n$ points. Use the canonical form only for equality tests and hashing; for side tests use the oriented form of lines L2 and L3, which keeps the direction of the segment.

## Pitfalls

- **Losing the orientation in line L5.** After the sign rule, $A x + B y + C > 0$ no longer means "left of $p \to q$". Code that needs the side, such as clipping, must use the triple from line L3.
- **Skipping line L4.** Without the gcd, the segments from $(1, 2)$ to $(4, 6)$ and from $(1, 2)$ to $(7, 10)$ give $(-4, 3, -2)$ and $(-8, 6, -4)$, the same line with different triples, so a hash table counts it twice.
- **Equal points in line L1.** For $p = q$ every coefficient is zero, and the "line" contains every point.
- **Floating-point normalization.** With the unit normal form, the same line from two different segments can give slightly different numbers, and an exact comparison fails.
- **Overflow in fixed-width integers.** $C$ is a product of two coordinates; with 32-bit coordinates it needs 64 bits.

## Implementations

## History

The equation of a line through two points is a basic result of the analytic geometry of Descartes and Fermat in the 1630s. In computational geometry the same expression appears as the determinant of three points, the signed area of a triangle, which gives the orientation test. The gcd normalization is common in programming practice for exact hashing of lines.

## References
