---
tag: 5D8W5S
kind: algorithm
slug: s3-fifo
name: S3-FIFO
aliases:
- S3-FIFO eviction
area: systems/caching-policies
level: research
summary: Three FIFO queues. A small queue filters out objects used once, a main queue keeps the rest with a capped counter, and a ghost queue recalls recent misses.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, c: the cache size in objects}
  time: {worst: O(n), expected: O(n)}
  space: {extra: Θ(c)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2023
  people: [Juncheng Yang, Yazhuo Zhang, Ziyue Qiu, Yao Yue, K. V. Rashmi]
  note: Yang, Zhang, Qiu, Yue and Rashmi presented S3-FIFO at ACM SOSP 2023, showing that static FIFO queues with quick demotion can beat LRU-based policies on web and storage traces.
prereqs: [fifo-replacement, ghost-lists, clock]
see_also: [sieve, two-q, arc, w-tinylfu, cache-admission-policy, lru, cache-replacement-policy, competitive-ratio]
sources:
  - paper: doi:10.1145/3600006.3613147
    title: "Juncheng Yang, Yazhuo Zhang, Ziyue Qiu, Yao Yue and K. V. Rashmi, FIFO Queues are All You Need for Cache Eviction, ACM SOSP 2023"
    locator: Section 3 (one-hit wonders in short sub-sequences), Section 4.1 and Algorithm 1 (the design), Section 4.2 (ring buffers and the ghost queue in the hash table)
---

S3-FIFO is a [cache replacement policy](/cache-replacement-policy/) built from three FIFO queues. A small queue $S$ takes new objects, a main queue $M$ holds objects that proved useful, and a ghost queue $G$ remembers the keys of objects recently dropped from $S$. Each cached object has a two-bit counter, capped at 3, that a hit raises. The point is quick demotion: most new objects are never used again, and $S$ removes them after a short trial, before they reach $M$.

## In plain words

A new object first waits in a small room near the door. If someone asks for it twice while it waits, it moves to the big room when its turn to leave comes. If not, it leaves, but its name goes on a short list. If the object comes back while its name is still on the list, it goes straight to the big room.

The big room also lets out the oldest object first. An object that was asked for since it came in gets another round instead, with its count lowered by one. Nothing is ever moved on a hit. A hit only raises a small counter, so hits are cheap and need no lock.

## The problem

The model is the [paging problem](/paging-problem/) with a cache of $c$ objects of equal size. S3-FIFO aims at web, key-value and storage caches with skewed popularity. The paper's observation (Section 3) is that in a short window of requests most objects appear only once, even when they appear more often over the whole trace. On 6594 production traces the median share of objects seen once is 26% over the whole trace and 72% over sub-sequences that contain 10% of the objects. A cache of size $c$ sees such short windows, so most objects it evicts were never hit. The goal is to evict these objects early while using only FIFO queues, which are cheap, scale to many threads and suit flash.

## The algorithm

$S$ gets a fraction $s$ of the cache and $M$ the rest. The paper uses $s = 10\%$: "We choose S to use 10% of the cache space based on experiments with 10 traces and find that 10% generalizes well" (Section 4.1). $G$ holds as many keys as $M$ holds objects. Each queue has a tail (oldest) and a head (newest). The pseudocode is Algorithm 1 of the paper.

```pseudo id=main
S3-FIFO-READ(x)                         ▷ queues S, M, G, cache size c, small fraction s
L1  if x ∈ S or x ∈ M then              ▷ cache hit
L2      x.freq ← min(x.freq + 1, 3) and return hit
L3  INSERT(x)                           ▷ cache miss
L4  x.freq ← 0 and return miss

INSERT(x)
L5  while |S| + |M| ≥ c do
L6      EVICT()
L7  if x ∈ G then
L8      remove x from G and insert x at the head of M
L9  else
L10     insert x at the head of S

EVICT()
L11 if |S| ≥ s · c then
L12     EVICT-S()
L13 else
L14     EVICT-M()

EVICT-S()
L15 while S is not empty do
L16     t ← remove the tail of S
L17     if t.freq > 1 then
L18         insert t at the head of M with t.freq ← 0
L19         if M is full then
L20             EVICT-M()
L21     else
L22         insert the key of t at the head of G, dropping the tail of G if G is full
L23         return

EVICT-M()
L24 while M is not empty do
L25     t ← the tail of M
L26     if t.freq > 0 then
L27         move t to the head of M with t.freq ← t.freq − 1
L28     else
L29         remove t from M and return
```

EVICT-S keeps moving useful objects from $S$ to $M$ until it drops one object from $S$ to $G$. EVICT-M works like [CLOCK](/clock/) with a counter in place of the bit: an object with a positive count goes back to the head with its count lowered by one, and the first object with count 0 leaves the cache. Objects evicted from $M$ do not enter $G$.

## Example

Take $c = 4$ with $s = 1/4$, so $S$ is evicted from whenever it holds at least one object, $M$ counts as full above 3 objects, and $G$ holds 3 keys. The queues are written from tail to head, each object with its counter.

| $t$ | request | result | evicted | $S$ | $M$ | $G$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | A | miss | | A0 | | |
| 2 | B | miss | | A0 B0 | | |
| 3 | A | hit | | A1 B0 | | |
| 4 | A | hit | | A2 B0 | | |
| 5 | C | miss | | A2 B0 C0 | | |
| 6 | D | miss | | A2 B0 C0 D0 | | |
| 7 | E | miss | B | C0 D0 E0 | A0 | B |
| 8 | F | miss | C | D0 E0 F0 | A0 | B C |
| 9 | B | miss | D | E0 F0 | A0 B0 | C D |
| 10 | G | miss | E | F0 G0 | A0 B0 | C D E |
| 11 | A | hit | | F0 G0 | A1 B0 | C D E |
| 12 | B | hit | | F0 G0 | A1 B1 | C D E |
| 13 | E | miss | F | G0 | A1 B1 E0 | D F |
| 14 | F | miss | G | | A1 B1 E0 F0 | D G |
| 15 | J | miss | E | J0 | F0 A0 B0 | D G |

While the cache is not full, $S$ grows past its share, since nothing needs to be evicted. At $t = 7$ the cache is full: EVICT-S moves A, with count 2, to $M$ and clears its count, then drops B to $G$. At $t = 9$, B was in $G$, so it enters $M$ directly. At $t = 13$ the key C falls off the tail of $G$ when F is added, and E, found in $G$, enters $M$. At $t = 15$, $S$ is empty, so EVICT-M runs: A and B go back to the head with their counts lowered to 0, and E, which was never hit in $M$, is evicted.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). It shows that EVICT-S and EVICT-M always stop, that the loop on line L5 stops after at most two calls of EVICT in a row that free nothing, that the cache never holds more than $c$ objects, that $S$, $M$ and $G$ are disjoint, that every counter stays between 0 and 3, that $G$ never holds more keys than its limit, and that the total work over $n$ requests is $O(n)$.

