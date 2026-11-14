---
tag: ZWYWXA
kind: definition
slug: minimum-variance-unbiased-estimator
name: Minimum variance unbiased estimator
aliases:
- UMVUE
- MVUE
- uniformly minimum variance unbiased estimator
area: statistics-and-inference/point-estimation
level: core
summary: An unbiased estimator whose variance is no larger than that of any other unbiased estimator, for every value of the parameter.
prereqs: [estimator, estimator-bias, variance]
see_also: [lehmann-scheffe-theorem, rao-blackwell-theorem, cramer-rao-bound, complete-statistic, mean-squared-error, admissible-estimator, gauss-markov-theorem]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 7.3.2 (Definition 7.3.7, best unbiased estimator) and Section 7.3.3 (Theorem 7.3.20, uncorrelated with unbiased estimators of zero, and Theorem 7.3.23)
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 2, Section 2.1 (UMVU estimators)
  - paper: "E. L. Lehmann and Henry Scheffé, Completeness, similar regions, and unbiased estimation, Part I, Sankhya 10 (1950)"
    title: Lehmann and Scheffé 1950
    locator: uniformly minimum variance unbiased estimation through complete sufficient statistics
---

A minimum variance unbiased estimator (UMVUE) of a quantity $\psi(\theta)$ is an [unbiased](/estimator-bias/) estimator whose [variance](/variance/) is no larger than that of any other unbiased estimator, at every value of the parameter at the same time. Among unbiased estimators, variance equals [mean squared error](/mean-squared-error/), so the UMVUE is the best unbiased estimator under squared error. When it exists it is unique. The [Lehmann-Scheffé theorem](/lehmann-scheffe-theorem/) finds it as an unbiased function of a [complete](/complete-statistic/) [sufficient statistic](/sufficient-statistic/), and the [Cramér-Rao bound](/cramer-rao-bound/) gives a lower bound on its variance.

## Definition

The sample $X$ has distribution $P_\theta$, $\theta \in \Theta$, and $\psi(\theta)$ is the estimand. Let $\mathcal U_\psi$ be the set of estimators $\delta(X)$ with $\mathbb{E}_\theta\, \delta(X) = \psi(\theta)$ and $\operatorname{Var}_\theta\, \delta(X) < \infty$ for every $\theta$.

**UMVUE.** An estimator $\delta^* \in \mathcal U_\psi$ is a **uniformly minimum variance unbiased estimator** of $\psi(\theta)$ when

$$\operatorname{Var}_\theta(\delta^*) \le \operatorname{Var}_\theta(\delta) \qquad \text{for every } \delta \in \mathcal U_\psi \text{ and every } \theta \in \Theta.$$

"Uniformly" means that one estimator wins at every $\theta$. An estimator that has the smallest variance at one point $\theta_0$ only is *locally* minimum variance unbiased at $\theta_0$.

**Unbiased estimators of zero.** A statistic $U$ with $\mathbb{E}_\theta U = 0$ and $\operatorname{Var}_\theta U < \infty$ for every $\theta$ is an unbiased estimator of zero. Every member of $\mathcal U_\psi$ is $\delta + U$ for one fixed $\delta \in \mathcal U_\psi$ and some such $U$.

### Properties

**(a) Characterization.** $\delta \in \mathcal U_\psi$ is a UMVUE if and only if $\operatorname{Cov}_\theta(\delta, U) = 0$ for every unbiased estimator of zero $U$ and every $\theta$ (Casella and Berger, Theorem 7.3.20).

