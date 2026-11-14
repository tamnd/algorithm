---
tag: 1WBGCK
kind: definition
slug: score-function
name: Score function
aliases:
- score vector
- gradient of the log-likelihood
area: statistics-and-inference/point-estimation
level: core
summary: The gradient of the log-likelihood with respect to the parameter. Under regularity it has mean zero, and its variance is the Fisher information.
prereqs: [likelihood-function, expected-value, variance]
see_also: [fisher-information-matrix, maximum-likelihood-estimation, cramer-rao-bound, score-test, fisher-scoring, wilson-score-interval, asymptotic-normality-of-mle, newton-raphson-method]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 7.3.2 (the derivative of the log-likelihood in the Cramér-Rao inequality and the information identity) and Section 10.3.2 (other large-sample tests, including the score test)
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 2, Section 2.5 (the information inequality) and Chapter 6 (likelihood equations)
  - paper: doi:10.1017/S0305004100009580
    title: R. A. Fisher, Theory of statistical estimation, Mathematical Proceedings of the Cambridge Philosophical Society 22(5), 1925
    locator: pages 700 to 725, the amount of information and the derivative of the log-likelihood
---

The score function is the derivative, or for a vector parameter the gradient, of the [log-likelihood](/likelihood-function/) with respect to the parameter. It tells how fast the log-likelihood changes when the parameter moves. At the true parameter value it is a random variable with mean zero, and its variance is the [Fisher information](/fisher-information-matrix/). Setting it to zero gives the likelihood equation of [maximum likelihood estimation](/maximum-likelihood-estimation/), and it is the main object behind the [Cramér-Rao bound](/cramer-rao-bound/), the [score test](/score-test/) and [Fisher scoring](/fisher-scoring/).

## Definition

Let $X_1, \ldots, X_n$ be iid with density or mass function $f(x; \theta)$, $\theta \in \Theta \subseteq \mathbb R^k$, with $\Theta$ open and $\log f(x; \theta)$ differentiable in $\theta$ for every $x$.

**Score of one observation.**

$$u(\theta; x) = \nabla_\theta \log f(x; \theta) = \frac{\nabla_\theta f(x; \theta)}{f(x; \theta)}, \qquad \text{where } f(x; \theta) > 0.$$

For $k = 1$ this is $\partial_\theta \log f(x; \theta)$.

**Score of the sample.** With $\ell(\theta; x) = \sum_i \log f(x_i; \theta)$,

$$U_n(\theta) = \nabla_\theta\, \ell(\theta; X) = \sum_{i=1}^n u(\theta; X_i).$$

For a fixed $\theta$, $U_n(\theta)$ is a random vector, a function of the data. For fixed data, $\theta \mapsto U_n(\theta)$ is a function of the parameter. Both readings are used, and the context says which.

**Fisher information.** $I(\theta) = \operatorname{Var}_\theta\, u(\theta; X_1)$ is the information of one observation, a $k \times k$ matrix for vector $\theta$, and $I_n(\theta) = n I(\theta) = \operatorname{Var}_\theta\, U_n(\theta)$ is the information of the sample.

**Observed information.** $J_n(\theta) = -\nabla_\theta^2\, \ell(\theta; X)$, minus the Jacobian of the score. It is a random matrix, and under the conditions below $\mathbb{E}_\theta J_n(\theta) = I_n(\theta)$.

### Properties

The properties below hold under the regularity conditions on the [Cramér-Rao bound](/cramer-rao-bound/) page: the support $\{x : f(x; \theta) > 0\}$ does not depend on $\theta$, and $\int f(x; \theta)\, dx$ can be differentiated under the integral sign (once for (a), twice for (c)).

**(a) Mean zero.** $\mathbb{E}_\theta\, u(\theta; X) = 0$.

*Proof.* $\mathbb{E}_\theta\, u = \int \frac{\nabla_\theta f}{f}\, f\, dx = \nabla_\theta \int f(x; \theta)\, dx = \nabla_\theta 1 = 0$. $\square$

The mean is zero only when the score and the distribution use the same $\theta$. For $\theta' \ne \theta$, $\mathbb{E}_\theta\, u(\theta'; X)$ is in general not zero; this is why the score detects a wrong parameter value.

**(b) Variance is the information.** By (a), $I(\theta) = \mathbb{E}_\theta[u\, u^\top]$, and for the sample $\operatorname{Var}_\theta U_n(\theta) = n I(\theta)$, because the terms are iid with mean zero.

**(c) Information identity.** $I(\theta) = -\mathbb{E}_\theta\, \nabla_\theta^2 \log f(X; \theta)$. Differentiate $\int u\, f\, dx = 0$ once more, and use $\nabla_\theta f = u f$. The [Fisher information matrix](/fisher-information-matrix/) page gives the details.

**(d) Covariance with an estimator.** If $T(X)$ has $\mathbb{E}_\theta T = \psi(\theta)$ and $\int T f\, dx$ can be differentiated under the integral, then $\operatorname{Cov}_\theta(T, U_n(\theta)) = \nabla_\theta \psi(\theta)$. With the Cauchy-Schwarz inequality this gives the [Cramér-Rao bound](/cramer-rao-bound/).

**(e) It depends on the data only through a sufficient statistic.** If $f(x; \theta) = g(t(x); \theta)\, h(x)$ ([factorization theorem](/fisher-neyman-factorization-theorem/)), then $U_n(\theta) = \nabla_\theta \log g(t(X); \theta)$, a function of $t(X)$.

**(f) Change of parameter.** If $\theta = \theta(\eta)$ with Jacobian $D = \partial\theta/\partial\eta$, the score in $\eta$ is $D^\top u(\theta; x)$, and the information becomes $D^\top I(\theta) D$.

