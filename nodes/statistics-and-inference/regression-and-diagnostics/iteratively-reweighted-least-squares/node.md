---
tag: N4YG7R
kind: algorithm
slug: iteratively-reweighted-least-squares
name: Iteratively reweighted least squares
aliases:
- IRLS
- IWLS
area: statistics-and-inference/regression-and-diagnostics
level: core
summary: Solves a sequence of weighted least squares problems whose weights come from the current fit. It fits generalized linear models and robust M-estimators.
model: real-ram
complexity:
  vars: {n: the number of observations, p: the number of columns of X, k: the number of iterations}
  time: {worst: Θ(k n p^2), best: Θ(n p^2)}
  space: {extra: Θ(n p)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1972
  people: [John A. Nelder, Robert W. M. Wedderburn, Paul W. Holland, Roy E. Welsch, Peter J. Green]
  note: Nelder and Wedderburn (1972) fitted all generalized linear models by iterative weighted regression. Holland and Welsch (1977) used the same loop for robust regression, and Green (1984) treated it as a general method for maximum likelihood and its robust variants.
prereqs: [weighted-least-squares, generalized-linear-model, fisher-scoring, newton-raphson-method, m-estimator]
see_also: [logistic-regression, huber-m-estimator, tukey-biweight, quantile-regression, quasi-likelihood, generalized-estimating-equations, mm-estimator, robust-model-fitting]
sources:
  - paper: doi:10.2307/2344614
    title: "J. A. Nelder and R. W. M. Wedderburn, Generalized linear models, Journal of the Royal Statistical Society Series A 135(3), 1972, pp. 370 to 384"
    locator: The whole paper (maximum likelihood for exponential family responses by iterative weighted linear regression)
  - paper: doi:10.1080/03610927708827533
    title: "Paul W. Holland and Roy E. Welsch, Robust regression using iteratively reweighted least-squares, Communications in Statistics, Theory and Methods 6(9), 1977, pp. 813 to 827"
    locator: The whole paper (weight functions for robust regression, their tuning constants and the reweighting loop)
  - paper: doi:10.1111/j.2517-6161.1984.tb01288.x
    title: "P. J. Green, Iteratively reweighted least squares for maximum likelihood estimation, and some robust and resistant alternatives, Journal of the Royal Statistical Society Series B 46(2), 1984, pp. 149 to 192 with the discussion"
    locator: The whole paper (the general form of the iteration, Fisher scoring and Newton steps, robust and resistant alternatives)
  - book: isbn:9780412317606
    title: P. McCullagh and J. A. Nelder, Generalized Linear Models, second edition, Chapman and Hall, 1989
    locator: Chapter 2 (the fitting algorithm with the working response and the iterative weights)
---

Iteratively reweighted least squares turns a hard fitting problem into a sequence of [weighted least squares](/weighted-least-squares/) problems. Each pass computes a weight $w_i$ and a working response $z_i$ for every observation from the current coefficients $b$, then fits $z$ on $X$ with those weights to get the next $b$. With the weights and responses of a [generalized linear model](/generalized-linear-model/) the pass is a [Fisher scoring](/fisher-scoring/) step, and for a canonical link such as the logit it is exactly a [Newton step](/newton-raphson-method/). With the weights of a robust loss, such as Huber's or Tukey's biweight, each pass cannot increase the loss. One routine, a weighted QR solve in a loop, fits logistic, Poisson and probit regression, robust [M-estimators](/m-estimator/) and least absolute deviations.

## In plain words

Many fitting problems would be easy if each point came with the right weight. For a yes or no outcome, points whose predicted chance is near one half carry the most information, but you only know the chances after you have a fit. For a robust line, a point far from the line should count less, but you only know which points are far after you have a line. The method breaks the circle by guessing. Start from some line, compute the weights it implies, fit again with those weights, and repeat. For the models in this page each round moves toward the answer, and a handful of rounds is usually enough.

## The problem

**Input.** A fixed real $n \times p$ design $X$ with rows $x_i^\top$ (the intercept is one of the $p$ columns), a response $y$, and a working rule that maps the response and the current linear predictor $\eta = Xb$ to weights $w_i \ge 0$ and working responses $z_i$.

**Output.** A coefficient vector $\hat b$ at which the weighted fit reproduces itself: fitting $z(\hat b)$ on $X$ with weights $w(\hat b)$ gives $\hat b$ back.

Two families of rules cover most uses:

| problem | objective | working response $z_i$ | weight $w_i$ |
|---|---|---|---|
| GLM with mean $\mu_i = g^{-1}(\eta_i)$, variance function $V$ | maximize the likelihood | $\eta_i + (y_i - \mu_i)g'(\mu_i)$ | $1/(V(\mu_i)g'(\mu_i)^2)$ |
| logistic regression (logit link) | maximize the likelihood | $\eta_i + (y_i - \mu_i)/(\mu_i(1 - \mu_i))$ | $\mu_i(1 - \mu_i)$ |
| Poisson regression (log link) | maximize the likelihood | $\eta_i + (y_i - \mu_i)/\mu_i$ | $\mu_i$ |
| M-estimation, $\rho(r) = f(r^2)$ with $f$ concave | minimize $\sum\rho(y_i - \eta_i)$ | $y_i$ | $f'(r_i^2)$, proportional to $\psi(r_i)/r_i$ |
| Huber loss, threshold $c$, scale $s$ | as above | $y_i$ | $\min(1, cs/\lvert r_i\rvert)$ |
| Tukey biweight, threshold $c$, scale $s$ | as above | $y_i$ | $(1 - (r_i/cs)^2)^2$ inside, $0$ outside |
| least absolute deviations, floor $\delta$ | minimize $\sum\lvert y_i - \eta_i\rvert$ | $y_i$ | $1/\max(\lvert r_i\rvert, \delta)$ |

