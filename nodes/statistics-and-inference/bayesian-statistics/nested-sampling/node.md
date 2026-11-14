---
tag: G4YCZZ
kind: algorithm
slug: nested-sampling
name: Nested sampling
aliases:
- Skilling's nested sampling
area: statistics-and-inference/bayesian-statistics
level: advanced
summary: Skilling's estimator of the marginal likelihood that replaces the worst of a set of live points by a new prior draw of higher likelihood and integrates over the shrinking prior mass.
model: real-ram
complexity:
  vars: {N: the number of live points, H: "the information, KL(posterior || prior), in nats", K: "log(1/eps) for the stopping tolerance eps", C: the cost of one constrained prior draw}
  time: {expected: Θ(N (H + K) C)}
  space: {extra: Θ(N (H + K))}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2006
  people: [John Skilling]
  note: Skilling presented nested sampling in 2004 and published the full account in Bayesian Analysis in 2006. Chopin and Robert (2010) proved its consistency. MultiNest, PolyChord and dynamic nested sampling made it a standard tool in cosmology and astrophysics.
prereqs: [marginal-likelihood, monte-carlo-integration, kullback-leibler-divergence, bayes-factor]
see_also: [bridge-sampling, laplace-approximation, annealed-importance-sampling, sequential-monte-carlo, slice-sampling, parallel-tempering, simulated-annealing, metropolis-hastings]
sources:
  - paper: doi:10.1214/06-BA127
    title: "John Skilling, Nested sampling for general Bayesian computation, Bayesian Analysis 1(4), 2006"
    locator: "pages 833 to 859: the transformation of Z into a one-dimensional integral over the prior mass X, the shrinkage of X by Beta(N, 1) factors, the information H and the error estimate sqrt(H/N), and the termination rule (general locator)"
  - paper: doi:10.1093/biomet/asq021
    title: "Nicolas Chopin and Christian P. Robert, Properties of nested sampling, Biometrika 97(3), 2010"
    locator: "pages 741 to 755: consistency of the estimate and the order N^(-1/2) of its error under exact constrained draws (general locator)"
---

Nested sampling estimates the [marginal likelihood](/marginal-likelihood/) $Z = \int L(\theta)\pi(\theta)\, d\theta$, where $L(\theta) = f(x \mid \theta)$ is the likelihood and $\pi$ the prior. It rewrites $Z$ as a one-dimensional integral $Z = \int_0^1 L(X)\, dX$ over the prior mass $X$ that lies above a given likelihood level. It keeps $N$ live points drawn from the prior. At each step it removes the live point with the lowest likelihood, which shrinks the prior mass above it by a random factor with known law, $\mathrm{Beta}(N, 1)$, and replaces the point by a prior draw constrained to higher likelihood. The removed points, with weights, give $Z$ and a weighted posterior sample. The error of $\log Z$ is about $\sqrt{H/N}$, where $H$ is the information gained from prior to posterior.

## In plain words

Picture the likelihood as a landscape of hills and the prior as a layer of sand over it. To find the total "weight" of the landscape, you can slice it into horizontal layers and add up height times the area of sand above each height. Nested sampling makes these slices from the bottom up. It keeps a fixed number of sample points spread over the sand. At each step it throws away the lowest point, and that point's height becomes the next slice. On average, each step removes the same small fraction of the remaining sand, so the area above each slice is known without measuring it. A new point is then placed at random anywhere higher than the one thrown away. The run stops when the points left can add almost nothing. The cost is to find random points above a given height.

## The problem

**Input.** A proper prior $\pi$ from which we can draw, a likelihood $L(\theta) \ge 0$ that we can evaluate, a number $N$ of live points, and a stopping tolerance $\varepsilon$. A routine that draws from $\pi$ restricted to $\{\theta : L(\theta) > L^*\}$ for any level $L^*$.

**Output.** An estimate of $\log Z$, an estimate of its error, and weighted posterior draws.

**The prior mass.** For a level $\lambda$, let $X(\lambda) = \pi(L > \lambda)$ be the prior mass above it. $X$ decreases from $1$ to $0$ as $\lambda$ grows. Its inverse $L(X)$ is a non-increasing function on $(0, 1)$, and the layer-cake identity

$$Z = \int_0^\infty X(\lambda)\, d\lambda = \int_0^1 L(X)\, dX$$

turns an integral over $\Theta$, of any dimension, into an integral of a monotone function of one variable. The difficulty is that $X$ cannot be computed. Nested sampling estimates it from the order of the likelihood values.

