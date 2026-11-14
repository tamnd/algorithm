---
tag: KGKBYG
kind: technique
slug: method-of-moments
name: Method of moments
aliases:
- moment matching estimation
area: statistics-and-inference/point-estimation
level: intro
summary: Estimate parameters by setting the first few sample moments equal to the population moments and solving for the parameters. Simple and consistent, but often not efficient.
prereqs: [estimator, consistent-estimator, law-of-large-numbers]
see_also: [generalized-method-of-moments, maximum-likelihood-estimation, delta-method, sample-variance, yule-walker-equations, gaussian-mixture-model, m-estimator, likelihood-function]
sources:
  - paper: doi:10.1098/rsta.1894.0003
    title: Karl Pearson, Contributions to the mathematical theory of evolution, Philosophical Transactions of the Royal Society A 185, 1894
    locator: pp. 71 to 110 (a mixture of two normal curves fitted by its first five moments, through an equation of degree nine)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 7.2.1 (method of moments, with the binomial example in which both k and p are unknown)
  - book: isbn:9780387402727
    title: Larry Wasserman, All of Statistics, Springer, 2004
    locator: Section 9.2 (method of moments, with its consistency and asymptotic normality)
  - paper: doi:10.1098/rsta.1922.0009
    title: R. A. Fisher, On the mathematical foundations of theoretical statistics, Philosophical Transactions of the Royal Society A 222, 1922
    locator: pp. 309 to 368 (efficiency, and the loss of efficiency of the method of moments compared with maximum likelihood)
---

The method of moments is a recipe for building an [estimator](/estimator/): write the first $k$ population moments as functions of the $k$ unknown parameters, replace them by the sample moments, and solve the $k$ equations for the parameters. The sample moments converge to the population moments by the [law of large numbers](/law-of-large-numbers/), so the estimate is [consistent](/consistent-estimator/) whenever the moment map can be inverted continuously. It needs no likelihood and often has a closed form, but it is usually less precise than [maximum likelihood](/maximum-likelihood-estimation/) and can give values that the data rule out.

## In plain words

A model with unknown numbers predicts what the average of the data should be, what the average of the squares should be, and so on. Compute those averages from the data you have. Then choose the unknown numbers so that the model's predictions match what you computed. With two unknowns you match two averages, with three unknowns three.

The idea is old and simple, and it often needs only a little algebra. With a lot of data the averages settle down, so the answer settles near the truth. With little data, or a model that the data fit badly, the answer can be poor or even impossible, such as a negative count.

## When it applies

- The data $X_1, \ldots, X_n$ are iid with law $P_\theta$, $\theta \in \Theta \subseteq \mathbb{R}^k$. The method extends to stationary data whose sample moments converge, as for the [Yule-Walker equations](/yule-walker-equations/).
- There are functions $g_1, \ldots, g_k$ with $\mathbb{E}_\theta \lvert g_j(X) \rvert < \infty$, usually $g_j(x) = x^j$. Write $\mu_j(\theta) = \mathbb{E}_\theta[g_j(X)]$ and $\mu(\theta) = (\mu_1(\theta), \ldots, \mu_k(\theta))$.
- The moment map $\mu: \Theta \to \mathbb{R}^k$ is one-to-one (the parameter is identified by these moments), and the equations can be solved, in closed form or numerically.
- For consistency, $\mu^{-1}$ must be continuous at $\mu(\theta)$. For a $\sqrt n$ normal limit, $\mathbb{E}_\theta[g_j(X)^2] < \infty$ and $\mu$ must be differentiable with an invertible Jacobian.

## The template

```pseudo id=main
MOMENT-ESTIMATE(x_1, ..., x_n)
L1  choose MOMENT-FUNCTIONS g_1, ..., g_k              ▷ hole: usually g_j(x) = x^j
L2  for j ← 1 to k do
L3      m_j ← (1/n) Σ_i g_j(x_i)                         ▷ sample moments
L4  write MOMENT-MAP μ_j(θ) = E_θ[g_j(X)], j = 1..k     ▷ hole: from the model
L5  θ̂ ← SOLVE(μ(θ) = m)                                  ▷ hole: algebra or a root finder
L6  if θ̂ does not exist or lies outside Θ then
L7      θ̂ ← REPAIR(m)                                    ▷ hole: report, project or switch method
L8  return θ̂ and the plug-in estimate ψ(θ̂)
```

The holes are the choice of moment functions (line L1), the moment map of the model (line L4), the solver (line L5) and the rule for an impossible solution (line L7). Central moments may replace raw ones: matching $\mathbb{E}X$ and $\mathbb{E}X^2$ is the same as matching the mean and the variance $\mathbb{E}(X - \mathbb{E}X)^2$, with the sample variance taken with divisor $n$, $\hat\sigma^2 = m_2 - m_1^2$. Say which divisor is used; the [sample variance](/sample-variance/) $S^2$ with divisor $n - 1$ gives a slightly different, equally consistent estimator.

