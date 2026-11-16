---
tag: P959WA
kind: algorithm
slug: ekf-slam
name: EKF SLAM
aliases:
- extended Kalman filter SLAM
- stochastic map
area: robotics/localization-and-slam
level: core
summary: Keeps one joint Gaussian over the robot pose and all m landmarks. Each reading updates the full covariance in O(m^2) time, which limits it to maps of a few hundred landmarks.
solves: [online-slam]
model: real-ram
complexity:
  vars: {m: the number of landmarks in the map, k: the number of readings in one step}
  time: {prediction: O(m), update: O(k m^2), association: O(k m)}
  space: {extra: O(m^2)}
properties: {deterministic: true, exact: false, online: true, recursive: true}
history:
  year: 1986
  people: [Randall Smith, Matthew Self, Peter Cheeseman]
  note: Smith and Cheeseman (1986) and Smith, Self and Cheeseman (1990) kept all uncertain spatial relations of a robot and its world in one state vector with one covariance matrix, the stochastic map, and updated it with a Kalman filter.
prereqs: [online-slam, extended-kalman-filter, velocity-motion-model, landmark-measurement-model]
see_also: [ekf-localization, ekf-slam-convergence-theorem, data-association-slam, joint-compatibility-branch-and-bound, extended-information-filter, sparse-extended-information-filter, fastslam, graphslam]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 10, Section 10.2 (EKF SLAM with known correspondences) and Section 10.3 (EKF SLAM with unknown correspondences)"
  - paper: doi:10.1177/027836498600500404
    title: "Randall C. Smith and Peter Cheeseman, On the representation and estimation of spatial uncertainty, International Journal of Robotics Research 5(4), 1986, pages 56 to 68"
    locator: the representation of uncertain relations between frames by a mean and a covariance, and their compounding
  - paper: "Randall Smith, Matthew Self and Peter Cheeseman, Estimating uncertain spatial relationships in robotics, in Ingemar J. Cox and Gordon T. Wilfong (eds.), Autonomous Robot Vehicles, Springer, 1990"
    locator: the stochastic map, one state vector and one covariance for the robot and all objects, with the addition of new objects
  - paper: "M. W. M. Gamini Dissanayake, Paul Newman, Steven Clark, Hugh F. Durrant-Whyte and M. Csorba, A solution to the simultaneous localization and map building (SLAM) problem, IEEE Transactions on Robotics and Automation 17(3), 2001, pages 229 to 241"
    locator: Section III (the convergence of the map covariance in the linear case) and the experiments with millimeter wave radar
  - paper: "Simon J. Julier and Jeffrey K. Uhlmann, A counter example to the theory of simultaneous localization and map building, Proceedings of the IEEE International Conference on Robotics and Automation, 2001"
    locator: the inconsistency of the nonlinear EKF SLAM for a stationary robot
  - paper: doi:10.1109/TRO.2007.903811
    title: "Shoudong Huang and Gamini Dissanayake, Convergence and consistency analysis for extended Kalman filter based SLAM, IEEE Transactions on Robotics 23(5), 2007, pages 1036 to 1049"
    locator: the analysis of the nonlinear planar EKF SLAM with range and bearing readings, and the role of the Jacobians evaluated at different estimates
  - paper: doi:10.1109/MRA.2006.1638022
    title: "Hugh Durrant-Whyte and Tim Bailey, Simultaneous localization and mapping, part I, IEEE Robotics and Automation Magazine 13(2), 2006, from page 99"
    locator: the EKF SLAM formulation and the history of the problem
---

EKF SLAM solves the [online SLAM](/online-slam/) problem with one [extended Kalman filter](/extended-kalman-filter/) whose state holds the robot pose and the positions of all landmarks. The belief is one Gaussian $N(\mu, \Sigma)$ over $(x, y, \theta, m_{1,x}, m_{1,y}, \dots, m_{m,x}, m_{m,y})$. A motion moves only the pose part. A reading of a landmark corrects the pose and every landmark at once, because the covariance $\Sigma$ links them all. A landmark enters the state at its first reading. This is the oldest SLAM algorithm, and the [EKF SLAM convergence theorem](/ekf-slam-convergence-theorem/) explains its behavior in the linear case. Its cost is $O(m^2)$ per reading for $m$ landmarks, because each update changes all of $\Sigma$. It differs from [EKF localization](/ekf-localization/), which has a fixed map and a 3 by 3 covariance, and from [FastSLAM](/fastslam/), which samples the path and keeps one small filter per landmark.

