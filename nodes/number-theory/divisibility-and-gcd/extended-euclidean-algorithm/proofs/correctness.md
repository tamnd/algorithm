---
title: The extended Euclidean algorithm returns gcd(a, b) and Bezout coefficients bounded by b/g and a/g
proves: [correctness, termination, time.worst, bit_operations.worst]
status: full
---

We use the pseudocode EXTENDED-EUCLID of the page, with inputs $a_0, b_0$ of any sign. Write $a = |a_0|$ and $b = |b_0|$. Number the values that the pairs take: $r_0 = a$, $r_1 = b$, and while $r_i \ne 0$, $q_i = \lfloor r_{i-1} / r_i \rfloor$ and

$$r_{i+1} = r_{i-1} - q_i r_i, \quad s_{i+1} = s_{i-1} - q_i s_i, \quad t_{i+1} = t_{i-1} - q_i t_i,$$

with $s_0 = 1, s_1 = 0, t_0 = 0, t_1 = 1$. Pass $i$ of the loop turns the pairs $(r_{i-1}, r_i)$, $(s_{i-1}, s_i)$, $(t_{i-1}, t_i)$ into $(r_i, r_{i+1})$, $(s_i, s_{i+1})$, $(t_i, t_{i+1})$. Let $k$ be the number of passes, so $r_{k+1} = 0$ and the loop returns from $(r_k, s_k, t_k)$.

**Lemma 1 (the remainder sequence).** The values $r_i$ are those of the [Euclidean algorithm](/euclidean-algorithm/) on $(a, b)$. So the loop stops after $k \le 2 + \log_\varphi \min(a, b)$ passes (for $a, b \ge 1$), and $r_k = \gcd(a, b) = \gcd(a_0, b_0)$.

*Proof.* $r_{i+1} = r_{i-1} - \lfloor r_{i-1}/r_i \rfloor r_i = r_{i-1} \bmod r_i$, which is the step of the Euclidean algorithm. Its correctness and its step bound are proved on that page. $\square$

**Lemma 2 (the invariant).** For each $i$ from $0$ to $k + 1$, $a s_i + b t_i = r_i$.

*Proof.* For $i = 0$: $a \cdot 1 + b \cdot 0 = a = r_0$. For $i = 1$: $a \cdot 0 + b \cdot 1 = r_1$. If it holds for $i - 1$ and $i$, then $a s_{i+1} + b t_{i+1} = (a s_{i-1} + b t_{i-1}) - q_i (a s_i + b t_i) = r_{i-1} - q_i r_i = r_{i+1}$. $\square$

**Theorem 1 (correctness).** EXTENDED-EUCLID$(a_0, b_0)$ stops and returns $(g, x, y)$ with $g = \gcd(a_0, b_0) \ge 0$ and $a_0 x + b_0 y = g$.

*Proof.* The loop stops by Lemma 1, with $r_k = g$. By Lemma 2, $a s_k + b t_k = g$. Line L9 sets $x = \sigma_a s_k$ and $y = \sigma_b t_k$, where $\sigma_a = -1$ if $a_0 < 0$ and $1$ otherwise, and likewise $\sigma_b$. Since $a_0 = \sigma_a a$ and $\sigma_a^2 = 1$, $a_0 x = a s_k$, and likewise $b_0 y = b t_k$. So $a_0 x + b_0 y = g$. If $a_0 = b_0 = 0$, the loop does not run and the result is $(0, 1, 0)$, which satisfies $0 \cdot 1 + 0 \cdot 0 = 0$. $\blacksquare$

**Lemma 3 (determinant and signs).** For $0 \le i \le k$:

1. $s_i t_{i+1} - s_{i+1} t_i = (-1)^i$.
2. $(-1)^i s_i \ge 0$ and $(-1)^{i+1} t_i \ge 0$; that is, the signs of the $s_i$ alternate (with zeros allowed), and so do the signs of the $t_i$.

*Proof.* (1) For $i = 0$: $1 \cdot 1 - 0 \cdot 0 = 1$. Step: $s_{i+1} t_{i+2} - s_{i+2} t_{i+1} = s_{i+1}(t_i - q_{i+1} t_{i+1}) - (s_i - q_{i+1} s_{i+1}) t_{i+1} = s_{i+1} t_i - s_i t_{i+1} = -(-1)^i$. (2) True for $i = 0, 1$: $s_0 = 1$, $s_1 = 0$, $t_0 = 0$, $t_1 = 1$. If true for $i - 1$ and $i$, then, since $q_i \ge 0$,

$$(-1)^{i+1} s_{i+1} = (-1)^{i-1} s_{i-1} + q_i (-1)^i s_i \ge 0,$$

and the same computation works for $t$. $\square$

