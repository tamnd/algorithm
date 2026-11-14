---
tag: X4CPDK
kind: algorithm
slug: clopper-pearson-interval
name: Clopper-Pearson interval
aliases:
- exact binomial confidence interval
area: statistics-and-inference/hypothesis-testing
level: core
summary: A confidence interval for a binomial p that inverts two one-sided exact tests. Its endpoints are Beta quantiles, and its coverage is at least 1 - alpha for every p.
model: real-ram
complexity:
  vars: {n: the number of trials, b: the number of bisection steps (about 60 in double precision)}
  time: {worst: Θ(n b), best: Θ(b)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1934
  people: [C. J. Clopper, Egon S. Pearson]
  note: Clopper and Pearson gave the interval and its charts in Biometrika in 1934, as an application of Neyman's new theory of confidence intervals.
prereqs: [binomial-test, confidence-interval, binomial-distribution]
see_also: [wilson-score-interval, test-interval-duality, pivotal-quantity, bisection-method, binomial-tail-bounds, credible-interval, t-confidence-interval, fisher-exact-test]
sources:
  - paper: doi:10.1093/biomet/26.4.404
    title: C. J. Clopper and E. S. Pearson, The use of confidence or fiducial limits illustrated in the case of the binomial, Biometrika 26(4), 1934
    locator: pp. 404 to 413
  - paper: doi:10.1214/ss/1009213286
    title: Lawrence D. Brown, T. Tony Cai and Anirban DasGupta, Interval estimation for a binomial proportion, Statistical Science 16(2), 2001
    locator: pp. 101 to 133 (the exact coverage of the Wald, Wilson, Agresti-Coull, Jeffreys and Clopper-Pearson intervals)
  - paper: doi:10.2307/2685469
    title: Alan Agresti and Brent A. Coull, Approximate is better than "exact" for interval estimation of binomial proportions, The American Statistician 52(2), 1998
    locator: pp. 119 to 126
  - book: isbn:9780470463635
    title: Alan Agresti, Categorical Data Analysis, third edition, Wiley, 2013
    locator: Section 1.4 (inference for binomial parameters) and Chapter 16 (small-sample exact inference and its conservatism)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 9.2 (methods of finding interval estimators, inverting a test and pivoting the CDF for discrete families)
---

The Clopper-Pearson interval is a confidence interval for the success probability $p$ of a [binomial distribution](/binomial-distribution/). From $x$ successes in $n$ trials, its lower end $L$ is the value of $p$ at which $x$ or more successes have probability $\alpha/2$, and its upper end $U$ is the value at which $x$ or fewer have probability $\alpha/2$. It is the set of $p_0$ that two one-sided exact [binomial tests](/binomial-test/) at level $\alpha/2$ do not reject. Its coverage is at least $1 - \alpha$ for every $p$ and every $n$, which is why it is often called "exact", but the coverage is usually well above $1 - \alpha$, so the interval is conservative and wider than it needs to be on average.

## In plain words

You saw 3 successes in 10 tries and want a range of plausible success rates. Try a candidate rate. If 3 or more successes would be very rare at that rate, the rate is too low. If 3 or fewer would be very rare, it is too high. "Very rare" means a chance of at most 2.5% on that side. The rates that pass both checks form the interval, here from about 0.067 to 0.652.

The interval never promises less than it says. Over many repeats, a 95% interval covers the true rate at least 95% of the time, whatever the true rate is. The price is that it often covers more than 95% of the time, so it is wider than the intervals that only promise 95% on average.

## The problem

**Input.** A count $x \in \{0, \ldots, n\}$ from $X \sim \text{Binomial}(n, p)$ with $n \ge 1$ fixed, and a level $\alpha \in (0, 1)$.

**Output.** An interval $[L(x), U(x)] \subseteq [0, 1]$.

**Coverage.** Conservative: $P_p(L(X) \le p \le U(X)) \ge 1 - \alpha$ for every $p \in [0, 1]$. The coverage is marginal over $X$ at a fixed $p$; nothing is conditioned on.

**Construction.** Inversion of a test, by [test-interval duality](/test-interval-duality/). Write $G_p(x) = P_p(X \ge x)$ and $F_p(x) = P_p(X \le x)$. The ends solve

$$G_{L}(x) = \frac{\alpha}{2} \;\; (x \ge 1), \qquad F_{U}(x) = \frac{\alpha}{2} \;\; (x \le n - 1),$$

with $L(0) = 0$ and $U(n) = 1$. The identity $G_p(x) = I_p(x, n - x + 1)$, where $I$ is the regularized incomplete beta function, turns these into Beta quantiles:

$$L(x) = B^{-1}\big(\tfrac{\alpha}{2};\, x,\, n - x + 1\big), \qquad U(x) = B^{-1}\big(1 - \tfrac{\alpha}{2};\, x + 1,\, n - x\big).$$

At the ends there are closed forms: $U(0) = 1 - (\alpha/2)^{1/n}$ and $L(n) = (\alpha/2)^{1/n}$.

## The algorithm

```pseudo id=main
CLOPPER-PEARSON(x, n, α)
L1  if x = 0 then L ← 0
L2  else L ← the root p in (0, 1) of P_p(X ≥ x) = α/2      ▷ bisection
L3  if x = n then U ← 1
L4  else U ← the root p in (0, 1) of P_p(X ≤ x) = α/2      ▷ bisection
L5  return [L, U]
```

Each root is found by [bisection](/bisection-method/) on $[0, 1]$. The function $p \mapsto P_p(X \ge x)$ is continuous and strictly increasing for $x \ge 1$, so a bracket that starts as $[0, 1]$ always holds the root. The code halves the bracket until its midpoint equals one of its ends, which happens when the ends are adjacent floating point numbers. Each step sums one binomial tail in log space with `lgamma`, as in the [binomial test](/binomial-test/). The lower tail $P_p(X \le x)$ is computed as the upper tail $P_{1-p}(n - X \ge n - x)$ of the failures, so neither tail is found by subtraction from 1.

A library with a Beta quantile function can return the two Beta quantiles directly. The code of this page does not use one, since the standard library has none, but its tests check the identity with the incomplete beta function of the group helper.

## Example

Take $n = 10$, $x = 3$ and $\alpha = 0.05$. Line L2 solves $P_p(X \ge 3) = 0.025$. The first steps of the bisection are:

| step | midpoint $p$ | $P_p(X \ge 3)$ | the root is |
|---|---|---|---|
| 1 | 0.5 | 0.94531 | below |
| 2 | 0.25 | 0.47441 | below |
| 3 | 0.125 | 0.11950 | below |
| 4 | 0.0625 | 0.02101 | above |
| 5 | 0.09375 | 0.05984 | below |
| 6 | 0.078125 | 0.03770 | below |
| 7 | 0.0703125 | 0.02867 | below |
| 8 | 0.06640625 | 0.02467 | above |

The bisection ends at $L = 0.0667395$. Line L4 gives $U = 0.6524529$, where $P_U(X \le 3) = 0.025$. So the 95% interval is $[0.0667, 0.6525]$.

Other cases, at $\alpha = 0.05$:

| $x$, $n$ | Clopper-Pearson | Wilson | Wald $\hat p \pm z \sqrt{\hat p(1 - \hat p)/n}$ |
|---|---|---|---|
| 3, 10 | [0.0667, 0.6525] | [0.1078, 0.6032] | [0.0160, 0.5840] |
| 0, 10 | [0, 0.3085] | [0, 0.2775] | [0, 0] |
| 10, 10 | [0.6915, 1] | [0.7225, 1] | [1, 1] |
| 7, 20 | [0.1539, 0.5922] | [0.1812, 0.5671] | [0.1410, 0.5590] |

For $x = 0$ and $n = 10$, the closed form gives $U = 1 - 0.025^{1/10} = 0.3085$.

**Exact coverage.** The coverage at a fixed $p$ is $C(p) = \sum_{x : L(x) \le p \le U(x)} \binom{n}{x} p^x (1-p)^{n-x}$, a finite sum, so it can be computed exactly with no simulation. On the grid $p = 0.001, 0.002, \ldots, 0.999$ at $\alpha = 0.05$:

| $n$ | Clopper-Pearson: minimum, mean | Wilson: minimum, mean, share of grid below 0.95 | Wald: minimum, mean |
|---|---|---|---|
| 10 | 0.9611, 0.9838 | 0.8424, 0.9542, 44% | 0.0100, 0.7699 |
| 20 | 0.9581, 0.9770 | 0.8516, 0.9532, 40% | 0.0198, 0.8467 |
| 50 | 0.9527, 0.9693 | 0.8605, 0.9517, 40% | 0.0488, 0.9015 |

Clopper-Pearson never falls below 0.95, as the theorem says, and its mean coverage is near 0.98 for $n = 10$. The [Wilson interval](/wilson-score-interval/) has mean coverage close to 0.95 but dips to about 0.85 near the ends of $[0, 1]$. The Wald interval collapses to a point at $x = 0$ and $x = n$ and is the worst of the three.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The derivative of $G_p(x)$ in $p$ telescopes to $n \binom{n-1}{x-1} p^{x-1}(1-p)^{n-x} > 0$, which proves the Beta identity and that each end is a unique root. Strict monotonicity gives $L(x) > p$ exactly when $G_p(x) < \alpha/2$. The set of such $x$ is an upper tail of $\{0, \ldots, n\}$, and an upper tail with $G_p < \alpha/2$ at its smallest point has probability less than $\alpha/2$. The same holds for $U(x) < p$, and the two miss events are disjoint, so the coverage is greater than $1 - \alpha$ at every $p$.

This is a proof for every $n$, not a measurement. In contrast, the coverage of the Wilson interval is only measured, by the exact sums above.

## Complexity

Each tail evaluation costs $\Theta(n)$ operations in the worst case, with `lgamma` and `exp` as unit operations, and the bisection does $b$ steps, about 55 to 70 in double precision, more when an end is very close to 0. So the time is $\Theta(n b)$ and the extra space is $\Theta(1)$. More exactly, the upper tail for $L$ has $n - x + 1$ terms and the tail of the failures for $U$ has $x + 1$ terms. For $x = 0$ or $x = n$ one end is free and the other tail has one term, so the time is $\Theta(b)$. With a Beta quantile routine based on a continued fraction for $I_p$, the cost per evaluation no longer grows linearly in $n$, and Newton steps can replace most bisection steps.

## Properties

- **Conservative.** The coverage is above $1 - \alpha$ at every $p$, and much higher for small $n$. The interval is wider than intervals with coverage near $1 - \alpha$ on average.
- **Equal tails.** Each side misses with probability less than $\alpha/2$. One-sided bounds are the same construction with $\alpha$ in place of $\alpha/2$.
- **Symmetry.** $L(x) = 1 - U(n - x)$, because the roles of successes and failures swap.
- **Monotone in $x$.** Both ends increase strictly with $x$.
- **Never degenerate.** The interval has positive length for every $x$, including $x = 0$ and $x = n$, unlike the Wald interval.
- **Not the shortest.** Among intervals with guaranteed coverage, others are shorter on average; see the variants.

## Variants and improvements

- **One-sided bound and the rule of three.** With $x = 0$, the one-sided upper bound at level $1 - \alpha$ is $1 - \alpha^{1/n}$, about $3/n$ for $\alpha = 0.05$.
- **Mid-p interval.** Replace $P_p(X \ge x)$ by $P_p(X > x) + \frac{1}{2} P_p(X = x)$ and similarly on the other side. The coverage is close to $1 - \alpha$ on average, but it is no longer guaranteed.
- **Shorter intervals with the same guarantee.** Inverting other exact tests gives intervals that are contained in Clopper-Pearson for many $x$: the Sterne interval inverts the minimum-likelihood two-sided test, and Blaker (2000) inverts a test that keeps the result an interval and nested in $\alpha$. Sterne's set can have gaps; see the [binomial test](/binomial-test/).
- **Approximate intervals.** The [Wilson score interval](/wilson-score-interval/), the Agresti-Coull interval and the Jeffreys interval (the equal-tailed interval of the $\text{Beta}(x + 1/2, n - x + 1/2)$ posterior) have mean coverage near $1 - \alpha$ and are shorter. Brown, Cai and DasGupta (2001) recommend Wilson or Jeffreys for small $n$.
- **A Bayesian view.** $L(x)$ and $U(x)$ are quantiles of the posteriors under the improper priors $\text{Beta}(0, 1)$ and $\text{Beta}(1, 0)$. This is a coincidence of formulas; the coverage statement is frequentist and is not a [credible interval](/credible-interval/) statement.

## When to use it

Use it when a guarantee at every $p$ is required, for example in regulation, quality control or safety work, where a reported upper bound on a failure rate must hold. It is also the standard report for $x = 0$ or $x = n$. When the goal is accurate average coverage and shorter intervals, use Wilson or Jeffreys instead. Do not use the Wald interval for small $n$ or for $p$ near 0 or 1.

## Pitfalls

- **"Exact" does not mean coverage equal to $1 - \alpha$.** It means the coverage is computed from the exact binomial law and is at least $1 - \alpha$. The coverage is above $1 - \alpha$ almost everywhere.
- **Swapping the Beta parameters.** The lower end uses $\text{Beta}(x, n - x + 1)$ and the upper end uses $\text{Beta}(x + 1, n - x)$. Using $\text{Beta}(x + 1, n - x + 1)$ for both gives the posterior of a uniform prior, not this interval.
- **Undefined quantiles at the ends.** $\text{Beta}(0, \cdot)$ does not exist, so code must set $L(0) = 0$ and $U(n) = 1$ directly, as lines L1 and L3 do.
- **Using $1 - F$ for a small tail.** For large $n$, compute each tail as a direct sum or with the incomplete beta function, not as 1 minus the other tail.
- **Dependence or overdispersion.** The coverage proof needs $X \sim \text{Binomial}(n, p)$. Clustered data give more spread and lower coverage.

## Implementations

## History

Clopper and Pearson (1934) gave the interval and charts of its ends for several $n$, as one of the first applications of Neyman's theory of confidence intervals, and called the ends confidence or fiducial limits. The Beta form of the ends follows from the identity between binomial tails and the incomplete beta function. Interest returned after Agresti and Coull (1998) and Brown, Cai and DasGupta (2001) showed by exact coverage computations how conservative Clopper-Pearson is and how badly the textbook Wald interval behaves, and both papers recommended approximate intervals for routine use.

## References
