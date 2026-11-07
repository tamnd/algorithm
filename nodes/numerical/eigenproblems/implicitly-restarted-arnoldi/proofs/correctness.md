---
title: Implicit restarting keeps an Arnoldi factorization and applies a polynomial filter to the start vector
proves: [correctness, termination]
status: full
---

Notation of the page: $A V_m = V_m H_m + f_m e_m^T$ is an Arnoldi factorization with $V_m^* V_m = I$, $V_m^* f_m = 0$ and $H_m$ upper Hessenberg; $v_1 = V_m e_1$; $p = m - k \ge 1$ shifts $\mu_1, \dots, \mu_p$; $Q = Q_1 \cdots Q_p$ from lines L7 and L8. Exact arithmetic.

**Lemma 1 (one shifted QR step).** Let $H$ be $m \times m$ upper Hessenberg and $H - \mu I = Q_1 R_1$ with $Q_1$ unitary and $R_1$ upper triangular, computed by Givens rotations in rows $(1, 2), (2, 3), \dots, (m - 1, m)$. Then $Q_1$ is upper Hessenberg and $H^{(1)} = Q_1^* H Q_1 = R_1 Q_1 + \mu I$ is upper Hessenberg.

*Proof.* $Q_1 = G_1^* G_2^* \cdots G_{m-1}^*$ where $G_i$ acts on rows $i, i + 1$. A product of such rotations in this order is upper Hessenberg: column $j$ of $G_1^* \cdots G_{m-1}^*$ is a combination of $e_1, \dots, e_{j+1}$. Then $R_1 Q_1$ is upper triangular times upper Hessenberg, which is upper Hessenberg, and $Q_1^* H Q_1 = Q_1^* (Q_1 R_1 + \mu I) Q_1 = R_1 Q_1 + \mu I$. $\square$

**Lemma 2 (band structure of $Q$).** $Q = Q_1 \cdots Q_p$ has $q_{ij} = 0$ for $i > j + p$. In particular $e_m^T Q e_j = 0$ for $j < k = m - p$.

*Proof.* Each $Q_i$ has lower bandwidth 1. A product of $p$ matrices of lower bandwidth 1 has lower bandwidth at most $p$, by induction: if $X$ has lower bandwidth $s$ and $Y$ has lower bandwidth 1, then $(XY)_{ij} = \sum_l x_{il} y_{lj}$ with $x_{il} = 0$ for $i > l + s$ and $y_{lj} = 0$ for $l > j + 1$, so every term vanishes when $i > j + 1 + s$. For row $m$ and column $j$, $m > j + p$ exactly when $j < m - p = k$. $\square$

**Theorem 1 (the restart keeps an Arnoldi factorization).** Let $V_m^+ = V_m Q$, $H_m^+ = Q^* H_m Q$, and let $V_k^+$, $H_k^+$ be the leading $k$ columns and the leading $k \times k$ block. Let $f_k^+ = V_m^+ e_{k+1} h^+_{k+1,k} + f_m\, q_{mk}$. Then
$$A V_k^+ = V_k^+ H_k^+ + f_k^+ e_k^T, \qquad V_k^{+*} V_k^+ = I, \qquad V_k^{+*} f_k^+ = 0,$$
and $H_k^+$ is upper Hessenberg.

*Proof.* Multiply the factorization on the right by $Q$: $A V_m^+ = V_m^+ H_m^+ + f_m e_m^T Q$. By Lemma 1, applied $p$ times, $H_m^+$ is upper Hessenberg, so column $j \le k$ of $V_m^+ H_m^+$ is $\sum_{i \le k} h^+_{ij} v_i^+$ for $j < k$, and $\sum_{i \le k} h^+_{ik} v_i^+ + h^+_{k+1,k} v^+_{k+1}$ for $j = k$. By Lemma 2, the row vector $e_m^T Q$ has zeros in columns $1, \dots, k - 1$ and the entry $q_{mk}$ in column $k$. Taking the first $k$ columns gives the stated relation. $V_m^+$ has orthonormal columns because $Q$ is unitary. Finally $v_{k+1}^+ \perp v_i^+$ for $i \le k$, and $f_m \perp \operatorname{span}(V_m) = \operatorname{span}(V_m^+) \ni v_i^+$, so $V_k^{+*} f_k^+ = 0$. $\square$

**Theorem 2 (polynomial filter).** Let $\psi(z) = \prod_{j=1}^{p} (z - \mu_j)$, and suppose no $\mu_j$ is an eigenvalue of the current $H$ at its step, so that each $R_j$ has nonzero $(1,1)$ entry. Then $V_m^+ e_1 = \psi(A) v_1 / \tau$ for a scalar $\tau \ne 0$. If $\mu_j$ are eigenvalues of $H$, the same holds as long as $\psi(A) v_1 \ne 0$, with $\tau = \prod_j (R_j)_{11}$.

