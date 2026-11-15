---
tag: R448P7
kind: algorithm
slug: linear-mpc
name: Linear MPC as a quadratic program
aliases:
- linear model predictive control
- linear quadratic MPC
area: control/optimal-and-predictive-control
level: core
summary: For a linear model, a quadratic cost and linear constraints, each MPC step is a convex QP in the N m future inputs; the controller applies the first input and repeats.
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs, N: the horizon, c: "the number of constraint rows, 2 N m + 2 N n plus the terminal rows for box limits", t: the number of QP iterations at one sampling instant}
  time: {worst: "O(t (c N m + N^2 m^2))", offline: "O(N^3 (n + m)^3)"}
  space: {extra: "O(N^2 m^2 + c (N m + n))"}
properties: {deterministic: true, exact: true, recursive: false, online: true}
history:
  year: 1986
  people: [Carlos E. García, A. M. Morshedi, Kenneth R. Muske, James B. Rawlings]
  note: "García and Morshedi (1986) posed the constrained move problem of DMC as a quadratic program (QDMC); Muske and Rawlings (1993) gave the state-space form with a terminal cost."
prereqs: [model-predictive-control, quadratic-programming, finite-horizon-lqr, state-space-representation]
see_also: [kkt-conditions, explicit-mpc, maximal-positively-invariant-set, mpc-stability-theorem, recursive-feasibility, infinite-horizon-lqr, dynamic-matrix-control, interior-point-method]
sources:
  - paper: doi:10.1080/00986448608911397
    title: Carlos E. García and A. M. Morshedi, Quadratic programming solution of dynamic matrix control (QDMC), Chemical Engineering Communications 46(1-3), 73-87, 1986
    locator: the move problem of DMC with input and output constraints written as a quadratic program
  - paper: doi:10.1002/aic.690390208
    title: Kenneth R. Muske and James B. Rawlings, Model predictive control with linear models, AIChE Journal 39(2), 262-287, 1993
    locator: linear MPC in state-space form with an infinite horizon cost replaced by a terminal penalty
  - paper: doi:10.1007/BF02591962
    title: D. Goldfarb and A. Idnani, A numerically stable dual method for solving strictly convex quadratic programs, Mathematical Programming 27(1), 1-33, 1983
    locator: the dual active set method that starts at the unconstrained minimum and adds violated constraints one at a time
  - paper: doi:10.1016/S0005-1098(99)00214-9
    title: D. Q. Mayne, J. B. Rawlings, C. V. Rao and P. O. M. Scokaert, Constrained model predictive control, stability and optimality, Automatica 36(6), 789-814, 2000
    locator: the terminal cost and terminal set conditions for linear MPC and the decrease of the optimal cost
  - paper: doi:10.1016/S0005-1098(01)00174-1
    title: Alberto Bemporad, Manfred Morari, Vivek Dua and Efstratios N. Pistikopoulos, The explicit linear quadratic regulator for constrained systems, Automatica 38(1), 3-20, 2002
    locator: the MPC law is continuous and piecewise affine and the value function is convex and piecewise quadratic
  - book: isbn:9780975937730
    title: James B. Rawlings, David Q. Mayne and Moritz M. Diehl, Model Predictive Control, Theory, Computation, and Design, 2nd edition, Nob Hill Publishing, 2017
    locator: Chapter 2, regulation, the linear quadratic problem with constraints
  - book: isbn:9781107016880
    title: Francesco Borrelli, Alberto Bemporad and Manfred Morari, Predictive Control for Linear and Hybrid Systems, Cambridge University Press, 2017
    locator: the chapters on constrained optimal control of linear systems with a quadratic cost and on receding horizon control, with the batch (condensed) formulation
---

