---
tag: G2PZNC
kind: technique
slug: probability-proportional-to-size-sampling
name: Probability proportional to size (PPS) sampling
aliases:
- PPS sampling
- pi-ps sampling
- unequal probability sampling
area: randomized/sampling
level: intro
summary: Select units with probability proportional to a size measure, and estimate totals with the Hansen-Hurwitz or Horvitz-Thompson estimator.
prereqs: [expected-value, variance, indicator-random-variable]
see_also: [weighted-sampling, importance-sampling, systematic-sampling, stratified-sampling, bernoulli-sampling, priority-sampling, weighted-reservoir-sampling, alias-method]
sources:
  - paper: doi:10.1214/aoms/1177731356
    title: Morris H. Hansen and William N. Hurwitz, On the theory of sampling from finite populations, Annals of Mathematical Statistics 14(4), 1943
    locator: pages 333 to 362 (sampling with probability proportional to size, with replacement)
  - paper: doi:10.1080/01621459.1952.10483446
    title: D. G. Horvitz and D. J. Thompson, A generalization of sampling without replacement from a finite universe, Journal of the American Statistical Association 47(260), 1952
    locator: pages 663 to 685 (the estimator with inclusion probabilities and its variance)
  - book: isbn:9780387975283
    title: Carl-Erik Särndal, Bengt Swensson and Jan Wretman, Model Assisted Survey Sampling, Springer, 1992
    locator: Sections 2.8 and 2.9 (the pi estimator and the pwr estimator), Section 3.6 (pi-ps sampling)
  - book: isbn:9780471162407
    title: William G. Cochran, Sampling Techniques, third edition, Wiley, 1977
    locator: Chapter 9A (sampling with unequal probabilities)
  - paper: "W. G. Madow, On the theory of systematic sampling, II, Annals of Mathematical Statistics 20(3), 1949"
    locator: pages 333 to 354
---

Probability proportional to size (PPS) sampling selects units of a finite population with probabilities proportional to a known size measure $x_i > 0$, and then estimates the population total $Y = \sum_i y_i$ of a study variable by weighting each observed $y_i$ by the inverse of its selection probability. With replacement, each of $m$ independent draws picks unit $i$ with probability $p_i = x_i / X$, and the Hansen-Hurwitz estimator $\frac{1}{m}\sum_k y_{i_k}/p_{i_k}$ is unbiased. Without replacement, a design of fixed size $n$ gives unit $i$ the inclusion probability $\pi_i = n x_i / X$, and the Horvitz-Thompson estimator $\sum_{i \in S} y_i / \pi_i$ is unbiased. Systematic PPS reaches these $\pi_i$ exactly with one random start. The gain is large when $y_i$ is roughly proportional to $x_i$: if $y_i = c\,x_i$ exactly, both estimators have zero variance. This page is the survey-sampling view; [weighted sampling](/weighted-sampling/) is the general problem of drawing indices by weight.

## In plain words

You want the total sales of a thousand shops, and you can visit only a few. You know the floor area of every shop, and big shops sell more. Picking shops uniformly often misses the big ones, and the estimate jumps around.

So pick each shop with a chance proportional to its area. Big shops come up more often. To correct for this, divide each observed value by the chance that its shop was picked. A shop that had a 1 in 10 chance stands for 10 shops' worth of sales.

If sales were exactly proportional to area, every sample would give the right total. If they are only roughly proportional, the estimate still has a much smaller spread than uniform sampling gives.

## When it applies

- The population is finite and listed, and a positive size $x_i$ is known for every unit before sampling.
- The target is a total or a mean of $y$, and $y_i$ is roughly proportional to $x_i$.
- The size measure is the same for all study variables, so one design serves a whole survey. A variable that is not related to size can get a worse estimate than from uniform sampling.

## The template

Notation: units $1, \ldots, N$, sizes $x_i > 0$ with $X = \sum x_i$, study values $y_i$ with total $Y$. For the fixed-size design, the inclusion probabilities are written as $\pi_i = a_i / D$ with integers $0 < a_i \le D$ and $\sum a_i = nD$, and $A_i = a_1 + \cdots + a_i$ with $A_0 = 0$.

```pseudo id=main
PPS-WITH-REPLACEMENT(x, y, m)
L1  for k ← 1 to m do  i_k ← an index drawn with Pr[i] = x_i / X
L2  return (1/m) · Σ_k y_{i_k} · X / x_{i_k}        ▷ Hansen-Hurwitz

SYSTEMATIC-PPS(a[1..N], D, n)
L3  t ← a uniform integer in {0, 1, ..., D − 1}
L4  S ← the units i such that some point t + kD, 0 ≤ k < n, lies in [A_{i−1}, A_i)
L5  return S

HORVITZ-THOMPSON(S, y, π)
L6  return Σ_{i ∈ S} y_i / π_i
```

