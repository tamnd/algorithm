---
tag: G9RNJT
kind: algorithm
slug: infinite-horizon-lqr
name: Infinite-horizon LQR
aliases:
- steady-state LQR
- LQR
area: control/optimal-and-predictive-control
level: core
summary: Computes the constant optimal gain K = R^(-1)B^T P from the stabilizing solution P of the algebraic Riccati equation.
solves: [lqr-problem]
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs, j: the number of iterations of the recursion}
  time: {worst: "O(j (n^3 + m^3))"}
  space: {extra: "O(n^2 + n m)"}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 1960
  people: [Rudolf E. Kalman]
  note: "Kalman (1960) showed that the optimal cost of the regulator problem on an unbounded interval is the limit of the finite-horizon costs, and that the limit gives a constant feedback that stabilizes the plant."
prereqs: [lqr-problem, finite-horizon-lqr, continuous-algebraic-riccati-equation, discrete-algebraic-riccati-equation]
see_also: [schur-method-riccati, kleinman-iteration, stabilizing-riccati-solution-theorem, lqr-stability-margins, lqg-control, h2-optimal-control, value-iteration, pole-placement-theorem]
sources:
  - paper: "R. E. Kalman, Contributions to the theory of optimal control, Boletín de la Sociedad Matemática Mexicana 5(2), 102-119, 1960"
    locator: the regulator problem on an unbounded interval, as the limit of the finite interval problem
  - book: isbn:9780691151878
    title: Daniel Liberzon, Calculus of Variations and Optimal Control Theory, A Concise Introduction, Princeton University Press, 2012
    locator: Section 6.2, Infinite-horizon LQR problem
  - book: isbn:9781886529434
    title: Dimitri P. Bertsekas, Dynamic Programming and Optimal Control, Volume I, fourth edition, Athena Scientific, 2017
    locator: Section 3.1, Linear Systems and Quadratic Cost, on the convergence of the Riccati recursion
  - book: isbn:9780486457666
    title: Brian D. O. Anderson and John B. Moore, Optimal Control, Linear Quadratic Methods, Prentice Hall, 1990 (Dover reprint, 2007)
    locator: the infinite-time regulator problem and the stability of the closed loop, in the chapters on the standard regulator problem
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 13, Algebraic Riccati Equations; Chapter 14, H2 Optimal Control
  - book: isbn:9781611972085
    title: Dario A. Bini, Bruno Iannazzo and Beatrice Meini, Numerical Solution of Algebraic Riccati Equations, SIAM, 2012
    locator: the doubling algorithms and their quadratic convergence
---

Infinite-horizon LQR is the solution of the [linear quadratic regulator problem](/lqr-problem/) when the horizon has no end. The optimal input is a constant linear state feedback $u = -K x$. In continuous time $K = R^{-1} B^T P$, where $P$ is the stabilizing solution of the [continuous algebraic Riccati equation](/continuous-algebraic-riccati-equation/) (CARE). In discrete time $K = (R + B^T P B)^{-1} B^T P A$, where $P$ is the stabilizing solution of the [discrete algebraic Riccati equation](/discrete-algebraic-riccati-equation/) (DARE). The optimal cost from $x_0$ is $x_0^T P x_0$, and the closed loop $A - B K$ is Hurwitz, or Schur in discrete time. This page computes $P$ as the limit of the [finite-horizon](/finite-horizon-lqr/) costs, which is the definition of the problem. The [Schur method](/schur-method-riccati/) and the [Kleinman iteration](/kleinman-iteration/) are faster solvers of the same equations.

## In plain words

A controller must keep a system near rest forever. Being away from rest costs something at every moment, and so does every push. The total cost is a sum over all time, so it is finite only if the system really goes to rest. The best controller turns out to be very simple: it measures the state and pushes back by a fixed multiple of it, the same multiple at all times. To find the multiple, solve the same problem for a long but finite time, and let the length grow. The answer settles down to a fixed value. That value tells the cost of every starting point and gives the gain. The settled gain always brings the system to rest, as long as every unstable motion can be pushed and every unstable motion is seen by the cost.

