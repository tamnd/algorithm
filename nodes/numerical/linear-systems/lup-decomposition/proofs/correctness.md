---
title: LUP-DECOMPOSITION computes PA = LU with bounded multipliers, and reports SINGULAR exactly for singular A
proves: [correctness, termination]
status: full
---

We work in exact arithmetic first. $A$ is a real $n \times n$ matrix, $e_k$ is the $k$-th unit vector, and for a permutation $\pi$ we write $P_\pi$ for the matrix with $(P_\pi A)_{k,:} = A_{\pi_k,:}$. The algorithm stops: line L2 runs at most $n$ times, and each inner loop has a fixed length.

**State after pass $k$.** Let $M$ be the array after pass $k$ (for $k = 0$, the input $A$) and $\pi$ the current permutation. Define

- $L^{(k)}$: the unit lower triangular matrix with $L^{(k)}_{ij} = M_{ij}$ for $j < i$ and $j \le k$, and $L^{(k)}_{ij} = 0$ for $j < i$ and $j > k$;
- $S^{(k)}$: the matrix with $S^{(k)}_{ij} = M_{ij}$ when $i \le k$ and $j \ge i$, or when $i > k$ and $j > k$, and $S^{(k)}_{ij} = 0$ otherwise.

So $S^{(k)} = \begin{pmatrix} U_{11} & U_{12} \\ 0 & C \end{pmatrix}$, where $U_{11}$ is $k \times k$ upper triangular and $C$ is the $(n - k) \times (n - k)$ trailing block of $M$.

**Invariant (I).** After pass $k$ (when line L4 has not returned): $P_\pi A = L^{(k)} S^{(k)}$, each multiplier satisfies $|L^{(k)}_{ij}| \le 1$, and the diagonal entries $u_{11}, \ldots, u_{kk}$ of $U_{11}$ are nonzero.

*Initialization.* For $k = 0$, $\pi$ is the identity, $L^{(0)} = I$, $S^{(0)} = A$, and there are no multipliers or pivots. So (I) holds.

*Maintenance.* Assume (I) after pass $k - 1$, with $L = L^{(k-1)}$, $S = S^{(k-1)}$ and trailing block $C$ (rows and columns $k$ to $n$). Pass $k$ does three things.

1. *The swap (line L5).* Let $\Pi$ be the permutation matrix that exchanges rows $k$ and $p$, where $k \le p$. The new permutation $\pi'$ has $P_{\pi'} = \Pi P_\pi$. Then
$$\Pi P_\pi A = (\Pi L \Pi)(\Pi S),$$
because $\Pi \Pi = I$. The matrix $\Pi L \Pi$ is $L$ with rows $k$ and $p$ exchanged and then columns $k$ and $p$ exchanged. Columns $k$ to $n$ of $L$ are those of the identity, so the column exchange undoes the row exchange on them, and $\Pi L \Pi$ is again unit lower triangular: it is $L$ with the multipliers in columns $1$ to $k - 1$ of rows $k$ and $p$ exchanged. This is exactly what line L5 does to the stored multipliers, because it exchanges whole rows. The matrix $\Pi S$ is $S$ with rows $k$ and $p$ exchanged; both rows have zeros in columns $1$ to $k - 1$, so $\Pi S$ has the same shape, with trailing block $C'$ equal to $C$ with two rows exchanged, and this is what line L5 does to the trailing block. So after line L5, $P_{\pi'} A = L S$ holds with the array updated in the same way.

2. *The pivot.* We show that if line L4 does not return, the pivot $c = M_{kk}$ after the swap is nonzero, and that $|M_{ik}| \le |c|$ for $i > k$. Line L3 picks $p$ with $|M_{pk}|$ maximal over $i \ge k$, so after the swap $|M_{kk}| \ge |M_{ik}|$ for each $i > k$. Line L4 returns when this maximum is $0$; if it does not return, $c \ne 0$.

