---
tag: Z520JB
kind: algorithm
slug: arc
name: Adaptive replacement cache (ARC)
aliases:
- ARC
- Adaptive Replacement Cache (ARC)
area: systems/caching-policies
level: advanced
summary: Splits the cache between pages seen once and pages seen twice, and uses ghost lists of evicted keys to tune the split online.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, c: the cache size in pages}
  time: {worst: O(n), expected: O(n)}
  space: {extra: Θ(c)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2003
  people: [Nimrod Megiddo, Dharmendra S. Modha]
  note: Megiddo and Modha of IBM Almaden published ARC at FAST 2003. IBM held a patent on it. It is the basis of the ARC in ZFS.
prereqs: [lru, paging-problem, ghost-lists]
see_also: [car, lirs, two-q, lru-k, clock-pro, s3-fifo, belady-optimal, competitive-ratio]
sources:
  - url: https://www.usenix.org/legacy/events/fast03/tech/full_papers/megiddo/megiddo.pdf
    title: "Nimrod Megiddo and Dharmendra S. Modha, ARC: A Self-Tuning, Low Overhead Replacement Cache, USENIX FAST 2003, 115-130"
    locator: Section III (DBL(2c) in Fig. 1 and the class of policies with conditions A.1 to A.5), Section IV and Fig. 4 (the ARC policy, Cases I to IV and the subroutine REPLACE)
  - paper: doi:10.1109/MC.2004.1297303
    title: "Nimrod Megiddo and Dharmendra S. Modha, Outperforming LRU with an adaptive replacement cache algorithm, IEEE Computer 37(4) (2004), 58-65"
    locator: the description of ARC for a general audience and the comparison with LRU
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the lower bound of k for every deterministic online paging rule
  - url: https://arxiv.org/abs/1503.07624
    title: "Mario E. Consuegra, Wendy A. Martinez, Giri Narasimhan, Raju Rangaswami, Leo Shao and Giuseppe Vietri, Analyzing Adaptive Cache Replacement Strategies, arXiv 1503.07624 (2015)"
    locator: the abstract, the claimed competitive ratios of ARC and CAR
---

The adaptive replacement cache (ARC) is a [cache replacement policy](/cache-replacement-policy/) for pages of equal size. It keeps two LRU lists of cached pages, $T_1$ for pages seen once recently and $T_2$ for pages seen at least twice. It also keeps two [ghost lists](/ghost-lists/), $B_1$ and $B_2$, that hold only the keys of pages recently evicted from $T_1$ and $T_2$. A miss that hits a ghost list tells ARC that the matching side was too small, and ARC moves a target $p$ for the size of $T_1$ toward that side. Each request costs $O(1)$ time, and the directory holds at most $2c$ keys for a cache of $c$ pages.

## In plain words

Picture two shelves. New books go on the first shelf. A book you ask for a second time moves to the second shelf. The two shelves share a fixed amount of space, and the question is how much each one gets.

ARC answers the question by keeping notes. When it sends a book back to the library, it writes the title on a list for that shelf. Later, if you ask for a book whose title is on the list of the first shelf, ARC learns that the first shelf was too small, so it gives the first shelf a little more space. A title on the list of the second shelf does the opposite. The notes cost only a title each, not a book, so ARC can learn without using cache space.

## The problem

The model is the [paging problem](/paging-problem/). A cache holds at most $c$ pages of the same size. Each request names one page. A request for a cached page is a hit. Any other request is a miss, the page is loaded, and if the cache is full, one cached page must go first. The policy is online and the cost is the number of misses. The aim of ARC is a policy that does as well as LRU on workloads with recency, better than LRU on workloads with frequency or scans, and that needs no tuning parameter.

## The algorithm

ARC keeps four lists, each in LRU order:

- $T_1$: cached pages that were requested exactly once since they entered the directory.
- $T_2$: cached pages that were requested at least twice.
- $B_1$: keys of pages evicted from $T_1$, with no data.
- $B_2$: keys of pages evicted from $T_2$, with no data.

The number $p$, with $0 \le p \le c$, is the target size of $T_1$. It starts at $0$. The pseudocode follows Fig. 4 of the paper, with the four cases named as there.

```pseudo id=main
ARC-ACCESS(x)                           ▷ lists T1, T2, B1, B2, target p, cache size c
L1  if x ∈ T1 ∪ T2 then                 ▷ Case I: cache hit
L2      move x to the MRU end of T2
L3      return hit
L4  if x ∈ B1 then                      ▷ Case II: ghost hit in B1
L5      p ← min(c, p + max(|B2| / |B1|, 1))
L6      REPLACE(x)
L7      move x from B1 to the MRU end of T2 and load it
L8      return miss
L9  if x ∈ B2 then                      ▷ Case III: ghost hit in B2
L10     p ← max(0, p − max(|B1| / |B2|, 1))
L11     REPLACE(x)
L12     move x from B2 to the MRU end of T2 and load it
L13     return miss
L14 if |T1| + |B1| = c then             ▷ Case IV(A): x is new, L1 is full
L15     if |T1| < c then
L16         delete the LRU key of B1
L17         REPLACE(x)
L18     else
L19         evict the LRU page of T1 and keep no ghost
L20 else                                ▷ Case IV(B): x is new, L1 has room
L21     if |T1| + |T2| + |B1| + |B2| ≥ c then
L22         if |T1| + |T2| + |B1| + |B2| = 2c then
L23             delete the LRU key of B2
L24         REPLACE(x)
L25 put x at the MRU end of T1 and load it
L26 return miss

REPLACE(x)
L27 if |T1| ≥ 1 and (|T1| > p or (x ∈ B2 and |T1| = p)) then
L28     evict the LRU page of T1 and put its key at the MRU end of B1
L29 else
L30     evict the LRU page of T2 and put its key at the MRU end of B2
```

The step sizes on lines L5 and L10 are the ratio of the ghost list sizes, at least $1$. If $B_1$ is small, a hit in $B_1$ is rare and strong evidence, so $p$ moves by a lot. REPLACE evicts from $T_1$ when $T_1$ is larger than its target, and from $T_2$ when it is not. The case $x \in B_2$ with $|T_1| = p$ breaks a tie toward $T_1$, because a hit in $B_2$ says that $T_2$ needs room.

Each list is a [doubly linked list](/doubly-linked-list/) and one [hash table](/hash-table/) maps every key in the directory to its node and list. With these, each line takes $O(1)$ time.

## Example

Take $c = 3$ and the trace $1, 2, 1, 3, 4, 2, 5, 4, 1, 6, 1, 2$. Lists are written LRU first, and "evicted" is the page that leaves the cache.

| $t$ | request | result | evicted | $T_1$ | $T_2$ | $B_1$ | $B_2$ | $p$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | miss | | 1 | | | | 0 |
| 2 | 2 | miss | | 1 2 | | | | 0 |
| 3 | 1 | hit | | 2 | 1 | | | 0 |
| 4 | 3 | miss | | 2 3 | 1 | | | 0 |
| 5 | 4 | miss | 2 | 3 4 | 1 | 2 | | 0 |
| 6 | 2 | miss | 3 | 4 | 1 2 | 3 | | 1 |
| 7 | 5 | miss | 1 | 4 5 | 2 | 3 | 1 | 1 |
| 8 | 4 | hit | | 5 | 2 4 | 3 | 1 | 1 |
| 9 | 1 | miss | 5 | | 2 4 1 | 3 5 | | 0 |
| 10 | 6 | miss | 2 | 6 | 4 1 | 3 5 | 2 | 0 |
| 11 | 1 | hit | | 6 | 4 1 | 3 5 | 2 | 0 |
| 12 | 2 | miss | 6 | | 4 1 2 | 3 5 6 | | 0 |

At $t = 5$ the cache is full and $|T_1| = 2 > p = 0$, so REPLACE evicts from $T_1$ and page 2 becomes a ghost in $B_1$. At $t = 6$ page 2 is found in $B_1$ (Case II), so $p$ grows by $\max(0/1, 1) = 1$ and page 2 enters $T_2$. At $t = 9$ page 1 is found in $B_2$ (Case III), so $p$ falls back to $0$. At $t = 12$, $|T_1| = 1 > p$, so page 6 leaves $T_1$ and page 2 returns from $B_2$ to $T_2$. All twelve rows are checked by the test file.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). It shows that $B_1$ followed by $T_1$ is the list $L_1$ of the policy DBL($2c$), and $B_2$ followed by $T_2$ is $L_2$, and that $|T_1| + |T_2| = \min(c, |L_1| + |L_2|)$. From this follow the invariants of the class of policies in Section III of the paper: the four lists are disjoint, $|T_1| + |B_1| \le c$, the directory has at most $2c$ keys, the ghost lists are empty until the cache is full, the cache stays full after that, and the cached pages of each side are more recent than its ghosts. It also follows that the directory always contains the $c$ most recently requested distinct pages.

