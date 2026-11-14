---
tag: H214DD
kind: definition
slug: m-estimator
name: M-estimator
aliases:
- maximum likelihood type estimator
- Z-estimator
area: statistics-and-inference/point-estimation
level: advanced
summary: An estimator that minimizes a sum of loss terms rho(X_i, theta) or solves a sum of estimating equations psi(X_i, theta) = 0. Its asymptotic covariance is the sandwich A^-1 B A^-T / n.
prereqs: [maximum-likelihood-estimation, asymptotic-normality-of-mle, slutsky-theorem]
see_also: [huber-m-estimator, heteroscedasticity-consistent-standard-errors, influence-function, generalized-method-of-moments, quantile-regression, generalized-estimating-equations, empirical-risk-minimization, robust-model-fitting]
sources:
  - paper: doi:10.1214/aoms/1177703732
    title: Peter J. Huber, Robust estimation of a location parameter, Annals of Mathematical Statistics 35(1), 1964
    locator: pages 73 to 101 (estimators that minimize a sum of rho(x_i - T), and the minimax property of the Huber estimator)
  - paper: "P. J. Huber, The behavior of maximum likelihood estimates under nonstandard conditions, Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability 1, 1967"
    locator: pages 221 to 233 (consistency and asymptotic normality of M-estimators without a correct model, and the sandwich covariance)
  - paper: "L. A. Stefanski and D. D. Boos, The calculus of M-estimation, The American Statistician 56(1), 2002"
    locator: pages 29 to 38 (the sandwich formula and how to stack estimating equations)
  - book: isbn:9780521496032
    title: A. W. van der Vaart, Asymptotic Statistics, Cambridge University Press, 1998
    locator: Chapter 5, Section 5.2 (consistency of M- and Z-estimators) and Section 5.3 (asymptotic normality)
  - book: isbn:9780470129906
    title: Peter J. Huber and Elvezio M. Ronchetti, Robust Statistics, second edition, Wiley, 2009
    locator: Chapter 3 (M-estimators of location) and Chapter 6 (M-estimators of a general parameter)
---

An M-estimator is a parameter estimate defined as the minimizer of a sum of loss terms, one for each observation, or as a root of a sum of estimating functions. The class contains the sample mean, the sample [median](/median/), least squares, [quantile regression](/quantile-regression/), the [maximum likelihood estimator](/maximum-likelihood-estimation/) and the robust [Huber estimator](/huber-m-estimator/). Huber introduced the name in 1964 for "maximum likelihood type" estimators. One theory covers all of them: under regularity conditions they are consistent for the root of the population estimating equation and asymptotically normal with the sandwich covariance, whether or not any parametric model is true.

## Definition

Let $X_1, \ldots, X_n$ be iid with law $P$ on a space $\mathcal X$, and let $\Theta \subseteq \mathbb R^k$.

**M-estimator ($\rho$ type).** Given a function $\rho : \mathcal X \times \Theta \to \mathbb R$, an M-estimator is any $\hat\theta_n$ with

$$\hat\theta_n \in \arg\min_{\theta \in \Theta}\ \sum_{i=1}^n \rho(X_i, \theta).$$

**Z-estimator ($\psi$ type).** Given $\psi : \mathcal X \times \Theta \to \mathbb R^k$, a Z-estimator is any root $\hat\theta_n$ of the estimating equation

$$\Psi_n(\theta) = \frac1n\sum_{i=1}^n \psi(X_i, \theta) = 0.$$

When $\rho$ is differentiable in $\theta$, the minimizer solves the equation with $\psi = \nabla_\theta\rho$, so the two forms often give the same estimator. They differ when $\rho$ is not differentiable (the median) or when the equation has roots that are not minima. Many authors use "M-estimator" for both.

**Target.** The population version of the estimator is the parameter $\theta_0 = \theta_0(P)$ that minimizes $\mathrm E_P\,\rho(X, \theta)$, or solves $\mathrm E_P\,\psi(X, \theta) = 0$. It is defined by $\rho$ or $\psi$ and $P$, not by a model. If the model $f(x; \theta)$ is correct and $\rho = -\log f$, then $\theta_0$ is the true parameter; if the model is wrong, $\theta_0$ is the parameter of the model closest to $P$ in [Kullback-Leibler divergence](/kullback-leibler-divergence/).

