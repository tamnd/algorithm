---
tag: YZK836
kind: algorithm
slug: lru-k
name: LRU-K
aliases:
- LRU-2
- LRU-K page replacement
area: systems/caching-policies
level: advanced
summary: Evict the page whose K-th most recent reference is oldest, counting a page with fewer than K references as infinitely old. Resists scans in database buffers.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the buffer size in pages}
  time: {worst: O(n k + n log n)}
  space: {extra: O(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1993
  people: [Elizabeth J. O'Neil, Patrick E. O'Neil, Gerhard Weikum]
  note: O'Neil, O'Neil and Weikum proposed LRU-K for database buffers at SIGMOD 1993, with the correlated reference period and the retained information period.
prereqs: [lru]
see_also: [lru, two-q, lirs, arc, lfu, lrfu, reuse-distance, independent-reference-model]
sources:
  - paper: doi:10.1145/170035.170081
    title: "Elizabeth J. O'Neil, Patrick E. O'Neil and Gerhard Weikum, The LRU-K page replacement algorithm for database disk buffering, Proceedings of ACM SIGMOD 1993, 297-306"
    locator: the definition of the backward K-distance, the correlated reference period, the retained information period, and the pseudocode of the algorithm
  - paper: doi:10.1145/300515.300518
    title: "Elizabeth J. O'Neil, Patrick E. O'Neil and Gerhard Weikum, An optimality proof of the LRU-K page replacement algorithm, Journal of the ACM 46(1) (1999), 92-112"
    locator: the optimality of LRU-K among policies that know the last K reference times, under the independent reference model
  - paper: "Theodore Johnson and Dennis Shasha, 2Q, a low overhead high performance buffer management replacement algorithm, Proceedings of VLDB 1994, 439-450"
    title: 2Q, a low overhead high performance buffer management replacement algorithm
    locator: the comparison with LRU-2 and its cost of a priority queue per access
---

LRU-K is the [cache replacement policy](/cache-replacement-policy/) for database buffers by O'Neil, O'Neil and Weikum (1993). It ranks a page by the time of its $K$-th most recent reference, not its most recent one. The *backward K-distance* $b_t(p, K)$ is the time since that reference, and it is infinite if $p$ has fewer than $K$ references. On a miss, LRU-K evicts the page with the largest backward $K$-distance. A page that was referenced only once, such as a page of a long scan, has an infinite distance, so it goes before a page with two recent references. With $K = 1$ it is [LRU](/lru/). LRU-2 is the usual choice.

## In plain words

LRU asks one question about each page: when was it last used? A page read once by a big scan looks just as fresh as a page that is used all the time, so a scan can push the useful pages out.

LRU-K asks: when was the page used $K$ times back? For $K = 2$, it looks at the second-to-last use. A page used once has no second-to-last use, so it counts as very old and leaves first. A page used twice within a short time ranks as fresh. Two more rules handle the details: uses that come in a quick burst count as one use, and the policy remembers the history of a page for a while after it leaves the cache.

## The problem

The model is the [paging problem](/paging-problem/) for a database buffer: a buffer of $k$ pages, a request sequence $\sigma$ of length $n$, an empty buffer at the start, and the number of misses as the cost. LRU-K is online and deterministic. It was designed for workloads that mix random access to a hot set, such as index pages, with sequential scans and with random access to a large cold set, such as data pages.

Two parameters shape the history:

- **Correlated reference period.** References to a page within a period of its last reference are correlated, for example several reads of the same page inside one transaction. A correlated reference does not count as a new reference, and a page referenced within this period cannot be evicted. Default 0: no references are correlated.
- **Retained information period.** The history of an evicted page is kept for this time after its last reference, so that a page that comes back soon gets its old history. Default: forever.

## The algorithm

For each page $p$, HIST$(p)$ holds the times of its last $K$ uncorrelated references, newest first, with 0 for none, and LAST$(p)$ holds the time of its latest reference. Time $t$ counts the requests from 1.

```pseudo id=main
LRU-K-ACCESS(p, t)               ▷ buffer B of k pages, CRP, RIP
L1  if p ∈ B then
L2      if t − LAST(p) > CRP then               ▷ a new, uncorrelated reference
L3          period ← LAST(p) − HIST(p, 1)       ▷ length of the last correlated period
L4          for i ← K downto 2 do HIST(p, i) ← HIST(p, i − 1) + period
L5          HIST(p, 1) ← t
L6      LAST(p) ← t
L7      return hit
L8  if |B| = k then
L9      E ← the pages q ∈ B with t − LAST(q) > CRP      ▷ eligible
L10     v ← the q ∈ E with the smallest HIST(q, K), the smallest LAST(q) on a tie
L11     evict v; keep HIST(v) and LAST(v) until t − LAST(v) > RIP
L12 if HIST(p) is retained then
L13     for i ← K downto 2 do HIST(p, i) ← HIST(p, i − 1)
L14 else HIST(p) ← (0, …, 0)
L15 HIST(p, 1) ← t; LAST(p) ← t
L16 add p to B
L17 return miss
```

The smallest HIST$(q, K)$ is the largest backward distance $t - \mathrm{HIST}(q, K)$, and the value 0 stands for an infinite distance. Line L4 moves the old reference times forward by the length of the correlated period that just ended, so that a burst counts as one reference at its start; the code leaves 0 entries at 0. Line L10 breaks ties, in particular among the pages of infinite distance, by LRU on LAST, which is the subsidiary policy the paper suggests. If no page is eligible at line L9, the code takes all pages of the buffer; the paper does not cover this case. The history of evicted pages is dropped lazily, at the next request after its period ends.

## Example

Run LRU-2 with $k = 3$, $\mathrm{CRP} = 0$, on $a, b, a, b, x_1, x_2, x_3, x_4, x_5, a, b$.

| $t$ | request | result | evicted | HIST after (first, second) |
| --- | --- | --- | --- | --- |
| 1, 2 | a, b | 2 misses | | a (1, 0), b (2, 0) |
| 3, 4 | a, b | 2 hits | | a (3, 1), b (4, 2) |
| 5 | $x_1$ | miss | | $x_1$ (5, 0) |
| 6 | $x_2$ | miss | $x_1$ | $x_2$ (6, 0) |
| 7 to 9 | $x_3, x_4, x_5$ | 3 misses | $x_2, x_3, x_4$ | $x_5$ (9, 0) |
| 10, 11 | a, b | 2 hits | | a (10, 3), b (11, 4) |

At $t = 6$, the distance of $a$ is $6 - 1 = 5$, of $b$ is $4$, and of $x_1$ is infinite, so $x_1$ goes. Each scan page evicts the one before it. LRU-2 has 7 misses. LRU evicts $a$ at $t = 6$ and $b$ at $t = 7$ and misses on both at the end: 9 misses.

## Correctness

With $\mathrm{CRP} = 0$, every reference is uncorrelated and the period at line L3 is 0, so HIST$(p)$ holds exactly the last $K$ reference times of $p$ that are still retained. Then line L10 evicts the page of largest backward $K$-distance, the least recently used one among the pages of infinite distance. With $K = 1$, HIST$(p, 1) = \mathrm{LAST}(p)$ and line L10 is the LRU rule. The tests check both facts against an implementation that keeps every reference time, and the effect of the two periods on small cases. The proof is below.

## Complexity

- **Time.** A hit is $O(K)$. The code finds the victim by a scan of the buffer, $O(k)$ per miss, and drops old histories with a heap at $O(\log n)$ per eviction, so $O(n k + n \log n)$ in total for a constant $K$. The paper suggests a search tree keyed by HIST$(q, K)$ for $O(\log k)$ per miss; pages inside the correlated period must then be skipped.
- **Space.** $K + 1$ times per page with a history. With an infinite retained information period, every page ever requested keeps one, so up to $O(n)$ for a constant $K$. A finite period bounds this by the number of pages requested within it.
- **No competitive bound is claimed.** O'Neil, O'Neil and Weikum later proved, under the [independent reference model](/independent-reference-model/), that LRU-K makes the best choice that the last $K$ reference times allow.

## Properties

- **Scan resistant.** Pages referenced once have an infinite distance and leave before any page with $K$ references, as in the example.
- **Between LRU and LFU.** For larger $K$, the $K$-th reference time is a better estimate of the rate of references, as in LFU, but the policy adapts more slowly to changes. $K = 2$ gives most of the gain.
- **LRU as the case $K = 1$.** With $K = 1$ and no correlated period, HIST$(p, 1)$ is the last reference and the rule is LRU, so all the bounds of LRU hold for it. For $K \ge 2$ the paper gives no worst-case bound against MIN.
- **History beyond the buffer.** With a retained information period, LRU-K remembers pages that are not cached, like the ghost entries of [ARC](/arc/) and [2Q](/two-q/).

## Variants and improvements

- **2Q.** [2Q](/two-q/) by Johnson and Shasha (1994) aims at the behavior of LRU-2 with queues in place of a priority queue, at $O(1)$ per request.
- **LIRS.** [LIRS](/lirs/) uses the reuse distance, the number of distinct pages between the last two references, in place of the time, and keeps it in a stack.
- **ARC.** [ARC](/arc/) splits the cache between pages seen once and pages seen at least twice, as LRU-2 does, and adapts the split.
- **LRFU.** [LRFU](/lrfu/) weights all past references by a decaying function in place of using only the $K$-th one.

## When to use it

Use LRU-2 for database buffer pools and other caches where scans and random access to a large table mix with a hot set, and where a priority queue per access is affordable. Choose the correlated reference period to cover the references inside one transaction or one operation, and the retained information period to cover the typical time between two references of a warm page. Where the cost of a priority queue at each access matters, 2Q or ARC give similar results at $O(1)$ per request.

## Pitfalls

- **Counting bursts.** Without a correlated reference period, two reads of a page inside one transaction give it a short backward $K$-distance, and a scan that touches each page twice in a row looks hot.
- **Forgetting history at eviction.** Without a retained information period, every page that comes back starts with an infinite distance and is evicted first again, so the policy cannot learn that it is hot.
- **Shifting HIST in the wrong order.** The shift at lines L4 and L13 must go from $K$ down to 2. Going up copies the newest time into every slot.
- **Ties among infinite distances.** Many pages can have fewer than $K$ references. A tie rule is needed; without one the result depends on the order of a hash table.

## Implementations

## History

O'Neil, O'Neil and Weikum presented LRU-K at SIGMOD 1993, motivated by database buffers where LRU cannot tell index pages from data pages that are touched once. The paper gave the backward $K$-distance, the correlated reference period and the retained information period, and simulations where LRU-2 needed a smaller buffer than LRU for the same hit ratio. A proof of optimality under the independent reference model followed in the Journal of the ACM in 1999. 2Q (1994), LIRS (2002) and ARC (2003) were later designed to get the benefits of LRU-2 at a lower cost.

## References
