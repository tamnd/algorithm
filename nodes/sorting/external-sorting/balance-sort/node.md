---
tag: A6ZN06
kind: algorithm
slug: balance-sort
name: Balance Sort
aliases:
- Nodine-Vitter Balance Sort
- BalanceSort
area: sorting/external-sorting
level: research
summary: An optimal external sort for the parallel disk model that keeps records balanced across disks while distributing them.
solves: [sorting-problem]
model: external-memory-model
complexity:
  vars: {N: the number of items, M: the number of items that fit in memory, B: the number of items in a disk block, D: the number of disks, n: the number of blocks N/B, m: the number of blocks M/B}
  time: {worst: O(N log N), average: O(N log N), best: O(N log N)}
  space: {extra: Θ(N)}
  io:
    worst: "O((n/D) log_m n)"
    average: "O((n/D) log_m n)"
    best: "O((n/D) log_m n)"
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: true}
prereqs: [external-samplesort, disk-striping, external-memory-model]
see_also: [external-sorting-io-lower-bound, external-merge-sort, bipartite-matching, balls-into-bins, sample-sort, bucket-sort]
sources:
  - paper: "Mark H. Nodine and Jeffrey Scott Vitter, Deterministic distribution sort in shared and distributed memory multiprocessors, Proceedings of the 5th ACM Symposium on Parallel Algorithms and Architectures (SPAA 1993)"
    locator: pp. 120 to 129, the Balance Sort algorithm and its balancing invariant
  - paper: doi:10.1561/0400000014
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4), 2008
    locator: Section 5.1.2, Load Balancing Across the Disks (the invariant on num_b(d), the matching, and the comparison with the randomized methods of Vitter and Shriver)
  - paper: doi:10.1007/BF01185207
    title: Jeffrey Scott Vitter and Elizabeth A. M. Shriver, Algorithms for parallel memory I, Two-level memories, Algorithmica 12(2-3), 1994, pages 110 to 147
    locator: the parallel disk model, the sorting bound for D disks, and the randomized distribution sort that Balance Sort makes deterministic
---

Balance Sort is a deterministic distribution sort for $D$ independent disks, by Nodine and Vitter. Like the [external samplesort](/external-samplesort/), it splits the file into buckets with splitters and sorts each bucket recursively. Its new part is the output: each parallel write sends blocks of several buckets to different disks, and the choice of disk keeps every bucket balanced across the disks, so that the next level can read each bucket with almost full parallelism. It meets the sorting bound $\Theta\big(\frac{N}{DB} \log_{M/B} \frac NB\big)$ of the parallel disk model, which [disk striping](/disk-striping/) does not.

## In plain words

You sort a big file with the help of several disks. Each disk can read or write one block at the same time as the others. A distribution sort cuts the file into piles by key. If all blocks of one pile land on the same disk, the next step must read that pile from one disk only, and the other disks wait.

Balance Sort keeps a count, for each pile, of how many of its blocks are on each disk. When it writes a row of blocks, one block per disk, it gives each block a disk that has few blocks of its pile. A block waits for the next row if no good disk is free. Each pile is then spread almost evenly, and the next step can read it with all disks at once.

## The problem

The input is a file $F$ of $N$ items with a total order, in blocks of $B$ items, spread over $D$ disks. One parallel I/O reads or writes at most one block on each disk. Memory holds $M \ge (2D + 4)B$ items. The output is the items in non-decreasing order. This is the [sorting problem](/sorting-problem/) in the parallel disk model of Vitter and Shriver, the [external memory model](/external-memory-model/) with $D$ disks.

## The algorithm

For a bucket $b$, let $X_b$ be the number of its blocks written so far, and $X_b(d)$ the number of them on disk $d$. A disk $d$ is *allowed* for the next block of $b$ if $X_b(d) + 1 \le 2\lceil (X_b + 1)/D \rceil$. The *invariant* is that $X_b(d) \le 2 \lceil X_b / D \rceil$ for every bucket and every disk.

```pseudo id=main
BALANCE-SORT(F, M, B, D)                ▷ F has N items on D disks, M ≥ (2D + 4)B
L1  if N ≤ M then read F, sort it in memory, write it striped, and return
L2  S ← max(2, min(M/B − 2D, ⌈4N/M⌉))
L3  choose the splitters s₁ < ⋯ < s_k, k ≤ S − 1, by deterministic sampling
L4  for each bucket b, set X_b and all X_b(d) to 0
L5  for each parallel read of F, one block from each disk, do
L6      put each item x in the output block of the bucket j with s_j ≤ x < s_{j+1}; a full block is ready
L7      while at least D blocks are ready: one parallel write; for each ready block of bucket b in turn, take the allowed and unused disk with the fewest blocks of b
L8      write each placed block, and update X_b and X_b(d); the blocks with no such disk wait
L9  write the last partial blocks in the same way, then sort each bucket with BALANCE-SORT
```

