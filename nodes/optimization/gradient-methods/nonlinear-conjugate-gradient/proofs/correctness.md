---
title: Nonlinear conjugate gradient is linear conjugate gradient on quadratics, and Fletcher-Reeves descends and converges under strong Wolfe steps
proves: [correctness, termination]
status: full
---

**Setting.** NONLINEAR-CG produces $x_{k+1} = x_k + \alpha_kd_k$ with $g_k = \nabla f(x_k)$, $d_0 = -g_0$ and $d_{k+1} = -g_{k+1} + \beta_{k+1}d_k$ (lines L4 to L6), unless line L7 replaces $d_{k+1}$ by $-g_{k+1}$. The rules are $\beta^{FR}_{k+1} = \|g_{k+1}\|^2/\|g_k\|^2$ and $\beta^{PR+}_{k+1} = \max(0, \beta^{PR}_{k+1})$ with $\beta^{PR}_{k+1} = g_{k+1}^\top(g_{k+1} - g_k)/\|g_k\|^2$.

**Claim 1 (descent and termination).** Every $d_k$ satisfies $g_k^\top d_k < 0$, every step satisfies the strong Wolfe conditions, $f(x_{k+1}) < f(x_k)$, and the method stops after at most $K$ iterations.

*Proof.* $d_0 = -g_0$ and $g_0 \ne 0$ inside the loop, so $g_0^\top d_0 = -\|g_0\|^2 < 0$. After line L7, either $g_{k+1}^\top d_{k+1} < 0$ or $d_{k+1} = -g_{k+1}$, and then $g_{k+1}^\top d_{k+1} = -\|g_{k+1}\|^2 < 0$ when the loop continues. The line search returns a step only after it has checked both strong Wolfe tests at that step, and it stops the method after a fixed number of trial points otherwise. For a continuously differentiable $f$ with $\varphi(\alpha) = f(x_k + \alpha d_k)$ bounded below, strong Wolfe steps exist and bracketing and zoom find one ([Wolfe conditions](/wolfe-conditions/)). The Armijo test gives $f(x_{k+1}) \le f(x_k) + c_1\alpha_kg_k^\top d_k < f(x_k)$. The loop of line L2 runs at most $K$ times. $\square$

**Claim 2 (quadratics with exact steps).** Let $f(x) = \frac12x^\top Ax - b^\top x$ with $A$ symmetric positive definite, so $g_{k+1} = g_k + \alpha_kAd_k$, and let $\alpha_k$ minimize $f(x_k + \alpha d_k)$, so $g_{k+1}^\top d_k = 0$. As long as $g_0, \dots, g_k$ are nonzero:

- (a) $g_i^\top g_j = 0$ and $d_i^\top Ad_j = 0$ for $i < j \le k$, and $g_j^\top d_j = -\|g_j\|^2$ for $j \le k$;
- (b) the FR, PR and PR+ values of $\beta_j$ are equal for $j \le k$, and line L7 does not act;
- (c) the iterates are those of linear conjugate gradient;
- (d) $g_k = 0$ for some $k \le m$, where $m$ is the number of distinct eigenvalues of $A$.

*Proof.* Induction on $k$. For $k = 0$, (a) says $g_0^\top d_0 = -\|g_0\|^2$, which holds. Assume (a) for $k$ and $g_{k+1} \ne 0$. The exact step is $\alpha_k = -g_k^\top d_k/(d_k^\top Ad_k) = \|g_k\|^2/(d_k^\top Ad_k) > 0$.

First, $g_{k+1}^\top d_i = 0$ for all $i \le k$. For $i = k$ this is the exact step. For $i < k$, $g_{i+1}^\top d_i = 0$ by the exact step at $i$, and for $i < j \le k$, $g_{j+1}^\top d_i = g_j^\top d_i + \alpha_jd_j^\top Ad_i = g_j^\top d_i$ by conjugacy, so $g_{k+1}^\top d_i = g_{i+1}^\top d_i = 0$.

