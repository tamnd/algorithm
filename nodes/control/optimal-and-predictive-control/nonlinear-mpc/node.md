---
tag: BD2QNC
kind: technique
slug: nonlinear-mpc
name: Nonlinear MPC
aliases:
- NMPC
- nonlinear model predictive control
area: control/optimal-and-predictive-control
level: advanced
summary: MPC with a nonlinear model, where each step is a nonlinear program solved by shooting or collocation.
prereqs: [model-predictive-control, optimal-control-problem, mpc-stability-theorem, kkt-conditions]
see_also: [real-time-iteration, linear-mpc, economic-mpc, tube-mpc, shooting-method, runge-kutta-methods, brockett-condition, extended-kalman-filter]
sources:
  - paper: doi:10.1016/S0005-1098(99)00214-9
    title: David Q. Mayne, James B. Rawlings, Christopher V. Rao and Pierre O. M. Scokaert, Constrained model predictive control, stability and optimality, Automatica 36(6), 789-814, 2000
    locator: the terminal cost, terminal set and local controller conditions for stability of nonlinear MPC
  - book: isbn:9780975937730
    title: James B. Rawlings, David Q. Mayne and Moritz M. Diehl, Model Predictive Control, Theory, Computation, and Design, 2nd edition, Nob Hill Publishing, 2017
    locator: the chapters on stability of MPC for nonlinear systems and on numerical optimal control
  - paper: doi:10.1137/S0363012902400713
    title: Moritz Diehl, Hans Georg Bock and Johannes P. Schlöder, A real-time iteration scheme for nonlinear optimization in optimal feedback control, SIAM Journal on Control and Optimization 43(5), 1714-1736, 2005
    locator: the multiple shooting formulation of nonlinear MPC and its solution by one SQP step per sample
---

Nonlinear MPC (NMPC) is [model predictive control](/model-predictive-control/) with a nonlinear model. At each sample it measures the state, solves a finite horizon [optimal control problem](/optimal-control-problem/) for the nonlinear model, applies the first input and repeats. The problem is a nonlinear program: the model is turned into equality constraints by single shooting, multiple shooting or collocation, and the program is solved by sequential quadratic programming or an interior point method, started from the shifted solution of the last sample. The stability argument of [linear MPC](/linear-mpc/) carries over unchanged: a terminal cost and a terminal set that fit a local controller make the optimal value a Lyapunov function. What does not carry over is convexity. The program can have local minima, its solution takes much more time, and the solver may fail. Fast methods such as the [real-time iteration](/real-time-iteration/) exist for this reason.

## In plain words

Linear predictive control looks ahead with a straight-line picture of the machine. That picture is fine near one operating point, but it gets worse the farther the machine moves from it. Nonlinear predictive control uses the real curved picture instead. It plans with the same rule as before: look ahead, find the best plan, do the first move, and plan again. The plan is now harder to find. There can be several plans that each look best in their own neighborhood, and the search takes longer. So the method trades computing time for a model that stays right over the whole range of the machine.

## When it applies

- The plant is $x^+ = F(x, u)$ or $\dot x = f(x, u)$ with $f$ smooth enough for a gradient-based solver, usually twice continuously differentiable.
- The plant moves over a range where one linearization is not accurate enough, for example in start-up, in batch processes, along a path, or near limits of the model such as saturation of a reaction.
- The constraints are known and must be met, as in all MPC.
- There is enough computing time at each sample to solve, or at least improve, a nonlinear program, or the sample time is long enough to iterate to convergence.

If the plant stays close to one operating point, [linear MPC](/linear-mpc/) on the linearization is simpler and often almost as good. If the goal is an economic cost and not a setpoint, see [economic MPC](/economic-mpc/).

## The template

