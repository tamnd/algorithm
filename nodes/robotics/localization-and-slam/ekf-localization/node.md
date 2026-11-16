---
tag: EVPG4E
kind: algorithm
slug: ekf-localization
name: EKF localization
aliases:
- extended Kalman filter localization
area: robotics/localization-and-slam
level: core
summary: Tracks the pose of a robot in a map of point landmarks with an extended Kalman filter. Fast, but it needs a good initial pose and correct data association.
solves: [mobile-robot-localization]
model: real-ram
complexity:
  vars: {k: the number of readings in one step, m: the number of landmarks of the map, T: the number of time steps}
  time: {known_correspondences: O(T k), unknown_correspondences: O(T k m)}
  space: {extra: O(1)}
properties: {deterministic: true, exact: false, online: true, recursive: true}
history:
  year: 1991
  people: [John J. Leonard, Hugh F. Durrant-Whyte]
  note: Leonard and Durrant-Whyte localized a mobile robot with an extended Kalman filter that matched sonar returns to geometric beacons of a map, with a validation gate on the innovation.
prereqs: [mobile-robot-localization, extended-kalman-filter, velocity-motion-model, landmark-measurement-model]
see_also: [markov-localization, monte-carlo-localization, ekf-slam, unscented-kalman-filter, data-association-slam, joint-compatibility-branch-and-bound, kalman-filter, chi-squared-goodness-of-fit-test]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 7, Section 7.4 (EKF localization with known correspondences, its derivation and its physical implementation), Section 7.5 (estimating correspondences by maximum likelihood), Section 7.6 (multi-hypothesis tracking) and Section 7.7 (UKF localization)"
  - paper: "John J. Leonard and Hugh F. Durrant-Whyte, Mobile robot localization by tracking geometric beacons, IEEE Transactions on Robotics and Automation 7(3), 1991, pages 376 to 382"
    locator: the extended Kalman filter that matches sonar features to beacons of an a priori map, with the validation gate on the innovation
---

EKF localization tracks the pose $(x, y, \theta)$ of a mobile robot in a known map with an [extended Kalman filter](/extended-kalman-filter/). The belief is one Gaussian with mean $\mu_t$ and covariance $\Sigma_t$. A prediction moves it with the [velocity motion model](/velocity-motion-model/), linearized at the mean, and each range and bearing reading of a landmark corrects it, with the [landmark measurement model](/landmark-measurement-model/) linearized in the same way. One step costs a few small matrix products, so it is the cheapest of the localization filters. In exchange it has two needs: the robot must know its pose to within the range where the linearization holds, and each reading must be matched to the right landmark. This page gives the algorithm of Thrun, Burgard and Fox (Section 7.4), the maximum likelihood association with a chi-square gate, a step with real numbers and a consistency test.

## In plain words

The robot keeps one best guess of its pose and a measure of how unsure it is, as an ellipse around the guess. When it drives, it moves the guess by the commanded motion and makes the ellipse larger, because the wheels slip. When it sees a known landmark, it compares where the landmark appears with where the guess says it should appear. The difference moves the guess, more if the guess was unsure and less if the sensor is noisy, and the ellipse gets smaller. If a reading is too far from every landmark, the robot ignores it.

## The problem

The input is a map of $m$ point landmarks $m_j = (m_{j,x}, m_{j,y})$, a Gaussian prior $N(\mu_0, \Sigma_0)$ on the pose, and at each time step a control $u_t = (v_t, \omega_t)$ held for $\Delta t$ seconds and a set of readings $z_t^i = (r_t^i, \phi_t^i)$. The output is a Gaussian approximation $N(\mu_t, \Sigma_t)$ of $p(x_t \mid z_{1:t}, u_{1:t}, m)$. This is the tracking case of [mobile robot localization](/mobile-robot-localization/).

**Motion model.** With $\theta = \mu_{t-1,\theta}$, the noise-free motion is

$$g(u_t, x_{t-1}) = x_{t-1} + \begin{pmatrix} -\tfrac{v}{\omega} \sin\theta + \tfrac{v}{\omega} \sin(\theta + \omega \Delta t) \\ \tfrac{v}{\omega} \cos\theta - \tfrac{v}{\omega} \cos(\theta + \omega \Delta t) \\ \omega \Delta t \end{pmatrix}$$

