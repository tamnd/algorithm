---
title: The BFGS update keeps the secant equation and positive definiteness, and terminates on quadratics with H_n = A^(-1)
proves: [correctness, termination]
status: full
---

**Setting.** With $s = x^+ - x$, $y = \nabla f(x^+) - \nabla f(x)$, $y^\top s > 0$, $\rho = 1/(y^\top s)$ and $V = I - \rho ys^\top$, line L7 computes $H^+ = V^\top HV + \rho ss^\top$. Write $g_k = \nabla f(x_k)$, $d_k = -H_kg_k$, $s_k = \alpha_kd_k$ and $y_k = g_{k+1} - g_k$.

**Claim 1 (secant equation and symmetry).** If $H$ is symmetric and $y^\top s > 0$, then $H^+$ is symmetric and $H^+y = s$.

*Proof.* $V^\top HV$ and $ss^\top$ are symmetric. $Vy = y - \rho y(s^\top y) = 0$, so $H^+y = V^\top H(Vy) + \rho s(s^\top y) = 0 + s$. $\square$

**Claim 2 (positive definiteness, descent, termination).** If $H$ is symmetric positive definite and $y^\top s > 0$, then $H^+$ is symmetric positive definite. If every step satisfies the Wolfe conditions with $c_2 < 1$, then $y_k^\top s_k > 0$ for all $k$, every $H_k$ is symmetric positive definite, every $d_k$ is a descent direction, $f(x_{k+1}) < f(x_k)$, and the method stops after at most $K$ iterations.

*Proof.* Let $z \ne 0$ and $w = Vz = z - \rho y(s^\top z)$. Then $z^\top H^+z = w^\top Hw + \rho(s^\top z)^2$. Both terms are at least $0$. If $s^\top z \ne 0$, the second term is positive. If $s^\top z = 0$, then $w = z \ne 0$ and the first term is positive. So $z^\top H^+z > 0$.

For the Wolfe steps, the curvature condition $g_{k+1}^\top d_k \ge c_2g_k^\top d_k$ gives $y_k^\top s_k = \alpha_k(g_{k+1} - g_k)^\top d_k \ge \alpha_k(c_2 - 1)g_k^\top d_k$. If $H_k$ is positive definite and $g_k \ne 0$, then $g_k^\top d_k = -g_k^\top H_kg_k < 0$, so $y_k^\top s_k > 0$, the test of line L7 passes, and $H_{k+1}$ is positive definite by the first part. The rescaled matrix of line L6 is $(y^\top s/y^\top y)I$ with $y^\top s > 0$, which is positive definite. Induction from $H_0$ gives the claim for all $k$. The Armijo condition gives $f(x_{k+1}) \le f(x_k) + c_1\alpha_kg_k^\top d_k < f(x_k)$. The line search returns only steps that pass both tests and otherwise stops the method after a fixed number of trial points, and the loop of line L2 runs at most $K$ times. $\square$

**Claim 3 (quadratic termination).** Let $f(x) = \frac12x^\top Ax - b^\top x$ with $A$ symmetric positive definite, so $y_k = As_k$, let $H_0$ be symmetric positive definite, and let every step be exact: $\alpha_k$ minimizes $f(x_k + \alpha d_k)$, so $g_{k+1}^\top s_k = 0$. As long as $g_0, \dots, g_k \ne 0$:

- (a) $s_i^\top As_j = 0$ for $i < j \le k$;
- (b) $H_{k+1}y_j = s_j$ for all $j \le k$;
- (c) $g_{k+1}^\top s_j = 0$ for all $j \le k$.

Hence $g_k = 0$ for some $k \le n$, and if $n$ steps are taken, then $H_n = A^{-1}$. The same holds with the rescaling of line L6, since it only replaces $H_0$ by another positive definite matrix before the first update.

*Proof.* Each $s_k \ne 0$ while $g_k \ne 0$: $H_k$ is positive definite (claim 2, with $y_k^\top s_k = s_k^\top As_k > 0$), so $g_k^\top d_k < 0$ and the exact step $\alpha_k = -g_k^\top d_k/(d_k^\top Ad_k)$ is positive.

(c) follows from (a): for $j \le k$, $g_{k+1} = g_{j+1} + \sum_{i=j+1}^kAs_i$, so $s_j^\top g_{k+1} = s_j^\top g_{j+1} + \sum_is_j^\top As_i = 0$, by the exact step at $j$ and by (a).

Induction on $k$. For $k = 0$, (a) is empty and (b) is $H_1y_0 = s_0$, which is claim 1. Assume (a) and (b) for $k$, and $g_{k+1} \ne 0$. Then (c) holds for $k$.

Conjugacy: for $j \le k$, $s_{k+1}^\top As_j = s_{k+1}^\top y_j = -\alpha_{k+1}g_{k+1}^\top H_{k+1}y_j = -\alpha_{k+1}g_{k+1}^\top s_j = 0$, by (b) and (c). So (a) holds for $k + 1$.

