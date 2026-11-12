---
tag: B2ANPG
kind: technique
slug: sequential-monte-carlo
name: Sequential Monte Carlo
aliases:
- sequential importance sampling
- SMC sampler
area: machine-learning/probabilistic-inference
level: advanced
summary: "Weighted particles move through a sequence of targets by importance sampling with any proposal, and are resampled when the ESS 1/sum w_i^2 drops below a threshold."
prereqs: [importance-sampling, resampling]
see_also: [particle-filter, filtering, state-space-model, annealed-importance-sampling, marginal-likelihood, effective-sample-size, likelihood-weighting, gibbs-sampling]
sources:
  - book: isbn:9780387951461
    title: "Arnaud Doucet, Nando de Freitas and Neil Gordon (editors), Sequential Monte Carlo Methods in Practice, Springer, 2001"
    locator: "Chapter 1 (an introduction to sequential Monte Carlo methods: sequential importance sampling, weight degeneracy and resampling)"
  - book: isbn:9780199532902
    title: "Arnaud Doucet and Adam M. Johansen, A tutorial on particle filtering and smoothing: fifteen years later, in Dan Crisan and Boris Rozovskii (editors), The Oxford Handbook of Nonlinear Filtering, Oxford University Press, 2011 (preprint 2009)"
    locator: the sections on sequential importance sampling, resampling, the effective sample size and the generic SMC algorithm
  - book: isbn:9780387202686
    title: "Pierre Del Moral, Feynman-Kac Formulae: Genealogical and Interacting Particle Systems with Applications, Springer, 2004"
    locator: the interacting particle interpretation of SMC, the unbiased normalizing constant estimate and the convergence results
  - paper: doi:10.1111/j.1467-9868.2006.00553.x
    title: "Pierre Del Moral, Arnaud Doucet and Ajay Jasra, Sequential Monte Carlo samplers, Journal of the Royal Statistical Society Series B 68(3), 2006, pages 411 to 436"
    locator: SMC samplers for a sequence of distributions on a fixed space, with MCMC moves and backward kernels
  - paper: doi:10.1080/01621459.1998.10473765
    title: "Jun S. Liu and Rong Chen, Sequential Monte Carlo methods for dynamic systems, Journal of the American Statistical Association 93(443), 1998, pages 1032 to 1044"
    locator: the general framework of sequential importance sampling with resampling only when the weights become uneven
  - book: isbn:9783030478445
    title: "Nicolas Chopin and Omiros Papaspiliopoulos, An Introduction to Sequential Monte Carlo, Springer, 2020"
    locator: "Chapter 8 (importance sampling and the effective sample size), Chapter 10 (particle filtering with general proposals), Chapter 17 (SMC samplers)"
---

Sequential Monte Carlo (SMC) is a family of methods that approximate a sequence of probability distributions $\pi_1, \pi_2, \ldots, \pi_T$ by a set of $N$ weighted samples, the particles, which are updated from one distribution to the next. Each update is an [importance sampling](/importance-sampling/) step: extend or move each particle with a proposal distribution and multiply its weight by an incremental weight. Without further steps this is sequential importance sampling (SIS), and its weights degenerate: after some steps one particle holds almost all the weight. SMC fixes this with [resampling](/resampling/), done when the effective sample size $\mathrm{ESS} = 1/\sum_i W_i^2$ falls under a threshold. As a by-product, SMC gives an unbiased estimate of the normalizing constant of each $\pi_t$. The [particle filter](/particle-filter/) is the case where $\pi_t$ is the posterior of a [state space model](/state-space-model/) and the proposal is the transition model; SMC samplers apply the same idea to a sequence of distributions on one fixed space.

## In plain words

You want to describe a moving target with a cloud of weighted points. At each step you move every point by a rule of your choice, and then adjust its weight by how much more or less likely the new point is under the new target than your rule made it. A good rule changes the weights only a little.

If you only move and reweight, after a while one point has almost all the weight and the rest are useless. So you watch a single number that says how many points still count. When it gets too small, you make a fresh cloud by copying heavy points and dropping light ones, all with equal weight. Then you go on.

## When it applies

The targets are $\pi_t(x_{0:t}) = \gamma_t(x_{0:t}) / Z_t$ for $t = 1, \ldots, T$, on spaces that grow with $t$, with $\pi_0 = \gamma_0$ a distribution that you can sample. You must be able to evaluate the unnormalized densities $\gamma_t$, or at least their ratios, but not the constants $Z_t$. For each $t$ you choose a proposal $q_t(x_t \mid x_{0:t-1})$ that you can sample and evaluate, with $q_t > 0$ wherever $\gamma_t > 0$. The incremental weight is

