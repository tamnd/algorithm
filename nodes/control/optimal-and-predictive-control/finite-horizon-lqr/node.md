---
tag: 6S5J80
kind: algorithm
slug: finite-horizon-lqr
name: Finite-horizon LQR
aliases:
- Riccati recursion
- backward Riccati recursion
area: control/optimal-and-predictive-control
level: core
summary: Computes the time-varying optimal gains of a finite-horizon LQ problem by a Riccati difference or differential equation run backward.
solves: [lqr-problem]
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs, N: the number of steps of the horizon}
  time: {worst: "O(N (n^3 + m^3))"}
  space: {extra: "O(N n m + n^2)"}
properties: {deterministic: true, exact: true, recursive: false, online: false}
history:
  year: 1960
  people: [Rudolf E. Kalman]
  note: "Kalman (1960) solved the linear quadratic problem on a finite interval with the Riccati differential equation; the discrete recursion is the dynamic programming solution of the same problem."
prereqs: [lqr-problem, principle-of-optimality, bellman-equation, state-space-representation]
see_also: [infinite-horizon-lqr, discrete-algebraic-riccati-equation, continuous-algebraic-riccati-equation, kalman-filter, linear-mpc, linear-time-varying-system, zero-order-hold-discretization, value-iteration]
sources:
  - paper: "R. E. Kalman, Contributions to the theory of optimal control, Boletín de la Sociedad Matemática Mexicana 5(2), 102-119, 1960"
    locator: the regulator problem on a finite interval and the Riccati differential equation of the optimal cost
  - book: isbn:9780486457666
    title: Brian D. O. Anderson and John B. Moore, Optimal Control, Linear Quadratic Methods, Prentice Hall, 1990 (Dover reprint, 2007)
    locator: Chapter 2, The Standard Regulator Problem I
  - book: isbn:9780691151878
    title: Daniel Liberzon, Calculus of Variations and Optimal Control Theory, A Concise Introduction, Princeton University Press, 2012
    locator: Section 6.1, Finite-horizon LQR problem, with Section 6.1.2 on the Riccati differential equation
  - book: isbn:9781886529434
    title: Dimitri P. Bertsekas, Dynamic Programming and Optimal Control, Volume I, fourth edition, Athena Scientific, 2017
    locator: Section 3.1, Linear Systems and Quadratic Cost
---

Finite-horizon LQR computes the optimal input of the [linear quadratic regulator problem](/lqr-problem/) on a horizon of $N$ steps, or on a time interval $[0, T]$. The answer is a linear state feedback $u_k = -K_k x_k$ whose gain changes with time. In discrete time the gains come from a recursion on symmetric matrices $P_k$ that starts at the terminal weight $P_N = Q_f$ and runs backward to $k = 0$. In continuous time the same role is played by the Riccati differential equation, which is integrated backward from $P(T) = Q_f$. The matrix $P_k$ gives the optimal cost from step $k$: it is $x_k^T P_k x_k$. The page differs from [infinite-horizon LQR](/infinite-horizon-lqr/), where the horizon is unbounded and the gain is constant, and from the [discrete](/discrete-algebraic-riccati-equation/) and [continuous algebraic Riccati equations](/continuous-algebraic-riccati-equation/), which are the fixed points of the backward recursion.

## In plain words

You must steer a system for a fixed number of steps. Each step costs something for being far from zero and something for pushing hard, and the final position has its own cost. The trick is to plan from the end. At the last step there is nothing left to decide, so the cost is known. One step earlier, you can try every push, see where it lands, and add the known cost of that landing point. The best push turns out to be a fixed multiple of the current state, and the best cost is again a simple bowl-shaped function of the state. So the same reasoning repeats, one step earlier each time, back to the start. The output is one gain per step, computed once, before the system runs. While the system runs, the controller only multiplies the measured state by the gain of the current step.

## The problem

