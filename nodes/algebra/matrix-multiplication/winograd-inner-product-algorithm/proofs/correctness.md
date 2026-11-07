---
title: Winograd's inner product algorithm computes the matrix product
proves: [correctness, termination]
status: full
---

Let $R$ be a commutative ring, $A \in R^{n \times m}$, $B \in R^{m \times p}$ with $n, m, p \ge 0$, and $h = \lfloor m/2 \rfloor$.

**Claim.** WINOGRAD-PRODUCT$(A, B)$ stops and returns $C = AB$.

**Lemma.** For all $x_1, x_2, y_1, y_2 \in R$, $(x_1 + y_2)(x_2 + y_1) = x_1 y_1 + x_2 y_2 + x_1 x_2 + y_1 y_2$.

*Proof.* By distributivity, $(x_1 + y_2)(x_2 + y_1) = x_1 x_2 + x_1 y_1 + y_2 x_2 + y_2 y_1$. By commutativity, $y_2 x_2 = x_2 y_2$ and $y_2 y_1 = y_1 y_2$. $\square$

**Proof of the claim.** Lines L2 and L3 set $\xi_i = \sum_{t<h} A[i][2t] A[i][2t+1]$ and $\eta_j = \sum_{t<h} B[2t][j] B[2t+1][j]$ (empty sums are $0$).

Fix $0 \le i < n$ and $0 \le j < p$. After line L5, $s = -\xi_i - \eta_j$. By induction on the loop of line L6, after the iteration with index $t$,

$$s = -\xi_i - \eta_j + \sum_{u \le t} (A[i][2u] + B[2u+1][j])(A[i][2u+1] + B[2u][j]).$$

The base case before the first iteration is the empty sum, and each iteration adds the next term. After the loop, applying the lemma with $x_1 = A[i][2u]$, $x_2 = A[i][2u+1]$, $y_1 = B[2u][j]$, $y_2 = B[2u+1][j]$ to each term,

$$s = -\xi_i - \eta_j + \sum_{u<h} \big( A[i][2u] B[2u][j] + A[i][2u+1] B[2u+1][j] \big) + \sum_{u<h} A[i][2u] A[i][2u+1] + \sum_{u<h} B[2u][j] B[2u+1][j].$$

The last two sums are $\xi_i$ and $\eta_j$, so $s = \sum_{k < 2h} A[i][k] B[k][j]$. If $m$ is even, $2h = m$ and this is $C[i][j]$. If $m$ is odd, $2h = m - 1$, and line L7 adds $A[i][m-1] B[m-1][j]$, so again $s = \sum_{k<m} A[i][k] B[k][j] = C[i][j]$. Line L8 stores this value. The value of $s$ for one entry does not depend on any other entry, so every entry of $C$ is correct.

**Termination.** Every loop runs over a finite range fixed before it starts ($n$, $p$ and $h$ iterations), and each iteration does a bounded number of ring operations. $\blacksquare$

**Where commutativity is needed.** Without it, the lemma fails: for $2 \times 2$ matrices $x_2 = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$, $y_2 = \begin{pmatrix} 0 & 0 \\ 1 & 0 \end{pmatrix}$ and $x_1 = y_1 = 0$, the left side is $y_2 x_2 = \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix}$ while the right side is $x_2 y_2 = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}$.