Linear MPC is [model predictive control](/model-predictive-control/) for the linear model $x_{k+1} = A x_k + B u_k$ with a quadratic cost and linear constraints on inputs and states. At each sampling instant the controller measures $x$, solves a convex [quadratic program](/quadratic-programming/) (QP) in the future inputs $u_0, \dots, u_{N-1}$, applies $u_0$, and repeats at the next instant. When the states are eliminated, the QP has $N m$ variables and a positive definite Hessian that does not depend on $x$; only the linear term and the right-hand side of the constraints change with $x$. This page builds that condensed QP, solves it with the dual active set method of Goldfarb and Idnani (1983), and checks the result with the [KKT conditions](/kkt-conditions/). Without active constraints and with the [DARE](/discrete-algebraic-riccati-equation/) solution as terminal cost, the law is the [infinite-horizon LQR](/infinite-horizon-lqr/) gain $u = -K x$.

## In plain words

The controller has a model that says how the system moves for each input. At each tick it looks at the present state and plans the inputs for the next few ticks. It picks the plan that keeps the states small and uses little input, and it respects the limits on inputs and states. For this kind of model and cost, the best plan is the answer to a standard and well understood optimization problem, a quadratic program, with one unique solution. The controller sends only the first input of the plan. At the next tick it measures again and makes a new plan. So the plan always starts from the real state, and errors of the model do not build up along the plan.

## The problem

Input: matrices $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, weights $Q \ge 0$, $R > 0$ and a terminal weight $P \ge 0$, a horizon $N \ge 1$, bounds $u_{\min} \le u_k \le u_{\max}$ for $k = 0, \dots, N - 1$, bounds $x_{\min} \le x_k \le x_{\max}$ for $k = 1, \dots, N$, an optional terminal set $\mathbb{X}_f = \{x : H_f x \le h_f\}$, and the current state $x$.

Output: the input $u_0^*(x)$, the first part of the minimizer of

$$V_N(x) = \min_{u_0, \dots, u_{N-1}} \sum_{k=0}^{N-1} \left(x_k^T Q x_k + u_k^T R u_k\right) + x_N^T P x_N$$

subject to $x_0 = x$, $x_{k+1} = A x_k + B u_k$ and the constraints, or the report that no input sequence meets the constraints. The map $\kappa_N(x) = u_0^*(x)$ is the MPC law. The set of $x$ for which the problem has a solution is the feasible set $\mathcal{X}_N$.

**Condensed form.** Stack $U = (u_0, \dots, u_{N-1}) \in \mathbb{R}^{Nm}$ and $X = (x_1, \dots, x_N)$. The model gives $X = \Phi x + \Gamma U$, where block row $k$ of $\Phi$ is $A^k$ and block $(k, j)$ of $\Gamma$ is $A^{k-1-j} B$ for $j < k$ and 0 otherwise. With $\bar Q = \mathrm{diag}(Q, \dots, Q, P)$ and $\bar R = \mathrm{diag}(R, \dots, R)$,

$$J = U^T H U + 2 (F x)^T U + x^T (Q + \Phi^T \bar Q \Phi) x, \qquad H = \Gamma^T \bar Q \Gamma + \bar R, \qquad F = \Gamma^T \bar Q \Phi.$$

All constraints become $G U \le w + E x$, with one row per bound. So each sampling instant solves

$$\min_U \ \tfrac12 U^T H U + (F x)^T U \quad \text{subject to} \quad G U \le w + E x,$$

which has the same minimizer as $J$. $H \ge \bar R > 0$, so the QP is strictly convex and has exactly one solution when it is feasible.

**Sparse form.** Keep the states as variables instead. The QP then has $N (n + m)$ variables, the $N n$ equality constraints $x_{k+1} = A x_k + B u_k$, and the bounds as simple bounds. Its KKT matrix is block banded, which is the reason that large horizons use this form.

## The algorithm

