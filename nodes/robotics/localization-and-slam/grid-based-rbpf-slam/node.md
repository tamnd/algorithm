---
tag: X1GN8F
kind: algorithm
slug: grid-based-rbpf-slam
name: Grid-based Rao-Blackwellized SLAM
aliases:
- improved proposal grid SLAM
- Grisetti RBPF SLAM
area: robotics/localization-and-slam
level: advanced
summary: Grisetti's particle filter that builds one occupancy grid per particle, with scan matching in the proposal and adaptive resampling.
solves: [slam-problem, full-slam]
model: real-ram
complexity:
  vars: {N: the number of particles, B: the number of beams per scan, S: the number of score evaluations of the scan matcher, K: the number of points of the proposal, L: the number of cells along one beam, G: the number of cells of a grid}
  time: {step: O(N B (S + K + L)), resampling: O(N G)}
  space: {extra: O(N G)}
properties: {deterministic: false, exact: false, online: true, recursive: true}
history:
  year: 2007
  people: [Giorgio Grisetti, Cyrill Stachniss, Wolfram Burgard]
  note: Grisetti, Stachniss and Burgard (2007) used scan matching to build an improved proposal for grid-based Rao-Blackwellized SLAM and resampled only when the effective sample size was low.
prereqs: [rao-blackwellized-particle-filter, occupancy-grid-mapping, effective-sample-size]
see_also: [fastslam, rao-blackwellized-particle-filter, occupancy-grid-map, correlative-scan-matching, iterative-closest-point, likelihood-field-model, monte-carlo-localization, pose-graph-optimization]
sources:
  - paper: "Giorgio Grisetti, Cyrill Stachniss and Wolfram Burgard, Improved techniques for grid mapping with Rao-Blackwellized particle filters, IEEE Transactions on Robotics 23(1), 2007, pages 34 to 46"
    locator: the improved proposal from scan matching, the computation of the weights and the adaptive resampling
  - paper: "Kevin Murphy, Bayesian map learning in dynamic environments, Advances in Neural Information Processing Systems 12 (NIPS), 1999"
    locator: the use of a Rao-Blackwellized particle filter to learn a grid map
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 13 (FastSLAM, including its grid-based version)"
---

Grid-based Rao-Blackwellized SLAM builds an [occupancy grid map](/occupancy-grid-map/) from laser scans and odometry with a particle filter in which each particle holds one robot path and one full grid built along that path. It is the [Rao-Blackwellized particle filter](/rao-blackwellized-particle-filter/) applied to grid maps, as [FastSLAM](/fastslam/) is for landmark maps. Its contribution is in how it moves the particles: in the version of Grisetti, Stachniss and Burgard (2007), each particle matches the new scan against its own map and draws its new pose near the match, not from the odometry alone, and the filter resamples only when the weights have become uneven. With these two changes, the filter needs far fewer particles than a grid particle filter that moves its particles by odometry alone. The open source implementation GMapping, from the same group, made the method a common tool for 2D laser SLAM.

## In plain words

A robot with a laser scanner drives through a building. The filter keeps a few guesses of where the robot has been, and each guess draws its own map. When a new scan arrives, each guess first checks where the scan fits best on its own map, and then picks its new position close to that fit. Guesses whose maps match the scan well get more weight. When a few guesses hold almost all the weight, the filter copies the good ones and drops the bad ones, but it waits until then, because each copy step also throws away variety. The best guess gives the map.

## The problem

The input is a stream of odometry steps $u_t$, which give the relative motion with noise, and laser scans $z_t$, each a list of ranges at known angles. The output is a grid map of the area, with each cell occupied or free, and the robot path. This is the [SLAM problem](/slam-problem/) with a dense map. A dense grid has thousands of cells, so one joint Gaussian over the pose and the map, as in [EKF SLAM](/ekf-slam/), is out of the question. Given the path, the map is easy: it is [occupancy grid mapping](/occupancy-grid-mapping/) with known poses. That is what makes a Rao-Blackwellized filter fit.

## The algorithm

