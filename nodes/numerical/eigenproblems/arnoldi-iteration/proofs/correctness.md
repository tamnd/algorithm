---
title: The Arnoldi process gives an orthonormal Krylov basis, a Hessenberg projection and computable Ritz residuals
proves: [correctness, termination]
status: full
---

Notation of the page: $A \in \mathbb{C}^{n \times n}$, $b \ne 0$, $K_j = K_j(A, b) = \operatorname{span}\{b, Ab, \dots, A^{j-1} b\}$, $Q_j = [q_1, \dots, q_j]$, and $h_{ij}$ the coefficients of lines L5 and L7. Exact arithmetic unless stated. In exact arithmetic the second pass of line L6 computes $q_i^* w = 0$ for every $i$, so it changes nothing, and modified Gram-Schmidt gives the same coefficients as classical Gram-Schmidt (Lemma 1).

**Lemma 1 (modified equals classical).** At step $j$, let $w^{(0)} = A q_j$ and $w^{(i)} = w^{(i-1)} - h_{ij} q_i$ with $h_{ij} = q_i^* w^{(i-1)}$. If $q_1, \dots, q_j$ are orthonormal, then $h_{ij} = q_i^* A q_j$.

*Proof.* $w^{(i-1)} = A q_j - \sum_{l < i} h_{lj} q_l$, and $q_i^* q_l = 0$ for $l < i$, so $q_i^* w^{(i-1)} = q_i^* A q_j$. $\square$

**Theorem 1 (orthonormal basis and the Arnoldi relation).** Suppose the loop completes steps $1, \dots, k$ with $h_{j+1,j} > 0$ for $j < k$. Then $q_1, \dots, q_k$ are orthonormal, $\operatorname{span}\{q_1, \dots, q_j\} = K_j$ for $j \le k$, and
$$A Q_k = Q_k H_k + w_k e_k^T, \qquad Q_k^* w_k = 0, \qquad H_k = Q_k^* A Q_k,$$
where $w_k$ is the vector $w$ after line L5 (or L6) of step $k$, $w_k = h_{k+1,k} q_{k+1}$ if $h_{k+1,k} > 0$, and $H_k = (h_{ij})_{i, j \le k}$ is upper Hessenberg with $h_{j+1,j} > 0$ for $j < k$.

*Proof.* Induction on $j$. For $j = 1$, $q_1 = b / \|b\|_2$ is a unit vector spanning $K_1$. Assume the claims for $j$. By Lemma 1, after line L5 we have $w = A q_j - \sum_{i \le j} (q_i^* A q_j) q_i$, so $q_l^* w = q_l^* A q_j - q_l^* A q_j = 0$ for every $l \le j$. If $h_{j+1,j} = \|w\|_2 > 0$, then $q_{j+1} = w / h_{j+1,j}$ is a unit vector orthogonal to $q_1, \dots, q_j$. Rearranging line L5 gives
$$A q_j = \sum_{i=1}^{j} h_{ij} q_i + h_{j+1,j} q_{j+1}. \qquad (1)$$
By the induction hypothesis $q_j \in K_j$, so $A q_j \in A K_j \subseteq K_{j+1}$. By (1), $q_{j+1} = (A q_j - \sum_{i \le j} h_{ij} q_i)/h_{j+1,j} \in K_{j+1}$. So $\operatorname{span}\{q_1, \dots, q_{j+1}\} \subseteq K_{j+1}$, and since the $j + 1$ orthonormal vectors are independent while $\dim K_{j+1} \le j + 1$, the spans are equal. Writing (1) for $j = 1, \dots, k$ as columns gives $A Q_k = Q_k H_k + w_k e_k^T$, with $h_{ij} = 0$ for $i > j + 1$ since such entries are never set. Multiplying by $Q_k^*$ and using $Q_k^* Q_k = I$ and $Q_k^* w_k = 0$ gives $H_k = Q_k^* A Q_k$. $\square$

**Theorem 2 (breakdown and termination).** Let $m$ be the smallest index with $K_m = K_{m+1}$, that is, the degree of the minimal polynomial of $b$ with respect to $A$. Then $h_{j+1,j} > 0$ for $j < m$ and $h_{m+1,m} = 0$. In that case $K_m$ is invariant under $A$, $A Q_m = Q_m H_m$, every eigenvalue of $H_m$ is an eigenvalue of $A$, and for $H_m y = \theta y$ the vector $Q_m y$ is an eigenvector of $A$. The loop runs at most $\min(k, n)$ times, and each run does finitely many operations, so the algorithm terminates.

