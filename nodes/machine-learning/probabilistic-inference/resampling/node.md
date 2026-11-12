---
tag: DF7EPS
kind: technique
slug: resampling
name: Resampling
aliases:
- multinomial resampling
- systematic resampling
- stratified resampling
- residual resampling
- particle resampling
area: machine-learning/probabilistic-inference
level: core
summary: "Replace N weighted particles by N equally weighted copies, particle i copied N w_i times on average. Multinomial, residual, stratified and systematic schemes."
prereqs: [importance-sampling, inverse-transform-sampling]
see_also: [sequential-monte-carlo, particle-filter, systematic-sampling, stratified-sampling, alias-method, weighted-sampling, effective-sample-size, variance]
sources:
  - paper: doi:10.1049/ip-f-2.1993.0015
    title: "Neil J. Gordon, David J. Salmond and Adrian F. M. Smith, Novel approach to nonlinear/non-Gaussian Bayesian state estimation, IEE Proceedings F 140(2), 1993, pages 107 to 113"
    locator: the resampling step of the bootstrap filter, which draws N times with replacement from the weighted particles (multinomial resampling)
  - paper: doi:10.1080/10618600.1996.10474692
    title: "Genshiro Kitagawa, Monte Carlo filter and smoother for non-Gaussian nonlinear state space models, Journal of Computational and Graphical Statistics 5(1), 1996, pages 1 to 25"
    locator: the resampling with one sorted point in each of N equal strata (stratified resampling)
  - paper: doi:10.1080/01621459.1998.10473765
    title: "Jun S. Liu and Rong Chen, Sequential Monte Carlo methods for dynamic systems, Journal of the American Statistical Association 93(443), 1998, pages 1032 to 1044"
    locator: residual resampling, and the advice to resample only when the weights become uneven
  - paper: doi:10.1049/ip-rsn:19990255
    title: "James Carpenter, Peter Clifford and Paul Fearnhead, Improved particle filter for nonlinear problems, IEE Proceedings Radar, Sonar and Navigation 146(1), 1999, pages 2 to 7"
    locator: the O(N) resampling with one uniform number and N evenly spaced points (systematic resampling)
  - paper: doi:10.1109/ISPA.2005.195385
    title: "Randal Douc, Olivier Cappé and Eric Moulines, Comparison of resampling schemes for particle filtering, Proceedings of the 4th International Symposium on Image and Signal Processing and Analysis (ISPA), 2005, pages 64 to 69"
    locator: residual and stratified resampling have a conditional variance no larger than multinomial resampling; systematic resampling can be worse
  - book: isbn:9783030478445
    title: "Nicolas Chopin and Omiros Papaspiliopoulos, An Introduction to Sequential Monte Carlo, Springer, 2020"
    locator: "Chapter 9, Importance resampling (the resampling schemes, their unbiasedness and their O(N) implementations)"
---

Resampling replaces a set of $N$ weighted samples (particles) $x_1, \ldots, x_N$ with normalized weights $w_1, \ldots, w_N$ by $N$ unweighted copies, chosen at random so that particle $i$ gets $N w_i$ copies on average. It is the step of [sequential Monte Carlo](/sequential-monte-carlo/) and of the [particle filter](/particle-filter/) that removes particles with small weights and multiplies those with large weights, so that the work goes where the probability mass is. The four standard schemes are multinomial, residual, stratified and systematic resampling. All four are unbiased; they differ in the variance they add and in how many random numbers they use.

## In plain words

You have a bag of guesses, and each guess has a score that says how good it is. Most scores are tiny and a few are large. You want a new bag of the same size in which all guesses have the same score, but good guesses appear many times and bad ones disappear.

The plainest way is to draw from the old bag again and again, each time picking a guess with a chance equal to its score. This works, but luck can give a good guess too few copies. Better ways remove some of the luck. One gives each guess its sure whole number of copies first and draws only for the rest. Another cuts the range of chances into equal slices and draws one point in each slice. The cheapest uses one random number and steps through the slices at a fixed spacing.

## When it applies

The input is a weighted particle set: values $x_i$ and weights $w_i \ge 0$ with $\sum_i w_i = 1$, which stands for the distribution $\sum_i w_i \delta_{x_i}$. This is the output of an [importance sampling](/importance-sampling/) step. The output is a list of $N$ ancestor indices $a_1, \ldots, a_N$; the new particles are $x_{a_1}, \ldots, x_{a_N}$, each with weight $1/N$.