## In plain words

The robot keeps one best guess of where it is and of where each landmark is, and it also keeps a table that says how the errors of all these guesses depend on each other. When the robot drives, its own guess becomes less sure, and the landmark guesses stay the same. When it sees a new landmark, it adds the landmark to its list, as sure as its own position allows. When it sees a known landmark again, it corrects its own position, and through the table it also corrects every landmark that it saw from nearby. The table grows with the square of the number of landmarks, and each correction touches all of it.

## The problem

The input is a Gaussian prior on the start pose, usually the origin with zero covariance, and at each time step a control $u_t = (v_t, \omega_t)$ held for $\Delta t$ seconds and a set of readings $z_t^i = (r_t^i, \phi_t^i)$ of point landmarks. The correspondence $c_t^i$, the landmark of reading $i$, is given or must be estimated. The output after each step is a Gaussian approximation of the online SLAM posterior $p(x_t, m \mid z_{1:t}, u_{1:t}, c_{1:t})$ over the current pose and the map.

**State.** $\mu = (\mu_x, \mu_{m_1}, \dots, \mu_{m_n})$ with $\mu_x = (x, y, \theta)$, where $n$ is the number of landmarks seen so far. $\Sigma$ has the blocks $\Sigma_{xx}$ (3 by 3), $\Sigma_{xm}$ (3 by $2n$) and $\Sigma_{mm}$ ($2n$ by $2n$).

**Models.** The motion is the [velocity motion model](/velocity-motion-model/) $g(u_t, x_{t-1})$ with the control noise $M_t = \mathrm{diag}(\alpha_1 v^2 + \alpha_2 \omega^2, \alpha_3 v^2 + \alpha_4 \omega^2)$, as in [EKF localization](/ekf-localization/). The landmarks do not move. A reading of landmark $j$ follows the [landmark measurement model](/landmark-measurement-model/)

$$h(x, m_j) = \begin{pmatrix} \sqrt{q} \\ \operatorname{atan2}(\delta_y, \delta_x) - \theta \end{pmatrix}, \qquad \delta = m_j - (x, y), \quad q = \delta^\top \delta,$$

plus noise $N(0, Q)$ with $Q = \mathrm{diag}(\sigma_r^2, \sigma_\phi^2)$. The inverse model gives the landmark from a pose and a reading: $f(x, z) = (x + r \cos(\phi + \theta),\ y + r \sin(\phi + \theta))$.

## The algorithm

```pseudo id=main
EKF-SLAM(μ, Σ, u_t, z_t)                  ▷ μ = (μ_x, μ_m1, ..., μ_mn), μ_x = (x, y, θ)
L1  G ← ∂g/∂x and V ← ∂g/∂u at (u_t, μ_x);  M ← diag(α1 v² + α2 ω², α3 v² + α4 ω²)
L2  μ_x ← g(u_t, μ_x)
L3  Σ_xx ← G Σ_xx Gᵀ + V M Vᵀ
L4  Σ_xm ← G Σ_xm;  Σ_mx ← Σ_xmᵀ                ▷ Σ_mm does not change
L5  for each reading z^i = (r^i, φ^i) in z_t do
L6      j ← c^i if known, else the landmark with the smallest Mahalanobis distance, or new if it fails the gate
L7      if j is new then append f(μ_x, z^i) to μ and grow Σ (below); continue
L8      ẑ ← h(μ_x, μ_mj);  H ← ∂h/∂(x, m_j), zero in all other columns
L9      S ← H Σ Hᵀ + Q;  K ← Σ Hᵀ S⁻¹
L10     μ ← μ + K wrap(z^i - ẑ)
L11     Σ ← (I - K H) Σ
L12 return μ, Σ
```