**Sandwich matrices.** For a Z-estimator with target $\theta_0$, put

$$A = \mathrm E_P\!\left[\frac{\partial\psi(X, \theta_0)}{\partial\theta^{\mathsf T}}\right], \qquad B = \mathrm E_P\bigl[\psi(X, \theta_0)\,\psi(X, \theta_0)^{\mathsf T}\bigr].$$

When $\psi$ is not differentiable, $A$ is the derivative of the map $\theta \mapsto \mathrm E_P\,\psi(X, \theta)$ at $\theta_0$.

### Properties

**Asymptotic normality (sandwich formula).** Assume: (1) $\theta_0$ is an interior point of $\Theta$ and the unique root of $\mathrm E_P\,\psi(X, \theta) = 0$; (2) $\hat\theta_n$ is a root of $\Psi_n$ with $\hat\theta_n \xrightarrow{p} \theta_0$; (3) $\theta \mapsto \mathrm E_P\,\psi(X, \theta)$ is differentiable at $\theta_0$ with invertible derivative $A$; (4) $B$ is finite; (5) $\psi$ is Lipschitz in $\theta$ near $\theta_0$ with an envelope $\dot\psi(x)$ that has $\mathrm E_P\,\dot\psi(X)^2 < \infty$, or a similar smoothness condition. Then

$$\sqrt n\,(\hat\theta_n - \theta_0) \xrightarrow{d} N_k\bigl(0,\ A^{-1}B\,A^{-\mathsf T}\bigr).$$

