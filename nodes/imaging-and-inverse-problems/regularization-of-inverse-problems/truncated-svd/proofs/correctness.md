---
title: TSVD returns the minimum norm solution of the truncated problem, its residuals are exact, and it converges at the optimal rate
proves: [correctness]
status: full
---

**Setting.** Let $A$ be a real $m \times n$ matrix with SVD $A = \sum_{i=1}^{p} \sigma_i u_i v_i^T$, $p = \min(m, n)$, where $u_1, \ldots, u_p$ are orthonormal in $\mathbb{R}^m$, $v_1, \ldots, v_p$ are orthonormal in $\mathbb{R}^n$, and $\sigma_1 \ge \cdots \ge \sigma_r > 0 = \sigma_{r+1} = \cdots = \sigma_p$. For $0 \le k \le r$ let $A_k = \sum_{i \le k} \sigma_i u_i v_i^T$, $\beta_i = u_i^T y$ and $P_k = \sum_{i \le k} u_i u_i^T$. All statements are in exact arithmetic. In floating point they hold for the exact SVD of a nearby matrix $A + E$ with $\|E\| \le c\,u\|A\|$, if the SVD is backward stable.

**Step 1: the output of TSVD.** Lines L2 to L5 return $x_k = \sum_{i \le k} (\beta_i/\sigma_i) v_i$. The loop adds one term per pass, and $k \le r$ makes each $\sigma_i$ positive, so no division by zero occurs.

**Step 2: $x_k$ is the minimum norm minimizer of $\|A_k x - y\|$.** Complete $v_1, \ldots, v_k$ to an orthonormal basis of $\mathbb{R}^n$ and write $z_i = v_i^T x$. Since $A_k x = \sum_{i \le k} \sigma_i z_i u_i \in R(P_k)$,
$$\|A_k x - y\|^2 = \|A_k x - P_k y\|^2 + \|y - P_k y\|^2 = \sum_{i \le k} (\sigma_i z_i - \beta_i)^2 + \|y - P_k y\|^2.$$
The second term does not depend on $x$, so the minimizers are exactly the $x$ with $z_i = \beta_i/\sigma_i$ for $i \le k$, and the other coordinates of $x$ are free. The norm $\|x\|^2 = \sum_i z_i^2$ is smallest when the free coordinates are zero, which gives $x_k$. So $x_k = A_k^\dagger y$. For $k = r$, $A_r = A$ and $x_r = A^\dagger y$, the minimum norm least squares solution.

**Step 3: the residual and the solution norm.** Let $y_\perp = y - P_r y$, which is orthogonal to every $u_i$ with $i \le r$. Then
$$A x_k - y = \sum_{i \le k} \beta_i u_i - y = -\Big(\sum_{k < i \le r} \beta_i u_i + y_\perp\Big),$$
and by orthogonality
$$\rho_k^2 = \|A x_k - y\|^2 = \|y_\perp\|^2 + \sum_{k < i \le r} \beta_i^2, \qquad \|x_k\|^2 = \sum_{i \le k} \frac{\beta_i^2}{\sigma_i^2}.$$
For $k = r$ the sum is empty, so $\rho_r^2 = \|y - \sum_{i \le r} \beta_i u_i\|^2$, which is line L7. For $k < r$, $\rho_k^2 - \rho_{k+1}^2 = \beta_{k+1}^2$, which is line L9. Line L8 runs $k$ from $r - 1$ down to $0$, so every $\rho_k^2$ is computed from $\rho_{k+1}^2$ after that value is known. Both formulas show that $\rho_k$ does not increase and $\|x_k\|$ does not decrease as $k$ grows. Line L10 scans $k = 0, 1, \ldots, r$ and returns the first $k$ with $\rho_k \le \tau\delta$; by the monotony, every larger $k$ also satisfies the test, and if $\rho_r > \tau\delta$ no $k$ does, so "none" is correct.

**Step 4: the error for noisy data.** Let $y = A x^\dagger$ with $x^\dagger = A^\dagger y$, so $\beta_i/\sigma_i = v_i^T x^\dagger$ for $i \le r$ and $x^\dagger = \sum_{i \le r} (v_i^T x^\dagger) v_i$. Let $\|y^\delta - y\| \le \delta$ and let $x_k^\delta$ be the TSVD solution for $y^\delta$. Then
$$x_k^\delta - x^\dagger = \sum_{i \le k} \frac{u_i^T (y^\delta - y)}{\sigma_i} v_i \;-\; \sum_{k < i \le r} (v_i^T x^\dagger)\, v_i.$$
The two sums are orthogonal. The first has norm squared $\sum_{i \le k} (u_i^T(y^\delta - y))^2/\sigma_i^2 \le \sigma_k^{-2} \sum_{i \le k} (u_i^T(y^\delta - y))^2 \le \delta^2/\sigma_k^2$, by Bessel's inequality. So
$$\|x_k^\delta - x^\dagger\| \le \frac{\delta}{\sigma_k} + \Big\| \sum_{i > k} \frac{u_i^T y}{\sigma_i} v_i \Big\|,$$
the propagated noise plus the truncation error. For $k = 0$ the first term is absent.

