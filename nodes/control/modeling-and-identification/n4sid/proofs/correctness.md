---
title: N4SID recovers the system up to similarity from noise-free data
proves: [correctness]
status: full
---

We work in exact real arithmetic, as in the real RAM, and assume that the LQ factorization, the SVD and the pseudoinverses are exact. The data come from a noise-free system

$$x_{k+1} = A x_k + B u_k, \qquad y_k = C x_k + D u_k, \qquad k = 0, \ldots, N-1,$$

with $x_k \in \mathbb{R}^n$, $u_k \in \mathbb{R}^m$, $y_k \in \mathbb{R}^p$, and $(A, B)$ controllable and $(A, C)$ observable. The number of block rows is $2i$ with $i > n$, and $j = N - 2i + 1$.

**Notation.** $U$ is the $2im \times j$ block Hankel matrix with block $(r, c)$ equal to $u_{r+c}$. $U_p$ is its first $i$ block rows (the past) and $U_f$ its last $i$ block rows (the future). $U_p^+$ is the first $i+1$ block rows and $U_f^-$ the last $i-1$ block rows. $Y$, $Y_p$, $Y_f$, $Y_p^+$, $Y_f^-$ are the same for $y$, and $W_p = \begin{pmatrix} U_p \\ Y_p \end{pmatrix}$, $W_p^+ = \begin{pmatrix} U_p^+ \\ Y_p^+ \end{pmatrix}$. $X_p = (x_0, \ldots, x_{j-1})$, $X_f = (x_i, \ldots, x_{i+j-1})$ and $X_f^+ = (x_{i+1}, \ldots, x_{i+j})$. $\Gamma_k$ stacks $C, CA, \ldots, CA^{k-1}$, $\Delta_k = (A^{k-1} B, \ldots, A B, B)$, and $\mathcal{T}_k$ is the lower block triangular Toeplitz matrix of $D$ and the Markov parameters.

For matrices $a$, $b$, $c$ with $j$ columns, $a / b^\perp = a - a b^T (b b^T)^{+} b$ removes from each row of $a$ its orthogonal projection on the row space of $b$, and the oblique projection is

$$a /_b c = (a / b^\perp)(c / b^\perp)^{+} c.$$

**Excitation condition.**

$$\operatorname{rank} \begin{pmatrix} X_p \\ U_p \\ U_f \end{pmatrix} = n + 2im. \tag{E}$$

**Lemma 1 (data equations).** $Y_p = \Gamma_i X_p + \mathcal{T}_i U_p$, $Y_f = \Gamma_i X_f + \mathcal{T}_i U_f$ and $X_f = A^i X_p + \Delta_i U_p$. The same holds with $i+1$ past and $i-1$ future block rows: $Y_f^- = \Gamma_{i-1} X_f^+ + \mathcal{T}_{i-1} U_f^-$ and $X_f^+ = A^{i+1} X_p + \Delta_{i+1} U_p^+$.

*Proof.* Iterate the state equation: $x_{k+r} = A^r x_k + \sum_{t=0}^{r-1} A^{r-1-t} B u_{k+t}$, and apply $C$ and add $D u_{k+r}$ for the outputs. Read column by column. $\square$

**Lemma 2 (the states lie in the past).** The row space of $W_p$ is the row space of $\begin{pmatrix} X_p \\ U_p \end{pmatrix}$, and the rows of $X_f$ lie in it. The row space of $W_p^+$ is the row space of $\begin{pmatrix} X_p \\ U_p^+ \end{pmatrix}$, and the rows of $X_f^+$ lie in it.

*Proof.* $\Gamma_i$ has full column rank because $i \ge n$ and $(A, C)$ is observable. By Lemma 1, $X_p = \Gamma_i^{+} (Y_p - \mathcal{T}_i U_p)$, so the rows of $X_p$ lie in the row space of $W_p$, and conversely the rows of $Y_p$ are combinations of the rows of $X_p$ and $U_p$. Then $X_f = A^i X_p + \Delta_i U_p$ lies in it too. The same argument with $i + 1$ block rows gives the second statement. $\square$

**Lemma 3 (the oblique projection).** Let $a = M c + P b$, and assume that the row spaces of $b$ and $c$ meet only in 0. Then $a /_b c = M c$.

*Proof.* Since $b / b^\perp = 0$ and the operation is linear, $a / b^\perp = M (c / b^\perp)$. Let $c' = c / b^\perp$ and let $\Pi = c' c'^{+}$, the orthogonal projection onto the column space of $c'$. Then $a /_b c = M \Pi c$, and it is enough to show $(I - \Pi) c = 0$. Let $w$ be in the range of $I - \Pi$, so $w^T c' = 0$. Then $w^T c = w^T c\, b^T (b b^T)^{+} b$ lies in the row space of $b$; it also lies in the row space of $c$, so $w^T c = 0$. Hence $c^T (I - \Pi) = 0$, and since $I - \Pi$ is symmetric, $(I - \Pi) c = 0$. $\square$

**Lemma 4 (O_i and O_(i-1)).** Under (E), the oblique projection of L3 is $O_i = \Gamma_i X_f$, and the one of L4 is $O_{i-1} = \Gamma_{i-1} X_f^+$.

*Proof.* By Lemma 2, $X_f = K W_p$ for some matrix $K$, so by Lemma 1, $Y_f = \Gamma_i K W_p + \mathcal{T}_i U_f$. By Lemma 2 and (E), the row space of $W_p$, which is that of $\begin{pmatrix} X_p \\ U_p \end{pmatrix}$, meets the row space of $U_f$ only in 0. Lemma 3 with $a = Y_f$, $b = U_f$ and $c = W_p$ gives $O_i = \Gamma_i K W_p = \Gamma_i X_f$. For $O_{i-1}$ use $Y_f^-$, $U_f^-$ and $W_p^+$: the rows of $\begin{pmatrix} X_p \\ U_p^+ \end{pmatrix}$ and of $U_f^-$ are rows of the matrix in (E), so the intersection is again 0. $\square$

