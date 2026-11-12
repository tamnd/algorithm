---
tag: MSGGRD
kind: algorithm
slug: w-tinylfu
name: W-TinyLFU
aliases:
- Window TinyLFU
area: systems/caching-policies
level: research
summary: A cache with a small LRU window in front of an SLRU main cache, where a TinyLFU frequency filter decides if an object leaving the window may replace a main victim.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, c: the cache size in objects, d: the number of rows of the sketch, W: the sample size of the filter}
  time: {worst: O(n d + n c d / W), expected: O(n d)}
  space: {extra: Θ(c d)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2017
  people: [Gil Einziger, Roy Friedman, Ben Manes]
  note: Introduced in the journal version of TinyLFU for workloads with sparse bursts, and used as the eviction policy of the Caffeine Java cache.
prereqs: [tinylfu, slru, lru]
see_also: [cache-admission-policy, count-min-sketch, frequency-estimation, arc, lirs, s3-fifo, two-q, sieve]
sources:
  - paper: doi:10.1145/3149371
    title: "Gil Einziger, Roy Friedman and Ben Manes, TinyLFU: A Highly Efficient Cache Admission Policy, ACM Transactions on Storage 13(4), 2017"
    locator: Section 4 (W-TinyLFU, Figure 5), Section 3.3 (the reset), Section 3.4 (the doorkeeper and small counters)
  - url: https://arxiv.org/abs/1512.00727
    title: "Gil Einziger, Roy Friedman and Ben Manes, TinyLFU: A Highly Efficient Cache Admission Policy, arXiv 1512.00727"
    locator: the section on W-TinyLFU
---

W-TinyLFU (Window TinyLFU) splits a cache of $c$ objects into a small [LRU](/lru/) window and a large main cache managed by [SLRU](/slru/). Every new object enters the window. When the window overflows, its LRU object becomes a candidate for the main cache, and the [TinyLFU](/tinylfu/) frequency filter compares it with the main cache's victim. The one with the higher estimated frequency stays. The window lets a new object collect hits during a short burst, and the filter protects the main cache from objects that are seldom requested.

## In plain words

Think of a shop with a small waiting room and a large hall. Every newcomer first sits in the waiting room. When the waiting room is full, the person who has waited longest must either move to the hall or leave. If the hall is full, a guard compares that person with the weakest person in the hall: the one who came more often lately gets the seat in the hall, and the other leaves.

The hall has two parts. People who came back at least once while in the hall sit in a protected part. Others sit in a probation part, and the weakest person is always taken from there.

## The problem

The model is the [paging problem](/paging-problem/) with a cache of $c$ objects. Plain TinyLFU in front of LRU admits a new object only when its count beats the victim's. On a trace with sparse bursts, where an object is requested several times close together and then not again for a long time, the object is rejected while its count is still low, so the burst gets no hits. Section 4 of the paper adds a window for this case. The goal is to keep the strong behavior of TinyLFU on skewed traces and to behave close to LRU on bursts.

## The algorithm

The window holds $w$ objects, by default 1% of $c$ and at least 1. The main cache holds $c - w$ objects as an SLRU: a protected segment of at most 80% of the main cache and a probation segment that holds the rest. The filter is the one of TinyLFU, with the doorkeeper, counters capped at $W/c$ and the reset after $W = 10c$ additions. Its RECORD and EST functions are on the TinyLFU page.

```pseudo id=main
W-TINYLFU-ACCESS(x)                     ▷ window LRU, main SLRU = probation + protected
L1  RECORD(x)
L2  if x is in the window then move x to the MRU end of the window and return hit
L3  if x is in protected then move x to the MRU end of protected and return hit
L4  if x is in probation then
L5      move x to the MRU end of protected
L6      if protected is over its limit then move its LRU object to the MRU end of probation
L7      return hit
L8  insert x at the MRU end of the window
L9  if the window has more than w objects then
L10     remove the LRU object u of the window
L11     if the main cache has fewer than c - w objects then insert u at the MRU end of probation
L12     else v ← the LRU object of probation
L13         if EST(u) > EST(v) then evict v and insert u at the MRU end of probation
L14         else evict u
L15 return miss
```

When the main cache is full, probation is not empty, because protected holds at most 80% of it. So line L12 always finds a victim.

Caffeine, the Java cache where W-TinyLFU is used, does not keep the window at 1%. It tunes the split between window and main cache at run time with a hill climbing search on the observed hit ratio. This page and its code use a fixed window.

## Example

Take $c = 4$ and $w = 1$. The main cache holds 3 objects and protected holds at most 2. The requests are A B A C A D A E B F B F G. The filter uses $W = 40$, so there is no reset in this run. A duel shows the window victim $u$, the probation victim $v$ and their estimates after RECORD.

| $t$ | request | result | duel $u$ vs $v$ | evicted | window | probation (LRU first) | protected (LRU first) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | miss | | | A | | |
| 2 | B | miss | | | B | A | |
| 3 | A | hit | | | B | | A |
| 4 | C | miss | | | C | B | A |
| 5 | A | hit | | | C | B | A |
| 6 | D | miss | | | D | B C | A |
| 7 | A | hit | | | D | B C | A |
| 8 | E | miss | D 1 vs B 1 | D | E | B C | A |
| 9 | B | hit | | | E | C | A B |
| 10 | F | miss | E 1 vs C 1 | E | F | C | A B |
| 11 | B | hit | | | F | C | A B |
| 12 | F | hit | | | F | C | A B |
| 13 | G | miss | F 2 vs C 1 | C | G | F | A B |

At $t = 8$ and $t = 10$ the tie keeps the old object. At $t = 9$, B gets a hit in probation and moves to protected. At $t = 12$, F hits while still in the window; this is the burst case that plain TinyLFU would miss. W-TinyLFU gets 6 hits on this trace. Plain LRU with 4 objects gets 5, because it evicts B at $t = 8$.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). It shows that the window never holds more than $w$ objects, that protected never holds more than its limit, that the three segments are disjoint and hold at most $c$ objects, that probation is never empty when line L12 runs, and that a window victim enters a full main cache exactly when its estimate beats the probation victim's.

