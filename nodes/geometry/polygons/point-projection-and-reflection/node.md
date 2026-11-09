---
tag: JWYTDW
kind: technique
slug: point-projection-and-reflection
name: Point projection and reflection
aliases:
- orthogonal projection onto a line
- foot of the perpendicular
- reflection across a line
area: geometry/polygons
level: intro
summary: Techniques for finding the nearest point on a line to a given point and its mirror image across that line.
prereqs: [point-and-vector, dot-product]
see_also: [point-to-line-distance, point-to-segment-distance, vector-rotation, cross-product, householder-reflections, separating-axis-theorem, ray-casting, ramer-douglas-peucker]
sources:
  - book: isbn:9781558605947
    title: Philip J. Schneider and David H. Eberly, Geometric Tools for Computer Graphics, Morgan Kaufmann, 2003
    locator: Chapter 6, Distance in 2D (the distance from a point to a line, a ray and a segment by projection and clamping)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 5.1, Householder and Givens transformations (the reflection matrix I − 2uu^T/u^Tu)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition, MIT Press, 2009
    locator: Section 33.1, Line-segment properties (dot and cross products as the basic primitives)
---

Projecting a point $p$ onto a line finds the point $q$ of the line nearest to $p$, the foot of the perpendicular from $p$. Reflecting $p$ across the line finds its mirror image $p' = 2q - p$. Both come from one [dot product](/dot-product/) and one division, $t = \frac{(p - a) \cdot d}{d \cdot d}$ for the line $a + t\,d$, with no square root and no angle, so on integer or rational input they are exact. The same few lines, with $t$ clamped to an interval, give the nearest point of a segment or a ray, and they are the inner step of [point-to-segment distance](/point-to-segment-distance/), of reflections in [ray casting](/ray-casting/), and of projecting a polygon onto an axis.

## In plain words

Stand at a point next to a straight road and walk to the road by the shortest way. You walk straight at a right angle to the road, and you reach it at the foot of the perpendicular. That point is the projection.

Now keep walking the same distance past the road. You end at the mirror image of your start, as if the road were a mirror. That point is the reflection.

To find the foot, measure how far along the road it lies, as a fraction of a step along the road. This fraction comes from one multiplication of the two directions. If the road is only a short piece, a fraction below zero or above one means the nearest point is an end of the piece.

## When it applies

- **Nearest point on a linear object.** The question asks for the closest point, or the distance, from a point to a line, a segment or a ray: a cursor snapping to an edge, a vertex tested against a chord in [polyline simplification](/ramer-douglas-peucker/), a point tested against a polygon edge.
- **A mirror.** A point, a vector or a whole polygon is mirrored across a line: symmetric shapes, light bouncing off a wall, a billiard ball, or the shortest path that must touch a line (reflect one end, then draw a straight segment).
- **Coordinates along a direction.** A set of points is reduced to their positions along one axis: the extent of a polygon in a direction, as in the [separating axis theorem](/separating-axis-theorem/) and [rotating calipers](/rotating-calipers/), or the order of points along a line.
- **Removing a component.** A vector is split into a part along $d$ and a part perpendicular to it, as in [Gram-Schmidt](/gram-schmidt-process/) or in sliding motion along a wall.

## The template

Notation: $p$, $a$, $b$ are points of the plane, $a \ne b$, and $d = b - a$. The line is $\{a + t\,d : t \in \mathbb{R}\}$; the parameter $t = 0$ is $a$ and $t = 1$ is $b$. All arithmetic is on the [real RAM](/real-ram/), or exact on integers and fractions.

```pseudo id=main
PROJECT(p, a, b)                 ▷ a ≠ b
L1  d ← b − a
L2  t ← ((p − a) · d) / (d · d)  ▷ parameter of the foot of the perpendicular
L3  t ← CLAMP(t)                 ▷ the range of the object
L4  q ← a + t d                  ▷ the nearest point of the object
L5  return COMBINE(p, q, t)      ▷ what to report
```

The holes are `CLAMP` and `COMBINE`.

