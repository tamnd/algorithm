---
tag: 1TJYDZ
kind: problem
slug: lqr-problem
name: Linear quadratic regulator problem
aliases:
- LQR problem
- LQ optimal control
area: control/optimal-and-predictive-control
level: core
summary: Minimize the integral or sum of x^T Q x + u^T R u for a linear system. The optimal input is a linear state feedback u = -K x, with K from a Riccati equation.
model: real-ram
prereqs: [state-space-representation, stabilizability, positive-definite-matrix]
see_also: [finite-horizon-lqr, infinite-horizon-lqr, continuous-algebraic-riccati-equation, discrete-algebraic-riccati-equation, optimal-control-problem, lqg-control, linear-mpc, minimum-energy-control]
sources:
  - paper: "R. E. Kalman, Contributions to the theory of optimal control, Boletín de la Sociedad Matemática Mexicana 5(2), 102-119, 1960"
    locator: the statement of the regulator problem with a quadratic cost, its solution by a linear feedback, and the limit of an infinite interval
  - book: isbn:9780486457666
    title: Brian D. O. Anderson and John B. Moore, Optimal Control, Linear Quadratic Methods, Prentice Hall, 1990 (Dover reprint, 2007)
    locator: Chapter 2, The Standard Regulator Problem I
  - book: isbn:9780691151878
    title: Daniel Liberzon, Calculus of Variations and Optimal Control Theory, A Concise Introduction, Princeton University Press, 2012
    locator: Section 6.1 (the finite-horizon problem) and Section 6.2 (the infinite-horizon problem and the algebraic Riccati equation)
  - book: isbn:9781886529434
    title: Dimitri P. Bertsekas, Dynamic Programming and Optimal Control, Volume I, fourth edition, Athena Scientific, 2017
    locator: Section 3.1, Linear Systems and Quadratic Cost
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 13 (algebraic Riccati equations) and Chapter 14 (H2 optimal control, with the state feedback case)
---

The linear quadratic regulator (LQR) problem asks for the input that drives a linear system $\dot x = A x + B u$, or $x_{k+1} = A x_k + B u_k$, toward zero at the smallest value of a quadratic cost. The cost adds a weight $Q \ge 0$ on the state and a weight $R > 0$ on the input, summed or integrated over a finite or an infinite horizon. The answer is always a linear state feedback $u = -K x$. On a finite horizon the gain changes with time and comes from a Riccati recursion or a Riccati differential equation ([finite-horizon LQR](/finite-horizon-lqr/)). On an infinite horizon the gain is constant and comes from the stabilizing solution of an algebraic Riccati equation ([infinite-horizon LQR](/infinite-horizon-lqr/), the [CARE](/continuous-algebraic-riccati-equation/) and the [DARE](/discrete-algebraic-riccati-equation/)). This page states the problem. The solution methods and the equations have their own pages.

## In plain words

A machine should go back to its rest position after a push. You can apply force to bring it back, but force costs fuel or wear, and being away from rest also costs something. The problem is to choose the force at each moment so that the total cost over time is as small as possible. Two dials set the trade: one says how much you dislike being away from rest, the other how much you dislike using force. For linear machines and costs of this squared form, the best force has a simple shape. It is the measured state multiplied by a fixed table of numbers, the gain. Finding the gain means solving one matrix equation. If you turn the force dial down, the gain gets larger and the machine returns faster. If you turn it up, the controller acts more gently.

## Definition

**Continuous time.** Input: matrices $A \in \mathbb{R}^{n \times n}$ and $B \in \mathbb{R}^{n \times m}$, weights $Q = Q^T \ge 0$ in $\mathbb{R}^{n \times n}$ and $R = R^T > 0$ in $\mathbb{R}^{m \times m}$, an initial state $x_0$, and either a horizon $T > 0$ with a terminal weight $Q_f = Q_f^T \ge 0$, or $T = \infty$. The plant is $\dot x = A x + B u$, $x(0) = x_0$. The cost is

$$J(x_0, u) = \int_0^T \left( x^T Q x + u^T R u \right) dt + x(T)^T Q_f x(T),$$

