---
tag: E6NP93
kind: algorithm
slug: rao-blackwellized-particle-filter
name: Rao-Blackwellized particle filter
aliases:
- RBPF
- marginalized particle filter
area: robotics/localization-and-slam
level: advanced
summary: A particle filter that samples only some state variables and computes the rest in closed form for each particle, for example by a Kalman filter. This lowers the variance for a given particle count.
solves: [filtering, state-estimation]
model: real-ram
complexity:
  vars: {N: the number of particles, K: the number of values of the sampled part per step, c: the cost of one closed form update, b: the size of one closed form belief}
  time: {step: O(N K c)}
  space: {extra: O(N b)}
properties: {deterministic: false, exact: false, online: true, recursive: true}
history:
  year: 2000
  people: [Arnaud Doucet, Nando de Freitas, Kevin Murphy, Stuart Russell]
  note: Doucet, de Freitas, Murphy and Russell (2000) described Rao-Blackwellized particle filtering for dynamic Bayesian networks. Murphy (1999) had used it to learn grid maps.
prereqs: [particle-filter, kalman-filter, importance-sampling]
see_also: [fastslam, grid-based-rbpf-slam, sequential-monte-carlo, rao-blackwell-theorem, dynamic-bayesian-network, hidden-markov-model, resampling, monte-carlo-localization]
sources:
  - paper: "Arnaud Doucet, Nando de Freitas, Kevin Murphy and Stuart Russell, Rao-Blackwellised particle filtering for dynamic Bayesian networks, Proceedings of the 16th Conference on Uncertainty in Artificial Intelligence (UAI), 2000, pages 176 to 183"
    locator: the RBPF algorithm, the choice of the proposal and the examples
  - paper: "Kevin Murphy, Bayesian map learning in dynamic environments, Advances in Neural Information Processing Systems 12 (NIPS), 1999"
    locator: the use of Rao-Blackwellization to learn a grid map with a particle filter over the robot path
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 13 (FastSLAM, a Rao-Blackwellized particle filter for SLAM)"
---

A Rao-Blackwellized particle filter (RBPF) estimates the hidden state of a system that changes over time, from noisy observations, when the state has two parts: one part that is hard to handle in closed form, and one part that becomes easy once the first part is known. A plain [particle filter](/particle-filter/) represents the whole state by random samples. The RBPF samples only the hard part. Each particle then carries an exact distribution of the easy part given its sample, usually a [Kalman filter](/kalman-filter/). This removes the sampling noise of the easy part, so the same accuracy needs fewer particles. In robotics, the sampled part is the robot path and the exact part is the map: [FastSLAM](/fastslam/) uses one small Kalman filter per landmark, and [grid-based RBPF SLAM](/grid-based-rbpf-slam/) uses one occupancy grid per particle. This page describes the general method.

## In plain words

Some problems are easy once you know one thing. If you knew the exact path of a robot, building its map would be simple bookkeeping. If you knew when a machine switched between its modes, its state would follow a simple linear law. The filter guesses the hard thing many times, with a different guess in each particle, and solves the easy part exactly for each guess. Guesses that explain the observations well get more weight, and bad guesses are dropped and replaced by copies of good ones. Because only the hard part is guessed, fewer guesses are needed than when the filter guesses everything.

## The problem

The state at time $t$ is $(r_t, x_t)$. The filter must estimate $p(r_{1:t}, x_t \mid z_{1:t})$, or expectations under it, from the observations $z_1, \dots, z_t$, one step at a time. The model must have this property: given the history $r_{1:t}$, the distribution $p(x_t \mid r_{1:t}, z_{1:t})$ and the predictive density $p(z_t \mid r_{1:t}, z_{1:t-1})$ can be computed in closed form, step by step. The common case is a model that is linear and Gaussian in $x_t$ given $r_{1:t}$, as in a switching linear system or a [hidden Markov model](/hidden-markov-model/) whose output is a linear system. The code on this page uses a scalar switching system: a mode $s_t$ follows a Markov chain, and $x_t = a_{s_t} x_{t-1} + b_{s_t} + w_t$, $z_t = c x_t + v_t$ with Gaussian noise.

## The algorithm

