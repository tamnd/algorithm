---
title: Mirror descent has the bound D(u, x_0) + Σ η_k² G² / (2σ) on its weighted regret
proves: [correctness, convergence-rate]
status: full
---

**Assumptions.**

- $C \subseteq \mathbb{R}^n$ is nonempty, closed and convex, and $f$ is convex on an open set that contains $C$.
- $\lVert\cdot\rVert$ is a norm on $\mathbb{R}^n$ and $\lVert g\rVert_* = \max_{\lVert x\rVert \le 1}\langle g, x\rangle$ is its dual norm.
- The mirror map $\psi$ is differentiable on an open set $\Omega$, and it is $\sigma$-strongly convex on $C \cap \overline{\Omega}$ with respect to $\lVert\cdot\rVert$: $D_\psi(x, y) \ge \frac{\sigma}{2}\lVert x - y\rVert^2$.
- Each step is well defined and stays in $\Omega$: $x_0 \in C \cap \Omega$, and
$$x_{k+1} = \operatorname*{argmin}_{x \in C}\big\{\eta_k\langle g_k, x\rangle + D_\psi(x, x_k)\big\} \in C \cap \Omega, \qquad g_k \in \partial f(x_k), \qquad \lVert g_k\rVert_* \le G,$$
with steps $\eta_k > 0$.

The form in lines L4 and L5 of the page (a dual step $\nabla\psi(x_k) - \eta_k g_k$, then the Bregman projection onto $C$) gives the same point. Indeed, if $\nabla\psi(y) = \nabla\psi(x_k) - \eta_k g_k$, then $\eta_k\langle g_k, x\rangle + D_\psi(x, x_k)$ and $D_\psi(x, y)$ differ by a term that does not depend on $x$: both equal $\psi(x) - \langle\nabla\psi(x_k) - \eta_k g_k, x\rangle$ plus a constant.

**Lemma 1 (three-point identity).** For $x \in C$ and $y, z \in \Omega$: $D_\psi(x, y) + D_\psi(y, z) - D_\psi(x, z) = \langle\nabla\psi(z) - \nabla\psi(y), x - y\rangle$.

*Proof.* Expand the three divergences; the values of $\psi$ cancel. The gradient terms are $-\langle\nabla\psi(y), x - y\rangle - \langle\nabla\psi(z), y - z\rangle + \langle\nabla\psi(z), x - z\rangle = \langle\nabla\psi(z) - \nabla\psi(y), x - y\rangle$. $\square$

**Lemma 2 (one step).** For each $u \in C$ and each $k$,

$$\eta_k\langle g_k, x_k - u\rangle \le D_\psi(u, x_k) - D_\psi(u, x_{k+1}) + \frac{\eta_k^2}{2\sigma}\lVert g_k\rVert_*^2.$$

*Proof.* The function $\phi(x) = \eta_k\langle g_k, x\rangle + D_\psi(x, x_k)$ is convex and differentiable at $x_{k+1} \in \Omega$, with gradient $\eta_k g_k + \nabla\psi(x_{k+1}) - \nabla\psi(x_k)$. Since $x_{k+1}$ minimizes $\phi$ over the convex set $C$, the first-order optimality condition gives, for $u \in C$,

$$\eta_k\langle g_k, x_{k+1} - u\rangle \le \langle\nabla\psi(x_{k+1}) - \nabla\psi(x_k), u - x_{k+1}\rangle.$$

Lemma 1 with the points $(u, x_{k+1}, x_k)$ says that the right side equals $D_\psi(u, x_k) - D_\psi(u, x_{k+1}) - D_\psi(x_{k+1}, x_k)$. Add $\eta_k\langle g_k, x_k - x_{k+1}\rangle$ to both sides:

$$\eta_k\langle g_k, x_k - u\rangle \le D_\psi(u, x_k) - D_\psi(u, x_{k+1}) - D_\psi(x_{k+1}, x_k) + \eta_k\langle g_k, x_k - x_{k+1}\rangle.$$

By the definition of the dual norm, $\eta_k\langle g_k, x_k - x_{k+1}\rangle \le \eta_k\lVert g_k\rVert_*\,\lVert x_k - x_{k+1}\rVert$. By strong convexity, $D_\psi(x_{k+1}, x_k) \ge \frac{\sigma}{2}\lVert x_{k+1} - x_k\rVert^2$. For every real $s$, $\eta_k\lVert g_k\rVert_* s - \frac{\sigma}{2}s^2 \le \frac{\eta_k^2\lVert g_k\rVert_*^2}{2\sigma}$, the maximum of a concave quadratic. Use it with $s = \lVert x_k - x_{k+1}\rVert$. $\square$

**Theorem.** For each $u \in C$ and each $K \ge 1$,

$$\sum_{k=0}^{K-1}\eta_k\big(f(x_k) - f(u)\big) \le D_\psi(u, x_0) + \frac{G^2}{2\sigma}\sum_{k=0}^{K-1}\eta_k^2.$$

