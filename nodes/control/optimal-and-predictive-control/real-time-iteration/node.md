---
tag: RM47HC
kind: algorithm
slug: real-time-iteration
name: Real-time iteration
aliases:
- RTI scheme
area: control/optimal-and-predictive-control
level: research
summary: Solves nonlinear MPC by one sequential quadratic programming step per sample, with the expensive part prepared before the state is measured.
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs, N: the number of shooting intervals, I: the number of active set iterations of the QP}
  time: {worst: "O(N^3 m^2 n + N n^2 (n + m) + I N^3 m^3)"}
  space: {extra: "O(N^2 m (n + m))"}
properties: {deterministic: true, exact: false, recursive: false, online: true}
history:
  year: 2005
  people: [Moritz Diehl, Hans Georg Bock, Johannes P. Schlöder]
  note: "Diehl, Bock and Schlöder developed the real-time iteration in Heidelberg on top of the direct multiple shooting method. In 2005 they published its contraction analysis, and Diehl, Findeisen, Allgöwer, Bock and Schlöder published the nominal stability of the closed loop."
prereqs: [nonlinear-mpc, gauss-newton-algorithm, quadratic-programming, runge-kutta-methods]
see_also: [linear-mpc, explicit-mpc, kkt-conditions, newton-method-for-systems, extended-kalman-filter, automatic-differentiation, interior-point-method, mpc-stability-theorem]
sources:
  - paper: doi:10.1137/S0363012902400713
    title: Moritz Diehl, Hans Georg Bock and Johannes P. Schlöder, A real-time iteration scheme for nonlinear optimization in optimal feedback control, SIAM Journal on Control and Optimization 43(5), 1714-1736, 2005
    locator: the real-time iteration with the initial value embedding, and its contraction analysis
  - paper: "Moritz Diehl, Rolf Findeisen, Frank Allgöwer, Hans Georg Bock and Johannes P. Schlöder, Nominal stability of real-time iteration scheme for nonlinear model predictive control, IEE Proceedings Control Theory and Applications 152(3), 296-308, 2005"
    locator: the nominal stability of the closed loop of the real-time iteration with shifted initial guesses
  - book: isbn:9780975937730
    title: James B. Rawlings, David Q. Mayne and Moritz M. Diehl, Model Predictive Control, Theory, Computation, and Design, 2nd edition, Nob Hill Publishing, 2017
    locator: the chapter on numerical optimal control, the real-time iteration
---

The real-time iteration (RTI) is a way to run [nonlinear MPC](/nonlinear-mpc/) fast enough for a real plant. Exact nonlinear MPC solves a nonlinear program to convergence at every sample, which takes several iterations and causes a delay. The RTI does only one Gauss-Newton step of sequential quadratic programming per sample, and it starts each step from the shifted solution of the previous sample. The step is split into two phases. The preparation phase integrates the model, computes the derivatives and condenses the problem into a small quadratic program, all before the new state is known. The feedback phase starts when the state is measured and only solves that quadratic program. So the delay between the measurement and the input is the time of one small QP, and the controller follows the exact nonlinear MPC solution closely as the plant moves.

## In plain words

A full nonlinear plan is too slow to compute again from the start at every moment. So keep the plan from the last moment, slide it one step forward, and improve it a little each time instead of solving it completely. Most of the work for that improvement does not need the newest measurement, so do it while you wait. When the measurement comes, only a small and fast correction is left, and the input goes out almost at once. Because the plan changes only a little between two moments, one improvement per moment is usually enough to stay close to the best plan.

## The problem

Input: a model $\dot x = f(x, u)$ with $f$ twice continuously differentiable and its Jacobians, a sample time $h$, a horizon of $N$ intervals, weights $Q$ and $P$ symmetric positive semidefinite and $R$ symmetric positive definite, an input bound $\bar u$, an initial guess of nodes $s_0, \dots, s_N$ and controls $q_0, \dots, q_{N-1}$, and a stream of measured states.

At each sample with measured state $x_0$, the nonlinear MPC problem in multiple shooting form is

$$\min_{s, q} \ \sum_{k=0}^{N-1} \left(s_k^T Q s_k + q_k^T R q_k\right) + s_N^T P s_N \quad \text{s.t.} \quad s_0 = x_0, \ s_{k+1} = F(s_k, q_k), \ -\bar u \le q_k \le \bar u,$$

where $F$ is one Runge-Kutta 4 step of length $h$.

Output: at each sample, an input $u$ within the bounds, with the least possible delay after the measurement.

## The algorithm

