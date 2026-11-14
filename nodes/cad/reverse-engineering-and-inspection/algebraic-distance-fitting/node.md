---
tag: K7A2W9
kind: technique
slug: algebraic-distance-fitting
name: Algebraic distance fitting
aliases:
- algebraic fit
area: cad/reverse-engineering-and-inspection
level: core
summary: Fits an implicit curve or surface by least squares of its values at the data points, a linear problem that is exact on noise-free data but biased under noise.
prereqs: [least-squares-approximation, implicit-surface, singular-value-decomposition]
see_also: [taubin-fitting, geometric-primitive-fitting, circle-fitting, least-squares-reference-feature, generalized-eigenvalue-problem, errors-in-variables-regression, curve-fitting, principal-component-analysis]
sources:
  - paper: doi:10.1016/0146-664X(79)90082-0
    title: Fred L. Bookstein, Fitting conic sections to scattered data, Computer Graphics and Image Processing 9(1), 1979, 56 to 71
    locator: the least squares fit of a general conic by its algebraic distance, with the quadratic normalization that is invariant under Euclidean motions
  - paper: doi:10.1145/37402.37420
    title: Vaughan Pratt, Direct least-squares fitting of algebraic surfaces, Computer Graphics 21(4) (SIGGRAPH 87), 1987, 145 to 152
    locator: the algebraic fit of implicit curves and surfaces as an eigenvector problem, and the normalization for circles and spheres
  - paper: doi:10.1109/34.765658
    title: Andrew Fitzgibbon, Maurizio Pilu and Robert B. Fisher, Direct least square fitting of ellipses, IEEE Transactions on Pattern Analysis and Machine Intelligence 21(5), 1999, 476 to 480
    locator: the normalization 4ac - b^2 = 1, which makes the algebraic fit return an ellipse, solved as a generalized eigenproblem
  - book: isbn:9781439835906
    title: Nikolai Chernov, Circular and Linear Regression, Fitting Circles and Lines by Least Squares, CRC Press, 2010
    locator: the chapters on the algebraic circle fits (Kasa, Pratt, Taubin, hyper) and on the statistical bias of these fits
---

Algebraic distance fitting fits an implicit curve or surface $f(x) = 0$ to data points by choosing the coefficients of $f$ that make $\sum_i f(x_i)^2$ smallest. The value $f(x_i)$ is the *algebraic distance* of the point $x_i$. It is zero exactly when the point is on the curve, but it is not the Euclidean distance from the point to the curve. Because $f$ is linear in its coefficients, the fit is a linear [least squares](/least-squares-approximation/) problem or a small eigenvalue problem, with no iteration and no starting guess. That makes it the usual first step for conics, circles, spheres, quadrics and higher degree implicit polynomials. On points that lie exactly on a curve of the family, the fit returns that curve. On noisy points it does not minimize the geometric distance, and its answer is biased: it depends on how the coefficients are normalized, and for circles on short arcs it is pulled toward circles that are too small. The two fixes are the [Taubin fit](/taubin-fitting/), which divides by the gradient and minimizes a first-order distance, and the [geometric fit](/geometric-primitive-fitting/), which minimizes the orthogonal distance itself.

## In plain words

A curve can be described by a formula that gives zero on the curve and some other number off it. To fit such a curve to measured points, choose the formula so that its values at the points are as close to zero as possible. This is easy to compute.

The catch is that the value of the formula at a point is not the distance from the point to the curve. Some points count more than others, depending on where they are and on the size of the curve. For a circle, the value grows with the radius, so the method likes small circles. When the points cover only a short piece of a circle and have some noise, it returns a circle that is clearly too small. It is a good first guess, and a method that uses true distances should then improve it.

## When it applies

