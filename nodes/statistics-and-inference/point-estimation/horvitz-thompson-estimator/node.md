---
tag: D95ZRB
kind: algorithm
slug: horvitz-thompson-estimator
name: Horvitz-Thompson estimator
aliases:
- HT estimator
- pi-estimator
area: statistics-and-inference/point-estimation
level: core
summary: Estimates a population total by summing each sampled value divided by its inclusion probability. It is unbiased for any design in which every unit can be sampled.
model: real-ram
complexity:
  vars: {n: "the number of distinct units in the sample"}
  time: {worst: Θ(n²), best: Θ(n²)}
  space: {extra: Θ(1)}
properties: {deterministic: true, unbiased: true, linear_in_y: true, design_based: true, needs_pairwise_probabilities: true}
history:
  year: 1952
  people: [Daniel G. Horvitz, Donovan J. Thompson]
  note: Horvitz and Thompson gave the estimator, its variance and an unbiased variance estimator for sampling without replacement with unequal probabilities in JASA in 1952. Sen and, independently, Yates and Grundy gave the variance form for fixed-size designs in 1953.
prereqs: [estimator-bias, indicator-random-variable, random-sampling]
see_also: [probability-proportional-to-size-sampling, stratified-sampling, bernoulli-sampling, importance-sampling, inverse-probability-weighting, off-policy-evaluation, priority-sampling, standard-error]
sources:
  - paper: doi:10.1080/01621459.1952.10483446
    title: D. G. Horvitz and D. J. Thompson, A generalization of sampling without replacement from a finite universe, Journal of the American Statistical Association 47(260), 1952
    locator: pp. 663 to 685 (the estimator of the total, its variance with the pairwise inclusion probabilities, and an unbiased estimate of that variance)
  - paper: "A. R. Sen, On the estimate of the variance in sampling with varying probabilities, Journal of the Indian Society of Agricultural Statistics 5, 1953, pp. 119 to 127"
    title: On the estimate of the variance in sampling with varying probabilities
    locator: the whole paper (the variance estimator for fixed-size designs)
  - paper: doi:10.1111/j.2517-6161.1953.tb00140.x
    title: F. Yates and P. M. Grundy, Selection without replacement from within strata with probability proportional to size, Journal of the Royal Statistical Society Series B 15(2), 1953
    locator: pp. 253 to 261 (the variance in the form of squared differences and its estimate)
  - book: isbn:9780471162407
    title: William G. Cochran, Sampling Techniques, third edition, Wiley, 1977
    locator: Section 9A.7, pp. 259 to 261 (the Horvitz-Thompson estimator and the Yates-Grundy variance estimate)
  - paper: "D. Basu, An essay on the logical foundations of survey sampling, part one, in V. P. Godambe and D. A. Sprott (eds.), Foundations of Statistical Inference, Holt, Rinehart and Winston, Toronto, 1971, pp. 203 to 242"
    title: An essay on the logical foundations of survey sampling, part one
    locator: the circus example (an unbiased estimate that is absurd for every sample)
---

The Horvitz-Thompson estimator estimates the total $Y = \sum_{i=1}^N y_i$ of a finite population from a random sample $S$ by $\hat Y = \sum_{i \in S} y_i/\pi_i$, where $\pi_i$ is the probability that unit $i$ is in the sample. It works for every sampling design, with or without equal probabilities, and is unbiased whenever every unit has $\pi_i > 0$. Its variance depends on the pairwise inclusion probabilities $\pi_{ij}$, and with all $\pi_{ij} > 0$ the sample gives an unbiased estimate of that variance. The weight $1/\pi_i$ is the same weight as in [importance sampling](/importance-sampling/) and [inverse probability weighting](/inverse-probability-weighting/). Designs that choose the $\pi_i$ on purpose, such as [PPS sampling](/probability-proportional-to-size-sampling/), use this estimator to undo their unequal chances.

## In plain words

