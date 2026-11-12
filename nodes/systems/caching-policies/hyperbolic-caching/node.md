---
tag: NR35XD
kind: algorithm
slug: hyperbolic-caching
name: Hyperbolic caching
aliases:
- hyperbolic eviction
area: systems/caching-policies
level: research
summary: Gives each cached item the priority n/t, its request count over its time in the cache, and on a miss evicts the least priority among a random sample of items.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, c: the cache size in items, S: the number of sampled items}
  time: {worst: O(n S), expected: O(n S)}
  space: {extra: Θ(c)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 2017
  people: [Aaron Blankstein, Siddhartha Sen, Michael J. Freedman]
  note: Presented at USENIX ATC 2017 with prototypes in Redis and in the Django caching framework.
prereqs: [lfu, random-sampling]
see_also: [lru, lhd, lfu-da, lrfu, cache-hit-ratio, random-replacement, tinylfu, w-tinylfu]
sources:
  - url: https://www.usenix.org/conference/atc17/technical-sessions/presentation/blankstein
    title: "Aaron Blankstein, Siddhartha Sen and Michael J. Freedman, Hyperbolic Caching: Flexible Caching for Web Applications, USENIX ATC 2017"
    locator: Section 2 and Figure 1 (the priority function), Section 3 (cost, cost classes, expiration and windowing), Section 5 (sampling and the Redis prototype)
---

Hyperbolic caching gives every cached item $i$ the priority $p_i = n_i / t_i$, where $n_i$ is the number of requests to $i$ since it entered the cache and $t_i$ is the time it has spent in the cache. On a miss with a full cache it draws a small random sample of cached items, as Redis does, and evicts the one of least priority. The priority is a request rate, so an item that was popular long ago loses priority as its time in the cache grows, unlike in [LFU](/lfu/).

## In plain words

Every item in the cache keeps two numbers: how many times it was asked for since it came in, and how long it has been there. Their ratio says how often it is asked for. When space is needed, the cache picks a few items at random, for example 64, and throws out the one with the lowest ratio.

There is no ordered list to keep up to date. A hit only adds one to a counter. The ratio of every item falls slowly while nobody asks for it, and rises when someone does. The name comes from the shape of $n/t$ as a function of $t$, which is a hyperbola.

## The problem

The model is the [paging problem](/paging-problem/) with a cache of $c$ items. LFU keeps items by total count, which keeps items that were popular once and are no longer. LRU looks only at the last request. The paper's aim is a policy that estimates each item's request rate, adapts to changes in popularity, and is easy to extend with costs, sizes and expiration times. Keeping items sorted by a priority that changes with time is costly, because every priority changes at every tick of the clock. Sampling avoids the sort.

## The algorithm

Time $t$ is an integer clock that grows by one on every request. For each cached item the cache stores $n_i$ and its insertion time $\tau_i$. Its priority at time $t$ is $n_i / (t - \tau_i)$. In Figure 1 of the paper, an item enters with $n_i = 1$ and $\tau_i$ equal to the current time. Ties go to the item that entered first.

```pseudo id=main
HYPERBOLIC-ACCESS(x)                     ▷ cache of c items, S samples
L1  t ← t + 1
L2  if x is cached then
L3      n_x ← n_x + 1 and return hit
L4  if c items are cached then
L5      draw S distinct cached items uniformly at random (all of them if fewer than S)
L6      v ← the sampled item with the least n_v / (t - τ_v)
L7      evict v
L8  insert x with n_x ← 1 and τ_x ← t
L9  return miss
```

The Redis prototype uses $S = 64$. If all priorities are distinct, the least of $S$ samples out of $N$ items has expected rank $(N + 1)/(S + 1)$ among them, rank 1 being the lowest. The paper uses the approximation $N/(S+1)$. So with $S = 64$ the evicted item is on average at rank about $N/65$, within the lowest 1.5% or so of the cache.

The paper extends the priority in Section 3:

- *Cost.* Multiply by a cost $c_i$ for item $i$, such as the time to fetch it again. For items of different sizes, $c_i = 1/s_i$, which gives the request rate per byte.
- *Cost classes.* Items of one class share one cost, which the cache can measure as it runs and change for the whole class at once.
- *Expiration.* The priority also takes into account the time left before an item expires.
- *Windowing.* Count only requests in a recent window, so that $n_i$ does not grow without limit for items that stay in the cache a long time.

## Example

Take $c = 3$, $S \ge 3$ so the sample is the whole cache, and the requests A A A B C B C D B C E B D. A is requested three times at the start. B and C are requested twice each.

| $t$ | request | result | priorities on a full miss | evicted | cache after ($n$) |
| --- | --- | --- | --- | --- | --- |
| 1 | A | miss | | | A 1 |
| 2 | A | hit | | | A 2 |
| 3 | A | hit | | | A 3 |
| 4 | B | miss | | | A 3, B 1 |
| 5 | C | miss | | | A 3, B 1, C 1 |
| 6 | B | hit | | | A 3, B 2, C 1 |
| 7 | C | hit | | | A 3, B 2, C 2 |
| 8 | D | miss | A 3/7, B 2/4, C 2/3 | A | B 2, C 2, D 1 |
| 9 | B | hit | | | B 3, C 2, D 1 |
| 10 | C | hit | | | B 3, C 3, D 1 |
| 11 | E | miss | B 3/7, C 3/6, D 1/3 | D | B 3, C 3, E 1 |
| 12 | B | hit | | | B 4, C 3, E 1 |
| 13 | D | miss | B 4/9, C 3/8, E 1/2 | C | B 4, E 1, D 1 |

At $t = 8$, LFU would keep A, which has the most requests, and evict B or C. Hyperbolic caching evicts A, because its three requests are spread over seven ticks. At $t = 13$, E has only one request but entered at $t = 11$, so its rate $1/2$ is higher than C's $3/8$.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). It shows that the cache holds at most $c$ items, that every priority is well defined and at most 1, that with $S \ge c$ the evicted item has the least priority in the cache, and that with $S$ samples out of $N$ distinct priorities the expected rank of the evicted item is $(N+1)/(S+1)$.

## Complexity

A hit costs $O(1)$ time with a [hash table](/hash-table/). To sample in $O(1)$ per item, the code also keeps the cached keys in an array and removes a key by moving the last one into its place. A miss with a full cache computes $S$ priorities, so it costs $O(S)$, and $n$ requests take $O(n S)$ time. The space is $\Theta(c)$: two numbers per item and the array. The paper notes that a kinetic heap could keep the exact order in $O(\log^2 n)$ time per operation for the basic function, but that it does not carry over to the extensions.

## Properties

- *Randomized.* The sample is random. The code uses a seeded `random.Random`, so runs are reproducible.
- *No worst-case guarantee.* The paper gives no competitive bound. A sample can miss every low priority item, and even the exact version is a deterministic online paging policy, whose [competitive ratio](/competitive-ratio/) is at least $c$.
- *Recent items are safe.* An item inserted at time $\tau$ has priority $1/(t - \tau)$, and no priority is above 1, so the newest item has the highest possible priority at the next miss.

## Variants and improvements

- *The extensions of Section 3*, listed above, change only the priority function, not the eviction loop. This is the main point of the design: any priority that can be computed from per-item data plugs into the same sampled eviction.
- *Exact eviction.* With $S \ge c$ the policy evicts the true minimum. This is slower but useful for testing.
- *[LHD](/lhd/)* uses the same sampled eviction with a different priority, the hit density learned from the age of objects.

## When to use it

Hyperbolic caching suits web application caches where items differ in cost or size and popularity changes over time, and where a sampled eviction is already in place, as in Redis. It needs no ordered list, so a hit only touches one counter.

A small seeded run made for this page uses Python `random.Random(1)`, $c = 100$, $S = 64$ and 30000 requests per trace. Zipf has 1000 keys with exponent 0.8. Scan repeats 1000 uniform requests to 80 hot keys followed by 300 new keys. Loop cycles through 120 keys. Mix takes 60% Zipf, 20% the next key of a 120-key loop and 20% new keys.

| policy | Zipf | scan | loop | mix |
| --- | --- | --- | --- | --- |
| MIN | 62.4% | 76.7% | 82.9% | 39.3% |
| LRU | 37.5% | 70.7% | 0.0% | 16.7% |
| Hyperbolic ($S = 64$) | 40.6% | 72.0% | 0.0% | 19.0% |
| W-TinyLFU | 48.1% | 76.7% | 78.9% | 28.6% |

These numbers come from small synthetic traces and say nothing about real workloads.

## Pitfalls

- *Division by zero.* Advance the clock before computing priorities, as on line L1, so that $t - \tau_i \ge 1$ for every cached item.
- *Floating point.* Priorities of old items are close together. The code uses exact fractions; with floats, use a fixed tie rule.
- *Sampling with repeats.* Draw distinct items, or the sample is smaller than $S$ in effect.
- *Counting from zero.* An item enters with $n = 1$; with 0, every new item has the lowest priority and is evicted at the next miss.

## Implementations

## History

Aaron Blankstein, Siddhartha Sen and Michael J. Freedman presented hyperbolic caching at USENIX ATC 2017. They built it into Redis, which already evicts by sampling, and into the Django caching framework, and they showed how costs, cost classes, expiration and windowing fit into the same priority function. The analysis of sampling for eviction follows earlier work by Konstantinos Psounis and Balaji Prabhakar.

## References
