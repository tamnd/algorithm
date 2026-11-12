---
tag: FENG7P
kind: algorithm
slug: particle-filter
name: Particle filter
aliases:
- bootstrap filter
- bootstrap particle filter
- sequential importance resampling filter
area: machine-learning/probabilistic-inference
level: advanced
summary: "Bootstrap filter: N particles are resampled, moved by the dynamics and weighted by the likelihood. For bounded test functions the error at step t is at most c_t/sqrt(N); c_t can grow with t."
solves: [filtering]
model: real-ram
complexity:
  vars: {N: the number of particles, T: the number of time steps}
  time: {worst: O(T N log N)}
  space: {extra: O(N)}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 1993
  people: [Neil J. Gordon, David J. Salmond, Adrian F. M. Smith]
  note: Gordon, Salmond and Smith published the bootstrap filter for nonlinear and non-Gaussian tracking in IEE Proceedings F, the first practical particle filter with resampling.
prereqs: [filtering, state-space-model, importance-sampling, resampling]
see_also: [sequential-monte-carlo, extended-kalman-filter, unscented-kalman-filter, kalman-filter, forward-algorithm, likelihood-weighting, smoothing, marginal-likelihood]
sources:
  - paper: doi:10.1049/ip-f-2.1993.0015
    title: "Neil J. Gordon, David J. Salmond and Adrian F. M. Smith, Novel approach to nonlinear/non-Gaussian Bayesian state estimation, IEE Proceedings F 140(2), 1993, pages 107 to 113"
    locator: the bootstrap filter (prediction by sampling the dynamics, weighting by the likelihood, resampling) and its comparison with the extended Kalman filter
  - paper: doi:10.1080/10618600.1996.10474692
    title: "Genshiro Kitagawa, Monte Carlo filter and smoother for non-Gaussian nonlinear state space models, Journal of Computational and Graphical Statistics 5(1), 1996, pages 1 to 25"
    locator: the Monte Carlo filter, found independently, and the particle smoother
  - book: isbn:9780387202686
    title: "Pierre Del Moral, Feynman-Kac Formulae: Genealogical and Interacting Particle Systems with Applications, Springer, 2004"
    locator: the unbiasedness of the particle estimate of the normalizing constant, and the convergence and stability of particle approximations
  - paper: doi:10.1109/78.984773
    title: "Dan Crisan and Arnaud Doucet, A survey of convergence results on particle filtering methods for practitioners, IEEE Transactions on Signal Processing 50(3), 2002, pages 736 to 746"
    locator: the mean squared error bound of order 1/N for bounded test functions
  - book: isbn:9783030478445
    title: "Nicolas Chopin and Omiros Papaspiliopoulos, An Introduction to Sequential Monte Carlo, Springer, 2020"
    locator: "Chapter 10 (particle filtering, the bootstrap filter and the likelihood estimate), Chapter 11 (convergence and stability)"
---

The particle filter, in its first and simplest form the bootstrap filter of Gordon, Salmond and Smith (1993), is a Monte Carlo solver for the [filtering](/filtering/) problem in a general [state space model](/state-space-model/). It represents the filtering distribution $p(x_t \mid y_{1:t})$ by $N$ samples, the particles, with weights. At each step it [resamples](/resampling/) the particles by their weights, moves each one by sampling the transition model, and gives each a new weight equal to the likelihood of the new observation. It needs only to sample the dynamics and to evaluate the likelihood, so it works for any nonlinear or non-Gaussian model. Its estimates converge to the exact filter at the rate $1/\sqrt N$, and the product of the mean weights is an unbiased estimate of the likelihood $p(y_{1:T})$. The general framework with other proposals and adaptive resampling is [sequential Monte Carlo](/sequential-monte-carlo/).

## In plain words

You want to follow a hidden object, such as a ship that you see only through noisy radar returns. Instead of one best guess, keep a crowd of guesses. At each tick, move every guess the way a ship could move, with some random wobble. Then compare each guess with the new radar return and give it a score: high if the guess explains the return well, low if not.