```pseudo id=main
RBPF(particles {(r^i, α^i, w^i)} for i = 1..N, z_t)
L1  for i ← 1 to N do
L2      draw r_t^i ~ π(r_t | r^i_{1:t-1}, z_t)
L3      predict α^i in closed form given r^i_{1:t}               ▷ for example a Kalman prediction
L4      w^i ← w^i · p(z_t | r^i_{1:t}, z_{1:t-1}) p(r_t^i | r_{t-1}^i) / π(r_t^i | r^i_{1:t-1}, z_t)
L5      update α^i with z_t in closed form                       ▷ for example a Kalman update
L6  normalize the weights w^i to sum 1
L7  if N_eff = 1 / Σ (w^i)² < N_T then resample the particles and set each w^i to 1/N
L8  return the particles; E[f(x_t) | z_{1:t}] ≈ Σ w^i E[f(x_t) | r^i_{1:t}, z_{1:t}]
```

$\alpha^i$ holds the closed form belief of $x_t$ for particle $i$: a mean and a covariance in the linear Gaussian case. The density $p(z_t \mid r^i_{1:t}, z_{1:t-1})$ of line L4 is a by-product of the Kalman filter: the Gaussian density of the innovation.

**The proposal of line L2.** The simplest choice is the prior $\pi = p(r_t \mid r_{t-1})$; then line L4 multiplies the weight by the predictive density of $z_t$. When the sampled part has few values, the code can also draw $r_t$ from $p(r_t \mid r^i_{1:t-1}, z_{1:t})$, which looks at the new reading. Then the weight factor is the sum of the predictive densities over all values, weighted by the transition probabilities, and it does not depend on the drawn value. This needs the prediction of line L3 for every value, which is why the code computes it before the draw.

**Line L7.** Resampling every step adds noise; resampling never lets the weights degenerate. The code resamples with the low variance sampler when the effective sample size drops below $N/2$, as Grisetti et al. do for grid maps.

## Example

A cart on a line is stopped (mode 0) or moves by 1 per step (mode 1), and it keeps its mode with probability 0.9. The position noise has variance $q = 0.01$, the reading is $z_t = x_t + v_t$ with variance $r = 0.25$, and at time 0 the cart is stopped at $x_0 \sim N(0, 0.01)$. The first reading is $z_1 = 0.9$.

One particle at time 0 predicts for mode 0 the position $N(0, 0.02)$ and the reading $N(0, 0.27)$, and for mode 1 the position $N(1, 0.02)$ and the reading $N(1, 0.27)$. The weight of each mode is the transition probability times the density of the reading:

- mode 0: $0.9 \cdot \exp(-0.9^2 / 0.54) / \sqrt{2 \pi \cdot 0.27} = 0.9 \cdot 0.2231 / 1.3025 = 0.1542$;
- mode 1: $0.1 \cdot \exp(-0.1^2 / 0.54) / \sqrt{2 \pi \cdot 0.27} = 0.1 \cdot 0.9817 / 1.3025 = 0.0754$.

So $P(s_1 = 0 \mid z_1) = 0.1542 / 0.2296 = 0.672$. The Kalman gain is $0.02 / 0.27 = 0.0741$ for both modes, so the mean of $x_1$ is $0 + 0.0741 \cdot 0.9 = 0.067$ in mode 0 and $1 + 0.0741 \cdot (0.9 - 1) = 0.993$ in mode 1, both with variance $0.0185$. The exact posterior mean is $0.672 \cdot 0.067 + 0.328 \cdot 0.993 = 0.371$. The particles that draw mode 0 or mode 1 carry these two Kalman filters exactly; only the share of each mode is a Monte Carlo estimate.

After the readings $2.1$ and $2.0$, the exact posterior, a mixture of $2^3$ Kalman filters, gives $P(\text{moving}) = 0.640$ and a mean position of $2.476$: the jump from 0.9 to 2.1 says that the cart moved, and the small step to 2.0 says that it may have stopped. The test file checks these numbers and shows that the RBPF approaches them as $N$ grows.

## Correctness

Given the sampled history, the rest of the model is a linear Gaussian state space model, so the Kalman filter of lines L3 and L5 gives the exact conditional of $x_t$. The weights of line L4 are the importance weights of the history under the target $p(r_{1:t} \mid z_{1:t})$, for any proposal that is positive where the target is. So line L8 is an importance sampling estimate of the exact sum over all histories, and it converges to it as $N$ grows. The [correctness proof](proofs/correctness.md) gives the details and the Rao-Blackwell argument for the variance. The tests compare the filter with an exact enumeration of all $2^t$ mode histories, check that one mode reduces it to a Kalman filter, and check that the average of the likelihood estimate matches $p(z_{1:t})$.

