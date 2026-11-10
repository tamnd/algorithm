---
title: Lossy counting estimates are low by at most N/w and use at most w H_B entries
proves: [correctness]
status: full
---

Let $w = \lceil 1/\varepsilon \rceil$, so $1/w \le \varepsilon$. After $N$ items, the current bucket is $b = \lceil N/w \rceil$ and the number of completed buckets is $c = \lfloor N/w \rfloor$. Let $f_x$ be the true count of $x$ among the $N$ items. For an entry of $D$, write $(f, \Delta)$ for its pair.

**Lemma 1.** After each update (lines L1 to L6):

- (E) each entry $x \in D$ has $f \le f_x \le f + \Delta$ and $\Delta \le b - 1$, and
- (U) each item $x \notin D$ has $f_x \le c$.

*Proof.* By induction on $N$. For $N = 0$ the table is empty and all counts are 0. Assume (E) and (U) after $N - 1$ items, and let $x$ be item $N$, in bucket $b$. The values $b$ and $c$ do not fall, so (E) and (U) stay true for the items that the update does not touch, until the pruning.

- *Line L3.* Both $f$ and $f_x$ grow by 1, so (E) holds for $x$.
- *Line L4.* Here $x \notin D$. The first $N - 1$ items lie in buckets $1$ to $b - 1$ and in the first part of bucket $b$, so $\lfloor (N-1)/w \rfloor \le b - 1$. By (U), the count of $x$ before this item was at most $b - 1 = \Delta$. So now $f_x \le 1 + \Delta = f + \Delta$, and $f = 1 \le f_x$. Also $\Delta = b - 1$.
- *Lines L5 and L6.* A pruning happens when $N = bw$, so $c = b$. An entry $y$ is removed only if $f + \Delta \le b$, and by (E), $f_y \le f + \Delta \le b = c$. So (U) holds for $y$. $\square$

**Theorem 1 (error).** After $N$ items, for every item $x$, the estimate $\hat f_x$ of line L7 satisfies
$$ f_x - \left\lfloor \frac{N}{w} \right\rfloor \;\le\; \hat f_x \;\le\; f_x . $$
For a support $s > \varepsilon$, line L8 returns every $x$ with $f_x \ge sN$ and no $x$ with $f_x < (s - \varepsilon) N$.

*Proof.* If $x \in D$, then by (E), $\hat f_x = f \le f_x$ and $f_x - f \le \Delta \le b - 1 \le c$, because $\lceil N/w \rceil - 1 \le \lfloor N/w \rfloor$. If $x \notin D$, then $\hat f_x = 0 \le f_x$ and $f_x \le c$ by (U). In both cases $f_x - \hat f_x \le c = \lfloor N/w \rfloor \le N/w \le \varepsilon N$.

For the report, let $f_x \ge sN$. If $x \notin D$, then $f_x \le \varepsilon N < sN$, which is false. So $x \in D$, and $f \ge f_x - \varepsilon N \ge (s - \varepsilon) N$, so line L8 returns $x$. If $f_x < (s - \varepsilon) N$ and $x \in D$, then $f \le f_x < (s - \varepsilon) N$, so line L8 does not return $x$. $\square$

**Theorem 2 (space).** Right after the pruning at the end of bucket $B \ge 1$, the table has at most $w H_B$ entries, where $H_B = \sum_{i=1}^{B} 1/i \le 1 + \ln B$. At any time with $B = \lfloor N/w \rfloor$ completed buckets, it has at most $w H_B + w$ entries.

*Proof.* Look at the table right after the pruning at the end of bucket $B$. An entry with $\Delta = B - i$ was inserted in bucket $B - i + 1$, so $1 \le i \le B$. Let $d_i$ be the number of entries with $\Delta = B - i$.

Such an entry survived the pruning at the end of bucket $B$, so $f + (B - i) > B$, that is $f > i$. Its count $f$ counts occurrences in buckets $B - i + 1$ to $B$ only. Distinct entries belong to distinct items, so their occurrences are distinct items of the stream. The entries with $i \le j$ all count occurrences in the last $j$ buckets, which hold $jw$ items. Hence for each $j = 1, \ldots, B$,
$$ S_j := \sum_{i=1}^{j} i \, d_i \;\le\; \sum_{i=1}^{j} \sum_{\text{entries with this } i} f \;\le\; j w . $$

Now write the number of entries with the weights $1/(j(j+1))$ and $1/B$:
$$ \sum_{i=1}^{B} d_i \;=\; \sum_{j=1}^{B-1} \frac{S_j}{j(j+1)} + \frac{S_B}{B} . $$
This is an identity: the coefficient of $i \, d_i$ on the right is $\sum_{j=i}^{B-1} \left(\frac{1}{j} - \frac{1}{j+1}\right) + \frac{1}{B} = \frac{1}{i} - \frac{1}{B} + \frac{1}{B} = \frac{1}{i}$. With $S_j \le jw$,
$$ |D| = \sum_{i=1}^{B} d_i \;\le\; \sum_{j=1}^{B-1} \frac{jw}{j(j+1)} + \frac{Bw}{B} \;=\; w \left( \sum_{j=2}^{B} \frac{1}{j} + 1 \right) \;=\; w H_B . $$
The bound $H_B \le 1 + \ln B$ follows from $1/i \le \int_{i-1}^{i} dt/t$ for $i \ge 2$. Between the prunings at the ends of buckets $B$ and $B + 1$, the at most $w$ items of bucket $B + 1$ add at most $w$ entries, and before the first pruning there are at most $N < w$ entries. $\blacksquare$
