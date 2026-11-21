---
title: Correctness of the Landweber iteration
proves: [correctness, termination]
status: full
---

Exact arithmetic. $A: X \to Y$ is a bounded linear operator between Hilbert spaces with a singular system $(\sigma_j; v_j, u_j)$; for a matrix this is the SVD, with the sums finite. The start is $x_0 = 0$ (line L1), the step is $\omega$ with $0 < \omega < 2/\|A\|^2$, and $x_{k+1} = x_k + \omega A^*(y - A x_k)$ (lines L3 and L5). $P$ is the orthogonal projection onto the closure of the range of $A$, and $x^\dagger = A^\dagger y$ for $y$ in the domain of $A^\dagger$.

**Lemma 1 (filter form).** For every $k \ge 0$,
$$x_k = \sum_j f_k(\sigma_j) \frac{\langle u_j, y\rangle}{\sigma_j} v_j, \qquad f_k(\sigma) = 1 - (1 - \omega\sigma^2)^k,$$
and $y - A x_k = \sum_j (1 - \omega\sigma_j^2)^k \langle u_j, y\rangle u_j + (I - P) y$.

*Proof.* Induction on $k$. Base: $f_0 = 0$, so the formula gives $x_0 = 0$. Step: assume the formula for $x_k$. Then $y - A x_k = (I - P) y + \sum_j (1 - f_k(\sigma_j)) \langle u_j, y\rangle u_j$, since $P y = \sum_j \langle u_j, y\rangle u_j$ and $A v_j = \sigma_j u_j$. Apply $A^*$: $A^*(I - P) y = 0$ because $(I - P)y$ is orthogonal to the range of $A$, and $A^* u_j = \sigma_j v_j$. So
$$x_{k+1} = \sum_j \Big[ f_k(\sigma_j) + \omega\sigma_j^2 (1 - f_k(\sigma_j)) \Big] \frac{\langle u_j, y\rangle}{\sigma_j} v_j.$$
With $1 - f_k = (1 - \omega\sigma^2)^k$, the bracket is $1 - (1 - \omega\sigma^2)^k (1 - \omega\sigma^2) = f_{k+1}(\sigma)$. The residual formula follows from the same computation with $k + 1$ in place of $k$. $\square$

**Lemma 2 (bounds on the filter).** Let $q(\sigma) = 1 - \omega\sigma^2$. For $0 < \sigma \le \|A\|$: (a) $|q(\sigma)| < 1$; (b) if $\omega\|A\|^2 \le 1$, then $0 \le f_k(\sigma) \le 1$ and $f_k(\sigma)/\sigma \le \sqrt{\omega k}$; (c) if $\omega\|A\|^2 \le 1$ and $\nu > 0$, then $(1 - f_k(\sigma))\, \sigma^{2\nu} \le (\nu/(\omega k))^\nu$ for $k \ge 1$.

*Proof.* (a) $0 < \omega\sigma^2 \le \omega\|A\|^2 < 2$, so $-1 < q < 1$. (b) Put $t = \omega\sigma^2 \in (0, 1]$. Then $(1 - t)^k \in [0, 1)$, so $0 \le f_k \le 1$. Bernoulli's inequality $(1 - t)^k \ge 1 - k t$ gives $f_k \le k t$. Hence $f_k \le \min(1, k t) \le \sqrt{k t}$, and $f_k/\sigma \le \sqrt{k t}/\sigma = \sqrt{\omega k}$. (c) $(1 - t)^k \sigma^{2\nu} = \omega^{-\nu} (1 - t)^k t^\nu$. On $[0, 1]$ the function $g(t) = (1 - t)^k t^\nu$ has its maximum where $g'(t) = 0$, that is at $t^* = \nu/(\nu + k)$, with $g(t^*) = (k/(\nu + k))^k (\nu/(\nu + k))^\nu \le (\nu/k)^\nu$. $\square$

**Theorem 1 (exact data).** If $y$ is in the domain of $A^\dagger$, then $x_k \to x^\dagger$ as $k \to \infty$.

*Proof.* By Lemma 1 and the Picard expansion $x^\dagger = \sum_j \langle u_j, y\rangle \sigma_j^{-1} v_j$, the error is $x^\dagger - x_k = \sum_j q(\sigma_j)^k \langle v_j, x^\dagger\rangle v_j$, so $\|x^\dagger - x_k\|^2 = \sum_j q(\sigma_j)^{2k} |\langle v_j, x^\dagger\rangle|^2$. Each term tends to $0$ by Lemma 2(a) and is bounded by $|\langle v_j, x^\dagger\rangle|^2$, a summable sequence. By dominated convergence the sum tends to $0$. $\square$

