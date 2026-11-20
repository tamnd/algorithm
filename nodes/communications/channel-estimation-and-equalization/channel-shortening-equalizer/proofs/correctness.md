---
title: The MSSNR filter is the leading generalized eigenvector of the window and wall matrices, and the iteration converges to it
proves: [correctness]
status: full
---

The channel taps are real, $h_0, \ldots, h_{L-1}$, and the filter is $w = (w_0, \ldots, w_{L_w-1})$. The effective channel is $c = h * w$, of length $L + L_w - 1$. In matrix form $c = \mathbf{H} w$, where $\mathbf{H}$ has $L + L_w - 1$ rows and $L_w$ columns, $\mathbf{H}_{kj} = h_{k-j}$ (zero outside $0 \le k - j \le L - 1$). Write $\mathbf{h}_k$ for row $k$. For the delay $d$ and the prefix length $\nu$, the window is the set of indices $W = \{d, \ldots, d + \nu\}$, and the wall is the rest. Line L1 computes
$$\mathbf{B} = \sum_{k \in W} \mathbf{h}_k \mathbf{h}_k^T, \qquad \mathbf{A} = \sum_{k \notin W} \mathbf{h}_k \mathbf{h}_k^T.$$

**Lemma 1 (energies as quadratic forms).** The window energy $\sum_{k \in W} c_k^2$ equals $w^T \mathbf{B} w$, and the wall energy $\sum_{k \notin W} c_k^2$ equals $w^T \mathbf{A} w$. Both matrices are symmetric and positive semidefinite.

*Proof.* $c_k = \mathbf{h}_k^T w$, so $c_k^2 = w^T \mathbf{h}_k \mathbf{h}_k^T w$. Sum over the window or over the wall. Each term is symmetric and positive semidefinite, so the sums are too. $\square$

So the shortening SNR of $w$ is the generalized Rayleigh quotient $S(w) = w^T \mathbf{B} w / w^T \mathbf{A} w$. From here on, $\mathbf{A}$ is positive definite. This holds when the wall rows have full column rank $L_w$, which is the usual case. If $\mathbf{A}$ is singular, a nonzero $w$ puts no energy on the wall, the channel is shortened exactly, and the solve in line L4 fails, which the code reports.

**Lemma 2 (the optimum is an eigenvector).** Let $\mathbf{A} = \mathbf{R}\mathbf{R}^T$ be the Cholesky factorization and $\mathbf{C} = \mathbf{R}^{-1} \mathbf{B} \mathbf{R}^{-T}$. Then $\mathbf{C}$ is symmetric and positive semidefinite, with the eigenvalues $\lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_{L_w} \ge 0$. The maximum of $S(w)$ over $w \ne 0$ is $\lambda_1$, and it is reached exactly at the vectors $w$ with $\mathbf{B} w = \lambda_1 \mathbf{A} w$.

*Proof.* Put $u = \mathbf{R}^T w$, a bijection of the nonzero vectors. Then $w^T \mathbf{A} w = u^T u$ and $w^T \mathbf{B} w = u^T \mathbf{C} u$, so $S(w) = u^T \mathbf{C} u / u^T u$, the Rayleigh quotient of $\mathbf{C}$. Its maximum is $\lambda_1$, reached exactly at the eigenvectors of $\lambda_1$. And $\mathbf{C} u = \lambda u$ is the same as $\mathbf{B} w = \lambda \mathbf{A} w$, by multiplying with $\mathbf{R}$ on the left. $\square$

With $\mu = 1/\lambda$, the condition is $\mathbf{A} w = \mu \mathbf{B} w$, so the optimum is the generalized eigenvector with the smallest $\mu$, and the best shortening SNR is $1/\mu_{\min}$.

**Lemma 3 (the iteration is the power method).** Lines L4 and L5 compute $w' = \mathbf{M} w / \sqrt{(\mathbf{M}w)^T \mathbf{B} (\mathbf{M}w)}$ with $\mathbf{M} = \mathbf{A}^{-1}\mathbf{B}$. The matrix $\mathbf{M}$ is similar to $\mathbf{C}$, so it has the same real nonnegative eigenvalues and is diagonalizable. If $\lambda_1 > \lambda_2$ and the start vector has a nonzero component along the eigenvector of $\lambda_1$, the direction of $w$ converges to that eigenvector, and the error shrinks by the factor $\lambda_2/\lambda_1$ per step.