- The model is an [implicit curve or surface](/implicit-surface/) $f(x) = \sum_{j=1}^{n} a_j \varphi_j(x) = 0$ that is linear in its coefficients $a = (a_1, \dots, a_n)$, for fixed basis functions $\varphi_j$ such as monomials. Circles, spheres, conics, quadrics and implicit polynomials of any degree have this form; a cylinder of fixed radius in a general position does not.
- The data are points $x_1, \dots, x_m$ in the plane or in space, with $m \ge n - 1$, sampled near one curve or surface. Segmentation into one region per model comes first; see [primitive segmentation](/primitive-segmentation/).
- A fast, direct answer is needed: as the final result when the noise is small and the points cover the whole curve, or as the starting point of an iterative [geometric fit](/geometric-primitive-fitting/).
- It does not apply when outliers are present: a single far point can dominate the sum of squares. Then [RANSAC](/ransac/) or another robust method selects the inliers first.

## The template

Write $\varphi(x) = (\varphi_1(x), \dots, \varphi_n(x))$ for the vector of basis functions. Then $f(x_i) = a^{\mathsf T} \varphi(x_i)$, and the sum of squares is $\lVert D a \rVert^2 = a^{\mathsf T} M a$ with the design matrix $D$ of rows $\varphi(x_i)^{\mathsf T}$ and $M = D^{\mathsf T} D$.

```pseudo id=main
ALGEBRAIC-FIT(x_1..x_m, φ, normalization)
L1  for i ← 1 to m do D[i] ← φ(x_i)
L2  M ← Dᵀ D
L3  if normalization fixes one coefficient, a_k = 1 then
L4      solve the normal equations of the other coefficients
L5  else if normalization is |a| = 1 then
L6      a ← unit eigenvector of the smallest eigenvalue of M
L7  else normalization is aᵀ N a = 1 for a fixed symmetric N
L8      a ← eigenvector of M a = λ N a with the smallest λ ≥ 0, scaled to aᵀ N a = 1
L9  return the curve aᵀ φ(x) = 0
```

The holes are the basis $\varphi$, which fixes the family of curves, and the normalization, which fixes the answer under noise.

**Why a normalization is needed.** The coefficients $a$ and $c\,a$ for $c \ne 0$ give the same curve, and $a = 0$ gives a sum of squares of $0$ but no curve. A constraint must rule out $a = 0$ and fix the scale. The three common kinds are lines L3 to L8.

**Line L4.** With $a_k = 1$ the cost is $\lVert D' a' + d_k \rVert^2$, where $d_k$ is column $k$ of $D$ and $D'$ holds the other columns. This is an ordinary linear least squares problem, solved by the normal equations $D'^{\mathsf T} D' a' = -D'^{\mathsf T} d_k$ or by a QR factorization.

**Lines L6 and L8.** A stationary point of $a^{\mathsf T} M a$ subject to $a^{\mathsf T} N a = 1$ satisfies $M a = \lambda N a$ by a [Lagrange multiplier](/lagrange-multiplier/). Multiply by $a^{\mathsf T}$: the cost at that point is $a^{\mathsf T} M a = \lambda\, a^{\mathsf T} N a = \lambda$. So the minimum is the eigenvector of the smallest admissible eigenvalue of the [generalized eigenvalue problem](/generalized-eigenvalue-problem/), and for $N = I$ it is the smallest eigenvector of $M$, which is the last right singular vector of $D$ in the [singular value decomposition](/singular-value-decomposition/). The SVD of $D$ is the better way to compute it, because forming $M$ squares the condition number. The ratio $a^{\mathsf T} M a / a^{\mathsf T} N a$ is a generalized [Rayleigh quotient](/rayleigh-quotient/).

**Exact on noise-free data.** If every $x_i$ lies on the curve $a^{*\mathsf T} \varphi(x) = 0$, then $D a^* = 0$, so the cost $0$ is reached at $a^*$, scaled to meet the normalization (for L4 this needs $a^*_k \ne 0$; for L8 it needs $a^{*\mathsf T} N a^* > 0$). Every minimizer has $D a = 0$. The answer is unique up to scale exactly when the null space of $D$ has dimension $1$, that is, when the points fix the curve: three points not on a line for a circle, five points in general position for a conic.

