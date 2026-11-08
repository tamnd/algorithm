---
tag: Y6MJH2
kind: concept
slug: smoothing-spline
name: Smoothing spline
aliases:
- Penalized regression spline
- Cubic smoothing spline
- Reinsch spline
area: numerical/interpolation-and-approximation
level: advanced
summary: Spline that trades off fit to noisy data against roughness, controlled by a smoothing parameter. The minimizer is a natural cubic spline with knots at the data, found in O(n) operations.
prereqs: [cubic-spline-interpolation, least-squares-problem]
see_also: [curve-fitting, b-spline, radial-basis-function-interpolation, kriging, least-squares-approximation, scattered-data-interpolation, spline-evaluation]
sources:
  - paper: "Isaac J. Schoenberg, Spline functions and the problem of graduation, Proceedings of the National Academy of Sciences 52 (1964) 947-950"
    locator: the minimizer of the penalized least-squares functional is a natural spline
  - paper: "Christian H. Reinsch, Smoothing by spline functions, Numerische Mathematik 10 (1967) 177-183"
    locator: the banded linear algebra that computes the smoothing spline in O(n) operations
  - paper: "Peter Craven and Grace Wahba, Smoothing noisy data with spline functions, Numerische Mathematik 31 (1979) 377-403"
    locator: generalized cross-validation for choosing the smoothing parameter
  - book: isbn:9780898712445
    title: Grace Wahba, Spline Models for Observational Data, SIAM, 1990
    locator: Chapter 1, Background (smoothing splines in reproducing kernel Hilbert spaces and the Bayesian interpretation), and Chapter 4, Estimating the smoothing parameter
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter XIV, Smoothing and least-squares approximation (the smoothing spline of Schoenberg and Reinsch)
---

A smoothing spline fits a smooth curve to noisy data by balancing two goals: stay close to the data, and do not bend too much. For the classical cubic smoothing spline the balance is a single number, the smoothing parameter $\lambda$. Remarkably, among all twice-differentiable functions the best compromise is always a natural cubic spline with knots at the data abscissae, and it can be computed in time linear in the number of data points. At $\lambda = 0$ it is the interpolating spline, and as $\lambda \to \infty$ it becomes the least-squares straight line.

## In plain words

When measurements are noisy, a curve that passes exactly through every point wiggles to follow the noise. A smoothing spline instead looks for a curve that stays near the points but is charged a price for bending. A small price gives a curve that hugs the data; a large price gives a curve that is nearly straight.

The amount of smoothing is one knob. It can be set by hand, or chosen automatically by checking how well the curve, fitted without one data point, predicts that point. The best curve turns out to be made of cubic pieces joined smoothly at the data points, so it is fast to compute.

## The idea

Notation on the interpolation pages: data $(x_i, y_i)$, $i = 1, \ldots, n$, with $a \le x_1 < \cdots < x_n \le b$ and $n \ge 3$; weights $w_i > 0$ (often 1); a spline $s$ has degree $k$ and knots $t_j$; $W^{2,2}[a, b]$ is the space of functions with square-integrable second derivative.

**The functional.** For $\lambda > 0$ minimize
$$J_\lambda(g) = \sum_{i=1}^{n} w_i\, \big(y_i - g(x_i)\big)^2 + \lambda \int_a^b g''(x)^2\, dx$$
over $g \in W^{2,2}[a, b]$. The first term measures the fit, the second the roughness (the linearized bending energy of a thin beam).

**Theorem (Schoenberg 1964; Reinsch 1967).** $J_\lambda$ has a unique minimizer $s_\lambda$, and it is a natural cubic spline with knots $x_1, \ldots, x_n$: a cubic polynomial on each $[x_i, x_{i+1}]$, twice continuously differentiable, and linear on $[a, x_1]$ and $[x_n, b]$.

