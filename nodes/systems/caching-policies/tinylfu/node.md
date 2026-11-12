---
tag: F0NQ2Y
kind: algorithm
slug: tinylfu
name: TinyLFU
area: systems/caching-policies
level: advanced
summary: An admission filter that counts recent requests in a small sketch and lets a new object replace the eviction victim only if it is estimated more frequent.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, c: the cache size in objects, d: the number of rows of the sketch, W: the sample size}
  time: {worst: O(n d + (n / W) c d), expected: O(n d)}
  space: {extra: Θ(c d)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2015
  people: [Gil Einziger, Roy Friedman, Ben Manes]
  note: Einziger and Friedman proposed TinyLFU in 2014, and the 2017 journal version with Ben Manes added the Caffeine integration and W-TinyLFU.
prereqs: [count-min-sketch, bloom-filter, cache-admission-policy, lfu]
see_also: [w-tinylfu, frequency-estimation, counting-bloom-filter, count-min-error-bound, lru, s3-fifo, arc, two-q]
sources:
  - paper: doi:10.1145/3149371
    title: "Gil Einziger, Roy Friedman and Ben Manes, TinyLFU: A Highly Efficient Cache Admission Policy, ACM Transactions on Storage 13(4), 2017"
    locator: Section 3.1 (architecture), Section 3.3 (the reset), Section 3.4.1 (counters capped at W/C), Section 3.4.2 (the doorkeeper), Section 3.6 (connecting to caches)
  - url: https://arxiv.org/abs/1512.00727
    title: "Gil Einziger, Roy Friedman and Ben Manes, TinyLFU: A Highly Efficient Cache Admission Policy, arXiv 1512.00727"
    locator: the same sections in the preprint
---

TinyLFU is a [cache admission policy](/cache-admission-policy/). It sits beside an ordinary cache, such as an [LRU](/lru/) cache, and counts how often each key was requested in a recent sample of $W$ requests. When the cache is full and a new object misses, the cache proposes a victim as usual, and TinyLFU admits the new object only if its estimated count is larger than the victim's. The counts live in a small [count-min sketch](/count-min-sketch/) with a [Bloom filter](/bloom-filter/) in front, so the memory per tracked key is a few bits.

## In plain words

A club has a fixed number of seats. When a newcomer arrives and the club is full, the usual rule picks a member to leave, for example the one who has sat longest without doing anything. TinyLFU adds a check at the door: it compares how often the newcomer and that member came in lately. The newcomer gets the seat only if they came more often. Otherwise the member stays and the newcomer is turned away.

To count visits cheaply, TinyLFU keeps rough tallies that may be a bit too high but never too low, and it halves every tally from time to time, so old visits count less than new ones.

## The problem

The model is the [paging problem](/paging-problem/) with a cache of $c$ objects. Under a skewed popularity, the best fixed content is the $c$ most popular objects, and [LFU](/lfu/) would keep them if it could count well. Exact counts for every key ever seen cost too much memory, and counts that never decay keep objects that were popular long ago. Eviction policies like LRU also let every new object in, so a flood of objects requested once pushes out popular ones. TinyLFU separates the two jobs: the eviction policy picks a victim, and a compact frequency filter decides if the swap is worth it.

## The algorithm

The filter has a count-min sketch of $d$ rows of counters, with the minimal increment rule (conservative update), a doorkeeper Bloom filter $D$, and a counter $n$ of additions. The sample size $W$ is a multiple of $c$; Caffeine 2.0 used $W = 10c$ (Section 5.1 of the paper), and so does this page. The cache below is LRU, as in the paper's tests with LRU.

```pseudo id=main
TINYLFU-ACCESS(x)                       ▷ LRU cache of c objects, filter with sample size W
L1  RECORD(x)
L2  if x is cached then
L3      move x to the MRU end and return hit
L4  if fewer than c objects are cached then
L5      insert x at the MRU end and return miss
L6  v ← the LRU object                  ▷ the victim the eviction policy proposes
L7  if EST(x) > EST(v) then
L8      evict v and insert x at the MRU end
L9  return miss                         ▷ otherwise x is not admitted

RECORD(x)
L10 if x ∉ D then insert x into D
L11 else raise by one each counter of x that equals the least of them, unless that least value is W/c
L12 n ← n + 1
L13 if n = W then RESET()

RESET()
L14 halve every counter and n, rounding down, and clear D

EST(x)
L15 return (the least counter of x) + (1 if x ∈ D else 0)
```

Three ideas keep the filter small and fresh.

- **Reset (Section 3.3).** After $W$ additions every counter is halved. This ages the counts without a sliding window. The paper proves that under a fixed distribution the expected count of an object with frequency $f$ settles at $f \cdot W$ just before each reset.
- **Small counters (Section 3.4.1).** Any object with frequency above $1/c$ deserves a place in the cache, so no counter needs to go above $W/c$. The paper notes that with $W = 8c$ and the doorkeeper, 3 bits per counter are enough.
- **Doorkeeper (Section 3.4.2).** The first request for a key in a sample only sets bits in $D$. Only later requests touch the sketch. Most keys in a skewed trace are seen once, so most never take a counter. A reset clears $D$ as well.

## Example

Take $c = 2$ and the requests A A B B C C C A D A C. The filter uses $W = 20$, so there is no reset, and in this run the estimates equal the true counts. The last column gives EST of the new object and of the victim, after RECORD.

| $t$ | request | result | victim | EST new vs victim | admitted | cache (LRU first) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | A | miss | | | | A |
| 2 | A | hit | | | | A |
| 3 | B | miss | | | | A B |
| 4 | B | hit | | | | A B |
| 5 | C | miss | A | 1 vs 2 | no | A B |
| 6 | C | miss | A | 2 vs 2 | no | A B |
| 7 | C | miss | A | 3 vs 2 | yes | B C |
| 8 | A | miss | B | 3 vs 2 | yes | C A |
| 9 | D | miss | C | 1 vs 3 | no | C A |
| 10 | A | hit | | | | C A |
| 11 | C | hit | | | | A C |

C has to be requested three times before it beats A, and D, seen once, never gets in. On this short trace plain LRU gets 5 hits and TinyLFU gets 4, because the filter is slow to admit C. The filter pays off on long skewed traces where most new objects are never requested again.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). It shows that the estimate is never below the count kept by an exact filter with the same doorkeeper, cap and reset rules, and so never below the true count in a sample while that count is at most $W/c$, that a counter never passes $W/c$, that a reset halves exactly and empties $D$, and that the cache keeps at most $c$ objects and admits a new object exactly when its estimate beats the victim's.

