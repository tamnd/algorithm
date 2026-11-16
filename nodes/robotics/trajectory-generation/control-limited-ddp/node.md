---
tag: DH08X0
kind: algorithm
slug: control-limited-ddp
name: Control-limited differential dynamic programming
aliases:
- box-constrained DDP
area: robotics/trajectory-generation
level: research
summary: "Tassa's differential dynamic programming that keeps the controls in a box by solving a small box-constrained quadratic program in each backward step."
solves: [trajectory-optimization]
model: real-ram
complexity:
  vars: {N: "the number of time steps", n: "the state dimension", m: "the control dimension", p: "the number of iterations of the box solver per stage", F: "the time to evaluate the dynamics and their Jacobians once", I: "the number of iterations"}
  time: {worst: O(I N (n^3 + p m^3 + F))}
  space: {extra: O(N n m + n^2)}
properties: {deterministic: true, randomized: false, online: false, exact: false}
prereqs: [trajectory-optimization, finite-horizon-lqr, quadratic-programming]
see_also: [lqr-problem, optimal-control-problem, nonlinear-mpc, projected-gradient-descent, kkt-conditions, shooting-method, sequential-convex-trajectory-optimization, contact-implicit-trajectory-optimization]
sources:
  - paper: doi:10.1109/ICRA.2014.6907001
    title: "Yuval Tassa, Nicolas Mansard and Emo Todorov, Control-limited differential dynamic programming, IEEE International Conference on Robotics and Automation (ICRA), 2014, 1168-1175"
    locator: "the whole paper (the box-constrained backward pass and the clamped feedback gains)"
  - paper: doi:10.1080/00207176608921369
    title: "David Q. Mayne, A second-order gradient method for determining optimal trajectories of non-linear discrete-time systems, International Journal of Control 3(1), 1966, 85-95"
    locator: "the whole paper (the original method)"
  - book: isbn:9780444000705
    title: "David H. Jacobson and David Q. Mayne, Differential Dynamic Programming, American Elsevier, 1970"
    locator: "the book as a whole (the classical theory of the method)"
---

Differential dynamic programming (DDP) improves a control sequence for a nonlinear system by a backward pass and a forward pass. The backward pass builds a quadratic model of the cost-to-go at each time step, from the last step to the first, and gets from it a change of the control and a feedback gain; the forward pass simulates the system with the new controls. The control-limited version of Tassa, Mansard and Todorov keeps every control inside a box $lo \le u \le hi$. At each step of the backward pass it solves a small quadratic program with box constraints, and the feedback gain acts only on the controls that are not at a bound. The cost goes down at every accepted iteration and the controls stay in the box, but the method is local: it finds a solution near its start, with no guarantee of a global minimum.

## In plain words

Imagine you drive a car along a planned route and want to improve the plan. Start at the end of the route and work backward: at each moment, ask how the remaining cost would change if you steered a little differently, and write down the best small correction together with a rule for how to react if the car is a bit off course. Then drive the route again with these corrections. Repeat until nothing improves. The control-limited version respects the limits of the car. If the best correction wants more steering than the wheel allows, it uses the full lock instead, and the reaction rule stops using that wheel, because it cannot turn any further. The result keeps every command within its limits and is a good plan near the first guess, not always the best plan overall.

## The problem

Input: discrete dynamics $x_{k+1} = f(x_k, u_k)$ with a start $x_0 \in \mathbb R^n$, a horizon of $N$ steps, a running cost $\ell(x, u)$ and a final cost $\ell_f(x)$, and bounds $lo \le hi$ in $\mathbb R^m$. Output: controls $u_0, \dots, u_{N-1}$ with $lo \le u_k \le hi$ that make

$$J(U) = \sum_{k=0}^{N-1} \ell(x_k, u_k) + \ell_f(x_N)$$

small. This is a [trajectory optimization](/trajectory-optimization/) problem with box limits on the controls, such as torque limits of motors. Without the box and with linear dynamics and quadratic costs it is the [LQR problem](/lqr-problem/).

