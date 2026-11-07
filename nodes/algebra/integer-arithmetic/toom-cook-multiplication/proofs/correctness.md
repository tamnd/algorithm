---
title: Toom-3 returns the product
proves: [correctness, termination]
status: full
---

Let $a$ and $b$ be nonnegative integers of $n$ limbs in radix $\beta = 2^w$ with $w \ge 3$, and let $k = \lceil n/3 \rceil$ and $x = \beta^k$. Line L2 writes $a = a_2x^2 + a_1x + a_0$ and $b = b_2x^2 + b_1x + b_0$ with $0 \le a_i, b_i < x$. Put $A(t) = a_2t^2 + a_1t + a_0$, $B(t) = b_2t^2 + b_1t + b_0$, and

$$C(t) = A(t)B(t) = r_0 + r_1t + r_2t^2 + r_3t^3 + r_4t^4, \qquad r_m = \sum_{i + j = m} a_ib_j .$$

Then $ab = A(x)B(x) = C(x)$, and every $r_m \ge 0$. For a polynomial, its value at $\infty$ means its leading coefficient: $A(\infty) = a_2$, $B(\infty) = b_2$, $C(\infty) = r_4 = a_2b_2$.

**Lemma 1 (evaluation).** Line L3 computes $A(0), A(1), A(-1), A(-2), A(\infty)$, and the same for $B$, and each has absolute value less than $5x \le \beta^{k+1}$.

*Proof.* With $p = a_0 + a_2$: $p + a_1 = A(1)$, $p - a_1 = A(-1)$, and $2(A(-1) + a_2) - a_0 = 2a_0 - 2a_1 + 4a_2 - a_0 = A(-2)$. The bounds: $0 \le A(1) < 3x$, $-x < A(-1) < 2x$, $-2x < A(-2) < 5x$. Since $w \ge 3$, $5x < 8x \le \beta x = \beta^{k+1}$, so each magnitude fits in $k + 1$ limbs. $\square$

**Lemma 2 (termination and depth).** For $n \ge 3$, $k + 1 < n$. Hence the recursion of line L4, whose operands have $k + 1$ limbs, ends, and with $n_0 = n$ and $n_{i+1} = \lceil n_i/3 \rceil + 1$ its depth is the least $i$ with $n_i \le \max(T, 2)$, which is $\log_3 n + O(1)$.

*Proof.* $\lceil n/3 \rceil \le (n + 2)/3$, so $k + 1 \le (n + 5)/3 < n$ when $2n > 5$, that is for $n \ge 3$; the base case of line L1 covers $n \le 2$ since $T \ge 2$. From $n_{i+1} \le (n_i + 5)/3$ we get $n_{i+1} - 5/2 \le (n_i - 5/2)/3$, so $n_i - 5/2 \le (n - 5/2)/3^i$, and $n_i \le 3$ as soon as $3^i \ge 2n$, that is after at most $\lceil \log_3 (2n) \rceil$ steps; one more step reaches 2 if needed. Each step makes five calls, so the recursion tree is finite. $\square$

**Lemma 3 (products).** By strong induction on $n$, every call returns the product of its operands. For the call on $a$ and $b$, line L4 therefore gives $v(t) = A(t)B(t) = C(t)$ for $t \in \{0, 1, -1, -2\}$, where the sign of $v(t)$ is the product of the signs of $A(t)$ and $B(t)$, and $v(\infty) = a_2 b_2 = r_4$.

*Proof.* The base case returns the schoolbook product. A recursive call multiplies the magnitudes $|A(t)|$ and $|B(t)|$, of $k + 1 < n$ limbs by Lemmas 1 and 2, so by the induction hypothesis it returns $|A(t)||B(t)|$, and attaching the sign gives $A(t)B(t)$. $\square$

**Lemma 4 (interpolation).** The assignments of line L5 end with $r_0, r_1, r_2, r_3, r_4$ equal to the coefficients of $C$, and the divisions in it are exact.

*Proof.* Evaluating $C$,

$$v(1) = r_0 + r_1 + r_2 + r_3 + r_4, \quad v(-1) = r_0 - r_1 + r_2 - r_3 + r_4, \quad v(-2) = r_0 - 2r_1 + 4r_2 - 8r_3 + 16r_4 .$$

Follow line L5, writing $t_1, t_2, t_3$ for the first values of $r_1, r_2, r_3$:

- $v(-2) - v(1) = -3r_1 + 3r_2 - 9r_3 + 15r_4$, a multiple of 3, so $t_3 = -r_1 + r_2 - 3r_3 + 5r_4$ exactly.
- $v(1) - v(-1) = 2r_1 + 2r_3$, so $t_1 = r_1 + r_3$ exactly.
- $t_2 = v(-1) - v(0) = -r_1 + r_2 - r_3 + r_4$.
- $t_2 - t_3 = 2r_3 - 4r_4$ is even, and $(t_2 - t_3)/2 + 2r_4 = r_3$.
- $t_2 + t_1 - r_4 = r_2$.
- $t_1 - r_3 = r_1$.

With $r_0 = v(0)$ and $r_4 = v(\infty)$, all five coefficients are right. Every quotient is an integer combination of the $r_m$, so the divisions are exact. $\square$

**Theorem.** TOOM-3 returns $ab$ as $2n$ limbs.

*Proof.* By Lemmas 3 and 4, line L6 computes $\sum_m r_m x^m = C(x) = ab$. Each $r_m$ is nonnegative, so line L6 adds nonnegative shifted arrays, and every partial sum is at most $ab < \beta^{2n}$; the result fits in $2n$ limbs. Termination is Lemma 2. $\blacksquare$
