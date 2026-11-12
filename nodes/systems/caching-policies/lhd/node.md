---
tag: VC0D27
kind: algorithm
slug: lhd
name: Least hit density (LHD)
aliases:
- LHD
area: systems/caching-policies
level: research
summary: Learns from age histograms the expected hits per byte and per unit of time of each cached object, and evicts the sampled object with the least such hit density.
solves: [variable-size-caching]
model: word-ram
complexity:
  vars: {n: the number of requests, m: the largest number of cached objects, S: the number of sampled objects, K: the number of classes, A: the number of age bins, I: the requests between reconfigurations}
  time: {worst: O(n S + (n / I) K A), expected: O(n S + (n / I) K A)}
  space: {extra: Θ(m + K A)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 2018
  people: [Nathan Beckmann, Haoxian Chen, Asaf Cidon]
  note: Presented at NSDI 2018 together with RankCache, a key-value cache built on memcached that evicts by sampled ranks.
prereqs: [cache-replacement-policy, random-sampling]
see_also: [hyperbolic-caching, gdsf, greedy-dual, variable-size-caching, cache-hit-ratio, belady-optimal, reuse-distance, lru]
sources:
  - url: https://www.usenix.org/conference/nsdi18/presentation/beckmann
    title: "Nathan Beckmann, Haoxian Chen and Asaf Cidon, LHD: Improving Cache Hit Rate by Maximizing Hit Density, NSDI 2018"
    locator: Section 3 (Eq. 2 for hit density, Eq. 3 to 5 for conditioning on age, Eq. 6 and Section 3.4 for classes), Section 4 (RankCache, sampling, coarsening and explorers)
---

Least hit density (LHD) is an eviction policy for caches that hold objects of different sizes. It asks of every cached object how many hits it is expected to give per byte and per unit of time it will spend in the cache, and evicts the object for which this hit density is least. The policy does not assume a model of the workload. It learns the density from histograms of the ages at which past objects were hit or evicted, split into a few classes. Like [hyperbolic caching](/hyperbolic-caching/), it evicts the worst object among a small random sample.

## In plain words

A cache spends two resources on an object: the bytes it takes and the time it stays. What the cache gains is hits. So a fair score for an object is the hits it will get divided by the bytes times the time. Large objects that stay long and get few hits score low.

Nobody knows the future, so LHD looks at the past. It records at which age (time since the last request) objects got hits and at which age they were thrown out. From these records it estimates, for an object of a given age, how likely it is to be hit later and how much longer it will stay. When space is needed, it picks a few objects at random and throws out the one with the lowest score.

## The problem

The model is [variable-size caching](/variable-size-caching/): a cache of $C$ bytes, requests for objects of known sizes, and the goal of the most hits. A policy such as [LRU](/lru/) ranks objects by one fixed rule, which is good for some access patterns and bad for others, and it ignores size. LHD replaces the fixed rule with a quantity that is right in principle and estimated from the trace.

Section 3 of the paper defines the hit density of an object as

$$
\text{hit density} = \frac{\text{hit probability}}{\text{size} \times \text{expected time in the cache}}. \qquad \text{(Eq. 2)}
$$

The paper then conditions on the object's age $a$: let $H$ be the age at which a lifetime ends with a hit and $L$ the age at which it ends by a hit or an eviction. For an object of age $a$ in class $c$,

$$
\text{hit density}(a, c) = \frac{\sum_{x \ge 1} \Pr[H = a + x \mid c]}{\text{size} \cdot \sum_{x \ge 1} x \cdot \Pr[L = a + x \mid c]}. \qquad \text{(Eq. 6)}
$$

A hit ends one lifetime and starts the next, with age 0.

## The algorithm

Time $t$ counts requests. The age of an object is the time since its last request, divided by a coarseness $\kappa$ and capped at the last of $A$ bins. The class of an object is its number of requests since it entered the cache, capped at $K$, as in Section 3.4 of the paper. For each class $k$ the policy keeps histograms $H_k[e]$ of hits and $L_k[e]$ of lifetimes (hits and evictions) by age bin $e$, and a table $\mathit{rank}_k[a]$. Every $I$ requests it decays the old histograms by a factor $\delta$, adds the new counts and recomputes the table. The hit density of an object $x$ is $\mathit{rank}_{k(x)}[a(x)] / \mathit{size}(x)$.

```pseudo id=main
LHD-ACCESS(x, s)                         ▷ cache of C bytes, S samples
L1  t ← t + 1
L2  if x is cached then
L3      k ← class of x, a ← age of x; add 1 to new hits[k][a] and to new lives[k][a]
L4      last(x) ← t, refs(x) ← refs(x) + 1, hit
L5  else if s > C then miss, and x is not cached
L6  else while the cached bytes plus s exceed C do
L7          draw S distinct cached objects uniformly at random
L8          v ← the sampled object of least rank[class(v)][age(v)] / size(v), the older one on a tie
L9          add 1 to new lives[class(v)][age(v)] and evict v
L10     cache x with size s, last(x) ← t, refs(x) ← 1, miss
L11 if t is a multiple of I then RECONFIGURE()

RECONFIGURE()
L12 for every class k and age bin e: H_k[e] ← δ·H_k[e] + new hits[k][e], L_k[e] ← δ·L_k[e] + new lives[k][e], and clear the new counts
L13 for every class k and age bin a:
L14     rank_k[a] ← (Σ_{e ≥ a} H_k[e]) / (Σ_{e ≥ a} (e − a + 1)·L_k[e]), or 0 if the sum below is 0
```

Line L14 is Eq. 6 on the grid of age bins. An object in bin $a$ will end its lifetime in bin $a$ or later, so the sums start at $e = a$, and the remaining time is counted as $e - a + 1$ bins. This grid, and the choices below, are made for this page; the paper gives the continuous formula and leaves the grid to the implementation. A single pass from the last bin down computes all of $\mathit{rank}_k$ in $O(A)$ time.

The defaults in the code are $S = 64$ (as in the paper), $K = 4$, $A = 64$, $\kappa = \lfloor C/4 \rfloor$, $I = 1000$ and $\delta = 9/10$. The paper's implementation also decays its histograms by 0.9 between reconfigurations. Its reconfiguration interval and coarseness are tuned to its traces and are much larger.

## Example

Take one class and $A = 4$ age bins, and suppose that after decay the histograms are:

| age bin $e$ | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| hits $H[e]$ | 0 | 3 | 0 | 1 |
| lifetimes $L[e]$ | 1 | 3 | 1 | 3 |

So 8 lifetimes ended: 3 hits at age 1, 1 hit at age 3, and 4 evictions at ages 0, 2, 3 and 3. Line L14 gives:

| age bin $a$ | $\sum_{e \ge a} H[e]$ | $\sum_{e \ge a} (e - a + 1) L[e]$ | $\mathit{rank}[a]$ |
| --- | --- | --- | --- |
| 3 | 1 | $1 \cdot 3 = 3$ | 1/3 |
| 2 | 1 | $1 \cdot 1 + 2 \cdot 3 = 7$ | 1/7 |
| 1 | 4 | $1 \cdot 3 + 2 \cdot 1 + 3 \cdot 3 = 14$ | 2/7 |
| 0 | 4 | $1 \cdot 1 + 2 \cdot 3 + 3 \cdot 1 + 4 \cdot 3 = 22$ | 2/11 |

For objects of equal size, an object in bin 2 is evicted before one in bin 3, although it is younger. Objects that pass bin 1 without a hit are unlikely to be hit soon, but those that reach bin 3 have a fair chance. LRU, which always evicts the oldest, cannot express this. A larger object has its rank divided by its size, so a 2-byte object in bin 1 (density 1/7) ties with a 1-byte object in bin 2.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). It shows that the cache never holds more than $C$ bytes, that the eviction loop stops, that every hit and eviction is counted in exactly one histogram bin, that the pass of lines L13 and L14 computes the formula, and that with $S$ at least the number of cached objects the evicted object has the least hit density.

