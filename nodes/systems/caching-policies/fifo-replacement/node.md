---
tag: DTB1HB
kind: algorithm
slug: fifo-replacement
name: First in, first out (FIFO) replacement
aliases:
- FIFO cache replacement
- First-in first-out (FIFO) replacement
- FIFO page replacement
area: systems/caching-policies
level: intro
summary: On a miss with a full cache, evict the page loaded earliest, whatever its use. k-competitive, but it shows Belady's anomaly.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size in pages}
  time: {expected: O(n)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [paging-problem, queue]
see_also: [lru, clock, belady-anomaly, belady-optimal, lru-competitiveness, s3-fifo, sieve, random-replacement]
sources:
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the paging part of the paper, FIFO with k pages against MIN with h pages
  - paper: "L. A. Belady, R. A. Nelson and G. S. Shedler, An anomaly in space-time characteristics of certain programs running in a paging machine, Communications of the ACM 12(6) (1969), 349-353"
    title: An anomaly in space-time characteristics of certain programs running in a paging machine
    locator: the anomaly of FIFO, with more faults for a larger memory
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 10, Section 10.4.2 (FIFO page replacement and Belady's anomaly)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 3, Section 3.4.3 (the first-in, first-out page replacement algorithm)
  - paper: "Neal E. Young, The k-server dual and loose competitiveness for paging, Algorithmica 11(6) (1994), 525-541"
    title: The k-server dual and loose competitiveness for paging
    locator: conservative paging algorithms, with FIFO as an example, and their bound k
---

First in, first out (FIFO) replacement is the [cache replacement policy](/cache-replacement-policy/) that, on a miss with a full cache, evicts the page that was loaded earliest, whether or not it was used since. It needs only a [queue](/queue/) of the cached pages in load order, and a hit changes nothing. It is $k$-competitive for the [paging problem](/paging-problem/), like [LRU](/lru/), but it is not a stack algorithm: on some traces a larger cache has more misses, which is [Belady's anomaly](/belady-anomaly/).

## In plain words

A parking lot has room for a fixed number of cars. Cars come in and wait in a line in the order they arrived. When a new car comes and the lot is full, the car that has been there the longest must leave, even if its owner just came back to use it. Using a car does not move it in the line.

FIFO is cheap because it never has to note which page was used. It only notes which page came in first. The price is that a page in heavy use is thrown out on schedule, and it must then be loaded again at once.

## The problem

The model is the [paging problem](/paging-problem/): a cache of $k$ pages of equal size, a request sequence $\sigma$ of length $n$, an empty cache at the start, and the number of misses as the cost. FIFO is online and deterministic.

## The algorithm

```pseudo id=main
FIFO-ACCESS(p)                   ▷ queue Q of cached pages in load order, capacity k
L1  if p ∈ Q then
L2      return hit                          ▷ nothing changes
L3  if |Q| = k then
L4      remove the head of Q                ▷ the page loaded earliest
L5  add p at the tail of Q
L6  return miss
```

A hash set next to the queue answers the test of line L1 in $O(1)$ expected time. In hardware or in a kernel, a circular array of $k$ frames with one pointer to the oldest frame is enough: the pointer moves one step at each miss.

## Example

Run FIFO with $k = 3$ on $\sigma = 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1$. The queue is listed from the oldest to the newest load.

| $t$ | request | result | evicted | queue after |
| --- | --- | --- | --- | --- |
| 1 to 3 | 7, 0, 1 | 3 misses | | 7 0 1 |
| 4 | 2 | miss | 7 | 0 1 2 |
| 5 | 0 | hit | | 0 1 2 |
| 6 | 3 | miss | 0 | 1 2 3 |
| 7 | 0 | miss | 1 | 2 3 0 |
| 8 | 4 | miss | 2 | 3 0 4 |
| 9 | 2 | miss | 3 | 0 4 2 |
| 10 | 3 | miss | 0 | 4 2 3 |
| 11 | 0 | miss | 4 | 2 3 0 |
| 12, 13 | 3, 2 | 2 hits | | 2 3 0 |
| 14 | 1 | miss | 2 | 3 0 1 |
| 15 | 2 | miss | 3 | 0 1 2 |
| 16, 17 | 0, 1 | 2 hits | | 0 1 2 |
| 18 | 7 | miss | 0 | 1 2 7 |
| 19 | 0 | miss | 1 | 2 7 0 |
| 20 | 1 | miss | 2 | 7 0 1 |

FIFO has 15 misses. [LRU](/lru/) has 12 on the same string and the offline optimum [MIN](/belady-optimal/) has 9. The costly step is $t = 6$: page 0 was just used at $t = 5$, but it is the oldest load, so FIFO evicts it and misses on it at $t = 7$.

**Belady's anomaly.** On $\sigma = 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5$, FIFO has 9 misses with $k = 3$ and 10 misses with $k = 4$. With $k = 4$, the hits at the second requests of 1 and 2 leave the queue order unchanged, so the request of 5 evicts 1, and then 1, 2, 3, 4 and 5 each evict the page needed next. The [Belady anomaly](/belady-anomaly/) page explains why this can happen and how large the gap can be.

## Correctness

The invariant is: after each request, $Q$ holds the cached pages in the order of their loads, the oldest first, and $|Q| \le k$. A hit does not change the cache, so the order is kept. A miss with $|Q| < k$ appends the new page as the newest load. A miss with $|Q| = k$ removes the head, the page with the earliest load, and appends the new page. So FIFO evicts exactly the page that was loaded earliest, and the requested page is cached after each request. The full proof is below, together with the bound against MIN.

## Complexity

- **Time.** $O(1)$ expected time per request with a hash set and a queue, so $O(n)$ expected in total. A hit does no write at all, which is the main practical gain over LRU.
- **Space.** $\Theta(k)$.
- **Misses against the optimum.** FIFO is $k$-competitive: for each $\sigma$, with both caches empty at the start, $\mathrm{FIFO}_k(\sigma) \le k \cdot \mathrm{MIN}_k(\sigma)$. Sleator and Tarjan proved the general bound $\frac{k}{k - h + 1}$ against MIN with $h \le k$ pages for FIFO as for LRU, and $k$ is the best ratio of any deterministic online policy. See [LRU competitiveness](/lru-competitiveness/). The proof below gives the simple case $h = k$.
- **The loop.** On a loop over $k + 1$ pages, FIFO misses on every request, as LRU does.

## Properties

- **Conservative, not marking.** In each part of $\sigma$ with at most $k$ distinct pages, FIFO has at most $k$ misses; Young calls such policies conservative. FIFO is not a [marking algorithm](/marking-algorithm/): it can evict a page that was requested in the current phase, as at $t = 6$ above.
- **Not a stack algorithm.** The FIFO cache of size $k$ is not always a subset of the FIFO cache of size $k + 1$, and the number of misses can rise with $k$. This is the anomaly above. LRU, MRU and MIN are stack algorithms and have no anomaly; see the [inclusion property](/inclusion-property/).
- **Blind to use.** The eviction order depends only on the misses. So FIFO evicts hot pages as often as cold ones.

## Variants and improvements

- **Second chance and CLOCK.** [CLOCK](/clock/) adds a reference bit to each page and skips a page whose bit is set, so a page in use gets another round. With no bit set it is FIFO.
- **FIFO with lazy promotion.** [S3-FIFO](/s3-fifo/) and [SIEVE](/sieve/) keep FIFO queues and move or keep a page only at eviction time, not at each hit. They aim at the hit ratio of LRU at the cost of FIFO.
- **FIFO in hardware.** Some set-associative caches use FIFO or round-robin within a set, because one pointer per set is enough. See [set-associative cache](/set-associative-cache/).
- **2Q.** [2Q](/two-q/) uses a FIFO queue for pages seen once, and an LRU queue for pages seen again.

## When to use it

Use FIFO when the cost of a hit must be minimal and no reference bit is available, or as the base of a policy such as CLOCK, S3-FIFO or SIEVE. It is also a fair baseline in experiments. Do not use plain FIFO when the workload has a hot set that is used all the time, because FIFO evicts those pages on schedule.

## Pitfalls

- **Moving a page on a hit.** That turns FIFO into LRU. In FIFO a hit changes nothing.
- **Assuming a larger cache helps.** For FIFO it can hurt, by Belady's anomaly. Do not extrapolate miss ratios of FIFO from one size to another with a stack method; simulate each size.
- **FIFO and the first $k$ misses.** The first request to each page is a miss for every policy. Compare policies from the same start state.
- **Reloads of hot pages.** A page used at each request is still evicted every $k$ misses. In a trace with a hot page and a stream of new pages, FIFO misses on the hot page again and again, while LRU keeps it.

## Implementations

## History

FIFO was one of the first replacement rules of virtual memory systems, because it needs no hardware support beyond a load order. Belady compared it with other rules and with the optimum MIN in 1966. Belady, Nelson and Shedler reported in 1969 that FIFO can have more page faults with more memory. Mattson, Gecsei, Slutz and Traiger (1970) explained this by the stack property, which FIFO does not have. Sleator and Tarjan proved in 1985 that FIFO is as good as LRU in the competitive sense.

## References