```pseudo id=main
RTI(f, h, N, Q, R, P, ū, s, q)
L1   for each sample do
L2       for k = 0, ..., N-1: (F_k, A_k, B_k) ← RK4 step at (s_k, q_k) with derivatives;  c_k ← F_k - s_{k+1}   ▷ prepare
L3       condense: Δs_k = M_k Δs₀ + Γ_k Δq + d_k, and from it H, g, G of the QP                        ▷ prepare
L4       measure x₀;  Δs₀ ← x₀ - s₀                                                                  ▷ feedback
L5       Δq ← argmin ½ Δqᵀ H Δq + (g + G Δs₀)ᵀ Δq  subject to  -ū ≤ q + Δq ≤ ū
L6       apply u = q₀ + Δq₀
L7       Δs_{k+1} ← A_k Δs_k + B_k Δq_k + c_k;  s ← s + Δs;  q ← q + Δq
L8       shift s and q by one interval and repeat the last node and control
```

Line L2 integrates each shooting interval with one RK4 step and propagates the derivatives through the four stages by the chain rule, so $A_k$ and $B_k$ are the exact Jacobians of the discrete map. The gaps $c_k$ are the defects of the multiple shooting guess. They need not be zero during the iteration.

Line L3 eliminates the node variables. With $M_0 = I$, $\Gamma_0 = 0$ and $d_0 = 0$, the recursion $M_{k+1} = A_k M_k$, $d_{k+1} = A_k d_k + c_k$, and $\Gamma_{k+1} = A_k \Gamma_k$ with block column $k$ replaced by $B_k$, gives the node steps as a linear function of $\Delta s_0$ and $\Delta q$. With $W_k = Q$ for $k < N$ and $W_N = P$, the condensed data are $H = 2 \sum_k \Gamma_k^T W_k \Gamma_k + 2\,\mathrm{blockdiag}(R)$, $g = 2 \sum_k \Gamma_k^T W_k (s_k + d_k) + 2 R q$ and $G = 2 \sum_k \Gamma_k^T W_k M_k$. None of this uses the measured state.

Line L4 is the initial value embedding: the measured state enters the QP only through the linear constraint $\Delta s_0 = x_0 - s_0$, so it changes only the gradient $g + G \Delta s_0$.

Line L5 solves a QP with a positive definite Hessian and box constraints. The implementation uses a primal active set method, which is warm-started cheaply in practice.

Line L8 makes the result of this sample the guess for the next one. The shifted guess is close to the next solution when the plant moves as predicted.

## Example

Take the inverted pendulum $\ddot\theta = \sin \theta + u$ with state $x = (\theta, \dot\theta)$, upright at $\theta = 0$. Without input it falls: from $\theta = 0.1$ the angle is $0.375$ after 2 seconds and $0.985$ after 3 seconds. Use $h = 0.1$, $N = 20$, $Q = \mathrm{diag}(10, 1)$, $R = 0.1$, $P = \begin{bmatrix} 50 & 10 \\ 10 & 10 \end{bmatrix}$ and the zero initial guess.

**The exact problem.** From $\theta_0 = 2.5$ with $\bar u = 10$, iterating the Gauss-Newton step at the same state gives:

| iteration | largest control step | largest gap | cost of the simulated controls |
|---|---|---|---|
| 1 | 10 | 0.188 | 866.58 |
| 2 | 3.71 | 8.7e-4 | 398.881 |
| 3 | 0.0134 | 2.0e-8 | 398.873 |
| 4 | 5.8e-5 | 6e-13 | 398.873 |
| 5 | 3.2e-7 | below 1e-15 | 398.873 |

The steps shrink by a roughly constant factor, which is the linear convergence of Gauss-Newton. The gaps close much faster.

**The RTI loop.** From $\theta_0 = 1$ with $\bar u = 10$, exact nonlinear MPC needs 5 iterations at the first sample and 3 or 4 at the later samples. The RTI does one at each sample. Its first input is $-8.579$, against $-8.4348$ for the converged solution. Compare the two at the same states, along the RTI trajectory:

| sample | 0 | 1 | 2 and later |
|---|---|---|---|
| difference from the converged input | 0.144 | 2.8e-5 | below 1e-6 |

Only the first sample, which starts from the poor zero guess, shows a visible error. After that, the shifted guess is so good that one step is enough. The state is below $10^{-2}$ after 20 samples.