**What it minimizes, and why it is biased.** The cost is a sum of algebraic distances. To first order, $f(x) \approx \lVert \nabla f(x) \rVert\, \delta(x)$, where $\delta(x)$ is the signed geometric distance to the curve; the proof is on the [Taubin fit](/taubin-fitting/) page. So the algebraic fit is a geometric fit in which point $i$ has the weight $\lVert \nabla f(x_i) \rVert^2$, and that weight depends both on where the point is and on the unknown curve. For a circle the relation is exact. With $f(x) = \lVert x - c \rVert^2 - r^2$ (the coefficient of $x^2 + y^2$ fixed at $1$, the Kasa fit) and $\delta = \lVert x - c \rVert - r$,
$$ f(x) = (\lVert x - c \rVert - r)(\lVert x - c \rVert + r) = \delta\,(\delta + 2r), $$
so the Kasa cost is $\sum_i \delta_i^2 (\delta_i + 2r)^2 \approx 4 r^2 \sum_i \delta_i^2$ when the $\delta_i$ are small against $r$. For the same geometric residuals, a smaller circle has a smaller cost. When the points cover the whole circle, shrinking the circle increases the residuals quickly and the effect is small. On a short arc, a smaller circle through the arc changes the residuals only a little, and the fit returns a circle that is too small. For the ellipse $x^2/a^2 + y^2/b^2 - 1 = 0$ with $a > b$, a point at geometric distance $\delta$ outside the vertex $(a, 0)$ has $f = 2\delta/a + \delta^2/a^2$, and a point at distance $\delta$ outside $(0, b)$ has $f = 2\delta/b + \delta^2/b^2$. The same error counts less, by the factor $(b/a)^2$ in the square, at the sharp end of the ellipse than on its flat side. The identity and the two values are exact; the size of the bias under noise is a statistical result, measured below and analysed in Chernov's book.

## Classic examples

- **Plane fitting.** For a plane $f(x) = n \cdot x - d$ with the normalization $\lVert n \rVert = 1$, $\lVert \nabla f \rVert = 1$ everywhere, so the algebraic distance is the geometric distance and the fit has no bias. The optimal $d$ is $n \cdot \bar x$ for the centroid $\bar x$, and $n$ is the eigenvector of the smallest eigenvalue of the covariance matrix of the points, as in [principal component analysis](/principal-component-analysis/). This is the orthogonal regression of [errors-in-variables models](/errors-in-variables-regression/).
- **The Kasa circle and sphere.** $x^2 + y^2 + D x + E y + G = 0$ with the leading coefficient fixed at $1$ (line L4): a $3 \times 3$ linear system. It is invariant under rotations and translations, because its residual depends only on $\lVert x - c \rVert$ and $r$. It is the standard starting point for [circle fitting](/circle-fitting/) and for the [least-squares reference feature](/least-squares-reference-feature/) of a circle in inspection, and it is biased toward small circles on short arcs.
- **The Pratt circle.** For $A(x^2 + y^2) + B x + C y + G = 0$ the radius satisfies $r^2 = (B^2 + C^2 - 4AG)/(4A^2)$, and Pratt's normalization $B^2 + C^2 - 4AG = 1$ is a quadratic constraint of line L8. It allows $A = 0$, so it also fits lines, and it is invariant under rigid motions.
- **Conics.** Bookstein's fit of a general conic $a x^2 + b xy + c y^2 + d x + e y + g = 0$ uses $a^2 + b^2/2 + c^2 = 1$, which is invariant under rotations and translations. The fit may return a hyperbola or a parabola for points from an elliptic arc. Fitzgibbon, Pilu and Fisher use $4ac - b^2 = 1$ instead, an indefinite $N$ in line L8, and the fit then always returns an ellipse.
- **Gradient weighting.** Taubin's choice $N = \sum_i J_i^{\mathsf T} J_i$, with $J_i$ the Jacobian of $\varphi$ at $x_i$, divides the cost by the mean squared gradient and gives the [Taubin fit](/taubin-fitting/), which is close to the first-order distance fit.

**A measured bias.** Twenty points were spaced evenly on an arc of $60$ degrees of the unit circle, and independent normal noise of standard deviation $\sigma$ was added to each coordinate. The Kasa circle (line L4) and the geometric circle ([Gauss-Newton](/gauss-newton-algorithm/) from the Kasa circle) were fitted to $1000$ such samples, with seed 2026.

