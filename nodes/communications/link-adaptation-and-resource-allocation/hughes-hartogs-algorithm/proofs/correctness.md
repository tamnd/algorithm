---
title: The Hughes-Hartogs greedy rule gives an optimal integer loading when the incremental costs increase
proves: [correctness]
status: full
---

Subcarrier $i$ has the list of next-bit costs $d_i(1), d_i(2), \ldots, d_i(m_i)$, where $d_i(k) = e_i(k) - e_i(k-1)$ is the extra power of bit $k$ and $m_i = b_{\max}$ (or unbounded). A loading $b = (b_1, \ldots, b_N)$ with $0 \le b_i \le m_i$ has the power

$$E(b) = \sum_{i=1}^{N} e_i(b_i) = \sum_{i=1}^{N} \sum_{k=1}^{b_i} d_i(k),$$

since $e_i(0) = 0$. So a loading is the same as a choice of a prefix of each list, and its power is the sum of the chosen elements. Call the union of all lists, with each element tagged by its pair $(i, k)$, the multiset $D$.

**Assumption.** Each list is nondecreasing: $d_i(1) \le d_i(2) \le \cdots$, and all costs are positive. For $e_i(b) = \Gamma(2^b - 1)/g_i$ we have $d_i(k) = \Gamma 2^{k-1}/g_i$, which is positive and strictly increasing in $k$.

Order the elements of $D$ by cost, with ties broken by the index $i$ and then by $k$. This is a total order, written $\prec$, and it agrees with the order of the heap in lines L2 to L7, whose keys are $(d_i(k), i)$; within one list only the head is in the heap, so $k$ never needs to break a tie inside the heap.

**Lemma 1 (the heap holds the heads).** At the start of each pass of line L3, the heap holds exactly one entry $(d_i(b_i + 1), i)$ for each $i$ with $b_i < m_i$, and no other entry.

*Proof.* Line L2 inserts $(d_i(1), i)$ for each $i$, and all $b_i = 0$. Line L6 removes the entry of one $i$ and raises $b_i$ by 1. Line L7 inserts $(d_i(b_i + 1), i)$ for the new $b_i$ if $b_i < m_i$. So the statement holds again. $\square$

**Lemma 2 (each step takes the smallest unchosen element).** Let $S_t$ be the set of the first $t$ elements removed by line L6. Then $S_t$ consists of the $t$ smallest elements of $D$ in the order $\prec$.

*Proof.* By induction on $t$; the case $t = 0$ is clear. Suppose it holds for $t$. The unchosen elements of list $i$ are $d_i(b_i + 1), \ldots, d_i(m_i)$, and because the list is nondecreasing, the head $d_i(b_i + 1)$ is the smallest of them in $\prec$ (a tie in cost is broken by $k$, and the head has the smallest $k$). By Lemma 1 the heap holds exactly these heads, so its minimum is the smallest unchosen element of $D$. Adding it to the $t$ smallest elements gives the $t + 1$ smallest. $\square$

**Lemma 3 (the sum of the smallest elements is least).** Let $T$ be any set of $t$ elements of $D$. Then the cost sum of $T$ is at least the cost sum of $S_t$.

*Proof.* List the elements of $T$ in the order $\prec$ as $y_1 \prec \cdots \prec y_t$ and those of $S_t$ as $x_1 \prec \cdots \prec x_t$. Since $S_t$ holds the $t$ smallest elements of $D$, exactly $j - 1$ elements of $D$ come before $x_j$. The $j$ distinct elements $y_1, \ldots, y_j$ cannot all be among them, so $y_j$, the last of them, does not come before $x_j$, and the cost of $y_j$ is at least the cost of $x_j$. Summing over $j$ gives the claim. $\square$

**Theorem 1 (margin-adaptive form).** For a target $B \le \sum_i m_i$, the greedy rule stops with $\sum_i b_i = B$, and its loading has the least power among all loadings with $B$ bits.

*Proof.* With no budget, line L5 stops the loop exactly when $k = B$, and the heap is not empty before that because fewer than $\sum_i m_i$ elements have been removed. By Lemma 2 the chosen set is $S_B$, and by construction it is a prefix of each list, so it is a loading with power $E = \sum S_B$. Any other loading with $B$ bits is a set of $B$ elements of $D$, so by Lemma 3 its power is at least $E$. $\square$

**Theorem 2 (rate-adaptive form).** For a budget $P \ge 0$, the greedy rule returns a loading with the most bits among all loadings with power at most $P$, and with the least power among those.

*Proof.* Let $E^*(t)$ be the sum of the $t$ smallest elements of $D$. Since all costs are positive, $E^*$ is strictly increasing in $t$. By Theorem 1, $E^*(t)$ is the least power of a loading with $t$ bits. The loop keeps $E = E^*(k)$ by Lemma 2. It stops either when the heap is empty, so $k = \sum_i m_i$ and no loading has more bits, or when $E^*(k) + c > P$ for the smallest unchosen cost $c$, that is $E^*(k + 1) > P$. In the second case every loading with $t \ge k + 1$ bits has power at least $E^*(t) \ge E^*(k+1) > P$, so none fits. The returned loading has $k$ bits, fits the budget, and has the least power $E^*(k)$ for $k$ bits. $\square$

**Remark (why the assumption is needed).** Lemma 2 uses the fact that the head of each list is its smallest unchosen element. Without it the heap can miss a cheap element that lies behind an expensive head. For the lists $(4, 1)$ and $(3, 3)$ and $B = 2$, the rule takes $3$ and $3$ for the power 6, while the loading that takes both bits of the first list costs 5.

**Remark (cost).** Line L2 builds the heap in $O(N)$. Each pass of the loop does a constant number of heap operations, each $O(\log N)$, and at most $B + 1$ passes run in the MA form; in the RA form the number of passes is the number of bits returned plus one. The total time is $O(N + B \log N)$.
