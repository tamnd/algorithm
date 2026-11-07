---
title: Householder tridiagonalization returns an orthogonal similarity to tridiagonal form
proves: [correctness, termination]
status: full
---

Exact arithmetic. Notation of the page: $A$ real symmetric of order $n$, $P_k = I - \beta_k v_k v_k^T$ acting on indices $k + 1$ to $n$, $A^{(0)} = A$ and $A^{(k)}$ the full symmetric matrix whose lower triangle is stored after the $k$-th pass of lines L3 to L8. The rounding error analysis, which gives the backward error $\|E\|_F = O(n u)\|A\|_F$ from the facts that a computed reflector is within $O(u)$ of an exact one and that applying it is backward stable, is in Wilkinson (1965, Chapter 3) and GVL Section 5.1 and Section 8.3.1; we do not repeat it.

**Lemma 1 (HOUSE).** For $x \in \mathbb R^m$, HOUSE returns $(v, \beta, \alpha)$ with $(I - \beta v v^T) x = \alpha e_1$ and $I - \beta v v^T$ orthogonal and symmetric.

*Proof.* If $\|x_{2..m}\|_2 = 0$, then $\beta = 0$, the matrix is $I$, and $x = x_1 e_1 = \alpha e_1$. Otherwise $\alpha = -\operatorname{sign}(x_1)\|x\|_2 \ne 0$ and $v = x - \alpha e_1 \ne 0$, since its tail is the nonzero $x_{2..m}$. Then $v^T x = \|x\|^2 - \alpha x_1$ and $v^T v = \|x\|^2 - 2\alpha x_1 + \alpha^2 = 2(\|x\|^2 - \alpha x_1)$, so with $\beta = 2 / v^T v$ we get $\beta v^T x = 1$ and $(I - \beta v v^T) x = x - v = \alpha e_1$. The matrix $I - \beta v v^T$ is symmetric, and its square is $I - 2\beta v v^T + \beta^2 (v^T v) v v^T = I$ because $\beta v^T v = 2$, so it is orthogonal. $\square$

**Lemma 2 (the rank-2 update).** Let $B$ be symmetric of order $m$, $P = I - \beta v v^T$, $p = \beta B v$ and $w = p - (\beta p^T v / 2) v$. Then $P B P = B - v w^T - w v^T$.

*Proof.* $P B P = B - \beta v v^T B - \beta B v v^T + \beta^2 (v^T B v) v v^T$. Since $B$ is symmetric, $\beta v^T B = p^T$, and $\beta^2 v^T B v = \beta p^T v$. So $P B P = B - v p^T - p v^T + \beta (p^T v) v v^T$. On the other hand $v w^T + w v^T = v p^T + p v^T - \beta (p^T v) v v^T$. The two agree. $\square$

Lemma 2 shows that the result of line L7 is symmetric, so computing its lower triangle determines it.

**Lemma 3 (the invariant).** For $k = 0, 1, \dots, n - 2$, $A^{(k)} = P_k \cdots P_1 A P_1 \cdots P_k$, and for every $j \le k$ the column $j$ of $A^{(k)}$ is zero in rows $j + 2$ to $n$, and the row $j$ is zero in columns $j + 2$ to $n$.

*Proof.* Induction on $k$; for $k = 0$ there is nothing to prove beyond $A^{(0)} = A$. Assume the claim for $k - 1$ and write $A^{(k-1)}$ in blocks with the index sets $\{1..k\}$ and $\{k+1..n\}$:

$$A^{(k-1)} = \begin{pmatrix} B_{11} & B_{21}^T \\ B_{21} & B_{22} \end{pmatrix}, \qquad \tilde P_k = \begin{pmatrix} I_k & 0 \\ 0 & P \end{pmatrix}, \qquad P = I - \beta_k v_k v_k^T.$$

By the hypothesis applied to the columns $j \le k - 1$, the block $B_{21}$ is zero except in its last column, which is the vector $x$ of line L3 (column $k$, rows $k + 1$ to $n$). Then

$$\tilde P_k A^{(k-1)} \tilde P_k = \begin{pmatrix} B_{11} & (P B_{21})^T \\ P B_{21} & P B_{22} P \end{pmatrix}.$$

$P B_{21}$ is zero except in its last column, which is $P x = \alpha e_1$ by Lemma 1: this is line L8. $P B_{22} P$ is the result of lines L5 to L7 by Lemma 2. $B_{11}$ is not touched. So the stored matrix after the $k$-th pass is $\tilde P_k A^{(k-1)} \tilde P_k$, which with $P_k = \tilde P_k$ proves the first claim. Column $k$ is now zero in rows $k + 2$ to $n$; the columns $j < k$ are unchanged in rows $1$ to $k$ and zero in rows $k + 1$ to $n$ (for $j \le k - 1$, row $k + 1$ is at least $j + 2$). The claims on rows follow by symmetry. $\square$

**Lemma 4 (the accumulation).** Lines L9 and L10 leave $Q = P_1 P_2 \cdots P_{n-2}$.

*Proof.* Let $Q^{(k)}$ be the value after the pass with index $k$, starting from $Q^{(n-1)} = I$. We claim $Q^{(k)} = P_k \cdots P_{n-2}$ and that $Q^{(k)}$ agrees with the identity in its first $k$ rows and first $k$ columns. For $k = n - 1$ this is $I$. Assume it for $k + 1$. Since $Q^{(k+1)}$ is the identity in rows and columns $1$ to $k + 1$, the product $P_k Q^{(k+1)}$, where $P_k$ acts on rows $k + 1$ to $n$, changes only rows $k + 1$ to $n$; in those rows the columns $1$ to $k$ of $Q^{(k+1)}$ are zero and stay zero. So $P_k Q^{(k+1)}$ is obtained by applying $I - \beta_k v_k v_k^T$ to the block $Q[k+1..n, k+1..n]$, which is line L10, and the result is the identity in rows and columns $1$ to $k$. $\square$

**Theorem 5 (correctness and termination).** The algorithm terminates after $n - 2$ passes of each loop, and returns $d$, $e$ and an orthogonal $Q$ with $A = Q T Q^T$, where $T$ is the symmetric tridiagonal matrix with diagonal $d$ and off-diagonal $e$, and $Q e_1 = e_1$.

*Proof.* Both loops are counted, so the algorithm stops; for $n \le 2$ they are empty, $A$ is already tridiagonal and $Q = I$. By Lemma 3 with $k = n - 2$, $A^{(n-2)} = Q^T A Q$ with $Q = P_1 \cdots P_{n-2}$, since each $P_k$ is symmetric. All its columns $j \le n - 2$ are zero below the subdiagonal, and columns $n - 1$ and $n$ have no entries below row $j + 1$ to check, so $A^{(n-2)}$ is upper Hessenberg and symmetric, that is, tridiagonal, and it equals $T$. $Q$ is orthogonal as a product of orthogonal matrices (Lemma 1), and by Lemma 4 it is what lines L9 and L10 return. Since no $P_k$ touches index 1, $Q e_1 = e_1$. Then $A = Q T Q^T$. $\blacksquare$

**Remark (the flop count).** At step $k$ with $m = n - k$, line L5 costs $2m^2$ flops for the symmetric product, line L6 $O(m)$, and line L7 updates $m(m+1)/2$ entries at 4 flops each. The total is $\sum_{m=2}^{n-1} (4m^2 + O(m)) = 4n^3/3 + O(n^2)$. Line L10 costs $4m^2$ at step $k$, again $4n^3/3 + O(n^2)$ in all.
