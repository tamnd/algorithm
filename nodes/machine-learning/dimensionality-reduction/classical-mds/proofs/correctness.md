---
title: Classical MDS recovers Euclidean configurations and minimizes the strain
proves: [correctness]
status: full
---

Let $D$ be a symmetric $n \times n$ matrix with zero diagonal, $A = D^{(2)}$ its matrix of squared entries, $J = I - \frac1n \mathbf{1}\mathbf{1}^\top$ and $B = -\frac12 JAJ$. Lines L2 to L4 compute exactly this $B$: expand $JAJ = A - \frac1n \mathbf{1}\mathbf{1}^\top A - \frac1n A \mathbf{1}\mathbf{1}^\top + \frac{1}{n^2}\mathbf{1}\mathbf{1}^\top A \mathbf{1}\mathbf{1}^\top$, whose $(i, j)$ entry is $a_{ij} - r_j - r_i + g$ because $A$ is symmetric.

**Lemma 1 (distances give inner products).** If $d_{ij} = \|z_i - z_j\|$ for points $z_i \in \mathbb{R}^p$ with mean $\bar z$, and $Z_c$ is the $n \times p$ matrix with rows $z_i - \bar z$, then $B = Z_c Z_c^\top$.

*Proof.* Distances do not change under translation, so we may replace $z_i$ by $z_i - \bar z$. Let $G = Z_c Z_c^\top$ and let $q$ be the vector of the diagonal entries $q_i = \|z_i - \bar z\|^2$. Then $a_{ij} = q_i + q_j - 2 g_{ij}$, so $A = q\mathbf{1}^\top + \mathbf{1}q^\top - 2G$. Since $J\mathbf{1} = 0$ and $\mathbf{1}^\top J = 0$, we get $JAJ = -2JGJ$. The rows of $Z_c$ sum to zero, so $G\mathbf{1} = 0$ and $JGJ = G$. Hence $B = -\frac12(-2G) = G$. $\square$

**Lemma 2 (inner products give distances).** For any symmetric $A$ with zero diagonal, $b_{ii} + b_{jj} - 2b_{ij} = a_{ij}$ for all $i, j$.

*Proof.* From the entry formula, $b_{ij} = -\frac12(a_{ij} - r_i - r_j + g)$ and, with $a_{ii} = 0$, $b_{ii} = r_i - \frac{g}{2}$. So $b_{ii} + b_{jj} - 2b_{ij} = r_i + r_j - g + a_{ij} - r_i - r_j + g = a_{ij}$. $\square$

**Theorem 1 (the Euclidean test; Schoenberg 1935, Young and Householder 1938).** $D$ is Euclidean of dimension $p$ if and only if $B$ is positive semidefinite with rank at most $p$. In that case, with the eigenpairs $(\lambda_j, v_j)$ of line L5, the rows of $X = [\sqrt{\lambda_1} v_1, \ldots, \sqrt{\lambda_p} v_p]$ have the distances $\|x_i - x_j\| = d_{ij}$.

*Proof.* If $D$ is Euclidean of dimension $p$, Lemma 1 gives $B = Z_c Z_c^\top$, so $u^\top B u = \|Z_c^\top u\|^2 \ge 0$ for each $u$, and the rank of $B$ is at most the number $p$ of columns of $Z_c$. Conversely, let $B$ be positive semidefinite of rank at most $p$. By the [spectral theorem](/spectral-theorem/), $B = \sum_{j=1}^n \lambda_j v_j v_j^\top$ with $\lambda_1 \ge \cdots \ge \lambda_n \ge 0$ and $\lambda_j = 0$ for $j > p$. So $B = XX^\top$ for the $X$ of the statement. Then $\|x_i - x_j\|^2 = b_{ii} + b_{jj} - 2b_{ij} = a_{ij} = d_{ij}^2$ by Lemma 2, and $d_{ij} \ge 0$ gives $\|x_i - x_j\| = d_{ij}$. $\square$