The code uses the quadratic cost $\ell(x, u) = \frac12 (x - g)^{\mathsf T} Q (x - g) + \frac12 u^{\mathsf T} R u$ and $\ell_f(x) = \frac12 (x - g)^{\mathsf T} Q_f (x - g)$. It uses only the first derivatives $A_k = f_x$ and $B_k = f_u$ of the dynamics, the Gauss-Newton form that is often called iLQR; the full second-order form adds terms with second derivatives of $f$ to the quadratic model, and the handling of the box is the same.

## The algorithm

```pseudo id=main
CONTROL-LIMITED-DDP(x_0, U, lo, hi)
L1  X ← simulate U from x_0;  μ ← 0
L2  repeat
L3      V_x ← ∇ℓ_f(x_N);  V_xx ← ∇²ℓ_f(x_N)
L4      for k ← N - 1 down to 0 do
L5          form Q_x, Q_u, Q_xx, Q_uu, Q_ux at (x_k, u_k);  H ← Q_uu + μI  (if H is not positive definite: μ ← max(10μ, μ_min), go to L2)
L6          k_k, F ← minimize ½ δᵀHδ + Q_uᵀδ subject to lo - u_k ≤ δ ≤ hi - u_k;  F ← the free indices
L7          K_k ← rows F: -H_FF⁻¹ (Q_ux)_F;  other rows: 0
L8          V_x ← Q_x + K_kᵀQ_uu k_k + K_kᵀQ_u + Q_uxᵀk_k;  V_xx ← Q_xx + K_kᵀQ_uu K_k + K_kᵀQ_ux + Q_uxᵀK_k
L9      if -ΔV(1) < tol then stop
L10     for α ← 1, 1/2, 1/4, … (at most 12 values) do
L11         x̂_0 ← x_0;  û_k ← clamp(u_k + α k_k + K_k (x̂_k - x_k));  x̂_{k+1} ← f(x̂_k, û_k)
L12         if J(Û) - J(U) ≤ c ΔV(α) then U, X ← Û, X̂;  μ ← μ/10 (0 below μ_min);  go to L2
L13     μ ← max(10μ, μ_min)
L14 return U, X
```

Here $\Delta V(\alpha) = \sum_k \bigl(\alpha\, k_k^{\mathsf T} Q_u + \frac12 \alpha^2 k_k^{\mathsf T} H k_k\bigr)$ is the change of the cost that the quadratic models predict, and the code uses $c = 0.1$, $\mu_{\min} = 10^{-6}$ and $tol = 10^{-10}$. The expansions of line L5 are $Q_x = \ell_x + A^{\mathsf T} V_x$, $Q_u = \ell_u + B^{\mathsf T} V_x$, $Q_{xx} = \ell_{xx} + A^{\mathsf T} V_{xx} A$, $Q_{uu} = \ell_{uu} + B^{\mathsf T} V_{xx} B$ and $Q_{ux} = \ell_{ux} + B^{\mathsf T} V_{xx} A$, with $V_x, V_{xx}$ from the step after.

Lines L3 to L8 are the backward pass. Without bounds, line L6 would give $k_k = -H^{-1} Q_u$ and line L7 the gain $K_k = -H^{-1} Q_{ux}$, and the backward pass would be the Riccati recursion of [finite-horizon LQR](/finite-horizon-lqr/) applied to the local model. With bounds, line L6 is a [quadratic program](/quadratic-programming/) over a box in $\mathbb R^m$. The code solves it with a projected Newton method: it fixes the variables that sit at a bound with the gradient pushing outward, takes a Newton step in the others, projects onto the box, and backtracks until the value goes down. It starts at $\delta = 0$, which is always in the box, so the solution is never worse than no change.

Line L7 is the key idea of the method. A control that is clamped at a bound cannot react to a small state deviation, so its row of the gain is zero, and the gain of the free controls is computed with the free block of $H$ only. Under strict complementarity this is exactly the derivative of the solution of line L6 with respect to the state (proof, Lemma 2). Line L8 then passes the cost-to-go model to the previous step.

