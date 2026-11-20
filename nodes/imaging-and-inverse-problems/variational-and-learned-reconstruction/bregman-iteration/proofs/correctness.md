---
title: Bregman iteration has a nonincreasing residual, an O(1/K) bound on the squared residual, a decreasing Bregman distance before the discrepancy stop, and an exact fit that minimizes R
proves: [correctness, convergence-rate, termination]
status: full
---

**Setting.** $A : \mathbb{R}^n \to \mathbb{R}^m$ is linear, $y \in \mathbb{R}^m$ is the data (exact or noisy), $\lambda > 0$, and $R : \mathbb{R}^n \to [0, \infty]$ is convex with $R(0) = 0$. We assume each inner problem $\min_x \tfrac12\|Ax - d\|^2 + \lambda R(x)$ has a minimizer and the subdifferential sum rule holds for it (true for example when $R$ is finite everywhere). The iteration is $y^0 = y$ and, for $k \ge 0$,

$$x^{k+1} \in \operatorname*{argmin}_x \tfrac12\|Ax - y^k\|^2 + \lambda R(x),\qquad y^{k+1} = y^k + (y - Ax^{k+1}).$$

Put $x^0 = 0$ and $p^k = A^\top(y^k - y)/\lambda$ for $k \ge 0$, so $p^0 = 0$. For $p \in \partial R(z)$ the Bregman distance is $D^p(x, z) = R(x) - R(z) - \langle p, x - z\rangle \ge 0$. Write $D_k(x) = D^{p^k}(x, x^k)$.

**Lemma 1 (subgradients).** $p^k \in \partial R(x^k)$ for all $k \ge 0$.

*Proof.* For $k = 0$: $p^0 = 0$ and $R(x) \ge 0 = R(0)$, so $0 \in \partial R(0)$. For $k \ge 0$ the optimality condition of the inner problem is $0 \in A^\top(Ax^{k+1} - y^k) + \lambda\partial R(x^{k+1})$, so $A^\top(y^k - Ax^{k+1})/\lambda \in \partial R(x^{k+1})$. By the update, $y^k - Ax^{k+1} = y^{k+1} - y$, so this vector is $p^{k+1}$. $\square$

**Lemma 2 (Bregman form).** For $k \ge 0$, $x^{k+1}$ minimizes $\Phi_k(x) = \tfrac12\|Ax - y\|^2 + \lambda D_k(x)$.

*Proof.* $\tfrac12\|Ax - y^k\|^2 = \tfrac12\|Ax - y\|^2 - \langle Ax, y^k - y\rangle + c_1 = \tfrac12\|Ax - y\|^2 - \lambda\langle p^k, x\rangle + c_1$, and $\lambda D_k(x) = \lambda R(x) - \lambda\langle p^k, x\rangle + c_2$, with $c_1, c_2$ independent of $x$. So the two objectives differ by a constant. $\square$

**Theorem 1 (monotone residual).** $\tfrac12\|Ax^{k+1} - y\|^2 + \lambda D_k(x^{k+1}) \le \tfrac12\|Ax^k - y\|^2$ for $k \ge 0$. In particular $\|Ax^{k+1} - y\| \le \|Ax^k - y\|$.

*Proof.* $\Phi_k(x^{k+1}) \le \Phi_k(x^k)$ by Lemma 2, and $D_k(x^k) = 0$. $\square$

**Lemma 3 (three-point identity).** For every $\tilde x$ and $k \ge 1$,

$$D_k(\tilde x) - D_{k-1}(\tilde x) + D_{k-1}(x^k) = \langle p^k - p^{k-1}, x^k - \tilde x\rangle = \tfrac1\lambda\langle y - Ax^k, Ax^k - A\tilde x\rangle.$$

*Proof.* Expand the three distances. The values $R(\tilde x)$, $R(x^k)$ and $R(x^{k-1})$ cancel, and what is left is $-\langle p^k, \tilde x - x^k\rangle + \langle p^{k-1}, \tilde x - x^{k-1}\rangle - \langle p^{k-1}, x^k - x^{k-1}\rangle = \langle p^k - p^{k-1}, x^k - \tilde x\rangle$. Finally $p^k - p^{k-1} = A^\top(y^k - y^{k-1})/\lambda = A^\top(y - Ax^k)/\lambda$. $\square$

**Lemma 4 (one step against any point).** For every $\tilde x$ and $k \ge 1$,

