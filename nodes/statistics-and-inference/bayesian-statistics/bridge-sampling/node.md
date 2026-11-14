---
tag: TC3WDX
kind: algorithm
slug: bridge-sampling
name: Bridge sampling
aliases:
- Meng-Wong bridge sampling
area: statistics-and-inference/bayesian-statistics
level: advanced
summary: Estimates a ratio of normalizing constants, such as a marginal likelihood, from draws of two distributions linked by a bridge function. The optimal bridge is found iteratively.
model: real-ram
complexity:
  vars: {n: "the total number of draws, n1 + n2", T: the number of iterations}
  time: {worst: Θ(n T)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1996
  people: [Xiao-Li Meng, Wing Hung Wong, Charles H. Bennett]
  note: Bennett (1976) found the optimal acceptance ratio estimator of free energy differences in physics. Meng and Wong (1996) gave the general bridge identity, the optimal bridge with a proof, and the iterative scheme. Gelman and Meng (1998) linked it to importance sampling and path sampling.
prereqs: [importance-sampling, marginal-likelihood, monte-carlo-integration, bayes-factor]
see_also: [laplace-approximation, nested-sampling, annealed-importance-sampling, savage-dickey-density-ratio, effective-sample-size, metropolis-hastings, parallel-tempering, delta-method]
sources:
  - paper: "Xiao-Li Meng and Wing Hung Wong, Simulating ratios of normalizing constants via a simple identity: a theoretical exploration, Statistica Sinica 6(4), 1996"
    title: Meng and Wong 1996
    locator: "pages 831 to 860: Section 2 (identity (2.3) and condition (2.1); importance sampling as alpha = 1/q2 and the generalized harmonic mean as special cases), Section 3 (relative mean squared error (3.1), its first-order form (3.2), Theorem 1 with the optimal bridge and its proof by Cauchy-Schwarz), Section 4 (the iterative scheme (4.1) and Theorem 2 on its convergence)"
  - paper: doi:10.1016/0021-9991(76)90078-4
    title: "Charles H. Bennett, Efficient estimation of free energy differences from Monte Carlo data, Journal of Computational Physics 22(2), 1976"
    locator: pages 245 to 268 (the acceptance ratio method and its optimal weighting function; general locator)
  - paper: doi:10.1214/ss/1028905934
    title: "Andrew Gelman and Xiao-Li Meng, Simulating normalizing constants: from importance sampling to bridge sampling to path sampling, Statistical Science 13(2), 1998"
    locator: pages 163 to 185 (bridge sampling between importance sampling and path sampling; general locator)
  - paper: doi:10.1016/j.jmp.2017.09.005
    title: "Quentin F. Gronau, Alexandra Sarafoglou, Dora Matzke and others, A tutorial on bridge sampling, Journal of Mathematical Psychology 81, 2017"
    locator: pages 80 to 97 (the beta-binomial running example, the normal proposal, splitting the posterior draws, the effective sample size in place of n1; general locator)
  - paper: doi:10.1198/106186002457
    title: "Xiao-Li Meng and Stephen Schilling, Warp bridge sampling, Journal of Computational and Graphical Statistics 11(3), 2002"
    locator: pages 552 to 586 (transforming the draws so that the two densities overlap more; general locator)
  - paper: doi:10.1111/j.2517-6161.1994.tb01956.x
    title: "Michael A. Newton and Adrian E. Raftery, Approximate Bayesian inference with the weighted likelihood bootstrap, Journal of the Royal Statistical Society Series B 56(1), 1994"
    locator: pages 3 to 48 with the discussion (the harmonic mean estimator of the marginal likelihood and its instability; general locator)
---

Bridge sampling estimates a ratio $r = c_1/c_2$ of two normalizing constants from draws of the two distributions. Its main use in Bayesian statistics is the [marginal likelihood](/marginal-likelihood/) $Z = \int f(x \mid \theta)\pi(\theta)\, d\theta$: take the posterior as the first distribution, with $q_1 = f(x \mid \theta)\pi(\theta)$ and $c_1 = Z$, and a normalized proposal density $g$ as the second, with $c_2 = 1$. The method rests on the identity $r = \mathbb{E}_2[q_1\alpha]/\mathbb{E}_1[q_2\alpha]$, true for every bridge function $\alpha$. [Importance sampling](/importance-sampling/) is the case $\alpha = 1/q_2$, and the harmonic mean estimator is the case $\alpha = 1/q_1$ with the prior as $g$. The bridge that minimizes the first-order error is $\alpha \propto 1/(s_1 q_1 + s_2 r q_2)$; it depends on $r$, so it is found by a fixed-point iteration that converges geometrically from any start.

## In plain words

To find the size of a hidden region, you can sample points from the region itself, or from a second region whose size you know, or from both. Importance sampling uses only the known region, and it fails when that region misses part of the hidden one. The harmonic mean trick uses only the hidden region, and it fails because a few rare points dominate the answer. Bridge sampling uses both samples and weighs each point by how well it sits in the overlap of the two regions. The best weights depend on the answer, so the method guesses, reweighs, and repeats. Each round moves the guess closer to one fixed value. With a second region that overlaps the first well, the answer is accurate to a few hundredths of a unit on the log scale from a few thousand points.

## The problem

**Input.** Two unnormalized densities $q_1, q_2 \ge 0$ that can be evaluated, with unknown constants $c_k = \int q_k > 0$ and normalized densities $p_k = q_k/c_k$. Draws $\theta_1, \ldots, \theta_{n_1}$ from $p_1$ and $\phi_1, \ldots, \phi_{n_2}$ from $p_2$, for example posterior draws from [Metropolis-Hastings](/metropolis-hastings/) and independent draws from a normal proposal.

**Output.** An estimate of $\log r = \log(c_1/c_2)$. For a marginal likelihood, $\log r = \log Z$; for two models, the difference of two such estimates is the log [Bayes factor](/bayes-factor/).

**The bridge identity.** For every $\alpha \ge 0$ with $0 < \int \alpha q_1 q_2 < \infty$,

$$r = \frac{c_1}{c_2} = \frac{\mathbb{E}_2[q_1(\phi)\alpha(\phi)]}{\mathbb{E}_1[q_2(\theta)\alpha(\theta)]},$$

because both expectations are integrals of $\alpha q_1 q_2$, divided by $c_2$ and $c_1$. Replacing the two expectations by sample means gives the estimate $\hat r_\alpha$.

## The algorithm

Write $l = q_1/q_2$, $l_{1i} = l(\theta_i)$, $l_{2j} = l(\phi_j)$, $n = n_1 + n_2$ and $s_k = n_k/n$. With the optimal bridge $\alpha = 1/(s_1 q_1 + s_2 r q_2)$, the factor $q_2$ cancels, and the estimate becomes the fixed point of the map on line L8.

```pseudo id=main
BRIDGE(θ₁..θ_{n₁} ~ p₁, φ₁..φ_{n₂} ~ p₂, q₁, q₂)
L1  s₁ ← n₁/(n₁ + n₂);  s₂ ← n₂/(n₁ + n₂)
L2  l₁ᵢ ← q₁(θᵢ)/q₂(θᵢ)  for i = 1..n₁              ▷ kept as logarithms
L3  l₂ⱼ ← q₁(φⱼ)/q₂(φⱼ)  for j = 1..n₂
L4  r ← (1/n₂) Σⱼ l₂ⱼ                                ▷ start: importance sampling
L5  repeat
L6      N ← (1/n₂) Σⱼ l₂ⱼ / (s₁ l₂ⱼ + s₂ r)
L7      D ← (1/n₁) Σᵢ 1 / (s₁ l₁ᵢ + s₂ r)
L8      r_new ← N / D
L9      if |log r_new - log r| ≤ tol then return log r_new
L10     r ← r_new
```

Lines L2 and L3 evaluate both densities at both samples, $2n$ density evaluations, which is usually the main cost. The ratios $l$ can be $e^{-500}$ or $e^{500}$, so the code keeps $\log l$ and computes L6 and L7 with log-sum-exp; the formulas above are the same in exact arithmetic. L4 is any positive start; the [importance sampling](/importance-sampling/) estimate is a good one. L6 and L7 are the two sample means of the bridge identity with $\alpha = 1/(s_1 q_1 + s_2 r q_2)$, after dividing by $q_2$. L9 stops when the log estimate moves by less than the tolerance.

**Choosing $p_2$ for a marginal likelihood.** A common choice, following Gronau et al. (2017), is a normal density whose mean and covariance match the posterior draws, in a scale where every parameter is unconstrained, with the Jacobian included in $q_1$. The mode and the inverse Hessian of the [Laplace approximation](/laplace-approximation/) also work. The proposal should be fitted on a different part of the posterior draws from the part used in L2.

## Example

**Trace.** Bernoulli data with $3$ successes in $10$ trials and the prior Beta(2, 2), in the logit scale $\theta = \log(p/(1-p))$: $q_1(\theta) = p^5(1 - p)^9/B(2, 2)$, with the Jacobian $p(1-p)$ included. The exact value is $\log Z = \log B(5, 9) - \log B(2, 2) = -6.977748$. For $p_2$ we take the Laplace normal $N(-0.587787, 0.557773^2)$ of the [Laplace approximation](/laplace-approximation/) page. With `random.Random(5)`, $n_1 = n_2 = 8$: the $\theta_i$ are logits of exact Beta(5, 9) draws, and the $\phi_j$ are normal draws.

| $i$ or $j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $\theta_i$ | $-0.7495$ | 0.6122 | $-0.6716$ | $-1.1907$ | 1.1076 | $-0.8125$ | $-0.2063$ | $-0.1818$ |
| $\log l_{1i}$ | $-6.9970$ | $-7.1332$ | $-6.9976$ | $-6.9586$ | $-7.2182$ | $-6.9958$ | $-7.0050$ | $-7.0064$ |
| $\phi_j$ | $-0.4630$ | $-0.4255$ | $-0.8283$ | 0.1314 | 0.2517 | $-0.5699$ | $-0.8398$ | $-0.1788$ |
| $\log l_{2j}$ | $-6.9980$ | $-6.9983$ | $-6.9954$ | $-7.0389$ | $-7.0585$ | $-6.9977$ | $-6.9951$ | $-7.0066$ |

All ratios are close to $e^{-7}$, because the Laplace normal is close to the posterior. The iteration, with $s_1 = s_2 = 1/2$:

| step | $N$ (L6) | $D$ (L7) | $\log r$ (L8) |
|---|---|---|---|
| start (L4) | | | $-7.010809$ |
| 1 | 0.999875 | 1124.111842 | $-7.024874$ |
| 2 | 1.006906 | 1132.142279 | $-7.024984$ |
| 3 | 1.006962 | 1132.205476 | $-7.024985$ |
| 4 to 6 | 1.006962 | 1132.205977 | $-7.024985$ |

The test of L9 with tolerance $10^{-12}$ stops at step 6. The estimate $-7.024985$ is off by $0.047$ nats from 16 draws. Bisection on the estimating equation of the proof gives the same root, $-7.024985$.

**Four estimators of the same $\log Z$.** Same model, $200$ repetitions with `random.Random(2024)`, $2000$ draws per estimate: the bridges use $1000$ posterior and $1000$ proposal draws, importance sampling uses $2000$ proposal draws, and the harmonic mean uses $2000$ posterior draws.

| estimator | bridge function | mean error (nats) | standard deviation | largest error |
|---|---|---|---|---|
| importance sampling | $1/q_2$ | $-0.0001$ | 0.0035 | 0.018 |
| harmonic mean | $1/q_1$, prior as $p_2$ | 0.0542 | 0.1271 | 0.518 |
| geometric bridge | $1/\sqrt{q_1 q_2}$ | 0.0002 | 0.0026 | 0.008 |
| optimal bridge | L1 to L10 | 0.0002 | 0.0026 | 0.008 |

Here the proposal is good, so importance sampling also works, and the bridges reduce its spread by a quarter. The harmonic mean has infinite variance in this model: $\mathbb{E}_{\mathrm{post}}[1/f(x \mid p)^2] \propto \int p^{-2}(1 - p)^{-6} dp = \infty$.

**The harmonic mean does not improve with more draws.** Take $x_i \sim N(\theta, 1)$ for $i = 1, \ldots, 20$ and the prior $\theta \sim N(0, 10^2)$, with data from `random.Random(1)`; the exact value is $\log Z = -31.327583$. The bridge uses a proposal $N(m, 2v)$, where $N(m, v)$ is the exact posterior. Twenty repetitions per row:

| draws $S$ per sample | harmonic mean, mean error | its standard deviation | optimal bridge, mean error | its standard deviation |
|---|---|---|---|---|
| 100 | 2.910 | 0.290 | 0.0009 | 0.0349 |
| 1000 | 2.621 | 0.326 | $-0.0007$ | 0.0090 |
| 10000 | 2.479 | 0.484 | 0.0000 | 0.0028 |
| 100000 | 2.389 | 0.258 | | |

The bridge error falls like $1/\sqrt S$. The harmonic mean overestimates $\log Z$ by more than two nats even with $10^5$ draws. In the normal-normal model with noise variance $\sigma^2$ and prior variance $\tau^2$, $\mathbb{E}_{\mathrm{post}}[1/f(x \mid \theta)^2]$ is finite only when $n\tau^2 < \sigma^2$, that is, when the prior is narrower than the noise of one mean. Here $n\tau^2 = 2000$ and $\sigma^2 = 1$. The posterior rarely visits the region where the likelihood is small, and that region carries most of $\mathbb{E}_{\mathrm{post}}[1/f]$. There is no page for the harmonic mean estimator, because it should not be used.

## Correctness

The full proof is in proofs/correctness.md. It proves:

1. **The identity** $r = \mathbb{E}_2[q_1\alpha]/\mathbb{E}_1[q_2\alpha]$ for every bridge function with $0 < \int\alpha q_1 q_2 < \infty$, and the consistency of $\hat r_\alpha$ for a fixed $\alpha$ by the [law of large numbers](/law-of-large-numbers/).
2. **Special cases.** $\alpha = 1/q_2$ gives importance sampling (support of $p_1$ inside that of $p_2$); $\alpha = 1/q_1$ gives reciprocal importance sampling, and with the prior as $p_2$ the harmonic mean identity $Z = 1/\mathbb{E}_{\mathrm{post}}[1/f(x \mid \theta)]$.
3. **The optimal bridge, under an approximation.** If all draws are independent, the first-order [delta method](/delta-method/) gives $\mathrm{RE}^2(\hat r_\alpha) \approx \frac{1}{n s_1 s_2}\big(\int p_1 p_2 (s_1 p_1 + s_2 p_2)\alpha^2 / (\int p_1 p_2\alpha)^2 - 1\big)$ (Meng and Wong 1996, equation (3.2)). By the Cauchy-Schwarz inequality this is minimized by $\alpha \propto 1/(s_1 p_1 + s_2 p_2)$, with minimum $\frac{1}{n s_1 s_2}\big((\int p_1 p_2/(s_1 p_1 + s_2 p_2))^{-1} - 1\big)$. The minimum is always finite, even when importance sampling and the harmonic mean have infinite variance.
4. **The iteration.** The fixed points of L8 are the roots of $\Psi(\rho) = \frac{1}{n_1}\sum_i \frac{\rho}{s_1 l_{1i} + s_2\rho} - \frac{1}{n_2}\sum_j \frac{l_{2j}}{s_1 l_{2j} + s_2\rho}$, which is strictly increasing from $-1/s_1$ to $1/s_2$, so there is exactly one. The map sends $(0, \infty)$ into a compact interval, and in the log scale its derivative lies in $(-1, 1)$, so it is a contraction there and converges geometrically from any start.
5. **Consistency of the root.** With independent draws and fixed $s_1, s_2$, the root converges to $r$ almost surely, because the sample estimating function converges to $(\rho/c_1 - 1/c_2)$ times a positive integral.

What is proved and what is only approximate: items 1, 2, 4 and 5 are exact statements. Item 3 is exact for the first-order formula, which is itself an approximation of the true relative error; for draws from a Markov chain, the formula holds with effective sample sizes in place of $n_1$ and $n_2$ only approximately. The errors in the tables are measured.

## Complexity

Lines L2 and L3 evaluate $q_1$ and $q_2$ at all $n$ draws: $2n$ density evaluations. Each pass of L6 and L7 costs $\Theta(n)$ arithmetic, so $T$ iterations cost $\Theta(nT)$. The proof shows that the error in $\log r$ shrinks by a factor $\kappa < 1$ per step, so $T = O(\log(1/\mathrm{tol}))$; in the examples $T$ is $5$ to $8$ for a tolerance of $10^{-12}$. The ratios take $\Theta(n)$ extra space. For a marginal likelihood, the posterior draws come from an MCMC run that usually costs far more than the bridge step.

## Properties

- **Deterministic given the draws.** All randomness is in the two samples.
- **Not exact.** It is a Monte Carlo estimate. Like every ratio estimate, $\hat r$ has a bias of order $1/n$; $\log\hat r$ has a bias of the same order.
- **Symmetric in the two distributions.** Swapping $p_1$ and $p_2$ gives $1/\hat r$ for the optimal bridge, which is not true of importance sampling.
- **Robust to tails.** The optimal bridge never has infinite first-order variance, because $\alpha q_1 q_2 \le q_1 q_2/(s_1 q_1)$ and $\le q_1 q_2/(s_2 r q_2)$.
- **Needs overlap.** The relative error is governed by $\int p_1 p_2/(s_1 p_1 + s_2 p_2)$, a measure of how much the two densities overlap. When they barely overlap, the error is large for every bridge.

## Variants and improvements

- **Geometric bridge.** $\alpha = 1/\sqrt{q_1 q_2}$ needs no iteration. In the table it is as good as the optimal one, because the proposal is good.
- **Warp bridge sampling.** Meng and Schilling (2002) transform the draws, by centring, scaling and symmetrizing, so that the two densities overlap more before the bridge is applied.
- **Path sampling.** Use a chain of bridges between $p_1$ and $p_2$, or a continuous path of densities; this is the [annealed importance sampling](/annealed-importance-sampling/) and thermodynamic integration family (Gelman and Meng 1998).
- **MCMC draws.** Replace $n_1$ in $s_1$ and $s_2$ by the [effective sample size](/effective-sample-size/) of the posterior draws (Gronau et al. 2017). The estimate stays consistent; the weights are closer to optimal.
- **Error estimates.** Plug the draws into the first-order formula of the Correctness section to estimate the relative error, or repeat the whole run several times.
- **Bayes factors directly.** With $q_1$ and $q_2$ the unnormalized posteriors of two models on the same parameter space, the bridge estimates the [Bayes factor](/bayes-factor/) without a proposal. For nested models, the [Savage-Dickey density ratio](/savage-dickey-density-ratio/) is often simpler.

## When to use it

Use bridge sampling for the marginal likelihood when you already have posterior draws, the parameter space is continuous and of moderate dimension, and you can fit a proposal that covers the posterior. It is more accurate than importance sampling from the same proposal and never has its failure mode of infinite variance. The [Laplace approximation](/laplace-approximation/) is cheaper but has an $O(1/n)$ bias. [Nested sampling](/nested-sampling/) needs no posterior draws but needs a sampler under a likelihood constraint. For multimodal posteriors, or when no proposal overlaps the posterior well, use path sampling, [parallel tempering](/parallel-tempering/) or sequential Monte Carlo. Never use the harmonic mean.

## Pitfalls

- **The harmonic mean.** Replacing L5 to L10 by the bridge $\alpha = 1/q_1$ with the prior as $p_2$ gives an exact identity, but its variance is infinite in most models, as the second table shows. Keep L5 to L10 and use a proposal fitted to the posterior.
- **Fitting the proposal on the same draws.** If the draws in L2 were also used to fit $p_2$, the two are dependent and the estimate is biased. Fit $p_2$ on one half of the posterior draws and use the other half in L2.
- **A missing Jacobian.** If $p_2$ is a normal on $\log\sigma$ or on a logit, then $q_1$ in L2 and L3 must be the posterior density in that scale, Jacobian included. Otherwise L8 converges to the integral of a different function.
- **Overflow.** $l$ is often $e^{-1000}$ or smaller. Computing L6 and L7 in floating point gives $0/0$. Keep $\log l$ and use log-sum-exp, as the implementation does.
- **Correlated draws counted as independent.** With MCMC draws, $s_1 = n_1/n$ in L1 overweights the posterior sample. Use the effective sample size in L1.
- **Poor overlap.** A proposal that is too narrow leaves posterior draws with tiny $l_{2j}$ and huge $l_{1i}$; the error grows quickly. Check the overlap, for example with a heavier-tailed Student $t$ proposal or by warping.

## Implementations

## History

Bennett (1976) found the acceptance ratio method for the difference of free energies of two physical systems, with the weighting that is optimal to first order. Meng and Wong (1996) brought the idea into statistics as bridge sampling, proved the identity for general bridges, derived the optimal bridge by the Cauchy-Schwarz inequality, and gave the iterative scheme with a convergence theorem. Gelman and Meng (1998) placed it between importance sampling and path sampling. Meng and Schilling (2002) added warping. The harmonic mean estimator of Newton and Raftery (1994) was criticized in the discussion of that paper for its instability, and its infinite variance in common models is a standard warning. Gronau and coauthors (2017) wrote a tutorial and the R package bridgesampling, which made the method a routine tool for Bayes factors.

## References