```pseudo id=main
GRID_RBPF(particles {(x^i, m^i, w^i)} for i = 1..N, u_t, z_t)
L1  for i ← 1 to N do
L2      x' ← x^i ⊕ u_t                                         ▷ the odometry guess
L3      x̂ ← scan match of z_t in m^i, by hill climbing from x'
L4      if the match fails then draw x^i ~ p(x | x^i, u_t); w^i ← w^i · p(z_t | m^i, x^i); go to L7
L5      draw x_1..x_K in a box around x̂; τ_j ← p(z_t | m^i, x_j) · p(x_j | x^i, u_t)
L6      μ, Σ ← the mean and covariance of the x_j weighted by τ_j;  draw x^i ~ N(μ, Σ);  w^i ← w^i · Σ_j τ_j
L7      update the grid m^i with z_t at x^i                     ▷ log-odds update
L8  normalize the weights;  if N_eff = 1 / Σ (w^i)² ≥ N/2 then return the particles
L9  resample N particles in proportion to w^i, each with its own copy of the grid and weight 1/N
```

**The proposal.** The best draw for a particle is from $p(x_t \mid m^i, x^i_{t-1}, z_t, u_t)$, the motion model times the scan likelihood, normalized. Its weight factor is then $p(z_t \mid m^i, x^i_{t-1}, u_t)$, the same whatever pose is drawn. A laser scan is far more precise than odometry, so this density is a narrow peak near the pose where the scan fits the map. Line L3 finds the peak, and lines L5 and L6 approximate the density by a Gaussian fitted to $K$ scored points around it. The sum of the scores in line L6 estimates the weight factor.

**The scan likelihood.** The code scores each beam endpoint by its distance $d$ to the nearest occupied cell nearby, as $\exp(-d^2 / 2 \sigma^2)$, a simple form of the [likelihood field model](/likelihood-field-model/). Any scan matcher that returns a good local fit can take its place.

**Adaptive resampling.** Line L8 resamples only when the effective sample size $N_\text{eff}$ falls below $N/2$, the threshold of Grisetti et al. Between resampling steps the weights carry the information, and no particle is lost.

## Example

**The proposal.** Take one coordinate only. The scan matcher returns $\hat x = 1.00$ m. Three points $0.95$, $1.00$ and $1.05$ get the scores $\tau = 1, 2, 1$. The weighted mean is $(0.95 + 2 \cdot 1.00 + 1.05) / 4 = 1.00$, and the weighted variance is $(0.05^2 + 0 + 0.05^2) / 4 = 0.00125$, a standard deviation of 3.5 cm. The particle draws its new position from $N(1.00, 0.00125)$, and its weight is multiplied by the sum of the scores, 4, times the volume of the box over $K$.

**Resampling.** Four particles end a step with the normalized weights $0.5, 0.3, 0.1, 0.1$. Then $N_\text{eff} = 1 / (0.25 + 0.09 + 0.01 + 0.01) = 2.78 \ge 2$, and the filter keeps them as they are. After the next step the weights are $0.7, 0.1, 0.1, 0.1$, so $N_\text{eff} = 1 / 0.52 = 1.92 < 2$, and the filter resamples. The test file checks both examples.

**A run.** The code drives a robot with 16 beams around a box in a room of 6 m by 4 m, on a grid of 10 cm cells. The robot turns 0.015 rad per step more than the odometry says. After 25 steps, over 6 seeds, odometry alone ends on average more than 0.48 m from the true position. These are measurements of this code:

| proposal | particles | mean final position error |
|---|---|---|
| scan matching (lines L3 to L6) | 5 | 0.05 m |
| motion model only | 5 | 0.13 m |
| motion model only | 30 | 0.06 m |

Of the cells that the best particle marks occupied, 96% are within one cell of a true wall, against about 60% for the map built along the odometry path. In this small Python code, 5 particles with scan matching took about as much time as 30 particles without it. The gain in memory is clearer: 5 grids instead of 30.

## Correctness

