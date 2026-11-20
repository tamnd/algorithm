---
title: The EIM matrix is unit lower triangular, the interpolant is quasi-optimal with a Lebesgue constant at most 2^M - 1, and the loop stops
proves: [correctness, termination]
status: full
---

We assume exact arithmetic. Functions live on the finite grid $\Omega_h$, $\|v\|_\infty = \max_{x \in \Omega_h} |v(x)|$, and $W_M = \operatorname{span}\{q_1, \ldots, q_M\}$. We write $I_M g$ for the interpolant of line L10 when $B$ is invertible, and $r^{M}_\mu = g(\cdot; \mu) - I_M g(\cdot; \mu)$, with $I_0 g = 0$.

**Lemma 1 (one step).** Suppose that after $M - 1$ steps the matrix $B$ of size $M - 1$ is lower triangular with a unit diagonal, that $I_{M-1}$ interpolates at $x_1, \ldots, x_{M-1}$, and that line L4 does not stop. Then the residual $r = r^{M-1}_{\mu^\ast}$ of line L6 is not 0, $r(x_M) \ne 0$, and the new function $q_M = r / r(x_M)$ satisfies $q_M(x_i) = 0$ for $i < M$, $q_M(x_M) = 1$ and $\|q_M\|_\infty = 1$. The new $B$ is lower triangular with a unit diagonal.

*Proof.* Line L4 did not stop, so $\|r\|_\infty = e(\mu^\ast) > \varepsilon_{tol} \ge 0$. Line L7 takes a point where $|r|$ reaches $\|r\|_\infty$, so $r(x_M) \ne 0$ and $|q_M(x)| = |r(x)| / |r(x_M)| \le 1$, with equality at $x_M$. For $i < M$, $r(x_i) = g(x_i; \mu^\ast) - I_{M-1} g(x_i; \mu^\ast) = 0$ by interpolation, so $q_M(x_i) = 0$. So the new column of $B$ has the entries $B_{iM} = q_M(x_i) = 0$ above the diagonal, which line L9 stores, and $B_{MM} = 1$. The earlier rows do not change. In particular $x_M$ differs from $x_1, \ldots, x_{M-1}$, where $r$ is 0. $\square$

**Lemma 2 (interpolation and reproduction).** If $B$ is lower triangular with a unit diagonal, then for every $g$ the system $B c = (g(x_i))_i$ has one solution, $I_M g = \sum_j c_j q_j$ satisfies $I_M g(x_i) = g(x_i)$ for $i \le M$, and $I_M v = v$ for every $v \in W_M$. Also $W_M = \operatorname{span}\{g(\cdot; \mu_1), \ldots, g(\cdot; \mu_M)\}$.

*Proof.* $\det B = 1$, so $c$ exists and is unique, and $(I_M g)(x_i) = \sum_j B_{ij} c_j = g(x_i)$. For $v = \sum_j a_j q_j$, the vector $a$ solves $B a = (v(x_i))_i$, so $c = a$ by uniqueness and $I_M v = v$. For the span, $q_M$ is a nonzero multiple of $g(\cdot; \mu_M) - I_{M-1} g(\cdot; \mu_M)$, where $I_{M-1} g \in W_{M-1}$. By induction $W_M \subseteq \operatorname{span}\{g(\cdot; \mu_j)\}_{j \le M}$, and $g(\cdot; \mu_M) = r(x_M) q_M + I_{M-1} g(\cdot; \mu_M) \in W_M$ gives the other inclusion. $\square$

By induction on $M$ with Lemmas 1 and 2, every step of the loop is well defined, $B$ stays lower triangular with a unit diagonal, and $\|q_j\|_\infty = 1$ for all $j$.

**Lemma 3 (Lagrange functions).** Let $\ell^M_j \in W_M$ with $\ell^M_j(x_i) = \delta_{ij}$ for $i, j \le M$. These exist and are unique, $I_M g = \sum_j g(x_j)\, \ell^M_j$, and for $j < M$

$$\ell^M_M = q_M, \qquad \ell^M_j = \ell^{M-1}_j - \ell^{M-1}_j(x_M)\, q_M .$$

*Proof.* Existence and uniqueness: $\ell^M_j = I_M$ applied to the grid function with values $\delta_{ij}$ at $x_i$, by Lemma 2, and the formula for $I_M g$ follows by linearity of the system. The recursion: $q_M \in W_M$ has the values $\delta_{iM}$ by Lemma 1. For $j < M$, the right side is in $W_M$. At $x_i$ with $i < M$ it equals $\ell^{M-1}_j(x_i) - \ell^{M-1}_j(x_M) \cdot 0 = \delta_{ij}$, and at $x_M$ it equals $\ell^{M-1}_j(x_M) - \ell^{M-1}_j(x_M) \cdot 1 = 0$. Uniqueness gives the identity. $\square$

**Theorem 1 (Lebesgue constant).** $\Lambda_M = \max_{x \in \Omega_h} \sum_{j=1}^{M} |\ell^M_j(x)| \le 2^M - 1$.

*Proof.* $\Lambda_1 = \|q_1\|_\infty = 1$. For $M \ge 2$, Lemma 3 and $\|q_M\|_\infty = 1$ give, at each $x$,

$$\sum_{j=1}^{M} |\ell^M_j(x)| \le \sum_{j<M} |\ell^{M-1}_j(x)| + |q_M(x)| \sum_{j<M} |\ell^{M-1}_j(x_M)| + |q_M(x)| \le \Lambda_{M-1} + \Lambda_{M-1} + 1 .$$

So $\Lambda_M + 1 \le 2(\Lambda_{M-1} + 1)$ and $\Lambda_M + 1 \le 2^{M-1}(\Lambda_1 + 1) = 2^M$. $\square$

**Theorem 2 (quasi-optimality).** For every grid function $g$, $\|g - I_M g\|_\infty \le (1 + \Lambda_M) \min_{v \in W_M} \|g - v\|_\infty$.

*Proof.* For $v \in W_M$, $I_M v = v$ by Lemma 2, so $g - I_M g = (g - v) - I_M(g - v)$. By Lemma 3, $|I_M w(x)| = |\sum_j w(x_j) \ell^M_j(x)| \le \|w\|_\infty \Lambda_M$. So $\|g - I_M g\|_\infty \le (1 + \Lambda_M) \|g - v\|_\infty$. The minimum exists because $W_M$ has finite dimension. $\square$

**Theorem 3 (termination and the stopping error).** The loop stops after at most $\min(m, M_{max})$ steps. If it stops by the tolerance, then $\|g(\cdot; \mu) - I_M g(\cdot; \mu)\|_\infty \le \varepsilon_{tol}$ for every $\mu \in \Xi$.

*Proof.* If step $M$ chooses $\mu^\ast$, its residual is not 0 by Lemma 1, so $g(\cdot; \mu^\ast) \notin W_{M-1}$ by Lemma 2. Each chosen $g(\cdot; \mu_j)$ lies in $W_M$ by Lemma 2, so a chosen parameter has residual 0 at all later steps and is never chosen again. So at most $m$ parameters are chosen. After $m$ steps every training function is in $W_m$ and all residuals are 0, so line L4 stops; it also stops at $M = M_{max}$. The second claim is the test of line L4 with the maximum of line L3. $\blacksquare$
