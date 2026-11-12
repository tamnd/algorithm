---
tag: JP6T1M
kind: algorithm
slug: sieve
name: SIEVE eviction
aliases:
- SIEVE
area: systems/caching-policies
level: research
summary: One FIFO queue with a visited bit per object and a hand that moves from old to new. Survivors keep their place, so new objects are examined first.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, c: the cache size in objects}
  time: {worst: O(n), expected: O(n)}
  space: {extra: Θ(c)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2024
  people: [Yazhuo Zhang, Juncheng Yang, Yao Yue, Ymir Vigfusson, K. V. Rashmi]
  note: Zhang, Yang, Yue, Vigfusson and Rashmi presented SIEVE at USENIX NSDI 2024 as an eviction algorithm for web caches that is simpler than LRU.
prereqs: [fifo-replacement, clock]
see_also: [s3-fifo, clock, lru, arc, ghost-lists, w-tinylfu, cache-replacement-policy, competitive-ratio]
sources:
  - url: https://www.usenix.org/conference/nsdi24/presentation/zhang-yazhuo
    title: "Yazhuo Zhang, Juncheng Yang, Yao Yue, Ymir Vigfusson and K. V. Rashmi, SIEVE is Simpler than LRU: an Efficient Turn-Key Eviction Algorithm for Web Caches, USENIX NSDI 2024"
    locator: Section 3.1 and Algorithm 1 (the design), Section 3.2 (implementations in five libraries), Section 7.2 (SIEVE is not scan-resistant)
---

SIEVE is a [cache replacement policy](/cache-replacement-policy/) that keeps the cached objects in one FIFO queue in the order they were inserted, with one visited bit per object. A hit only sets the bit. A hand moves through the queue from the oldest object toward the newest, clears the bits it passes, and evicts the first object whose bit is clear. Unlike [CLOCK](/clock/), SIEVE never moves an object that survives: it keeps its place, and new objects go to the head.

## In plain words

Think of a queue of people waiting for a free seat. The oldest person is at the back and new people join at the front. A guard walks from the back toward the front. Each person who has done something useful since the guard last passed gets a pass and stays where they are. The first person who has done nothing is sent away.

The guard remembers where he stopped. Next time he starts there, so he soon reaches the people who joined recently. If one of them has not been useful yet, he sends that person away. People who proved useful long ago sit behind him and are safe until he comes round again. So new objects get a short trial, and old useful objects stay.

## The problem

The model is the [paging problem](/paging-problem/) with a cache of $c$ objects of equal size. SIEVE aims at web caches, where most objects are requested once or a few times and the popular ones change slowly. The goal is a hit ratio at least as good as [LRU](/lru/) with less work on a hit: no list update and no lock, only one bit to set. The paper reports twice the throughput of an optimized LRU with 16 threads in its Cachelib prototype.

## The algorithm

$T$ is a queue kept as a [doubly linked list](/doubly-linked-list/). Its tail is the oldest object and its head the newest. For an object $o$, $o.\mathit{prev}$ is the next newer object, toward the head. The hand $p$ is a pointer into $T$ or NULL. The pseudocode is Algorithm 1 of the paper.

```pseudo id=main
SIEVE-ACCESS(x)                         ▷ queue T, hand p, cache size c
L1  if x ∈ T then                       ▷ cache hit
L2      x.visited ← 1 and return hit
L3  else                                ▷ cache miss
L4      if |T| = c then                 ▷ the cache is full
L5          o ← p
L6          if o = NULL then
L7              o ← the tail of T
L8          while o.visited = 1 do
L9              o.visited ← 0
L10             o ← o.prev              ▷ one step toward the head
L11             if o = NULL then
L12                 o ← the tail of T
L13         p ← o.prev
L14         discard o from T
L15     insert x at the head of T
L16     x.visited ← 0 and return miss
```

Lines L11 and L12 wrap the hand from the head back to the tail. Line L13 leaves the hand on the object just newer than the evicted one, so the next search starts there.

**How SIEVE differs from CLOCK.** CLOCK, Second Chance and FIFO with reinsertion are the same algorithm. When the hand finds an object with its bit set, it clears the bit and moves the object to the head of the queue. SIEVE clears the bit and leaves the object where it is. So in CLOCK a survivor is treated like a new object, while in SIEVE the survivors gather behind the hand and the new objects in front of it, near the head, are examined first. The paper calls these two effects lazy promotion (a hit costs only a bit) and quick demotion (a new object that is not used again leaves soon).

## Example

Take $c = 3$ and the requests D C A D B E C D. The queue is written from tail to head, a star marks a set bit, and a caret marks the object under the hand. The last two columns run CLOCK, as FIFO with reinsertion, on the same requests.

| $t$ | request | SIEVE | SIEVE evicts | SIEVE queue | CLOCK | CLOCK evicts | CLOCK queue |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | D | miss | | D | miss | | D |
| 2 | C | miss | | D C | miss | | D C |
| 3 | A | miss | | D C A | miss | | D C A |
| 4 | D | hit | | D* C A | hit | | D* C A |
| 5 | B | miss | C | D A^ B | miss | C | A D B |
| 6 | E | miss | A | D B^ E | miss | A | D B E |
| 7 | C | miss | B | D E^ C | miss | D | B E C |
| 8 | D | hit | | D* E^ C | miss | B | E C D |

At $t = 5$ both policies clear the bit of D and evict C. CLOCK moves D to the head, behind the new objects A and B. SIEVE leaves D at the tail and the hand moves on to A. At $t = 6$ and $t = 7$ SIEVE evicts the new objects A and B, which were not used again, while CLOCK reaches D at $t = 7$ and evicts it. So SIEVE hits on D at $t = 8$ and CLOCK misses: 2 hits against 1. The test file checks every row of this table.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). It shows that the loop on lines L8 to L12 stops after at most $|T|$ steps, that the hand is always NULL or an object of $T$, that the cache never holds more than $c$ objects and the queue always lists the cached objects in the order they were inserted, and that a request is a hit exactly when its object is cached.