- `CLAMP` is the identity for a line, $\max(t, 0)$ for the ray from $a$ through $b$, and $\min(\max(t, 0), 1)$ for the segment $ab$.
- `COMBINE` returns $q$ for the projection, $2q - p$ for the reflection, $|p - q|^2$ for the squared distance, or $t$ alone when only the position along the line matters.

**Why line L2 gives the nearest point.** Let $t^*$ be the value of line L2 and $q^* = a + t^* d$. Then $(p - q^*) \cdot d = (p - a) \cdot d - t^* (d \cdot d) = 0$, so $p - q^*$ is perpendicular to the line. For any point $r = a + s\,d$ of the line, $p - r = (p - q^*) + (t^* - s)\,d$, and the two parts are perpendicular, so

$$|p - r|^2 = |p - q^*|^2 + (s - t^*)^2\, |d|^2.$$

This is smallest exactly at $s = t^*$, so the nearest point of the line is unique.

**Why clamping is right.** By the same identity, $|p - r|^2$ is a quadratic in $s$ with its minimum at $t^*$, increasing in $|s - t^*|$. On an interval of allowed $s$, the minimum is at the point of the interval nearest to $t^*$, which is what line L3 computes.

**Why $2q - p$ is the mirror image.** For the line (no clamping), the midpoint of $p$ and $p' = 2q - p$ is $q$, on the line, and $p' - p = 2(q - p)$ is perpendicular to the line. For every point $r$ on the line, $p' - r = (q - r) - (p - q)$ with perpendicular parts, so $|p' - r| = |p - r|$: the reflection keeps every distance to the line's points.

**Distance without the foot.** The squared distance to the line is also $\frac{(d \times (p - a))^2}{d \cdot d}$ with the [cross product](/cross-product/), since $|d|^2 |p - a|^2 = (d \cdot (p - a))^2 + (d \times (p - a))^2$. This is the form used in [point-to-line distance](/point-to-line-distance/).

**Exact form.** With $D = d \cdot d$ and $k = (p - a) \cdot d$, the points $D\,q = D\,a + k\,d$ and $D\,p' = 2(D\,a + k\,d) - D\,p$ have integer coordinates when the input does. So one can either keep $q$ as a pair of fractions with denominator $D$, or compare scaled values $D\,q$ without dividing.

**Cost.** A constant number of additions, multiplications and one division: $O(1)$ time and space. With integer inputs of absolute value at most $M$, the numbers in $D\,q$ are $O(M^3)$.

**Matrix form.** For a line through the origin with direction $d$, the projection is the matrix $\Pi = \frac{d\,d^{\mathsf T}}{d^{\mathsf T} d}$ and the reflection is $2\Pi - I$. With the unit direction $(\cos\varphi, \sin\varphi)$ the reflection is $\begin{pmatrix} \cos 2\varphi & \sin 2\varphi \\ \sin 2\varphi & -\cos 2\varphi \end{pmatrix}$. With $u$ a normal of the line, $2\Pi - I = I - \frac{2\,u\,u^{\mathsf T}}{u^{\mathsf T} u}$, which is a [Householder reflection](/householder-reflections/).

### Example

Take $a = (0, 0)$, $b = (4, 2)$, so $d = (4, 2)$ and $d \cdot d = 20$.

| $p$ | $(p - a) \cdot d$ | $t$ | object | $q$ | $2q - p$ | $\lvert p - q \rvert^2$ |
| --- | --- | --- | --- | --- | --- | --- |
| $(1, 3)$ | 10 | $1/2$ | line or segment | $(2, 1)$ | $(3, -1)$ | 5 |
| $(6, 5)$ | 34 | $17/10$ | line | $(34/5, 17/5)$ | $(38/5, 9/5)$ | $16/5$ |
| $(6, 5)$ | 34 | $17/10 \to 1$ | segment | $(4, 2)$ | not a reflection | 13 |
| $(-2, 1)$ | $-6$ | $-3/10 \to 0$ | segment or ray | $(0, 0)$ | not a reflection | 5 |

For $p = (1, 3)$, the cross product form gives the same distance: $d \times (p - a) = 4 \cdot 3 - 2 \cdot 1 = 10$, and $10^2 / 20 = 5$. For $p = (6, 5)$ it gives $8^2 / 20 = 16/5$ to the line, while the segment ends at $b$ and the distance to it is $\sqrt{13}$.

