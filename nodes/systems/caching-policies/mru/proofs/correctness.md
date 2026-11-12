---
title: MRU serves each request, and it is optimal on a cyclic trace
proves: [correctness]
status: full
---

We use the pseudocode of the page, a cache of capacity $k \ge 1$ that starts empty, and a request sequence $\sigma_0 \ldots \sigma_{n-1}$. For a cached page $q$ at time $t$, let $\ell_q < t$ be the time of its last request.

**Claim 1 (validity).** After each request, the requested page is cached, $|C| \le k$, and $C$ lists the cached pages in increasing order of $\ell_q$.

*Proof.* By induction on the requests. The empty start satisfies the claim. If $p \in C$, line L2 moves $p$ to the end and $\ell_p$ becomes the current time, the largest of all, so the order is kept and the size does not change. If $p \notin C$ and $|C| < k$, line L6 appends $p$ with the largest $\ell_p$ and the size is at most $k$. If $p \notin C$ and $|C| = k$, line L5 removes the last page of $C$ and line L6 appends $p$, so the size stays $k$ and the order is kept. In each case $p$ is cached. $\square$

So line L5 evicts the cached page with the largest $\ell_q$, the most recently used one.

**Claim 2 (optimality on loops).** Let $L > k$ and $\sigma_t = t \bmod L$ for $0 \le t < n$. Then MRU has the minimum number of misses over all policies with $k$ pages.

*Proof.* Let MIN be the offline rule that, on a miss with a full cache, evicts a cached page whose next request is the furthest in the future, with a page that is never requested again counted as furthest. By Belady's theorem, MIN has the minimum number of misses. We show that MRU and MIN keep the same cache at each step when MIN breaks ties as MRU does; since the cached sets are equal, they have the same misses.

Belady's theorem holds for each way of breaking ties, so we let MIN break ties in favor of the page with the largest $\ell_q$. Both rules start empty and load the same pages while the cache is not full, so they agree until the first miss with a full cache. Assume they hold the same cache before a miss at time $t$ with a full cache. Page $q$ is requested exactly at the times $u$ with $u \bmod L = q$. Its last request before $t$ is at $\ell_q$, so its next request is at $\ell_q + L$, or never if $\ell_q + L \ge n$. The cached pages are distinct, so their times $\ell_q$ are distinct. If the page $r$ with the largest $\ell_r$ is requested again, then each other cached page is requested again earlier, at $\ell_q + L < \ell_r + L$, so $r$ is the unique furthest page. If $r$ is never requested again, it is among the furthest pages, and the tie rule picks it. So MIN evicts $r$, the most recently used page, as MRU does, and the two caches stay equal after time $t$. By induction they hold the same cache at each step, so they have the same misses, which are the minimum. $\square$

**The count for $L = k + 1$.** The requests at times $0, \ldots, k - 1$ ask for $k$ new pages, so they are $k$ misses, and they fill the cache. From then on, the cache holds $k$ of the $k + 1$ pages. At a miss at time $t \ge k$, MRU evicts $\sigma_{t-1}$, whose next request is at $t - 1 + L = t + k$. After the miss, the cache holds every page of the loop except $\sigma_{t-1}$. The requests at times $t + 1, \ldots, t + k - 1$ ask for pages other than $\sigma_{t-1}$, so they are hits, and hits evict nothing. So after a miss at time $t \ge k$, the next miss is at time $t + k$. The request at time $k$ asks for page $k$, which is not cached, so it is a miss. The misses with a full cache are thus at times $k, 2k, 3k, \ldots$ below $n$, and there are $\lfloor (n - 1)/k \rfloor$ of them. The total is $k + \lfloor (n - 1)/k \rfloor = (k + 1) + \lfloor (n - k - 1)/k \rfloor$ for $n \ge k + 1$.

**Not competitive.** Let $\sigma = 1, 2, \ldots, k$, then $k + 1, k$ repeated $m$ times. By claim 1, at the first request of $k + 1$ MRU evicts $k$, the page requested last. Then each request asks for the page that was evicted at the previous request, and MRU evicts the page just requested, which is the next one asked for. So MRU misses on all $k + 2m$ requests. MIN misses on the first $k$ requests and once more at the first request of $k + 1$, where it evicts page 1, and then it hits on each request. So MIN has $k + 1$ misses for each $m$, and the ratio grows without bound.

**Cost.** With a hash map from page to list node and a doubly linked list in recency order, each line takes $O(1)$ expected time. The space is $\Theta(k)$.