**Line L7, a new landmark.** With $G_x = \partial f / \partial x$ (2 by 3) and $G_z = \partial f / \partial z$ (2 by 2) at $(\mu_x, z^i)$, the new landmark gets the mean $f(\mu_x, z^i)$, the cross covariance $G_x \Sigma_{x\cdot}$ with the whole old state, and the covariance $G_x \Sigma_{xx} G_x^\top + G_z Q G_z^\top$. The [correctness proof](proofs/correctness.md) shows that this is the exact posterior for a landmark with a flat prior, in the linear case. The reading is not used a second time for an update, because that would count it twice. Thrun et al. (Section 10.2) instead put all landmarks in the state from the start, with a very large initial covariance, and initialize a landmark at its first reading; the result is close to the one here.

**Line L8, the Jacobian.** With $\delta$ and $q$ as above,

$$\frac{\partial h}{\partial (x, y, \theta, m_{j,x}, m_{j,y})} = \frac{1}{q} \begin{pmatrix} -\sqrt{q}\,\delta_x & -\sqrt{q}\,\delta_y & 0 & \sqrt{q}\,\delta_x & \sqrt{q}\,\delta_y \\ \delta_y & -\delta_x & -q & -\delta_y & \delta_x \end{pmatrix}.$$

$H$ has only these 5 nonzero columns. So $\Sigma H^\top$ costs $O(n)$, but line L11 still changes every entry of $\Sigma$.

**Line L6, unknown correspondences.** For each landmark $j$ in the map, compute the innovation $\nu_j$ and $S_j$ as in lines L8 and L9, and its squared Mahalanobis distance $d_j^2 = \nu_j^\top S_j^{-1} \nu_j$. Take the landmark with the smallest $d_j^2$ if $d_j^2 \le 9.210$, the $0.99$ quantile of the chi-square distribution with 2 degrees of freedom. If no landmark passes, the reading starts a new landmark. Thrun et al. (Section 10.3) use the same rule with a threshold $\alpha$ on the distance. The code also has a second, larger threshold: a reading between the two is dropped, so that a reading of a known landmark with a large error does not create a copy. See [data association in SLAM](/data-association-slam/) and [JCBB](/joint-compatibility-branch-and-bound/) for joint tests.

## Example

Take $\alpha = (0.01, 0.005, 0.005, 0.01)$, $\sigma_r = 0.1$ m and $\sigma_\phi = 0.03$ rad. The robot starts at the origin with $\Sigma = 0$; the start pose defines the frame of the map.

**Step 1, drive.** The control is $v = 1$ m/s and $\omega = 0$ for 1 s, so $M = \mathrm{diag}(0.01, 0.005)$. Lines L2 and L3 give $\mu_x = (1, 0, 0)$ and

$$\Sigma_{xx} = \begin{pmatrix} 0.01 & 0 & 0 \\ 0 & 0.00125 & 0.0025 \\ 0 & 0.0025 & 0.005 \end{pmatrix}.$$

The heading noise moves the robot sideways, so $y$ and $\theta$ are correlated.

**Step 1, a new landmark A.** The reading is $z = (2.0, 0.5)$. Line L7 puts A at $(1 + 2 \cos 0.5,\ 2 \sin 0.5) = (2.7552, 0.9589)$ with variances $0.02313$ and $0.0305$, larger than those of the reading alone, because the uncertainty of the pose carries over. The new cross terms are not zero: for example $\mathrm{Cov}(x, m_{A,x}) = 0.01$ and $\mathrm{Cov}(\theta, m_{A,y}) = 0.01128$. The robot and the landmark are now correlated.

**Step 2, drive again.** The same control gives $\mu_x = (2, 0, 0)$. The pose variances grow to $(0.02, 0.0125, 0.01)$, so the standard deviations are $(0.141, 0.112, 0.100)$. The landmark block does not change.

