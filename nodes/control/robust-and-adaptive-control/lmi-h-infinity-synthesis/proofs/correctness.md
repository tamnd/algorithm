---
title: The LMI synthesis code builds a valid closed loop Lyapunov matrix and controller
proves: [correctness]
status: full
---

Notation is that of the page. The theorem of Gahinet and Apkarian (1994) is cited: the controller exists if and only if the three LMIs hold, and for any $X_{\rm cl} > 0$ with $(X_{\rm cl})_{11} = S$ and $(X_{\rm cl}^{-1})_{11} = R$ for a solution $(R, S)$ with strict inequalities, the bounded real LMI in $\Omega$ is feasible. We prove the parts that the code adds.

## Claim 1: the reconstructed matrix has the right blocks

*Let $R$ and $S$ be symmetric with $\begin{bmatrix} R & I \\ I & S \end{bmatrix} > 0$. Put $N = I - SR$ and $X_{\rm cl} = \begin{bmatrix} S & N \\ N^T & W \end{bmatrix}$ with $W = RSR - R$. Then $X_{\rm cl} > 0$, $(X_{\rm cl})_{11} = S$ and $(X_{\rm cl}^{-1})_{11} = R$.*

*Proof.* The strict coupling LMI gives $R > 0$ and, by a Schur complement, $S - R^{-1} > 0$. Then $W = R(S - R^{-1})R > 0$. Also $N = (R^{-1} - S)R$ is invertible, and $W = -R N$, so $W^{-1} = -N^{-1} R^{-1}$. Using $N^T = I - RS$:

$$N W^{-1} N^T = -R^{-1} N^T = -R^{-1}(I - RS) = S - R^{-1}.$$

So the Schur complement of $W$ in $X_{\rm cl}$ is $S - N W^{-1} N^T = R^{-1} > 0$. With $W > 0$ this gives $X_{\rm cl} > 0$, and the block inverse formula gives $(X_{\rm cl}^{-1})_{11} = (S - N W^{-1} N^T)^{-1} = R$. The (1,1) block is $S$ by construction. $\square$

The code symmetrizes $W$ before use, which changes nothing in exact arithmetic.

## Claim 2: the closed loop matrices are affine in Omega

*With $\Omega = \begin{bmatrix} A_K & B_K \\ C_K & D_K \end{bmatrix}$, $\tilde B = \begin{bmatrix} 0 & B_2 \\ I & 0 \end{bmatrix}$, $\tilde C = \begin{bmatrix} 0 & I \\ C_2 & 0 \end{bmatrix}$, $\tilde D_{12} = [0 \ D_{12}]$ and $\tilde D_{21} = \begin{bmatrix} 0 \\ D_{21} \end{bmatrix}$:*

$$A_{\rm cl} = \begin{bmatrix} A & 0 \\ 0 & 0 \end{bmatrix} + \tilde B \Omega \tilde C, \quad B_{\rm cl} = \begin{bmatrix} B_1 \\ 0 \end{bmatrix} + \tilde B \Omega \tilde D_{21}, \quad C_{\rm cl} = [C_1 \ 0] + \tilde D_{12} \Omega \tilde C, \quad D_{\rm cl} = D_{11} + \tilde D_{12} \Omega \tilde D_{21}.$$

*Proof.* With $u = C_K x_K + D_K y$, $\dot x_K = A_K x_K + B_K y$ and $y = C_2 x + D_{21} w$, substitute into the plant:

$\dot x = (A + B_2 D_K C_2) x + B_2 C_K x_K + (B_1 + B_2 D_K D_{21}) w$, $\dot x_K = B_K C_2 x + A_K x_K + B_K D_{21} w$, and $z = (C_1 + D_{12} D_K C_2) x + D_{12} C_K x_K + (D_{11} + D_{12} D_K D_{21}) w$.

These are the matrices on the page. Next, $\tilde B \Omega = \begin{bmatrix} B_2 C_K & B_2 D_K \\ A_K & B_K \end{bmatrix}$, and multiplying by $\tilde C$ on the right gives $\begin{bmatrix} B_2 D_K C_2 & B_2 C_K \\ B_K C_2 & A_K \end{bmatrix}$; multiplying by $\tilde D_{21}$ gives $\begin{bmatrix} B_2 D_K D_{21} \\ B_K D_{21} \end{bmatrix}$. Also $\tilde D_{12} \Omega = [D_{12} C_K \ D_{12} D_K]$, so $\tilde D_{12} \Omega \tilde C = [D_{12} D_K C_2 \ D_{12} C_K]$ and $\tilde D_{12} \Omega \tilde D_{21} = D_{12} D_K D_{21}$. These match term by term. $\square$

So, for fixed $X_{\rm cl}$ and $\gamma$, the bounded real matrix is affine in $\Omega$, and the routine `affine` recovers it exactly from its values at $0$ and at the unit vectors.

## Claim 3: every iterate of the barrier method is strictly feasible

*If the starting point $x$ has $G_i(x) > 0$ for all $i$, then every point that `_center` returns has $G_i > 0$ for all $i$. Phase I starts at a strictly feasible point of the augmented problem.*