```pseudo id=main
LINEAR-MPC-SETUP(A, B, Q, R, P, N, bounds, H_f, h_f)        ▷ once, offline
L1   (Φ, Γ) ← prediction matrices, X = Φ x + Γ U
L2   H ← Γᵀ Q̄ Γ + R̄;  F ← Γᵀ Q̄ Φ                          ▷ H is Nm × Nm and positive definite
L3   (G, w, E) ← one row per bound: G U ≤ w + E x
MPC-STEP(x)                                                  ▷ at each sampling instant
L4   f ← F x;  b ← w + E x
L5   (U, λ) ← QP-SOLVE(H, f, G, b)
L6   if QP-SOLVE reports infeasible then raise Infeasible
L7   return u_0 = U[1..m]
QP-SOLVE(H, f, G, b)                                         ▷ dual active set, Goldfarb and Idnani
L8   z ← -H⁻¹ f;  W ← ∅;  λ_W ← ()                           ▷ unconstrained minimum
L9   repeat
L10      p ← the row with the largest violation s_p = g_pᵀ z - b_p
L11      if s_p ≤ tol then return (z, λ, W)                   ▷ z is primal feasible
L12      λ_p ← 0
L13      repeat
L14          r ← (N_Wᵀ H⁻¹ N_W)⁻¹ N_Wᵀ H⁻¹ g_p;  d ← H⁻¹ (g_p - N_W r)
L15          t₁ ← min over k in W with r_k > 0 of λ_k / r_k     ▷ partial step, ∞ if none
L16          t₂ ← (g_pᵀ z - b_p) / (g_pᵀ d) if g_pᵀ d > 0, else ∞   ▷ full step
L17          if t₁ = t₂ = ∞ then raise Infeasible
L18          t ← min(t₁, t₂);  z ← z - t d;  λ_W ← λ_W - t r;  λ_p ← λ_p + t
L19          if t = t₂ then add p to W with λ_p and leave the inner loop
L20          else drop from W the row k that reached λ_k = 0
```

Lines L1 to L3 run once, because $H$, $F$, $G$, $w$ and $E$ do not depend on the state. Line L4 is the only place where the measured state enters: it moves the linear term and the right-hand side. The columns of $N_W$ are the rows $g_j$ of $G$ for $j \in W$.

The QP solver keeps a pair $(z, W)$ in which $z$ is the minimizer of the objective subject to the rows in $W$ held as equalities, with nonnegative multipliers $\lambda_W$. Line L8 starts at the unconstrained minimizer with $W$ empty, which is such a pair. Each pass of the outer loop picks a violated row $p$ (line L10). The inner loop moves $z$ along $-d$, the direction that reduces the violation of row $p$ and keeps the rows in $W$ as equalities, while it raises $\lambda_p$ and changes $\lambda_W$ along $-r$. The full step $t_2$ makes row $p$ hold with equality; the partial step $t_1$ stops when an active multiplier reaches 0, and that row is dropped (line L20). If neither step is finite, the violated row cannot be met together with the rows in $W$, and the QP is infeasible (line L17). The method needs no feasible start, which is the reason it suits MPC: the unconstrained minimizer is the LQR plan, and in most instants only a few constraints are active.

## Example

Take the double integrator sampled with $h = 1$ s by [zero-order hold](/zero-order-hold-discretization/): $A = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}$, $B = \begin{bmatrix} 0.5 \\ 1 \end{bmatrix}$, with $Q = I$, $R = 1$ and $N = 5$. The terminal weight $P$ is the DARE solution

$$P = \begin{bmatrix} 2.367101 & 1.118034 \\ 1.118034 & 2.587483 \end{bmatrix}, \qquad P_{12} = \sqrt 5 / 2, \qquad K = \begin{bmatrix} 0.434483 & 1.028466 \end{bmatrix}.$$

The constraints are $|u_k| \le 1$ and $|x_{k,i}| \le 5$, and the terminal set $\mathbb{X}_f$ is the [maximal positively invariant set](/maximal-positively-invariant-set/) of $x^+ = (A - BK) x$ inside these limits:

$$|x_1| \le 5, \qquad |0.434483\, x_1 + 1.028466\, x_2| \le 1, \qquad |0.106756\, x_1 - 0.181781\, x_2| \le 1.$$

