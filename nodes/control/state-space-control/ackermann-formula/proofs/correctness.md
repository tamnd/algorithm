---
title: Ackermann's formula gives the only single-input gain with the wanted characteristic polynomial
proves: [correctness]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$, $b \in \mathbb{R}^n$, and $p(s) = \sum_{i=0}^{n} p_i s^{n-i}$ with $p_0 = 1$. Write $W = [b, Ab, \dots, A^{n-1} b]$, $A_c = A - bK$ for a row vector $K$, and $e_n$ for the last unit vector. The claim is: if $W$ is invertible, then $K = e_n^T W^{-1} p(A)$ is the only row vector with $\det(sI - A_c) = p(s)$, and lines L1 to L5 compute it.

## Lemma 1: expansion of the powers

For every row vector $K$ and every $k \ge 0$,

$$A_c^k = A^k - \sum_{j=0}^{k-1} A^j b\, K A_c^{k-1-j}.$$

*Proof.* For $k = 0$ the sum is empty and both sides are $I$. If the identity holds for $k$, then

$$A_c^{k+1} = A A_c^k - bK A_c^k = A^{k+1} - \sum_{j=0}^{k-1} A^{j+1} b\, K A_c^{k-1-j} - b K A_c^k.$$

Shift the index $j + 1 \to j$ in the sum. The last term is the term $j = 0$ of the new sum, so $A_c^{k+1} = A^{k+1} - \sum_{j=0}^{k} A^j b\, K A_c^{k-j}$. $\square$

## Lemma 2: the polynomial of the closed loop

$p(A_c) = p(A) - W M$, where $M$ is the $n \times n$ matrix with rows

$$r_j = K \sum_{k=j+1}^{n} p_{n-k} A_c^{k-1-j}, \qquad j = 0, \dots, n-1,$$

and the last row is $r_{n-1} = K$.

*Proof.* By Lemma 1, $p(A_c) = \sum_{k=0}^{n} p_{n-k} A_c^k = p(A) - \sum_{k=1}^{n} p_{n-k} \sum_{j=0}^{k-1} A^j b\, K A_c^{k-1-j}$. Exchange the two sums: $j$ runs from 0 to $n-1$, and for fixed $j$, $k$ runs from $j + 1$ to $n$. This gives $p(A) - \sum_{j=0}^{n-1} A^j b\, r_j = p(A) - W M$, because $A^j b$ is column $j + 1$ of $W$ and $r_j$ is row $j + 1$ of $M$. For $j = n - 1$ only $k = n$ occurs, with $p_0 = 1$ and $A_c^0 = I$, so $r_{n-1} = K$. $\square$

## Lemma 3: uniqueness

If $W$ is invertible and $\det(sI - A_c) = p(s)$, then $K = e_n^T W^{-1} p(A)$.

*Proof.* By the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/), a matrix satisfies its characteristic polynomial, so $p(A_c) = 0$. Lemma 2 gives $W M = p(A)$, so $M = W^{-1} p(A)$. The last row of $M$ is $K$ (Lemma 2), and the last row of $W^{-1} p(A)$ is $e_n^T W^{-1} p(A)$. $\square$

## Lemma 4: existence

If $W$ is invertible, some row vector $K$ gives $\det(sI - A_c) = p(s)$.

*Proof.* Let $q^T = e_n^T W^{-1}$, so $q^T W = e_n^T$, that is, $q^T A^j b = 0$ for $j < n - 1$ and $q^T A^{n-1} b = 1$. Let $T$ be the matrix with rows $q^T, q^T A, \dots, q^T A^{n-1}$.

*$T$ is invertible.* The entry $(i, j)$ of $TW$ is $q^T A^{i+j-2} b$. It is 0 if $i + j < n + 1$ and 1 if $i + j = n + 1$. So $TW$ has ones on the antidiagonal and zeros above it, its determinant is $\pm 1$, and $T$ is invertible.

*The new coordinates.* Entry $i$ of $Tb$ is $q^T A^{i-1} b$, which is 1 for $i = n$ and 0 otherwise, so $Tb = e_n$. Row $i$ of $TA$ is $q^T A^i$, which is row $i + 1$ of $T$ for $i < n$. Let $\det(sI - A) = s^n + a_1 s^{n-1} + \cdots + a_n$. By the Cayley-Hamilton theorem, $q^T A^n = -\sum_{k=1}^{n} a_k\, q^T A^{n-k}$. So $TA = \bar A T$, where $\bar A$ has rows $e_2^T, \dots, e_n^T$ and the last row $[-a_n, \dots, -a_1]$.

*The gain.* Let $\bar K = [p_n - a_n, \dots, p_1 - a_1]$. Then $\bar A - e_n \bar K$ has rows $e_2^T, \dots, e_n^T$ and the last row $[-p_n, \dots, -p_1]$. Call this companion matrix $C_p$. Expand $\det(sI - C_p)$ along the first column. The entry $s$ in position $(1, 1)$ has the minor $\det(sI - C_{p'})$ with $p'(s) = s^{n-1} + p_1 s^{n-2} + \cdots + p_{n-1}$. The entry $p_n$ in position $(n, 1)$ has a minor that is lower triangular with $-1$ on the diagonal, so its cofactor is $(-1)^{n+1} (-1)^{n-1} p_n = p_n$. So $\det(sI - C_p) = s\, p'(s) + p_n = p(s)$ by induction on $n$, with the base case $\det(s - (-p_1)) = s + p_1$. Finally set $K = \bar K T$. Then $T(A - bK)T^{-1} = \bar A - e_n \bar K = C_p$, and similar matrices have the same characteristic polynomial. $\square$

## Theorem

If $W$ is invertible, the output of lines L1 to L5 is the only row vector $K$ with $\det(sI - (A - bK)) = p(s)$.

*Proof.* By Lemma 4 a solution exists, and by Lemma 3 every solution equals $e_n^T W^{-1} p(A)$, so this vector is the unique solution. It remains to see that the lines compute it.

Line L1 builds $W$ column by column, since column $j + 1$ is $A$ times column $j$. Line L2 solves $W^T q = e_n$, so $q^T W = e_n^T$ and $q^T = e_n^T W^{-1}$. In lines L3 and L4, the loop invariant is: after the coefficients $p_0, \dots, p_i$ have been used, $K = q^T \sum_{l=0}^{i} p_l A^{i-l}$. This holds after the first step, where $K = 0 \cdot A + p_0 q^T$. If it holds after step $i$, the update $K \leftarrow KA + p_{i+1} q^T$ gives $q^T \sum_{l=0}^{i+1} p_l A^{i+1-l}$. After step $n$, $K = q^T p(A)$, which line L5 returns. The code forms $KA$ as the vector $A^T K^T$, which is the same numbers. $\square$

## When $W$ is singular

If $W$ is singular, $(A, b)$ is not controllable by the [Kalman rank condition](/kalman-rank-condition/). By the [pole placement theorem](/pole-placement-theorem/), the eigenvalues of the uncontrollable part are then eigenvalues of $A - bK$ for every $K$, so some polynomials $p$ cannot be reached. The solve in line L2 meets a zero pivot, and the code raises an error for every $p$, also for the polynomials that could be reached. With exact data this test is exact. With floating point data, a nearly singular $W$ usually gives a nonzero pivot, and the code returns a very large gain; the page discusses this.
