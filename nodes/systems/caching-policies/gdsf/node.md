---
tag: J6DJ3W
kind: algorithm
slug: gdsf
name: Greedy-Dual-Size-Frequency (GDSF)
aliases:
- GDSF
- GD-Size-Frequency
- Greedy-Dual-Size-Frequency
area: systems/caching-policies
level: research
summary: "A web cache policy with the key L + frequency × cost / size. The cache evicts the lowest keys and raises L to them, so it keeps small, popular and costly objects."
solves: [variable-size-caching]
model: word-ram
complexity:
  vars: {n: the number of requests, m: the largest number of objects in the cache}
  time: {worst: O(n m log m), average: O(n log m)}
  space: {extra: O(m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1998
  people: [Ludmila Cherkasova]
  note: Cherkasova proposed GDSF at HP Labs in 1998 as a change to GreedyDual-Size. Arlitt, Cherkasova, Dilley, Friedrich and Jin built it into the Squid proxy and studied it in 2000.
prereqs: [greedy-dual, lfu]
see_also: [lfu-da, variable-size-caching, landlord-algorithm, cache-hit-ratio, cache-admission-policy, binary-heap, tinylfu, lru]
sources:
  - paper: "Ludmila Cherkasova, Improving WWW proxies performance with Greedy-Dual-Size-Frequency caching policy, HP Laboratories technical report HPL-98-69 (R.1), November 1998"
    title: "Ludmila Cherkasova, Improving WWW proxies performance with Greedy-Dual-Size-Frequency caching policy, HPL-98-69 (R.1), 1998"
    locator: "Section 5, the policy with the key Pr(f) = Clock + Fr(f) * Cost(f) / Size(f) and the choice of files to evict; Section 6, its properties; Section 7, Greedy-Dual-Frequency for pages of one size"
  - paper: doi:10.1145/346000.346003
    title: "Martin Arlitt, Ludmila Cherkasova, John Dilley, Rich Friedrich and Tai Jin, Evaluating content management techniques for Web proxy caches, ACM SIGMETRICS Performance Evaluation Review 27(4) (2000), 3-11"
    locator: the GDSF and LFU-DA policies, their heap implementation in Squid, and their hit ratios and byte hit ratios on proxy traces
  - paper: "Pei Cao and Sandy Irani, Cost-aware WWW proxy caching algorithms, Proceedings of the USENIX Symposium on Internet Technologies and Systems (USITS), 1997"
    title: "Pei Cao and Sandy Irani, Cost-aware WWW proxy caching algorithms, USITS 1997"
    locator: GreedyDual-Size, the rule that GDSF extends
---

Greedy-Dual-Size-Frequency (GDSF) is a cache replacement policy for web proxies, proposed by Cherkasova in 1998. It extends [GreedyDual-Size](/greedy-dual/) with a request count. Each cached object $f$ has the key $\mathrm{Pr}(f) = L + \mathrm{Fr}(f) \cdot c(f)/s(f)$, where $\mathrm{Fr}(f)$ counts the requests to $f$ since it entered the cache, $c(f)$ is its cost, $s(f)$ its size, and $L$ a clock that rises to the key of each evicted object. So the cache prefers objects that are popular, small and expensive to fetch. GDSF gives a high hit ratio on web traces, but unlike GreedyDual-Size it has no competitive bound.

## In plain words

Each object in the cache has a score. The score is high when the object was requested often, is small, and was slow or expensive to fetch. When space is needed, the objects with the lowest scores leave.

The cache also keeps a clock $L$. Each time an object leaves, the clock moves up to its score. A requested object gets its new score on top of the current clock. So an object that is not requested for a long time falls behind newer objects, even if it was very popular once.

A new object also gets a score, and it competes with the objects in the cache. If its score is the lowest, the cache does not keep it at all. This stops one large and cold object from pushing out many small and useful ones.

## The problem

The cache has capacity $k$ bytes. Each request names an object $f$ with size $s(f)$ and cost $c(f)$. A hit is free; a miss costs $c(f)$. The goal is a low miss cost on a sequence that is known only up to now, as in [caching with variable object sizes](/variable-size-caching/). The two usual goals are a high hit ratio, with $c = 1$, and a high byte hit ratio, with a cost that grows with the size (see [cache hit ratio](/cache-hit-ratio/)).

## The algorithm

The cache stores the key $\mathrm{Pr}(g)$ and the count $\mathrm{Fr}(g)$ for each cached object $g$, the space in use, and the clock $L$, which starts at $0$. The order of objects is by key; for equal keys the older key comes first.

```pseudo id=main
GDSF-REQUEST(f)                            ▷ size s(f), cost c(f), capacity k
L1  if f is in the cache then
L2      Fr(f) ← Fr(f) + 1
L3      Pr(f) ← L + Fr(f) · c(f) / s(f)
L4      return hit
L5  Pr(f) ← L + c(f) / s(f)                    ▷ Fr(f) = 1, with L before any eviction
L6  V ← ∅
    while used − size(V) + s(f) > k do
L7      g ← the first object of (the cache − V) ∪ {f} in the order
L8      if g = f then
L9          return miss                        ▷ f is not cached; nothing is evicted
L10     V ← V ∪ {g}
L11 evict each object of V
L12 if V ≠ ∅ then L ← the largest key in V
L13 load f with Pr(f) and Fr(f) = 1
L14 return miss
```

A [binary heap](/binary-heap/) keyed by $(\mathrm{Pr}, \text{time})$ gives line L7. A hit pushes a new entry and leaves the old one, which is thrown away when it comes to the top. If the new object is refused at line L9, the candidates already popped are pushed back.

Two details come from the report. The count starts again at $1$ each time an object enters the cache: it counts requests while the object is cached, not over all time. And the key of the new object is computed at line L5, with the value of $L$ before the evictions of this miss; GreedyDual-Size computes it after.

## Example

Capacity $k = 2$, all sizes and costs $1$, and the trace $a\,a\,a\,b\,c\,a$.

| $t$ | request | GDSF | keys after | $L$ | GreedyDual-Size |
|---|---|---|---|---|---|
| 1 | $a$ | miss | $a{:}1$ | 0 | miss |
| 2 | $a$ | hit | $a{:}2$ | 0 | hit |
| 3 | $a$ | hit | $a{:}3$ | 0 | hit |
| 4 | $b$ | miss | $a{:}3$, $b{:}1$ | 0 | miss |
| 5 | $c$ | miss, evict $b$ | $a{:}3$, $c{:}1$ | 1 | miss, evict $a$ |
| 6 | $a$ | hit | $a{:}5$, $c{:}1$ | 1 | miss |

At time 5 the new object $c$ has the key $0 + 1 = 1$, and $b$ also has the key $1$ but is older, so $b$ is first in the order and leaves. GreedyDual-Size has no count; with unit sizes and costs it is [LRU](/lru/), so it evicts $a$, which was used before $b$. GDSF has 3 misses and GreedyDual-Size has 4.

**A refused object.** Capacity $4$, unit costs. After $a\,a\,b\,b$ (size 1 each) and $c$ (size 2), the keys are $a{:}2$, $b{:}2$, $c{:}1/2$, and the cache is full. A request for $z$ of size 3 gives it the key $0 + 1/3$. This is the lowest key, so $z$ is not cached and nothing leaves. GreedyDual-Size would evict $c$, then $a$ and $b$ to make room for $z$.

## Correctness

GDSF is a heuristic, so "correct" means that the code follows the rule and that the rule has the effect it claims. The full proofs are below.

- **The heap code is the rule.** Popping the heap gives the cached objects in increasing order. Comparing each of them with the new object before taking it gives the same set, and the same refusals, as sorting all candidates with the new object among them.
- **$L$ is a clock.** After each request each cached key is at least $L$, and $L$ never falls. The objects evicted are the first ones in the order, and the new object comes after all of them, so all keys that remain are at least the new $L$.
- **LRU is a special case.** With unit sizes and costs and no count, each key is $L + 1$ at the time of its last request. These keys grow with time, so the order is the order of last use.

## Complexity

A hit is one heap push, $O(\log m)$ time. A miss that evicts $r$ objects pops $r$ valid entries. Each valid entry was pushed once, so over the whole run these pops cost no more than the pushes. A refused object is different: it may pop many candidates and push them back, and nothing pays for this work. So a miss takes $O((1 + r') \log m)$ time, where $r'$ is the number of candidates examined, and the worst case for $n$ requests is $O(n m \log m)$. On web traces a refused object is usually large, and only a few candidates are examined. The space is $O(m)$ for the keys, counts and heap.

## Properties

- **Frequency with aging.** The count raises the key of popular objects, and the clock $L$ lets new objects pass objects that were popular long ago.
- **Size-aware.** A key falls with the size, so small objects stay longer. This raises the hit ratio and lowers the byte hit ratio.
- **Admission built in.** A new object with the lowest key is not cached.
- **No competitive bound.** On the sequence $a^N (b\,c)^N$ with $k = 2$, GDSF has $2N + 1$ misses while the optimum has 3. The count can keep an object that will not be used again for a time that grows with its old popularity.
- **Online and deterministic.**

## Variants and improvements

- **GD-Size-Frequency(1) and (packets).** Cherkasova follows Cao and Irani in two cost choices: $c = 1$, aimed at the hit ratio, and $c = 2 + s/536$, the estimated number of network packets of a miss, aimed at both the hit ratio and the byte hit ratio.
- **[LFU-DA](/lfu-da/).** The key $L + \mathrm{Fr}(f) \cdot c(f)$, with no division by the size. Arlitt and others report that it gives the better byte hit ratio, and GDSF the better hit ratio.
- **Greedy-Dual-Frequency.** For pages of one size, Section 7 of the report proposes the key $L + \mathrm{Fr}(f) \cdot c(f)$ for paging.
- **Counts that survive eviction.** Keeping counts of objects that left the cache needs extra memory for objects that are not cached. A compact sketch such as [TinyLFU](/tinylfu/) does this with little space.

## When to use it

Use GDSF for a proxy or CDN cache whose objects vary much in size, when the object hit ratio matters most and the popularity of objects is skewed. Squid offers it as heap GDSF. When the byte hit ratio matters more, use LFU-DA or [GreedyDual-Size](/greedy-dual/) with the cost equal to the size. For key-value caches, newer policies such as W-TinyLFU often do as well with less state.

## Pitfalls

- **Old popularity.** An object with a large count stays long after its last use, as the example of the properties shows. The clock limits this, but only as fast as $L$ rises.
- **The new key and the old $L$.** The key of the new object uses $L$ before the evictions of its miss. An implementation that computes it after the evictions is closer to GreedyDual-Size; both are used, and results differ in small ways.
- **Bytes against objects.** A hit ratio in objects can rise while the hit ratio in bytes falls. Measure the one that matters.
- **Floating point.** $L$ grows without limit; use exact or wide numbers.

## Implementations

## History

Cao and Irani proposed GreedyDual-Size for web proxies in 1997 and showed that it beat LRU, SIZE and other policies of the time on proxy traces. In 1998 Cherkasova, at HP Labs, noted that GreedyDual-Size does not use how often a document was requested. Her report added the count to the key, gave the full rule with the admission test, and proposed Greedy-Dual-Frequency for pages of one size. In 2000 Arlitt, Cherkasova, Dilley, Friedrich and Jin implemented GDSF and LFU-DA with heaps in the Squid proxy and compared them with LRU on proxy workloads; both policies have been part of Squid since.

## References