**Why it is consistent.** Fix $\theta$. By the law of large numbers, $m = (m_1, \ldots, m_k) \to \mu(\theta)$ in probability. If $\mu^{-1}$ is continuous at $\mu(\theta)$ and defined on a neighbourhood of it, then $\hat\theta = \mu^{-1}(m) \to \mu^{-1}(\mu(\theta)) = \theta$ in probability, because continuous maps keep consistency (proved on [consistent estimator](/consistent-estimator/)). The event that line L7 is needed has probability tending to 0. This is proved; it holds for every $\theta$ that meets the conditions.

**The asymptotic law.** Let $\Sigma(\theta)$ be the covariance matrix of $(g_1(X), \ldots, g_k(X))$, assumed finite, and $J(\theta) = \partial\mu/\partial\theta$, assumed invertible and continuous. The multivariate central limit theorem gives $\sqrt n (m - \mu(\theta)) \to N(0, \Sigma)$, and the [delta method](/delta-method/) applied to $\mu^{-1}$ gives

$$\sqrt n(\hat\theta - \theta) \to N\big(0,\; J^{-1} \Sigma J^{-\mathsf T}\big) \quad \text{in distribution}.$$

Plugging $\hat\theta$ into this matrix gives standard errors.

## Classic examples

**Normal.** For $N(\mu, \sigma^2)$, $\mathbb{E}X = \mu$ and $\mathbb{E}X^2 = \sigma^2 + \mu^2$, so $\tilde\mu = \bar x$ and $\tilde\sigma^2 = m_2 - m_1^2 = \hat\sigma^2$, the divisor-$n$ variance. For $x = (3, 7, 7, 9, 14)$ this is $\tilde\mu = 8$ and $\tilde\sigma^2 = 64/5 = 12.8$. Here the method agrees with maximum likelihood.

**Gamma.** For the gamma law with shape $\alpha > 0$ and scale $\beta > 0$, the mean is $\alpha\beta$ and the variance is $\alpha\beta^2$. Solving gives

$$\tilde\alpha = \bar x^2/\hat\sigma^2, \qquad \tilde\beta = \hat\sigma^2/\bar x.$$

On the same data, $\tilde\alpha = 64/12.8 = 5$ and $\tilde\beta = 12.8/8 = 1.6$; check: $5 \cdot 1.6 = 8$ and $5 \cdot 1.6^2 = 12.8$. The maximum likelihood estimate of $\alpha$ has no closed form and needs a root finder such as the [Newton-Raphson method](/newton-raphson-method/); the moment estimate is a common starting point for it.

**Binomial with both parameters unknown.** For Binomial$(k, p)$ counts, the mean is $kp$ and the variance is $kp(1-p)$, so $\tilde p = 1 - \hat\sigma^2/\bar x$ and $\tilde k = \bar x^2/(\bar x - \hat\sigma^2)$ (Casella and Berger, Section 7.2.1). For the counts $(0, 0, 0, 1, 9)$, $\bar x = 2$ and $\hat\sigma^2 = 82/5 - 4 = 62/5$, so $\tilde p = -26/5$ and $\tilde k = -5/13 \approx -0.385$. Both lie outside $\Theta = \{1, 2, \ldots\} \times (0, 1)$. This happens whenever $\hat\sigma^2 \ge \bar x$, a sample that is more spread out than any binomial law with that mean.

**Mixtures.** Pearson (1894) fitted a mixture of two normal laws, five parameters, to measurements of crabs by matching five moments. The equations reduce to one polynomial equation of degree nine, which he solved by hand. The modern alternative is [expectation-maximization](/expectation-maximization/) on the [Gaussian mixture model](/gaussian-mixture-model/).

**Autoregressions.** The [Yule-Walker equations](/yule-walker-equations/) match the sample autocovariances of a stationary series with those of an autoregressive model; for AR(1), $\tilde\phi = r_1/r_0$.

## Variations

- **Generalized method of moments.** With more moment conditions $\mathbb{E}_\theta[g(X, \theta)] = 0$ than parameters, the equations cannot all hold on data, and the [generalized method of moments](/generalized-method-of-moments/) minimizes a weighted quadratic form in the sample moments instead. The plain method is the exactly identified case.
- **Estimating equations.** Matching $\frac1n \sum_i g(x_i, \theta) = 0$ for functions that depend on $\theta$ is an [M-estimator](/m-estimator/). Maximum likelihood is the case $g$ = the [score](/score-function/), which shows that the right moments can recover full efficiency.
- **Other moments.** Probability-weighted moments, L-moments, factorial moments for counts and moments of $\log X$ are the same template with other $g_j$.
- **Matching other summaries.** Matching sample quantiles to population quantiles is the same idea with a different summary; it does not need any moments to exist.
- **Simulated moments.** When $\mu(\theta)$ has no formula, estimate it by simulation at each trial $\theta$ and solve by a stochastic search.

