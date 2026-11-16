---
title: The decomposition returns the unique K, R and t of a finite camera
proves: [correctness]
status: full
---

We use the notation of the page. The input is a real $3 \times 4$ matrix $P = [M \mid p_4]$ with $\det M \ne 0$. A matrix $K$ is an intrinsic matrix if it is upper triangular with a positive diagonal and $K_{33} = 1$. A rotation is a real $3 \times 3$ matrix $R$ with $R^{\mathsf T} R = I$ and $\det R = +1$.

**Claim.** DECOMPOSE-CAMERA$(P)$ returns an intrinsic matrix $K$, a rotation $R$, a vector $t$ and the point $C = -R^{\mathsf T} t$, such that $P = \lambda K [R \mid t]$ for some real $\lambda \ne 0$ and $P (C, 1)^{\mathsf T} = 0$. Moreover, these $K$, $R$ and $t$ are the only ones with this property.

**Lemma 1 (RQ).** Every real square matrix $A$ can be written $A = U Q$ with $U$ upper triangular and $Q$ orthogonal.

*Proof.* Let $J$ be the reversal matrix, with ones on the anti-diagonal, so $J = J^{\mathsf T} = J^{-1}$. Take a QR factorization $(J A)^{\mathsf T} = Q_1 U_1$, with $Q_1$ orthogonal and $U_1$ upper triangular; it exists for every real square matrix, for example by Householder reflections. Then $J A = U_1^{\mathsf T} Q_1^{\mathsf T}$, so $A = (J U_1^{\mathsf T} J)(J Q_1^{\mathsf T})$. The matrix $J U_1^{\mathsf T} J$ is upper triangular, because $U_1^{\mathsf T}$ is lower triangular and conjugation by $J$ reverses the order of both the rows and the columns. The matrix $J Q_1^{\mathsf T}$ is orthogonal as a product of orthogonal matrices. $\square$

**Lemma 2.** An orthogonal upper triangular matrix is diagonal, with diagonal entries $\pm 1$.

*Proof.* If $U$ is upper triangular and invertible, $U^{-1}$ is upper triangular. If $U$ is also orthogonal, $U^{-1} = U^{\mathsf T}$ is lower triangular. So $U^{-1}$ is diagonal, and then $U$ is diagonal. A diagonal orthogonal matrix has entries $d$ with $d^2 = 1$. $\square$

**Existence.** Let $\sigma = \operatorname{sign}(\det M) \in \{+1, -1\}$. After line L3, the algorithm works with $\sigma P = [M' \mid p_4']$, and $\det M' = \sigma^3 \det M = |\det M| > 0$. Line L4 gives $M' = K Q$ by Lemma 1. Since $\det M' \ne 0$, every diagonal entry of $K$ is nonzero. Line L5 multiplies $K$ on the right and $Q$ on the left by $D = \operatorname{diag}(d_1, d_2, d_3)$ with $d_i = \operatorname{sign}(K_{ii})$. Because $D^2 = I$, the product is unchanged: $M' = (K D)(D Q)$. Now $K D$ is upper triangular with a positive diagonal, and $R = D Q$ is orthogonal. Its determinant is $\det M' / \det(K D)$, a quotient of two positive numbers, and it is $\pm 1$, so $\det R = +1$ and $R$ is a rotation. Write $K$ for $K D$ from now on.

Line L6 sets $t = K^{-1} p_4'$, so $K [R \mid t] = [K R \mid p_4'] = \sigma P$. Line L7 divides $K$ by $k = K_{33} > 0$; call the result $\hat K$, which is an intrinsic matrix. Then $P = \sigma k\, \hat K [R \mid t]$, which is the claim with $\lambda = \sigma k \ne 0$. Line L8 sets $C = -R^{\mathsf T} t$, so $R C + t = 0$ and $P (C, 1)^{\mathsf T} = \lambda \hat K (R C + t) = 0$.

**Uniqueness.** Suppose that $P = \lambda_1 K_1 [R_1 \mid t_1] = \lambda_2 K_2 [R_2 \mid t_2]$, with $K_1, K_2$ intrinsic matrices, $R_1, R_2$ rotations and $\lambda_1, \lambda_2 \ne 0$. Let $\mu = \lambda_1 / \lambda_2$. The left blocks give $\mu K_1 R_1 = K_2 R_2$, so
$$U = \mu\, K_2^{-1} K_1 = R_2 R_1^{\mathsf T}.$$
The middle term is upper triangular, and the right term is orthogonal. By Lemma 2, $U$ is diagonal with entries $\pm 1$. The diagonal of $K_2^{-1} K_1$ is positive (it is the quotient of the diagonals), so all diagonal entries of $U$ have the sign of $\mu$, and $U = \pm I$. Since $\det U = \det R_2 \det R_1^{\mathsf T} = +1$, $U = I$. So $R_1 = R_2$ and $K_1 = K_2 / \mu$. The $(3,3)$ entries are both 1, so $\mu = 1$ and $K_1 = K_2$. Finally the last columns give $K_1 t_1 = K_2 t_2$, so $t_1 = t_2$. $\square$

**Remark (degenerate input).** If $\det M = 0$, then no factorization $P = \lambda K [R \mid t]$ exists, because $\det(\lambda K R) = \lambda^3 \det K \ne 0$. Line L2 reports this case. The center is then a point at infinity, as for an affine camera.
