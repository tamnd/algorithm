---
title: SGD converges at the rate O(1/k) for strongly convex smooth functions with bounded variance, O(1/√K) for convex functions, and O(1/√K) in squared gradient norm for smooth nonconvex functions
proves: [correctness, convergence-rate]
status: full
---

**Setting.** $F : \mathbb{R}^n \to \mathbb{R}$, and the method is $x_{k+1} = x_k - \eta_kG_k$ (Parts 1 and 3) or $x_{k+1} = P_X(x_k - \eta_kG_k)$ (Part 2). Let $\mathcal{F}_k$ be the history up to $x_k$. The oracle is unbiased: $\mathbb{E}[G_k \mid \mathcal{F}_k] = \nabla F(x_k)$ (or a subgradient in Part 2). The steps $\eta_k$ are fixed in advance. Write $a_k = \mathbb{E}\lVert x_k - x^*\rVert^2$.

**Part 1. Strongly convex and smooth.**

Assume that $F$ is $\mu$-strongly convex with an $L$-Lipschitz gradient, $x^*$ is its minimizer, $\kappa = L/\mu$, and $\mathbb{E}[\lVert G_k - \nabla F(x_k)\rVert^2 \mid \mathcal{F}_k] \le \sigma^2$.

**Lemma 1.** If $\eta_k \le 1/L$, then $a_{k+1} \le (1 - \mu\eta_k)a_k + \eta_k^2\sigma^2$.

*Proof.* Write $x = x_k$, $\eta = \eta_k$ and $g = \nabla F(x)$. Expand the square and take $\mathbb{E}[\cdot \mid \mathcal{F}_k]$:

$$\mathbb{E}[\lVert x_{k+1} - x^*\rVert^2 \mid \mathcal{F}_k] = \lVert x - x^*\rVert^2 - 2\eta\langle g, x - x^*\rangle + \eta^2\,\mathbb{E}[\lVert G_k\rVert^2 \mid \mathcal{F}_k].$$

Since $G_k$ is unbiased, $\mathbb{E}[\lVert G_k\rVert^2 \mid \mathcal{F}_k] = \lVert g\rVert^2 + \mathbb{E}[\lVert G_k - g\rVert^2 \mid \mathcal{F}_k] \le \lVert g\rVert^2 + \sigma^2$. Strong convexity at $x$, evaluated at $x^*$, gives $\langle g, x - x^*\rangle \ge F(x) - F^* + \frac{\mu}{2}\lVert x - x^*\rVert^2$. Smoothness gives $\lVert g\rVert^2 \le 2L(F(x) - F^*)$: apply the descent lemma at $x$ with the step $1/L$ and use $F(x - g/L) \ge F^*$. Therefore

$$-2\eta\langle g, x - x^*\rangle + \eta^2\lVert g\rVert^2 \le -\mu\eta\lVert x - x^*\rVert^2 - 2\eta(1 - L\eta)(F(x) - F^*) \le -\mu\eta\lVert x - x^*\rVert^2,$$

because $L\eta \le 1$ and $F(x) \ge F^*$. Take the full expectation. $\square$

**Theorem 1 (diminishing steps).** Let $k_0 \ge 2\kappa$ and $\eta_k = \frac{2}{\mu(k + k_0)}$. Then for each $k \ge 0$

$$\mathbb{E}\lVert x_k - x^*\rVert^2 \le \frac{\nu}{k + k_0}, \qquad \nu = \max\Big(k_0\lVert x_0 - x^*\rVert^2,\ \frac{4\sigma^2}{\mu^2}\Big),$$

and $\mathbb{E}F(x_k) - F^* \le \frac{L}{2}\cdot\frac{\nu}{k + k_0}$.

*Proof.* The steps decrease, and $\eta_0 = 2/(\mu k_0) \le 1/L$, so Lemma 1 applies at each step. The claim holds for $k = 0$ by the choice of $\nu$. Assume it for $k$ and write $t = k + k_0 \ge 2$. Then $\mu\eta_k = 2/t$ and

$$a_{k+1} \le \Big(1 - \frac{2}{t}\Big)\frac{\nu}{t} + \frac{4\sigma^2}{\mu^2t^2} \le \frac{(t - 2)\nu}{t^2} + \frac{\nu}{t^2} = \frac{(t - 1)\nu}{t^2} \le \frac{\nu}{t + 1},$$

since $(t - 1)(t + 1) \le t^2$. For the function value, smoothness and $\nabla F(x^*) = 0$ give $F(x) - F^* \le \frac{L}{2}\lVert x - x^*\rVert^2$. $\blacksquare$

**Theorem 2 (constant step).** If $\eta_k = \eta \le 1/L$ for all $k$, then

$$\mathbb{E}\lVert x_k - x^*\rVert^2 \le (1 - \mu\eta)^k\lVert x_0 - x^*\rVert^2 + \frac{\eta\sigma^2}{\mu}.$$

*Proof.* Unroll Lemma 1: $a_k \le (1 - \mu\eta)^ka_0 + \eta^2\sigma^2\sum_{j<k}(1 - \mu\eta)^j \le (1 - \mu\eta)^ka_0 + \eta^2\sigma^2/(\mu\eta)$. $\blacksquare$