## Pitfalls

- **Estimates the data rule out.** For iid Uniform$(0, \theta)$, $\mathbb{E}X = \theta/2$ gives $\tilde\theta = 2\bar x$. For the data $(1, 2, 3, 10)$, $\tilde\theta = 8$, while the largest observation is 10, so $\theta \ge 10$ is certain. The estimate is still inside $\Theta = (0, \infty)$; truly impossible values come from examples such as the binomial one above.
- **Low efficiency.** In the same uniform model, $\operatorname{Var}(2\bar X) = \theta^2/(3n)$, while the unbiased estimator $\frac{n+1}{n}\max_i X_i$ has variance $\theta^2/(n(n+2))$. The ratio is $(n+2)/3$, so the moment estimator needs about $n^2/3$ observations for the accuracy that the maximum reaches with $n$. Fisher (1922) used efficiency to compare the method with maximum likelihood for Pearson's curves.
- **The choice of moments matters.** For Poisson data, $\mathbb{E}X = \lambda$ and $\operatorname{Var}X = \lambda$, so both $\bar x$ and $\hat\sigma^2$ are moment estimators of $\lambda$. On $(3, 7, 7, 9, 14)$ they give 8 and 12.8. Use the lowest moments that identify $\theta$; higher moments have larger variance and need more moments to be finite.
- **Moments that do not exist.** For Cauchy data no moment exists, and $\bar X$ does not converge. Use quantiles or the likelihood.
- **Several roots, or none.** Nonlinear moment equations can have several solutions in $\Theta$, as Pearson's degree nine equation does, or none. The template must say which root is reported.
- **Cancellation.** Computing $m_2 - m_1^2$ in floating point loses digits when $\lvert \bar x \rvert$ is large compared with the spread. Compute the central moments by a two-pass formula or by [Welford's algorithm](/welford-algorithm/).

## Exercises

1. For iid exponential data with rate $\lambda$ ($\mathbb{E}X = 1/\lambda$), find the moment estimator, and use the delta method to find its asymptotic variance.
   *Answer.* $\tilde\lambda = 1/\bar x$. With $g(t) = 1/t$, $g'(1/\lambda)^2 \operatorname{Var}X = \lambda^4 \cdot \lambda^{-2} = \lambda^2$, so $\sqrt n(\tilde\lambda - \lambda) \to N(0, \lambda^2)$. This is also the maximum likelihood estimator.
2. For iid Uniform$(a, b)$, find the moment estimators from the mean and the divisor-$n$ variance, and evaluate them on $(3, 7, 7, 9, 14)$.
   *Answer.* The mean is $(a + b)/2$ and the variance is $(b - a)^2/12$, so $\tilde a = \bar x - \sqrt{3\hat\sigma^2}$ and $\tilde b = \bar x + \sqrt{3\hat\sigma^2}$. Here $\sqrt{38.4} = 6.197$, so $(\tilde a, \tilde b) = (1.803, 14.197)$; both agree with the data, since $1.803 < 3$ and $14.197 > 14$.
3. For the beta law with parameters $\alpha, \beta > 0$, with mean $\alpha/(\alpha+\beta)$ and variance $\alpha\beta/((\alpha+\beta)^2(\alpha+\beta+1))$, find the moment estimators and the condition on the data for them to lie in $\Theta$.
   *Answer.* With $c = \bar x(1 - \bar x)/\hat\sigma^2 - 1$, $\tilde\alpha = \bar x c$ and $\tilde\beta = (1 - \bar x) c$. They are positive exactly when $0 < \bar x < 1$ and $\hat\sigma^2 < \bar x(1 - \bar x)$.
4. Show that for Bernoulli$(p)$ data the moment estimator from $\mathbb{E}X$ and the maximum likelihood estimator are both $\bar x$, and that matching $\mathbb{E}X^2$ instead gives nothing new.
   *Answer.* $\ell'(p) = n\bar x/p - n(1 - \bar x)/(1 - p) = 0$ gives $p = \bar x$. Since $X^2 = X$ for 0 and 1 data, $m_2 = m_1$.
5. Prove the efficiency ratio $(n+2)/3$ for the uniform example.
   *Answer.* $\operatorname{Var}X = \theta^2/12$, so $\operatorname{Var}(2\bar X) = \theta^2/(3n)$. The maximum $M$ has density $n t^{n-1}/\theta^n$ on $[0, \theta]$, so $\mathbb{E}M = n\theta/(n+1)$ and $\mathbb{E}M^2 = n\theta^2/(n+2)$, which give $\operatorname{Var}\big(\tfrac{n+1}{n}M\big) = \theta^2/(n(n+2))$. Divide.

## References
