---
title: The Faddeev-LeVerrier recurrence returns the characteristic polynomial and M_n
proves: [correctness, termination]
status: full
---

Let $R$ be a commutative ring in which the integers $1, 2, \dots, n$ are invertible, for example a field of characteristic $0$ or of characteristic greater than $n$, and let $A$ be an $n \times n$ matrix over $R$. Write

$$
\chi_A(x) = \det(xI - A) = \sum_{k=0}^{n} p_k\, x^{n-k}, \qquad p_0 = 1,
$$

so that $p_k$ is the coefficient of $x^{n-k}$, the same indexing as the pseudocode. The case of the integers is treated at the end.

**Claim.** FADDEEV-LEVERRIER$(A)$ stops, returns $(p_0, \dots, p_n)$, and returns a matrix $M_n$ with $A M_n = -p_n I$ and $\operatorname{adj}(A) = (-1)^{n-1} M_n$ for $n \ge 1$.

**Termination.** Line L2 runs $k$ over $n$ values, and each of lines L3 to L5 is a finite computation.

**Lemma 1 (the adjugate of $xI - A$).** Let $B(x) = \operatorname{adj}(xI - A)$, a matrix over $R[x]$. Define matrices $M_1, \dots, M_n$ by $M_1 = I$ and $M_{k+1} = A M_k + p_k I$ for $1 \le k \le n - 1$. Then $B(x) = \sum_{k=1}^{n} M_k\, x^{n-k}$, and $A M_n + p_n I = 0$.

*Proof.* Each entry of $B(x)$ is, up to sign, a minor of order $n - 1$ of $xI - A$, so it has degree at most $n - 1$. Write $B(x) = \sum_{k=1}^{n} B_k x^{n-k}$ with $B_k \in R^{n \times n}$. By Cramer's rule over the commutative ring $R[x]$, $(xI - A)B(x) = \chi_A(x) I$. Comparing the coefficients of $x^{n}, x^{n-1}, \dots, x^0$:

- $x^n$: $B_1 = p_0 I = I$.
- $x^{n-k}$ for $1 \le k \le n - 1$: $B_{k+1} - A B_k = p_k I$.
- $x^0$: $-A B_n = p_n I$.

So the $B_k$ satisfy the same recurrence as the $M_k$ with the same start, hence $B_k = M_k$ for all $k$, and $A M_n + p_n I = 0$. $\square$

**Lemma 2 (derivative of the determinant).** $\chi_A'(x) = \operatorname{tr} B(x)$, where $'$ is the formal derivative in $R[x]$.

*Proof.* Write $\chi_A(x) = \sum_\sigma \operatorname{sgn}(\sigma) \prod_{i} (xI - A)_{i, \sigma(i)}$. The formal derivative satisfies the product rule, and the derivative of the entry $(xI - A)_{ij}$ is $1$ if $i = j$ and $0$ otherwise. So $\chi_A'(x) = \sum_{i} \det N_i(x)$, where $N_i(x)$ is $xI - A$ with row $i$ replaced by the unit row $e_i^T$. Expanding $\det N_i(x)$ along row $i$ gives the cofactor of the entry $(i, i)$ of $xI - A$, which is the diagonal entry $B(x)_{ii}$ of the adjugate. Summing over $i$ gives $\operatorname{tr} B(x)$. $\square$

**Lemma 3 (the trace recurrence).** For $1 \le k \le n$, $k\, p_k = -\operatorname{tr}(A M_k)$.

*Proof.* The coefficient of $x^{n-k}$ in $\chi_A'(x) = \sum_{j} (n - j) p_j x^{n-j-1}$ is $(n - k + 1) p_{k-1}$. By Lemmas 1 and 2, it is also $\operatorname{tr} M_k$. So $\operatorname{tr} M_k = (n - k + 1) p_{k-1}$ for $1 \le k \le n$, and the same formula with $k + 1$ gives $\operatorname{tr} M_{k+1} = (n - k) p_k$ for $k \le n - 1$.

For $k \le n - 1$, take the trace of $M_{k+1} = A M_k + p_k I$: $(n - k) p_k = \operatorname{tr}(A M_k) + n\, p_k$, so $k\, p_k = -\operatorname{tr}(A M_k)$. For $k = n$, take the trace of $A M_n + p_n I = 0$: $\operatorname{tr}(A M_n) + n\, p_n = 0$, which is the same formula. $\square$

**Invariant.** At the start of the iteration of line L2 with index $k$, the stored values $p_0, \dots, p_{k-1}$ are the coefficients of $\chi_A$ and $N = A M_{k-1}$, where we put $M_0 = 0$.

*Initialization.* For $k = 1$, line L1 set $p_0 = 1$ and $N = 0 = A M_0$.

*Maintenance.* Line L3 sets $M = N + p_{k-1} I = A M_{k-1} + p_{k-1} I$. For $k = 1$ this is $0 + I = M_1$, and for $k \ge 2$ it is $M_k$ by the recurrence of Lemma 1. Line L4 sets $N = A M_k$. Line L5 sets $p_k = -\operatorname{tr}(A M_k)/k$, which is the coefficient $p_k$ by Lemma 3, since $k$ is invertible. So the invariant holds for $k + 1$.

*End.* After the iteration with $k = n$, the list holds $p_0, \dots, p_n$, and $M = M_n$; line L6 returns them. For $n = 0$ the loop is empty and the result is $(1)$, the characteristic polynomial of the empty matrix. By Lemma 1, $A M_n = -p_n I$. Since $B(0) = M_n$ and $B(0) = \operatorname{adj}(-A) = (-1)^{n-1} \operatorname{adj}(A)$ (each cofactor is a minor of order $n - 1$), $\operatorname{adj}(A) = (-1)^{n-1} M_n$.

**Integers.** Let $R = \mathbb{Z}$. Run the argument in $\mathbb{Q}$, where $1, \dots, n$ are invertible: the computed $p_k$ and $M_k$ are the coefficients of $\chi_A$ and of $\operatorname{adj}(xI - A)$, which have integer entries because they are integer combinations of minors of $A$. So every quotient on line L5 is an integer, and the exact integer division of the implementation computes it. $\blacksquare$

**Remark.** If some $k \le n$ is not invertible in $R$, Lemma 3 still holds but does not determine $p_k$. Over $\mathbb{Z}/2\mathbb{Z}$ with $n = 2$, the equation $2 p_2 = -\operatorname{tr}(A M_2)$ reads $0 = 0$ for every matrix, so the method has no way to find $\det A$.
