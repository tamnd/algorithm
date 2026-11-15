---
title: MOESP recovers the system up to similarity from noise-free data, and the column space of the observability matrix under white output noise
proves: [correctness]
status: full
---

We work in exact real arithmetic, as in the real RAM, and assume that the LQ factorization and the SVD are exact. The data come from

$$x_{k+1} = A x_k + B u_k, \qquad y_k = C x_k + D u_k + v_k, \qquad k = 0, \ldots, N-1,$$

with $x_k \in \mathbb{R}^n$, $u_k \in \mathbb{R}^m$, $y_k \in \mathbb{R}^p$. In the first part $v_k = 0$. The integer $i > n$ is the number of block rows and $j = N - i + 1$ is the number of columns.

**Notation.** $U$ and $Y$ are the $im \times j$ and $ip \times j$ block Hankel matrices with block $(r, c)$ equal to $u_{r+c}$ and $y_{r+c}$ for $r = 0, \ldots, i-1$ and $c = 0, \ldots, j-1$. $X = (x_0, x_1, \ldots, x_{j-1})$ is the $n \times j$ state sequence. $\Gamma_i$ is the extended observability matrix that stacks $C, CA, \ldots, CA^{i-1}$, and $\mathcal{T}_i$ is the $ip \times im$ lower block triangular Toeplitz matrix with $D$ on the block diagonal and $C A^{r-c-1} B$ in block $(r, c)$ for $r > c$. $V$ is the block Hankel matrix of the $v_k$.

**Lemma 1 (data equation).** $Y = \Gamma_i X + \mathcal{T}_i U + V$.

*Proof.* Iterating the state equation gives $x_{k+r} = A^r x_k + \sum_{t=0}^{r-1} A^{r-1-t} B u_{k+t}$, so $y_{k+r} = C A^r x_k + \sum_{t=0}^{r-1} C A^{r-1-t} B u_{k+t} + D u_{k+r} + v_{k+r}$. Block row $r$ and column $k$ of the right side is exactly this. $\square$

**Lemma 2 (the LQ blocks).** Let $\begin{pmatrix} U \\ Y \end{pmatrix} = \begin{pmatrix} L_{11} & 0 \\ L_{21} & L_{22} \end{pmatrix} \begin{pmatrix} Q_1 \\ Q_2 \end{pmatrix}$ with $L$ lower triangular and $\begin{pmatrix} Q_1 \\ Q_2 \end{pmatrix}$ with orthonormal rows. If $U$ has full row rank $im$, then $L_{11}$ is nonsingular, $U Q_2^T = 0$ and $L_{22} = Y Q_2^T$.

*Proof.* $U = L_{11} Q_1$ has rank $im$, so the $im \times im$ matrix $L_{11}$ is nonsingular. The rows of $Q$ are orthonormal, so $Q_1 Q_2^T = 0$ and $Q_2 Q_2^T = I$. Hence $U Q_2^T = L_{11} Q_1 Q_2^T = 0$ and $Y Q_2^T = L_{21} Q_1 Q_2^T + L_{22} Q_2 Q_2^T = L_{22}$. $\square$

## Noise-free data

Assume $v_k = 0$, that $(A, C)$ is observable, and the excitation condition

$$\operatorname{rank} \begin{pmatrix} X \\ U \end{pmatrix} = n + im. \tag{E}$$

(E) implies that $U$ has full row rank, so Lemma 2 applies.

**Lemma 3 (the column space).** $L_{22} = \Gamma_i X Q_2^T$, $X Q_2^T$ has full row rank $n$, and the column space of $L_{22}$ is the column space of $\Gamma_i$.

*Proof.* By Lemmas 1 and 2, $L_{22} = Y Q_2^T = \Gamma_i X Q_2^T + \mathcal{T}_i U Q_2^T = \Gamma_i X Q_2^T$.

Suppose $a^T X Q_2^T = 0$ for some $a \in \mathbb{R}^n$. Since $i > n$ and $(A, C)$ is observable, $\Gamma_i$ has full column rank, so $X = \Gamma_i^{+} (Y - \mathcal{T}_i U)$ lies in the row space of $\begin{pmatrix} U \\ Y \end{pmatrix}$, which is contained in the row space of $\begin{pmatrix} Q_1 \\ Q_2 \end{pmatrix}$. Write $a^T X = b^T Q_1 + c^T Q_2$. Multiplying by $Q_2^T$ gives $c = 0$, so $a^T X = b^T Q_1 = b^T L_{11}^{-1} U$. By (E), the rows of $X$ and $U$ are linearly independent together, so $a = 0$. Hence $X Q_2^T$ has full row rank $n$.

The product of the full column rank matrix $\Gamma_i$ and the full row rank matrix $X Q_2^T$ has the column space of $\Gamma_i$. $\square$

**Lemma 4 (the observability factor).** L3 to L5 give $G = U_n$ with $\sigma_n > 0 = \sigma_{n+1}$, and there is a nonsingular $T$ with $G = \Gamma_i T$.

*Proof.* By Lemma 3, $L_{22}$ has rank $n$, so exactly $n$ singular values are nonzero and the first $n$ left singular vectors span the column space of $L_{22}$, which is the column space of $\Gamma_i$. So $U_n = \Gamma_i T$ for an $n \times n$ matrix $T$, and $T$ is nonsingular because $U_n$ has rank $n$. $\square$

**Lemma 5 (A and C).** L6 gives $\hat C = C T$ and L7 gives $\hat A = T^{-1} A T$.

