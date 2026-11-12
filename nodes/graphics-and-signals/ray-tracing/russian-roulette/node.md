---
tag: QF25TE
kind: technique
slug: russian-roulette
name: Russian roulette
aliases:
- unbiased path termination
area: graphics-and-signals/ray-tracing
level: intro
summary: Stop a random sum or path with probability 1 - q and divide what survives by q. The expected value does not change, so infinite sums get finite, unbiased estimates.
prereqs: [monte-carlo-integration, expected-value]
see_also: [path-tracing, light-tracing, importance-sampling, geometric-distribution, neumann-series, particle-filter]
sources:
  - paper: doi:10.1145/97879.97886
    title: James Arvo and David Kirk, Particle transport and image synthesis, Computer Graphics (SIGGRAPH 90) 24(4), 1990, 63 to 66
    locator: Russian roulette and splitting, taken from particle transport into image synthesis
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 13.7 Russian Roulette and Splitting, and the use in Section 14.5 Path Tracing
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: Chapter 2, Monte Carlo Integration (variance reduction by Russian roulette and splitting)
  - book: isbn:9781568813073
    title: Philip Dutré, Kavita Bala and Philippe Bekaert, Advanced Global Illumination, second edition, A K Peters, 2006
    locator: Chapter 3, Monte Carlo Methods, and Chapter 5, Stochastic Path-Tracing Algorithms
---

Russian roulette replaces a random value $X$ by $X / q$ with the probability $q$ and by $0$ otherwise, so the expected value stays $E[X]$ for any $q$ in $(0, 1]$. Applied after each term of a sum, it stops the sum at a random point and gives an unbiased estimate of an infinite series with a finite expected amount of work. It is how [path tracing](/path-tracing/) and [light tracing](/light-tracing/) end their paths without the bias of a fixed depth. The price is a larger [variance](/variance/). The method comes from the Monte Carlo simulation of particle transport, and Arvo and Kirk brought it to image synthesis in 1990.

## In plain words

Suppose you must add up a very long list of numbers, and the late numbers are small. You could stop at some fixed place, but then your answer is always a little too small. Russian roulette stops at a random place instead.

After each number, flip a biased coin. If the coin says stop, you stop. If it says go on, you go on, and from then on you count every number as if it were bigger, by the factor of how unlikely it was to get this far. A sum that stops early is too small, and a sum that goes far is too big, and on average the two cancel exactly. You get the right answer on average, and you almost never have to read the whole list. Each single answer is less precise than the full sum.

## When it applies

- **An unbiased estimate is needed and the work can be cut at random points.** The quantity is a sum $\sum_k a_k$ with many or infinitely many terms, an integral of a [Neumann series](/neumann-series/), or one term whose computation is costly.
- **The terms are not negative, or the sum converges absolutely.** Then the expected value of the estimate can be computed term by term.
- **The late terms are small.** Roulette saves work on terms that add little. A good survival probability follows the size of what is still to come; for light paths, the throughput or the albedo.
- **The survival probability can be computed from the past.** It may depend on anything that is known when the coin is thrown, but not on the coin.

## The template

ROULETTE is one step on a value $X$ that is known or cheap to estimate. ROULETTE-SUM applies it after each term of a sum. The holes are the terms and the survival rule.

```pseudo id=main
ROULETTE(X, q)
L1  draw u uniform in [0, 1);  if u < q then
L2      return X / q
L3  return 0

ROULETTE-SUM(a, q)
L4  S ← 0;  w ← 1;  k ← 0
L5  loop:  S ← S + w · a(k)          ▷ hole: term k, or an unbiased estimate of it given the past
L6      qk ← q(k, w)                  ▷ hole: a survival probability in [0, 1], from the past only
L7      draw u uniform in [0, 1);  if u ≥ qk then return S
L8      w ← w / qk
L9      k ← k + 1
```

The weight $w$ at term $k$ is $1 / (q_0 q_1 \cdots q_{k-1})$, the inverse of the probability that the sum reaches term $k$.

**Why the mean is exact.** For one step, $E[\text{ROULETTE}(X, q)] = q \cdot E[X] / q = E[X]$. For the sum, let $R_k$ be the event that term $k$ is reached and $w_k$ the weight there. Given the past at term $k$, the event $R_{k+1}$ has probability $q_k$ and gives $w_{k+1} = w_k / q_k$, so $E[\mathbf{1}[R_{k+1}]\, w_{k+1} \mid \text{past}] = \mathbf{1}[R_k]\, w_k$ when $q_k > 0$. By induction $E[\mathbf{1}[R_k]\, w_k] = 1$, and if each term estimate has the conditional mean $a_k$, then $E[\mathbf{1}[R_k]\, w_k\, \hat a_k] = a_k$. With terms that are not negative (or a sum that converges absolutely), the expected value of $S$ is $\sum_k a_k$. This needs $q_k > 0$ at every point where a later term can be nonzero: a step with $q_k = 0$ throws away the tail.

**The variance.** For one step,

$$\operatorname{Var}[\text{ROULETTE}(X, q)] = \frac{E[X^2]}{q} - E[X]^2 = \frac{\operatorname{Var}[X]}{q} + \frac{1 - q}{q}\, E[X]^2,$$

which is larger than $\operatorname{Var}[X]$ for each $q < 1$. Roulette pays off when the work it saves is worth more than the variance it adds: the efficiency of an estimator is $1 / (\text{variance} \times \text{cost})$, and roulette raises efficiency when it stops the work on terms that are small.

## Classic examples

