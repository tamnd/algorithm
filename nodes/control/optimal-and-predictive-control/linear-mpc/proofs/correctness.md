---
title: The condensed QP is the MPC problem, the dual active set method solves it or proves it infeasible, and the receding horizon loop decreases the value
proves: [correctness]
status: full
---

The plant is $x_{k+1} = A x_k + B u_k$ with $x \in \mathbb{R}^n$ and $u \in \mathbb{R}^m$. The weights are $Q = Q^T \ge 0$, $R = R^T > 0$ and $P = P^T \ge 0$. The horizon cost of the input sequence $U = (u_0, \dots, u_{N-1})$ from $x_0$ is

$$J(x_0, U) = \sum_{k=0}^{N-1} (x_k^T Q x_k + u_k^T R u_k) + x_N^T P x_N.$$

The proof has three parts. Part 1 shows that the QP built in lines L1 to L4 is the MPC problem. Part 2 shows that the QP solver of lines L8 to L20 returns the unique minimizer or correctly reports that no feasible point exists. Part 3 shows what the receding horizon loop of lines L5 to L7 gives when the terminal ingredients are chosen as on the page. Parts 1 and 2 are in exact arithmetic; the code adds a tolerance to each sign test.

## Part 1: the condensed form

**Lemma 1.** Let $X = (x_1, \dots, x_N)$. Then $X = \Phi x_0 + \Gamma U$, where block row $k$ of $\Phi$ is $A^k$ and block $(k, j)$ of $\Gamma$ is $A^{k-1-j} B$ for $j < k$ and 0 otherwise.

*Proof.* Induction on $k$: $x_1 = A x_0 + B u_0$, and if $x_k = A^k x_0 + \sum_{j<k} A^{k-1-j} B u_j$ then $x_{k+1} = A x_k + B u_k = A^{k+1} x_0 + \sum_{j<k+1} A^{k-j} B u_j$. $\square$

**Lemma 2.** With $\bar Q = \mathrm{diag}(Q, \dots, Q, P)$, $\bar R = \mathrm{diag}(R, \dots, R)$, $H = \Gamma^T \bar Q \Gamma + \bar R$ and $F = \Gamma^T \bar Q \Phi$,

$$J(x_0, U) = U^T H U + 2 (F x_0)^T U + x_0^T (Q + \Phi^T \bar Q \Phi) x_0,$$

and $H$ is positive definite.

*Proof.* $J = x_0^T Q x_0 + X^T \bar Q X + U^T \bar R U$. Substitute Lemma 1 and expand $(\Phi x_0 + \Gamma U)^T \bar Q (\Phi x_0 + \Gamma U)$. For $H$: $U^T H U = (\Gamma U)^T \bar Q (\Gamma U) + U^T \bar R U \ge U^T \bar R U > 0$ for $U \ne 0$, since $\bar Q \ge 0$ and $\bar R > 0$. $\square$

The last term does not depend on $U$. So minimizing $J(x_0, \cdot)$ is the same as minimizing $\frac12 U^T H U + (F x_0)^T U$, which is the objective of line L5 with $f = F x_0$ from line L4.

**Lemma 3.** The rows built in line L3 describe the constraints: $U$ satisfies $u_{\min} \le u_k \le u_{\max}$ for $k < N$, $x_{\min} \le x_k \le x_{\max}$ for $1 \le k \le N$ and $H_f x_N \le h_f$ if and only if $G U \le w + E x_0$.

*Proof.* The input rows are the coordinate rows of $U$ with $E = 0$. For the state rows, row $r$ of $X$ is $\Phi_r x_0 + \Gamma_r U$ by Lemma 1, so $X_r \le x_{\max, i}$ is $\Gamma_r U \le x_{\max, i} - \Phi_r x_0$, which is the row stored; the lower bound is the same with the signs changed. The terminal rows use the last block row of $\Phi$ and $\Gamma$ in the same way. $\square$

## Part 2: the dual active set method

Write the QP as: minimize $\phi(z) = \frac12 z^T H z + f^T z$ subject to $g_i^T z \le b_i$ for $i = 1, \dots, q$, with $H > 0$. The KKT conditions are

$$H z + f + \textstyle\sum_i \lambda_i g_i = 0, \quad g_i^T z \le b_i, \quad \lambda_i \ge 0, \quad \lambda_i (b_i - g_i^T z) = 0.$$

Because $\phi$ is strictly convex and the constraints are affine, a point satisfies them if and only if it is the unique minimizer.

