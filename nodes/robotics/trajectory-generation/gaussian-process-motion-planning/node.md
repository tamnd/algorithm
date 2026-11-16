---
tag: 6FK8HV
kind: algorithm
slug: gaussian-process-motion-planning
name: Gaussian process motion planning
aliases:
- GPMP
- GPMP2
area: robotics/trajectory-generation
level: research
summary: "Represents a trajectory by a Gaussian process prior and solves planning as inference on a sparse factor graph."
solves: [trajectory-optimization]
model: real-ram
complexity:
  vars: {N: "the number of support states", k: "the number of interpolated check points per interval", m: "the number of obstacles", d: "the dimension of the configuration space", I: "the number of iterations"}
  time: {worst: O(I N ((k + 1) m d + d^3))}
  space: {extra: O(N d^2)}
properties: {deterministic: true, randomized: false, online: false, exact: false}
prereqs: [trajectory-optimization, gaussian-process, factor-graph]
see_also: [chomp, sequential-convex-trajectory-optimization, stomp, levenberg-marquardt, gauss-newton-algorithm, cubic-hermite-spline, isam2, rauch-tung-striebel-smoother]
sources:
  - paper: doi:10.1177/0278364918790369
    title: "Mustafa Mukadam, Jing Dong, Xinyan Yan, Frank Dellaert and Byron Boots, Continuous-time Gaussian process motion planning via probabilistic inference, The International Journal of Robotics Research 37(11), 2018, 1319-1340"
    locator: "the whole paper (the Gaussian process prior, the obstacle factors with a hinge loss, the interpolation between support states, and the solution on a factor graph)"
---

Gaussian process motion planning treats a trajectory as a continuous function of time with a Gaussian process prior, and turns planning into finding the most probable trajectory given that it should avoid obstacles. The prior used in GPMP2 is the constant-velocity process: white noise on the acceleration. Its states are positions and velocities, and its density is a product of factors that each connect two consecutive support states, so the problem is a sparse [factor graph](/factor-graph/). Obstacle costs are further factors, and they can be checked between support states at no extra variables, because the [Gaussian process](/gaussian-process/) gives the trajectory between support states as a fixed linear function of the two neighbors. The most probable trajectory is a nonlinear least squares problem with a block tridiagonal Hessian, solved by [Gauss-Newton](/gauss-newton-algorithm/) or [Levenberg-Marquardt](/levenberg-marquardt/) steps. Like the other methods for [trajectory optimization](/trajectory-optimization/), it is local.

## In plain words

Describe a motion by a few snapshots of position and speed, and assume the motion between snapshots is as smooth as possible, which gives a fixed curve between each pair. Smoothness has a price, and so has coming close to an obstacle. Planning means finding the snapshots with the lowest total price. Because each price depends on at most two neighboring snapshots, the system to solve at each step is a short chain, and it can be solved quickly. Obstacles can also be checked on the curve between snapshots, so few snapshots are enough. Closeness to obstacles is only a price, not a hard rule, so the result can stay a little inside the safety distance. The method improves the motion near the start and does not search for the best one.

## The problem

Input: a start state $\theta_0$ and a goal state $\theta_N$ (position and velocity), a total time $T$, $N$ intervals of length $\Delta t = T/N$, signed distance functions $\mathrm{sd}_j$ of the obstacles, a safety distance $\varepsilon$, an obstacle weight $\sigma$, and the spectral density $Q_c$ of the prior. The unknowns are the support states $\theta_1, \dots, \theta_{N-1}$ with $\theta_i = (p_i, v_i)$. Minimize

$$F = \frac12 \sum_{i=0}^{N-1} e_i^{\mathsf T} Q^{-1} e_i + \frac{1}{2\sigma^2} \sum_{\text{check points } p} \sum_j \max\bigl(0,\ \varepsilon - \mathrm{sd}_j(p)\bigr)^2,$$

with the prior error $e_i = \theta_{i+1} - \Phi\theta_i$, where

$$\Phi = \begin{pmatrix} I & \Delta t\, I \\ 0 & I \end{pmatrix}, \qquad Q = Q_c \begin{pmatrix} \tfrac{\Delta t^3}{3} I & \tfrac{\Delta t^2}{2} I \\ \tfrac{\Delta t^2}{2} I & \Delta t\, I \end{pmatrix}.$$

