---
tag: GRKHHG
kind: algorithm
slug: monte-carlo-localization
name: Monte Carlo localization
aliases:
- particle filter localization
area: robotics/localization-and-slam
level: core
summary: Represents the pose belief by particles that the motion model moves and the sensor model weights, then resamples them. Augmented MCL adds random poses to recover.
solves: [mobile-robot-localization]
model: real-ram
complexity:
  vars: {N: the number of particles, D: the cost of one evaluation of the measurement model, T: the number of time steps}
  time: {per_step: O(N D), total: O(T N D)}
  space: {extra: O(N)}
properties: {deterministic: false, exact: false, online: true, randomized: true, recursive: true}
history:
  year: 1999
  people: [Frank Dellaert, Dieter Fox, Wolfram Burgard, Sebastian Thrun]
  note: Dellaert, Fox, Burgard and Thrun applied the particle filter to mobile robot localization with laser and sonar sensors and named it Monte Carlo localization.
prereqs: [mobile-robot-localization, bayes-filter, particle-filter]
see_also: [markov-localization, ekf-localization, kld-sampling, kidnapped-robot-problem, global-localization, resampling, likelihood-field-model, rao-blackwellized-particle-filter]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 4, Section 4.3 (the particle filter and the low variance sampler), and Chapter 8, Section 8.3 (Monte Carlo localization, its properties and random particle MCL in Section 8.3.5)"
  - paper: "Frank Dellaert, Dieter Fox, Wolfram Burgard and Sebastian Thrun, Monte Carlo localization for mobile robots, Proceedings of the IEEE International Conference on Robotics and Automation (ICRA), 1999"
    locator: the sample-based representation of the pose belief and its update by the motion and sensor models
  - paper: doi:10.1016/S0004-3702(01)00069-8
    title: "Sebastian Thrun, Dieter Fox, Wolfram Burgard and Frank Dellaert, Robust Monte Carlo localization for mobile robots, Artificial Intelligence 128(1-2), 2001, pages 99 to 141"
    locator: the failure of MCL with accurate sensors and small sample sets, and Mixture-MCL, which also samples poses from the sensor model
---

Monte Carlo localization (MCL) is the [particle filter](/particle-filter/) applied to [mobile robot localization](/mobile-robot-localization/). The belief over the pose is a set of $N$ particles, each a pose hypothesis. At each step every particle is moved by a draw from the motion model, weighted by the likelihood of the reading under the sensor model, and the set is resampled in proportion to the weights. The particles collect where the readings agree with the map, so the belief can have one peak, many peaks or none. This makes MCL usable for [global localization](/global-localization/), which a Gaussian filter cannot do, at a cost that grows with $N$ and not with the size of the map. Augmented MCL adds random particles when the weights drop, a heuristic that lets the robot recover from a [kidnapping](/kidnapped-robot-problem/).

## In plain words

The robot keeps many guesses of where it is. When it drives, each guess drives too, with a little random error, because the real wheels also slip. When it takes a reading, each guess gets a score: how well would the reading match the map if the robot were there? Then the robot makes a new set of guesses by copying good guesses many times and dropping bad ones. After a few steps the guesses gather around the true pose. If all scores suddenly become bad, the robot may have been moved, so it adds some guesses at random places.

## The problem

The input is a map $m$, a motion model $p(x_t \mid u_t, x_{t-1}, m)$ that can be sampled, a measurement model $p(z_t \mid x_t, m)$ that can be evaluated, an initial set of particles, and the controls and readings $u_t, z_t$ for $t = 1, 2, \dots$. The output at each step is a set $\mathcal{X}_t = \{x_t^{[1]}, \dots, x_t^{[N]}\}$ whose empirical distribution approximates the posterior $p(x_t \mid z_{1:t}, u_{1:t}, m)$ of the [Bayes filter](/bayes-filter/). For global localization, the initial particles are uniform over the free space. For tracking, they are drawn around the known start pose.

Typical models are the [odometry motion model](/odometry-motion-model/) or the [velocity motion model](/velocity-motion-model/) for $u_t$, and the [beam model](/beam-range-finder-model/) or the [likelihood field](/likelihood-field-model/) for a range scan $z_t$. Their noise parameters are fitted to data. A scan model usually treats the beams as independent given the pose, which is an approximation.

## The algorithm

```pseudo id=main
MCL(X_{t-1}, u_t, z_t, m)                        ▷ N particles; w_slow, w_fast persist
L1  for k ← 1 to N do
L2      x̄^[k] ← sample of p(x_t | u_t, x_{t-1}^[k], m)
L3      w^[k] ← p(z_t | x̄^[k], m)
L4  w_avg ← (1/N) Σ_k w^[k]
L5  w_slow ← w_slow + α_slow (w_avg - w_slow);  w_fast ← w_fast + α_fast (w_avg - w_fast)   ▷ augmented only
L6  X_t ← N draws from {x̄^[k]} with probabilities w^[k] / Σ w, by the low variance sampler
L7  replace each particle of X_t by a random pose with probability max(0, 1 - w_fast / w_slow)   ▷ augmented only
L8  return X_t
```

