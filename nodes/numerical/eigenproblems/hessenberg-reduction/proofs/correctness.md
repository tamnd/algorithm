---
title: Householder reduction gives a unitary similarity to Hessenberg form
proves: [correctness, termination, flops.worst]
status: full
---

Notation of the page: $A \in \mathbb{C}^{n \times n}$, $P_k = I - \beta_k \hat v_k \hat v_k^*$ the reflector of step $k$, where $\hat v_k$ is $v_k$ padded with $k$ leading zeros (indices $0$ to $k$ of the 0-based code), and $A^{(k)}$ the matrix after step $k$, with $A^{(0)} = A$. Exact arithmetic unless stated.

**Lemma 1 (the reflector).** For $x \in \mathbb{C}^m$ with $\sigma^2 = \sum_{i \ge 2} |x_i|^2 > 0$, let $\phi = x_1 / |x_1|$ (or $\phi = 1$ if $x_1 = 0$), $\alpha = -\phi \|x\|_2$, $v = x - \alpha e_1$ and $\beta = 2 / (v^* v)$. Then $P = I - \beta v v^*$ is unitary and Hermitian, and $P x = \alpha e_1$.

*Proof.* $P^* = P$ since $\beta$ is real. $P^2 = I - 2\beta v v^* + \beta^2 v (v^* v) v^* = I$ because $\beta v^* v = 2$. So $P$ is unitary. Next, $v^* x = \|x\|_2^2 - \bar\alpha x_1 = \|x\|_2^2 + \|x\|_2 |x_1|$, which is real, and $v^* v = \|x\|_2^2 - 2\operatorname{Re}(\bar\alpha x_1) + |\alpha|^2 = 2(\|x\|_2^2 + \|x\|_2 |x_1|)$. So $\beta v^* x = 1$ and $P x = x - v = \alpha e_1$. $\square$

The choice of the sign makes $|v_1| = |x_1| + \|x\|_2$, a sum of two nonnegative numbers, so $v_1$ is computed without cancellation. If $\sigma = 0$, the code takes $\beta = 0$, $P = I$, and the column already has zeros below position 1.

**Theorem 1 (invariant).** After step $k$ of the loop of line L1 ($k = 1, \dots, n-2$ in the 1-based count):

> **(H)** $A^{(k)} = Q_k^* A Q_k$ with $Q_k = P_1 P_2 \cdots P_k$ unitary, and $a^{(k)}_{ij} = 0$ for all $j \le k$ and $i > j + 1$.

*Proof.* By induction on $k$; $Q_0 = I$ and the statement on zeros is empty for $k = 0$. Step $k$ applies $P_k$ on the left (line L3) and on the right (line L4), so $A^{(k)} = P_k A^{(k-1)} P_k = Q_k^* A Q_k$ since $P_k^* = P_k$. The reflector $P_k$ acts on rows and columns $k+1$ to $n$ only.

*Left product.* $P_k$ leaves rows 1 to $k$ unchanged, and maps column $k$ below row $k$, the vector $x = (a^{(k-1)}_{k+1,k}, \dots, a^{(k-1)}_{n,k})$, to $\alpha e_1$ by Lemma 1. For a column $j < k$, rows $k+1$ to $n$ hold zeros by (H) for $k - 1$ (since $k + 1 > j + 1$), and a linear map sends zero to zero.

*Right product.* $P_k$ on the right combines only columns $k+1$ to $n$. Columns 1 to $k$, which hold all the zeros we need, are unchanged.

So after both products, column $k$ has zeros in rows $k + 2$ to $n$, and the earlier columns keep theirs. Line L5 stores exact zeros where the exact result is zero. $\square$

**Corollary (correctness).** After the last step, $k = n - 2$, the matrix $H = A^{(n-2)}$ has $h_{ij} = 0$ for $i > j + 1$ and every $j \le n - 2$; for $j \ge n - 1$ the condition $i > j + 1 \ge n$ is empty. So $H$ is upper Hessenberg and $A = Q H Q^*$ with $Q = Q_{n-2}$, which line L6 accumulates. As a similarity, $H$ has the same eigenvalues as $A$. The first column of $Q$ is $e_1$, because each $P_k$ fixes $e_1$. If $A$ is Hermitian, then $H = Q^* A Q$ is Hermitian and Hessenberg, hence tridiagonal.

**Termination.** The loop of line L1 has $n - 2$ iterations (none if $n \le 2$), each of finite length.

**Theorem 2 (flop count).** For real $A$, computing $H$ costs $10n^3/3 + O(n^2)$ flops, and accumulating $Q$ costs $4n^3/3 + O(n^2)$ more.

*Proof.* At step $k$ the reflector has length $m = n - k$. Line L3 updates the $m \times (n - k + 1)$ block of rows $k + 1$ to $n$ and columns $k$ to $n$: for each column, one inner product and one update, $4m$ flops, so $4m(m + 1)$ flops. Line L4 updates the $n \times m$ block of all rows and columns $k + 1$ to $n$: $4 n m$ flops. Summing over $m = 2, \dots, n - 1$ (the vector $x$ has length $m$ at $k = n - m$): $\sum 4m^2 \approx 4n^3/3$ and $\sum 4nm \approx 2n^3$, which add to $10n^3/3 + O(n^2)$. For $Q$, a backward accumulation $Q = P_1(P_2(\cdots P_{n-2}))$ that works on the trailing $m \times m$ block costs $\sum 4m^2 = 4n^3/3 + O(n^2)$; the forward product of line L6 updates all $n$ rows and costs $\sum 4 n m = 2n^3 + O(n^2)$, which is the simple form the code uses. $\square$

**Theorem 3 (backward stability).** In floating point with unit roundoff $u$, the computed $\hat H$ satisfies $\hat H = Q^* (A + E) Q$ for an exactly unitary $Q$ and $\|E\|_F \le c \, n^2 u \|A\|_F$ for a modest constant $c$, and the computed $\hat Q$ is within $c\, n^2 u$ of $Q$ in the Frobenius norm.

*Sketch with source.* Each computed reflector is close to an exact unitary reflector, and applying a nearly exact reflector to a matrix gives the exact product with a nearby matrix, with a relative backward error of order $m u$ for a vector of length $m$ (Higham, Accuracy and Stability of Numerical Algorithms, second edition, Chapter 19). Sequences of $n$ such products accumulate the errors additively, because unitary matrices do not change the Frobenius norm of the errors. Golub and Van Loan state the result in Section 7.4.3, and Trefethen and Bau prove the normwise form $\|E\| / \|A\| = O(u)$ in Lecture 26.