with no terminal term when $T = \infty$. The task is to find an input $u$ that minimizes $J$ over all square integrable inputs, and the minimum value.

**Discrete time.** The plant is $x_{k+1} = A x_k + B u_k$, and the cost is $\sum_{k=0}^{N-1} (x_k^T Q x_k + u_k^T R u_k) + x_N^T Q_f x_N$ for a horizon $N$, or the infinite sum with no terminal term.

**Cross term.** This area also allows a cost $x^T Q x + 2 x^T S u + u^T R u$ with $S \in \mathbb{R}^{n \times m}$, under the condition that the block matrix $\begin{bmatrix} Q & S \\ S^T & R \end{bmatrix}$ is positive semidefinite and $R > 0$. By the [Schur complement](/schur-complement/), that is the same as $Q - S R^{-1} S^T \ge 0$. The Reductions section removes the cross term, so the rest of the page sets $S = 0$.

**What is known about the answer.**

- *Finite horizon.* A minimizer always exists and is unique. It is $u(t) = -R^{-1} B^T P(t) x(t)$, where $P$ solves the Riccati differential equation $-\dot P = A^T P + P A - P B R^{-1} B^T P + Q$ with $P(T) = Q_f$. The minimum is $x_0^T P(0) x_0$. In discrete time, $u_k = -K_k x_k$ with the gains of the backward Riccati recursion.
- *Infinite horizon, stabilizable.* If $(A, B)$ is [stabilizable](/stabilizability/), some input gives a finite cost, so the minimum is finite for every $x_0$.
- *Infinite horizon, stabilizable and detectable.* If also $(Q^{1/2}, A)$ is [detectable](/detectability/), the minimizer is $u = -K x$ with $K = R^{-1} B^T P$ in continuous time and $K = (R + B^T P B)^{-1} B^T P A$ in discrete time. Here $P$ is the unique stabilizing solution of the CARE or the DARE (the [stabilizing solution theorem](/stabilizing-riccati-solution-theorem/)), and the minimum is $x_0^T P x_0$. The closed loop $A - B K$ is Hurwitz in continuous time and Schur in discrete time.

Without detectability, the optimal input can leave the state unbounded. The scalar example below shows this.

## Variants

- **Finite or infinite horizon, continuous or discrete time.** These are the four basic cases. In discrete time the data may also come from sampling a continuous plant with a [zero-order hold](/zero-order-hold-discretization/).
- **Time-varying data.** $A(t)$, $B(t)$, $Q(t)$ and $R(t)$ may depend on time ([linear time-varying systems](/linear-time-varying-system/)). The finite-horizon solution keeps the same form, with the data of each time in the Riccati equation.
- **Output weighting.** $Q = C^T C$ for an output $y = C x$, so the cost is $\int (|y|^2 + u^T R u)\, dt$. Detectability is then the detectability of $(C, A)$.
- **Stabilizing inputs only.** Some texts minimize over inputs for which $x(t) \to 0$. If $(A, B)$ is stabilizable and $(Q^{1/2}, A)$ has no unobservable mode on the imaginary axis (the unit circle in discrete time), the stabilizing solution of the ARE exists and solves this problem even when detectability fails. Its minimum may then be larger than the unconstrained one.
- **Discounted cost.** The cost $\sum_k \gamma^k (x_k^T Q x_k + u_k^T R u_k)$ with $0 < \gamma < 1$, which reduces to the standard problem (see Reductions).
- **Tracking.** The state should follow a reference $r$ in place of zero. With a constant reference, a shift of coordinates to the steady state, or an [integral state](/integral-state-feedback/), gives a regulator problem again.
- **Constraints.** With bounds on $u$ or $x$, the solution is no longer linear. [Linear MPC](/linear-mpc/) solves this case online with a [quadratic program](/quadratic-programming/).
- **Noise and output feedback.** With process and measurement noise and only $y$ measured, the problem becomes [LQG control](/lqg-control/), equivalently the [H2 optimal control](/h2-optimal-control/) problem.

