---
tag: 2F4S7V
kind: algorithm
slug: stomp
name: STOMP
aliases:
- stochastic trajectory optimization for motion planning
area: robotics/trajectory-generation
level: advanced
summary: "Improves a trajectory by sampling noisy variants, weighting them by cost, and averaging, so the cost needs no gradient."
solves: [trajectory-optimization]
model: real-ram
complexity:
  vars: {n: "the number of waypoints", d: "the dimension of the configuration space", K: "the number of samples per iteration", C: "the time to evaluate the state cost at one waypoint", I: "the number of iterations"}
  time: {worst: O(I (K n (d + C) + n^2 d))}
  space: {extra: O(K n d + n^2)}
properties: {deterministic: false, randomized: true, online: false, exact: false}
prereqs: [trajectory-optimization, chomp]
see_also: [sequential-convex-trajectory-optimization, gaussian-process-motion-planning, cross-entropy-method, elastic-bands, tridiagonal-system-solving, rapidly-exploring-random-tree]
sources:
  - paper: doi:10.1109/ICRA.2011.5980280
    title: "Mrinal Kalakrishnan, Sachin Chitta, Evangelos Theodorou, Peter Pastor and Stefan Schaal, STOMP: Stochastic trajectory optimization for motion planning, IEEE International Conference on Robotics and Automation (ICRA), 2011, 4569-4574"
    locator: "the whole paper (the original method)"
  - paper: doi:10.1177/0278364913488805
    title: "Matt Zucker, Nathan Ratliff, Anca D. Dragan, Mihail Pivtoraiko, Matthew Klingensmith, Christopher M. Dellin, J. Andrew Bagnell and Siddhartha S. Srinivasa, CHOMP: Covariant Hamiltonian optimization for motion planning, The International Journal of Robotics Research 32(9-10), 2013, 1164-1193"
    locator: "Sections 3.4 and 3.5 (the finite-difference smoothness matrix and steps measured in its norm, which STOMP also uses)"
---

STOMP improves a robot trajectory without gradients. In each iteration it adds random smooth noise to the current trajectory several times, evaluates the cost of each noisy copy at every waypoint, and moves each waypoint toward the noisy copies that were cheap there. The noise is drawn from a Gaussian whose covariance is the inverse of a smoothness matrix, the same kind of finite-difference matrix that [CHOMP](/chomp/) uses for its steps, so the samples are smooth curves and not jagged ones. Because only cost values are used, the cost can be a step function, a collision count, or the output of a simulator. Like all methods for [trajectory optimization](/trajectory-optimization/), STOMP is local, and it has no convergence guarantee; the implementation keeps the best trajectory it has seen.

## In plain words

Lay a chain of beads from start to goal. Shake the chain gently many times, each time in a smooth random way, and note for every bead where it was cheap to be. Then move every bead toward the places where its shaken copies did well, and smooth the move so the chain stays smooth. Repeat. Nothing needs to know which way is downhill; it is enough to compare a few tries. The price is randomness: the chain wanders, and once all the tries look the same it keeps wandering without a goal. So the method remembers the best chain it has seen and returns that one. It can still get stuck in a poor local solution, and it does not promise a collision-free result.

## The problem

Input: a start $q_0$ and a goal $q_{n+1}$ in $\mathbb R^d$, a number $n$ of free waypoints $\theta = (\theta_1, \dots, \theta_n)$, a state cost $q(\theta_t) \ge 0$ that can be evaluated but need not be differentiable, and a weight $w > 0$ for smoothness. Let $A$ be the $n \times n$ second-difference matrix, with $-2$ on the diagonal and $1$ next to it, and $R = A^{\mathsf T} A$. The total cost is

$$Q(\theta) = \sum_{t=1}^n q(\theta_t) + \frac w2 \sum_{t=1}^n \|\theta_{t-1} - 2\theta_t + \theta_{t+1}\|^2,$$

with $\theta_0 = q_0$ and $\theta_{n+1} = q_{n+1}$; the second sum is the sum of squared accelerations. Output: a trajectory with a small $Q$. Nothing guarantees a minimum.

This page uses a point robot in the plane ($d = 2$) and, for discs, the state cost $q(p) = \sum_j \max(0, \text{margin} + r_j - \|p - o_j\|)$, which is positive near or inside a disc. The algorithm never uses its gradient.

## The algorithm