## Complexity

A hit takes $O(1)$ time and changes one counter. A miss takes $O(1)$ time plus the work of EVICT. Each step of EVICT-M that does not evict lowers a counter, and each move from $S$ to $M$ uses up a counter of at least 2. Counters only grow on hits, by one each time, so the total number of such steps over $n$ requests is at most $n$. Every other step evicts an object or moves one to $G$, and there are at most $n$ of those. So the total time is $O(n)$ with a [hash table](/hash-table/), and one miss can take $\Theta(c)$ steps. The extra space is $\Theta(c)$: the queues, two bits per object, and up to $(1 - s)\,c$ ghost keys. Section 4.2 of the paper keeps the ghost keys as 4-byte fingerprints with an insertion count inside the hash table, and the queues in ring buffers.

## Properties

- *Online and deterministic.* Each decision uses only the past requests.
- *No worst-case guarantee.* Like any deterministic online policy it can be forced to miss on every request while [MIN](/belady-optimal/) misses once per $c$ requests, so its [competitive ratio](/competitive-ratio/) is at least $c$. The paper proves no bound.
- *Static sizes.* The split between $S$ and $M$ never changes. In Section 6.2 the paper tries an adaptive version, S3-FIFO-d, and finds it better only on about 2% of the traces. It argues that adaptive schemes such as [ARC](/arc/) have parameters that are hard to tune and often overreact to small changes in the workload.
- *Scan resistance.* Objects of a scan pass through $S$ and $G$ and do not displace $M$. Popular objects mixed into a scan also go to $G$, but if they come back soon they enter $M$.
- *Not a stack algorithm.* A larger cache can get fewer hits. With the default $s = 10\%$, the requests A B C D A B E C E give 1 hit with $c = 2$ and none with $c = 3$. The sequence comes from a search over short strings, and the test file checks it.

