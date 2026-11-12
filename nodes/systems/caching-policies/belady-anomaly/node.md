---
tag: 8EZ63W
kind: concept
slug: belady-anomaly
name: Belady's anomaly
aliases:
- Bélády's anomaly
- FIFO anomaly
- Belady FIFO paging anomaly
area: systems/caching-policies
level: intro
summary: "With FIFO replacement, a larger cache can have more misses on the same trace: 1 2 3 4 1 2 5 1 2 3 4 5 gives 9 faults with 3 frames and 10 with 4."
prereqs: [cache-replacement-policy, cache-hit-ratio]
see_also: [fifo-replacement, inclusion-property, stack-algorithms, mattson-stack-algorithm, lru, clock, belady-optimal, page-fault]
sources:
  - paper: doi:10.1145/363011.363155
    title: "L. A. Belady, R. A. Nelson and G. S. Shedler, An anomaly in space-time characteristics of certain programs running in a paging machine, Communications of the ACM 12(6) (1969), 349-353"
    locator: the FIFO example in which more page frames give more page faults, and its discussion
  - paper: doi:10.1147/sj.92.0078
    title: "R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2) (1970), 78-117"
    locator: stack algorithms, which have the inclusion property and so cannot show the anomaly; FIFO is not one
  - url: "https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys-policy.pdf"
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces, Chapter 22, Beyond Physical Memory, Policies
    locator: Section 22.4, the aside on Belady's anomaly
---

Belady's anomaly is the fact that some replacement policies, FIFO first among them, can have more misses with a larger cache on the same request sequence. Belady, Nelson and Shedler showed it in 1969 with the trace $1\,2\,3\,4\,1\,2\,5\,1\,2\,3\,4\,5$: FIFO has 9 page faults with 3 frames and 10 with 4. The anomaly cannot happen for a *stack algorithm*, such as LRU or Belady's MIN, because there the content of the smaller cache is always part of the content of the larger one. This is the [inclusion property](/inclusion-property/), and the anomaly is the simplest sign that a policy lacks it.

## In plain words

You would expect more memory to help, or at least not to hurt. For most good policies that is true. But FIFO, which always throws out the item that came in first, can do worse with more room.

The reason is that a cache with more room does not simply hold everything the small cache holds and more. With FIFO, the two caches load items at different times, so their queues are in different orders, and at some moment the large cache has thrown out an item that the small cache still holds. If the program asks for that item next, the small cache hits and the large cache misses. On the right trace, this happens often enough that the large cache loses overall.

## The idea

**The classic trace.** Run FIFO on $1\,2\,3\,4\,1\,2\,5\,1\,2\,3\,4\,5$ with 3 and with 4 frames. Each queue is listed oldest first.

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| request | 1 | 2 | 3 | 4 | 1 | 2 | 5 | 1 | 2 | 3 | 4 | 5 |
| 3 frames | F | F | F | F | F | F | F | | | F | F | |
| queue | 1 | 12 | 123 | 234 | 341 | 412 | 125 | 125 | 125 | 253 | 534 | 534 |
| 4 frames | F | F | F | F | | | F | F | F | F | F | F |
| queue | 1 | 12 | 123 | 1234 | 1234 | 1234 | 2345 | 3451 | 4512 | 5123 | 1234 | 2345 |

With 3 frames there are 9 faults; with 4 frames there are 10. The two runs part at $t = 7$. The small cache faulted on 1 and 2 at $t = 5$ and $t = 6$, so 1 and 2 are young in its queue, and at $t = 7$ it evicts 4. The large cache hit on 1 and 2, which does not change a FIFO queue, so 1 is still its oldest item, and it evicts 1. Now the small cache $\{1, 2, 5\}$ is not a subset of the large cache $\{2, 3, 4, 5\}$. The next requests, 1 and 2, hit in the small cache and miss in the large one, and each miss of the large cache evicts the item that is needed next.

**Why stack algorithms are safe.** Suppose a policy has the inclusion property: for each trace and each time, the cache of size $k$ is a subset of the cache of size $k + 1$. Then each hit of the small cache is a hit of the large cache, so the misses never rise with $k$. Mattson, Gecsei, Slutz and Traiger (1970) called such policies stack algorithms and showed that a policy is one when it ranks the items by a priority that does not depend on the cache size. LRU ranks by the time of the last use, MIN by the time of the next use, and an LFU that counts all past uses, also of evicted items, by that count. FIFO ranks by the time of the *load*, and the load times depend on the cache size, because the two caches miss at different times. See the [Mattson stack algorithm](/mattson-stack-algorithm/) and [stack algorithms](/stack-algorithms/).

**Size of the effect.** The anomaly is rare on real traces, and the difference is usually small. It also needs a trace of some length. By exhaustive search, FIFO has no anomaly on any trace of at most 7 requests over 4 pages, or of at most 9 requests over 5 pages. So the classic example, with 12 requests over 5 pages, is not far from the shortest.

## Examples

**FIFO.** The trace above, with faults $12, 12, 9, 10, 5$ for 1 to 5 frames.

**LRU, a non-example.** On the same trace, LRU has $12, 12, 10, 8, 5$ faults, and MIN has $12, 9, 7, 6, 5$. Both lists never rise. LRU is a stack algorithm: the cache of size $k$ is always the $k$ most recently used items, which lie in the $k + 1$ most recently used items.

**CLOCK, a variant that shows it.** [CLOCK](/clock/) is a cheap form of LRU with one reference bit per frame, and it is not a stack algorithm. In the form that sets the bit on a hit but not on a load, the trace $1\,1\,2\,2\,3\,4\,3$ gives 4 faults with 2 frames and 5 with 3 frames. With 3 frames, the hand clears the bits of 1 and 2 and then evicts 3 to load 4, so the last request for 3 misses. With 2 frames, the hand evicts 1 and then 2, and 3 stays. The more common form, which also sets the bit on a load, showed no anomaly in a search over all traces of at most 9 requests over 4 pages; that does not prove that it has none.
## Where it is used

- **Choosing a policy.** The anomaly is a standard argument for stack algorithms in operating systems. A policy without inclusion can surprise an administrator who adds memory and sees more faults.
- **One-pass simulation.** Only stack algorithms allow the [Mattson stack algorithm](/mattson-stack-algorithm/) to compute the misses of every cache size in one pass. For FIFO, CLOCK and most adaptive policies, each size needs its own simulation, and the [miss ratio curve](/miss-ratio-curve/) need not fall.
- **Multilevel caches.** The same question, whether a smaller cache's content lies inside a larger one's, decides whether a [multilevel cache](/multilevel-caching/) can keep inclusion without extra invalidations.
- **Teaching.** The trace of Belady, Nelson and Shedler is the usual first example that more resources need not help a heuristic.

## References