The check points are the support positions and $k$ points in each interval, at the positions given by the interpolation below. $F$ is minus the logarithm of the posterior density, up to a constant, so its minimizer is the most probable trajectory. This page uses a point robot in the plane; the paper also handles robot arms, where the check points are spheres on the links.

## The algorithm

```pseudo id=main
GPMP(θ_0, θ_N, N, λ, I)
L1  θ_1, …, θ_{N-1} ← states on the segment, at constant velocity
L2  for it ← 1 to I do
L3      linearize all factors at θ; H ← Σ JᵀWJ; g ← Σ JᵀWr        ▷ block tridiagonal
L4      solve (H + λI) δ = -g
L5      F′ ← F(θ + δ)
L6      if F′ < F(θ) then θ ← θ + δ; λ ← λ/10
L7      else λ ← 10λ and go back to L4
L8      if the decrease is small then stop
L9  return θ
```

Line L3 linearizes each factor. For a prior factor the error is linear in the two states it connects, with Jacobians $-\Phi$ and $I$. For an obstacle factor at a check point $p$, the residual is $\max(0, \varepsilon - \mathrm{sd}(p))/\sigma$ with the Jacobian $-\nabla\mathrm{sd}(p)^{\mathsf T}/\sigma$ times the derivative of $p$ with respect to the states, and zero where the point is farther than $\varepsilon$.

A check point at time $t_i + \tau$ between two support states has the state

$$\theta(t_i + \tau) = \Lambda\theta_i + \Psi\theta_{i+1}, \qquad \Psi = Q_\tau \Phi_{\Delta t - \tau}^{\mathsf T} Q_{\Delta t}^{-1}, \quad \Lambda = \Phi_\tau - \Psi\Phi_{\Delta t},$$

the mean of the process given the two support states. For the constant-velocity prior this is the cubic Hermite curve through the two states (proof, Theorem 1). The matrices depend only on $\tau$ and $\Delta t$, so they are computed once. Each check point involves only two neighboring support states, so the Hessian keeps its block tridiagonal form.

Lines L4 to L7 are a [Levenberg-Marquardt](/levenberg-marquardt/) step: a damped [Gauss-Newton](/gauss-newton-algorithm/) step, accepted only when the cost goes down. The system of line L4 has $4 \times 4$ blocks on the diagonal and next to it, and the code solves it by block elimination in $O(N)$ block operations. The paper solves the same sparse system with a factor graph library.

## Example

A point moves from rest at $(-1, 0)$ to rest at $(1, 0)$ in time $T = 1$ with $N = 5$ intervals, so there are four free support states. One disc of radius $0.5$ has its center at $(0, -0.15)$. The parameters are $Q_c = 1$, $\varepsilon = 0.1$, $\sigma = 0.02$, and $k = 4$ check points in each interval. The start is the straight line at constant velocity.

| iteration | $F$ | prior part | obstacle part | clearance at check points | clearance at support states |
|---|---|---|---|---|---|
| 0 | 1660.597 | 80.000 | 1580.597 | $-0.345$ | $-0.250$ |
| 1 | 64.679 | 64.679 | 0.000 | 0.129 | 0.140 |
| 2 | 60.293 | 44.537 | 15.755 | 0.047 | 0.065 |
| 3 | 44.957 | 43.837 | 1.120 | 0.083 | 0.099 |
| 4 | 43.016 | 42.077 | 0.940 | 0.082 | 0.111 |
| 5 | 42.786 | 42.256 | 0.530 | 0.086 | 0.119 |
| 7 | 42.786 | 42.255 | 0.531 | 0.086 | 0.119 |

The method stops after seven iterations. The first step jumps clear of the disc, and the later steps trade smoothness against clearance. The final clearance, $0.086$ at the check points and $0.084$ on a fine sampling of the whole curve, is below $\varepsilon$: the obstacle term is a soft cost. Without obstacles, the optimum is the cubic $p(t) = A + (B - A)(3t^2 - 2t^3)$ with prior cost exactly $24$ (proof, Theorem 2); the obstacle raises it to $42.3$.

The check points between support states matter. With $k = 0$, only the four support states are checked. The result then has $F = 38.831$ and a clearance of $0.081$ at the support states, but the curve between them comes as close as $0.021$ to the disc, because the middle of the trajectory falls between two support states.

