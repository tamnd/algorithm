---
title: Modified Kneser-Ney gives a proper distribution after every history when each discount D(k) lies in [0, k], and it reduces to Kneser-Ney when the three discounts are equal
proves: [correctness]
status: full
---

We use the notation of the page. Level $n$ uses the raw counts $a_n(g) = c(g)$, and each level $m < n$ uses the continuation counts $a_m(g) = N_{1+}(\cdot\, g)$. Lines L1 and L2 compute them as on the [Kneser-Ney](/kneser-ney-smoothing/) page, with the same proof: every $(m+1)$-gram that ends at a predicted token is the suffix of the n-gram that ends there, because of the padding with $n - 1$ copies of <s>. For a history $h$ of length $m - 1$ we write $T(h) = \sum_x a_m(h x)$ and $N_r(h\, \cdot)$ for the number of $x$ with $a_m(h x) = r$, with $N_{3+}(h\, \cdot)$ for $r \ge 3$. The discount of a count $k$ at level $m$ is $D(0) = 0$, $D(1) = D_1$, $D(2) = D_2$ and $D(k) = D_{3+}$ for $k \ge 3$.

**Theorem 1 (a proper distribution).** Assume that at every level $0 \le D_1 \le 1$, $0 \le D_2 \le 2$ and $0 \le D_{3+} \le 3$, that is $0 \le D(k) \le k$ for every $k$. Then for every level $m \ge 0$ and every history $h$ of length $m - 1$, $P_m(w \mid h) \ge 0$ and $\sum_{w \in V} P_m(w \mid h) = 1$.

*Proof.* Induction on $m$. Level 0 is uniform on $V$. Let $m \ge 1$. If $T(h) = 0$, line L6 returns $P_{m-1}(w \mid h')$, which sums to 1. Otherwise, by the assumption $a_m(h w) - D(a_m(h w)) \ge 0$ for every $w$, and it is 0 when $a_m(h w) = 0$. Sum line L8 over $w$:

$$\sum_w \frac{a_m(h w) - D(a_m(h w))}{T(h)} = 1 - \frac{\sum_{w :\, a_m(h w) > 0} D(a_m(h w))}{T(h)} = 1 - \frac{D_1 N_1(h\, \cdot) + D_2 N_2(h\, \cdot) + D_{3+} N_{3+}(h\, \cdot)}{T(h)} = 1 - \gamma(h),$$

where the middle step groups the seen words by their count. The second term adds $\gamma(h) \sum_w P_{m-1}(w \mid h') = \gamma(h)$ by the induction hypothesis, and $\gamma(h) \ge 0$. So the total is 1 and every term is non-negative. $\square$

The bounds are tight. If $D_2 > 2$, a word seen twice gets a negative first term; if only $D_1 > 1$, a word seen once does. The code raises an error instead of clipping, because a clipped discount no longer matches $\gamma(h)$ and the row no longer sums to 1.

**Theorem 2 (positivity).** Assume in addition that the discounts of level 1 are 0, that every word of $V$ was seen, and that all discounts of the levels $m \ge 2$ are positive. Then $P_m(w \mid h) > 0$ for all $w$ and $h$.

*Proof.* At level 1 with zero discounts, $P_1(w) = a_1(w) / T()$, and $a_1(w) \ge 1$ for every seen word because it ends at least one seen bigram (for $n = 1$, $a_1(w) = c(w) \ge 1$). At a level $m \ge 2$ with $T(h) > 0$, at least one word was seen after $h$, so $\gamma(h) > 0$ and $P_m(w \mid h) \ge \gamma(h) P_{m-1}(w \mid h') > 0$. With $T(h) = 0$ the level returns $P_{m-1}$. $\square$

**Theorem 3 (equal discounts give Kneser-Ney).** If $D_1 = D_2 = D_{3+} = D$ at every level, the model is interpolated Kneser-Ney with the discount $D$ at that level.

*Proof.* Then $D(k) = D$ for every $k \ge 1$, so $a - D(a) = \max(a - D, 0)$ for every integer $a \ge 0$ when $D \le 1$, and $\gamma(h) = D (N_1 + N_2 + N_{3+})(h\, \cdot) / T(h) = D N_{1+}(h\, \cdot) / T(h)$. These are the two terms of Kneser-Ney. $\square$

**Lemma 4 (the default discounts).** Let $n_r$ be the number of keys of a level with count $r$, with $n_1, n_2 > 0$, and $Y = n_1 / (n_1 + 2 n_2)$. The estimates of Chen and Goodman are $D_r = r - (r+1) Y n_{r+1} / n_r$ for $r = 1, 2$ and $D_{3+} = 3 - 4 Y n_4 / n_3$. Then:

1. $D_1 = Y$, so $0 < D_1 \le 1$ always.
2. $D_r = r - Y r^*$, where $r^* = (r+1) n_{r+1} / n_r$ is the Good-Turing adjusted count.
3. $D_2$ and $D_{3+}$ can be negative. So the default needs a check.

*Proof.* (1) $D_1 = 1 - 2 Y n_2 / n_1 = 1 - 2 n_2 / (n_1 + 2 n_2) = n_1 / (n_1 + 2 n_2) = Y$, and $0 < Y \le 1$. (2) is the definition of $r^*$ rewritten. (3) Take $n_1 = n_2 = 1$ and $n_3 = 6$. Then $Y = 1/3$ and $D_2 = 2 - 3 \cdot \frac13 \cdot 6 = -4$. $\square$

When $n_3 = 0$ the formula for $D_{3+}$ divides by zero, and when $n_2 = 0$ the formula for $D_2$ does. The implementation raises an error in all of these cases and accepts explicit discounts.
