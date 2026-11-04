---
tag: PAB348
kind: algorithm
slug: external-samplesort
name: External samplesort
aliases:
- external sample sort
- external distribution sort
area: sorting/external-sorting
level: advanced
summary: Pick splitters from a sample, partition records into buckets in one pass, and sort each bucket recursively.
solves: [sorting-problem]
model: external-memory-model
complexity:
  vars: {N: the number of items, M: the number of items that fit in memory, B: the number of items in a disk block, n: the number of blocks N/B, m: the number of blocks M/B}
  time: {worst: O(N^2), average: O(N log N), best: O(N log N)}
  space: {extra: Θ(N)}
  io:
    worst: "O(n N)"
    average: "O(n log_m n)"
    best: "O(n)"
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: false, comparison: true, recursive: true}
prereqs: [external-merge-sort, sample-sort, external-memory-model]
see_also: [disk-striping, balance-sort, external-sorting-io-lower-bound, bucket-sort, chernoff-bound, k-way-merge]
sources:
  - paper: doi:10.1561/0400000014
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4), 2008
    locator: Section 5.1, Sorting by Distribution (Section 5.1.1 on the choice of the S - 1 partitioning elements by random sampling, and Section 5.1.2 on load balancing across the disks)
  - paper: doi:10.1145/48529.48535
    title: Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9), 1988, pages 1116 to 1127
    locator: the distribution sort that meets the sorting bound
  - paper: "Jeffrey Scott Vitter and David A. Hutchinson, Distribution sort with randomized cycling, Journal of the ACM 53(4), 2006"
    locator: pp. 656 to 680, the randomized cycling distribution sort for D disks
---

External samplesort is the distribution counterpart of the [external merge sort](/external-merge-sort/). It draws a random sample of the file, picks $S - 1$ *splitters* from the sorted sample, reads the file once and writes each item to the bucket between two splitters, then sorts each bucket in the same way until it fits in memory. The buckets are in order, so their concatenation is the sorted file. With $S$ about $M/(2B)$, it does $O\big(\frac NB \log_{M/B} \frac NB\big)$ block transfers on average, like the merge sort, but it does the hard work before the recursion instead of after it.

## In plain words

You must sort a large heap of exam papers by name, and your desk holds only a few hundred. First pick some papers at random and look at the names on them. From these, choose a few dividing names, for example "F", "L" and "R", so that the parts between them are about the same size. Then go through the whole heap once and put each paper on one of the piles: before "F", from "F" to "L", and so on.

Now each pile is smaller. If a pile fits on the desk, sort it there. If it does not, do the same again with that pile. At the end, put the piles one after the other. Because the piles were in order, the whole heap is now in order.

## The problem

The input is a file $F$ of $N$ items with a total order, in blocks of $B$ items on a disk, and a memory of $M \ge 4B$ items. The output is a file with the same items in non-decreasing order. This is the [sorting problem](/sorting-problem/) in the [external memory model](/external-memory-model/).

## The algorithm

```pseudo id=main
EXTERNAL-SAMPLESORT(F, M, B)            ▷ F has N items on disk, M ≥ 4B
L1  if N ≤ M then read F, sort it in memory with a stable sort, write it, and return
L2  S ← max(2, min(M/(2B), ⌈4N/M⌉)); a ← ⌈8 ln S⌉
L3  draw aS positions of F at random, with replacement, and read the items at these positions
L4  sort the sample; the splitters s₁ < ⋯ < s_k are the distinct values at the ranks a, 2a, …, (S − 1)a
L5  read F block by block, and put each item x in a bucket: E_j if x = s_j, else U_j for s_j < x < s_{j+1}
L6  for j ← 0 to k do
L7      U_j ← EXTERNAL-SAMPLESORT(U_j, M, B)
L8  return U₀, E₁, U₁, E₂, …, E_k, U_k, one after the other
```

