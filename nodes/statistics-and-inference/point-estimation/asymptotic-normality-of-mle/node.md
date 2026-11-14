---
tag: 3XKA6D
kind: theorem
slug: asymptotic-normality-of-mle
name: Asymptotic normality of the MLE
aliases:
- asymptotic efficiency of the MLE
area: statistics-and-inference/point-estimation
level: core
summary: Under regularity conditions a consistent root of the likelihood equation satisfies sqrt(n)(theta-hat - theta_0) -> N(0, I(theta_0)^(-1)), so it attains the Cramer-Rao bound in the limit.
prereqs: [maximum-likelihood-estimation, score-function, fisher-information-matrix, slutsky-theorem, kullback-leibler-divergence]
see_also: [cramer-rao-bound, wilks-theorem, wald-test, score-test, delta-method, m-estimator, bernstein-von-mises-theorem, fisher-scoring]
sources:
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 6, Section 6.3 (efficient likelihood estimation, one parameter, with Theorem 3.10 on consistent roots) and Section 6.5 (the multiparameter case)
  - book: isbn:9780521496032
    title: A. W. van der Vaart, Asymptotic Statistics, Cambridge University Press, 1998
    locator: Chapter 5, Section 5.5 (Theorem 5.39, asymptotic normality of the MLE under differentiability in quadratic mean); Chapter 7 (local asymptotic normality); Chapter 8 (superefficiency and the convolution theorem)
  - book: isbn:9780691005478
    title: Harald Cramér, Mathematical Methods of Statistics, Princeton University Press, 1946
    locator: Chapter 33 (properties of maximum likelihood estimates in large samples)
  - paper: "A. Wald, Note on the consistency of the maximum likelihood estimate, Annals of Mathematical Statistics 20(4), 1949"
    locator: pages 595 to 601 (consistency of the global maximizer)
  - paper: "J. Neyman and E. L. Scott, Consistent estimates based on partially consistent observations, Econometrica 16(1), 1948"
    locator: pages 1 to 32 (inconsistency of the MLE when the number of parameters grows with n)
  - paper: "L. Le Cam, On some asymptotic properties of maximum likelihood estimates and related Bayes' estimates, University of California Publications in Statistics 1, 1953"
    locator: pages 277 to 329 (the Hodges estimator and the result that superefficiency holds only on a set of Lebesgue measure zero)
---

Asymptotic normality of the MLE is the reason the [maximum likelihood estimator](/maximum-likelihood-estimation/) is the default estimator for parametric models. Under regularity conditions, a consistent root $\hat\theta_n$ of the likelihood equation is approximately normal with mean $\theta_0$ and covariance $I(\theta_0)^{-1}/n$, the inverse of the [Fisher information](/fisher-information-matrix/) of the sample. This is the [Cramér-Rao bound](/cramer-rao-bound/), so in the limit no regular estimator does better. The result gives the standard errors and [Wald tests](/wald-test/) of almost every fitted model, and it is the base of [Wilks' theorem](/wilks-theorem/) for likelihood ratio tests.

## Statement

Let $X_1, \ldots, X_n$ be observations with density or mass function $f(x; \theta)$, $\theta \in \Theta \subseteq \mathbb R^k$, and true value $\theta_0$. Write $\ell_n(\theta) = \sum_i \log f(X_i; \theta)$, $U_n(\theta) = \nabla_\theta \ell_n(\theta)$ for the [score](/score-function/), and $I(\theta) = \operatorname{Var}_\theta\,\nabla_\theta \log f(X_1; \theta)$ for the information of one observation.

**Conditions.**

1. $X_1, \ldots, X_n$ are iid with density $f(x; \theta_0)$.
2. The model is identifiable: $\theta \ne \theta'$ implies $f(\cdot; \theta) \ne f(\cdot; \theta')$ as distributions.
3. $\theta_0$ is an interior point of $\Theta$.
4. The support $\{x : f(x; \theta) > 0\}$ does not depend on $\theta$.
5. For every $x$, $\log f(x; \theta)$ is three times differentiable in $\theta$ on a neighbourhood $N$ of $\theta_0$, and every third partial derivative is bounded in absolute value on $N$ by a function $M(x)$ with $\mathrm E_{\theta_0} M(X) < \infty$.
6. $\int f(x; \theta)\,dx$ can be differentiated twice under the integral sign at $\theta_0$.
7. $I(\theta_0)$ is finite and positive definite.

