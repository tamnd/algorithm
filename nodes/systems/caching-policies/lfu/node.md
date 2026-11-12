---
tag: 4DET4E
kind: algorithm
slug: lfu
name: Least frequently used (LFU)
aliases:
- LFU
- LFU replacement
- Least frequently used (LFU) replacement
- least frequently used
area: systems/caching-policies
level: intro
summary: On a miss with a full cache, evict the page with the fewest hits since it was loaded, the least recently used one on a tie. O(1) per request with frequency buckets.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size in pages}
  time: {expected: O(n)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [paging-problem, lru, doubly-linked-list]
see_also: [lru, lfu-da, lrfu, tinylfu, w-tinylfu, mq-cache, arc, count-min-sketch]
sources:
  - url: http://dhruvbird.com/lfu.pdf
    title: Ketan Shah, Anirban Mitra and Dhruv Matani, An O(1) algorithm for implementing the LFU cache eviction scheme, 2010
    locator: the list of frequency nodes, each with its list of items, and the O(1) insert, access and evict operations
  - paper: doi:10.1145/321623.321632
    title: "Alfred V. Aho, Peter J. Denning and Jeffrey D. Ullman, Principles of optimal page replacement, Journal of the ACM 18(1) (1971), 80-93"
    locator: the independent reference model, where keeping the pages of highest probability is optimal
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 10, Section 10.4.6 (counting-based page replacement, LFU and MFU)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 3, Section 3.4.7 (simulating LRU in software, the not frequently used algorithm and aging)
---

Least frequently used (LFU) is the [cache replacement policy](/cache-replacement-policy/) that, on a miss with a full cache, evicts the cached page with the smallest use count. Ties are frequent, because each new page starts with count 1, so a rule for ties is part of the policy: this page breaks them by [LRU](/lru/), so among the pages with the smallest count it evicts the one used least recently. With the structure of Shah, Mitra and Matani, a list of frequency buckets, each request takes $O(1)$ expected time. LFU keeps pages that are popular over a long time, but it is not competitive: pages that were hot long ago can stay forever.

## In plain words

Each book on the shelf has a tally of how many times it was read since it came. When a new book needs room, the book with the smallest tally goes. If several books share the smallest tally, the one that was read longest ago goes.

This protects the books that are read again and again, even when they were not read in the last hour. A burst of books read only once does not push them out, as it does with LRU. The weak point is the past: a book read a hundred times last year still has a big tally, so it stays even if nobody needs it now.

## The problem

The model is the [paging problem](/paging-problem/): a cache of $k$ pages of equal size, a request sequence $\sigma$ of length $n$, an empty cache at the start, and the number of misses as the cost. LFU is online and deterministic.

There are two kinds of count. **In-cache LFU** counts the requests to a page since it was loaded, and forgets the count when the page is evicted. **Perfect LFU** keeps a count for every page ever requested, also for pages not in the cache. This page and its code use in-cache LFU, which needs only $\Theta(k)$ space. Perfect LFU needs space for all pages seen; [TinyLFU](/tinylfu/) approximates it with a sketch.

## The algorithm

The structure of Shah, Mitra and Matani (2010) is a [doubly linked list](/doubly-linked-list/) of frequency nodes, one node for each count that some cached page has, in increasing order of count. Each frequency node holds its pages in a list in LRU order, and a hash map sends each page to its frequency node.

```pseudo id=main
LFU-ACCESS(p)                    ▷ frequency list F, map N from page to node
L1  if p is in N then
L2      y ← the node for count N[p].f + 1, created right after N[p] if needed
L3      move p from N[p] to the tail of y; drop N[p] if it is now empty
L4      return hit
L5  if |N| = k then
L6      x ← the first node of F                 ▷ the smallest count
L7      q ← the head of the list of x           ▷ least recently used in x
L8      remove q; drop x if it is now empty
L9  add p at the tail of the node for count 1, created at the front of F if needed
L10 return miss
```

A page reaches count $f$ at the time of its latest request, and line L3 or L9 then puts it at the tail of the list of node $f$. So each list is in order of the latest request, and line L7 takes the least recently used page among the pages with the smallest count. Every step changes a constant number of links: there is no heap and no search.

## Example

Run LFU with $k = 3$ on $\sigma = a, a, b, b, c, d, a, e, b$. The counts are shown after each request.

| $t$ | request | result | evicted | counts after |
| --- | --- | --- | --- | --- |
| 1 | a | miss | | a 1 |
| 2 | a | hit | | a 2 |
| 3 | b | miss | | a 2, b 1 |
| 4 | b | hit | | a 2, b 2 |
| 5 | c | miss | | a 2, b 2, c 1 |
| 6 | d | miss | c | a 2, b 2, d 1 |
| 7 | a | hit | | a 3, b 2, d 1 |
| 8 | e | miss | d | a 3, b 2, e 1 |
| 9 | b | hit | | a 3, b 3, e 1 |

At $t = 6$, $c$ is the only page with count 1. At $t = 8$, $d$ is. LRU would evict $a$ at $t = 6$, the page used least recently, and then miss on $a$ at $t = 7$. LFU keeps $a$ and $b$, which were used twice, and gives up the pages used once.

**A tie.** With $k = 3$ and $x, y, z, x, w$, the miss on $w$ finds $y$ and $z$ with count 1. The tie rule evicts $y$, which was used before $z$.

## Correctness

The invariant has three parts. The frequency nodes are in increasing order of count and none is empty. Each cached page is in exactly one node, the node of its count, and the map points to it. Each node lists its pages in increasing order of the time of their latest request. A hit moves a page from node $f$ to the tail of node $f + 1$, which is right after node $f$ or new; this keeps the order of counts, and the page has the latest request time. A miss removes the head of the first node, which is the least recently used page of smallest count, and adds the new page at the tail of node 1. The proof is below.

## Complexity

- **Time.** $O(1)$ expected per request: one hash lookup and a constant number of link changes. So $O(n)$ expected in total. A [binary heap](/binary-heap/) keyed by (count, time of last use) also works, at $O(\log k)$ per request.
- **Space.** $\Theta(k)$: one entry per cached page and at most $k$ frequency nodes.
- **Not competitive.** For any $k \ge 2$ and any $m \ge 2$, request $k - 1$ pages $m$ times each, then two new pages $a$ and $b$ alternately. Each new page has count 1, so each miss evicts the other one, and LFU misses on every request of the alternating part. MIN keeps $a$ and $b$ and misses only $O(k)$ times. So no ratio bounds LFU against MIN.

## Properties

- **Frequency, not recency.** The decision uses the count first and the time only for ties. A page used once is always evicted before a page used twice.
- **Optimal in a static model.** If the requests are independent draws from a fixed distribution, the [independent reference model](/independent-reference-model/), the best policy keeps the $k$ pages of highest probability (Aho, Denning and Ullman 1971). Perfect LFU estimates these pages from the counts, so it tends to this policy on long traces.
- **Cache pollution.** Pages with high counts from the past stay after their popularity ends, and new pages, which start at count 1, are evicted first. This is the main fault of LFU on traces whose popularity changes.
- **Not a marking algorithm.** It can evict a page requested in the current phase, as in the alternating sequence above.

## Variants and improvements

- **Aging.** [LFU with dynamic aging](/lfu-da/) adds a global age to the key, so that old counts lose weight. Other variants halve all counts from time to time, as [TinyLFU](/tinylfu/) does in its sketch.
- **Recency and frequency together.** [LRFU](/lrfu/) uses a decaying sum of past requests that goes from LFU to LRU with one parameter. [MQ](/mq-cache/) keeps one LRU queue per range of counts. [ARC](/arc/) splits the cache between pages seen once and pages seen twice or more.
- **Admission by frequency.** [W-TinyLFU](/w-tinylfu/) keeps an LRU window and admits a page to the main cache only if its estimated count is higher than the count of the victim, with a [count-min sketch](/count-min-sketch/).
- **MFU.** Most frequently used evicts the page with the highest count, on the idea that a page with a small count was just loaded and will be used. It is rarely good.

## When to use it

Use LFU when popularity is stable over long periods: content caches with a fixed catalog, caches of static assets, or lookup tables in a skewed key space. Do not use plain LFU when popularity changes over time, as in news or session data; use an aged variant or a policy that mixes recency and frequency.

## Pitfalls

- **No tie rule.** "Evict the least frequently used" does not name a page when several pages share the smallest count, and with new pages at count 1 this is the normal case. Name the rule; the usual one is LRU among the least frequent.
- **A heap without the time.** A heap keyed by the count alone breaks ties in an order that depends on the heap layout, so two runs can differ.
- **Counts that never shrink.** Without aging, the counts of old pages grow without bound and pollute the cache.
- **In-cache against perfect counts.** Results for the two kinds of LFU differ a lot. Say which one a measurement uses.

## Implementations

## History

Frequency-based replacement was studied together with LRU and FIFO in the early work on virtual memory. Aho, Denning and Ullman showed in 1971 that, under the independent reference model, keeping the most probable pages is optimal, which is the model where LFU does well. Textbook descriptions of LFU often leave the tie rule and the data structure open. Shah, Mitra and Matani gave the $O(1)$ structure with frequency nodes in 2010. Later policies, such as LFU-DA, LRFU, ARC and TinyLFU, fix the pollution problem by mixing frequency with recency or by aging the counts.

## References