**Step 5: the rate under a source condition.** Assume $x^\dagger = (A^T A)^\nu w$ with $\nu > 0$ and $\|w\| \le C$. Then $v_i^T x^\dagger = \sigma_i^{2\nu}\, v_i^T w$, and the truncation error is
$$\Big\| \sum_{k < i \le r} \sigma_i^{2\nu} (v_i^T w) v_i \Big\| \le \sigma_{k+1}^{2\nu} \|w\| \le \sigma_{k+1}^{2\nu} C,$$
with $\sigma_{r+1} = 0$. Let $\mu = \delta^{1/(2\nu+1)}$ and let $k \le r$ be the largest index with $\sigma_k \ge \mu$, or $k = 0$ if $\sigma_1 < \mu$. Then $\sigma_{k+1} < \mu$, so the truncation error is at most $C\mu^{2\nu} = C\,\delta^{2\nu/(2\nu+1)}$. The noise term is $0$ if $k = 0$ and at most $\delta/\mu = \delta^{2\nu/(2\nu+1)}$ otherwise. Hence
$$\|x_k^\delta - x^\dagger\| \le (1 + C)\, \delta^{2\nu/(2\nu+1)}.$$
The bound $\sigma_{k+1}^{2\nu}$ holds for every $\nu$, so there is no saturation: the qualification of TSVD is infinite. In $\delta$ this is the order $\delta^{2\nu/(2\nu+1)}$ that no method can beat on this set (see the order optimality statement on the page [regularization method](/regularization-method/)).

**Step 6: convergence for an operator.** The same computation holds for a compact operator with singular system $(\sigma_i; v_i, u_i)$ and $y$ in the domain of $A^\dagger$; the sums become series, which converge by the [Picard condition](/picard-condition/). If $k(\delta) \to \infty$ and $\delta/\sigma_{k(\delta)} \to 0$ as $\delta \to 0$, both terms of Step 4 tend to zero: the first by assumption, the second because it is the tail of a convergent series. The bound does not depend on which $y^\delta$ was chosen, so TSVD with such a rule is a regularization method.

**Step 7: $A_k$ is the best rank-$k$ approximation (Eckart-Young).** First the 2-norm. $\|A - A_k\|_2 = \|\sum_{i > k} \sigma_i u_i v_i^T\|_2 = \sigma_{k+1}$. Let $B$ have rank at most $k$. Its null space has dimension at least $n - k$, and the span of $v_1, \ldots, v_{k+1}$ has dimension $k + 1$, so the two spaces share a unit vector $z = \sum_{i \le k+1} c_i v_i$ with $\sum c_i^2 = 1$. Then
$$\|(A - B) z\|^2 = \|A z\|^2 = \sum_{i \le k+1} \sigma_i^2 c_i^2 \ge \sigma_{k+1}^2,$$
so $\|A - B\|_2 \ge \sigma_{k+1}$.

Next the Frobenius norm, through Weyl's inequality $\sigma_{i+j-1}(C + D) \le \sigma_i(C) + \sigma_j(D)$. To prove it, let $C_{i-1}$ and $D_{j-1}$ be the truncations of $C$ and $D$. Their sum has rank at most $i + j - 2$, so by the 2-norm result
$$\sigma_{i+j-1}(C + D) \le \|C + D - C_{i-1} - D_{j-1}\|_2 \le \|C - C_{i-1}\|_2 + \|D - D_{j-1}\|_2 = \sigma_i(C) + \sigma_j(D).$$
Apply it with $C = A - B$, $D = B$ and $j = k + 1$. Since $\sigma_{k+1}(B) = 0$, we get $\sigma_{i+k}(A) \le \sigma_i(A - B)$ for every $i$. Squaring and adding over $i$ gives
$$\|A - B\|_F^2 = \sum_i \sigma_i(A - B)^2 \ge \sum_{i > k} \sigma_i(A)^2 = \|A - A_k\|_F^2.$$
So $A_k$ is a closest matrix of rank at most $k$ in both norms. $\square$