Heredity: let $s = s_{k+1}$, $y = y_{k+1}$ and $j \le k$. Then $s^\top y_j = s_{k+1}^\top As_j = 0$ and $y^\top s_j = s_{k+1}^\top As_j = 0$. So $Vy_j = y_j - \rho y(s^\top y_j) = y_j$, $H_{k+1}y_j = s_j$ by (b), $V^\top s_j = s_j - \rho s(y^\top s_j) = s_j$, and
$$H_{k+2}y_j = V^\top H_{k+1}Vy_j + \rho s(s^\top y_j) = V^\top s_j + 0 = s_j.$$
With $H_{k+2}y_{k+1} = s_{k+1}$ (claim 1), (b) holds for $k + 1$.

Termination: nonzero, mutually $A$-conjugate vectors are linearly independent, because $\sum_ic_is_i = 0$ gives $c_js_j^\top As_j = 0$ after multiplication by $s_j^\top A$. So at most $n$ steps have $g_k \ne 0$. If $n$ steps are taken, $s_0, \dots, s_{n-1}$ is a basis, $g_n$ is orthogonal to all of them by (c), so $g_n = 0$. Also $H_nAs_j = H_ny_j = s_j$ for all $j < n$ by (b), so $H_nA = I$ on a basis, and $H_n = A^{-1}$. $\square$

**Claim 4 (conjugate gradient).** Under the conditions of claim 3 with $H_0 = I$ and no rescaling, $d_k = -g_k + \beta_kd_{k-1}$ with $\beta_k = \|g_k\|^2/\|g_{k-1}\|^2$, so the iterates are those of the linear conjugate gradient method.

*Proof.* Induction on $k$. Both methods start with $d_0 = -g_0$ and use the exact step, which is the step of linear conjugate gradient. Assume the iterates agree up to $x_{k+1}$. Then $g_0, \dots, g_{k+1}$ are the residuals of linear conjugate gradient, which are mutually orthogonal, and $g_k^\top d_k = -\|g_k\|^2$ ([nonlinear conjugate gradient](/nonlinear-conjugate-gradient/), claim 2).

First, for $0 \le j \le k + 1$, $H_jg_{k+1} = g_{k+1} + \sum_{i<j}c_is_i$ for some numbers $c_i$, and for $j \le k$
$$H_{j+1}g_{k+1} = H_jg_{k+1} - \rho_j(y_j^\top H_jg_{k+1})s_j.$$
Indeed $H_0g_{k+1} = g_{k+1}$. For $j \le k$, (c) gives $s_j^\top g_{k+1} = 0$, so $V_jg_{k+1} = g_{k+1}$ and $H_{j+1}g_{k+1} = V_j^\top H_jg_{k+1} = H_jg_{k+1} - \rho_js_j(y_j^\top H_jg_{k+1})$, which also keeps the form.

Second, $y_j^\top H_jg_{k+1} = y_j^\top g_{k+1} + \sum_{i<j}c_iy_j^\top s_i = y_j^\top g_{k+1}$, because $y_j^\top s_i = s_j^\top As_i = 0$ for $i < j$. And $y_j^\top g_{k+1} = g_{j+1}^\top g_{k+1} - g_j^\top g_{k+1}$, which is $0$ for $j < k$ and $\|g_{k+1}\|^2$ for $j = k$, by the orthogonality of the gradients.

So $H_{k+1}g_{k+1} = g_{k+1} - \rho_k\|g_{k+1}\|^2s_k$. Here $\rho_k^{-1} = y_k^\top s_k = \alpha_k^2d_k^\top Ad_k = \alpha_k\|g_k\|^2$, because $\alpha_kd_k^\top Ad_k = -g_k^\top d_k = \|g_k\|^2$. With $s_k = \alpha_kd_k$,
$$d_{k+1} = -H_{k+1}g_{k+1} = -g_{k+1} + \frac{\|g_{k+1}\|^2}{\alpha_k\|g_k\|^2}\alpha_kd_k = -g_{k+1} + \frac{\|g_{k+1}\|^2}{\|g_k\|^2}d_k,$$
which is the direction of linear conjugate gradient. The exact steps along equal directions are equal, so $x_{k+2}$ agrees. $\square$

**Remark (cited theorems).** Global convergence on uniformly convex functions and the superlinear local rate are stated on the main page with their assumptions; their proofs (Powell; Byrd and Nocedal; Nocedal and Wright, Section 6.4) use the trace and determinant of $B_k = H_k^{-1}$ to bound the angles between $d_k$ and $-g_k$, and are not repeated here.

**Remark (floating point).** In floating point, $g_{k+1}^\top s_k$ is at rounding size after an exact step, so (a) to (c) hold only up to rounding, and $H_n$ agrees with $A^{-1}$ to a relative accuracy that degrades with the condition number of $A$.
