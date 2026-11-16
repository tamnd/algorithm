---
tag: ZKY15F
kind: algorithm
slug: kld-sampling
name: KLD-sampling
aliases:
- adaptive particle filter
area: robotics/localization-and-slam
level: advanced
summary: A particle filter that draws particles until their number reaches a bound from the count of occupied bins. The bound limits the KL error of the histogram only asymptotically.
solves: [mobile-robot-localization]
model: real-ram
complexity:
  vars: {n: the number of particles drawn in one step, N: the number of particles of the previous step, k: the number of occupied bins, D: the cost of one evaluation of the measurement model, epsilon: the error bound}
  time: {per_step: O(N + n log N + n D)}
  space: {extra: O(N + n + k)}
properties: {deterministic: false, exact: false, online: true, randomized: true, adaptive: true}
history:
  year: 2003
  people: [Dieter Fox]
  note: Fox chose the number of particles at each step from a statistical bound on the Kullback-Leibler divergence between the sample histogram and the true distribution, and used it for Monte Carlo localization.
prereqs: [monte-carlo-localization, kullback-leibler-divergence]
see_also: [particle-filter, chi-squared-goodness-of-fit-test, wilks-theorem, likelihood-ratio-test, central-limit-theorem, global-localization, resampling, sequential-monte-carlo]
sources:
  - paper: doi:10.1177/0278364903022012001
    title: "Dieter Fox, Adapting the sample size in particle filters through KLD-sampling, The International Journal of Robotics Research 22(12), 2003, pages 985 to 1003"
    locator: "the bound of equation (13), the Wilson-Hilferty form of equation (14), the KLD-sampling algorithm of Table 2 and the localization experiments"
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 8, Section 8.3.7 (KLD-sampling)"
---

KLD-sampling is a variant of [Monte Carlo localization](/monte-carlo-localization/) that chooses the number of particles at each step. It draws the new particles one at a time and puts each in a bin of a fixed grid over the pose space. It stops when the number of particles $n$ reaches a bound that grows with the number $k$ of bins that hold at least one particle. When the belief is spread out, as at the start of [global localization](/global-localization/), many bins are occupied and the filter uses many particles. When the belief is concentrated, few bins are occupied and the filter uses few. Fox (2003) derived the bound from the distribution of the [Kullback-Leibler divergence](/kullback-leibler-divergence/) between a sample histogram and the true distribution: with $n = \chi^2_{k-1, 1-\delta} / (2\varepsilon)$ samples, the divergence is at most $\varepsilon$ with probability about $1 - \delta$. This holds only asymptotically, and only for the histogram of independent samples of a fixed distribution.

## In plain words

A robot that does not know where it is needs many guesses, because the guesses must cover the whole building. Once it knows where it is, a few guesses near the right place are enough. KLD-sampling counts how many different areas the guesses fall in while it makes them. Each new area means that more guesses are needed. It stops when it has enough guesses for the number of areas it has seen. So the robot spends its computation where it helps, and runs fast when it is sure of its pose.

## The problem

The setting is [Monte Carlo localization](/monte-carlo-localization/): a map, a motion model that can be sampled, a measurement model that can be evaluated, and a weighted particle set $\{(x_{t-1}^{[i]}, w_{t-1}^{[i]})\}$ for the previous belief. In addition, there is a grid of bins over the pose space, an error bound $\varepsilon > 0$ and a probability $\delta \in (0, 1)$. The output is a weighted particle set for the new belief, with a number of particles that depends on the belief.

The goal behind the bound is this. Let a distribution $p$ over $k$ bins be sampled $n$ times independently, and let $\hat p$ be the histogram of the samples. Choose $n$ so that $P(K(\hat p, p) \le \varepsilon) \approx 1 - \delta$, where $K(\hat p, p) = \sum_j \hat p_j \log(\hat p_j / p_j)$.

## The algorithm