**Theorem 2 (uniqueness up to a rigid motion).** If $Y \in \mathbb{R}^{n \times p}$ and $X \in \mathbb{R}^{n \times p}$ have the same pairwise distances, then there is an orthogonal $p \times p$ matrix $Q$ and a vector $t$ with $y_i = Q x_i + t$ for each $i$.

*Proof.* Center both configurations; this is a translation. By Lemma 1, both centered matrices satisfy $X_c X_c^\top = B = Y_c Y_c^\top$. For each $u \in \mathbb{R}^n$, $\|X_c^\top u\|^2 = u^\top B u = \|Y_c^\top u\|^2$. Define $T$ on the column space $R_X = \{X_c^\top u\}$ by $T(X_c^\top u) = Y_c^\top u$. It is well defined: if $X_c^\top u = X_c^\top u'$, then $\|Y_c^\top(u - u')\| = \|X_c^\top(u - u')\| = 0$. It is linear and preserves norms, so it is an isometry from $R_X$ onto $R_Y = \{Y_c^\top u\}$, and the two spaces have the same dimension. Extend $T$ by any isometry between the orthogonal complements of $R_X$ and $R_Y$ in $\mathbb{R}^p$, which also have equal dimensions. The result is an orthogonal $Q$ with $Q X_c^\top = Y_c^\top$, that is $Y_c = X_c Q^\top$. Undo the centering to get $t$. $\square$

Theorems 1 and 2 together say: on a Euclidean $D$ of dimension $p \le k$, classical MDS returns the true points up to a rigid motion (the extra axes $p < j \le k$ are zero).

**Theorem 3 (optimality for the strain).** For any symmetric $B$ with eigenvalues $\lambda_1 \ge \cdots \ge \lambda_n$, the output $X$ of lines L6 and L7 minimizes $\|B - XX^\top\|_F$ over all $X \in \mathbb{R}^{n \times k}$, and the minimum is $\big(\sum_{j \le k} \min(\lambda_j, 0)^2 + \sum_{j > k} \lambda_j^2\big)^{1/2}$.

*Proof.* Let $M = XX^\top$. It is positive semidefinite with rank at most $k$, so its eigenvalues in descending order are $\mu_1 \ge \cdots \ge \mu_k \ge 0 = \mu_{k+1} = \cdots = \mu_n$. The [Hoffman-Wielandt theorem](/hoffman-wielandt-theorem/) for symmetric matrices gives $\|B - M\|_F^2 \ge \sum_{j=1}^n (\lambda_j - \mu_j)^2$ with both lists in descending order. For $j > k$ the term is $\lambda_j^2$. For $j \le k$, the term $(\lambda_j - \mu_j)^2$ with $\mu_j \ge 0$ is at least $\min(\lambda_j, 0)^2$. So the strain is at least the stated value. The output gives $M = \sum_{j \le k} \max(\lambda_j, 0) v_j v_j^\top$, so $B - M = \sum_{j \le k} \min(\lambda_j, 0) v_j v_j^\top + \sum_{j > k} \lambda_j v_j v_j^\top$, whose squared Frobenius norm is the stated value because the $v_j$ are orthonormal. $\square$

**Exact Euclidean test.** The implementation decides "$B$ is positive semidefinite" exactly over the rationals. If some $b_{pp} > 0$, write $B$ in block form with the pivot $p$ first. Then $B$ is positive semidefinite if and only if its Schur complement $S = B_{-p,-p} - b_{\cdot p} b_{p \cdot} / b_{pp}$ is, because $B = L \,\mathrm{diag}(b_{pp}, S)\, L^\top$ with an invertible $L$. If no diagonal entry is positive and some diagonal entry is negative, $B$ is not positive semidefinite. If the whole diagonal is zero, $B$ is positive semidefinite only if $B = 0$: for $b_{ij} \ne 0$, the vector $u = e_i - t\, \mathrm{sign}(b_{ij})\, e_j$ with $t > 0$ gives $u^\top B u = -2t|b_{ij}| < 0$. Each step removes one row and one column, so the test stops after at most $n$ steps.
