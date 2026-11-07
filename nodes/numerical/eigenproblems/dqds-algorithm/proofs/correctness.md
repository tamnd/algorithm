---
title: The dqds transform shifts the squared singular values, stays positive below the smallest one, and the algorithm returns them
proves: [correctness, termination]
status: full
---

Notation of the page. $B$ is $n \times n$ upper bidiagonal with diagonal $\sqrt{q_k}$ and superdiagonal $\sqrt{e_k}$, $q_k \ge 0$, $e_k \ge 0$. Its singular values are $\sigma_1 \ge \dots \ge \sigma_n \ge 0$. $S$ is the accumulated shift. The arithmetic is exact except in the last section.

**Lemma 0 (signs do not matter).** The bidiagonal with entries $a_k, b_k$ and the one with entries $|a_k|, |b_k|$ have the same singular values.

*Proof.* Choose signs $s_k, t_k \in \{\pm 1\}$ one after another so that $s_k a_k t_k = |a_k|$ and $s_k b_k t_{k+1} = |b_k|$. Then $\operatorname{diag}(s) B \operatorname{diag}(t)$ is the matrix with absolute values, and orthogonal factors keep singular values. $\square$

**Lemma 1 (the transform).** Let $e_k > 0$ for all $k$ and $\tau \in \mathbb{R}$. Suppose lines L4 to L9 run with every $\hat q_k \ne 0$. Then the output defines $\hat B$ with $\hat B^T \hat B = B B^T - \tau I$.

*Proof.* $BB^T$ is tridiagonal, with $(BB^T)_{kk} = q_k + e_k$ (where $e_n = 0$) and $(BB^T)_{k,k+1}^2 = q_{k+1} e_k$. Also $\hat B^T \hat B$ is tridiagonal, with $(\hat B^T \hat B)_{kk} = \hat q_k + \hat e_{k-1}$ (where $\hat e_0 = 0$) and $(\hat B^T \hat B)_{k,k+1}^2 = \hat q_k \hat e_k$. Both off-diagonals are nonnegative, so it is enough to match the diagonals and the squared off-diagonals.

By induction, the $d$ at the start of iteration $k$ (with $d_1 = q_1 - \tau$) satisfies $d_k = q_k - \hat e_{k-1} - \tau$. For $k = 1$ this is L4. If it holds for $k$, then L7 and L8 give
$$d_{k+1} = \frac{d_k q_{k+1}}{\hat q_k} - \tau = \frac{(\hat q_k - e_k) q_{k+1}}{\hat q_k} - \tau = q_{k+1} - \hat e_k - \tau.$$
Hence L6 gives $\hat q_k + \hat e_{k-1} = d_k + e_k + \hat e_{k-1} = q_k + e_k - \tau$ for $k < n$. L9 gives $\hat q_n + \hat e_{n-1} = q_n - \tau$. For the off-diagonal, L7 gives $\hat q_k \hat e_k = e_k q_{k+1}$. $\square$

So $\sigma_i(\hat B)^2 = \sigma_i(B)^2 - \tau$ for every $i$, because $BB^T$ and $B^T B$ have the same eigenvalues. After the update $S \leftarrow S + \tau$ at L10, the multiset $\{S + \sigma_i(B)^2\}$ is the same as before the transform. It is therefore the multiset of squared singular values of the input matrix.

**Lemma 2 (the meaning of $d_k$).** Suppose all $q_j > 0$ and $e_j > 0$, and $\hat q_1, \dots, \hat q_{k-1} > 0$. Let $B_k$ be the leading $k \times k$ block of $B$. Then $\hat q_1, \dots, \hat q_{k-1}, d_k$ are the pivots of the Cholesky ($LDL^T$) factorization of $B_k B_k^T - \tau I$.

*Proof.* $B_k B_k^T$ agrees with the leading $k \times k$ block of $BB^T$, except at $(k, k)$, where it has $q_k$ instead of $q_k + e_k$. The pivots of a tridiagonal $T$ satisfy $p_1 = t_{11}$ and $p_j = t_{jj} - t_{j-1,j}^2 / p_{j-1}$. For $BB^T - \tau I$ this reads $p_j = q_j + e_j - \tau - q_j e_{j-1}/p_{j-1}$. By Lemma 1, $\hat q_j = d_j + e_j$ and $d_j = q_j - \tau - q_j e_{j-1}/\hat q_{j-1}$, so $p_j = \hat q_j$ for $j < k$. The last pivot of $B_k B_k^T - \tau I$ uses $q_k$ in place of $q_k + e_k$, which gives $d_k$. $\square$

**Lemma 3 (positivity).** Let all $q_j, e_j > 0$. The transform runs with every $d_k > 0$ if and only if $\tau < \sigma_n^2$, and then every $\hat q_k > 0$ and $\hat e_k > 0$.

*Proof.* Suppose first that $\tau < \sigma_n^2$. $B$ is upper triangular and nonsingular, so $B^{-1}$ is upper triangular with leading block $B_k^{-1}$. Hence $\lVert B_k^{-1}\rVert_2 \le \lVert B^{-1}\rVert_2$, that is, $\sigma_{\min}(B_k) \ge \sigma_n$. Therefore $B_k B_k^T - \tau I$ is positive definite for every $k$, and its last pivot $d_k$ is positive by Lemma 2, by induction on $k$. Then $\hat q_k = d_k + e_k > 0$ and $\hat e_k = e_k q_{k+1}/\hat q_k > 0$.

