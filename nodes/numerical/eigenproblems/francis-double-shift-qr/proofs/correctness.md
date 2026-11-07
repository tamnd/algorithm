---
title: The Francis step equals an explicit double-shift QR step and keeps Hessenberg form
proves: [correctness, termination]
status: full
---

Notation of the page: $H \in \mathbb{R}^{p \times p}$ is the window of the algorithm, renumbered $1, \dots, p$, upper Hessenberg and unreduced, $p \ge 3$. $M = H^2 - s H + t I = (H - \mu_1 I)(H - \mu_2 I)$ with $s = \mu_1 + \mu_2$ and $t = \mu_1 \mu_2$ real. Exact arithmetic unless stated.

**Lemma 1 (first column of $M$).** $M e_1 = (x, y, z, 0, \dots, 0)^T$ with $x$, $y$ and $z$ as in line L1.

*Proof.* $H e_1 = (h_{11}, h_{21}, 0, \dots)^T$ since $H$ is Hessenberg. Then $H^2 e_1 = h_{11} H e_1 + h_{21} H e_2$ and $H e_2 = (h_{12}, h_{22}, h_{32}, 0, \dots)^T$, so $H^2 e_1 = (h_{11}^2 + h_{21} h_{12},\ h_{21} (h_{11} + h_{22}),\ h_{21} h_{32},\ 0, \dots)^T$. Subtract $s H e_1$ and add $t e_1$. $\square$

**Lemma 2 (the bulge chase keeps Hessenberg form).** Let $P_1$ be the reflector of line L3 at $k = 1$, acting on coordinates $1, 2, 3$, and $P_k$ for $k = 2, \dots, p - 2$ act on coordinates $k, k + 1, k + 2$, and $P_{p-1}$ on $p - 1, p$, chosen as in lines L3 and L6 from column $k - 1$ of the current matrix. Then $H' = Z^T H Z$ with $Z = P_1 \cdots P_{p-1}$ is upper Hessenberg.

*Proof.* Write $H^{(k)}$ for the matrix after $P_1, \dots, P_k$. Claim: for $1 \le k \le p - 2$, $H^{(k)}$ is upper Hessenberg except for the entries $(k + 2, k)$, $(k + 3, k)$ and $(k + 3, k + 1)$ (those that exist), the bulge. For $k = 1$: $P_1 H$ mixes rows 1 to 3, so it is Hessenberg except that row 3 may be nonzero in column 1. Then $(P_1 H) P_1$ mixes columns 1 to 3; rows 1 to 4 can be nonzero there, since $h_{43} \ne 0$ enters columns 1 and 2. So the nonzeros below the subdiagonal are at $(3, 1)$, $(4, 1)$ and $(4, 2)$. For the step $k - 1 \to k$ with $2 \le k \le p - 2$, line L5 takes $(x, y, z)$ from column $k - 1$, rows $k$, $k + 1$, $k + 2$. $P_k$ maps this vector to a multiple of $e_1$ in its coordinates, so in $P_k H^{(k-1)}$ column $k - 1$ has zeros in rows $k + 1$ and $k + 2$; rows outside $k, k + 1, k + 2$ do not change. Right multiplication by $P_k$ mixes columns $k$, $k + 1$, $k + 2$, which does not touch column $k - 1$, and it creates nonzeros in rows up to $k + 3$, because $h_{k+3,k+2} \ne 0$. So the bulge is now at $(k + 2, k)$, $(k + 3, k)$ and $(k + 3, k + 1)$. At $k = p - 2$ there is no row $p + 1$, so the bulge is only the entry $(p, p - 2)$. Finally $P_{p-1}$ from line L6 zeros $(p, p - 2)$ using rows $p - 1$ and $p$, and right multiplication mixes columns $p - 1$ and $p$, which keeps the Hessenberg form. $\square$

**Lemma 3 ($Z e_1$ is parallel to $M e_1$).** $Z e_1 = P_1 e_1 = \pm M e_1 / \|M e_1\|_2$.

*Proof.* For $k \ge 2$, $P_k$ acts on coordinates $k$ and higher, so $P_k e_1 = e_1$. Hence $Z e_1 = P_1 P_2 \cdots P_{p-1} e_1 = P_1 e_1$. A Householder reflector is symmetric and orthogonal, so $P_1 w = \alpha e_1$ with $w = M e_1$ and $|\alpha| = \|w\|_2$ gives $P_1 e_1 = w / \alpha$. By Lemma 1, $M e_1$ has nonzeros only in the first three positions, so the reflector of order 3 suffices. $M e_1 \ne 0$ because $z = h_{21} h_{32} \ne 0$ in an unreduced $H$. $\square$

**Theorem 1 (implicit Q theorem).** Let $Z$ and $W$ be orthogonal with $Z e_1 = W e_1$, and suppose $G = Z^T H Z$ and $F = W^T H W$ are upper Hessenberg and $F$ is unreduced. Then $Z e_j = \pm W e_j$ for all $j$, and $|g_{ij}| = |f_{ij}|$.

