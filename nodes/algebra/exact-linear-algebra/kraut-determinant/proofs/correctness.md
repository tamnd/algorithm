---
title: Crout's method returns the determinant
proves: [correctness, termination]
status: full
---

Let $A_0$ be the input, an $n \times n$ matrix over a field $K$, and let $A$ be the working matrix. Indices start at $0$, as in the pseudocode. Line L6 swaps whole rows of $A$; let $A'$ be $A_0$ with the same swaps applied, so that $A'$ is the input with its rows in the current order. The working matrix stores two triangular matrices. For $k \le i$, $L[i, k]$ means $A[i, k]$ after line L3 of iteration $k$ has written it. For $k < t$, $U[k, t]$ means $A[k, t]$ after line L7 of iteration $k$ has written it, and $U[k, k] = 1$.

**Claim.** KRAUT-DET$(A_0)$ stops and returns $\det A_0$. If it does not return on line L5, then $A' = LU$ with $L$ lower triangular and $U$ unit upper triangular.

**Termination.** Line L2 runs $j$ over $n$ values, and every inner loop and every sum on lines L3 and L7 has at most $n$ terms.

**Which entries hold what.** An entry $A[i, j]$ with $i \ge j$ is written only by line L3 in iteration $j$, and an entry $A[j, t]$ with $t > j$ only by line L7 in iteration $j$. Line L6 moves whole rows. So at the start of iteration $j$, the entries $A[i, j]$ for $i \ge j$ and $A[j, t]$ for $t > j$ still hold the entries of $A'$, and the entries read in the sums are $L[i, k]$ and $U[k, t]$ with $k < j$, which are already final.

**Invariant.** At the start of iteration $j$, let $L_1 = L[0..j-1, 0..j-1]$, $L_2 = L[j..n-1, 0..j-1]$, $U_1 = U[0..j-1, 0..j-1]$ and $U_2 = U[0..j-1, j..n-1]$, and let $S$ be the $(n-j) \times (n-j)$ matrix with entries

$$
S[i, t] = A'[i, t] - \sum_{k<j} L[i, k]\, U[k, t] \qquad (j \le i, t \le n - 1).
$$

Then:

- (K1) $A' = \begin{pmatrix} L_1 & 0 \\ L_2 & I \end{pmatrix} \begin{pmatrix} U_1 & U_2 \\ 0 & S \end{pmatrix}$, where $L_1$ is lower triangular and $U_1$ is unit upper triangular.
- (K2) $\det A_0 = s \cdot \det A' = s \cdot \prod_{k<j} L[k, k] \cdot \det S$.

*Initialization.* For $j = 0$ the blocks $L_1, L_2, U_1, U_2$ are empty, $S = A' = A_0$ and $s = 1$, so both parts hold.

*Maintenance.* Assume the invariant at the start of iteration $j$. Line L3 computes $A[i, j] = S[i, j]$ for $i \ge j$, the first column of $S$.

If lines L4 and L5 find no nonzero entry, the first column of $S$ is zero, so $\det S = 0$, and by (K2) $\det A_0 = 0$. Line L5 returns $0$, which is correct.

Otherwise line L6 may swap rows $j$ and $p \ge j$ of $A$. These rows lie below the blocks $L_1$ and $U_1$, so the swap exchanges two rows of $A'$, of $L_2$ and of $S$ at the same time, and (K1) holds for the new $A'$. The swap negates $\det A'$ and $\det S$, and line L6 negates $s$, so (K2) holds. Now $L[j, j] = S[j, j] \ne 0$ (we index $S$ by $j, \dots, n-1$).

Line L7 computes, for $t > j$, $U[j, t] = S[j, t] / S[j, j]$. Put $U[j, j] = 1$. The new $L$ column is $L[i, j] = S[i, j]$ for $i \ge j$. Let $S'$ be the matrix on the indices $j + 1, \dots, n - 1$ with $S'[i, t] = S[i, t] - L[i, j]\, U[j, t]$; this is the $S$ of iteration $j + 1$, because its defining sum gains the term $k = j$. Then

$$
S = \begin{pmatrix} 1 & 0 \\ c & I \end{pmatrix} \begin{pmatrix} S[j, j] & r \\ 0 & S' \end{pmatrix}, \qquad c_i = L[i, j] / S[j, j], \quad r_t = S[j, t],
$$

which one checks entry by entry: row $j$ gives $S[j, j]$ and $S[j, t]$, column $j$ gives $c_i S[j, j] = S[i, j]$, and the other entries give $c_i r_t + S'[i, t] = L[i, j] U[j, t] + S'[i, t] = S[i, t]$. Substituting this into (K1), and moving the column $(S[j, j], c\, S[j, j])^T = L[j..n-1, j]$ into $L$ and the row $(1, r / S[j, j]) = U[j, j..n-1]$ into $U$, gives (K1) for $j + 1$, with $L_1$ still lower triangular and $U_1$ unit upper triangular. Taking determinants, $\det S = S[j, j] \cdot \det S' = L[j, j] \det S'$, so (K2) holds for $j + 1$.

*End.* If the algorithm does not return on line L5, the loop ends with $j = n$. Then $S$ is empty with determinant $1$, (K1) says $A' = LU$, and (K2) says $\det A_0 = s \prod_{k<n} L[k, k]$. Lines L8 to L10 compute exactly this product. $\blacksquare$

**Remark.** The proof shows that $L[j, j]$ equals the pivot of step $j$ of [Gaussian elimination](/determinant-gaussian-elimination/) with the same row swaps, and that every partial sum on line L3 is an entry of an intermediate matrix of Gaussian elimination. So the numbers that Crout's method stores and computes over $\mathbb{Q}$ are quotients of minors of the input, as in Gaussian elimination.
