---
title: The Ho-Kalman algorithm returns a minimal realization of the Markov parameters
proves: [correctness]
status: full
---

We work in exact arithmetic, as in the real RAM (the implementation uses Fraction). The data are $h_0, h_1, \ldots, h_{2N}$, matrices of size $p \times m$. The precondition is that some system $(A_0, B_0, C_0)$ of order $n_0 \le N$ has $h_k = C_0 A_0^{k-1} B_0$ for every $k \ge 1$. Let $n$ be the minimal order of a realization of the sequence $(h_k)_{k \ge 1}$.

For a system $(A_0, B_0, C_0)$ of order $n_0$ write the $N$-step observability and controllability matrices

$$\mathcal{O} = \begin{pmatrix} C_0 \\ C_0 A_0 \\ \vdots \\ C_0 A_0^{N-1} \end{pmatrix} \in \mathbb{R}^{Np \times n_0}, \qquad \mathcal{C} = \begin{pmatrix} B_0 & A_0 B_0 & \cdots & A_0^{N-1} B_0 \end{pmatrix} \in \mathbb{R}^{n_0 \times Nm}.$$

$H$ is the $Np \times Nm$ block Hankel matrix of L1, with block $(i, j)$ equal to $h_{i+j+1}$ for $0 \le i, j \le N-1$. $H_s$ is the shifted matrix of L2, with block $(i, j)$ equal to $h_{i+j+2}$. Both use only $h_1, \ldots, h_{2N}$.

**Lemma 1 (factorization).** For every realization $(A_0, B_0, C_0)$ of the sequence, $H = \mathcal{O} \mathcal{C}$ and $H_s = \mathcal{O} A_0 \mathcal{C}$.

*Proof.* Block $(i, j)$ of $\mathcal{O} \mathcal{C}$ is $C_0 A_0^{i} A_0^{j} B_0 = C_0 A_0^{i+j} B_0 = h_{i+j+1}$. Block $(i, j)$ of $\mathcal{O} A_0 \mathcal{C}$ is $C_0 A_0^{i+j+1} B_0 = h_{i+j+2}$. $\square$

**Lemma 2 (the rank is the minimal order).** $\operatorname{rank} H = n$.

*Proof.* The precondition gives a realization of order at most $N$, so $n \le N$. Take a minimal realization $(A_0, B_0, C_0)$ of order $n$. A minimal realization is controllable and observable (the [minimal realization](/minimal-realization/) theorem; otherwise the Kalman decomposition gives a realization of smaller order with the same Markov parameters). By the Kalman rank condition, the matrices with $n$ block rows and $n$ block columns already have rank $n$, and $N \ge n$, so $\mathcal{O}$ has full column rank $n$ and $\mathcal{C}$ has full row rank $n$. For such a product, $\operatorname{rank} \mathcal{O} \mathcal{C} = n$: the map $\mathcal{C}$ is onto $\mathbb{R}^n$ and $\mathcal{O}$ is one to one. With Lemma 1, $\operatorname{rank} H = n$. $\square$

From now on fix this minimal realization, so $\mathcal{O}$ is $Np \times n$ and $\mathcal{C}$ is $n \times Nm$.

**Lemma 3 (the selected blocks are invertible).** L3 returns a set $J$ of $n$ column indices with $H[:, J]$ of rank $n$, and L4 returns a set $I$ of $n$ row indices with $M = H[I, J]$ nonsingular. Let $T = \mathcal{C}[:, J]$ and $S = \mathcal{O}[I, :]$, both $n \times n$. Then $M = S T$, and $S$ and $T$ are nonsingular.

*Proof.* The routine of L3 is Gaussian elimination: it keeps column $j$ exactly when column $j$ is not a linear combination of the columns kept before it. The kept columns are linearly independent, and every other column is a combination of them, so they span the column space and there are $\operatorname{rank} H = n$ of them (Lemma 2). L4 applies the same routine to the rows of the $Np \times n$ matrix $H[:, J]$, which has rank $n$, so it returns $n$ rows that form a nonsingular $n \times n$ matrix $M$. By Lemma 1, $H[:, J] = \mathcal{O} T$ and $M = H[I, J] = S T$. Since $M$ is nonsingular, $\det S \det T \ne 0$. $\square$

**Lemma 4 (the result is similar to the minimal realization).** The matrices of L6 to L8 are $A = T^{-1} A_0 T$, $B = T^{-1} B_0$ and $C = C_0 T$.

*Proof.* By Lemma 1, $H_s[I, J] = \mathcal{O}[I, :] A_0 \mathcal{C}[:, J] = S A_0 T$. So L6 gives $A = M^{-1} H_s[I, J] = T^{-1} S^{-1} S A_0 T = T^{-1} A_0 T$. The first $m$ columns of $H$ are $\mathcal{O} B_0$, because the first block column of $\mathcal{C}$ is $B_0$. So L7 gives $B = M^{-1} H[I, 0{:}m] = T^{-1} S^{-1} S B_0 = T^{-1} B_0$. The first $p$ rows of $H$ are $C_0 \mathcal{C}$, because the first block row of $\mathcal{O}$ is $C_0$. So L8 gives $C = C_0 \mathcal{C}[:, J] = C_0 T$. $\square$

**Theorem.** Under the precondition, the Ho-Kalman algorithm returns $(A, B, C, D)$ of order $n$, the minimal order, with $C A^{k-1} B = h_k$ for every $k \ge 1$ (also for $k > 2N$) and $D = h_0$.

*Proof.* By Lemma 4, $C A^{k-1} B = C_0 T \, T^{-1} A_0^{k-1} T \, T^{-1} B_0 = C_0 A_0^{k-1} B_0 = h_k$ for every $k \ge 1$. L9 sets $D = h_0$. The order is $|J| = n$ by Lemma 3, and no realization has a smaller order by the definition of $n$. $\blacksquare$

**Remark (uniqueness).** Any two minimal realizations are similar (the minimal realization theorem), so the result differs from every other minimal realization by a change of state coordinates. The choice of $J$ and $I$ only selects the coordinates: the state of the result is $T^{-1}$ times the state of $(A_0, B_0, C_0)$.

**Remark (the precondition).** Without a realization of order at most $N$, the rank of $H$ can be smaller than the minimal order of the whole sequence, and Lemma 2 fails. Example: $A_0 = \operatorname{diag}(1/2, -1/2)$, $B_0 = (1, 1)^T$, $C_0 = (1, 1)$ has $h_1 = 2$, $h_2 = 0$, $h_3 = 1/2$. With $N = 1$ the algorithm returns the order 1 system $A = 0$, $B = 1$, $C = 2$. It matches $h_1$ and $h_2$, but it gives $0$ for $h_3$. The test test_too_few_block_rows_fails checks this case.
