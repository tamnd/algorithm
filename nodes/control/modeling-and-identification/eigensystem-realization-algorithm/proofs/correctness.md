---
title: ERA returns a balanced minimal realization on exact data, and the order gap survives small noise
proves: [correctness]
status: full
---

We work in exact real arithmetic, as in the real RAM, and assume that the SVD of L3 is exact. The data are $h_0, \ldots, h_{2N}$, matrices of size $p \times m$. $H$ is the $Np \times Nm$ block Hankel matrix with block $(i, j)$ equal to $h_{i+j-1}$ for $i, j = 1, \ldots, N$, and $H_s$ has block $(i, j)$ equal to $h_{i+j}$. The SVD is $H = U \Sigma V^T$ with $\sigma_1 \ge \sigma_2 \ge \cdots \ge 0$. For the chosen order $n$, $U_n$ and $V_n$ hold the first $n$ columns of $U$ and $V$, and $\Sigma_n = \operatorname{diag}(\sigma_1, \ldots, \sigma_n)$ with $\sigma_n > 0$. Write

$$P = U_n \Sigma_n^{1/2} \in \mathbb{R}^{Np \times n}, \qquad Q = \Sigma_n^{1/2} V_n^T \in \mathbb{R}^{n \times Nm}.$$

Then L6 to L8 read $A = P^{+} H_s Q^{+}$, $B = Q[:, 1{:}m]$ and $C = P[1{:}p, :]$, with $P^{+} = \Sigma_n^{-1/2} U_n^T$ and $Q^{+} = V_n \Sigma_n^{-1/2}$. Since $U_n^T U_n = I$ and $V_n^T V_n = I$, we have $P^{+} P = I$ and $Q Q^{+} = I$.

## Exact data

Assume that some system of order at most $N$ has $h_k = C A^{k-1} B$ for $k \ge 1$, let $(A_0, B_0, C_0)$ be a minimal realization of order $n_0$, and let $\mathcal{O}$ and $\mathcal{C}$ be its $N$-step observability and controllability matrices: $\mathcal{O}$ stacks $C_0 A_0^{i}$ and $\mathcal{C}$ lines up $A_0^{j} B_0$ for $i, j = 0, \ldots, N-1$.

**Lemma 1 (factorization and rank).** $H = \mathcal{O} \mathcal{C}$, $H_s = \mathcal{O} A_0 \mathcal{C}$, and $\operatorname{rank} H = n_0$. So $\sigma_{n_0} > 0 = \sigma_{n_0 + 1}$, and L4 with any threshold below $\sigma_{n_0} / \sigma_1$ chooses $n = n_0$.

*Proof.* Block $(i, j)$ of $\mathcal{O} \mathcal{C}$ is $C_0 A_0^{i-1} A_0^{j-1} B_0 = h_{i+j-1}$, and block $(i, j)$ of $\mathcal{O} A_0 \mathcal{C}$ is $h_{i+j}$. The minimal realization is controllable and observable (see [minimal realization](/minimal-realization/)). Its order is $n_0 \le N$, so by the Kalman rank condition $\mathcal{O}$ has full column rank $n_0$ and $\mathcal{C}$ has full row rank $n_0$. The product of an injective map and a surjective map through $\mathbb{R}^{n_0}$ has rank $n_0$. The number of nonzero singular values is the rank. $\square$

From now on $n = n_0$.

**Lemma 2 (the SVD factors are the system factors in new coordinates).** There is a nonsingular $n \times n$ matrix $T$ with $P = \mathcal{O} T$ and $Q = T^{-1} \mathcal{C}$.

*Proof.* Since $\sigma_{n+1} = 0$, the truncated SVD is exact: $H = U_n \Sigma_n V_n^T = P Q$. The column space of $H$ is the column space of $U_n$, and by Lemma 1 it is also the column space of $\mathcal{O}$, because $\mathcal{C}$ is onto. So $U_n = \mathcal{O} G$ for some $n \times n$ matrix $G$, and $P = \mathcal{O} T$ with $T = G \Sigma_n^{1/2}$. $P$ has rank $n$, so $T$ is nonsingular. Now $\mathcal{O} T Q = P Q = H = \mathcal{O} \mathcal{C}$, and $\mathcal{O}$ has full column rank, so $T Q = \mathcal{C}$. $\square$