*Proof.* A step is accepted only when `_objective` is finite, and `_objective` returns a number only when the Cholesky factorization of every $G_i$ succeeds, that is, when every $G_i$ is positive definite. If no step is accepted, the old point is returned. For phase I, the loop doubles $s$ until $G_i(x_0) + sI > 0$ for all $i$ and then doubles it once more, so $G_i(x_0) + sI \ge \tfrac{s}{2} I$. When phase I stops with $s < 0$, every $G_i(x) > -sI > 0$. $\square$

## Claim 4: the infeasibility test of phase I is sound

*Let $z(t)$ be the exact minimizer of $t s - \sum_i \log\det(G_i(x) + sI)$ and $d$ the sum of the block sizes. Then $s^\star \ge s(t) - d/t$, where $s^\star$ is the minimum of $s$. So if $s(t) > d/t$, the LMIs have no solution.*

*Proof.* This is the duality gap bound on the central path of the log-det barrier (Boyd and Vandenberghe 2004, chapter 11): the point $Z_i = (t\,(G_i + sI))^{-1}$ is dual feasible, and the gap between $s(t)$ and its dual value is $\sum_i \mathrm{tr}(Z_i (G_i + sI)) = d/t$. Since $s^\star$ is at least the dual value, $s^\star \ge s(t) - d/t$. If $s^\star > 0$, no $x$ has all $G_i(x) > 0$. $\square$

The code centers to a Newton decrement of $10^{-10}$, not exactly. The tests use the test with a clear margin: the level $0.99\,\gamma_{\rm opt}$.

## Claim 5: the scalar example reduces to scalar inequalities

*For the plant of the example with any real $a$, the three LMIs at level $\gamma > 0$ have a solution if and only if $\gamma > a + \sqrt{a^2 + 2}$.*

*Proof.* The kernel of $[B_2^T \ D_{12}^T] = [1, 0, 1]$ has the orthonormal basis $v_1 = (0, 1, 0)$ and $v_2 = (1, 0, -1)/\sqrt 2$ in the coordinates $(x, z_1, z_2)$. The middle matrix of the first LMI in the coordinates $(x, z_1, z_2, w_1, w_2)$ has the entries $2aR$ at $(x, x)$, $R$ at $(x, z_1)$, $1$ at $(x, w_1)$, and $-\gamma$ on the rest of the diagonal. The projection gives

$$\begin{bmatrix} -\gamma & R/\sqrt 2 & 0 & 0 \\ R/\sqrt 2 & aR - \gamma/2 & 1/\sqrt 2 & 0 \\ 0 & 1/\sqrt 2 & -\gamma & 0 \\ 0 & 0 & 0 & -\gamma \end{bmatrix} < 0.$$

The last row and column only need $\gamma > 0$. A Schur complement on the two other $-\gamma$ entries reduces the rest to $aR - \gamma/2 + (R^2 + 1)/(2\gamma) < 0$, that is $q(R) < \gamma^2$ with $q(t) = t^2 + 2a\gamma t + 1$. The plant is the same after the swaps $A \leftrightarrow A^T$, $B_1 \leftrightarrow C_1^T$, $B_2 \leftrightarrow C_2^T$, $D_{12} \leftrightarrow D_{21}^T$, so the second LMI is $q(S) < \gamma^2$. The third LMI is $R > 0$, $S > 0$ and $RS \ge 1$.

If $\gamma > \gamma^* = a + \sqrt{a^2 + 2}$, then $\gamma^2 - 2a\gamma - 2 > 0$, that is $q(1) < \gamma^2$, so $R = S = 1$ is a solution. Conversely, let $(R, S)$ be a solution and $m = (R + S)/2$. Then $m \ge \sqrt{RS} \ge 1$, and $q$ is convex, so $q(m) \le \max(q(R), q(S)) < \gamma^2$. Divide $q(m) < \gamma^2$ by $m \ge 1$: $m + 1/m + 2a\gamma < \gamma^2/m \le \gamma^2$. Since $m + 1/m \ge 2$, this gives $2 + 2a\gamma < \gamma^2$, so $\gamma > \gamma^*$. $\square$

This agrees with the two-Riccati page, where the same plant has $\gamma_{\rm opt} = a + \sqrt{a^2 + 2}$. At the boundary $q(1) = \gamma^2$, so the solution is $R = S = 1$, which the test checks.

## What the tests check

- The kernel bases are orthonormal and span the kernel, for random matrices with a fixed seed.
- The minimum of $\gamma$ matches $a + \sqrt{a^2 + 2}$ for $a = -1, 0, 1, 2$ with relative error below $10^{-7}$, with $R = S = 1$ at the optimum.
- For a plant with two states, the minimum matches the value $7.2145628072$ from the two-Riccati page within $10^{-7}$ relative.
- At $0.99\,\gamma_{\rm opt}$ phase I reports infeasible; at $1.01\,\gamma_{\rm opt}$ the analytic center makes every LMI positive definite with a Cholesky margin.
- The blocks of $X_{\rm cl}$ and of its inverse (Claim 1).
- The controllers give a Hurwitz closed loop and a frequency sweep peak between $\gamma_{\rm opt}(1 - 10^{-4})$ and $\gamma$.
- A singular plant with $D_{12} = 0$, where the two-Riccati method does not apply. For any stabilizing controller the map from $w_2$ to $z$ equals $-1$ at the unstable pole $s = 1$, so $\gamma_{\rm opt} \ge 1$ by the maximum modulus principle. The code returns a value in $[1, 1.01)$ and a controller that meets its level.