**Saturation.** With $\bar u = 2$ from $\theta_0 = 2.5$, the input stays at $-2$ for the first 12 samples or more, the box QP keeps every input within its bound, and the state is below $10^{-2}$ after 35 samples. The RTI inputs agree with the converged ones within $3 \times 10^{-7}$ after 10 samples.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The RK4 derivatives are exact by the chain rule through the four stages. By induction over the intervals, the condensed QP has the same cost as the linearized multiple shooting problem, for every $\Delta s_0$ and $\Delta q$. The box QP solver returns only at a point that meets the KKT conditions, and the Hessian is positive definite, so it returns the unique solution. So each sample performs one exact Gauss-Newton SQP step. If the step is zero at some guess, the guess has no gaps, its nodes are the simulated trajectory, and its controls meet the KKT conditions of the nonlinear MPC problem. How close the RTI stays to the exact solution along the closed loop depends on the contraction of the Gauss-Newton step and on how far the plant moves between samples. Diehl, Bock and Schlöder (2005) give the contraction analysis and Diehl and coauthors (2005) the nominal stability of the closed loop. These results are cited and not proved here.

## Complexity

The preparation phase does $N$ RK4 steps with derivatives, $O(N n^2 (n + m))$ for dense Jacobians, and dense condensing. Building all $\Gamma_k$ costs $O(N^2 n^2 m)$, and forming $H$ from them $O(N^3 m^2 n)$. The feedback phase solves the box QP with $N m$ variables, and each active set iteration solves a dense system in $O(N^3 m^3)$. Condensed storage is $O(N^2 m (n + m))$. Variants that keep the sparse structure and use a Riccati recursion bring both phases down to linear in $N$. The main gain is not the operation count but the delay: only the QP lies between the measurement and the input.

## Properties

- **One SQP step per sample,** always the same amount of work, so the timing is predictable.
- **Small feedback delay,** since the integration, the derivatives and the condensing are done before the measurement.
- **Exact Gauss-Newton step** for a least squares cost, with no Hessian of the model.
- **Initial value embedding.** The measured state enters linearly, so the feedback is a first-order correct prediction of the exact solution even when the guess was prepared for a different state.
- **Approximate.** The input is not the exact solution of the nonlinear program. The error is small when the guess is good and the sampling is fast compared to the plant.
- **Fixed points are KKT points.** If the iteration stands still, it stands at a KKT point of the nonlinear MPC problem.

## Variants and improvements

- **Sparse QP.** Keep the node variables and solve the QP with a structure-exploiting solver, for long horizons or many states.
- **Inexact sensitivities.** Reuse old Jacobians and correct only the gradient, which makes the preparation cheaper.
- **Several iterations.** When time allows, do more than one SQP step per sample, which moves toward exact nonlinear MPC.
- **General Hessians.** For costs that are not least squares, use an exact or quasi-Newton Hessian of the Lagrangian, with a regularization to keep the QP convex.
- **Estimation.** The same idea runs moving horizon estimation, with one Gauss-Newton step per sample.
- **Code generation.** Toolkits such as ACADO Code Generation and acados generate the RTI as plain C code for embedded processors.

## When to use it

Use the RTI when a nonlinear model is needed and the sample time is short, for example in vehicles, drones, robots or engines. It is the standard method for embedded nonlinear MPC. It assumes that the guess from the last sample is good, so the sample time must be short compared to the time in which the plant changes. When the plant can change abruptly, for example after a large disturbance, more iterations or a globalization strategy are needed. For a linear model, plain [linear MPC](/linear-mpc/) or [explicit MPC](/explicit-mpc/) is simpler.

## Pitfalls

- **A poor first guess.** The first sample starts from whatever guess is given, and one step may not be enough. In the example the first input is off by 0.144. Warm-start from a simulation, or iterate to convergence at the first sample.
- **No globalization.** The full step is taken without a line search. Far from the solution the step can make things worse.
- **Using the state too early.** Anything that uses the measured state belongs to the feedback phase. If the preparation uses it, the delay comes back.
- **Wrong derivatives.** The method needs the exact Jacobians of the discrete map, not of the continuous model. Check them against finite differences.
- **Indefinite Hessians.** The Gauss-Newton Hessian is positive semidefinite only for a least squares cost. With other costs, the QP can be nonconvex.

## Implementations

## History

Diehl, Bock and Schlöder developed the real-time iteration in Heidelberg, on top of the direct multiple shooting method of Bock and Plitt (1984) for optimal control. The key ideas are the initial value embedding, which puts the measured state into the QP as a linear constraint, and the split into a preparation phase and a feedback phase. In 2005 Diehl, Bock and Schlöder published the contraction analysis of the scheme, and Diehl, Findeisen, Allgöwer, Bock and Schlöder proved the nominal stability of the closed loop. The method spread to fast mechatronic and automotive applications through code generation tools, and it is now a standard way to run nonlinear MPC on embedded hardware.

## References
