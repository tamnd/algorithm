---
tag: DWN5JT
kind: definition
slug: sample-variance
name: Sample variance
aliases:
- Bessel's correction
- unbiased sample variance
area: statistics-and-inference/point-estimation
level: intro
summary: The sum of squared deviations from the sample mean divided by n - 1. Dividing by n - 1 instead of n makes it unbiased for the population variance.
prereqs: [variance, estimator, estimator-bias]
see_also: [welford-algorithm, chan-parallel-variance, standard-error, mean-squared-error, catastrophic-cancellation, consistent-estimator, sampling-distribution, u-statistic]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 5.2 (the sample mean and the sample variance, and E S^2 = sigma^2) and Section 5.3.1 (the chi-square law of (n - 1) S^2 / sigma^2 for normal data)
  - book: isbn:9780471162407
    title: William G. Cochran, Sampling Techniques, third edition, Wiley, 1977
    locator: Chapter 2 (simple random sampling, the finite population variance with divisor N - 1)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 1.9 (computing the sample variance, the one-pass and two-pass formulas)
---

The sample variance of numbers $x_1, \ldots, x_n$ is the sum of their squared deviations from the sample mean, divided by $n - 1$. As an [estimator](/estimator/) of the population [variance](/variance/) $\sigma^2$ it is unbiased whenever $\sigma^2$ is finite, while the same sum divided by $n$ is biased downward by $\sigma^2/n$. The factor $n/(n-1)$ that turns the second into the first is Bessel's correction. This page is the definition and its exact properties; [Welford's algorithm](/welford-algorithm/) and the [Chan-Golub-LeVeque algorithm](/chan-parallel-variance/) are ways to compute it.

## Definition

Let $X_1, \ldots, X_n$ be the sample, $n \ge 2$, with sample mean $\bar X = \frac1n \sum_{i=1}^n X_i$. The sample variance is

$$S^2 = \frac{1}{n - 1} \sum_{i=1}^{n} (X_i - \bar X)^2,$$

and the sample standard deviation is $S = \sqrt{S^2}$. The version with divisor $n$ is written here as

$$\hat\sigma^2 = \frac{1}{n} \sum_{i=1}^{n} (X_i - \bar X)^2 = \frac{n - 1}{n} S^2.$$

It is the maximum likelihood estimator of $\sigma^2$ for normal data. Both are defined on the observed values $x_i$ by the same formulas. For $n = 1$, $S^2$ is not defined, and $\hat\sigma^2 = 0$.

**Equal forms.** Write $\mathrm{SS} = \sum_i (x_i - \bar x)^2$. For all real $x_1, \ldots, x_n$:

1. $\mathrm{SS} = \sum_i x_i^2 - n\bar x^2$. Expand $(x_i - \bar x)^2$ and use $\sum_i x_i = n\bar x$.
2. $\mathrm{SS} = \sum_i (x_i - c)^2 - n(\bar x - c)^2$ for every real $c$. This is form 1 applied to $x_i - c$, whose mean is $\bar x - c$ and whose $\mathrm{SS}$ is the same. So $S^2$ does not change when every value is shifted by $c$.
3. $\mathrm{SS} = \frac{1}{n} \sum_{i<j} (x_i - x_j)^2$, so $S^2 = \frac{1}{n(n-1)} \sum_{i<j} (x_i - x_j)^2$. *Proof.* $\sum_{i=1}^n \sum_{j=1}^n (x_i - x_j)^2 = 2n\sum_i x_i^2 - 2(\sum_i x_i)^2 = 2n\,\mathrm{SS}$ by form 1, and the double sum counts each pair $i < j$ twice. $\blacksquare$ Form 3 shows that $S^2$ is the [U-statistic](/u-statistic/) with kernel $(x - y)^2/2$.

The forms are equal in exact arithmetic only. In floating point, form 1 subtracts two large, nearly equal numbers when $\lvert \bar x \rvert$ is large compared with the spread, and it can lose every digit ([catastrophic cancellation](/catastrophic-cancellation/)). Form 2 with $c$ near $\bar x$ is the cure used by the shifted and two-pass methods.

**Unbiasedness.** Let $X_1, \ldots, X_n$ be uncorrelated with common mean $\mu$ and common variance $\sigma^2 < \infty$. Then $\mathbb{E}[S^2] = \sigma^2$ and $\mathbb{E}[\hat\sigma^2] = \frac{n-1}{n}\sigma^2$.

*Proof.* Form 2 with $c = \mu$ gives $\mathrm{SS} = \sum_i (X_i - \mu)^2 - n(\bar X - \mu)^2$. Take expectations: $\mathbb{E}[(X_i - \mu)^2] = \sigma^2$ for each $i$, and $\mathbb{E}[(\bar X - \mu)^2] = \operatorname{Var}(\bar X) = \sigma^2/n$ for uncorrelated data (see [standard error](/standard-error/)). So $\mathbb{E}[\mathrm{SS}] = n\sigma^2 - \sigma^2 = (n - 1)\sigma^2$. Divide by $n - 1$ and by $n$. $\blacksquare$