Here $r_i = y_i - \eta_i$ and $\psi = \rho'$.

## The algorithm

```pseudo id=main
ITERATIVELY-REWEIGHTED-LEAST-SQUARES(X, y, RULE, b⁽⁰⁾, tol, maxit)
L1  b ← b⁽⁰⁾                                       ▷ often 0, or a least squares fit
L2  for k ← 1 to maxit do
L3      η ← X b
L4      (w, z) ← RULE(y, η)                         ▷ weights and working response from the current fit
L5      b⁺ ← argmin_β Σᵢ wᵢ (zᵢ - xᵢᵀβ)²           ▷ weighted least squares by QR of √w-scaled rows
L6      if ‖b⁺ - b‖ ≤ tol · (‖b⁺‖ + tol) then return (b⁺, converged)
L7      b ← b⁺
L8  return (b, not converged)
```

Line L5 is the only heavy step. It solves a weighted least squares problem by a QR factorization of the rows scaled by $\sqrt{w_i}$, as on the weighted least squares page; rows with $w_i = 0$ (the biweight beyond $c$) drop out. For a GLM, line L4 needs $\mu_i = g^{-1}(\eta_i)$, and the implementation keeps $\mu_i$ a small distance away from the boundary of its range so that $w_i$ and $z_i$ stay finite. The dispersion $\phi$ of the GLM cancels and is not needed. For M-estimation the scale $s$ is fixed during the loop; in practice it is a robust scale of a starting fit, such as the median absolute deviation of its residuals.

## Example

**Logistic regression.** Take $x = (1, 2, 3, 4, 5, 6)$, $y = (0, 0, 1, 0, 1, 1)$, and the model $\operatorname{logit}\mu_i = b_0 + b_1x_i$. Start at $b = 0$. Then every $\mu_i = 1/2$, every weight is $1/4$, and $z_i = 4y_i - 2 = (-2, -2, 2, -2, 2, 2)$. With equal weights, line L5 is ordinary least squares of $z$ on $x$: the slope is $14/17.5 = 0.8$ and the intercept $0 - 0.8 \cdot 3.5 = -2.8$. This is exactly the Newton step from $b = 0$. The passes go on:

| $k$ | $b_0$ | $b_1$ | deviance $-2\ell$ |
|---|---|---|---|
| 0 | 0 | 0 | 8.3178 |
| 1 | -2.8000 | 0.8000 | 5.2129 |
| 2 | -3.8842 | 1.1098 | 4.9697 |
| 3 | -4.2214 | 1.2061 | 4.9560 |
| 4 | -4.2489 | 1.2140 | 4.95597 |
| 5 | -4.2491 | 1.2140 | 4.95597 |

The number of correct digits roughly doubles per pass near the end, as for Newton's method; the step test with tolerance $10^{-10}$ stops after 7 passes. At the limit the score $X^\top(y - \mu)$ is zero.

**A robust line.** For $x = 1, \dots, 10$ and $y = (1.1, 2.0, 2.9, 4.2, 5.0, 5.9, 7.1, 8.0, 30.0, 10.1)$, where the ninth point is a gross error, ordinary least squares gives the slope 1.892. Starting from $b = 0$ with the scale fixed at $s = 0.5$, the Huber rule ($c = 1.345$) gives slope 1.040 after 8 passes, the biweight ($c = 4.685$) gives 1.002 after 7 passes with weight 0 on the bad point, and the L1 rule ($\delta = 10^{-6}$) gives 1.0125 after 12 passes. In each run the loss decreased at every pass, as the proof says it must.

## Correctness