**QP size.** The condensed QP has $N m = 5$ variables and 36 rows: 10 input bounds, 20 state bounds and 6 terminal rows. The sparse form has 15 variables, 10 equalities and the same 36 inequalities. For $N = 3$ the condensed QP has 3 variables and 24 rows; for $N = 10$ it has 10 variables and 66 rows. The first row of $H$ is $(86.5836, 65.0636, 45.5436, 28.0236, 13.5036)$.

**One QP from $x = (-5, 3)$.** Line L8 gives the unconstrained plan $z = (-0.9130, -1.0791, -0.6416, -0.2803, -0.0903)$. Its first entry is the LQR input $-K x = -0.9130$, as it must be with $P$ from the DARE. Only one row is violated: $u_1 \ge -1$, by $0.0791$. One full step (lines L14 to L19) makes it active with $\lambda = 0.1643$, and the next pass finds no violation. The result is

$$U^* = (-0.9516, -1, -0.6753, -0.2896, -0.0910), \qquad V_5(x) = 48.9369.$$

The MPC input $-0.9516$ differs from the LQR input $-0.9130$: the plan knows that $u_1$ will saturate and pushes a little harder now. The KKT residual of the result is below $10^{-9}$.

**Other states.** From $x = (3, 2)$ the unconstrained plan starts with $u_0 = -3.3604$. The solution has $u_0, u_1, u_2$ at $-1$, with multipliers $36.03$, $18.24$ and $6.21$: $U^* = (-1, -1, -1, -0.9267, 0.6622)$ and $V_5 = 102.709$. From $x = (-4.5, 2)$ no row is active, and the input is the LQR input $-0.1018$ with $V_5 = 38.1591$. From $x = (4, 2)$ the QP is infeasible: even $u_0 = -1$ gives $x_{1,1} = 4 + 2 - 0.5 = 5.5 > 5$.

**Closed loop from $(-5, 3)$.** Applying $u_0$ and solving again at each instant gives (measurement of the implementation):

| $k$ | $x_k$ | $u_k$ | $V_5(x_k)$ | active rows |
|---|---|---|---|---|
| 0 | $(-5, 3)$ | $-0.9516$ | 48.9369 | $u_1 \ge -1$ |
| 1 | $(-2.4758, 2.0484)$ | $-1$ | 14.0313 | $u_0 \ge -1$ |
| 2 | $(-0.9274, 1.0484)$ | $-0.6753$ | 2.7058 | none |
| 3 | $(-0.2167, 0.3731)$ | $-0.2896$ | 0.2906 | none |
| 4 | $(0.0116, 0.0835)$ | $-0.0910$ | 0.0205 | none |

From $k = 2$ on no constraint is active and $u_k = -K x_k$. Each value drops by at least the stage cost $x_k^T Q x_k + u_k^T R u_k$, as the [MPC stability theorem](/mpc-stability-theorem/) says, and the state goes to the origin while every constraint holds.

## Correctness

The full proofs are in proofs/correctness.md. There are three parts.

1. **The condensed QP is the MPC problem.** By induction on $k$, $x_k = A^k x + \sum_{j<k} A^{k-1-j} B u_j$, which is block row $k$ of $\Phi x + \Gamma U$. Substituting it into the cost and the constraints gives the formulas for $H$, $F$, $G$, $w$ and $E$ above. $H \ge \bar R > 0$ because $\Gamma^T \bar Q \Gamma \ge 0$. So the QP has at most one minimizer, and $J$ and the QP objective differ by a positive factor and a constant.
2. **The QP solver returns the minimizer or a correct infeasibility report.** The invariant is that $z$ minimizes the objective subject to the rows in $W$ as equalities, with $\lambda_W \ge 0$. A full step adds row $p$ and keeps the invariant, a partial step drops a row whose multiplier reached 0, and each full step increases the dual objective strictly, so no active set repeats and the method stops. When it stops at line L11, $z$ is feasible and the pair $(z, \lambda)$ meets the KKT conditions, which for a convex QP prove optimality. When it stops at line L17, a Farkas-type argument shows that the rows in $W$ and row $p$ have no common point. This is the proof of Goldfarb and Idnani (1983), written out in the proof file. The tests check the KKT residual at random states, and compare the solver with a brute force over all active sets on small random QPs.
3. **The closed loop.** If $\mathbb{X}_f$ is positively invariant under $u = -K x$, the constraints hold in it, and $P$ satisfies $P = Q + K^T R K + (A - BK)^T P (A - BK)$, then the shifted plan $(u_1^*, \dots, u_{N-1}^*, -K x_N^*)$ is feasible at the next state and $V_N(x^+) \le V_N(x) - x^T Q x - u_0^T R u_0$. This is the argument of the [MPC stability theorem](/mpc-stability-theorem/), and it gives [recursive feasibility](/recursive-feasibility/). The DARE solution $P$ with its gain $K$ meets the Lyapunov identity.

