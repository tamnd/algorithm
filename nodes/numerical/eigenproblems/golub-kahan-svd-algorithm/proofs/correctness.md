---
title: The Golub-Kahan step is an implicit QR step on B^T B, and the algorithm returns an SVD
proves: [correctness, termination]
status: full
---

Notation of the page. $A \in \mathbb{R}^{m \times n}$, $m \ge n$. $B$ is $n \times n$ upper bidiagonal with diagonal $d_i$ and superdiagonal $e_i$. Exact arithmetic unless stated.

**Lemma 1 (bidiagonalization).** Line L1 produces $B = U_B^T A V_B$ with orthogonal $U_B$ (its first $n$ columns are kept) and $V_B$, $B$ upper bidiagonal, and $V_B e_1 = e_1$.

*Proof.* Induction on $k$. Assume rows and columns $1, \dots, k - 1$ are in bidiagonal form. The left reflector $P_k$ acts on rows $k, \dots, m$ and maps column $k$, rows $k$ to $m$, to a multiple of $e_1$; rows $1, \dots, k - 1$ do not change, and columns $1, \dots, k - 1$ are zero in rows $k, \dots, m$, so they stay zero. The right reflector $Q_k$ acts on columns $k + 1, \dots, n$ and maps row $k$, columns $k + 1$ to $n$, to a multiple of $e_1$; columns $1, \dots, k$ do not change, so column $k$ keeps its zeros below the diagonal. Rows $1, \dots, k - 1$ are zero in columns $k + 1, \dots, n$ except $b_{k-1,k}$, which is in column $k$ and is untouched. Every $Q_k$ fixes $e_1$, so $V_B e_1 = e_1$. Products of reflectors are orthogonal. $\square$

**Lemma 2 (singular values are kept).** For orthogonal $W$, $Z$, the matrices $B$ and $W^T B Z$ have the same singular values, and $A = U_B B V_B^T$.

*Proof.* If $B = X \Sigma Y^T$ is an SVD, then $W^T B Z = (W^T X) \Sigma (Z^T Y)^T$ is one. $\square$

**Lemma 3 (the step keeps bidiagonal form).** Let $B$ be the unreduced block $p..q$, renumbered $1..r$. After lines L6 to L10, $\bar B = W^T B Z$ is upper bidiagonal, where $Z = G_1 G_2 \cdots G_{r-1}$ is the product of the right rotations and $W$ that of the left rotations.

*Proof.* The claim after the right rotation $G_k$: the only entry outside the bidiagonal pattern is at $(k + 1, k)$. After the left rotation at step $k$: the only one is at $(k, k + 2)$ (for $k < r - 1$; none for $k = r - 1$). For $k = 1$, $G_1$ mixes columns 1 and 2. Rows 1 and 2 have entries there, and row 2 gains $(2, 1) = s\, d_2 \ne 0$ in general. The left rotation on rows 1 and 2 with $(y, z) = (b_{11}, b_{21})$ zeros $(2, 1)$; row 1 gains column 3 from row 2, the entry $(1, 3)$. For $k \ge 2$, $(y, z) = (b_{k-1,k}, b_{k-1,k+1})$ and $G_k$ on columns $k, k + 1$ zeros $(k - 1, k + 1)$. Rows $k$ and $k + 1$ have entries in these columns, and $(k + 1, k)$ becomes nonzero; nothing else changes the pattern, because column $k + 1$ has nonzeros only in rows $k$ and $k + 1$. The left rotation on rows $k$, $k + 1$ then zeros $(k + 1, k)$, and row $k$ gains column $k + 2$ from row $k + 1$ when $k + 2 \le r$. At $k = r - 1$ there is no column $r + 1$, so the result is bidiagonal. $\square$

**Lemma 4 (first column).** $Z e_1$ is parallel to $(B^T B - \mu I) e_1$.

*Proof.* $T = B^T B$ is symmetric tridiagonal with $t_{11} = d_1^2$ and $t_{21} = d_1 e_1$. So $(T - \mu I) e_1 = (d_1^2 - \mu, d_1 e_1, 0, \dots)^T$, which is $(y, z, 0, \dots)$ of line L6. The rotation $G_1$ has first column $(c, s, 0, \dots)^T = (y, z, 0, \dots)^T / r$, and $G_k$ for $k \ge 2$ fixes $e_1$. Hence $Z e_1 = G_1 e_1$. $\square$