## Complexity

A hit takes $O(1)$ time and writes one bit. A miss takes $O(1)$ time plus the steps of the loop. Each step of the loop clears a bit, and only a hit sets a bit, so over $n$ requests the loop runs at most $n$ times in total. One miss can still take $\Theta(c)$ steps when every bit is set. With a [hash table](/hash-table/) from keys to list nodes the total time is $O(n)$, and the extra space is $\Theta(c)$: two pointers and one bit per object, plus the hand.

## Properties

- *Online and deterministic.* Each decision uses only the past requests.
- *No worst-case guarantee beyond the trivial one.* Like any deterministic online policy it can be forced to miss on every request while [MIN](/belady-optimal/) misses only once per $c$ requests, so its [competitive ratio](/competitive-ratio/) is at least $c$. The paper proves no bound, so SIEVE has no worst-case guarantee better than this.
- *No ghost entries.* SIEVE forgets an object as soon as it is evicted. An object that comes back is new again.
- *Not scan resistant.* Section 7.2 of the paper reports that on some block cache traces SIEVE misses more than LRU. When popular objects arrive mixed with a scan, they are new objects among new objects, and they can be evicted before their second request.
- *Not a stack algorithm.* A larger cache can get fewer hits, as in [Belady's anomaly](/belady-anomaly/). On A A B B C D C, SIEVE gets 3 hits with $c = 2$ and 2 hits with $c = 3$. With $c = 3$ the hand passes A and B and evicts the new object C, which comes back at once. The sequence comes from a search over short strings, and the test file checks it.

## Variants and improvements

- *CLOCK and FIFO with reinsertion* are the same idea with the survivor moved to the head. See [CLOCK](/clock/).
- *[S3-FIFO](/s3-fifo/)*, by the same group, adds a small probation queue and a [ghost list](/ghost-lists/), which makes it scan resistant at the cost of three queues.
- *SIEVE as a building block.* Section 6.2 of the paper replaces the LRU lists inside LeCaR, [2Q](/two-q/) and ARC (for ARC, only the list of frequent pages) with SIEVE, and reports lower miss ratios for all three.

## When to use it

SIEVE suits web and key-value caches where most new objects are never reused and the popular ones stay popular. It is a small change to a cache that already uses a linked list for LRU: the paper reports that it changed five open source libraries (Cachelib, groupcache, mnemonist, lru-dict and lru-rs) with fewer than 20 lines each on average. Avoid it for block or page caches with scans and loops, where a policy with ghost entries such as [ARC](/arc/) or [LIRS](/lirs/) does better.

A small seeded run made for this page shows both sides. It uses Python `random.Random(1)`, $c = 100$ and 30000 requests per trace. Zipf has 1000 keys with exponent 0.8. Scan repeats 1000 uniform requests to 80 hot keys followed by 300 new keys. Loop cycles through 120 keys. Mix takes 60% Zipf, 20% the next key of a 120-key loop and 20% new keys.

| policy | Zipf | scan | loop | mix |
| --- | --- | --- | --- | --- |
| MIN | 62.4% | 76.7% | 82.9% | 39.3% |
| LRU | 37.5% | 70.7% | 0.0% | 16.7% |
| CLOCK-Pro | 46.8% | 76.6% | 80.7% | 28.6% |
| SIEVE | 48.1% | 76.7% | 0.0% | 28.2% |

On a loop longer than the cache, SIEVE gets no hits, the same as LRU.

## Pitfalls

- *Direction of the hand.* The hand moves from the tail toward the head, and the hand stays where it stopped. Restarting it at the tail on every miss gives a different policy.
- *Inserting at the hand.* New objects go to the head, not to the slot of the evicted object. Putting them at the hand gives CLOCK back.
- *Removing the object under the hand.* If an object is deleted by the application, the hand must move to its newer neighbour first, or it points to a freed node.
- *Expecting scan resistance.* SIEVE has no memory of evicted objects. Add a ghost list, or use S3-FIFO, if the workload has scans.

## Implementations

## History

Yazhuo Zhang, Juncheng Yang, Yao Yue, Ymir Vigfusson and K. V. Rashmi presented SIEVE at USENIX NSDI 2024. The paper notes how close the algorithm is to CLOCK, which dates from the late 1960s, and suggests that it stayed unnoticed because caching research focused on page and block workloads with scans, where SIEVE is weak. The same authors had shown a year earlier, in S3-FIFO, that FIFO queues with quick demotion can beat LRU on web traces.

## References