## Examples

**Scalar, continuous time.** Take $\dot x = x + u$ with $q = r = 1$ and $T = \infty$. The CARE is $2 p - p^2 + 1 = 0$, with roots $p = 1 \pm \sqrt 2$. The stabilizing root is $p = 1 + \sqrt 2 \approx 2.414214$. The gain is $K = p = 1 + \sqrt 2$, the closed loop is $\dot x = -\sqrt 2\, x$, and the minimal cost from $x_0$ is $(1 + \sqrt 2) x_0^2$. Check by hand: with $u = -K x$, $x(t) = x_0 e^{-\sqrt 2 t}$ and the cost is $(1 + K^2) x_0^2 / (2 \sqrt 2) = (4 + 2 \sqrt 2) x_0^2 / (2 \sqrt 2) = (1 + \sqrt 2) x_0^2$.

**Double integrator.** Take $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $Q = I$ and $R = 1$. Write $P = \begin{bmatrix} p_1 & p_2 \\ p_2 & p_3 \end{bmatrix}$. The three entries of the CARE give $1 - p_2^2 = 0$, $p_1 - p_2 p_3 = 0$ and $2 p_2 - p_3^2 + 1 = 0$. The solution with $P > 0$ is

$$P = \begin{bmatrix} \sqrt 3 & 1 \\ 1 & \sqrt 3 \end{bmatrix}, \qquad K = \begin{bmatrix} 1 & \sqrt 3 \end{bmatrix}.$$

The closed loop has the characteristic polynomial $s^2 + \sqrt 3\, s + 1$, with roots $-0.866025 \pm 0.5 i$ and damping ratio $\sqrt 3 / 2$.

**Scalar, discrete time.** Take $x_{k+1} = x_k + u_k$ with $q = r = 1$. The DARE is $p = p - p^2 / (1 + p) + 1$, so $p^2 - p - 1 = 0$, and $p = (1 + \sqrt 5)/2 \approx 1.618034$, the golden ratio. The gain is $K = p / (1 + p) \approx 0.618034$, and the closed loop is $x_{k+1} = 0.381966\, x_k$.

**No detectability.** Take $\dot x = x + u$ with $q = 0$ and $r = 1$. The input $u = 0$ costs nothing, so it is optimal, but $x(t) = x_0 e^t$ grows without bound. The CARE $2 p - p^2 = 0$ has the solutions $p = 0$, which gives this input, and $p = 2$, which is the stabilizing solution. If only inputs with $x \to 0$ are allowed, the minimum is $2 x_0^2$, attained by $u = -2 x$.

**Not stabilizable.** Take $\dot x = x$ with $B = 0$ and $q = 1$. No input acts on the state, the cost is infinite for every $x_0 \ne 0$, and the infinite-horizon problem has no solution.

## Known algorithms

- [Finite-horizon LQR](/finite-horizon-lqr/): the backward Riccati recursion in discrete time, $O(N (n^3 + m^3))$ arithmetic operations and exact in rational arithmetic, or the Riccati differential equation integrated backward.
- Batch least squares: in discrete time, stack $u_0, \dots, u_{N-1}$ into one vector. The cost is a convex quadratic in that vector, so the minimizer solves one [least squares problem](/least-squares-problem/) of size $N m$. Dense, this costs $O(N^3 m^3)$, more than the recursion, but it extends to constraints as a quadratic program.
- [Infinite-horizon LQR](/infinite-horizon-lqr/): the finite-horizon recursion run to its limit, which is value iteration in discrete time.
- [Schur method](/schur-method-riccati/): an ordered Schur form of the [Hamiltonian matrix](/hamiltonian-matrix/) gives the stable invariant subspace and $P$, in $O(n^3)$ operations. It is the usual dense method.
- [Kleinman iteration](/kleinman-iteration/): Newton's method on the CARE, one [Lyapunov equation](/lyapunov-equation/) per step, from a stabilizing initial gain. Hewer's method is the discrete version.
- Doubling algorithms and the matrix sign function, both with quadratic convergence (Bini, Iannazzo and Meini).
- [Semidefinite programming](/semidefinite-programming/): the stabilizing solution is the largest symmetric $P$ that satisfies the [linear matrix inequality](/linear-matrix-inequality/) $\begin{bmatrix} A^T P + P A + Q & P B \\ B^T P & R \end{bmatrix} \ge 0$, so it maximizes $\operatorname{trace} P$ over that set. This is slower than the Schur method, but it combines with other LMI constraints.

