---
title: The two-loop recursion computes the BFGS product, L-BFGS directions go downhill, and on quadratics with exact steps L-BFGS is conjugate gradient
proves: [correctness, termination]
status: full
---

**Setting.** For pairs $(s_1, y_1), \dots, (s_\ell, y_\ell)$ with $y_i^\top s_i > 0$, let $\rho_i = 1/(y_i^\top s_i)$, $V_i = I - \rho_iy_is_i^\top$, and for a number $\gamma > 0$ let
$$H_0 = \gamma I, \qquad H_i = V_i^\top H_{i-1}V_i + \rho_is_is_i^\top \quad (i = 1, \dots, \ell).$$
TWO-LOOP (lines L9 to L12) uses $\gamma = s_\ell^\top y_\ell/y_\ell^\top y_\ell$, or $\gamma = 1$ when $\ell = 0$.

**Claim 1 (the two-loop recursion).** For a fixed $\gamma$, lines L9 to L12 return $H_\ell q$.

*Proof.* Induction on $\ell$. For $\ell = 0$ both loops are empty and the result is $\gamma q = H_0q$.

Let $\ell \ge 1$. The first pass of the first loop (with $i = \ell$) sets $a_\ell = \rho_\ell s_\ell^\top q$ and $q' = q - a_\ell y_\ell = V_\ell q$. The rest of the first loop, the scaling and the second loop up to $i = \ell - 1$ are exactly lines L9 to L12 applied to $q'$ and the first $\ell - 1$ pairs with the same $\gamma$, so by the hypothesis they produce $r' = H_{\ell-1}q'$. The last pass of the second loop sets $b = \rho_\ell y_\ell^\top r'$ and returns $r' + (a_\ell - b)s_\ell$. On the other side,
$$H_\ell q = V_\ell^\top H_{\ell-1}V_\ell q + \rho_\ell s_\ell(s_\ell^\top q) = V_\ell^\top r' + a_\ell s_\ell = r' - \rho_\ell s_\ell(y_\ell^\top r') + a_\ell s_\ell = r' + (a_\ell - b)s_\ell.$$
The two are equal. $\square$

**Claim 2 (positive definiteness, secant equation, descent, termination).** If every stored pair has $y_i^\top s_i > 0$, then $\gamma > 0$, $H_\ell$ is symmetric positive definite, $H_\ell y_\ell = s_\ell$, and $d = -H_\ell g$ satisfies $g^\top d < 0$ for $g \ne 0$. With Wolfe steps, every pair is stored, $f(x_{k+1}) < f(x_k)$, and the method stops after at most $K$ iterations.

*Proof.* $\gamma = s_\ell^\top y_\ell/\|y_\ell\|^2 > 0$, so $H_0$ is symmetric positive definite. Each update keeps symmetry and positive definiteness when $y_i^\top s_i > 0$, and the last one gives $H_\ell y_\ell = s_\ell$ ([BFGS](/bfgs/), claims 1 and 2). So $g^\top d = -g^\top H_\ell g < 0$. Line L6 stores only pairs with $y^\top s > 0$. Under the Wolfe curvature condition, $y_k^\top s_k \ge (1 - c_2)\alpha_k|g_k^\top d_k| > 0$, so every pair is stored. The Armijo condition gives $f(x_{k+1}) \le f(x_k) + c_1\alpha_kg_k^\top d_k < f(x_k)$. The line search returns only steps that pass both tests and otherwise stops the method after a fixed number of trial points, and the loop of line L2 runs at most $K$ times. $\square$

**Claim 3 (quadratics with exact steps).** Let $f(x) = \frac12x^\top Ax - b^\top x$ with $A$ symmetric positive definite, and let every $\alpha_k$ minimize $f(x_k + \alpha d_k)$. Then for every $m \ge 1$, each $d_k$ is a positive multiple of the direction $p_k$ of linear conjugate gradient from the same $x_0$, the iterates are those of linear conjugate gradient, and $\nabla f(x_k) = 0$ for some $k \le n$ in exact arithmetic.

*Proof.* Induction on $k$. For $k = 0$ there are no pairs, $d_0 = -g_0 = p_0$, and the exact steps agree. Assume that $x_0, \dots, x_k$ are the conjugate gradient iterates and $g_k \ne 0$. Write $g_j = \nabla f(x_j)$ and $s_j = x_{j+1} - x_j = \tau_jp_j$, where $\tau_j = \|g_j\|^2/(p_j^\top Ap_j)$ is the conjugate gradient step. By the properties of linear conjugate gradient ([nonlinear conjugate gradient](/nonlinear-conjugate-gradient/), claim 2, and its proof): the gradients $g_0, \dots, g_k$ are mutually orthogonal, the steps $s_j$ are mutually $A$-conjugate, and $g_k^\top s_j = 0$ for $j < k$. Also $y_j = As_j$ and $y_j^\top s_j = s_j^\top As_j > 0$, so every pair is stored, and the list holds the pairs $j = k - \ell, \dots, k - 1$ with $\ell = \min(m, k)$.

By claim 1, $d_k = -H_\ell g_k$, where $H_\ell$ comes from $\gamma_kI$ by the updates with these pairs in order. Let $G_j$ denote the matrix after the updates with the stored pairs up to $j$. For each stored $j$, $s_j^\top g_k = 0$ gives $V_jg_k = g_k$, so
$$G_jg_k = V_j^\top G_{j-1}g_k = G_{j-1}g_k - \rho_j(y_j^\top G_{j-1}g_k)s_j.$$
By induction, $G_{j-1}g_k = \gamma_kg_k + \sum_ic_is_i$ over stored $i < j$, and $y_j^\top s_i = s_j^\top As_i = 0$ for $i \ne j$, so $y_j^\top G_{j-1}g_k = \gamma_ky_j^\top g_k = \gamma_k(g_{j+1} - g_j)^\top g_k$. By the orthogonality of the gradients this is $0$ for $j < k - 1$ and $\gamma_k\|g_k\|^2$ for $j = k - 1$. Hence
$$H_\ell g_k = \gamma_k\left(g_k - \rho_{k-1}\|g_k\|^2s_{k-1}\right).$$
Here $\rho_{k-1}^{-1} = s_{k-1}^\top As_{k-1} = \tau_{k-1}^2p_{k-1}^\top Ap_{k-1} = \tau_{k-1}\|g_{k-1}\|^2$, so $\rho_{k-1}\|g_k\|^2s_{k-1} = \frac{\|g_k\|^2}{\|g_{k-1}\|^2}p_{k-1}$, and
$$d_k = \gamma_k\left(-g_k + \frac{\|g_k\|^2}{\|g_{k-1}\|^2}p_{k-1}\right) = \gamma_kp_k,$$
with $\gamma_k > 0$. The exact line search along a positive multiple of $p_k$ reaches the same point as along $p_k$, so $x_{k+1}$ is the conjugate gradient iterate. Linear conjugate gradient reaches $g_k = 0$ for some $k \le n$ in exact arithmetic. $\square$

**Remark (the R-linear theorem).** The R-linear convergence on uniformly convex functions stated on the main page is the theorem of Liu and Nocedal. Its proof bounds the trace and the determinant of $H_k^{-1}$ in terms of the bounds on the Hessian and on the starting matrices, which gives a lower bound on the cosine of the angle between $d_k$ and $-\nabla f(x_k)$ at every step; the linear decrease then follows from the Wolfe conditions as in [gradient descent](/gradient-descent/). It is not repeated here.

**Remark (floating point).** In floating point the orthogonality and conjugacy of claim 3 hold up to rounding, so on ill-conditioned quadratics the iterates drift from those of linear conjugate gradient, and more than $n$ steps can be needed.