A sampling plan gives some units a high chance of being picked and others a low one. If a unit had a one in ten chance, then on average it shows up in one sample out of ten, so when it does show up, it stands in for ten copies of itself. The estimate of the total adds up every sampled value multiplied by one over its chance.

Averaged over all the samples the plan can draw, every unit is counted exactly once, so the estimate is right on average. How much it varies depends on how often pairs of units appear together, so the error estimate needs the chance of each pair as well. If some unit can never be picked, nothing can stand in for it, and the estimate misses its value.

## The problem

A population has $N$ units, labelled $1, \ldots, N$, with fixed unknown values $y_1, \ldots, y_N$. A *sampling design* is a probability distribution $p$ on the subsets of $\{1, \ldots, N\}$, chosen by the statistician and known. One subset $S$ is drawn from $p$, and $y_i$ is observed for $i \in S$. The randomness is in $S$ only; the $y_i$ are constants. This is design-based inference.

The *inclusion probabilities* are

$$\pi_i = \Pr[i \in S] = \sum_{s \ni i} p(s), \qquad \pi_{ij} = \Pr[i \in S \text{ and } j \in S] = \sum_{s \ni i, j} p(s),$$

with $\pi_{ii} = \pi_i$. The design has *fixed size* $n$ if every subset with $p(s) > 0$ has $n$ units. The task is to estimate $Y$, to estimate the variance of that estimate, and to compute both from $S$, the observed $y_i$ and the $\pi_i$ and $\pi_{ij}$ of the sampled units.

## The algorithm

```pseudo id=main
HT-ESTIMATE(S, y, π)                         ▷ every i ∈ S has π_i > 0
L1  T ← 0
L2  for each i ∈ S do
L3      T ← T + y_i / π_i                    ▷ unit i stands for 1/π_i units
L4  return T

HT-VARIANCE(S, y, π, π2)                     ▷ needs π_ij > 0 for i, j ∈ S
L5  v ← 0
L6  for each i ∈ S do
L7      v ← v + (1 − π_i) · (y_i / π_i)²
L8      for each j ∈ S with j ≠ i do
L9          v ← v + (1 − π_i π_j / π_ij) · (y_i / π_i) · (y_j / π_j)
L10 return v

SYG-VARIANCE(S, y, π, π2)                    ▷ fixed-size designs only
L11 v ← 0
L12 for each pair i < j in S do
L13     v ← v + (π_i π_j / π_ij − 1) · (y_i / π_i − y_j / π_j)²
L14 return v
```

Lines L1 to L4 compute the estimate $\hat Y$. Lines L5 to L10 compute the Horvitz-Thompson variance estimate

$$v_{\mathrm{HT}} = \sum_{i \in S} (1 - \pi_i)\frac{y_i^2}{\pi_i^2} + \sum_{i \in S}\sum_{j \in S, j \ne i} \frac{\pi_{ij} - \pi_i\pi_j}{\pi_{ij}}\,\frac{y_i}{\pi_i}\frac{y_j}{\pi_j},$$

and lines L11 to L14 compute the Sen-Yates-Grundy estimate

$$v_{\mathrm{SYG}} = \sum_{i < j,\ i, j \in S} \frac{\pi_i\pi_j - \pi_{ij}}{\pi_{ij}}\left(\frac{y_i}{\pi_i} - \frac{y_j}{\pi_j}\right)^2.$$

Both estimate the same variance $\operatorname{Var}[\hat Y]$. The first works for every design with $\pi_{ij} > 0$; the second needs a fixed sample size, and then it is usually the better one, because it is zero when $y_i/\pi_i$ is the same for all sampled units, and nonnegative whenever $\pi_{ij} \le \pi_i \pi_j$ for all pairs. The [standard error](/standard-error/) is the square root of the estimate.

The algorithm does not draw the sample. Drawing is the job of the design: [simple random sampling](/random-sampling/), [Bernoulli sampling](/bernoulli-sampling/), [stratified sampling](/stratified-sampling/), [PPS sampling](/probability-proportional-to-size-sampling/), or any other plan whose $\pi_i$ and $\pi_{ij}$ can be computed.

