---
tag: DRMB6N
kind: algorithm
slug: graphslam
name: GraphSLAM
aliases:
- Thrun-Montemerlo GraphSLAM
area: robotics/localization-and-slam
level: advanced
summary: Full SLAM in information form. It links all poses and landmarks in a sparse matrix, removes the landmarks by Schur complements, solves for the path, recovers the map, and relinearizes.
solves: [full-slam]
model: real-ram
complexity:
  vars: {p: the number of poses, m: the number of landmarks, k: the number of measurements, I: the number of iterations}
  time: {linearize: O(p + k), reduce: O(m p^2), solve: O(p^3 + k), total: O(I (m p^2 + p^3 + k))}
  space: {information_form: O(p + k), reduced: O(p^2)}
properties: {deterministic: true, exact: false, batch: true, local_optimum: true}
history:
  year: 2006
  people: [Sebastian Thrun, Michael Montemerlo]
  note: Thrun and Montemerlo built the information form of full SLAM, removed the map variables, and solved for the path, with large urban maps as the application. Probabilistic Robotics gives it as Chapter 11.
prereqs: [full-slam, schur-complement, gauss-newton-algorithm]
see_also: [pose-graph, pose-graph-optimization, square-root-sam, extended-information-filter, sparse-extended-information-filter, ekf-slam, factor-graph, variable-elimination]
sources:
  - paper: doi:10.1177/0278364906065387
    title: "Sebastian Thrun and Michael Montemerlo, The GraphSLAM algorithm with applications to large-scale mapping of urban structures, International Journal of Robotics Research 25(5-6), 2006, pages 403 to 429"
    locator: "the information form of the constraints, the elimination of the map variables, and the solution for the path"
  - book: isbn:9780262201629
    title: "Sebastian Thrun, Wolfram Burgard and Dieter Fox, Probabilistic Robotics, MIT Press, 2005"
    locator: "Chapter 11, The GraphSLAM Algorithm: the initialize, linearize, reduce and solve steps, and the notation of this page"
  - paper: doi:10.1023/A:1008854305733
    title: "Feng Lu and Evangelos Milios, Globally consistent range scan alignment for environment mapping, Autonomous Robots 4(4), 1997, pages 333 to 349"
    locator: "the network of pose constraints solved jointly, the idea that GraphSLAM extends to landmarks"
  - paper: doi:10.1109/MITS.2010.939925
    title: "Giorgio Grisetti, Rainer Kümmerle, Cyrill Stachniss and Wolfram Burgard, A tutorial on graph-based SLAM, IEEE Intelligent Transportation Systems Magazine 2(4), 2010, pages 31 to 43"
    locator: "the graph view of full SLAM and the Gauss-Newton solution of the linearized system"
---

GraphSLAM solves the [full SLAM problem](/full-slam/) in one batch. It turns every control and every measurement into a constraint between two variables, a pose and the next pose or a pose and a landmark. It linearizes these constraints and adds them into a sparse information matrix $\Omega$ and an information vector $\xi$ over all poses and all landmarks. It then removes the landmarks from this system by [Schur complements](/schur-complement/), solves the smaller system for the path, and recovers each landmark from the path. It repeats these steps from the new estimate until the estimate stops changing. Each pass is one [Gauss-Newton](/gauss-newton-algorithm/) step on the full SLAM cost. Thrun and Montemerlo (2006) published it, and it is Chapter 11 of Probabilistic Robotics. A [pose graph](/pose-graph/) is the special case without landmarks, and [square root SAM](/square-root-sam/) solves the same least squares problem by a factorization of the Jacobian instead of by elimination of the map.

## In plain words

The robot drives and writes down two kinds of notes: how far it thinks it moved, and where it saw each landmark from where it stood. Each note ties two things together, like a spring. GraphSLAM puts all the springs in one big table. The table is mostly empty, because each note touches only two things. To make the problem smaller, it first removes the landmarks. Each removed landmark leaves springs between all the places it was seen from. Then it finds the path where all springs are least stretched, puts the landmarks back where the path says, and does it all again from there, because the springs were only straight lines near the old guess.

## The problem

The input is the controls $u_1, \dots, u_T$, the measurements $z_i$ of landmark $c_i$ from pose $x_{t_i}$ (the correspondences are known), the motion model $x_t = g(u_t, x_{t-1}) + \varepsilon_t$ with $\varepsilon_t \sim N(0, R)$, and the measurement model $z_i = h(x_{t_i}, m_{c_i}) + \delta_i$ with $\delta_i \sim N(0, Q)$. The notation is that of Thrun, Burgard and Fox. The output is the path $x_0, \dots, x_T$ and the map $m = (m_1, \dots, m_M)$ that minimize the negative log posterior

$$J = x_0^\top \Omega_0\, x_0 + \sum_t \big(x_t - g(u_t, x_{t-1})\big)^\top R^{-1} \big(x_t - g(u_t, x_{t-1})\big) + \sum_i \big(z_i - h(x_{t_i}, m_{c_i})\big)^\top Q^{-1} \big(z_i - h(x_{t_i}, m_{c_i})\big),$$

