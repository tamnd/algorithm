---
title: LRFU evicts the block of least CRF, is LFU when λ is 0 and LRU when λ is 1
proves: [correctness]
status: full
---

We use the pseudocode of the page, a cache of capacity $k \ge 1$, a parameter $0 \le \lambda \le 1$, an empty cache at the start, and a request sequence $\sigma_1 \ldots \sigma_n$, with $\sigma_t$ requested at time $t$. For a resident block $b$, let $t_1 < \ldots < t_j$ be the times of its references since it last entered the cache. Its CRF at time $t$ is $C_t(b) = \sum_{i} F(t - t_i)$ with $F(x) = 2^{-\lambda x}$.

**Lemma 1 (the stored value).** After each request, each resident block $b$ has $last[b] = t_j$ and $C[b] = C_{t_j}(b)$.

*Proof.* By induction on the references to $b$. When $b$ enters at time $t_1$, line L8 sets $C[b] = 1 = F(0) = C_{t_1}(b)$ and $last[b] = t_1$. If $b$ is referenced again at time $t$ while resident, line L3 sets
$$C[b] \leftarrow 1 + F(t - t_j) \, C_{t_j}(b) = F(0) + \sum_i F(t - t_j) F(t_j - t_i) = F(0) + \sum_i F(t - t_i) = C_t(b),$$
since $F(x) F(y) = F(x + y)$, and it sets $last[b] = t$. When $b$ leaves, its values are deleted, and a later load starts again at line L8. $\square$

**Lemma 2 (the order).** At time $t$, for resident blocks $a$ and $b$, $C_t(a) < C_t(b)$ if and only if $\kappa(a) < \kappa(b)$, where $\kappa(b) = \log_2 C[b] + \lambda \cdot last[b]$.

*Proof.* By Lemma 1, $C_t(b) = C[b] \cdot F(t - last[b])$, so $\log_2 C_t(b) = \log_2 C[b] - \lambda t + \lambda \cdot last[b] = \kappa(b) - \lambda t$. The term $-\lambda t$ is the same for all blocks, and $\log_2$ is increasing. $\square$

The key $\kappa(b)$ changes only at lines L3 and L8, when $b$ itself is requested. So the heap, ordered by $(\kappa(b), last[b])$ and updated at lines L4 and L9, has at its root the resident block of least CRF at the current time, with ties to the older last reference. Line L6 evicts this block. With a lazy heap, each request pushes one entry, and an entry is valid only if its time equals $last[b]$ for a resident $b$; line L6 discards the other entries. So the victim is the same.

**Claim 1 (λ = 0 gives LFU).** With $\lambda = 0$, LRFU evicts the resident block with the fewest references since it entered the cache, with ties to the block whose last reference is oldest.

*Proof.* With $\lambda = 0$, $F(x) = 1$ for all $x$, so $C_t(b) = j$, the number of references to $b$ since it entered. By Lemma 2 and the tie rule, the victim has the least $j$, and among those the least $last[b]$. This is LFU with counts kept for resident blocks only and ties broken by LRU. $\square$

**Claim 2 (λ = 1 gives LRU).** With $\lambda = 1$, LRFU evicts the resident block whose last reference is oldest.

*Proof.* First, $1 \le C[b] < 2$ after each request. Line L8 sets $C[b] = 1$. If $1 \le C[b] < 2$ before line L3, then, since $t - last[b] \ge 1$, the new value is $1 + 2^{-(t - last[b])} C[b] \le 1 + C[b]/2 < 2$, and it is at least 1. Now let $a$ and $b$ be resident with $last[a] < last[b]$. These are integers, so $last[b] \ge last[a] + 1$, and
$$\kappa(a) = \log_2 C[a] + last[a] < 1 + last[a] \le last[b] \le \log_2 C[b] + last[b] = \kappa(b).$$
So the block with the oldest last reference has the least key, and it is evicted. This is LRU. $\square$

In floating point, $C[b]$ can round to 2.0 after many references in a row. Then $\kappa(a) \le \kappa(b)$, and equality goes to $a$ by the tie rule, so the victim is still the least recently used block. The tests check this with 80 references in a row.

**Claim 3 (bounded CRF).** For $\lambda > 0$, $C[b] < 1/(1 - 2^{-\lambda})$.

*Proof.* The references are at distinct integer times, so $C_t(b) \le \sum_{x \ge 0} 2^{-\lambda x}$, and the sum of a finite part of this series with positive terms is less than the full sum, $1/(1 - 2^{-\lambda})$. $\square$

**Tests.** The tests compare the code, for $\lambda = 1$, with an LRU list, and for $\lambda = 0$, with a direct LFU on resident counts with LRU ties, on random traces. For $\lambda$ in $\{0.1, 0.3, 0.5, 0.7, 0.9\}$ they compare it with a direct sum of $F(t - t_i)$ over all references of each block.

**Cost.** A hash map gives $C[b]$ and $last[b]$ in $O(1)$ expected time. A heap with an index from blocks to positions does lines L4, L6, L7 and L9 in $O(\log k)$. The lazy heap of the code holds at most $2k + 17$ entries, since it is rebuilt from the $k$ resident blocks in $O(k)$ time when it has more than $2k + 16$; a rebuild happens at most once per $k + 16$ pushes, so the cost is $O(\log k)$ amortized per request. The space is $\Theta(k)$.