$$\alpha_t(x_{0:t}) = \frac{\gamma_t(x_{0:t})}{\gamma_{t-1}(x_{0:t-1})\, q_t(x_t \mid x_{0:t-1})}.$$

For a state space model with $\gamma_t(x_{0:t}) = p(x_{0:t}, y_{1:t})$ this is $\alpha_t = p(y_t \mid x_t)\, p(x_t \mid x_{t-1}) / q_t(x_t \mid x_{t-1})$, and $Z_t = p(y_{1:t})$. With the transition as the proposal, $\alpha_t = p(y_t \mid x_t)$, which is the bootstrap [particle filter](/particle-filter/).

The effective sample size of normalized weights $W_1, \ldots, W_N$ is $\mathrm{ESS} = 1/\sum_i W_i^2$. It is a heuristic for the number of equally weighted samples that the weighted set is worth. It is different from the [effective sample size](/effective-sample-size/) of an MCMC chain, which measures autocorrelation.

## The template

```pseudo id=main
SMC(N, T, threshold τ)
L1  draw x_0^i ~ π_0 for i = 1..N;  W^i ← 1/N;  log Ẑ ← 0
L2  for t ← 1 to T do
L3      ESS ← 1 / Σ_i (W^i)²
L4      if ESS < τ N then resample the particles by W (systematic);  W^i ← 1/N
L5      draw x_t^i ~ q_t(· | x_{0:t−1}^i) for each i                  ▷ extend each path
L6      compute α_t^i = α_t(x_{0:t}^i) for each i                    ▷ incremental weight
L7      log Ẑ ← log Ẑ + log Σ_i W^i α_t^i
L8      W^i ← W^i α_t^i / Σ_j W^j α_t^j;  report Σ_i W^i φ(x_{0:t}^i) as the estimate of π_t(φ)
L9  return the estimates and log Ẑ
```

The threshold $\tau \in [0, 1]$ sets the policy. With $\tau = 0$ the method never resamples and is plain SIS. With $\tau > 1$ it resamples at every step. A common choice is $\tau = 1/2$. Weights are kept as logarithms in code, and line L7 subtracts the largest log weight before exponentiating.

**Theorem (unbiased normalizing constant).** For every $N \ge 1$, every threshold, and every unbiased resampling scheme, $\mathbb E[\hat Z_T] = Z_T$, where $\hat Z_T = \prod_{t=1}^T \sum_i W^i_{t-1} \alpha^i_t$ uses the weights $W_{t-1}$ after the resampling decision of step $t$.

*Proof.* For a function $\varphi$ of the path, let $\gamma_t(\varphi) = \int \gamma_t \varphi$ and let $\gamma^N_t(\varphi) = \hat Z_t \sum_i W^i_t \varphi(x^i_{0:t})$ be its particle version, with $\hat Z_0 = 1$. We show $\mathbb E[\gamma^N_t(\varphi)] = \gamma_t(\varphi)$ by induction; $\varphi = 1$ gives the theorem. For $t = 0$ it holds because the particles are draws from $\pi_0 = \gamma_0$. Fix $t \ge 1$ and condition on the history $\mathcal F_{t-1}$ up to the end of step $t - 1$. The decision of line L4 is known given $\mathcal F_{t-1}$. Write $(\bar W^i, \bar x^i)$ for the particles after line L4. If the method resamples, unbiasedness of the scheme gives $\mathbb E[\sum_i \bar W^i \psi(\bar x^i) \mid \mathcal F_{t-1}] = \sum_i W^i_{t-1} \psi(x^i_{0:t-1})$ for every $\psi$; if not, this holds trivially. By line L8,
$$\gamma^N_t(\varphi) = \hat Z_{t-1} \Bigl(\sum_j \bar W^j \alpha^j_t\Bigr) \sum_i \frac{\bar W^i \alpha^i_t}{\sum_j \bar W^j \alpha^j_t} \varphi(x^i_{0:t}) = \hat Z_{t-1} \sum_i \bar W^i \alpha^i_t \varphi(x^i_{0:t}).$$
Each $x^i_t$ is drawn from $q_t(\cdot \mid \bar x^i)$, and $\int q_t\, \alpha_t\, \varphi \, dx_t = \int \frac{\gamma_t}{\gamma_{t-1}} \varphi\, dx_t =: K\varphi$. So $\mathbb E[\gamma^N_t(\varphi) \mid \mathcal F_{t-1}] = \hat Z_{t-1} \sum_i W^i_{t-1} K\varphi(x^i_{0:t-1}) = \gamma^N_{t-1}(K\varphi)$. By the induction hypothesis its mean is $\gamma_{t-1}(K\varphi) = \int \gamma_{t-1} \frac{\gamma_t}{\gamma_{t-1}} \varphi = \gamma_t(\varphi)$. $\blacksquare$

