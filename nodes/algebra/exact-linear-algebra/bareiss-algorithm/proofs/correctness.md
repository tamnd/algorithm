---
title: The Bareiss algorithm returns the determinant, with exact divisions
proves: [correctness, termination]
status: full
---

Let $A_0$ be the input, an $n \times n$ matrix over an integral domain $R$ with field of fractions $F$, and let $A$ be the working matrix. Indices start at $0$, as in the pseudocode. Line L7 swaps two rows of $A$ at or below row $k$; let $A'$ be the input with its rows in the current order, so that $A'$ is $A_0$ with the same swaps applied. For $0 \le k \le n$ let $d_k$ be the leading principal minor of order $k$ of $A'$, with $d_0 = 1$. For $k \le i, j \le n - 1$ let

$$
m_k(i, j) = \det A'[\{0, \dots, k-1, i\}, \{0, \dots, k-1, j\}],
$$

the minor of $A'$ in the first $k$ rows plus row $i$ and the first $k$ columns plus column $j$. Note that $m_k(k, k) = d_{k+1}$ and $m_0(i, j) = A'[i, j]$.

**Claim.** BAREISS$(A_0)$ stops, every division on line L10 is exact in $R$, and the result is $\det A_0$.

**Termination.** Line L3 runs $k$ over at most $n - 1$ values, and the loops on lines L5, L8 and L9 have fewer than $n$ steps each.

**Lemma (the Bareiss identity, a case of Sylvester's identity).** If $d_k \ne 0$, then for all $i, j$ with $k < i, j \le n - 1$,

$$
d_k \cdot m_{k+1}(i, j) = m_k(k, k)\, m_k(i, j) - m_k(i, k)\, m_k(k, j).
$$

*Proof.* Let $C$ be the $(k+2) \times (k+2)$ submatrix of $A'$ in the rows $0, \dots, k, i$ and the columns $0, \dots, k, j$, so that $\det C = m_{k+1}(i, j)$. Let $B$ be its leading $k \times k$ block, with $\det B = d_k \ne 0$. Since $B$ is invertible over $F$, we can subtract from row $k$ and from row $i$ of $C$ combinations of the first $k$ rows so that both rows become zero in the first $k$ columns. Call the result $C'$. It has the block form

$$
C' = \begin{pmatrix} B & X \\ 0 & S \end{pmatrix}, \qquad S = \begin{pmatrix} s_{kk} & s_{kj} \\ s_{ik} & s_{ij} \end{pmatrix}.
$$

Adding to a row a combination of other rows does not change a determinant. The same row operations, applied to the submatrix of $C$ in the rows $0, \dots, k-1, i'$ and the columns $0, \dots, k-1, j'$ for $i' \in \{k, i\}$ and $j' \in \{k, j\}$, turn it into $\begin{pmatrix} B & * \\ 0 & s_{i'j'} \end{pmatrix}$, which has determinant $d_k\, s_{i'j'}$. So $m_k(i', j') = d_k\, s_{i'j'}$ for these four pairs. Also $\det C = \det C' = d_k \det S$. Hence

$$
m_k(k, k)\, m_k(i, j) - m_k(i, k)\, m_k(k, j) = d_k^2 (s_{kk} s_{ij} - s_{ik} s_{kj}) = d_k^2 \det S = d_k \det C = d_k\, m_{k+1}(i, j). \qquad \square
$$

**Invariant.** At the start of the iteration of line L3 with index $k$, and also when the loop ends, with $k = n - 1$:

- (J1) $\det A_0 = s \cdot \det A'$.
- (J2) $d_k \ne 0$, and $\mathit{prev} = d_k$.
- (J3) $A[i, j] = m_k(i, j)$ for all $k \le i, j \le n - 1$.
- (J4) $A[t, j] = m_t(t, j)$ for all $t < k$ and $t \le j \le n - 1$.

*Initialization.* For $k = 0$, no swap has happened, so $A' = A_0$ and $s = 1$. Also $\mathit{prev} = 1 = d_0$, and $m_0(i, j) = A_0[i, j] = A[i, j]$. (J4) is empty.

*Maintenance.* Assume the invariant at the start of iteration $k \le n - 2$. By (J3), $A[i, k] = m_k(i, k)$ for $i \ge k$.

*Case 1: lines L4 to L6 return $0$.* Then $m_k(i, k) = 0$ for every $i \ge k$. Apply to all of $A'$ the row operations of the lemma: subtract from every row $i \ge k$ the combination of the first $k$ rows that clears its first $k$ entries. The result is $\begin{pmatrix} B & X \\ 0 & S \end{pmatrix}$ with an $(n-k) \times (n-k)$ block $S$, and as in the lemma $m_k(i, j) = d_k\, S_{ij}$. So the first column of $S$ is zero, $\det S = 0$, and $\det A' = d_k \det S = 0$. By (J1), $\det A_0 = 0$, and the return value $0$ is correct.

*Case 2: line L7 swaps rows $k$ and $p > k$.* This swaps two rows of $A'$ that are not among the first $k$, so $d_k$ does not change, and the entries of the rows $k$ and $p$ of $A$ are exchanged exactly as the minors $m_k(k, \cdot)$ and $m_k(p, \cdot)$ of the new $A'$ require. So (J3) and (J4) still hold. The swap negates $\det A'$ and line L7 negates $s$, so (J1) still holds.

After lines L4 to L7, $A[k, k] = m_k(k, k) = d_{k+1} \ne 0$. For $k < i, j \le n - 1$, line L10 computes

$$
\frac{A[k, k]\, A[i, j] - A[i, k]\, A[k, j]}{\mathit{prev}} = \frac{m_k(k, k)\, m_k(i, j) - m_k(i, k)\, m_k(k, j)}{d_k} = m_{k+1}(i, j)
$$

by the lemma. The value $m_{k+1}(i, j)$ is a minor of an integral domain matrix, so it is an element of $R$. In an integral domain, $d_k \ne 0$ divides the numerator with a unique quotient, so the division is exact and gives this minor. Line L10 reads $A[i, k]$ and $A[k, j]$, which it does not change in the iteration, so the order of the updates does not matter. Row $k$ is not changed, so it holds $m_k(k, j)$ for $j \ge k$, which gives (J4) for $k + 1$. Line L11 sets $\mathit{prev} = A[k, k] = d_{k+1} \ne 0$, which gives (J2) for $k + 1$. So the invariant holds at the start of iteration $k + 1$.

*End.* If $n = 0$, line L1 returns $1 = \det A_0$. Otherwise, if no return happens inside the loop, the loop ends with $k = n - 1$. By (J3), $A[n-1, n-1] = m_{n-1}(n-1, n-1) = d_n = \det A'$, and by (J1) line L12 returns $s \det A' = s^2 \det A_0 = \det A_0$. $\blacksquare$

**Remark.** The proof shows more than the claim. Every number that the algorithm stores is a minor of the row-permuted input, and every numerator on line L10 is $d_k$ times such a minor. This is the fact that bounds the sizes of the numbers by the Hadamard bound.