Let $N_i = |\{j : a_j = i\}|$ be the number of copies of particle $i$. A scheme is **unbiased** if

$$\mathbb{E}[N_i \mid w] = N w_i \quad \text{for each } i.$$

Then for each function $f$, the resampled estimate $\frac1N \sum_j f(x_{a_j}) = \frac1N \sum_i N_i f(x_i)$ has the same conditional mean $\sum_i w_i f(x_i)$ as the weighted estimate. Resampling adds variance and never removes it; it pays off later, when the copies of good particles move apart under the dynamics, and the bad particles no longer use any work.

Resample when the weights are uneven. The usual measure is the effective sample size $\mathrm{ESS} = 1/\sum_i w_i^2$, which is $N$ for equal weights and $1$ when one particle has all the weight. Sequential Monte Carlo resamples when the ESS falls under a threshold such as $N/2$. This ESS is a different quantity from the [effective sample size](/effective-sample-size/) of an MCMC run.

## The template

All schemes use the cumulative weights $C_0 = 0$, $C_i = w_1 + \cdots + w_i$, and the rule "a point $u \in [0, 1)$ selects the particle $i$ with $C_{i-1} \le u < C_i$". This is [inverse transform sampling](/inverse-transform-sampling/) for the discrete distribution $w$. The schemes differ only in how they choose the $N$ points.

```pseudo id=main
MULTINOMIAL(w, N)
L1  C ← the cumulative sums of w
L2  for j ← 1 to N: draw U_j uniform on [0, 1); a_j ← the smallest i with U_j < C_i
L3  return a, sorted

RESIDUAL(w, N)
L4  for i ← 1 to N: k_i ← ⌊N w_i⌋; put k_i copies of i in a
L5  R ← N − (k_1 + ⋯ + k_N)
L6  add R indices drawn by MULTINOMIAL from the residual weights r_i = (N w_i − k_i) / R
L7  return a, sorted

STRATIFIED(w, N)
L8  for j ← 1 to N: u_j ← (j − 1 + U_j) / N, with U_1, …, U_N independent uniforms
L9  return MERGE(w, u)

SYSTEMATIC(w, N)
L10 draw one U uniform on [0, 1)
L11 for j ← 1 to N: u_j ← (j − 1 + U) / N; return MERGE(w, u)

MERGE(w, u)                       ▷ u_1 < u_2 < ⋯ < u_N
L12 i ← 1, s ← w_1
L13 for j ← 1 to N: while u_j ≥ s do i ← i + 1, s ← s + w_i; a_j ← i
```

MERGE walks once through the sorted points and the cumulative weights, so stratified and systematic resampling take $O(N)$ time. Multinomial resampling with a [binary search](/binary-search/) for each draw takes $O(N \log N)$; it can be made $O(N)$ by generating the $N$ uniforms already sorted, or with the [alias method](/alias-method/). Residual resampling costs $O(N)$ plus the multinomial step on $R < N$ draws. The number of uniforms used is $N$, $R$, $N$ and $1$.

**Theorem (unbiasedness).** Each of the four schemes satisfies $\mathbb{E}[N_i \mid w] = N w_i$.

*Proof.* Let $I_i = [C_{i-1}, C_i)$, of length $w_i$. A point $u$ selects $i$ if and only if $u \in I_i$.

*Multinomial.* Each $U_j$ lands in $I_i$ with probability $w_i$, independently, so $N_i \sim \mathrm{Binomial}(N, w_i)$ and $\mathbb{E}[N_i] = N w_i$.

*Residual.* $N_i = k_i + M_i$, where $M_i \sim \mathrm{Binomial}(R, r_i)$. So $\mathbb{E}[N_i] = k_i + R r_i = k_i + (N w_i - k_i) = N w_i$. The $r_i$ sum to $1$ because $\sum_i (N w_i - k_i) = N - \sum_i k_i = R$.

*Stratified and systematic.* In both schemes the point $u_j$ is uniform on the stratum $S_j = [(j-1)/N, j/N)$, so $\Pr[u_j \in I_i] = N \cdot |I_i \cap S_j|$. The strata partition $[0, 1)$, and by linearity of expectation

$$\mathbb{E}[N_i] = \sum_{j=1}^N \Pr[u_j \in I_i] = N \sum_{j=1}^N |I_i \cap S_j| = N |I_i| = N w_i.$$

The joint law of the points does not matter here, so the same proof covers independent points (stratified) and points tied to one $U$ (systematic). $\blacksquare$

