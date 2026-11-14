---
tag: Y142G8
kind: algorithm
slug: fisher-scoring
name: Fisher scoring
aliases:
- method of scoring
- Fisher's scoring algorithm
area: statistics-and-inference/point-estimation
level: core
summary: Maximizes a likelihood by Newton steps that use the expected information in place of the observed one. For GLMs it is IRLS, and for canonical links it equals Newton's method.
model: real-ram
complexity:
  vars: {n: the number of observations, p: the number of parameters, t: the number of iterations}
  time: {worst: "O(t (n p^2 + p^3))"}
  space: {extra: "O(p^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1935
  people: [R. A. Fisher, C. I. Bliss]
  note: Fisher gave the iterative maximum likelihood fit of the probit model with expected weights in his appendix to Bliss's 1935 paper on the dosage-mortality curve. Nelder and Wedderburn (1972) showed that scoring for every generalized linear model is iteratively reweighted least squares.
prereqs: [score-function, fisher-information-matrix, newton-raphson-method, maximum-likelihood-estimation]
see_also: [iteratively-reweighted-least-squares, generalized-linear-model, logistic-regression, gauss-newton-algorithm, expectation-maximization, asymptotic-normality-of-mle, score-test, quasi-newton-method]
sources:
  - paper: doi:10.2307/1403504
    title: M. R. Osborne, Fisher's method of scoring, International Statistical Review 60(1), 1992
    locator: pages 99 to 117 (convergence of scoring, its relation to Gauss-Newton, and step-length control)
  - paper: "C. I. Bliss, The calculation of the dosage-mortality curve, Annals of Applied Biology 22(1), 1935, with an appendix by R. A. Fisher, The case of zero survivors"
    locator: pages 134 to 167; the appendix is on pages 164 to 165 (iterative fit of the probit line with expected weights)
  - paper: "J. A. Nelder and R. W. M. Wedderburn, Generalized linear models, Journal of the Royal Statistical Society, Series A 135(3), 1972"
    locator: pages 370 to 384 (the fitting algorithm as iterative weighted least squares, equal to scoring)
  - book: isbn:9780412317606
    title: P. McCullagh and J. A. Nelder, Generalized Linear Models, second edition, Chapman and Hall, 1989
    locator: Chapter 2 (the iteratively reweighted least squares algorithm for fitting a GLM, and its use of expected information)
  - book: isbn:9780521496032
    title: A. W. van der Vaart, Asymptotic Statistics, Cambridge University Press, 1998
    locator: Chapter 5, Section 5.7 (one-step estimators)
---

Fisher scoring finds a [maximum likelihood estimate](/maximum-likelihood-estimation/) by repeated Newton steps on the likelihood equation, with one change: the Hessian of the log-likelihood is replaced by minus its expectation, the [Fisher information](/fisher-information-matrix/) $I_n(\theta)$. The expected information is positive definite under mild conditions, so each step goes uphill, and it is often simpler to compute than the observed Hessian. For a [generalized linear model](/generalized-linear-model/), a scoring step is one weighted least squares fit, which is why the method is also called [iteratively reweighted least squares](/iteratively-reweighted-least-squares/). For a canonical link, such as [logistic regression](/logistic-regression/) or Poisson regression with a log link, the expected and the observed information are equal, and scoring is exactly [Newton's method](/newton-raphson-method/).

## In plain words

You want the top of a hill, the parameter value that makes the data most likely. At your current position you can measure the slope. Newton's method also measures how the slope is bending, and jumps to where the bend says the top is.

Fisher scoring uses the average bend instead: the bend you would expect, on average, over all data sets the model could produce at this parameter value. The average bend always points to a top, never to a valley, so the method moves uphill when the actual bend would send Newton's method the wrong way. Near the top, the actual and the average bend are close, so the method is almost as fast as Newton's.

If a step is too long and the height drops, cut it in half until the height no longer drops.

## The problem

The input is a log-likelihood $\ell(\theta)$ of a sample, $\theta \in \mathbb R^k$, given through its [score](/score-function/) $U(\theta) = \nabla\ell(\theta)$ and the expected information of the sample $I(\theta) = \operatorname{Var}_\theta U(\theta)$, which is $n$ times the information of one observation for iid data. $I(\theta)$ must be positive definite at every point the method visits. Optionally $\ell$ itself is given, for step control. The input also has a start $\theta_0$, a tolerance $\varepsilon \ge 0$ and a limit $t_{\max}$ on the number of iterations.

The output is a point $\hat\theta$ with $U(\hat\theta)^{\mathsf T}I(\hat\theta)^{-1}U(\hat\theta) \le \varepsilon$, which approximates a root of the likelihood equation $U(\theta) = 0$, and the matrix $I(\hat\theta)^{-1}$, the usual estimate of the covariance of $\hat\theta$. If the test is not met in $t_{\max}$ iterations, or no step along the scoring direction raises $\ell$, the output says that the method did not converge.

For a GLM with design rows $x_i \in \mathbb R^p$, mean $\mu_i = h(\eta_i)$, $\eta_i = x_i^{\mathsf T}\beta$, and variance function $V(\mu)$,

$$U(\beta) = \sum_{i=1}^n x_i\,\frac{(y_i - \mu_i)\,h'(\eta_i)}{V(\mu_i)}, \qquad I(\beta) = \sum_{i=1}^n x_i x_i^{\mathsf T}\,\frac{h'(\eta_i)^2}{V(\mu_i)}.$$

## The algorithm

```pseudo id=main
FISHER-SCORING(U, I, ℓ, θ_0, ε, t_max)
L1  θ ← θ_0
L2  for t ← 0 to t_max - 1 do
L3      g ← U(θ)                                ▷ score of the sample at θ
L4      H ← I(θ)                                ▷ expected information of the sample
L5      δ ← solution of H δ = g                 ▷ the scoring direction
L6      if gᵀδ ≤ ε then return θ, H⁻¹, converged
L7      s ← 1
L8      while ℓ(θ + sδ) < ℓ(θ) and s > s_min do s ← s / 2
L9      if ℓ(θ + sδ) < ℓ(θ) then return θ, H⁻¹, stalled
L10     θ ← θ + sδ
L11 return θ, I(θ)⁻¹, not converged
```

Line L5 solves a $k \times k$ positive definite system; a Cholesky factorization is the usual choice. The quantity $g^{\mathsf T}\delta = U^{\mathsf T}I^{-1}U$ in line L6 is the [score test](/score-test/) statistic for the current point, so the stopping rule does not depend on how the parameters are scaled. Lines L7 to L9 are step halving. Without $\ell$ they are skipped and every step has $s = 1$, which is plain scoring.

For a GLM, put $w_i = h'(\eta_i)^2/V(\mu_i)$ and the working response $z_i = \eta_i + (y_i - \mu_i)/h'(\eta_i)$. Then $H = X^{\mathsf T}WX$ and $H\beta + g = X^{\mathsf T}Wz$, so the full step $\beta + \delta$ is the weighted least squares fit of $z$ on $X$ with weights $w_i$. That is the IRLS form of the same step.

## Example

**Logistic and probit regression.** The data are the doses $1, \ldots, 6$, each given to 10 subjects, with $1, 2, 4, 6, 8$ and $9$ responses; the model has an intercept and a slope in the dose, and the start is $\beta = (0, 0)$. The table gives the scoring iterates without halving, computed in double precision. For the logit link, Newton's method gives the same iterates to all printed digits, as Lemma 5 of the proof says it must.

| $t$ | logit $\beta_0$ | logit $\beta_1$ | probit $\beta_0$ | probit $\beta_1$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | $-2.4000000000$ | $0.6857142857$ | $-1.5039769648$ | $0.4297077042$ |
| 2 | $-3.0276954635$ | $0.8650558467$ | $-1.8156375678$ | $0.5187535908$ |
| 3 | $-3.1189201800$ | $0.8911200514$ | $-1.8488825242$ | $0.5282521498$ |
| 4 | $-3.1206983729$ | $0.8916281066$ | $-1.8491436546$ | $0.5283267585$ |
| 5 | $-3.1206990360$ | $0.8916282960$ | $-1.8491426875$ | $0.5283264822$ |

The logit errors (the largest coordinate distance to the final estimate) are $0.72$, $0.093$, $1.8 \times 10^{-3}$, $6.6 \times 10^{-7}$ and below $10^{-15}$: quadratic convergence, as for Newton's method. The probit errors are $0.35$, $0.034$, $2.6 \times 10^{-4}$, $9.6 \times 10^{-7}$ and $3.7 \times 10^{-9}$: each step gains a roughly constant number of digits, which is linear convergence with a small rate. Newton's method with the observed information gives the same first probit step, because the two informations agree at $\eta = 0$, and then differs from the second step on. It reaches the same estimate in 5 steps instead of 6. At the estimate, the inverse information gives the standard errors $0.853$ and $0.226$ (logit) and $0.466$ and $0.122$ (probit).

**Cauchy location.** For 25 draws from a Cauchy law with location 2 (seed 7 of Python's `random.Random`), the information of the sample is $n/2$, a constant, while the observed information $\sum 2(1 - r_i^2)/(1 + r_i^2)^2$ with $r_i = x_i - \theta$ is negative far from the data. From the sample median, Newton's method takes 3 steps and scoring with halving takes 8 to reach the global maximizer $\hat\theta = 1.59503$. From the smallest observation, Newton's method stops at the stationary point $9.5156$, and from the largest at $13.438$. Scoring with halving reaches $1.59503$ from every start tried, which agrees with a dense grid search over the range of the data.

## Correctness

The returned point satisfies $U^{\mathsf T}I^{-1}U \le \varepsilon$, and with $\varepsilon = 0$ it is a root of the likelihood equation, because $I^{-1}$ is positive definite. The direction $\delta = I^{-1}U$ has positive inner product $U^{\mathsf T}I^{-1}U$ with the gradient, so it points uphill, and step halving finds a step that does not lower $\ell$. For a canonical exponential family the Hessian of $\ell$ does not depend on the data, so it equals minus its expectation, and scoring is Newton's method step by step. In general, the Jacobian of the full scoring map at a root is $I_k - I^{-1}J$, where $J$ is the observed information, so the local rate of convergence is the spectral radius of that matrix. The full proofs are below. They do not show that the limit is the global maximum, which is false in general.

## Complexity

For a GLM, one iteration computes the $n$ linear predictors in $O(np)$, the score in $O(np)$, the information $X^{\mathsf T}WX$ in $O(np^2)$, and solves the $p \times p$ system in $O(p^3)$. Each halving costs one more log-likelihood, $O(np)$. Over $t$ iterations the time is $O(t(np^2 + p^3))$ plus the halvings, and the extra space is $O(p^2)$ for $H$ and its factor.

The number of iterations depends on the problem. With a canonical link and a start near the estimate, convergence is quadratic and 5 to 10 iterations are typical. Otherwise it is linear with the rate of Lemma 6 of the proof, which is small when the model fits and $n$ is large.

Scoring needs no second derivatives of the data terms, only $h'$ and $V$, which is part of its appeal. Compared with Newton's method it saves little per step for GLMs but gives a matrix $H$ that is positive definite whenever $X$ has full column rank and all weights are positive.

## Properties

- **Ascent with halving.** With step halving the log-likelihood never decreases.
- **Invariant to reparametrization of the linear kind.** If $\theta = A\phi$ with $A$ invertible, the iterates in $\phi$ map to the iterates in $\theta$, and the stopping test of line L6 is unchanged.
- **Covariance for free.** $I(\hat\theta)^{-1}$ at the end is the inverse expected information, the standard covariance estimate of [asymptotic normality of the MLE](/asymptotic-normality-of-mle/). For a non-canonical link it differs from the inverse observed information at finite $n$.
- **One-step efficiency.** One full scoring step from a $\sqrt n$-consistent start gives an estimator with the same limit law as the MLE (van der Vaart, Section 5.7). This is a statement about large samples, not about one data set.
- **Exact for linear models.** For a normal linear model the information does not depend on $\beta$, and one step from any start gives the least squares estimate exactly.

## Variants and improvements

- **Newton-Raphson.** Use the observed information $J$. It is faster near the root for non-canonical models, but $J$ can be indefinite away from it.
- **Mixed strategies.** Start with scoring steps for safety and switch to Newton steps near the root, or use $J$ when it is positive definite and $I$ otherwise.
- **Gauss-Newton.** For nonlinear least squares with normal errors, scoring is the [Gauss-Newton algorithm](/gauss-newton-algorithm/), and Levenberg-Marquardt damping can replace halving.
- **Quasi-likelihood and estimating equations.** The same step with $U = \sum D_i^{\mathsf T}V_i^{-1}(y_i - \mu_i)$ and $I = \sum D_i^{\mathsf T}V_i^{-1}D_i$ fits [generalized estimating equations](/generalized-estimating-equations/) and quasi-likelihood models.
- **Line search and trust regions.** Halving is the simplest step control; Armijo line search or a trust region gives the same guarantee with fewer function evaluations.
- **Incomplete data.** When the expected complete-data information is easy and the observed-data information is not, [EM](/expectation-maximization/) or a scoring step with an estimated information can be used.

## When to use it

Use Fisher scoring for generalized linear models, nonlinear regression and other models where the expected information has a closed form and the observed Hessian is messy or indefinite. It is the default fitting method of most GLM software. For models with canonical links it is identical to Newton's method, so nothing is lost. For models with many parameters, where forming and factoring a $p \times p$ matrix costs too much, use a [quasi-Newton method](/quasi-newton-method/) or a first-order method instead.

## Pitfalls

- **Separation in logistic regression.** If a hyperplane separates the responses $0$ and $1$, the likelihood increases toward a supremum that is not attained, and the coefficients grow without bound. Scoring may report convergence at a huge $\beta$, because the score and the information both go to zero. Check the fitted probabilities: if they are all within rounding of the responses, the estimate does not exist.
- **Starting values.** For the identity or square-root link with Poisson data, or the identity link with binomial data, a step can leave the parameter space (a negative mean). The log-likelihood is then undefined; halving must treat it as $-\infty$, and the start must be inside the space.
- **A root is not the maximum.** Like Newton's method, scoring finds a root of the score. With a multimodal likelihood, start from several points or from a consistent estimate.
- **Expected versus observed standard errors.** For non-canonical links, $I(\hat\beta)^{-1}$ and $J(\hat\beta)^{-1}$ give different standard errors. Both are valid asymptotically; say which one is reported.
- **Loose tolerance.** A test on the change in $\ell$ alone can stop early on a flat ridge. The test $U^{\mathsf T}I^{-1}U \le \varepsilon$ uses the scale of the information; with linear convergence, a tolerance of $10^{-10}$ can still leave errors near $10^{-6}$ in $\beta$.
- **Singular information.** If $X$ does not have full column rank, or a fitted weight is zero, $H$ is singular. Remove aliased columns before fitting.

## Implementations

## History

R. A. Fisher used the expected information to fit maximum likelihood estimates iteratively. His appendix to C. I. Bliss's 1935 paper on the dosage-mortality curve gives the iterative fit of the probit line with expected weights, and the method spread in bioassay through probit analysis. Nelder and Wedderburn (1972) defined generalized linear models and showed that one fitting algorithm, iterative weighted least squares, is Fisher scoring for all of them. Osborne (1992) analysed the convergence of scoring for likelihoods and quasi-likelihoods and its relation to the Gauss-Newton method.

## References
