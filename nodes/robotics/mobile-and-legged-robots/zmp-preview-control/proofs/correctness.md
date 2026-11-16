---
title: The preview law is the optimal control of the incremental cart-table problem
proves: [correctness]
status: full
---

This proof is about the cart-table model only. It shows that the law of ZMP-PREVIEW-CONTROL is the exact minimizer of its quadratic cost and that the closed loop of the model is stable. It says nothing about the stability of a real multibody robot.

**Setting.** The sampling period is $T > 0$ and $h = z_c / g > 0$. The cart-table model is $x_{k+1} = A x_k + B u_k$, $p_k = C x_k$, with

$$A = \begin{bmatrix} 1 & T & T^2/2 \\ 0 & 1 & T \\ 0 & 0 & 1 \end{bmatrix}, \quad B = \begin{bmatrix} T^3/6 \\ T^2/2 \\ T \end{bmatrix}, \quad C = \begin{bmatrix} 1 & 0 & -h \end{bmatrix}.$$

Write $e_k = p_k - r_k$, $\Delta x_k = x_k - x_{k-1}$, $\Delta u_k = u_k - u_{k-1}$, $d_k = r_k - r_{k-1}$ and $X_k = (e_k, \Delta x_k) \in \mathbb{R}^4$. Then $\Delta x_{k+1} = A \Delta x_k + B \Delta u_k$ and $e_{k+1} = e_k + C A \Delta x_k + C B \Delta u_k - d_{k+1}$, so

$$X_{k+1} = \tilde A X_k + \tilde B \Delta u_k + F d_{k+1}, \quad \tilde A = \begin{bmatrix} 1 & CA \\ 0 & A \end{bmatrix}, \quad \tilde B = \begin{bmatrix} CB \\ B \end{bmatrix}, \quad F = -e_1.$$

The weights are $Q = \operatorname{diag}(Q_e, Q_x)$ with $Q_e > 0$ and $Q_x \succeq 0$, and $R > 0$.

**Lemma 1 (controllability and observability).** The pair $(\tilde A, \tilde B)$ is controllable, and the pair $(\tilde A, e_1^T)$ is observable.

*Proof.* The matrix $\tilde A$ is upper triangular with all diagonal entries 1, so its only eigenvalue is 1. By the Popov-Belevitch-Hautus test it is enough to check the rank at $\lambda = 1$. The first column of $\tilde A - I$ is zero, so the rank of $[\tilde A - I, \tilde B]$ is the rank of the $4 \times 4$ matrix with rows $(CA, CB)$ and $(A - I, B)$:

$$\begin{bmatrix} 1 & T & T^2/2 - h & T^3/6 - hT \\ 0 & T & T^2/2 & T^3/6 \\ 0 & 0 & T & T^2/2 \\ 0 & 0 & 0 & T \end{bmatrix}.$$

It is upper triangular with determinant $T^3 \ne 0$, so the rank is 4. For observability, stack $\tilde A - I$ on $e_1^T$. The row $e_1^T$ gives the first column, and the last three columns contain the rows $CA = (1, T, T^2/2 - h)$, $(0, T, T^2/2)$ and $(0, 0, T)$, which are independent. So the rank is 4. $\square$

Because $Q \succeq e_1 Q_e e_1^T$ with $Q_e > 0$, Lemma 1 gives that $(\tilde A, \tilde B)$ is stabilizable and $(\tilde A, Q^{1/2})$ is detectable. The standard theory of the [discrete algebraic Riccati equation](/discrete-algebraic-riccati-equation/) then gives a unique symmetric $P \succeq 0$ with

$$P = Q + \tilde A^T P \tilde A - \tilde A^T P \tilde B (R + \tilde B^T P \tilde B)^{-1} \tilde B^T P \tilde A,$$

such that $A_c = \tilde A - \tilde B K$ is Schur stable, where $s = R + \tilde B^T P \tilde B > 0$ and $K = s^{-1} \tilde B^T P \tilde A$. The value iteration from $P_0 = Q$ converges to this $P$. This is what line L3 computes, and lines L4 and L5 compute $K$ and $A_c$.

**Theorem (optimality).** Fix a step $k$ and a preview length $N \ge 1$, and assume $d_j = 0$ for every $j > k + N$. For every horizon $H \ge N$, the problem