```pseudo id=main
STOMP(θ, K, λ, σ, I)
L1  for i ← 1 to I do
L2      for k ← 1 to K do
L3          draw ε_k ~ N(0, σ² R⁻¹) for each coordinate; θ̃_k ← θ + ε_k
L4          S_{k,t} ← q(θ̃_{k,t}) for t = 1, …, n
L5      for t ← 1 to n do
L6          P_{k,t} ← exp(-S_{k,t}/λ) / Σ_j exp(-S_{j,t}/λ) for k = 1, …, K
L7          δ̃_t ← Σ_k P_{k,t} ε_{k,t}
L8      θ ← θ + M δ̃                                  ▷ smooth the update
L9      if Q(θ) < Q(best) then best ← θ
L10 return best
```

Line L3 draws smooth noise. With $z \sim N(0, I)$, the vector $\sigma A^{-1} z$ has covariance $\sigma^2 R^{-1}$, and $A$ is tridiagonal, so one sample costs $O(n)$ per coordinate with the [Thomas algorithm](/tridiagonal-system-solving/). Noise with large accelerations has a small density, so the samples are smooth bumps that vanish at the fixed ends. Line L4 evaluates the state cost of each noisy copy at each waypoint; this is the only place the cost enters, and only its values are used.

Lines L5 to L7 are the core. At each waypoint separately, the costs of the $K$ samples become weights by a softmax with temperature $\lambda$: a sample that is cheap at waypoint $t$ gets a large weight there. The update $\tilde\delta_t$ is the weighted average of the noise at waypoint $t$. Because the weights are computed per waypoint, a sample that is good in one part of the trajectory and bad in another helps only where it is good. The code subtracts the smallest cost before the exponential; this does not change the weights and prevents overflow.

Line L8 smooths the update with a matrix $M$ built from $R^{-1}$, because the per-waypoint averages of line L7 can be rough. This page follows a common choice: the columns of $R^{-1}$, each scaled so that its largest entry is $1/n$. Then each waypoint moves by at most the largest noise value of the iteration (proof, Step 4). Line L9 keeps the best iterate by the total cost $Q$, which includes the smoothness term that lines L4 to L7 ignore.

## Example

A point moves from $(-1, 0)$ to $(1, 0)$ with $n = 19$ waypoints. One disc of radius $0.5$ has its center at $(0, -0.15)$, so the straight start line cuts it $0.35$ deep. The state cost uses a margin of $0.1$. The parameters are $K = 20$, $\sigma = 0.02$, $\lambda = 0.05$, $w = 10$, and the random seed is 2011.

| iteration | $Q$ of the iterate | smallest clearance | height of the middle waypoint |
|---|---|---|---|
| 0 | 3.0202 | $-0.350$ | 0.000 |
| 1 | 1.9150 | $-0.185$ | 0.165 |
| 2 | 1.2449 | $-0.097$ | 0.253 |
| 5 | 0.5744 | $-0.008$ | 0.344 |
| 7 | 0.0075 | 0.110 | 0.477 |
| 10 | 0.0102 | 0.197 | 0.565 |
| 20 | 0.0211 | 0.307 | 0.800 |
| 50 | 0.0380 | 0.438 | 1.102 |
| 100 | 0.0459 | 0.420 | 1.184 |

The trajectory climbs over the side of the disc away from its center and leaves the margin after seven iterations. $Q$ is not monotone: it is $0.5244$ after iteration 3, $0.4198$ after iteration 4, and $0.5744$ after iteration 5. Once the trajectory is clear of the margin, more and more samples have state cost zero at every waypoint; where all samples cost zero the weights are uniform and the update is the smoothed mean of the noise. The iterate then drifts at random, upward in this run, and $Q$ grows again through the smoothness term. Line L9 returns the iterate of iteration 7, with $Q = 0.0075$ and clearance $0.110$.

With a cost that has no useful gradient at all, $q(p) = 1$ within distance $0.6$ of the disc center and $0$ elsewhere, the start line costs $11$ (eleven waypoints are inside). With the same parameters and seed 7, sixty iterations return a trajectory with $Q = 0.0086$ and clearance $0.173$.

## Correctness

STOMP has no convergence guarantee, and the [proof](proofs/correctness.md) does not claim one. It proves what holds for every run. The noise of line L3 has covariance $\sigma^2 R^{-1}$. The weights are positive, sum to one, favor cheaper samples, and do not change when a constant is added to the costs. Each update moves a waypoint by at most the largest noise value of the iteration, and the ends never move. When the costs at every waypoint are equal, the expected update is zero, so the iterates perform a random walk; this is the drift of the example. Finally, the returned trajectory has the smallest $Q$ among all iterates, so it is never worse than the start. Nothing is proved about collisions: if no sample ever finds a cheaper position, the trajectory stays in collision.