## Complexity

With hash tables and linked lists for the three segments, every line except RECORD and EST takes $O(1)$ time. RECORD and EST take $O(d)$, and each request calls RECORD once and EST at most twice. A reset of the filter touches all $\Theta(c d)$ counters once per $W/2$ additions, which adds $O(c d / W) = O(d)$ amortized time per request when $W = 10c$. The space is $c$ cache entries plus $\Theta(c d)$ small counters and $\Theta(W)$ bits for the doorkeeper.

## Properties

- *Deterministic for fixed hash functions.* The code draws the hash salts from a seeded random number generator.
- *No worst-case guarantee.* The filter can turn away an object just before it is requested many times, so W-TinyLFU can do worse than LRU on some traces. Like any deterministic online paging policy, its [competitive ratio](/competitive-ratio/) is at least $c$, and the paper gives no bound.
- *Close to LRU for a large window.* With $w = c - 1$ and a main cache of one object, almost all decisions are made by the LRU window.
## Variants and improvements

- *Adaptive window.* Caffeine changes the window size with hill climbing, as noted above.
- *Other main caches.* The paper uses SLRU for the main cache. Any eviction policy that proposes a victim can sit behind the filter.
- *Plain [TinyLFU](/tinylfu/)* is the case with no window, where the filter guards the whole cache.

## When to use it

W-TinyLFU is a strong general choice for in-memory caches of objects of about the same size, where the workload mixes a skewed, stable popularity with bursts and with many objects requested once. It is the default policy of Caffeine. It needs a few bits per tracked key and $O(d)$ time per request, and it is harder to make concurrent than [CLOCK](/clock/)-like policies, since a hit changes linked lists.

A small seeded run made for this page uses Python `random.Random(1)`, $c = 100$ and 30000 requests per trace. Zipf has 1000 keys with exponent 0.8. Scan repeats 1000 uniform requests to 80 hot keys followed by 300 new keys. Loop cycles through 120 keys. Mix takes 60% Zipf, 20% the next key of a 120-key loop and 20% new keys.

| policy | Zipf | scan | loop | mix |
| --- | --- | --- | --- | --- |
| MIN | 62.4% | 76.7% | 82.9% | 39.3% |
| LRU | 37.5% | 70.7% | 0.0% | 16.7% |
| ARC | 45.6% | 76.7% | 0.0% | 28.0% |
| TinyLFU over LRU | 44.0% | 76.7% | 79.7% | 22.2% |
| W-TinyLFU | 48.1% | 76.7% | 78.9% | 28.6% |

These numbers come from small synthetic traces and say nothing about real workloads.

## Pitfalls

- *Rounding the window to zero.* For $c < 100$ the 1% window rounds to 0; the code uses at least one object.
- *Taking the victim from protected.* The main victim is the LRU object of probation, not of the whole main cache.
- *Forgetting to demote.* After a probation hit, protected may pass its limit; its LRU object must move back to probation, not leave the cache.
- *Recording only misses.* RECORD runs on every request, hits too, or popular objects in the cache lose their counts and then lose duels.
- *Ties.* The rule is strict. With "at least", objects seen once push out cached objects with the same estimate.

## Implementations

## History

Gil Einziger and Roy Friedman proposed TinyLFU in 2014. Working with Ben Manes on the Caffeine cache, they found that TinyLFU over LRU lost hits on traces with sparse bursts, and added the LRU window in front of an SLRU main cache. The journal paper of 2017 in ACM Transactions on Storage describes W-TinyLFU and its use in Caffeine. Caffeine later made the window size adaptive.

## References