## Complexity

A hit costs $O(1)$ time with a [hash table](/hash-table/). Each eviction samples and scores $S$ objects in $O(S)$ time, and an object can be evicted at most once after it is inserted, so all evictions together cost $O(n S)$. A reconfiguration costs $O(K A)$ and happens every $I$ requests. The space is $\Theta(m)$ for the cached objects and $\Theta(K A)$ for the histograms and tables.

## Properties

- *Randomized.* The sample is random; the code uses a seeded `random.Random`.
- *No worst-case guarantee.* LHD estimates averages from the past. The paper gives no competitive bound, and a trace that changes its pattern can make the learned ranks wrong.
- *Size aware.* Dividing by size favors small objects, which give more hits per byte.
- *It learns only from what it keeps.* If the policy always evicts objects before some age, it never sees hits at that age, and the rank of that age stays 0. The paper keeps 1% of objects as explorers that are not evicted until they reach the largest age, so that the histograms keep covering all ages. The code has no explorers. Its test shows the effect: on a loop of 40 objects mixed with objects requested once, in a cache of 50, LRU and LHD with a sample of 64 get no hits at all, while LHD with a sample of 4 lets some loop objects grow old by chance, learns from their hits, and gets more than 500 hits in the last 2000 requests.

## Variants and improvements