## Complexity

Costs are in the [real-RAM model](/real-ram/), with $n$ states, $m$ inputs, horizon $N$ and $c$ constraint rows. For box limits on inputs and states, $c = 2 N m + 2 N n$ plus the terminal rows.

- **Offline (lines L1 to L3).** The powers $A^k$ cost $O(N n^3)$. $\Gamma^T \bar Q \Gamma$ and $\Gamma^T \bar Q \Phi$ cost $O(N^3 n^2 m)$ by direct products, and a Cholesky factorization of $H$ costs $O(N^3 m^3)$. Together this is $O(N^3 (n + m)^3)$ at most.
- **Per sampling instant (lines L4 to L7).** Line L4 costs $O(N m n + c n)$. The QP is the main cost. With factorizations that are updated when a row enters or leaves $W$, as in the Goldfarb and Idnani method, one iteration costs $O(N^2 m^2)$ for the update and $O(c N m)$ to find the most violated row, so $t$ iterations cost $O(t (c N m + N^2 m^2))$ per sampling instant. Finite termination is a theorem; the paper gives no polynomial bound on the number of iterations. For MPC the count is usually close to the number of rows that are active at the solution (rule of thumb). In the example below, one QP needs one full step.
- **The simple code.** The implementation recomputes $N_W^T H^{-1} N_W$ in every inner step, which costs $O(|W|^2 N^2 m^2)$ per step. That is enough for the small QPs of the examples.
- **Sparse form.** With $N(n+m)$ variables, a block banded factorization of the KKT matrix costs $O(N (n + m)^3)$, linear in $N$. An [interior point method](/interior-point-method/) on the sparse form therefore costs $O(N (n + m)^3)$ per iteration, and its number of iterations has a bound that grows with $\sqrt{c}$ and $\log(1/\epsilon)$ for accuracy $\epsilon$.

Space: $H$ needs $O(N^2 m^2)$ and the constraint data $O(c (N m + n))$.

## Properties

- **Strict convexity.** For $R > 0$ the QP has a unique solution for every feasible $x$ (theorem, from $H > 0$).
- **Piecewise affine law.** $\kappa_N$ is continuous and piecewise affine on a partition of $\mathcal{X}_N$ into polyhedra, and $V_N$ is convex and piecewise quadratic (theorem, Bemporad, Morari, Dua and Pistikopoulos 2002; see [explicit MPC](/explicit-mpc/) and [multiparametric quadratic programming](/multiparametric-quadratic-programming/)).
- **LQR near the origin.** If $P$ is the DARE solution and no constraint is active at the unconstrained plan, then $\kappa_N(x) = -K x$ (theorem: the unconstrained plan of the finite horizon problem with terminal cost $P$ is $u_k = -K x_k$, by the [principle of optimality](/principle-of-optimality/)). In the example this holds from $k = 2$.
- **Feasible set.** $\mathcal{X}_N$ is a polyhedron, the projection of the feasible set of $(x, U)$ on $x$. It grows with $N$ when $\mathbb{X}_f$ is control invariant.
- **Closed-loop guarantees.** They need the terminal ingredients: see [MPC stability theorem](/mpc-stability-theorem/) and [recursive feasibility](/recursive-feasibility/). Without them a finite horizon MPC can lose feasibility or give a closed loop that is not asymptotically stable.

