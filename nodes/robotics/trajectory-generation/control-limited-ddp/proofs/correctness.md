---
title: Control-limited DDP keeps the controls in the box, lowers the cost at every accepted iteration, is exact for linear-quadratic problems, and stops only near a first-order point
proves: [correctness]
status: full
---

We use the notation of the page and of the code. The problem is to minimize $J(U) = \sum_{k=0}^{N-1} \ell(x_k, u_k) + \ell_f(x_N)$ subject to $x_{k+1} = f(x_k, u_k)$ with $x_0$ given and $lo \le u_k \le hi$. The cost is $\ell(x, u) = \frac12 (x - g)^{\mathsf T} Q (x - g) + \frac12 u^{\mathsf T} R u$ and $\ell_f(x) = \frac12 (x - g)^{\mathsf T} Q_f (x - g)$ with $Q, Q_f$ positive semidefinite and $R$ positive definite. At stage $k$, $A_k = f_x(x_k, u_k)$ and $B_k = f_u(x_k, u_k)$. The stage model of line L6 is

$$q_k(\delta) = \tfrac12 \delta^{\mathsf T} H_k \delta + Q_{u,k}^{\mathsf T} \delta, \qquad H_k = Q_{uu,k} + \mu I,$$

over the box $\mathcal B_k = \{\delta : lo - u_k \le \delta \le hi - u_k\}$, and the expected change of line L9 is $\Delta V(\alpha) = \sum_k \bigl(\alpha\, k_k^{\mathsf T} Q_{u,k} + \frac12 \alpha^2 k_k^{\mathsf T} H_k k_k\bigr) = \sum_k q_k(\alpha k_k)$.

The method is local. Nothing below says that it converges to a global minimum, or that the line search of line L10 always succeeds.

## Lemma 1: the box quadratic program

**Claim.** Let $H$ be positive definite. (a) The problem $\min \frac12 \delta^{\mathsf T} H \delta + c^{\mathsf T}\delta$ over a box has exactly one minimizer, and a feasible $\delta$ is that minimizer if and only if, with $\gamma = H\delta + c$, for each $i$: $\gamma_i = 0$ if $\delta_i$ is strictly inside its bounds, $\gamma_i \ge 0$ if $\delta_i$ is at its lower bound, and $\gamma_i \le 0$ if it is at its upper bound. (b) The solver `box_qp` started at $0 \in \mathcal B_k$ returns a feasible point with $q_k(k_k) \le q_k(0) = 0$.

*Proof.* (a) The objective is strictly convex and the box is compact, convex and not empty, so a minimizer exists and is unique. The listed conditions say that $\gamma^{\mathsf T}(y - \delta) \ge 0$ for every $y$ in the box, coordinate by coordinate; for a convex differentiable function on a convex set this variational inequality holds exactly at the minimizers. (b) Every point of the solver is a projection onto the box, so it is feasible. A step is taken only if the value does not go up (the acceptance test of the solver has a right side at most the current value). The start is $0$, which lies in $\mathcal B_k$ because $u_k$ lies in the box (Lemma 3). $\square$

When the solver meets its stopping test, the conditions of (a) hold up to the tolerance, so $k_k$ is the minimizer up to that tolerance. The test of the page compares it with all active sets.

## Lemma 2: the feedback gain is the derivative of the clamped solution

**Claim.** Let $\delta^*(y)$ minimize $\frac12 \delta^{\mathsf T} H \delta + (Q_u + Q_{ux} y)^{\mathsf T}\delta$ over $\mathcal B_k$, where $y$ is a state deviation. Suppose that at $y = 0$ each bound that is active has $\gamma_i \ne 0$ (strict complementarity), and let $F$ be the set of free indices. Then for all small $y$, $\delta^*(y) = k_k + K_k y$ with $K_k$ as in line L7: the rows in $F$ are $-H_{FF}^{-1} (Q_{ux})_F$ and the other rows are zero.

*Proof.* At $y = 0$ the clamped coordinates have $\gamma_i \ne 0$ with the sign of (a), and the free coordinates are strictly inside their bounds or have $\gamma_i = 0$; by strict complementarity they are strictly inside. Put $\delta(y)$ with the clamped coordinates fixed at their bounds and the free ones given by $H_{FF}\delta_F = -(Q_u + Q_{ux} y)_F - H_{FC}\delta_C$. At $y = 0$ this is $k_k$, and $\delta_F(y) = (k_k)_F - H_{FF}^{-1}(Q_{ux})_F\, y$. By continuity, for small $y$ the free coordinates stay strictly inside their bounds and the clamped gradients keep their strict signs, so $\delta(y)$ meets the conditions of Lemma 1(a) and equals $\delta^*(y)$. $\square$

So the feedback of line L11 follows the solution of the box problem to first order, and a clamped control does not react to state deviations. Without strict complementarity the active set can change for arbitrarily small $y$, and $K_k$ is one of the one-sided derivatives.

## Lemma 3: the controls stay in the box

**Claim.** Every control sequence that the algorithm holds or returns lies in the box.

*Proof.* The input is clamped before line L1, and line L11 clamps every control of a forward pass. Only such sequences are accepted in line L12. $\square$

## Theorem 1: every accepted iteration lowers the cost

**Claim.** If line L9 does not stop, then $\Delta V(\alpha) < 0$ for every $\alpha \in (0, 1]$, and an iteration accepted in line L12 has $J(\hat U) < J(U)$. So the costs of the accepted iterates strictly decrease.