## Example

The population has $N = 4$ units with $y = (2, 3, 6, 10)$, so $Y = 21$. The design draws one of six pairs with these probabilities.

| sample $S$ | $\{1,2\}$ | $\{1,3\}$ | $\{1,4\}$ | $\{2,3\}$ | $\{2,4\}$ | $\{3,4\}$ |
|---|---|---|---|---|---|---|
| $p(S)$ | 0.1 | 0.1 | 0.2 | 0.1 | 0.2 | 0.3 |

Summing the rows gives $\pi = (0.4, 0.4, 0.5, 0.7)$, which add up to $n = 2$, and each $\pi_{ij}$ is the probability of the pair $\{i, j\}$ itself. For the sample $\{1, 4\}$, line L3 adds $2/0.4 = 5$ and $10/0.7 = 100/7$, so $\hat Y = 135/7 \approx 19.29$. All six samples, in exact arithmetic:

| $S$ | $\hat Y$ | $v_{\mathrm{HT}}$ | $v_{\mathrm{SYG}}$ |
|---|---|---|---|
| $\{1,2\}$ | $12.5$ | $3.75$ | $3.75$ |
| $\{1,3\}$ | $17$ | $-33$ | $49$ |
| $\{1,4\}$ | $135/7 \approx 19.29$ | $935/49 \approx 19.08$ | $1690/49 \approx 34.49$ |
| $\{2,3\}$ | $19.5$ | $-74.25$ | $20.25$ |
| $\{2,4\}$ | $305/14 \approx 21.79$ | $1815/196 \approx 9.26$ | $1805/98 \approx 18.42$ |
| $\{3,4\}$ | $184/7 \approx 26.29$ | $3728/49 \approx 76.08$ | $128/147 \approx 0.87$ |

Weighting by $p(S)$, the mean of $\hat Y$ is exactly $21 = Y$, and its variance is $127/7 \approx 18.14$. The mean of $v_{\mathrm{HT}}$ and the mean of $v_{\mathrm{SYG}}$ are both exactly $127/7$, so both are unbiased, but $v_{\mathrm{HT}}$ is negative on two of the six samples. Here $\pi_i\pi_j \ge \pi_{ij}$ for every pair, so $v_{\mathrm{SYG}}$ is never negative. For comparison, simple random sampling of 2 of the 4 units, with $\hat Y = 2(y_i + y_j)$, has variance $155/3 \approx 51.67$.

## Correctness

Write $I_i$ for the [indicator](/indicator-random-variable/) of $i \in S$, so that $\hat Y = \sum_{i=1}^N I_i\,y_i/\pi_i$ with $\mathbb{E}[I_i] = \pi_i$ and $\mathbb{E}[I_iI_j] = \pi_{ij}$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[\hat Y] = \sum_i y_i = Y$. The covariance of $I_i$ and $I_j$ is $\pi_{ij} - \pi_i\pi_j$, which gives

$$\operatorname{Var}[\hat Y] = \sum_{i=1}^N\sum_{j=1}^N (\pi_{ij} - \pi_i\pi_j)\frac{y_i}{\pi_i}\frac{y_j}{\pi_j}.$$

Each term of $v_{\mathrm{HT}}$ is a term of this sum divided by the probability $\pi_{ij}$ that the sample contains it, so $v_{\mathrm{HT}}$ is unbiased. For a fixed-size design, $\sum_j (\pi_{ij} - \pi_i\pi_j) = 0$ for each $i$, which turns the sum into $\sum_{i<j}(\pi_i\pi_j - \pi_{ij})(y_i/\pi_i - y_j/\pi_j)^2$, and the same argument shows that $v_{\mathrm{SYG}}$ is unbiased. The full proofs are below. They are exact statements about expectations over the design; the normal interval in the variants is an approximation.

## Complexity

