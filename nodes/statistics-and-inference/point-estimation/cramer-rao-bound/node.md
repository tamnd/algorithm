---
tag: ER50ZC
kind: theorem
slug: cramer-rao-bound
name: Cramer-Rao bound
aliases:
- Cramer-Rao inequality
- Cramer-Rao lower bound
- CRLB
- information inequality
area: statistics-and-inference/point-estimation
level: core
summary: Under regularity conditions, the variance of any unbiased estimator is at least the inverse of the Fisher information. An estimator that attains it is efficient.
prereqs: [score-function, fisher-information-matrix, minimum-variance-unbiased-estimator, estimator-bias]
see_also: [lehmann-scheffe-theorem, maximum-likelihood-estimation, asymptotic-normality-of-mle, exponential-family-distribution, covariance-matrix, positive-definite-matrix, james-stein-estimator]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 7.3.2, Theorem 7.3.9 (the Cramér-Rao inequality) and Corollary 7.3.15 (attainment)
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 2, Section 2.5 (the information inequality, with the multiparameter form and other bounds)
  - paper: "C. Radhakrishna Rao, Information and the accuracy attainable in the estimation of statistical parameters, Bulletin of the Calcutta Mathematical Society 37 (1945), pages 81 to 91"
    title: Rao 1945
    locator: the lower bound for the variance of unbiased estimators, in one and several parameters
  - book: "Harald Cramér, Mathematical Methods of Statistics, Princeton University Press, 1946"
    title: Cramér 1946
    locator: the chapters on the theory of estimation (the inequality for the variance of an estimate)
---

The Cramér-Rao bound says that, under regularity conditions, no unbiased estimator of $\psi(\theta)$ from $n$ iid observations has variance below $\psi'(\theta)^2 / (n I(\theta))$, where $I(\theta)$ is the [Fisher information](/fisher-information-matrix/) of one observation. An unbiased estimator that attains the bound is called efficient, and it is then a [minimum variance unbiased estimator](/minimum-variance-unbiased-estimator/). The bound is attained exactly only in one-parameter exponential families, but the [maximum likelihood estimator](/maximum-likelihood-estimation/) attains it in the limit of large samples. Fréchet (1943), Darmois (1945), Rao (1945) and Cramér (1946) found it independently.

## Statement

Let $X_1, \ldots, X_n$ be iid with density or mass function $f(x; \theta)$, let $U_n(\theta)$ be the [score](/score-function/) of the sample, and let $I(\theta) = \operatorname{Var}_\theta\, \partial_\theta \log f(X_1; \theta)$.

**Conditions.**

1. $\Theta$ is an open interval of $\mathbb R$ (an open set of $\mathbb R^k$ for a vector $\theta$).
2. The support $\{x : f(x; \theta) > 0\}$ does not depend on $\theta$.
3. $f(x; \theta)$ is differentiable in $\theta$ for every $x$.
4. For the estimator $T$ below, $\int f(x; \theta)\, dx$ and $\int T(x) f(x; \theta)\, dx$ can both be differentiated in $\theta$ under the integral sign (sums for discrete data, and the integrals are over the whole sample space).
5. $0 < I(\theta) < \infty$.

**Theorem (one parameter).** Let $T = T(X_1, \ldots, X_n)$ have $\mathbb{E}_\theta T = \psi(\theta)$ and $\operatorname{Var}_\theta T < \infty$ for all $\theta$. Under conditions 1 to 5,