1. **Discretize the model.** On each interval of length $h$, replace the differential equation by a numerical integrator $F(x, u)$, for example a [Runge-Kutta](/runge-kutta-methods/) step, or by a collocation polynomial.
2. **State the problem.** For the measured state $x$, solve
$$V_N(x) = \min_{u_0, \dots, u_{N-1}} \sum_{k=0}^{N-1} \ell(x_k, u_k) + V_f(x_N) \quad \text{s.t.} \quad x_0 = x, \ x_{k+1} = F(x_k, u_k), \ (x_k, u_k) \in \mathbb{Z}, \ x_N \in X_f.$$
3. **Transcribe.** In single shooting the inputs are the only variables and the states come from simulation. In multiple shooting the states at the start of each interval are variables too, and the model gives $N$ continuity constraints $s_{k+1} = F(s_k, q_k)$. In direct collocation the states at all collocation points are variables, and the model gives one equation per point.
4. **Solve.** Use sequential quadratic programming, often with a Gauss-Newton Hessian, or an [interior point method](/interior-point-method/). Start from the solution of the last sample, shifted by one interval, with a last input from the terminal controller.
5. **Apply and repeat.** Apply $u_0$ and solve again at the next sample.

**Terminal ingredients.** Choose a local controller $\kappa_f$, a terminal cost $V_f$ and a terminal set $X_f$ such that $X_f$ is invariant under $\kappa_f$, the constraints hold in $X_f$, and

$$V_f(F(x, \kappa_f(x))) \le V_f(x) - \ell(x, \kappa_f(x)) \quad \text{for all } x \in X_f.$$

For a model whose linearization at the setpoint is stabilizable, a standard choice is the quasi-infinite horizon design of Chen and Allgöwer (1998): $\kappa_f$ is an LQR gain of the linearization, $V_f$ is a quadratic form slightly larger than the LQR cost, and $X_f$ is a small level set of $V_f$ on which the nonlinear terms are dominated.

**Why it works.** Let $u^*$ be the solution at $x$, with the predicted states $x^*_k$. At the next state $x^+ = x^*_1$, the shifted sequence $(u^*_1, \dots, u^*_{N-1}, \kappa_f(x^*_N))$ is feasible, because $x^*_N \in X_f$ and $X_f$ is invariant under $\kappa_f$. Its cost is $V_N(x) - \ell(x, u^*_0) - V_f(x^*_N) + \ell(x^*_N, \kappa_f(x^*_N)) + V_f(F(x^*_N, \kappa_f(x^*_N)))$, and the terminal inequality makes the last three terms at most 0. So

$$V_N(x^+) \le V_N(x) - \ell(x, u^*_0).$$

With $\ell$ bounded below by a class K function of $|x|$ and $V_N$ bounded above by one, $V_N$ is a [Lyapunov function](/lyapunov-function/) and the closed loop is asymptotically stable on the feasible set. This is the [MPC stability theorem](/mpc-stability-theorem/). The proof never uses that $u^*$ is a global optimum. It only needs a feasible solution whose cost is no larger than that of the shifted warm start. So a local solver that starts from the shifted sequence and does not increase the cost keeps the guarantee.

**What is not proved here.** The argument assumes that the solver returns a feasible point that is no worse than the warm start, on time. Nonlinear programs can fail to converge, and the first problem has no warm start. The existence of the terminal ingredients needs a stabilizable linearization, and the region of attraction can be small. The guarantee is nominal: Grimm and coauthors (2004) gave examples where nonlinear MPC has no robustness at all to small disturbances, because the value function is not continuous.

## Classic examples

**The inverted pendulum.** Take $\ddot\theta = \sin \theta + u$, upright at $\theta = 0$, with RK4 steps of $h = 0.1$, $N = 20$, $\ell(x, u) = 10 \theta^2 + \dot\theta^2 + 0.1 u^2$, $V_f(x) = x^T \begin{bmatrix} 50 & 10 \\ 10 & 10 \end{bmatrix} x$ and multiple shooting from the zero guess. From $\theta_0 = 1$ with $|u| \le 10$, Gauss-Newton SQP converges in 5 iterations, with first input $-8.4348$ and predicted cost $62.0155$. With $|u| \le 2$, 8 of the 20 inputs are at the bound and the cost is $86.645$. In the closed loop, solved to convergence at each sample from the shifted guess, no sample needs more than 5 iterations from $\theta_0 = 1$ or more than 7 from $\theta_0 = 2.5$.

The comparison with linear MPC on the linearization at the upright position is instructive:

| start and bound | closed loop cost of linear MPC | closed loop cost of NMPC |
|---|---|---|
| $\theta_0 = 1$, $\lvert u \rvert \le 10$ | 62.022 | 62.015 |
| $\theta_0 = 2.5$, $\lvert u \rvert \le 10$ | 398.992 | 398.871 |
| $\theta_0 = 2.5$, $\lvert u \rvert \le 2$ | 730.918 | 730.916 |

The gain is small here, because $|\sin \theta| \le |\theta|$: the linear model overestimates gravity, so it errs on the safe side. NMPC pays off when the linear model is wrong in the harmful direction, or when the operating point moves far.

**Unstable plants and multiple shooting.** For the pendulum, the free motion grows like $e^{t}$, so over the 2 second horizon a small change of an early input changes the final state about $e^2 \approx 7.4$ times as much. Single shooting must integrate over the whole horizon at each iteration and sees this growth in its derivatives. Multiple shooting integrates only over one interval at a time and lets the continuity gaps close during the iteration, which is better conditioned, and it can be started from a state guess that is not a simulated trajectory.

**Systems that no smooth feedback can stabilize.** The nonholonomic integrator, a model of a wheeled vehicle, fails [Brockett's condition](/brockett-condition/), so no continuous static feedback makes its origin asymptotically stable. NMPC with a suitable terminal set can stabilize it, because the feedback law defined by an optimization need not be continuous.

## Variations

- **Real-time iteration.** Do only one SQP step per sample, and prepare it before the measurement, as in the [real-time iteration](/real-time-iteration/).
- **Explicit nonlinear MPC.** Approximate the law offline over the state space. This works only for few states.
- **No terminal constraint.** Drop $X_f$ and use a long enough horizon. Stability then follows from controllability assumptions on the cost, with a horizon bound.
- **Robust NMPC.** Add tubes, as in [tube MPC](/tube-mpc/), with a nonlinear ancillary controller, or optimize over a tree of scenarios.
- **Economic NMPC.** Replace the tracking cost by an economic one, as in [economic MPC](/economic-mpc/).
- **Output feedback.** Estimate the state with an [extended Kalman filter](/extended-kalman-filter/) or with moving horizon estimation, which solves a nonlinear program over a past window.

## Pitfalls

- **Local minima.** The program is not convex. Different warm starts can give different inputs, and the closed loop can switch between them.
- **No convergence on time.** Limit the iterations, and keep a feasible fallback, such as the shifted solution of the last sample.
- **Infeasible first problem.** Hard state constraints far from the initial state can make the program infeasible. Use soft state constraints with exact penalties.
- **Poor derivatives.** Finite differences in the solver make it slow and inaccurate. Use [automatic differentiation](/automatic-differentiation/) or exact sensitivities of the integrator.
- **Integrator error.** A coarse integrator gives a model that differs from the plant. Check the integration error at the largest expected speeds.
- **Fragile nominal stability.** A discontinuous value function can make the loop sensitive to small disturbances. Soft constraints and no hard terminal equality help.

## Exercises

1. For the scalar plant $x^+ = x^2 + u$ with $N = 1$, $\ell = x^2 + u^2$ and $V_f(x) = p x^2$, find the NMPC law with no constraints. (Answer: setting the derivative of $u^2 + p (x^2 + u)^2$ to 0 gives $u = -p x^2 / (1 + p)$, a nonlinear feedback.)
2. In exercise 1, find the optimal value. (Answer: $V_1(x) = x^2 + p x^4 / (1 + p)$.)
3. Count the variables of single and multiple shooting for $n$ states, $m$ inputs and $N$ intervals. (Answer: $N m$ for single shooting, and $N m + (N + 1) n$ with $(N + 1) n$ equality constraints for multiple shooting.)
4. Show that a solver that returns any feasible point with cost at most that of the shifted warm start keeps the decrease $V(x^+) \le V(x) - \ell(x, u_0)$, where $V$ is now the cost of the returned point. (Answer: the shifted sequence has cost at most $V(x) - \ell(x, u_0)$ by the terminal inequality, and the returned point is no worse.)
5. Why does the pendulum example show almost no gain from NMPC? (Answer: $|\sin \theta| \le |\theta|$, so the linear model predicts more gravity than there is, and the linear controller is a little too strong but never too weak.)

## References