**Theorem (variance; Douc, Cappé and Moulines 2005).** For each function $f$ on the particles, let $\hat\mu = \frac1N \sum_i N_i f(x_i)$. Then

$$\mathrm{Var}_{\text{res}}(\hat\mu) \le \mathrm{Var}_{\text{mult}}(\hat\mu) \quad\text{and}\quad \mathrm{Var}_{\text{strat}}(\hat\mu) \le \mathrm{Var}_{\text{mult}}(\hat\mu),$$

where all variances are conditional on the weights, and $\mathrm{Var}_{\text{mult}}(\hat\mu) = \frac1N \bigl(\sum_i w_i f_i^2 - (\sum_i w_i f_i)^2\bigr)$ with $f_i = f(x_i)$.

*Proof.* Let $\phi(u) = f_i$ for $u \in I_i$. Under multinomial resampling, $N \hat\mu = \sum_j \phi(U_j)$ is a sum of $N$ independent copies of $\phi(U)$, with $U$ uniform on $[0,1)$, so $\mathrm{Var}(N\hat\mu) = N \,\mathrm{Var}\,\phi(U)$, which is the formula above.

*Stratified.* Here $N \hat\mu = \sum_j \phi(u_j)$ with independent $u_j$ uniform on $S_j$. Let $m_j$ and $v_j$ be the mean and the variance of $\phi$ on $S_j$, and $m$ the mean of $\phi$ on $[0,1)$. Then $\mathrm{Var}(N\hat\mu) = \sum_j v_j$. By the law of total variance, with the stratum index uniform on $\{1, \ldots, N\}$,

$$\mathrm{Var}\,\phi(U) = \frac1N \sum_j v_j + \frac1N \sum_j (m_j - m)^2 \ge \frac1N \sum_j v_j.$$

Multiply by $N$: $N\,\mathrm{Var}\,\phi(U) \ge \sum_j v_j$.

*Residual.* The deterministic part $\sum_i k_i f_i$ has no variance, so $\mathrm{Var}(N\hat\mu) = R \sum_i r_i (f_i - \mu_r)^2$ with $\mu_r = \sum_i r_i f_i$ (zero when $R = 0$). Let $\mu = \sum_i w_i f_i$. Since $N w_i = k_i + R r_i$,

$$N \sum_i w_i (f_i - \mu)^2 = \sum_i k_i (f_i - \mu)^2 + R \sum_i r_i (f_i - \mu)^2 \ge R \sum_i r_i (f_i - \mu)^2 \ge R \sum_i r_i (f_i - \mu_r)^2.$$

The last step holds because the mean $\mu_r$ minimizes $c \mapsto \sum_i r_i (f_i - c)^2$. The left side is $N\,\mathrm{Var}\,\phi(U)$. $\blacksquare$

**Systematic resampling keeps counts tight but has no variance guarantee.** The points $u_j$ are spaced exactly $1/N$ apart, and $I_i$ has length $w_i$, so it holds $\lfloor N w_i \rfloor$ or $\lceil N w_i \rceil$ of them: each single count has the smallest possible spread. But all points move together with the one uniform $U$, so the counts of different particles are strongly correlated, and for some $f$ the variance of $\hat\mu$ is larger than under multinomial resampling. The second example below is such a case.

## Classic examples

**Four particles.** Take $N = 4$ and $w = (0.1, 0.2, 0.3, 0.4)$, so $C = (0.1, 0.3, 0.6, 1)$ and $N w = (0.4, 0.8, 1.2, 1.6)$.

- Systematic with $U = 0.3$: the points are $0.075, 0.325, 0.575, 0.825$, the ancestors are $(1, 3, 3, 4)$, and the counts are $(1, 0, 2, 1)$.
- Stratified with $U = (0.9, 0.1, 0.5, 0.2)$: the points are $0.225, 0.275, 0.625, 0.8$, and the ancestors are $(2, 2, 4, 4)$.
- Residual: $k = (0, 0, 1, 1)$, so $R = 2$ and the residual weights are $(0.2, 0.4, 0.1, 0.3)$. Particles 3 and 4 get one sure copy each, and two more draws go by these residual weights.

The exact variances of the counts, computed by enumerating all values of the uniforms on a grid fine enough that the output is constant on each cell:

| scheme | $\mathrm{Var}(N_1)$ | $\mathrm{Var}(N_2)$ | $\mathrm{Var}(N_3)$ | $\mathrm{Var}(N_4)$ | $\mathrm{Var}(\sum_i i \, N_i)$ |
|---|---|---|---|---|---|
| multinomial | 9/25 | 16/25 | 21/25 | 24/25 | 4 |
| residual | 8/25 | 12/25 | 9/50 | 21/50 | 5/2 |
| stratified | 6/25 | 2/5 | 2/5 | 6/25 | 16/25 |
| systematic | 6/25 | 4/25 | 4/25 | 6/25 | 8/5 |

All four have $\mathbb{E}[N] = (2/5, 4/5, 6/5, 8/5) = N w$. The multinomial column is $N w_i (1 - w_i)$.

**Systematic can lose.** Take $N = 4$, $w = (1/8, 1/8, 1/8, 5/8)$ and $f = (0, 1, 0, 1)$, so $\sum_i w_i f_i = 3/4$. Systematic points are $U/4, (1+U)/4, (2+U)/4, (3+U)/4$. The last two always select particle 4. If $U < 1/2$ the first two select particles 1 and 3, and $\sum_i N_i f_i = 2$; if $U \ge 1/2$ they select particles 2 and 4, and the sum is $4$. So $\mathrm{Var}(\sum_i N_i f_i) = 1$. Multinomial gives $4 (3/4 - 9/16) = 3/4$, and stratified and residual both give $1/2$. The two random choices that systematic resampling makes are the same coin, so their errors add up instead of cancelling.

**The particle filter.** The bootstrap [particle filter](/particle-filter/) of Gordon, Salmond and Smith (1993) resamples by the multinomial scheme at every step. Kitagawa (1996) used stratified points. Carpenter, Clifford and Fearnhead (1999) introduced the systematic scheme, which is now the common default in practice because it is fast and has low variance on typical problems.

**Survey sampling, a different use.** [Systematic sampling](/systematic-sampling/) in surveys picks every $k$-th unit of a list after a random start; with probabilities proportional to size it is the same rule as systematic resampling. [Stratified sampling](/stratified-sampling/) in surveys is the source of the stratified scheme. There the goal is to choose distinct units from a population, not to copy weighted particles.

## Variations

- **Adaptive resampling.** Resample only when the ESS falls under a threshold; between resampling steps the weights are carried forward. This is the standard form in [sequential Monte Carlo](/sequential-monte-carlo/) (Liu and Chen 1998).
- **Residual with a stratified or systematic remainder.** Replace the multinomial step of line L6 by stratified or systematic resampling of the residual weights.
- **Sorted multinomial in O(N).** Generate $N$ sorted uniforms directly from the normalized partial sums of $N + 1$ exponential variables, then run MERGE.
- **Other output sizes.** Draw $M \ne N$ indices with weight $1/M$ each; all four schemes extend with $N$ replaced by $M$ in the points.
- **Resampling with weights kept.** Some schemes copy particles with a probability and keep non-uniform weights afterwards; they trade randomness against weight variance.

## Pitfalls

- **Forgetting to reset the weights.** After resampling, each new particle has weight $1/N$. Keeping the old weights counts the weights twice.
- **Resampling too often.** Each resampling step adds variance. With equal weights, multinomial resampling still drops about a fraction $1/e$ of the particles for large $N$. Resample only when the ESS is low, and compute estimates of the current target before you resample.
- **Unnormalized weights or rounding.** The rule needs $\sum_i w_i = 1$. In floating point the last cumulative sum can be slightly below $1$, and a uniform close to $1$ then falls off the end; clamp the index to $N$ as the code does.
- **Weights from logarithms.** Weights are usually computed in logarithms; subtract the largest log weight before you exponentiate, or all weights can underflow to zero.
- **Order dependence of systematic resampling.** Its output depends on the order of the particles, and it can be worse than multinomial resampling, as the example shows. Do not use it where a proof needs independent draws.
- **Sample impoverishment.** Resampling removes diversity: after several steps many particles share one ancestor, and with a deterministic state component they become exact copies. Resampling cannot fix a poor proposal.

## Exercises

1. Show that under multinomial resampling $\mathrm{Cov}(N_i, N_k) = -N w_i w_k$ for $i \ne k$. What is the covariance under systematic resampling in the four-particle example?
2. Prove that after systematic resampling $|N_i - N w_i| < 1$ for each $i$.
3. Show that residual resampling with $N w_i$ all integers is deterministic.
4. Find weights for $N = 2$ for which stratified and systematic resampling give the same law of $(N_1, N_2)$, and weights for which they differ.
5. Write MERGE so that it works in place on the particle array when the counts $N_i$ are known.

## References
