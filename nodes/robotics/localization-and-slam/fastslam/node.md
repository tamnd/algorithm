---
tag: RCNQFQ
kind: algorithm
slug: fastslam
name: FastSLAM
aliases:
- FastSLAM 1.0
area: robotics/localization-and-slam
level: advanced
summary: SLAM by a Rao-Blackwellized particle filter over robot paths, with one small EKF per landmark per particle, kept in a tree so that a step costs O(N log m).
solves: [slam-problem, full-slam]
model: real-ram
complexity:
  vars: {N: the number of particles, k: the number of readings per step, m: the number of landmarks}
  time: {step: O(N k log m)}
  space: {extra: O(N m)}
properties: {deterministic: false, exact: false, online: true, recursive: true}
history:
  year: 2002
  people: [Michael Montemerlo, Sebastian Thrun, Daphne Koller, Ben Wegbreit]
  note: Montemerlo, Thrun, Koller and Wegbreit (2002) factored the SLAM posterior given the path and kept the landmark filters in a tree. FastSLAM 2.0 (2003) added a proposal that uses the readings.
prereqs: [rao-blackwellized-particle-filter, extended-kalman-filter, ekf-slam]
see_also: [rao-blackwellized-particle-filter, grid-based-rbpf-slam, ekf-slam, particle-filter, monte-carlo-localization, persistent-binary-search-tree, data-association-slam, landmark-measurement-model]
sources:
  - paper: "Michael Montemerlo, Sebastian Thrun, Daphne Koller and Ben Wegbreit, FastSLAM: A factored solution to the simultaneous localization and mapping problem, Proceedings of the AAAI National Conference on Artificial Intelligence, 2002, pages 593 to 598"
    locator: the factorization of the SLAM posterior, the per landmark filters, the tree of landmarks and the per particle data association
  - paper: "Michael Montemerlo, Sebastian Thrun, Daphne Koller and Ben Wegbreit, FastSLAM 2.0: An improved particle filtering algorithm for simultaneous localization and mapping that provably converges, Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI), 2003, from page 1151"
    locator: the proposal that uses the readings, and the convergence result for the linear Gaussian case
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 13 (FastSLAM 1.0 with known correspondences, FastSLAM 2.0 and data association)"
---

FastSLAM solves landmark [SLAM](/slam-problem/) with a particle filter. Each particle holds one guess of the robot path and, for that guess, one small extended Kalman filter for each landmark. It is the [Rao-Blackwellized particle filter](/rao-blackwellized-particle-filter/) applied to landmark maps: the path is sampled, and the map is computed in closed form. [Grid-based RBPF SLAM](/grid-based-rbpf-slam/) applies the same idea to occupancy grids from laser scans, where each particle holds a grid instead of landmark filters. Compared with [EKF SLAM](/ekf-slam/), which keeps one joint Gaussian over the pose and all $m$ landmarks and pays $O(m^2)$ per reading, FastSLAM keeps $m$ separate $2 \times 2$ filters per particle. With the landmarks in a balanced tree, one step costs $O(N \log m)$ per reading for $N$ particles.

## In plain words

If you knew exactly where the robot had been, mapping would be easy: each landmark could be located on its own, from the readings of that landmark only. FastSLAM uses this. It keeps many guesses of the robot path. For each guess it locates every landmark separately, with a small filter. Guesses whose maps agree well with the new readings get more weight. Bad guesses are dropped and good ones are copied. To make copies cheap, a copy shares the landmark filters of the original and only makes new ones when a landmark changes.

## The problem

The robot moves with known controls $u_t$ and noisy motion. It reads the range and bearing $z$ of point landmarks $m_1, \dots, m_m$ in the plane. In the basic version each reading comes with the id of its landmark (known correspondences). FastSLAM estimates the path posterior and the map, $p(x_{1:t}, m \mid z_{1:t}, u_{1:t})$, which is the [full SLAM](/full-slam/) posterior, with a cost per step that does not grow with the length of the path. The code uses the velocity motion model and the [landmark measurement model](/landmark-measurement-model/).

## The algorithm