**Step 2, see A again.** The reading is $z = (1.28, 0.95)$, and line L8 predicts $\hat z = (1.2206, 0.9036)$. After lines L9 to L11:

- the pose is $(2.0041, -0.0141, -0.0282)$, and its standard deviations shrink to $(0.128, 0.109, 0.084)$;
- landmark A moves to $(2.7629, 0.9790)$, and its standard deviations shrink from $(0.152, 0.175)$ to $(0.142, 0.170)$, although the reading was taken from a less certain pose;
- the correlation between $y$ and $m_{A,y}$ is $0.948$: both are now known mostly relative to each other.

The landmark improved because it is correlated with the pose at the time of its first reading, and that pose is correlated with the current one through the odometry. With many landmarks, this is how one reading corrects the whole map.

## Correctness

For linear motion and measurement models with Gaussian noise, EKF SLAM is the [Kalman filter](/kalman-filter/) on the joint state of robot and map, so its output is the exact online SLAM posterior. The [correctness proof](proofs/correctness.md) shows the three parts: the prediction moves only the pose block and the cross block (lines L2 to L4); the addition of a landmark is the exact posterior for a flat prior (line L7); and the sparse update of lines L8 to L11 equals the dense Kalman update. The tests check the last claim as a whole: on a linear model with three landmarks, the filter matches the marginal of the batch least squares solution over all poses and landmarks within $10^{-9}$.

For the nonlinear planar models, the filter uses Jacobians at the current mean, and the result is an approximation with no error bound. In simulation with the noise of the model, the tests measure a mean normalized pose error of 2.59 for 3 degrees of freedom and 2.13 for the 2 degrees of freedom of each landmark, over 10 runs of 25 steps; values near the dimension mean that the covariance matches the real error. This is a measurement for these noise levels, not a guarantee (see Pitfalls).

## Complexity

Let $m$ be the number of landmarks in the map and $k$ the number of readings in one step. Costs are in the [real RAM](/real-ram/) model.

- **Prediction:** $O(m)$. Lines L3 and L4 change only the 3 rows and 3 columns of the pose. The map block is untouched, because the landmarks do not move.
- **Update:** $O(m^2)$ per reading. $\Sigma H^\top$ costs $O(m)$ because $H$ has 5 nonzero columns, but line L11 changes all $(3 + 2m)^2$ entries of $\Sigma$. So a step costs $O(k m^2)$.
- **A new landmark:** $O(m)$ for the new rows, plus the time to grow the arrays.
- **Association:** $O(m)$ per reading for the distances, so $O(k m)$ per step. The distances use only the 5 by 5 block of $\Sigma$ of the pose and the landmark.
- **Memory:** $O(m^2)$ for $\Sigma$.

The quadratic cost is the main limit of EKF SLAM. With $m = 1000$, $\Sigma$ has about 4 million entries, and every reading changes all of them. Information filters ([EIF](/extended-information-filter/), [SEIF](/sparse-extended-information-filter/)), particle filters ([FastSLAM](/fastslam/)), submaps and graph methods ([GraphSLAM](/graphslam/)) avoid this cost in different ways.

## Properties

- **Correlations are the map.** After a while, the landmark estimates are strongly correlated with each other. Their positions relative to each other are known much better than their positions in the world frame. Dropping the cross terms to save time makes the filter overconfident and can make it diverge.
- **Monotone map uncertainty, in the linear case.** The determinant of the covariance of any set of landmarks never increases, and the covariance of each landmark stays above the covariance of the first pose. These are theorems of Dissanayake et al. (2001) for the linear Gaussian model; see the [convergence theorem](/ekf-slam-convergence-theorem/). The tests check both on random linear runs.
- **Unimodal.** The belief has one peak. It cannot keep two hypotheses about a loop closure or an association.
- **Deterministic.** The same data give the same result.
- **Order dependent, a little.** Each update relinearizes at the new mean, so the order of the readings changes the result slightly. With linear models it does not.

## Variants and improvements

