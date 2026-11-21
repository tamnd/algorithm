---
title: The SVD formula gives the distances between neighbouring Tikhonov solutions, the discrete rule tends to the continuous one, and the distances are bounded by the two error terms
proves: [correctness, termination]
status: full
---

**Setting.** $A$ is a real $m \times n$ matrix with thin SVD $A = \sum_{i=1}^r s_iu_iv_i^T$, $s_1 \ge \dots \ge s_r > 0$. For $\alpha > 0$, $x_\alpha = (A^TA + \alpha I)^{-1}A^Ty$. Line L1 computes $b_i = \langle u_i, y\rangle$. The grid is $\alpha_j = \alpha_0q^j$ with $\alpha_0 > 0$, $0 < q < 1$ and $j = 0, \dots, N$.

**Claim 1 (solutions and distances).** $x_\alpha = \sum_i s_ib_i/(s_i^2 + \alpha)\,v_i$, and the number $d_j$ of line L3 equals $\lVert x_{\alpha_{j+1}} - x_{\alpha_j}\rVert$.

*Proof.* In the basis $v_i$ the normal equations $(A^TA + \alpha I)x = A^Ty$ read $(s_i^2 + \alpha)\xi_i = s_ib_i$ for $i \le r$ and $\alpha\xi = 0$ on the null space of $A$. So the coefficient of $v_i$ in $x_{\alpha_{j+1}} - x_{\alpha_j}$ is $s_ib_i(1/(s_i^2 + \alpha_{j+1}) - 1/(s_i^2 + \alpha_j))$, and the $v_i$ are orthonormal. $\square$

**Claim 2 (termination and output).** Line L3 computes $N$ numbers with $\Theta(r)$ work each, line L4 returns an index $j^\ast$ with $d_{j^\ast} = \min_j d_j$, and line L5 returns $x_{\alpha_{j^\ast}}$ by Claim 1. There is no loop with an open end. $\square$

**Claim 3 (the derivative).** $x_\alpha$ is differentiable in $\alpha$ with $dx_\alpha/d\alpha = -(A^TA + \alpha I)^{-1}x_\alpha = -\sum_i s_ib_i/(s_i^2 + \alpha)^2\,v_i$.

*Proof.* Differentiate $(A^TA + \alpha I)x_\alpha = A^Ty$: $x_\alpha + (A^TA + \alpha I)x_\alpha' = 0$. The SVD form follows from differentiating each coefficient $s_ib_i/(s_i^2 + \alpha)$. $\square$

**Claim 4 (continuous limit).** For fixed $\alpha$, $\lVert x_{q\alpha} - x_\alpha\rVert/(1 - q) \to \alpha\lVert dx_\alpha/d\alpha\rVert$ as $q \to 1$.

*Proof.* $x_{q\alpha} - x_\alpha = x'_\alpha(q\alpha - \alpha) + o(|1 - q|\alpha) = -(1 - q)\alpha x'_\alpha + o(1 - q)$, since $x_\alpha$ is smooth in $\alpha > 0$ by Claim 3. Divide by $1 - q$ and take norms. $\square$

**Claim 5 (scaling).** If $A$, $y$ and $\alpha_0$ are replaced by $cA$, $cy$ and $c^2\alpha_0$ for $c > 0$, the distances $d_j$ are unchanged, so the rule picks the same $j^\ast$, the parameter $c^2\alpha_{j^\ast}$ and the same solution.

*Proof.* The singular values become $cs_i$ and the coefficients $cb_i$, with the same $v_i$. Each coefficient $cs_icb_i/(c^2s_i^2 + c^2\alpha_j) = s_ib_i/(s_i^2 + \alpha_j)$ is unchanged. $\square$

**Claim 6 (the distances are bounded by the errors).** Let $y = \bar y + e$ with $\bar y = Ax^\dagger$, let $\bar x_\alpha$ be the Tikhonov solution for $\bar y$, $\varphi(\alpha) = \lVert\bar x_\alpha - x^\dagger\rVert$ the approximation error and $\psi_e(\alpha) = \lVert x_\alpha - \bar x_\alpha\rVert$ the propagated noise. Assume $x^\dagger$ lies in the span of the $v_i$ (the minimum norm solution). Then

$$d_j \le \varphi(\alpha_j) + \psi_e(\alpha_{j+1}).$$

*Proof.* Write $\xi_i = \langle x^\dagger, v_i\rangle$ and $\epsilon_i = \langle u_i, e\rangle$, so $b_i = s_i\xi_i + \epsilon_i$. The coefficient of $\bar x_\alpha - x^\dagger$ on $v_i$ is $-\alpha\xi_i/(s_i^2 + \alpha)$, and that of $x_\alpha - \bar x_\alpha$ is $s_i\epsilon_i/(s_i^2 + \alpha)$. With $\beta = \alpha_{j+1} < \alpha = \alpha_j$, the coefficient of $x_\beta - x_\alpha$ is the sum of

$$\Big(\frac{\alpha}{s_i^2 + \alpha} - \frac{\beta}{s_i^2 + \beta}\Big)\xi_i \quad\text{and}\quad \Big(\frac{s_i}{s_i^2 + \beta} - \frac{s_i}{s_i^2 + \alpha}\Big)\epsilon_i.$$

The first factor lies in $[0, \alpha/(s_i^2 + \alpha)]$, because $\beta/(s_i^2 + \beta) \ge 0$ and the map $\gamma \mapsto \gamma/(s_i^2 + \gamma)$ is increasing. The second factor lies in $[0, s_i/(s_i^2 + \beta)]$. So the first vector has norm at most $\varphi(\alpha)$ and the second at most $\psi_e(\beta)$, and the triangle inequality gives the claim. $\square$

**What Claim 6 means.** By Claim 6, $\min_j d_j \le \min_j(\varphi(\alpha_j) + \psi_e(\alpha_{j+1}))$, so the smallest distance is never larger than an error-like quantity at the best grid point. A small $d_j$ is necessary for $\alpha_j$ to be good. It is not sufficient: $d_j$ can be small by cancellation, or because all filter factors are close to $0$ or $1$ at the two parameters. That is why the rule is a heuristic. Convergence and oracle results need conditions on the noise (Bauer and Reiss 2008 for white noise; Kindermann and Neubauer for deterministic noise), and by the Bakushinskii veto some condition is unavoidable. The near-optimal error in the example of the page is a measurement.