*Proof.* For $j < m$, $\dim K_{j+1} = j + 1$, so $K_{j+1} \ne K_j$. If $h_{j+1,j} = 0$ held, (1) would give $A q_j \in \operatorname{span}\{q_1, \dots, q_j\} = K_j$. Together with $A q_i \in K_{i+1} \subseteq K_j$ for $i < j$, this means $A K_j \subseteq K_j$, hence $A^j b \in K_j$ and $K_{j+1} = K_j$, a contradiction. At $j = m$, $w = A q_m - Q_m Q_m^* A q_m$ is the component of $A q_m \in K_{m+1} = K_m$ orthogonal to $K_m$, so $w = 0$. Then $A Q_m = Q_m H_m$, and $H_m y = \theta y$ gives $A (Q_m y) = Q_m H_m y = \theta Q_m y$ with $Q_m y \ne 0$, because $Q_m$ has orthonormal columns. Since $\dim K_j \le n$, $m \le n$; the loop also stops at $k$, and line L8 or the loop bound ends it. $\square$

**Theorem 3 (Ritz residual).** Let $H_k y = \theta y$ with $\|y\|_2 = 1$ and $x = Q_k y$. Then $\|x\|_2 = 1$ and
$$\|A x - \theta x\|_2 = h_{k+1,k} |e_k^T y|.$$
Moreover $(\theta, x)$ is an exact eigenpair of $A + E$ with $E = -r x^*$, $r = A x - \theta x$, and $\|E\|_2 = \|r\|_2$.

*Proof.* By Theorem 1, $A x = Q_k H_k y + h_{k+1,k} q_{k+1} e_k^T y = \theta x + h_{k+1,k} (e_k^T y) q_{k+1}$, and $\|q_{k+1}\|_2 = 1$. For $E = -r x^*$, $(A + E) x = A x - r = \theta x$, and $\|r x^*\|_2 = \|r\|_2 \|x\|_2$. $\square$

**Lemma 2.** If the first $k$ steps complete with $h_{j+1,j} > 0$ for $j < k$, then $A^j q_1 = Q_k H_k^j e_1$ for $0 \le j \le k - 1$, and $A^k q_1 = Q_k H_k^k e_1 + \gamma\, w_k$ with $\gamma = \prod_{j=1}^{k-1} h_{j+1,j}$.

*Proof.* The case $j = 0$ is $q_1 = Q_k e_1$. If $A^j q_1 = Q_k H_k^j e_1$, then by Theorem 1, $A^{j+1} q_1 = A Q_k H_k^j e_1 = Q_k H_k^{j+1} e_1 + w_k\, e_k^T H_k^j e_1$. Since $H_k$ is upper Hessenberg, $H_k^j e_1$ has nonzero entries only in positions $1, \dots, j + 1$, and its entry $j + 1$ is $\prod_{l=1}^{j} h_{l+1,l}$. So $e_k^T H_k^j e_1 = 0$ for $j < k - 1$, and it equals $\gamma$ for $j = k - 1$. $\square$

**Theorem 4 (polynomial optimality).** Under the hypothesis of Lemma 2, let $p_k$ be the characteristic polynomial of $H_k$. Then $\|p_k(A) b\|_2 \le \|p(A) b\|_2$ for every monic polynomial $p$ of degree $k$.

*Proof.* Every monic $p$ of degree $k$ gives $p(A) b = A^k b - v$ with $v \in K_k$, and conversely. The minimum of $\|A^k b - v\|_2$ over $v \in K_k$ is attained when $A^k b - v \perp K_k$. By Lemma 2, $p_k(A) q_1 = Q_k p_k(H_k) e_1 + \gamma\, w_k$, and $p_k(H_k) = 0$ by the Cayley-Hamilton theorem, so $p_k(A) b = \|b\|_2 \gamma\, w_k$. By Theorem 1, $w_k \perp K_k$. Hence $p_k$ attains the minimum. $\square$

**Floating point (statements, with references).** For the computed $\hat Q_{k+1}$ and $\hat{\bar H}_k$ from modified Gram-Schmidt, $A \hat Q_k = \hat Q_{k+1} \hat{\bar H}_k + F$ with $\|F\|_2$ bounded by $u \|A\|_2$ times a low-degree polynomial in $n$ and $k$. The loss of orthogonality $\|I - \hat Q_{k+1}^* \hat Q_{k+1}\|_2$ is bounded by a modest multiple of $u$ times the condition number of the matrix $[b, A \hat Q_k]$ (Björck's bound for modified Gram-Schmidt, applied to the Arnoldi basis by Paige, Rozložník and Strakoš in 2006). For classical Gram-Schmidt applied twice, Giraud, Langou, Rozložník and van den Eshof (2005) proved orthogonality of order $u$ when the matrix being orthogonalized is numerically of full rank. Theorem 3 then holds for the computed quantities up to these errors. The implementation's tests check the relation and the orthogonality against $10\, n\, u$ for a random $60 \times 60$ matrix.