## Variants and improvements

- **Sparse QP with a structured solver.** Keep the states as variables and exploit the banded KKT matrix. The cost per iteration is linear in $N$. Use it for long horizons or many states.
- **Interior point and first order methods.** An [interior point method](/interior-point-method/) has a polynomial iteration bound. Projected or accelerated gradient methods suit box constraints on inputs only, where the projection is a clip.
- **Warm start.** Start an active set method from the active set of the previous instant, shifted by one step. It often saves iterations, because the active set changes little between instants (rule of thumb, no bound).
- **Explicit MPC.** Solve the QP for all $x$ offline as a [multiparametric QP](/multiparametric-quadratic-programming/), and evaluate a piecewise affine function online. See [explicit MPC](/explicit-mpc/).
- **Input moves and tracking.** Use $\Delta u_k = u_k - u_{k-1}$ as variables and penalize them, or track a reference with the state and input targets of [offset-free MPC](/offset-free-mpc/).
- **Soft state constraints.** Add slack variables with a linear and a quadratic penalty. An $\ell_1$ penalty with a weight larger than the largest multiplier of the hard problem gives the hard solution whenever the hard problem is feasible (exact penalty theorem), and the QP stays feasible when it is not.
- **Robust variants.** [Tube MPC](/tube-mpc/) and [min-max MPC](/min-max-mpc/) handle bounded disturbances.

## When to use it

Use it for a plant with a good linear model near the operating point, a few to a few hundred states, and hard limits on inputs or states that matter for performance. The sampling period must be long enough to solve the QP in the worst case; measure the solve time of the chosen solver on the target hardware. If no constraint is ever active, the [infinite-horizon LQR](/infinite-horizon-lqr/) gives the same law at a lower cost. If the model is nonlinear far from one operating point, use [nonlinear MPC](/nonlinear-mpc/). For a step response model of an asymptotically stable plant, as in process control, [DMC](/dynamic-matrix-control/) is the older form of the same idea.

## Pitfalls

- **Infeasibility at run time.** A disturbance can push the state out of $\mathcal{X}_N$, and the QP then has no solution. Plan for it: soften the state constraints, or keep a backup input. The example state $(4, 2)$ shows the case.
- **No terminal ingredients.** With $P = Q$ and no terminal set, a short horizon can give a closed loop that is not asymptotically stable, even with no constraint active. Use the DARE terminal cost and an invariant terminal set, or check the closed loop.
- **Conditioning of the condensed form.** For an $A$ that is not Schur, the powers $A^k$ grow, $H$ becomes badly conditioned for long $N$, and the condensed QP loses accuracy. Use the sparse form, or prestabilize with $u = -K x + v$ and optimize $v$.
- **Trusting the solver's flag.** Check the result with the KKT conditions when you test a solver, as the tests here do. A solver that stops at its iteration limit can return a point that is not optimal.
- **State constraints at $k = 0$.** The current state is measured, not chosen. Constraints apply from $k = 1$; a constraint at $k = 0$ only makes the QP infeasible when it is violated.
- **Sampling time and delay.** The QP takes time. If the solve uses a large part of the period, the input acts late. Model the delay as an extra state, or compute the plan for the predicted next state.
- **Constraint scaling.** Rows with very different scales make the tolerance test at line L11 meaningless for some rows. Scale the constraints to similar magnitudes.

## Implementations

## History

Predictive control with a step response model and an online optimization came from the process industry in the late 1970s; see [dynamic matrix control](/dynamic-matrix-control/) for that history. García and Morshedi (1986) wrote the constrained DMC move problem as a quadratic program, which is the form on this page. Muske and Rawlings (1993) put linear MPC in state-space form, with a terminal cost that makes the finite horizon problem equal to an infinite horizon one when no constraint is active. Mayne, Rawlings, Rao and Scokaert (2000) collected the conditions on the terminal cost and the terminal set that give closed-loop stability. The dual active set method used here is that of Goldfarb and Idnani (1983).

## References