$$\lambda\big(D_k(\tilde x) - D_{k-1}(\tilde x)\big) + \lambda D_{k-1}(x^k) \le \tfrac12\|A\tilde x - y\|^2 - \tfrac12\|Ax^k - y\|^2.$$

*Proof.* Let $r = y - Ax^k$ and $s = y - A\tilde x$. Then $Ax^k - A\tilde x = s - r$, and $\langle r, s - r\rangle = \langle r, s\rangle - \|r\|^2 \le \tfrac12\|s\|^2 + \tfrac12\|r\|^2 - \|r\|^2$. Multiply Lemma 3 by $\lambda$. $\square$

**Theorem 2 (rate).** For every $\tilde x$ with $R(\tilde x) < \infty$ and every $K \ge 1$,

$$\tfrac12\|Ax^K - y\|^2 \le \tfrac12\|A\tilde x - y\|^2 + \frac{\lambda R(\tilde x)}{K}.$$

*Proof.* Sum Lemma 4 over $k = 1, \dots, K$ and drop $\lambda D_{k-1}(x^k) \ge 0$ and $\lambda D_K(\tilde x) \ge 0$: $\sum_{k=1}^K \tfrac12\|Ax^k - y\|^2 \le K\cdot\tfrac12\|A\tilde x - y\|^2 + \lambda D_0(\tilde x)$. Here $D_0(\tilde x) = R(\tilde x) - R(0) - 0 = R(\tilde x)$. By Theorem 1 each term of the sum is at least $\tfrac12\|Ax^K - y\|^2$. Divide by $K$. $\square$

With exact data $y = Ax^\dagger$ and $\tilde x = x^\dagger$ this gives $\|Ax^K - y\|^2 \le 2\lambda R(x^\dagger)/K$.

**Theorem 3 (noisy data).** Let $\|Ax^\dagger - y\| \le \delta$ and $R(x^\dagger) < \infty$. If $\|Ax^k - y\| > \delta$ for some $k \ge 1$, then $D_k(x^\dagger) < D_{k-1}(x^\dagger)$. So the Bregman distance to $x^\dagger$ strictly decreases at every step before the first $k$ with $\|Ax^k - y\| \le \delta$, and for $\tau \ge 1$ the stop rule "first $k$ with $\|Ax^k - y\| \le \tau\delta$" is reached at an index $k_*$ with $D_k(x^\dagger)$ strictly decreasing for $k < k_*$.

*Proof.* Lemma 4 with $\tilde x = x^\dagger$ gives $\lambda(D_k(x^\dagger) - D_{k-1}(x^\dagger)) \le \tfrac12\delta^2 - \tfrac12\|Ax^k - y\|^2 < 0$. For the second claim: before the stop, $\|Ax^k - y\| > \tau\delta \ge \delta$. $\square$

**Theorem 4 (termination of the stop rule).** If $\tau > 1$ and $\|Ax^\dagger - y\| \le \delta$ with $\delta > 0$, the stop rule is reached after at most $K = \lceil 2\lambda R(x^\dagger)/((\tau^2 - 1)\delta^2)\rceil + 1$ steps.

*Proof.* By Theorem 2 with $\tilde x = x^\dagger$, $\|Ax^K - y\|^2 \le \delta^2 + 2\lambda R(x^\dagger)/K$, and this is at most $\tau^2\delta^2$ once $K \ge 2\lambda R(x^\dagger)/((\tau^2 - 1)\delta^2)$. $\square$

**Theorem 5 (exact fit).** If $Ax^k = y$ for some $k \ge 1$, then $x^k$ minimizes $R$ over $\{x : Ax = y\}$.

*Proof.* By Lemma 1, $p^k = A^\top w \in \partial R(x^k)$ with $w = (y^k - y)/\lambda$. For any $x$ with $Ax = y$: $R(x) \ge R(x^k) + \langle A^\top w, x - x^k\rangle = R(x^k) + \langle w, Ax - Ax^k\rangle = R(x^k)$. $\square$

**Remark (augmented Lagrangian).** With $\mu^k = y^k - y$, the inner problem is $\min_x \lambda R(x) + \langle \mu^k, y - Ax\rangle + \tfrac12\|Ax - y\|^2$ up to a constant, and the update is $\mu^{k+1} = \mu^k + (y - Ax^{k+1})$. This is the method of multipliers with penalty 1 for $\min \lambda R(x)$ subject to $Ax = y$. The finite termination for $R = \|\cdot\|_1$ (Yin, Osher, Goldfarb and Darbon 2008) is not proved here.
