---
tag: BHNQV4
kind: problem
slug: curve-fitting
name: Curve fitting
aliases:
- Data fitting
- Regression fitting
- least-squares curve approximation
- model fitting
area: numerical/interpolation-and-approximation
level: intro
summary: Given data points, often noisy, choose a curve from a model family and a fit criterion (interpolation, least squares, robust or smoothing) so that it shows the trend behind the data.
prereqs: [least-squares-approximation, interpolation-problem]
see_also: [least-squares-approximation, interpolation-problem, smoothing-spline, cubic-spline-interpolation, linear-regression, b-spline-fitting, isotonic-regression, function-approximation]
sources:
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 4.3, The least squares approximation problem, and Section 3.7, Piecewise polynomial interpolation
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter XIV, Smoothing and least-squares approximation
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Chapter 5, Orthogonalization and least squares
  - book: isbn:9780521880688
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Chapter 15, Modeling of data (least squares as maximum likelihood, general linear least squares, nonlinear models and robust estimation)
---

Curve fitting is the problem of choosing a curve from a model family so that it represents a set of data points $(x_i, y_i)$, usually measured with noise. The choice has two parts: the family (lines, polynomials, splines, a physical model with a few parameters) and the criterion (pass through each point, as in the [interpolation problem](/interpolation-problem/), or minimize a measure of the misfit, as in [least-squares approximation](/least-squares-approximation/)). When the data are noisy, the aim is the trend behind the data, and a curve that fits the points too closely is worse, not better.

## In plain words

You have measured something at several points and you want a curve that shows how it behaves. If the measurements are exact, you can ask for a curve that passes through every point. Measured data have errors, though, so a curve through every point follows the errors too and can wiggle wildly between the points.

The usual approach is to pick a simple shape with a few free numbers, such as a line or a gentle curve, and to set the numbers so that the misses at the points are small overall. The skill is in the choice of shape. Too simple a shape misses the real trend. Too flexible a shape copies the noise. A good fit lies between the two.

## Definition

Notation on the interpolation and approximation pages: the data are $(x_i, y_i)$ for $i = 1, \ldots, m$, with $x_i$ in an interval $[a, b]$; $\mathcal{P}_n$ is the set of polynomials of degree at most $n$; a spline $s$ of degree $k$ has knots $t_j$.

**Input.** Data points $(x_i, y_i)$, optional weights $w_i > 0$ (often $w_i = 1/\sigma_i^2$ for a noise of standard deviation $\sigma_i$); a model family $\{g(\cdot\,; \theta) : \theta \in \Theta\}$; and a loss $\rho$.

**Output.** Parameters $\hat\theta$ that minimize the total misfit
$$\Phi(\theta) = \sum_{i=1}^{m} w_i\, \rho\big(y_i - g(x_i; \theta)\big),$$
possibly plus a penalty $\lambda R(\theta)$ on the roughness or size of the model.

The common cases are $\rho(r) = r^2$ (least squares), $\rho(r) = |r|$ (least absolute deviations), the Huber loss (quadratic for small $|r|$, linear for large $|r|$), and the limit $\max_i w_i |r_i|$ (minimax, the discrete form of [minimax approximation](/minimax-approximation/)). Interpolation is the case where the family has $m$ free parameters and $\Phi(\hat\theta) = 0$ is required. When $g$ is linear in $\theta$, $g(x; \theta) = \sum_j \theta_j \varphi_j(x)$, the least-squares case is the matrix [least-squares problem](/least-squares-problem/) $\min \|W^{1/2}(A\theta - y)\|_2$ with $A_{ij} = \varphi_j(x_i)$.

## Variants

- **Linear in the parameters**: polynomials, splines with fixed knots, trigonometric sums. One QR factorization solves the least-squares fit; see [least-squares approximation](/least-squares-approximation/) and [B-spline fitting](/b-spline-fitting/).
- **Nonlinear in the parameters**: exponentials $c_0 e^{c_1 x}$, Gaussians, rational functions. The fit needs an iteration (Gauss and Newton steps, with a damping as in the Levenberg and Marquardt method) and can have several local minima.
- **Smoothing**: minimize $\sum_i w_i (y_i - s(x_i))^2 + \lambda \int (s'')^2$ over all smooth $s$; the minimizer is a natural cubic spline, the [smoothing spline](/smoothing-spline/). The parameter $\lambda$ trades fit against roughness, from interpolation ($\lambda \to 0$) to the least-squares line ($\lambda \to \infty$).
- **Shape constraints**: monotone fits ([isotonic regression](/isotonic-regression/), [monotone cubic interpolation](/fritsch-carlson-monotone-interpolation/)), convex fits, positive fits.
- **Errors in both coordinates**: orthogonal distance regression and total least squares measure the misfit perpendicular to the curve.
- **Parametric curves**: points in the plane or in space with no natural $x$; fit $(x(u), y(u))$ with a parameter $u$ chosen from the chord lengths, as with [B-spline fitting](/b-spline-fitting/) and [curve interpolation](/curve-interpolation/) in graphics.
- **Statistical view**: with independent Gaussian noise, least squares is maximum likelihood, and the fit comes with confidence intervals; this is [linear regression](/linear-regression/).