*Proof sketch.* When $\psi$ is differentiable in $\theta$, a mean-value expansion of each coordinate of $\Psi_n$ gives $0 = \Psi_n(\hat\theta_n) = \Psi_n(\theta_0) + \dot\Psi_n(\tilde\theta_n)(\hat\theta_n - \theta_0)$, where the rows of $\dot\Psi_n$ are evaluated at points $\tilde\theta_n$ between $\hat\theta_n$ and $\theta_0$. The [central limit theorem](/central-limit-theorem/) gives $\sqrt n\,\Psi_n(\theta_0) \xrightarrow{d} N(0, B)$, because $\mathrm E\,\psi(X, \theta_0) = 0$. The [law of large numbers](/law-of-large-numbers/) and consistency give $\dot\Psi_n(\tilde\theta_n) \xrightarrow{p} A$. The vector form of [Slutsky's theorem](/slutsky-theorem/) gives $\sqrt n\,(\hat\theta_n - \theta_0) = -\dot\Psi_n(\tilde\theta_n)^{-1}\sqrt n\,\Psi_n(\theta_0) \xrightarrow{d} -A^{-1}N(0, B)$. For non-smooth $\psi$, such as the median, the expansion is replaced by an empirical process argument; see van der Vaart, Section 5.3, and Huber (1967). $\square$

**The sandwich estimate.** The covariance is estimated by $\hat A^{-1}\hat B\hat A^{-\mathsf T}/n$, with $\hat A = \dot\Psi_n(\hat\theta_n)$ and $\hat B = n^{-1}\sum_i \psi(X_i, \hat\theta_n)\psi(X_i, \hat\theta_n)^{\mathsf T}$ (divisor $n$). It is consistent under the conditions above without any parametric model. For least squares it is the [heteroscedasticity-consistent standard error](/heteroscedasticity-consistent-standard-errors/) of White.

**The MLE as a special case.** For $\psi = -\nabla_\theta\log f$ and a correct model, the information identity gives $B = I(\theta_0)$ and $A = I(\theta_0)$, so the sandwich reduces to $I(\theta_0)^{-1}$, as in [asymptotic normality of the MLE](/asymptotic-normality-of-mle/). Under a wrong model $A \ne B$ in general, and the inverse information is the wrong variance.

**Influence function.** The [influence function](/influence-function/) of a Z-estimator is $\mathrm{IF}(x) = -A^{-1}\psi(x, \theta_0)$, and $B$ is the covariance of $A\,\mathrm{IF}(X)$. The estimator is robust to gross outliers in $x$ exactly when $\psi$ is bounded in $x$.

**Equivariance.** For location, $\psi(x, \theta) = \phi(x - \theta)$ gives an estimator that moves with shifts of the data. Scale equivariance needs a scale estimate in the argument, $\phi((x - \theta)/\hat s)$, which is why practical robust estimators come with a robust scale such as the median absolute deviation.

## Examples and non-examples

**Mean and median.** With $\rho(x, \theta) = (x - \theta)^2$ the estimator is $\bar X$, with $A = 2$, $B = 4\sigma^2$ and sandwich variance $\sigma^2/n$. With $\rho(x, \theta) = |x - \theta|$ it is the sample median, a Z-estimator with $\psi(x, \theta) = -\operatorname{sign}(x - \theta)$. Here $A = 2f(\theta_0)$ for the density $f$ of $X$, $B = 1$, and the sandwich gives the known variance $1/(4n f(\theta_0)^2)$ of the median.

**Huber's estimator.** $\psi_k(r) = \max(-k, \min(k, r))$ applied to $r = x - \theta$ is linear for small residuals and constant for large ones. Take the five numbers $1, 2, 3, 4, 20$, with the scale fixed at 1. The mean is 6, pulled by the outlier, and the median is 3. With $k = 3$ the equation $\sum\psi_3(x_i - \theta) = 0$ has the unique root $\theta = 13/4$: the residuals are $-9/4, -5/4, -1/4, 3/4$ and $67/4$, the last is clipped to 3, and $-9/4 - 5/4 - 1/4 + 3/4 + 3 = 0$. The plug-in sandwich uses $\hat A = 4/5$ (the fraction of residuals inside $(-3, 3)$) and $\hat B = (81 + 25 + 1 + 9)/(16 \cdot 5) + 9/5 = 13/4$, so the variance estimate is $\hat B/(\hat A^2 n) = 65/64$. The same formula for the mean gives $\sum(x_i - 6)^2/n^2 = 10$. Five numbers are far too few for these asymptotic values to be accurate; the example only shows the arithmetic.

**Maximum likelihood.** $\rho = -\log f(x; \theta)$. Every MLE in a regular model is an M-estimator, and its target under misspecification is the Kullback-Leibler projection (White 1982).

**Regression.** Least squares, $\rho = (y - x^{\mathsf T}\beta)^2$; least absolute deviations and [quantile regression](/quantile-regression/), $\rho = \rho_\tau(y - x^{\mathsf T}\beta)$ with the check loss; robust regression with Huber or Tukey loss. [Generalized estimating equations](/generalized-estimating-equations/) are Z-estimators for clustered data, and the [generalized method of moments](/generalized-method-of-moments/) generalizes Z-estimation to more equations than parameters.

**Non-example: L-estimators.** The trimmed mean is a linear combination of order statistics. It is asymptotically equivalent to a Huber-type M-estimator for symmetric distributions, but it is not defined by minimizing a sum of terms $\rho(X_i, \theta)$, one for each observation.

**Non-example: a pairwise criterion.** The Hodges-Lehmann estimator, the median of all pairwise means, solves an equation in pairs $(X_i, X_j)$. It is an R-estimator, and its asymptotic theory uses U-statistics, not the sandwich formula above.

**Non-example: a root that is not consistent.** For Cauchy location data the likelihood equation can have several roots. Each root is a Z-estimator in the formal sense, but only a consistent sequence of roots has the sandwich limit; condition (2) above is not automatic.

## Related definitions

- [Huber M-estimator](/huber-m-estimator/): the M-estimator with $\psi_k$, minimax over contaminated normal laws.
- [Influence function](/influence-function/): $-A^{-1}\psi$ for a Z-estimator.
- [Heteroscedasticity-consistent standard errors](/heteroscedasticity-consistent-standard-errors/): the sandwich for least squares.
- [Generalized method of moments](/generalized-method-of-moments/): more moment conditions than parameters, weighted.
- [Empirical risk minimization](/empirical-risk-minimization/): the same definition in learning theory, where $\rho$ is a loss.
- [Robust model fitting](/robust-model-fitting/): M-estimators in geometric fitting.

## References