## The problem

Continuous time. Input: $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $Q = Q^T \ge 0$ and $R = R^T > 0$, with $(A, B)$ [stabilizable](/stabilizability/) and $(Q^{1/2}, A)$ [detectable](/detectability/). The plant is $\dot x = A x + B u$ and the cost is $J(x_0, u) = \int_0^\infty (x^T Q x + u^T R u)\, dt$. Output: the matrix $P = P^T \ge 0$ with $\min_u J(x_0, u) = x_0^T P x_0$ for all $x_0$, and the gain $K$ such that $u = -K x$ attains the minimum. Discrete time: the same, with $x_{k+1} = A x_k + B u_k$ and $J = \sum_{k \ge 0} (x_k^T Q x_k + u_k^T R u_k)$.

The two hypotheses are the ones of the [stabilizing solution theorem](/stabilizing-riccati-solution-theorem/). Stabilizability makes some input give a finite cost. Detectability makes every input with finite cost drive the state to 0, so that a finite cost means a stable closed loop. The cost has no cross term $2 x^T S u$ here; with one, replace $Q$ by $Q - S R^{-1} S^T$ and $A$ by $A - B R^{-1} S^T$ and add $R^{-1} S^T$ to the gain.

## The algorithm

The discrete-time version, by the backward recursion of the finite horizon run to its fixed point:

```pseudo id=main
INFINITE-HORIZON-LQR(A, B, Q, R, tol)
L1  P ← 0                                       ▷ the cost of horizon 0
L2  repeat
L3      K ← (R + B^T P B)^(-1) B^T P A           ▷ solve, do not invert
L4      P_new ← Q + A^T P A - A^T P B K          ▷ one step of the Riccati recursion
L5      δ ← ||P_new - P||_F; P ← P_new
L6  until δ ≤ tol · ||P||_F
L7  K ← (R + B^T P B)^(-1) B^T P A
L8  if A - B K is not Schur then fail; return (P, K)
```

After $j$ passes, $P$ is the cost matrix of the finite horizon $j$ with terminal weight 0. The loop stops when two horizons give nearly the same matrix. Line L8 checks the result, because the stopping test alone does not prove that the limit is the stabilizing solution: if $(Q^{1/2}, A)$ is not detectable, the iteration can stop at a solution that does not stabilize, and line L8 then reports the failure.

The continuous-time version runs the same idea on the Riccati differential equation. In the backward time $\tau$, it is $dP/d\tau = A^T P + P A - P B R^{-1} B^T P + Q$ with $P(0) = 0$. The implementation integrates it with the classical RK4 method and the fixed step $h = 0.5 / (1 + \|H\|_\infty)$, where $H$ is the [Hamiltonian matrix](/hamiltonian-matrix/). It stops when the CARE residual, the right side of the equation, is below $10^{-13}$ times the size of the data, then sets $K = R^{-1} B^T P$ and checks that $A - B K$ is Hurwitz. The step is chosen so that $h$ times each eigenvalue of the linearized flow near the solution lies inside the stability region of RK4.

## Example

**Continuous double integrator.** For $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $Q = I$ and $R = 1$, the code takes 102 RK4 steps of size $1/6$ and returns

$$P = \begin{bmatrix} \sqrt 3 & 1 \\ 1 & \sqrt 3 \end{bmatrix} = \begin{bmatrix} 1.732051 & 1 \\ 1 & 1.732051 \end{bmatrix}, \qquad K = \begin{bmatrix} 1 & \sqrt 3 \end{bmatrix},$$

