---
title: Power iteration returns a small backward error and converges at the rate of the eigenvalue ratio
proves: [correctness, termination]
status: full
---

Exact arithmetic, except in Lemma 2, which holds for every computed pair. Notation of the page: $A \in \mathbb C^{n \times n}$ with $|\lambda_1| \ge |\lambda_2| \ge \dots \ge |\lambda_n|$, $q_k$ the unit vector after $k$ executions of line L8 ($q_0$ from line L1), $\rho_k = q_k^* A q_k$, $r_k = A q_k - \rho_k q_k$, $\theta_k = \angle(q_k, v_1)$, and $\varrho = |\lambda_2 / \lambda_1|$.

**Lemma 1 (the iterates).** If the method has not returned before step $k + 1$, then $A^j x_0 \ne 0$ for $j \le k$ and $q_k = A^k x_0 / \|A^k x_0\|_2$.

*Proof.* Induction on $k$. For $k = 0$ this is line L1. If $q_k = A^k x_0 / \|A^k x_0\|$ and the method reaches line L8 at step $k + 1$, then $z = A q_k = A^{k+1} x_0 / \|A^k x_0\|$. If $z = 0$, then $r = 0$ and line L6 returns, so at line L8 $z \ne 0$, hence $A^{k+1} x_0 \ne 0$, and $q_{k+1} = z / \|z\| = A^{k+1} x_0 / \|A^{k+1} x_0\|$. $\square$

**Lemma 2 (backward error).** Let $q$ be a unit vector, $\rho = q^* A q$ and $r = A q - \rho q$. Then $(A - r q^*) q = \rho q$ and $\|r q^*\|_2 = \|r\|_2$. So when line L6 returns, $(\rho, q)$ is an exact eigenpair of $A + E$ with $\|E\|_2 = \|r\|_2 \le \mathrm{tol} \, \|A q\|_2 \le \mathrm{tol} \, \|A\|_2$.

*Proof.* $(A - r q^*) q = A q - r (q^* q) = A q - r = \rho q$. The rank-one matrix $r q^*$ has 2-norm $\|r\|_2 \|q\|_2 = \|r\|_2$. $\square$

**Theorem 1 (Hermitian A).** Let $A^* = A$ with orthonormal eigenvectors $v_i$, $|\lambda_1| > |\lambda_2|$, and $c_1 = v_1^* x_0 \ne 0$. Let $\delta = \lambda_{\max} - \lambda_{\min}$. Then for each $k \ge 0$:

1. $\tan\theta_k \le \varrho^k \tan\theta_0$;
2. $|\rho_k - \lambda_1| \le \delta \sin^2\theta_k \le \delta \, \varrho^{2k} \tan^2\theta_0$;
3. $\|r_k\|_2 \le \sqrt 2 \, \delta \sin\theta_k \le \sqrt 2 \, \delta \, \varrho^k \tan\theta_0$.

*Proof.* Write $x_0 = \sum_i c_i v_i$. By Lemma 1, $q_k$ is a positive multiple of $A^k x_0 = \sum_i c_i \lambda_i^k v_i$. Since the $v_i$ are orthonormal, $\cos\theta_k = |c_1 \lambda_1^k| / \|A^k x_0\|$ and $\sin\theta_k = \bigl(\sum_{i \ge 2} |c_i|^2 |\lambda_i|^{2k}\bigr)^{1/2} / \|A^k x_0\|$. Hence

$$\tan\theta_k = \frac{\bigl(\sum_{i \ge 2} |c_i|^2 |\lambda_i|^{2k}\bigr)^{1/2}}{|c_1| \, |\lambda_1|^k} \le \frac{|\lambda_2|^k}{|\lambda_1|^k} \cdot \frac{\bigl(\sum_{i \ge 2} |c_i|^2\bigr)^{1/2}}{|c_1|} = \varrho^k \tan\theta_0 .$$

This is item 1. Item 2 is the bound $|\rho(x) - \lambda_j| \le \delta \sin^2\angle(x, v_j)$ of the [Rayleigh quotient](/rayleigh-quotient/) page with $j = 1$, together with $\sin\theta \le \tan\theta$. For item 3 write $q_k = \sum_i d_i v_i$ with $\sum_i |d_i|^2 = 1$, $|d_1| = \cos\theta_k$ and $\sum_{i \ge 2} |d_i|^2 = \sin^2\theta_k$. Then $r_k = \sum_i d_i (\lambda_i - \rho_k) v_i$, and

