---
tag: VWYKNJ
kind: algorithm
slug: two-q-replacement
name: 2Q replacement
aliases:
- 2Q
- two queue
- full 2Q
area: online-and-streaming/paging-and-caching-online
level: advanced
summary: Uses an FIFO queue for first-time pages and an LRU queue for re-referenced pages to resist scans.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, c: the number of page slots, m: the number of identifiers in A1out}
  time: {expected: O(n)}
  space: {extra: O(c + m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1994
  people: [Theodore Johnson, Dennis Shasha]
  note: Johnson and Shasha gave 2Q at VLDB 1994 as a buffer rule for database systems that behaves like LRU-2 but costs only constant time for each access.
prereqs: [paging-problem, lru, fifo-replacement]
see_also: [two-q, lru-k, arc, lirs, s3-fifo, ghost-lists, slru, cache-replacement-policy]
sources:
  - paper: "Theodore Johnson and Dennis Shasha, 2Q: A Low Overhead High Performance Buffer Management Replacement Algorithm, Proceedings of the 20th International Conference on Very Large Data Bases (VLDB), Santiago, Chile, 1994, 439-450"
    locator: Section 2 (the simplified 2Q and the full 2Q pseudocode, the queues A1in, A1out and Am), Section 3 (the tuning of Kin and Kout, with Kin near 25% and Kout near 50% of the page slots)
  - paper: doi:10.1145/2786.2793
    title: Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2), 1985, 202-208
    locator: the lower bound k for each deterministic online paging rule
  - paper: doi:10.1145/170035.170081
    title: "Elizabeth J. O'Neil, Patrick E. O'Neil and Gerhard Weikum, The LRU-K page replacement algorithm for database disk buffering, Proceedings of SIGMOD 1993, 297-306"
    locator: the LRU-2 rule that 2Q approximates
---

2Q is a cache replacement rule of Johnson and Shasha (1994) for database buffer pools. A page seen for the first time goes into a small FIFO queue, and it moves into the main LRU queue only if it is requested again soon after it left the small queue. So a long scan of pages that are read once passes through the small queue and does not push the hot pages out. Each access takes constant time, like [LRU](/lru/), while the hit rate is close to that of [LRU-2](/lru-k/). In the worst case, 2Q with the usual parameters is not competitive at all.

## In plain words

A cache that holds the most recently used pages has one weak point. If a program reads a large file once, the file fills the cache and the pages that are used all the time are lost.

2Q puts new pages in a short waiting line first. When a page leaves the waiting line, the cache keeps only its name in a list of recent visitors. If the page is requested again while its name is in that list, it was not a one-time visitor, so it goes into the main part of the cache. The main part works like LRU. Pages from a one-time scan come and go in the waiting line, and the main part stays as it was.

## The problem

The input is a sequence of page requests and a cache with $c$ page slots. A request to a page in the cache is a hit. Otherwise it is a miss: the page is loaded, and if all slots are full, one page is paged out. The aim is few misses. This is the [paging problem](/paging-problem/), and the online rule must choose the page to evict without knowledge of the future. Database workloads mix index pages that are used again and again with large scans of pages that are used once, so the rule must tell the two kinds apart. The [cache replacement policy](/cache-replacement-policy/) page lists the other rules.

## The algorithm

2Q keeps three queues. $A1_{in}$ is a FIFO queue of resident pages. $A1_{out}$ is a FIFO queue of at most $K_{out}$ page identifiers, with no page data. $A_m$ is an LRU queue of resident pages. The resident pages are those in $A1_{in}$ and $A_m$, at most $c$ in total. The threshold $K_{in} < c$ sets the normal size of $A1_{in}$. New items enter each queue at its head, and old items leave at its tail.

```pseudo id=main
2Q(σ, c, K_in, K_out)
L1  misses ← 0, all three queues empty
L2  for each request x in σ do
L3      if x is in A_m then move x to the head of A_m (hit)
L4      else if x is in A1_in then do nothing (hit)
L5      else if x is in A1_out then remove x from A1_out, RECLAIM, add x to the head of A_m, misses ← misses + 1
L6      else RECLAIM, add x to the head of A1_in, misses ← misses + 1
L7  return misses

RECLAIM()
L8  if |A1_in| + |A_m| < c then return (a slot is free)
L9  if |A1_in| > K_in then page out the tail of A1_in, add its identifier to the head of A1_out, and if |A1_out| > K_out, drop the tail of A1_out
L10 else page out the tail of A_m
```

Line L4 is the important difference from LRU. A second request while the page is still in $A1_{in}$ does not promote it. Johnson and Shasha call such requests *correlated*: a transaction often reads the same page several times within a short time, and these reads do not show that the page is hot. Only a request in line L5, after the page has left $A1_{in}$ but while its identifier is still in $A1_{out}$, shows that the page has a real reuse.

Line L9 keeps $A1_{in}$ near $K_{in}$ pages, so $A_m$ gets the rest of the slots. A page paged out of $A_m$ in line L10 does not go to $A1_{out}$, because it was not used for a long time. Johnson and Shasha suggest $K_{in}$ near $25\%$ of the page slots and $K_{out}$ near $50\%$ of the page slots. $A1_{out}$ holds only identifiers, so it costs little memory.

## Example

Four slots, $c = 4$, with $K_{in} = 1$ and $K_{out} = 2$. The requests are $a, b, c, d, e, a, b, a$ and then a scan $x, y, z, w$, and then $a, b$. Each queue is written from its head to its tail.

| request | result | paged out | $A1_{in}$ | $A1_{out}$ | $A_m$ |
|---|---|---|---|---|---|
| a | miss (L6) | - | a | - | - |
| b | miss (L6) | - | b, a | - | - |
| c | miss (L6) | - | c, b, a | - | - |
| d | miss (L6) | - | d, c, b, a | - | - |
| e | miss (L6) | a | e, d, c, b | a | - |
| a | miss (L5) | b | e, d, c | b | a |
| b | miss (L5) | c | e, d | c | b, a |
| a | hit (L3) | - | e, d | c | a, b |
| x | miss (L6) | d | x, e | d, c | a, b |
| y | miss (L6) | e | y, x | e, d | a, b |
| z | miss (L6) | x | z, y | x, e | a, b |
| w | miss (L6) | y | w, z | y, x | a, b |
| a | hit (L3) | - | w, z | y, x | a, b |
| b | hit (L3) | - | w, z | y, x | b, a |

2Q has $11$ misses. The pages $a$ and $b$ show reuse at the requests 6 and 7, so they enter $A_m$, and the scan $x, y, z, w$ then goes through $A1_{in}$ only. LRU with $4$ slots has $13$ misses on the same sequence, because the scan pushes $a$ and $b$ out. The offline optimum ([Belady's rule](/belady-algorithm/)) has $9$ misses.

## Correctness

2Q serves each request: after line L3, L4, L5 or L6, the page $x$ is resident. Line L8 or line L9 or line L10 always frees a slot when the cache is full, because $|A1_{in}| \le K_{in}$ and a full cache give $|A_m| \ge c - K_{in} \ge 1$. The queues stay disjoint, at most $c$ pages are resident, and $A1_{out}$ holds at most $K_{out}$ identifiers of pages that are not resident. The proof below shows these invariants. It also shows that if $K_{out} \ge 1$ and $K_{in} + K_{out} + 2 \le c$, then 2Q is not competitive: there is no bound $\mathrm{2Q}(\sigma) \le \alpha \cdot \mathrm{OPT}(\sigma) + \beta$. The usual parameters $K_{in} = c/4$ and $K_{out} = c/2$ meet this condition for each $c \ge 8$.

## Complexity

With a hash table from page identifiers to queue nodes, and doubly linked lists for the queues, each line takes $O(1)$ expected time. So $n$ requests take $O(n)$ expected time. The memory is $c$ page slots and $K_{out}$ identifiers, plus $O(c + K_{out})$ words for the lists and the table. The paper presents this constant cost as the main advantage over LRU-2, which needs a priority queue and $O(\log c)$ time for each access.

## Properties

- **Scan resistance.** Once the hot pages are in $A_m$ and $|A1_{in}| > K_{in}$, a scan of new pages evicts only from $A1_{in}$. So the hot pages survive a scan of any length. The tests check this with $c = 8$ and a scan of $100$ pages.
- **Not competitive with the usual parameters.** Put $c - K_{in} - 1$ pages in $A_m$ that are never used again, and then request a cycle over $c$ new pages again and again. If $c \ge K_{in} + K_{out} + 2$, each new page leaves $A1_{out}$ before it comes back, so each request is a miss, and the stale pages in $A_m$ are never paged out. The offline optimum loads the $c$ cycle pages once. So the ratio is unbounded.
- **The lower bound of all deterministic rules.** By the theorem of [Sleator and Tarjan](/sleator-tarjan-paging-bound/), every deterministic online rule with $c$ slots has a competitive ratio of at least $c$, so 2Q can never be better than $c$-competitive.
- **A special case is FIFO.** With $K_{out} = 0$, line L5 never applies, $A_m$ stays empty, and 2Q is [FIFO](/fifo-replacement/), which is $c$-competitive.
- **Good hit rates in practice.** On the traces of Johnson and Shasha, 2Q gave hit rates close to those of LRU-2 and higher than those of LRU.

## Variants and improvements

- **Simplified 2Q.** The paper first gives a simpler rule with two resident queues: a FIFO queue $A1$ and an LRU queue $A_m$. A hit in $A1$ moves the page to $A_m$. This rule promotes pages on correlated requests, which is why the full version adds $A1_{out}$.
- **SLRU.** [Segmented LRU](/slru/) has a probationary segment and a protected segment, both of resident pages. It is close to the simplified 2Q.
- **ARC.** [ARC](/arc/) also has a list of recent pages and a list of frequent pages with [ghost lists](/ghost-lists/), but it moves the boundary between the two lists by itself. So it needs no parameter like $K_{in}$.
- **LIRS and S3-FIFO.** [LIRS](/lirs/) uses the reuse distance to choose the hot pages. [S3-FIFO](/s3-fifo/) uses a small FIFO queue, a main FIFO queue and a ghost queue, an idea close to 2Q with FIFO queues only.
- **Systems view.** The [2Q page in the systems area](/two-q/) describes the rule as it is used in database and operating system caches.

## When to use it

Use 2Q for a buffer pool or a page cache where scans of cold data mix with a smaller set of hot pages, and where the cost of each access must stay constant. It is a good choice when LRU loses its hot set to scans and LRU-2 costs too much. If the mix of the workload changes a lot, an adaptive rule such as ARC needs less tuning. If a worst-case guarantee matters, use LRU or FIFO, which are $c$-competitive, or a randomized [marking](/marking-algorithm/) rule.

## Pitfalls

- **Forgetting to remove the identifier from $A1_{out}$.** The pseudocode of the paper adds $x$ to $A_m$ in line L5 but does not say that its identifier leaves $A1_{out}$. If it stays, the page is in two queues, and a later trim of $A1_{out}$ can act on a resident page. This page removes it, as most implementations do.
- **Promoting on a hit in $A1_{in}$.** That gives the simplified rule. Correlated requests then fill $A_m$ with pages that are not hot.
- **Bad sizes of $K_{in}$ and $K_{out}$.** If $A1_{out}$ is too short, a page with real reuse leaves it before its second request and never enters $A_m$. If $A1_{in}$ is too large, $A_m$ is small and the hot set does not fit.
- **Stale pages in $A_m$.** A page in $A_m$ leaves only when $|A1_{in}| \le K_{in}$. While new pages keep $A1_{in}$ full, old pages in $A_m$ stay, even if they are never used again. This is the cause of the bad worst case above.

## Implementations

## History

Johnson and Shasha presented 2Q at the VLDB conference in 1994. Their aim was the hit rate of the LRU-K rule of O'Neil, O'Neil and Weikum (1993), without its priority queue. The idea of a short queue for first-time pages and a list of identifiers of recently evicted pages came back in many later rules, such as ARC (2003), LIRS (2002) and S3-FIFO (2023). The worst case of 2Q in the competitive sense was not a topic of the original paper.

## References
