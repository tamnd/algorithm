---
title: Correctness of the Kaczmarz method
proves: [correctness, termination]
status: full
---

Exact arithmetic throughout. $A \in \mathbb{R}^{m \times n}$ has rows $a_i^T$, and only rows with $a_i \ne 0$ are used (line L5). One step on row $i$ with relaxation $\omega$ maps $x$ to $x' = x + \omega \frac{b_i - a_i^T x}{\|a_i\|^2} a_i$.

**Lemma 1 (projection).** For $\omega = 1$, $a_i^T x' = b_i$, and $x'$ is the point of the hyperplane $H_i = \{ y : a_i^T y = b_i \}$ nearest to $x$.

*Proof.* $a_i^T x' = a_i^T x + (b_i - a_i^T x) = b_i$. For any $y \in H_i$, $x - x' = -\frac{b_i - a_i^T x}{\|a_i\|^2} a_i$ is parallel to $a_i$ and $x' - y$ is orthogonal to $a_i$ (both lie in $H_i$), so $\|x - y\|^2 = \|x - x'\|^2 + \|x' - y\|^2 \ge \|x - x'\|^2$. $\square$

**Theorem 2 (error identity).** Let $x^\ast$ satisfy $a_i^T x^\ast = b_i$, $e = x - x^\ast$, $e' = x' - x^\ast$ and $\rho = b_i - a_i^T x$. Then $\|e'\|^2 = \|e\|^2 - \omega(2 - \omega)\rho^2/\|a_i\|^2$.

*Proof.* $\rho = a_i^T (x^\ast - x) = -a_i^T e$, and $e' = e + \omega \rho\, a_i / \|a_i\|^2$. Expanding, $\|e'\|^2 = \|e\|^2 + 2\omega\rho\, a_i^T e/\|a_i\|^2 + \omega^2 \rho^2/\|a_i\|^2 = \|e\|^2 - 2\omega \rho^2/\|a_i\|^2 + \omega^2\rho^2/\|a_i\|^2$. $\square$

So if $A x = b$ is consistent and $0 < \omega < 2$, the distance to every solution is nonincreasing, and strictly decreasing whenever the chosen equation is violated.

**Lemma 3 (invariant subspace).** Every iterate lies in $x_0 + \operatorname{range}(A^T)$.

*Proof.* Each step adds a multiple of a row $a_i$, which lies in $\operatorname{range}(A^T)$. $\square$

Let $\bar x = A^+ b + (I - A^+ A) x_0$. If $A x = b$ is consistent, $\bar x$ is a solution, and $\bar x - x_0 = A^+(b - A x_0) \in \operatorname{range}(A^T)$. Since $\operatorname{range}(A^T) \perp \ker A$, for any solution $y = \bar x + w$, $w \in \ker A$, $\|y - x_0\|^2 = \|\bar x - x_0\|^2 + \|w\|^2$, so $\bar x$ is the solution nearest $x_0$. By Lemma 3, $e_k = x_k - \bar x \in \operatorname{range}(A^T)$ for all $k$.

**Theorem 4 (cyclic convergence).** If $A x = b$ is consistent and $0 < \omega < 2$, the cyclic iterates converge to $\bar x$.

*Proof.* Write one cyclic sweep on the error as $e \mapsto Q e$ with $Q = P_m \cdots P_1$, $P_i = I - \omega a_i a_i^T/\|a_i\|^2$ (identity for zero rows); this holds because $b_i = a_i^T \bar x$. Each $P_i$ is symmetric with eigenvalues $1$ (on $a_i^\perp$) and $1 - \omega \in (-1, 1)$, so $\|P_i\|_2 \le 1$, and $\|P_i v\| = \|v\|$ only if $a_i^T v = 0$, in which case $P_i v = v$. The space $S = \operatorname{range}(A^T)$ is invariant under every $P_i$. Let $v \in S$ with $\|Q v\| = \|v\|$. Then every factor preserves the norm, so inductively $a_1^T v = 0$, $P_1 v = v$, $a_2^T v = 0$, and so on: $v \perp a_i$ for all $i$, so $v \in S \cap S^\perp = \{0\}$. Hence $\|Q v\| < \|v\|$ for every nonzero $v$ in $S$, and by compactness of the unit sphere of $S$, $q = \max_{v \in S, \|v\| = 1} \|Q v\| < 1$. So $\|e_{\text{sweep } s}\| \le q^s \|e_0\|$, and the iterates within a sweep are bounded by the norm at the start of the sweep by Theorem 2. $\square$

**Theorem 5 (randomized rate, Strohmer and Vershynin).** Let $A x = b$ be consistent, $\omega = 1$, and let each step choose row $i$ independently with probability $p_i = \|a_i\|^2/\|A\|_F^2$. Then $\mathbb{E}\|x_k - \bar x\|^2 \le (1 - \sigma_{\min}^2/\|A\|_F^2)^k \|x_0 - \bar x\|^2$, where $\sigma_{\min}$ is the smallest nonzero singular value of $A$.

*Proof.* Condition on $e = e_k$. By Theorem 2 with $\omega = 1$ and $\rho = -a_i^T e$, $\mathbb{E}[\|e_{k+1}\|^2 \mid e] = \|e\|^2 - \sum_i p_i (a_i^T e)^2/\|a_i\|^2 = \|e\|^2 - \|A e\|^2/\|A\|_F^2$. Since $e \in \operatorname{range}(A^T)$, which is spanned by the right singular vectors of the nonzero singular values, $\|A e\|^2 \ge \sigma_{\min}^2 \|e\|^2$. So $\mathbb{E}[\|e_{k+1}\|^2 \mid e] \le (1 - \sigma_{\min}^2/\|A\|_F^2)\|e\|^2$; take expectations and induct. $\square$

The factor equals $1 - \kappa^{-2}$ with $\kappa = \|A\|_F/\sigma_{\min} = \|A\|_F \|A^+\|_2$, and it lies in $[0, 1)$ because $\|A\|_F^2 = \sum_j \sigma_j^2 \ge \sigma_{\min}^2$.

**Termination.** Line L2 runs at most $maxit$ sweeps of $m$ steps each, and each step is a constant number of vector operations, so the procedure halts. It returns "converged" only when line L9 has verified $\|b - A x\|_2 \le tol \cdot \|b\|_2$ for the returned $x$; otherwise it returns "maxit". $\blacksquare$