**A finite sum, exact.** Take the five terms $a = (3, \tfrac12, 2, \tfrac54, 1)$ with the sum $\tfrac{31}{4} = 7.75$, the constant survival $q = \tfrac12$, and a sure stop after the last term. The weights are $1, 2, 4, 8, 16$, and the sum stops after term $k$ with these probabilities:

| stop after term | probability | value of $S$ |
|---|---|---|
| 0 | $\tfrac12$ | $3$ |
| 1 | $\tfrac14$ | $3 + 2 \cdot \tfrac12 = 4$ |
| 2 | $\tfrac18$ | $4 + 4 \cdot 2 = 12$ |
| 3 | $\tfrac{1}{16}$ | $12 + 8 \cdot \tfrac54 = 22$ |
| 4 | $\tfrac{1}{16}$ | $22 + 16 \cdot 1 = 38$ |

The mean is $\tfrac32 + 1 + \tfrac32 + \tfrac{22}{16} + \tfrac{38}{16} = \tfrac{31}{4}$, exactly the sum. The expected number of terms read is $\tfrac{31}{16} \approx 1.94$ of $5$, and the variance is $\tfrac{1391}{16} \approx 86.9$, where the full sum has variance $0$. Without the division of line L8 the mean is $3 + \tfrac14 + \tfrac12 + \tfrac{5}{64} + \tfrac{1}{16} = \tfrac{127}{32} \approx 3.97$, about half of the true sum. With the survival probabilities $(\tfrac13, \tfrac34, 1, \tfrac15)$ the mean is again $\tfrac{31}{4}$, now with variance $\tfrac{1267}{16}$ and $\tfrac{113}{60} \approx 1.88$ terms on average.

**The furnace.** In a closed scene where every surface emits radiance $e$ and has albedo $\rho < 1$, the radiance is the [geometric series](/geometric-series/) $e (1 + \rho + \rho^2 + \cdots) = e / (1 - \rho)$. With cosine sampling and $q = \rho$, the weight after each bounce is $\rho / q = 1$, so each path gives $e$ times its number of vertices. That number has a [geometric distribution](/geometric-distribution/) with mean $1 / (1 - \rho)$ and variance $\rho / (1 - \rho)^2$. With $e = 1.5$ and $\rho = 0.6$, the exact answer is $3.75$ and one path has the standard deviation $1.5 \sqrt{0.6} / 0.4 \approx 2.90$.

**[Path tracing](/path-tracing/).** After each bounce, the path survives with a probability such as $\min(1, \rho)$ or $\min(1, \beta)$ for the throughput $\beta$, and $\beta$ is divided by it. Many renderers start roulette only after a few bounces, because the first bounces carry most of the light.

**[Light tracing](/light-tracing/), [photon mapping](/photon-mapping/) and [bidirectional path tracing](/bidirectional-path-tracing/).** A particle from a light is absorbed with probability $1 - q$ at each surface. Photon tracing often takes $q$ equal to the albedo, so that each surviving photon keeps the same power.

**Random walks for linear systems.** A random walk on the indices of a matrix with $\|T\| < 1$ estimates one entry of $(I - T)^{-1} b = \sum_k T^k b$, the Neumann series, and stops with roulette. The rendering equation is the continuous case.

## Variations

- **Splitting.** The opposite step: replace $X$ by the mean of $s$ independent copies. The expected value stays the same and the variance falls, at $s$ times the cost. Renderers split where a path has a high weight, for example at the first bounce or at a light sample.
- **Survival by throughput.** $q = \min(1, \beta / \beta_{\text{target}})$ keeps the weights of all surviving paths near a target, which bounds the weights and avoids rare large values.
- **Delayed start.** $q = 1$ for the first $d$ bounces. This is still unbiased; it only adds work on the early bounces, where it is useful.
- **Weight windows.** Particle transport codes keep the weight in a window: roulette below the window, splitting above it.
- **Unbiased series estimators.** The same idea with a random stopping index whose distribution is fixed in advance gives the single-term and the Russian roulette estimators of an infinite series in statistics.

## Pitfalls

- **No division by $q$.** This is the common bug. The estimate then has the mean $\sum_k a_k\, q_0 \cdots q_{k-1}$, which is too small; in the example above it is $3.97$ in place of $7.75$.
- **$q = 0$ too early.** A survival probability of $0$ at a point where more light can still arrive cuts the tail and gives bias. Use a small positive floor, or stop only where the rest is known to be $0$.
- **$q$ that never falls below 1.** With $q = \min(1, \rho)$ in a closed scene with $\rho = 1$, paths never stop. Cap $q$ below 1.
- **A survival rule that looks at the coin.** $q$ must be fixed before $u$ is drawn. A rule that depends on $u$, or on a term that is computed only for the paths that survive, breaks the proof.
- **Too low survival.** A small $q$ gives large weights $1 / q$ and bright single pixels. The mean is right, but the variance may cost more than the work saved.

## Exercises

1. Prove the variance formula of one step, and show that ROULETTE with $q < 1$ never lowers the variance.
2. In the five-term example, find the expected number of terms for a general constant $q$, and the $q$ that minimizes the product of the variance and the expected number of terms.
3. Show that splitting into $s$ copies, then one roulette step with $q = 1 / s$, has the same mean as $X$, and find its variance.
4. A sum of positive terms that do not increase uses $q_k = a_{k+1} / a_k$. Show that each reached term adds exactly $w_k\, a_k = a_0$, so that the estimate is $a_0$ times the number of terms read, and find its variance for $a_k = r^k$.
5. Give a rule that sets $q$ after looking at $u$ and makes the estimate biased.

## References