Discrete time. Input: $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, weights $Q = Q^T \ge 0$, $Q_f = Q_f^T \ge 0$ and $R = R^T > 0$, and a horizon $N \ge 0$. The plant is $x_{k+1} = A x_k + B u_k$ and the cost is

$$J(x_0, u_0, \dots, u_{N-1}) = \sum_{k=0}^{N-1} \left( x_k^T Q x_k + u_k^T R u_k \right) + x_N^T Q_f x_N.$$

Output: gains $K_0, \dots, K_{N-1} \in \mathbb{R}^{m \times n}$ such that, for every initial state $x_0$, the inputs $u_k = -K_k x_k$ minimize $J$ over all input sequences, and matrices $P_0, \dots, P_N$ such that the minimum of the cost from step $k$ and state $x$ is $x^T P_k x$.

Continuous time. The plant is $\dot x = A x + B u$ on $[0, T]$, and the cost is $\int_0^T (x^T Q x + u^T R u)\, dt + x(T)^T Q_f x(T)$. Output: the function $P(t)$ on $[0, T]$ and the gain $K(t) = R^{-1} B^T P(t)$. This page has no cross term $2 x^T S u$ in the cost; the Variants section gives the change for it. The plant data may also depend on $k$ or $t$; the recursion then uses $A_k$, $B_k$, $Q_k$, $R_k$ at step $k$ with no other change.

## The algorithm

```pseudo id=main
FINITE-HORIZON-LQR(A, B, Q, R, Q_f, N)
L1  P_N ← Q_f
L2  for k ← N - 1 down to 0
L3      S_k ← R + B^T P_(k+1) B                     ▷ m by m, positive definite
L4      K_k ← S_k^(-1) B^T P_(k+1) A                ▷ solve S_k K_k = B^T P_(k+1) A
L5      P_k ← Q + A^T P_(k+1) A - A^T P_(k+1) B K_k
L6  return (P_0, ..., P_N), (K_0, ..., K_(N-1))
```

Line L1 sets the cost of the last state. Lines L3 and L4 compute the optimal gain of step $k$ from the cost matrix of step $k + 1$; line L4 solves $S_k K_k = B^T P_{k+1} A$ and does not form $S_k^{-1}$. Line L5 is the Riccati difference equation. It can also be written $P_k = Q + K_k^T R K_k + (A - B K_k)^T P_{k+1} (A - B K_k)$, which is a sum of positive semidefinite terms and keeps the symmetry better in floating point. The implementation also replaces each float $P_k$ by $(P_k + P_k^T)/2$.

In continuous time the backward step is replaced by the Riccati differential equation

$$-\dot P(t) = A^T P(t) + P(t) A - P(t) B R^{-1} B^T P(t) + Q, \qquad P(T) = Q_f,$$

with the feedback $u(t) = -R^{-1} B^T P(t) x(t)$. The implementation integrates it in the backward time $\tau = T - t$ with the classical [Runge-Kutta](/runge-kutta-methods/) method of order 4 and a fixed step $T / s$ for $s$ steps. To apply the controller to a plant model in continuous time, it stores $P$ on a grid twice as fine as the simulation step, so every stage of the RK4 step of the plant has its own $P$.

## Example

**Scalar case.** Take $a = b = q = r = 1$, $q_f = 0$ and $N = 5$. Then $S_k = 1 + p_{k+1}$, $K_k = p_{k+1} / (1 + p_{k+1})$ and $p_k = 1 + p_{k+1} / (1 + p_{k+1})$. Starting from $p_5 = 0$:

| $k$ | 5 | 4 | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|---|
| $p_k$ | 0 | 1 | 3/2 | 8/5 | 21/13 | 55/34 |
| $K_k$ | | 0 | 1/2 | 3/5 | 8/13 | 21/34 |

