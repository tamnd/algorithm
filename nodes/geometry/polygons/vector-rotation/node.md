---
tag: E9F88R
kind: technique
slug: vector-rotation
name: Rotating a vector
aliases:
- rotation matrix
- 2D rotation
- rotation about a point
area: geometry/polygons
level: intro
summary: Technique for turning a vector by a given angle around the origin using sine and cosine in a rotation matrix.
prereqs: [point-and-vector, dot-product, cross-product]
see_also: [point-projection-and-reflection, givens-rotations, gauss-complex-multiplication, rotating-calipers, minimum-area-enclosing-rectangle, angular-sort, kabsch-algorithm, polygon-orientation]
sources:
  - book: isbn:9780201848403
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 5, Geometrical transformations (the 2D rotation matrix, rotation about an arbitrary point by translation, and composition)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 5.1, Householder and Givens transformations (Givens rotations and the stable computation of c and s)
  - book: isbn:9781558605947
    title: Philip J. Schneider and David H. Eberly, Geometric Tools for Computer Graphics, Morgan Kaufmann, 2003
    locator: Chapter 4, Matrices and transformations (rotation as an orthogonal transformation with determinant 1)
---

Rotating a vector $v = (x, y)$ by an angle $\theta$ counterclockwise around the origin gives $(x\cos\theta - y\sin\theta,\ x\sin\theta + y\cos\theta)$, the product of $v$ with the rotation matrix $R_\theta$. Four multiplications and two additions, $O(1)$ time. Rotating around another center $o$ is the same step on $p - o$, followed by adding $o$ back. The rotation keeps lengths, [dot products](/dot-product/), [cross products](/cross-product/) and so the [orientation](/polygon-orientation/) of every triangle. It is exact for the angles whose cosine and sine are rational, such as the quarter turn, and for the scaled form $(u \cdot v,\ u \times v)$ that turns $v$ into the frame of a direction $u$ without any square root.

## In plain words

Pin a stick at one end and turn it around the pin. Its length stays the same and only its direction changes. A rotation of a vector does exactly this.

To compute the new end point, split the stick into a part along the x axis and a part along the y axis. Each part turns by the same angle, and the turned parts are added up. Two numbers, the cosine and the sine of the angle, say how much of each part ends up along each axis.

To turn a whole shape around some other point, move that point to the origin first, turn, and move it back. The shape keeps its size, its angles and the order of its corners.

## When it applies

- **A shape in a new direction.** A polygon, a sprite or a robot outline is drawn or tested after it has turned by a known angle.
- **Working in the frame of a direction.** A problem is simpler when one direction is horizontal: the edge of a hull in [rotating calipers](/rotating-calipers/) and the [minimum-area enclosing rectangle](/minimum-area-enclosing-rectangle/), the axis of a projection, or the edge of a sweep.
- **Comparing directions.** Two vectors are compared by angle after turning one into the frame of the other, as in [angular sorting](/angular-sort/).
- **Zeroing a coordinate.** Linear algebra turns a vector $(a, b)$ onto the first axis with a [Givens rotation](/givens-rotations/), to clear one entry of a matrix.

## The template

Notation: $p$ and $o$ are points, $v = p - o$ is a vector, and $\theta$ is the angle, positive for a counterclockwise turn in a coordinate system with the y axis pointing up. The pair $(c, s)$ has $c^2 + s^2 = 1$ and stands for $(\cos\theta, \sin\theta)$. Arithmetic is on the [real RAM](/real-ram/).

```pseudo id=main
ROTATE(p, o, θ)
L1  (c, s) ← COS-SIN(θ)             ▷ how the angle is given
L2  (x, y) ← p − o                  ▷ o = (0, 0) for a vector
L3  x′ ← c·x − s·y                  ▷ uses the old x and y
L4  y′ ← s·x + c·y
L5  return o + (x′, y′)
```

The holes are `COS-SIN`, how the pair $(c, s)$ is obtained, and the center $o$.

- **From an angle.** $(c, s) = (\cos\theta, \sin\theta)$ from the math library, in floating point.
- **Quarter turns.** $(0, 1)$ for $90°$, $(-1, 0)$ for $180°$, $(0, -1)$ for $270°$; then lines L3 and L4 are exact, for example $(x, y) \mapsto (-y, x)$ for $90°$.
- **Rational rotations.** $(c, s) = \left(\frac{1 - m^2}{1 + m^2}, \frac{2m}{1 + m^2}\right)$ for a rational $m$, such as $(3/5, 4/5)$ for $m = 1/2$. These are exact on rational input.
- **From a direction.** To turn the direction $u = (u_x, u_y) \ne 0$ onto the positive x axis, $(c, s) = (u_x, -u_y)/|u|$. Without the division by $|u|$, lines L3 and L4 return $(u \cdot v,\ u \times v)$, the rotated vector scaled by $|u|$, which is exact on integers.

**Why lines L3 and L4 rotate.** Write $v = r(\cos\alpha, \sin\alpha)$ with $r = |v|$. By the addition formulas,

$$c\,x - s\,y = r(\cos\theta\cos\alpha - \sin\theta\sin\alpha) = r\cos(\alpha + \theta), \qquad s\,x + c\,y = r\sin(\alpha + \theta).$$

So the result has the same length $r$ and the angle $\alpha + \theta$. In complex numbers this is the product $(x + iy)(c + is)$, and turning $v$ by $\theta$ is multiplying by $e^{i\theta}$.

**Why it keeps lengths and orientations.** The matrix $R = \begin{pmatrix} c & -s \\ s & c \end{pmatrix}$ has $R^{\mathsf T} R = I$ when $c^2 + s^2 = 1$, so $(Ru) \cdot (Rv) = u \cdot v$ for all $u, v$. Its determinant is $c^2 + s^2 = 1$, so $(Ru) \times (Rv) = u \times v$, and every orientation test and every [shoelace area](/shoelace-formula/) is unchanged. A matrix with determinant $-1$ would be a reflection instead.