Before the next tick, make a new crowd of the same size by copying guesses in proportion to their scores. Good guesses get several copies, bad ones die out. The crowd then gathers where the ship probably is, and it can split into two groups when the data cannot tell two places apart. With more guesses the crowd gives a more accurate picture.

## The problem

The model is $x_0 \sim p(x_0)$, $x_t \sim p(x_t \mid x_{t-1})$ and $y_t \sim p(y_t \mid x_t)$ for $t = 1, \ldots, T$. The state space and the distributions are arbitrary. The algorithm needs only a sampler for $p(x_0)$, a sampler for $p(x_t \mid x_{t-1})$, and the value of the likelihood $g_t(x) = p(y_t \mid x_t = x)$ up to a constant. The output, for each $t$, is a weighted sample $\{(x^i_t, W^i_t)\}_{i=1}^N$ whose weighted averages estimate $\mathbb E[\varphi(x_t) \mid y_{1:t}]$, and an estimate $\hat Z_T$ of the likelihood $p(y_{1:T})$.

## The algorithm

```pseudo id=main
BOOTSTRAP-FILTER(N, y_1..y_T)
L1  draw x^i ~ p(x_0) for i = 1..N;  W^i ← 1/N;  log Ẑ ← 0
L2  for t ← 1 to T do
L3      if t > 1 then draw ancestors a_1..a_N i.i.d. with P(a = i) = W^i;  x^i ← x^{a_i}
L4      draw x^i ~ p(x_t | x_{t−1} = x^i) for each i                 ▷ propagate
L5      w̃^i ← p(y_t | x_t = x^i) for each i                          ▷ weight by the likelihood
L6      log Ẑ ← log Ẑ + log((1/N) Σ_i w̃^i)
L7      W^i ← w̃^i / Σ_j w̃^j;  report Σ_i W^i φ(x^i) as the estimate of E[φ(x_t) | y_1..y_t]
L8  return the estimates and log Ẑ
```

Line L3 is multinomial [resampling](/resampling/): $N$ independent draws by weight. Lines L3 and L4 together draw each new particle from the mixture $\sum_i W^i p(x_t \mid x^i_{t-1})$, which is the particle approximation of the predictive distribution $p(x_t \mid y_{1:t-1})$. Line L5 is the [Bayes](/bayes-theorem/) update of the [filtering](/filtering/) recursion, done by [importance sampling](/importance-sampling/) with the prediction as the proposal. In code the weights are kept as logarithms, and the largest log weight is subtracted before exponentiating.

The name bootstrap refers to the proposal: new states are drawn from the transition model itself, ignoring $y_t$. Other proposals, which look at $y_t$, need a different weight; they belong to the general [sequential Monte Carlo](/sequential-monte-carlo/) framework.

## Example

**A two-state trace.** Take a hidden Markov model with states $0$ and $1$: $P(x_0 = 1) = 1/4$, the state stays the same with probability $3/4$, and $p(y_t \mid x_t)$ is $3/4$ if $y_t = x_t$ and $1/4$ otherwise. The observations are $y = (1, 0)$. With $N = 4$ and Python's `random.Random(3)`:

| step | particles | likelihoods $\tilde w$ | mean $\tilde w$ | estimate of $P(x_t = 1 \mid y_{1:t})$ |
|---|---|---|---|---|
| draw $x_0$ | 1, 0, 0, 0 | | | |
| $t = 1$, propagate | 1, 0, 0, 1 | 3/4, 1/4, 1/4, 3/4 | 1/2 | 3/4 |
| $t = 2$, resample | 1, 1, 1, 0 (ancestors 1, 1, 4, 2) | | | |
| $t = 2$, propagate | 0, 1, 1, 0 | 3/4, 1/4, 1/4, 3/4 | 1/2 | 1/2 |