The values are ratios of Fibonacci numbers, $p_{N-j} = F_{2j} / F_{2j-1}$ for $j \ge 1$. They increase toward the golden ratio $(1 + \sqrt 5)/2 = 1.618034$, and the gains increase toward $0.618034$. These limits are the solution and the gain of the scalar [DARE](/discrete-algebraic-riccati-equation/). The last gain $K_4$ is 0: with no terminal cost, the last input only costs and gains nothing.

**Sampled double integrator.** The [zero-order hold](/zero-order-hold-discretization/) model of $\ddot y = u$ with period 1 is $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$, $B = \begin{bmatrix} 1/2 \\ 1 \end{bmatrix}$. Weight the position only, $Q = Q_f = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$, with $R = 1$ and $N = 3$. At $k = 2$, line L3 gives $S_2 = 1 + 1/4 = 5/4$, and $B^T P_3 A = \begin{bmatrix} 1/2 & 1/2 \end{bmatrix}$, so line L4 gives $K_2 = \begin{bmatrix} 2/5 & 2/5 \end{bmatrix}$. Line L5 gives

$$P_2 = \begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix} + \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix} - \begin{bmatrix} 1/5 & 1/5 \\ 1/5 & 1/5 \end{bmatrix} = \begin{bmatrix} 9/5 & 4/5 \\ 4/5 & 4/5 \end{bmatrix}.$$

Two more steps give $K_1 = \begin{bmatrix} 34/61 & 58/61 \end{bmatrix}$, $K_0 = \begin{bmatrix} 466/949 & 938/949 \end{bmatrix}$ and $P_0 = \frac{1}{949}\begin{bmatrix} 1817 & 900 \\ 900 & 1388 \end{bmatrix}$. From $x_0 = (1, 0)$ the optimal cost is $1817/949 = 1.914647$. The tests check $P_0$ exactly against the minimum of $J$ over all three inputs, computed by one linear solve on the stacked input vector.

**Continuous double integrator.** For $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $Q = I$, $R = 1$ and $Q_f = 0$, the Riccati differential equation gives these values of $P(0)$:

| $T$ | $P_{11}(0) = P_{22}(0)$ | $P_{12}(0)$ |
|---|---|---|
| 1 | 0.964836 | 0.389571 |
| 2 | 1.536475 | 0.833236 |
| 5 | 1.730851 | 0.998961 |
| 10 | 1.732051 | 1.000000 |

As $T$ grows, $P(0)$ tends to $\begin{bmatrix} \sqrt 3 & 1 \\ 1 & \sqrt 3 \end{bmatrix}$, the stabilizing solution of the [CARE](/continuous-algebraic-riccati-equation/), and the gain tends to $\begin{bmatrix} 1 & \sqrt 3 \end{bmatrix}$. For the scalar plant $a = b = q = r = 1$ with $q_f = 0$, the equation is $-\dot p = 2p - p^2 + 1$, with the closed form $p(t) = (p_+ - w p_-)/(1 - w)$, where $p_\pm = 1 \pm \sqrt 2$ and $w = (p_+ / p_-)\, e^{-2\sqrt 2 (T - t)}$. For $T = 1$ it gives $p(0) = 1.689498$; the limit for large $T$ is $1 + \sqrt 2 = 2.414214$.

## Correctness

The full proof is in proofs/correctness.md. In short, it is an induction on $k$ from $N$ down to 0, using the [principle of optimality](/principle-of-optimality/): the optimal cost $V_k(x)$ from step $k$ satisfies the [Bellman equation](/bellman-equation/) $V_k(x) = \min_u \left( x^T Q x + u^T R u + V_{k+1}(A x + B u) \right)$ with $V_N(x) = x^T Q_f x$. If $V_{k+1}(x) = x^T P_{k+1} x$ with $P_{k+1} \ge 0$, the expression in the minimum is $u^T S_k u + 2 u^T B^T P_{k+1} A x + x^T (Q + A^T P_{k+1} A) x$. Because $S_k \ge R > 0$, it is a strictly convex quadratic in $u$, and completing the square gives the unique minimizer $u = -K_k x$ and the value $x^T P_k x$ with $P_k$ from line L5. The form $P_k = Q + K_k^T R K_k + (A - B K_k)^T P_{k+1} (A - B K_k)$ shows $P_k \ge 0$, which keeps the induction going. In continuous time, the identity $\frac{d}{dt} (x^T P x) = -x^T Q x - u^T R u + (u + K x)^T R (u + K x)$ along every trajectory, integrated from 0 to $T$, gives $J = x_0^T P(0) x_0 + \int_0^T (u + K x)^T R (u + K x)\, dt$. The proof file also shows that $P(t)$ exists on all of $[0, T]$.