*Proof.* $\mathbf{R}^T \mathbf{M} \mathbf{R}^{-T} = \mathbf{R}^T \mathbf{R}^{-T}\mathbf{R}^{-1} \mathbf{B} \mathbf{R}^{-T} = \mathbf{C}$. So $\mathbf{M} = \mathbf{R}^{-T} \mathbf{C} \mathbf{R}^T$, and with the eigenvectors $u_i$ of $\mathbf{C}$, the vectors $v_i = \mathbf{R}^{-T} u_i$ are a basis of eigenvectors of $\mathbf{M}$. Write the start vector as $\sum_i a_i v_i$. After $t$ steps, up to a positive scale, $w = \sum_i a_i \lambda_i^t v_i = \lambda_1^t \big(a_1 v_1 + \sum_{i \ge 2} a_i (\lambda_i/\lambda_1)^t v_i\big)$, and the sum over $i \ge 2$ goes to zero as $(\lambda_2/\lambda_1)^t$. The scaling in line L5 changes only the length. Line L4 is an inverse iteration for the pencil $\mathbf{A} - \mu \mathbf{B}$ with the shift 0, which is why the smallest $\mu$ wins. $\square$

**Theorem 1 (the output).** At the fixed point, line L6 gives $\mu = w^T \mathbf{A} w = 1/\lambda_1$, and the returned value $1/\mu$ is the shortening SNR of the returned $w$ and the largest shortening SNR of any filter with $L_w$ taps for the delay $d$.

*Proof.* Line L5 makes $w^T \mathbf{B} w = 1$, so $w^T \mathbf{A} w = 1/S(w)$ for every iterate, and $1/\mu = S(w)$ exactly, even before convergence. At the limit, $\mathbf{B} w = \lambda_1 \mathbf{A} w$, so $1 = w^T \mathbf{B} w = \lambda_1 w^T \mathbf{A} w$ and $\mu = 1/\lambda_1$. By Lemma 2 this is the maximum. $\square$

**Lemma 4 (the polishing steps are safe).** The code then takes up to 3 Rayleigh quotient steps, $v = (\mathbf{A} - \mu \mathbf{B})^{-1} \mathbf{B} w$, and keeps a step only if the new $\mu$ is not larger than the old one (up to a relative $10^{-9}$). A kept step cannot make the result worse than by that margin, and the result is never above the optimum.

*Proof.* Every candidate is scaled so that $w^T \mathbf{B} w = 1$, so its $\mu$ is $1/S(w) \ge 1/\lambda_1$ by Lemma 2. A kept step therefore leaves $S(w) \le \lambda_1$ and does not lower $S(w)$ by more than the margin. Near a simple eigenvalue the Rayleigh quotient iteration converges fast, so these steps remove the last rounding error of the power method. $\square$

**Lemma 5 (the best delay).** `best_delay` runs the method for every delay $d$ with $0 \le d \le L + L_w - 2 - \nu$, the delays for which the window lies inside $c$, and keeps the largest SNR. By Theorem 1 each run gives the optimum for its delay, so the result is the optimum over all filters and delays.

**Theorem 2 (the cost).** Line L1 costs $O((L + L_w) L_w^2)$. Each step of the loop solves an $L_w \times L_w$ system, $O(L_w^3)$ by Gaussian elimination. With $K$ steps, a delay costs $O((L + L_w) L_w^2 + K L_w^3)$, and the search over all delays multiplies this by $L + L_w - 1 - \nu$. The extra space is $O(L_w^2)$.

*Proof.* Each of the $L + L_w - 1$ rows adds an outer product of size $L_w \times L_w$ to one of the matrices. The rest is counted in the code. A factorization of $\mathbf{A}$ computed once would make each step $O(L_w^2)$. $\square$