with an anchor $\Omega_0$ that fixes $x_0$, because the measurements fix the path and the map only up to a rigid motion. On this page and in the code, the robot is planar, $x_t = (x, y, \theta)$, the control is a motion in the frame of $x_{t-1}$, the landmarks are points, and each measurement is a range and a bearing. Angle differences are wrapped to $[-\pi, \pi)$.

## The algorithm

INITIALIZE composes the controls from $x_0 = 0$ and puts each landmark where its first measurement says. The main loop runs LINEARIZE, REDUCE and SOLVE. In LINEARIZE, $G_t$ and $H_i$ are the Jacobians of $g$ and $h$ at the current estimate $\mu$, $\hat x_t = g(u_t, \mu_{t-1})$ and $\hat z_i = h(\mu_{t_i}, \mu_{c_i})$. $\tau(j)$ is the set of poses that measured landmark $j$.

```pseudo id=main
INITIALIZE(u, z)
L1  μ_0 ← 0;  μ_t ← g(u_t, μ_{t-1}) for t = 1 to T;  put each landmark at its first measurement
LINEARIZE(u, z, μ)
L2  Ω ← anchor on x_0;  ξ ← 0
L3  for t ← 1 to T do
L4      add [-G_t I]ᵀ R⁻¹ [-G_t I] to Ω at (x_{t-1}, x_t);  add [-G_t I]ᵀ R⁻¹ (x̂_t - G_t μ_{t-1}) to ξ
L5  for each measurement i do
L6      add H_iᵀ Q⁻¹ H_i to Ω at (x_{t_i}, m_{c_i});  add H_iᵀ Q⁻¹ (z_i - ẑ_i + H_i μ) to ξ
REDUCE(Ω, ξ)
L7  Ω̃ ← Ω_{x,x};  ξ̃ ← ξ_x
L8  for each landmark j do
L9      ξ̃_{τ(j)} ← ξ̃_{τ(j)} - Ω_{τ(j),j} Ω_{j,j}⁻¹ ξ_j
L10     Ω̃_{τ(j),τ(j)} ← Ω̃_{τ(j),τ(j)} - Ω_{τ(j),j} Ω_{j,j}⁻¹ Ω_{j,τ(j)}
SOLVE(Ω̃, ξ̃, Ω, ξ)
L11 Σ ← Ω̃⁻¹
L12 μ_x ← Σ ξ̃
L13 for each landmark j do
L14     μ_j ← Ω_{j,j}⁻¹ (ξ_j - Ω_{j,τ(j)} μ_{τ(j)})
GRAPHSLAM(u, z)
L15 μ ← INITIALIZE(u, z)
L16 repeat
L17     Ω, ξ ← LINEARIZE(u, z, μ)
L18     Ω̃, ξ̃ ← REDUCE(Ω, ξ)
L19     μ, Σ ← SOLVE(Ω̃, ξ̃, Ω, ξ)
L20 until μ changes by less than a tolerance
L21 return μ, Σ
```

Line L4 is the information of the linearized motion residual $x_t - G_t x_{t-1} - (\hat x_t - G_t \mu_{t-1})$, and line L6 that of the linearized measurement residual. Lines L9 and L10 touch only the poses in $\tau(j)$, because $\Omega_{x,j}$ is zero elsewhere. No factor links two landmarks, so the landmarks can be removed one at a time and in any order. Line L14 comes from the landmark row of $\Omega \mu = \xi$.

In the code, the anchor is $10^8$ on the diagonal of $x_0$ instead of infinity, the inverse is a dense Gauss-Jordan inverse, and the predicted angle $\hat\theta_t$ is moved by a multiple of $2\pi$ to lie near $\mu_t$, so that the linear system stays continuous across $\pm\pi$.

## Example

The robot drives 12 steps of 1 m with a turn of $30°$ after each step. This is a closed regular polygon of 12 sides, with the radius $1.93$ m. Five landmarks lie around it, and the robot measures each landmark within 3.5 m. The control noise has the standard deviations $0.02$ m and $0.01$ rad, and the measurement noise $0.05$ m in range and $0.02$ rad in bearing. With the seed 4, there are 42 measurements and 13 poses, so $\Omega$ is $49 \times 49$.

| | dead reckoning (INITIALIZE) | GraphSLAM |
|---|---|---|
| cost $J/2$ | 276.67 | 38.00 |
| error of the last position | 0.239 m | 0.036 m |
| error of the last heading | -0.033 rad | -0.013 rad |
| largest landmark error | 0.099 m | 0.065 m |

The estimate converged in 8 passes. The largest change of a pose coordinate was $0.21$ after the first pass, $5.2 \times 10^{-3}$ after the second, $4.2 \times 10^{-4}$ after the third, and $2.3 \times 10^{-5}$ after the fourth, which is the fast local convergence of Gauss-Newton on a problem with small residuals. The standard deviations of the last pose from $\Sigma$ are $0.023$ m, $0.030$ m and $0.014$ rad.