**Theorem 1 (implicit QR on $B^T B$).** Let $T = B^T B$ with $B$ unreduced and $d_i \ne 0$, and let $T - \mu I = Q R$ be a QR factorization with $T' = Q^T T Q$. Then $\bar B^T \bar B = D T' D$ for a diagonal $D$ with entries $\pm 1$, provided $T'$ is unreduced.

*Proof.* $\bar B^T \bar B = Z^T B^T W W^T B Z = Z^T T Z$, which is tridiagonal by Lemma 3 (the product of a lower and an upper bidiagonal matrix). $T$ is unreduced since $t_{i+1,i} = d_i e_i \ne 0$. Both $Z^T T Z$ and $Q^T T Q$ are tridiagonal, and $Z e_1 = \pm Q e_1$ by Lemma 4 and the first column of $T - \mu I = QR$. The implicit Q theorem for symmetric tridiagonal matrices (proved as Theorem 1 of the [Francis double-shift QR](/francis-double-shift-qr/) proof, for Hessenberg matrices) gives $Z = Q D$ when $Q^T T Q$ is unreduced. $\square$

**Lemma 5 (zero diagonal).** If $d_k = 0$ with $k < q$, the rotations of line L4 on rows $(k + 1, k), \dots, (q, k)$ make row $k$ zero and keep the bidiagonal form; if $d_q = 0$, the rotations on columns $(q - 1, q), \dots, (p, q)$ make column $q$ zero.

*Proof.* Case $k < q$. Before rotation $j$ (for $j = k + 1, \dots, q$), row $k$ has a single nonzero at column $j$, starting with $e_k$ at $j = k + 1$. The rotation of rows $j$ and $k$ with $c = b_{jj}/r$, $s = b_{kj}/r$ zeros $b_{kj}$, and it sets $b_{k,j+1} = -s\, b_{j,j+1}$. Row $j$ keeps its pattern, because row $k$ has no other nonzeros. After $j = q$, row $k$ is zero; the divisions are safe because $r \ge |b_{kj}| > 0$ when a rotation is needed. Case $d_q = 0$ is the transpose of this argument. In both cases $e_k$ or $e_{q-1}$ becomes zero and the block splits. $\square$

**Theorem 2 (correctness).** If the algorithm stops at line L11, it returns $U$, $\sigma$ and $V$ with $A = U \operatorname{diag}(\sigma) V^T$, orthonormal columns and $\sigma_1 \ge \dots \ge \sigma_n \ge 0$.

*Proof.* Every operation is an orthogonal transformation from the left or the right, applied to $B$ and accumulated into $U$ or $V$, so $A = U B V^T$ holds throughout (Lemmas 1 and 2). Line L3 goes to L11 only when every $e_i = 0$, and then $B = \operatorname{diag}(d)$. Negating column $i$ of $V$ together with $d_i$ keeps $U B V^T$. Sorting the triplets by the same permutation keeps it too. $\square$

**Theorem 3 (termination).** The algorithm terminates.

*Proof.* Each sweep of line L4 makes some $e_i$ zero, and zeros are never undone, so there are at most $n - 1$ such sweeps. Golub-Kahan steps are bounded by the cap of $40n$ in the implementation, after which it stops with an error. $\square$

**Convergence (statements).** By Theorem 1, the steps on a block are symmetric tridiagonal QR steps on $B^T B$. The shift $\mu$ is the Wilkinson shift of $B^T B$. For the Wilkinson-shifted symmetric tridiagonal QR algorithm, $t_{r,r-1} \to 0$ for every starting matrix, and the convergence is at least quadratic and generically cubic (Wilkinson 1968; Parlett, The Symmetric Eigenvalue Problem, Chapter 8). Since $t_{r,r-1} = d_{r-1} e_{r-1}$, with $d_{r-1}$ bounded away from zero, $e_{r-1}$ converges at the same rate. The count of about two steps per singular value is observed, not proved.

**Floating point (statement).** Each rotation and reflector is applied backward stably. The computed $\hat B$ and accumulated $\hat U$, $\hat V$ satisfy $\hat U_0^T (A + E) \hat V_0 = \hat B$ for exactly orthogonal $\hat U_0$, $\hat V_0$ within $c(m, n) u$ of the computed ones, and $\|E\|_2 \le c(m, n)\, u\, \|A\|_2$. Setting a negligible $e_i$ or $d_k$ to zero is a perturbation of the same size. Weyl's inequality for singular values, $|\sigma_i(A + E) - \sigma_i(A)| \le \|E\|_2$, then bounds the error in every computed singular value by $c(m, n)\, u\, \sigma_1$ (GVL Section 8.6; Demmel Section 5.4).