Plain MCL is lines L1 to L4, L6 and L8 (Thrun et al., Section 8.3). Line L2 is the proposal: the particles are drawn from the predicted belief. Line L3 is the importance weight, the ratio of the target (the posterior) to the proposal, up to a constant. Line L6 is the [resampling](/resampling/) step. The code uses the low variance sampler of Thrun et al. (Section 4.3), which is [systematic sampling](/systematic-sampling/): one uniform $r \in [0, 1/N)$, and the $N$ points $r + i/N$ select the particles through the cumulative normalized weights. A particle with normalized weight $\tilde w$ is copied $\lfloor N \tilde w \rfloor$ or $\lceil N \tilde w \rceil$ times.

**Augmented MCL.** Lines L5 and L7 follow Thrun et al. (Section 8.3.5), with $0 \le \alpha_\text{slow} \ll \alpha_\text{fast}$. The mean weight $w_\text{avg}$ estimates $p(z_t \mid z_{1:t-1}, u_{1:t}, m)$, the probability of the reading under the current belief. When the short term average $w_\text{fast}$ falls below the long term average $w_\text{slow}$, the readings fit the belief worse than they used to, and a fraction of the particles restarts at random poses. Thrun et al. draw each new particle either at random or from the weights. The code first resamples and then replaces, which gives the same probability per particle. This rule is a heuristic: it has no guarantee to find the true pose, and the rates are set by hand.

## Example

**One resampling step.** A ring of 30 cells has a color in each cell. The sensor reads the right color with probability $0.85$ and each of the 3 other colors with probability $0.05$. After line L2, five particles are at cells 5, 10, 11, 14 and 21, whose colors are 0, 3, 3, 1 and 2. The reading is $z = 3$.

| particle | cell | color | $w$ (L3) | $\tilde w = w / 1.85$ | cumulative | copies |
|---|---|---|---|---|---|---|
| 1 | 5 | 0 | 0.05 | 0.027 | 0.027 | 0 |
| 2 | 10 | 3 | 0.85 | 0.459 | 0.486 | 2 |
| 3 | 11 | 3 | 0.85 | 0.459 | 0.946 | 3 |
| 4 | 14 | 1 | 0.05 | 0.027 | 0.973 | 0 |
| 5 | 21 | 2 | 0.05 | 0.027 | 1.000 | 0 |

With $r = 0.1$, the points are $0.1, 0.3, 0.5, 0.7, 0.9$. The first two fall in the interval $(0.027, 0.486]$ of particle 2 and the other three in $(0.486, 0.946]$ of particle 3, so $\mathcal{X}_t = \{10, 10, 11, 11, 11\}$. The expected copies are $5 \times 0.459 = 2.30$ for each of particles 2 and 3; the sampler gives 2 or 3. The mean weight is $w_\text{avg} = 0.37$.

**Against the exact filter.** On the same ring, with the motion of 1 cell ahead with probability $0.8$ and of 0 or 2 cells with probability $0.1$ each, the test runs MCL with $N = 3000$ particles from a uniform start and the exact [histogram filter](/histogram-filter/) side by side. Over 8 steps, the total variation distance between the particle histogram and the exact belief stays below $0.08$, while the exact belief concentrates to more than $0.8$ on one cell. This is a measurement for one seed.

**Kidnapping.** With $N = 300$, the robot is moved 13 cells ahead after step 20. With $\alpha_\text{slow} = 0.05$ and $\alpha_\text{fast} = 0.5$, the injection probability rises to about $0.3$ to $0.4$ in the steps just after the kidnapping, and the most frequent cell of augmented MCL is the true cell in 21 of steps 41 to 70. Plain MCL has no particle near the new pose and gets the true cell in none of those steps. This is a measurement for one seed; for other seeds, plain MCL sometimes recovers by chance through its motion noise.

## Correctness

MCL does not compute the posterior exactly; it approximates it with random particles. The [correctness proof](proofs/correctness.md) shows the parts that are exact. Given the particles $\mathcal{X}_{t-1}$, the weighted particles of lines L1 to L3 are an unbiased importance sample of the Bayes update of the empirical belief: $E[\tfrac{1}{N} \sum_k w^{[k]} f(\bar x^{[k]})] = \tfrac{1}{N} \sum_k \int f(x)\, p(z_t \mid x, m)\, p(x \mid u_t, x_{t-1}^{[k]}, m)\, dx$ for each bounded $f$. The low variance sampler copies each particle $N \tilde w$ times on average, and $\lfloor N \tilde w \rfloor$ or $\lceil N \tilde w \rceil$ times always. If the particles $\mathcal{X}_{t-1}$ are independent draws of the prior belief, the ratio $\sum_k w^{[k]} f(\bar x^{[k]}) / \sum_k w^{[k]}$ converges almost surely to the posterior mean of $f$ as $N \to \infty$.

