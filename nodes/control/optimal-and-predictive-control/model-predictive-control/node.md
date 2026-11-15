---
tag: 2G3P7D
kind: technique
slug: model-predictive-control
name: Model predictive control
aliases:
- receding horizon control
- moving horizon control
area: control/optimal-and-predictive-control
level: core
summary: At each sample, solves an optimal control problem over a finite horizon from the measured state and applies only the first input.
prereqs: [optimal-control-problem, state-space-representation, feedback-control-loop]
see_also: [linear-mpc, dynamic-matrix-control, generalized-predictive-control, nonlinear-mpc, explicit-mpc, mpc-stability-theorem, recursive-feasibility, principle-of-optimality]
sources:
  - paper: doi:10.1016/S0005-1098(99)00214-9
    title: D. Q. Mayne, J. B. Rawlings, C. V. Rao and P. O. M. Scokaert, Constrained model predictive control, stability and optimality, Automatica 36(6), 789-814, 2000
    locator: the survey of MPC, the receding horizon principle, and the terminal cost and terminal set conditions for stability
  - paper: doi:10.1007/BF00938540
    title: S. S. Keerthi and E. G. Gilbert, Optimal infinite-horizon feedback laws for a general class of constrained discrete-time systems, stability and moving-horizon approximations, Journal of Optimization Theory and Applications 57(2), 265-293, 1988
    locator: the stability of moving horizon control with a terminal equality constraint for constrained discrete-time systems
  - paper: doi:10.1109/9.751369
    title: P. O. M. Scokaert, D. Q. Mayne and J. B. Rawlings, Suboptimal model predictive control (feasibility implies stability), IEEE Transactions on Automatic Control 44(3), 648-654, 1999
    locator: the stability of MPC that applies a feasible plan with enough cost decrease instead of the optimal plan
  - paper: doi:10.1016/S0967-0661(02)00186-7
    title: S. Joe Qin and Thomas A. Badgwell, A survey of industrial model predictive control technology, Control Engineering Practice 11(7), 733-764, 2003
    locator: the history of industrial MPC and the survey of commercial products
  - paper: doi:10.1016/0005-1098(78)90001-8
    title: J. Richalet, A. Rault, J. L. Testud and J. Papon, Model predictive heuristic control, applications to industrial processes, Automatica 14(5), 413-428, 1978
    locator: the early predictive control scheme with an impulse response model and its industrial applications
  - book: isbn:9780975937730
    title: James B. Rawlings, David Q. Mayne and Moritz M. Diehl, Model Predictive Control, Theory, Computation, and Design, 2nd edition, Nob Hill Publishing, 2017
    locator: Chapter 2, regulation, the MPC problem, its feasible set and the stability results
  - book: isbn:9781107016880
    title: Francesco Borrelli, Alberto Bemporad and Manfred Morari, Predictive Control for Linear and Hybrid Systems, Cambridge University Press, 2017
    locator: the chapters on receding horizon control of constrained linear systems
---

Model predictive control (MPC) is a way to turn an [optimal control problem](/optimal-control-problem/) into a feedback law. At each sampling instant it measures or estimates the state $x$, solves a finite-horizon optimal control problem that starts at $x$, applies the first input of the optimal plan, and throws the rest of the plan away. At the next instant it solves the problem again from the new state, with the horizon shifted by one step. The feedback law $\kappa_N(x)$ is implicit: it is the first input of the solution of an optimization problem. The strength of MPC is that the problem can contain hard limits on the inputs and the states, which a fixed linear gain cannot respect. The cost is one optimization problem per sampling instant, and the closed loop is not automatically asymptotically stable: the horizon and the terminal cost and set must be chosen with care.

## In plain words

A driver looks some distance down the road, plans how to steer and brake over that stretch, and starts the plan. A moment later the driver looks again, from the new place, and makes a new plan. Only the start of each plan is ever used. MPC does the same with a model of the system. At every tick it asks: from where I am now, which inputs over the next few steps give the best result and keep within all the limits? It uses the first of those inputs and asks again at the next tick. Because each new plan starts from the measured state, the method corrects for model errors and disturbances, as a feedback controller does. The limits are part of each plan, so the controller respects them by design.

## When it applies

