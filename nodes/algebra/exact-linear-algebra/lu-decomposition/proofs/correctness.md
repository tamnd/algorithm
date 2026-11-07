---
title: LU-DECOMPOSE returns P A = L U with U in echelon form, and LU-SOLVE solves A x = b
proves: [correctness, termination]
status: full
---

We use the notation of the page. $A$ is $m \times n$ over a field $K$. For a permutation $\pi$ of $\{1, \ldots, m\}$, $P_\pi$ is the matrix with $(P_\pi A)$ row $r$ equal to row $\pi(r)$ of $A$. $E_{ij}$ is the $m \times m$ matrix with $1$ in place $(i, j)$ and $0$ elsewhere.

**Termination.** The loop of line L2 runs at most $n$ times, and the inner loops of lines L6 and L8 have fixed bounds. So LU-DECOMPOSE stops after $O(m n \min(m, n) + m n)$ steps. LU-SOLVE has two loops of $n$ steps each.

**Invariant.** At each test of line L2, with $c$ the next column and $r$ the next pivot row:

> **(I1)** $P_\pi A = L U$.
>
> **(I2)** $L$ is unit lower triangular, and for each row $i \ge r$, $L[i, k] = 0$ for $r \le k < i$.
>
> **(I3)** Rows $1$ to $r - 1$ of $U$ are nonzero, the first nonzero entry of row $t$ is in a column $p_t$ with $p_1 < \cdots < p_{r-1} < c$, and rows $r$ to $m$ of $U$ are zero in columns $1$ to $c - 1$.

*Initialization.* Line L1 sets $U = A$, $L = I$, $\pi$ the identity and $r = 1$, before column $c = 1$. Then $P_\pi A = A = I A$, $L = I$ satisfies (I2), and (I3) holds with no pivot rows and no columns before $c$.

*Maintenance.* Consider one pass with column $c$, and suppose $r \le m$ (else line L3 stops the loop, and the invariant is not changed).

Case 1: no $i \ge r$ has $U[i, c] \ne 0$ (line L4 goes to the next column). Then rows $r$ to $m$ of $U$ are zero in columns $1$ to $c$, so (I3) holds for $c + 1$. Nothing else changes.

Case 2: line L4 finds $i \ge r$ with $U[i, c] \ne 0$. Let $T$ be the transposition of rows $r$ and $i$ (the identity if $i = r$). Line L5 replaces $U$ by $T U$ and $\pi$ by the permutation with $P_{\pi'} = T P_\pi$. It replaces $L$ by $L' = T L T$ restricted as follows: $T L T$ swaps rows $r, i$ and columns $r, i$ of $L$. By (I2), rows $r$ and $i$ of $L$ have zeros in the columns $r$ to $m$ except on the diagonal, so $T L T$ is obtained from $L$ by swapping only the entries in columns $1$ to $r - 1$ of rows $r$ and $i$, which is exactly what line L5 does. Then

$$P_{\pi'} A = T P_\pi A = T L U = (T L T)(T U) = L' U',$$

since $T T = I$. So (I1) holds after line L5. $L'$ is still unit lower triangular and satisfies (I2), because the swap keeps zeros in columns $r$ to $m$ of the rows $r$ to $m$, apart from the diagonal. (I3) still holds for rows $1$ to $r - 1$, which are not touched, and rows $r$ to $m$ are still zero in the columns before $c$.

Now let $u = U[r, c] \ne 0$. For $i = r + 1, \ldots, m$, lines L7 and L8 set $f_i = U[i, c] / u$, store $L[i, r] = f_i$, and replace row $i$ of $U$ by row $i$ minus $f_i$ times row $r$. This is $U \leftarrow G U$ with $G = I - \sum_{i > r} f_i E_{ir}$, and $G^{-1} = I + \sum_{i > r} f_i E_{ir}$, because $E_{ir} E_{i' r} = 0$ for $i, i' > r$. Right multiplication by $G^{-1}$ adds $f_i$ times column $i$ of $L$ to column $r$, for each $i > r$. Column $i$ of $L$ is the unit vector $e_i$: its entries above row $i$ are zero because $L$ is lower triangular, its diagonal entry is $1$, and its entries in the rows $i' > i$ are zero by (I2), because $r \le i < i'$. Column $r$ of $L$ is $e_r$ for the same reason. So $L G^{-1}$ is $L$ with $f_i$ put in place $(i, r)$, which is what line L7 stores. Hence $L U = (L G^{-1})(G U)$ and (I1) holds. After the update, $U[i, c] = U[i, c] - f_i u = 0$ for $i > r$; rows $r + 1$ to $m$ are zero in columns $1$ to $c$ (they were zero in columns before $c$, and row $r$ is too). Row $r$ is nonzero, its first nonzero entry is in column $p_r = c > p_{r-1}$. Line L9 sets $r \leftarrow r + 1$. Now (I2) holds for the new $r$, because the only new nonzero entries of $L$ below the diagonal are in column $r_{\text{old}}$, and (I3) holds for $c + 1$.

*Termination of the loop.* When the loop ends, either $c$ ran past $n$, or $r > m$. In the first case (I3) with $c = n + 1$ says that rows $r$ to $m$ of $U$ are zero and rows $1$ to $r - 1$ have strictly increasing leading columns: $U$ is in row echelon form. In the second case all $m$ rows are pivot rows with increasing leading columns, which is also an echelon form. With (I1) and (I2), line L10 returns $\pi$, a unit lower triangular $L$ and an echelon $U$ with $P_\pi A = L U$. $\square$

**LU-SOLVE.** Let $A$ be $n \times n$ and nonsingular. Then $U = L^{-1} P_\pi A$ is nonsingular, and since it is in echelon form and square, its $n$ rows are pivot rows with leading columns $p_1 < \cdots < p_n$ in $\{1, \ldots, n\}$, so $p_t = t$ and $U$ is upper triangular with a nonzero diagonal. Line L11 computes, for $i = 1, \ldots, n$ in order, the unique $y_i$ with $\sum_{k < i} L[i, k] y_k + y_i = (P_\pi b)_i = b_{\pi(i)}$, using only the $y_k$ with $k < i$ already computed; so $L y = P_\pi b$. Line L12 computes, for $i = n, \ldots, 1$, the unique $x_i$ with $U[i, i] x_i + \sum_{k > i} U[i, k] x_k = y_i$, which is possible because $U[i, i] \ne 0$; so $U x = y$. Then $P_\pi A x = L U x = L y = P_\pi b$, and since $P_\pi$ is invertible, $A x = b$. The solution is unique because $A$ is nonsingular. $\blacksquare$

**Determinant.** For square $A$, $\det(P_\pi) \det A = \det L \det U = \prod_i U[i, i]$, and $\det P_\pi = \operatorname{sgn}(\pi) = \pm 1$, so $\det A = \operatorname{sgn}(\pi) \prod_i U[i, i]$. If $A$ is singular, the echelon form $U$ has a zero row, so the product is $0$, as it must be.
