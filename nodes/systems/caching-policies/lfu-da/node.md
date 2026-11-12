---
tag: 6K0S3T
kind: algorithm
slug: lfu-da
name: LFU with dynamic aging
aliases:
- LFUDA
- LFU-DA
area: systems/caching-policies
level: advanced
summary: LFU whose key is the count plus a cache age L. L rises to the key of each evicted object, so new objects can overtake objects that were popular long ago.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size in objects}
  time: {worst: O(n log k)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2000
  people: [Martin Arlitt, Ludmila Cherkasova, John Dilley, Rich Friedrich, Tai Jin]
  note: Arlitt, Cherkasova, Dilley, Friedrich and Jin described LFU-DA and GDSF for web proxy caches and their heap-based implementation in Squid.
prereqs: [lfu, binary-heap]
see_also: [lfu, gdsf, greedy-dual, lrfu, tinylfu, lru, variable-size-caching, priority-queue]
sources:
  - paper: doi:10.1145/346000.346003
    title: "Martin Arlitt, Ludmila Cherkasova, John Dilley, Rich Friedrich and Tai Jin, Evaluating content management techniques for Web proxy caches, ACM SIGMETRICS Performance Evaluation Review 27(4) (2000), 3-11"
    locator: the description of the LFU-DA and GDSF policies, with the key K_i = C_i * F_i + L
  - url: http://www.squid-cache.org/Doc/config/cache_replacement_policy/
    title: Squid configuration reference, cache_replacement_policy
    locator: the heap LFUDA and heap GDSF policies
  - paper: "Pei Cao and Sandy Irani, Cost-aware WWW proxy caching algorithms, Proceedings of the USENIX Symposium on Internet Technologies and Systems (1997), 193-206"
    title: Cost-aware WWW proxy caching algorithms
    locator: GreedyDual-Size, the inflation value L that LFU-DA and GDSF reuse
---

LFU with dynamic aging (LFU-DA) is a [cache replacement policy](/cache-replacement-policy/) for web proxy caches by Arlitt, Cherkasova, Dilley, Friedrich and Jin (2000). It fixes the main fault of [LFU](/lfu/), cache pollution by objects that were popular long ago. Each cached object $i$ has a key $K_i = C_i \cdot F_i + L$, where $F_i$ is its request count, $C_i = 1$ is its cost, and $L$ is a global cache age. A miss with a full cache evicts the object with the smallest key and sets $L$ to that key. So $L$ grows as the cache works, each new or requested object gets a key based on the current $L$, and an object that stops being requested is in time overtaken by newer ones.

## In plain words

Plain LFU keeps a tally of uses per object and throws out the object with the smallest tally. An object that was used a thousand times last month keeps its large tally, so it never leaves, even when nobody asks for it now.

LFU-DA adds a clock that only moves forward. Each time the cache throws an object out, the clock moves up to that object's score. When an object is used, its score becomes its tally plus the current clock. So an object used now gets a score above all the old scores, and an old object with a large tally slowly falls behind as the clock rises past it. It leaves once the clock reaches its old score.

## The problem

The model is the [paging problem](/paging-problem/) as used for web caches: a cache that holds $k$ objects, a request sequence $\sigma$ of length $n$, an empty cache at the start, and the number of misses as the cost. With $C_i = 1$ for every object, the policy aims at the hit ratio. Arlitt et al. also use LFU-DA with byte sizes and costs; the size-aware form is [GDSF](/gdsf/).

## The algorithm

```pseudo id=main
LFUDA-ACCESS(i)                  ▷ heap H of keys, counts F, cache age L
L1  if i is cached then
L2      F[i] ← F[i] + 1
L3      K[i] ← C_i · F[i] + L; update i in H     ▷ C_i = 1
L4      return hit
L5  if the cache holds k objects then
L6      j ← the object of smallest key in H, the least recently requested on a tie
L7      L ← K[j]                                  ▷ the cache ages
L8      evict j and forget F[j]
L9  F[i] ← 1
L10 K[i] ← C_i · F[i] + L; insert i in H
L11 return miss
```

The key of an object is computed only at its requests (lines L3 and L10), with the value of $L$ at that time; it does not change when $L$ rises later. The code keeps the heap with lazy deletion: line L3 pushes a new entry, and line L6 skips entries that are no longer the current entry of a cached object. The entries are the triples $(K, t, i)$, where $t$ is the time of the latest request, so that ties go to the least recently requested object. When the heap holds more than $2 k + 16$ entries, it is rebuilt from the current entries, so its size stays $O(k)$.

## Example

Run LFU-DA with $k = 2$ on $a, a, a, b, c, b, c, b, c, b, c$. The table shows $(F, K)$ for each cached object.

| $t$ | request | result | evicted | $L$ after | cache after |
| --- | --- | --- | --- | --- | --- |
| 1 to 3 | a, a, a | miss, hit, hit | | 0 | a (3, 3) |
| 4 | b | miss | | 0 | a (3, 3), b (1, 1) |
| 5 | c | miss | b | 1 | a (3, 3), c (1, 2) |
| 6 | b | miss | c | 2 | a (3, 3), b (1, 3) |
| 7 | c | miss | a | 3 | b (1, 3), c (1, 4) |
| 8 | b | hit | | 3 | b (2, 5), c (1, 4) |
| 9 to 11 | c, b, c | 3 hits | | 3 | b (3, 6), c (3, 6) |

Each miss raises $L$ by one, and each new object gets the key $1 + L$. At $t = 7$, $a$ and $b$ both have key 3, and $a$ was requested longer ago, so $a$ goes. LFU-DA has 5 misses. Plain LFU keeps $a$ with its count 3 forever, so $b$ and $c$ evict each other, and LFU misses on all 8 requests from $t = 4$ on.

On a longer run, $20$ requests to one object and then $400$ requests that cycle over three other objects with $k = 3$, LFU misses 401 times and LFU-DA 42 times: the old object leaves once $L$ reaches 20.

## Correctness

Two facts make the policy well defined and show how it ages.

- **The age never falls.** Every key is at least the value of $L$ at the time it was set, and $L$ never falls between that time and now, by induction. So each key in the cache is at least the current $L$, and the next evicted key, the new $L$, is at least the old $L$.
- **The victim is the right one.** The heap entry that line L6 returns is the current entry of a cached object with the smallest $(K, t)$, because stale entries are skipped and every cached object has its current entry in the heap.

With $L$ held at 0, the key is the count, and LFU-DA is LFU with LRU ties. The full proof is below.

## Complexity

- **Time.** $O(\log k)$ per request for the heap, amortized over the rebuilds, plus $O(1)$ expected for the hash map. So $O(n \log k)$ in total.
- **Space.** $\Theta(k)$: the counts, the current keys and a heap of at most $2 k + 16$ entries.
- **No competitive bound is claimed.** LFU-DA is built for a good hit ratio on web traces, not for a worst-case ratio against MIN.

## Properties

- **Frequency with a forward clock.** An object requested at time $t$ has a key between $L(t) + 1$ and $L(t) + F$. To stay, it must be requested often enough to keep its key above the keys of the objects that arrive later.
- **Old popularity fades.** An object that is not requested again keeps its key $K$. Each new key is at least $L + 1$, and $L$ rises to each evicted key. So once $L$ reaches $K$, every object that arrives later has a larger key, and the old object is the next to go among the old keys. In LFU it stays as long as any cached object has a smaller count.
- **Integer keys.** With $C_i = 1$, all keys and $L$ are integers, and ties are common. The tie rule is part of the policy; here it is LRU.
- **A special case of the GreedyDual family.** LFU-DA uses the inflation value $L$ of GreedyDual-Size by Cao and Irani: each eviction raises the base value, and each request resets a key relative to it. See [GreedyDual](/greedy-dual/).

## Variants and improvements

- **GDSF.** [GDSF](/gdsf/) uses $K_i = C_i \cdot F_i / S_i + L$ with the size $S_i$, so that small objects are kept: this raises the hit ratio in objects at the cost of the hit ratio in bytes. LFU-DA without the size is better for the byte hit ratio.
- **Costs.** With $C_i$ set to the fetch cost or the latency, the same rule aims at the total cost of the misses.
- **Periodic aging.** Some LFU caches halve all counts at fixed times instead of using a global age. [TinyLFU](/tinylfu/) does this in its frequency sketch.
- **Decay in time.** [LRFU](/lrfu/) weights each past request by a factor that decays with its age, which gives a continuous range between LFU and LRU.

## When to use it

Use LFU-DA for a proxy or content cache where popularity is skewed but changes over hours or days, and where the byte hit ratio matters. Squid offers it as heap LFUDA. Prefer GDSF when object sizes vary a lot and the object hit ratio matters more. For general key-value caches, policies such as W-TinyLFU usually do better with less state.

## Pitfalls

- **Updating keys when $L$ rises.** The key of an object uses the value of $L$ at its latest request. Recomputing all keys with the new $L$ adds the same amount to each key and undoes the aging.
- **Setting $L$ to the wrong value.** $L$ must become the key of the evicted object, not its count, and not the smallest key after the eviction.
- **Keeping counts after eviction.** The count is reset when the object leaves. Keeping it, as in perfect LFU, brings back the pollution that the age was meant to remove.
- **Stale heap entries.** With lazy deletion, the heap grows at each hit. Rebuild it, or use an [indexed priority queue](/indexed-priority-queue/) with a decrease-key, so that the space stays $O(k)$.

## Implementations

## History

Cao and Irani introduced GreedyDual-Size in 1997, with an inflation value $L$ that rises to the priority of each evicted document. Arlitt, Cherkasova, Dilley, Friedrich and Jin at HP Labs applied the same idea to frequency, as LFU with dynamic aging, and its size-aware form GDSF. They implemented both in the Squid proxy cache with a heap and reported their results in Performance Evaluation Review in 2000. Squid still offers both policies.

## References