*Why.* Given any $g$, let $s$ be the natural cubic spline that interpolates $g$ at the $x_i$. The fit terms of $g$ and $s$ are equal, and the natural spline has the least $\int (g'')^2$ among all interpolants of the same values (integrate $\int s''(g - s)''$ by parts: it vanishes because $s'''$ is piecewise constant, $s''$ vanishes at the ends and $g - s$ vanishes at the knots). So the search reduces to natural cubic splines, a space of dimension $n$, where $J_\lambda$ is a positive definite quadratic form.

**Computation (Reinsch).** Write $g_i = s(x_i)$ and $\gamma_i = s''(x_i)$ with $\gamma_1 = \gamma_n = 0$. With $h_i = x_{i+1} - x_i$, define the $n \times (n - 2)$ tridiagonal matrix $Q$ with entries $1/h_{j-1}$, $-1/h_{j-1} - 1/h_j$, $1/h_j$ in column $j$, and the $(n - 2) \times (n - 2)$ symmetric tridiagonal $R$ with diagonal $(h_{j-1} + h_j)/3$ and off-diagonal $h_j/6$. A vector $g$ and $\gamma$ define a natural cubic spline exactly when $Q^T g = R \gamma$, and then $\int (s'')^2 = \gamma^T R \gamma$. Minimizing gives
$$\big(R + \lambda\, Q^T W^{-1} Q\big)\, \gamma = Q^T y, \qquad g = y - \lambda\, W^{-1} Q \gamma.$$
The matrix is symmetric positive definite and pentadiagonal, so a banded Cholesky factorization solves it in $O(n)$ operations.

**Linear smoother.** $g = S_\lambda y$ with the hat matrix $S_\lambda = (W + \lambda Q R^{-1} Q^T)^{-1} W$. Its trace, the **effective degrees of freedom**, decreases from $n$ (interpolation) to 2 (a straight line) as $\lambda$ grows. Each fitted value is a weighted average of the data with an equivalent kernel whose width scales like $\lambda^{1/4}$ (Silverman 1984).

**Choosing $\lambda$.** Generalized cross-validation (Craven and Wahba 1979) minimizes
$$\mathrm{GCV}(\lambda) = \frac{n\, \sum_i w_i (y_i - g_i)^2}{\big(n - \operatorname{tr} S_\lambda\big)^2},$$
which approximates leave-one-out prediction error and needs no estimate of the noise variance. Alternatives: Mallows' $C_p$ with known variance, restricted maximum likelihood, or the discrepancy principle $\sum (y_i - g_i)^2 \approx n \sigma^2$ (Reinsch's original form, which fixes the residual instead of $\lambda$).

**Interpretations.**

- **Bayesian (Wahba 1978):** $s_\lambda$ is the posterior mean when $g$ is a (partially improper) integrated Wiener process prior and the noise is Gaussian, with $\lambda$ the ratio of noise to signal variance.
- **Kernel:** $s_\lambda$ is a regularized interpolant in a reproducing kernel Hilbert space; in several variables the thin-plate smoothing spline is the [RBF](/radial-basis-function-interpolation/) system with $A + \lambda I$.
- **Penalized regression splines (P-splines):** use fewer knots than data, a [B-spline](/b-spline/) basis and a difference penalty; cheaper for large $n$ and nearly the same fit.

## Examples

**A noisy sine.** Take $n = 50$ random abscissae in $[0, 1]$ (seed 7), $y_i = \sin(2\pi x_i) + \varepsilon_i$ with $\varepsilon_i$ normal of standard deviation $0.2$, and unit weights. The root mean square error of the raw data against the true function is $0.218$. For the smoothing spline:

| $\lambda$ | degrees of freedom | residual sum of squares | GCV | RMS error against $\sin(2\pi x)$ |
|---|---|---|---|---|
| $10^{-8}$ | 43.6 | 0.21 | 0.247 | 0.198 |
| $10^{-6}$ | 25.1 | 0.89 | 0.072 | 0.139 |
| $10^{-5}$ | 15.9 | 1.52 | 0.065 | 0.101 |
| $10^{-4}$ | 9.7 | 1.91 | 0.059 | 0.078 |
| $10^{-3}$ | 6.0 | 2.17 | 0.056 | 0.083 |
| $10^{-2}$ | 3.9 | 3.74 | 0.088 | 0.214 |
| $1$ | 2.1 | 9.10 | 0.198 | 0.413 |

Small $\lambda$ follows the noise, large $\lambda$ flattens the sine toward the least-squares line (whose RMS error is $0.419$). GCV, minimized over this list, picks $\lambda = 10^{-3}$, close to the best value $10^{-4}$ in true error, and reduces the error to about $0.38$ times that of the raw data.

**Limits.** At $\lambda \to 0$ the system becomes $R\gamma = Q^T y$, the equations of the natural interpolating [cubic spline](/cubic-spline-interpolation/). As $\lambda \to \infty$, $Q^T g \to 0$ forces $g$ to be linear, and the fit term makes it the weighted least-squares line.

## Where it is used

- Nonparametric regression and data smoothing in statistics (the `smooth.spline` type of routine), including generalized additive models built from one smoothing spline per variable.
- Smoothing experimental and observational data before differentiation, for example velocities from noisy positions; the second derivative of $s_\lambda$ is continuous.
- Growth curves, dose-response curves and time series trends; the Hodrick-Prescott filter in economics is a discrete analogue.
- Geodesy and meteorology through thin-plate smoothing splines in two and three variables, and through their equivalence with [kriging](/kriging/).
- As a regularization template: the same "fit plus penalty" structure underlies Tikhonov regularization and kernel ridge regression.

## References
