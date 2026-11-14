---
title: The SIMP iteration keeps feasible designs, its OC update stops, and its fixed points are KKT points
proves: [correctness, termination]
status: full
---

**Setting.** The grid has $n$ elements. The element matrix $k_0$ is symmetric positive semidefinite, because $k_0 = \int B^{\mathsf T} D B$ with $D$ positive definite. The supports fix enough degrees of freedom that $\sum_e s_e K_e$, restricted to the free degrees of freedom, is positive definite whenever every $s_e > 0$. Let $0 < x_{\min} < v \le 1$, $p \ge 1$, $m > 0$, $\eta > 0$, $V = v n$, and let $r > 0$ be the filter radius. The proof uses exact real arithmetic.

**Claim.**

1. Every design $x$ that the method computes satisfies $x_{\min} \le x_e \le 1$ and $\sum_e x_e \le V$, and every linear system of line L3 has a unique solution.
2. Each call of OC stops, and the main loop stops after at most maxit iterations.
3. If a design $x$ with $\sum_e x_e = V$ satisfies $x = \text{TRIAL}(\lambda)$ for some $\lambda > 0$, with $dc$ computed from $x$ itself and $r \le 1$, then $x$ satisfies the KKT conditions of the penalized problem with the multiplier $\lambda$.
4. For $p = 1$ the compliance is convex in $x$, so such a point is a global minimum of the problem with $p = 1$.

**Step 1 (signs).** Let $x$ satisfy $x_{\min} \le x_e \le 1$. Then $K(x) = \sum_e x_e^p K_e$ has all scales $x_e^p \ge x_{\min}^p > 0$, so it is positive definite and line L3 has a unique solution $u$. Line L5 gives $dc_e = -p\,x_e^{p-1}\, u_e^{\mathsf T} k_0 u_e \le 0$, because $k_0$ is positive semidefinite. In line L6, $H_{ef} \ge 0$ for all $f$ and $H_{ee} = r > 0$, so the denominator $x_e \sum_f H_{ef}$ is positive and the numerator $\sum_f H_{ef} x_f\, dc_f$ is at most 0. So the filtered values also satisfy $dc_e \le 0$.

**Step 2 (TRIAL is monotone and stays in the box).** Fix $x$ in the box and $dc \le 0$. For $\lambda > 0$ let $g_e(\lambda) = x_e(-dc_e/\lambda)^\eta$ and
$$T_e(\lambda) = \max\bigl(x_{\min},\ x_e - m,\ \min(1,\ x_e + m,\ g_e(\lambda))\bigr).$$
The function $g_e$ does not increase with $\lambda$, and min and max are nondecreasing in each argument, so $T_e$ and $S(\lambda) = \sum_e T_e(\lambda)$ do not increase with $\lambda$. Each $T_e$ is continuous for $\lambda > 0$, so $S$ is too. Each of the three arguments of the outer max is at most 1 (since $x_{\min} < 1$ and $x_e - m < 1$), so $T_e \le 1$, and $T_e \ge x_{\min}$. Also $T_e \ge x_e - m$ and $T_e \le \max(x_{\min}, x_e - m, x_e + m) = x_e + m$, so the move limit holds.

**Step 3 (line L12 stops).** Let $L_e = \max(x_{\min}, x_e - m)$. Then $L_e \le x_e$, with equality only if $x_e = x_{\min}$. If some $x_e > x_{\min}$, then $\sum_e L_e < \sum_e x_e \le V$. If every $x_e = x_{\min}$, then $\sum_e L_e = n x_{\min} < n v = V$. So $\sum_e L_e < V$ in both cases. Let $\Lambda = \max_e (-dc_e)(x_e / x_{\min})^{1/\eta}$. For $\lambda \ge \Lambda$ and every $e$, $g_e(\lambda) \le x_e \cdot x_{\min}/x_e = x_{\min}$ (and $g_e = 0$ if $dc_e = 0$), so the inner min is at most $x_{\min}$ and $T_e(\lambda) = L_e$. Hence $S(\lambda) < V$ for $\lambda \ge \Lambda$. Line L12 sets $l_2 = 2^j$ after $j$ doublings, so it stops after at most $\max(0, \lceil \log_2 \Lambda \rceil)$ doublings. When it stops, $S(l_2) \le V$, and $l_1 = 0$ or $S(l_1) > V$.