## Correctness

The [proof](proofs/correctness.md) shows three facts. First, the prior factor $\frac12 e^{\mathsf T} Q^{-1} e$ equals the smallest value of $\frac{1}{2Q_c}\int \|p''\|^2$ over all paths that connect the two states in time $\Delta t$, and the cubic Hermite curve attains it. This explains the prior: it charges acceleration energy. Second, the interpolation formula gives exactly the state of that cubic, so the check points lie on the curve that the prior describes; without obstacles the result is the cubic of least acceleration energy. Third, every accepted step of line L6 lowers $F$, and as long as the gradient is not zero, line L7 increases $\lambda$ only finitely often before a step is accepted. Nothing guarantees a global minimum or a collision-free result. The obstacle term is a penalty, and the method is local.

## Complexity

Line L3 evaluates the signed distance at $N(k+1)$ check points for $m$ obstacles and adds small blocks, $O(N(k+1)md)$ for a configuration space of dimension $d$. Line L4 eliminates a block tridiagonal system with blocks of size $2d$, $O(Nd^3)$. So one iteration costs $O(N((k+1)md + d^3))$, and the memory is $O(Nd^2)$. Rejected steps repeat lines L4 and L5 only. The number of iterations has no useful bound; the seven of the example are a measurement.

## Properties

- **Continuous time.** The trajectory is defined at every time by the interpolation, and collisions can be checked at any time without new variables.
- **Sparse.** Each factor touches at most two neighboring support states, so each iteration is linear in $N$.
- **Few support states.** With check points between them, a few support states describe a smooth motion.
- **Soft obstacles.** The safety distance is a cost, so the result can stay inside it; a smaller $\sigma$ pushes harder.
- **Local and deterministic.** The same start gives the same result, which is a local minimum at best.

## Variants and improvements

- **Incremental replanning.** Keep the factor graph and update it with an incremental solver such as [iSAM2](/isam2/) when the goal or the obstacles change, instead of solving from scratch. The paper uses this for replanning.
- **Other priors.** Use a prior with more states, such as constant acceleration, for smoother motions; the blocks grow but stay tridiagonal.
- **Constraints as factors.** Joint limits, velocity limits and goal regions become further factors with their own weights.
- **Smoothing view.** With a linear prior and linear measurements, the same chain structure is solved by a Kalman smoother such as the [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/); here the obstacle factors are nonlinear, hence the iterations.
- **Related methods.** [CHOMP](/chomp/) uses a fixed finite-difference metric in place of the Gaussian process prior. [TrajOpt](/sequential-convex-trajectory-optimization/) treats collision as a hard constraint.

## When to use it

Use it when the motion should be smooth in continuous time, collisions must be checked between waypoints, and planning must be fast or repeated, as in replanning when the scene changes. The factor graph form also makes it easy to add estimation and planning factors in one problem. For maze-like scenes use a [sampling planner](/rapidly-exploring-random-tree/) first. When a hard safety margin is required, check the result, or use a method with constraints.

## Pitfalls

- **No check points between support states.** If line L3 checks only the support states, the curve can cut through an obstacle between them, as in the example with $k = 0$.
- **The safety distance is soft.** Line L3 charges closeness, but the result can stay inside $\varepsilon$. Use a larger $\varepsilon$ than the true margin, or a smaller $\sigma$, and check the result.
- **Weights.** The balance of $Q_c$ and $\sigma$ decides how hard the obstacles push. A very small $\sigma$ makes the system of line L4 badly scaled and the steps of line L6 small.
- **Gradients of the distance.** At the center of a disc, or with a coarse distance field, the gradient in line L3 is zero or wrong, and the method can stall inside an obstacle.
- **Local minima.** The start of line L1 decides on which side of an obstacle the result passes.

## Implementations

## History

Mustafa Mukadam, Xinyan Yan and Byron Boots introduced Gaussian process motion planning in a conference paper. It used a Gaussian process prior of the kind developed for continuous-time state estimation, where the same sparse structure had been used to estimate trajectories. GPMP2, with Jing Dong and Frank Dellaert, followed in a conference paper and in the 2018 journal paper. It replaced the earlier optimizer with inference on a factor graph, which allowed incremental replanning with iSAM2.

## References
