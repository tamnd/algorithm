---
title: FIFO evicts the earliest load, and it misses at most k times as often as MIN
proves: [correctness]
status: full
---

We use the pseudocode of the page, a cache of capacity $k \ge 1$ that starts empty, and a request sequence $\sigma_1 \ldots \sigma_n$.

**Claim 1 (validity).** After each request, the requested page is cached, $Q$ holds the cached pages in increasing order of the time they were loaded, and $|Q| \le k$.

*Proof.* By induction on the requests. The empty queue satisfies the claim. On a hit, lines L1 and L2 change nothing, and the requested page is cached. On a miss with $|Q| < k$, line L5 appends $p$, whose load time is the latest, so the order holds and $|Q| \le k$. On a miss with $|Q| = k$, line L4 removes the head, which by the hypothesis is the page loaded earliest, and line L5 appends $p$; the size stays $k$ and the order holds. $\square$

**Claim 2 (conservative).** Let $\tau$ be a contiguous part of $\sigma$ that requests at most $k$ distinct pages. Then FIFO has at most $k$ misses on the requests of $\tau$.

*Proof.* We show that no page misses twice inside $\tau$. Assume that page $p$ misses at times $t_1 < t_2$, both inside $\tau$. Then $p$ was loaded at $t_1$ and evicted at some time $e$ with $t_1 < e < t_2$, by a miss on a page $q$. By claim 1, an eviction happens only when $|Q| = k$, and it removes the head. So just before the eviction at $e$, $Q$ holds $p$ at the head and $k - 1$ other pages behind it. By claim 1 these $k - 1$ pages were loaded after $p$, that is, at misses at times in $(t_1, e)$, so they were requested inside $[t_1, e]$. They are distinct from each other and from $p$, because they are in the cache together. The page $q$ was requested at time $e$; it is not cached just before $e$, so it differs from these $k - 1$ pages and from $p$.

All of these requests lie in $[t_1, t_2]$, which is inside $\tau$, so $\tau$ requests at least the $k + 1$ distinct pages $p$, the $k - 1$ pages behind it, and $q$. This contradicts the hypothesis. So each of the at most $k$ distinct pages of $\tau$ misses at most once in $\tau$. $\square$

**Claim 3 (the bound).** $\mathrm{FIFO}_k(\sigma) \le k \cdot \mathrm{MIN}_k(\sigma)$, with both caches empty at the start.

*Proof.* Cut $\sigma$ into phases from left to right: each phase is the longest part, starting where the last one ended, that requests at most $k$ distinct pages. Let $m$ be the number of phases. By claim 2, FIFO has at most $k$ misses in each phase, so $\mathrm{FIFO}_k(\sigma) \le k m$.

Now count the misses of any policy with $k$ pages, in particular of MIN. The first request of $\sigma$ is a miss, because the cache is empty. For $i = 1, \ldots, m - 1$, let $B_i$ be the part of $\sigma$ from the second request of phase $i$ to the first request of phase $i + 1$, both included. Phase $i$ together with the first request of phase $i + 1$ requests $k + 1$ distinct pages, so $B_i$ requests at least $k$ distinct pages other than $f_i$, the first page of phase $i$. Right after the first request of phase $i$, the policy holds $f_i$. If it has no miss in $B_i$, its cache does not change during $B_i$, so all $k$ distinct pages of $B_i$ other than $f_i$ plus $f_i$ itself, that is $k + 1$ pages, are in the cache of $k$ pages, which is impossible. So each $B_i$ holds a miss. The parts $B_1, \ldots, B_{m-1}$ do not overlap, and none of them holds the first request of $\sigma$. So MIN has at least $m$ misses, and $\mathrm{FIFO}_k(\sigma) \le k m \le k \cdot \mathrm{MIN}_k(\sigma)$. $\square$

**Cost.** With a hash set for the test of line L1 and a queue for lines L4 and L5, each request takes $O(1)$ expected time, and the space is $\Theta(k)$.