**Lemma 5 (rank).** $X_f$ has full row rank $n$, and the matrix $\begin{pmatrix} X_f \\ U_{i|i} \end{pmatrix}$ has full row rank $n + m$, where $U_{i|i}$ is the block row $i$ of $U$ (the first block row of $U_f$).

*Proof.* Suppose $a^T X_f + b^T U_{i|i} = 0$. By Lemma 1, $a^T A^i X_p + a^T \Delta_i U_p + b^T U_{i|i} = 0$. These are combinations of rows of the matrix in (E), so $a^T A^i = 0$, $a^T \Delta_i = 0$ and $b = 0$. $\Delta_i$ has rank $n$ because $(A, B)$ is controllable and $i \ge n$, so $a = 0$. With $b = 0$ forced, the first statement is the special case. $\square$

**Lemma 6 (the factors).** L5 and L6 give $G = U_n \Sigma_n^{1/2} = \Gamma_i T$ for a nonsingular $T$, with $\sigma_n > 0 = \sigma_{n+1}$. Then $G_1 = \Gamma_{i-1} T$, and L7 gives $\hat X_i = T^{-1} X_f$ and $\hat X_{i+1} = T^{-1} X_f^+$.

*Proof.* By Lemmas 4 and 5, $O_i = \Gamma_i X_f$ is a product of a full column rank and a full row rank matrix, so it has rank $n$, and its column space is that of $\Gamma_i$. The first $n$ left singular vectors span this space, so $U_n = \Gamma_i S$ with $S$ nonsingular, and $T = S \Sigma_n^{1/2}$. Deleting the last block row gives $G_1 = \Gamma_{i-1} T$. Both $\Gamma_i T$ and $\Gamma_{i-1} T$ have full column rank, since $i - 1 \ge n$, so $(\Gamma_i T)^{+} = T^{-1} \Gamma_i^{+}$ is a left inverse, and the same for $i - 1$. Hence $\hat X_i = T^{-1} \Gamma_i^{+} \Gamma_i X_f = T^{-1} X_f$ and $\hat X_{i+1} = T^{-1} \Gamma_{i-1}^{+} \Gamma_{i-1} X_f^+ = T^{-1} X_f^+$. $\square$

**Lemma 7 (the regression).** The least squares problem of L8 has the unique solution

$$\theta = \begin{pmatrix} T^{-1} A T & T^{-1} B \\ C T & D \end{pmatrix},$$

and the residual of L9 is zero.

*Proof.* Column $c$ of $X_f$ is $x_{i+c}$, column $c$ of $X_f^+$ is $x_{i+c+1}$, and column $c$ of $Y_{i|i}$ is $y_{i+c}$. The system equations give, column by column,

$$\begin{pmatrix} X_f^+ \\ Y_{i|i} \end{pmatrix} = \begin{pmatrix} A & B \\ C & D \end{pmatrix} \begin{pmatrix} X_f \\ U_{i|i} \end{pmatrix}.$$

Substitute $X_f = T \hat X_i$ and $X_f^+ = T \hat X_{i+1}$ and multiply the first block row by $T^{-1}$: the stated $\theta$ solves $\begin{pmatrix} \hat X_{i+1} \\ Y_{i|i} \end{pmatrix} = \theta \begin{pmatrix} \hat X_i \\ U_{i|i} \end{pmatrix}$ exactly. By Lemma 5 the right factor has full row rank, so the solution of the least squares problem is unique, and it is this zero-residual solution. $\square$

**Lemma 8 (working on the rows of L).** Computing every step on the rows of the LQ factor $L$ instead of the rows of the data gives the same results.

*Proof.* $\begin{pmatrix} U \\ Y \end{pmatrix} = L Q$ with $Q Q^T = I$, so each data row is the matching row of $L$ times $Q$. For rows $a = a_L Q$ and $b = b_L Q$, $a b^T = a_L b_L^T$, so all inner products are the same. The projections of L3 and L4 are combinations of rows formed with these inner products, so the projection of the data rows is the projection of the $L$ rows times $Q$. If $O = O_L Q$, then $O O^T = O_L O_L^T$, so $O$ and $O_L$ have the same left singular vectors and singular values. $G^{+} O = (G^{+} O_L) Q$, so the state rows are the $L$ rows times $Q$. In L8, $(R_L Q)^{+} = Q^T R_L^{+}$, so $(S_L Q)(R_L Q)^{+} = S_L R_L^{+}$, and the residual covariance is $\frac{1}{j} (E_L Q)(E_L Q)^T = \frac{1}{j} E_L E_L^T$. $\square$

**Theorem.** Under (E), with $(A, B)$ controllable, $(A, C)$ observable, $i > n$ and the order chosen as the rank of $O_i$, N4SID returns $(T^{-1} A T, T^{-1} B, C T, D)$ for a nonsingular $T$, and a zero residual covariance.

*Proof.* By Lemma 8 the algorithm computes the same quantities as on the data rows. Lemmas 4 to 7 give the result. $\blacksquare$

**Remark (noise).** With innovation noise, $x_{k+1} = A x_k + B u_k + K e_k$ and $y_k = C x_k + D u_k + e_k$, Van Overschee and De Moor (1994) show that as $j \to \infty$, $O_i$ tends to $\Gamma_i \tilde X_i$, where $\tilde X_i$ is a sequence of Kalman filter states. The residuals of L8 then estimate the noise covariances. That proof needs probability limits and is not repeated here; the test file checks the consistency of the poles and of the output noise variance by a measurement.
