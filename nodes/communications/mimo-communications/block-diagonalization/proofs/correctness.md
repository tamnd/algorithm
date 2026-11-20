---
title: Block diagonalization removes all inter-user interference, meets the power exactly, and has the largest sum rate of all precoders with zero inter-user interference
proves: [correctness]
status: full
---

User $k$ has $N_k$ antennas and receives $y_k = H_k x + w_k$, with $H_k \in \mathbb{C}^{N_k \times M}$ and $w_k \sim \mathcal{CN}(0, N_0 I)$. The transmitter sends $x = \sum_k W_k d_k$ with independent unit-energy Gaussian symbols $d_k$, so the transmit power is $\sum_k \|W_k\|_F^2$. Let $\tilde H_k$ stack the channels $H_j$, $j \ne k$. Lines L1 to L7 compute an orthonormal basis $V_k^{(0)}$ of the null space of $\tilde H_k$ (line L2), the SVD $H_k V_k^{(0)} = U_k \Sigma_k V_k^{(1)H}$ (line L3), one water-filling over the gains $\sigma^2 / N_0$ of all users (lines L4 and L5), and $W_k = V_k^{(0)} V_k^{(1)} P_k^{1/2}$ with the first $r_k$ columns of $V_k^{(1)}$ and the diagonal power matrix $P_k$ (line L6). The proof uses exact arithmetic for the ranks.

**Lemma 1 (the null space basis).** Let $\tilde H_k = \tilde U \tilde \Sigma \tilde V^H$ with the singular values in decreasing order and rank $\rho$. The last $M - \rho$ columns of $\tilde V$ are an orthonormal basis of the null space of $\tilde H_k$.

*Proof.* $\tilde V$ is unitary, so its columns are orthonormal. For a column $v_i$ with $i > \rho$, $\tilde H_k v_i = \sigma_i \tilde u_i = 0$. The null space has dimension $M - \rho$ by the rank theorem, and these $M - \rho$ orthonormal vectors lie in it, so they span it. $\square$

If $\rho = M$, user $k$ has no null space, and the implementation raises an error. So BD needs $\mathrm{rank}(\tilde H_k) < M$ for every $k$; for generic channels this means $\sum_{j \ne k} N_j < M$.

**Theorem 1 (no inter-user interference).** $H_j W_k = 0$ for all $j \ne k$.

*Proof.* The rows of $H_j$ are rows of $\tilde H_k$, and the columns of $W_k$ are combinations of the columns of $V_k^{(0)}$, which lie in the null space of $\tilde H_k$ by Lemma 1. $\square$

So $y_k = H_k W_k d_k + w_k$: each user sees a single-user MIMO channel.

**Theorem 2 (power).** $\sum_k \|W_k\|_F^2 = P$ when at least one gain is positive.

*Proof.* $V_k^{(0)}$ and $V_k^{(1)}$ have orthonormal columns, so $V_k^{(0)} V_k^{(1)}$ has orthonormal columns too, and $\|W_k\|_F^2 = \mathrm{tr}(P_k)$. Water-filling returns powers with the sum $P$ (Lemma 1 of the [SVD precoding proof](/svd-precoding/)). $\square$

**Lemma 2 (the rate).** With $W_k$ from line L6 and the receive filter $U_k^H$, the streams of user $k$ are parallel scalar channels with gains $\sigma_{k,i}^2 p_{k,i} / N_0$, and

$$\log_2 \det\bigl(I + H_k W_k W_k^H H_k^H / N_0\bigr) = \sum_i \log_2 (1 + \sigma_{k,i}^2 p_{k,i} / N_0).$$

*Proof.* $H_k W_k = H_k V_k^{(0)} V_k^{(1)} P_k^{1/2} = U_k \Sigma_k P_k^{1/2}$ for the first $r_k$ columns, because $V_k^{(1)H} V_k^{(1)} = I$ on those columns. The columns of $U_k$ are orthonormal, so $U_k^H y_k = \Sigma_k P_k^{1/2} d_k + U_k^H w_k$ with white noise of variance $N_0$. For the determinant, use $\det(I + A B) = \det(I + B A)$ with $A = U_k$: the matrix becomes $I + \Sigma_k^2 P_k / N_0$, which is diagonal. $\square$

**Theorem 3 (best zero-interference precoder).** Among all precoders $(W_1, \ldots, W_K)$ with $H_j W_k = 0$ for $j \ne k$ and $\sum_k \|W_k\|_F^2 \le P$, BD has the largest sum rate $\sum_k \log_2 \det(I + H_k W_k W_k^H H_k^H / N_0)$.

*Proof.* Take any feasible precoder. By the condition $\tilde H_k W_k = 0$, every column of $W_k$ lies in the null space of $\tilde H_k$, so $W_k = V_k^{(0)} X_k$ for some $X_k$, by Lemma 1. Since $V_k^{(0)}$ has orthonormal columns, $\|W_k\|_F = \|X_k\|_F$. Let $G_k = H_k V_k^{(0)}$, $G = \mathrm{diag}(G_1, \ldots, G_K)$ (block diagonal) and $Q = \mathrm{diag}(X_1 X_1^H, \ldots, X_K X_K^H)$. Then the sum rate is

$$\sum_k \log_2 \det(I + G_k X_k X_k^H G_k^H / N_0) = \log_2 \det(I + G Q G^H / N_0),$$

because the determinant of a block diagonal matrix is the product of the determinants of its blocks. Also $\mathrm{tr}(Q) = \sum_k \|X_k\|_F^2 \le P$. So the sum rate is at most the maximum of $\log_2 \det(I + G Q G^H / N_0)$ over all positive semidefinite $Q$ with $\mathrm{tr}(Q) \le P$, block diagonal or not. By the capacity theorem of the [SVD precoding proof](/svd-precoding/) (Theorem 2 there), this maximum is $\sum_i \log_2 (1 + \sigma_i^2 p_i / N_0)$, where $\sigma_i$ runs over the singular values of $G$ and $p$ is the water-filling over the gains $\sigma_i^2 / N_0$. The singular values of the block diagonal $G$ are the union of those of the blocks $G_k$, which are the values of line L3. Lines L4 and L5 do exactly this water-filling, and by Lemma 2 BD reaches the bound. $\square$

**Corollary (single-antenna users).** If every $N_k = 1$, the null space precoder of user $k$ is the direction of column $k$ of $H^H (H H^H)^{-1}$, and the gain is $\sigma_k^2 = 1 / [(H H^H)^{-1}]_{kk}$, so BD is zero-forcing precoding with water-filling.

*Proof.* With $N_k = 1$, $G_k = h_k^H V_k^{(0)}$ is a row, and its only singular value is the norm of the projection of $h_k$ onto the null space of the other channels. This squared norm is $1 / [(H H^H)^{-1}]_{kk}$ by Lemma 3 of the [zero-forcing precoding proof](/zero-forcing-precoding/). $\square$

The tests check Theorem 1 within $10^{-9}$, Theorem 2 within $10^{-9}$, Lemma 1 (orthonormal basis and $\tilde H_k V_k^{(0)} = 0$), Lemma 2 against the log det rate with the other users treated as noise, the corollary, the KKT conditions of the water-filling, Theorem 3 against a grid over the power split on the example and against random precoders in the same null spaces, and the example of the page.