**Theorem (range of the ESS).** $1 \le \mathrm{ESS} \le N$, with $\mathrm{ESS} = N$ exactly when all weights are $1/N$ and $\mathrm{ESS} = 1$ exactly when one weight is $1$.

*Proof.* By the Cauchy-Schwarz inequality $1 = (\sum_i W_i)^2 \le N \sum_i W_i^2$, with equality only for equal weights. Since $0 \le W_i \le 1$, $\sum_i W_i^2 \le \sum_i W_i = 1$, with equality only when each $W_i$ is $0$ or $1$. $\blacksquare$

**Theorem (weight degeneracy of SIS).** Let the targets be products $\pi_t(x_{1:t}) = \prod_{s \le t} f(x_s)$ and the proposals $q_t = g$ for one density $g$ with $g > 0$ where $f > 0$. Let $w_t = \prod_{s \le t} f(x_s)/g(x_s)$ with $x_s$ independent draws from $g$. Then $\mathbb E[w_t] = 1$ and
$$\mathbb E[w_t^2] = \bigl(1 + \chi^2(f \,\|\, g)\bigr)^t, \qquad \chi^2(f \,\|\, g) = \int \frac{(f - g)^2}{g},$$
which grows exponentially in $t$ unless $g = f$.

*Proof.* The factors are independent, $\mathbb E[f(x)/g(x)] = \int f = 1$, and $\mathbb E[(f(x)/g(x))^2] = \int f^2/g = 1 + \int (f - g)^2/g$. Multiply over $s$. $\blacksquare$

For large $N$, $\mathrm{ESS}/N = (\sum_i w^i)^2 / (N \sum_i (w^i)^2) \approx \mathbb E[w_t]^2 / \mathbb E[w_t^2]$ by the [law of large numbers](/law-of-large-numbers/), so without resampling the ESS falls like $N (1 + \chi^2)^{-t}$. Resampling resets the weights to be equal, so in this example it brings the ESS back to $N$ and stops the exponential decay. Kong, Liu and Wong (1994) gave the general statement that the variance of the SIS weights tends to grow with $t$.

The cost of SMC is $O(TN)$ for the arithmetic with systematic resampling, plus $TN$ proposal draws and incremental weight evaluations. With full paths kept, the memory is $O(TN)$; for filtering, only the current states are needed, $O(N)$.

## Classic examples

**Weight degeneracy on a linear Gaussian model.** Take $x_0 \sim \mathcal N(0, 1)$, $x_t = 0.9 x_{t-1} + q_t$ with $q_t \sim \mathcal N(0, 0.5)$, $y_t = x_t + r_t$ with $r_t \sim \mathcal N(0, 1)$, and $T = 50$ observations simulated with Python's `random.Random(0)`. The [Kalman filter](/kalman-filter/) gives the exact $\log Z_T = \log p(y_{1:50}) = -96.96$. We ran SMC with $N = 100$ particles, 200 times from one `random.Random(1)` stream, with two proposals: the bootstrap proposal $q_t = p(x_t \mid x_{t-1})$, and the locally optimal proposal $q_t = p(x_t \mid x_{t-1}, y_t)$, which here is Gaussian with variance $(1/0.5 + 1/1)^{-1} = 1/3$ and gives the incremental weight $\alpha_t = \mathcal N(y_t;\, 0.9 x_{t-1},\, 1.5)$, which does not depend on $x_t$.

| proposal | resampling rule | resampling steps (mean) | ESS at the start of step 50 (first run) | mean of $\log(\hat Z / Z)$ | standard deviation |
|---|---|---|---|---|---|
| bootstrap | never (SIS) | 0 | 1.1 | -25.5 | 8.6 |
| optimal | never (SIS) | 0 | 2.2 | -2.03 | 1.49 |
| bootstrap | every step | 50 | 55.4 | -0.51 | 0.87 |
| bootstrap | ESS < N/2 | 21.0 | 33.3 | -0.36 | 0.95 |
| optimal | ESS < N/2 | 10.0 | 60.6 | -0.14 | 0.59 |

Without resampling, the bootstrap SIS run had an ESS of $1.1$ by step 20: one particle did all the work, and the log likelihood estimate was useless. The better proposal slows the decay but does not stop it. Resampling when the ESS is below $N/2$ uses less than half the resampling steps of the every-step rule with a similar error, and the optimal proposal with adaptive resampling is the best of the five. All five estimates $\hat Z$ are unbiased; the strongly negative means of $\log \hat Z$ show how skewed $\hat Z$ is when the weights degenerate.

