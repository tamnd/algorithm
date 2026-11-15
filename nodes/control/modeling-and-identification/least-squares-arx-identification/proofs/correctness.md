---
title: ARX-LS returns the unique minimizer of the sum of squared equation errors
proves: [correctness]
status: full
---

Fix the data $y(0), \ldots, y(N-1)$, $u(0), \ldots, u(N-1)$ and the orders $n_a \ge 0$, $n_b \ge 1$, $n_k \ge 0$. Let $d = n_a + n_b$ and $k_0 = \max(n_a, n_k + n_b - 1)$, and let $\varphi(k)$ be the regressor of line L4. We work in exact real arithmetic, as in the real RAM. Write

$$R_k = \sum_{j=k_0}^{k} \varphi(j) \varphi(j)^T, \qquad f_k = \sum_{j=k_0}^{k} \varphi(j)\, y(j),$$

with $R_{k_0 - 1} = 0$ and $f_{k_0 - 1} = 0$, and $V(\theta) = \sum_{k=k_0}^{N-1} \big(y(k) - \varphi(k)^T \theta\big)^2$.

**Lemma 1 (the regressor is defined).** For $k \ge k_0$ every index used by L4 lies in $\{0, \ldots, N-1\}$.

*Proof.* The output terms use $k - i$ for $1 \le i \le n_a$, and $k - i \ge k_0 - n_a \ge 0$. The input terms use $k - n_k - j$ for $0 \le j \le n_b - 1$, and $k - n_k - j \ge k_0 - n_k - n_b + 1 \ge 0$. All indices are at most $k - 1 \le N - 1$ or $k - n_k \le N - 1$. $\square$

**Lemma 2 (loop invariant).** After the pass of the loop of L3 for time $k$, the variables hold $R = R_k$ and $f = f_k$.

*Proof.* By induction on $k$. Before the loop, L2 sets $R = 0 = R_{k_0 - 1}$ and $f = 0 = f_{k_0 - 1}$. If $R = R_{k-1}$ and $f = f_{k-1}$ before the pass for $k$, then L5 and L6 give $R = R_{k-1} + \varphi(k) \varphi(k)^T = R_k$ and $f = f_{k-1} + \varphi(k)\, y(k) = f_k$. $\square$

So after the loop $R = R_{N-1}$ and $f = f_{N-1}$; write them $R$ and $f$ from now on.

**Lemma 3 (the criterion as a quadratic).** For every $\theta \in \mathbb{R}^d$,

$$V(\theta) = \theta^T R \theta - 2 f^T \theta + c, \qquad c = \sum_{k=k_0}^{N-1} y(k)^2,$$

and $R$ is symmetric and positive semidefinite.

*Proof.* Expand each square: $(y(k) - \varphi(k)^T \theta)^2 = y(k)^2 - 2 y(k)\, \varphi(k)^T \theta + \theta^T \varphi(k) \varphi(k)^T \theta$, and sum over $k$. Each $\varphi(k)\varphi(k)^T$ is symmetric, and $v^T R v = \sum_k (\varphi(k)^T v)^2 \ge 0$ for every $v$. $\square$

**Lemma 4 (the minimizers).** A vector $\theta$ minimizes $V$ if and only if $R \theta = f$. If $R$ is nonsingular, there is exactly one minimizer, $R^{-1} f$. If $R$ is singular, $V$ has infinitely many minimizers.

*Proof.* For any $\theta$ and $\delta$, Lemma 3 gives

$$V(\theta + \delta) - V(\theta) = 2 (R \theta - f)^T \delta + \delta^T R \delta.$$

If $R \theta = f$, the right side is $\delta^T R \delta \ge 0$, so $\theta$ is a minimizer. If $R \theta \ne f$, take $\delta = -t (R \theta - f)$ with $t > 0$; the right side is $-2t \lVert R\theta - f \rVert^2 + t^2 \delta_1$ with $\delta_1 = (R\theta - f)^T R (R\theta - f)$, which is negative for small $t$, so $\theta$ is not a minimizer.

Now $f = \sum_k \varphi(k) y(k)$ lies in the column space of $R$: if $R v = 0$, then $v^T R v = \sum_k (\varphi(k)^T v)^2 = 0$, so $\varphi(k)^T v = 0$ for every $k$ and $f^T v = 0$. Since $R$ is symmetric, its column space is the orthogonal complement of its null space, and $f$ is orthogonal to that null space. Hence $R \theta = f$ always has a solution $\theta^*$. If $R$ is nonsingular the solution is unique. If $R$ is singular, pick $v \ne 0$ with $R v = 0$; then $\theta^* + t v$ solves $R\theta = f$ for every real $t$, and these are infinitely many minimizers. $\square$

**Theorem.** If $R$ is nonsingular, ARX-LS returns the unique minimizer of $V$. If $R$ is singular, it stops at L7, and in that case the minimizer of $V$ is not unique.

*Proof.* By Lemma 1 every regressor is well defined, and by Lemma 2 the matrix and vector after the loop are $R$ and $f$. If $R$ is singular, L7 reports it, and Lemma 4 shows that $V$ has infinitely many minimizers. Otherwise L8 computes the unique solution of $R \theta = f$, which by Lemma 4 is the unique minimizer of $V$, and L9 returns it. $\blacksquare$