## The algorithm

```pseudo id=main
NESTED-SAMPLING(π, L, N, ε)
L1  draw θ₁..θ_N from π                          ▷ the live points
L2  Z ← 0;  X₀ ← 1;  i ← 0
L3  repeat
L4      i ← i + 1;  k ← argmin_j L(θ_j);  Lᵢ* ← L(θ_k)     ▷ the dead point
L5      Xᵢ ← exp(-i/N)                            ▷ estimated prior mass above Lᵢ*
L6      wᵢ ← X_{i-1} - Xᵢ;  Z ← Z + Lᵢ* wᵢ
L7      θ_k ← a draw from π restricted to {θ : L(θ) > Lᵢ*}
L8  until max_j L(θ_j) · Xᵢ < ε Z
L9  Z ← Z + (Xᵢ/N) Σ_j L(θ_j)                     ▷ the live points share the rest
L10 return Z, the dead points with weights Lᵢ* wᵢ / Z, and the live points with weights L(θ_j) Xᵢ / (N Z)
```

L1 starts with $N$ independent prior draws. At every step, the live points are independent draws from the prior above the current level, so their prior masses are independent uniform values below the current mass $X_{i-1}$. L4 picks the lowest likelihood, which is the point with the largest prior mass. Its mass is the largest of $N$ uniform values on $(0, X_{i-1})$, so the ratio $t_i = X_i/X_{i-1}$ has the law $\mathrm{Beta}(N, 1)$, whatever the model is. Since $\mathbb{E}\log t_i = -1/N$, L5 sets $\log X_i$ to its mean $-i/N$. L6 adds the slab between $X_i$ and $X_{i-1}$ at height $L_i^*$. L7 is the only model-specific step: it must give an independent draw from the prior above the new level. L8 stops when even the best live point, times the remaining mass, would change $Z$ by less than a fraction $\varepsilon$. L9 adds the remaining mass, shared equally among the live points.

The implementation works with $\log L$, $\log X$ and $\log Z$, and adds terms with log-sum-exp, because $L$ is often $e^{-1000}$. It keeps the live points in a heap keyed by $L$. It also computes the information

$$H = \int p(\theta \mid x)\log\frac{p(\theta \mid x)}{\pi(\theta)}\, d\theta \approx \sum_i \frac{L_i^* w_i}{Z}\log L_i^* - \log Z,$$

the [Kullback-Leibler divergence](/kullback-leibler-divergence/) from the prior to the posterior, and reports $\sqrt{H/N}$ as the error of $\log Z$.

**Constrained draws.** In the tests, $\{L > L^*\}$ is an interval, so L7 draws from the prior restricted to it exactly by the inverse distribution function. In real problems, L7 is approximate: a short Markov chain started from a random live point ([slice sampling](/slice-sampling/) or random walk [Metropolis-Hastings](/metropolis-hastings/) that rejects moves below $L^*$), or a draw from ellipsoids that bound the live points.

## Example

**Trace.** $3$ successes in $10$ Bernoulli trials, $L(p) = \binom{10}{3}p^3(1-p)^7$, uniform prior on $p$. The exact value is $Z = 1/11$, $\log Z = -2.397895$; the posterior is Beta(4, 8) and $H = 0.6366$. Run with $N = 4$, $\varepsilon = 10^{-3}$ and `random.Random(4)`. The column "true $X_i$" is the length of the interval $\{L > L_i^*\}$, which the method does not know.

| $i$ | dead point $p$ | $L_i^*$ | $\hat X_i = e^{-i/4}$ | true $X_i$ | $w_i$ | $Z$ so far |
|---|---|---|---|---|---|---|
| 1 | 0.1032 | 0.06149 | 0.7788 | 0.4652 | 0.2212 | 0.01360 |
| 2 | 0.1341 | 0.10563 | 0.6065 | 0.3785 | 0.1723 | 0.03180 |
| 3 | 0.1550 | 0.13742 | 0.4724 | 0.3240 | 0.1342 | 0.05023 |
| 4 | 0.4524 | 0.16404 | 0.3679 | 0.2797 | 0.1045 | 0.06737 |
| 5 | 0.3966 | 0.21800 | 0.2865 | 0.1826 | 0.0814 | 0.08511 |
| 6 | 0.3961 | 0.21849 | 0.2231 | 0.1816 | 0.0634 | 0.09896 |
| 7 | 0.2360 | 0.23969 | 0.1738 | 0.1336 | 0.0494 | 0.11079 |
| 8 | 0.3537 | 0.25009 | 0.1353 | 0.1040 | 0.0384 | 0.12040 |

