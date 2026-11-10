---
tag: YQPE6A
kind: concept
slug: cache-replacement-policy
name: Cache replacement policy
aliases:
- eviction policy
- replacement policy
- page replacement policy
area: online-and-streaming/paging-and-caching-online
level: intro
summary: The rule that chooses which cached item to evict when a new item must be brought in.
prereqs: [paging-problem, competitive-ratio]
see_also: [lru, fifo-replacement, clock, lfu, mru, random-replacement, marking-algorithm, stack-algorithms]
sources:
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the paging rules LRU, FIFO, LFU and LIFO, the bound k for LRU and FIFO, and the rules that are not competitive
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, Section 3.1, Some paging algorithms (LRU, FIFO, LIFO, LFU, FWF, marking algorithms), and Chapter 4 (RANDOM)
  - paper: "Neal E. Young, The k-server dual and loose competitiveness for paging, Algorithmica 11(6) (1994), 525-541"
    title: The k-server dual and loose competitiveness for paging
    locator: the definition of conservative paging algorithms and their bound k
  - paper: "Prabhakar Raghavan and Marc Snir, Memory versus randomization in on-line algorithms, ICALP 1989, LNCS 372, 687-703"
    title: Memory versus randomization in on-line algorithms
    locator: the bound k for random replacement against an adaptive online adversary
  - paper: doi:10.1147/sj.52.0078
    title: "L. A. Belady, A study of replacement algorithms for a virtual-storage computer, IBM Systems Journal 5(2) (1966), 78-101"
    locator: the comparison of replacement algorithms by simulation
---

