---
title: Weighted random choice by prefix sums returns backend i with probability w_i / W
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The weights $w_0, \ldots, w_{n-1}$ are integers $\ge 0$ with $W = \sum_i w_i > 0$, and $n \ge 1$. Lines L1 and L2 build $P[0] = 0$ and $P[i+1] = P[i] + w_i$, so $P[i] = \sum_{k < i} w_k$, $P$ is non-decreasing, and $P[n] = W$.

**Lemma 1 (the intervals).** For each integer $r$ with $0 \le r < W$ there is exactly one index $i$ with $P[i] \le r < P[i+1]$, and it is the smallest $i$ with $P[i+1] > r$. The set of such $r$ for a fixed $i$ is $\{P[i], \ldots, P[i+1] - 1\}$, which has $w_i$ elements.

*Proof.* Let $i^*$ be the smallest index with $P[i^*+1] > r$. It exists since $P[n] = W > r$. If $i^* = 0$ then $P[0] = 0 \le r$. If $i^* > 0$, then $P[i^*] \le r$ by the choice of $i^*$ as smallest. So $P[i^*] \le r < P[i^*+1]$. For any $i < i^*$, $P[i+1] \le r$; for any $i > i^*$, $P[i] \ge P[i^*+1] > r$ since $P$ is non-decreasing. So no other index satisfies both inequalities. The last sentence follows because the integers in $[P[i], P[i+1])$ number $P[i+1] - P[i] = w_i$. $\square$

**Lemma 2 (the binary search).** For $0 \le r < W$, lines L4 to L8 return the smallest $i$ with $P[i+1] > r$, after at most $\lceil \lg n \rceil$ passes of the loop.

*Proof.* Let $i^*$ be that index. We show the invariant $lo \le i^* \le hi$ at each test of line L5. *Initialization:* $lo = 0$ and $hi = n - 1$, and $0 \le i^* \le n - 1$ because $P[n] > r$. *Maintenance:* line L6 gives $lo \le mid < hi$. If $P[mid+1] > r$, then $i^* \le mid$ by the minimality of $i^*$, and line L7 sets $hi = mid$. Otherwise $P[mid + 1] \le r$, so every $i \le mid$ has $P[i+1] \le P[mid+1] \le r$, hence $i^* > mid$, and line L7 sets $lo = mid + 1$. *Termination:* the length $hi - lo + 1$ falls from $L$ to at most $\lceil L/2 \rceil$ in each pass and stays $\ge 1$ by the invariant, so after at most $\lceil \lg n \rceil$ passes $lo = hi$, and the invariant gives $lo = i^*$. $\square$

**Theorem.** WR-PICK returns backend $i$ with probability exactly $w_i / W$. In particular a backend of weight 0 is never returned.

*Proof.* Line L3 draws $r$ uniformly from the $W$ integers in $[0, W)$. By Lemma 2 the call returns the index $i$ with $P[i] \le r < P[i+1]$, and by Lemma 1 exactly $w_i$ of the $W$ values of $r$ give $i$. So the probability is $w_i / W$. $\blacksquare$

**Many picks.** Successive picks use independent draws of $r$, so they are independent. After $m$ picks the count $K_i$ of backend $i$ is binomial with parameters $m$ and $p_i = w_i / W$: $\mathbb{E}[K_i] = m p_i$ and $\mathrm{Var}[K_i] = m p_i (1 - p_i)$. The count deviates from its mean by about $\sqrt{m p_i (1 - p_i)}$, which grows with $m$, while its share $K_i / m$ tends to $p_i$.