| arc | $\sigma$ | median Kasa radius | median geometric radius |
| --- | --- | --- | --- |
| $60$ degrees | $0.02$ | $0.868$ | $0.999$ |
| $60$ degrees | $0.05$ | $0.546$ | $1.006$ |
| full circle | $0.05$ | $1.002$ | $1.001$ |

On the short arc the Kasa radius is too small, and more so as the noise grows; on the full circle both are close to $1$. These are runs on synthetic data, not a proof; the expansion of the bias in powers of $\sigma$ is in Chernov's book.

## Variations

- **Fixed coefficient (Kasa, line L4).** The cheapest. It needs the fixed coefficient to be nonzero on the true curve, so the choice of $k$ excludes some curves: fixing the coefficient of $x^2 + y^2$ excludes lines.
- **Unit coefficient vector (line L6).** The smallest singular vector of $D$. It allows every curve of the family, but it is not invariant: the answer changes when the data are moved or scaled.
- **Invariant quadratic constraints (line L8).** Bookstein for conics, Pratt for circles and spheres, Fitzgibbon for ellipses only.
- **Gradient weighted fits.** Taubin's constraint (one generalized eigenproblem), and the iterated version that divides each residual by the gradient at the current estimate, which converges to the first-order (Sampson) distance fit.
- **Hyper fit.** A further choice of $N$ by Al-Sharadqah and Chernov removes the leading term of the bias of the circle fit; it is in Chernov's book.
- **Higher degree implicit polynomials.** The same template with all monomials up to degree $d$. Taubin's 1991 paper treats this case, with the gradient weighting.

## Pitfalls

- **The normalization changes the answer.** Take the seven rational points of the unit circle with $x = 0, \pm 5/13, \pm 8/17, \pm 3/5$ and $y > 0$, and move them radially by $-5\%$ for $x = 0$ and $x = \pm 5/13$ and by $+5\%$ for the others. The $\lvert a \rvert = 1$ fit of $A(x^2 + y^2) + Bx + Cy + G$ gives radius $3.552$; after a shift of the data by $2$ in $x$ and the shift back, $0.952$; after a shift by $10$, $1.228$. The Kasa fit gives $1.250$ for every shift. Use an invariant normalization, or at least center and scale the data first.
- **The family is not the type.** A general conic or quadric fit returns whatever member of the family is best: a hyperbola for an elliptic arc, a pair of planes for a cylinder patch. Constrain the type (Fitzgibbon) or fit the intended primitive directly.
- **Extra branches.** The zero set of a polynomial of degree three or more can have components far from the data, or come close to the data where $\nabla f$ is small. A low cost does not show that the curve looks like the data.
- **Bias on short arcs and small patches.** In reverse engineering, fillets and partial holes are exactly such patches. Refine with a [geometric fit](/geometric-primitive-fitting/) before the radius is used.
- **Conditioning.** Monomials of coordinates in millimeters far from the origin give a badly conditioned $D$. Translate to the centroid and scale to unit size, solve, and transform the coefficients back.
- **Outliers.** Squares of algebraic distances grow faster than squares of distances for far points (by the factor $(\delta + 2r)^2$ for a circle), so one outlier does even more damage than in a geometric fit.

## Exercises

1. Show that the Kasa circle fit gives the same circle after the data are rotated and translated. *Hint:* its residual is $\lVert x - c \rVert^2 - r^2$.
2. For the plane $n \cdot x = d$ with $\lVert n \rVert = 1$, show that minimizing $\sum_i (n \cdot x_i - d)^2$ gives $d = n \cdot \bar x$ and that $n$ is the eigenvector of the smallest eigenvalue of $\sum_i (x_i - \bar x)(x_i - \bar x)^{\mathsf T}$.
3. Find the algebraic distance of the point $(0, 2)$ to the circle $x^2 + y^2 - 1 = 0$, and to the same circle written as $2x^2 + 2y^2 - 2 = 0$. Which one is the geometric distance? *Answer:* $3$ and $6$; neither, the geometric distance is $1$.

## References