*Proof.* The first block row of $\Gamma_i T$ is $C T$. Let $\underline{G}$ be $G$ without its last block row and $\overline{G}$ be $G$ without its first block row. Then $\underline{G} = \Gamma_{i-1} T$ and $\overline{G} = \Gamma_{i-1} A T$. Since $i - 1 \ge n$ and $(A, C)$ is observable, $\Gamma_{i-1} T$ has full column rank, so its pseudoinverse is a left inverse, and $\underline{G}^{+} \overline{G} = (\Gamma_{i-1} T)^{+} (\Gamma_{i-1} T) T^{-1} A T = T^{-1} A T$. $\square$

**Lemma 6 (x_0, B and D).** With $\hat A$ and $\hat C$ fixed, the output is linear in $(x_0, B, D)$:

$$y_k = \hat C \hat A^k \hat x_0 + \sum_{t=0}^{k-1} \hat C \hat A^{k-1-t} \hat B u_t + \hat D u_k.$$

The values $\hat x_0 = T^{-1} x_0$, $\hat B = T^{-1} B$, $\hat D = D$ give zero residual. If the regressor matrix of L8 has full column rank, the least squares solution is unique and equals these values.

*Proof.* With $\hat A = T^{-1} A T$ and $\hat C = C T$, the right side with these values is $C A^k x_0 + \sum_t C A^{k-1-t} B u_t + D u_k = y_k$. A zero-residual point is a minimizer of the sum of squares, and with full column rank the minimizer is unique. $\square$

**Theorem (noise-free case).** If $(A, C)$ is observable, $i > n$, (E) holds, the regressor of L8 has full column rank, and the order is chosen as the number of nonzero singular values of $L_{22}$, MOESP returns $(T^{-1} A T, T^{-1} B, C T, D)$ and $T^{-1} x_0$ for a nonsingular $T$. So the model has the transfer function and the output of the true system.

*Proof.* Lemmas 4, 5 and 6. $\blacksquare$

## White output noise

Now let $v_k$ be a zero-mean noise, independent of the input, with $\frac{1}{j} V V^T \to \sigma^2 I$ and $\frac{1}{j} V Z^T \to 0$ for $Z = U$ and $Z = X$, as $j \to \infty$, with probability 1. Here the state does not depend on the noise, because the noise enters only the output. Assume also that $\frac{1}{j} U U^T$, $\frac{1}{j} X U^T$ and $\frac{1}{j} X X^T$ converge, with the limit of $\frac{1}{j} \begin{pmatrix} X \\ U \end{pmatrix} \begin{pmatrix} X \\ U \end{pmatrix}^T$ positive definite. This is the limit form of (E).

**Lemma 7 (the noise only adds a multiple of the identity).** $\frac{1}{j} L_{22} L_{22}^T \to \Gamma_i M \Gamma_i^T + \sigma^2 I$, where $M$ is positive definite.

*Proof.* $L_{22} L_{22}^T = Y Q_2^T Q_2 Y^T$. The rows of $Y$ lie in the row space of $Q$, and $Q_1^T Q_1$ is the orthogonal projection onto the row space of $U$, so $Q_2^T Q_2$ acts on the rows of $Y$ as the projection $\Pi = I - U^T (U U^T)^{-1} U$ onto the orthogonal complement of the row space of $U$. Hence $L_{22} L_{22}^T = Y \Pi Y^T$, and with $\Pi U^T = 0$ and Lemma 1, $Y \Pi Y^T = (\Gamma_i X + V) \Pi (\Gamma_i X + V)^T$. Divide by $j$ and pass to the limit. $\frac{1}{j} X \Pi X^T$ tends to the Schur complement $M = R_{xx} - R_{xu} R_{uu}^{-1} R_{ux}$ of the limit covariance, which is positive definite because the whole limit matrix is. The cross terms $\frac{1}{j} X \Pi V^T$ tend to 0, and $\frac{1}{j} V \Pi V^T$ tends to $\sigma^2 I$, because the correction $\frac{1}{j} V U^T (\frac{1}{j} U U^T)^{-1} \frac{1}{j} U V^T$ tends to 0. $\square$

**Theorem (consistency of the column space).** Under these assumptions, the span of the first $n$ left singular vectors of $L_{22}$ tends to the column space of $\Gamma_i$, and the estimates of the poles tend to the true poles.

*Proof.* The left singular vectors of $L_{22}$ are the eigenvectors of $\frac{1}{j} L_{22} L_{22}^T$. For the limit matrix $\Gamma_i M \Gamma_i^T + \sigma^2 I$, every vector in the column space of $\Gamma_i$ is mapped into that space, and every vector orthogonal to it is an eigenvector with eigenvalue $\sigma^2$. On the column space of $\Gamma_i$ the eigenvalues are $\sigma^2$ plus the positive eigenvalues of $\Gamma_i M \Gamma_i^T$ there. So the $n$ dominant eigenvectors span the column space of $\Gamma_i$, with a gap above $\sigma^2$. Invariant subspaces of a symmetric matrix with such a gap depend continuously on the matrix (the Davis-Kahan theorem), so the estimate converges. Lemma 5 is continuous in $G$ at a point where $\underline{G}$ has full column rank, and the eigenvalues of $\hat A$ do not depend on the choice of $T$. $\blacksquare$

The identity in Lemma 7 needs $\frac{1}{j} V V^T \to \sigma^2 I$: the noise must be white in time and have the same variance in every output. Colored output noise or process noise adds a matrix that is not a multiple of the identity, and then the column space is biased. The PI-MOESP and PO-MOESP variants use past inputs or past outputs as instruments to remove this bias.