## Complexity

Each request does a constant number of hash table operations and list moves, so a trace of $n$ requests takes $O(n)$ expected time with a hash table, or $O(n)$ worst case time with keys that index an array. The directory holds at most $2c$ keys and the cache at most $c$ pages, so the extra space is $\Theta(c)$ keys. The ghost lists hold keys only, which is small next to the pages in most uses.

## Properties

- **Online and deterministic.** The choice depends only on past requests.
- **No tuning parameter.** The target $p$ is learned. The paper calls ARC self-tuning.
- **Scan resistance.** A scan of new pages enters $T_1$ and leaves through $B_1$. While $p$ stays small, it never pushes out pages of $T_2$. A scan of pages that are all new never causes a ghost hit, so it never moves $p$.
- **No better worst-case guarantee than LRU.** Every deterministic online paging policy has a [competitive ratio](/competitive-ratio/) of at least $c$ ([Sleator and Tarjan](/sleator-tarjan-paging-bound/)). ARC has no proven ratio better than LRU's $c$. A 2015 preprint by Consuegra, Martinez, Narasimhan, Rangaswami, Shao and Vietri claims that ARC is at most $4c$-competitive, which is weaker than LRU's bound. That claim has not been through peer review.
- **Not loop resistant.** On a cyclic trace over more than $c$ pages, all four lists are in LRU order, and ARC drops the page that the loop needs next. The test file checks that ARC gets zero hits on loops of $11$ to $30$ pages with $c = 10$.