The second term does not go to zero. For $F(x) = \frac{\mu}{2}x^2$ with additive noise of variance $\sigma^2$, the recursion holds with equality in the form $a_{k+1} = (1 - \mu\eta)^2a_k + \eta^2\sigma^2$, whose limit is $\eta\sigma^2/(\mu(2 - \mu\eta))$, at least half the bound. So a constant step converges linearly only to a ball of radius of order $\sqrt{\eta}\,\sigma$.

**Part 2. Convex, possibly nonsmooth, with bounded second moment.**

**Theorem 3.** Let $F$ be convex on a closed convex set $X$, with a minimizer $x^* \in X$ and $R = \lVert x_0 - x^*\rVert$, $x_0 \in X$. Let $\mathbb{E}[G_k \mid \mathcal{F}_k] \in \partial F(x_k)$ and $\mathbb{E}[\lVert G_k\rVert^2 \mid \mathcal{F}_k] \le G^2$. With the projected step and $\bar{x}_K = \sum_{k<K}\eta_kx_k/\sum_{k<K}\eta_k$,

$$\mathbb{E}F(\bar{x}_K) - F^* \le \frac{R^2 + G^2\sum_{k<K}\eta_k^2}{2\sum_{k<K}\eta_k}.$$

With $\eta_k = R/(G\sqrt{K})$ the bound is $RG/\sqrt{K}$.

*Proof.* Let $g_k = \mathbb{E}[G_k \mid \mathcal{F}_k] \in \partial F(x_k)$. The projection onto $X$ does not increase distances, and $x^* = P_X(x^*)$, so

$$\lVert x_{k+1} - x^*\rVert^2 \le \lVert x_k - x^*\rVert^2 - 2\eta_k\langle G_k, x_k - x^*\rangle + \eta_k^2\lVert G_k\rVert^2.$$

Take $\mathbb{E}[\cdot \mid \mathcal{F}_k]$; the middle term becomes $-2\eta_k\langle g_k, x_k - x^*\rangle \le -2\eta_k(F(x_k) - F^*)$ by the subgradient inequality. Take the full expectation, sum over $k < K$ and drop $a_K \ge 0$: $2\sum_k\eta_k(\mathbb{E}F(x_k) - F^*) \le R^2 + G^2\sum_k\eta_k^2$. By convexity (Jensen's inequality), $F(\bar{x}_K) \le \sum_k\eta_kF(x_k)/\sum_k\eta_k$. For the constant step, the numerator is $2R^2$ and the denominator is $2RK^{1/2}/G$. $\blacksquare$

**Part 3. Smooth nonconvex.**

**Theorem 4.** Let $F$ have an $L$-Lipschitz gradient and $F \ge F_{\inf}$, let $\mathbb{E}[\lVert G_k - \nabla F(x_k)\rVert^2 \mid \mathcal{F}_k] \le \sigma^2$, and let $\eta_k = \eta \le 1/L$. Then, with $\Delta = F(x_0) - F_{\inf}$,

$$\frac{1}{K}\sum_{k<K}\mathbb{E}\lVert\nabla F(x_k)\rVert^2 \le \frac{2\Delta}{\eta K} + L\eta\sigma^2.$$

With $\eta = \min\big(1/L,\ \sqrt{2\Delta/(L\sigma^2K)}\big)$ the right side is at most $\frac{4L\Delta}{K} + 2\sigma\sqrt{\frac{2L\Delta}{K}}$.

*Proof.* The descent lemma gives $F(x_{k+1}) \le F(x_k) - \eta\langle\nabla F(x_k), G_k\rangle + \frac{L\eta^2}{2}\lVert G_k\rVert^2$. Take $\mathbb{E}[\cdot \mid \mathcal{F}_k]$ and use $\mathbb{E}\lVert G_k\rVert^2 \le \lVert\nabla F(x_k)\rVert^2 + \sigma^2$:

$$\mathbb{E}[F(x_{k+1}) \mid \mathcal{F}_k] \le F(x_k) - \eta\Big(1 - \frac{L\eta}{2}\Big)\lVert\nabla F(x_k)\rVert^2 + \frac{L\eta^2\sigma^2}{2} \le F(x_k) - \frac{\eta}{2}\lVert\nabla F(x_k)\rVert^2 + \frac{L\eta^2\sigma^2}{2}.$$

Take the full expectation, sum over $k < K$, and use $\mathbb{E}F(x_K) \ge F_{\inf}$. Divide by $\eta K/2$. If $\eta = \sqrt{2\Delta/(L\sigma^2K)} \le 1/L$, both terms equal $\sigma\sqrt{2L\Delta/K}$. Otherwise $\eta = 1/L$ and $\sigma^2 < 2L\Delta/K$, so the bound is at most $2L\Delta/K + \sigma^2 \le 4L\Delta/K$. $\blacksquare$

**Remarks.** A random iterate chosen uniformly from $x_0, \dots, x_{K-1}$ has $\mathbb{E}\lVert\nabla F\rVert^2$ equal to the left side of Theorem 4, which is the output rule of Ghadimi and Lan (2013). The test file checks Theorem 1 and Theorem 2 on the exact expectation of a quadratic with Gaussian noise, where the per-coordinate recursion of Lemma 1 holds with equality in the form $e_{k+1} = (1 - \eta d_i)^2e_k + \eta^2s^2$, and checks a Monte Carlo average over 400 seeds against it.
