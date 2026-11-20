---
title: ISTA decreases the LASSO objective at the rate L R^2 / (2k), its fixed points are the minimizers, and the refit is exact on a correct support
proves: [correctness, termination]
status: full
---

We assume exact arithmetic. Let $A$ be the real $N \times P$ matrix and $y \in \mathbb{R}^N$ of lines L1 and L2, $f(c) = \frac{1}{2} \|A c - y\|^2$, $g(c) = \lambda \|c\|_1$ with $\lambda > 0$, and $F = f + g$. The gradient is $\nabla f(c) = A^{\mathsf T}(A c - y)$. We assume $L \ge \|A\|_2^2$, the largest eigenvalue of $A^{\mathsf T} A$. Write $T(c) = S_{\lambda/L}(c - \nabla f(c) / L)$ for the step of line L4, with $S_\tau$ applied entrywise.

**Lemma 1 (a minimizer exists).** $F$ is convex and has at least one minimizer $c^*$.

*Proof.* $f$ is convex as a convex quadratic, and $g$ is a norm times $\lambda$. $F$ is continuous and $F(c) \ge \lambda \|c\|_1$, so the set $\{c : F(c) \le F(0)\}$ is closed and bounded, and $F$ attains its minimum on it. $\square$

**Lemma 2 (the step is a proximal step).** $T(c)$ is the unique minimizer of $z \mapsto \frac{L}{2} \|z - (c - \nabla f(c)/L)\|^2 + \lambda \|z\|_1$.

*Proof.* The function is a sum over entries of $h_j(z_j) = \frac{L}{2}(z_j - v_j)^2 + \lambda |z_j|$, with $v = c - \nabla f(c)/L$, and each $h_j$ is strictly convex. For $z_j > 0$, $h_j' = L(z_j - v_j) + \lambda$ vanishes at $z_j = v_j - \lambda/L$, which is positive exactly when $v_j > \lambda / L$; the case $z_j < 0$ is symmetric. If $|v_j| \le \lambda/L$, then the one-sided derivatives at 0 are $-L v_j + \lambda \ge 0$ on the right and $-L v_j - \lambda \le 0$ on the left, so $z_j = 0$ is the minimizer. In all cases the minimizer is $S_{\lambda/L}(v_j)$. $\square$

**Lemma 3 (the key inequality).** For every $c$ and $z$, with $c^+ = T(c)$,

$$F(z) - F(c^+) \ge \tfrac{L}{2} \big(\|c^+ - z\|^2 - \|c - z\|^2\big).$$

*Proof.* The optimality condition of Lemma 2 says that $\gamma = -\nabla f(c) - L (c^+ - c)$ is a subgradient of $g$ at $c^+$, so $g(z) \ge g(c^+) + \gamma^{\mathsf T}(z - c^+)$. Convexity of $f$ gives $f(z) \ge f(c) + \nabla f(c)^{\mathsf T}(z - c)$. Since $\nabla f$ is $\|A\|_2^2$-Lipschitz and $L \ge \|A\|_2^2$, the descent lemma gives $f(c^+) \le f(c) + \nabla f(c)^{\mathsf T}(c^+ - c) + \frac{L}{2}\|c^+ - c\|^2$; for this quadratic $f$ it is the identity $f(c^+) = f(c) + \nabla f(c)^{\mathsf T}(c^+ - c) + \frac{1}{2}\|A (c^+ - c)\|^2$ together with $\|A w\|^2 \le \|A\|_2^2 \|w\|^2$. Add the three inequalities:

$$F(z) - F(c^+) \ge (\nabla f(c) + \gamma)^{\mathsf T}(z - c^+) - \tfrac{L}{2}\|c^+ - c\|^2 = -L (c^+ - c)^{\mathsf T}(z - c^+) - \tfrac{L}{2}\|c^+ - c\|^2.$$

Expand $\|c - z\|^2 = \|c^+ - c\|^2 + 2 (c - c^+)^{\mathsf T}(c^+ - z) + \|c^+ - z\|^2$; the right side above is exactly $\frac{L}{2}(\|c^+ - z\|^2 - \|c - z\|^2)$. $\square$

**Lemma 4 (descent).** $F(T(c)) \le F(c) - \frac{L}{2} \|T(c) - c\|^2$. So the objective never increases along the ISTA iterates.

*Proof.* Take $z = c$ in Lemma 3. $\square$

**Lemma 5 (the rate, Beck and Teboulle, Theorem 3.1).** Let $c_0$ be any start, $c_{k+1} = T(c_k)$, and $c^*$ any minimizer. Then for $k \ge 1$, $F(c_k) - F(c^*) \le L \|c_0 - c^*\|^2 / (2k)$.

