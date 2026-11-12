---
title: Smith's rule minimizes the weighted sum of completion times
proves: [correctness]
status: full
---

We use the notation of the page. There are $n$ jobs, all present at time $0$, with $p_j \ge 0$ and $w_j > 0$. For an order $\pi$, the cost is $F(\pi) = \sum_{k=1}^{n} w_{\pi(k)} C_{\pi(k)}$ with $C_{\pi(k)} = \sum_{i \le k} p_{\pi(i)}$. A schedule with idle time has a larger or equal cost than the same order without idle time, so we only look at orders.

**Lemma (adjacent swap).** Let $\pi'$ be $\pi$ with the jobs $i = \pi(k)$ and $j = \pi(k+1)$ swapped. Then $F(\pi') - F(\pi) = w_i p_j - w_j p_i$.

*Proof.* Let $t = \sum_{l < k} p_{\pi(l)}$, the start time of position $k$. The jobs in positions other than $k$ and $k + 1$ start at the same time in both orders, because the total time of the two jobs is $p_i + p_j$ in both. So their terms of $F$ do not change. In $\pi$ the two jobs add $w_i(t + p_i) + w_j(t + p_i + p_j)$. In $\pi'$ they add $w_j(t + p_j) + w_i(t + p_j + p_i)$. The difference is $w_i p_j - w_j p_i$. $\square$

Since $w_i, w_j > 0$, the difference is negative exactly when $p_j / w_j < p_i / w_i$, zero exactly when the two ratios are equal, and positive otherwise.

**Theorem.** The order $\sigma$ of line L1, in which $p_{\sigma(1)}/w_{\sigma(1)} \le p_{\sigma(2)}/w_{\sigma(2)} \le \cdots$, has the least cost. Every optimal order is in nondecreasing order of ratios.

*Proof.* Let $\pi$ be any order. Call a pair of positions $k < l$ an inversion of $\pi$ if job $\pi(k)$ comes after job $\pi(l)$ in $\sigma$. If $\pi \ne \sigma$, then $\pi$ has an inversion, and then it has an inversion at two adjacent positions $k, k + 1$: otherwise the jobs of $\pi$ would be in the order of $\sigma$ along the whole sequence. Let $i = \pi(k)$ and $j = \pi(k+1)$ be such a pair. Job $j$ comes before job $i$ in $\sigma$, so $p_j / w_j \le p_i / w_i$, and by the lemma the swap does not raise the cost. The swap removes exactly one inversion and creates none, since only the relative order of $i$ and $j$ changes. After at most $\binom{n}{2}$ swaps we reach $\sigma$, and the cost never rose. So $F(\sigma) \le F(\pi)$ for every $\pi$.

For the second claim, let $\pi$ be an order that is not in nondecreasing order of ratios. Then some adjacent pair $i, j$ of $\pi$, $i$ first, has $p_j / w_j < p_i / w_i$: if each adjacent pair were in order, the whole sequence of ratios would be nondecreasing. The swap of this pair lowers the cost by $w_j p_i - w_i p_j > 0$, so $\pi$ is not optimal. $\blacksquare$

**Ties.** Two orders that are both in nondecreasing ratio order differ only inside groups of equal ratio. Inside such a group, every adjacent swap changes the cost by $0$ by the lemma, and any order of the group is reached by such swaps. So all orders in ratio order have the same cost, and the stable sort of line L1 is one of them.

**Zero weights.** If some $w_j = 0$, put these jobs last. A job with weight $0$ adds nothing to the cost, and moving it to the end does not make any other job complete later. Among the other jobs the theorem applies.