## Examples

**Choosing the degree.** Take $x_i = i/9$ for $i = 0, \ldots, 9$ and $y_i = 1 + 2x_i - x_i^2 + e_i$, with the noise
$$e = (-0.013,\ 0.026,\ -0.011,\ -0.016,\ -0.047,\ -0.011,\ 0.056,\ 0.021,\ 0.052,\ 0.012).$$
Least-squares fits in $\mathcal{P}_n$ give:

| degree $n$ | residual sum of squares | max distance from $1 + 2x - x^2$ on $[0, 1]$ |
|---|---|---|
| 1 | 0.0755 | 0.177 |
| 2 | 0.00699 | 0.041 |
| 3 | 0.00587 | 0.033 |
| 5 | 0.00220 | 0.049 |
| 9 | 0 (interpolation) | 0.154 |

The quadratic fit has the coefficients $0.996, 1.967, -0.923$, close to the true $1, 2, -1$. The residual sum falls with every added degree and reaches 0 at degree 9, where the fit interpolates the noisy points; but the distance from the true curve is smallest near degree 2 or 3 and grows again after that. The coefficients of the degree 9 fit are large and of mixed sign (the coefficient of $x^3$ is about 528 and that of $x^5$ about 3130), a common sign of overfitting.

**A robust fit.** For the points $(0, 0), (1, 1), (2, 2), (3, 3), (4, 10)$, the least-squares line is $y = -1.2 + 2.2x$, pulled up by the outlier at $x = 4$; the least absolute deviations fit $y = x$ passes through the four good points and leaves a single residual of 6.

**A non-example.** A cubic spline through 1000 noisy points is a valid interpolant, but as a curve fit it reproduces the noise: its second derivative is large, and its values between points are not a better estimate of the trend than the raw data. Use a [smoothing spline](/smoothing-spline/) instead.

## Known algorithms

- Linear least squares by [Householder QR](/qr-decomposition/) in $O(m n^2)$, or by orthogonal polynomials on the data points in $O(mn)$ for polynomial fits; see [least-squares approximation](/least-squares-approximation/).
- [Normal equations](/normal-equations/), acceptable only for a well-conditioned basis.
- [Cubic spline interpolation](/cubic-spline-interpolation/) in $O(m)$ for exact data, and [smoothing splines](/smoothing-spline/) in $O(m)$ by a banded solve (the Reinsch algorithm).
- [Isotonic regression](/isotonic-regression/) by the pool adjacent violators algorithm in $O(m)$.
- Robust fits: least absolute deviations as a linear program, and iteratively reweighted least squares for the Huber loss.

## Bounds

For a linear model with $n + 1$ parameters, the dense least-squares fit costs $\Theta(m n^2)$ by QR, and at least $\Omega(mn)$ to read the design matrix. The statistical error of a least-squares fit with independent noise of variance $\sigma^2$ is $\sigma^2 (A^T W A)^{-1}$ for the parameters (the Gauss and Markov theorem). The bias of a fit of degree $n$ to a smooth trend is bounded by the best approximation error $E_n$ of the trend; the variance grows with $n$. This trade-off has no general closed-form optimum, and in practice the degree or $\lambda$ is chosen by cross-validation or a statistical criterion.

## Reductions

- Linear least-squares fitting reduces to an orthogonal factorization and a [triangular solve](/back-substitution/).
- Discrete minimax and $L^1$ fitting reduce to linear programming.
- Interpolation is the special case of a zero residual with as many parameters as points.

## Applications

- Calibration curves in laboratories, and physical laws with unknown constants (decay rates, growth rates).
- Trend estimation in time series and in economics, and [linear regression](/linear-regression/) in statistics.
- Computer graphics and CAD: fitting spline curves and surfaces to scanned points.
- Building surrogate models of expensive computations.

## References