## Complexity

RECORD and EST hash the key $d$ times for the sketch and a few times for $D$, so they take $O(d)$ time. A request calls RECORD once and EST at most twice, plus $O(1)$ for the LRU cache with a [hash table](/hash-table/). A reset touches every counter, $O(c d)$ when each row has $\Theta(c)$ counters, once per $W/2$ requests after the first, so its amortized cost is $O(c d / W)$ per request, which is $O(d)$ when $W = \Theta(c)$. The sketch and $D$ take $\Theta(c d)$ small counters and $\Theta(W)$ bits.

## Properties

- *Deterministic for fixed hash functions.* The code draws the hash salts from a seeded random number generator, so a run is reproducible.
- *One-sided error.* Collisions in the sketch and false positives in $D$ can only raise an estimate. A rarely seen object may look more popular than it is, and win a duel it should lose.
- *No worst-case guarantee.* An admission filter can reject the object that is about to be requested many times, so TinyLFU over LRU can do worse than LRU, and like any deterministic online policy its [competitive ratio](/competitive-ratio/) is at least $c$. The paper gives no bound.
- *No ghost entries.* The sketch plays the role that [ghost lists](/ghost-lists/) play in [ARC](/arc/) or [2Q](/two-q/): it remembers keys that are not cached, but as counts, not as a list.

## Variants and improvements

- *[W-TinyLFU](/w-tinylfu/)* puts a small LRU window in front of the filtered main cache, so that bursts of requests to a new object can hit before the object has a high count. It is the version used in Caffeine.
- *Other eviction policies.* The paper also pairs TinyLFU with random eviction and with LFU; with LFU the cache counts must be halved together with the filter (Section 3.6).
- *Counting Bloom filter.* The paper's prototype uses a minimal increment [counting Bloom filter](/counting-bloom-filter/) instead of a count-min sketch. Both give estimates that never fall below the true count.

## When to use it

TinyLFU suits caches with skewed, fairly stable popularity, such as web objects, search results and database rows, especially when many objects are requested only once. It adds a few bits per tracked key and an $O(d)$ step per request. When the workload has bursts of requests to new objects, use W-TinyLFU instead.

A small seeded run made for this page uses Python `random.Random(1)`, $c = 100$ and 30000 requests per trace. Zipf has 1000 keys with exponent 0.8. Scan repeats 1000 uniform requests to 80 hot keys followed by 300 new keys. Loop cycles through 120 keys. Mix takes 60% Zipf, 20% the next key of a 120-key loop and 20% new keys.

| policy | Zipf | scan | loop | mix |
| --- | --- | --- | --- | --- |
| MIN | 62.4% | 76.7% | 82.9% | 39.3% |
| LRU | 37.5% | 70.7% | 0.0% | 16.7% |
| TinyLFU over LRU | 44.0% | 76.7% | 79.7% | 22.2% |
| W-TinyLFU | 48.1% | 76.7% | 78.9% | 28.6% |

On the loop of 120 keys, every key has the same count, the filter almost never admits a new key, and the cache keeps a fixed part of the loop.

## Pitfalls

- *Recording before the check.* RECORD runs on every request, hit or miss, before the duel. If misses are not recorded, a new object can never build a count.
- *Ties.* The rule is a strict "greater than". With "at least", a stream of objects seen once replaces cached objects with count 1.
- *Forgetting the doorkeeper in EST.* A key in $D$ has one more request than its counters show.
- *Resetting without clearing $D$.* The paper clears $D$ on every reset; otherwise $D$ fills up and every key looks seen.
- *Hash quality.* The bound of the count-min sketch assumes independent hash functions per row. Reusing one hash for all rows makes collisions repeat in every row.

## Implementations

## History

Gil Einziger and Roy Friedman proposed TinyLFU in 2014 as a frequency-based admission policy built on approximate counting. Ben Manes integrated it into the Caffeine Java cache, and the three authors published the journal version in ACM Transactions on Storage in 2017, together with W-TinyLFU, the doorkeeper and the counter cap. The arXiv preprint dates from 2015.

## References
