---
tag: 4TBMTK
kind: algorithm
slug: taubin-fitting
name: Taubin's gradient-weighted fitting
aliases:
- Taubin fit
- gradient-weighted algebraic fit
area: cad/reverse-engineering-and-inspection
level: advanced
summary: Taubin's fit of implicit curves and surfaces that divides the algebraic error by the gradient norm, one generalized eigenproblem whose answer is close to the geometric fit.
solves: [curve-fitting]
model: real-ram
complexity:
  vars: {m: the number of points, n: the number of basis functions, d: the dimension of the space, s: the number of Jacobi sweeps}
  time: {worst: Θ(m n² d + s n³)}
  space: {extra: Θ(n²)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1991
  people: [Gabriel Taubin]
  note: He replaced the algebraic distance by its quotient with the gradient norm, and the mean of these quotients by a quotient of means, which turns the fit into one generalized eigenproblem.
prereqs: [algebraic-distance-fitting, generalized-eigenvalue-problem, implicit-surface]
see_also: [geometric-primitive-fitting, circle-fitting, least-squares-reference-feature, cholesky-decomposition, jacobi-eigenvalue-algorithm, rayleigh-quotient, efficient-ransac-shape-detection, errors-in-variables-regression]
sources:
  - paper: doi:10.1109/34.103273
    title: Gabriel Taubin, Estimation of planar curves, surfaces, and nonplanar space curves defined by implicit equations with applications to edge and range image segmentation, IEEE Transactions on Pattern Analysis and Machine Intelligence 13(11), 1991, 1115 to 1138
    locator: the first-order approximation of the distance to an implicit curve or surface, the approximate mean square distance as a quotient, its minimization as a generalized eigenproblem, and the use in segmentation
  - paper: "Paul D. Sampson, Fitting conic sections to very scattered data, an iterative refinement of the Bookstein algorithm, Computer Graphics and Image Processing 18(1), 1982, 97 to 108"
    title: Paul D. Sampson, Fitting conic sections to very scattered data, an iterative refinement of the Bookstein algorithm, Computer Graphics and Image Processing 18(1), 1982, 97 to 108
    locator: the algebraic distance divided by the gradient norm as an approximate distance for conics, minimized by reweighted algebraic fits
  - book: isbn:9781439835906
    title: Nikolai Chernov, Circular and Linear Regression, Fitting Circles and Lines by Least Squares, CRC Press, 2010
    locator: the Taubin circle fit, its comparison with the Kasa and Pratt fits, and the statistical analysis of the bias of algebraic circle fits
---

Taubin's fit is an algorithm that fits an implicit curve or surface $f(x) = 0$, with $f$ linear in its coefficients, to data points by minimizing the *first-order distance* $\lvert f(x) \rvert / \lvert \nabla f(x) \rvert$ in an averaged form. The plain [algebraic fit](/algebraic-distance-fitting/) minimizes $\sum_i f(x_i)^2$, whose terms are the squared distances weighted by $\lvert \nabla f \rvert^2$, so its answer depends on how $f$ is scaled and is biased. Dividing each algebraic distance by the gradient removes that weight to first order, because $\lvert f(x) \rvert / \lvert \nabla f(x) \rvert$ equals the Euclidean distance from $x$ to the curve up to an error of order $\delta^2$. Taubin then divides the sum of the $f(x_i)^2$ by the sum of the $\lvert \nabla f(x_i) \rvert^2$, not term by term. Both sums are quadratic forms in the coefficient vector $a$, so the minimum is the smallest eigenvalue of one [generalized eigenvalue problem](/generalized-eigenvalue-problem/) $M a = \lambda N a$, solved directly without iteration. The fit returns the exact curve on noise-free data, it is invariant under rotations, translations and scaling, and its bias is much smaller than that of the plain algebraic fit. It is still not the [geometric fit](/geometric-primitive-fitting/), which minimizes the orthogonal distances themselves and needs iteration, and it is the usual starting point for that fit.

## In plain words

To fit a curve to points, a simple method uses a formula that is zero on the curve and asks the formula to be close to zero at every point. The number that the formula gives is not a distance, though. Where the formula changes fast, a point near the curve already gets a large number, and where it changes slowly, a point far from the curve gets a small one.

Taubin's idea is to divide by how fast the formula changes there. Near the curve, the result is almost the true distance. He also divides the total of the values by the total of the rates, and not each value by its own rate, so the best curve can be found in one step of linear algebra. The result is nearly as good as a fit with true distances, which needs a slower search.

## The problem

The input is $m$ points $x_1, \dots, x_m$ in $\mathbb{R}^d$ and a family of [implicit curves or surfaces](/implicit-surface/) $f_a(x) = \sum_{j=1}^{n} a_j \varphi_j(x) = 0$, given by $n$ linearly independent polynomial basis functions $\varphi_j$: the six monomials $x^2, xy, y^2, x, y, 1$ for conics, $\lvert x \rvert^2, x_1, \dots, x_d, 1$ for circles and spheres, all monomials up to degree $k$ for implicit polynomials. The output is a unit coefficient vector $a$ that minimizes Taubin's approximate mean square distance
$$ q(a) = \frac{\sum_i f_a(x_i)^2}{\sum_i \lvert \nabla f_a(x_i) \rvert^2} , $$
and the minimum value. This is one choice of the normalization in the template of [algebraic distance fitting](/algebraic-distance-fitting/): the constraint $a^{\mathsf T} N a = 1$ with $N$ built from the gradients at the data. It is a solution method for one form of [curve fitting](/curve-fitting/).

## The algorithm

Let $J(x)$ be the $n \times d$ Jacobian of the basis, with row $j$ equal to $\nabla \varphi_j(x)$. Then $f_a(x_i) = \varphi(x_i)^{\mathsf T} a$ and $\nabla f_a(x_i) = J(x_i)^{\mathsf T} a$, so $q(a) = a^{\mathsf T} M a / a^{\mathsf T} N a$ with the two matrices below.

```pseudo id=main
TAUBIN-FIT(x_1..x_m, φ)
L1  M ← 0, N ← 0                                 ▷ n × n
L2  for i ← 1 to m do
L3      M ← M + φ(x_i) φ(x_i)ᵀ
L4      N ← N + J(x_i) J(x_i)ᵀ
L5  split a = (b, c), with c the coefficient of the constant basis function
L6  M' ← M_bb − M_bc M_cb / M_cc                 ▷ c is eliminated
L7  L ← Cholesky factor of N_bb                  ▷ N_bb = L Lᵀ
L8  (λ, y) ← smallest eigenpair of L⁻¹ M' L⁻ᵀ
L9  b ← L⁻ᵀ y,  c ← −M_cb b / M_cc
L10 return a ← (b, c) / |(b, c)| and λ
```

**Why L5 and L6.** The gradient of a constant is $0$, so the row and column of the constant coefficient in $N$ are zero and $N$ is singular. That coefficient appears only in the numerator, as a quadratic in $c$ with leading coefficient $M_{cc} = m$ for the basis function $1$, so the best $c$ for a given $b$ is $-M_{cb} b / M_{cc}$, and what remains of the numerator is the Schur complement $b^{\mathsf T} M' b$. A basis with no constant skips these two lines.

**Why L7 to L9.** $N_{bb}$ is positive definite when no nonconstant member of the family has a zero gradient at all the data points; for conics this holds as soon as three points are not on one line. With the [Cholesky factor](/cholesky-decomposition/) $L$ and $y = L^{\mathsf T} b$, the quotient becomes the ordinary [Rayleigh quotient](/rayleigh-quotient/) $y^{\mathsf T} C y / y^{\mathsf T} y$ of the symmetric matrix $C = L^{-1} M' L^{-\mathsf T}$, whose minimum is the smallest eigenvalue of $C$. The code finds it with the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/); a library would use a symmetric eigensolver or the QZ algorithm on $(M, N)$ directly.

**The distance it minimizes.** Taubin's fit minimizes neither the algebraic distance nor the geometric distance. The first-order distance $\lvert f \rvert / \lvert \nabla f \rvert$ of a point at distance $\delta$ from the curve is $\delta + O(\delta^2)$, so the *Sampson cost* $\sum_i f(x_i)^2 / \lvert \nabla f(x_i) \rvert^2$ is the geometric cost up to higher order terms. Taubin's quotient of sums is a further approximation of the Sampson cost: it treats the gradient as if it had the same size at all data points. The returned $\lambda$ is a weighted mean of the squared first-order distances, with weights $\lvert \nabla f(x_i) \rvert^2$, and serves as an estimate of the mean squared distance.

## Example

**A noise-free ellipse.** The six rational points $(2, 0)$, $(8/5, 3/5)$, $(6/5, 4/5)$, $(0, 1)$, $(-6/5, 4/5)$ and $(6/5, -4/5)$ lie on the ellipse $x^2 + 4y^2 - 4 = 0$. With the conic basis $x^2, xy, y^2, x, y, 1$, the code returns a vector proportional to $(1, 0, 4, 0, 0, -4)$ up to rounding of order $10^{-15}$, with $\lambda \approx 2 \cdot 10^{-17}$. In exact arithmetic the design matrix of these points has a one-dimensional null space spanned by $(1, 0, 4, 0, 0, -4)$, so by Theorem 2 below the fit is exactly this ellipse.

**Short circular arcs.** Twenty points were spaced evenly on an arc of the unit circle and moved by independent normal noise of standard deviation $\sigma$ in each coordinate; $1000$ samples were drawn with seed 2026. The table gives the median radius of the Kasa fit (the algebraic fit with the coefficient of $x^2 + y^2$ fixed), of the Taubin fit with the circle basis, and of the geometric fit ([Gauss-Newton](/gauss-newton-algorithm/) started at the Kasa circle).

| arc | $\sigma$ | Kasa | Taubin | geometric |
| --- | --- | --- | --- | --- |
| $60$ degrees | $0.02$ | $0.868$ | $0.998$ | $0.999$ |
| $60$ degrees | $0.05$ | $0.546$ | $0.992$ | $1.006$ |
| full circle | $0.05$ | $1.002$ | $1.002$ | $1.001$ |

On the short arc the algebraic fit shrinks the circle badly, and the Taubin fit stays close to the geometric fit. On the full circle all three agree.

**An elliptic arc.** Thirty points on the quarter of the ellipse $x^2/4 + y^2 = 1$ in the first quadrant, with normal noise $\sigma = 0.01$ (500 samples, seed 2026): the general conic fit with the normalization $\lvert a \rvert = 1$ returned a curve that is not an ellipse in $358$ samples, and the Taubin fit in $11$. With $\sigma = 0.03$ the counts were $415$ and $138$. The Taubin fit does not force an ellipse; when the type must be an ellipse, the constraint of Fitzgibbon, Pilu and Fisher on the [algebraic fit](/algebraic-distance-fitting/) page does. All numbers in this section are measured on synthetic data.

## Correctness

The proofs are in the correctness file. In outline:

- **First-order distance.** If $y$ is the nearest point of $\{f = 0\}$ to $x$, at distance $\delta$, with $\lvert \nabla f(y) \rvert = g > 0$ and the Hessian of $f$ bounded by $K$ near $y$, then $\bigl| \lvert f(x) \rvert / \lvert \nabla f(x) \rvert - \delta \bigr| \le 3 K \delta^2 / g$ when $K\delta \le g/2$. The proof is a first-order Taylor expansion at $y$, using that $x - y$ is parallel to $\nabla f(y)$.
- **The eigen step.** $q(a) = a^{\mathsf T} M a / a^{\mathsf T} N a$; eliminating the constant gives the Schur complement $M'$, and the change of variables $y = L^{\mathsf T} b$ turns the quotient into a symmetric Rayleigh quotient. So the algorithm returns a global minimizer of $q$, and $M' b = \lambda N_{bb} b$.
- **Exact on noise-free data.** If all points lie on $f_{a^*} = 0$ and they determine the curve (the null space of the design matrix is spanned by $a^*$), then $\lambda = 0$ and the fit returns $\pm a^* / \lvert a^* \rvert$. The tests check this on rational points of ellipses, hyperbolas and circles, with the null space computed in exact arithmetic.
- **Invariance.** For a family closed under similarities, such as all polynomials of degree at most $k$, moving, rotating or scaling the data moves, rotates or scales the fitted curve in the same way, because the cost of $f \circ T^{-1}$ on the moved points is a constant times the cost of $f$.

Not proved here: how close Taubin's quotient of sums is to the Sampson cost, and the size of the statistical bias of the fit. Chernov's book analyses the bias of the circle fits; there the Taubin fit has a much smaller bias than the Kasa fit and a smaller one than the Pratt fit, which matches the measured table.

## Complexity

Building $M$ costs $\Theta(m n^2)$ and building $N$ costs $\Theta(m n^2 d)$. The Cholesky factorization and the two triangular solves of line L8 cost $\Theta(n^3)$, and each Jacobi sweep costs $\Theta(n^3)$, so the total is $\Theta(m n^2 d + s n^3)$ on the [real RAM](/real-ram/), with $s$ sweeps, usually fewer than ten. For a conic $n = 6$ and for a quadric surface $n = 10$, so the cost is linear in the number of points with a small constant. The extra space is $\Theta(n^2)$; the points are read once.

## Properties

- **Direct.** No starting guess and no iteration other than the eigensolver.
- **Exact on exact data**, and invariant under rotations, translations and uniform scaling of the data, for families closed under these maps.
- **Approximate distance.** It minimizes a quotient of sums of algebraic distances and squared gradients, an approximation of the first-order distance, not the geometric distance.
- **Small bias.** Much smaller than the bias of the plain algebraic fit in the measured and the published circle results, but not zero.
- **No type control.** The best member of the family is returned, whatever its type: a hyperbola may fit an elliptic arc, and a circle fit may return a line ($A = 0$).

## Variants and improvements

- **Sampson fit.** Minimize $\sum_i f(x_i)^2 / \lvert \nabla f(x_i) \rvert^2$ itself, by refitting with the weights $1 / \lvert \nabla f_{a_{\text{old}}}(x_i) \rvert^2$ from the previous estimate, or by [Gauss-Newton](/gauss-newton-algorithm/). Sampson did this for conics in 1982.
- **Hyper fit.** A different $N$, found by Al-Sharadqah and Chernov for circles, removes the leading term of the bias; it is in Chernov's book.
- **Geometric fit.** Use the Taubin result as the start of a [Gauss-Newton](/gauss-newton-algorithm/) or [Levenberg-Marquardt](/levenberg-marquardt/) fit of the orthogonal distances, as on the [geometric primitive fitting](/geometric-primitive-fitting/) page.
- **Ellipse-specific fit.** When the curve must be an ellipse, the constraint $4ac - b^2 = 1$ of Fitzgibbon, Pilu and Fisher replaces $N$.
- **Space curves.** Taubin also fits curves in space as the intersection of two implicit surfaces, with the same first-order distance built from both gradients.

## When to use it

Use it for circles, spheres, conics and quadrics when a fast fit without a starting guess is needed and the points may cover only part of the curve, as for fillets, holes and partial cylinders in [reverse engineering](/reverse-engineering-of-geometric-models/) and for the reference features of inspection. Use the plain [algebraic fit](/algebraic-distance-fitting/) only when the points cover the whole curve and speed matters most. Use the [geometric fit](/geometric-primitive-fitting/) after it when the result goes into a dimension or a tolerance check, since standards define those by orthogonal distances.

## Pitfalls

- **A singular $N$.** The constant must be eliminated, as in lines L5 and L6; a general eigensolver on a singular $N$ returns infinite eigenvalues or garbage. Points on a line make $N_{bb}$ singular for conics, and the code raises an error.
- **Wrong type of curve.** The fit may return a hyperbola for an elliptic arc, or a pair of lines. Check the type before use.
- **Outliers.** One point far from the curve can dominate both sums. Remove outliers first, for example by [RANSAC](/ransac/).
- **Conditioning.** As with every polynomial fit, center and scale the data before forming $M$ and $N$; the invariance theorem says the answer does not change in exact arithmetic, but rounding does.
- **Reading $\lambda$ as an error.** $\lambda$ is a weighted mean of squared first-order distances, not the mean or the largest geometric distance. For a tolerance check compute the true distances.

## Implementations

## History

Bookstein fitted conics by algebraic distance in 1979, and Sampson in 1982 proposed dividing the algebraic distance by the gradient norm and refining Bookstein's fit iteratively with this weight. Taubin's 1991 paper took the same first-order distance for implicit curves and surfaces of any degree and for space curves, and observed that replacing the mean of the quotients by a quotient of means turns the fit into a single generalized eigenproblem; he used it to segment edge maps and range images. Chernov and coworkers later analysed the statistical bias of the algebraic circle fits and found that the Taubin fit has a much smaller bias than the Kasa fit and a smaller one than the Pratt fit, and Al-Sharadqah and Chernov derived the hyper fit, which removes the leading bias term.

## References