For a set $W$ of constraint indices with linearly independent rows, let $N_W$ be the matrix with the columns $g_j$, $j \in W$. Call $(z, W)$ a *solution pair* if $g_j^T z = b_j$ for $j \in W$ and $H z + f + N_W \lambda_W = 0$ with $\lambda_W \ge 0$. Then $z$ is the minimizer of $\phi$ on the affine set $\{z : g_j^T z = b_j, j \in W\}$, so $\phi(z)$ depends on $W$ only. Line L8 starts with the solution pair $(-H^{-1} f, \emptyset)$.

**Invariant of the inner loop.** At line L13 the current values satisfy

$$H z + f + N_W \lambda_W + \lambda_p g_p = 0, \quad g_j^T z = b_j \ (j \in W), \quad \lambda_W \ge 0, \quad \lambda_p \ge 0, \quad g_p^T z > b_p,$$

and the columns of $N_W$ are linearly independent. At the first entry $\lambda_p = 0$ (line L12) and this is the solution pair condition plus the choice of a violated $p$ (lines L10 and L11).

**Lemma 4 (the step).** Line L14 computes $r = (N_W^T H^{-1} N_W)^{-1} N_W^T H^{-1} g_p$ and $d = H^{-1}(g_p - N_W r)$. Then $N_W^T d = 0$, $H d + N_W r = g_p$ and $g_p^T d = (g_p - N_W r)^T H^{-1} (g_p - N_W r) \ge 0$, with equality if and only if $g_p$ is a combination of the columns of $N_W$, and then $d = 0$. For every $t \ge 0$, the update $z \leftarrow z - t d$, $\lambda_W \leftarrow \lambda_W - t r$, $\lambda_p \leftarrow \lambda_p + t$ keeps the stationarity equation and the equalities on $W$, and changes the objective by

$$\phi(z - t d) - \phi(z) = t \, g_p^T d \, (\lambda_p + t/2).$$

*Proof.* The matrix $N_W^T H^{-1} N_W$ is positive definite because the columns are independent, so $r$ exists. $N_W^T d = N_W^T H^{-1} g_p - (N_W^T H^{-1} N_W) r = 0$. The identity $H d + N_W r = g_p$ is the definition of $d$. Since $N_W^T d = 0$, $g_p^T d = (g_p - N_W r)^T d$, which is the stated quadratic form; it is 0 only if $g_p = N_W r$, and then $d = H^{-1} 0 = 0$. The stationarity residual changes by $-t (H d + N_W r - g_p) = 0$, and $g_j^T (z - t d) = g_j^T z$ for $j \in W$. For the objective, $\nabla \phi(z) = H z + f = -N_W \lambda_W - \lambda_p g_p$, so

$$\phi(z - t d) - \phi(z) = -t d^T \nabla \phi(z) + \tfrac12 t^2 d^T H d = t \lambda_p g_p^T d + \tfrac12 t^2 g_p^T d,$$

using $d^T N_W = 0$ and $d^T H d = d^T (g_p - N_W r) = g_p^T d$. $\square$

The step length (lines L15 to L18) is $t = \min(t_1, t_2)$, where $t_1 = \min\{\lambda_k / r_k : r_k > 0\}$ is the largest step that keeps $\lambda_W \ge 0$, and $t_2 = (g_p^T z - b_p) / g_p^T d$ is the step that makes constraint $p$ active ($t_2 = \infty$ if $g_p^T d = 0$). The value $g_p^T z - b_p$ decreases by $t \, g_p^T d$, so for $t \le t_2$ constraint $p$ stays violated or becomes active, and the invariant holds after the update, except for the last condition when $t = t_2$.

**Lemma 5 (infeasibility).** If $t_1 = t_2 = \infty$ (line L17), the QP has no feasible point.

*Proof.* $t_2 = \infty$ means $g_p^T d = 0$, so $g_p = N_W r$ by Lemma 4. $t_1 = \infty$ means $r_k \le 0$ for all $k$. Let $\hat z$ be any point with $g_j^T \hat z \le b_j$ for $j \in W$. Then

$$g_p^T \hat z = \textstyle\sum_{k} r_k g_k^T \hat z \ge \sum_k r_k b_k = \sum_k r_k g_k^T z = g_p^T z > b_p,$$

where the inequality uses $r_k \le 0$, the middle equality uses $g_k^T z = b_k$ on $W$, and the last step is the invariant. So no point satisfies the constraints in $W \cup \{p\}$. $\square$

**Lemma 6 (the two kinds of step).** If $t = t_2$ (a full step, line L19), then $p$ joins $W$, the columns stay independent, and $(z, W \cup \{p\})$ is a solution pair with a strictly larger objective than the solution pair at the start of the outer iteration. If $t = t_1 < t_2$ (a partial step, line L20), the index $k_1$ with $\lambda_{k_1} = 0$ leaves $W$, the invariant still holds, and $|W|$ decreases.