- **Unknown correspondences.** Nearest neighbor with a chi-square gate, as here, or the maximum likelihood landmark (Thrun et al., Section 10.3). For many readings in one step, [joint compatibility branch and bound](/joint-compatibility-branch-and-bound/) tests the pairings together and rejects sets that are only individually compatible.
- **Information form.** The [extended information filter](/extended-information-filter/) stores $\Sigma^{-1}$. Its update is cheap, but its prediction and its mean recovery are expensive. The [sparse extended information filter](/sparse-extended-information-filter/) bounds the number of links per pose, at the cost of an approximation.
- **Submaps.** Build small independent EKF maps and join them later, so that each update is cheap. The joining needs care with the shared landmarks.
- **Unscented and iterated filters.** The [unscented Kalman filter](/unscented-kalman-filter/) replaces the Jacobians by sigma points, and the iterated EKF relinearizes the update. Both reduce linearization errors but keep the quadratic cost.
- **Consistent Jacobians.** Huang and Dissanayake (2007) relate the inconsistency to Jacobians that are evaluated at different estimates of the same quantity. Later filters fix the linearization point of each state to reduce the overconfidence.
- **Smoothing.** [GraphSLAM](/graphslam/) and [square root SAM](/square-root-sam/) keep all poses and solve the [full SLAM](/full-slam/) problem, which avoids the early fixing of linearization points and gives a sparse system.
- **Monocular SLAM.** [MonoSLAM](/monoslam/) is EKF SLAM with one camera as the only sensor.

## When to use it

Use EKF SLAM for small maps with distinct point landmarks, up to a few hundred, when a full covariance is useful, for example for active exploration or to gate associations. Use it as a reference: on small linear problems it is exact, which makes it a good test for other methods. For large maps or raw range scans, use [GraphSLAM](/graphslam/) or [pose graph optimization](/pose-graph-optimization/), [FastSLAM](/fastslam/), or [grid-based Rao-Blackwellized SLAM](/grid-based-rbpf-slam/).

## Pitfalls

- **A wrong association.** A reading matched to the wrong landmark corrects the whole map in the wrong way, and the filter cannot undo it. The gate reduces the risk; joint tests reduce it more.
- **Inconsistency of the nonlinear filter.** Julier and Uhlmann (2001) showed that for a stationary robot that observes a landmark, the nonlinear EKF SLAM reports a heading variance that keeps shrinking, although the readings carry no information about the heading. Over long runs the covariance becomes too small, so later readings fail the gate. Huang and Dissanayake (2007) analyze the cause. Check the normalized error in simulation before trusting the covariance.
- **Angles.** Wrap the bearing innovation and the heading after each update, as in [EKF localization](/ekf-localization/).
- **The first pose.** Starting with $\Sigma_{xx} = 0$ fixes the frame of the map. The pose covariance then has rank 2 after the first control, so any test that inverts it must wait one more step.
- **Symmetry and positive definiteness.** Rounding can make $\Sigma$ slightly asymmetric or indefinite after many updates. Compute each entry once and copy it, as the code does, or use the Joseph form.
- **A duplicate landmark.** With one threshold, a reading of a known landmark with a large error creates a second copy of it. A second, larger threshold for new landmarks, or a check on landmarks that are seen only once, avoids this.

## Implementations

## History

Smith and Cheeseman (1986) gave a calculus for uncertain spatial relations, with means and covariances that compound along chains of frames. Smith, Self and Cheeseman (1990) put the robot and all objects into one state vector, the stochastic map, and showed that the estimates of the objects become correlated through the robot. This is EKF SLAM. Leonard and Durrant-Whyte used the same filter with sonar on real robots in the early 1990s, and the problem got the name SLAM in the mid 1990s. Dissanayake et al. (2001) proved the convergence of the map covariance in the linear case and ran the filter outdoors with millimeter wave radar. Julier and Uhlmann (2001) gave a counterexample to its consistency in the nonlinear case, and Huang and Dissanayake (2007) analyzed it. Thrun, Burgard and Fox (2005) present EKF SLAM in Chapter 10 of Probabilistic Robotics, and Durrant-Whyte and Bailey (2006) in their tutorial.

## References