**The bootstrap particle filter.** With $\pi_0 = p(x_0)$, $q_t = p(x_t \mid x_{t-1})$ and $\tau > 1$, SMC is the bootstrap filter of Gordon, Salmond and Smith (1993); the [particle filter](/particle-filter/) page has its code and analysis.

**Exact check on a small HMM.** On a two-state [hidden Markov model](/hidden-markov-model/) with a uniform proposal on the states and no resampling, enumerating all values of the random numbers on a grid fine enough to be exact gives a mean of $\hat Z$ equal to the [forward algorithm](/forward-algorithm/) value of $p(y_{1:T})$, as the theorem says.

**SMC samplers.** Del Moral, Doucet and Jasra (2006) apply SMC to a sequence of distributions $\pi_1, \ldots, \pi_T$ on one fixed space, for example tempered posteriors $\pi_t(\theta) \propto p(\theta)\, p(y \mid \theta)^{\beta_t}$ with $0 = \beta_0 < \beta_1 < \cdots < \beta_T = 1$. The particles are moved by an MCMC kernel that leaves $\pi_t$ invariant, such as [Gibbs sampling](/gibbs-sampling/) steps, and an auxiliary backward kernel makes the path-space weights computable. With this choice the incremental weight is $p(y \mid \theta)^{\beta_t - \beta_{t-1}}$, the same as in [annealed importance sampling](/annealed-importance-sampling/); SMC adds resampling between the temperatures. The final $\hat Z$ estimates the [marginal likelihood](/marginal-likelihood/) $p(y)$.

## Variations

- **Resampling scheme.** Multinomial, residual, stratified or systematic [resampling](/resampling/) all keep the estimate of $Z_T$ unbiased; the last three add less noise.
- **Auxiliary particle filter.** Resample with weights that already include a prediction of the next incremental weight, then correct (Pitt and Shephard 1999).
- **Resample-move.** After resampling, apply an MCMC move that leaves $\pi_t$ invariant to each particle, to restore diversity (Gilks and Berzuini 2001).
- **Adaptive tempering.** In SMC samplers, choose the next temperature $\beta_t$ so that the ESS after reweighting equals a target value, such as $N/2$.
- **Conditional SMC and particle MCMC.** Keep one path fixed and run SMC around it; this gives MCMC kernels on paths and, with the unbiased $\hat Z$, exact MCMC for static parameters (Andrieu, Doucet and Holenstein 2010).
- **Twisted and guided proposals.** Change the targets or proposals to look ahead at future data, which lowers the variance of $\hat Z$.

## Pitfalls

- **Wrong incremental weight.** The weight must divide by the proposal density actually used. With the transition as the proposal the transition terms cancel; with any other proposal they do not.
- **Proposal with thin tails.** If $q_t$ has lighter tails than $\gamma_t / \gamma_{t-1}$, the weights have infinite variance and the estimates can be wild while the ESS looks fine.
- **The ESS is only a heuristic.** A high ESS means the weights are even, not that the particles cover the target. All particles can sit in one mode and still have equal weights.
- **Resampling too often or too rarely.** Every resampling step adds noise; never resampling lets the weights degenerate. The threshold $N/2$ is a common compromise.
- **Path degeneracy.** Repeated resampling makes the stored paths $x^i_{0:t}$ share ancestors, so estimates of functions of early states are poor, even when the filter estimates of $x_t$ are good.
- **Reporting $\log \hat Z$ as unbiased.** Only $\hat Z$ is unbiased; $\mathbb E[\log \hat Z] \le \log Z$ by [Jensen's inequality](/jensens-inequality/).
- **Underflow.** Products of many likelihoods underflow. Keep log weights and use the log-sum-exp form in line L7.

## Exercises

1. Show that with $\tau > 1$, $\pi_0 = p(x_0)$ and $q_t = p(x_t \mid x_{t-1})$, the estimate $\hat Z_T$ of the template equals the estimate of the bootstrap [particle filter](/particle-filter/).
2. For the locally optimal proposal $q_t = p(x_t \mid x_{t-1}, y_t)$, show that $\alpha_t = p(y_t \mid x_{t-1})$, and that it does not depend on the new state $x_t$.
3. Compute $\chi^2(f \,\|\, g)$ for $f = \mathcal N(0, 1)$ and $g = \mathcal N(0, \sigma^2)$, and show that it is infinite for $\sigma^2 \le 1/2$.
4. Show that the ESS is invariant under scaling all unnormalized weights by the same constant, and that $N / \mathrm{ESS} - 1$ is the squared coefficient of variation of the weights, computed with divisor $N$.
5. In the SMC sampler with tempering, show that the incremental weight for an MCMC move with the time-reversal backward kernel is $\gamma_t(\theta)/\gamma_{t-1}(\theta)$, evaluated at the particle before the move.

## References