*Proof.* Full step: $t_2 < \infty$ gives $g_p^T d > 0$, so $g_p$ is not in the span of $N_W$, and the new columns are independent. After the step $g_p^T z = b_p$, $\lambda_p = $ old $\lambda_p + t \ge 0$ and $\lambda_W \ge 0$ by $t \le t_1$; stationarity holds by Lemma 4, so this is a solution pair. Along the inner loop the objective never decreases by Lemma 4, since $t \ge 0$, $g_p^T d \ge 0$ and $\lambda_p \ge 0$. In the full step $t = t_2 > 0$ because constraint $p$ is violated before it, and $g_p^T d > 0$, so this step increases $\phi$ strictly. Partial step: $\lambda_{k_1} - t_1 r_{k_1} = 0$, so removing $k_1$ from $W$ does not change $N_W \lambda_W$, and the stationarity equation, the equalities on the remaining set and the signs still hold. A subset of independent columns is independent. $\square$

**Theorem.** In exact arithmetic the method stops after finitely many steps. It either reports infeasibility, and then the QP has no feasible point, or returns $(z, \lambda)$ satisfying the KKT conditions, so $z$ is the unique minimizer.

*Proof.* Each inner loop ends with a full step or with the infeasible report after at most $|W| \le$ (number of variables) partial steps, by Lemma 6. Each full step gives a solution pair whose objective is strictly larger than the previous one. The objective of a solution pair depends only on its set $W$, so no set repeats, and there are finitely many sets. So the outer loop runs finitely often. The infeasible report is correct by Lemma 5. When the outer loop stops at line L11, no constraint is violated, so $z$ is feasible; the solution pair gives stationarity and $\lambda \ge 0$ with $\lambda_i = 0$ off $W$ and $g_i^T z = b_i$ on $W$, which is complementarity. $\square$

## Part 3: the receding horizon loop

Line L7 returns the first $m$ entries of the minimizer $U^*(x)$, so the controller is $\kappa_N(x) = u_0^*(x)$ and the value is $V_N(x) = J(x, U^*(x))$. Let $K$ and $P$ come from the DARE $P = A^T P A - A^T P B (R + B^T P B)^{-1} B^T P A + Q$ with $K = (R + B^T P B)^{-1} B^T P A$ and $A_K = A - B K$ Schur. Let $X_f = \{x : H_f x \le h_f\}$ be a set with $A_K X_f \subseteq X_f$, and such that every $x \in X_f$ satisfies the state box and $-K x$ satisfies the input box (the maximal positively invariant set of $A_K$ under these constraints is such a set).

**Lemma 7.** If the QP is feasible at $x$, then it is feasible at $x^+ = A x + B \kappa_N(x)$ and

$$V_N(x^+) \le V_N(x) - (x^T Q x + \kappa_N(x)^T R \kappa_N(x)).$$

*Proof.* Let $U^* = (u_0^*, \dots, u_{N-1}^*)$ with states $x_0 = x, x_1, \dots, x_N \in X_f$. From $x^+ = x_1$ take the shifted sequence $\tilde U = (u_1^*, \dots, u_{N-1}^*, -K x_N)$. Its states are $x_2, \dots, x_N, A_K x_N$. The inputs $u_1^*, \dots, u_{N-1}^*$ and the states $x_2, \dots, x_N$ satisfy the constraints because they did for $U^*$. The input $-K x_N$ and the state $x_N$ satisfy the boxes because $x_N \in X_f$, and $A_K x_N \in X_f$ by invariance, so it also satisfies the state box and the terminal rows. So $\tilde U$ is feasible and

$$J(x^+, \tilde U) = V_N(x) - (x^T Q x + u_0^{*T} R u_0^*) + \big[x_N^T Q x_N + x_N^T K^T R K x_N + x_N^T A_K^T P A_K x_N - x_N^T P x_N\big].$$

The DARE can be written $P = Q + K^T R K + A_K^T P A_K$, so the bracket is 0. Then $V_N(x^+) \le J(x^+, \tilde U)$ gives the claim. $\square$

So the set of states where the QP is feasible is positively invariant for the closed loop (recursive feasibility), and $V_N$ decreases at each sampling instant by at least the stage cost. If $Q > 0$, summing the decrease gives $\sum_k x_k^T Q x_k \le V_N(x_0) < \infty$, so $x_k \to 0$. The full stability statement, with the bounds on $V_N$ needed for asymptotic stability, is on the [MPC stability theorem](/mpc-stability-theorem/) page.
