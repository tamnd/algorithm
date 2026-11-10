---
title: The GK summary answers every rank query within εn
proves: [correctness]
status: full
---

We prove that the summary of lines L1 to L12 keeps the invariants (R) and (C), and that every query is answered within $\varepsilon n$ in rank. The proof of correctness is complete. At the end we give a sketch of the space bound, which is from Assadi, Joshi, Prabhu and Shah (2023) and is not proved here in full.

**Setup.** After $n$ inserts, give the $k$-th item the key (value, $k$). Keys are distinct, and the rank of an item is the position of its key among the $n$ keys. The summary holds tuples $e_1, \ldots, e_s$ sorted by key, with $r_{\min}(e_i) = g_1 + \cdots + g_i$ and $r_{\max}(e_i) = r_{\min}(e_i) + \Delta_i$. Let $\ell = \lceil 1/(2\varepsilon) \rceil$ and $t = \lfloor n/\ell \rfloor$. Since $\ell \ge 1/(2\varepsilon)$, we have $t \le n/\ell \le 2\varepsilon n$. Let $M = \max_i (g_i + \Delta_i)$.

**Lemma 1 (invariant R).** After each operation, $\sum_i g_i = n$, the last tuple holds the item of largest key with $\Delta_s = 0$, and $r_{\min}(e_i) \le \operatorname{rank}(e_i) \le r_{\max}(e_i)$ for each $i$.

*Proof.* By induction on the operations. The empty summary satisfies the claims. Consider Insert($x$) with key $\kappa = (x, n)$, where $n$ is the new count. The key $\kappa$ is larger than every older key with value at most $x$, so line L2 finds the first tuple $e_i$ with key above $\kappa$. After the insert, each old item with key above $\kappa$ moves up one rank, and each other old item keeps its rank.

- Tuples before position $i$ keep their rank, their $r_{\min}$ (the prefix of $g$ values does not change) and their $\Delta$.
- Tuples at position $i$ and after it gain 1 in rank. Their $r_{\min}$ also gains 1, from the new $g = 1$ before them, and $\Delta$ does not change.
- Line L3: no tuple has a larger key. The last tuple holds the largest old key by induction, so $\kappa$ is the largest key and $\operatorname{rank}(x) = n$. The new tuple has $r_{\min} = n = r_{\max}$, and it becomes the last tuple with $\Delta = 0$.
- Line L4: let $\rho = r_{\min}(e_{i-1})$ before the insert, with $\rho = 0$ if $i = 1$. The new tuple has $r_{\min} = \rho + 1$. The item $x$ has a key above that of $e_{i-1}$, so $\operatorname{rank}(x) \ge \operatorname{rank}(e_{i-1}) + 1 \ge \rho + 1$. The key of $x$ is below that of $e_i$, so $\operatorname{rank}(x) \le \operatorname{rank}_{\text{new}}(e_i) - 1 = \operatorname{rank}_{\text{old}}(e_i) \le r_{\max,\text{old}}(e_i) = \rho + g_i + \Delta_i$. The new tuple claims $r_{\max} = \rho + 1 + (g_i + \Delta_i - 1)$, which is the same bound.

The sum of the $g$ values grows by 1, which matches the new $n$. Now consider line L8. It deletes a run $e_j, \ldots, e_i$ with $i < s$ and adds $G^*_i = g_j + \cdots + g_i$ to $g_{i+1}$. No item changes rank. For a tuple before $e_j$ the prefix sum of $g$ values does not change. For a tuple after $e_i$ the prefix sum loses $G^*_i$ and gains it back at $e_{i+1}$. So no remaining $r_{\min}$ changes, and no $\Delta$ changes. The sum of the $g$ values does not change. The last tuple is never deleted, since $i < s$. $\square$

**Lemma 2 (invariant C).** After each operation, $M \le \max(1, t)$.

*Proof.* By induction. Line L3 makes a tuple with $g + \Delta = 1$. Line L4 makes a tuple with $g + \Delta = 1 + (g_i + \Delta_i - 1) = g_i + \Delta_i \le M$. An insert changes the $g$ and $\Delta$ of no other tuple. So an insert does not raise $M$ above $\max(1, M)$, and $t$ never goes down. Line L8 changes only $e_{i+1}$, whose new value is $G^*_i + g_{i+1} + \Delta_{i+1}$, and line L7 allows the merge only when this is at most $t$. $\square$