for $\omega \ne 0$, and a straight line $(v \Delta t \cos\theta, v \Delta t \sin\theta, 0)$ for $\omega = 0$. The control noise has the covariance $M_t = \mathrm{diag}(\alpha_1 v^2 + \alpha_2 \omega^2, \alpha_3 v^2 + \alpha_4 \omega^2)$. The $\alpha_i$ are fitted to the robot; they are not derived. The final rotation term of the full velocity model is left out, as in Thrun et al.

**Measurement model.** With $q = (m_{j,x} - x)^2 + (m_{j,y} - y)^2$, a landmark $j$ is seen at

$$h(x_t, j) = \begin{pmatrix} \sqrt{q} \\ \operatorname{atan2}(m_{j,y} - y, m_{j,x} - x) - \theta \end{pmatrix}$$

plus noise $N(0, Q_t)$ with $Q_t = \mathrm{diag}(\sigma_r^2, \sigma_\phi^2)$. Readings are independent given the pose. The bearing and the heading wrap to $[-\pi, \pi)$.

**Correspondences.** The index $c_t^i$ of the landmark of reading $i$ is either given (known correspondences) or must be estimated.

## The algorithm

```pseudo id=main
EKF-LOCALIZATION(μ, Σ, u_t, z_t, m)              ▷ u_t = (v, ω), θ = μ_θ
L1  G_t ← ∂g/∂x at (u_t, μ);  V_t ← ∂g/∂u at (u_t, μ)
L2  M_t ← diag(α1 v² + α2 ω², α3 v² + α4 ω²)
L3  μ̄ ← g(u_t, μ)
L4  Σ̄ ← G_t Σ G_tᵀ + V_t M_t V_tᵀ
L5  for each reading z^i = (r^i, φ^i) in z_t do
L6      j ← c^i if known, else the most likely landmark that passes the gate (or skip z^i)
L7      ẑ ← h(μ̄, j)
L8      H ← ∂h/∂x at μ̄ = [[-Δx/√q, -Δy/√q, 0], [Δy/q, -Δx/q, -1]]
L9      S ← H Σ̄ Hᵀ + Q_t
L10     K ← Σ̄ Hᵀ S⁻¹
L11     μ̄ ← μ̄ + K wrap(z^i - ẑ)
L12     Σ̄ ← (I - K H) Σ̄
L13 return μ̄, Σ̄
```

Here $\Delta x = m_{j,x} - \bar\mu_x$ and $\Delta y = m_{j,y} - \bar\mu_y$. For $\omega \ne 0$ the Jacobians are

$$G_t = \begin{pmatrix} 1 & 0 & \tfrac{v}{\omega}(\cos(\theta + \omega\Delta t) - \cos\theta) \\ 0 & 1 & \tfrac{v}{\omega}(\sin(\theta + \omega\Delta t) - \sin\theta) \\ 0 & 0 & 1 \end{pmatrix},$$

and $V_t$ has the columns $\partial g / \partial v$ and $\partial g / \partial \omega$, given in full in the code. For $\omega \to 0$ the code takes the limits, for example $\partial g_x / \partial \omega \to -v \Delta t^2 \sin\theta / 2$. Lines L1 to L4 are the prediction of the EKF. Lines L5 to L12 apply the readings one after the other. Because the readings are independent given the pose, this gives the same result as one update with the stacked readings, up to the relinearization at the new mean after each reading.

**Line L6, unknown correspondences.** For each landmark $j$, compute the innovation $\nu_j = z^i - h(\bar\mu, j)$ and its covariance $S_j$. Thrun et al. (Section 7.5) choose the $j$ with the largest likelihood $\det(2\pi S_j)^{-1/2} \exp(-\tfrac{1}{2} \nu_j^\top S_j^{-1} \nu_j)$. The code also applies the validation gate of Leonard and Durrant-Whyte: $j$ is a candidate only if $\nu_j^\top S_j^{-1} \nu_j \le 9.210$, the $0.99$ quantile of the chi-square distribution with 2 degrees of freedom. A reading with no candidate is dropped. If the innovation were exactly Gaussian, a correct reading would fail the gate with probability $0.01$; the level is a choice of the user.