The likelihood estimate is $\hat Z = \frac12 \cdot \frac12 = \frac14$. The exact values, from the [forward algorithm](/forward-algorithm/), are $p(y_{1:2}) = 13/64 \approx 0.203$, $P(x_1 = 1 \mid y_1) = 9/14 \approx 0.643$ and $P(x_2 = 1 \mid y_{1:2}) = 4/13 \approx 0.308$. Four particles give a rough answer. The estimate $\hat Z$ is still right on average: with $N = 2$ the filter uses eight uniform numbers, and each of them only matters through which quarter of $[0, 1)$ it falls in, so the $4^8$ equally likely cases give its exact law. The mean of $\hat Z$ over these cases is exactly $13/64$.

**Convergence on a linear Gaussian model.** Take $x_0 \sim \mathcal N(0, 1)$, $x_t = 0.9 x_{t-1} + q_t$ with $q_t \sim \mathcal N(0, 0.5)$, $y_t = x_t + r_t$ with $r_t \sim \mathcal N(0, 1)$, and $y = (0.8, 1.5, -0.3, 0.4, 1.1)$. The [Kalman filter](/kalman-filter/) gives the exact filtered means $0.454, 0.943, 0.306, 0.334, 0.675$ and $\log p(y_{1:5}) = -7.266$. The largest error of the particle means over the five steps, averaged over seeds 0 to 9:

| $N$ | 10 | 100 | 1000 | 10000 |
|---|---|---|---|---|
| mean of the largest error | 0.353 | 0.116 | 0.035 | 0.012 |

Each tenfold increase in $N$ cuts the error by about $\sqrt{10} \approx 3.2$. Over 2000 runs (one `random.Random(7)` stream), the mean of $\hat Z / Z$ was $1.007 \pm 0.015$ for $N = 5$, $0.995 \pm 0.007$ for $N = 20$ and $0.999 \pm 0.003$ for $N = 100$ (one standard error), as unbiasedness predicts. The mean of $\log(\hat Z / Z)$ was $-0.233$, $-0.058$ and $-0.012$: the log estimate is biased down, by about half its variance.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). It shows two results.