*Proof.* Take $c = c_j$ and $z = c^*$ in Lemma 3: $F(c^*) - F(c_{j+1}) \ge \frac{L}{2}(\|c_{j+1} - c^*\|^2 - \|c_j - c^*\|^2)$. Sum over $j = 0, \ldots, k-1$; the right side telescopes:

$$k F(c^*) - \sum_{j=1}^{k} F(c_j) \ge \tfrac{L}{2}\big(\|c_k - c^*\|^2 - \|c_0 - c^*\|^2\big) \ge -\tfrac{L}{2}\|c_0 - c^*\|^2.$$

By Lemma 4, $F(c_j) \ge F(c_k)$ for $j \le k$, so $\sum_{j=1}^k F(c_j) \ge k F(c_k)$. Then $k (F(c_k) - F(c^*)) \le \frac{L}{2} \|c_0 - c^*\|^2$. $\square$

**Lemma 6 (fixed points are minimizers).** $T(c) = c$ if and only if $c$ minimizes $F$, if and only if, with $r = A^{\mathsf T}(y - A c)$, $r_j = \lambda \operatorname{sign}(c_j)$ for $c_j \ne 0$ and $|r_j| \le \lambda$ for $c_j = 0$.

*Proof.* Since $F$ is convex, $c$ is a minimizer if and only if $0 \in \nabla f(c) + \lambda\, \partial \|c\|_1$, which in entries is the stated condition, because $\nabla f(c) = -r$ and the subdifferential of $|t|$ is $\{\operatorname{sign} t\}$ for $t \ne 0$ and $[-1, 1]$ for $t = 0$. On the other hand, $T(c) = c$ means $S_{\lambda/L}(c_j + r_j/L) = c_j$ for every $j$. If $c_j \ne 0$, Lemma 2 shows that this holds if and only if $c_j = c_j + r_j/L - (\lambda/L) \operatorname{sign}(c_j)$, that is $r_j = \lambda \operatorname{sign}(c_j)$. If $c_j = 0$, it holds if and only if $|r_j / L| \le \lambda / L$. $\square$

**Lemma 7 (the refit is exact on a correct support).** Let $y = A c^\circ$ for a vector $c^\circ$ whose nonzero entries lie in $S$, and let the columns $S$ of $A$ be linearly independent. Then the refit of line L6 returns $c^\circ$.

*Proof.* The columns $S$ form a matrix $A_S$ of full column rank, so the least-squares problem $\min_u \|A_S u - y\|$ has a unique solution (the normal equations have a positive definite matrix). The restriction of $c^\circ$ to $S$ gives a zero residual, so it is that solution, and the other entries are set to 0. $\square$

**Theorem.** SPARSE-PCE stops after $N$ model runs and a fixed number of arithmetic operations. After $K$ steps from $c_0 = 0$, the ISTA iterate satisfies $F(c_K) \le F(c_{K-1}) \le \ldots \le F(0)$ and $F(c_K) - \min F \le L \|c^*\|^2 / (2K)$. Every limit point of the iterates is a minimizer. If the support found in line L5 contains the support of the true coefficient vector of a polynomial $q$ in the span, and the columns on it are independent, the returned coefficients are the true ones.

*Proof.* Termination: power iteration runs a fixed number of steps, ISTA runs $K$ steps, and the refit is one Cholesky solve on at most $N - 1$ columns. Monotonicity and the rate are Lemmas 4 and 5 with $c_0 = 0$. The iterates stay in the bounded set $\{F \le F(0)\}$; if $c_{k_i} \to \bar c$, then $\|T(c_{k_i}) - c_{k_i}\|^2 \le \frac{2}{L}(F(c_{k_i}) - F(c_{k_i + 1})) \to 0$ by Lemma 4, because $F(c_k)$ is decreasing and bounded below. $T$ is continuous, so $T(\bar c) = \bar c$, and Lemma 6 makes $\bar c$ a minimizer. The last claim is Lemma 7. $\blacksquare$

Two parts of the method are not covered by the theorem. First, the reference code estimates $L$ by 200 power iteration steps times 1.01. Power iteration approaches $\|A\|_2^2$ from below, so the margin is a heuristic; the tests check that the estimate bounds $\|A^{\mathsf T} A v\| / \|v\|$ on random vectors. Second, the theorem does not say that the support of the LASSO minimizer is the true support. That needs a property of $A$ such as the restricted isometry property, which random samples give only with high probability.