Given the path, the map is the occupancy grid of that path, so the filter only needs to sample paths; this is the Rao-Blackwellized factorization. For the proposal $p(x_t \mid m, x_{t-1}, z_t, u_t)$, the importance weight factor is $p(z_t \mid m, x_{t-1}, u_t)$, by Bayes' rule. Lines L5 and L6 approximate both: the sum of the scores times the volume over $K$ is an unbiased estimate of the integral over the box, and the Gaussian is a moment fit. The fallback of line L4 is a plain particle filter step whose weight has the same expected value. The [correctness proof](proofs/correctness.md) gives the derivation, the limits of the approximation, and why the scan matcher stops. Note that the grid update itself treats the cells as independent, so even with exact sampling the map is an approximation.

## Complexity

- **Time per step:** $O(N B (S + K + L))$. Each score evaluation looks at $B$ beam endpoints, the matcher makes $S$ evaluations and the proposal $K$ more, and the grid update walks about $L$ cells per beam.
- **Resampling:** $O(N G)$ for copying grids of $G$ cells. Adaptive resampling makes this rarer. Real implementations share unchanged parts of the maps between particles, for example in a tree of map patches, to avoid the full copy.
- **Memory:** $O(N G)$, one grid per particle. This, more than time, limits the number of particles for large areas.

## Properties

- **Few particles (measurement).** The improved proposal puts the particles where the scan fits, so most of them keep a useful weight. Grisetti et al. report maps of real data sets built with far fewer particles than earlier grid-based filters needed; the table above shows the same effect on a small scale.
- **Multimodal over paths.** Each particle has its own path and map. When the robot closes a loop, the particles whose maps fit the old part survive, which corrects the whole map at once.
- **Loss of path diversity.** Each resampling step reduces the number of distinct path histories. Adaptive resampling slows this, but after many steps without a loop closure, the particles may share all of their old path, and a later loop closure cannot be fixed.
- **Not exact.** The Gaussian fit, the box, the scan matcher and the independent cells of the grid are all approximations.

## Variants and improvements

- **Plain grid FastSLAM.** The motion model as the proposal and one grid per particle, as in the grid-based FastSLAM of Probabilistic Robotics. It needs far more particles with a precise laser.
- **Selective resampling only.** Keeping the motion model proposal but resampling by $N_\text{eff}$ already helps.
- **Shared maps.** Representing the grid of each particle as differences from the grids of its ancestors saves memory and copy time.
- **Graph-based SLAM.** For large areas, graph-based methods such as [pose graph optimization](/pose-graph-optimization/), with [correlative scan matching](/correlative-scan-matching/) for the constraints, have mostly replaced particle filters, because they can optimize the whole path again after a loop closure.

## When to use it

Use it for 2D laser SLAM in indoor areas of moderate size, when odometry is available and an online grid map is wanted. It handles ambiguous loop closures better than a single-hypothesis method, because the particles keep several paths. For large areas, long trajectories or 3D data, a graph-based method is usually better. For landmark maps, use [FastSLAM](/fastslam/). For localization in a known map, use [Monte Carlo localization](/monte-carlo-localization/).

## Pitfalls

- **Copies that share one grid.** A copied particle must own its grid, or share it only through a structure that never changes shared parts.
- **A peaked likelihood with the motion model.** With a precise laser and the motion model as the proposal, almost all particles get a near zero weight. This is the problem the improved proposal solves.
- **A scan matcher stuck in a local maximum.** Hill climbing can stop near, not at, the right pose, and then the Gaussian is centered there. Start from the odometry guess, and fall back to the motion model when too few beams match.
- **Too few particles for a large loop.** Particles cannot hold many paths. If no particle has a path that closes the loop correctly, the map gets a double wall.
- **Units of the weights.** The weights of the two branches of lines L4 and L6 must estimate the same quantity, with the same constants, or the branch decides which particles survive.

## Implementations

## History

Murphy (1999) used a Rao-Blackwellized particle filter to learn grid maps. FastSLAM (2002) used the same factorization for landmark maps, and FastSLAM 2.0 (2003) added a proposal that uses the readings. Grisetti, Stachniss and Burgard combined these ideas for grid maps: their 2007 paper in the IEEE Transactions on Robotics computes the proposal from a scan match and a set of sampled points, and resamples only when the effective sample size is below $N/2$. Their implementation, released as GMapping, became one of the most used SLAM programs for 2D lasers.

## References