Line L1 is one [weighted draw](/weighted-sampling/), for example a uniform integer in $\{0, \ldots, X - 1\}$ located by [binary search](/binary-search/) in the [prefix sums](/prefix-sums/) of $x$. Line L4 is one pass over the units with a pointer to the next point.

Before L3, set $\pi_i = n x_i / X$. If some $\pi_i > 1$, take those units with certainty ($\pi_i = 1$), and spread the remaining $n$ minus their count over the other units in proportion to size; repeat until no value exceeds 1.

### Example

Five units with sizes $x = (2, 3, 5, 4, 6)$, $X = 20$, values $y = (5, 6, 11, 9, 12)$, $Y = 43$, and $n = 2$. Then $\pi = (0.2, 0.3, 0.5, 0.4, 0.6)$, so $a = (2, 3, 5, 4, 6)$ with $D = 10$, and $A = (2, 5, 10, 14, 20)$.

With start $t = 3$, the points are 3 and 13. Point 3 lies in $[2, 5)$, unit 2; point 13 lies in $[10, 14)$, unit 4. The estimate is $6/0.3 + 9/0.4 = 20 + 22.5 = 42.5$.

| start $t$ | 0, 1 | 2, 3 | 4 | 5 to 9 |
|---|---|---|---|---|
| sample | units 1, 4 | units 2, 4 | units 2, 5 | units 3, 5 |
| estimate | 47.5 | 42.5 | 40 | 42 |

The mean over the ten starts is $43 = Y$, and the variance is $5.5$. Simple random sampling of 2 units with the estimate $\frac{N}{n}\sum_{i \in S} y_i$ is also unbiased, but its variance is $69.75$. Hansen-Hurwitz with $m = 2$ draws has variance $10/2 = 5$.

### Why it is correct

**Lemma 1 (systematic PPS).** Every sample has exactly $n$ distinct units, and unit $i$ is in the sample with probability exactly $a_i / D = \pi_i$.

*Proof.* The intervals $[A_{i-1}, A_i)$ partition $[0, nD)$, and the $n$ points $t + kD$ lie in $[0, nD)$, so each point lies in exactly one interval. Two points are $D$ apart and an interval has length $a_i \le D$, so no interval holds two points: the $n$ points hit $n$ distinct units. The interval of unit $i$ holds $a_i$ consecutive integers, and since $a_i \le D$, they have $a_i$ distinct remainders mod $D$. The interval contains a point $t + kD$ exactly when $t$ is one of these remainders, which happens for $a_i$ of the $D$ equally likely starts. $\blacksquare$

**Theorem 2 (Hansen-Hurwitz).** With $p_i = x_i / X$, the estimate of line L2 is unbiased for $Y$, with variance $\frac{1}{m}\sum_i p_i\,(y_i/p_i - Y)^2$.

*Proof.* One draw $I$ gives $\mathbb{E}[y_I / p_I] = \sum_i p_i\,y_i/p_i = Y$, and its variance is $\sum_i p_i (y_i/p_i - Y)^2$. The $m$ draws are independent, so the average has the same mean and $1/m$ times the variance. $\blacksquare$

This is [importance sampling](/importance-sampling/) on a finite set: the target is the uniform sum, the proposal is $p$, and the weight is $1/p_i$.

**Theorem 3 (Horvitz-Thompson).** For any design in which every unit with $y_i \ne 0$ has $\pi_i = \Pr[i \in S] > 0$, the estimate $\hat Y = \sum_{i \in S} y_i/\pi_i$ is unbiased for $Y$. Its variance is

$$\operatorname{Var}[\hat Y] = \sum_i \sum_j (\pi_{ij} - \pi_i \pi_j)\frac{y_i}{\pi_i}\frac{y_j}{\pi_j},$$

where $\pi_{ij} = \Pr[i \in S \text{ and } j \in S]$ and $\pi_{ii} = \pi_i$.

*Proof.* Let $I_i$ be the [indicator](/indicator-random-variable/) of $i \in S$, so $\mathbb{E}[I_i] = \pi_i$. Then $\hat Y = \sum_{i : \pi_i > 0} I_i\,y_i/\pi_i$, and by [linearity of expectation](/linearity-of-expectation/),

$$\mathbb{E}[\hat Y] = \sum_{i : \pi_i > 0} \pi_i \frac{y_i}{\pi_i} = \sum_{i : \pi_i > 0} y_i = Y,$$

since $y_i = 0$ for every unit with $\pi_i = 0$. For the variance, $\operatorname{Cov}(I_i, I_j) = \pi_{ij} - \pi_i\pi_j$, and $\operatorname{Var}[\sum_i c_i I_i] = \sum_i\sum_j c_i c_j \operatorname{Cov}(I_i, I_j)$ with $c_i = y_i/\pi_i$. $\blacksquare$