*Proof.* If $\operatorname{Cov}_{\theta_0}(\delta, U) = c \ne 0$ for some $U$ and $\theta_0$, then $U$ is not constant, and $\delta + aU$ with $a = -c/\operatorname{Var}_{\theta_0}(U)$ is unbiased with $\operatorname{Var}_{\theta_0}(\delta + aU) = \operatorname{Var}_{\theta_0}(\delta) - c^2/\operatorname{Var}_{\theta_0}(U)$, which is smaller. Conversely, if all such covariances are zero, any $\delta' \in \mathcal U_\psi$ is $\delta + U$ with $U = \delta' - \delta$, and $\operatorname{Var}_\theta(\delta') = \operatorname{Var}_\theta(\delta) + \operatorname{Var}_\theta(U) \ge \operatorname{Var}_\theta(\delta)$. $\square$

**(b) Uniqueness.** If $\delta_1$ and $\delta_2$ are both UMVUEs of $\psi(\theta)$, then $\delta_1 = \delta_2$ with probability 1 under every $\theta$.

*Proof.* $U = \delta_1 - \delta_2$ is an unbiased estimator of zero. By (a), $\operatorname{Cov}_\theta(\delta_1, U) = \operatorname{Cov}_\theta(\delta_2, U) = 0$, so $\operatorname{Var}_\theta(U) = \operatorname{Cov}_\theta(\delta_1 - \delta_2, U) = 0$. $\square$

**(c) Linearity.** If $\delta_1$ and $\delta_2$ are UMVUEs of $\psi_1(\theta)$ and $\psi_2(\theta)$, then $a\delta_1 + b\delta_2$ is the UMVUE of $a\psi_1(\theta) + b\psi_2(\theta)$, because the covariance condition in (a) is linear.

**(d) Three ways to find one.**
1. Find an unbiased function of a complete sufficient statistic ([Lehmann-Scheffé theorem](/lehmann-scheffe-theorem/)), for example by [Rao-Blackwellization](/rao-blackwell-theorem/) of a simple unbiased estimator.
2. Find an unbiased estimator whose variance equals the [Cramér-Rao bound](/cramer-rao-bound/). It is then a UMVUE, but this works only in exponential families with a matching estimand.
3. Check the covariance condition (a) directly.

## Examples and non-examples

**Common UMVUEs.** Each is an unbiased function of a complete sufficient statistic.

| model, iid sample of size $n$ | estimand | UMVUE | variance |
|---|---|---|---|
| Bernoulli$(p)$ | $p$ | $\bar X$ | $p(1-p)/n$ |
| Bernoulli$(p)$, $n \ge 2$ | $p(1-p)$ | $T(n - T)/(n(n-1))$, $T = \sum_i X_i$ | $2/81$ at $n = 3$, $p = 1/3$ |
| Poisson$(\lambda)$ | $e^{-\lambda}$ | $(1 - 1/n)^T$ | $e^{-2\lambda}(e^{\lambda/n} - 1)$ |
| $N(\mu, \sigma^2)$ | $\mu$ | $\bar X$ | $\sigma^2/n$ |
| $N(\mu, \sigma^2)$ | $\sigma^2$ | $S^2$, divisor $n - 1$ | $2\sigma^4/(n-1)$ |
| Uniform$(0, \theta)$ | $\theta$ | $\frac{n+1}{n}\max_i X_i$ | $\theta^2/(n(n+2))$ |

**Above the Cramér-Rao bound.** A UMVUE need not attain the Cramér-Rao bound. For the Poisson case at $n = 5$ and $\lambda = 1$, the UMVUE of $e^{-\lambda}$ has variance $e^{-2}(e^{0.2} - 1) \approx 0.02996$, and the bound is $\lambda e^{-2\lambda}/n \approx 0.02707$. No unbiased estimator does better than the UMVUE, so no unbiased estimator attains the bound here. For $\sigma^2$ in the normal model, $S^2$ has variance $2\sigma^4/(n-1)$ and the bound is $2\sigma^4/n$.

**Below the Cramér-Rao "bound".** For Uniform$(0, \theta)$ the support depends on $\theta$, so the Cramér-Rao conditions fail. The UMVUE variance $\theta^2/(n(n+2))$ falls like $1/n^2$, faster than any $c/n$.

**An absurd UMVUE.** Let $X$ be one Poisson$(\lambda)$ observation and $\psi(\lambda) = e^{-2\lambda}$. Then $\mathbb{E}_\lambda (-1)^X = e^{-\lambda}\sum_k (-\lambda)^k/k! = e^{-2\lambda}$, so $(-1)^X$ is unbiased. $X$ is complete, so it is the only unbiased estimator, and so the UMVUE. It takes only the values $1$ and $-1$, while $\psi(\lambda)$ lies in $(0, 1)$. The biased estimator $\max((-1)^X, 0) = \mathbf{1}\{X \text{ even}\}$ moves the value $-1$ closer to every possible $\psi(\lambda)$, so it has smaller mean squared error at every $\lambda$.

**Non-example: no unbiased estimator.** Let $X$ be Binomial$(n, p)$ and $\psi(p) = 1/p$. For any $\delta$, $\mathbb{E}_p\, \delta(X) = \sum_{x=0}^n \delta(x)\binom{n}{x}p^x(1-p)^{n-x}$ is a polynomial in $p$ of degree at most $n$. It stays bounded as $p \to 0$, so it cannot equal $1/p$. $\mathcal U_\psi$ is empty and there is no UMVUE.

**Non-example: unbiased estimators but no UMVUE.** Let $X$ take the value $-1$ with probability $p$ and the value $k \in \{0, 1, 2, \ldots\}$ with probability $(1-p)^2 p^k$, $0 < p < 1$. Here $\mathbb{E}_p X = 0$ for every $p$, and the unbiased estimators of zero are exactly $aX$, $a \in \mathbb R$ (see the bounded completeness example on [complete statistic](/complete-statistic/)). The indicator $\mathbf{1}\{X = -1\}$ is unbiased for $p$, so every unbiased estimator of $p$ is $\mathbf{1}\{X = -1\} + aX$. Its variance at $p$ is smallest for $a = (1-p)/2$, because $\operatorname{Cov}_p(\mathbf{1}\{X = -1\}, X) = -p$ and $\operatorname{Var}_p X = 2p/(1-p)$. The best $a$ changes with $p$, so no single estimator wins at every $p$.

### Pitfalls

- **Unbiased is not the same as good.** A biased estimator can have smaller mean squared error at every $\theta$. In the normal model, $\sum_i (X_i - \bar X)^2/(n+1)$ has mean squared error $2\sigma^4/(n+1)$, below the $2\sigma^4/(n-1)$ of the UMVUE $S^2$. The UMVUE can be [inadmissible](/admissible-estimator/).
- **Unbiasedness does not survive nonlinear maps.** $S^2$ is the UMVUE of $\sigma^2$, but $S$ is biased for $\sigma$; the UMVUE of $\sigma$ in the normal model is $S$ times a constant that depends on $n$.
- **The maximum likelihood estimator is not the UMVUE in general.** For $\sigma^2$ the MLE uses divisor $n$ and is biased; for Uniform$(0, \theta)$ the MLE is $\max_i X_i$, which is biased.
- **"Minimum variance" without "unbiased" is empty.** The constant estimator $\delta = c$ has variance zero. The restriction to unbiased estimators is what makes the problem meaningful.

## Related definitions

- [Estimator bias](/estimator-bias/) and [mean squared error](/mean-squared-error/): for unbiased estimators the mean squared error is the variance.
- Efficient estimator: an unbiased estimator whose variance equals the [Cramér-Rao bound](/cramer-rao-bound/). Every efficient estimator is a UMVUE; the converse fails.
- Best linear unbiased estimator: the minimum is taken only over linear unbiased estimators; in the linear model the least squares estimator is one ([Gauss-Markov theorem](/gauss-markov-theorem/)).
- [Admissible estimator](/admissible-estimator/): an estimator no other estimator beats everywhere, with no unbiasedness condition.

## References