Conversely, if every $d_k > 0$, then every $\hat q_k > 0$. By Lemma 2 with $k = n$, these are the Cholesky pivots of $BB^T - \tau I$, so that matrix is positive definite and $\tau < \sigma_n^2$. $\square$

If $\tau = \sigma_n^2$ exactly, the same argument gives $d_k > 0$ for $k < n$ and $d_n = 0$. If some $q_j = 0$, then $\sigma_n = 0$, line L3 takes $\tau = 0$, and the transform runs with $d_k \ge 0$. When $\hat q_k = 0$, then $d_k = e_k = 0$, and the code sets $\hat e_k = 0$ and restarts $d$ at $q_{k+1} - \tau$. That is the transform applied to the two blocks separately, so Lemma 1 still holds blockwise. The transform therefore keeps all quantities nonnegative.

**Lemma 4 (the Newton shift is a lower bound).** If all $q_j > 0$, the value $\tau$ of line L3 satisfies $0 < \tau \le \sigma_n^2$.

*Proof.* Let $c_j = \lVert B^{-1} e_j \rVert_2^2$, where $e_j$ is the $j$-th unit vector. From $B^{-1} B = I$, column $j$ gives $\sqrt{q_j}\, B^{-1} e_j + \sqrt{e_{j-1}}\, B^{-1} e_{j-1} = e_j$. The vector $B^{-1} e_{j-1}$ is supported on rows $1, \dots, j - 1$ and is orthogonal to $e_j$. Hence $c_j = (1 + e_{j-1} c_{j-1})/q_j$ and $c_1 = 1/q_1$. So $\sum_j c_j = \lVert B^{-1}\rVert_F^2 = \sum_i \sigma_i^{-2} \ge \sigma_n^{-2}$, and $\tau = 1/\sum_j c_j \le \sigma_n^2$. This value is also $-f(0)/f'(0)$ for $f(x) = \det(BB^T - xI)$, which is one Newton step from $0$. $\square$

By Lemmas 3 and 4, in exact arithmetic the test at L8 fails only when $\tau = \sigma_n^2$ exactly. In that case $d_n = 0 \ge 0$ and the transform is accepted.

**Lemma 5 (deflation).** Suppose $e_{n-1} \le u^2 (S + q_n)$ at L2. Recording $S + q_n$ and continuing with the leading $(n-1) \times (n-1)$ block changes each eigenvalue of $BB^T + SI$ by at most $(u + u^2)(S + q_n)$.

*Proof.* Write $M = BB^T + SI$. The matrix $M'$ is block diagonal, with the leading block $B_{n-1} B_{n-1}^T + SI$ and the trailing entry $S + q_n$. Then $M - M'$ has only three nonzero entries: $e_{n-1}$ at $(n-1, n-1)$ and $\beta = \sqrt{q_n e_{n-1}}$ at $(n-1, n)$ and $(n, n-1)$. Its 2-norm is at most $e_{n-1} + \beta$. Since $q_n \le S + q_n$, we have $\beta \le u (S + q_n)$, and $e_{n-1} \le u^2 (S + q_n)$. Weyl's inequality bounds each eigenvalue change by $\lVert M - M'\rVert_2$. $\square$

Since $S \ge 0$ and every eigenvalue of $M$ is at least $S$, the bound is of the order of $u$ times the deflated value. That makes it relative for that value. For the remaining values it is at most $(u + u^2)$ times their own size, plus $(u + u^2) q_n$. When $e_{n-1} = 0$, the deflation is exact.

**Theorem (correctness and termination).** In exact arithmetic, the values returned at L11 are the singular values of the input, provided the loop ends without the step cap. The loop always ends, after at most $n + 60n$ passes.

*Proof.* By Lemma 0, the squared variables represent the input. Each accepted transform keeps the multiset $\{S + \sigma_i(B)^2\}$ (Lemma 1, with Lemma 3 and the remarks for the degenerate cases). An exact deflation with $e_{n-1} = 0$ splits $M$ into two blocks. The recorded $S + q_n$ is the eigenvalue of the trailing $1 \times 1$ block, and the rest is carried by the leading block. When $n = 1$, the value is $S + q_1$. L11 returns their square roots, sorted. For termination, each pass of L2 either lowers $n$, which can happen at most $n$ times, or performs a transform. Transforms are counted and capped at $60n$, after which the code raises an error. $\square$

**Convergence (cited, not proved here).** With $\tau = 0$, the qd recurrences give $e_k^{(t)} \to 0$ like $(\sigma_{k+1}/\sigma_k)^{2t}$ (Rutishauser 1954; Fernando and Parlett 1994). Aishima, Matsuo, Murota and Sugihara (2008) proved global convergence of dqds under a class of shift strategies, together with its asymptotic rate. The bound of $60n$ transforms is a safety cap. In the tests, about 9 transforms per value were used.

**Floating point (cited).** Fernando and Parlett (1994) proved that the computed dqds transform is mixed stable in the relative sense. Make relative changes of a few ulps to each $q_k$ and $e_k$, apply the exact transform, and change each output entry by a few ulps; the result is the computed $(\hat q, \hat e)$. Demmel and Kahan (1990) proved that relative changes of size at most $\eta$ in the $2n - 1$ entries of a bidiagonal matrix change each singular value by a factor between $(1 + \eta)^{-(2n-1)}$ and $(1 + \eta)^{2n-1}$. Combining the two results bounds the relative error in each $\sigma_i$ by $O(n u)$ per transform, whatever the ratio $\sigma_i / \sigma_1$.