**Step 4 (the bisection keeps a feasible end).** Lines L13 to L16 keep the invariant $0 \le l_1 < l_2$ and $S(l_2) \le V$. Line L14 picks $\lambda$ strictly between $l_1$ and $l_2$, so $\lambda > 0$. If $S(\lambda) > V$, line L15 moves $l_1$ and leaves $l_2$. Otherwise it sets $l_2 = \lambda$, and then $S(l_2) \le V$. The loop runs at most 100 times. Line L17 returns $T(l_2)$, so by Step 2 the result is in the box, within the move limit, and meets the volume bound. If $l_1 > 0$ at the end, then $S(l_1) > V \ge S(l_2)$, and by continuity some $\lambda^* \in (l_1, l_2]$ has $S(\lambda^*) = V$, so $l_2$ is within the relative distance tol$_\lambda$ of a multiplier that makes the volume bound tight when line L16 ended the loop.

**Step 5 (claims 1 and 2).** Line L1 sets $x_e = v$, which is in the box with $\sum_e x_e = V$. By Steps 1 to 4, if the current design is feasible, then the design of line L9 is feasible. By induction every design is feasible, and line L3 is always solvable. Each OC call stops by Steps 3 and 4, and the loop of line L2 runs at most maxit times.

**Step 6 (claim 3).** With $r \le 1$, every $f \ne e$ has $\operatorname{dist}(e, f) \ge 1 \ge r$, so $H_{ef} = 0$ and line L6 returns $dc_e$ unchanged. So $dc_e = \partial c / \partial x_e$. Let $x = T(\lambda)$. Since $x_e - m < x_e$, the outer max equals $x_e$ in one of two ways.

- $x_e = x_{\min}$ and $\min(1, x_e + m, g_e) \le x_{\min}$, or $x_e = \min(1, x_e + m, g_e)$.
- In the second way, $x_e + m > x_e$, so $x_e = 1 \le g_e$ or $x_e = g_e$.

If $x_{\min} < x_e < 1$, then $x_e = g_e = x_e(-dc_e/\lambda)^\eta$, and since $x_e > 0$, $-dc_e = \lambda$. If $x_e = x_{\min}$, then $g_e \le x_{\min} = x_e$ in both ways, because the bounds 1 and $x_e + m$ are above $x_{\min}$, so $(-dc_e/\lambda)^\eta \le 1$ and $-dc_e \le \lambda$. If $x_e = 1$, then $g_e \ge 1$, so $-dc_e \ge \lambda$. Now set $\mu_e = \lambda + dc_e \ge 0$ where $x_e = x_{\min}$, $\nu_e = -dc_e - \lambda \ge 0$ where $x_e = 1$, and $\mu_e = \nu_e = 0$ elsewhere. Then
$$\frac{\partial c}{\partial x_e} + \lambda - \mu_e + \nu_e = 0, \quad \mu_e (x_e - x_{\min}) = 0, \quad \nu_e (1 - x_e) = 0, \quad \lambda \Bigl(\sum_e x_e - V\Bigr) = 0,$$
with $\lambda, \mu, \nu \ge 0$. These are the KKT conditions of $\min c(x)$ subject to $\sum_e x_e \le V$ and $x_{\min} \le x_e \le 1$.

**Step 7 (claim 4).** For a positive definite $K$ and every $f$, $f^{\mathsf T} K^{-1} f = \max_u\, (2 f^{\mathsf T} u - u^{\mathsf T} K u)$, because the concave quadratic on the right has its maximum at $u = K^{-1} f$. For $p = 1$, $K(x) = \sum_e x_e K_e$ is linear in $x$, so for each fixed $u$ the function $x \mapsto 2 f^{\mathsf T} u - u^{\mathsf T} K(x) u$ is affine. A pointwise maximum of affine functions is convex, so $c(x)$ is convex on the box. The constraints are linear, so a KKT point of a convex problem is a global minimum. The same formula shows that $c$ does not increase when $K$ grows in the positive semidefinite order, because each $u^{\mathsf T} K u$ grows.

**Remark.** The claims hold in exact arithmetic. In floating point the sums of Steps 3 and 4 are rounded, and the test checks the volume bound with a relative tolerance of $10^{-12}$. Claim 3 is about exact fixed points. The code stops when no density changes by more than a tolerance, so its result is only near such a point. With $r > 1$ the same argument gives the conditions for the filtered values, which are not the derivatives of $c$. For $p > 1$ the function $c$ is not convex in general, and a KKT point need not be a global minimum. $\blacksquare$