```pseudo id=main
FASTSLAM_1(particles {(x^i, tree^i, w^i)} for i = 1..N, u_t, z_t with landmark ids)
L1  for i ← 1 to N do
L2      draw x^i ~ p(x_t | x^i, u_t)                              ▷ sample the motion model
L3      for each reading z of landmark j do
L4          if j is not in tree^i then insert (μ ← h⁻¹(x^i, z), Σ ← H⁻¹ Q H⁻ᵀ); w^i ← w^i · p0; continue
L5          ẑ ← h(x^i, μ_j);  H ← ∂h/∂m at μ_j;  S ← H Σ_j Hᵀ + Q
L6          K ← Σ_j Hᵀ S⁻¹;  μ_j ← μ_j + K (z - ẑ);  Σ_j ← (I - K H) Σ_j   ▷ a new tree path
L7          w^i ← w^i · N(z; ẑ, S)
L8  resample N particles in proportion to w^i; a copy shares the tree of its source
L9  return the particles, each with weight 1/N
```

Each landmark belief is a mean $\mu_j$ and a $2 \times 2$ covariance $\Sigma_j$. Line L6 writes the new belief into the tree of the particle by copying the path from the root to its leaf, so other particles that share the tree are not affected. $p_0$ is the weight factor of a new landmark; with known correspondences every particle sees the new landmark at the same step, so $p_0$ cancels.

**The tree.** The landmarks of a particle are the leaves of a complete binary tree indexed by the landmark id. A lookup follows $\log_2 m$ links. A change makes new copies of the $\log_2 m$ nodes on the path to the leaf and shares all other nodes with the old tree, as in a [persistent binary search tree](/persistent-binary-search-tree/). Resampling copies a particle by copying the pointer to its root. Without the tree, each copy would copy $m$ filters.

## Example

The robot is at pose $(0, 0, 0)$ and reads a new landmark at range 2 and bearing 0.5, with $Q = \mathrm{diag}(0.01, 0.0009)$. Line L4 places it at $(2 \cos 0.5, 2 \sin 0.5) = (1.7552, 0.9589)$ with

$$\Sigma = H^{-1} Q H^{-\top} = \begin{pmatrix} 0.008529 & 0.002693 \\ 0.002693 & 0.005071 \end{pmatrix}.$$

At the next step, three particles have sampled three poses, and each gets the same reading $(2, 0.5)$ of this landmark:

- At pose $(0, 0, 0)$, $\hat z = (2, 0.5)$, so the innovation is zero. Here $S = 2Q$, the mean does not move and $\Sigma$ halves, as two equal readings should give. The weight factor is $1 / (2 \pi \sqrt{\det 2Q}) = 26.53$.
- At pose $(0, 0, 0.05)$, $\hat z = (2.0, 0.45)$. The bearing is off by 0.05, and the weight factor is $26.53 \cdot \exp(-0.5 \cdot 0.05^2 / 0.0018) = 13.25$.
- At pose $(0.3, 0, 0)$, $\hat z = (1.7427, 0.5826)$. Both parts are off, and the weight factor is 1.067.

After normalization, the three particles have weights 0.65, 0.32 and 0.03, and resampling will most likely drop the third. Each particle has its own landmark mean: the third moves the landmark to $(1.914, 0.962)$, to fit its wrong pose. The test file checks these numbers.

## Correctness

Given the whole path, the readings of different landmarks are independent, so the map posterior factors into one posterior per landmark: $p(x_{1:t}, m \mid z_{1:t}, u_{1:t}) = p(x_{1:t} \mid z_{1:t}, u_{1:t}) \prod_j p(m_j \mid x_{1:t}, z_{1:t})$. This is a theorem, and it needs the whole path: given only the current pose, the landmarks are correlated. Lines L2 to L7 are then the RBPF step with the motion model as the proposal. The EKF of each landmark is exact when the measurement model is linear in the landmark, and the weight of line L7 is the predictive density of the reading under the linearized model. The [correctness proof](proofs/correctness.md) gives the details, the case of a new landmark and the cost of the tree. The tests check that with a known pose each landmark follows an independent EKF, that the weight is the innovation density, and that the tree keeps old versions intact.

## Complexity