Lines L1 to L4 do one division and one addition per sampled unit: $2n$ operations, $\Theta(n)$ time. Lines L5 to L10 visit all ordered pairs of sampled units, and lines L11 to L14 all unordered pairs, so both take $\Theta(n^2)$ time if each $\pi_{ij}$ can be looked up or computed in $O(1)$. The extra space is $\Theta(1)$ besides the inputs. The time in the front matter is for the estimate and one variance estimate together; the estimate alone is a single pass and can run on a stream.

Computing the $\pi_i$ and $\pi_{ij}$ is the design's cost, not the estimator's. For simple random sampling of $n$ from $N$ they are the closed forms $n/N$ and $n(n-1)/(N(N-1))$. For [Bernoulli sampling](/bernoulli-sampling/) with unequal probabilities, $\pi_{ij} = \pi_i\pi_j$. For a design given as a list of samples and probabilities, as in the example, summing over the list costs $\Theta(n)$ per sample.

## Properties

- **Unbiased for every design.** The only condition is $\pi_i > 0$ for every unit with $y_i \ne 0$. It does not need the design to be simple, stratified or of fixed size.
- **Linear in $y$.** The estimate of $Y + Y'$ is the sum of the estimates, so the estimate of a domain total is the estimate with $y_i$ set to 0 outside the domain, and stratified estimates add over strata.
- **Exact recovery.** If $y_i = c\,\pi_i$ for all $i$ in a fixed-size design, then $\hat Y = cn = Y$ for every sample and the variance is zero. The closer $\pi_i$ is to proportional to $y_i$, the smaller the variance; this is the reason for [PPS sampling](/probability-proportional-to-size-sampling/).
- **Simple random sampling.** With $\pi_i = n/N$, $\hat Y = N\bar y_S$, and both variance estimates reduce to $N^2(1 - f)s^2/n$ with $f = n/N$ and $s^2$ the [sample variance](/sample-variance/) of the sampled values with divisor $n - 1$.
- **Not equivariant to a shift.** Adding a constant $c$ to every $y_i$ adds $c\sum_{i \in S}1/\pi_i$ to $\hat Y$, not $cN$, unless $\sum_{i \in S}1/\pi_i = N$ for every sample.

## Variants and improvements

- **Mean and proportion.** $\hat Y / N$ estimates the mean, with variance estimate $v/N^2$. For a 0-1 variable it estimates a proportion, and it can exceed 1; see the pitfalls.
- **Hájek ratio.** $\hat{\bar y}_{\mathrm{H}} = \sum_{i \in S} (y_i/\pi_i) \big/ \sum_{i \in S} (1/\pi_i)$ divides by the estimate $\hat N$ of $N$ instead of $N$. It is a ratio of two unbiased estimates, so it is biased: in the example its mean is $2159/396 \approx 5.452$ against the true mean $5.25$. It stays between the smallest and largest sampled values, is equivariant to a shift, and often has a much smaller variance when the sample size is random. It is the self-normalized form of [importance sampling](/importance-sampling/) and the usual form of [inverse probability weighting](/inverse-probability-weighting/).
- **Poisson sampling.** With independent inclusions, $\pi_{ij} = \pi_i\pi_j$ for $i \ne j$, so all cross terms vanish: $\operatorname{Var}[\hat Y] = \sum_i (1 - \pi_i)y_i^2/\pi_i$ and $v_{\mathrm{HT}} = \sum_{i \in S}(1 - \pi_i)y_i^2/\pi_i^2$. The sample size is random, so $v_{\mathrm{SYG}}$ does not apply.
- **A normal interval.** For large samples from designs where a central limit theorem holds, $\hat Y \pm z_{1-\alpha/2}\sqrt{v}$ is an approximate $1 - \alpha$ [confidence interval](/confidence-interval/). Its coverage is measured, not proved, for any given design and sample size.
- **Generalized regression.** Using an auxiliary variable known for all units, the regression and calibration estimators adjust the weights $1/\pi_i$ so that the weighted sample reproduces the known auxiliary totals.
- **Streams and sketches.** [Priority sampling](/priority-sampling/) keeps a weighted sample of a stream with a threshold, and the Horvitz-Thompson idea with that threshold gives unbiased estimates of subset sums.
- **Off-policy evaluation.** Weighting each logged reward by one over the probability that the logging policy took the action is the same estimator in [off-policy evaluation](/off-policy-evaluation/).

