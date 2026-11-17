---
title: The sweep over the end points returns a chain of maximum weight
proves: [correctness]
status: full
---

The input is a list of $n$ exons $I_j = (l_j, r_j, w_j)$ with integers $l_j \le r_j$ and real weights $w_j$. Two exons *overlap* when the closed intervals $[l_i, r_i]$ and $[l_j, r_j]$ share a position. A *chain* is a set of pairwise non-overlapping exons, and its weight is the sum of their weights. The empty chain has weight 0. For a set $X$ of exons, $\mathrm{OPT}(X)$ is the largest weight of a chain whose exons are all in $X$. Since the empty chain is allowed, $\mathrm{OPT}(X) \ge 0$.

**Order of the points.** Line L1 makes the $2n$ points $(l_j, 0, j)$ and $(r_j, 1, j)$, where 0 means a left point and 1 a right point. Line L2 sorts them as tuples, so a point with a smaller position comes first, and at equal positions every left point comes before every right point. Let $p_1, p_2, \ldots, p_{2n}$ be the sorted list. For $t = 0, 1, \ldots, 2n$, let $R_t$ be the set of exons whose right point is among $p_1, \ldots, p_t$.

**Lemma 1.** If $p_t$ is the left point of exon $j$, then $R_{t-1} = \{ i : r_i < l_j \}$.

*Proof.* Take an exon $i$. If $r_i < l_j$, the right point of $i$ has a smaller position than $p_t$, so it comes earlier and $i \in R_{t-1}$. If $r_i > l_j$, the right point of $i$ comes later. If $r_i = l_j$, the right point $(l_j, 1, i)$ comes after the left point $(l_j, 0, j)$ by the second key. So $i \notin R_{t-1}$ in both cases. This also holds for $i = j$, because $r_j \ge l_j$. $\square$

**Lemma 2.** Let exon $j$ and a chain $C \ni j$ be given, and let every exon of $C$ have $r_i \le r_j$. Then every exon $i \ne j$ of $C$ has $r_i < l_j$.

*Proof.* The exons $i$ and $j$ do not overlap, so $r_i < l_j$ or $r_j < l_i$. In the second case $r_j < l_i \le r_i$, which is false. $\square$

**Lemma 3 (invariant).** After line L4 has handled $p_1, \ldots, p_t$, the variable `best` is $\mathrm{OPT}(R_t)$. For each exon $j$ whose left point is among $p_1, \ldots, p_t$, the value $s[j]$ is $\mathrm{OPT}(\{ i : r_i < l_j \})$.

*Proof.* By induction on $t$. For $t = 0$, line L3 sets `best` to $0 = \mathrm{OPT}(\emptyset)$, and no $s[j]$ is claimed.

Let $t \ge 1$. If $p_t$ is the left point of exon $j$, line L6 sets $s[j]$ to `best`, which is $\mathrm{OPT}(R_{t-1})$ by the hypothesis. By Lemma 1 this is $\mathrm{OPT}(\{ i : r_i < l_j \})$. No right point is handled, so $R_t = R_{t-1}$ and `best` stays correct. No other $s$ value changes, because each exon has one left point.

If $p_t$ is the right point of exon $j$, then $R_t = R_{t-1} \cup \{ j \}$. The left point of $j$ comes before $p_t$, so $s[j]$ is already set and correct. A best chain in $R_t$ either does not hold $j$, and then its weight is at most $\mathrm{OPT}(R_{t-1})$, or it holds $j$. In the second case, every exon of the chain is in $R_t$, so its right point is not after $p_t$, and its right end is at most $r_j$. By Lemma 2, the other exons have $r_i < l_j$, so their weight is at most $s[j]$. So $\mathrm{OPT}(R_t) \le \max(\mathrm{OPT}(R_{t-1}), s[j] + w_j)$. Both values are reached: the first by a chain in $R_{t-1} \subseteq R_t$, and the second by a best chain in $\{ i : r_i < l_j \}$ with $j$ added, which is a chain because each of its exons ends before $l_j$, and whose exons are in $R_t$ by Lemma 1. Lines L7 and L8 set `best` to the larger of the two values. $\square$

At the end $R_{2n}$ holds every exon, so `best` is the weight of a best chain.

**Lemma 4 (the chain).** Define $\mathrm{ch}(\mathit{nil})$ as the empty list and $\mathrm{ch}(j) = \mathrm{ch}(\mathit{pred}[j])$ followed by $j$. Whenever `best` and `last` are read or written, $\mathrm{ch}(\mathit{last})$ is a chain of weight `best`, listed from left to right, whose exons all have their right point already handled.

*Proof.* Each $\mathit{pred}[j]$ is written once, at the left point of $j$, and never changes after that. At line L3 the claim holds with $\mathit{last} = \mathit{nil}$. Line L6 copies `last` into $\mathit{pred}[j]$ when the handled right points are those of $\{ i : r_i < l_j \}$ (Lemma 1). So $\mathrm{ch}(\mathit{pred}[j])$ is a chain of weight $s[j]$ whose exons all end before $l_j$. Then, when line L8 sets $\mathit{last} = j$, the list $\mathrm{ch}(j)$ is that chain followed by $j$: it is a chain, it is in order from left to right, and its weight is $s[j] + w_j$, the new `best`. $\square$

Lines L9 and L10 build $\mathrm{ch}(\mathit{last})$. The loop stops, because each step goes from $j$ to an exon whose right end is less than $l_j \le r_j$, so the right ends strictly decrease. So line L11 returns a best weight and a chain with that weight. $\blacksquare$

**Remarks.** An exon with $w_j \le 0$ is never put in the chain: `best` never decreases, and $s[j]$ is an earlier value of `best`, so $s[j] + w_j \le$ `best` and the strict test of line L7 fails. If all weights are at most 0, the result is $(0, [\,])$. Among best chains, the strict test keeps the first one found, so the last exon of the returned chain has the leftmost right point among the last exons of all best chains.

**Cost.** Line L2 sorts $2n$ tuples in $O(n \log n)$ time. The loop of line L4 does $O(1)$ work per point, and the loop of line L10 does at most $n$ steps. The arrays $s$ and $\mathit{pred}$ and the list of points take $O(n)$ space. If the end points are already sorted, or are integers in a range of size $O(n)$ that a counting sort can sort, the whole method runs in $O(n)$ time.
