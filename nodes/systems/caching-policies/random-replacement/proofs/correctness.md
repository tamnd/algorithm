---
title: Random replacement keeps a valid cache, evicts each page with probability 1/k, and misses at rate 2/(k+1) on a loop of k+1 pages
proves: [correctness]
status: full
---

We use the pseudocode of the page, a cache of capacity $k \ge 1$ that starts empty, and a request sequence $\sigma_1 \ldots \sigma_n$.

**Claim 1 (validity).** After each request, the requested page is cached, $|C| \le k$, the array holds each cached page exactly once with no gaps, and the hash map sends each cached page to its slot.

*Proof.* By induction on the requests. The empty array and the empty map satisfy the claim. On a hit, line L1 returns and nothing changes. On a miss with $|C| < k$, line L5 puts $p$ at the end of the array and records that slot in the map. On a miss with $|C| = k$, line L3 picks a slot $i$ and the page $q$ in it. Line L4 removes the last page $r$ of the array; if $i$ is not the last slot, $r$ moves to slot $i$ and the map records the new slot of $r$. Then $q$ leaves the map. The array now holds the $k - 1$ pages other than $q$, with no gaps, and the map is correct for each of them. Line L5 adds $p$ at the end. So the size is $k$ again and the requested page is cached. $\square$

**Claim 2 (uniform victim).** On a miss with a full cache, each cached page is evicted with probability exactly $1/k$, independently of the past.

*Proof.* Line L3 draws $i$ uniformly from $\{0, \ldots, k - 1\}$ with a fresh random number. By claim 1, the $k$ slots hold the $k$ cached pages, one each. So the map from slots to pages is a bijection, and each page is chosen with probability $1/k$. $\square$

**Claim 3 (the loop).** Let $\sigma$ be the loop $0, 1, \ldots, k, 0, 1, \ldots, k, \ldots$ over $k + 1$ pages. After the first $k + 1$ requests, the gaps between consecutive misses are independent and uniform on $\{1, \ldots, k\}$. So the long-run fraction of misses is $2/(k + 1)$.

*Proof.* The first $k + 1$ requests are to distinct pages, so they are misses, and from then on the cache holds exactly $k$ of the $k + 1$ pages: each miss evicts one page and loads one. Look at a miss at time $t$, after the first $k$ requests. Just after it, the cache holds $k$ pages and one page $x$ is absent, the page evicted at $t$. In the loop, the $k + 1$ pages are requested once each in any $k + 1$ consecutive requests. Before the load at $t$, the cache held the $k$ pages other than $\sigma_t$, and these are exactly the pages requested at $t + 1, \ldots, t + k$, one each. By claim 2, $x$ is each of them with probability $1/k$. All requests between $t$ and the request of $x$ are hits, because the only absent page is $x$. The request of $x$ is a miss. So the gap $D$ to the next miss is uniform on $\{1, \ldots, k\}$, and it depends only on the fresh random number of this miss.

The gaps $D_1, D_2, \ldots$ are independent with mean $\mathbb{E}[D] = (1 + \cdots + k)/k = (k + 1)/2$. By the renewal theorem (here, the strong law of large numbers for the sums $D_1 + \cdots + D_m$), the number of misses in the first $n$ requests, divided by $n$, tends to $1/\mathbb{E}[D] = 2/(k + 1)$ with probability 1. $\square$

For comparison, LRU and FIFO evict the page requested next at each miss of this loop, so they miss at rate 1, and MIN misses about once in $k$ requests. So on this loop RAND is better than LRU by a factor of about $(k + 1)/2$.

**Claim 4 (competitive bound, cited).** For each sequence $\sigma$, $\mathbb{E}[\mathrm{RAND}_k(\sigma)] \le k \cdot \mathrm{OPT}_k(\sigma) + c$ for a constant $c$, even if each request may depend on the past random choices (an adaptive online adversary). This is the theorem of Raghavan and Snir (1989). We do not repeat the proof. It uses a potential function on the pages that are in the cache of the adversary but not in the cache of RAND: each miss of RAND that the adversary does not pay for lowers the expected potential, because the victim is uniform. Since an oblivious adversary fixes $\sigma$ in advance, it is a special case, and the same bound holds against it. The tests check the weaker statement $\mathbb{E}[\mathrm{RAND}_k(\sigma)] \le k \cdot \mathrm{MIN}_k(\sigma)$ exactly, with rational numbers, on many short random sequences.

**Cost.** Line L1 is one hash lookup. Lines L3 to L5 take one random number and a constant number of array and map writes. So each request takes $O(1)$ expected time, and the space is $\Theta(k)$.