## When to use it

Use it whenever the sample was drawn by a known probability design with unequal inclusion probabilities, and an estimate of a total, mean or proportion is needed that is unbiased by construction, without a model for $y$. Under simple random sampling it is the ordinary expansion estimate $N\bar y_S$. When $y$ is not related to the $\pi_i$, or the sample size is random, the Hájek ratio or a regression estimator is usually more accurate. When the probabilities are estimated, as with propensity scores in observational data, the unbiasedness no longer holds exactly; see [inverse probability weighting](/inverse-probability-weighting/).

## Pitfalls

- **Units with $\pi_i = 0$.** A unit that can never be sampled is missing from every estimate, and $\mathbb{E}[\hat Y] = Y - \sum_{\pi_i = 0} y_i$. No weighting can repair a frame that leaves units out.
- **Pairs with $\pi_{ij} = 0$.** In systematic sampling, many pairs never occur together. Then neither $v_{\mathrm{HT}}$ nor $v_{\mathrm{SYG}}$ can be computed, and dropping the missing terms gives a biased estimate of the variance.
- **Negative variance estimates.** $v_{\mathrm{HT}}$ can be negative, as for the samples $\{1, 3\}$ and $\{2, 3\}$ of the example. $v_{\mathrm{SYG}}$ is nonnegative only when $\pi_{ij} \le \pi_i\pi_j$ for every pair. Report and handle a negative value; do not take its square root.
- **The proportion can exceed 1.** With the example design and $y = (1, 1, 0, 1)$, the true proportion is $3/4$, but the sample $\{1, 2\}$ gives $(1/0.4 + 1/0.4)/4 = 1.25$. The Hájek ratio gives 1 on the same sample.
- **The wrong probabilities.** The $\pi_i$ must be those of the design actually used. Successive draws proportional to size, for instance, do not give $\pi_i$ proportional to size; the [PPS page](/probability-proportional-to-size-sampling/) shows the bias that follows.
- **With-replacement formulas.** In $m$ independent draws with probabilities $p_i$, the Hansen-Hurwitz estimator divides each draw by $m p_i$. The Horvitz-Thompson estimator applies to the set of distinct units, with $\pi_i = 1 - (1 - p_i)^m$. Mixing the two, by using $m p_i$ as $\pi_i$ for the distinct units or by counting a unit once per draw with weight $1/\pi_i$, gives a biased estimate.
- **Unbiased but absurd.** Basu (1971) told of a circus owner who wanted the total weight of 50 elephants from one weighing. A design that picks the average elephant with probability $99/100$ and each of the other 49 with probability $1/4900$ makes $\hat Y$ about $1.01$ times the average weight when the average elephant is picked, and 4900 times an elephant's weight otherwise. The estimate is unbiased and useless for every sample: unbiasedness is a property of the average over samples, and says nothing about the sample at hand.
- **The divisor.** The $s^2$ in the simple random sampling formula uses $n - 1$, and the population $S^2$ in $\operatorname{Var}[\hat Y] = N^2(1 - f)S^2/n$ uses $N - 1$. Say which one is meant.

## Implementations

## History

Horvitz and Thompson (1952) generalized sampling without replacement to unequal probabilities and gave the estimator $\sum_{i \in S} y_i/\pi_i$, its variance in terms of the $\pi_{ij}$, and an unbiased estimate of the variance. Sen (1953) and, independently, Yates and Grundy (1953) gave the variance for fixed-size designs as a sum over pairs of squared differences, with the estimate $v_{\mathrm{SYG}}$. Basu's 1971 essay on the foundations of survey sampling used the circus example to argue that design unbiasedness alone does not make an estimate sensible. Cochran's textbook treats the estimator in Section 9A.7.

## References
