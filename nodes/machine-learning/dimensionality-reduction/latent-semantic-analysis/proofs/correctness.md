---
title: The truncated SVD is the best rank-k term-document matrix, and folding in is a projection
proves: [correctness]
status: full
---

We use the pseudocode and notation of the page. $A$ is the weighted $m \times n$ term-document matrix built in line L1, with rank $\rho$ and singular value decomposition $A = \sum_{i=1}^{\rho} \sigma_i u_i v_i^{\top}$, $\sigma_1 \ge \cdots \ge \sigma_\rho > 0$, orthonormal $u_i \in \mathbb{R}^m$ and orthonormal $v_i \in \mathbb{R}^n$. For $k \le \rho$, $U_k = [u_1 \ldots u_k]$, $V_k = [v_1 \ldots v_k]$, $\Sigma_k = \operatorname{diag}(\sigma_1, \ldots, \sigma_k)$ and $A_k = U_k \Sigma_k V_k^{\top}$. We put $\sigma_i = 0$ for $i > \rho$.

**Lemma 1 (the SVD from the eigenvectors of $A^{\top} A$).** Let $A^{\top} A = \sum_t \lambda_t v_t v_t^{\top}$ with orthonormal $v_t$ and $\lambda_1 \ge \lambda_2 \ge \cdots \ge 0$. For $\lambda_t > 0$ put $\sigma_t = \sqrt{\lambda_t}$ and $u_t = A v_t / \sigma_t$. Then the $u_t$ are orthonormal, $A v_t = \sigma_t u_t$, $A^{\top} u_t = \sigma_t v_t$, and $A = \sum_{\lambda_t > 0} \sigma_t u_t v_t^{\top}$.

*Proof.* $u_s^{\top} u_t = v_s^{\top} A^{\top} A v_t / (\sigma_s \sigma_t) = \lambda_t [s = t] / (\sigma_s \sigma_t) = [s = t]$, and $A^{\top} u_t = A^{\top} A v_t / \sigma_t = \sigma_t v_t$. If $\lambda_t = 0$ then $\lVert A v_t \rVert^2 = v_t^{\top} A^{\top} A v_t = 0$. So $A = A \sum_t v_t v_t^{\top} = \sum_{\lambda_t > 0} \sigma_t u_t v_t^{\top}$. $\square$

This is how line L2 is computed in the implementation, and it shows that the $\sigma_t$ are the singular values of $A$.

**Theorem 1 (Eckart-Young).** $\lVert A - A_k \rVert_F^2 = \sum_{i > k} \sigma_i^2$ and $\lVert A - A_k \rVert_2 = \sigma_{k+1}$. For every matrix $B$ of rank at most $k$, $\lVert A - B \rVert_F \ge \lVert A - A_k \rVert_F$ and $\lVert A - B \rVert_2 \ge \lVert A - A_k \rVert_2$.

*Proof.* The equalities: $A - A_k = \sum_{i > k} \sigma_i u_i v_i^{\top}$ is itself an SVD, so its squared Frobenius norm is the sum of the squares of its singular values and its spectral norm is the largest one, $\sigma_{k+1}$.