## Example

**One step.** The prior is $\mu_0 = (0, 0, 0)$ and $\Sigma_0 = \mathrm{diag}(0.01, 0.01, 0.0025)$, so standard deviations of 10 cm, 10 cm and 0.05 rad. The control is $v = 1$ m/s and $\omega = 0.5$ rad/s for $\Delta t = 1$ s, with $\alpha = (0.01, 0.005, 0.005, 0.01)$, so $M = \mathrm{diag}(0.01125, 0.0075)$.

- L1: $G = \begin{pmatrix} 1 & 0 & -0.2448 \\ 0 & 1 & 0.9589 \\ 0 & 0 & 1 \end{pmatrix}$ and $V = \begin{pmatrix} 0.9589 & -0.1625 \\ 0.2448 & 0.4692 \\ 0 & 1 \end{pmatrix}$.
- L3: $\bar\mu = (2 \sin 0.5,\ 2 - 2 \cos 0.5,\ 0.5) = (0.9589, 0.2448, 0.5)$.
- L4: the standard deviations grow to $(0.144, 0.121, 0.100)$, and $\bar\Sigma$ gets a correlation between $y$ and $\theta$ ($\bar\Sigma_{y\theta} = 0.0059$): a heading error moves the robot sideways.

The true pose is $(1.0, 0.2, 0.45)$. A landmark at $(5, 0)$ is read at $z = (4.00, -0.500)$, with $\sigma_r = 0.1$ m and $\sigma_\phi = 0.03$ rad.

- L7: $\hat z = (4.0486, -0.5605)$, so the innovation is $\nu = (-0.0486, 0.0605)$.
- L8: $H = \begin{pmatrix} -0.9982 & 0.0605 & 0 \\ -0.0149 & -0.2466 & -1 \end{pmatrix}$.
- L9: $S = \begin{pmatrix} 0.0305 & -0.0017 \\ -0.0017 & 0.0147 \end{pmatrix}$, and $\nu^\top S^{-1} \nu = 0.306$, far inside the gate.
- L11 and L12: $\mu = (0.9916, 0.2078, 0.4517)$, and the standard deviations shrink to $(0.083, 0.091, 0.033)$.

One bearing reading fixes the heading well, because the bearing depends on $\theta$ directly. The position along the line of sight to the landmark improves through the range, and the position across it only through the correlation with $\theta$.

**Consistency.** A filter is consistent if its covariance matches its real error. The test runs 50 simulations of 20 steps with four landmarks and the noise of the model, and computes the normalized estimation error squared $e^\top \Sigma^{-1} e$ with $e = x_t - \mu_t$. For a consistent filter its mean is 3, the dimension of the pose. The measured mean over the 1000 steps is $3.04$. This is a measurement for these noise levels; with larger heading noise or few landmarks, the linearization error makes the EKF overconfident, and the mean grows above 3.

## Correctness

For a linear motion model and a linear measurement model with Gaussian noise, the algorithm is the [Kalman filter](/kalman-filter/), and its output is the exact posterior. For the nonlinear models here, the EKF replaces $g$ and $h$ by their first order Taylor expansions at the current mean, so the output is an approximation with no general error bound. The [correctness proof](proofs/correctness.md) shows what is exact: the prediction is the exact moment propagation of the linearized model, each update is the exact Bayes update of the linearized measurement, and the update in lines L10 to L12 equals the information form $\Sigma^{-1} \leftarrow \bar\Sigma^{-1} + H^\top Q^{-1} H$. The tests check the Jacobians against central differences, the update against the information form, and the consistency by the NEES test.

## Complexity

Let $k$ be the number of readings in one step and $m$ the number of landmarks. The state has 3 dimensions and a reading 2, so each matrix operation costs $O(1)$ in the [real RAM](/real-ram/) model.

- Prediction: $O(1)$.
- Update with known correspondences: $O(1)$ per reading, so $O(k)$ per step.
- Association by maximum likelihood: $O(m)$ per reading, so $O(k m)$ per step. A spatial index over the landmarks, for example a [k-d tree](/kd-tree/) with the gate as the search radius, reduces the number of candidates.
- Memory: $O(1)$ for the belief, plus the map.

