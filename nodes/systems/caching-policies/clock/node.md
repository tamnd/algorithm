---
tag: Z35MNC
kind: algorithm
slug: clock
name: CLOCK algorithm
aliases:
- CLOCK
- CLOCK (second chance) replacement
- clock replacement
- second chance
area: systems/caching-policies
level: core
summary: A circle of frames with one reference bit each. The hand skips and clears pages whose bit is set and evicts the first clear one. It approximates LRU at FIFO cost.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size in pages}
  time: {worst: O(n k), amortized: O(n)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1968
  people: [Fernando J. Corbató]
  note: Corbató described the clock-like scan of a used bit for the Multics paging system in a 1968 Project MAC report, published in 1969.
prereqs: [fifo-replacement, lru]
see_also: [lru, fifo-replacement, clock-pro, car, sieve, s3-fifo, belady-anomaly, working-set-model]
sources:
  - paper: "F. J. Corbató, A paging experiment with the Multics system, MIT Project MAC report MAC-M-384, 1968; also in H. Feshbach and K. U. Ingard (eds.), In Honor of Philip M. Morse, MIT Press, 1969, 217-228"
    title: A paging experiment with the Multics system
    locator: the replacement rule of Multics, a pointer that cycles over the page frames and clears the used bits
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 10, Section 10.4.5 (LRU approximation page replacement, the second chance algorithm)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 3, Sections 3.4.4 and 3.4.5 (the second chance and the clock page replacement algorithms)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces
    locator: Chapter 22, Beyond Physical Memory, Policies (approximating LRU with a use bit and a clock hand)
  - paper: "Richard W. Carr and John L. Hennessy, WSCLOCK, a simple and effective algorithm for virtual memory management, Proceedings of the 8th ACM Symposium on Operating Systems Principles (1981), 87-95"
    title: WSCLOCK, a simple and effective algorithm for virtual memory management
    locator: the clock scan combined with the working set rule
---

CLOCK, also called second chance, is the [cache replacement policy](/cache-replacement-policy/) that keeps the cached pages in a circle of $k$ frames, with one reference bit per frame and a hand that points at a frame. Each request to a page sets its bit. On a miss with a full cache, the hand moves around the circle: it clears each set bit it meets, and it evicts the first page whose bit is already clear. So a page that was used since the hand last passed it gets a second chance. CLOCK approximates [LRU](/lru/) with one bit per page, and it is [FIFO](/fifo-replacement/) when no page is used again inside the window.

## In plain words

Picture the cached pages on the face of a clock, with one hand. Each page has a small flag. When a page is used, its flag goes up. When room is needed, the hand looks at the page it points to. If the flag is up, the hand puts it down and moves on: the page stays for one more round. If the flag is down, that page goes, and the new page takes its place.

A page that is used often has its flag up each time the hand comes, so it stays. A page that nobody used since the last round goes. The hardware only has to set a flag on each use, which is much cheaper than moving the page to the front of a list as LRU does.

## The problem

The model is the [paging problem](/paging-problem/): a cache of $k$ pages of equal size, a request sequence $\sigma$ of length $n$, an empty cache at the start, and the number of misses as the cost. CLOCK is online and deterministic. In a virtual memory system, the hardware sets the reference bit at each access, and the operating system runs the hand only at a page fault.

## The algorithm

```pseudo id=main
CLOCK-ACCESS(p)                  ▷ frames F[0..k-1], bits R[0..k-1], hand h
L1  if p is in some frame i then
L2      R[i] ← 1                            ▷ hit: mark the page as used
L3      return hit
L4  if fewer than k frames are in use then
L5      put p in the next free frame with R = 1
L6      return miss
L7  while R[h] = 1 do                       ▷ second chance
L8      R[h] ← 0
L9      h ← (h + 1) mod k
L10 evict the page in F[h]
L11 F[h] ← p; R[h] ← 1                      ▷ the faulting access sets the bit
L12 h ← (h + 1) mod k
L13 return miss
```

A hash map from page to frame answers line L1. The frames fill in order $0, 1, \ldots, k - 1$, so when the cache becomes full the hand is at frame 0, the oldest load. After each eviction the hand moves one step past the new page, so the order of the frames from the hand onward is the load order, as in a FIFO queue. The loop of lines L7 to L9 ends within one full turn, because it clears every bit it passes.

Some texts and caches load a page with a clear bit. That variant is not $k$-competitive; see the pitfalls.

## Example

Run CLOCK with $k = 3$ on $\sigma = a, b, a, c, d, a$. A star marks a set bit; the frames are listed from frame 0.

| $t$ | request | result | evicted | frames after | hand after |
| --- | --- | --- | --- | --- | --- |
| 1 | a | miss | | a* | 0 |
| 2 | b | miss | | a* b* | 0 |
| 3 | a | hit | | a* b* | 0 |
| 4 | c | miss | | a* b* c* | 0 |
| 5 | d | miss | a | d* b c | 1 |
| 6 | a | miss | b | d* a* c | 2 |

At $t = 5$ all three bits are set, so the hand clears them all in one turn, comes back to frame 0 and evicts the oldest load $a$, as FIFO does. LRU knows that $a$ was used at $t = 3$, after $b$, so it evicts $b$ and hits on $a$ at $t = 6$: LRU has 4 misses and CLOCK has 5. On $a, b, a, c, d, b$ the roles change, and CLOCK has 4 misses against 5 for LRU. One bit cannot record the order of the uses, only that a use happened since the last pass.

On the textbook string $7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1$ with $k = 3$, CLOCK has 14 misses, between FIFO with 15 and LRU with 12. The offline optimum [MIN](/belady-optimal/) has 9.

## Correctness

The invariant is: the frames hold the cached pages, one each, $|C| \le k$, and the requested page is cached after each request. A hit only sets a bit. A miss with a free frame fills it. A miss with a full cache stops the loop of lines L7 to L9 at a frame with a clear bit, which exists after at most one turn, evicts that one page and puts the new page in its frame. Two facts tie CLOCK to FIFO and LRU:

- If every bit is set or every bit is clear at a miss, the hand evicts the page at the hand, which is the oldest load. If no page is requested again while it is cached, there are no hits, and CLOCK evicts exactly as FIFO does.
- A page is evicted only if it was not requested since the hand last cleared its bit. So a page in steady use stays, as in LRU.

CLOCK is conservative: in any part of $\sigma$ with at most $k$ distinct pages, it has at most $k$ misses. With the phase count of the [FIFO](/fifo-replacement/) page, this gives $\mathrm{CLOCK}_k(\sigma) \le k \cdot \mathrm{MIN}_k(\sigma)$. The proof is below.

## Complexity

- **Time.** A hit is $O(1)$ expected: a hash lookup and one bit write. A miss moves the hand at most $k$ steps, so it is $O(k)$ in the worst case. Each step of the hand except the last clears a bit, and each bit is set by at most one request before it is cleared, so the total number of steps is at most $2n$: $O(n)$ amortized in total.
- **Space.** $\Theta(k)$ for the frames, the bits and the map, and one bit per page beyond the data that FIFO keeps.
- **Misses against the optimum.** $k$-competitive with the bit set at load, like LRU and FIFO; see [LRU competitiveness](/lru-competitiveness/) for the general bound and the lower bound $k$ for deterministic policies. On a loop over $k + 1$ pages, CLOCK misses on every request.

## Properties

- **Conservative, not marking.** The proof below shows the bound of $k$ misses in each part with at most $k$ distinct pages. CLOCK is not a [marking algorithm](/marking-algorithm/): at $t = 5$ above it evicts $a$, which was requested in the current phase.
- **Not a stack algorithm.** On $1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5$, CLOCK has 9 misses with $k = 3$ and 10 with $k = 4$, the same [Belady anomaly](/belady-anomaly/) as FIFO.
- **One bit of history.** CLOCK sorts the pages into two classes, used and not used since the last pass of the hand. Within a class it falls back to load order.
- **Cheap hits.** A hit writes one bit and moves nothing, so CLOCK needs no lock on a shared list for hits. This is why kernels and databases use it in place of exact LRU.

## Variants and improvements

- **Second chance as a queue.** The same policy, written as a FIFO queue: a page at the head with a set bit is moved to the tail with a clear bit. The circle and the hand avoid the moves.
- **GCLOCK.** A counter in place of the bit: a hit adds to the counter, the hand subtracts one. It keeps more frequency information.
- **WSCLOCK.** Carr and Hennessy (1981) combined the clock scan with the [working set](/working-set-model/) rule: a page with a clear bit is evicted only if its last use is older than a window.
- **Two-handed clock.** A front hand clears bits and a back hand, a fixed distance behind, evicts pages whose bit is still clear. Some Unix kernels used it to bound the time a page has to be used again.
- **CLOCK-Pro and CAR.** [CLOCK-Pro](/clock-pro/) brings the reuse distance idea of LIRS to the clock, and [CAR](/car/) runs ARC with two clocks.
- **SIEVE.** [SIEVE](/sieve/) keeps the visited bit but does not move a kept page to the head: new pages enter at the head and the hand moves from the tail, so the hand passes old pages before new ones.

## When to use it

Use CLOCK when hits are frequent and must be cheap, and when the hardware or the runtime can set one bit per access: page replacement in virtual memory, buffer pools in databases, and caches shared by many threads. Prefer exact LRU when the cache is small and the order of uses matters. Prefer a scan-resistant variant such as CLOCK-Pro when the workload mixes long scans with a hot set.

## Pitfalls

- **A clear bit at load.** If a new page starts with a clear bit, a page loaded and not used again can go at the next miss, before the other pages had their turn. This variant is not conservative and not $k$-competitive: with $k = 2$, the loop $(0, 0, 1, 2, 1, 1, 0, 2, 0)^m$ costs it 6 misses per round, while MIN has 2 and CLOCK with the bit set at load has 3. The test code checks these counts.
- **An endless scan.** The loop of lines L7 to L9 ends because it clears the bits it passes. Code that only reads the bits, or that lets another thread set bits during the scan without a bound, can loop.
- **Expecting LRU behavior.** When all bits are set, as after a burst of hits, CLOCK evicts in FIFO order and can drop the most recently used page.
- **Assuming that a larger cache helps.** CLOCK has Belady's anomaly. Simulate each cache size.

## Implementations

## History

Corbató described the replacement rule of Multics in a 1968 Project MAC report on a paging experiment, published in 1969 in the volume *In Honor of Philip M. Morse*. Multics kept a used bit per page, set by the hardware, and a pointer that cycled over the page frames, clearing the bits and choosing the first frame whose bit was clear. The rule spread to other systems under the names clock and second chance. Carr and Hennessy combined it with the working set in WSCLOCK in 1981. Later work, such as CLOCK-Pro (2005), CAR (2004) and SIEVE (2024), kept the hand and the bit and changed what the bit decides.

## References
