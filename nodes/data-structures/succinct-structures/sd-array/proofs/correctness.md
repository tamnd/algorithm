---
title: The rank, select and access of the SD-array are correct
proves: [correctness]
status: full
---

Let $B$ have length $n$ and its 1s at $p_0 < \cdots < p_{m-1}$, with $m \ge 1$, and let $\ell$, $Lo$ and $H$ be the [Elias-Fano](/elias-fano-encoding/) code of this sequence with universe $n$. Write $h_j = \lfloor p_j / 2^\ell \rfloor$, so $p_j = h_j 2^\ell + Lo[j]$. We use two facts proved on the Elias-Fano page: the $(j+1)$-th 1 of $H$ is at $h_j + j$ (fact A), and for $0 \le h \le \lfloor (n-1)/2^\ell \rfloor$, with $P(h) = 0$ for $h = 0$ and $P(h) = \text{SELECT0}_H(h) + 1$ otherwise, $P(h) - h = |\{j : h_j < h\}|$ (fact B).

**Select1 (line L1).** By fact A, SELECT1$_H(j) - (j - 1) = h_{j-1}$, so line L1 returns $h_{j-1} 2^\ell + Lo[j-1] = p_{j-1}$, the position of the $j$-th 1.

**Rank1 (lines L2 to L7).** If $i = n$, every 1 is before $i$ and line L2 returns $m$. Let $0 \le i < n$, $h = \lfloor i / 2^\ell \rfloor$ and $l = i \bmod 2^\ell$, so $0 \le h \le \lfloor (n-1)/2^\ell \rfloor$. Let $J_{<} = \{j : h_j < h\}$, $J_= = \{j : h_j = h\}$ and $J_> = \{j : h_j > h\}$. Since the $h_j$ are nondecreasing, these are consecutive ranges of indices in this order. By fact B with $h$, line L6 sets $r = P(h) - h = |J_<|$. By fact B with $h + 1$, $P(h+1) - (h+1) = |J_<| + |J_=|$, and line L5 sets $s = P(h+1) - 1 - P(h) = |J_=|$. So the indices of bucket $h$ are $J_= = \{r, \ldots, r + s - 1\}$. Fact B applies to $h + 1$ when $h + 1 \le \lfloor (n-1)/2^\ell \rfloor + 1$, which holds, because $H$ has $\lfloor (n-1)/2^\ell \rfloor + 1$ zeros. Now:

- for $j \in J_<$, $p_j < (h_j + 1) 2^\ell \le h 2^\ell \le i$, so each such 1 is before $i$;
- for $j \in J_>$, $p_j \ge (h+1) 2^\ell > i$, so none is before $i$;
- for $j \in J_=$, $p_j = h 2^\ell + Lo[j] < h 2^\ell + l = i$ if and only if $Lo[j] < l$.

So $\text{rank}_1(i) = r + |\{t < s : Lo[r + t] < l\}|$, which line L7 returns. The positions in $J_=$ are strictly increasing with the same high part, so $Lo[r], \ldots, Lo[r + s - 1]$ are strictly increasing, and the binary search for the first $t$ with $Lo[r + t] \ge l$ computes this count.

**Access (lines L8, L9).** Let $r = \text{rank}_1(i)$, the number of 1s before $i$. If $B[i] = 1$, then $i = p_r$, so $r < m$ and SELECT1$(r + 1) = p_r = i$. If $B[i] = 0$, then either $r = m$, or the next 1 after the first $r$ ones is $p_r > i$, so SELECT1$(r + 1) \ne i$. Line L9 returns $B[i]$ in both cases.

**Select0 (line L10).** The function $f(q) = (q + 1) - \text{rank}_1(q + 1) = \text{rank}_0(q + 1)$ is nondecreasing in $q$ and increases by one exactly at the positions $q$ with $B[q] = 0$. For $1 \le j \le n - m$, the least $q$ with $f(q) \ge j$ is therefore the position of the $j$-th 0, and $f(n - 1) = n - m \ge j$ ensures that it lies in $[0, n-1]$, the range of the binary search.

**The case $m = 0$.** Then $\ell = 0$, $H$ has only zeros, every rank is $0$ by fact B, and access returns 0 by line L9. $\blacksquare$