with an error below $10^{-11}$. The closed loop $A - B K = \begin{bmatrix} 0 & 1 \\ -1 & -\sqrt 3 \end{bmatrix}$ has the characteristic polynomial $s^2 + \sqrt 3\, s + 1$, so the poles are $-0.866025 \pm 0.5 i$: natural frequency 1 and damping ratio $\sqrt 3 / 2$. From $x_0 = (1, 0.5)$ the optimal cost is $x_0^T P x_0 = \sqrt 3 + 1 + 0.25 \sqrt 3 = 3.165064$, and an RK4 simulation of the closed loop over 40 seconds gives the same value within $10^{-8}$. The [finite-horizon](/finite-horizon-lqr/) page shows how $P(0)$ of horizon $T$ tends to this matrix.

**Scalar cases.** For $a = b = q = r = 1$ in continuous time, the CARE is $2p - p^2 + 1 = 0$, whose roots are $1 \pm \sqrt 2$. The stabilizing one is $p = 1 + \sqrt 2 = 2.414214$, with $K = 2.414214$ and the closed loop $1 - K = -\sqrt 2$. In discrete time, the DARE is $p = 1 + p - p^2/(1 + p)$, that is $p^2 = p + 1$, so $p = (1 + \sqrt 5)/2 = 1.618034$ and $K = p/(1 + p) = 0.618034$. The recursion from 0 meets the tolerance $10^{-14}$ after 19 passes; its iterates are the Fibonacci ratios $1, 3/2, 8/5, 21/13, \dots$

**Sampled double integrator.** The ZOH model with period 1 is $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$, $B = \begin{bmatrix} 1/2 \\ 1 \end{bmatrix}$. With $Q = I$ and $R = 1$, the recursion stops after 22 passes with

$$P = \begin{bmatrix} 2.367101 & 1.118034 \\ 1.118034 & 2.587483 \end{bmatrix}, \qquad K = \begin{bmatrix} 0.434483 & 1.028466 \end{bmatrix}.$$

The off-diagonal entry is $\sqrt 5 / 2$. The closed loop has the eigenvalues $0.377146 \pm 0.215723 i$, of modulus $0.434483$, so it is Schur. A sum of the cost over 400 steps of the closed loop gives $x_0^T P x_0$ within $10^{-10}$ (relative), and random nearby gains with a Schur closed loop all give a larger cost.

**When the cost does not see the instability.** Take $a = 2$, $b = 1$, $q = 0$, $r = 1$ in discrete time. Then $(q^{1/2}, a) = (0, 2)$ is not detectable. Starting from $P = 0$, every pass gives $P = 0$ again, so the loop stops at once with $K = 0$, and line L8 fails because $a - bK = 2$. The DARE $p = 4p - 4p^2/(1 + p)$ has the two solutions $p = 0$ and $p = 3$. The second one stabilizes: $K = 1.5$ and $a - bK = 0.5$. Starting the recursion from $P = 1$ finds it. In words: with $q = 0$ the cheapest input is no input at all, the cost is 0, and the state grows without bound.

## Correctness

The full proof is in proofs/correctness.md. It has three parts. First, if $P \ge 0$ solves the Riccati equation and $A - B K$ is Hurwitz (Schur), then for every input with finite cost $J = x_0^T P x_0 + \int_0^\infty (u + K x)^T R (u + K x)\, dt$, or the same with a sum and $R + B^T P B$ in discrete time. Detectability is used here: a finite cost forces $x(t) \to 0$, so the term $x(t)^T P x(t)$ at the far end vanishes. So $u = -K x$ is optimal and the minimum is $x_0^T P x_0$. Second, the finite-horizon costs from $P = 0$ do not decrease with the horizon and are bounded by the cost of any stabilizing gain, so they converge, and the limit solves the Riccati equation because one step of the recursion is a continuous map. Third, the limit stabilizes: if $(A - BK) v = \lambda v$ with $|\lambda| \ge 1$, the identity $P = Q + K^T R K + (A - BK)^T P (A - BK)$ gives $(1 - |\lambda|^2) v^* P v = v^* (Q + K^T R K) v$, so $Q^{1/2} v = 0$ and $K v = 0$, hence $A v = \lambda v$, which contradicts detectability by the [PBH test](/popov-belevitch-hautus-test/).