## Bounds

- The finite-horizon discrete problem with rational data has a rational solution, and the recursion computes it exactly with $O(N (n^3 + m^3))$ operations on rational numbers.
- The infinite-horizon problem has no exact finite algorithm in general. The entries of $P$ are algebraic numbers, and the scalar examples above already give $1 + \sqrt 2$ and $(1 + \sqrt 5)/2$. All practical methods are iterative, with a stopping test on the Riccati residual.
- Monotonicity (a theorem): the minimal cost does not decrease when $Q$ or $R$ increases, and in discrete time the cost of horizon $N$ with $Q_f = 0$ does not decrease with $N$ and is at most the infinite-horizon cost.
- The size of the gain (a rule of thumb): scaling $R$ down by a factor makes the gain larger and the closed loop faster, at the price of larger inputs and more sensitivity to noise and unmodeled dynamics.

## Reductions

- **Cross term to no cross term.** Set $u = v - R^{-1} S^T x$. Then $x^T Q x + 2 x^T S u + u^T R u = x^T (Q - S R^{-1} S^T) x + v^T R v$, and the plant becomes $\dot x = (A - B R^{-1} S^T) x + B v$. Solve this problem for $P$; the optimal input of the original problem is $u = -R^{-1} (B^T P + S^T) x$. The same change works in discrete time.
- **Discounted to undiscounted.** With $\tilde x_k = \gamma^{k/2} x_k$ and $\tilde u_k = \gamma^{k/2} u_k$, the plant becomes $\tilde x_{k+1} = \sqrt\gamma\, (A \tilde x_k + B \tilde u_k)$ and the cost loses its discount. Detectability and stabilizability are now asked of $(\sqrt\gamma\, A, \sqrt\gamma\, B)$.
- **LQR as a special case.** It is the [H2 optimal control](/h2-optimal-control/) problem with the full state measured and no noise on the measurement, and a special case of the [optimal control problem](/optimal-control-problem/). The [Pontryagin maximum principle](/pontryagin-maximum-principle/) and the [Hamilton-Jacobi-Bellman equation](/hamilton-jacobi-bellman-equation/) both give the Riccati solution: the costate is a fixed multiple of $P x$ (the factor depends on how the Hamiltonian is scaled), and the value function is $x^T P x$.
- **Duality with estimation.** The steady-state [Kalman filter](/kalman-filter/) for $(A, C)$ with noise covariances $W$ and $V$ solves the Riccati equation of the LQR problem for $(A^T, C^T)$ with weights $W$ and $V$. So any LQR solver is also a Kalman filter solver.
- **Minimum energy control.** With $Q = 0$ and a fixed final state in place of a terminal cost, the problem becomes [minimum energy control](/minimum-energy-control/), which the controllability Gramian solves.

## Applications

- State feedback design for aircraft, spacecraft attitude and other multivariable plants, where pole placement leaves too many free parameters and the weights are easier to tune.
- The state feedback half of [LQG control](/lqg-control/), with a [Kalman filter](/kalman-filter/) as the other half. The margins of the next point are then lost (see the [LQR stability margins](/lqr-stability-margins/) page).
- A design with guaranteed robustness: in continuous time with one input, the LQR loop has a gain margin of $[1/2, \infty)$ and a phase margin of at least 60 degrees.
- The terminal cost and the local controller of [model predictive control](/mpc-stability-theorem/): the infinite-horizon cost $x^T P x$ and the gain $K$ are the usual choices.
- Inside iterative methods for nonlinear optimal control, which solve a time-varying LQR problem around the current trajectory at each step.

## References