**The bound.** By the [likelihood ratio test](/likelihood-ratio-test/) theory ([Wilks' theorem](/wilks-theorem/)), $2 n K(\hat p, p)$ converges in distribution to the chi-square distribution with $k - 1$ degrees of freedom as $n \to \infty$. So the probability that $K(\hat p, p) \le \varepsilon$ is about $1 - \delta$ for

$$n = \frac{1}{2\varepsilon} \chi^2_{k-1, 1-\delta}$$

(Fox, equation (13)), where $\chi^2_{k-1, 1-\delta}$ is the $1 - \delta$ quantile. The Wilson-Hilferty approximation of the quantile gives

$$n \approx \frac{k-1}{2\varepsilon} \left(1 - \frac{2}{9(k-1)} + \sqrt{\frac{2}{9(k-1)}}\, z_{1-\delta}\right)^3$$

(Fox, equation (14)), where $z_{1-\delta}$ is the $1 - \delta$ quantile of the standard normal distribution. For large $k$, $n$ is about $(k-1)/(2\varepsilon)$: linear in the number of occupied bins.

**The sampler.** $k$ is not known in advance. KLD-sampling counts the bins that the new particles occupy and updates the bound after each new bin.

```pseudo id=main
KLD-MCL(X_{t-1}, u_t, z_t, m, ε, δ, n_min, n_max)
L1  X_t ← ∅;  n ← 0;  k ← 0;  n_χ ← 0;  all bins empty
L2  repeat
L3      draw an index i with probability w_{t-1}^[i] / Σ w_{t-1}
L4      x ← sample of p(x_t | u_t, x_{t-1}^[i], m)
L5      w ← p(z_t | x, m);  add (x, w) to X_t
L6      if the bin of x is empty then
L7          mark it nonempty;  k ← k + 1
L8          if k > 1 then n_χ ← (k-1)/(2ε) · (1 - 2/(9(k-1)) + √(2/(9(k-1))) z_{1-δ})³
L9      n ← n + 1
L10 until (n ≥ n_χ and n ≥ n_min) or n ≥ n_max
L11 return X_t
```

Unlike the MCL of Thrun et al., which moves and then resamples a set of fixed size, KLD-sampling draws each new particle independently from the previous weighted set (line L3), so the number of draws can be chosen while sampling. The new set stays weighted. Fox uses a lower limit $n_\text{min}$ (typically 10). The code adds $n_\text{max}$ so that the loop always ends.

**The loop condition.** The listing of the algorithm in Fox (2003), Table 2, prints the loop condition as "while ($n < n_\chi$ and $n < n_{\chi\text{min}}$)". With $n_\chi = 0$ at the start, this would stop after one particle. The text and the version of Thrun et al. (Section 8.3.7) mean that the loop continues while either bound is not reached, which is line L10 here.

## Example

**The bound for $\varepsilon = 0.05$.** The table gives $\lceil n \rceil$ by the Wilson-Hilferty form, and in brackets by the exact chi-square quantile where they differ.

| $k$ | $\delta = 0.01$ | $\delta = 0.05$ | $\delta = 0.01$, $\varepsilon = 0.1$ |
|---|---|---|---|
| 2 | 66 (67) | 38 | 33 |
| 3 | 93 | 60 | 47 |
| 5 | 134 (133) | 95 | 67 |
| 10 | 217 | 170 | 109 |
| 20 | 363 (362) | 302 | 182 |
| 50 | 750 | 664 | 375 |
| 100 | 1347 | 1233 | 674 |
| 1000 | 11060 | 10737 | 5530 |

The Wilson-Hilferty form is worst for $k = 2$, with 1 degree of freedom, where it is up to 2.5 percent low for $\delta = 0.05$ and $\delta = 0.1$. For $k \ge 5$ it is within 0.5 percent of the exact value in the tests.

**Coverage.** The test draws $n = 147$ samples, the bound for $k = 10$, $\varepsilon = 0.05$ and $\delta = 0.1$, from a fixed distribution over 10 bins, 1500 times. The divergence of the histogram is at most $0.05$ in 89.1 percent of the trials, against the asymptotic $90$ percent. This is a measurement for one distribution and one seed.

**Localization on a ring.** A robot moves 1 m per step on a ring of 30 m with a color in each 1 m cell, and the bins are 0.5 m long, 60 bins in all. The start is 5000 particles spread over the ring. With $\varepsilon = 0.05$ and $\delta = 0.01$, the numbers of particles in the first 10 steps are 872, 836, 688, 444, 444, 263, 248, 169, 134 and 114, and in the last 7 of 25 steps they are 93 or 114, which is the bound for 3 or 4 bins. The first step occupies all 60 bins, and the bound for $k = 60$ is 872. This is a measurement for one seed.

## Correctness

The [correctness proof](proofs/correctness.md) shows three things. The loop ends after at most $n_\text{max}$ draws. When it ends before $n_\text{max}$, $n \ge \max(n_\text{min}, n_\chi(k))$ for the number $k$ of occupied bins. And, for $n$ independent samples of a fixed distribution with $k$ bins of positive mass and $n$ set by equation (13), $P(K(\hat p, p) \le \varepsilon) \to 1 - \delta$ as $\varepsilon \to 0$.

Each of these is a theorem with its assumptions. The use of the bound for a particle filter is a heuristic, for these reasons.

- The bound is asymptotic. For small $n$ the true probability can differ from $1 - \delta$.
- It is about the histogram of the samples, not about the continuous belief, and the grid size sets what it measures.
- The particles are drawn from the predicted belief and weighted afterwards, so the histogram that the bound controls is that of the proposal, not that of the posterior.
- $k$ is counted from the samples themselves, and it grows while they are drawn.
- A bound on the error of one step does not bound the error over many steps. Fox (2003) states that the approach is not guaranteed not to diverge.

## Complexity

Let $N$ be the size of the previous set and $n$ the number of new particles.

- Building the cumulative weights: $O(N)$.
- Each draw in line L3 by binary search: $O(\log N)$. Each motion sample: $O(1)$. Each weight: $O(D)$.
- Each bin test: $O(1)$ expected time with a hash set.
- Total per step: $O(N + n \log N + n D)$. Space: $O(N + n + k)$.

The point is that $n$ adapts: it is about $(k-1)/(2\varepsilon)$ for large $k$, and $\max(n_\text{min}, n_\chi(k))$ in general. During tracking, $k$ is small and $n$ can be one or two orders of magnitude below the $n$ needed for global localization.

## Properties

- **Adaptive.** The number of particles follows the spread of the belief, as measured by the number of occupied bins.
- **Two parameters with meaning.** $\varepsilon$ and $\delta$ replace the number of particles, which is hard to choose. The grid size is a third parameter, and it matters as much.
- **No guarantee to find the pose.** Like plain MCL, it can lose the true pose. When the belief is concentrated at a wrong pose, $k$ is small and so is $n$, which makes recovery harder. Random particles, as in augmented MCL, help.
- **Monotone bound.** $n_\chi(k)$ increases with $k$ and with $1/\varepsilon$, and $n_\chi(k)$ for $2\varepsilon$ is half of that for $\varepsilon$.

## Variants and improvements

- **Exact quantile.** Compute $\chi^2_{k-1, 1-\delta}$ exactly, for example by bisection on the regularized incomplete gamma function, as the test does. For $k \ge 5$ the gain is under 0.5 percent.
- **Bins by tree.** Instead of a fixed grid, count leaves of a [kd-tree](/kd-tree/) or of a multi-resolution grid to adapt the bin size.
- **Adaptive resampling.** Combine KLD-sampling with resampling only when the effective sample size is low.
- **Random particles.** Add a few random poses at each step, as in augmented MCL, so that a wrong concentrated belief can still recover.

## When to use it

Use KLD-sampling in Monte Carlo localization when the robot has phases with very different uncertainty, such as a global start and long tracking, and computation is limited. The gain is large when the map is large compared with the bin size. When the belief always stays concentrated, a fixed small number of particles is as good and simpler.

## Pitfalls

- **Bins too large.** With large bins, a tracked belief occupies one or two bins, $n$ drops to $n_\text{min}$, and the filter can lose the true pose. With bins too small, $k$ grows with $n$ and the loop can run to $n_\text{max}$.
- **Heading bins.** The grid must include the heading. A 2D position grid alone hides spread in the heading.
- **The printed loop condition.** Copying the "and" of Table 2 in Fox (2003) gives a sampler that stops after one particle. Use "or" for the continue condition, or "and" for the stop condition as in line L10.
- **Reading the bound as a guarantee.** The probability $1 - \delta$ is asymptotic and about the histogram of the proposal. It does not mean that the filter keeps the error of the belief below $\varepsilon$.
- **No upper limit.** Without $n_\text{max}$, a belief spread over a very large map can make the loop draw more particles than fit in memory.

## Implementations

## History

Fox presented KLD-sampling at a conference in 2001 and in a journal article in 2003, with experiments in Monte Carlo localization where, in his measurements, the adaptive filter needed far fewer particles than a filter of fixed size for the same accuracy. Thrun, Burgard and Fox (2005) include it in Chapter 8 as a standard part of MCL. Its form of the bound, a chi-square quantile in the number of occupied bins, comes from the classical asymptotic theory of the likelihood ratio and of Pearson's chi-square statistic.

## References
