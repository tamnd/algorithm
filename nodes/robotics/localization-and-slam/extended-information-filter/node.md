---
tag: DYEYTV
kind: algorithm
slug: extended-information-filter
name: Extended information filter
aliases:
- EIF
area: robotics/localization-and-slam
level: advanced
summary: The extended Kalman filter written with the information matrix and vector. Readings add to a few entries, but the motion step and the mean need a matrix inverse.
solves: [state-estimation, online-slam]
model: real-ram
complexity:
  vars: {n: the size of the state, k: the number of state entries that one reading depends on}
  time: {prediction: O(n^3), update: O(k^2), mean: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: false, online: true, recursive: true}
history:
  year: 2004
  people: [Sebastian Thrun, Yufeng Liu, Daphne Koller, Andrew Y. Ng, Zoubin Ghahramani, Hugh Durrant-Whyte]
  note: The information form of the Kalman filter is older. Thrun et al. (2004) studied the extended information filter for SLAM, showed that motion fills in its information matrix, and made it sparse by an approximation, the SEIF.
prereqs: [extended-kalman-filter, positive-definite-matrix, ekf-slam]
see_also: [sparse-extended-information-filter, graphslam, factor-graph, gaussian-belief-propagation, schur-complement, sherman-morrison-formula, unscented-kalman-filter, kalman-filter]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Section 3.5 (the information filter and the extended information filter) and Chapter 12 (the information form of SLAM)"
  - paper: "Sebastian Thrun, Yufeng Liu, Daphne Koller, Andrew Y. Ng, Zoubin Ghahramani and Hugh Durrant-Whyte, Simultaneous localization and mapping with sparse extended information filters, International Journal of Robotics Research 23(7-8), 2004, pages 693 to 716"
    locator: the extended information filter for SLAM and the effect of the motion update on the information matrix
---

The extended information filter (EIF) is the [extended Kalman filter](/extended-kalman-filter/) with the belief $N(\mu, \Sigma)$ stored as the information matrix $\Omega = \Sigma^{-1}$ and the information vector $\xi = \Omega \mu$. It linearizes the same way and gives the same estimate, up to rounding. What changes is the cost: a reading adds a small term to a few entries of $\Omega$, while the motion step and the recovery of the mean need a matrix inverse. In SLAM, the update of a reading of one landmark is local, but each motion step links all landmarks that the robot has seen, so $\Omega$ fills in. The [sparse extended information filter](/sparse-extended-information-filter/) (SEIF) removes some of these links by an approximation to keep $\Omega$ sparse; the EIF on this page is exact up to linearization and keeps all of them.

## In plain words

A Kalman filter keeps a best guess and a table that says how unsure it is. The information filter keeps the opposite table: how much it knows. Knowledge from independent readings simply adds up, so a reading changes only the few numbers that it is about, and readings can come in any order. A step of the robot destroys some knowledge, and that is hard to write as a sum, so the motion step must convert the table, which takes time. The best guess is not stored directly either, and getting it back also takes a full computation. The filter knows nothing about a new landmark at the start, which it can store as zero, while a Kalman filter cannot store an infinite doubt.

## The problem

The input is the information form $(\xi, \Omega)$ of the belief at time $t-1$, a control $u_t$, and the readings $z_t^1, \dots, z_t^k$ of the step. The motion model is $x_t = g(u_t, x_{t-1}) + w$ with $w \sim N(0, R_t)$, and reading $i$ is $z^i = h_i(x_t) + v_i$ with $v_i \sim N(0, Q_i)$. The output is the information form of the Gaussian approximation of the belief at time $t$. In [online SLAM](/online-slam/), the state is the robot pose and the landmarks, as in [EKF SLAM](/ekf-slam/).

## The algorithm

```pseudo id=main
EIF(ξ, Ω, u_t, z_t)
L1  μ ← Ω⁻¹ ξ                                   ▷ recover the mean: a linear solve
L2  G ← ∂g/∂x at (u_t, μ)
L3  Ω̄ ← (G Ω⁻¹ Gᵀ + R_t)⁻¹
L4  μ̄ ← g(u_t, μ)
L5  ξ̄ ← Ω̄ μ̄
L6  for each reading z^i in z_t do
L7      H ← ∂h_i/∂x at μ̄
L8      Ω̄ ← Ω̄ + Hᵀ Q_i⁻¹ H                         ▷ only the entries where H is not zero
L9      ξ̄ ← ξ̄ + Hᵀ Q_i⁻¹ (z^i - h_i(μ̄) + H μ̄)
L10 return ξ̄, Ω̄
```