The tests check the CARE and DARE residuals (at most $10^{-9}$ times the size of the data), the symmetry and positive semidefiniteness of $P$, the closed-loop eigenvalues, the double integrator and scalar closed forms, the simulated cost in both time domains, a grid search over scalar gains, and the failure cases.

## Complexity

In the [real RAM](/real-ram/), with dense matrices:

- One pass of lines L3 to L5 costs $O(n^3 + m^3)$, the same as one step of the [finite-horizon](/finite-horizon-lqr/) recursion. Line L8 costs $O(n^3)$ for the closed-loop matrix and its characteristic polynomial, plus the root finding.
- Convergence is linear. If $P$ is the stabilizing solution and $A_K = A - B K$, the error after $j$ passes behaves like $\rho(A_K)^{2j}$, where $\rho$ is the [spectral radius](/spectral-radius/). The number of passes for a tolerance $\epsilon$ is therefore about $\log(1/\epsilon) / (2 \log(1/\rho(A_K)))$. It grows without bound as the closed loop approaches the unit circle. The pass counts in the examples are measurements, not bounds.
- In continuous time, one RK4 step costs four evaluations of the Riccati right side, each $O(n^3 + m^3)$. The error decays like $e^{-2 \alpha \tau}$, where $-\alpha$ is the largest real part of an eigenvalue of $A - B K$, and the step is at most of order $1 / \|H\|$. So the number of steps is of order $\|H\| / \alpha$ times $\log(1/\epsilon)$.

The extra space is $O(n^2 + n m)$. For a fast solution use the [Schur method](/schur-method-riccati/), which costs $O(n^3)$ flops with a constant that does not depend on the closed loop, or the [Kleinman iteration](/kleinman-iteration/), which converges quadratically. The controller costs $O(n m)$ per step online.

## Properties

- **Constant gain.** The optimal feedback does not depend on time or on $x_0$. This is why it is used much more than the finite-horizon version.
- **Guaranteed stability.** Under stabilizability and detectability, $A - B K$ is Hurwitz (Schur). Pole placement gives any poles; LQR gives poles that are optimal for a cost, and the weights $Q$ and $R$ are the design knobs.
- **Robustness in continuous time.** With one input, or a diagonal $R$, the loop has a gain margin of $(1/2, \infty)$ and a phase margin of at least 60 degrees in each channel. The [LQR stability margins](/lqr-stability-margins/) page proves this. Discrete-time LQR has smaller guaranteed margins, and LQG with an observer has none in general.
- **Monotone in the weights.** If $Q_1 \le Q_2$, then $P_1 \le P_2$, because every cost with $Q_1$ is at most the same cost with $Q_2$.
- **Scaling.** Multiplying $Q$ and $R$ by the same positive number multiplies $P$ by it and does not change $K$. Only the ratio of the weights matters.
- **Symmetric root locus.** For one input, $Q = c^T c$ and $R = \rho > 0$, let $G(s) = c (sI - A)^{-1} B$. The closed-loop poles are the roots in the open left half plane of $1 + G(-s) G(s) / \rho = 0$. As $\rho \to 0$ (cheap control), some poles tend to the zeros of $G$ in the left half plane and to the mirror images of its zeros in the right half plane, and the others go to infinity in a Butterworth pattern. As $\rho \to \infty$ (expensive control), the poles tend to the stable eigenvalues of $A$ and to the mirror images of the unstable ones.
- **Duality.** With $A \to A^T$, $B \to C^T$, the same Riccati equation gives the steady-state gain of the [Kalman filter](/kalman-filter/) in discrete time, and of the [Kalman-Bucy filter](/kalman-bucy-filter/) in continuous time.

## Variants and improvements