- **Unbiased likelihood** (Del Moral 2004). $\mathbb E[\hat Z_T] = p(y_{1:T})$ exactly, for every $N \ge 1$. The proof goes by induction on $t$: given the past, resampling and propagation draw each new particle from the particle predictive distribution, so the expected value of the product of mean weights carries over from one step to the next. By [Jensen's inequality](/jensens-inequality/) $\log \hat Z_T$ is biased down.
- **Convergence.** For each bounded test function $\varphi$ and each $t$, the root mean squared error of the estimate in line L7 is at most $c_t \|\varphi\|_\infty / \sqrt N$, where $c_t$ depends on the model and the data but not on $N$. The proof bounds the three sources of error at each step: resampling, propagation and the ratio of the update.

The estimate of $\mathbb E[\varphi(x_t) \mid y_{1:t}]$ itself is biased for finite $N$, because it is a ratio; the bias is $O(1/N)$.

## Complexity

Each step draws $N$ transitions and evaluates $N$ likelihoods. Multinomial resampling with a [binary search](/binary-search/) over the cumulative weights costs $O(N \log N)$; systematic or stratified resampling costs $O(N)$. The total time is $O(T N \log N)$, or $O(TN)$ with the faster schemes, plus $TN$ draws from the dynamics and $TN$ likelihood evaluations. The filter keeps only the current particles and weights: $O(N)$ memory, times the size of a state.

The cost to reach a given accuracy can grow very fast with the dimension of the state or of the observation. When the likelihood is sharp compared with the spread of the prediction, almost all the weight falls on a few particles, and $N$ must grow exponentially with the dimension to prevent this (the curse of dimensionality for particle filters).

## Properties

- **Randomized.** Repeated runs give different answers; the error is $O(1/\sqrt N)$.
- **General.** Any model that can be simulated and whose likelihood can be evaluated; no linearity, no Gaussian noise, no derivatives.
- **Multimodal.** The particle cloud can represent any shape of posterior, unlike the [extended](/extended-kalman-filter/) and [unscented](/unscented-kalman-filter/) Kalman filters.
- **Unbiased likelihood.** $\hat Z_T$ is unbiased for every $N$, which makes the filter usable inside MCMC for parameters (particle MCMC).
- **Online.** Each step uses only the current particles and the new observation.
- **Path degeneracy.** If the full paths $x^i_{0:t}$ are kept, repeated resampling makes them share a common ancestor in the distant past, so the filter is a poor estimate of the smoothing distribution of early states.

## Variants and improvements

- **Adaptive resampling.** Resample only when the effective sample size $1/\sum_i (W^i)^2$ falls under a threshold, such as $N/2$. This is part of [sequential Monte Carlo](/sequential-monte-carlo/).
- **Lower-variance resampling.** Replace the multinomial draw of line L3 by residual, stratified or systematic [resampling](/resampling/).
- **Better proposals.** Draw $x_t$ from a distribution that looks at $y_t$, such as the locally optimal proposal $p(x_t \mid x_{t-1}, y_t)$, and correct with the weight $p(y_t \mid x_t) p(x_t \mid x_{t-1}) / q(x_t \mid x_{t-1}, y_t)$.
- **Auxiliary particle filter.** Resample with weights that already include a guess of the next likelihood (Pitt and Shephard 1999).
- **Rao-Blackwellized particle filter.** When part of the state is linear Gaussian given the rest, sample only the rest and run a Kalman filter for each particle (as in FastSLAM).
- **Particle smoothers.** Forward filtering backward smoothing and backward simulation reuse the stored particles to estimate $p(x_t \mid y_{1:T})$; see [smoothing](/smoothing/).
- **Regularized filter.** Add a small kernel jitter after resampling to fight sample impoverishment when the dynamics have little noise.

## When to use it

Use a particle filter when the model is nonlinear or non-Gaussian, the posterior may have several modes, and the state has a small dimension, roughly up to ten: target tracking with clutter, robot localization with a map (Monte Carlo localization), stochastic volatility in finance, and epidemic models. When the model is linear Gaussian use the Kalman filter, which is exact and far cheaper. When the model is nearly linear and unimodal, an EKF or UKF is cheaper. When the state space is finite and small, the forward algorithm of a [hidden Markov model](/hidden-markov-model/) is exact.

## Pitfalls

- **Weight underflow.** Likelihoods of many observations, or of sharp ones, underflow to zero. Work with log weights and subtract the maximum before exponentiating, as in the code.
- **All weights zero.** If no particle explains $y_t$, the filter fails. This shows a wrong model, an outlier, or too few particles; use heavier-tailed likelihoods or a better proposal.
- **Estimating after resampling.** Compute estimates of $p(x_t \mid y_{1:t})$ from the weighted particles before resampling; resampling only adds noise.
- **Deterministic dynamics.** With no process noise, resampled copies stay identical forever and the particle set collapses. Add jitter or use an MCMC move.
- **Static parameters.** Putting a fixed parameter into the state with no dynamics leads to the same collapse. Use particle MCMC or SMC samplers instead.
- **Trusting $\log \hat Z$.** Its expectation is below $\log p(y_{1:T})$, and its variance grows with $T$ for fixed $N$. Scale $N$ with $T$ when the likelihood estimate matters.

## Implementations

## History

Monte Carlo methods for filtering go back to Handschin and Mayne in 1969, who used sequential importance sampling without resampling; their weights degenerated after a few steps. Gordon, Salmond and Smith added the resampling step in 1993 and showed that the resulting bootstrap filter tracks the hard nonlinear benchmark where the extended Kalman filter fails. Kitagawa found the same method independently, with a smoother, and published it in 1996; Isard and Blake used it for visual tracking under the name Condensation in 1998. Del Moral gave the mathematical theory as interacting particle systems, including the unbiasedness of the likelihood estimate, collected in his 2004 book.

## References
