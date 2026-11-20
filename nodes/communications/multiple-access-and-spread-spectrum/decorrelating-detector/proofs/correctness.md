---
title: The decorrelator removes all multiple access interference, and its error rate does not depend on the other users
proves: [correctness]
status: full
---

The model is $y = S A b + w$ for one symbol interval. The matrix $S$ is $N \times K$, its column $s_k$ is the signature of user $k$ with $\|s_k\| = 1$, $A = \mathrm{diag}(A_1, \ldots, A_K)$ with $A_k > 0$, $b \in \{-1, +1\}^K$, and $w \sim \mathcal{N}(0, \sigma^2 I_N)$. Let $R = S^\top S$. Line L1 computes $z = S^\top y$, line L2 computes $R$, line L3 solves $R x = z$, and line L4 decides $\hat b_k = \mathrm{sgn}(x_k)$.

**Lemma 1 (the matched filter outputs).** $z = R A b + n$ with $n \sim \mathcal{N}(0, \sigma^2 R)$.

*Proof.* $z = S^\top S A b + S^\top w$. The vector $n = S^\top w$ is Gaussian with mean zero and covariance $E[S^\top w w^\top S] = \sigma^2 S^\top S = \sigma^2 R$. $\square$

**Lemma 2 (when line L3 succeeds).** $R$ is invertible if and only if the signatures $s_1, \ldots, s_K$ are linearly independent. This needs $K \le N$.

*Proof.* For any $v$, $v^\top R v = \|S v\|^2$. So $R$ is positive semidefinite, and $R v = 0$ implies $S v = 0$. Conversely, $S v = 0$ implies $R v = S^\top S v = 0$. So $R$ is singular exactly when some nonzero $v$ has $S v = 0$. $\square$

**Theorem 1 (no interference).** If the signatures are linearly independent, then

$$x = R^{-1} z = A b + \tilde n, \qquad \tilde n \sim \mathcal{N}(0, \sigma^2 R^{-1}). \tag{1}$$

So $x_k = A_k b_k + \tilde n_k$, where $\tilde n_k$ has variance $\sigma^2 (R^{-1})_{kk}$ and does not depend on $b$ or on the amplitudes. The error probability of user $k$ is

$$P_k = Q\Big( \frac{A_k}{\sigma \sqrt{(R^{-1})_{kk}}} \Big). \tag{2}$$

*Proof.* By Lemma 1, $R^{-1} z = A b + R^{-1} n$, and $R^{-1} n$ has covariance $\sigma^2 R^{-1} R R^{-1} = \sigma^2 R^{-1}$. Given $b_k = +1$, line L4 errs when $\tilde n_k < -A_k$, which has probability $Q(A_k / (\sigma \sqrt{(R^{-1})_{kk}}))$. The case $b_k = -1$ is symmetric. $\square$

**Corollary (no noise).** If $w = 0$, then $x = A b$ exactly and every decision is right, for every choice of the amplitudes.

**Lemma 3 (least squares).** The vector $x$ of line L3 is the unique minimizer of $\|y - S x\|^2$ over $x \in \mathbb{R}^K$. So it is the maximum likelihood estimate of the vector $A b$ when that vector is treated as an unknown real vector, with no use of the fact that $b_k = \pm 1$.

*Proof.* The function $\|y - S x\|^2$ is a convex quadratic with gradient $2(S^\top S x - S^\top y) = 2(R x - z)$. The gradient is zero exactly when $R x = z$, which has the single solution $R^{-1} z$. Under the Gaussian model, the log-likelihood of $y$ given the mean $S x$ is $-\|y - S x\|^2 / (2 \sigma^2)$ plus a constant. $\square$

**Lemma 4 (the noise penalty).** Let $P_k$ be the orthogonal projection onto the span of the signatures other than $s_k$. Then

$$\frac{1}{(R^{-1})_{kk}} = \|s_k - P_k s_k\|^2 = 1 - \|P_k s_k\|^2 \le 1,$$

with equality if and only if $s_k$ is orthogonal to every other signature.

*Proof.* Order the users so that $k$ comes first and write $R = \begin{pmatrix} 1 & r^\top \\ r & R' \end{pmatrix}$, where $r$ holds the correlations $s_j^\top s_k$ for $j \ne k$ and $R'$ is the correlation matrix of the others. $R'$ is invertible, because the other signatures are independent. By the formula for the inverse of a block matrix, $(R^{-1})_{kk} = 1 / (1 - r^\top R'^{-1} r)$, where $1 - r^\top R'^{-1} r$ is the [Schur complement](/schur-complement/) of $R'$. With $S'$ the matrix of the other signatures, $P_k = S' R'^{-1} S'^\top$, so $P_k s_k = S' R'^{-1} r$ and $\|P_k s_k\|^2 = r^\top R'^{-1} R' R'^{-1} r = r^\top R'^{-1} r$. Since $\|s_k\| = 1$ and $s_k - P_k s_k$ is orthogonal to $P_k s_k$, $1 - \|P_k s_k\|^2 = \|s_k - P_k s_k\|^2$. This is 1 if and only if $P_k s_k = 0$, that is, if and only if $r = 0$. $\square$

So the decorrelator works as if user $k$ were alone with the energy $A_k^2 / (R^{-1})_{kk}$: the part of $s_k$ that lies in the span of the others is lost, and only the orthogonal part carries the bit. Compared with the single-user error rate $Q(A_k / \sigma)$, the loss is the factor $\eta_k = 1 / (R^{-1})_{kk}$ in energy, for every $\sigma$.

**Corollary (near-far resistance).** The asymptotic efficiency of a detector for user $k$ is the supremum of the $e \in [0, 1]$ with $P_k = O(Q(\sqrt{e}\, A_k / \sigma))$ as $\sigma \to 0$. Its near-far resistance is the infimum of the asymptotic efficiency over all amplitudes of the other users. By (2), the decorrelator has asymptotic efficiency $\eta_k = 1/(R^{-1})_{kk}$ whatever the other amplitudes are, so its near-far resistance is also $\eta_k$, which is positive whenever the signatures are independent. Lupas and Verdú proved that no detector has a larger near-far resistance; that result is cited, not proved here. For two users with correlation $\rho$, $\eta_k = 1 - \rho^2$.

**Remark (the cost).** Line L1 costs $O(K N)$, line L2 costs $O(K^2 N)$, and line L3 costs $O(K^3)$ with Gaussian elimination. When the signatures do not change from one interval to the next, $R^{-1}$, or a [Cholesky](/cholesky-decomposition/) factor of $R$, is computed once, and each interval costs $O(K N + K^2)$.