- **Other solvers.** The [Schur method](/schur-method-riccati/) (Laub 1979) computes the stable invariant subspace of the [Hamiltonian matrix](/hamiltonian-matrix/) and is the standard direct method. The [Kleinman iteration](/kleinman-iteration/) is Newton's method on the CARE; Hewer (1971) gave the discrete version. Both need fewer operations than the recursion when the closed loop is slow. The recursion on this page is the [value iteration](/value-iteration/) of dynamic programming, and Kleinman's method is the [policy iteration](/policy-iteration/).
- **Doubling.** Doubling algorithms compute the cost of horizon $2j$ from the cost of horizon $j$, so $j$ passes give horizon $2^j$, and the convergence becomes quadratic (Bini, Iannazzo and Meini).
- **Cross term and discounting.** A cross term $2 x^T S u$ is removed by the change of variables in The problem. A discount factor $\gamma < 1$ in discrete time replaces $A$ and $B$ by $\sqrt\gamma\, A$ and $\sqrt\gamma\, B$.
- **Integral action.** To remove steady-state error for constant references, add the integral of the error to the state and apply LQR to the larger system; see [integral state feedback](/integral-state-feedback/).
- **Output feedback.** When the state is not measured, combine the gain with a Kalman filter: this is [LQG control](/lqg-control/), which has the same gain by the [separation principle](/separation-principle/) but no guaranteed margins ([Doyle's counterexample](/lqg-guaranteed-margins-counterexample/)).
- **H2 view.** The LQR cost from a random initial state with covariance $I$ is $\operatorname{trace} P$, which is the squared H2 norm of a closed-loop system; see [H2 optimal control](/h2-optimal-control/).

## When to use it

Use it to regulate a linear plant, or a linearization about an equilibrium, when the state is measured and the task has no fixed end. It is the default first design for multivariable plants because it always gives a stabilizing gain, handles many inputs with no extra effort, and has the margins of the [LQR stability margins](/lqr-stability-margins/) page in continuous time. Use [finite-horizon LQR](/finite-horizon-lqr/) for a fixed time or a time-varying plant, and [linear MPC](/linear-mpc/) when the inputs or states have hard limits. To compute $P$ for a real plant, call a Schur-based solver; the recursion on this page is the clearest way to see why the answer is right, not the fastest way to get it.

## Pitfalls

- **"Stable" needs the hypotheses.** Without detectability of $(Q^{1/2}, A)$, the optimal cost can be finite while the state grows, and the iteration from 0 can return a gain that does not stabilize. The example above shows it. Always check the closed loop.
- **Slow convergence.** If the closed loop has a pole near the unit circle (discrete) or near the imaginary axis (continuous), the recursion needs very many passes. A stopping test on the change $\delta$ can then stop early, far from the solution. A test on the Riccati residual is better.
- **Weights are not specifications.** The choice of $Q$ and $R$ is a design step. Bryson's rule, which sets each diagonal weight to one over the square of the largest allowed value of the variable, is a rule of thumb, not a result.
- **The discrete margins are smaller.** Do not quote the 60 degree phase margin for a discrete-time LQR design or for LQG. Check the margins of the actual loop.
- **Sampling.** A continuous design implemented with a sampler and a hold is a different loop. Either design in discrete time on the [zero-order hold](/zero-order-hold-discretization/) model, or check the sampled loop.
- **Symmetry.** In floating point, symmetrize $P$ after each step. A slightly unsymmetric $P$ gives a slightly wrong gain and can make the stopping test fail.

## Implementations

## History

Kalman (1960) posed the linear quadratic regulator problem, solved it on a finite interval with the Riccati differential equation, and showed that under controllability and observability the solution has a limit as the interval grows. The limit gives a constant feedback that stabilizes the plant. Wonham (1968) and Kučera (1972) weakened the hypotheses to stabilizability and detectability. Kleinman (1968) gave a Newton iteration for the algebraic equation, and Laub (1979) gave the Schur method, which became the standard numerical solver. Kalman (1964) showed that LQR loops satisfy the return difference inequality, which gives the classical robustness of the design.

## References