## Complexity

One iteration draws $K$ samples at $O(nd)$ each, evaluates the state cost at $Kn$ points at $O(C)$ each, computes $Kn$ weights and averages, and multiplies by the dense matrix $M$ at $O(n^2 d)$. So one iteration costs $O(Kn(d + C) + n^2 d)$, and $M$ is computed once in $O(n^2)$ with $2n$ tridiagonal solves. The memory is $O(Knd)$ for the samples and $O(n^2)$ for $M$. The cost evaluations usually dominate, because $C$ includes collision checks of the whole robot.

There is no bound on the number of iterations, and the seven iterations of the example are a measurement of one run with one seed.

## Properties

- **Gradient-free.** Only values of the state cost are used, so costs from collision checkers, step functions and simulations work.
- **Local.** The samples explore only near the current trajectory, with a spread set by $\sigma$.
- **Randomized.** Different seeds give different results; the runs are reproducible only with a fixed seed.
- **Not monotone.** $Q$ of the iterates can go up; keeping the best iterate makes the returned value monotone in the number of iterations.
- **Smooth updates.** The noise and the update are shaped by $R^{-1}$, so trajectories stay smooth and the ends stay fixed.
- **Parallel.** The $K$ samples are independent and can be evaluated at the same time.

## Variants and improvements

- **Reuse of samples.** Keep the best samples of earlier iterations, with their costs updated, so fewer new samples are needed per iteration.
- **Normalized costs.** Rescale the costs at each waypoint by their range before line L6, so that the temperature does not depend on the scale of the cost.
- **Noise schedule.** Shrink $\sigma$ over the iterations, so that the drift of the example dies out near the end.
- **Constraints.** Add constraint violations to the state cost as penalties; there is no hard constraint handling in the basic method.
- **Related methods.** The [cross-entropy method](/cross-entropy-method/) is another sampling optimizer, which refits a distribution to the best samples instead of averaging with weights. [CHOMP](/chomp/) uses the same smoothness matrix but follows gradients. [TrajOpt](/sequential-convex-trajectory-optimization/) and [GPMP2](/gaussian-process-motion-planning/) use gradients and handle collisions more precisely.

## When to use it

Use STOMP when the cost has no useful gradient: a collision checker that only says yes or no, costs from a physics simulation, or terms such as torque limits that are easy to evaluate and hard to differentiate. It is also easy to implement for a new cost. Prefer a gradient method such as [CHOMP](/chomp/) or [TrajOpt](/sequential-convex-trajectory-optimization/) when gradients are available and cheap, because they need far fewer cost evaluations. For maze-like problems use a [sampling planner](/rapidly-exploring-random-tree/) first.

## Pitfalls

- **The temperature.** If $\lambda$ in line L6 is too small, one sample takes all the weight and the update is as noisy as a single sample; if it is too large, all samples get almost the same weight and the update is the mean noise, which carries no information.
- **The noise level.** If $\sigma$ in line L3 is too small, no sample reaches a cheaper region and the trajectory does not move out of a deep obstacle; if it is too large, the samples are far from the trajectory and the averages are rough.
- **Drift.** Once the state costs of line L4 are flat, line L8 adds a random walk. Without line L9 the result would depend on when the loop stops.
- **Thin obstacles.** Line L4 evaluates the cost only at the waypoints, so a thin obstacle between two waypoints is not seen. Check the segments, or use enough waypoints.
- **Weights are tuning.** The parameters of the original paper (the number of samples, the noise level, the temperature) are chosen for its experiments; they are rules of thumb, not derived values, and other scenes need other values.

## Implementations

## History

Mrinal Kalakrishnan, Sachin Chitta, Evangelos Theodorou, Peter Pastor and Stefan Schaal presented STOMP at ICRA 2011. It took the smoothness matrix and the idea of measuring steps in its norm from [CHOMP](/chomp/), and the weighted averaging of sampled noise from the path integral approach to reinforcement learning developed by Theodorou, Buchli and Schaal. A STOMP planner was added to the MoveIt motion planning framework of ROS, where it is used next to CHOMP and sampling planners.

## References