**Composition and inverse.** $R_\varphi R_\theta = R_{\varphi + \theta}$ by the addition formulas, and $R_\theta^{-1} = R_{-\theta} = R_\theta^{\mathsf T}$. The scaled form $(u \cdot v,\ u \times v)$ equals $|u|\, R_{-\alpha} v$ where $\alpha$ is the angle of $u$.

**Cost.** Four multiplications and two additions per point, plus the cost of `COS-SIN` once. A polygon with $n$ vertices turns in $\Theta(n)$ time.

### Example

Take $p = (4, 2)$ and $o = (1, 1)$, so $v = (3, 1)$ with $|v|^2 = 10$.

| angle | $(c, s)$ | $(x', y')$ | result $o + (x', y')$ |
| --- | --- | --- | --- |
| $90°$ | $(0, 1)$ | $(-1, 3)$ | $(0, 4)$ |
| $180°$ | $(-1, 0)$ | $(-3, -1)$ | $(-2, 0)$ |
| $\arctan(4/3) \approx 53.13°$ | $(3/5, 4/5)$ | $(1, 3)$ | $(2, 4)$ |
| $30°$ | $(\sqrt3/2, 1/2)$ | $(\frac{3\sqrt3 - 1}{2}, \frac{3 + \sqrt3}{2}) \approx (2.098, 2.366)$ | $\approx (3.098, 3.366)$ |

Each $(x', y')$ has squared length 10. The direction $u = (1, 1)$ turned onto the x axis by the scaled form sends $v = (3, 1)$ to $(u \cdot v, u \times v) = (4, -2)$: $v$ points below $u$ (the second coordinate is negative), and $(4, -2)/|u|$ is $v$ in the frame of $u$.

## Classic examples

- **[Rotating calipers](/rotating-calipers/) and the [minimum-area enclosing rectangle](/minimum-area-enclosing-rectangle/).** For each hull edge direction $u$, the extents of the hull along $u$ and along its normal are the coordinates $u \cdot v$ and $u \times v$ of the scaled rotation, compared exactly without turning the hull.
- **[Angular sort](/angular-sort/).** Sorting vectors by angle compares $u \times v$, the second coordinate of $v$ in the frame of $u$, with a half-plane test first.
- **[Givens rotations](/givens-rotations/).** For a pair $(a, b)$ the rotation with $(c, s) = (a, -b)/\sqrt{a^2 + b^2}$ turns it into $(\sqrt{a^2 + b^2}, 0)$; a QR decomposition applies one such rotation per cleared entry.
- **[Gauss's complex multiplication](/gauss-complex-multiplication/).** Multiplying by $c + is$ is lines L3 and L4. Gauss's trick does it with three real multiplications instead of four, at the cost of more additions.
- **[Kabsch algorithm](/kabsch-algorithm/).** Finds the rotation that best superposes two point sets in the least-squares sense, from a singular value decomposition, and applies it as in the template.

## Variations

- **Rotation about a point as one affine map.** $p \mapsto R(p - o) + o = Rp + (o - Ro)$. In homogeneous coordinates this is one $3 \times 3$ matrix, so a chain of rotations and translations multiplies into one matrix.
- **Three dimensions.** A rotation about a unit axis $k$ by $\theta$ is Rodrigues' formula $v \cos\theta + (k \times v)\sin\theta + k (k \cdot v)(1 - \cos\theta)$; a unit quaternion encodes the same map and composes with fewer operations.
- **Rotation by reflections.** Two [reflections](/point-projection-and-reflection/) across lines through the origin at angle $\theta/2$ give the rotation by $\theta$.
- **Rational rotations.** The pairs $\left(\frac{1 - m^2}{1 + m^2}, \frac{2m}{1 + m^2}\right)$ for rational $m$ give every rotation with rational cosine and sine except the half turn $(-1, 0)$, so exact code can approximate any angle by one of them.

## Pitfalls

- **Overwriting $x$ too early.** Code that runs `x = c*x - s*y` and then `y = s*x + c*y` uses the new $x$ at line L4. Keep the old values, as the template does with $x'$ and $y'$.
- **Degrees and radians.** Math libraries take radians; passing degrees gives a wrong angle without an error.
- **Screen coordinates.** With the y axis pointing down, as on most screens, a positive angle turns the shape clockwise on the screen.
- **Drift.** Turning a shape by a small angle many times, each time from the last result, multiplies rounding errors and the shape slowly grows or shrinks. Keep the total angle and rotate the original shape, or renormalize.
- **Forgetting the center.** Applying lines L3 and L4 to $p$ instead of $p - o$ turns the shape around the origin, which also moves it.
- **Testing exactness on rotated floats.** After a rotation by $30°$, points that were collinear may no longer test as collinear in floating point. Compute predicates on the input, which the rotation does not change, or use an exact rotation.

## Exercises

1. Show that the shoelace area of a polygon does not change when every vertex is rotated around the same center.
2. Show that every rotation with rational $c$ and $s$, other than the half turn, has the form $\left(\frac{1 - m^2}{1 + m^2}, \frac{2m}{1 + m^2}\right)$ with rational $m$. (Hint: $m = s / (1 + c)$.)
3. Given two vectors $u$ and $v$ of the same length, find the rotation that turns $u$ into $v$ without any trigonometric function.
4. Show that the composition of the reflections across lines through the origin with directions $(\cos\alpha, \sin\alpha)$ and $(\cos\beta, \sin\beta)$, in this order, is the rotation by $2(\beta - \alpha)$.

## References