**Theorem 1.** For each $n \ge 1$ and each $r$ with $1 \le r \le n$, Query($r$) returns an item with rank in $[r - \varepsilon n, r + \varepsilon n]$. For repeated values, some copy of the returned value has rank in this range.

*Proof.* By Lemma 2 and $t \le 2\varepsilon n$, either $M \le 2\varepsilon n$, or $M = 1$.

*Line L9.* Here $r - \varepsilon n \le 1$. The first copy of $x_{\min}$ has rank 1, and $r - \varepsilon n \le 1 \le r \le r + \varepsilon n$.

*Line L11.* Here $r_{\max}(e_j) \le r + \varepsilon n$ for each $j$. By Lemma 1 the last tuple holds the item of rank $n$, so $n = r_{\min}(e_s) = r_{\max}(e_s) \le r + \varepsilon n$, and $n \ge r \ge r - \varepsilon n$.

*Line L12.* Line L9 did not return, so $r - \varepsilon n > 1$, and $r > 1$. First we show that $j \ge 2$. We have $r_{\max}(e_1) = g_1 + \Delta_1 \le M$. If $M \le 2\varepsilon n$, then $r + \varepsilon n > 1 + 2\varepsilon n > M$. If $M = 1$, then $r + \varepsilon n > 1 = M$. In both cases $e_1$ does not satisfy the test of line L10, so $j \ge 2$ and $e_{j-1}$ exists. By the choice of $j$, $r_{\max}(e_{j-1}) \le r + \varepsilon n$, and Lemma 1 gives $\operatorname{rank}(e_{j-1}) \le r + \varepsilon n$. For the lower side,
$$\operatorname{rank}(e_{j-1}) \ge r_{\min}(e_{j-1}) = r_{\min}(e_j) - g_j = r_{\max}(e_j) - g_j - \Delta_j > r + \varepsilon n - M.$$
If $M \le 2\varepsilon n$, the right side is at least $r - \varepsilon n$. If $M = 1$, the rank is an integer above $r + \varepsilon n - 1 \ge r - 1$, so it is at least $r$. In both cases $\operatorname{rank}(e_{j-1}) \ge r - \varepsilon n$. $\square$

**Corollary.** For $\phi \in (0, 1]$, Query($\lceil \phi n \rceil$) returns an $\varepsilon$-approximate $\phi$-quantile.

**The space bound (sketch).** Assadi, Joshi, Prabhu and Shah (Lemma 4.1) prove that after the loop of line L7 the summary has $O(\ell \log t) = O((1/\varepsilon)\log(\varepsilon n))$ tuples. We give only the outline. A tuple of band value $b$ has an age between about $2^{b-1}$ and $2^{b+1}$ steps (their Observation 2.4), so there are $O(\log t)$ band values, and at most $\ell \cdot 2^{\alpha + 1}$ items have arrived in the steps that make up bands 0 to $\alpha$. Merges send a tuple and its segment only into a tuple of the same or a higher band, so tuples of bands at most $\alpha$ cover only items of bands at most $\alpha$. After the loop, each tuple $e_i$ with $i < s$ is of type 1, $b_i > b_{i+1}$, or of type 2, $G^*_i + g_{i+1} + \Delta_{i+1} > t$. For type 2, the value $\Delta_{i+1}$ was fixed when $e_{i+1}$ arrived and is at most the step of its arrival, so $G^*_i + g_{i+1}$ is at least about $2^{\alpha - 1}$ with $\alpha = b_{i+1}$. These sums count disjoint sets of items of bands at most $\alpha$, of which there are $O(\ell 2^\alpha)$, so there are $O(\ell)$ type 2 tuples for each $\alpha$. A similar charge, which uses the fact that a tuple is always deleted with its whole segment, gives $O(\ell)$ type 1 tuples for each $\alpha$ (their Lemma 4.3). Summing over the $O(\log t)$ bands gives the bound. $\blacksquare$