*Proof.* Let $V = W^T Z$, orthogonal with $V e_1 = e_1$, and $F V = W^T H Z = V G$. Compare column $j$: $F v_j = \sum_{i \le j + 1} g_{ij} v_i$, so $g_{j+1,j} v_{j+1} = F v_j - \sum_{i \le j} g_{ij} v_i$. By induction, $v_1, \dots, v_j \in \operatorname{span}(e_1, \dots, e_j)$, and since $F$ is Hessenberg, $F v_j \in \operatorname{span}(e_1, \dots, e_{j+1})$, so $g_{j+1,j} v_{j+1} \in \operatorname{span}(e_1, \dots, e_{j+1})$. Also $v_{j+1} \perp v_1, \dots, v_j$, which span $\operatorname{span}(e_1, \dots, e_j)$, so $g_{j+1,j} v_{j+1}$ is a multiple of $e_{j+1}$. It is nonzero: its $e_{j+1}$ component is $e_{j+1}^T F v_j = f_{j+1,j} (e_j^T v_j)$, and $e_j^T v_j = \pm 1$ by induction, while $f_{j+1,j} \ne 0$. Hence $v_{j+1} = \pm e_{j+1}$ and $V = D$ is diagonal with entries $\pm 1$. Then $G = D F D$. $\square$

**Theorem 2 (the step is the explicit double step).** Let $M = W R$ be a QR factorization. Then $W^T H W$ is upper Hessenberg, $W e_1 = \pm M e_1 / \|M e_1\|_2$, and if $W^T H W$ is unreduced, the Francis step gives $Z^T H Z = D (W^T H W) D$ with $D = \operatorname{diag}(\pm 1)$.

*Proof.* $W e_1 = M e_1 / r_{11}$ from the first column of $M = WR$. $M$ commutes with $H$, so $W^T H W = W^T H M R^{-1} = W^T M H R^{-1} = R H R^{-1}$ when $M$ is nonsingular; a triangular times Hessenberg times triangular matrix is Hessenberg. (If $M$ is singular, that is, a shift is an eigenvalue, the same holds by a limit argument or by the direct construction in GVL Section 7.5.) By Lemmas 2 and 3, $Z$ has the same first column up to sign and $Z^T H Z$ is Hessenberg. Theorem 1 gives the claim. $\square$

**Theorem 3 (equal to two single steps).** For complex shifts, let $H - \mu_1 I = W_1 R_1$, $H_1 = W_1^* H W_1$, $H_1 - \mu_2 I = W_2 R_2$, $H_2 = W_2^* H_1 W_2$. Then $(W_1 W_2)(R_2 R_1) = M$, so $H_2$ is the explicit double step with $W = W_1 W_2$ up to a unitary diagonal factor.

*Proof.* $W_1 W_2 R_2 R_1 = W_1 (H_1 - \mu_2 I) R_1 = (H - \mu_2 I) W_1 R_1 = (H - \mu_2 I)(H - \mu_1 I) = M$, using $W_1 H_1 = H W_1$. QR factorizations are unique up to a unitary diagonal factor when $M$ is nonsingular. $\square$

**Theorem 4 (deflation and termination).** Setting $h_{l,l-1} = 0$ in line L8 is an exact similarity of $H + E$ with $\|E\|_2 \le u (|h_{l-1,l-1}| + |h_{ll}|) \le 2u \|H\|_2$. The algorithm terminates.

*Proof.* The change is one entry of the stated size. For termination: each Francis step is a finite sequence of operations. Line L9 removes one or two rows from the active part each time it applies, and it applies at least once every 30 steps, or the implementation stops with an error. The number of rows is $n$, so at most $30n$ steps run. $\square$

**Convergence (statements).** Theorem 3 makes each Francis step two shifted QR steps, so the convergence theory of the shifted QR algorithm applies: the QR iteration is subspace iteration with $M$ on nested subspaces, and inverse subspace iteration on the trailing ones. When the shifts are the eigenvalues of the trailing $2 \times 2$ block and that block converges to one with simple eigenvalues distinct from the rest of the spectrum, $h_{p-1,p-2}$ converges to zero quadratically (Watkins and Elsner 1991; GVL Section 7.5). Global convergence is not proved. The cyclic permutation matrix is a fixed point up to signs of the step with the shifts $0, 0$, which is why line L10 uses exceptional shifts.

**Floating point (statement).** Each reflector is applied backward stably, and Hessenberg structure is enforced by setting entries known to be zero to zero. Wilkinson's analysis of sequences of Householder similarities gives $\hat T = \hat Q^T (A + E) \hat Q$ with $\hat Q$ exactly orthogonal, $\|E\|_2 \le c(n)\, u\, \|A\|_2$ for a modest $c(n)$, and a computed $Q$ within $c(n) u$ of $\hat Q$ (GVL Section 7.5; Wilkinson 1965, Chapter 8).
