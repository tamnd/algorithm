---
title: LRU keeps the k most recently requested distinct pages
proves: [correctness]
status: full
---

We use the pseudocode of the page, with a cache $C$ of capacity $k \ge 1$ that starts empty, and a request sequence $\sigma_1 \ldots \sigma_n$. For $t \ge 0$, let $R_t$ be the list of the distinct pages of $\sigma_1 \ldots \sigma_t$, ordered by the time of their last request, the oldest first. Let $d_t = |R_t|$, and let $\mathrm{top}_k(R_t)$ be the last $\min(k, d_t)$ entries of $R_t$, the most recently requested ones.

**Claim.** After request $t$, the list $C$ equals $\mathrm{top}_k(R_t)$, in the same order. In particular, a miss with a full cache evicts the cached page whose last request is the oldest, and request $\sigma_t$ is a hit if and only if $\sigma_t \in \mathrm{top}_k(R_{t-1})$.

*Proof.* By induction on $t$. For $t = 0$, both $C$ and $R_0$ are empty.

Assume the claim for $t - 1$, and let $p = \sigma_t$. The list $R_t$ is $R_{t-1}$ with $p$ removed (if it was there) and then put at the end, because the request at time $t$ is the latest request of all.

- *Case 1: $p \in C$.* By the hypothesis, $p$ is one of the last $\min(k, d_{t-1})$ entries of $R_{t-1}$. Line L2 moves $p$ to the end of $C$. Removing $p$ from the tail part of $R_{t-1}$ and appending it changes only the position of $p$ inside that tail part, and $d_t = d_{t-1}$. So the last $\min(k, d_t)$ entries of $R_t$ are the same pages as before, with $p$ last and the others in their old order. This is the new $C$. The request is a hit, and $p \in \mathrm{top}_k(R_{t-1})$.
- *Case 2: $p \notin C$ and $|C| < k$.* By the hypothesis, $|C| = \min(k, d_{t-1}) < k$, so $C = R_{t-1}$ holds all distinct pages so far. Then $p$ is new, $d_t = d_{t-1} + 1 \le k$, and $R_t$ is $R_{t-1}$ with $p$ appended. Line L6 appends $p$ to $C$, so $C = R_t = \mathrm{top}_k(R_t)$. The request is a miss, and $p \notin \mathrm{top}_k(R_{t-1})$.
- *Case 3: $p \notin C$ and $|C| = k$.* Then $C$ is the last $k$ entries of $R_{t-1}$, and $p$ is not among them. In $R_t$, $p$ moves to the end (or is appended), so the last $k$ entries of $R_t$ are $p$ and the last $k - 1$ entries of $R_{t-1}$. These are $C$ without its first entry, plus $p$. Line L5 removes the first entry of $C$, the cached page with the oldest last request, and line L6 appends $p$. So $C = \mathrm{top}_k(R_t)$. The request is a miss, and $p \notin \mathrm{top}_k(R_{t-1})$.

In each case the claim holds for $t$. $\square$

**The size bound.** By the claim, $|C| = \min(k, d_t) \le k$ at each step.

**Hits and reuse distance.** Let $r$ be the number of distinct pages other than $p = \sigma_t$ that were requested strictly between the previous request of $p$ and time $t$ (and $r = \infty$ if $p$ is new). In $R_{t-1}$, exactly these $r$ pages follow $p$. So $p$ is among the last $k$ entries of $R_{t-1}$ if and only if $r \le k - 1$. By the claim, $\sigma_t$ is a hit if and only if $r < k$.

**The loop.** Let $\sigma$ be the cycle $0, 1, \ldots, k$ repeated. For $t > k + 1$, the $k$ requests before time $t$ are the $k$ pages of the cycle other than $\sigma_t$, so $r = k$, and the request is a miss. The first $k + 1$ requests are misses because each page is new. So every request is a miss.

**Inclusion.** For each $t$, $\mathrm{top}_k(R_t)$ is a subset of $\mathrm{top}_{k+1}(R_t)$, so the LRU cache of size $k$ is a subset of the LRU cache of size $k + 1$ at every step. By the hit rule above, each hit of the size $k$ cache is a hit of the size $k + 1$ cache.

**Cost.** With a hash map from page to list node, line L1 is one expected $O(1)$ lookup, and lines L2, L5 and L6 are each a constant number of pointer changes in a doubly linked list. So each request takes $O(1)$ expected time, and the space is $\Theta(k)$.
