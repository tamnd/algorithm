---
tag: F080QZ
kind: algorithm
slug: greedy-dual
name: GreedyDual and GreedyDual-Size
aliases:
- GD-Size
- Greedy Dual algorithm
- GreedyDual
- GreedyDual-Size
area: systems/caching-policies
level: advanced
summary: "Online caching for objects of different costs and sizes. Each object gets the priority L + cost/size; evict the lowest and raise L to its value. It is k-competitive."
solves: [weighted-paging-problem, variable-size-caching]
model: word-ram
complexity:
  vars: {n: the number of requests, m: the largest number of objects in the cache}
  time: {worst: O(n log m)}
  space: {extra: O(m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1991
  people: [Neal E. Young, Pei Cao, Sandy Irani]
  note: Young gave GreedyDual for weighted caching at SODA 1991, with the journal version in Algorithmica in 1994. Cao and Irani added the size and the inflation value L for web proxies in 1997.
prereqs: [weighted-paging-problem, variable-size-caching, lru]
see_also: [landlord-algorithm, gdsf, lfu-da, binary-heap, priority-queue, competitive-ratio, sleator-tarjan-paging-bound, cache-hit-ratio]
sources:
  - paper: doi:10.1007/BF01189992
    title: "Neal E. Young, The k-server dual and loose competitiveness for paging, Algorithmica 11(6) (1994), 525-541"
    locator: the GreedyDual algorithm for weighted caching and its ratio k/(k - h + 1); the conference version is On-line caching as cache size varies, SODA 1991
  - paper: "Pei Cao and Sandy Irani, Cost-aware WWW proxy caching algorithms, Proceedings of the USENIX Symposium on Internet Technologies and Systems (USITS), 1997"
    title: "Pei Cao and Sandy Irani, Cost-aware WWW proxy caching algorithms, USITS 1997"
    locator: the GreedyDual-Size algorithm, its form with the inflation value L, and the proof that it is k-competitive with k the cache size over the smallest object size
  - paper: doi:10.1007/s00453-001-0124-5
    title: "Neal E. Young, On-line file caching, Algorithmica 33(3) (2002), 371-383"
    locator: the Landlord algorithm, which contains GreedyDual-Size, and its ratio k/(k - h + 1) for objects of any size and cost
---

GreedyDual is an online cache replacement rule for objects that cost different amounts to fetch again. GreedyDual-Size extends it to objects of different sizes. Each cached object $p$ has a priority $H(p) = L + c(p)/s(p)$, set when $p$ is loaded or hit, where $c(p)$ is the cost, $s(p)$ the size and $L$ a global *inflation value*. To make room, the cache evicts the object with the least $H$ and raises $L$ to that value. The rule is $k$-competitive, the best ratio for a deterministic rule, and with unit sizes and costs it is exactly [LRU](/lru/).

## In plain words

Each object in the cache has a score. A new or used object gets a high score if it was expensive to fetch, and a low score if it was cheap or large. When the cache is full, the object with the lowest score leaves.

Old objects must lose value over time, or an object that was expensive once would stay forever. Young's first version subtracts the lowest score from every score at each eviction. GreedyDual-Size does the same thing in a cheaper way: it keeps one number $L$, the score of the last object that left, and adds $L$ to the score of each object when it is used. Objects that are not used fall behind $L$ and leave in turn.

## The problem

The cache has capacity $k$. Each request names an object $p$ with size $s(p) \ge 1$ and cost $c(p) \ge 0$. A miss costs $c(p)$, and the cache must then hold $p$, unless $p$ is larger than the whole cache. The goal is a small total miss cost on a sequence that is learned one request at a time. This is [caching with variable object sizes](/variable-size-caching/); with all sizes $1$ it is [weighted paging](/weighted-paging-problem/).

## The algorithm

The cache stores $H(q)$ for each object $q$ that it holds, the total size $used$ of these objects, and the value $L$, which starts at $0$.

```pseudo id=main
GD-SIZE-REQUEST(p)                         ▷ size s(p), cost c(p), capacity k
L1  if p is in the cache then
L2      H(p) ← L + c(p)/s(p)
L3      return hit
L4  if s(p) > k then return miss               ▷ too large: serve p without loading it
L5  while used + s(p) > k do
L6      q ← the cached object with the least H(q)
L7      L ← H(q)
L8      evict q, used ← used − s(q)
L9  load p, H(p) ← L + c(p)/s(p), used ← used + s(p)
L10 return miss
```

A [binary heap](/binary-heap/) keyed by $H$ gives line L6. A hit changes $H(p)$, so the code pushes a new entry and leaves the old one in the heap; a pop that finds an entry whose time stamp is out of date throws it away. Ties in line L6 go to the object whose value was set first.

**The decrement form.** Young's GreedyDual sets $H(p) = c(p)$ at a hit or load. At an eviction it subtracts $\delta = \min_q H(q)$ from $H(q)$ for each cached $q$, then evicts an object with value $0$. This takes time linear in the cache size at each eviction. The inflation form keeps $L$ equal to the sum of all the subtracted amounts, so the stored values are the decrement values plus $L$. Cao and Irani gave this form in their paper on GreedyDual-Size. With sizes $1$ the two rules are the same algorithm.

## Example

Capacity $k = 4$. The objects are $a$ (size 1, cost 4), $b$ (size 2, cost 2), $c$ (size 2, cost 6) and $d$ (size 1, cost 1). So $c(x)/s(x)$ is $4, 1, 3, 1$. The trace is $a\,b\,c\,a\,d\,b$.

| $t$ | request | result | evicted | $L$ after | values after |
|---|---|---|---|---|---|
| 1 | $a$ | miss | | 0 | $a{:}4$ |
| 2 | $b$ | miss | | 0 | $a{:}4$, $b{:}1$ |
| 3 | $c$ | miss | $b$ | 1 | $a{:}4$, $c{:}4$ |
| 4 | $a$ | hit | | 1 | $a{:}5$, $c{:}4$ |
| 5 | $d$ | miss | | 1 | $a{:}5$, $c{:}4$, $d{:}2$ |
| 6 | $b$ | miss | $d$, then $c$ | 4 | $a{:}5$, $b{:}5$ |

At time 3, $c$ needs 2 free units and only 1 is free, so $b$ leaves and $L$ becomes 1. At time 4 the hit on $a$ gives $a$ the value $L + 4 = 5$, above the value 4 it had before. At time 6, $b$ needs 2 units and none is free. The rule evicts $d$ (value 2), which frees only 1 unit, and then $c$ (value 4). $L$ ends at 4, so the new $b$ gets $4 + 1 = 5$.

## Correctness

The two forms make the same decisions. In the decrement form all stored values differ from those of the inflation form by the same amount $L$, so both forms order the objects in the same way and choose the same victim. When the victim has inflation value $H$, the decrement form subtracts $H - L$ from each value, and the inflation form raises $L$ to $H$; the identity still holds after the step. One consequence is that $L$ never decreases.

The ratio comes from a potential function. With unit sizes, an offline optimum OPT with $h \le k$ slots, and $G$ the values of the decrement form, the potential

$$\Phi = (h - 1) \sum_{x \in \mathrm{GD}} G(x) + k \sum_{x \in \mathrm{OPT}} \bigl(c(x) - G(x)\bigr)$$

is non-negative. Each request changes it so that $(k - h + 1)\,\Delta\mathrm{GD} + \Delta\Phi \le k\,\Delta\mathrm{OPT}$, so the cost of GreedyDual is at most $k/(k - h + 1)$ times that of OPT. The full proof is below. For objects of any size the same bound is Young's theorem on [Landlord](/landlord-algorithm/), whose full-credit case is GreedyDual-Size.

## Complexity

Each request does $O(1)$ heap pushes. Each pop removes an entry that some push made, so the pops cost no more than the pushes in total. With $m$ the largest number of cached objects, and the heap rebuilt when stale entries make up more than half of it, each heap operation takes $O(\log m)$ time. So $n$ requests take $O(n \log m)$ time and $O(m)$ space. The decrement form takes $O(m)$ time per eviction.

The values grow with $L$ and do not wrap: $L$ is at most the largest value ever set, which is at most the sum of $c(x)/s(x)$ over the misses. With floating point numbers, a long run can make $L$ large enough that small differences of $c/s$ are lost. The code uses exact fractions.

## Properties

- **Competitive.** GreedyDual is $k/(k - h + 1)$-competitive against an optimum with $h$ slots, so $k$-competitive for $h = k$ (Young 1994). GreedyDual-Size is $k$-competitive where $k$ is the cache size over the smallest object size (Cao and Irani 1997).
- **It contains LRU.** With $s = c = 1$ each value is $L + 1$ at its last use, and $L$ never falls, so the least value belongs to the least recently used object.
- **Cost-aware.** An expensive object survives about $c/s$ units of growth in $L$ after its last use; a cheap one leaves soon.
- **No frequency.** One hit resets the value, but many hits do not raise it more. [GDSF](/gdsf/) adds a count for this.
- **Online and deterministic.**

## Variants and improvements

- **Cost choices.** Cao and Irani studied $c = 1$, which aims at a high object hit ratio and so favors small objects, and a cost that grows with the number of network packets of the object, which aims at a low latency. With $c(p) = s(p)$ each value is $L + 1$, so the rule is LRU for bytes.
- **[GDSF](/gdsf/).** The value is $L + F(p)\,c(p)/s(p)$, where $F(p)$ counts the hits on $p$ while it is cached.
- **[LFU-DA](/lfu-da/).** LFU with dynamic aging uses the value $L + F(p)$, the case $c = s$ of GDSF.
- **[Landlord](/landlord-algorithm/).** At a hit Landlord may raise the credit of $p$ to any value between its current credit and its cost; GreedyDual-Size always raises it to the cost.
- **Randomized rules.** A randomized algorithm can reach $O(\log k)$ for weighted paging; see the [weighted paging](/weighted-paging-problem/) page.

## When to use it

Use GreedyDual-Size when objects differ much in size or in cost to fetch again: web proxies, CDN edges, caches of query results and caches in front of slow stores. Choose $c$ to match the goal: $c = 1$ for the object hit ratio, $c = s$ for the byte hit ratio (this makes the rule LRU), or a latency or price for the cost of misses. For objects of one size and one cost, plain [LRU](/lru/) or [CLOCK](/clock/) does the same work with less code.

## Pitfalls

- **The bound counts in units of the smallest object.** With objects from 100 bytes to 100 MB, $k$ is huge, and the guarantee says little. The rule is still good in practice, but for other reasons.
- **Subtracting from all values.** The decrement form takes linear time per eviction. Use $L$.
- **Forgetting to add $L$ at a hit.** If a hit sets $H(p) = c(p)/s(p)$ without $L$, an object that was used just now can be below objects that were not used for a long time.
- **Floating point drift.** $L$ grows without limit. Use exact or wide numbers, or subtract $L$ from all values at rare moments.
- **Large objects.** An object larger than the cache cannot be loaded; serve it without loading, as in line L4.
- **Scan pollution.** A burst of one-time objects with high $c/s$ can push out useful ones. An [admission policy](/cache-admission-policy/) helps here.

## Implementations

## History

Young introduced GreedyDual at SODA 1991 in a paper on how the competitive ratio of paging changes with the cache size. The journal version, *The k-server dual and loose competitiveness for paging* (Algorithmica, 1994), derives the rule from the dual of a linear program and proves the ratio $k/(k - h + 1)$ for weighted caching. Cao and Irani took the rule to web proxy caches in 1997. They added the size, called the result GreedyDual-Size, gave the form with the inflation value $L$, and showed on proxy traces that it does well on the hit ratio and on the latency. Young then gave the Landlord rule and its proof for objects of any size at SODA 1998, with the journal version in 2002. Cherkasova added the frequency count of GDSF in 1998.

## References
