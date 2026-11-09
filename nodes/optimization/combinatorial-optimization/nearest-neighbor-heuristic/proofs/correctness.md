---
title: The nearest neighbor rule returns a tour, and with metric costs the tour is within (lg n rounded up + 1)/2 of the optimum
proves: [correctness, termination, approximation-ratio]
status: full
---

Let $V$ be the set of $n \ge 2$ cities, with symmetric costs $c(u, v) \ge 0$, and let $\mathrm{OPT}$ be the cost of an optimal tour $T^*$.

**Lemma 1 (tour).** The algorithm stops, and it returns every city exactly once.

*Proof.* Line L3 runs exactly $n - 1$ times. Before iteration $t$ (for $t = 1, \ldots, n-1$), exactly $t$ cities are visited, so at least one city is unvisited, and lines L5 and L6 set *next* to an unvisited city. Line L7 appends it and marks it, so no city appears twice. After $n - 1$ iterations the list holds $n$ distinct cities, which are all of $V$. $\square$

Write the returned tour as $p_1 = s, p_2, \ldots, p_n$ and close it with $p_{n+1} = p_1$. For each city $i = p_t$ let $\ell_i = c(p_t, p_{t+1})$, the cost of the tour edge that leaves $i$. The tour costs $\sum_{i \in V} \ell_i$. From now on assume the triangle inequality $c(u, w) \le c(u, v) + c(v, w)$.

**Lemma 2.** For all distinct cities $i, j$, $c(i, j) \ge \min(\ell_i, \ell_j)$.

*Proof.* Say $i = p_t$ comes before $j = p_u$ in the tour, so $t < u \le n$. Then $t \le n - 1$, so the edge leaving $i$ was chosen by line L6 in the iteration where $cur = i$. At that time $j$ was unvisited, and line L6 keeps a city with least cost among the unvisited ones, so $\ell_i = c(i, p_{t+1}) \le c(i, j)$. The case where $j$ comes first is symmetric. $\square$

**Lemma 3.** For all distinct cities $i, j$, $2\,c(i, j) \le \mathrm{OPT}$. In particular $2 \ell_i \le \mathrm{OPT}$ for every $i$.

*Proof.* The cities $i$ and $j$ split $T^*$ into two paths from $i$ to $j$. By the triangle inequality, applied along each path, each path costs at least $c(i, j)$. So $\mathrm{OPT} \ge 2\,c(i, j)$. Each $\ell_i$ is $c(i, j)$ for some $j \ne i$. $\square$

**Lemma 4 (shortcut).** Let $H \subseteq V$ with $m = |H| \ge 2$, and let $h_1, \ldots, h_m$ be the cities of $H$ in the order of $T^*$, with $h_{m+1} = h_1$. Then $\sum_{t=1}^{m} c(h_t, h_{t+1}) \le \mathrm{OPT}$.

*Proof.* For each $t$, the part of $T^*$ from $h_t$ to $h_{t+1}$ costs at least $c(h_t, h_{t+1})$ by the triangle inequality. These $m$ parts are disjoint and together form $T^*$. (For $m = 2$ this is Lemma 3.) $\square$

Now number the cities $1, \ldots, n$ so that $\ell_1 \ge \ell_2 \ge \cdots \ge \ell_n$.

**Lemma 5.** For every integer $k$ with $1 \le k < n$, $\mathrm{OPT} \ge 2 \sum_{i=k+1}^{\min(2k, n)} \ell_i$.

*Proof.* Let $m = \min(2k, n) \ge 2$, $H = \{1, \ldots, m\}$ and $q = m - k$, so $1 \le q \le k$. Take the cyclic sequence of Lemma 4 for $H$. It has $m$ terms $c(h_t, h_{t+1})$, and each city of $H$ is an end of exactly two of them. By Lemma 2 each term is at least $\ell$ of one of its two ends. Assign each term to such an end, and let $a_h \in \{0, 1, 2\}$ be the number of terms assigned to city $h$. Then $\sum_{h \in H} a_h = m = k + q$ and, by Lemma 4,

$$ \mathrm{OPT} \ge \sum_{h=1}^{m} a_h \ell_h. $$

For $h \le k$, $\ell_h \ge \ell_k$. For $h > k$, $\ell_h \le \ell_k$ and $a_h \le 2$. So

$$ \sum_{h=1}^{m} a_h \ell_h \ \ge\ \ell_k \sum_{h \le k} a_h + \sum_{h > k} a_h \ell_h \ =\ \ell_k (k + q) - \sum_{h > k} a_h (\ell_k - \ell_h) \ \ge\ \ell_k (k + q) - 2 \sum_{h > k} (\ell_k - \ell_h). $$

The last sum has $q$ terms, so the right side is $\ell_k (k - q) + 2 \sum_{h=k+1}^{m} \ell_h \ge 2 \sum_{h=k+1}^{m} \ell_h$, because $k \ge q$ and $\ell_k \ge 0$. $\square$

**Theorem (Rosenkrantz, Stearns and Lewis, 1977).** With metric costs and $n \ge 2$, the tour returned by the algorithm costs at most $\frac{1}{2}(\lceil \lg n \rceil + 1) \cdot \mathrm{OPT}$.

*Proof.* Let $r = \lceil \lg n \rceil \ge 1$. For $j = 0, 1, \ldots, r - 1$, the number $k = 2^j$ satisfies $k \le 2^{r-1} < n$, so Lemma 5 applies. The index ranges $\{2^j + 1, \ldots, \min(2^{j+1}, n)\}$ for $j = 0, \ldots, r-1$ are disjoint, and their union is $\{2, \ldots, n\}$, because $2^r \ge n$. Adding the $r$ inequalities gives $r \cdot \mathrm{OPT} \ge 2 \sum_{i=2}^{n} \ell_i$. Lemma 3 gives $\mathrm{OPT} \ge 2 \ell_1$. Adding these,

$$ (r + 1)\,\mathrm{OPT} \ \ge\ 2 \sum_{i=1}^{n} \ell_i, $$

and the sum on the right is the cost of the tour. $\blacksquare$

**Remark.** The bound is tight up to a constant factor: Rosenkrantz, Stearns and Lewis construct metric instances for infinitely many $n$ on which the ratio exceeds $\frac{1}{3}\lg(n + 1) + \frac{4}{9}$. That construction is not reproduced here. Without the triangle inequality Lemmas 3 and 4 fail, and the ratio is unbounded.