## Variants and improvements

- *[SIEVE](/sieve/)*, by the same group, uses a single queue and no ghost, and is simpler but not scan resistant.
- *[2Q](/two-q/)* has the same three-part shape with LRU in place of FIFO for the main part, and moves objects to the main part only from the ghost list.
- *Ring buffers and one queue.* Section 4.2 notes that $S$ and $M$ can share one queue with a pointer at the 10% mark, at some cost in scalability.
- *Admission view.* $S$ acts as an [admission policy](/cache-admission-policy/) for $M$: an object enters $M$ only after a second request.

## When to use it

S3-FIFO suits large shared caches with skewed popularity, many threads, or flash storage, where LRU's list updates on every hit are costly. The paper reports lower miss ratios than state-of-the-art algorithms across 6594 traces from 14 datasets, the lowest mean miss ratio on 10 of the 14 datasets, and 6 times the throughput of an optimized LRU at 16 threads.

A small seeded run made for this page uses Python `random.Random(1)`, $c = 100$ and 30000 requests per trace. Zipf has 1000 keys with exponent 0.8. Scan repeats 1000 uniform requests to 80 hot keys followed by 300 new keys. Loop cycles through 120 keys. Mix takes 60% Zipf, 20% the next key of a 120-key loop and 20% new keys.

| policy | Zipf | scan | loop | mix |
| --- | --- | --- | --- | --- |
| MIN | 62.4% | 76.7% | 82.9% | 39.3% |
| LRU | 37.5% | 70.7% | 0.0% | 16.7% |
| ARC | 45.6% | 76.7% | 0.0% | 28.0% |
| S3-FIFO | 47.8% | 76.7% | 64.1% | 28.6% |

On the loop, objects that come back through $G$ fill $M$, so S3-FIFO keeps part of the loop where LRU and ARC keep nothing.

## Pitfalls

- *The move threshold.* The text of Section 4.1 says an object at the tail of $S$ moves to $M$ "if it is accessed more than once", while line 23 of Algorithm 1 tests `t.freq > 1`. A counter of 1 means one hit after insertion, so the two readings differ by one. This page and its code follow the pseudocode: $M$ needs two hits in $S$. The code takes the threshold as a parameter.
- *Clearing the counter on the move.* The text says the access bits are cleared when an object moves from $S$ to $M$. Algorithm 1 does not show this, so a version that keeps the counter gives a different policy. This page clears it.
- *When $M$ is full.* Algorithm 1 says "if M is full". This page reads it as "$M$ holds more than $(1 - s)\,c$ objects" after the move. The cache as a whole is still bounded by $c$ through the loop on line L5.
- *Ghost size.* $G$ holds as many keys as $M$ can hold objects. With small caches $(1 - s)\,c$ is not an integer, and this page rounds it up.
- *Order inside INSERT.* Line L5 evicts before line L7 checks $G$. An eviction can push the key of $x$ out of the tail of $G$ first, and then $x$ goes to $S$.
- *Evictions from $M$ do not enter $G$.* Only objects dropped from $S$ become ghosts.

## Implementations

## History

Juncheng Yang, Yazhuo Zhang, Ziyue Qiu, Yao Yue and K. V. Rashmi presented S3-FIFO at ACM SOSP 2023. It grew out of their study of one-hit wonders in production traces and their earlier argument that FIFO with lazy promotion and quick demotion can be as good as LRU. A year later the same group published [SIEVE](/sieve/), which keeps quick demotion with a single queue.

## References
