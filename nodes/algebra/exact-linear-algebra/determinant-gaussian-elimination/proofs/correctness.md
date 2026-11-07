---
title: Elimination returns the determinant
proves: [correctness, termination]
status: full
---

Let $A_0$ be the input, an $n \times n$ matrix over a field $K$, and let $A$ be the working matrix. Indices start at $0$, as in the pseudocode. For $0 \le k \le n$, let $S_k$ be the submatrix of the working matrix in rows $k, \dots, n-1$ and columns $k, \dots, n-1$; $S_n$ is the $0 \times 0$ matrix, with determinant $1$.

**Claim.** DET-ELIM$(A_0)$ stops and returns $\det A_0$.

**Termination.** Line L2 runs $k$ over $n$ values, and the loops of lines L3, L7 and L9 have at most $n$ steps each. Line L4 may stop the algorithm earlier.

**Lemma.** Let $T$ be a square matrix of size $s \ge 1$ whose first column is $(t, 0, \dots, 0)^T$, and let $T'$ be $T$ without its first row and first column. Then $\det T = t \cdot \det T'$.

*Proof.* In the Leibniz formula $\det T = \sum_\sigma \operatorname{sgn}(\sigma) \prod_j T_{\sigma(j) j}$, the factor for column $1$ is $0$ unless $\sigma(1) = 1$. The permutations with $\sigma(1) = 1$ are the permutations of $\{2, \dots, s\}$, with the same sign and the same remaining factors, so the sum is $t \cdot \det T'$. $\square$

**Invariant.** At the start of the iteration of line L2 with index $k$:

$$
\det A_0 = d \cdot \det S_k. \qquad (\ast)
$$

*Initialization.* For $k = 0$, $d = 1$ and $S_0$ is the whole working matrix, which equals $A_0$.

*Maintenance.* Assume $(\ast)$ at the start of iteration $k$.

If line L3 finds no index $i \ge k$ with $A[i, k] \ne 0$, then the first column of $S_k$ is zero, so $\det S_k = 0$ (the determinant is linear in that column). By $(\ast)$, $\det A_0 = 0$, and line L4 returns $0$, which is correct.

Otherwise line L5 swaps rows $k$ and $p$ of $A$ when $p \ne k$. Both rows meet $S_k$, so this swaps two rows of $S_k$, which negates $\det S_k$. Line L5 also negates $d$, so the product $d \cdot \det S_k$ does not change. Now $A[k, k] \ne 0$.

For each $i > k$, lines L8 and L9 subtract $f = A[i, k]/A[k, k]$ times row $k$ from row $i$, in the columns $t > k$. Consider the matrix $S'_k$ that this step would give if it also updated column $k$. Adding a multiple of one row to another row does not change a determinant, so $\det S'_k = \det S_k$. In $S'_k$ the first column is $(A[k, k], 0, \dots, 0)^T$, because $A[i, k] - f A[k, k] = 0$. By the lemma, $\det S'_k = A[k, k] \cdot \det S'_{k+1}$, where $S'_{k+1}$ is $S'_k$ without its first row and column. The matrix $S'_{k+1}$ is exactly the new $S_{k+1}$, since line L9 updates all columns $t > k$ of the rows $i > k$ and line L9 never needs column $k$ again. Line L6 multiplied $d$ by $A[k, k]$. So after the iteration,

$$
d_{\text{new}} \cdot \det S_{k+1} = d \cdot A[k, k] \cdot \det S_{k+1} = d \cdot \det S_k = \det A_0,
$$

which is $(\ast)$ for $k + 1$.

*End.* If line L4 never returns, the loop ends with $k = n$. Then $S_n$ is empty with determinant $1$, so $(\ast)$ gives $\det A_0 = d$, and line L10 returns $d$. $\blacksquare$

**Remark.** The proof also shows that $d$ is, up to the sign $(-1)^s$ for $s$ swaps, the product of the pivots, and that each pivot $A[k, k]$ after step $k$ is the quotient $\det A_k / \det A_{k-1}$ of two leading principal minors of the row-permuted input. This is the fact that bounds the sizes of the numbers over $\mathbb{Q}$.