**Lemma 3 (the result is a minimal realization).** $A = T^{-1} A_0 T$, $B = T^{-1} B_0$ and $C = C_0 T$. Hence $C A^{k-1} B = h_k$ for every $k \ge 1$, and with $D = h_0$ from L9 the result is a minimal realization.

*Proof.* By Lemmas 1 and 2, $A = P^{+} \mathcal{O} A_0 \mathcal{C} Q^{+} = P^{+} P \, T^{-1} A_0 T \, Q Q^{+} = T^{-1} A_0 T$. The first block column of $\mathcal{C}$ is $B_0$, so $B = Q[:, 1{:}m] = T^{-1} B_0$. The first block row of $\mathcal{O}$ is $C_0$, so $C = P[1{:}p, :] = C_0 T$. Then $C A^{k-1} B = C_0 A_0^{k-1} B_0 = h_k$. The order is $n_0$, the minimal order. $\square$

**Lemma 4 (balanced on the data window).** Let $\mathcal{O}_r$ and $\mathcal{C}_r$ be the $N$-step observability and controllability matrices of the result $(A, B, C)$. Then $\mathcal{O}_r^T \mathcal{O}_r = \mathcal{C}_r \mathcal{C}_r^T = \Sigma_n$.

*Proof.* $C A^{i} = C_0 A_0^{i} T$, so $\mathcal{O}_r = \mathcal{O} T = P$. $A^{j} B = T^{-1} A_0^{j} B_0$, so $\mathcal{C}_r = T^{-1} \mathcal{C} = Q$. Then $P^T P = \Sigma_n^{1/2} U_n^T U_n \Sigma_n^{1/2} = \Sigma_n$ and $Q Q^T = \Sigma_n^{1/2} V_n^T V_n \Sigma_n^{1/2} = \Sigma_n$. $\square$

The two products are the $N$-step observability and controllability gramians of the result. They are equal and diagonal, which is the definition of a balanced realization over the window of $N$ steps. If $A_0$ is Schur, they converge to the infinite gramians as $N \to \infty$.

**Theorem (exact data).** If the data have a realization of order at most $N$ and $n$ is the rank of $H$, ERA returns a minimal realization of the data whose $N$-step gramians are both $\Sigma_n$.

*Proof.* Lemmas 1, 3 and 4. $\blacksquare$

## Noisy data

**Lemma 5 (Weyl's inequality for singular values).** For matrices $X$ and $E$ of the same size, $|\sigma_k(X + E) - \sigma_k(X)| \le \lVert E \rVert_2$ for every $k$, where $\lVert \cdot \rVert_2$ is the induced 2-norm.

*Proof.* By the Courant-Fischer theorem, $\sigma_k(X) = \max_{\dim W = k} \min_{w \in W, \lVert w \rVert = 1} \lVert X w \rVert$. For each unit $w$, $\lVert (X + E) w \rVert \ge \lVert X w \rVert - \lVert E \rVert_2$. Take the subspace $W$ that attains the maximum for $X$; then $\sigma_k(X + E) \ge \sigma_k(X) - \lVert E \rVert_2$. Exchange the roles of $X$ and $X + E$ for the other inequality. $\square$

**Theorem (the gap survives noise).** Let the measured parameters be $h_k + e_k$, and let $E$ be the block Hankel matrix of the $e_k$. If $\lVert E \rVert_2 < \sigma_n(H) / 2$, where $n$ is the rank of the noise-free $H$, then the singular values of the measured Hankel matrix satisfy $\sigma_n > \sigma_n(H)/2 > \sigma_{n+1}$. So the gap after the $n$-th singular value shows the true order.

*Proof.* By Lemma 5, $\sigma_n(H + E) \ge \sigma_n(H) - \lVert E \rVert_2 > \sigma_n(H)/2$ and $\sigma_{n+1}(H + E) \le \sigma_{n+1}(H) + \lVert E \rVert_2 = \lVert E \rVert_2 < \sigma_n(H)/2$. $\blacksquare$

Near data with $\sigma_n > \sigma_{n+1}$, the dominant singular subspaces depend continuously on the data (Wedin's theorem). The factors $U_n$ and $V_n$ are fixed only up to an orthogonal change of basis, which changes $A$ by a similarity, so the eigenvalues of $A$ depend continuously on the data. So for small enough noise the eigenvalues of $A$ are close to the true poles. This is a statement about the limit of small noise; it gives no bias bound for a fixed noise level.