**Conclusion.** With probability tending to 1 there is a root $\hat\theta_n$ of the likelihood equation $U_n(\theta) = 0$ such that $\hat\theta_n \xrightarrow{p} \theta_0$, and every such consistent sequence of roots satisfies

$$\sqrt n\,(\hat\theta_n - \theta_0) \xrightarrow{d} N_k\bigl(0,\ I(\theta_0)^{-1}\bigr).$$

If in addition the likelihood equation has a unique root for each $n$, or $\hat\theta_n$ is the global maximizer and the global maximizer is consistent (Wald 1949 gives conditions), then the conclusion holds for that estimator. The theorem is about a consistent root, not about every root and not always about the global maximizer.

**Studentized form.** If $\hat I_n$ is $I(\hat\theta_n)$ or the observed information $J_n(\hat\theta_n)/n$, then $\hat I_n \xrightarrow{p} I(\theta_0)$, and by [Slutsky's theorem](/slutsky-theorem/) $\sqrt n\,\hat I_n^{1/2}(\hat\theta_n - \theta_0) \xrightarrow{d} N_k(0, I_k)$. This gives the Wald interval $\hat\theta_{n,j} \pm z_{1-\alpha/2}\sqrt{(\hat I_n^{-1})_{jj}/n}$. Its coverage tends to $1 - \alpha$; it is not exact.

## In plain words

Pick the parameter value that makes the observed data most likely. When the model is smooth and the sample is large, this guess lands close to the truth. Its error is bell-shaped, centred at zero, and its spread shrinks like one over the square root of the sample size.

The spread is set by how sharply the likelihood peaks. A sharp peak means the data carry a lot of information about the parameter, and the error is small. No other well-behaved method can have a smaller spread in the limit, so the method is called efficient.

The result can fail when the range of possible data depends on the parameter, when the truth sits on the edge of the allowed values, or when the number of unknowns grows with the data.

## Proof

This is a proof for one parameter ($k = 1$). The vector case follows the same steps with matrices, but the existence of a consistent root needs a longer argument; it is given in Lehmann and Casella, Section 6.5. A version under weaker conditions, differentiability in quadratic mean, is van der Vaart, Theorem 5.39.

**Step 1: a consistent root exists.** Fix $a > 0$ small enough that $[\theta_0 - a, \theta_0 + a] \subset N$. By the strong [law of large numbers](/law-of-large-numbers/),

$$\frac1n\bigl(\ell_n(\theta_0) - \ell_n(\theta_0 \pm a)\bigr) \to D(\theta_0 \,\|\, \theta_0 \pm a)$$

almost surely, where $D$ is the [Kullback-Leibler divergence](/kullback-leibler-divergence/). By identifiability (condition 2) and the Gibbs inequality, both limits are strictly positive. So with probability tending to 1, $\ell_n(\theta_0) > \ell_n(\theta_0 - a)$ and $\ell_n(\theta_0) > \ell_n(\theta_0 + a)$. On that event the continuous function $\ell_n$ has a local maximum in the open interval $(\theta_0 - a, \theta_0 + a)$, which is a root of $U_n(\theta) = 0$. Let $\hat\theta_n$ be the root closest to $\theta_0$; it is a random variable because the set of roots is closed. Then $P(|\hat\theta_n - \theta_0| < a) \to 1$ for every small $a$, so $\hat\theta_n \xrightarrow{p} \theta_0$.

**Step 2: expand the score.** Let $\hat\theta_n$ be any consistent sequence of roots. On the event that $\hat\theta_n \in N$, Taylor's theorem gives a point $\theta_n^*$ between $\theta_0$ and $\hat\theta_n$ with

$$0 = U_n(\hat\theta_n) = U_n(\theta_0) + (\hat\theta_n - \theta_0)\,U_n'(\theta_0) + \tfrac12(\hat\theta_n - \theta_0)^2\,U_n''(\theta_n^*).$$

Solve for the error:

$$\sqrt n\,(\hat\theta_n - \theta_0) = \frac{n^{-1/2}\,U_n(\theta_0)}{-n^{-1}U_n'(\theta_0) - \tfrac12(\hat\theta_n - \theta_0)\,n^{-1}U_n''(\theta_n^*)}.$$

**Step 3: the numerator.** $U_n(\theta_0)$ is a sum of iid scores. By condition 6 they have mean 0 and variance $I(\theta_0)$ (properties (a) and (b) on the [score function](/score-function/) page). The [central limit theorem](/central-limit-theorem/) gives $n^{-1/2}U_n(\theta_0) \xrightarrow{d} N(0, I(\theta_0))$.

**Step 4: the denominator.** By the law of large numbers and the information identity (property (c), which uses condition 6), $-n^{-1}U_n'(\theta_0) \to I(\theta_0)$ almost surely. By condition 5, $|n^{-1}U_n''(\theta_n^*)| \le n^{-1}\sum_i M(X_i)$, which converges to $\mathrm E M(X) < \infty$, so it is bounded in probability. It is multiplied by $\hat\theta_n - \theta_0 \xrightarrow{p} 0$, so the product converges in probability to 0. Hence the denominator converges in probability to $I(\theta_0) > 0$ (condition 7).

**Step 5: combine.** The event $\hat\theta_n \in N$ has probability tending to 1, so it does not change limits in distribution. Part (c) of Slutsky's theorem gives

$$\sqrt n\,(\hat\theta_n - \theta_0) \xrightarrow{d} \frac{N(0, I(\theta_0))}{I(\theta_0)} = N\bigl(0, I(\theta_0)^{-1}\bigr). \qquad \blacksquare$$

Condition 3 is used in Step 1, where the interval around $\theta_0$ must lie inside $\Theta$. Condition 4 is used through condition 6, because differentiation under the integral sign fails when the limits of integration move with $\theta$.

## Consequences

**Standard errors and tests.** The inverse observed information $J_n(\hat\theta_n)^{-1}$ is the usual estimate of the covariance of $\hat\theta_n$. The [Wald test](/wald-test/) and the [score test](/score-test/) are built on the limit law above, and the [delta method](/delta-method/) carries it to smooth functions $g(\hat\theta_n)$, with asymptotic variance $\nabla g^{\mathsf T} I^{-1}\nabla g/n$. [Wilks' theorem](/wilks-theorem/) follows from the same expansion taken one order further.

**Efficiency, and its limits.** The asymptotic variance $I(\theta_0)^{-1}$ equals the [Cramér-Rao bound](/cramer-rao-bound/) for unbiased estimators. But asymptotic efficiency is not a statement about a fixed $n$. For iid exponential data with rate $\lambda$, the MLE is $\hat\lambda = 1/\bar X$ with $I(\lambda) = 1/\lambda^2$. Here $\mathrm E\hat\lambda = n\lambda/(n - 1)$, and the exact variance is $n^3/((n - 1)^2(n - 2))$ times the asymptotic variance $\lambda^2/n$. Because $2n\lambda\bar X$ is chi-square with $2n$ degrees of freedom, the coverage of the nominal 95% Wald interval $\hat\lambda \pm z_{0.975}\hat\lambda/\sqrt n$ and of the interval $\exp(\log\hat\lambda \pm z_{0.975}/\sqrt n)$ on the log scale can be computed exactly from the gamma distribution function:

| $n$ | exact variance / $(\lambda^2/n)$ | Wald coverage | log-scale coverage |
|---|---|---|---|
| 5 | 2.604 | 0.9562 | 0.9322 |
| 10 | 1.543 | 0.9549 | 0.9410 |
| 50 | 1.085 | 0.9512 | 0.9482 |
| 200 | 1.020 | 0.9503 | 0.9495 |

These numbers are computed, not proved; the theorem only says that each coverage tends to 0.95 and that the variance ratio tends to 1.

**Superefficiency.** Some estimators beat $I(\theta_0)^{-1}$ at single points. Hodges' estimator for $N(\theta, 1)$ data is $\bar X$ when $|\bar X| \ge n^{-1/4}$ and 0 otherwise. At $\theta = 0$ its limit variance is 0, and at every $\theta \ne 0$ it is 1, the same as for $\bar X$. The price is paid near 0. The values of $n\,\mathrm E(\hat\theta - \theta)^2$, computed from normal integrals, are:

| $n$ | at $\theta = 0$ | largest value over $\theta$ | at $\theta \approx$ |
|---|---|---|---|
| 100 | 0.0186 | 5.58 | $0.94\,n^{-1/4}$ |
| $10^4$ | below $10^{-6}$ | 68.9 | $0.88\,n^{-1/4}$ |
| $10^6$ | below $10^{-6}$ | 858 | $0.94\,n^{-1/4}$ |

The worst-case risk grows without bound. Le Cam (1953) proved that superefficiency can hold only on a set of Lebesgue measure zero, and the convolution and local minimax theorems (van der Vaart, Chapter 8) make "no regular estimator does better" exact.

**M-estimators and misspecification.** The proof uses only that $\hat\theta_n$ solves a sum of iid estimating equations with mean zero at $\theta_0$. Under a wrong model the same steps give the sandwich covariance of an [M-estimator](/m-estimator/), centred at the parameter that minimizes the Kullback-Leibler divergence to the true law.

**Computation.** [Fisher scoring](/fisher-scoring/) and Newton's method started from a $\sqrt n$-consistent estimate reach, after one step, an estimator with the same limit law as $\hat\theta_n$.

## Tightness

Each condition can fail, and the conclusion fails with it.

**The parameter on the boundary (condition 3).** Let $X_i \sim N(\theta, 1)$ with $\Theta = [0, \infty)$ and $\theta_0 = 0$. The MLE is $\max(\bar X, 0)$, and $\sqrt n\,\hat\theta_n \xrightarrow{d} \max(Z, 0)$ with $Z \sim N(0, 1)$: half of the limit mass sits at 0. The limit is not normal.

**A support that moves (condition 4).** For $X_i$ uniform on $(0, \theta)$ the MLE is $\max_i X_i$. The error is of order $1/n$, not $1/\sqrt n$, and $n(\theta - \max_i X_i)/\theta$ converges in distribution to the standard exponential law. The exact value $P(n(\theta - \max X_i)/\theta > 1) = (1 - 1/n)^n$ is 0.34868 at $n = 10$ and 0.36603 at $n = 100$, against the limit $e^{-1} = 0.36788$.

**The number of parameters grows with $n$ (condition 1 with fixed $k$).** Neyman and Scott (1948): let $X_{i1}, X_{i2} \sim N(\mu_i, \sigma^2)$ independent for $i = 1, \ldots, n$, with a new mean $\mu_i$ for each pair. The MLE of $\sigma^2$ is $\hat\sigma^2 = (4n)^{-1}\sum_i (X_{i1} - X_{i2})^2$, which converges almost surely to $\sigma^2/2$. The MLE is not even consistent.

**A model that is not identifiable (conditions 2 and 7).** In the mixture $p\,N(\mu, 1) + (1 - p)\,N(0, 1)$, every $(p, \mu)$ with $p = 0$ or $\mu = 0$ gives the same law $N(0, 1)$. At such a point the information matrix is singular and the limit law of the MLE is not normal.

**A model with infinite information.** If condition 7 fails because $I(\theta_0) = \infty$, the rate can be faster than $\sqrt n$, as in the uniform example.

## History

R. A. Fisher stated the asymptotic efficiency of maximum likelihood in the 1920s, with heuristic arguments. Harald Cramér gave a rigorous proof for a consistent root under conditions of the type listed above in his 1946 book. Abraham Wald (1949) proved consistency of the global maximizer under separate conditions. Joseph Hodges found his superefficient estimator around 1951, and Lucien Le Cam (1953) published it and showed that superefficiency can hold only on a null set, which started the local asymptotic theory that van der Vaart presents in Chapters 7 and 8. Neyman and Scott (1948) gave the classic example where the MLE fails with many nuisance parameters.

## References