Line L5 returns $b^+ = (X^\top WX)^{-1}X^\top Wz$. For a GLM, the score is $U = \phi^{-1}X^\top W\bigl((y_i - \mu_i)g'(\mu_i)\bigr)_i$ and the expected information is $\mathcal I = \phi^{-1}X^\top WX$; substituting $z = \eta + (y - \mu)g'(\mu)$ gives $b^+ = b + \mathcal I^{-1}U$, a Fisher scoring step. For the logit link $W = \operatorname{diag}(\mu_i(1 - \mu_i))$ is also minus the Hessian of the log-likelihood, so the step is Newton's step; the same holds for every canonical link. For a loss $\rho(r) = f(r^2)$ with $f$ concave, the tangent line of $f$ gives a weighted sum of squares that lies above the loss and touches it at the current $b$; line L5 minimizes that upper bound, so the loss cannot increase. The L1 weights with a floor $\delta$ do this exactly for a smoothed absolute loss, and a fixed point is within $n\delta/2$ of the least absolute deviations minimum. The proof gives the details and says what is not proved.

## Complexity

One pass costs $O(np)$ for $\eta$, $O(n)$ for the rule and $\Theta(np^2)$ for the QR of line L5, so $k$ passes cost $\Theta(knp^2)$ time and $\Theta(np)$ extra space. Forming $X^\top WX$ instead of a QR halves the flops of one pass but squares the condition number. There is no useful bound on $k$ in terms of $n$ and $p$. For GLMs with an estimate that exists, 5 to 10 passes are typical; for the L1 rule convergence is linear and can be slow when $\delta$ is tiny. These counts are observed, not proved.

## Properties

- **Fisher scoring in disguise.** For any GLM the iteration is Fisher scoring, and the last $X^\top WX$ divided by $\phi$ is the estimated information. Its inverse gives the usual model-based standard errors.
- **Newton for canonical links.** For the logit, log (Poisson) and identity (normal) links the iteration is Newton's method, which converges quadratically near a maximizer with nonsingular information. The log-likelihood is concave in $b$, so a maximizer is global.
- **Descent for M-estimation.** For Huber, biweight and smoothed L1 the loss sequence is nonincreasing (a majorize-minimize argument). For a convex loss the limit points are minimizers; for the biweight, a redescending loss, they can be local minima, so the start matters.
- **Exact one-step cases.** With the identity link and normal responses, $w_i = 1$ and $z = y$, and the first pass is the least squares fit. With the Huber rule and a threshold larger than every residual, the same happens.
- **Invariance.** Only the ratios of the weights matter, which is why the constant factors of $f'$ and the dispersion $\phi$ can be dropped.

## Variants and improvements

- **Step halving.** If a full GLM step lowers the log-likelihood or leaves the valid range of $\mu$, halve it until it does not. The [generalized linear model](/generalized-linear-model/) page implements this; the version here does not.
- **Quasi-likelihood and estimating equations.** The same loop solves the [quasi-likelihood](/quasi-likelihood/) equations, which need only a mean and a variance function, and the [generalized estimating equations](/generalized-estimating-equations/) for clustered data, where line L5 becomes a block-weighted solve.
- **Robust regression with a robust start.** For a redescending loss, start from a high-breakdown fit such as [least trimmed squares](/least-trimmed-squares/) and keep the scale fixed; this is the [MM-estimator](/mm-estimator/). The [Huber M-estimator](/huber-m-estimator/) and [Tukey's biweight](/tukey-biweight/) pages treat the location case.
- **L1 and quantile regression.** The floored weights approximate least absolute deviations; asymmetric weights approximate [quantile regression](/quantile-regression/). Linear programming solves both exactly and is usually faster.
- **Sparse recovery.** Weights $1/(|b_j| + \varepsilon)$ on the coefficients instead of the residuals give reweighted schemes for $\ell_1$ and $\ell_p$ penalties; the same majorization argument applies.

## When to use it

Use the loop to fit any generalized linear model, to compute M-estimates of regression, and as the inner solver when the objective is a sum of terms that each depend on one residual or one linear predictor. It is short to write given a good weighted least squares routine, and each pass has the numerical quality of a QR solve. For least absolute deviations or quantile regression at scale, prefer a linear programming or interior point method; for very large $n$ or $p$ in a GLM, prefer a first-order or quasi-Newton method that does not factor $X$ each pass.

## Pitfalls

- **Separation.** If a hyperplane separates the 0s from the 1s of a binary response, the logistic likelihood has no maximizer: the deviance goes to 0 as $\lVert b\rVert \to \infty$, the weights $\mu_i(1 - \mu_i)$ go to 0 and the loop never converges. On the data $y = (0, 0, 0, 1, 1, 1)$ with $x = 1, \dots, 6$, after 50 passes $b = (-219, 62.6)$ and every fitted probability is within $10^{-8}$ of 0 or 1. Check for this case instead of reporting the last iterate; [logistic regression](/logistic-regression/) discusses penalized remedies.
- **Zero counts.** A Poisson group whose counts are all 0 sends its coefficient to $-\infty$ in the same way.
- **No step control.** Far from the maximizer, a full Fisher scoring or Newton step can lower the likelihood. Use step halving or start from a sensible fit.
- **The scale in M-estimation.** Huber and biweight weights depend on $r/s$. Re-estimating $s$ inside the loop from the current residuals can break the descent property and, with the biweight, can collapse onto a subset. Fix $s$ from a robust start or update it by a separate rule.
- **Tiny floors.** The L1 rule with a very small $\delta$ gives weights near $1/\delta$ on the points the fit passes through, which makes line L5 badly conditioned and convergence slow.
- **Standard errors.** For robust rules, the final weighted least squares covariance $s^2(X^\top WX)^{-1}$ is not the covariance of the M-estimate. Use the sandwich form of the [M-estimator](/m-estimator/) page.

## Implementations

## History

Nelder and Wedderburn (1972) unified regression for normal, binomial, Poisson and gamma responses as generalized linear models and showed that one iterative weighted regression gives the maximum likelihood estimate for all of them; earlier probit analysis already used working responses and weights. Beaton and Tukey (1974) and Holland and Welsch (1977) applied reweighting to robust regression with the biweight and other weight functions. Green (1984) gave the general treatment of the method for maximum likelihood, its Newton and Fisher scoring forms and its robust and resistant variants.

## References
