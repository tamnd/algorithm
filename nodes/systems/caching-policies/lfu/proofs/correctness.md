---
title: The frequency list evicts the least recently used page of smallest count, and LFU is not competitive
proves: [correctness]
status: full
---

We use the pseudocode of the page, a cache of capacity $k \ge 1$ that starts empty, and a request sequence $\sigma_1 \ldots \sigma_n$. For a cached page $p$, let $c(p)$ be the number of requests to $p$ since it was last loaded, and $\ell(p)$ the time of its latest request. LFU with LRU ties must evict the cached page that minimizes the pair $(c(p), \ell(p))$ in lexicographic order.

**Invariant.** After each request:

1. the frequency nodes after the sentinel have distinct counts in increasing order, and none is empty;
2. each cached page is in exactly one node, the node with count $c(p)$, and the map $N$ points to it;
3. the list of each node is in increasing order of $\ell$;
4. at most $k$ pages are cached, and the requested page is cached.

*Proof.* By induction on the requests. The empty structure satisfies the invariant.

*Hit on $p$.* Let $x = N[p]$ with count $f = c(p)$. Line L2 finds the node $y$ for count $f + 1$: by part 1, if it exists, it is the node right after $x$, since no count lies between $f$ and $f + 1$; otherwise a new node is linked right after $x$, before every node with a count above $f + 1$. So part 1 holds for the new node. Line L3 moves $p$ to the tail of $y$. Now $c(p) = f + 1$ and $\ell(p)$ is the current time, larger than every other $\ell$, so parts 2 and 3 hold for $y$. Removing $p$ from $x$ keeps the order in $x$, and $x$ is dropped if empty, so part 1 holds. Part 4 holds since the cache does not change.

*Miss on $p$ with a full cache.* By part 1, the first node $x$ has the smallest count $f_0$ among the cached pages. By parts 2 and 3, its head $q$ has $c(q) = f_0$ and the smallest $\ell$ among the pages with count $f_0$. So $q$ minimizes $(c, \ell)$, which is the LFU victim with LRU ties. Line L8 removes it and drops $x$ if empty. In both cases parts 1 to 3 hold for the rest.

*Load of $p$.* Line L9 puts $p$ in the node for count 1. All counts are at least 1, so this node is the first node, or a new node linked right after the sentinel, which keeps part 1. Now $c(p) = 1$ and $\ell(p)$ is the latest time, so $p$ at the tail keeps parts 2 and 3. The size is at most $k$, because a page was removed when the cache was full. $\square$

So the structure evicts exactly the page that LFU with LRU ties names. The tests compare it with a direct implementation that keeps $c$ and $\ell$ in a dictionary and takes the minimum of $(c, \ell)$ at each miss.

**Not competitive.** Let $k \ge 2$, let $m \ge 2$ and $r \ge 1$. Let $\sigma$ request the pages $1, \ldots, k - 1$ each $m$ times, in any order, and then $a, b, a, b, \ldots$ with $2 r$ requests, where $a$ and $b$ are new pages.

After the first part, the pages $1, \ldots, k - 1$ are cached with counts $m \ge 2$. The request of $a$ fills the last slot, with count 1. The request of $b$ is a miss with a full cache. By the invariant, the victim minimizes $(c, \ell)$. Every old page has a count of at least 2, so the victim is $a$, the only page with count 1. Then $a$ misses and evicts $b$ in the same way, and so on. So LFU misses on all $2 r$ requests of the second part.

An offline policy, after the first part, evicts one of the old pages at the request of $b$ and then holds $a$ and $b$. It misses at most $k + 1$ times in total. So $\mathrm{LFU}_k(\sigma) \ge 2 r$ while $\mathrm{MIN}_k(\sigma) \le k + 1$. As $r$ grows, no constant $c$ and no additive term $d$ give $\mathrm{LFU}_k(\sigma) \le c \cdot \mathrm{MIN}_k(\sigma) + d$ for all $\sigma$. $\square$

**Cost.** Each line does a constant number of hash operations and link changes, so each request takes $O(1)$ expected time. There are at most $k$ cached pages and at most $k$ nonempty frequency nodes, so the space is $\Theta(k)$.
