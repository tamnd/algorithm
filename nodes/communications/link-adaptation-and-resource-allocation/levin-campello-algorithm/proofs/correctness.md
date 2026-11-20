---
title: The Levin-Campello algorithm reaches an optimal loading from any start
proves: [correctness]
status: full
---

**Setting.** Subcarrier $i$ has the next-bit costs $d_i(k) = \Gamma 2^{k-1}/g_i$ for $k = 1, \ldots, m_i$, where $m_i = b_{\max}$ or $m_i = \infty$. They are positive and strictly increasing in $k$. A loading $b$ with $0 \le b_i \le m_i$ is the choice of the prefix $d_i(1), \ldots, d_i(b_i)$ of each list, and its power $E(b) = \sum_i \sum_{k \le b_i} d_i(k)$ is the sum of the chosen costs. Let $D$ be the set of all pairs $(i, k)$ with cost $d_i(k)$, and let $C(b)$ be the chosen pairs. For $b_i > 0$, the *last cost* of $i$ is $d_i(b_i)$; for $b_i < m_i$, the *next cost* of $i$ is $d_i(b_i + 1)$.

Let $E^*(t)$ be the least power of a loading with $t$ bits. Since each list is increasing, the $t$ cheapest elements of $D$ form a prefix of each list, so $E^*(t)$ is the sum of the $t$ smallest costs in $D$. Since all costs are positive, $E^*$ is strictly increasing.

**Definition.** A loading is *efficient* if its largest last cost is at most its smallest next cost (an empty side counts as $-\infty$ or $+\infty$).

**Lemma 1.** In any loading, the largest cost in $C(b)$ is the largest last cost, and the smallest cost in $D \setminus C(b)$ is the smallest next cost.

*Proof.* In list $i$ the chosen part is a prefix and the list is increasing, so its largest chosen cost is $d_i(b_i)$ and its smallest unchosen cost is $d_i(b_i + 1)$. Take the maximum and the minimum over $i$. $\square$

**Lemma 2 (efficient means optimal).** An efficient loading with $t$ bits has the power $E^*(t)$.

*Proof.* By Lemma 1, every chosen cost is at most every unchosen cost. Sort the costs of $D$ in increasing order. Then the chosen costs are $t$ values that are each at most every other value, so as a multiset they are the $t$ smallest values, and their sum is $E^*(t)$. $\square$

**Lemma 3 (the swap phase).** In each pass of lines L2 and L3 with $m$ at the largest last cost $c_\ell$ and $n$ at the smallest next cost $c_n < c_\ell$: (a) $m \ne n$; (b) the bit count does not change and the power falls by $c_\ell - c_n > 0$; (c) the phase stops, and it stops at an efficient loading.

*Proof.* (a) If $m = n$, then $c_\ell = d_m(b_m) < d_m(b_m + 1) = c_n$, which is false. (b) Line L3 removes the chosen element of cost $c_\ell$ and adds the unchosen element of cost $c_n$. Since $m \ne n$, the next cost of $n$ is not changed by the removal, so the new loading is a prefix of each list again. (c) The count $t = \sum_i b_i$ is fixed, and each subcarrier has at most $t$ bits, so there are finitely many loadings with $t$ bits. The power falls strictly in every pass, so no loading repeats, and the phase stops. It stops exactly when the test of line L2 fails, which is the definition of efficient. $\square$

**Lemma 4 (the number of swaps).** Order $D$ totally by $(\text{cost}, i, k)$, and let the implementation break ties so that line L3 removes the largest last element and adds the smallest next element in this order. Let $b^*$ be the loading whose chosen set $S$ is the first $t$ elements in this order. Then the swap phase makes at most $\frac12 \sum_i |b_i - b^*_i|$ swaps, where $b$ is the start.

