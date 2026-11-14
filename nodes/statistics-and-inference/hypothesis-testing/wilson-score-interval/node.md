---
tag: H3CD21
kind: algorithm
slug: wilson-score-interval
name: Wilson score interval
aliases:
- Wilson interval
area: statistics-and-inference/hypothesis-testing
level: core
summary: A confidence interval for a binomial p that inverts the score test by solving a quadratic. Coverage is near 1 - alpha on average but dips below it for some p.
model: real-ram
complexity:
  vars: {n: the number of trials}
  time: {worst: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1927
  people: [Edwin B. Wilson]
  note: Wilson derived the interval in 1927 by solving the normal approximation for p instead of plugging in the estimate. Agresti and Coull (1998) and Brown, Cai and DasGupta (2001) made it a standard recommendation.
prereqs: [binomial-distribution, confidence-interval, z-test, central-limit-theorem]
see_also: [clopper-pearson-interval, binomial-test, score-test, test-interval-duality, score-function, quadratic-formula, wald-test, credible-interval]
sources:
  - paper: doi:10.1080/01621459.1927.10502953
    title: Edwin B. Wilson, Probable inference, the law of succession, and statistical inference, Journal of the American Statistical Association 22(158), 1927
    locator: pp. 209 to 212
  - paper: doi:10.1214/ss/1009213286
    title: Lawrence D. Brown, T. Tony Cai and Anirban DasGupta, Interval estimation for a binomial proportion, Statistical Science 16(2), 2001
    locator: pp. 101 to 133 (the oscillating coverage of the Wald interval and the comparison with the Wilson, Agresti-Coull and Jeffreys intervals)
  - paper: doi:10.2307/2685469
    title: Alan Agresti and Brent A. Coull, Approximate is better than "exact" for interval estimation of binomial proportions, The American Statistician 52(2), 1998
    locator: pp. 119 to 126 (the score interval and the add two successes and two failures interval)
  - book: isbn:9780470463635
    title: Alan Agresti, Categorical Data Analysis, third edition, Wiley, 2013
    locator: Section 1.4 (the Wald, score and likelihood-ratio intervals for a binomial parameter)
---

The Wilson score interval is a confidence interval for the success probability $p$ of a [binomial distribution](/binomial-distribution/). It is the set of $p_0$ that the two-sided score test, the [z-test](/z-test/) for one proportion with the null variance $p_0(1 - p_0)/n$, does not reject. That set is the solution of a quadratic inequality in $p_0$, so the interval has a closed form. Its center is pulled from $\hat p = x/n$ toward $1/2$, it never leaves $[0, 1]$, and it has positive length when $x = 0$ or $x = n$. Its coverage is not guaranteed: it is close to $1 - \alpha$ on average over $p$, but it dips below $1 - \alpha$ for many $p$, and to about $0.84$ near the ends at the 95% level for every $n$.

## In plain words

The usual quick interval takes the observed rate and adds and subtracts about two standard errors, with the standard error computed from the observed rate. That fails badly when the rate is near 0 or 1, or when there are few trials. With 0 successes it gives an interval of length zero.

Wilson's idea is to ask, for each candidate rate, whether the observed count is within about two standard errors of what that candidate predicts, with the standard error computed from the candidate. The candidates that pass form the interval. The answer comes from solving a quadratic equation, so no search is needed. The interval is a little shifted toward one half, which is what makes it behave well. It is usually shorter than the exact Clopper-Pearson interval, but it does not promise its level at every rate.

## The problem

**Input.** A count $x \in \{0, \ldots, n\}$ from $X \sim \text{Binomial}(n, p)$ with $n \ge 1$, and a level $\alpha \in (0, 1)$.

**Output.** An interval $[L, U] \subseteq [0, 1]$.

**Construction.** Inversion of the score test, by [test-interval duality](/test-interval-duality/). Let $z = z_{1 - \alpha/2}$ be the upper $\alpha/2$ point of the standard normal law, $z_{0.975} \approx 1.959964$. The interval is

$$\big\{ p : (x - np)^2 \le z^2\, n p (1 - p) \big\} = [\,c - h,\; c + h\,],$$

$$c = \frac{x + z^2/2}{n + z^2}, \qquad h = \frac{z}{n + z^2} \sqrt{\frac{x(n - x)}{n} + \frac{z^2}{4}}.$$

**Coverage.** Asymptotic and not uniform: for each fixed $p \in (0, 1)$ the coverage tends to $1 - \alpha$ as $n \to \infty$ (by the [central limit theorem](/central-limit-theorem/)), but for every $n$ there are $p$ where it is well below $1 - \alpha$. The coverage is marginal over $X$ at a fixed $p$.

## The algorithm

```pseudo id=main
WILSON(x, n, α)
L1  z ← the upper α/2 point of N(0, 1)
L2  c ← (x + z²/2) / (n + z²)
L3  h ← z / (n + z²) · sqrt(x (n - x) / n + z²/4)
L4  U ← c + h                          ▷ U = 1 exactly when x = n
L5  L ← (x² / n) / ((n + z²) · U)      ▷ product of the roots over U
L6  return [L, U]
```

Line L1 uses `statistics.NormalDist().inv_cdf`. Line L5 uses Vieta's formula: the two roots of $(n + z^2) p^2 - (2x + z^2) p + x^2/n$ have the product $(x^2/n)/(n + z^2)$. The direct form $c - h$ subtracts two close numbers when $x$ is small. The loss is only a few digits at the usual levels, but at $x = 0$ the direct form gave a nonzero lower end, about $10^{-19}$, for 545 of the values $n = 1, \ldots, 1999$ at $\alpha = 0.05$, and a negative one for some $n$ at $\alpha = 0.32$. Line L5 gives $L = 0$ exactly at $x = 0$.

## Example

Take $n = 10$, $x = 3$ and $\alpha = 0.05$, so $z^2 = 3.8415$.

- Line L2: $c = (3 + 1.9207)/13.8415 = 0.35551$.
- Line L3: $h = (1.95996/13.8415) \sqrt{2.1 + 0.96037} = 0.14160 \times 1.74939 = 0.24771$.
- Line L4: $U = 0.60322$.
- Line L5: $L = 0.9/(13.8415 \times 0.60322) = 0.10779$.

So the 95% Wilson interval is $[0.1078, 0.6032]$, against $[0.0667, 0.6525]$ for [Clopper-Pearson](/clopper-pearson-interval/) and $[0.0160, 0.5840]$ for the Wald interval $\hat p \pm z \sqrt{\hat p (1 - \hat p)/n}$. At each end the score statistic is $\pm z$: for example at $p = 0.60322$, $(3 - 6.0322)/\sqrt{10 \times 0.60322 \times 0.39678} = -1.95996$.

At $x = 0$, $L = 0$ and $U = z^2/(n + z^2) = 0.2775$ for $n = 10$. At $x = n$, $U = 1$ and $L = n/(n + z^2) = 0.7225$.

**Measured coverage.** The coverage at a fixed $p$ is the finite sum $C(p) = \sum_{x : L(x) \le p \le U(x)} \binom{n}{x} p^x (1-p)^{n-x}$, computed exactly, with no simulation. On the grid $p = 0.001, \ldots, 0.999$ at $\alpha = 0.05$:

| $n$ | smallest coverage on the grid (at $p$) | mean coverage | share of the grid below 0.95 |
|---|---|---|---|
| 10 | 0.8424 (0.017) | 0.9542 | 44% |
| 20 | 0.8516 (0.008) | 0.9532 | 40% |
| 50 | 0.8605 (0.003) | 0.9517 | 40% |

The mean is close to 0.95, but the coverage falls below 0.95 for a large share of $p$ and has deep dips near the ends. A grid misses the exact worst point, which the theorem below locates.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Expanding $(x - np)^2 \le z^2 np(1 - p)$ gives a convex quadratic in $p$ whose discriminant is $4z^2(x(n - x)/n + z^2/4) > 0$, so the acceptance set is the interval between its roots $c \mp h$. The quadratic is non-negative at $p = 0$ and $p = 1$, so both roots lie in $[0, 1]$, and it is non-positive at $x/n$, so the interval contains $\hat p$.

**What is proved about coverage.** For fixed $p \in (0, 1)$, the coverage is $P(\lvert Z_n \rvert \le z)$ for the standardized count $Z_n$, which tends to $1 - \alpha$. Near the ends this fails for every $n$: let $\lambda^*$ be the smaller root of $\lambda^2 - (2 + z^2)\lambda + 1 = 0$, which is $0.176525$ at $\alpha = 0.05$. For $0 < p < \lambda^*/n$, only $x = 0$ gives an interval that contains $p$, so the coverage is exactly $(1 - p)^n$, and it approaches $(1 - \lambda^*/n)^n < e^{-\lambda^*} = 0.8382$ as $p$ rises to $\lambda^*/n$. For $n = 10$ this is $0.8369$, slightly below the grid minimum in the table. The proof holds for $\alpha \le 0.38$.

**What is only measured.** The mean coverage near $1 - \alpha$ and the share of $p$ below $1 - \alpha$ come from the exact sums in the table, not from a theorem. Contrast the [Clopper-Pearson interval](/clopper-pearson-interval/), whose coverage of at least $1 - \alpha$ at every $p$ is proved.

## Complexity

The interval costs a fixed number of arithmetic operations, one square root and one normal quantile: $\Theta(1)$ time and space, independent of $n$. Clopper-Pearson, by contrast, needs a root search over binomial tails or Beta quantiles.

## Properties

- **Inside $[0, 1]$.** Both ends lie in $[0, 1]$ for every $x$, with no truncation needed.
- **Never degenerate.** The length is positive for every $x$, including $x = 0$ and $x = n$.
- **Shrunk center.** The center $c = \frac{n}{n + z^2}\hat p + \frac{z^2}{n + z^2} \cdot \frac{1}{2}$ is a weighted mean of $\hat p$ and $1/2$. For 95% it is close to adding two successes and two failures.
- **Symmetry.** $L(x) = 1 - U(n - x)$.
- **Monotone in $x$.** Both ends increase with $x$.
- **Not equal-tailed.** The two miss probabilities can be very unequal near the ends; see Pitfalls.
- **Shorter than Clopper-Pearson.** In the examples above it is contained in the Clopper-Pearson interval, and its mean coverage is closer to $1 - \alpha$.

## Variants and improvements

- **Continuity correction.** Replace $\lvert x - np \rvert$ by $\lvert x - np \rvert - 1/2$ in the inequality. The coverage rises toward that of Clopper-Pearson and the interval gets wider.
- **Agresti-Coull interval.** Use $\tilde n = n + z^2$ and $\tilde p = (x + z^2/2)/\tilde n$, the Wilson center, with the simple width $z \sqrt{\tilde p (1 - \tilde p)/\tilde n}$. It contains the Wilson interval and is easy to compute by hand; for 95% it is the "add two successes and two failures" rule.
- **Jeffreys interval.** The equal-tailed interval of the $\text{Beta}(x + 1/2, n - x + 1/2)$ posterior, with the frequentist coverage studied by Brown, Cai and DasGupta. It is recommended with Wilson for small $n$.
- **Modified ends.** Brown, Cai and DasGupta (2001) suggest replacing the Wilson lower end for the smallest positive $x$ (up to 2 or 3, depending on $n$) by a one-sided Poisson-based bound, which removes the deepest dips near $p = 0$; the upper end changes in the same way by symmetry.
- **Wald interval.** $\hat p \pm z \sqrt{\hat p(1 - \hat p)/n}$ inverts the [Wald test](/wald-test/) instead of the score test. Its coverage is erratic even for large $n$, and it collapses to a point at $x = 0$ and $x = n$. Avoid it.
- **Two samples and other models.** The same inversion of the score test gives intervals for a difference of proportions and for a Poisson rate.

## When to use it

Use it as the default interval for one proportion when an average coverage close to $1 - \alpha$ and a short interval matter more than a guarantee at every $p$, and for any $n$, including small $n$. Use [Clopper-Pearson](/clopper-pearson-interval/) when a guarantee at every $p$ is required. If $p$ may be very close to 0 or 1 and the lower end matters, use the modified ends or an exact interval.

## Pitfalls

- **Average is not a guarantee.** "Coverage about 95%" is an average over $p$. At $p$ just below $0.1765/n$ the 95% interval covers $p$ with probability below $0.84$, for every $n$.
- **Uneven tails.** Near $p = 0$ almost all misses come from the interval lying above $p$. Do not use one end of a two-sided Wilson interval as a one-sided bound at level $1 - \alpha/2$ without checking.
- **The direct lower root.** $c - h$ loses digits for small $x$ and can be slightly negative or nonzero at $x = 0$. Use line L5.
- **Wrong variance.** The score test uses the variance $p_0(1 - p_0)/n$ at the candidate $p_0$, not at $\hat p$. Using $\hat p$ gives the Wald interval.
- **Dependence and overdispersion.** As for every binomial method, clustered trials make the true variance larger, and the coverage falls.

## Implementations

## History

Edwin B. Wilson (1927) observed that the usual interval $\hat p \pm z \sqrt{\hat p(1 - \hat p)/n}$ treats the estimate as if it were the true value in the variance, and solved $\lvert x - np \rvert = z \sqrt{np(1 - p)}$ for $p$ instead. The interval was little used for decades. Agresti and Coull (1998) showed by exact coverage computations that it beats both the Wald and the Clopper-Pearson intervals as a practical choice, and Brown, Cai and DasGupta (2001) showed that the Wald interval's coverage oscillates even for large $n$ and recommended Wilson or Jeffreys for small $n$.

## References