The example also shows the price of the reduction. Landmark 3 is seen from all 13 poses. The full $\Omega$ has 761 nonzero entries out of 2401, but after REDUCE, $\tilde\Omega$ has 1521 nonzero entries out of 1521. One landmark seen from every pose makes the reduced matrix dense.

## Correctness

The [correctness proof](proofs/correctness.md) shows three things. LINEARIZE builds the $\Omega$ and $\xi$ of the quadratic model of $J$ at $\mu$, whose minimizer is $\Omega^{-1}\xi$. REDUCE and SOLVE return exactly $\Omega^{-1}\xi$, and $\Sigma$ is the pose block of $\Omega^{-1}$, because $\tilde\Omega$ is the Schur complement of the block diagonal landmark block. A fixed point of the loop is a point where the gradient of $J$ is zero. With noise-free data, the true path and map are a fixed point with zero cost. The proof gives no global result: $J$ is not convex in the headings, and Gauss-Newton converges only from a good start. The tests check the noise-free case to $10^{-9}$, check REDUCE and SOLVE against a dense solve of the full system to $10^{-8}$, and check that every partial derivative of $J$ at the noisy solution is below $10^{-3}$.

## Complexity

Let $p = T + 1$ be the number of poses, $m$ the number of landmarks, $k$ the number of measurements, and $I$ the number of passes.

- LINEARIZE: $O(p + k)$ work. $\Omega$ has $O(p + k)$ nonzero blocks.
- REDUCE: $O(\sum_j |\tau(j)|^2)$, which is at most $O(m p^2)$. It can fill $\tilde\Omega$ completely, as in the example.
- SOLVE: $O(p^3)$ for the dense inverse, plus $O(k)$ to recover the landmarks.
- Memory: $O(p + k)$ for $\Omega$ in sparse form, and up to $O(p^2)$ for $\tilde\Omega$.

The code stores $\Omega$ as a dense matrix, so it uses $O((p + m)^2)$ memory; this keeps it short and does not change the result. The number of passes $I$ is not bounded by the analysis. In the example it was 8 to reach a change below $10^{-10}$, and 4 to reach $10^{-4}$.

## Properties

- **Batch.** It uses all data at once and recomputes from the start. It is an offline method. For an online version, see [iSAM](/isam/) and [iSAM2](/isam2/).
- **A local optimum.** Each pass is a Gauss-Newton step, so the result is a stationary point of $J$, and in general a local minimum. Bad initial headings can lead to a wrong one.
- **Exact elimination.** Removing the landmarks loses nothing: the path and its covariance are the same as from the full system. This is unlike the [sparse extended information filter](/sparse-extended-information-filter/), which drops links on purpose.
- **Known correspondences.** The basic algorithm assumes that each measurement names its landmark. Thrun and Montemerlo add a test that merges two landmarks when the information form says that they are probably the same.

## Variants and improvements

- **Without landmarks.** If the measurements are relative poses, for example from scan matching, the problem is [pose graph optimization](/pose-graph-optimization/), and REDUCE has nothing to do.
- **Factorization instead of elimination of the map.** [Square root SAM](/square-root-sam/) factors the whole Jacobian with a fill-reducing [elimination ordering](/elimination-ordering/). Removing all landmarks first is one fixed ordering, and often not the best one.
- **Sparse solvers.** Replace the dense inverse by a sparse Cholesky factorization or the [conjugate gradient method](/conjugate-gradient-method/) when only $\mu$ is needed and not all of $\Sigma$.
- **Robust costs.** Replace the squares by an [M-estimator](/m-estimator/) to limit the effect of wrong data associations.

## When to use it

Use GraphSLAM for offline mapping with landmarks and known data association, when all data is available and the path is not too long for the reduced system. For long runs where a landmark is seen from many poses, or for online use, prefer [square root SAM](/square-root-sam/) with a good ordering, or [iSAM2](/isam2/). For laser data without landmarks, use a [pose graph](/pose-graph/).

## Pitfalls

- **Unwrapped angles.** A predicted heading and the current heading can differ by $2\pi$. If the difference is not wrapped, one factor pulls the robot through a full turn.
- **A missing anchor.** Without the anchor, $\Omega$ is singular, because the whole solution can move and turn freely.
- **Dense reduction.** The reduced matrix can be dense, as in the example. Do not assume that $\tilde\Omega$ stays banded.
- **The sign in the landmark recovery.** Derive it from the landmark row of $\Omega\mu = \xi$: the term $\Omega_{j,\tau(j)}\mu_{\tau(j)}$ is subtracted from $\xi_j$.
- **Overconfident $\Sigma$.** $\Sigma$ comes from the linearization at the final estimate. It is too small when the linearization is poor or the noise models are too small.

## Implementations

## History

Lu and Milios (1997) solved jointly for a network of poses linked by scan matches, which started the graph view of SLAM. Thrun and Montemerlo (2006) named GraphSLAM, extended it to landmarks with the information form and the elimination of the map, and used it to map urban structures. Probabilistic Robotics (2005) gives it as a complete chapter. Dellaert and Kaess (2006) gave the factorization view in square root SAM, and Grisetti, Kümmerle, Stachniss and Burgard (2010) wrote a tutorial on graph-based SLAM.

## References
