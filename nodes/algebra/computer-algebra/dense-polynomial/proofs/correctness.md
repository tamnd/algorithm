---
title: The recursive dense operations keep the invariant, and pseudo-division is correct
proves: [correctness, termination]
status: full
---

Let $R$ be a commutative ring with a zero test. A value over $R$ is a list $c = [c_0, \ldots, c_{m-1}]$ standing for $\sum_i c_i x^i \in R[x]$. When $R = S[y]$ is itself represented in this way, operations in $R$ are the operations of this page one level down. We prove each statement for $R$ given that it holds for the coefficient ring; for the base ring, such as $\mathbb{Z}$ or $\mathbb{Q}$, the operations are exact by assumption. This is an induction on the number of variables.

**Lemma 1 (NORMALIZE).** NORMALIZE$(c)$ returns the longest prefix of $c$ whose last entry is nonzero, or the empty list, and it represents the same polynomial.

*Proof.* Lines L7 and L8 remove entries from the end while the last one is zero. The removed entries are coefficients equal to 0, so the polynomial does not change. When the loop stops, the list is empty or its last entry is nonzero. Each pass removes one entry, so it stops after at most $m$ passes. By the induction hypothesis, an entry of a polynomial ring is zero exactly when it is the empty list, so the zero test is correct at every level. $\square$

**Lemma 2 (ADD and MUL).** ADD$(a, b)$ and MUL$(a, b)$ represent $a + b$ and $ab$ and meet (N).

*Proof.* Line L1 sets $c_i = a_i + b_i$, with $a_i = 0$ for $i \ge m$ and $b_i = 0$ for $i \ge n$; this is the definition of the sum, coefficient by coefficient. For MUL, if one factor is zero the product is zero (line L3). Otherwise, line L5 adds $a_i b_j$ to $c_{i+j}$ once for each pair $(i, j)$, so at the end $c_k = \sum_{i + j = k} a_i b_j$, the coefficient of $x^k$ in $ab$, for $0 \le k \le m + n - 2$; there are no terms of higher degree. The sums and products of coefficients are correct and meet (N) one level down by the induction hypothesis. Lemma 1 gives (N) at the top level. $\square$

Scaling, negation, evaluation by Horner's rule and the derivative are similar: each computes the defining formula entry by entry and then normalizes.

**Theorem (pseudo-division).** Let $b \ne 0$, $\deg a = m - 1$, $\deg b = n - 1$ and $\ell = \operatorname{LC}(b)$. PSEUDO-DIVMOD$(a, b)$ terminates and returns $q, r$ with $\ell^{\max(m - n + 1, 0)} a = q b + r$ and $\deg r < \deg b$.

*Proof.* Write $E = \max(m - n + 1, 0)$ and let $k$ count the passes of the loop of line L10. We claim that at the test of line L10,

$$\ell^{k} a = q b + r, \qquad e = E - k, \qquad \deg r \le m - 1 - k .$$

At the start $k = 0$, $q = 0$, $r = a$ and $e = E$ (line L9), so the claim holds. Suppose it holds and the body runs, so $\deg r \ge \deg b$ and $r \ne 0$. Let $\delta = \deg r - \deg b \ge 0$ and $t = \operatorname{LC}(r) x^\delta$ (line L11). Line L12 gives the new values $q' = \ell q + t$ and $r' = \ell r - t b$. Then

$$q' b + r' = \ell q b + t b + \ell r - t b = \ell (q b + r) = \ell^{k+1} a .$$

The coefficient of $x^{\deg r}$ in $r'$ is $\ell \operatorname{LC}(r) - \operatorname{LC}(r) \ell = 0$, because $R$ is commutative, and $r'$ has no term of higher degree, because $\ell r$ has degree $\deg r$ and $t b$ has degree $\delta + \deg b = \deg r$. So $\deg r' \le \deg r - 1 \le m - 1 - (k + 1)$. Line L13 sets $e = E - (k + 1)$. The claim holds for $k + 1$.

Since $\deg r$ falls by at least one in each pass and the loop runs only while $\deg r \ge n - 1$, starting from $\deg r = m - 1$, there are at most $m - n + 1$ passes when $m \ge n$, and none when $m < n$. So the loop terminates with $k \le E$, $e = E - k \ge 0$ and $\deg r < \deg b$. Line L14 returns $\ell^e q$ and $\ell^e r$, and

$$\ell^{e} q\, b + \ell^{e} r = \ell^{e} \ell^{k} a = \ell^{E} a,$$

while scaling does not raise the degree of $r$. This is the stated identity. $\square$

**Uniqueness.** If $\ell$ is not a zero divisor of $R$, the pair $(q, r)$ is unique: if $\ell^E a = q b + r = q_1 b + r_1$ with $\deg r, \deg r_1 < \deg b$, then $(q - q_1) b = r_1 - r$. If $q \ne q_1$, the left side has degree at least $\deg b$, because its leading coefficient is $\operatorname{LC}(q - q_1)\, \ell \ne 0$, while the right side has smaller degree. So $q = q_1$ and $r = r_1$. Polynomial rings over $\mathbb{Z}$ or a field have no zero divisors, so this applies to every level of the recursive representation over such a base. $\blacksquare$
