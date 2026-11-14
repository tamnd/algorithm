---
tag: FF7D9Q
kind: algorithm
slug: implicitization
name: Implicitization of rational curves and surfaces
aliases:
- implicitization by resultants
- moving curves implicitization
area: cad/surface-interrogation-and-design
level: advanced
summary: Converts a rational parametric curve or surface into an implicit polynomial equation by eliminating the parameter with a resultant, after Sederberg, Anderson and Goldman.
model: real-ram
complexity:
  vars: {d: the degree of the rational curve}
  time: {worst: O(d^5)}
  space: {extra: O(d^2)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1984
  people: [Thomas W. Sederberg, David C. Anderson, Ronald N. Goldman]
  note: They brought the resultants of classical elimination theory into geometric modeling, as a way to find the implicit equation of any rational curve or surface and to reduce intersection problems to one polynomial.
prereqs: [parametric-curve, resultant, sylvester-matrix]
see_also: [rational-bezier-curve, implicit-surface, elimination-theorem, groebner-basis, curve-surface-intersection, algebraic-surface-intersection, polynomial-interpolation, bareiss-algorithm]
sources:
  - paper: doi:10.1016/0734-189X(84)90140-3
    title: Thomas W. Sederberg, David C. Anderson and Ronald N. Goldman, Implicit representation of parametric curves and surfaces, Computer Vision, Graphics, and Image Processing 28(1), 72 to 84, 1984
    locator: the whole paper (the implicit equation of a rational curve as a resultant in the parameter, and of a rational surface as a resultant in two parameters)
  - paper: doi:10.1145/218380.218460
    title: Thomas W. Sederberg and Falai Chen, Implicitization using moving curves and surfaces, Proceedings of SIGGRAPH 95, 301 to 308, 1995
    locator: the whole paper (implicit equations as determinants of smaller matrices built from moving lines, moving conics and moving planes)
---

Implicitization turns a rational parametric curve $x = X(t) / W(t)$, $y = Y(t) / W(t)$ into one polynomial equation $F(x, y) = 0$ that holds exactly on the curve. The method of Sederberg, Anderson and Goldman takes $F$ as the [resultant](/resultant/) in $t$ of $X(t) - x W(t)$ and $Y(t) - y W(t)$, which vanishes exactly when the two have a common root, that is, when the point $(x, y)$ is on the curve. With the implicit form, the question "is this point on the curve, and on which side" becomes one evaluation, and the intersection of two curves becomes the roots of one polynomial in one unknown.

## In plain words

A curve given by a formula with a moving parameter is easy to draw, because you can step the parameter and get points. But it is hard to test whether a given point is on the curve, because you must solve for the parameter. An implicit equation is the reverse: you put in a point and get a number that is zero exactly on the curve.

To get the equation, write the two coordinate formulas as two conditions on the parameter. A point is on the curve when one parameter value makes both conditions true. A classical tool, the resultant, is a determinant of the coefficients that is zero exactly when two polynomials share a root. So that determinant, read as a formula in the point, is the implicit equation. This page computes it exactly with fractions, at a grid of points, and rebuilds the formula from those values.

## The problem

The input is three polynomials $X, Y, W$ in $t$ with rational coefficients, $W \ne 0$, of largest degree $d \ge 1$. They define the rational curve $C$ of points $(X(t) / W(t), Y(t) / W(t))$ with $W(t) \ne 0$. A [rational Bézier curve](/rational-bezier-curve/) of degree $d$ is of this form, after a change from the Bernstein basis to powers of $t$. The output is a nonzero polynomial $F(x, y)$ with integer coefficients and no common factor, of total degree at most $d$, whose zero set in $\mathbb{C}^2$ is the closure of $C$. Here the closure adds at most one point, the limit of the curve as $t \to \infty$.

Two cases are outside the problem, and the method shows them. If $X$, $Y$ and $W$ have a common root, a *base point*, the resultant is the zero polynomial; divide by their greatest common divisor first. If the parametrization is not proper, so that each point of the curve comes from $k > 1$ values of $t$, the method returns the $k$th power of the irreducible equation.

## The algorithm

For a point $(x, y)$ put $A(t) = X(t) - x W(t)$ and $B(t) = Y(t) - y W(t)$. Both have degree at most $d$, and the method reads both with the *formal* degree $d$, even if their leading coefficients vanish. Their [Sylvester matrix](/sylvester-matrix/) $S(A, B)$ is the $2d \times 2d$ matrix whose first $d$ rows hold the coefficients of $t^{d - 1} A, \dots, t A, A$ and whose last $d$ rows hold those of $t^{d - 1} B, \dots, B$. Its determinant $R(x, y) = \det S(A, B)$ is the implicit polynomial.

```pseudo id=main
IMPLICITIZE(X, Y, W)
L1  d ← max(deg X, deg Y, deg W)
L2  for each grid point (x_i, y_j) with x_i, y_j ∈ {0, 1, …, d}
L3      A ← X − x_i W and B ← Y − y_j W, both of formal degree d
L4      R[i][j] ← det S(A, B), in exact rational arithmetic
L5  interpolate R in y for each i, then in x for each power of y, to get F(x, y)
L6  return F scaled to coprime integer coefficients, leading coefficient positive
```

The entries of the first $d$ rows of $S(A, B)$ are linear in $x$, and those of the last $d$ rows linear in $y$, so $R$ has degree at most $d$ in each variable, and its values on the $(d + 1) \times (d + 1)$ grid fix it. Line L4 uses fraction free [Bareiss elimination](/bareiss-algorithm/), and line L5 solves Vandermonde systems in rational arithmetic, a form of [polynomial interpolation](/polynomial-interpolation/). The code takes $X$, $Y$ and $W$ as coefficient lists from the constant term up, and returns $F$ as a map from exponent pairs $(a, b)$ to the coefficient of $x^a y^b$. A computer algebra system computes the same determinant with $x$ and $y$ as symbols. The grid form needs only exact numbers.

## Example

Take the circle $X = 1 - t^2$, $Y = 2t$, $W = 1 + t^2$, so $d = 2$. Then $A = -(1 + x) t^2 + (1 - x)$ and $B = -y t^2 + 2t - y$, and

$$S(A, B) = \begin{pmatrix} -1 - x & 0 & 1 - x & 0 \\ 0 & -1 - x & 0 & 1 - x \\ -y & 2 & -y & 0 \\ 0 & -y & 2 & -y \end{pmatrix}, \qquad \det S(A, B) = 4 (x^2 + y^2 - 1).$$

Line L4 computes this determinant at the $9$ points of $\{0, 1, 2\}^2$:

| $R(x_i, y_j)$ | $y = 0$ | $y = 1$ | $y = 2$ |
|---|---|---|---|
| $x = 0$ | $-4$ | $0$ | $12$ |
| $x = 1$ | $0$ | $4$ | $16$ |
| $x = 2$ | $12$ | $16$ | $28$ |

Line L5 recovers $4x^2 + 4y^2 - 4$, and line L6 returns $x^2 + y^2 - 1$. The check by substitution is exact: at $t = \tfrac12$ the curve point is $(\tfrac{3/4}{5/4}, \tfrac{1}{5/4}) = (\tfrac35, \tfrac45)$, and $\tfrac{9}{25} + \tfrac{16}{25} - 1 = 0$.

Two points show the role of the formal degree. The point $(1, 0)$ comes from $t = 0$, a common root of $A = -2t^2$ and $B = 2t$. The point $(-1, 0)$ comes from no finite $t$: there $A = 2$ and $B = 2t$ have no common root, but both formal leading coefficients, $-1 - x$ and $-y$, are $0$, so the first column of $S$ is zero. It is the limit of the curve as $t \to \infty$, and the resultant includes it, which closes the circle.

Other curves give the expected equations. The folium $X = 3t$, $Y = 3t^2$, $W = 1 + t^3$ gives $x^3 + y^3 - 3xy$. The cuspidal cubic $(t^2, t^3)$ gives $x^3 - y^2$. The line $(t, 2t + 3)$ gives $2x - y + 3$.

## Correctness

The [full proof](proofs/correctness.md) shows four facts. First, the Sylvester determinant of two polynomials of formal degree $d$ is zero exactly when they have a common root or both formal leading coefficients are zero, by the usual argument that $\det S = 0$ exactly when $P A + Q B = 0$ for some $P, Q$ of degree less than $d$, not both zero. Second, without base points, $R(x, y) = 0$ exactly on the curve and at its point at infinity, because a common root $t_0$ with $W(t_0) = 0$ would be a base point. Third, $R$ has degree at most $d$ in $x$ and in $y$, so lines L2 to L5 return it exactly, and its total degree is also at most $d$: on any line $(x_0 + s p, y_0 + s q)$, replacing the rows of $B$ by those of $q A - p B$, which does not depend on $s$, shows that $R$ has degree at most $d$ in $s$. Fourth, $R$ is not the zero polynomial, because on a suitable vertical line it has at most $d + 1$ zeros.

The finer fact that $R$ is a power $G^k$ of an irreducible polynomial, with $k$ the number of parameter values per point, is cited from Sederberg, Anderson and Goldman and not proved here. The tests check the circle, the folium, the cusp, a line, the improper parametrization and a base point, and for $40$ random curves of degree $1$ to $4$ they check by exact substitution with fractions that $F$ vanishes at random points of the curve, that its total degree is at most $d$, and that it has at most $d + 1$ zeros on a vertical line.

## Complexity

Line L4 runs $(d + 1)^2$ times, and each run is Bareiss elimination on a $2d \times 2d$ matrix, $O(d^3)$ operations, so $O(d^5)$ in all. Line L5 solves $2 (d + 1)$ Vandermonde systems of size $d + 1$ by Gaussian elimination, $O(d^4)$. The total is $O(d^5)$ arithmetic operations, and $O(d^2)$ extra space for the grid of values and one matrix. The operations are on rational numbers whose size grows with $d$ and with the size of the input coefficients. Bareiss elimination keeps every intermediate value a minor of the matrix, so the sizes stay polynomial. Interpolation by a faster method, or a direct symbolic determinant, changes the constants but not the nature of the result.

For curves the cost is small: a cubic needs $16$ determinants of $6 \times 6$ matrices. For surfaces it is the size of the result that hurts. A tensor product patch of bidegree $(m, n)$ has an implicit equation of degree up to $2mn$, which is $18$ for a bicubic patch, with up to $\binom{21}{3} = 1330$ coefficients.

## Properties

- **Exact.** With rational input, the result is exact. Rounding in floats would turn the zero set of a high degree polynomial into a different curve, so implicitization is done in exact arithmetic.
- **Degree preserving.** A rational curve of degree $d$ without base points has an implicit equation of degree at most $d$, the number of points in which a general line meets the curve.
- **Whole curve.** The zero set is the closure of the whole image of the parameter line, not the image of $[0, 1]$. Points of the implicit curve outside the segment of a Bézier curve are still zeros of $F$, and an inversion step decides whether a zero belongs to the segment.
- **Always possible.** Every rational curve and surface has an implicit equation. The converse is false: most implicit curves of degree $3$ or more have no rational parametrization.

## Variants and improvements

- **Surfaces.** A rational surface $x = X(s, t) / W(s, t)$ and so on gives three polynomials in two parameters, and the implicit equation is their resultant in $s$ and $t$. Sederberg, Anderson and Goldman used the Dixon form of this resultant for tensor product patches. The degree is at most $2mn$ for a patch of bidegree $(m, n)$, and base points of the surface lower it, but they also make the plain resultant vanish identically, which is the main practical difficulty.
- **Moving lines and moving surfaces.** Sederberg and Chen (1995) build the implicit equation from polynomial families of lines, conics or planes that follow the curve or surface, and get it as the determinant of a matrix smaller than the Sylvester or Dixon matrix. The method handles some base points better.
- **Gröbner bases.** Elimination of the parameters from the ideal of $W x - X$, $W y - Y$ and $1 - z W$ with a lex [Gröbner basis](/groebner-basis/), by the [elimination theorem](/elimination-theorem/), gives the implicit equation of curves and surfaces of any form, without the base point problem, but usually at much higher cost.
- **Approximate implicitization.** For use in intersection, a low degree polynomial that is small on the curve or surface is often enough, and it is found by least squares on sample points.

## When to use it

Use it when one of two curves or surfaces in an intersection problem is rational and of low degree: implicitize one, substitute the other, and solve one polynomial, as in [curve and surface intersection](/curve-surface-intersection/) and [algebraic surface intersection](/algebraic-surface-intersection/). Use it also for exact inside and outside tests and for a symbolic description of the curve. Do not implicitize bicubic or higher patches in a time critical loop, because the degree and the number of coefficients of the result are large. Subdivision or marching methods on the parametric form are then cheaper.

## Pitfalls

- **Base points.** If $X$, $Y$ and $W$ share a root, every $A$ and $B$ share it, and the method returns the zero polynomial. The curve $(t^2 + t) / (t^2 + 3t)$, $(t^2 + 2t) / (t^2 + 3t)$ is an example; dividing by $t$ gives a curve of degree $1$.
- **Improper parametrization.** The map $t \mapsto (t^2, t^4)$ covers the parabola $y = x^2$ twice, and the method returns $(y - x^2)^2 = x^4 - 2x^2 y + y^2$. Take the square free part of the result, or reparametrize first.
- **Formal degree.** If $A$ and $B$ are taken with their actual degree at each point, the size of the matrix changes from point to point and the values on the grid are not values of one polynomial. Keep the formal degree $d$ for all points.
- **Points not on the segment.** A root of $F$ in an intersection may come from a parameter outside $[0, 1]$ or from the point at infinity. Invert each point found and check its parameter.
- **Floating point.** The coefficients of $F$ can be large, and they cancel on the curve. Computing them in floats, or evaluating a high degree $F$ near the curve in floats, gives a result whose sign is not reliable.

## Implementations

## History

Elimination of variables by resultants is classical algebra, from Sylvester's matrix of 1840 and the work of the nineteenth and early twentieth centuries on the resultants of several polynomials. Sederberg, Anderson and Goldman (1984) brought these tools into geometric modeling: they showed that every rational curve and surface has an implicit equation found by a resultant, with the degrees above, and used it to reduce intersections to polynomials in one variable. Sederberg and Chen (1995) introduced moving lines and moving surfaces, which give the same equations from smaller determinants, and they applied the surface version to the bicubic patches of the Utah teapot. Gröbner basis methods and approximate implicitization are later alternatives.

## References