- A model of the plant is available, for example a [state-space model](/state-space-representation/) $x_{k+1} = f(x_k, u_k)$, a step response or a transfer function.
- There are limits on the inputs (actuator ranges, rates) or on the states and outputs (safety, quality) that the controller must respect, or the plant has several inputs and outputs that interact.
- The optimization problem can be solved reliably within one sampling period. This holds for slow process plants and, for linear models, also for fast mechanical and electrical systems with a few states.
- The state can be measured or estimated, for example with a [Kalman filter](/kalman-filter/) or a [Luenberger observer](/luenberger-observer/).

## The template

At each sampling instant $k$:

1. Measure or estimate the current state $x = x(k)$.
2. Solve the finite-horizon problem $\mathbb{P}_N(x)$:

$$V_N(x) = \min_{u_0, \dots, u_{N-1}} \ \sum_{i=0}^{N-1} \ell(x_i, u_i) + V_f(x_N)$$

subject to $x_0 = x$, $x_{i+1} = f(x_i, u_i)$, $(x_i, u_i) \in \mathbb{Z}$ for $i < N$, and $x_N \in \mathbb{X}_f$.

3. Apply $u(k) = u_0^*(x)$, the first input of the optimal plan.
4. Wait for the next sampling instant and go to step 1.

The design choices are the model $f$, the stage cost $\ell$, the constraint set $\mathbb{Z}$, the horizon $N$, the terminal cost $V_f$ and the terminal set $\mathbb{X}_f$. The set of states $x$ for which $\mathbb{P}_N(x)$ has a solution is the feasible set $\mathcal{X}_N$; the law $\kappa_N(x) = u_0^*(x)$ is defined only on it.

**Cost per sampling instant.** One solve of $\mathbb{P}_N(x)$. For a linear model, a quadratic cost and polyhedral constraints, $\mathbb{P}_N(x)$ is a [quadratic program](/quadratic-programming/): in condensed form it has $N m$ variables and $c$ inequality rows, where $c = 2 N m + 2 N n$ plus the terminal rows for box limits on $m$ inputs and $n$ states. It is solved by an active set method or an [interior point method](/interior-point-method/); see [linear MPC](/linear-mpc/) for the costs. For a nonlinear model it is a nonlinear program, usually not convex, and solvers return a local solution; see [nonlinear MPC](/nonlinear-mpc/).

**The terminal ingredients.** Theorem ([MPC stability theorem](/mpc-stability-theorem/)): if $\mathbb{X}_f$ is invariant under a local controller that meets the constraints, and $V_f$ decreases along that controller by at least the stage cost, then for the nominal model the MPC is [recursively feasible](/recursive-feasibility/) on $\mathcal{X}_N$ and the origin is asymptotically stable. Without these ingredients, a long enough horizon often works, but a short one can fail, as the second example shows.

## Classic examples

**Unconstrained linear MPC is LQR.** With $f(x, u) = A x + B u$, $\ell(x, u) = x^T Q x + u^T R u$, no constraints, and $V_f(x) = x^T P x$ with $P$ the solution of the [discrete algebraic Riccati equation](/discrete-algebraic-riccati-equation/), the MPC law equals the [infinite-horizon LQR](/infinite-horizon-lqr/) law $u = -K x$ for every $N \ge 1$. This is a theorem: by the [principle of optimality](/principle-of-optimality/), $x^T P x$ is the exact optimal cost from $x_N$ to infinity, so the finite problem is the infinite problem. With constraints, MPC agrees with LQR in the region where no constraint is active.

**A short horizon without a terminal cost.** Take the scalar plant $x_{k+1} = 2 x_k + u_k$ with $\ell = x^2 + u^2$, no constraints and $V_f = 0$. The [finite-horizon LQR](/finite-horizon-lqr/) recursion $P_{j+1} = 1 + 4 P_j - 4 P_j^2 / (1 + P_j)$ from $P_0 = 0$ gives $P_1 = 1$, $P_2 = 3$, $P_3 = 4$, and the MPC gain is $K_N = 2 P_{N-1} / (1 + P_{N-1})$:

| $N$ | $K_N$ | closed loop $x_{k+1} = (2 - K_N) x_k$ |
|---|---|---|
| 1 | 0 | $2 x_k$, not Schur |
| 2 | 1 | $x_k$, not asymptotically stable |
| 3 | 1.5 | $0.5\, x_k$, Schur |
| 4 | 1.6 | $0.4\, x_k$, Schur |

