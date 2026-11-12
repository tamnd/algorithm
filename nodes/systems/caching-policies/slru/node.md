---
tag: 1K8PDH
kind: algorithm
slug: slru
name: Segmented LRU (SLRU)
aliases:
- SLRU
- segmented LRU
area: systems/caching-policies
level: advanced
summary: LRU split into a probationary segment for new pages and a protected segment for pages hit at least once. Victims come from the probationary segment only.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size in pages}
  time: {expected: O(n)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1994
  people: [Ramakrishna Karedla, J. Spencer Love, Bradley G. Wherry]
  note: Karedla, Love and Wherry described SLRU in IEEE Computer in 1994 as a policy for disk caches in storage controllers.
prereqs: [lru]
see_also: [two-q, lru-k, arc, w-tinylfu, tinylfu, s3-fifo, lru, cache-replacement-policy]
sources:
  - paper: doi:10.1109/2.268884
    title: "Ramakrishna Karedla, J. Spencer Love and Bradley G. Wherry, Caching strategies to improve disk system performance, Computer 27(3), 1994, 38-46"
    locator: the segmented LRU policy with a probationary and a protected segment, and its comparison with LRU on disk cache traces
  - paper: "Theodore Johnson and Dennis Shasha, 2Q, a low overhead high performance buffer management replacement algorithm, Proceedings of the 20th International Conference on Very Large Data Bases (VLDB), 1994, 439-450"
    title: 2Q, a low overhead high performance buffer management replacement algorithm
    locator: the simplified 2Q, a close relative of SLRU with a FIFO first queue
  - paper: doi:10.1145/3149371
    title: "Gil Einziger, Roy Friedman and Ben Manes, TinyLFU, a highly efficient cache admission policy, ACM Transactions on Storage 13(4), 2017, article 35"
    locator: W-TinyLFU, whose main cache is an SLRU with 80% of the space in the protected segment
---

Segmented LRU (SLRU) is a [cache replacement policy](/cache-replacement-policy/) by Karedla, Love and Wherry (1994). It splits an [LRU](/lru/) list into two segments. A page that is not in the cache enters the **probationary segment**. A page that is hit moves to the **protected segment**, which holds at most $p$ pages. When the protected segment is too full, its least recently used page drops back to the most recently used end of the probationary segment. Victims always come from the least recently used end of the probationary segment. So a page used only once leaves before a page used twice, and a long scan of new pages never reaches the protected pages. The cost per request is $O(1)$, as for LRU.

## In plain words

Think of a club with a waiting room and a members' room. A new guest sits in the waiting room. If the guest comes back while still there, the guest becomes a member and goes to the members' room.

When the waiting room is full and a new guest arrives, the guest who has waited longest without a visit has to leave. Members never leave straight from the members' room. If that room is full, the member who has not visited for the longest time goes back to the front of the waiting room, and has one more chance there.

A crowd of one-time guests only fills the waiting room. The members stay.

## The problem

The model is the [paging problem](/paging-problem/): a cache of $k$ pages of equal size, a request sequence $\sigma$ of length $n$, an empty cache at the start, and the number of misses as the cost. SLRU is online and deterministic. Karedla, Love and Wherry wanted a policy for the disk cache of a storage controller that keeps pages used more than once, and that does not lose them to sequential reads, with no more cost than LRU.

## The algorithm

SLRU has one parameter, the size $p$ of the protected segment, with $0 \le p < k$. Both segments are LRU lists. The probationary segment can hold up to $k$ pages, less the pages of the protected segment.

```pseudo id=main
SLRU-ACCESS(x)                      ▷ PROB, PROT: LRU lists, |PROT| ≤ p
L1  if x ∈ PROT then
L2      move x to the MRU end of PROT; return hit
L3  if x ∈ PROB then
L4      remove x from PROB; add x to the MRU end of PROT
L5      if |PROT| > p then
L6          move the LRU page of PROT to the MRU end of PROB
L7      return hit
L8  if |PROB| + |PROT| = k then
L9      evict the LRU page of PROB
L10 add x to the MRU end of PROB
L11 return miss
```

A page that drops back at line L6 is not evicted. It goes to the safe end of the probationary segment, and a hit there moves it up again. Karedla, Love and Wherry used a fixed split, and the best split depends on the workload. Later caches often give the protected segment about $80\%$ of the space.

## Example

Run SLRU with $k = 4$ and $p = 2$ on $a, b, a, b, c, d, e, f, a, b$. Each segment is written from its MRU end to its LRU end.

| $t$ | request | result | evicted | probationary | protected |
| --- | --- | --- | --- | --- | --- |
| 1 | a | miss | | a | |
| 2 | b | miss | | b a | |
| 3 | a | hit | | b | a |
| 4 | b | hit | | | b a |
| 5 | c | miss | | c | b a |
| 6 | d | miss | | d c | b a |
| 7 | e | miss | c | e d | b a |
| 8 | f | miss | d | f e | b a |
| 9 | a | hit | | f e | a b |
| 10 | b | hit | | f e | b a |

The four new pages $c, d, e, f$ evict each other inside the probationary segment, and $a$ and $b$ survive. SLRU has 6 misses. LRU evicts $a$ at $t = 7$ and $b$ at $t = 8$, and has 8 misses.

## Correctness

After each request the two segments are disjoint, the protected segment holds at most $p$ pages, at most $k$ pages are resident, and the requested page is resident. When the cache is full at line L8, the probationary segment holds at least $k - p \ge 1$ pages, so line L9 always has a page to evict. With $p = 0$, a hit at line L4 moves the page into the protected segment and line L6 moves it at once to the MRU end of the probationary segment, so SLRU is LRU. The proofs are below.

## Complexity

- **Time.** Each segment is a hash map from page identifiers to the nodes of a [doubly linked list](/doubly-linked-list/). Each line is $O(1)$ expected, so a sequence of $n$ requests takes $O(n)$ expected time.
- **Space.** $\Theta(k)$: one list node and one map entry for each resident page, and a flag or a second map that tells the segment.
- **Hit ratio.** On the disk traces of Karedla, Love and Wherry, SLRU gave higher hit ratios than LRU at the same cache size.
- **Worst case.** SLRU with $p \ge 1$ is not competitive. Pages that were hit once and then never used again can hold the protected segment, while new pages fight for the $k - p$ probationary slots. With $k = 2$ and $p = 1$, the sequence $a, a, (x, y)^m$ costs SLRU $1 + 2m$ misses and the optimal [Belady MIN](/belady-optimal/) only 3.

## Properties

- **Scan resistant.** A scan of new pages only evicts probationary pages. A protected page leaves the protected segment only when a hit promotes another page.
- **Two levels of use.** SLRU sees only two classes: pages seen once and pages hit at least once since they entered. It does not count further.
- **Second chance for demoted pages.** A page that drops out of the protected segment enters the probationary segment at the MRU end, so it is the last probationary page to be evicted.
- **Not a stack algorithm.** With a fixed $p \ge 1$, the contents with $k$ pages need not be a subset of the contents with $k + 1$ pages, and a larger cache can miss more, as in [Belady's anomaly](/belady-anomaly/). With $k \in \{2, 3\}$, $p = 1$ and the requests $2, 4, 6, 6, 2, 0, 3, 6, 5, 0, 4, 6, 1$, SLRU has 10 misses with 2 pages and 11 with 3 pages. With $p = 0$, SLRU is LRU, which is a stack algorithm.

## Variants and improvements

- **More segments.** Karedla, Love and Wherry note that the idea extends to more than two segments. A hit moves a page one segment up, and the overflow of each segment drops one segment down. [MQ](/mq-cache/) is a related policy with $m$ LRU queues chosen by frequency.
- **Simplified 2Q.** The simplified [2Q](/two-q/) is SLRU with a FIFO first queue. The full 2Q adds a ghost queue and does not promote on a correlated second request.
- **W-TinyLFU.** [W-TinyLFU](/w-tinylfu/) puts an SLRU behind a small LRU window and a [TinyLFU](/tinylfu/) admission filter. This is the policy of the Caffeine library for Java.
- **ARC.** [ARC](/arc/) also has a list for pages seen once and a list for pages seen at least twice, but it moves the split between them by itself with two ghost lists.

## When to use it

Use SLRU when a workload mixes a set of pages that are used many times with long runs of pages that are used once, and when the cost per request must stay that of LRU. Disk caches in storage controllers, database buffers and the main area of W-TinyLFU are common uses. Prefer [ARC](/arc/) when the mix of recency and frequency changes and no one can tune $p$. Prefer LRU or [FIFO](/fifo-replacement/) when a worst-case bound on misses matters.

## Pitfalls

- **$p = k$.** Then a full protected segment leaves no probationary page to evict at line L9. Keep $p < k$.
- **Evicting the demoted page.** The page that drops out of the protected segment at line L6 must go to the MRU end of the probationary segment. If it goes to the LRU end, or out of the cache, the policy loses its second chance and is no longer the SLRU of the paper.
- **Promoting on a miss.** Only a hit promotes. A miss always enters the probationary segment, even for a page that was protected before it was evicted.
- **Too large a protected segment.** With $p$ close to $k$, a working set of new pages larger than $k - p$ misses on every request, even if it fits in $k$ pages.

## Implementations

## History

Karedla, Love and Wherry described segmented LRU in IEEE Computer in 1994, in a study of caching for disk systems. In the same year Johnson and Shasha published 2Q, whose simplified version is close to SLRU with a FIFO first queue. SLRU later became a part of other policies. W-TinyLFU by Einziger, Friedman and Manes uses an SLRU as its main cache, and the Caffeine cache library for Java uses W-TinyLFU.

## References