A cache replacement policy is the rule that a cache uses to choose which item to evict when a new item must come in and the cache is full. In the [paging problem](/paging-problem/) it is an online rule for each [page fault](/page-fault/), and its quality is measured by the [competitive ratio](/competitive-ratio/) against the offline optimum of [Belady's algorithm](/belady-algorithm/). The common policies are LRU, FIFO, LFU, CLOCK, random and MRU. Two classes, the [marking algorithms](/marking-algorithm/) and the conservative algorithms, explain why LRU, FIFO and CLOCK are $k$-competitive while LFU and MRU are not competitive at all.

## In plain words

A cache is a small fast store. When it is full and a new item must come in, one old item must go. The policy is the rule that picks it.

Simple rules look at the past. Throw out the item used longest ago, the item that came in first, the item used least often, or a random item. Each rule works well on some patterns of use and badly on others.

Theory asks how bad a rule can be compared with a perfect rule that knows the future. For the best simple rules, the answer is at most the cache size times worse, and no rule that only sees the past can promise better. Some popular rules have no such bound at all.

## The idea

Fix a cache of $k$ pages. A *replacement policy* is a [demand paging](/demand-paging/) rule: on a fault with a full cache, it evicts one cached page, and its choice depends only on the requests so far, and on random bits for a randomized policy.

Split the requests into *$k$-phases*, the maximal blocks of requests with at most $k$ distinct pages (see [marking phases](/marking-phases/)). Two classes of policies bound the faults inside a phase.

- A **marking algorithm** marks a page when it is requested, unmarks all pages when a new phase starts, and never evicts a marked page.
- A **conservative algorithm** (Young 1994) has at most $k$ faults on each block of consecutive requests with at most $k$ distinct pages.

A policy of either class has at most $k$ faults in each phase, and OPT has at least one fault for each new phase, so the policy is $k$-competitive. No deterministic policy is better than $k$-competitive ([lower bound](/online-caching-lower-bound/)), so each deterministic policy in either class has competitive ratio exactly $k$.

| policy | evicts | marking | conservative | competitive ratio |
|---|---|---|---|---|
| [LRU](/lru/) | the page whose last request is oldest | yes | yes | $k$ |
| [FIFO](/fifo-replacement/) | the page that was loaded first | no | yes | $k$ |
| [FWF](/flush-when-full/) | all pages, on a fault with a full cache | yes | no | $k$ |
| [CLOCK](/clock/), bit set on load | the first page under the hand with a clear reference bit | no | yes | $k$ |
| [LFU](/lfu/) | the page with the fewest requests while cached | no | no | not competitive |
| [MRU](/mru/), LIFO | the page requested last, or loaded last | no | no | not competitive |
| [random](/random-replacement/) | a uniform random cached page | no | no | $k$, against an adaptive online adversary |
| [randomized marking](/randomized-marking/) | a uniform random unmarked page | yes | no | $2H_k - 1$, against an oblivious adversary |

**Why LRU is both.** In a phase, a page requested in that phase was requested more recently than each page not yet requested in it. So while an unmarked page is cached, the oldest page is unmarked, and LRU evicts it. So LRU never evicts a marked page. It is conservative for the same reason: in a block with at most $k$ distinct pages, a page requested in the block is evicted only after $k$ other distinct pages are requested after it, which cannot happen.

**Why FIFO is conservative.** Suppose FIFO evicts, inside a block, a page $p$ that it loaded inside the block. The $k$ pages loaded after $p$ are all requested in the block, and with $p$ that makes $k + 1$ distinct pages. So each page loaded in the block stays to its end, and the block has at most $k$ faults.

**Why CLOCK is conservative.** The reference bit is set on load and on each hit. Let a page $p$ be loaded at time $s$ and evicted at time $e$. The hand must clear the bit of $p$ and come back to it with the bit still clear. So between $s$ and $e$ it passes each other frame twice, or once if the frame was filled after $s$. At a second pass, a clear bit means that the hand evicts the page there and loads the page requested then, and a set bit means that the page there was requested at or after the first pass. So at time $e$ each of the $k - 1$ other frames holds a page requested in $(s, e]$, and $\sigma_e$ is one more page. If $s$ and $e$ are in one block, the block has $k + 1$ distinct pages.

**Why LFU and MRU fail.** For LFU with $k = 2$, request $a$ $m$ times and then $b\,c$ $m$ times. Page $a$ keeps its high count, so LFU evicts $b$ for $c$ and $c$ for $b$, with $2m + 1$ faults. OPT evicts $a$ once and has 3 faults. For MRU with $k = 2$, request $1\,2$ and then $3\,2$ $m$ times. MRU evicts the page just used, so each request faults, while OPT has 3 faults. In both cases the ratio grows with $m$, so no constant $c$ works.

**Random replacement.** RAND is not a marking algorithm, since it can evict a page just used. Raghavan and Snir showed that it is $k$-competitive even against an adaptive online adversary, an adversary that sees its past random choices. It uses no memory of the past, which matters in hardware.

## Examples

Take $\sigma = 1\,2\,3\,4\,1\,2\,5\,1\,2\,3\,4\,5$ with an empty start. LFU breaks ties by evicting the page loaded first. CLOCK sets the bit on load.

| policy | faults with $k = 3$ | faults with $k = 4$ |
|---|---|---|
| OPT ([Belady](/belady-algorithm/)) | 7 | 6 |
| LRU | 10 | 8 |
| FIFO | 9 | 10 |
| FWF | 12 | 10 |
| CLOCK | 9 | 10 |
| LFU | 10 | 8 |
| MRU | 7 | 6 |

MRU is optimal on this sequence, though it is not competitive. FIFO and CLOCK have more faults with the larger cache, which is [Belady's anomaly](/belady-anomaly/). LRU and OPT cannot show it, because they are [stack algorithms](/stack-algorithms/). LFU is a stack algorithm when it counts all past requests of a page, but not when it counts only the requests since the last load, as here.

**FIFO is not a marking algorithm.** Take $k = 3$ and $\sigma = 1\,2\,3\,4\,2\,1$. The phases are $[1\,2\,3]$ and $[4\,2\,1]$. At the request for 4, FIFO evicts 1. Page 2 is then requested and marked. At the last request, FIFO evicts 2, the page loaded first, while 3 is unmarked.

**CLOCK is not a marking algorithm.** Take $k = 4$ and $\sigma = 5\,0\,1\,4\,6\,0\,5\,2\,4\,6\,5\,1$, with phases $[5\,0\,1\,4]$, $[6\,0\,5\,2]$ and $[4\,6\,5\,1]$. At the last request the frames hold 6, 4, 5 and 2, all with the bit set, so the hand clears all four and evicts 5, which was requested one step before. Page 2 is unmarked in this phase.

**FWF is not conservative.** Take $k = 2$ and $\sigma = 1\,2\,3\,2$. At the request for 3 FWF empties the cache, so the block $2\,3\,2$ with 2 distinct pages has 3 faults.

## Where it is used

- **Operating systems.** Virtual memory uses CLOCK and its variants, because a true LRU order costs too much work on each memory access. CLOCK keeps the bound $k$ of LRU.
- **Processor caches.** Hardware uses tree [pseudo-LRU](/plru-replacement/) and random replacement in [set-associative caches](/set-associative-cache/), where each set is a small cache with its own policy.
- **Databases and web caches.** Buffer pools and content caches use [2Q](/two-q-replacement/), [ARC](/arc/) and [LRU-K](/lru-k/), which mix recency and frequency to resist scans, and [GreedyDual](/greedy-dual/) or the [Landlord algorithm](/landlord-algorithm/) when items have costs or sizes.
- **Simulation.** [Stack algorithms](/stack-algorithms/) give the [miss ratio curve](/miss-ratio-curve/) for all cache sizes in one pass, and [Belady's algorithm](/belady-algorithm/) gives the best possible miss count to compare with.
- **Scans.** MRU suits a repeated scan over a set slightly larger than the cache, where LRU faults on each request.
- **Theory.** The competitive analysis of these policies started [online algorithms](/online-algorithm/) as a field. The gap between the bound $k$ and the observed behaviour of LRU led to models of [locality of reference](/locality-of-reference/) and to [resource augmentation](/sleator-tarjan-paging-bound/).

## References