Lines L10 to L12 are the forward pass with a backtracking line search on the feedforward part. Line L11 clamps the controls again, because the feedback term can push a control out of the box when the state differs from the old trajectory. Line L12 accepts the new trajectory only if the cost goes down by at least a fraction of the predicted change. The regularization $\mu$ makes $H$ positive definite when $Q_{uu}$ is not, and shortens the steps when the model is poor; it grows after a failure and shrinks after a success.

## Example

A pendulum swings up with a weak motor. The state is the angle $\theta$, with $\theta = 0$ hanging down, and the angular velocity $\omega$. The dynamics are $\ddot\theta = u - 9.81 \sin\theta - 0.1\,\dot\theta$, stepped by the explicit Euler method with $\Delta t = 0.05$ for $N = 80$ steps (4 seconds). The running cost is $0.0025\,u^2$ per step, and the final cost is $\frac12\bigl(100(\theta_N - \pi)^2 + 10\,\omega_N^2\bigr)$. The torque limit is $|u| \le 3$, much less than the $9.81$ needed to hold the pendulum level, so it must pump energy by swinging. The start is $u = 0$, which leaves the pendulum hanging.

| iteration | cost | accepted step $\alpha$ |
|---|---|---|
| 0 | 493.4802 | |
| 1 | 142.2482 | 0.5 |
| 2 | 57.3002 | 0.5 |
| 5 | 2.1554 | 1 |
| 10 | 0.9548 | 1 |
| 20 | 0.8580 | 1 |
| 50 | 0.8549 | 1 |
| 60 | 0.8549 | 1 |

After 60 accepted iterations the predicted change is below the tolerance and the loop stops with cost $0.854863$. The pendulum ends at $\theta_N = 3.1368$ and $\omega_N = 0.0135$, close to upright. It first swings to one side, then back through the bottom, and then up. Nineteen of the 80 controls sit exactly at the limit, and every control lies in the box. The cost went down at every iteration. At the result, the derivative of $J$ with respect to each free control is below $10^{-6}$, and each derivative at a bound points out of the box, so the result is a first-order point.

Without the limit the same problem reaches cost $0.848792$ with a largest torque of $3.618$, so the limit costs a little. With a limit of $2$ the method stops after 7 iterations at cost $14.392$, with 79 of 80 controls at the limit and the pendulum at $\theta_N = 2.647$: the result is again a first-order point, but four seconds of pumping at this torque do not bring it to the top from this start.

## Correctness

The [proof](proofs/correctness.md) shows four things. The controls stay in the box, because line L11 clamps them. Every accepted iteration lowers the cost, because the box solver of line L6 starts at zero, so each stage model has a value at most zero and the predicted change is negative. For linear dynamics and quadratic costs with no active bound, one iteration with $\mu = 0$ gives the exact optimum, because the backward pass is then the Riccati recursion. If the backward pass returns zero changes, the controls satisfy the first-order conditions of the problem with the box: the derivative of the cost is zero for free controls and points out of the box for clamped ones; for convex problems this is the global optimum. The proof also shows that the gain of line L7 is the derivative of the clamped solution. It does not prove convergence for nonlinear systems, and the method finds only a local solution.

## Complexity

The backward pass of one iteration costs $O(n^3)$ per step for the products with $V_{xx}$, $O(p\,m^3)$ for the box solver with $p$ iterations, and $O(F)$ for the dynamics and their Jacobians, so $O(N(n^3 + p\,m^3 + F))$ in total; the terms $n^2 m$ and $n m^2$ are at most $n^3 + m^3$. A forward pass costs $O(N(nm + F))$, and the line search tries at most a constant number of step sizes. So one iteration costs $O(N(n^3 + p\,m^3 + F))$, and $I$ iterations cost $I$ times that. The memory holds the trajectory and the gains, $O(Nnm)$, and the matrices of one step, $O(n^2)$.