**Lemma 4 (two exact identities).** For $0 \le i \le k$, if $a, b \ge 1$:

$$|s_i| \, r_{i+1} + |s_{i+1}| \, r_i = b, \qquad |t_i| \, r_{i+1} + |t_{i+1}| \, r_i = a.$$

*Proof.* By Lemma 2, $s_i r_{i+1} - s_{i+1} r_i = s_i (a s_{i+1} + b t_{i+1}) - s_{i+1}(a s_i + b t_i) = b (s_i t_{i+1} - s_{i+1} t_i) = (-1)^i b$ by Lemma 3 (1). Multiply by $(-1)^i$. By Lemma 3 (2), $(-1)^i s_i = |s_i|$ and $-(-1)^i s_{i+1} = (-1)^{i+1} s_{i+1} = |s_{i+1}|$, and the $r$ values are non-negative, so the left side is $|s_i| r_{i+1} + |s_{i+1}| r_i$. The identity for $t$ is the same computation: $t_i r_{i+1} - t_{i+1} r_i = a(t_i s_{i+1} - t_{i+1} s_i) = -(-1)^i a$. $\square$

**Theorem 2 (size of the coefficients).** Let $a, b \ge 1$ and $g = \gcd(a, b)$.

1. Each $|s_i| \le b/g$ and each $|t_i| \le a/g$, for $0 \le i \le k + 1$. In particular $|x| \le b/g$ and $|y| \le a/g$.
2. $|s_{k+1}| = b/g$ and $|t_{k+1}| = a/g$.
3. If $b \nmid a$, then $|x| \le b/(2g)$ and $|y| \le a/(2g)$. If $b \mid a$, then $(x, y) = (0, \pm 1)$.
4. $q_i |s_i| \le b/g$ and $q_i |t_i| \le a/g$ for $1 \le i \le k$, so no intermediate product is larger than the inputs.

*Proof.* Each $r_i$ with $i \le k$ is a positive multiple of $g$, so $r_i \ge g$. (1) For $1 \le j \le k + 1$, Lemma 4 with $i = j - 1$ gives $|s_j| r_{j-1} \le b$, so $|s_j| \le b/g$; and $|s_0| = 1 \le b/g$ because $g \mid b$. The same holds for $t$. (2) Lemma 4 with $i = k$, where $r_{k+1} = 0$ and $r_k = g$, gives $|s_{k+1}| g = b$ and $|t_{k+1}| g = a$. (3) If $b \mid a$, then $k = 1$ and the result is $(s_1, t_1) = (0, 1)$, up to the signs of line L9. Otherwise $k \ge 2$, because $r_2 = a \bmod b \ne 0$. Then $r_{k-1} > r_k = g$, since the remainders $r_1 > r_2 > \cdots > r_k$ strictly decrease, and $r_{k-1}$ is a multiple of $g$, so $r_{k-1} \ge 2g$. Lemma 4 with $i = k - 1$ gives $|s_k| r_{k-1} \le b$, so $|s_k| \le b/(2g)$, and likewise $|t_k| \le a/(2g)$. (4) By Lemma 3 (2), $s_{i-1}$ and $-q_i s_i$ have the same sign or are zero, so $|s_{i+1}| = |s_{i-1}| + q_i |s_i| \ge q_i |s_i|$, and $|s_{i+1}| \le b/g$ by (1). The same holds for $t$. $\blacksquare$

**Theorem 3 (cost).** On the word RAM, if $|a_0|$ and $|b_0|$ fit in a signed word, the algorithm uses $\Theta(\log m)$ word operations in the worst case, where $m = \min(|a_0|, |b_0|)$, and no value overflows. On inputs of at most $n$ binary digits it uses $O(n^2)$ bit operations.

*Proof.* Each pass does one division and three multiply-subtract steps, and by Lemma 1 there are $O(\log m)$ passes; the Fibonacci inputs of the Euclidean algorithm show the bound is reached. By Theorem 2 (1) and (4), every $s_i$, $t_i$ and product $q_i s_i$, $q_i t_i$ has absolute value at most $\max(a, b)$, so it fits in the word. In the bit model, the $r_i$ part costs $O(n^2)$, as proved for the Euclidean algorithm. Each $|s_i|, |t_i| < 2^n$ by Theorem 2, so the products $q_i s_i$ and $q_i t_i$ cost $O((1 + \lg q_i) n)$ bit operations each with schoolbook multiplication, and the subtractions $O(n)$. Summed over the passes this is $O(n (k + \sum_i \lg q_i))$. As on the Euclidean algorithm page, $q_1 q_2 \cdots q_k \le a$ when $a \ge b$ (with one extra pass with $q_1 = 0$ when $a < b$), so $\sum \lg q_i \le n$, and $k = O(n)$. The total is $O(n^2)$. $\blacksquare$
