---
title: Householder QR produces an orthogonal Q and an upper triangular R with A = Q R
proves: [correctness, termination]
status: full
---

$A \in \mathbb{R}^{m \times n}$ with $m \ge n \ge 1$. Each loop has a fixed length, so the algorithm stops after $n$ steps.

## The reflection

**Lemma 1.** For $v \ne 0$ and $\beta = 2/(v^T v)$, the matrix $H = I - \beta v v^T$ is symmetric and orthogonal.

*Proof.* $H^T = H$ is clear. $H^T H = H^2 = I - 2\beta v v^T + \beta^2 v (v^T v) v^T = I - 2\beta v v^T + 2\beta v v^T = I$, using $\beta\, v^T v = 2$. $\square$

**Lemma 2.** Let $a \in \mathbb{R}^p$ be nonzero, $\alpha = -\operatorname{sign}(a_1)\|a\|_2$ with $\operatorname{sign}(0) = 1$, and $v = a - \alpha e_1$. Then $v \ne 0$ and $H a = \alpha e_1$.

*Proof.* $v_1 = a_1 - \alpha = a_1 + \operatorname{sign}(a_1)\|a\|_2$, and both terms have the same sign with $\|a\|_2 > 0$, so $|v_1| \ge \|a\|_2 > 0$. Next, $v^T v = \|a\|_2^2 - 2\alpha a_1 + \alpha^2 = 2(\|a\|_2^2 - \alpha a_1)$ because $\alpha^2 = \|a\|_2^2$, and $v^T a = \|a\|_2^2 - \alpha a_1$. So $\beta\, v^T a = 1$ and $H a = a - v = \alpha e_1$. $\square$

## The algorithm

**Invariant.** Before step $k$ the array holds $A^{(k)} = H_{k-1} \cdots H_1 A$, where $H_j = \operatorname{diag}(I_{j-1}, \tilde H_j)$ and $\tilde H_j$ is the reflection of step $j$ (the identity if the active column was zero). The first $k - 1$ columns of $A^{(k)}$ are zero below the diagonal.

*Proof by induction on $k$.* For $k = 1$ there is nothing to show. At step $k$, if $a^{(k)}_{k:m,k} = 0$, then $H_k = I$ and the claim for $k + 1$ holds since column $k$ is already zero below the diagonal. Otherwise lines L2 and L3 build $v$ and $\beta$ as in Lemma 2 for $a = a^{(k)}_{k:m,k}$, and line L5 records the result $\alpha e_1$ of Lemma 2 in column $k$. Line L4 applies $\tilde H_k$ to rows $k, \ldots, m$ of the columns $j > k$: $a_{k:m,j} - \beta v (v^T a_{k:m,j}) = \tilde H_k a_{k:m,j}$. Rows $1, \ldots, k - 1$ are not touched, which is the action of $H_k = \operatorname{diag}(I_{k-1}, \tilde H_k)$. Columns $1, \ldots, k - 1$ are zero in rows $k, \ldots, m$, so $H_k$ leaves them unchanged and they stay zero below the diagonal. So the array is $H_k A^{(k)} = A^{(k+1)}$, with columns $1, \ldots, k$ zero below the diagonal. $\square$

**Theorem.** After step $n$, $R = H_n \cdots H_1 A$ is upper triangular and $A = Q R$ with $Q = H_1 H_2 \cdots H_n$ orthogonal.

*Proof.* By the invariant with $k = n + 1$, all $n$ columns are zero below the diagonal. Each $H_k$ is orthogonal and symmetric by Lemma 1, so $Q = H_1 \cdots H_n$ is orthogonal and $Q^T = H_n \cdots H_1$. Then $Q^T A = R$, and $A = Q R$. $\blacksquare$

**Least squares.** If $A$ has full column rank, then $R_1$ (the top $n \times n$ block) is nonsingular, because $R_1^T R_1 = R^T R = A^T Q Q^T A = A^T A$ is positive definite. For each $x$, $\|b - A x\|_2 = \|Q^T b - R x\|_2$ because $Q^T$ preserves the 2-norm, and with $Q^T b = (c_1, c_2)$ this equals $(\|c_1 - R_1 x\|_2^2 + \|c_2\|_2^2)^{1/2}$. It is minimized exactly when $R_1 x = c_1$. If some $r_{kk} = 0$ then $\det(A^T A) = \prod r_{kk}^2 = 0$, so $A$ is rank deficient; the implementation reports this case.

## Floating point

Higham (Section 19.3) proves that the computed $\hat R$ satisfies $A + \Delta A = Q \hat R$ for the exactly orthogonal $Q = H_1 \cdots H_n$ built from the exact reflectors of the computed columns, with $\|\Delta a_j\|_2 \le \tilde\gamma_{mn}\|a_j\|_2$. The idea is that each computed application $\mathrm{fl}(\tilde H_k y)$ equals $\tilde H_k (y + \Delta y)$ with $\|\Delta y\|_2 \le \tilde\gamma_m \|y\|_2$, because the computed $\hat v$ is close to the exact $v$ relative to its norm (thanks to the sign choice of line L2), and an orthogonal map does not change the size of a perturbation. Accumulating $n$ such steps, each of relative size $\tilde\gamma_m$ in the 2-norm of the column, gives $\tilde\gamma_{mn}$. The tests measure $\|A - \hat Q \hat R\|_F/\|A\|_F$ and $\|\hat Q^T \hat Q - I\|_F$ exactly and check them against $4 m n u$.