The number of iterations has no general bound. The 60 iterations of the example are a measurement for this problem and start; near the end the cost changes only in the sixth digit, and a looser tolerance stops much earlier.

## Properties

- **Feasible controls.** Every control sequence the method holds, including all intermediate ones, lies in the box.
- **Monotone.** The cost goes down at every accepted iteration.
- **Local.** The result depends on the start; a swing-up can end at a different local solution from a different first guess.
- **Feedback.** Besides the controls, the method returns time-varying gains, which a controller can use near the trajectory; the gains of clamped controls are zero.
- **Linear in the horizon.** The work grows linearly with $N$, because each step solves only problems of size $m$ and $n$.
- **Only control bounds.** The box is handled exactly; bounds on states and general constraints need other tools.

## Variants and improvements

- **Clamping in the forward pass only.** The simplest approach ignores the box in the backward pass and clamps in line L11. The gains then still try to use clamped controls, and the predicted change of the cost is wrong when many controls sit at a bound.
- **Squashing.** Replacing $u$ by a smooth function of a free variable, such as $u = \tanh(v)$, removes the box, but the gradient of the cost with respect to $v$ vanishes at the limits, and convergence slows down there.
- **Second-order DDP.** Adding the second derivatives of the dynamics to $Q_{xx}$, $Q_{uu}$ and $Q_{ux}$ gives the original method of Mayne, with faster local convergence and a higher cost per iteration.
- **State constraints.** [Augmented Lagrangian](/augmented-lagrangian-method/) and [penalty](/penalty-method/) terms in the cost, or a [barrier](/barrier-method/), handle constraints on the states; this gives methods that combine DDP with constrained optimization.
- **Receding horizon.** Running a few iterations at every control cycle, with the solution of the last cycle shifted as the start, gives a [nonlinear MPC](/nonlinear-mpc/) controller with torque limits.

## When to use it

Use control-limited DDP when the only constraints are bounds on the controls, the horizon is long, and the dynamics are smooth and cheap to differentiate, as for torque-limited robot arms, swing-up tasks and receding-horizon control. It is simple, its memory is small, and it returns feedback gains. When there are obstacles or other state constraints, use a method that handles general constraints, such as [sequential convex optimization](/sequential-convex-trajectory-optimization/). When contacts switch on and off, see [contact-implicit trajectory optimization](/contact-implicit-trajectory-optimization/). For a convex problem with linear dynamics, a general [quadratic programming](/quadratic-programming/) solver over the whole horizon also works and gives the global optimum.

## Pitfalls

- **Ignoring the clamp in the gain.** If line L7 uses the full $H$ even for clamped controls, the feedback acts on controls that cannot move, and the forward pass of line L11 clamps them anyway, so the model and the simulation disagree and the line search fails often.
- **Forgetting the clamp in the forward pass.** Without the clamp of line L11 the feedback term can push a control out of the box when the state differs from the old trajectory.
- **A poor start.** Starting from zero controls at an equilibrium can give zero gradients for some problems. Here the final cost has a nonzero gradient, but a different start, for example with the pendulum already swinging, can lead to another local solution.
- **Stopping on a tolerance.** The test of line L9 measures the predicted change of the cost, which depends on the scale of the cost; scale the tolerance with the problem.
- **Regularization.** If $\mu$ of line L5 grows without bound, the steps become tiny and the method stalls; a bound on $\mu$ is needed, and the code stops when $\mu$ exceeds $10^{10}$.

## Implementations

## History

David Mayne introduced differential dynamic programming in 1966, as a second-order method for the optimal control of nonlinear discrete-time systems, and the book by David Jacobson and Mayne in 1970 developed its theory. The Gauss-Newton form that drops the second derivatives of the dynamics, known as iLQR, became popular in robotics in the 2000s, through the work of Weiwei Li and Emo Todorov among others. Yuval Tassa, Nicolas Mansard and Emo Todorov presented the control-limited version at ICRA 2014; its box-constrained backward pass and clamped gains made DDP practical for robots with torque limits.

## References