The items carry their input position, which breaks ties, so all items differ and the sort is stable. Line L3 reads $F$ one memoryload at a time, sorts each load in memory, keeps every $q$-th item with $q = \max(2, \lceil M/(4S) \rceil)$, sorts this sample (recursively if it does not fit in memory), and takes the splitters at the ranks $r, 2r, \ldots$ of the sample, with $r = \max(2, \lfloor \text{sample size}/S \rfloor)$. Each bucket then has at most $(r + L)q$ items for $L$ memoryloads. Lines L7 and L8 are the balancing. A write step continues while it has free disks, and takes the ready blocks in the order in which they became ready.

## Example

Sort $F = (19, 8, 9, 2, 16, 12, 4, 1, 15, 14, 5, 6, 17, 13, 11, 3, 18, 10, 7, 20)$ on $D = 4$ disks with $B = 1$, so that each item is a block, and $M = 12$. The file is striped: disk 0 holds 19, 16, 15, 17, 18, and so on. Line L2 gives $S = \min(12 - 8, 7) = 4$, and line L3 with $q = 2$ takes every second item of the sorted loads $(1, 2, 4, 5, 6, 8, 9, 12, 14, 15, 16, 19)$ and $(3, 7, 10, 11, 13, 17, 18, 20)$. The sorted sample is $(2, 5, 7, 8, 11, 12, 15, 17, 19, 20)$, and the ranks 2, 4, 6 give the splitters 5, 8 and 12. So the buckets are $b_0$: below 5, $b_1$: 5 to 7, $b_2$: 8 to 11, and $b_3$: 12 and above.

| write | ready blocks, in order (bucket) | disks chosen | waits |
|---|---|---|---|
| 1 | 19 ($b_3$), 8 ($b_2$), 9 ($b_2$), 2 ($b_0$) | 0, 1, 2, 3 | |
| 2 | 16 ($b_3$), 12 ($b_3$), 4 ($b_0$), 1 ($b_0$) | 1, 2, 0, 3 | |
| 3 | 15 ($b_3$), 14 ($b_3$), 5 ($b_1$), 6 ($b_1$) | 3, 0, 1, 2 | |
| 4 | 17 ($b_3$), 13 ($b_3$), 11 ($b_2$), 3 ($b_0$) | 1, 2, 0, none | 3 |
| 5 | 3 ($b_0$), 18 ($b_3$), 10 ($b_2$), 7 ($b_1$), 20 ($b_3$) | 1, 3, 0, 2 | 20 |
| 6 | 20 ($b_3$) | 0 | |

In write 4, the only free disk is 3, which already holds 2 and 1 of $b_0$. With $X_{b_0} = 3$, the limit is $2\lceil 4/4 \rceil = 2$, so block 3 waits, and write 5 puts it on disk 1. At the end, $b_0 = \{1, 2, 3, 4\}$ has the counts $(1, 1, 0, 2)$ on the four disks, and $b_3$ has 9 blocks with the counts $(3, 2, 2, 2)$. All four buckets fit in memory. The sort makes 5 reads for the sample, 5 reads and 6 writes for the distribution, and 9 reads and 6 writes for the buckets: 31 parallel I/Os in total.

## Correctness

Lines L6 and L9 put each item in exactly one bucket, and the buckets are in the order of the splitters, so the concatenation of the sorted buckets is the sorted file. The sample has an item smaller than $s_1$, which goes to the first bucket, and every other bucket misses this item, while the first bucket misses $s_1$. So each bucket is smaller than $F$ and the recursion ends. For the balance, more than half of the disks are allowed for each block, so a write step places at least $\min(\text{ready}, \lfloor D/2 \rfloor + 1)$ blocks, and the invariant holds after each placement. The full proofs are in [the proof page](proofs/correctness.md).

## Complexity