## Variants and improvements

- **CAR.** [CAR](/car/) replaces the LRU lists $T_1$ and $T_2$ with two clocks, so that a hit only sets a bit. It uses the same ghost lists and the same rule for $p$.
- **CART.** A variant of CAR in the same paper that also uses a filter bit to separate short-term from long-term use.
- **ZFS ARC.** The file system ZFS uses a changed ARC with pages of variable size and extra lists for data that must stay in memory.
- **LIRS and CLOCK-Pro.** [LIRS](/lirs/) and [CLOCK-Pro](/clock-pro/) also keep keys of evicted pages, but rank pages by reuse distance. They handle loops that ARC does not.
- **S3-FIFO.** [S3-FIFO](/s3-fifo/) keeps the idea of a small probation area and a ghost list, but uses FIFO queues.

## When to use it

Use ARC when the workload mixes recency and frequency and changes over time, and when one tuning parameter for the split is not acceptable. Storage controllers, file systems and buffer pools are the classic uses. ARC needs a lock for each hit, as LRU does, so in a highly concurrent cache [CAR](/car/), [CLOCK](/clock/) or [S3-FIFO](/s3-fifo/) may be a better fit. If the workload is a loop over slightly more than the cache, use [LIRS](/lirs/) or a policy with a loop detector.

A small seeded run made for this page uses Python `random.Random(1)`, $c = 100$ and 30000 requests per trace. Zipf has 1000 keys with exponent 0.8. Scan repeats 1000 uniform requests to 80 hot keys followed by 300 new keys. Loop cycles through 120 keys. Mix takes 60% Zipf, 20% the next key of a 120-key loop and 20% new keys.

| policy | Zipf | scan | loop | mix |
| --- | --- | --- | --- | --- |
| MIN | 62.4% | 76.7% | 82.9% | 39.3% |
| LRU | 37.5% | 70.7% | 0.0% | 16.7% |
| ARC | 45.6% | 76.7% | 0.0% | 28.0% |
| CAR | 46.2% | 76.7% | 0.0% | 28.2% |
| LIRS | 44.9% | 76.7% | 82.2% | 25.6% |

ARC resists the scan but, like LRU, gets no hits on the loop. These numbers come from small synthetic traces and say nothing about real workloads.

## Pitfalls

- **Moving $p$ after REPLACE.** In ARC the update of $p$ comes before REPLACE, and REPLACE uses the new value. In CAR the order is the other way round. Mixing the two gives a different policy.
- **Integer division.** The step $|B_2| / |B_1|$ is a ratio. If you use integer division, $p$ moves in coarser steps. The test file keeps $p$ as an exact fraction.
- **Forgetting the tie rule.** The test $x \in B_2$ and $|T_1| = p$ on line L27 is part of the policy. Without it, a hit in $B_2$ can evict from $T_2$, the side that just asked for room.
- **The case $|T_1| = c$.** In Case IV(A), when $T_1$ fills the whole cache, the LRU page of $T_1$ is deleted with no ghost (line L19). Putting it in $B_1$ would break $|T_1| + |B_1| \le c$.
- **The patent.** IBM held a patent on ARC. PostgreSQL used ARC in version 8.0 and replaced it in later versions for this reason. Check the legal state before you ship it.

## Implementations

## History

Nimrod Megiddo and Dharmendra S. Modha of IBM Almaden Research Center presented ARC at the USENIX FAST conference in 2003. They first defined DBL($2c$), a policy that keeps two LRU lists over $2c$ pages, and a class of policies that cache $c$ of those pages. ARC is the member of that class that moves the boundary by learning. A paper in IEEE Computer in 2004 gave a shorter account. IBM held a patent on ARC. Sorav Bansal and Modha gave the clock form [CAR](/car/) in 2004. ZFS adopted a changed ARC as its main memory cache.

## References
