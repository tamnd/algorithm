---
tag: CYEN4M
kind: algorithm
slug: james-stein-estimator
name: James-Stein estimator
aliases:
- Stein shrinkage estimator
- Stein's paradox
area: statistics-and-inference/point-estimation
level: advanced
summary: Shrinks the sample means of three or more normal means toward zero by a data-driven factor. It has lower total squared error than the sample means for every parameter value.
model: real-ram
complexity:
  vars: {p: the number of means}
  time: {worst: Θ(p), best: Θ(p)}
  space: {extra: Θ(p)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1961
  people: [Charles Stein, Willard James]
  note: Stein proved in 1956 that the sample mean of three or more normal means is inadmissible under total squared error. James and Stein gave the explicit estimator and its risk in 1961.
prereqs: [admissible-estimator, statistical-decision-theory, mean-squared-error]
see_also: [empirical-bayes, bayes-estimator, ridge-regression, hierarchical-bayesian-model, minimum-variance-unbiased-estimator, cramer-rao-bound, tikhonov-regularization, lasso-regression]
sources:
  - paper: "W. James and Charles Stein, Estimation with quadratic loss, Proceedings of the Fourth Berkeley Symposium on Mathematical Statistics and Probability, volume 1 (1961), pages 361 to 379"
    title: James and Stein 1961
    locator: the estimator (1 - (p - 2)/||X||^2) X, its risk, and the version with an estimated variance
  - paper: "Charles Stein, Inadmissibility of the usual estimator for the mean of a multivariate normal distribution, Proceedings of the Third Berkeley Symposium on Mathematical Statistics and Probability, volume 1 (1956), pages 197 to 206"
    title: Stein 1956
    locator: the sample mean is admissible for p = 1 and 2 and inadmissible for p of 3 or more
  - paper: doi:10.1080/01621459.1973.10481350
    title: Bradley Efron and Carl Morris, Stein's estimation rule and its competitors, an empirical Bayes approach, Journal of the American Statistical Association 68(341) (1973), pages 117 to 130
    locator: the empirical Bayes derivation and the positive-part rule
  - paper: "A. J. Baranchik, Multiple regression and estimation of the mean of a multivariate normal distribution, Technical Report 51, Department of Statistics, Stanford University, 1964"
    title: Baranchik 1964
    locator: the positive-part estimator and its dominance over the James-Stein estimator
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 5 (minimaxity and admissibility, shrinkage estimators of a normal mean)
  - book: isbn:9780387402727
    title: Larry Wasserman, All of Statistics, Springer, 2004
    locator: Chapter 12, Section 12.7 (Stein's Paradox)
---

The James-Stein estimator estimates $p \ge 3$ normal means at once. It takes the vector of observations $X$ and multiplies it by the factor $1 - (p-2)\sigma^2/\lVert X \rVert^2$, which pulls every coordinate toward zero, more strongly when $\lVert X \rVert$ is small. Its expected total squared error is smaller than that of $X$ itself for every value of the true means, so the obvious estimator $X$, which is unbiased, minimax and the maximum likelihood estimator, is [inadmissible](/admissible-estimator/). Stein (1956) proved that $X$ can be beaten, and James and Stein (1961) gave the estimator. The fact that combining unrelated estimation problems helps is called Stein's paradox. The computation is one pass over the data, $\Theta(p)$ time.

## In plain words

Suppose you measure several unrelated quantities, each with the same amount of normal noise, and you care about the total squared error. The natural answer is to report each measurement as it is. Stein found that, with three or more quantities, you can do better on average by pulling all the measurements part of the way toward zero, or toward any fixed point chosen in advance. How far to pull is decided by the data: if the measurements are close to the point, they are mostly noise and you pull hard; if they are far away, you pull little. The total error goes down for every possible truth, but the error of a single quantity can go up.

## The problem

**Input.** One observation $x \in \mathbb R^p$ of $X \sim N_p(\theta, \sigma^2 I_p)$, with $p \ge 3$ and a known $\sigma^2 > 0$, and optionally a target $m \in \mathbb R^p$ fixed before seeing the data (default $m = 0$). In practice $X_i$ is often the mean of $n_i$ observations of group $i$, with $\sigma^2$ the variance of that mean.

**Output.** An estimate $\hat\theta \in \mathbb R^p$.

**Goal.** Small risk under the total squared error loss

$$L(\theta, \hat\theta) = \lVert \hat\theta - \theta \rVert^2 = \sum_{i=1}^p (\hat\theta_i - \theta_i)^2, \qquad R(\theta, \hat\theta) = \mathbb{E}_\theta\, L(\theta, \hat\theta(X)).$$

The estimator $\hat\theta = X$ has risk $p\sigma^2$ for every $\theta$ (see [statistical decision theory](/statistical-decision-theory/)).

## The algorithm

```pseudo id=main
JAMES-STEIN(x, σ², m, positive)        ▷ x, m ∈ ℝᵖ with p ≥ 3; σ² > 0
L1  p ← length of x
L2  s ← Σᵢ (xᵢ - mᵢ)²
L3  if s = 0 then return m
L4  k ← (p - 2) σ²
L5  if positive and s ≤ k then return m
L6  for i ← 1 to p do  θ̂ᵢ ← mᵢ + (1 - k/s)(xᵢ - mᵢ)
L7  return θ̂
```

Line L2 measures the squared distance of the data from the target. Line L6 moves each coordinate toward $m_i$ by the common factor $c = 1 - (p-2)\sigma^2/s$. When $s < (p-2)\sigma^2$, the plain factor $c$ is negative and the estimate jumps past the target to the other side. The positive-part variant (L5, `positive` true) uses $\max(c, 0)$ and returns the target instead, which is never worse. Line L3 handles $s = 0$, which has probability zero.

## Example

Take $p = 5$, $\sigma^2 = 1$, $m = 0$ and $x = (2, -1, 0.5, 1.5, -0.5)$.

1. L2: $s = 4 + 1 + 0.25 + 2.25 + 0.25 = 7.75$.
2. L4: $k = 3$, so $c = 1 - 3/7.75 = 19/31 \approx 0.6129$.
3. L6: $\hat\theta = c\, x \approx (1.2258, -0.6129, 0.3065, 0.9194, -0.3065)$.

Every coordinate moves $38.7\%$ of the way to zero. With $x$ scaled by $1/4$, $s = 0.484 < 3$: the plain factor is $1 - 3/0.484 \approx -5.19$, and the positive-part version returns $0$.

**Exact risk** (from the theorem in Correctness, with $\sigma^2 = 1$; $X$ itself has risk $p$):

| $\lVert \theta - m \rVert^2$ | $0$ | $1$ | $5$ | $10$ | $25$ | $100$ |
|---|---|---|---|---|---|---|
| $p = 3$ | $2.0000$ | $2.2752$ | $2.7437$ | $2.8843$ | $2.9582$ | $2.9899$ |
| $p = 5$ | $2.0000$ | $2.5230$ | $3.6613$ | $4.2041$ | $4.6551$ | $4.9109$ |
| $p = 10$ | $2.0000$ | $2.7378$ | $4.7837$ | $6.2091$ | $7.9640$ | $9.3969$ |

**Measured risk.** A simulation with `random.Random(20240601)`, $p = 5$, $\theta = (\sqrt\lambda, 0, 0, 0, 0)$ and 20000 draws for each $\lambda$ gave the averages below. The plain column agrees with the exact risk within two standard errors; the positive-part column is only measured.

| $\lambda = \lVert \theta \rVert^2$ | exact plain risk | plain, measured | positive part, measured | $X$, measured |
|---|---|---|---|---|
| $0$ | $2.0000$ | $2.010 \pm 0.028$ | $1.431$ | $5.051$ |
| $5$ | $3.6613$ | $3.655 \pm 0.018$ | $3.498$ | $4.979$ |
| $25$ | $4.6551$ | $4.687 \pm 0.021$ | $4.686$ | $5.032$ |

## Correctness

With $m = 0$ and $\sigma^2 = 1$ (the general case follows by a change of variable), the risk is

$$R(\theta, \hat\theta^{JS}) = p - (p - 2)^2\, \mathbb{E}_\theta\Big[\frac{1}{\lVert X \rVert^2}\Big] < p.$$

The proof writes $\hat\theta^{JS} = X - g(X)$ with $g(x) = (p-2)x/\lVert x \rVert^2$ and uses Stein's identity $\mathbb{E}[(X_i - \theta_i) g_i(X)] = \mathbb{E}[\partial_i g_i(X)]$, which is integration by parts against the normal density. The divergence of $g$ is $(p-2)^2/\lVert x \rVert^2$, and $\lVert g \rVert^2$ is the same, which gives the formula. The expectation $\mathbb{E}[1/\lVert X \rVert^2]$ is finite only for $p \ge 3$, and equals the Poisson mixture $\sum_k e^{-\lambda/2}\frac{(\lambda/2)^k}{k!}\frac{1}{p - 2 + 2k}$ with $\lambda = \lVert \theta \rVert^2$. At $\theta = 0$ it is $1/(p-2)$, so the risk is exactly $2$ for every $p \ge 3$. The risk rises with $\lVert \theta \rVert$ and tends to $p$. The full proof is in proofs/correctness.md. It also shows that $p - (p-2)^2/\lVert X \rVert^2$ is an unbiased estimate of the risk (Stein's unbiased risk estimate).

What is proved: the risk formula, the domination of $X$, and the value $2$ at the target. What is only cited and measured: the dominance of the positive-part version over the plain one (Baranchik 1964).

## Complexity

One pass computes $s$, and a second pass writes the $p$ outputs: $\Theta(p)$ arithmetic operations, best and worst case. Extra space is $\Theta(p)$: the output, and in the implementation also the differences $x - m$. The exact risk function in the implementation sums $O(\sqrt{\lambda} + 1)$ Poisson terms.

## Properties

- **Dominates $X$ for $p \ge 3$.** The risk is below $p\sigma^2$ at every $\theta$, with the largest gain, risk $2\sigma^2$ instead of $p\sigma^2$, at $\theta = m$.
- **Biased.** $\mathbb{E}_\theta \hat\theta^{JS} \ne \theta$ for $\theta \ne m$. It does not contradict the [Cramér-Rao bound](/cramer-rao-bound/), which concerns unbiased estimators, or the optimality of $X$ as the [minimum variance unbiased estimator](/minimum-variance-unbiased-estimator/).
- **Minimax.** $X$ is minimax with maximum risk $p\sigma^2$, and the James-Stein estimator has risk below $p\sigma^2$, so it is minimax too.
- **Not admissible.** The positive-part estimator dominates it. The positive-part estimator is also inadmissible, but the known estimators that dominate it are complicated and the gain is very small.
- **Depends on the target.** The gain is large only when $\theta$ is near $m$ relative to $\sqrt p\,\sigma$. Far from $m$ the factor is close to $1$ and the estimate is close to $X$.
- **Not translation equivariant** unless the target moves with the data, as in the variant toward the mean.

## Variants and improvements

- **Positive part.** $\hat\theta^{JS+} = m + \max\big(0, 1 - (p-2)\sigma^2/\lVert x - m \rVert^2\big)(x - m)$. It dominates the plain estimator (Baranchik 1964).
- **Shrinking toward the mean (Lindley).** For $p \ge 4$, $\hat\theta_i = \bar x + \big(1 - (p-3)\sigma^2/\sum_j (x_j - \bar x)^2\big)(x_i - \bar x)$. The mean direction is not shrunk, so the factor uses $p - 3$, and the risk is below $p\sigma^2$ everywhere and equal to $3\sigma^2$ when all $\theta_i$ are equal. The implementation has it as `james_stein_toward_mean`.
- **Unknown variance.** If $S$ is independent of $X$ with $S/\sigma^2 \sim \chi^2_\nu$, the factor $1 - (p-2)S/((\nu + 2)\lVert X \rVert^2)$ also dominates $X$ (James and Stein 1961).
- **Empirical Bayes view.** If $\theta_i \sim N(0, \tau^2)$ independently, the [Bayes estimator](/bayes-estimator/) is $(1 - \sigma^2/(\sigma^2 + \tau^2))X$. Marginally $\lVert X \rVert^2 \sim (\sigma^2 + \tau^2)\chi^2_p$, so $(p-2)\sigma^2/\lVert X \rVert^2$ is an unbiased estimate of the shrinkage $\sigma^2/(\sigma^2 + \tau^2)$. The James-Stein estimator is this Bayes rule with the prior variance estimated from the data, which is [empirical Bayes](/empirical-bayes/) (Efron and Morris 1973). A full [hierarchical model](/hierarchical-bayesian-model/) puts a prior on $\tau^2$ instead.
- **Regression.** [Ridge regression](/ridge-regression/) shrinks least squares coefficients toward zero with a fixed penalty; in an orthonormal design it multiplies each coefficient by the same factor, like the James-Stein rule with a factor chosen by the user instead of by the data.
- **Unequal variances and general quadratic loss.** Versions exist for $X \sim N_p(\theta, \Sigma)$ and weighted losses; the factor uses $\Sigma$ and the loss matrix (Lehmann and Casella, Chapter 5).

## When to use it

Use it when you estimate many similar means with known or well estimated noise levels, and the total error matters more than the error of any single mean: batting averages, small-area rates, test scores of many schools, the effects of many genes. Use the positive-part version, and shrink toward a sensible target, such as the grand mean, so that the gain is large. Do not use it when the error of one particular coordinate matters, when $p \le 2$, or when the noise is far from normal or has very different variances without a model for them.

## Pitfalls

- **The gain is for the total, not for each coordinate.** A single coordinate with an unusual true value can have a larger error than with $X$. The coordinates with the most extreme true values usually suffer most. Rules that limit how far each coordinate can move reduce this problem.
- **The target must be fixed before seeing the data.** Choosing $m$ after looking at $x$ breaks the risk formula. Shrinking toward the data mean is fine only with the $p - 3$ factor of Lindley's variant.
- **The plain factor can be negative.** When $\lVert x - m \rVert^2 < (p-2)\sigma^2$, the plain estimate is on the other side of the target. Use the positive-part version.
- **$\sigma^2$ must be right.** Using a wrong $\sigma^2$ changes the factor; if it is too large, the estimator can lose to $X$.
- **Confidence statements.** The usual intervals $X_i \pm z\sigma$ are not centered at the James-Stein estimate; recentering them without adjustment does not keep the coverage.

## Implementations

## History

Stein (1956) showed that for the mean of a $p$-dimensional normal distribution under total squared error, $X$ is admissible when $p = 1$ or $2$ and inadmissible when $p \ge 3$. James and Stein (1961) gave the explicit estimator $(1 - (p-2)/\lVert X \rVert^2)X$, computed its risk, and treated an unknown variance. Baranchik (1964) studied the positive-part rule. Efron and Morris (1973) explained the estimator as empirical Bayes and made it popular with data examples, such as predicting baseball batting averages.

## References