**Theorem 2 (the residual does not increase).** $\|y - A x_{k+1}\| \le \|y - A x_k\|$ for every $k$ and every $y \in Y$.

*Proof.* By Lemma 1, $\|y - A x_k\|^2 = \sum_j q(\sigma_j)^{2k} |\langle u_j, y\rangle|^2 + \|(I - P)y\|^2$, and $q(\sigma_j)^{2(k+1)} \le q(\sigma_j)^{2k}$ by Lemma 2(a). $\square$

**Theorem 3 (error bound).** Let $\omega\|A\|^2 \le 1$, let $\|y^\delta - y\| \le \delta$ with $y = A x^\dagger$, and let $x_k$ and $x_k^\delta$ be the iterates for $y$ and $y^\delta$. Then $\|x_k^\delta - x_k\| \le \sqrt{\omega k}\,\delta$. If also $x^\dagger = (A^* A)^\nu w$ with $\|w\| \le \rho$ and $\nu > 0$, then for $k \ge 1$
$$\|x_k^\delta - x^\dagger\| \le \Big(\frac{\nu}{\omega k}\Big)^\nu \rho + \sqrt{\omega k}\,\delta.$$

*Proof.* The iterate is linear in the data, so $x_k^\delta - x_k = \sum_j f_k(\sigma_j) \sigma_j^{-1} \langle u_j, y^\delta - y\rangle v_j$. By Lemma 2(b) each coefficient is multiplied by at most $\sqrt{\omega k}$, and by Bessel's inequality $\|x_k^\delta - x_k\| \le \sqrt{\omega k}\, \|y^\delta - y\|$. For the second part, $\langle v_j, x^\dagger\rangle = \sigma_j^{2\nu} \langle v_j, w\rangle$, so by the proof of Theorem 1 and Lemma 2(c), $\|x^\dagger - x_k\|^2 = \sum_j \big(q(\sigma_j)^k \sigma_j^{2\nu}\big)^2 |\langle v_j, w\rangle|^2 \le (\nu/(\omega k))^{2\nu} \rho^2$. The triangle inequality adds the two parts. $\square$

**Corollary (a priori rate).** With $\omega k = (\rho/\delta)^{2/(2\nu+1)}$ (rounded up to an integer $k$), Theorem 3 gives $\|x_k^\delta - x^\dagger\| \le (\nu^\nu + 1 + o(1))\, \rho^{1/(2\nu+1)} \delta^{2\nu/(2\nu+1)}$ as $\delta \to 0$. Substitute: $(\nu/(\omega k))^\nu \rho = \nu^\nu \rho^{1/(2\nu+1)} \delta^{2\nu/(2\nu+1)}$ and $\sqrt{\omega k}\,\delta = \rho^{1/(2\nu+1)} \delta^{2\nu/(2\nu+1)}$; the rounding of $k$ changes the second term by a factor $\sqrt{1 + 1/k} \to 1$. $\square$

**Theorem 4 (termination of the discrepancy rule).** Let $y = A x^\dagger$, $\|y^\delta - y\| \le \delta$ and $\tau > 1$. Then the loop L2 to L5 with the test of line L4 stops after finitely many steps (for $K$ large enough), and the returned $x_k$ satisfies $\|y^\delta - A x_k\| \le \tau\delta$, while every earlier iterate has a residual above $\tau\delta$.

*Proof.* By Lemma 1 for the data $y^\delta$, $\|y^\delta - A x_k\|^2 = \sum_j q(\sigma_j)^{2k} |\langle u_j, y^\delta\rangle|^2 + \|(I - P) y^\delta\|^2$. The sum tends to $0$ by Lemma 2(a) and dominated convergence, as in Theorem 1. Since $y$ is in the range of $A$, $(I - P) y^\delta = (I - P)(y^\delta - y)$, so $\|(I - P) y^\delta\| \le \delta < \tau\delta$. So the residual is below $\tau\delta$ for all large $k$, and the first such $k$ exists. Line L4 tests the residual of each iterate in order of $k$ and returns at the first one that passes, which gives the last two claims. $\square$

The order optimality of the discrepancy rule, an error $O(\delta^{2\nu/(2\nu+1)})$ for every $\nu > 0$ with a stopping index $k_* = O(\delta^{-2/(2\nu+1)})$, is a theorem of Engl, Hanke and Neubauer (Chapter 6). It is not proved here and the code does not rely on it. $\blacksquare$
