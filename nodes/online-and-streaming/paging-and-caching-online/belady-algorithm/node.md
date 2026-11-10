---
tag: 6CTF08
kind: algorithm
slug: belady-algorithm
name: Belady's algorithm (MIN/OPT)
aliases:
- MIN
- OPT
- optimal offline caching
- LFD
- longest forward distance
- furthest in the future
area: online-and-streaming/paging-and-caching-online
level: intro
summary: Offline optimal policy that evicts the page whose next request is farthest in the future.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size}
  time: {worst: O(n log n)}
  space: {extra: Θ(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1966
  people: [László Bélády]
  note: Belady described the optimal replacement rule MIN in his 1966 study of replacement algorithms for virtual storage at IBM.
prereqs: [paging-problem, demand-paging, binary-heap]
see_also: [belady-optimality, belady-optimal, lru, stack-algorithms, online-caching-lower-bound, learning-augmented-marking]
sources:
  - paper: doi:10.1147/sj.52.0078
    title: "L. A. Belady, A study of replacement algorithms for a virtual-storage computer, IBM Systems Journal 5(2) (1966), 78-101"
    locator: the algorithm MIN and its use as the optimum in the simulations
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, Section 3.4, LFD, an optimal offline paging algorithm
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 4.3, Optimal caching, the Farthest-in-Future algorithm
  - paper: doi:10.1147/sj.92.0078
    title: "R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2) (1970), 78-117"
    locator: the optimal replacement rule as a stack algorithm
---

Belady's algorithm, also called MIN, OPT or LFD (longest forward distance), is the offline rule for the [paging problem](/paging-problem/): on a [fault](/page-fault/) with a full cache, evict the page whose next request is furthest in the future, or a page that is never requested again. [Belady's optimality theorem](/belady-optimality/) proves that it has the fewest faults of all algorithms on every request sequence. It needs the whole sequence in advance, so it is not an [online algorithm](/online-algorithm/). It is the measure $\mathrm{OPT}(\sigma)$ against which the [competitive ratio](/competitive-ratio/) of LRU, FIFO and the marking algorithms is defined, and with a heap it runs in $O(n \log n)$ time.

## In plain words

You have room for a few books on your desk and the rest are on a far shelf. You have the full list of the books you will read, in order. When you need a book that is not on the desk and the desk is full, put back the book that you will need again last. A book that you will never need again is the best one to put back.

This choice keeps on the desk the books that you will need soonest. Any other choice puts back a book that comes back earlier, and that can only make you walk to the shelf sooner. The algorithm cannot be used where the future is unknown, but it tells you the smallest number of walks to the shelf, so you can judge real rules against it.

## The problem

The input is a cache size $k \ge 1$ and a request sequence $\sigma = \sigma_1 \cdots \sigma_n$ of pages. The cache starts empty and holds at most $k$ pages. The output is a [demand paging](/demand-paging/) schedule: for each fault with a full cache, the page to evict. The goal is to make the number of faults as small as possible. The value is $\mathrm{OPT}(\sigma)$.

For a time $t$ and a page $q$, let $\mathrm{next}_t(q)$ be the smallest $s > t$ with $\sigma_s = q$, or $\infty$ if there is none.

## The algorithm

The first loop computes, for each position $t$, the position of the next request for the same page. The main loop keeps the cache $C$, and a max-heap $H$ of pairs (next request time, page). A page in the cache has exactly one *current* pair, and the heap may also hold *stale* pairs from earlier times, which the algorithm skips.

```pseudo id=main
BELADY(σ, k)                                    ▷ σ = σ_1 .. σ_n, cache size k ≥ 1
L1  for t ← n downto 1 do next[t] ← the next s > t with σ_s = σ_t, else ∞
L2  C ← ∅, H ← an empty max-heap, faults ← 0
L3  for t ← 1 to n do
L4      p ← σ_t
L5      if p ∉ C then
L6          faults ← faults + 1
L7          if |C| = k then
L8              repeat (u, q) ← POP-MAX(H) until q ∈ C and key[q] = u
L9              C ← C \ {q}                     ▷ evict q
L10         C ← C ∪ {p}
L11     key[p] ← next[t], PUSH(H, (key[p], p))
L12 return faults
```

Line L1 scans the sequence from the end with a [hash table](/hash-table/) that maps each page to the last position seen so far. Line L11 runs on a hit and on a fault, so $key[q] = \mathrm{next}_{t}(q)$ for each $q \in C$ after request $t$. The pair pushed before is now stale. Line L8 pops pairs until it finds a current one. The correctness proof shows that the first popped pair is always current, and the test is a guard. Ties, which happen only between pages with key $\infty$, may be broken in any way; the implementation evicts the page whose last request is oldest.

## Example

Take $k = 3$ and $\sigma = 1\,2\,3\,4\,1\,2\,5\,1\,2\,3$. The column "next requests" gives $\mathrm{next}_t(q)$ for the cached pages at each fault with a full cache.

| $t$ | $\sigma_t$ | result | next requests of the cached pages | evict | cache after |
|---|---|---|---|---|---|
| 1 | 1 | fault | | | {1} |
| 2 | 2 | fault | | | {1, 2} |
| 3 | 3 | fault | | | {1, 2, 3} |
| 4 | 4 | fault | 1 at 5, 2 at 6, 3 at 10 | 3 | {1, 2, 4} |
| 5 | 1 | hit | | | {1, 2, 4} |
| 6 | 2 | hit | | | {1, 2, 4} |
| 7 | 5 | fault | 1 at 8, 2 at 9, 4 never | 4 | {1, 2, 5} |
| 8 | 1 | hit | | | {1, 2, 5} |
| 9 | 2 | hit | | | {1, 2, 5} |
| 10 | 3 | fault | 1, 2 and 5 never | 5 | {1, 2, 3} |

Belady's algorithm has 6 faults. Five of them are forced, one for each distinct page. On the same sequence [LRU](/lru/) and [FIFO](/fifo-replacement/) each have 8 faults, and [flush when full](/flush-when-full/) has 10. At $t = 10$ each choice is optimal, because no page is requested again.

## Correctness

The schedule is a valid demand paging schedule: each request is in the cache after it is served, and the cache never holds more than $k$ pages. The invariant of the main loop is: after request $t$, the heap holds the current pair $(\mathrm{next}_t(q), q)$ for each $q \in C$, and each other pair in the heap has a key of at most $t$. A current pair has a key greater than $t$, so at the next fault the maximum of the heap is the current pair of the cached page with the furthest next request. So the algorithm evicts as the rule says. [Belady's optimality theorem](/belady-optimality/) then shows, by an exchange argument, that this rule gives $\mathrm{OPT}(\sigma)$ faults.

## Complexity

- **Next requests.** Line L1 does $n$ table lookups and updates, so $O(n)$ time when a table operation costs $O(1)$. With hashing this is expected time. If the pages are integers in $\{0, \ldots, n-1\}$, an array gives $O(n)$ in the worst case.
- **The heap.** Line L11 pushes $n$ pairs in total, so the heap has at most $n$ pairs and each push costs $O(\log n)$. Each pop at line L8 removes a pair pushed before, so there are at most $n$ pops in total, each $O(\log n)$. So the main loop takes $O(n \log n)$ time in the worst case.
- **Few distinct pages.** If the sequence has at most $k$ distinct pages, no eviction happens. A version that starts to push pairs only when the cache first becomes full then runs in $O(n)$ time. Each version needs $\Omega(n)$ time, because it must read each request.
- **Space.** The array $next$ and the heap take $\Theta(n)$ space.
- **An indexed heap of size $k$.** With a heap that supports changing the key of a page in place, each hit and each fault costs $O(\log k)$, so the time is $O(n \log k)$ after line L1.

## Properties

- **Offline.** The rule reads $\sigma_{t+1}, \ldots, \sigma_n$, so it cannot run online. No online rule can match it: the [deterministic lower bound](/online-caching-lower-bound/) gives a ratio of at least $k$.
- **Optimal.** It has $\mathrm{OPT}(\sigma)$ faults on each $\sigma$ and for each $k$ ([proof](/belady-optimality/)).
- **Deterministic.** Up to the choice among pages that are never requested again, which does not change the number of faults.
- **Demand paging.** It loads a page only on a fault and evicts one page only when the cache is full.
- **A stack algorithm.** The priority "next request time" does not depend on $k$. With a tie rule that also does not depend on $k$, the cache of size $k$ is always a subset of the cache of size $k + 1$, so one pass gives OPT for all cache sizes (Mattson et al. 1970). See [stack algorithms](/stack-algorithms/).

## Variants and improvements

- **One pass for all cache sizes.** Mattson, Gecsei, Slutz and Traiger computed the OPT fault count for all $k$ in one pass, with a stack ordered by priority. See [stack algorithms](/stack-algorithms/) and the [Mattson stack algorithm](/mattson-stack-algorithm/).
- **Weighted and variable size pages.** With costs or sizes, furthest in the future is no longer optimal. [Weighted paging](/weighted-paging-problem/) offline is solved by min-cost flow, and general caching with sizes is NP-hard.
- **Learned predictions.** Online rules that guess the next request time and then act as Belady's rule are the basis of [learning-augmented marking](/learning-augmented-marking/), which keeps a worst-case guarantee.
- **Hardware imitation.** Systems such as Hawkeye train a predictor on what Belady's rule would have done on the past accesses.

## When to use it

Use Belady's algorithm when the whole trace is known: to compute the best possible miss count of a cache in a simulation, as the yardstick in a competitive or experimental study, or to plan the evictions of a batch job whose access order is fixed in advance, such as some compiler register and buffer allocations. It does not apply to a live cache. There, use an online rule such as [LRU](/lru/), [CLOCK](/clock/) or a [marking algorithm](/marking-algorithm/), and compare its miss count with this one.

## Pitfalls

- **Evicting the page used least far in the past.** That is LRU, an online rule. Line L8 must use the next request time, not the last one.
- **Forgetting to update the key on a hit.** If line L11 runs only on a fault, the key of a page that was hit still points to the request just served, and the eviction can pick a page that is needed soon. The update must run on each request.
- **Comparing keys of stale pairs.** In a heap with lazy deletion, line L8 must skip a pair whose page was evicted or whose key changed. Without the test of line L8 the code depends on a fact proved only for this exact order of updates.
- **Infinity as a large number.** When positions run from 1 to $n$, code $\infty$ as $n + 1$ or more. If it is coded as $n$, a page that is requested at position $n$ ties with the pages that are never requested again, and the rule can evict it and fault once more.
- **Mixing up the theorem.** The rule is optimal for the number of faults with unit costs. With different costs per page or with page sizes, it is not optimal.

## Implementations

## History

Belady described MIN in 1966, in a study at IBM that compared replacement algorithms for virtual storage by simulation, with MIN as the optimum. Mattson, Gecsei, Slutz and Traiger (1970) placed the optimal rule among the stack algorithms and gave a one-pass method for all cache sizes. Borodin and El-Yaniv call the rule LFD, for longest forward distance, and Kleinberg and Tardos call it Farthest-in-Future and use it as the main example of an exchange argument.

## References