$$\operatorname{Var}_\theta(T) \ \ge\ \frac{\psi'(\theta)^2}{n I(\theta)} \qquad \text{for every } \theta \in \Theta.$$

Equality holds for every $\theta$ if and only if $U_n(\theta) = a(\theta)\,(T - \psi(\theta))$ with probability 1 for some function $a(\theta)$, that is, the score is an affine function of $T$. This happens exactly when $f$ is a one-parameter exponential family with sufficient statistic $T$, up to affine maps.

**Biased estimators.** If $T$ estimates $\theta$ with [bias](/estimator-bias/) $b(\theta) = \mathbb{E}_\theta T - \theta$, take $\psi(\theta) = \theta + b(\theta)$: $\operatorname{Var}_\theta(T) \ge (1 + b'(\theta))^2 / (n I(\theta))$.

**Theorem (vector form).** Let $\theta \in \Theta \subseteq \mathbb R^k$, let $T \in \mathbb R^m$ have $\mathbb{E}_\theta T = \psi(\theta)$ with finite second moments, let $D(\theta) = \partial \psi / \partial \theta$ be the $m \times k$ Jacobian, and let the $k \times k$ information matrix $I(\theta)$ be invertible. Under the conditions above,

$$\operatorname{Cov}_\theta(T) \ \succeq\ \frac{1}{n}\, D(\theta)\, I(\theta)^{-1}\, D(\theta)^\top,$$

where $A \succeq B$ means that $A - B$ is [positive semidefinite](/positive-definite-matrix/). In particular, for an unbiased estimator of one coordinate $\theta_j$, $\operatorname{Var}_\theta(T) \ge [I(\theta)^{-1}]_{jj}/n$, which is at least $1/(n I(\theta)_{jj})$: not knowing the other parameters can only raise the bound.

## In plain words

Information measures how sharply the probability of the data changes when the unknown quantity changes. If the data change a lot, they can pin down the unknown quantity well; if they change little, they cannot. The bound turns this into a number. Any method that is right on average must have a spread at least as large as one over the total information. More data add information, so the floor falls as the sample grows. The bound holds only for smooth models whose set of possible values does not move with the unknown quantity, and only for methods that are right on average.

## Proof

**One parameter.** Let $f_n(x; \theta) = \prod_i f(x_i; \theta)$ be the joint density, so $U_n(\theta) = \partial_\theta \log f_n(X; \theta)$ and $\partial_\theta f_n = U_n f_n$.

*Step 1: the score has mean zero and variance $n I(\theta)$.* By condition 4 applied to $\int f_n = 1$, $\mathbb{E}_\theta U_n = \int \partial_\theta f_n\, dx = \partial_\theta 1 = 0$. The terms of $U_n$ are iid, each with variance $I(\theta)$, so $\operatorname{Var}_\theta U_n = n I(\theta)$. (Condition 2 makes the support of $f_n$ fixed, so $\log f_n$ is defined on it for every $\theta$.)

*Step 2: the covariance of $T$ with the score.* By condition 4 applied to $\int T f_n$,

$$\psi'(\theta) = \partial_\theta \int T(x) f_n(x; \theta)\, dx = \int T(x)\, U_n(\theta) f_n(x; \theta)\, dx = \mathbb{E}_\theta[T U_n] = \operatorname{Cov}_\theta(T, U_n),$$

where the last step uses $\mathbb{E}_\theta U_n = 0$.

*Step 3: the Cauchy-Schwarz inequality.* For any two random variables with finite variance, $\operatorname{Cov}(A, B)^2 \le \operatorname{Var}(A)\operatorname{Var}(B)$, with equality if and only if one is an affine function of the other with probability 1. So

$$\psi'(\theta)^2 = \operatorname{Cov}_\theta(T, U_n)^2 \le \operatorname{Var}_\theta(T)\cdot n I(\theta),$$

and dividing by $n I(\theta) > 0$ (condition 5) gives the bound.

*Step 4: equality.* Since $\operatorname{Var}_\theta U_n > 0$, equality at $\theta$ holds if and only if $U_n(\theta) = a(\theta)(T - \psi(\theta))$ with probability 1 for some constant $a(\theta)$; taking the covariance with $T$ gives $a(\theta) = n I(\theta)/\psi'(\theta)$. If this holds for every $\theta$, integrate $\partial_\theta \log f_n = a(\theta) T - a(\theta)\psi(\theta)$ in $\theta$:

$$f_n(x; \theta) = h(x)\exp\big(\eta(\theta)\, T(x) - B(\theta)\big), \qquad \eta' = a, \quad B' = a\psi,$$

an exponential family in which $T$ is the sufficient statistic. Conversely, in such a family $U_n = \eta'(\theta)(T - \mathbb{E}_\theta T)$, so $T$ attains the bound for $\psi(\theta) = \mathbb{E}_\theta T$.

**Vector form.** As in Step 2, $\operatorname{Cov}_\theta(T, U_n) = D(\theta)$, and $\operatorname{Cov}_\theta(U_n) = n I(\theta)$. Let $W = T - D\,(nI)^{-1} U_n$. Then

$$0 \preceq \operatorname{Cov}_\theta(W) = \operatorname{Cov}_\theta(T) - 2 D (nI)^{-1} D^\top + D (nI)^{-1}(nI)(nI)^{-1} D^\top = \operatorname{Cov}_\theta(T) - \tfrac{1}{n} D I^{-1} D^\top,$$

because a [covariance matrix](/covariance-matrix/) is positive semidefinite. $\blacksquare$

## Consequences

**Efficient estimators are UMVUEs.** If an unbiased $T$ attains the bound at every $\theta$, no unbiased estimator has smaller variance anywhere, so $T$ is the [minimum variance unbiased estimator](/minimum-variance-unbiased-estimator/).

**Exact checks.** Each line gives the bound and the variance of an unbiased estimator.

| model | estimand | $I(\theta)$ | bound | estimator, variance |
|---|---|---|---|---|
| Bernoulli$(p)$ | $p$ | $1/(p(1-p))$ | $p(1-p)/n$ | $\bar X$, $p(1-p)/n$ (attains) |
| Poisson$(\lambda)$ | $\lambda$ | $1/\lambda$ | $\lambda/n$ | $\bar X$, $\lambda/n$ (attains) |
| $N(\mu, \sigma^2)$, $\sigma^2$ known | $\mu$ | $1/\sigma^2$ | $\sigma^2/n$ | $\bar X$, $\sigma^2/n$ (attains) |
| $N(\mu, \sigma^2)$, $\mu$ known | $\sigma^2$ | $1/(2\sigma^4)$ | $2\sigma^4/n$ | $\frac{1}{n}\sum_i (X_i - \mu)^2$, $2\sigma^4/n$ (attains) |
| $N(\mu, \sigma^2)$, both unknown | $\sigma^2$ | diagonal matrix | $2\sigma^4/n$ | $S^2$ (divisor $n - 1$), $2\sigma^4/(n-1)$ |
| Poisson$(\lambda)$ | $e^{-\lambda}$ | $1/\lambda$ | $\lambda e^{-2\lambda}/n$ | $(1 - 1/n)^T$, $e^{-2\lambda}(e^{\lambda/n} - 1)$ |

For Bernoulli data with $n = 4$ and $p = 1/3$, $I = 9/2$, $nI = 18$, and an exact sum over the 16 outcomes gives $\mathbb{E}\, U_4 = 0$, $\operatorname{Var}(U_4) = 18$ and $\operatorname{Var}(\bar X) = 1/18$, equal to the bound. In the last two rows the UMVUE stays above the bound, so no unbiased estimator attains it: for $e^{-\lambda}$ at $n = 5$, $\lambda = 1$, the UMVUE variance is $0.02996$ and the bound is $0.02707$. Since $e^{x} - 1 > x$, the gap is strict, but the ratio tends to 1 as $n \to \infty$.

**Asymptotic efficiency.** Under conditions stronger than those above, the maximum likelihood estimator satisfies $\sqrt n(\hat\theta - \theta) \to N(0, I(\theta)^{-1})$ in distribution: it attains the bound in the limit ([asymptotic normality of the MLE](/asymptotic-normality-of-mle/)). The bound also sets the scale of the standard error, $1/\sqrt{n I(\theta)}$.

**Design.** Since the bound depends on the design through $I$, maximizing a scalar function of the information matrix is the basis of [optimal experimental design](/optimal-experimental-design/).

## Tightness

**A moving support breaks the bound.** For Uniform$(0, \theta)$, condition 2 fails. The naive information is $\mathbb{E}[(\partial_\theta \log f)^2] = 1/\theta^2$, which would give the "bound" $\theta^2/n$. The unbiased estimator $\frac{n+1}{n}\max_i X_i$ has variance $\theta^2/(n(n+2))$, of order $1/n^2$; at $n = 5$ it is $\theta^2/35$, against the "bound" $\theta^2/5$.

**Biased estimators can go below.** The bound with $\psi(\theta) = \theta$ applies to unbiased estimators only. The constant estimator $T = \theta_0$ has variance zero. Shrinkage estimators such as the [James-Stein estimator](/james-stein-estimator/) trade a bias for a lower mean squared error.

**Superefficiency.** The asymptotic statement is not a bound at every point. Hodges's estimator, which replaces $\bar X$ by $0$ when $\lvert \bar X \rvert < n^{-1/4}$ in the normal mean problem, has asymptotic variance $0$ at $\theta = 0$ and $1/I$ elsewhere. Le Cam showed that such improvements can happen only on a set of parameter values of Lebesgue measure zero.

**Attainment is rare.** For a fixed $n$, the bound is attained for every $\theta$ only for affine functions of the mean of $T$ in a one-parameter exponential family (Step 4). For other estimands, the UMVUE, when it exists, lies strictly above it.

**Sharper bounds.** The Bhattacharyya bounds use higher derivatives of $f$ and are closer to the UMVUE variance. The Hammersley-Chapman-Robbins bound replaces the derivative by a difference,

$$\operatorname{Var}_\theta(T) \ge \sup_{\Delta \ne 0} \frac{(\psi(\theta + \Delta) - \psi(\theta))^2}{\mathbb{E}_\theta\big[(f_n(X; \theta + \Delta)/f_n(X; \theta) - 1)^2\big]},$$

and needs no differentiability, but needs the support of $f(\cdot\,; \theta + \Delta)$ to lie in that of $f(\cdot\,; \theta)$. The van Trees inequality is a Bayesian form that bounds the average mean squared error over a prior, for any estimator, biased or not.

## History

Fréchet (1943) and Darmois (1945) gave the inequality, and Rao (1945) and Cramér (1946) gave it independently in the forms that became standard. Rao's paper also contains the multiparameter form and the [Rao-Blackwell](/rao-blackwell-theorem/) argument. Fisher (1925) had defined the information and claimed that maximum likelihood is efficient in large samples. The name "information inequality", used by Lehmann and Casella, avoids the question of priority.

## References