The tests check the recursion in exact rational arithmetic against the stacked least squares minimum on random problems, check that the simulated cost of the feedback equals $x_0^T P_0 x_0$ exactly and that random other inputs cost more, check the scalar closed forms, and check that a long horizon gives the DARE and CARE solutions within $10^{-9}$.

## Complexity

In the [real RAM](/real-ram/), with dense matrices and flops counted as $O(n^3)$ for a dense product or factorization of size $n$:

- Line L3 costs $O(n^2 m + n m^2)$.
- Line L4 costs $O(n^2 m)$ for the right side and $O(m^3 + m^2 n)$ for the solve with $n$ right sides.
- Line L5 costs $O(n^3 + n^2 m)$.

One step costs $O(n^3 + n^2 m + n m^2 + m^3)$, which is $O(n^3 + m^3)$, and the whole recursion costs $O(N (n^3 + m^3))$. Storing all gains takes $O(N n m)$ space; the recursion itself needs $O(n^2 + n m)$. A controller that runs online pays $O(n m)$ per step for $u_k = -K_k x_k$. In continuous time, one RK4 step costs four evaluations of the right side, each $O(n^3 + m^3)$, and the number of steps is set by the accuracy wanted and by the stiffness of the equation, not by $n$.

The stacked formulation, which treats $(u_0, \dots, u_{N-1})$ as one vector of size $N m$, costs $O(N^3 m^3)$ for a dense solve. The backward recursion uses the stage structure and is linear in $N$.

## Properties

- **Feedback, not a fixed sequence.** The gains do not depend on $x_0$. The same gains are optimal from every initial state, and from every state reached at step $k$.
- **Symmetric and positive semidefinite.** Every $P_k$ is symmetric and $P_k \ge 0$, by the induction in the proof. If $Q > 0$, then $P_k \ge Q > 0$ for $k < N$.
- **Monotone in the horizon.** With $Q_f = 0$, the cost matrix $P_0$ of horizon $N$ does not decrease when $N$ grows, because a longer horizon adds nonnegative terms to the cost. The scalar example shows this.
- **Convergence for a long horizon.** If $(A, B)$ is [stabilizable](/stabilizability/) and $(Q^{1/2}, A)$ is [detectable](/detectability/), then $P_0 \to P$ as $N \to \infty$, where $P$ is the stabilizing solution of the DARE, for every $Q_f \ge 0$. Bertsekas (Section 3.1) proves this under the stronger hypotheses that $(A, B)$ is controllable and $(Q^{1/2}, A)$ is observable; the [stabilizing solution theorem](/stabilizing-riccati-solution-theorem/) gives the limit. With $Q_f = P$ the recursion stays at $P$ and the gain is constant.
- **Certainty equivalence.** If zero mean independent noise $w_k$ with finite covariance is added to the plant, the same gains minimize the expected cost (Bertsekas, Section 3.1). The noise only adds a constant to the cost.
- **Duality with the Kalman filter.** With $A \to A^T$, $B \to C^T$, $Q \to$ process noise covariance and $R \to$ measurement noise covariance, line L5 becomes the covariance recursion of the [Kalman filter](/kalman-filter/), which runs forward in time.

## Variants and improvements

