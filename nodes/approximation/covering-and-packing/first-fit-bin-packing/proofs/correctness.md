---
title: First fit is feasible, uses at most 2 OPT - 1 bins, and less than 1.7 OPT + 2.9 bins
proves: [correctness]
status: full
---

We use the pseudocode of the page. The input is a list $s_1, \ldots, s_n$ with $0 < s_i \le 1$, $S = \sum_i s_i$, the bins are $B_1, \ldots, B_k$ in the order in which line L4 opens them, and $\ell(B)$ is the final load of bin $B$. We write $\mathrm{FF} = k$.

**Lemma 1 (feasibility).** First fit returns a partition of the items into bins, and each bin has load at most 1.

*Proof.* Line L3 picks a bin $j$ with $\mathrm{load}[j] + s_i \le 1$, or a new bin $k + 1$ with load 0, which also satisfies this test because $s_i \le 1$. Line L5 puts item $i$ into exactly that bin. So after each pass, each load is at most 1, and each processed item is in exactly one bin. $\square$

**Lemma 2 (later items do not fit earlier).** If $e < j$ and item $i$ is in $B_j$, then $s_i > 1 - \ell(B_e)$.

*Proof.* Bin $B_e$ was opened before $B_j$, so it existed when item $i$ came. Line L3 chose the least index with enough room, and it did not choose $e$, so $s_i$ was more than the free space of $B_e$ at that time. Loads only grow, so that free space is at least the final free space $1 - \ell(B_e)$. $\square$

**Theorem 1.** If $k \ge 2$, then $S > k/2$. Hence $\mathrm{FF} \le 2\lceil S \rceil - 1 \le 2\,\mathrm{OPT} - 1$ for $n \ge 1$.

*Proof.* Suppose two bins $B_e$, $B_j$ with $e < j$ have load at most $\frac12$. The first item of $B_j$ has size at most $\ell(B_j) \le \frac12 \le 1 - \ell(B_e)$, which contradicts Lemma 2. So at most one bin has load at most $\frac12$. If no bin has load at most $\frac12$, then $S > k/2$. If one bin $B_e$ does, take any other bin $B_j$. If $e < j$, Lemma 2 gives $\ell(B_j) > 1 - \ell(B_e)$. If $j < e$, Lemma 2 for the items of $B_e$ gives $\ell(B_e) > 1 - \ell(B_j)$. In both cases $\ell(B_e) + \ell(B_j) > 1$, and the other $k - 2$ bins each hold more than $\frac12$, so $S > 1 + \frac{k-2}{2} = \frac{k}{2}$. From $S > k/2$ we get $k < 2S \le 2\lceil S \rceil$, so $k \le 2\lceil S \rceil - 1$. For $k = 1$ the bound holds because $\lceil S \rceil \ge 1$. The size bound $\lceil S \rceil \le \mathrm{OPT}$ ends the proof. $\square$

## The bound 1.7 OPT + 2.9

The weight of an item of size $a$ is $w(a) = \frac65 a + v(a)$, with the bonus

$$v(a) = \begin{cases} 0 & a \le \frac16, \\ \frac35\left(a - \frac16\right) & \frac16 < a \le \frac13, \\ \frac1{10} & \frac13 < a \le \frac12, \\ \frac25 & a > \frac12. \end{cases}$$

The weight $w(B)$ of a set is the sum of the weights of its items, and $W$ is the weight of the whole list.

**Lemma 3 (upper bound on weight).** Each set of items with total size at most 1 has weight at most $\frac{17}{10}$. Hence $W \le \frac{17}{10}\,\mathrm{OPT}$.

*Proof.* Let $X$ be the set. It is enough to show $v(X) \le \frac12$, since $\frac65 \cdot 1 + \frac12 = \frac{17}{10}$.

*Case 1: $X$ has an item $a > \frac12$.* It is the only such item. The rest $R$ has total size less than $\frac12$, and we show $v(R) \le \frac1{10}$. At most one item of $R$ is larger than $\frac13$. If one item of $R$ is in $(\frac13, \frac12]$, the other items of $R$ have total size less than $\frac16$, so their bonus is 0, and $v(R) = \frac1{10}$. Otherwise each item of $R$ is at most $\frac13$, and at most two items of $R$ are larger than $\frac16$. With one such item $c$, $v(R) = \frac35(c - \frac16) \le \frac35 \cdot \frac16 = \frac1{10}$. With two such items $c, d$, $v(R) = \frac35(c + d - \frac13) < \frac35(\frac12 - \frac13) = \frac1{10}$. So $v(X) \le \frac25 + \frac1{10} = \frac12$.

*Case 2: each item is at most $\frac12$.* Then $v(a) \le \frac3{10} a$ for each item: for $a \le \frac16$ the bonus is 0; for $\frac16 < a \le \frac13$, $\frac35(a - \frac16) \le \frac3{10}a$ holds because it is the same as $a \le \frac13$; for $\frac13 < a \le \frac12$, $\frac1{10} \le \frac3{10} a$ holds because $a \ge \frac13$. So $v(X) \le \frac3{10} < \frac12$.

An optimal packing splits the list into $\mathrm{OPT}$ sets of total size at most 1, so $W \le \frac{17}{10}\mathrm{OPT}$. $\square$

**Lemma 4 (bins of weight at least 1).** A bin has weight at least 1 if it has an item larger than $\frac12$, or load at least $\frac56$, or two items larger than $\frac13$.