*Proof.* For one shift, $(A - \mu_1 I) V_m = V_m (H_m - \mu_1 I) + f_m e_m^T = V_m Q_1 R_1 + f_m e_m^T$. Apply both sides to $e_1$ and use $m \ge 2$, so $e_m^T e_1 = 0$: $(A - \mu_1 I) v_1 = V_m Q_1 R_1 e_1 = (R_1)_{11}\, V_m Q_1 e_1$. Hence $V_m Q_1 e_1 = (A - \mu_1 I) v_1 / (R_1)_{11}$. The new factorization $A (V_m Q_1) = (V_m Q_1) H^{(1)} + f_m e_m^T Q_1$ is not an Arnoldi factorization in general, because $e_m^T Q_1$ has two nonzeros. But the same computation applies: $(A - \mu_2 I) V_m Q_1 = V_m Q_1 Q_2 R_2 + f_m e_m^T Q_1$, and $e_m^T Q_1 e_1 = 0$ when $m \ge 3$, since $Q_1$ has lower bandwidth 1. In general, $e_m^T Q_1 \cdots Q_{j-1} e_1 = 0$ when $m > j$, by Lemma 2, and $m > p \ge j$. Induction on $j$ gives $V_m Q e_1 = \prod_j (A - \mu_j I) v_1 / \prod_j (R_j)_{11}$. $\square$

**Corollary (uniqueness).** If $H_k^+$ is unreduced, the factorization of Theorem 1 is the $k$-step Arnoldi factorization from the start vector $v_1^+$, up to unimodular scaling of the columns. *Proof.* In Theorem 1 of the [Arnoldi correctness proof](/arnoldi-iteration/), the vectors $q_1, \dots, q_k$ and the entries of $H_k$ are determined by $q_1$ through the Gram-Schmidt recurrence when the subdiagonal is nonzero; an Arnoldi factorization with the same first column and a nonzero subdiagonal satisfies the same recurrence column by column, so it agrees up to phases. $\square$ Hence $\operatorname{span}(V_k^+) = K_k(A, \psi(A) v_1) = \psi(A) K_k(A, v_1)$.

**Theorem 3 (exact shifts).** Suppose $H_m$ is unreduced and has eigenvalues $\theta_1, \dots, \theta_k$ (wanted) and $\mu_1, \dots, \mu_p$ (shifts), and that the leading $(m - j) \times (m - j)$ block stays unreduced after $j$ shifts, for $j < p$. Then the eigenvalues of $H_k^+$ are $\theta_1, \dots, \theta_k$.

*Proof.* First one shift. Let $H$ be unreduced upper Hessenberg of order $s$ with eigenvalue $\mu$. Its first $s - 1$ columns are independent, because the subdiagonal is nonzero, and the same holds for $H - \mu I$. Hence the QR factorization $H - \mu I = Q_1 R_1$ has $(R_1)_{ii} \ne 0$ for $i < s$, and $(R_1)_{ss} = 0$ since $H - \mu I$ is singular. The last row of $R_1 Q_1$ is $(R_1)_{ss} e_s^T Q_1 = 0$, so $H^{(1)} = R_1 Q_1 + \mu I = \begin{pmatrix} H' & g \\ 0 & \mu \end{pmatrix}$, and $H'$ has the other $s - 1$ eigenvalues of $H$, since $H^{(1)}$ is similar to $H$.

Now the second shift $\mu_2$, an eigenvalue of $H'$, applied to the full matrix $H^{(1)}$. Rotation $i \le s - 2$ is computed from the entries $(i, i)$ and $(i + 1, i)$, which lie in the leading block, and row $s$ is zero in columns $1, \dots, s - 1$, so these rotations are exactly those of the QR step on $H' - \mu_2 I$. After them, the entry $(s - 1, s - 1)$ is $(R')_{s-1,s-1}$, which is zero by the argument above applied to the unreduced $H'$, and the entry $(s, s - 1)$ is zero. So rotation $s - 1$ is computed from $(0, 0)$ and is the identity (the implementation uses $c = 1$, $s = 0$ when $r = 0$). Therefore $Q_2 = \operatorname{diag}(Q', 1)$ and
$$H^{(2)} = Q_2^* H^{(1)} Q_2 = \begin{pmatrix} Q'^* H' Q' & Q'^* g \\ 0 & \mu_1 \end{pmatrix},$$
where $Q'^* H' Q'$ has last row $\mu_2 e_{s-1}^T$ by the one-shift case. Repeating this with the hypothesis that each new leading block is unreduced, after $p$ shifts $H_m^+ = \begin{pmatrix} H_k^+ & * \\ 0 & T \end{pmatrix}$ with $T$ upper triangular with diagonal $\mu_p, \dots, \mu_1$. So the eigenvalues of $H_k^+$ are $\theta_1, \dots, \theta_k$. $\square$

**Theorem 4 (stopping test and termination).** The quantity of line L5 equals the residual norm $\|A V_m y_i - \theta_i V_m y_i\|_2 = \|f_m\|_2 |e_m^T y_i|$, the backward error of the Ritz pair. The loop ends after at most the given maximum number of restarts, and each pass is finite, so the algorithm terminates. If line L3 breaks down at step $j < m$, the factorization $A V_j = V_j H_j$ is exact, every Ritz pair is an eigenpair, and the implementation returns them.

*Proof.* The residual identity is Theorem 3 of the Arnoldi proof, with $f_m$ in place of $h_{m+1,m} q_{m+1}$. Breakdown: by Theorem 2 of the Arnoldi proof, a zero residual means that $\operatorname{span}(V_j)$ is invariant. Termination is the explicit bound on restarts. $\square$

**What is not proved here.** Convergence of the wanted Ritz values for general $A$ is not guaranteed. Sorensen (1992) proved convergence for Hermitian $A$ with exact shifts under a nondegeneracy assumption. In floating point, the restart is a sequence of unitary transformations of the small matrices and is backward stable in the sense of the QR algorithm; loss of orthogonality of $V_m$ is controlled by the second Gram-Schmidt pass in line L3.