Second, $g_{k+1}^\top g_i = 0$ for $i \le k$, because $g_0 = -d_0$ and $g_i = -d_i + \beta_id_{i-1}$ for $i \ge 1$ (line L7 did not act, by the induction hypothesis), and $g_{k+1}$ is orthogonal to every $d_i$ with $i \le k$.

Third, since $g_{k+1}^\top g_k = 0$, $\beta^{PR}_{k+1} = \|g_{k+1}\|^2/\|g_k\|^2 = \beta^{FR}_{k+1} > 0$, so all three rules agree. Write $\beta = \beta_{k+1}$. Then $g_{k+1}^\top d_{k+1} = -\|g_{k+1}\|^2 + \beta g_{k+1}^\top d_k = -\|g_{k+1}\|^2 < 0$, so line L7 does not act.

Fourth, conjugacy. For $i \le k$, $Ad_i = (g_{i+1} - g_i)/\alpha_i$, so
$$d_{k+1}^\top Ad_i = -\frac{g_{k+1}^\top(g_{i+1} - g_i)}{\alpha_i} + \beta d_k^\top Ad_i.$$
For $i < k$ both terms are $0$ by the second step and the hypothesis. For $i = k$ it is $-\|g_{k+1}\|^2/\alpha_k + \beta\|g_k\|^2/\alpha_k = 0$, because $\alpha_kd_k^\top Ad_k = \|g_k\|^2$ and $\beta = \|g_{k+1}\|^2/\|g_k\|^2$. This proves (a) and (b) for $k + 1$.

For (c), linear conjugate gradient sets $r_0 = Ax_0 - b = g_0$, $p_0 = -r_0$, $\alpha_k = \|r_k\|^2/(p_k^\top Ap_k)$, $r_{k+1} = r_k + \alpha_kAp_k$ and $p_{k+1} = -r_{k+1} + (\|r_{k+1}\|^2/\|r_k\|^2)p_k$. These are the formulas above with $r_k = g_k$ and $p_k = d_k$, so the two sequences are the same.

For (d), let $\mathcal{K}_j = \operatorname{span}\{g_0, Ag_0, \dots, A^{j-1}g_0\}$. By induction $g_j, d_j \in \mathcal{K}_{j+1}$: this holds for $j = 0$, and $g_{j+1} = g_j + \alpha_jAd_j \in \mathcal{K}_{j+2}$, $d_{j+1} = -g_{j+1} + \beta d_j \in \mathcal{K}_{j+2}$. Write $g_0 = v_1 + \dots + v_m$ with $v_i$ in the eigenspace of the eigenvalue $\lambda_i$. Then $A^tg_0 = \sum_i\lambda_i^tv_i$, so every $\mathcal{K}_j$ lies in $\operatorname{span}\{v_1, \dots, v_m\}$, which has dimension at most $m$. The nonzero gradients are mutually orthogonal vectors in this space, so there are at most $m$ of them, and $g_k = 0$ for some $k \le m$. $\square$

**Claim 3 (Fletcher-Reeves descent).** Let every step satisfy the strong Wolfe conditions with $0 < c_1 < c_2 < \frac12$ and use the FR rule. Then for every $k$ with $g_k \ne 0$,
$$-\frac{1}{1 - c_2} \le \frac{g_k^\top d_k}{\|g_k\|^2} \le \frac{2c_2 - 1}{1 - c_2},$$
the right side is negative, and line L7 never acts.

