---
title: Each sample of the code performs one exact Gauss-Newton SQP step of the multiple shooting problem, and its fixed points are KKT points
proves: [correctness]
status: full
---

**Setting.** The discrete model is $x^+ = F(x, u)$, one Runge-Kutta 4 step of length $h$ for $\dot x = f(x, u)$ with $f$ twice continuously differentiable. The optimal control problem for the measured state $x_0$ is

$$\min_{s, q} \ \sum_{k=0}^{N-1} \left(s_k^T Q s_k + q_k^T R q_k\right) + s_N^T P s_N \quad \text{s.t.} \quad s_0 = x_0, \ s_{k+1} = F(s_k, q_k), \ -\bar u \le q_k \le \bar u, \tag{NLP}$$

with $Q$, $P$ symmetric positive semidefinite and $R$ symmetric positive definite. The cost is quadratic in $(s, q)$, so its Hessian is constant. The **Gauss-Newton SQP step** at a guess $(s, q)$ keeps this cost and replaces each constraint by its linearization, which drops the curvature of the constraints from the Hessian of the Lagrangian:

$$\Delta s_0 = x_0 - s_0, \quad \Delta s_{k+1} = A_k \Delta s_k + B_k \Delta q_k + c_k, \quad -\bar u \le q_k + \Delta q_k \le \bar u, \tag{QP}$$

with $A_k = \partial F / \partial x$, $B_k = \partial F / \partial u$ at $(s_k, q_k)$ and the gaps $c_k = F(s_k, q_k) - s_{k+1}$. The new guess is $(s + \Delta s, q + \Delta q)$.

## Part 1: the derivatives of the RK4 step

**Lemma 1.** `rk4` returns $F(x, u)$ and its exact Jacobians $A = \partial F / \partial x$ and $B = \partial F / \partial u$.

*Proof.* The RK4 step is $k_1 = f(x, u)$, $k_2 = f(x + \frac h2 k_1, u)$, $k_3 = f(x + \frac h2 k_2, u)$, $k_4 = f(x + h k_3, u)$, $F = x + \frac h6 (k_1 + 2 k_2 + 2 k_3 + k_4)$. Let $\xi_i$ be the point at which $k_i$ is evaluated. By the chain rule,

$$\frac{\partial k_i}{\partial x} = f_x(\xi_i, u) \frac{\partial \xi_i}{\partial x}, \qquad \frac{\partial k_i}{\partial u} = f_x(\xi_i, u) \frac{\partial \xi_i}{\partial u} + f_u(\xi_i, u),$$

with $\partial \xi_1 / \partial x = I$, $\partial \xi_1 / \partial u = 0$, $\partial \xi_{i+1} / \partial x = I + c_i h\, \partial k_i / \partial x$ and $\partial \xi_{i+1} / \partial u = c_i h\, \partial k_i / \partial u$ for $c = (\frac12, \frac12, 1)$. The loop in `rk4` computes exactly these matrices in this order (`dxs`, `dus`, `kx`, `ku`), and then $A = I + \frac h6 \sum_i w_i\, \partial k_i / \partial x$ and $B = \frac h6 \sum_i w_i\, \partial k_i / \partial u$ with $w = (1, 2, 2, 1)$. $\square$

## Part 2: condensing

**Lemma 2.** For every $\Delta s_0$ and $\Delta q$, the solution of the recursion in (QP) is $\Delta s_k = M_k \Delta s_0 + \Gamma_k \Delta q + d_k$, where $M_0 = I$, $\Gamma_0 = 0$, $d_0 = 0$, $M_{k+1} = A_k M_k$, $d_{k+1} = A_k d_k + c_k$, and $\Gamma_{k+1}$ equals $A_k \Gamma_k$ except that its block column $k$ is $B_k$.

*Proof.* By induction. At $k = 0$ it holds. If it holds at $k$, then $A_k \Delta s_k + B_k \Delta q_k + c_k = A_k M_k \Delta s_0 + (A_k \Gamma_k) \Delta q + B_k \Delta q_k + A_k d_k + c_k$. Block column $k$ of $\Gamma_k$ is 0 (inputs at step $k$ or later do not affect $\Delta s_k$), so adding $B_k \Delta q_k$ sets that block column to $B_k$. $\square$

**Lemma 3.** With $W_k = Q$ for $k < N$, $W_N = P$, and $y_k = s_k + d_k + M_k \Delta s_0$, the cost of (QP) as a function of $\Delta q$ is

$$\tfrac12 \Delta q^T H \Delta q + (g + G \Delta s_0)^T \Delta q + \text{const},$$

with $H = 2 \sum_k \Gamma_k^T W_k \Gamma_k + 2\, \mathrm{blockdiag}(R)$, $g = 2 \sum_k \Gamma_k^T W_k (s_k + d_k) + 2 (R q_0, \dots, R q_{N-1})$ and $G = 2 \sum_k \Gamma_k^T W_k M_k$. These are the quantities that `prepare` returns, and they do not depend on $x_0$.

