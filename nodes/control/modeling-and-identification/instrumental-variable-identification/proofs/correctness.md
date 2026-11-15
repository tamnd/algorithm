---
title: IV-ARX solves the IV equations, and its error is R^-1 times the instrument-noise sum
proves: [correctness]
status: full
---

Fix the data $y(0), \ldots, y(N-1)$, $u(0), \ldots, u(N-1)$, the orders $n_a \ge 0$, $n_b \ge 1$, $n_k \ge 0$, and $d = n_a + n_b$. We work in exact real arithmetic, as in the real RAM. Let $\varphi(k)$ be the regressor and $\zeta(k)$ the instrument vector of line L4, and write

$$R_k = \sum_{j=k_0}^{k} \zeta(j) \varphi(j)^T, \qquad f_k = \sum_{j=k_0}^{k} \zeta(j)\, y(j),$$

with $R_{k_0-1} = 0$ and $f_{k_0-1} = 0$.

**Lemma 1 (the vectors are defined).** For $k \ge k_0$ every index used by $\varphi(k)$ and $\zeta(k)$ lies in $\{0, \ldots, N-1\}$.

*Proof.* The regressor uses $k - i$ for $1 \le i \le n_a$ and $k - n_k - j$ for $0 \le j \le n_b - 1$; these are at least $k - n_a$ and $k - n_k - n_b + 1$. The delayed instruments use $k - n_k - j$ for $0 \le j \le d - 1$, at least $k - n_k - d + 1$. The model instruments use the same indices as the regressor, into the simulated signal $x$, which has the same length as $u$. In each case L1 chooses $k_0$ as the largest of the shifts that occur, so every index is at least $k - k_0 \ge 0$. Every index is at most $k \le N - 1$. $\square$

**Lemma 2 (loop invariant).** After the pass of the loop of L3 for time $k$, the variables hold $R = R_k$ and $f = f_k$.

*Proof.* By induction on $k$. Line L2 sets $R = 0 = R_{k_0-1}$ and $f = 0 = f_{k_0-1}$. If $R = R_{k-1}$ and $f = f_{k-1}$ before the pass for $k$, then L5 and L6 give $R_{k-1} + \zeta(k) \varphi(k)^T = R_k$ and $f_{k-1} + \zeta(k)\, y(k) = f_k$. $\square$

After the loop, $R = R_{N-1}$ and $f = f_{N-1}$; write them $R$ and $f$.

**Lemma 3 (the IV equations).** A vector $\theta$ solves $\sum_{k=k_0}^{N-1} \zeta(k) \big(y(k) - \varphi(k)^T \theta\big) = 0$ if and only if $R \theta = f$.

*Proof.* The left side equals $\sum \zeta(k) y(k) - \big(\sum \zeta(k) \varphi(k)^T\big) \theta = f - R \theta$. $\square$

**Lemma 4 (the error formula).** Suppose $R$ is nonsingular and, for some $\theta_0$ and some sequence $v$, $y(k) = \varphi(k)^T \theta_0 + v(k)$ for every $k \ge k_0$. Then the solution of $R\theta = f$ is $\hat\theta = \theta_0 + R^{-1} \sum_{k=k_0}^{N-1} \zeta(k)\, v(k)$.

*Proof.* $f = \sum \zeta(k) \big(\varphi(k)^T \theta_0 + v(k)\big) = R \theta_0 + \sum \zeta(k) v(k)$. Multiply by $R^{-1}$. $\square$

**Theorem.** If $R$ is nonsingular, IV-ARX returns the unique solution $\hat\theta$ of the IV equations; if $R$ is singular, it stops at L7. Under the hypothesis of Lemma 4:

1. if $v(k) = 0$ for all $k \ge k_0$, then $\hat\theta = \theta_0$;
2. for a sequence of data sets with $N \to \infty$, if $\frac{1}{N} R \to \bar R$ with $\bar R$ nonsingular and $\frac{1}{N} \sum \zeta(k) v(k) \to 0$, then $\hat\theta \to \theta_0$.

*Proof.* By Lemma 1 every vector in the loop is well defined, and by Lemma 2 the loop leaves $R$ and $f$. If $R$ is singular, L7 stops. Otherwise L8 computes the unique solution of $R \theta = f$, which by Lemma 3 is the unique solution of the IV equations, and L9 returns it.

(1) follows from Lemma 4 with $\sum \zeta v = 0$.

(2) Write $\hat\theta - \theta_0 = \big(\frac1N R\big)^{-1} \big(\frac1N \sum \zeta v\big)$ by Lemma 4. Matrix inversion is continuous on the open set of nonsingular matrices, so $\frac1N R$ is nonsingular for all large $N$ and $\big(\frac1N R\big)^{-1} \to \bar R^{-1}$. The product of a convergent sequence of matrices and a sequence of vectors that tends to 0 tends to 0. Hence $\hat\theta \to \theta_0$. $\blacksquare$

The hypotheses of (2) are where the instruments matter. In open loop with $v$ stationary, ergodic and independent of $u$, and with $\zeta$ built from $u$ only, the law of large numbers gives $\frac1N \sum \zeta v \to \mathbb{E}\, \zeta v = 0$ and $\frac1N R \to \mathbb{E}\, \zeta \varphi^T$ with probability 1, so (2) holds whenever $\mathbb{E}\, \zeta \varphi^T$ is nonsingular. With $\zeta = \varphi$ the first limit is $\mathbb{E}\, \varphi v$, which is not 0 for colored $v$, and this is the bias of least squares.