3. *The elimination (lines L6 to L9).* Write the trailing block after the swap as $C' = \begin{pmatrix} c & w^T \\ v & B \end{pmatrix}$ with $c \ne 0$. Lines L7 set $l = v / c$ in column $k$ below the pivot, and lines L8 and L9 replace $B$ by $B - l w^T$. Now
$$C' = \begin{pmatrix} 1 & 0 \\ l & I \end{pmatrix} \begin{pmatrix} c & w^T \\ 0 & B - l w^T \end{pmatrix},$$
as one checks block by block: the $(2,1)$ block is $l c = v$, and the $(2,2)$ block is $l w^T + B - l w^T = B$. Embedding this identity in rows and columns $k$ to $n$ gives $L S = L^{(k)} S^{(k)}$ for the new array, because the first factor puts $l$ into column $k$ of the unit lower triangular factor (columns $k$ to $n$ of $L$ were the identity) and the second factor is the new $S^{(k)}$. By step 2, $|l_i| = |v_i|/|c| \le 1$, and the new pivot $u_{kk} = c$ is nonzero. So (I) holds after pass $k$.

**Termination with success.** If line L4 never returns, then after pass $n$ the trailing block is empty, $S^{(n)} = U$ is upper triangular with nonzero diagonal, $L^{(n)} = L$, and (I) gives $P_\pi A = L U$ with $|l_{ij}| \le 1$. Line L10 returns this result.

**SINGULAR is reported exactly for singular $A$.** By (I) after pass $k - 1$, $\det(P_\pi A) = \det L \cdot \det S = \pm \det A$, and $\det L = 1$, $\det S = u_{11} \cdots u_{k-1,k-1} \cdot \det C$, where the $u_{ii}$ are nonzero. So $\det C \ne 0$ if and only if $\det A \ne 0$. If $A$ is nonsingular, $C$ is nonsingular, so its first column is not zero, and line L4 does not return at pass $k$; by induction on $k$, it never returns. If line L4 returns at pass $k$, the first column of $C$ is zero, so $\det C = 0$ and $A$ is singular. If $A$ is singular, the algorithm cannot reach line L10, because then $\det A = \pm \prod u_{ii} \ne 0$; so line L4 returns at some pass. $\blacksquare$

## Floating point

Assume the standard model $\mathrm{fl}(a \circ b) = (a \circ b)(1 + \delta)$, $|\delta| \le u$, and $n u < 1$. Swaps and comparisons are exact. So the computed result is the result of elimination without pivoting applied to the matrix $P A$, where $P$ is the permutation that the computation chose. Entry $(i, j)$ of $P A$ is processed by the recurrence $a^{(k+1)}_{ij} = a^{(k)}_{ij} - l_{ik} u_{kj}$ for $k < \min(i, j)$, and then by $u_{ij} = a^{(i)}_{ij}$ for $i \le j$ or $l_{ij} = a^{(j)}_{ij} / u_{jj}$ for $i > j$. This is the evaluation of $s = (a - \sum_{k=1}^{m} l_k u_k)$, followed by a division in the second case, with $m = \min(i, j) - 1$. By the standard bound for such an expression (Higham, Lemma 8.4), for $i \le j$

$$\Bigl| (P A)_{ij} - \sum_{k=1}^{i} \hat l_{ik} \hat u_{kj} \Bigr| \le \gamma_{i} \sum_{k=1}^{i} |\hat l_{ik}|\,|\hat u_{kj}|, \qquad \hat l_{ii} = 1,$$

and for $i > j$ the same bound holds with $\gamma_j$ and the sum to $j$. Since $\gamma_m \le \gamma_n$ for $m \le n$, this is $\hat L \hat U = P A + \Delta A$ with $|\Delta A| \le \gamma_n |\hat L|\,|\hat U|$ (Higham, Theorem 9.3). The pivot rule makes $|\hat l_{ij}| \le 1$ exactly, because $\mathrm{fl}(v/c)$ with $|v| \le |c|$ is at most $1$ in modulus under rounding to nearest. The $\infty$-norm bound $\|\Delta A\|_\infty \le n^2 \gamma_n \rho_n \|A\|_\infty$ on the page follows from $\|\,|\hat L|\,\|_\infty \le n$ and $|\hat u_{ij}| \le \rho_n \max |a_{ij}|$.