Line L5 is the distribution pass. Memory holds one input block and one output block for each of the at most $2S - 1$ buckets, which is at most $M$ items because $S \le M/(2B)$. When the output block of a bucket is full, the pass writes it to the end of that bucket on disk. Lines L6 and L7 sort the open buckets $U_j$. The buckets $E_j$ need no sort: all their items are equal to $s_j$. They also make sure that the recursion ends when many keys are equal, because every splitter goes to an $E_j$, so each $U_j$ is smaller than $F$. In line L2, the term $\lceil 4N/M \rceil$ makes the buckets of the next level fit in memory with high probability, and the term $M/(2B)$ is the largest number that the buffers allow. The factor $a$ is the *oversampling*: more sample items for each splitter make the buckets more even.

## Example

Sort $F = (14, 3, 9, 3, 17, 6, 12, 3, 20, 1, 8, 15, 3, 11, 5, 18, 7, 3, 16, 10)$, so $N = 20$, with $M = 12$ and $B = 2$. Line L2 gives $S = \min(3, 7) = 3$. To keep the example small we take $a = 2$, so the sample has 6 items. Say that line L3 draws the positions 0, 1, 6, 10, 12 and 15, which hold 14, 3, 12, 8, 3 and 18. The sorted sample is $(3, 3, 8, 12, 14, 18)$, and the items of ranks 2 and 4 give the splitters $s_1 = 3$ and $s_2 = 12$.

| bucket | items, in the order of $F$ | blocks written | then |
|---|---|---|---|
| $U_0$: less than 3 | 1 | 1 | sorted in memory |
| $E_1$: equal to 3 | 3, 3, 3, 3, 3 | 3 | no sort |
| $U_1$: from 3 to 12, exclusive | 9, 6, 8, 11, 5, 7, 10 | 4 | sorted in memory |
| $E_2$: equal to 12 | 12 | 1 | no sort |
| $U_2$: greater than 12 | 14, 17, 20, 15, 18, 16 | 3 | sorted in memory |

The sample touches 5 distinct blocks. The distribution pass reads 10 blocks and writes 12, one more than $\lceil 20/2 \rceil$ because each bucket can end in a partial block. The three open buckets fit in memory, and line L1 reads and writes them: $2 + 8 + 6 = 16$ I/Os. The total is $5 + 10 + 12 + 16 = 43$ I/Os. The five equal keys 3 are never compared again.

## Correctness

The buckets split $F$ by key: every item of $U_{j-1}$ is less than $s_j$, every item of $E_j$ equals $s_j$, and every item of $U_j$ is greater. So the sorted file is the sorted $U_0$, then $E_1$, then the sorted $U_1$, and so on, which is what line L8 returns. Each $U_j$ is smaller than $F$, because the splitter $s_1$ is an item of $F$ that goes to $E_1$, so the recursion ends. The distribution pass keeps the order of $F$ inside each bucket, and line L1 uses a stable sort, so the whole sort is stable. The full proof, with the bound on the size of the buckets, is in [the proof page](proofs/correctness.md).

## Complexity

- **Bucket sizes.** With $a \ge 8 \ln S$, every open bucket has fewer than $4N/S + 2$ items with probability at least $1 - 1/(2S)$. The proof cuts the sorted file into chunks of about $2N/S$ items: a larger bucket must contain a whole chunk with at most $a$ sample items, while the expected number is at least $2a$, and a [Chernoff bound](/chernoff-bound/) makes this unlikely.
- **One level.** A distribution pass reads $n$ blocks and writes at most $n + 2S - 1$. The sample costs at most $\min(aS, n)$ reads. So a level of the recursion costs at most about $3n$ I/Os in total over its calls, and about $2n$ when the sample is small compared with the file.
- **Levels.** With high probability each level divides the size of the buckets by about $S/4$, where $S$ is up to $m/2$. So there are about $\log_{m/8}(N/M) + 1$ levels, and the expected cost is $O(n \log_m n)$, which meets the [I/O lower bound for sorting](/external-sorting-io-lower-bound/).
- **Measured.** For $N = 10^6$ random keys, $M = 8192$ and $B = 64$, one run of the implementation made 103955 I/Os, $6.65n$, where the external merge sort made $62500$, $4n$. For $M = 65536$ and $B = 256$, the numbers were 17395 ($4.45n$) and 15628 ($4.0n$). The merge sort merges up to $m - 1$ runs at once, but the distribution has only $m/2$ buffers and some slack in the bucket sizes.
- **Worst case.** Bad samples can make a bucket almost as large as its parent. Each level still costs $O(n)$, and the depth is at most $N$, so the worst case is $O(nN)$ I/Os. It has a very small probability.
- **Time in memory.** $O(N \log S)$ per level for the binary searches of line L5, and $O(N \log N)$ in expectation in total.