The theorem holds for every design: systematic PPS, [Bernoulli sampling](/bernoulli-sampling/) with unequal probabilities (Poisson sampling), stratified designs, and others. Only the $\pi_i$ must be the true inclusion probabilities of the design used.

**Corollary 4 (zero variance).** If $y_i = c\,x_i$ for all $i$, then $y_i/p_i = cX = Y$ for every draw, and for a fixed-size design with $\pi_i = n x_i/X$, $\hat Y = n \cdot cX/n = Y$ for every sample. $\blacksquare$

In the example, $y_i/x_i$ lies between 2 and 2.5, which is why the variance is small.

### Cost

- **Setup.** $\Theta(N)$ to compute $X$, the $\pi_i$ and the prefix sums. The capping of units with $\pi_i > 1$ repeats at most $n$ times.
- **With replacement.** $O(\log N)$ per draw with binary search, or $O(1)$ with the [alias method](/alias-method/).
- **Systematic PPS.** One random integer and one pass of $\Theta(N)$. With $X$ known in advance, the pass can read the units as a stream.
- **Exactness.** With integer sizes and rational $\pi_i$, the integer start of line L3 gives the inclusion probabilities exactly. The common floating-point form, a start $u$ in $[0, 1)$ and points $u, u + 1, \ldots$, compares rounded cumulative sums and is exact only in exact arithmetic.

## Classic examples

- **Establishment and farm surveys.** Size is the number of employees, the turnover or the area from a census or register.
- **Two-stage household surveys.** Select areas with probability proportional to their number of households, then the same number of households in each selected area. Every household then has about the same overall probability, and the field work per area is equal.
- **Auditing.** Monetary unit sampling selects accounts with probability proportional to their recorded amount, so that every currency unit has the same chance.
- **Network and stream measurement.** [Priority sampling](/priority-sampling/) and [weighted reservoir sampling](/weighted-reservoir-sampling/) keep a weighted sample of a stream, and the Horvitz-Thompson idea gives unbiased estimates of subset sums from it.

## Variations

- **Poisson sampling.** Include each unit independently with probability $\pi_i$, as in [Bernoulli sampling](/bernoulli-sampling/). Horvitz-Thompson stays unbiased, but the sample size is random, which adds variance.
- **Sampford's method and conditional Poisson sampling.** Fixed-size designs with the exact $\pi_i$ and $\pi_{ij} > 0$ for all pairs, so that the variance can be estimated without bias.
- **Randomized systematic PPS.** Shuffle the units before the systematic pass, so that $\pi_{ij} > 0$ for most pairs.
- **The Sen-Yates-Grundy form.** For fixed-size designs, $\operatorname{Var}[\hat Y] = \frac{1}{2}\sum_{i \ne j}(\pi_i\pi_j - \pi_{ij})(y_i/\pi_i - y_j/\pi_j)^2$, which shows the zero variance when $y \propto \pi$ directly.
- **Stratified PPS.** Combine with [stratified sampling](/stratified-sampling/); the estimators add over strata.
- **Successive sampling.** Draw one unit at a time with probability proportional to size among those left, as in [Gumbel top-k](/gumbel-max-trick/) or the Efraimidis-Spirakis keys. This is a different design: its inclusion probabilities are not $n x_i / X$. See the pitfalls.

## Pitfalls

- **Wrong inclusion probabilities.** Horvitz-Thompson needs the true $\pi_i$ of the design used. Successive sampling of two units from the example gives $\pi \approx (0.219, 0.318, 0.492, 0.410, 0.561)$, not $(0.2, 0.3, 0.5, 0.4, 0.6)$, and using the second set gives a mean of about $43.10$ instead of $43$.
- **Units with $\pi_i > 1$.** When $n x_i > X$, the unit must be taken with certainty and the rest recomputed. Otherwise systematic PPS can hit the unit twice, and the design is no longer one without replacement.
- **Zero pairwise probabilities.** In systematic PPS, many pairs have $\pi_{ij} = 0$; in the example, units 1 and 2 are never together. No unbiased variance estimate exists then. The order of the list also changes the variance.
- **A size not related to $y$.** If $y$ does not grow with $x$, or a small unit has a large $y$, the weights $1/\pi_i$ make the estimate vary more than uniform sampling would.
- **Size measures that are zero or out of date.** A unit with $x_i = 0$ is never selected and drops out of the estimate. Give such units a small positive size or a separate stratum.

## Exercises

1. Show that the Hansen-Hurwitz variance is zero if and only if $y_i / x_i$ is the same for all units, and compute it for the example with $m = 1$.
2. For systematic PPS on the example, list $\pi_{ij}$ for all pairs and verify that the variance formula of Theorem 3 gives $5.5$.
3. Prove the Sen-Yates-Grundy form of the variance for any fixed-size design.
4. Show that for successive sampling of two units, $\pi_i = p_i + \sum_{j \ne i} p_j\,p_i/(1 - p_j)$, and check it on the example.

## References