Lines L1 to L5 are the EKF prediction, converted to information form and back. Lines L8 and L9 are the EKF update in information form; the [correctness proof](proofs/correctness.md) derives them. The term $z^i - h_i(\bar\mu)$ is the innovation, with the angle wrapped for a bearing. All readings of the step are linearized at the same $\bar\mu$, so their order does not matter. The sequential EKF relinearizes after each reading, which differs slightly in the nonlinear case.

**Line L8 in SLAM.** A reading of landmark $j$ depends on the pose and on $m_j$ only, so $H$ has $k = 5$ nonzero columns in the plane, and the update changes a 5 by 5 block of $\Omega$ and 5 entries of $\xi$. The EKF changes all of $\Sigma$ for the same reading.

**Line L3 in SLAM.** The motion changes only the pose. Write the pose block of $\Omega$ as $\Omega_{xx}$, the links between the pose and the landmarks as $\Omega_{xm}$, and let the pose move as $x_t = G x_{t-1} + w$ with $w \sim N(0, R)$. The step adds the new pose and then removes the old one, which is a [Schur complement](/schur-complement/): the landmark block becomes

$$\bar\Omega_{mm} = \Omega_{mm} - \Omega_{mx} (\Omega_{xx} + G^\top R^{-1} G)^{-1} \Omega_{xm}.$$

The second term is nonzero for every pair of landmarks that are both linked to the old pose. So every landmark seen from the old pose becomes linked to every other one, as the example shows.

## Example

A robot moves on a line and sees two landmarks A and B. The state is $(x, A, B)$, and a reading of a landmark is its offset from the robot, $z = m - x$ with the variance $0.04$. The robot starts at $x = 0$ with variance $0.01$, and nothing is known about A and B, so

$$\Omega = \begin{pmatrix} 100 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}, \qquad \xi = (0, 0, 0).$$

A Kalman filter cannot start like this, because $\Sigma$ would be infinite.

**Two readings.** The robot reads A at $2.0$ and B at $5.0$. Each reading has $H = (-1, 1, 0)$ or $(-1, 0, 1)$, and lines L8 and L9 add $25\, H^\top H$ and $25\, H^\top z$:

$$\Omega = \begin{pmatrix} 150 & -25 & -25 \\ -25 & 25 & 0 \\ -25 & 0 & 25 \end{pmatrix}, \qquad \xi = (-175, 50, 125).$$

The entry between A and B is 0: the two readings link each landmark to the robot, not to each other. Solving $\Omega \mu = \xi$ gives $\mu = (0, 2, 5)$ and the covariance has the variances $(0.01, 0.05, 0.05)$, the same as EKF SLAM when it adds each landmark from the reading.

**A motion.** The robot moves by $u = 1$ with the variance $0.01$. Lines L1 to L5 give

$$\bar\Omega = \begin{pmatrix} 60 & -10 & -10 \\ -10 & 22.5 & -2.5 \\ -10 & -2.5 & 22.5 \end{pmatrix}, \qquad \bar\xi = (-10, 22.5, 97.5).$$

Now A and B are linked by $-2.5$. They were both linked to the old pose, and removing the old pose moves the link to them. This is the fill-in that makes the EIF for SLAM dense, and that SEIF limits.

**A reading of A.** The robot reads A at $0.95$, a little less than the predicted $2 - 1 = 1$. Lines L8 and L9 change only the entries of $x$ and A: $\Omega_{xx} = 85$, $\Omega_{xA} = -35$, $\Omega_{AA} = 47.5$, and $\xi = (-33.75, 46.25, 97.5)$. The mean is $(1.0056, 1.9778, 5.0)$ with the standard deviations $(0.137, 0.180, 0.224)$. B does not move: its covariance with $x$ and with A is the same, $0.01$, so a reading of the offset $A - x$ tells nothing about it.

## Correctness

The [correctness proof](proofs/correctness.md) shows that with the same linearization points, each step of the EIF gives the information form of the EKF belief: line L3 is the inverse of the predicted covariance, and lines L8 and L9 give $\Omega^{-1} = (I - KH)\bar\Sigma$ and $\Omega^{-1} \xi = \bar\mu + K \nu$. For linear models with Gaussian noise the EKF is the [Kalman filter](/kalman-filter/), so the EIF is exact. The proof also shows that several readings add up in any order and that a reading changes only the entries of the state that it depends on. The tests compare the EIF with a dense EKF on 12 steps of a planar SLAM run and find agreement within $10^{-8}$; a linear run with a flat prior matches batch least squares within $10^{-9}$. For nonlinear models, the EIF has the same linearization error as the EKF and no error bound.