The dead points move in from both sides towards the mode $0.3$, and their likelihoods increase. In this run the first dead point was low by chance: the true mass $0.4652$ is far below the estimate $0.7788$, because the largest of $4$ uniform values happened to be small. That error stays in every later $\hat X_i$. The test of L8 stops after $32$ dead points, and L9 adds the $4$ live points. The result is $\log\hat Z = -1.8590$, an error of $0.54$, with the reported error bar $0.17$. With $N = 4$ the error bar is unreliable too, since it uses the estimated $H = 0.11$ in place of $0.64$.

**The error is about $\sqrt{H/N}$.** Same model, $\varepsilon = 10^{-6}$: over $400$ runs with $N = 4$ the standard deviation of $\log\hat Z$ is $0.422$, against $\sqrt{H/N} = 0.399$. Over $100$ runs with $N = 50$ it is $0.114$, against $0.113$.

**Normal-normal.** $x_1, \ldots, x_{20} \sim N(\theta, 1)$, prior $\theta \sim N(0, 10^2)$, data from `random.Random(1)`, exact $\log Z = -31.327583$ and $H = 3.3061$ from the closed form in the proof. With $\varepsilon = 10^{-6}$ and exact constrained draws:

| $N$ | runs | mean error | standard deviation | $\sqrt{H/N}$ | iterations |
|---|---|---|---|---|---|
| 25 | 200 | 0.054 | 0.391 | 0.364 | 451 |
| 100 | 200 | $-0.007$ | 0.184 | 0.182 | 1802 |
| 400 | 50 | $-0.023$ | 0.094 | 0.091 | 7200 |

The standard deviation halves when $N$ is multiplied by $4$, and stays within $8$ percent of $\sqrt{H/N}$. The number of iterations is about $N(H + \log(1/\varepsilon)) = N \cdot 17.1$, a little more because the test of L8 uses the estimated $Z$.

## Correctness

The full proof is in proofs/correctness.md. It proves:

1. **The layer-cake identity** $Z = \int_0^1 L(X)\, dX$ with $L(X)$ non-increasing, for every prior and likelihood.
2. **Uniform prior masses.** If the law of $L(\theta)$ under the prior has no atoms, the prior mass $X(L(\theta))$ of a prior draw is uniform on $(0, 1)$, and that of a draw constrained to $L > \lambda$ is uniform on $(0, X(\lambda))$.
3. **The shrinkage law.** With exact, independent constrained draws, the ratios $t_i = X_i/X_{i-1}$ of the true masses are independent $\mathrm{Beta}(N, 1)$. So $-\log t_i$ is exponential with rate $N$, $\mathbb{E}\log X_i = -i/N$ and $\mathrm{Var}\log X_i = i/N^2$. The key invariant is: after each step, the live points are independent prior draws above the current level.
4. **The estimate.** With the true masses, the sum of L6 is an upper Riemann sum of $\int_{X_m}^1 L(X)\, dX$ for a monotone function, and the live-point term estimates the rest. L5 uses the geometric mean of $X_i$.
5. **The information** of the normal-normal model in closed form.

What is proved and what is only measured: items 1 to 3 and 5 are exact. The error size $\sqrt{H/N}$ is a heuristic of Skilling (2006): the posterior mass sits near $\log X = -H$, reached after about $NH$ steps, where $\log X$ has standard deviation $\sqrt{NH}/N$. Chopin and Robert (2010) prove consistency and an error of order $N^{-1/2}$ with exact constrained draws; this page cites that result and does not prove it. The agreement of the measured standard deviations with $\sqrt{H/N}$ in the tables is measured only. With approximate constrained draws, none of the guarantees hold.

## Complexity

The run ends when $\log X_i$ is near $-H - \log(1/\varepsilon)$, after about $N(H + K)$ iterations with $K = \log(1/\varepsilon)$. Each iteration makes one constrained draw of cost $C$ and one heap update of cost $O(\log N)$; the test of L8 costs $O(N)$, and the code runs it once every $N$ iterations. The expected time is $\Theta(N(H + K)C)$. Since the error is about $\sqrt{H/N}$, halving the error costs four times the work. $H$ grows with the dimension $d$, roughly like $\frac{d}{2}\log(n)$ for $n$ data points in a regular model, and the cost $C$ of a constrained draw also grows with $d$. The dead points take $\Theta(N(H + K))$ space.

