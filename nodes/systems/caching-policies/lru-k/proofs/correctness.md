---
title: LRU-K evicts the page of largest backward K-distance, and LRU-1 is LRU
proves: [correctness]
status: full
---

We use the pseudocode of the page, a buffer of capacity $k \ge 1$ that starts empty, and a request sequence $\sigma_1 \ldots \sigma_n$, with $\sigma_t$ requested at time $t$. For a page $p$ and a time $t$, let $R_t(p)$ be the list of reference times of $p$ up to $t$ whose history is retained, newest first. The backward $K$-distance is $b_t(p, K) = t - r$ where $r$ is the $K$-th entry of $R_t(p)$, and $b_t(p, K) = \infty$ if $R_t(p)$ has fewer than $K$ entries.

**Claim 1 (validity).** After each request, $p$ is in the buffer, $|B| \le k$, and every page in the buffer has a history.

*Proof.* A hit changes only HIST$(p)$ and LAST$(p)$. A miss with a full buffer evicts one page at line L11, which exists because $E$ or, if $E$ is empty, the buffer is not empty. Lines L12 to L16 give $p$ a history and add it. $\square$

**Claim 2 (history with no correlated references).** Let $\mathrm{CRP} = 0$. After request $t$, for each page $p$ with a history, HIST$(p, i)$ is the $i$-th entry of $R_t(p)$ for $i \le K$, and 0 if there is no such entry. LAST$(p)$ is the first entry.

*Proof.* By induction on $t$. With $\mathrm{CRP} = 0$, the test at line L2 holds for every hit, since $t > \mathrm{LAST}(p)$. By the hypothesis, $\mathrm{LAST}(p) = \mathrm{HIST}(p, 1)$ before the request, so the period at line L3 is 0, and lines L4 and L5 shift the list by one place and put $t$ first. Lines L13 and L15 do the same for a page whose history was retained, and line L14 with line L15 gives the list $(t, 0, \ldots, 0)$ for a new page. Pages not requested keep their lists. The history of an evicted page is dropped at the first request after $t - \mathrm{LAST} > \mathrm{RIP}$, exactly when its references stop being retained. The shift goes from $K$ down to 2, so each slot receives the old value of the slot before it. $\square$

**Claim 3 (the victim).** Let $\mathrm{CRP} = 0$. On a miss at time $t$ with a full buffer, line L10 evicts a page of largest $b_t(q, K)$ among the pages in the buffer, and among several such pages the one with the oldest last reference.

*Proof.* With $\mathrm{CRP} = 0$ every cached page $q$ has $\mathrm{LAST}(q) < t$, so $E = B$. By claim 2, HIST$(q, K)$ is the $K$-th reference time, and $t - \mathrm{HIST}(q, K) = b_t(q, K)$ when it is positive. A value 0 means fewer than $K$ references, an infinite distance, and 0 is smaller than every time. So the smallest HIST$(q, K)$ is the largest distance, and the second key LAST$(q)$ breaks the ties by LRU. $\square$

The tests compare the code, for $K = 1, 2, 3$, with or without a retained information period, against an implementation that keeps every reference time and evicts by the definition.

**Claim 4 (LRU-1 is LRU).** With $K = 1$ and $\mathrm{CRP} = 0$, LRU-K evicts the page with the oldest last reference, so its hits and misses are those of LRU.

*Proof.* By claim 2, HIST$(q, 1) = \mathrm{LAST}(q)$ for each cached page, and every value is positive, since a cached page was referenced. By claim 3 the victim minimizes LAST$(q)$, the least recently used page. The two policies start equal and evict the same page at each miss, so they hold the same pages at all times. $\square$

**Correlated references.** For $\mathrm{CRP} > 0$, a hit at time $t$ with $t - \mathrm{LAST}(p) \le \mathrm{CRP}$ changes only LAST$(p)$, so a burst of references with gaps of at most CRP counts as one reference, recorded at its first time in HIST$(p, 1)$. At the next uncorrelated reference, line L4 adds the length LAST$(p) - $ HIST$(p, 1)$ of the burst to the older entries. A page with $t - \mathrm{LAST}(q) \le \mathrm{CRP}$ is not in $E$ and is not evicted while another page is eligible. The tests check these cases on small traces.

**Cost.** A hit takes $O(K)$ for the shift. A miss scans the buffer in $O(k)$ and shifts in $O(K)$. Dropping retained histories uses a heap ordered by LAST: each eviction pushes one entry, and each entry is popped once, at $O(\log n)$. So the total time is $O(n (k + K + \log n))$, which is $O(n k + n \log n)$ for a constant $K$, and the space is $O(K)$ per page with a history.