*Proof.* Induction on $k$. For $k = 0$ the ratio is $-1$, and $-\frac{1}{1 - c_2} \le -1 \le \frac{2c_2 - 1}{1 - c_2}$ because $c_2 \ge 0$ and $c_2 < 1$. Assume the bounds for $k$; in particular $g_k^\top d_k < 0$, so the strong Wolfe step exists. Before line L7, $d_{k+1} = -g_{k+1} + \beta^{FR}_{k+1}d_k$ and
$$\frac{g_{k+1}^\top d_{k+1}}{\|g_{k+1}\|^2} = -1 + \frac{g_{k+1}^\top d_k}{\|g_k\|^2}.$$
The strong Wolfe curvature test gives $|g_{k+1}^\top d_k| \le -c_2g_k^\top d_k$, so
$$-1 + c_2\frac{g_k^\top d_k}{\|g_k\|^2} \le \frac{g_{k+1}^\top d_{k+1}}{\|g_{k+1}\|^2} \le -1 - c_2\frac{g_k^\top d_k}{\|g_k\|^2}.$$
By the hypothesis $g_k^\top d_k/\|g_k\|^2 \ge -1/(1 - c_2)$, the left side is at least $-1 - c_2/(1 - c_2) = -1/(1 - c_2)$ and the right side is at most $-1 + c_2/(1 - c_2) = (2c_2 - 1)/(1 - c_2)$. Since $c_2 < \frac12$, this upper bound is negative, so $g_{k+1}^\top d_{k+1} < 0$ and line L7 does not act. $\square$

**Claim 4 (Fletcher-Reeves global convergence).** Under the conditions of claim 3, let $f$ be bounded below and let $\nabla f$ be Lipschitz continuous on an open set that contains $\{x : f(x) \le f(x_0)\}$. Run FR with $K = \infty$ and $\varepsilon = 0$. Then either $g_k = 0$ for some $k$, or $\liminf_{k\to\infty}\|g_k\| = 0$.

*Proof.* Assume $g_k \ne 0$ for all $k$. Let $\cos\theta_k = -g_k^\top d_k/(\|g_k\|\|d_k\|)$. The iterates stay in the level set because $f$ decreases (claim 1), and the steps satisfy the Wolfe conditions, so Zoutendijk's theorem ([Wolfe conditions](/wolfe-conditions/)) gives $\sum_k\cos^2\theta_k\|g_k\|^2 < \infty$. By claim 3, $\cos\theta_k \ge \frac{1 - 2c_2}{1 - c_2}\cdot\frac{\|g_k\|}{\|d_k\|}$, so
$$\sum_k\frac{\|g_k\|^4}{\|d_k\|^2} < \infty. \qquad (1)$$
Now bound $\|d_k\|$. For $k \ge 1$, $\|d_k\|^2 \le \|g_k\|^2 + 2\beta_k|g_k^\top d_{k-1}| + \beta_k^2\|d_{k-1}\|^2$. By the curvature test and claim 3, $|g_k^\top d_{k-1}| \le -c_2g_{k-1}^\top d_{k-1} \le \frac{c_2}{1 - c_2}\|g_{k-1}\|^2$, and $\beta_k\|g_{k-1}\|^2 = \|g_k\|^2$. With $c_3 = \frac{1 + c_2}{1 - c_2} \ge 1$,
$$\|d_k\|^2 \le c_3\|g_k\|^2 + \beta_k^2\|d_{k-1}\|^2.$$
Divide by $\|g_k\|^4$ and use $\beta_k^2/\|g_k\|^4 = 1/\|g_{k-1}\|^4$:
$$\frac{\|d_k\|^2}{\|g_k\|^4} \le \frac{c_3}{\|g_k\|^2} + \frac{\|d_{k-1}\|^2}{\|g_{k-1}\|^4}.$$
Since $\|d_0\|^2/\|g_0\|^4 = 1/\|g_0\|^2$, summing gives $\|d_k\|^2/\|g_k\|^4 \le c_3\sum_{j=0}^k\|g_j\|^{-2}$. If $\liminf\|g_k\| > 0$, there is $\gamma > 0$ with $\|g_j\| \ge \gamma$ for all $j$, so $\|g_k\|^4/\|d_k\|^2 \ge \gamma^2/(c_3(k + 1))$. The harmonic series diverges, which contradicts (1). So $\liminf\|g_k\| = 0$. $\square$

**Remark (floating point).** In floating point the exact step on a quadratic leaves $g_{k+1}^\top d_k$ at rounding size, so the orthogonality and conjugacy of claim 2 hold only up to rounding, and the gradient after $m$ steps is small relative to $\|g_0\|$ rather than zero. On ill-conditioned problems the loss of conjugacy grows, and more than $m$ steps can be needed.