- **Time-varying data.** For $x_{k+1} = A_k x_k + B_k u_k$ and weights $Q_k$, $R_k$, use the data of step $k$ in lines L3 to L5. In continuous time this is the [linear time-varying system](/linear-time-varying-system/) case.
- **Cross term.** For a cost term $2 x_k^T S u_k$, replace $B^T P_{k+1} A$ by $B^T P_{k+1} A + S^T$ in line L4, and line L5 becomes $P_k = Q + A^T P_{k+1} A - (A^T P_{k+1} B + S) K_k$. The weight matrix $\begin{bmatrix} Q & S \\ S^T & R \end{bmatrix}$ must be positive semidefinite with $R > 0$.
- **Tracking.** To follow a known reference, add an affine term: the value function becomes $x^T P_k x + 2 q_k^T x + c_k$, and $q_k$ follows a linear backward recursion next to $P_k$.
- **Sampled continuous cost.** To minimize a continuous cost with a held input, sample the plant with the [zero-order hold](/zero-order-hold-discretization/) and compute the matching $Q$, $S$ and $R$ by one block matrix exponential (Van Loan 1978). The result has a cross term even when the continuous cost has none.
- **Square root forms.** For poorly conditioned data, propagate a Cholesky factor of $P_k$ with orthogonal transformations instead of $P_k$ itself, as in square root Kalman filters.
- **Constraints.** With bounds on $u_k$ or $x_k$ the value function is no longer quadratic, and the problem becomes a quadratic program; see [linear MPC](/linear-mpc/), which repeats a finite-horizon problem at every sampling instant.

## When to use it

Use it when the task has a natural end: a maneuver with a fixed duration, a landing, a batch process, or the inner problem of model predictive control without constraints. It is also the right tool for time-varying plants, where no constant gain exists, for example a trajectory that was linearized along a nominal path. For regulation about an equilibrium over a long time, use [infinite-horizon LQR](/infinite-horizon-lqr/) instead. Its constant gain is simpler to implement, and it comes with the stability guarantee that a finite horizon does not give.

## Pitfalls

- **Wrong direction.** The recursion runs backward from $Q_f$. Running line L5 forward from $P_0 = Q_f$ computes the gains of a different problem. In continuous time, integrating the Riccati differential equation forward from $P(0) = Q_f$ is a sign error, and the solution can blow up.
- **Index shift.** The gain $K_k$ uses $P_{k+1}$, not $P_k$. An off-by-one error here gives a feedback that looks reasonable and is not optimal.
- **No stability from a finite horizon.** The time-varying gains are optimal for the horizon, but the gains near the end are small (here $K_{N-1} = 0$ when $Q_f = 0$). Repeating the first gain $K_0$ forever as a constant feedback is not guaranteed to give a Schur closed loop unless $Q_f$ is chosen well, for example equal to the DARE solution. This is the stability problem of receding horizon control that the [MPC stability theorem](/mpc-stability-theorem/) addresses.
- **Loss of symmetry.** In floating point, the form in line L5 can lose symmetry and even positive semidefiniteness. Symmetrize, or use the form $Q + K_k^T R K_k + (A - B K_k)^T P_{k+1} (A - B K_k)$.
- **Stiff differential equation.** The Riccati differential equation can be stiff when the closed loop has fast and slow modes. A fixed step explicit method then needs a small step. The tests use RK4 with steps of at most $0.01$ on plants with eigenvalues of size about 1.
- **The name.** "Riccati recursion" also names the covariance update of the Kalman filter, so say which one is meant.

## Implementations

## History

Kalman (1960) posed the regulator problem for linear systems with a quadratic cost and showed that the optimal control on a finite interval is a linear feedback whose gain comes from a Riccati differential equation solved backward from the terminal time. The discrete version follows from Bellman's dynamic programming, which was developed in the 1950s. Kalman's paper also studied the limit of an unbounded horizon. The textbooks of Anderson and Moore made the backward Riccati equation the standard tool of the area; their 1990 book is the one cited here.

## References