*Proof.* By Lemma 1(b), $q_k(k_k) \le 0$ for every $k$. The function $q_k$ is convex with $q_k(0) = 0$, so $q_k(\alpha k_k) \le (1 - \alpha) q_k(0) + \alpha q_k(k_k) = \alpha q_k(k_k)$. Summing, $\Delta V(\alpha) \le \alpha \Delta V(1)$. Line L9 continues only if $-\Delta V(1) \ge tol > 0$, so $\Delta V(\alpha) \le -\alpha\, tol < 0$. Line L12 accepts only if $J(\hat U) - J(U) \le c\,\Delta V(\alpha)$ with $c > 0$, which is negative. $\square$

## Theorem 2: one iteration is exact for an unconstrained linear-quadratic problem

**Claim.** Let $f(x, u) = Ax + Bu$ (or $A_k, B_k$ that depend on $k$ only), let $\mu = 0$, and suppose that the box is so large that no bound is active in line L6 and no clamp acts in line L11 (for example, no bounds at all). Then the backward pass is the Riccati recursion of the [finite-horizon LQR problem](/finite-horizon-lqr/), $\Delta V(1)$ equals the true change of the cost, and the forward pass with $\alpha = 1$ returns the optimal control sequence.

*Proof.* Let $V_k(x)$ be the optimal cost-to-go from state $x$ at stage $k$. We show by induction, from $k = N$ down, that $V_k(x_k + y) = V_k(x_k) + V_{x}^{\mathsf T} y + \frac12 y^{\mathsf T} V_{xx} y$ with the $V_x, V_{xx}$ that the backward pass holds after stage $k$, that $V_{xx}$ is positive semidefinite, and that the optimal control at $x_k + y$ is $u_k + k_k + K_k y$. At $k = N$ this is the Taylor expansion of the quadratic $\ell_f$ (line L3). For the step, the dynamics are linear, so

$$\ell(x_k + y, u_k + \delta) + V_{k+1}\bigl(x_{k+1} + A y + B\delta\bigr)$$

is exactly the quadratic with the coefficients $Q_x, Q_u, Q_{xx}, Q_{uu}, Q_{ux}$ of line L5 plus a constant. $Q_{uu} = R + B^{\mathsf T} V_{xx} B$ is positive definite. Its minimizer over $\delta$ is $-Q_{uu}^{-1}(Q_u + Q_{ux} y)$; no bound is active by assumption, so the box solver returns it at $y = 0$ (Lemma 1(a)), and line L7 gives $K_k = -Q_{uu}^{-1} Q_{ux}$. Substituting $\delta = k_k + K_k y$ gives a quadratic in $y$ whose linear and quadratic coefficients are exactly the two formulas of line L8, and whose constant is the old constant plus $q_k(k_k)$. As a minimum over $\delta$ of a quadratic that is jointly convex in $(y, \delta)$, it is convex, so $V_{xx}$ is positive semidefinite. This is the Riccati recursion.

At $y = 0$ the constant of stage $k$ is $\ell(x_k, u_k) + V_{k+1}(x_{k+1}) + q_k(k_k)$, so $V_0(x_0) = J(U) + \sum_k q_k(k_k) = J(U) + \Delta V(1)$. The forward pass with $\alpha = 1$ applies the optimal policy $u_k + k_k + K_k y$ from $x_0$, and no clamp acts by assumption. Its cost is $V_0(x_0)$, so the actual change equals $\Delta V(1) \le c\,\Delta V(1)$ for $c \le 1$, and line L12 accepts. $\square$

With active bounds the cost-to-go is only piecewise quadratic, and one iteration is no longer enough; the test of the page checks the result of several iterations against an independent solver of the same convex problem.

## Theorem 3: a stop in line L9 happens only near a first-order point

**Claim.** Suppose that, with $\mu = 0$ or any $\mu$, the backward pass returns $k_k = 0$ at every stage and that $0$ is the exact minimizer of every stage model. Then $U$ satisfies the first-order conditions of $\min J(U)$ over the box: for each $k$ and $i$, $\partial J/\partial u_{k,i} = 0$ where $u_{k,i}$ is strictly inside its bounds, $\ge 0$ at its lower bound and $\le 0$ at its upper bound. If $J$ is convex, for example for linear dynamics, $U$ is a global minimizer.

*Proof.* With $k_k = 0$ the formula of line L8 becomes $V_x = Q_x + K_k^{\mathsf T} Q_u$. By Lemma 1(a) applied at $\delta = 0$, $\gamma = Q_u$, and a free index has $Q_{u,i} = 0$: if it is strictly inside, by (a); if it sits at a bound, it is free only when the gradient does not push outward, and (a) then forces $Q_{u,i} = 0$. The rows of $K_k$ for clamped indices are zero. So $K_k^{\mathsf T} Q_u = 0$ and $V_{x,k} = \nabla_x \ell(x_k, u_k) + A_k^{\mathsf T} V_{x,k+1}$ with $V_{x,N} = \nabla \ell_f(x_N)$. This is the adjoint recursion, so $V_{x,k+1}$ is the derivative of the cost from stage $k + 1$ on with respect to $x_{k+1}$, and by the chain rule

$$\frac{\partial J}{\partial u_k} = \nabla_u \ell(x_k, u_k) + B_k^{\mathsf T} V_{x,k+1} = Q_{u,k}.$$

The regularization $\mu$ does not enter $Q_u$. So the conditions of Lemma 1(a) at $\delta = 0$ are the stated conditions for $\partial J/\partial u_k$. For convex $J$ on a convex set they imply a global minimum. Only first derivatives of $f$ enter, so dropping the second derivatives of the dynamics does not change this result. $\blacksquare$

The code stops when $-\Delta V(1) < tol$, which is a small version of $k_k = 0$: by Lemma 1(a) and strict convexity, $-q_k(k_k) \ge \frac12 \lambda_{\min}(H_k)\|k_k\|^2$, so every $k_k$ is small. The test of the page measures the first-order conditions of the returned controls directly.