This is the main advantage over grid and particle methods, whose cost grows with the number of poses or particles.

## Properties

- **Unimodal.** The belief has one peak. It cannot represent two hypotheses, so it cannot do [global localization](/global-localization/) or recover from a [kidnapping](/kidnapped-robot-problem/).
- **Local.** The linearization holds only near the mean. If the pose error is large compared with the distance to the landmarks, or the heading error is large, the update can move the mean the wrong way.
- **Deterministic and fast.** The same data give the same result, at a cost independent of the size of the map when correspondences are known.
- **The order of the readings matters a little.** Each update relinearizes at the new mean, so a different order gives slightly different results. With linear models the order does not matter.

## Variants and improvements

- **Unknown correspondences.** Maximum likelihood association with a gate, as above (Thrun et al., Section 7.5). Joint association of all readings of a step, for example with [joint compatibility branch and bound](/joint-compatibility-branch-and-bound/), avoids two readings taking the same landmark. See [data association in SLAM](/data-association-slam/).
- **Multi-hypothesis tracking.** Keep a mixture of Gaussians, one per association history, and prune the unlikely ones (Thrun et al., Section 7.6). It handles a few ambiguous hypotheses at a cost that grows with their number.
- **UKF localization.** The [unscented Kalman filter](/unscented-kalman-filter/) propagates sigma points through $g$ and $h$ instead of Jacobians (Thrun et al., Section 7.7). It needs no derivatives and handles stronger nonlinearity, at a small constant factor more.
- **Iterated EKF.** Repeat lines L7 to L11 with $H$ evaluated at the updated mean, a Gauss-Newton step on the measurement. This reduces the linearization error of sharp readings.
- **Joseph form.** Replace line L12 by $(I - K H) \bar\Sigma (I - K H)^\top + K Q K^\top$, which keeps $\Sigma$ symmetric and positive definite under rounding. The code instead symmetrizes $\Sigma$ after each update.
- **EKF SLAM.** If the landmarks are unknown, put them in the state; see [EKF SLAM](/ekf-slam/).

## When to use it

Use EKF localization to track a robot whose initial pose is known well, in a map of distinct landmarks, for example reflectors or fiducial markers, when computation is limited. Use [Markov localization](/markov-localization/) or [Monte Carlo localization](/monte-carlo-localization/) when the initial pose is unknown, when the map has repeated structure that makes association ambiguous, or when the sensor gives raw scans instead of landmarks.

## Pitfalls

- **Angles.** Wrap the bearing innovation $z - \hat z$ to $[-\pi, \pi)$ before line L11, and wrap $\mu_\theta$ after it. Without this, a reading near $\pm\pi$ gives an innovation near $2\pi$ and a huge wrong correction. The code has a test for this case.
- **A wrong association.** One reading matched to the wrong landmark moves the mean by a full innovation and shrinks the covariance, so the filter becomes sure of a wrong pose. Later correct readings then fail the gate. The gate reduces the risk but does not remove it: in a map with landmarks close together, two landmarks can pass the gate for one reading.
- **Overconfidence.** Neglected correlations, such as several readings of the same object or a noise model that is too small, make $\Sigma$ too small. The NEES test above detects this in simulation. Inflating $Q$ or $M$ is a common rule of thumb.
- **$\omega$ near zero.** The arc formulas divide by $\omega$. Use the straight-line limits below a small threshold, for $g$ and for both Jacobians.
- **A landmark at the robot.** $H$ divides by $q$ and $\sqrt q$. Skip readings of landmarks that are very close.

## Implementations

## History

In the second half of the 1980s, robotics researchers started to write the uncertain geometry of robot poses and features in terms of means and covariances. Leonard and Durrant-Whyte (1991) built the first widely cited EKF localization system: a robot with sonar sensors tracked its pose by matching returns to geometric beacons of a map, with a validation gate on the innovation. Thrun, Burgard and Fox (2005) present EKF localization in Chapter 7 next to Markov localization, with maximum likelihood correspondences, multi-hypothesis tracking and the UKF variant.

## References