## Properties

- **Stable.** The distribution keeps the order of $F$ inside each bucket, and line L1 uses a stable sort.
- **Randomized.** The sample depends on random choices. The output does not, only the cost.
- **Not in place.** The buckets need disk space for a copy of the file at each level.
- **Good with many equal keys.** The equal buckets $E_j$ take out the most frequent keys without further work.

## Variants and improvements

- **Deterministic splitters.** Vitter's Section 5.1.1 explains that the best number of buckets is $S = \Theta(\min\{m, n/m\})$, and that deterministic methods find $S = \Theta(\min\{\sqrt m, n/m\})$ splitters with buckets of nearly equal size. This doubles the number of levels, but keeps the bound in the worst case.
- **Parallel disks.** With $D$ disks, the blocks of each bucket must be spread so that each parallel I/O writes or reads blocks on different disks. Randomized cycling, by Vitter and Hutchinson, writes the blocks of each bucket to the disks in a random cyclic order chosen for that bucket, and meets the bound for $D$ disks. [Balance sort](/balance-sort/) does the same deterministically. Simple [disk striping](/disk-striping/) also works, but with fewer buckets.
- **A cheaper sample.** Vitter's Section 5.1.1 takes $S = O(\min\{m, n/m\})$, which is $O(\sqrt n)$, so the sample of $O(S \log S)$ items costs $o(n)$ I/Os, even when it is read one item per I/O. The constant 8 of line L2 is for a clean proof; implementations use a smaller oversampling factor.
- **In memory.** The same method in internal memory is [samplesort](/sample-sort/), a generalization of quicksort to many pivots.

## When to use it

Use an external distribution sort when the buckets are useful by themselves: for a parallel sort, in which each processor or disk takes some buckets, for a hash or range partition in a database, or when many keys are equal. On one disk, an [external merge sort](/external-merge-sort/) is simpler, deterministic, and often needs a little less I/O. For $D$ independent disks, distribution with randomized cycling is one of the simplest sorts that meets the optimal bound.

## Pitfalls

- **No buckets for equal keys.** If line L5 puts the items equal to $s_j$ into $U_j$, a file with one key repeated $N$ times gives one bucket of $N$ items, and the recursion never ends.
- **Too many buckets for the buffers.** Line L2 must keep $2S - 1$ output blocks and an input block in memory. With $S = M/B$ the distribution pass overflows memory.
- **A sample that is too small.** With $a = 1$, the buckets vary a lot, and many of them are too large for memory. The oversampling of line L2 is what gives the high probability bound.
- **A sample that is not random.** If line L3 takes the first $aS$ items, a sorted or nearly sorted input gives splitters from a small range of keys, and one bucket gets almost all items.
- **Forgetting partial blocks.** Each bucket can end in a partial block. With many buckets and small files, these extra writes matter; line L2 keeps $S$ small for small files.

## Implementations

## History

Distribution sorts on disk are as old as sorting on punched cards, which split the cards by one digit at a time. Aggarwal and Vitter gave in 1988 a distribution sort that meets the sorting bound in the external memory model. The random sample with oversampling is the method of samplesort in internal memory. Vitter's survey gives the external distribution sort in Section 5.1, with the choice of the number of buckets in Section 5.1.1. Vitter and Hutchinson published distribution sort with randomized cycling, for parallel disks, in 2006.

## References