*Proof.* As in Lemma 1, the largest chosen element in this order is the largest last element $x$, and the smallest unchosen element is the smallest next element $y$. Suppose a swap happens, so the cost of $x$ exceeds the cost of $y$, and $x$ comes after $y$ in the order. If $x \in S$, then every chosen element, which comes no later than $x$, lies in $S$, because $S$ is an initial segment; then $C(b) = S$, since both have $t$ elements, and $y$, being unchosen, comes after every element of $S$, including $x$. This contradicts the order of $x$ and $y$. So $x \notin S$. In the same way, if $y \notin S$, then every unchosen element comes no earlier than $y$ and lies outside $S$, so $S \subseteq C(b)$ and again $C(b) = S$, a contradiction. So $y \in S$. The swap removes $x \notin S$ and adds $y \in S$, so it lowers $|C(b) \triangle S|$ by exactly 2. The size of the symmetric difference is $\sum_i |b_i - b^*_i|$ at the start and is never negative, which gives the bound. $\square$

When all costs are different, the phase stops only at $C(b) = S$, so the bound is met with equality.

**Lemma 5 (tightening keeps efficiency).** Let $b$ be efficient with $t$ bits. Removing a bit at the largest last cost gives an efficient loading with $t - 1$ bits. Adding a bit at the smallest next cost $c$ gives an efficient loading with $t + 1$ bits.

*Proof.* Removal: let $c$ be the largest last cost, at subcarrier $m$. After the removal, the next cost of $m$ is $c$, and the other next costs are at least $c$ by efficiency, so the smallest next cost is $c$. The last costs are now the old ones except at $m$, where the new last cost is $c/2$ or absent; all are at most $c$. So the loading is efficient. Addition: the same argument with the roles of last and next costs exchanged; the new last cost of $n$ is $c$, the old last costs are at most $c$, the new next cost of $n$ is $2c$, and the other next costs are at least $c$. $\square$

**Theorem 1 (margin-adaptive form).** For a target $B$ with $0 \le B \le \sum_i m_i$ and any start $b$, the algorithm returns a loading with $B$ bits and the power $E^*(B)$.

*Proof.* By Lemma 3, after line L3 the loading is efficient with $t$ bits. If $t > B$, lines L4 and L5 remove $t - B$ bits; if $t < B$, lines L6 and L7 add $B - t$ bits, and a next bit exists at each step because $B \le \sum_i m_i$. By Lemma 5 the loading stays efficient, so by Lemma 2 its power at the end is $E^*(B)$. $\square$

**Theorem 2 (rate-adaptive form).** For a budget $P \ge 0$ and any start, the algorithm returns a loading with $t^* = \max\{t : E^*(t) \le P\}$ bits and the power $E^*(t^*)$, which is the most bits within the budget at the least power for that number of bits.

*Proof.* After the swap phase, the loading is efficient with some $t$ bits and power $E^*(t)$ (Lemmas 3 and 2). Lines L4 and L5 remove bits while the power exceeds $P$; by Lemma 5 the powers are $E^*(t), E^*(t-1), \ldots$, and since $E^*(0) = 0 \le P$ the loop stops at the largest $t' \le t$ with $E^*(t') \le P$. Lines L6 and L7 add a bit while $E^*(t') + c \le P$, where $c$ is the smallest next cost; by Lemmas 5 and 2 the sum $E^*(t') + c$ equals $E^*(t' + 1)$. So the loop stops at the first $t''$ with $E^*(t'' + 1) > P$, or when no next bit exists. Since $E^*$ is increasing, the set $\{t : E^*(t) \le P\}$ is an interval that starts at 0, and in both phases the loop stops at its largest element, $t^*$. Any loading within the budget with $t$ bits has $E^*(t) \le P$, so $t \le t^*$. $\square$

**Remark (cost).** With a max-heap of last costs and a min-heap of next costs, each move of a bit costs $O(\log N)$ heap work (with lazy deletion, $O(\log(N + M))$ for $M$ moves). Building the heaps costs $O(N)$. The total time is $O(N + M \log(N + M))$, where $M$ is the number of swaps plus the number of tightening steps.