- **Time per step:** $O(N k \log m)$ for $k$ readings, plus $O(N)$ for resampling. Each reading does a constant amount of $2 \times 2$ algebra and one tree update of $O(\log m)$. Montemerlo et al. (2002) give $O(N \log m)$ per reading. EKF SLAM needs $O(m^2)$ per reading.
- **Space:** $O(N m)$ in the worst case. Particles that come from the same source share all landmarks that neither has changed since.
- **Without the tree:** with an array per particle, resampling costs $O(N m)$ per step, which is still linear in $m$ and simpler. For small maps the array is faster.

## Properties

- **Multimodal over paths.** Different particles can hold quite different paths, and so different maps. EKF SLAM holds one Gaussian.
- **Data association per particle.** Each particle can decide for itself which landmark a reading belongs to, by the most likely landmark under its own map. Wrong decisions only hurt the particles that make them, and these tend to lose weight. The code on this page uses known correspondences.
- **Loss of path diversity (measurement and known limit).** Resampling makes the particles share their early path. After a long loop, all particles may descend from one particle of the early part, and the filter becomes overconfident about the map. With 30 particles on a loop of 60 steps around 8 landmarks, the code places the landmarks with a mean error of less than 0.5 m on two seeds, and the mean pose ends within 0.3 m of the truth, against more than 0.9 m for odometry alone. These are measurements of this code, not general results.
- **Linearization per landmark.** Each landmark filter is linearized at its own mean, given an exact pose. The error from the linearization does not spread through a large joint covariance as in EKF SLAM.

## Variants and improvements

- **FastSLAM 2.0.** Montemerlo et al. (2003) draw the new pose from a Gaussian approximation of the proposal that uses the readings of the step as well as the motion model. This needs far fewer particles when the sensor is more precise than the motion. For the linear Gaussian case they prove convergence with even one particle; this result does not cover the general nonlinear case.
- **Unknown correspondences.** Per particle maximum likelihood association, with a new landmark when no likelihood is above a threshold. See [data association in SLAM](/data-association-slam/).
- **Grid maps.** Replacing the landmark filters by an occupancy grid per particle gives [grid-based RBPF SLAM](/grid-based-rbpf-slam/), with scan matching in the proposal and adaptive resampling.
- **Adaptive resampling.** Resample only when the effective sample size is low, to slow the loss of path diversity.

## When to use it

Use FastSLAM for landmark SLAM when the map has many landmarks, when the data association is uncertain, or when the pose posterior can have more than one mode. Use [EKF SLAM](/ekf-slam/) for small maps where one joint Gaussian is good enough and a deterministic result is wanted. For large loops and offline maps, a smoothing method such as [pose graph optimization](/pose-graph-optimization/) or [iSAM2](/isam2/) usually gives better maps, because it keeps the whole path and optimizes it again after each loop closure.

## Pitfalls

- **A shared tree changed in place.** Two particles that come from one source share their tree. An update must make new nodes; a change in place corrupts the other particle.
- **The motion proposal with a precise sensor.** If the readings are much more precise than the motion, few sampled poses fit, and most weights are near zero. Use FastSLAM 2.0 or more particles.
- **Underflow of the weights.** Many readings in one step multiply many small densities. Work with log weights, or normalize after each step.
- **The bearing difference.** The innovation of the bearing must be wrapped to $[-\pi, \pi)$, or a landmark behind the robot gets a huge innovation.
- **Overconfidence after long loops.** A small number of particles cannot hold enough paths for a large loop. The map then looks certain but has the errors of one path.

## Implementations

## History

Murphy (1999) had used a particle filter over the robot path with a grid map per particle, and Doucet, de Freitas, Murphy and Russell (2000) described Rao-Blackwellized particle filters in general. Montemerlo, Thrun, Koller and Wegbreit presented FastSLAM at AAAI 2002. They observed that the landmarks are independent given the path, gave each particle one Kalman filter per landmark, and kept the filters in a balanced tree so that a step is logarithmic in the number of landmarks. They also showed data association per particle. FastSLAM 2.0 followed at IJCAI 2003, with a proposal that uses the readings. Thrun, Burgard and Fox present both versions in Chapter 13 of Probabilistic Robotics (2005).

## References