So the weighted average $\bar{x}_K = \sum_k \eta_k x_k / \sum_k \eta_k$ and the best iterate both satisfy

$$f(\bar{x}_K) - f(u) \le \frac{D_\psi(u, x_0) + \frac{G^2}{2\sigma}\sum_k\eta_k^2}{\sum_k\eta_k}, \qquad \min_{k<K}f(x_k) - f(u) \le \frac{D_\psi(u, x_0) + \frac{G^2}{2\sigma}\sum_k\eta_k^2}{\sum_k\eta_k}.$$

*Proof.* By the subgradient inequality, $f(x_k) - f(u) \le \langle g_k, x_k - u\rangle$. Multiply by $\eta_k > 0$, use Lemma 2 and $\lVert g_k\rVert_* \le G$, and sum over $k < K$. The divergence terms telescope to $D_\psi(u, x_0) - D_\psi(u, x_K) \le D_\psi(u, x_0)$. For the average, convexity of $f$ (Jensen's inequality) gives $f(\bar{x}_K) \le \sum_k\eta_k f(x_k)/\sum_k\eta_k$. For the best iterate, $\min_k f(x_k) \le \sum_k\eta_k f(x_k)/\sum_k\eta_k$. Divide the summed bound by $\sum_k\eta_k$. $\blacksquare$

**Corollary 1 (constant step).** Let $u = x^*$ be a minimizer and $D \ge D_\psi(x^*, x_0)$. The constant step $\eta = \sqrt{2\sigma D/(G^2K)}$ gives

$$f(\bar{x}_K) - f^* \le G\sqrt{\frac{2D}{\sigma K}}.$$

*Proof.* The bound of the theorem is $\frac{D}{K\eta} + \frac{\eta G^2}{2\sigma}$. With this $\eta$, both terms equal $G\sqrt{D/(2\sigma K)}$. $\square$

**Corollary 2 (entropy on the simplex).** Let $C = \Delta_n = \{x \ge 0, \sum_i x_i = 1\}$, $\psi(x) = \sum_i x_i\log x_i$, $x_0 = (1/n, \dots, 1/n)$, and $\lVert g_k\rVert_\infty \le G$. Then the step is $x_{k+1, i} = x_{k,i}e^{-\eta_k g_{k,i}}/Z_k$, where $Z_k$ makes the entries sum to $1$, and the constant step $\eta = \sqrt{2\log n/(G^2K)}$ gives $f(\bar{x}_K) - f^* \le G\sqrt{2\log n/K}$.

*Proof.* Three facts are needed.

1. *The step.* On the simplex, $D_\psi(x, x_k) = \sum_i x_i\log(x_i/x_{k,i})$. Minimize $\eta\langle g, x\rangle + D_\psi(x, x_k)$ subject to $\sum_i x_i = 1$. Since the derivative of $x_i\log x_i$ goes to $-\infty$ as $x_i \to 0$, the minimizer has $x_i > 0$, and the Lagrange condition is $\eta g_i + \log(x_i/x_{k,i}) + 1 + \lambda = 0$. So $x_i = x_{k,i}e^{-\eta g_i}e^{-1-\lambda}$, and the constraint fixes the factor. All iterates are positive, so they stay in $\Omega = \mathbb{R}^n_{>0}$.
2. *Strong convexity.* For $p, q$ in the relative interior of the simplex, $D_\psi(p, q) = \sum_i p_i\log(p_i/q_i) \ge \frac{1}{2}\lVert p - q\rVert_1^2$ (Pinsker's inequality), so $\sigma = 1$ for the norm $\lVert\cdot\rVert_1$, whose dual is $\lVert\cdot\rVert_\infty$. By continuity in $p$ the inequality extends to $p$ on the boundary.
3. *The initial divergence.* $D_\psi(u, x_0) = \sum_i u_i\log(nu_i) = \log n + \sum_i u_i\log u_i \le \log n$, because the entropy $-\sum_i u_i\log u_i$ is nonnegative.

Corollary 1 with $\sigma = 1$ and $D = \log n$ gives the claim. $\square$

**Remarks.** For $\psi = \frac{1}{2}\lVert x\rVert_2^2$, $D_\psi(x, y) = \frac{1}{2}\lVert x - y\rVert_2^2$, $\sigma = 1$, and the step is the projected subgradient step. Corollary 1 then gives $GR/\sqrt{K}$ with $R = \lVert x_0 - x^*\rVert_2$ and $G$ a bound on $\lVert g\rVert_2$. On the simplex with $\lVert g\rVert_\infty \le G_\infty$, the Euclidean bound has $\lVert g\rVert_2 \le \sqrt{n}\,G_\infty$, which is why the entropy is better by a factor of order $\sqrt{n/\log n}$.