## Complexity

Let $n$ be the size of the state and $k$ the number of state entries that one reading depends on. Costs are in the [real RAM](/real-ram/) model, for the dense matrices of the code.

- **Mean recovery (line L1):** $O(n^3)$ for a dense solve. With a sparse $\Omega$ it is much cheaper, and iterative methods can reuse the last mean.
- **Prediction (lines L2 to L5):** $O(n^3)$, two inverses. In SLAM, the motion changes only the pose entries, and the [Sherman-Morrison-Woodbury formula](/sherman-morrison-formula/) brings the step to $O(n^2)$ for a dense $\Omega$.
- **Update (lines L7 to L9):** $O(k^2)$ per reading, after the $O(dn)$ scan of the Jacobian that the code does. In SLAM, $k$ is a constant, so this is $O(1)$, against $O(n^2)$ for the EKF.
- **Memory:** $O(n^2)$ for $\Omega$.

So the EIF trades a cheap update for an expensive prediction and an expensive mean. It pays off when there are many readings per motion step, or when $\Omega$ stays sparse.

## Properties

- **Same estimate as the EKF.** With the same linearization points, a theorem proved on this page. The rounding differs: inverting $\Omega$ loses precision when $\Omega$ is badly conditioned.
- **Additive, local updates.** Information from independent readings adds up. This makes the filter useful for fusing many sensors and for merging the results of several robots, where the shared information must be counted only once.
- **Zero information is allowed.** A state that nothing has been measured about has a zero row in $\Omega$. The covariance form needs an infinite variance for it.
- **Fill-in under motion.** In SLAM, the motion step links every pair of landmarks that are linked to the pose. Over time $\Omega$ becomes dense, but most of its entries are small after normalization, which Thrun et al. (2004) observed and the SEIF exploits.
- **The full path is sparse.** If the old poses are kept in the state instead of being removed, no fill-in happens: $\Omega$ has a block for each motion and each reading, as in [GraphSLAM](/graphslam/) and other [factor graph](/factor-graph/) methods.

## Variants and improvements

- **Sparse extended information filter.** [SEIF](/sparse-extended-information-filter/) keeps the number of landmarks linked to the pose bounded, so that $\Omega$ stays sparse and each step costs constant time, at the cost of an approximation that makes the estimate overconfident.
- **Delayed state filters.** Keeping the past poses that have readings gives an exactly sparse information matrix without an approximation. This is the step from the [online](/online-slam/) to the [full](/full-slam/) SLAM problem.
- **The linear information filter.** For linear models, lines L2 to L9 use the fixed matrices of the model, and the filter is exact.
- **Distributed estimation.** Because updates add, nodes of a sensor network can each sum their own terms and exchange them. [Gaussian belief propagation](/gaussian-belief-propagation/) passes such terms along the edges of a graph.

## When to use it

Use the EIF when readings are many and cheap to add, and motion steps are rare, or when you need a prior with zero information on some states. Use it as a step towards [SEIF](/sparse-extended-information-filter/) or [GraphSLAM](/graphslam/), which are where the information form pays off for SLAM. For a small dense state with one reading per step, the EKF is simpler and does the same work with fewer inverses.

## Pitfalls

- **The mean is not stored.** Lines L4, L7 and L9 need the mean. Forgetting to recover it, or using an old value, gives wrong linearization points.
- **A singular matrix.** Line L1 and line L3 need $\Omega$ to be invertible. With a flat prior, the filter must first get enough readings to make it so; until then, only updates are possible.
- **Angles.** Wrap the bearing innovation $z^i - h_i(\bar\mu)$, not $z^i$ or $h_i(\bar\mu)$ alone, before line L9.
- **Double counting.** When two filters exchange information, the terms that both have already used must be subtracted once. Otherwise the result is overconfident.
- **Rounding.** Two inverses per step lose precision. Symmetrize $\Omega$, and prefer a Cholesky solve to an explicit inverse.

## Implementations

## History

The information form of the Kalman filter is a standard rewriting of the filter in estimation theory, and its additive update suits the fusion of data from many sensors. For SLAM, Thrun, Liu, Koller, Ng, Ghahramani and Durrant-Whyte (2004) studied the extended information filter and observed that the normalized information matrix is close to sparse, with strong links only between nearby landmarks. They made it exactly sparse by an approximation, the SEIF. Thrun, Burgard and Fox (2005) present the EIF in Section 3.5 of Probabilistic Robotics and the information form of SLAM in Chapter 12. Keeping the whole path gives an exactly sparse problem, and this is the basis of the smoothing methods for the full SLAM problem.

## References
