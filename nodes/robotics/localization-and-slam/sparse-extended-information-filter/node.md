---
tag: 1KKHWC
kind: algorithm
slug: sparse-extended-information-filter
name: Sparse extended information filter
aliases:
- SEIF
area: robotics/localization-and-slam
level: advanced
summary: Online SLAM in information form that bounds the landmarks linked to the robot. The bound gives near constant time steps, but its sparsification is an approximation that makes the map overconfident.
solves: [online-slam]
model: real-ram
complexity:
  vars: {k: the bound on the active landmarks, n: the number of landmarks}
  time: {motion: O(k^3), update: O(1), sparsification: O(k^3), mean: O(k^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: false, online: true, recursive: true}
history:
  year: 2004
  people: [Sebastian Thrun, Yufeng Liu, Daphne Koller, Andrew Y. Ng, Zoubin Ghahramani, Hugh Durrant-Whyte]
  note: Thrun et al. (2004) bounded the landmarks linked to the pose by a sparsification step. Eustice, Walter and Leonard (2005) showed that this step makes the global map overconfident.
prereqs: [schur-complement, extended-information-filter, ekf-slam]
see_also: [extended-information-filter, ekf-slam, fastslam, graphslam, isam2, gauss-seidel-method, conditional-independence, sparse-matrix]
sources:
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 12 (the sparse extended information filter)"
  - paper: "Sebastian Thrun, Yufeng Liu, Daphne Koller, Andrew Y. Ng, Zoubin Ghahramani and Hugh Durrant-Whyte, Simultaneous localization and mapping with sparse extended information filters, International Journal of Robotics Research 23(7-8), 2004, pages 693 to 716"
    locator: the SEIF, its motion update, measurement update, sparsification and mean recovery
  - paper: doi:10.1109/IROS.2005.1545053
    title: "Ryan M. Eustice, Matthew R. Walter and John J. Leonard, Sparse extended information filters: insights into sparsification, IEEE/RSJ International Conference on Intelligent Robots and Systems, 2005, pages 3281 to 3288"
    locator: the analysis of the sparsification step and the experiments on the consistency of the global and the relative map
  - paper: "Matthew R. Walter, Ryan M. Eustice and John J. Leonard, Exactly sparse extended information filters for feature-based SLAM, International Journal of Robotics Research 26(4), 2007, pages 335 to 359"
    locator: the exactly sparse extended information filter (ESEIF)
---

The sparse extended information filter (SEIF) solves [online SLAM](/online-slam/) in information form, as the [extended information filter](/extended-information-filter/) (EIF) does, but it keeps the information matrix $\Omega$ sparse. A landmark is active if $\Omega$ links it to the robot pose. Each motion step links all active landmarks to each other, which is how the EIF matrix fills in. The SEIF keeps at most $k$ landmarks active: when there are more, a sparsification step removes the links from the pose to the oldest ones. This step is an approximation, while the EIF is exact up to linearization. With a bounded active set and sparse storage, the motion step, the update and the sparsification touch a constant number of entries. The price is an estimate that is overconfident, and a mean that the filter recovers only approximately.

## In plain words

The filter keeps a table of how much it knows about the robot and about each landmark, and how they relate. When the robot drives, everything that it relates to the robot becomes related to everything else, so the table fills up and becomes slow to work with. The filter limits how many landmarks may be related to the robot at the same time. When one more is seen, it cuts the relation to the landmark seen longest ago, and moves that knowledge to the map. This cut keeps the work per step small and does not change the best guess. But it pretends that some map knowledge is exact, so the filter believes its map more than it should.

## The problem

The input is the belief at time $t-1$ in information form, $\Omega$ and $\xi = \Omega \mu$, an estimate of the mean $\mu$, the list of active landmarks, a control $u_t$ and the readings $z_t$ with known correspondences. The motion model $x_t = g(u_t, x_{t-1}) + w$ has the noise $w \sim N(0, R_t)$ on the pose, and a reading of landmark $j$ is $z = h(x_t, m_j) + v$ with $v \sim N(0, Q)$. The output is the belief at time $t$ in the same form, with at most $k$ active landmarks. The state is the pose and the landmarks, as in [EKF SLAM](/ekf-slam/).

## The algorithm

```pseudo id=main
SEIF(ξ, Ω, μ, u_t, z_t)
L1  δ, G_x ← motion offset and pose Jacobian at μ                  ▷ μ_x moves to μ_x + δ
L2  Φ ← Tᵀ Ω T, with T = G_x⁻¹ on the pose block and I elsewhere
L3  κ ← Φ F_xᵀ R_t (I + F_x Φ F_xᵀ R_t)⁻¹ F_x Φ
L4  ξ ← ξ + (Φ - κ - Ω) μ + (Φ - κ) F_xᵀ δ;  Ω ← Φ - κ
L5  μ_x ← μ_x + δ
L6  for each reading z^i of landmark j in z_t do
L7      if m_j is new then add m_j with zero information and μ_j from z^i
L8      H ← ∂h/∂(x, m_j) at μ
L9      Ω ← Ω + Hᵀ Q⁻¹ H;  ξ ← ξ + Hᵀ Q⁻¹ (z^i - h(μ) + H μ);  mark m_j as active and most recent
L10 if more than k landmarks are active then
L11     m_0 ← the active landmarks seen least recently, beyond k;  m_+ ← the other active ones
L12     Ω̃ ← Ω_1 - Ω_2 + Ω_3;  ξ ← ξ + (Ω̃ - Ω) μ;  Ω ← Ω̃
L13 for each block b in (the pose with m_+, then a few passive landmarks) do μ_b ← Ω_bb⁻¹ (ξ_b - Ω_b,rest μ_rest)
L14 return ξ, Ω, μ
```

$F_x$ selects the pose from the state. Lines L1 to L5 are the EIF prediction in a form that touches only the pose and the active landmarks. $\Phi$ moves the information to the new pose, and $\kappa$ removes what the motion noise destroys. Lines L8 and L9 are the EIF update, linearized at the estimate $\mu$, and the innovation $z^i - h(\mu)$ has its bearing wrapped.

**Line L12.** Let $m_-$ be the passive landmarks. The step replaces the belief $p(x \mid m_0, m_+, m_-) \, p(m)$ by $p(x \mid m_+, m_- = \mu_-) \, p(m)$. In matrix form, with $S$ the pose, $m_0$ and $m_+$:

- $\Omega_1$ is the [Schur complement](/schur-complement/) of $m_0$ in $\Omega_{SS}$, the information of $(x, m_+)$ given $m_-$;
- $\Omega_2$ is the Schur complement of $(x, m_0)$ in $\Omega_{SS}$, the information of $m_+$ given $m_-$;
- $\Omega_3$ is the Schur complement of $x$ in $\Omega$, the information of the map.

$\Omega_1 - \Omega_2$ is the conditional of the pose, which has no entry for $m_0$, and $\Omega_3$ has no entry for the pose. So the links from the pose to $m_0$ become zero. The change of $\xi$ keeps the mean.

**Line L13.** The filter does not store $\Omega^{-1}$, so it cannot read the mean. Each block solve sets $\mu_b$ to the best value with the other entries fixed. The code solves the pose with the active landmarks as one block, and then visits a few passive landmarks in turn. This is block [coordinate descent](/coordinate-descent/), one sweep per step. With one block per variable and no joint block, the error of the mean was up to 0.55 m in our runs; the joint block brings it close to zero.

## Example

Take the 1-D example at the end of the [EIF page](/extended-information-filter/): the robot at $x$ and the landmarks $A$ and $B$ on a line, with

$$\Omega = \begin{pmatrix} 85 & -35 & -10 \\ -35 & 47.5 & -2.5 \\ -10 & -2.5 & 22.5 \end{pmatrix}, \qquad \xi = (-33.75, 46.25, 97.5), \qquad \mu = (1.0056, 1.9778, 5.0).$$

Both landmarks are active. Let $k = 1$: $B$, seen least recently, goes to $m_0$, and $m_+ = \{A\}$. There is no passive landmark. The three pieces of line L12 are $\Omega_1 = \begin{pmatrix} 80.5556 & -36.1111 \\ -36.1111 & 47.2222 \end{pmatrix}$ on $(x, A)$, $\Omega_2 = 31.0345$ on $A$, and $\Omega_3 = \begin{pmatrix} 33.0882 & -6.6176 \\ -6.6176 & 21.3235 \end{pmatrix}$ on $(A, B)$. The sum is

$$\tilde\Omega = \begin{pmatrix} 80.5556 & -36.1111 & 0 \\ -36.1111 & 49.2760 & -6.6176 \\ 0 & -6.6176 & 21.3235 \end{pmatrix}, \qquad \tilde\xi = (9.5833, 28.0570, 93.5294).$$

The link between $x$ and $B$ is now zero, and $\tilde\Omega^{-1} \tilde\xi = \mu$, so the mean does not change. The standard deviations stay at 0.137, 0.180 and 0.224, and the covariance of $(x, A)$ and of $(A, B)$ also stays. Only the covariance of $x$ and $B$ changes, from 0.0100 to 0.0045: given $A$, the filter now treats the pose and $B$ as independent. In this example nothing becomes overconfident, because no landmark is passive. In a real map, $m_-$ is not empty, and the conditional at $m_- = \mu_-$ treats the passive landmarks as known.

## Correctness

The [correctness proof](proofs/correctness.md) shows the following. The motion step equals the EIF prediction exactly, by a matrix inversion identity that also holds for a singular $R_t$, and it changes only the block of the pose and the active landmarks. The update is the EIF update. The sparsification gives zero links from the pose to $m_0$ and to the passive landmarks, a positive definite $\Omega$, the same mean and the same marginal of the map. If no landmark is passive, the marginal of the pose with $m_+$ is also exact. The mean recovery never increases $\tfrac12 \mu^\top \Omega \mu - \xi^\top \mu$ and has the exact mean as a fixed point.

What the proof does not give is consistency. Conditioning on $m_- = \mu_-$ removes the uncertainty of the passive landmarks from the pose conditional. On random matrices, this does not always shrink the marginal variances, so overconfidence is not a theorem. It is a measurement: Eustice, Walter and Leonard (2005) found the global map overconfident and the map relative to the robot close to consistent. The tests compare the step with dense formulas and a dense EIF, and measure the effect in simulation.

## Complexity

The code stores $\Omega$ as dense rows to stay short. The counts below assume a sparse store, which the SEIF needs.

- **Motion (lines L1 to L5):** $O(k^3)$ on the block of the pose and the active landmarks, so constant for a fixed $k$. The dense EIF needs $O(n^2)$ or more.
- **Update (lines L6 to L9):** $O(1)$ per reading, plus the lookup of the landmark.
- **Sparsification (lines L10 to L12):** $O(k^3)$, on the block $S$.
- **Mean (line L13):** $O(k^3)$ for the joint block, plus a few passive blocks, each one a scan of its row of $\Omega$. A row is short when each landmark links to few others, which holds for a local map but is not guaranteed.
- **Memory:** the number of nonzero entries of $\Omega$. Landmarks that were active at the same time stay linked, so this is near $O(n)$ for a robot that sees few landmarks at a time, and $O(n^2)$ in the worst case.

So the constant time claim of the SEIF holds for the motion, the update and the sparsification, with a bounded active set and a sparse store. It does not hold for an exact mean, which needs a sparse solve of the full system.

## Properties

- **Approximate.** The sparsification changes the belief. The bound $k$ trades speed for accuracy.
- **Overconfident in practice (measurement).** In the test file, 6 runs of 30 steps with 10 landmarks give a mean normalized landmark error (NEES, 2 for a consistent filter) of 1.78 without sparsification, 1.88 with $k = 4$ and 2.60 with $k = 3$. The mean landmark errors are 0.22 m, 0.22 m and 0.27 m. In 20 runs of 40 steps with $k = 2$, the median NEES was 5.2, and two runs reached 250 and 14644, with a small covariance and a large error.
- **The mean is approximate.** Each step does one sweep of block coordinate descent. The error of the mean then enters the linearization of the next steps.
- **Additive readings.** As in the EIF, a reading changes only the pose and one landmark, and readings can be added in any order.
- **No zero pattern for old poses.** The SEIF keeps only the current pose. Methods that keep the whole path, as [GraphSLAM](/graphslam/) and [iSAM2](/isam2/), get an exactly sparse matrix without an approximation.

## Variants and improvements

- **Exactly sparse extended information filter (ESEIF).** Walter, Eustice and Leonard (2007) control the number of active landmarks by marginalizing out the pose and relocating it from a few readings, so that the sparsity needs no approximate conditional.
- **Choice of $m_0$.** The code deactivates the landmarks seen least recently. Other rules choose by distance or by the size of the link.
- **Exact mean on demand.** A sparse Cholesky or [conjugate gradient](/conjugate-gradient-method/) solve gives the exact mean when it matters, for example before data association or a loop closure.
- **Multi-robot merging.** Because readings add, the information of several robots can be merged by adding their matrices, after the robots agree on a common frame.

## When to use it

The SEIF matters mostly as a step in the history of SLAM: it showed that the information form can be sparse and that each step can then cost constant time. For a new system, prefer [FastSLAM](/fastslam/) for many landmarks with a filter, or a smoothing back end such as [GraphSLAM](/graphslam/) or [iSAM2](/isam2/), which gets sparsity without an approximation. Use the SEIF when you need a filter with a fixed cost per step and can accept an overconfident global map, for example if you use mainly the map near the robot.

## Pitfalls

- **Overconfidence.** The covariance of the global map is too small. A gate for data association that uses it rejects true matches. Check the estimate with a ground truth run before trusting it.
- **A stale mean.** Lines L1, L8 and L9 linearize at $\mu$. If the mean recovery is too weak, the linearization drifts. Solve the pose and the active landmarks jointly.
- **The vector and the mean must agree.** Each change of $\Omega$ must update $\xi$ with the same $\mu$. Do not wrap the heading in $\mu$ alone: $\xi$ encodes it too.
- **A link left behind.** Rounding leaves tiny values in the entries that line L12 sets to zero. Write exact zeros, or the sparse store fills in again.
- **New landmarks.** A landmark with zero information has no mean in $\Omega^{-1} \xi$ until a reading arrives. Set its mean from the reading at line L7.

## Implementations

## History

Thrun, Liu, Koller, Ng, Ghahramani and Durrant-Whyte (2004) observed that the normalized information matrix of the EIF in SLAM has a few strong entries and many weak ones. They proposed the SEIF, which bounds the active landmarks, keeps $\Omega$ sparse by the sparsification step, and recovers the mean by a few steps of an iterative method. Thrun, Burgard and Fox present it in Chapter 12 of Probabilistic Robotics (2005). Eustice, Walter and Leonard (2005) analyzed the sparsification and showed that it makes the global map overconfident. Walter, Eustice and Leonard (2007) proposed the exactly sparse ESEIF. Later work moved to smoothing over the whole path, where the information matrix is sparse without an approximation.

## References