Over many steps, the resampled particles are no longer independent. That the error over a fixed number of steps still goes to 0 as $N \to \infty$ is a theorem of the theory of [sequential Monte Carlo](/sequential-monte-carlo/) under conditions such as bounded likelihoods; the proof here does not cover it. For a fixed $N$, nothing guarantees that a particle lies near the true pose.

## Complexity

One step evaluates the motion sampler and the measurement model once per particle and resamples in one pass.

- Time: $O(N D)$ per step, where $D$ is the cost of the measurement model. For the beam model with $B$ beams ray cast in a grid, $D$ is $O(B)$ times the cost of a ray cast; the likelihood field makes each beam $O(1)$ after a precomputed [distance transform](/distance-transform/).
- Space: $O(N)$ for the particles, plus the map.

The number of particles that is enough depends on the problem. Global localization in a large building needs far more particles than tracking. [KLD-sampling](/kld-sampling/) adapts $N$ at each step.

## Properties

- **Multimodal.** The particles can represent any distribution, so MCL handles global localization and symmetric maps.
- **Any models.** The motion model must only be sampled and the measurement model must only be evaluated, up to a constant factor. Neither needs to be linear or Gaussian.
- **Randomized.** Two runs with the same data give different particle sets. Tests need fixed seeds.
- **Resampling adds variance.** It removes particles of low weight, so it keeps the set useful, but it also loses diversity. Many implementations resample only when the effective sample size $(\sum w)^2 / \sum w^2$ falls below a threshold.
- **Particle deprivation.** For a fixed $N$, there is a positive probability that no particle lies near the true pose, and plain MCL cannot recover from this. Augmented MCL and Mixture-MCL reduce this risk; they do not remove it.

## Variants and improvements

- **Augmented MCL** (Thrun et al., Section 8.3.5): random particles when $w_\text{fast} < w_\text{slow}$, as above. A simpler form adds a fixed small fraction of random particles at each step.
- **Mixture-MCL** (Thrun, Fox, Burgard and Dellaert, 2001): a part of the particles is drawn from the sensor model, that is, at poses that fit the reading, and weighted by the motion model. This works better when the sensor is accurate, where plain MCL gives most particles a weight near 0.
- **KLD-sampling** (Fox, 2003): choose $N$ at each step from the number of grid bins that the particles occupy. See [KLD-sampling](/kld-sampling/).
- **Rao-Blackwellized filters:** when a part of the state can be estimated in closed form given the rest, sample only the rest. FastSLAM uses this for the map. See the [Rao-Blackwellized particle filter](/rao-blackwellized-particle-filter/).
- **Smoother sensor models:** with a very accurate sensor, the weights are almost all 0. A common rule of thumb is to inflate the sensor noise, or to raise the likelihood to a power below 1, so that the particles can follow it. This is a heuristic.

## When to use it

Use MCL when the initial pose is unknown, when the map has repeated structure, when the robot may be kidnapped, or when the models are far from linear and Gaussian, for example a laser scan in a grid map. It is the usual choice for indoor robots with a laser scanner. Use [EKF localization](/ekf-localization/) when the pose is known well, the map has distinct landmarks and the computation budget is small. Use [Markov localization](/markov-localization/) on a grid when the state space is small enough to enumerate and an exact belief is needed.

## Pitfalls

- **Too few particles.** The filter can converge to a wrong pose in a symmetric map, or lose the true pose in a large one. Check with many seeds, not one.
- **An overconfident sensor model.** If $p(z \mid x)$ is too sharp, few particles get a weight above 0 and the set collapses to a few poses. Independent beams make the likelihood of a scan far too sharp; inflate the noise or use fewer beams.
- **All weights 0.** If no particle explains the reading, line L6 cannot normalize. The code raises an error in plain MCL; augmented MCL keeps the moved particles and lets line L7 act.
- **Resampling with no motion.** If the robot does not move, the particles do not spread, and repeated resampling with the same reading makes the set too narrow. Skip the update when the robot is still, as many systems do.
- **Angles.** Average headings with $\operatorname{atan2}$ of the mean sine and cosine, not with the arithmetic mean.
- **Rounding of weights.** Products of many beam likelihoods underflow. Compute log weights and subtract the largest before taking the exponential.

## Implementations

## History

The particle filter came from the bootstrap filter of Gordon, Salmond and Smith (1993) and from related sampling methods in statistics and computer vision. Dellaert, Fox, Burgard and Thrun (1999) used it for mobile robot localization and called it Monte Carlo localization; it replaced the grids of [Markov localization](/markov-localization/) by a set of samples that follows the belief. Thrun, Fox, Burgard and Dellaert (2001) showed that plain MCL can fail with accurate sensors and proposed Mixture-MCL. Fox (2003) made the number of particles adaptive with [KLD-sampling](/kld-sampling/). Thrun, Burgard and Fox (2005) present MCL and augmented MCL in Chapter 8.

## References