**(g) Large samples.** By the central limit theorem, $U_n(\theta)/\sqrt n$ converges in distribution to $N(0, I(\theta))$ under $\theta$. This is the step behind the [asymptotic normality of the MLE](/asymptotic-normality-of-mle/) and the null distribution of the [score test](/score-test/). Under $\theta$, the sequence $U_1(\theta), U_2(\theta), \ldots$ is a sum of iid mean-zero terms, so it is a martingale in $n$.

**(h) Likelihood equation.** An interior maximum $\hat\theta$ of the likelihood solves $U_n(\hat\theta) = 0$. [Newton's method](/newton-raphson-method/) on this equation uses $J_n$; [Fisher scoring](/fisher-scoring/) replaces $J_n$ by $I_n$.

## Examples and non-examples

**Bernoulli.** $u(p; x) = \frac{x}{p} - \frac{1 - x}{1 - p} = \frac{x - p}{p(1-p)}$, so $U_n(p) = \frac{n(\bar X - p)}{p(1-p)}$ and $I(p) = 1/(p(1-p))$. The score is an affine function of $\bar X$, which is why $\bar X$ attains the Cramér-Rao bound.

**Poisson, on the sample $(3, 7, 7, 9, 14)$.** $u(\lambda; x) = x/\lambda - 1$, so $U_5(\lambda) = 40/\lambda - 5$ with $\sum_i x_i = 40$.

| $\lambda$ | $U_5(\lambda)$ | observed $J_5(\lambda) = 40/\lambda^2$ | expected $I_5(\lambda) = 5/\lambda$ |
|---|---|---|---|
| $5$ | $3$ | $8/5$ | $1$ |
| $8$ | $0$ | $5/8$ | $5/8$ |
| $10$ | $-1$ | $2/5$ | $1/2$ |

The score is positive below the maximum likelihood estimate $\hat\lambda = \bar x = 8$ and negative above it. At $\hat\lambda$ the observed and expected information agree, which holds for every Poisson sample.

**Normal with both parameters.** For $\theta = (\mu, \sigma^2)$,

$$u(\theta; x) = \Big(\frac{x - \mu}{\sigma^2},\ -\frac{1}{2\sigma^2} + \frac{(x - \mu)^2}{2\sigma^4}\Big), \qquad I(\theta) = \begin{pmatrix} 1/\sigma^2 & 0 \\ 0 & 1/(2\sigma^4) \end{pmatrix}.$$

On $(3, 7, 7, 9, 14)$, with $\bar x = 8$ and $\sum_i (x_i - \bar x)^2 = 64$: at $\mu = 6$, $\sigma^2 = 16$ the $\mu$ component is $(40 - 30)/16 = 5/8$; at $\mu = 8$, $\sigma^2 = 16$ the $\sigma^2$ component is $-5/32 + 64/512 = -1/32$. The $\sigma^2$ component is zero at $\sigma^2 = 64/5 = 12.8$, the maximum likelihood estimate with divisor $n$, not at $S^2 = 16$.

**Exponential.** For rate $\beta$, $f(x; \beta) = \beta e^{-\beta x}$, so $u = 1/\beta - x$ and $U_n(\beta) = n/\beta - \sum_i X_i$.

**Exponential families.** In natural form $h(x)\exp(\eta^\top T(x) - A(\eta))$, $u(\eta; x) = T(x) - \nabla A(\eta)$: the score is the sufficient statistic minus its mean.

**Non-example: a support that moves.** For Uniform$(0, \theta)$, $\log f = -\log\theta$ on the support, so $u = -1/\theta$ for every $x$ in $(0, \theta)$. Its mean is $-1/\theta \ne 0$. The support depends on $\theta$, the derivative does not pass under the integral, and properties (a) to (d) fail. The likelihood is maximized at $\max_i x_i$, where it is not differentiable, and the likelihood equation has no solution.

**Non-example: several roots.** For the Cauchy location model, $u(\theta; x) = \frac{2(x - \theta)}{1 + (x - \theta)^2}$. With two observations $x = (-a, a)$ and $a > 1$, $U_2(\theta) = 0$ has the three roots $0$ and $\pm\sqrt{a^2 - 1}$; at $a = 5$ these are $0$ and $\pm 4.899$. The root at $0$ is a local minimum of the likelihood. A zero of the score is not always a maximum.

### Pitfalls

- **Score in the parameter, not in the data.** In machine learning, "score" often means $\nabla_x \log p(x)$, the gradient with respect to the data point, used in score matching and diffusion models. That is a different object; this page is about $\nabla_\theta$.
- **Sign and scale.** Some texts define the score with $\log L$ for the full sample, others per observation, and some divide by $n$. The mean zero property holds in all of them; the variance scales accordingly.
- **The information identity needs two derivatives under the integral.** When only the first exists, $\mathbb{E}[u^2]$ is still the information, but $-\mathbb{E}[\partial^2 \log f]$ may differ from it.

## Related definitions

- [Fisher information matrix](/fisher-information-matrix/): the covariance matrix of the score.
- [Maximum likelihood estimation](/maximum-likelihood-estimation/): solves the likelihood equation $U_n(\hat\theta) = 0$; [Fisher scoring](/fisher-scoring/) and [Newton's method](/newton-raphson-method/) solve it numerically.
- [Score test](/score-test/): compares $U_n(\theta_0)$ with its null variance $I_n(\theta_0)$; for a binomial proportion, inverting it gives the [Wilson score interval](/wilson-score-interval/).
- [Cramér-Rao bound](/cramer-rao-bound/): the covariance of an unbiased estimator with the score gives a lower bound on its variance.

## References
