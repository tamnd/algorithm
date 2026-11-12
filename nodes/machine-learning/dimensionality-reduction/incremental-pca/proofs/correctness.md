---
title: Incremental PCA without truncation equals batch PCA
proves: [correctness]
status: full
---

**Setup.** Take $f = 1$. A set $A$ of $n$ points has the mean $\mu_A$ and the scatter $S_A = \sum_{x \in A} (x - \mu_A)(x - \mu_A)^T$; for $n = 0$ put $S_A = 0$. The state before an update is $(U, \sigma, \mu_A, n)$ with $U^T U = I_r$ and $U \Sigma^2 U^T = S_A$, where $\Sigma = \operatorname{diag}(\sigma)$. The batch $B$ has $m \ge 1$ points with mean $\mu_B$, and $C = A \cup B$.

**Lemma 1 (merge).** $S_C = S_A + S_B + \frac{n m}{n + m}(\mu_B - \mu_A)(\mu_B - \mu_A)^T$.

*Proof.* The mean of $C$ is $\mu_C = (n \mu_A + m \mu_B)/(n + m)$, so $\mu_A - \mu_C = \frac{m}{n+m}(\mu_A - \mu_B)$ and $\mu_B - \mu_C = \frac{n}{n+m}(\mu_B - \mu_A)$. For $x \in A$, write $x - \mu_C = (x - \mu_A) + (\mu_A - \mu_C)$ and expand the outer product. The cross terms add up to zero over $A$, because $\sum_{x \in A}(x - \mu_A) = 0$. So $\sum_{x \in A}(x - \mu_C)(x - \mu_C)^T = S_A + n(\mu_A - \mu_C)(\mu_A - \mu_C)^T$, and in the same way for $B$. The two rank-one terms add up to $\big(\frac{n m^2}{(n+m)^2} + \frac{m n^2}{(n+m)^2}\big) (\mu_B - \mu_A)(\mu_B - \mu_A)^T = \frac{nm}{n+m}(\mu_B - \mu_A)(\mu_B - \mu_A)^T$. $\square$

**Lemma 2.** Let $\hat B$ be the matrix of L2. Then $\hat B \hat B^T = S_B + \frac{nm}{n+m}(\mu_B - \mu_A)(\mu_B - \mu_A)^T$, and so $S_C = M M^T$ with $M = [U\Sigma,\ \hat B]$.

*Proof.* The first $m$ columns are $b_j - \mu_B$, whose outer products add up to $S_B$. The last column is $\sqrt{nm/(n+m)}\,(\mu_B - \mu_A)$, whose outer product is the last term; for $n = 0$ the term is zero and the column is left out. Then $M M^T = U\Sigma^2 U^T + \hat B \hat B^T = S_A + \hat B \hat B^T = S_C$ by Lemma 1. $\square$

**Lemma 3.** With $P$, $E$, $\tilde B$ and $R$ as in L3 to L5, $Q = [U\ \tilde B]$ has orthonormal columns and $Q R = M$.

*Proof.* $U^T E = U^T \hat B - U^T U P = P - P = 0$, so $E$ is orthogonal to $\operatorname{span} U$. $\tilde B$ is an orthonormal basis of $\operatorname{span} E$ (in exact arithmetic Gram-Schmidt drops only columns that depend on the previous ones), so $U^T \tilde B = 0$ and $Q^T Q = I$. Also $\tilde B \tilde B^T$ is the orthogonal projection on $\operatorname{span} E$, so $\tilde B \tilde B^T E = E$. Now $Q R = [U\Sigma,\ U P + \tilde B \tilde B^T E] = [U \Sigma,\ UP + E] = [U\Sigma,\ \hat B] = M$. $\square$

**Theorem.** If no nonzero singular value is dropped in L7, then after the update $\mu'$ is the mean of $C$, the count is $n + m$, the new $U$ has orthonormal columns, and $U \operatorname{diag}(\sigma)^2 U^T = S_C$. Hence by induction over the batches, the state after all batches satisfies: the columns of $U$ are eigenvectors of the covariance $S_C / |C|$ with the eigenvalues $\sigma_j^2 / |C|$, and every eigenvector of a nonzero eigenvalue is in the span of $U$. So the columns of $U$ are the principal directions of batch PCA, each unique up to sign when the nonzero eigenvalues are distinct.

*Proof.* L1 with $f = 1$ gives $\mu' = (n\mu_A + m\mu_B)/(n + m) = \mu_C$, and L8 returns $n + m$. Let $R = \tilde U \tilde\Sigma \tilde V^T$ be the SVD of L6, with $\tilde U$ square orthogonal of size $r + p$ (pad $\tilde\Sigma$ with zero rows if $R$ has more rows than columns). By Lemma 3, $S_C = M M^T = Q R R^T Q^T = (Q\tilde U)\,\tilde\Sigma\tilde\Sigma^T (Q\tilde U)^T$, and $Q\tilde U$ has orthonormal columns because $(Q\tilde U)^T Q \tilde U = \tilde U^T \tilde U = I$. If L7 drops only columns with $\tilde\sigma_j = 0$, those columns add nothing to the sum, so the kept columns $U'$ and values $\sigma'$ satisfy $U' \operatorname{diag}(\sigma')^2 U'^T = S_C$. This is the invariant for $C$.

For the eigenvectors: $S_C U' = U' \operatorname{diag}(\sigma')^2 U'^T U' = U' \operatorname{diag}(\sigma')^2$, so each column $u_j$ is an eigenvector with eigenvalue $\sigma_j'^2$, and dividing by $|C|$ gives the covariance. Every vector $w$ orthogonal to $\operatorname{span} U'$ has $S_C w = 0$, so all nonzero eigenvalues of $S_C$ appear among the $\sigma_j'^2$, with the same multiplicities, and their eigenvectors lie in $\operatorname{span} U'$. Since the $\sigma'$ are sorted in decreasing order, the first $k$ columns of $U'$ are the top $k$ principal directions, as in batch PCA. For a simple eigenvalue, the unit eigenvectors are $\pm u_j$ only.

The base case is $n = 0$, $r = 0$: then $S_A = 0$, the invariant holds trivially, and the first update reduces to the SVD of the centered first batch. $\blacksquare$

**Remark (low rank).** If the centered union of all batches has rank at most $k$, then every $S_C$ along the way has rank at most $k$: $S_C$ is a sum of positive semidefinite terms whose ranges lie in the span of the centered final data, so its rank is at most $k$. Then $R$ has at most $k$ nonzero singular values and L7 drops only zeros, so the theorem applies with truncation to $k$.
