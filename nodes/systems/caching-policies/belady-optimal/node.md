---
tag: WA9T1Y
kind: algorithm
slug: belady-optimal
name: Bélády's optimal algorithm (MIN)
aliases:
- MIN algorithm
- optimal offline replacement
- Belady's MIN for cache simulation
area: systems/caching-policies
level: intro
summary: "Offline policy that evicts the item needed furthest in the future. With unit sizes and costs it has the fewest misses, so cache studies use it as the upper bound on hit ratio."
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size}
  time: {worst: O(n log n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1966
  people: [László Bélády]
  note: Belady defined MIN in his 1966 IBM study of replacement algorithms for virtual storage, as the optimum against which to judge practical policies.
prereqs: [cache, paging-problem, exchange-argument]
see_also: [belady-algorithm, belady-optimality, lru, mattson-stack-algorithm, variable-size-caching, three-cs-model, lru-competitiveness, belady-anomaly]
sources:
  - paper: doi:10.1147/sj.52.0078
    title: "L. A. Belady, A study of replacement algorithms for a virtual-storage computer, IBM Systems Journal 5(2) (1966), 78-101"
    locator: the definition of the optimal replacement rule MIN, and its use as the reference in simulations of practical replacement algorithms
  - paper: doi:10.1147/sj.92.0078
    title: "R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2) (1970), 78-117"
    locator: OPT as a stack algorithm, with the priority given by the time of the next reference, so that one pass gives its miss ratio for all capacities
  - paper: doi:10.1007/s00453-011-9502-9
    title: "Marek Chrobak, Gerhard J. Woeginger, Kazuhisa Makino and Haifeng Xu, Caching is hard, even in the fault model, Algorithmica 63(4) (2012), 781-794"
    locator: offline caching with items of different sizes is strongly NP-hard, even when each miss costs 1
  - paper: doi:10.1109/ISCA.2016.17
    title: "Akanksha Jain and Calvin Lin, Back to the future: leveraging Belady's algorithm for improved cache replacement, ISCA 2016"
    locator: OPTgen, which computes the decisions of Belady's rule on past accesses, and the Hawkeye policy that learns from them
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 4.3, Optimal Caching, a more complex exchange argument
---

Bélády's MIN is the replacement rule that, on a miss with a full cache, evicts the item whose next request is furthest in the future. It needs the whole request sequence in advance, so no live cache can run it. On a trace that is already known, it gives the smallest possible number of misses for a cache of $k$ items of equal size and equal miss cost. For this reason it is the standard yardstick of cache studies: the gap between the misses of a practical policy and the misses of MIN is the most that a better policy could gain. This page treats MIN as a tool of the systems designer. The same rule, stated for the [paging problem](/paging-problem/) of online algorithms, is on the page [Belady's algorithm](/belady-algorithm/), and its optimality theorem, with a proof that converts schedules to demand paging, is on the page [Belady's optimality](/belady-optimality/).

## In plain words

Suppose a cache could see the future. When it must drop an item, it looks at when each item it holds will be asked for next. It drops the one that will be asked for last, or one that will never be asked for again.

No real cache can do this, because it does not know the future. But a simulator that replays a recorded trace does know it. So engineers run this rule on the trace to find the fewest misses that any cache of that size could have. If LRU has 1,000 misses and this rule has 900, then no policy can save more than 100 misses on that trace. The rule is best only when all items have the same size and each miss costs the same.

## The problem

The input is a trace $\sigma_0 \cdots \sigma_{n-1}$ of item keys and a cache size $k \ge 1$. The cache starts empty. Each request for an item that is not in the cache is a miss; the item is then loaded, and if the cache is full, one item is evicted. All items have size 1 and each miss costs 1. The output is the eviction choice at each miss, and the goal is the fewest misses.

This is the demand form of the problem: the cache changes only on a miss. Loading items early, or evicting without need, never reduces the number of loads, which the conversion on the page [demand paging](/demand-paging/) shows. So the demand form loses nothing.

## The algorithm

Let $\mathrm{next}[t]$ be the position of the next request for $\sigma_t$ after $t$, or $n$ if there is none. The value $n$ stands for "never". The algorithm keeps a map $key$ from each cached item to the position of its next request, and a max-heap $H$ of pairs (next position, item) with lazy deletion.

```pseudo id=main
MIN(σ, k)                                    ▷ σ = σ_0 .. σ_{n−1}, cache size k ≥ 1
L1  last ← an empty map
L2  for t ← n − 1 downto 0 do
L3      next[t] ← last[σ_t] if σ_t ∈ last, else n
L4      last[σ_t] ← t
L5  key ← an empty map, H ← an empty max-heap, misses ← 0
L6  for t ← 0 to n − 1 do
L7      x ← σ_t
L8      if x ∉ key then
L9          misses ← misses + 1
L10         if |key| = k then
L11             repeat (d, y) ← POP-MAX(H) until y ∈ key and key[y] = d
L12             delete key[y]                    ▷ evict y
L13     key[x] ← next[t]; PUSH(H, (next[t], x))
L14 return misses
```

Lines L1 to L4 scan the trace backward once. Line L13 runs on a hit and on a miss, so the key of each cached item is always the position of its next request. The heap holds stale pairs for items whose key changed or that were evicted, and line L11 skips them. Ties are possible only among items with key $n$, which are never requested again. The implementation breaks them by evicting the one whose last request is oldest; the number of misses does not depend on the tie rule.

## Example

Take the classic trace $1\,2\,3\,4\,1\,2\,5\,1\,2\,3\,4\,5$ with $k = 3$. Positions are numbered from 1 here.

| $t$ | request | result | next requests of the cached items | evict | cache after |
|---|---|---|---|---|---|
| 1 to 3 | 1, 2, 3 | 3 misses | | | {1, 2, 3} |
| 4 | 4 | miss | 1 at 5, 2 at 6, 3 at 10 | 3 | {1, 2, 4} |
| 5, 6 | 1, 2 | hits | | | {1, 2, 4} |
| 7 | 5 | miss | 1 at 8, 2 at 9, 4 at 11 | 4 | {1, 2, 5} |
| 8, 9 | 1, 2 | hits | | | {1, 2, 5} |
| 10 | 3 | miss | 1 never, 2 never, 5 at 12 | 1 | {2, 3, 5} |
| 11 | 4 | miss | 2 never, 3 never, 5 at 12 | 2 | {3, 4, 5} |
| 12 | 5 | hit | | | {3, 4, 5} |

MIN has 7 misses, 5 of them compulsory. The same trace, for each cache size:

| $k$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| MIN | 12 | 9 | 7 | 6 | 5 |
| [LRU](/lru/) | 12 | 12 | 10 | 8 | 5 |
| [FIFO](/fifo-replacement/) | 12 | 12 | 9 | 10 | 5 |

The MIN row never rises as $k$ grows. The FIFO row rises from 9 to 10, which is [Belady's anomaly](/belady-anomaly/). At $k = 2$, MIN still gets 3 hits, while LRU and FIFO get none, because each item comes back only after two other items.

## Correctness

Two facts are needed. First, the eviction at line L11 is the cached item with the furthest next request. After line L13 at time $t$, each cached item $y$ has one *current* pair $(key[y], y)$ in $H$, and $key[y]$ is the position of its next request after its last request, which is also its next request after $t$. A stale pair for $y$ has a smaller key than any later pair for $y$, so it never passes the test of line L11. So the first pair that passes is the current pair with the largest key.

Second, the rule is optimal. The proof in [the correctness file](proofs/correctness.md) is an exchange argument of the lazy kind. Take a schedule $S$ that first differs from MIN at time $t$, where $S$ evicts $u$ and MIN evicts $v$, so $u$ is requested before $v$. The new schedule $S'$ evicts $v$ and then copies $S$ as long as it can. It never loads an item that is not requested; the two caches differ in one item until they become equal, and the first request for $u$ gives $S'$ a hit that pays for the one later miss on $v$. This differs from the proof on the page [Belady's optimality](/belady-optimality/), which loads $v$ early and then converts the schedule to demand form.

## Complexity

- **Time.** The backward scan takes $O(n)$ expected time with a hash map. Line L13 pushes $n$ pairs, and each pop at line L11 removes one of them, so the heap work is $O(n \log n)$.
- **Space.** $\Theta(n)$ for the array $next$ and the heap.
- **Small caches.** For hardware simulation with small $k$, scanning the $k$ cached keys at each miss costs $O(k)$ and is often faster than a heap.
- **Many cache sizes.** One run of the [Mattson stack algorithm](/mattson-stack-algorithm/) with the priority "next request soonest" gives the MIN miss count for all $k$ at once.

## Properties

- **Offline.** MIN needs the future of the trace. It is a tool for simulation and analysis, and for planning when the access order is fixed in advance.
- **A stack algorithm.** With a tie rule that does not depend on $k$, the MIN cache of size $k$ is always a subset of the MIN cache of size $k + 1$. So MIN has the [inclusion property](/inclusion-property/) and no anomaly.
- **A bound for all online policies.** Each online policy has at least the misses of MIN. LRU and FIFO can have up to $k$ times as many from an empty cache, see [LRU competitiveness](/lru-competitiveness/).
- **Only for unit sizes and costs.** With sizes or costs the rule is a heuristic, see the pitfalls.

## Variants and improvements

- **Bypass.** Many hardware and software caches may decline to store an item. Then the optimum also bypasses: on a miss, if the requested item's next request is further than all cached ones, do not cache it. The same exchange argument applies.
- **Learning from MIN.** Hawkeye (Jain and Lin 2016) runs OPTgen, which finds what MIN would have done on a window of past accesses, and trains a predictor of which load addresses lead to items that MIN would keep. Later processor policies follow the same idea.
- **Sizes.** With items of different sizes, finding the fewest misses offline is strongly NP-hard (Chrobak, Woeginger, Makino and Xu 2012), see [variable-size caching](/variable-size-caching/).
- **Costs.** With equal sizes and different miss costs, the problem is [weighted paging](/weighted-paging-problem/). Furthest in the future is not optimal there, but the offline problem can still be solved in polynomial time.

## When to use it

Use MIN to measure the headroom of a cache design on a trace: run the real policy and MIN at the same size, and compare. Use its miss curve, from the Mattson stack algorithm, as the lower envelope of all miss ratio curves. Use it when the whole request order is known in advance, such as in the reuse of buffers in a compiled program or in the out-of-core schedule of a fixed computation. Do not use it as a live policy, since it needs the future; use [LRU](/lru/), [CLOCK](/clock/) or an adaptive policy, and judge them by the gap to MIN.

## Pitfalls

- **Sizes.** Furthest in the future can be wrong when items have different sizes. Take sizes $a = 3$ and $b = c = d = 1$, a capacity of 4, and the trace $a\,b\,c\,d\,c\,a\,b$. The rule that evicts furthest items until the new item fits has 6 misses: it evicts $b$ at $c$ and $a$ at $d$. The best schedule has 5: it evicts $a$ at $c$, then evicts $c$ and $d$ for the second $a$, and keeps $b$ for the last request.
- **Writes.** MIN counts misses. If evicting a dirty item costs a write to the backing store, as in a [write-back](/write-back/) cache, MIN need not give the least traffic.
- **The wrong baseline.** The fully associative LRU cache of the [three Cs model](/three-cs-model/) is not MIN. A study that quotes "capacity misses" should say which one it used.
- **Warm start.** On a short trace, most misses of MIN are compulsory. Compare policies on the non-compulsory misses, or use long traces.
- **Infinity.** Code "never" as $n$ or more, never as a valid position, or an item needed at the last position looks like an item never needed.

## Implementations

## History

Belady defined MIN in 1966, in an IBM study of replacement algorithms for virtual memory that compared practical policies with MIN by simulation. Mattson, Gecsei, Slutz and Traiger (1970) showed that OPT, with the priority "next reference soonest", is a stack algorithm, so its miss ratio for all memory sizes comes from one pass. Kleinberg and Tardos present the optimality proof as their main example of a subtle exchange argument. Chrobak, Woeginger, Makino and Xu (2012) proved that the problem with sizes is NP-hard. In 2016, Jain and Lin turned MIN from a yardstick into a teacher, with the Hawkeye cache that learns from its decisions on the past.

## References