- **Balance.** By the invariant, a bucket of $X$ blocks has at most $2\lceil X/D \rceil$ blocks on any disk, so the next level reads it in at most $2\lceil X/D \rceil$ parallel reads, at most about twice the ideal.
- **Writes.** Each write step of line L7 writes at least $\lfloor D/2 \rfloor + 1$ blocks, so a level writes its $n + O(S)$ blocks in at most about $2n/D$ parallel writes.
- **One level.** The sample and the distribution each read the file once, in at most $2\lceil n/D \rceil$ steps, and the sample is a fraction $1/q$ of the file. So a level costs $O(n/D)$ parallel I/Os.
- **Levels.** Each level divides the bucket size by $\Theta(S)$, with $S = \Theta(m)$ when $m \ge 4D$, so there are $O(\log_m n)$ levels and the cost is $O\big(\frac nD \log_m n\big)$. This meets the bound of the [I/O lower bound for sorting](/external-sorting-io-lower-bound/) for $D$ disks. With $m < 4D$ the number of buckets is limited by the term $2D$ of line L2.
- **Measured.** For $N = 10^5$ random keys, $M = 2048$, $B = 16$ and $D = 8$, the implementation made $5030$ parallel I/Os, $6.44\, n/D$. The write steps held $7.99$ blocks on average, nearly full, and no bucket needed more than $1.5$ times the ideal number of reads. With $D = 16$ the cost was $6.51\, n/D$.
- **Time in memory.** $O(N \log S)$ per level for the binary searches of line L6 and $O(D)$ per placed block for line L7. Nodine and Vitter use a faster matching step, see below.

## Properties

- **Deterministic.** No step uses random choices. The cost bound holds in the worst case.
- **Stable.** The ties are broken by the input position, which the sort carries with each item.
- **Not in place.** Each level writes the buckets as a new copy of the file.
- **Full stripes.** Each write step can fill a whole stripe, so parity for error recovery can be written per stripe, as Vitter notes.

## Variants and improvements

- **Matching.** Nodine and Vitter do not place blocks one at a time. They view a write step as a matching problem between ready blocks and disks, and with [bipartite matching](/bipartite-matching/) techniques they write at least half of a memoryload per step and keep a stronger invariant: the $D/2$ largest counts $X_b(d)$ of each bucket differ by at most 1. The greedy rule of line L7 is a simpler form of the same idea, with the weaker factor 2 bound.
- **Randomized balancing.** Vitter and Shriver write each stripe in a random order of the disks, which spreads the buckets well when they have $\Omega(D \log D)$ blocks, like [balls into bins](/balls-into-bins/), and use a second random method for smaller buckets. Randomized cycling, by Vitter and Hutchinson, is simpler and has better constants; the [external samplesort](/external-samplesort/) page describes it.
- **Greed Sort.** Nodine and Vitter also gave Greed Sort, a deterministic merge sort that is optimal for $D$ disks.
- **Disk striping.** [Disk striping](/disk-striping/) is simpler but loses a factor of up to $\log m / \log(m/D)$ in the number of levels.

## When to use it

Use a balanced distribution when a sort must be optimal on many independent disks and must have a worst-case bound, for example in a system that cannot accept a rare slow run. When a high-probability bound is enough, randomized cycling is simpler and has smaller constants. With one disk, or when $D$ is small against $M/B$, a striped [external merge sort](/external-merge-sort/) is simpler and is within a small factor of optimal.

## Pitfalls

- **Balance only at the end.** Line L7 must check the limit at each placement. A rule that balances only the total of each bucket at the end of the pass cannot undo the blocks already written.
- **Two blocks on one disk.** A write step must use each disk at most once. Line L7 must mark the disks it has used and skip them.
- **Too many buckets.** Line L2 must leave memory for up to $2D$ ready blocks besides the $S$ output blocks. With $S = M/B$ the ready blocks of line L7 overflow memory.
- **Equal keys.** Without the position of each item, line L6 puts all copies of one key in one bucket, and a file of equal keys never gets smaller. The position makes all items differ.
- **Splitters at rank 1.** Line L3 must take ranks of at least 2. If the smallest sample item is a splitter, the first bucket can be empty and another bucket can hold all of $F$.

## Implementations

## History

Aggarwal and Vitter proved the sorting bound in 1988 for a model in which the $D$ blocks of one I/O can come from anywhere. Vitter and Shriver defined the more realistic parallel disk model, with one block per disk per I/O, and gave randomized distribution sorts that meet the bound in it. Nodine and Vitter gave the first deterministic optimal sorts for this model: Balance Sort, presented at SPAA 1993, and Greed Sort, published in the Journal of the ACM in 1995. Balance Sort also runs on shared and distributed memory multiprocessors, as the title of its paper says. Vitter's survey describes it in Section 5.1.2.

## References