The deviations $X_i - \bar X$ sum to zero, so only $n - 1$ of them are free; the divisor $n - 1$ is the number of these degrees of freedom. Measuring the spread around $\bar X$, which is fitted to the same data, gives a smaller sum than measuring it around the true $\mu$, and the loss is exactly one $\sigma^2$ on average.

**Further properties.**

- *Normal data.* For iid $N(\mu, \sigma^2)$ data, $(n - 1)S^2/\sigma^2$ has the chi-square law with $n - 1$ degrees of freedom and is independent of $\bar X$ (see [sampling distribution](/sampling-distribution/)). So $\operatorname{Var}(S^2) = 2\sigma^4/(n - 1)$, the variance of that chi-square law times $\sigma^4/(n-1)^2$.
- *The divisor and the mean squared error.* Unbiased does not mean best in squared error. For normal data the divisor $n + 1$ gives the smallest [mean squared error](/mean-squared-error/) among the divisors; that page has the computation.
- *$S$ is biased for $\sigma$.* $\mathbb{E}[S] < \sigma$ unless $S$ is constant; see [bias of an estimator](/estimator-bias/) for the exact factor under normality.
- *Consistency.* For iid data with $\sigma^2 < \infty$, $S^2 \to \sigma^2$ in probability; the proof is on [consistent estimator](/consistent-estimator/). The same argument with the strong law of large numbers gives almost sure convergence.

## Examples and non-examples

**A sample of five.** For $x = (3, 7, 7, 9, 14)$, $\bar x = 40/5 = 8$.

| $x_i$ | 3 | 7 | 7 | 9 | 14 | sum |
|---|---|---|---|---|---|---|
| $x_i - \bar x$ | $-5$ | $-1$ | $-1$ | 1 | 6 | 0 |
| $(x_i - \bar x)^2$ | 25 | 1 | 1 | 1 | 36 | 64 |

So $S^2 = 64/4 = 16$, $S = 4$ and $\hat\sigma^2 = 64/5 = 12.8$. Form 1 gives $\sum_i x_i^2 - n \bar x^2 = 384 - 320 = 64$. The 10 pairwise squared differences sum to $320 = 5 \cdot 64$, as form 3 states.

**A proportion.** For 0 and 1 data with sample proportion $\hat p$, $\sum_i x_i^2 = n\hat p$, so $\hat\sigma^2 = \hat p(1 - \hat p)$ and $S^2 = \frac{n}{n-1}\hat p(1 - \hat p)$.

**A finite population.** For a whole finite population $y_1, \ldots, y_N$ there is nothing to estimate: its variance has divisor $N$. Survey sampling texts still define $S_U^2 = \frac{1}{N-1}\sum_i (y_i - \bar y_U)^2$, because with this divisor the sample variance $S^2$ of a simple random sample drawn without replacement is unbiased for $S_U^2$ (Cochran, Chapter 2). Say which divisor a formula uses.

**Frequency weights.** If value $x_i$ occurs $w_i$ times (integer $w_i$), the sample variance of the expanded data is $\frac{1}{W - 1}\sum_i w_i (x_i - \bar x_w)^2$ with $W = \sum_i w_i$ and $\bar x_w = \frac1W \sum_i w_i x_i$. Weights that express precision instead of counts need a different correction.

**Non-example: dividing by $n - 1$ around the true mean.** If $\mu$ is known, $\frac1n \sum_i (X_i - \mu)^2$ is unbiased. Dividing it by $n - 1$ would bias it upward. The correction belongs to deviations from $\bar X$ only.

**Non-example: the mean absolute deviation.** $\frac1n\sum_i \lvert x_i - \bar x \rvert$ measures spread too, but it is not a variance, and it is not unbiased for $\sigma$ or for $\sigma^2$.

## Related definitions

- [Variance](/variance/): the population quantity $\sigma^2 = \mathbb{E}[(X - \mu)^2]$ that $S^2$ estimates.
- [Standard error](/standard-error/): $S/\sqrt n$ estimates the standard error of $\bar X$.
- [Welford's algorithm](/welford-algorithm/): computes $\bar x$ and $\mathrm{SS}$ in one pass and in constant memory, without the cancellation of form 1.
- [Chan-Golub-LeVeque algorithm](/chan-parallel-variance/): combines the $(n, \bar x, \mathrm{SS})$ of two parts into those of their union, for parallel and pairwise computation.
- [Covariance matrix](/covariance-matrix/): the sample covariance uses the same divisor $n - 1$ and the same forms.
- [U-statistic](/u-statistic/): form 3 makes $S^2$ the simplest nontrivial example.

## References