## Complexity

- **Time per step:** $O(N K c)$, where $c$ is the cost of one closed form step and $K$ the number of values that the proposal looks at. For the prior proposal, $K = 1$. For a Kalman filter on $d$ variables, $c = O(d^3)$, or less with structure, as in FastSLAM, where each landmark has its own small filter.
- **Resampling:** $O(N)$ with the low variance sampler, plus the cost of copying the closed form beliefs. FastSLAM shares the unchanged parts in a tree so that a copy costs $O(\log m)$ for $m$ landmarks.
- **Memory:** $N$ closed form beliefs.

## Properties

- **Exact in the closed form part.** The only Monte Carlo error is in the sampled part. If the sampled part has one value, the RBPF is the Kalman filter, with no sampling error at all.
- **Lower variance (theorem for perfect sampling, measurement for the full filter).** For draws from the posterior, the law of total variance gives $\mathrm{Var}[E[f \mid r]] \le \mathrm{Var}[f]$, which is the [Rao-Blackwell theorem](/rao-blackwell-theorem/). On the example with 8 steps, over 20 seeds, the mean squared error of the posterior mean is $5.3 \cdot 10^{-4}$ for the RBPF and $2.2 \cdot 10^{-3}$ for a plain particle filter at 100 particles, and $4.8 \cdot 10^{-5}$ against $2.9 \cdot 10^{-4}$ at 1000 particles.
- **Unbiased likelihood.** The product of the normalizers of line L6 over the steps is an estimate of $p(z_{1:t})$ whose average over runs is the exact value. The tests check this on 300 runs.
- **Degeneracy of the past.** Resampling makes the particles share their early history. The estimate of the current state is fine, but the samples of old values of $r$ have little diversity. In SLAM this is the loss of the diversity of the path, which matters at a loop closure.

## Variants and improvements

- **The optimal proposal.** Drawing $r_t$ given $z_t$ as well, as the code does for a few modes, keeps more particles in useful places. Grid-based RBPF SLAM approximates it by scan matching, and FastSLAM 2.0 does the same with the landmark readings.
- **Adaptive resampling.** Resampling only when the effective sample size is low, as in line L7, reduces the loss of diversity.
- **FastSLAM.** The sampled part is the robot path, and given the path the landmarks are independent, so each particle has one small EKF per landmark instead of one large filter.
- **Mixture Kalman filters and the marginalized particle filter.** The same idea under other names in signal processing, often for models with a nonlinear part and a linear Gaussian part, where the nonlinear part is sampled.

## When to use it

Use an RBPF when the state has a part that is hard, because it is discrete, multimodal or strongly nonlinear, and a part that is linear and Gaussian, or otherwise tractable, given the first. Switching linear systems, fault detection, target tracking with an unknown maneuver mode and SLAM are the typical cases. If the whole state is tractable, use the exact filter. If no part is tractable, use a plain [particle filter](/particle-filter/). If the tractable part is large and its closed form step is expensive, compare the cost per particle with that of more particles in a plain filter.

## Pitfalls

- **The wrong conditional.** The closed form part must be exact given the full sampled history, not only given the current value of $r$. A particle must keep its own filter state, which carries the history.
- **Sharing filters after resampling.** Copies of a particle must not share a mutable filter state. Copy it, or share it only in a persistent structure, as FastSLAM does.
- **A peaked likelihood.** With a precise sensor and the prior proposal, almost all weights are near zero. Use a proposal that looks at $z_t$.
- **Underflow.** Multiply weights in the log domain when the likelihoods are small, and normalize at each step.
- **Too few particles for the history.** The closed form part cannot fix a wrong sampled history. If the right history has no particle, the estimate is wrong with a small reported variance.

## Implementations

## History

The idea of replacing a sampled variable by its conditional expectation comes from the Rao-Blackwell theorem of statistics. In particle filtering, it appeared in several forms around 1999 and 2000. Murphy (1999) used it to learn a grid map with a particle filter over the robot path, and Doucet, de Freitas, Murphy and Russell (2000) described Rao-Blackwellized particle filtering for dynamic Bayesian networks at UAI 2000. In SLAM, Montemerlo, Thrun, Koller and Wegbreit (2002) built FastSLAM on it, and Grisetti, Stachniss and Burgard (2007) built a grid-based version with an improved proposal and adaptive resampling. Thrun, Burgard and Fox present it as the basis of FastSLAM in Chapter 13 of Probabilistic Robotics (2005).

## References