## Classic examples

- **[Point-to-line distance](/point-to-line-distance/).** `CLAMP` is the identity and `COMBINE` returns $|p - q|$, or directly $|d \times (p - a)| / |d|$.
- **[Point-to-segment distance](/point-to-segment-distance/).** `CLAMP` is $[0, 1]$; this is the template exactly, and the base of the distance from a point to a polygon boundary.
- **[Ramer-Douglas-Peucker](/ramer-douglas-peucker/).** Each step finds the vertex farthest from the chord between two kept vertices, by the squared distance of `COMBINE`.
- **[Separating axis theorem](/separating-axis-theorem/).** Every vertex of two convex polygons is reduced to $t$ along an edge normal, and the two intervals of $t$ values are compared.
- **[Ray casting](/ray-casting/) and [Whitted ray tracing](/whitted-ray-tracing/).** A ray direction $v$ hitting a mirror with normal $n$ leaves in direction $v - 2\frac{v \cdot n}{n \cdot n} n$, the reflection of $v$ across the mirror line (or plane).
- **[Householder reflections](/householder-reflections/).** The same reflection matrix in $n$ dimensions, chosen to send a column of a matrix onto the first axis; it is the basis of QR decomposition.

## Variations

- **Reflecting a direction.** A vector $v$ is mirrored across a line through the origin with direction $d$ as $2\frac{v \cdot d}{d \cdot d} d - v$, or across the line with normal $n$ as $v - 2\frac{v \cdot n}{n \cdot n} n$. There is no translation by $a$, because a direction has no position.
- **Line given by an equation.** For the line $\alpha x + \beta y = \gamma$ with normal $n = (\alpha, \beta)$, the foot is $q = p - \frac{n \cdot p - \gamma}{n \cdot n} n$ and the reflection is $p - 2\frac{n \cdot p - \gamma}{n \cdot n} n$; see [line representation](/line-representation/).
- **Higher dimensions.** The template is unchanged for a line in $\mathbb{R}^k$. Projection onto a plane or a subspace replaces $d$ by a basis, and the division by $d \cdot d$ by solving the normal equations, or by an orthonormal basis.
- **Composing reflections.** Reflecting across two lines through the origin at angle $\theta$ is a [rotation](/vector-rotation/) by $2\theta$. Reflection reverses orientation: $\mathrm{orient}(p', q', r') = -\mathrm{orient}(p, q, r)$, so a mirrored polygon has the opposite [orientation](/polygon-orientation/), and its vertex order must be reversed to keep it counterclockwise.

## Pitfalls

- **A degenerate line.** If $a = b$ then $d \cdot d = 0$ and line L2 divides by zero. Test for it, and treat the object as the single point $a$.
- **Clamping a reflection.** Clamping at line L3 makes $2q - p$ a reflection across an end point, not across the line. Use the identity `CLAMP` for reflections.
- **Normalizing first.** Code that divides $d$ by $|d|$ needs a square root, so it is never exact. Divide by $d \cdot d$ once, at line L2, or keep the scaled form $D\,q$.
- **Distance to the line when a segment is meant.** The cross product formula gives the distance to the whole line. For $p = (6, 5)$ in the example, it gives $\sqrt{16/5}$ instead of $\sqrt{13}$ for the segment.
- **Floating-point feet.** The computed $q$ is in general not exactly on the line. Tests such as "is $q$ on the segment" should use the parameter $t$ and the exact orientation, not $q$ itself.

## Exercises

1. Show that reflecting twice across the same line gives back $p$, and that $\mathrm{orient}(p', q', r') = -\mathrm{orient}(p, q, r)$ for three reflected points.
2. Heron's problem: given two points $A$ and $B$ on the same side of a line $\ell$, find the point $X$ on $\ell$ that minimizes $|AX| + |XB|$. (Hint: reflect $B$ across $\ell$.)
3. Show that the reflections across two lines through the origin with directions at angle $\theta$ compose to the rotation by $2\theta$.
4. Give a test, with integer arithmetic only and no division, of whether the foot of the perpendicular from $p$ lies inside the segment $ab$, and of which of two points is nearer to the segment.

## References