The inequalities use [Weyl's inequality](/weyls-inequality/) for singular values, $\sigma_{i + j - 1}(X + Y) \le \sigma_i(X) + \sigma_j(Y)$. Take $X = A - B$, $Y = B$ and $j = k + 1$. Since $B$ has rank at most $k$, $\sigma_{k+1}(B) = 0$, so
$$ \sigma_{k + i}(A) \le \sigma_i(A - B) \qquad \text{for all } i \ge 1 . $$
With $i = 1$ this is $\lVert A - B \rVert_2 \ge \sigma_{k+1}$. Summing the squares over $i$ gives $\lVert A - B \rVert_F^2 = \sum_i \sigma_i(A - B)^2 \ge \sum_{i \ge 1} \sigma_{k+i}(A)^2 = \lVert A - A_k \rVert_F^2$. $\square$

So $A_k$ is the best rank-$k$ approximation of the weighted term-document matrix in both norms, and the error left in the discarded dimensions is exactly $\sigma_{k+1}^2 + \cdots + \sigma_\rho^2$. The general statement and its history are on the [singular value decomposition](/singular-value-decomposition/) page.

**Theorem 2 (folding in).** Let $q \in \mathbb{R}^m$ be a query or a new document, weighted as in line L1, and $\hat q = \Sigma_k^{-1} U_k^{\top} q$ as in line L3. Then:

1. $U_k U_k^{\top} q = U_k \Sigma_k \hat q$, so $\Sigma_k \hat q$ holds the coordinates of the orthogonal projection of $q$ onto the span of $u_1, \ldots, u_k$.
2. If $q = A e_j$ is column $j$ of $A$, then $\hat q$ is row $j$ of $V_k$.

*Proof.* (1) $U_k \Sigma_k \hat q = U_k U_k^{\top} q$, and $U_k U_k^{\top}$ is the orthogonal projector onto the column span of $U_k$ because $U_k^{\top} U_k = I$. (2) $U_k^{\top} A e_j = U_k^{\top} \sum_i \sigma_i u_i v_i^{\top} e_j = \Sigma_k V_k^{\top} e_j$, because $u_s^{\top} u_i = [s = i]$. Multiply by $\Sigma_k^{-1}$. $\square$

So a folded-in document lands where it would be if it had been part of the collection, provided that the SVD would not change. A new document changes the true SVD, which is why repeated folding in degrades the space and the SVD must be recomputed or updated from time to time.

**Theorem 3 (what the scores measure).** Put $d_j = \Sigma_k V_k^{\top} e_j$ (document $j$, scaled as in line L4) and $\tilde q = \Sigma_k \hat q = U_k^{\top} q$. Then:

1. $d_i^{\top} d_j = (A_k e_i)^{\top} (A_k e_j)$, so cosines between scaled documents are cosines between the columns of $A_k$.
2. $\tilde q^{\top} d_j = (U_k U_k^{\top} q)^{\top} (A_k e_j)$ and $\lVert \tilde q \rVert = \lVert U_k U_k^{\top} q \rVert$. So the score of line L5 is the cosine between the projected query and column $j$ of $A_k$.
3. Term $i$ is represented by row $i$ of $U_k \Sigma_k$, and the inner products of these rows are the entries of $A_k A_k^{\top}$.

*Proof.* (1) $A_k^{\top} A_k = V_k \Sigma_k U_k^{\top} U_k \Sigma_k V_k^{\top} = V_k \Sigma_k^2 V_k^{\top}$, and $d_i^{\top} d_j = e_i^{\top} V_k \Sigma_k^2 V_k^{\top} e_j$. (2) $\tilde q^{\top} d_j = q^{\top} U_k \Sigma_k V_k^{\top} e_j = q^{\top} A_k e_j$, and $A_k e_j$ lies in the span of $U_k$, so $q^{\top} A_k e_j = (U_k U_k^{\top} q)^{\top} A_k e_j$. Also $\lVert U_k^{\top} q \rVert = \lVert U_k U_k^{\top} q \rVert$ because $U_k$ has orthonormal columns. (3) $A_k A_k^{\top} = U_k \Sigma_k^2 U_k^{\top}$. $\square$

Two terms that never occur in the same document have orthogonal rows in a count matrix, but their rows in $A_k$ can be strongly correlated if they occur with the same other terms. This is the effect that LSA is used for.

**Cost.** Line L1 takes time linear in the total length of the documents. The implementation computes $A^{\top} A$ in $\Theta(m n^2)$ and its eigendecomposition with Jacobi sweeps in $O(n^3)$ per sweep, so it suits $n \le m$ and small $n$; for $m < n$, use $A A^{\top}$ instead. For a large sparse $A$ with $N$ nonzero entries, a Lanczos or randomized method finds the top $k$ singular triplets with $O(N k)$ work per iteration. Line L3 costs $\Theta(m k)$, or the number of query terms times $k$ for a sparse query, and lines L4 and L5 cost $\Theta(n k)$. The reduced representation needs $\Theta((m + n) k)$ memory.