- *Richer classes.* Section 3.4 of the paper uses the reference count; the paper's implementation also separates objects by the age of their last hit and by application.
- *RankCache.* The paper's key-value cache, built on memcached, computes ranks off the critical path and evicts by sampling, with slab memory rebalanced between size classes.
- *Other priorities.* [Hyperbolic caching](/hyperbolic-caching/) uses the same sampled eviction with the priority $n/t$, and [GDSF](/gdsf/) combines frequency, size and cost in a priority queue.

## When to use it

LHD suits key-value caches with objects of many sizes, such as memcached in front of a web service, where the access pattern is stable enough to learn from histograms. It is harder to set up than LRU: the coarseness, the number of classes and the reconfiguration interval must fit the trace, and it needs explorers to keep learning.

A small seeded run made for this page uses Python `random.Random(1)`, a cache of 100 objects of size 1, and 30000 requests per trace, with the code's default parameters. Zipf has 1000 keys with exponent 0.8. Scan repeats 1000 uniform requests to 80 hot keys followed by 300 new keys. Loop cycles through 120 keys. Mix takes 60% Zipf, 20% the next key of a 120-key loop and 20% new keys.

| policy | Zipf | scan | loop | mix |
| --- | --- | --- | --- | --- |
| MIN | 62.4% | 76.7% | 82.9% | 39.3% |
| LRU | 37.5% | 70.7% | 0.0% | 16.7% |
| LHD ($S = 64$, no explorers) | 39.1% | 76.4% | 0.0% | 17.8% |
| Hyperbolic ($S = 64$) | 40.6% | 72.0% | 0.0% | 19.0% |

With all sizes equal the size term has no effect, and with no explorers LHD does not learn the loop. With the finer coarseness $\lfloor C/16 \rfloor$, the scan result fell to 52.7%, which shows how much the grid matters. These numbers come from small synthetic traces and say nothing about real workloads.

## Pitfalls

- *Ages too fine.* If most lifetimes end in the last bin, the table cannot tell old ages apart. Choose $\kappa$ so that the range $\kappa A$ covers the typical reuse time.
- *No explorers.* Without them the policy can lock into a pattern it learned early, as the loop test shows.
- *Counting a hit in the new class.* A hit ends a lifetime in the class the object had before the hit. Raise the reference count after recording the hit, as on lines L3 and L4.
- *Forgetting the evictions.* Lifetimes include evictions. Counting only hits gives densities that are too high for old ages.
- *Objects larger than the cache.* They must not be cached, or the eviction loop empties the cache and still fails.

## Implementations

## History

Nathan Beckmann, Haoxian Chen and Asaf Cidon presented LHD at NSDI 2018. The idea grows out of Beckmann and Sanchez's earlier work on caches that rank lines by their expected value, learned from age histograms, for processor caches. The paper's RankCache showed that sampled eviction by learned ranks can run at the speed of memcached.

## References