*Proof.* By Lemma 2, $s_k + \Delta s_k = y_k + \Gamma_k \Delta q$. Expanding $(y_k + \Gamma_k \Delta q)^T W_k (y_k + \Gamma_k \Delta q)$ gives $y_k^T W_k y_k + 2 y_k^T W_k \Gamma_k \Delta q + \Delta q^T \Gamma_k^T W_k \Gamma_k \Delta q$, using $W_k = W_k^T$. Expanding $(q_k + \Delta q_k)^T R (q_k + \Delta q_k)$ gives $q_k^T R q_k + 2 q_k^T R \Delta q_k + \Delta q_k^T R \Delta q_k$. Summing and collecting the terms that are linear in $\Delta q$ gives $2 \sum_k \Gamma_k^T W_k (s_k + d_k + M_k \Delta s_0) + 2 R q = g + G \Delta s_0$. $\square$

$H$ is positive definite, since $R$ is, so the condensed QP has a unique solution. Its feasible set is the box $-\bar u - q \le \Delta q \le \bar u - q$, which is what `feedback` passes to `box_qp`, and its gradient uses the measured state only through $G \Delta s_0$.

## Part 3: the box QP

**Lemma 4.** If `box_qp` returns $x$, then $x$ is the unique minimizer of $\frac12 x^T H x + g^T x$ over $lo \le x \le hi$.

*Proof.* The iterate is feasible at all times: it starts at the projection of 0 onto the box, a step moves only the free variables and is cut at the first bound that it would cross (that variable is then fixed at its bound), and removing a variable from the working set does not move it. The method returns only when the step on the free set is zero, so the free variables minimize the objective with the fixed variables held, which means $\nabla_i = (H x + g)_i = 0$ for every free $i$. It also checks that $\nabla_i \ge 0$ for every variable at its lower bound and $\nabla_i \le 0$ for every variable at its upper bound. These are the KKT conditions of the box QP, with multipliers $\max(\pm \nabla_i, 0)$. The problem is convex, so KKT points are minimizers, and the minimizer is unique because $H$ is positive definite. $\square$

The method is the primal active set method for a strictly convex QP, which ends after finitely many steps when no step has length zero for ever; the code stops with an error after `max_iter` iterations in any case.

## Part 4: one sample

**Theorem 1.** `prepare` followed by `feedback` returns the exact Gauss-Newton SQP step of (NLP) at $(s, q)$ for the measured $x_0$: the new controls $q + \Delta q$ with $\Delta q$ the solution of (QP), the new nodes $s + \Delta s$ from the recursion of (QP), and the first control $q_0 + \Delta q_0$.

*Proof.* Lemma 1 gives $A_k$, $B_k$ and $c_k$ (line L2). Lemma 2 and Lemma 3 show that (QP), after the substitution of $\Delta s$, is the condensed QP with data $H$, $g + G \Delta s_0$ and the box (lines L3 to L5). Lemma 4 shows that `box_qp` solves it. Line L6 returns $q_0 + \Delta q_0$. Line L7 runs the recursion of (QP) from $\Delta s_0 = x_0 - s_0$, so the new $s_0$ is $x_0$, and the new nodes are $s_k + \Delta s_k$. $\square$

**Theorem 2.** If $(s, q)$ is a fixed point of the step for $x_0$, that is $\Delta s = 0$ and $\Delta q = 0$, then $q$ is a KKT point of the reduced problem $\min_q J(q)$ subject to $-\bar u \le q \le \bar u$, where $J(q)$ is the cost of the trajectory simulated from $x_0$, and $s$ is that trajectory.

*Proof.* $\Delta s_0 = 0$ gives $s_0 = x_0$. With $\Delta q = 0$ and $\Delta s = 0$, the recursion gives $c_k = 0$ for all $k$, so $s_{k+1} = F(s_k, q_k)$ and $s$ is the trajectory of $q$ from $x_0$. The map from $q$ to the simulated trajectory is differentiable, and by the chain rule its derivative at $q$ is $\Gamma$ of Lemma 2 (with $c = 0$ and $\Delta s_0 = 0$, $\Delta s = \Gamma \Delta q$ is the linearized trajectory). So the gradient of $J$ at $q$ is the derivative at $\Delta q = 0$ of the cost of Lemma 3, which is $g$. Since $\Delta q = 0$ solves the box QP, it meets its KKT conditions at 0 with gradient $H \cdot 0 + g = g$; these are exactly the KKT conditions of $\min J(q)$ over the box at $q$. $\square$

So iterating the step at a fixed $x_0$ (`solve_nmpc`) converges, when it converges, to a KKT point of (NLP). The RTI does not iterate: line L8 shifts the result and uses it as the guess for the next sample. How close the RTI inputs stay to the exact NMPC inputs is a question of contraction of the Gauss-Newton step together with the motion of the plant; Diehl, Bock and Schlöder (2005) give conditions under which the closed loop of the RTI is stable. That analysis is not reproduced here.

## Part 5: what the code computes

- **Line L1** is the loop over the samples in `rti_loop`.
- **Line L2** integrates each interval with its sensitivities (Lemma 1) and forms the gaps.
- **Line L3** condenses (Lemmas 2 and 3). Lines L2 and L3 make up the preparation phase and use only $(s, q)$.
- **Lines L4 to L6** are the feedback phase: $\Delta s_0 = x_0 - s_0$, the box QP, and the first control.
- **Line L7** expands the solution to the new nodes.
- **Line L8** shifts the nodes and controls by one interval for the next sample.
