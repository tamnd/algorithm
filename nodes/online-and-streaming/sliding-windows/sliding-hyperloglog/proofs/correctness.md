---
title: Sliding HyperLogLog reads the HyperLogLog registers of each window exactly
proves: [correctness]
status: full
---

The notation is that of the page. Fix a register $j$. The items that the stream sends to register $j$ are $e_1, e_2, \ldots$ in the order of arrival, with timestamps $\tau(e_1) \le \tau(e_2) \le \cdots$ and ranks $r(e_i)$. Say that $e_k$ **dominates** $e_i$ when $k > i$ and $r(e_k) \ge r(e_i)$. Let $\tau'$ be the time of the last item of register $j$ so far, or $-\infty$ if there is none.

**Lemma 1 (the list).** After each update, $L_j$ holds, in the order of arrival, exactly the pairs $(\tau(e_i), r(e_i))$ of the items $e_i$ of register $j$ such that

- (a) no later item of register $j$ dominates $e_i$, and
- (b) $e_i$ was not removed by line L2. Each item removed by line L2 during the update at a time $\sigma$ has $\tau(e_i) < \sigma - W \le \tau' - W$.

The ranks of $L_j$ strictly decrease from the oldest pair to the newest pair, and each pair has time at least $\tau' - W$.

*Proof.* By induction on the updates of register $j$; updates of other registers do not change $L_j$. At the start the list is empty. Consider the update with a new item $e$ of rank $r$ at time $\tau$. Line L2 removes old pairs from the oldest end. Line L3 removes, from the newest end, the pairs with rank at most $r$; these are exactly the pairs that $e$ dominates, because by induction the ranks strictly decrease from the oldest to the newest pair, so the pairs with rank at most $r$ form a block at the newest end. A pair that $e$ does not dominate has a rank greater than $r$ and stays. Line L4 appends $e$, which no later item dominates yet. So (a) and (b) hold after the update, and the new list is the old one with pairs removed at both ends and $e$ at the end. The pair before $e$, if any, has a rank greater than $r$, so the ranks still strictly decrease. After line L2 each remaining pair has time at least $\tau - W$, and $e$ has time $\tau$, so each pair has time at least $\tau' - W$, with $\tau' = \tau$. $\square$

**Theorem 1 (exact registers).** Let $\tau$ be at or after the last timestamp of the stream and $0 \le w \le W$. Line L6 sets $M_j$ to the largest rank among the items of register $j$ with time in $[\tau - w, \tau]$, or 0 if there is none. This is the value of register $j$ of HyperLogLog, run with the same hash on the items of the window.

*Proof.* Let $u = \tau - w \ge \tau - W$. The items of register $j$ with time in $[u, \tau]$ are the items with time at least $u$, since no item has time greater than $\tau$; because times do not decrease, they form a final block $e_a, e_{a+1}, \ldots$ of the arrival order.

If the block is empty, each pair of $L_j$ belongs to an item with time less than $u$, so line L6 finds no pair and sets $M_j = 0$, which is right.

Otherwise let $R$ be the largest rank in the block, and let $e$ be the last item of the block with rank $R$. Each item after $e$ is in the block and has a rank less than $R$, by the choice of $e$, so no item dominates $e$, and (a) holds. Also $\tau(e) \ge u \ge \tau - W \ge \tau' - W$, so by Lemma 1 line L2 has not removed $e$, and $e$ is in $L_j$. Let $p$ be the oldest pair of $L_j$ with time at least $u$; it exists, because $e$ is such a pair. The item of $p$ is in the block, so its rank is at most $R$. The pair $p$ is $e$ or comes before $e$ in the list, and the ranks strictly decrease along the list, so its rank is at least $R$. So $M_j = R$. $\square$

**Corollary.** SHLL-QUERY$(w, \tau)$ returns the value that HyperLogLog, with the same hash and the same range corrections, returns after it reads the items with time in $[\tau - w, \tau]$. So each accuracy result for HyperLogLog on a stream with $n$ distinct items, such as the standard error of about $1.04/\sqrt{m}$ for an ideal random hash (Flajolet, Fusy, Gandouet and Meunier, Theorem 1), holds for the window with $n$ the number of distinct items in it. $\square$

**Lemma 2 (list length).** Each list has at most $65 - b$ pairs. Assume an ideal random hash: the rank bits of distinct items are independent of each other and of the register bits. Let $D$ be the number of distinct items of register $j$ with time in $[\tau' - W, \tau']$. Then, given the register bits, the expected length of $L_j$ is at most $H_D = 1 + \frac{1}{2} + \cdots + \frac{1}{D} \le 1 + \ln D$ (and 0 if $D = 0$).

*Proof.* The ranks in $L_j$ are distinct values in $\{1, \ldots, 65 - b\}$ by Lemma 1, which gives the first bound. By Lemma 1 each pair belongs to an item with time at least $\tau' - W$, and to an item that no later item dominates. Two occurrences of one item have the same hash, so an earlier occurrence is dominated by a later one; so each pair belongs to the last occurrence of its item. List the $D$ distinct items in the order of their last occurrences, $y_1, \ldots, y_D$. The item of a pair, say $y_i$, has a rank greater than the ranks of $y_{i+1}, \ldots, y_D$, since their last occurrences come later. The order $y_1, \ldots, y_D$ depends only on the stream and the register bits. Given these, the ranks of $y_i, \ldots, y_D$ are independent with one distribution, so by symmetry the probability that $y_i$ has a rank strictly greater than each of the other $D - i$ ranks is at most $1/(D - i + 1)$. Summing over $i$, the expected length is at most $\sum_{i=1}^{D} 1/(D - i + 1) = H_D$. $\square$

**Time.** In each update, line L4 appends one pair, and lines L2 and L3 remove pairs. Each pair is removed at most once, so the total work of lines L2 to L4 over $N$ updates is $O(N)$. One update removes at most $65 - b$ pairs. A query scans $m$ lists of at most $65 - b$ pairs each. $\square$