## Properties

- **Randomized and not exact.** $\log\hat Z$ has a random error of size about $\sqrt{H/N}$, and $\hat Z$ has a small bias in finite runs.
- **One run gives three results:** $\log Z$, an error estimate, and a weighted posterior sample.
- **No tuning of a temperature schedule.** The level of L4 sets its own schedule, which adapts to the likelihood.
- **Handles phase transitions.** Methods that follow a path of tempered posteriors $\pi L^\beta$ can jump across a region where the energy changes suddenly; nested sampling moves in prior mass and does not.
- **Needs a proper prior** from which one can draw, and works best when the posterior is not far smaller than the prior, since the work grows with $H$.

## Variants and improvements

- **Ellipsoidal and multi-ellipsoidal sampling.** Mukherjee, Parkinson and Liddle (2006) draw L7 from an ellipsoid around the live points; MultiNest (Feroz, Hobson and Bridges, 2009) uses several ellipsoids for multimodal posteriors.
- **Slice sampling in L7.** PolyChord (Handley, Hobson and Lasenby, 2015) replaces L7 by a short [slice sampling](/slice-sampling/) chain, which scales to more dimensions than ellipsoids.
- **Dynamic nested sampling.** Higson and coauthors (2019) change $N$ during the run, with more live points where the posterior mass is.
- **Several dead points per step.** Removing the $r$ worst points at once lets $r$ constrained draws run in parallel; $\log X$ then shrinks by order statistics of uniform values.
- **Random $X_i$.** Replace the plug-in of L5 by draws of $t_i \sim \mathrm{Beta}(N, 1)$, repeat the sum many times, and read the error bar from the spread of $\log\hat Z$.

## When to use it

Use nested sampling when you need the [marginal likelihood](/marginal-likelihood/) and also posterior draws, the posterior may be multimodal, and the dimension is small or moderate. It is a standard choice for [Bayes factors](/bayes-factor/) in cosmology and astrophysics. If you already have posterior draws and a proposal that covers them, [bridge sampling](/bridge-sampling/) is more accurate for the same work. The [Laplace approximation](/laplace-approximation/) is far cheaper when the posterior is close to normal. [Annealed importance sampling](/annealed-importance-sampling/) and [sequential Monte Carlo](/sequential-monte-carlo/) are alternatives that follow a path of tempered densities.

## Pitfalls

- **Correlated constrained draws.** If L7 runs a Markov chain from a live point for only a few steps, the new point is not an independent draw above $L_i^*$, the law $\mathrm{Beta}(N, 1)$ fails, and $\log Z$ is biased. Run the chain in L7 long enough to forget its start, and check the result by repeated runs or by comparing with a smaller $\varepsilon$ and a larger $N$.
- **Likelihood plateaus.** If $L$ is constant on a region of positive prior mass, the uniform law of Claim 2 fails, and L4 has ties. L5 then assigns wrong masses. Break the ties in L4 by a tiny random extra coordinate, or treat the plateau mass separately.
- **Linear-scale arithmetic.** Computing L6 as written underflows when $L_i^* \approx e^{-1000}$, and the sum is $0$. Keep $\log L$, $\log X$ and $\log Z$, and add with log-sum-exp.
- **Dropping the live points.** Stopping at L8 and returning without L9 loses the part of $Z$ under the live points. At the stop of L8 it is below $\varepsilon Z$, but with a loose $\varepsilon$ or a run cut short by an iteration limit it can be most of $Z$. Keep L9.
- **Dead points as an equal-weight sample.** The dead points are spread over the prior, not the posterior. Weighting them equally in L10 gives a sample from the wrong law. Use the weights $L_i^* w_i/Z$, or resample with them.
- **Too few live points for many modes.** With small $N$, a mode of small prior mass can lose all its live points early and is never found again. Increase $N$ until the estimate is stable.

## Implementations

## History

John Skilling presented nested sampling in 2004 and gave the full account in Bayesian Analysis in 2006. He took the idea of sorting the prior by likelihood from statistical physics, where the density of states plays the same role as $X$. Mukherjee, Parkinson and Liddle (2006) applied it to cosmological model selection with ellipsoidal sampling. Chopin and Robert (2010) gave the first formal analysis, with consistency and the rate of the error. MultiNest (2009) and PolyChord (2015) made the method practical for multimodal and higher-dimensional problems, and dynamic nested sampling (2019) changes the number of live points during the run.

## References