With $N = 1$ the input only costs and gains nothing, so the plan is $u = 0$. With the terminal cost $V_f(x) = P x^2$, $P = 2 + \sqrt 5$ (the Riccati solution), every $N$ gives the LQR gain $2P/(1+P) = (1 + \sqrt 5)/2 \approx 1.618$, and the closed loop $x_{k+1} \approx 0.382\, x_k$.

**Linear MPC with constraints.** The double integrator with $|u| \le 1$ and $|x_i| \le 5$, $N = 5$, is worked out on the [linear MPC](/linear-mpc/) page: each step is a QP with 5 variables and 36 rows, and from $x = (-5, 3)$ only the row $u_1 \ge -1$ is active.

**Industrial MPC with step response models.** [Dynamic matrix control](/dynamic-matrix-control/) predicts with a measured step response and a constant output disturbance; without constraints, each step is a least squares problem.

**MPC on a transfer function.** [Generalized predictive control](/generalized-predictive-control/) predicts with a CARIMA model through a Diophantine identity.

**Explicit solution.** For linear MPC the law $\kappa_N$ is continuous and piecewise affine on polyhedral regions, so it can be computed offline; see [explicit MPC](/explicit-mpc/).

## Variations

- **Offset-free MPC** adds disturbance states and an observer to remove steady-state error under model error; see [offset-free MPC](/offset-free-mpc/).
- **Robust MPC** guarantees the constraints for all bounded disturbances, with a min-max problem ([min-max MPC](/min-max-mpc/)) or with a nominal plan and a tube around it ([tube MPC](/tube-mpc/)).
- **Stochastic MPC** uses chance constraints and expected costs; see [stochastic MPC](/stochastic-mpc/).
- **Economic MPC** uses a cost that is not a tracking cost, such as profit or energy; see [economic MPC](/economic-mpc/).
- **Hybrid MPC** handles models with logic and switching as mixed-integer programs; see [hybrid MPC](/hybrid-mpc/).
- **Nonlinear MPC** uses a nonlinear model; see [nonlinear MPC](/nonlinear-mpc/).
- **Reference governors** keep an existing loop and only change its setpoint to respect the constraints; see [reference governor](/reference-governor/).
- **Suboptimal MPC** applies a feasible, not optimal, plan that decreases the cost enough; stability can still be proved (Scokaert, Mayne and Rawlings 1999, see the [stability theorem](/mpc-stability-theorem/)).

## Pitfalls

- **No stability by default.** A short horizon without terminal ingredients can give an unstable loop, as in the scalar example. Use a terminal cost and set, or check the closed loop.
- **Loss of feasibility.** A disturbance or a model error can move the state to a point where $\mathbb{P}_N$ has no solution. Use soft state constraints with a large penalty, or a robust design.
- **Computation time.** If the solver does not finish within the sampling period, the controller has no input to apply. Measure the worst case of the solver, use warm starts, limit the iterations, or use [explicit MPC](/explicit-mpc/) for small problems.
- **Steady-state offset.** A model error or a constant disturbance gives an offset unless the controller has integral action, for example through a disturbance model.
- **Nonconvex problems.** For a nonlinear model the solver can return a local minimum or fail, and the theory for the exact optimum does not apply directly.
- **Delay of one sample.** The solve takes time, so the input is often applied one sample late. Include this delay in the model.

## Exercises

1. In the scalar example, compute $P_4$ and $K_5$, and show that $K_N$ tends to $(1 + \sqrt 5)/2$ as $N$ grows.
2. Prove that with $V_f(x) = x^T P x$ and $P$ the DARE solution, unconstrained MPC gives the LQR law for every horizon $N \ge 1$.
3. For $n = 4$ states, $m = 2$ inputs, $N = 20$ and box limits on all inputs and states, give the number of variables and rows of the condensed QP, and the number of variables and equality constraints of the sparse QP.
4. In the scalar example with $N = 2$, the plan computed at time 0 has $u_1 = 0$. Show that the MPC applies a different input at time 1, even without disturbances. Explain why this cannot happen with the terminal cost $V_f(x) = P x^2$.
5. The input limit $|u| \le 1$ is added to the scalar example with $N = 3$. Find the set of states for which the MPC law saturates.

## References