$$\min_{\Delta u_k, \dots, \Delta u_{k+H-1}} \sum_{i=k}^{k+H-1} \left( X_i^T Q X_i + R \Delta u_i^2 \right) + X_{k+H}^T P X_{k+H}$$

has a unique minimizer, and its first input is

$$\Delta u_k = -K X_k + \sum_{j=1}^{N} f_j d_{k+j}, \qquad f_j = s^{-1} \tilde B^T (A_c^T)^{j-1} P e_1.$$

*Proof.* We use dynamic programming backward from $i = k + H$. We claim that the optimal cost to go from step $i$ is $V_i(X) = X^T P X + 2 X^T w_i + c_i$, where $w_{k+H} = 0$, $c_i$ does not depend on $X$, and

$$w_i = A_c^T (P F d_{i+1} + w_{i+1}).$$

The claim holds at $i = k + H$ by the terminal cost. Assume it holds at $i + 1$. Put $y = \tilde A X + \tilde B v + F d_{i+1}$ into $V_{i+1}$. Up to terms that do not depend on $X$ or $v$, the cost of the input $v$ at step $i$ is

$$X^T Q X + R v^2 + (\tilde A X + \tilde B v)^T P (\tilde A X + \tilde B v) + 2 (\tilde A X + \tilde B v)^T g, \quad g = P F d_{i+1} + w_{i+1}.$$

This is a quadratic in the scalar $v$ with leading coefficient $s > 0$, so the minimizer is unique. Setting the derivative to zero gives $s v = -\tilde B^T P \tilde A X - \tilde B^T g$, so $v^* = -K X - s^{-1} \tilde B^T g$. Put $v^*$ back. The terms quadratic in $X$ are $X^T (Q + \tilde A^T P \tilde A - \tilde A^T P \tilde B s^{-1} \tilde B^T P \tilde A) X = X^T P X$ by the Riccati equation. For the terms linear in $X$, differentiate the minimum with respect to $X$; because $v^*$ is a stationary point, only the explicit dependence counts, and the part of the gradient that is linear in $g$ is $2 \tilde A^T g + 2 \tilde A^T P \tilde B (-s^{-1} \tilde B^T g) = 2 (\tilde A - \tilde B K)^T g = 2 A_c^T g$, where we used $\tilde A^T P \tilde B s^{-1} = K^T$. So the linear term is $2 X^T A_c^T g$, which is the claim at step $i$.

Now unroll the recursion from step $k$. Because $d_j = 0$ for $j > k + N$ and $H \ge N$, the vector $g$ at step $k$ is

$$g_k = P F d_{k+1} + w_{k+1} = \sum_{j=1}^{N} (A_c^T)^{j-1} P F d_{k+j}.$$

With $F = -e_1$, the first input is $\Delta u_k = -K X_k - s^{-1} \tilde B^T g_k = -K X_k + \sum_{j=1}^{N} f_j d_{k+j}$. $\blacksquare$

**The code computes these gains.** Line L6 sets $v = P e_1$. In the loop of lines L7 to L9, before pass $j$ the vector is $v = (A_c^T)^{j-1} P e_1$, line L8 appends $s^{-1} \tilde B^T v = f_j$, and line L9 multiplies $v$ by $A_c^T$. Lines L12 to L15 form $X_k$, apply the law of the theorem, and add $\Delta u_k$ to $u_{k-1}$. Line L16 is the exact discrete model.

**Remarks.**

1. The terminal cost $X^T P X$ is the optimal cost of the problem without reference changes, because $P$ is the stabilizing solution. So the theorem also gives the first input of the infinite-horizon problem when the reference is constant after the preview window. If the reference changes after step $k + N$, the law ignores those changes and is optimal only for the truncated reference.
2. If the reference is constant from some step on, then $d = 0$ from there and $X_{k+1} = A_c X_k$. Because $A_c$ is Schur stable, $X_k \to 0$, so the ZMP error $e_k$ and the increments $\Delta x_k$ go to zero. The integrator in $e$ removes a constant offset of the ZMP.
3. Lemma 1 holds for every $T > 0$ and $h > 0$, but the gains that the iteration gives depend on $T$, $h$, $Q$ and $R$, and the numbers in the page are computed, not derived.