$$\|r_k\|_2^2 = |d_1|^2 (\lambda_1 - \rho_k)^2 + \sum_{i \ge 2} |d_i|^2 (\lambda_i - \rho_k)^2 \le \delta^2 \sin^4\theta_k + \delta^2 \sin^2\theta_k \le 2 \delta^2 \sin^2\theta_k,$$

using item 2 for the first term and $|\lambda_i - \rho_k| \le \delta$ (both lie in $[\lambda_{\min}, \lambda_{\max}]$) for the others. $\square$

**Theorem 2 (diagonalizable A).** Let $A = V \Lambda V^{-1}$ with unit eigenvectors $v_i$ (the columns of $V$), $|\lambda_1| > |\lambda_2|$, and $x_0 = \sum_i c_i v_i$ with $c_1 \ne 0$. Let $C = \sum_{i \ge 2} |c_i / c_1|$. Then $\sin\theta_k \le C \varrho^k$ for each $k$, and $|\rho_k - \lambda_1| \le 4 |\lambda_1| C \varrho^k$ whenever $C \varrho^k \le 1/2$.

*Proof.* $|\lambda_1| > |\lambda_2| \ge 0$ gives $\lambda_1 \ne 0$. Let $w_k = A^k x_0 / (c_1 \lambda_1^k) = v_1 + \sum_{i \ge 2} (c_i / c_1) (\lambda_i / \lambda_1)^k v_i$, a nonzero multiple of $q_k$ (Lemma 1). Then $\|w_k - v_1\| \le \sum_{i \ge 2} |c_i / c_1| \, |\lambda_i / \lambda_1|^k \le C \varrho^k$. For nonzero $w$ and unit $v$, $\sin\angle(w, v) = \min_t \|v - t w\| \le \|v - w\|$; with $w = w_k$ and $v = v_1$ this gives the first claim. The Rayleigh quotient does not depend on the scale, so

$$|\rho_k - \lambda_1| = \frac{|w_k^* (A - \lambda_1 I) w_k|}{w_k^* w_k} \le \frac{\|(A - \lambda_1 I) w_k\|}{\|w_k\|}.$$

Here $(A - \lambda_1 I) w_k = \sum_{i \ge 2} (c_i / c_1) (\lambda_i / \lambda_1)^k (\lambda_i - \lambda_1) v_i$ has norm at most $2 |\lambda_1| C \varrho^k$, because $|\lambda_i - \lambda_1| \le 2|\lambda_1|$. And $\|w_k\| \ge 1 - C \varrho^k \ge 1/2$. $\square$

**Theorem 3 (termination).** Under the hypotheses of Theorem 2 and for each $\mathrm{tol} > 0$, line L6 returns CONVERGED after finitely many steps if $\mathrm{maxit}$ is large enough.

*Proof.* With $w_k$ as above, $q_k = \phi_k w_k / \|w_k\|$ for a scalar $|\phi_k| = 1$. Then $\|r_k\| \le \|(A - \lambda_1 I) q_k\| + |\lambda_1 - \rho_k| \le 2 \cdot 4 |\lambda_1| C \varrho^k$ once $C \varrho^k \le 1/2$, by the two bounds in the proof of Theorem 2. Also $\|A q_k\| \ge |\lambda_1| - \|(A - \lambda_1 I) q_k\| \ge |\lambda_1| (1 - 4 C \varrho^k)$. Since $\varrho < 1$, the ratio $\|r_k\| / \|A q_k\|$ tends to $0$, so it is at most $\mathrm{tol}$ for some finite $k$, and line L6 returns at step $k + 1$. $\square$

**Remark (a defective dominant eigenvalue).** The hypothesis that $A$ is diagonalizable cannot simply be dropped without a loss of rate. For $A = \begin{pmatrix} \lambda & 1 \\ 0 & \lambda \end{pmatrix}$ with real $\lambda \ne 0$ and $x_0 = e_2$, $A^k e_2 = (k \lambda^{k-1}, \lambda^k)^T$, so $q_k$ is parallel to $(k, \lambda)^T$, $\tan\theta_k = |\lambda| / k$, and $\rho_k - \lambda = \lambda k / (k^2 + \lambda^2)$. The error decays like $1/k$, not geometrically. $\blacksquare$