*Proof.* With an item $a > \frac12$: $w \ge \frac65 \ell + \frac25 > \frac65 \cdot \frac12 + \frac25 = 1$. With load at least $\frac56$: $w \ge \frac65 \cdot \frac56 = 1$. With two items larger than $\frac13$: the bonus is at least $\frac15$ and the load is more than $\frac23$, so $w > \frac45 + \frac15 = 1$. $\square$

Let $D_1, \ldots, D_s$ be the bins with weight less than 1, in the order of their index. By Lemma 4, each $D_t$ has all items at most $\frac12$, load less than $\frac56$, and at most one item larger than $\frac13$. Let $g_t = 1 - \ell(D_{t-1})$ for $t \ge 2$, the final free space of the previous such bin. Then $g_t > \frac16$, and by Lemma 2 each item of $D_t$ is larger than $g_t$.

**Lemma 5 (one item only at the end).** If $D_t$ has load at most $\frac12$, then $t = s$. In particular, each $D_t$ with $t < s$ has at least two items.

*Proof.* If $t < s$, each item of $D_{t+1}$ is larger than $1 - \ell(D_t) \ge \frac12$ by Lemma 2. But the items of $D_{t+1}$ are at most $\frac12$. A bin with one item at most $\frac12$ has load at most $\frac12$. $\square$

**Lemma 6 (the key inequality).** If $2 \le t \le s - 1$, then $w(D_t) \ge 1 + \frac95(g_t - g_{t+1})$.

*Proof.* Write $g = g_t$, $\ell = \ell(D_t) = 1 - g_{t+1}$, and let $m \ge 2$ be the number of items of $D_t$. Since $w(D_t) = \frac65 \ell + v(D_t)$, the claim is the same as

$$v(D_t) \ge \tfrac35 \ell + \tfrac95 g - \tfrac45. \qquad (\ast)$$

Each item is larger than $g > \frac16$, so each item in $(\frac16, \frac13]$ has bonus $\frac35 a - \frac1{10}$. Since $m g < \ell < \frac56$ and $g > \frac16$, we get $m \le 4$.

*No item larger than $\frac13$.* Then $v(D_t) = \frac35 \ell - \frac{m}{10}$, and $(\ast)$ is the same as $g \le \frac{8 - m}{18}$. For $m = 2$ this is $g \le \frac13$, true because the items are larger than $g$ and at most $\frac13$. For $m = 3$ it is $g \le \frac5{18}$, true because $3g < \frac56$. For $m = 4$ it is $g \le \frac29$, true because $4g < \frac56$ gives $g < \frac5{24}$.

*One item $b \in (\frac13, \frac12]$.* The other $m - 1$ items have total $\ell - b$, so $v(D_t) = \frac1{10} + \frac35(\ell - b) - \frac{m-1}{10}$, and $(\ast)$ is the same as $18 g + 6 b \le 10 - m$. For $m = 2$, let $c$ be the other item. The weight $\frac65(b + c) + \frac35 c$ is less than 1, so $6b < 5 - 9c < 5 - 9g$ and $18g + 6b < 9g + 5 < 8$, because $g < c \le \frac13$. For $m = 3$, the weight $\frac65 b + \frac95(\ell - b) - \frac1{10}$ is less than 1 and $\ell - b > 2g$, so $12 b < 11 - 36 g$, and $18 g + 6b < \frac{11}{2} < 7$. For $m = 4$, $b + 3g < \ell < \frac56$ gives $18g + 6b < 5 < 6$. $\square$

**Theorem 2.** $\mathrm{FF} < \frac{17}{10}\,\mathrm{OPT} + \frac{29}{10}$.

*Proof.* Each bin that is not a $D_t$ has weight at least 1. If $s \le 2$, then $W \ge k - s \ge k - 2$. If $s \ge 3$, Lemma 6 for $t = 2, \ldots, s-1$ and a telescoping sum give

$$\sum_{t=2}^{s-1} w(D_t) \ge (s - 2) + \tfrac95 (g_2 - g_s).$$

Here $g_2 > \frac16$. The bin $D_{s-1}$ has at least two items, by Lemma 5, and each is larger than $g_{s-1} > \frac16$, so $\ell(D_{s-1}) > \frac13$ and $g_s < \frac23$. So the sum is more than $s - 2 - \frac9{10}$, and with $w(D_1), w(D_s) \ge 0$ we get $W > (k - s) + s - \frac{29}{10} = k - \frac{29}{10}$. Lemma 3 gives $k < W + \frac{29}{10} \le \frac{17}{10}\mathrm{OPT} + \frac{29}{10}$. $\blacksquare$

The same proof works for [best fit](/best-fit-bin-packing/) only after a change: Lemma 2 is false for best fit, and the proof for best fit uses a different order of the bins.

**A family with ratio 5/3.** Fix $m \ge 1$ and a small $\varepsilon > 0$ with $6(\frac17 + \varepsilon) \le 1$. The list has $6m$ items of size $\frac17 + \varepsilon$, then $6m$ of size $\frac13 + \varepsilon$, then $6m$ of size $\frac12 + \varepsilon$. First fit puts six small items into each of $m$ bins, two items of the middle size into each of $3m$ bins, and each large item alone, so $\mathrm{FF} = 10m$. The packing with one item of each size per bin has load $\frac{41}{42} + 3\varepsilon \le 1$ for small $\varepsilon$ and uses $6m$ bins. No two items larger than $\frac12$ share a bin, so $\mathrm{OPT} \ge 6m$. So $\mathrm{FF} = \frac53\,\mathrm{OPT}$.
